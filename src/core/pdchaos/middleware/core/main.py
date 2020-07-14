import contextvars
import os

import yaml
from logzero import logger
from pdchaos.middleware.core import HEADER_ATTACK, model, inject, dice

loaded_config = contextvars.ContextVar('loaded_config', default=None)


def load_config():
    settings_path = "chaos-config.yml"

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


def execute(called_path: str, called_method: str, requested_headers: dict):
    """Execute chaos"""
    # Server side configuration
    if load_config() and loaded_config.get():
        paths = model.parse_paths(loaded_config.get())
        for path in paths['paths']:
            if _is_attack_applicable(called_path, called_method, path):
                _execute_attacks(path['attacks'])

    # Client side configuration
    elif requested_headers:
        if HEADER_ATTACK in requested_headers:
            attacks = model.parse_attack(requested_headers.get(HEADER_ATTACK))
            _execute_attacks(attacks)


def _is_attack_applicable(called_path, called_method, path):
    response = True

    if called_path != path['path']:
        response = False

    if path.get('methods') and called_method not in path.get('methods'):
        response = False

    return response


def _execute_attacks(attacks):
    for attack in attacks:
        to_be_attacked = dice.roll(attack.get('probability'))

        if not to_be_attacked:
            continue

        if attack['type'] == 'delay':
            inject.delay(attack['value'])

        if attack['type'] == 'failure':
            inject.failure(attack['value'])
