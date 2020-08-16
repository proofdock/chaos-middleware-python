import json

from flask import Flask, request
from logzero import logger

from pdchaos.middleware.contrib.flask.config import FlaskConfig
from pdchaos.middleware.core import ATTACK_KEY_ROUTE, HEADER_ATTACK, chaos


def _after_request(response):
    """Runs after each request.
    See: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.after_request
    """
    attack = json.loads(request.headers.get(HEADER_ATTACK)) if (HEADER_ATTACK in request.headers) else None
    attack_ctx = {ATTACK_KEY_ROUTE: request.path}

    chaos.attack(attack, attack_ctx)
    return response


class FlaskMiddleware(object):

    def __init__(self, app=None):
        self.app = app

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        try:
            config = FlaskConfig(app)
            chaos.register(config)
            self.app.after_request(_after_request)
        except Exception as ex:
            logger.error("Unable to configure chaos middleware. Error: %s", ex, stack_info=True)
