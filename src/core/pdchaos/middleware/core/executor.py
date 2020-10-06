import re

from pdchaos.middleware import core
from pdchaos.middleware.core import inject, dice, config, chaos


def execute(target=None, attack_actions=None, attack_ctx={}):
    for action in attack_actions:

        if not _is_app_targeted(target):
            continue

        if not _is_route_targeted(attack_ctx.get(core.ATTACK_KEY_ROUTE), action.get(core.ATTACK_KEY_ROUTE)):
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
    environment = target.get(core.ATTACK_KEY_TARGET_ENVIRONMENT)

    is_app_targeted = \
        (application and application == chaos.loaded_app_config.get(config.AppConfig.APPLICATION_NAME)) \
        or not application

    is_env_targeted = \
        (environment and environment == chaos.loaded_app_config.get(config.AppConfig.APPLICATION_ENV)) \
        or not environment

    return is_app_targeted and is_env_targeted
