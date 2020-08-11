from abc import ABCMeta, abstractmethod
from typing import Callable, Dict

from logzero import logger
from pdchaos.middleware.core.config import AppConfig


class AttackLoader(metaclass=ABCMeta):
    """
    This class is a base class for implementing different type of attack config loaders.

    For example, different loaders implementation can load an attack configuration from a file, network or other source.
    The loading mechanism depends on the configured settings.
    """

    @abstractmethod
    def load(set_attacks_action_func: Callable[[Dict], None]):
        """ Load function. Call callback function to set new attack actions.  """
        pass


def get(app_config: AppConfig) -> AttackLoader:
    """Load the attack configuration from the API provider"""
    provider = app_config.get(AppConfig.ATTACK_LOADER, "proofdock")

    if provider == "proofdock":
        from pdchaos.middleware.core.proofdock.loader import ProofdockAttackLoader
        return ProofdockAttackLoader(app_config)
    else:
        logger.warning(
            "Unable to find an attack loader provider '{}'. "
            "Please set a valid CHAOS_MIDDLEWARE_ATTACK_LOADER, e.g. 'proofdock'".format(provider))
        return None
