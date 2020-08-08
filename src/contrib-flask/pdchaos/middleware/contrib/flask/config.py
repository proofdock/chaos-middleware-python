import uuid

from flask import Flask
from logzero import logger
from pdchaos.middleware.core.config import AppConfig


class FlaskConfig(AppConfig):

    def __init__(self, app: Flask):
        self._app = app
        self._app.config.setdefault(AppConfig.APPLICATION_ID, str(uuid.uuid4()))

    def _load_from_config(self, key: str, default) -> str:
        result = self._app.config.get(key, default)

        if not result:
            logger.warning("'{}' has not been set. The chaos middleware may not work as expected.".format(key))

        return result

    def get(self, item: str, default=None) -> str:
        return self._load_from_config(item, default)
