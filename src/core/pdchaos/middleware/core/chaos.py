import re
from typing import Dict, List

from logzero import logger
from pdchaos.middleware import core
from pdchaos.middleware.core import config, dice, inject, loader, parse

# Application configuration
from pdchaos.middleware.core.inject import ChaosMiddlewareError

loaded_app_config = None

# List of attack actions that are intended for this target (running application)
loaded_attack_actions = []


def register(app_config: config.AppConfig):
    """Register an application"""
    if app_config is None:
        raise Exception('Application config is not set')
    global loaded_app_config
    loaded_app_config = app_config
    _init_attack_loader()


def attack(attack_input: Dict = {}, attack_ctx: Dict = {}):
    """Execute chaos"""

    try:
        # Validate attack schema
        attack = parse.attack(attack_input)

        # Attack from request header: from client
        if attack:
            _execute_attacks(
                target=attack.get(core.ATTACK_KEY_TARGET),
                attack_actions=attack.get(core.ATTACK_KEY_ACTIONS),
                attack_ctx=attack_ctx)

        # Attack from attack configuration: from Chaos API
        elif loaded_attack_actions and len(loaded_attack_actions) > 0:
            _execute_attacks(
                attack_actions=loaded_attack_actions,
                attack_ctx=attack_ctx)

    except ChaosMiddlewareError as error:
        if error.__cause__:
            raise error.__cause__
        else:
            raise error

    except Exception as ex:
        logger.error("Unable to perform chaos attack. Error: %s", ex, stack_info=True)


def _set_attack_action(attack_action: List[Dict]):
    # Validate
    parsed_attack_actions = parse.attack_actions(attack_action)

    # Configure
    global loaded_attack_actions
    loaded_attack_actions = parsed_attack_actions
    logger.debug("Current attack actions: {}".format(loaded_attack_actions))


def _init_attack_loader():
    attack_loader = loader.get(loaded_app_config)
    if attack_loader:
        attack_loader.load(_set_attack_action)


def _execute_attacks(target=None, attack_actions=None, attack_ctx={}):
    for action in attack_actions:

        if not _is_app_targeted(target):
            continue

        if not _is_route_targeted(action.get(core.ATTACK_KEY_ROUTE), attack_ctx.get(core.ATTACK_KEY_ROUTE)):
            continue

        if not _is_lucky_to_be_attacked(action.get(core.ATTACK_KEY_PROBABILITY)):
            continue

        if action[core.ATTACK_KEY_ACTION_NAME] == core.ATTACK_ACTION_DELAY:
            inject.delay(action[core.ATTACK_KEY_VALUE])

        if action[core.ATTACK_KEY_ACTION_NAME] == core.ATTACK_ACTION_FAULT:
            inject.failure(action[core.ATTACK_KEY_VALUE])


def _is_lucky_to_be_attacked(probability):
    is_lucky = dice.roll(probability)

    return is_lucky


def _is_route_targeted(attack_ctx_route, action_route):
    if not action_route or not attack_ctx_route:
        return True

    text = action_route.replace("/*", "/[\\w-]*")
    is_route_targeted = re.search(text, attack_ctx_route)

    return is_route_targeted


def _is_app_targeted(target):
    if not target:
        return True

    application = target.get(core.ATTACK_KEY_TARGET_APPLICATION)
    is_app_targeted = \
        (application and application == loaded_app_config.get(config.AppConfig.APPLICATION_NAME)) \
        or not application

    return is_app_targeted
