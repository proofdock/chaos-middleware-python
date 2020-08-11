from abc import ABCMeta, abstractmethod


class AppConfig(metaclass=ABCMeta):

    APPLICATION_ENV = "CHAOS_MIDDLEWARE_APPLICATION_ENV"
    APPLICATION_ID = "CHAOS_MIDDLEWARE_APPLICATION_ID"
    APPLICATION_NAME = "CHAOS_MIDDLEWARE_APPLICATION_NAME"
    ATTACK_LOADER = "CHAOS_MIDDLEWARE_ATTACK_LOADER"

    # Proofdock specific settings
    PROOFDOCK_API_URL = "CHAOS_MIDDLEWARE_PROOFDOCK_API_URL"
    PROOFDOCK_API_TOKEN = "CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN"

    @abstractmethod
    def get(self, item: str, default=None) -> str:
        raise NotImplementedError("Function get is not implemented")
