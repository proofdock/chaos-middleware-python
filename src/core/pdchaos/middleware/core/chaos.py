from typing import Dict, List

from logzero import logger

from pdchaos.middleware import core
from pdchaos.middleware.core import config, loader, parse, executor
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
    if loaded_app_config is None:
        loaded_app_config = app_config
        loader.init(loaded_app_config, _set_attack_action)


def attack(attack_input: Dict = {}, attack_ctx: Dict = {}):
    """Execute chaos"""

    try:
        # Validate attack schema
        attack_schema = parse.attack(attack_input)

        # Attack from request header: from client
        if attack_schema:
            executor.execute(
                target=attack_schema.get(core.ATTACK_KEY_TARGET),
                attack_actions=attack_schema.get(core.ATTACK_KEY_ACTIONS),
                attack_ctx=attack_ctx)

        # Attack from attack configuration: from Chaos API
        elif loaded_attack_actions and len(loaded_attack_actions) > 0:
            executor.execute(
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
