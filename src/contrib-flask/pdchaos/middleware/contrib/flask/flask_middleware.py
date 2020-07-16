import uuid

from flask import request, Flask
from logzero import logger

from pdchaos.middleware.core.main import attack, register


def _load_from_config(app: Flask, key: str):
    result = app.config.get(key, '')

    if not result:
        logger.warning("'{}' has not been set. The chaos middleware may not work as expected.".format(key))

    return result


def _load_context(app: Flask) -> dict:
    result = {
        'SERVICE_ENV': _load_from_config(app, 'CHAOS_MIDDLEWARE_SERVICE_ENVIRONMENT'),
        'SERVICE_ID': str(uuid.uuid4()),
        'SERVICE_NAME': _load_from_config(app, 'CHAOS_MIDDLEWARE_SERVICE_NAME'),
        'API_TOKEN': _load_from_config(app, 'CHAOS_MIDDLEWARE_API_TOKEN'),
    }
    return result


def _after_request(response):
    """Runs after each request.
    See: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.after_request
    """

    attack(request.path, request.headers)

    return response


class FlaskMiddleware(object):

    def __init__(self, app=None):
        self.app = app

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        self.app.after_request(_after_request)
        context = _load_context(app)
        register(context)
