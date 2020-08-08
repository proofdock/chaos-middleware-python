import contextvars
from typing import Dict

from logzero import logger
from pdchaos.middleware import core
from pdchaos.middleware.core import config, dice, inject, loader, parse

loaded_app_config = contextvars.ContextVar('loaded_app_config', default={})
loaded_attack_config = contextvars.ContextVar('loaded_attack_config', default=None)


def register(app_config: config.AppConfig):
    """Register an application"""
    loaded_app_config.set(app_config)
    _init_attack_loader()


def set_attack(attack: Dict):
    try:
        # Validate
        parsed_attack = parse.attack_as_dict(attack)
        # Configure
        loaded_attack_config.set(parsed_attack)
        logger.debug("New attack configuration: {}".format(attack))
    except Exception as e:
        logger.warning("Unable to set attack configuration. Reason: {}".format(e))


def _init_attack_loader():
    attack_loader = loader.get(loaded_app_config.get())
    attack_loader.load(set_attack)


def attack(called_path: str, requested_headers: dict):
    """Execute chaos"""
    # Client side configuration
    if requested_headers and core.HEADER_ATTACK in requested_headers:
        attacks = parse.attack_as_str(requested_headers.get(core.HEADER_ATTACK))
        if attacks:
            _execute_attacks(attacks, called_path)

    # Server side configuration
    elif loaded_attack_config.get():
        attacks = parse.attack_as_dict(loaded_attack_config.get())
        if attacks:
            _execute_attacks(attacks, called_path)


def _execute_attacks(attacks, called_path):
    for _attack in attacks:
        _is_lucky_to_be_attacked = dice.roll(_attack.get(core.ATTACK_KEY_PROBABILITY))

        if not _is_lucky_to_be_attacked:
            continue

        if not _is_aimed_for_attack(_attack, called_path):
            continue

        if _attack[core.ATTACK_KEY_ACTION] == core.ATTACK_ACTION_DELAY:
            inject.delay(_attack[core.ATTACK_KEY_VALUE])

        if _attack[core.ATTACK_KEY_ACTION] == core.ATTACK_ACTION_FAULT:
            inject.failure(_attack[core.ATTACK_KEY_VALUE])


def _is_aimed_for_attack(_attack, called_route):
    target = _attack.get(core.ATTACK_KEY_TARGET)

    if not target:
        return True

    service = target.get(core.ATTACK_KEY_TARGET_SERVICE)
    is_svc_targeted = \
        (service and service == loaded_app_config.get().get(config.AppConfig.APPLICATION_NAME)) \
        or not service

    route = target.get(core.ATTACK_KEY_TARGET_ROUTE)
    is_route_targeted = (route and route == called_route) or not route

    return is_svc_targeted and is_route_targeted
