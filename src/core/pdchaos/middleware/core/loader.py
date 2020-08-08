from abc import ABCMeta, abstractmethod
from typing import Callable, Dict

from logzero import logger
from pdchaos.middleware.core.config import AppConfig


class AttackLoader(metaclass=ABCMeta):
    """
    This class is a base class for implementing different type of attack config loaders.

    Example loader can load attack configuration from file, network or any other place. Loader can as well
    periodically pull for new configurations.
    """

    @abstractmethod
    def load(set_attack_func: Callable[[Dict], None]):
        """ Load function. Call callback function to set new attack.  """
        pass


def get(app_config: AppConfig) -> AttackLoader:
    """Load the attack configuration from the API provider"""
    provider = app_config.get(AppConfig.API_PROVIDER, "proofdock")

    if provider == "proofdock":
        from pdchaos.middleware.core.proofdock.loader import ProofdockAttackLoader
        return ProofdockAttackLoader(app_config)
    else:
        logger.warn(
            "Unable to find attack loader provider '{}'. "
            "Please sets  a valid CHAOS_MIDDLEWARE_API_PROVIDER, e.g. 'proofdock'".format(provider))
        return None