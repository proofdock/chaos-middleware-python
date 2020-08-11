from typing import Dict, List

from logzero import logger
from pdchaos.middleware import core
from pdchaos.middleware.core import config, dice, inject, loader, parse

# Application configuration
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
    # validate attack schema
    attack = parse.attack(attack_input)

    # Attack was passed directly
    if attack:
        _execute_attacks(
            target=attack.get(core.ATTACK_KEY_TARGET),
            attack_actions=attack.get(core.ATTACK_KEY_ACTIONS),
            attack_ctx=attack_ctx)
    # Check if there are any attack already loaded for this target
    elif loaded_attack_actions and len(loaded_attack_actions) > 0:
        _execute_attacks(
            attack_actions=loaded_attack_actions,
            attack_ctx=attack_ctx)


def _set_attack_action(attack_action: List[Dict]):
    try:
        # Validate
        parsed_attack_actions = parse.attack_actions(attack_action)
        # Configure
        global loaded_attack_actions
        loaded_attack_actions = parsed_attack_actions
        logger.debug("Current attack actions: {}".format(loaded_attack_actions))
    except Exception as e:
        logger.warning("Unable to set attack configuration. Reason: {}".format(e))


def _init_attack_loader():
    attack_loader = loader.get(loaded_app_config)
    if attack_loader:
        attack_loader.load(_set_attack_action)


def _execute_attacks(target=None, attack_actions=None, attack_ctx={}):
    for action in attack_actions:

        if not _is_app_targeted(target):
            continue

        _is_lucky_to_be_attacked = dice.roll(action.get(core.ATTACK_KEY_PROBABILITY))
        if not _is_lucky_to_be_attacked:
            continue

        # for now we assume that all actions (delay, fault) contain route
        route = action.get(core.ATTACK_KEY_TARGET_ROUTE)
        is_route_targeted = (route and route == attack_ctx.get(core.ATTACK_KEY_TARGET_ROUTE)) or not route
        if not is_route_targeted:
            continue

        if action[core.ATTACK_KEY_ACTION_NAME] == core.ATTACK_ACTION_DELAY:
            inject.delay(action[core.ATTACK_KEY_VALUE])

        if action[core.ATTACK_KEY_ACTION_NAME] == core.ATTACK_ACTION_FAULT:
            inject.failure(action[core.ATTACK_KEY_VALUE])


def _is_app_targeted(target):
    if not target:
        return True

    application = target.get(core.ATTACK_KEY_TARGET_APPLICATION)
    is_app_targeted = \
        (application and application == loaded_app_config.get(config.AppConfig.APPLICATION_NAME)) \
        or not application

    return is_app_targeted
