import contextvars
import os

import yaml
from logzero import logger
from pdchaos.middleware.core import HEADER_ATTACK, inject, dice, parse

loaded_context = contextvars.ContextVar('loaded_context', default={})
loaded_config = contextvars.ContextVar('loaded_config', default=None)


def load_config():
    settings_path = "chaos-config.json"

    if loaded_config.get() is None:
        if os.path.exists(settings_path):
            with open(settings_path) as f:
                settings = yaml.safe_load(f.read())
                loaded_config.set(settings)
                logger.debug("Loaded Chaos config file from '{c}'.".format(c=settings_path))
                return True
        else:
            logger.debug("The Chaos config file could not be found at '{c}'.".format(c=settings_path))
            loaded_config.set(dict())
            return False

    else:
        return len(loaded_config.get()) != 0


def register(service_app_context: dict):
    """Register a service application"""
    loaded_context.set(service_app_context)


def attack(called_path: str, requested_headers: dict):
    """Execute chaos"""
    # Client side configuration
    if requested_headers and HEADER_ATTACK in requested_headers:
        attacks = parse.attack_as_str(requested_headers.get(HEADER_ATTACK))
        if attacks:
            _execute_attacks(attacks, called_path)

    # Server side configuration
    elif load_config() and loaded_config.get():
        attacks = parse.attack_as_dict(loaded_config.get())
        if attacks:
            _execute_attacks(attacks, called_path)


def _execute_attacks(attacks, called_path):
    for _attack in attacks:
        lucky_to_be_attacked = dice.roll(_attack.get('probability'))

        if not lucky_to_be_attacked:
            continue

        if not _targeted(_attack, called_path):
            continue

        if _attack['action'] == 'delay':
            inject.delay(_attack['value'])

        if _attack['action'] == 'fault':
            inject.failure(_attack['value'])


def _targeted(_attack, called_route):
    target = _attack.get('target')

    if not target:
        return True

    service = target.get('service')
    is_svc_targeted = (service and service == loaded_context.get().get('SERVICE_NAME')) or not service

    route = target.get('route')
    is_route_targeted = (route and route == called_route) or not route

    return is_svc_targeted and is_route_targeted
