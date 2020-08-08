from abc import ABCMeta, abstractmethod


class AppConfig(metaclass=ABCMeta):

    API_URL = "CHAOS_MIDDLEWARE_API_URL"
    API_PROVIDER = "CHAOS_MIDDLEWARE_API_PROVIDER"
    API_TOKEN = "CHAOS_MIDDLEWARE_API_TOKEN"
    APPLICATION_ENV = "CHAOS_MIDDLEWARE_APPLICATION_ENV"
    APPLICATION_ID = "CHAOS_MIDDLEWARE_APPLICATION_ID"
    APPLICATION_NAME = "CHAOS_MIDDLEWARE_APPLICATION_NAME"

    @abstractmethod
    def get(self, item: str, default=None) -> str:
        raise NotImplementedError("Function get is not implemented")
