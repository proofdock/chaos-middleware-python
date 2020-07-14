from flask import request

from pdchaos.middleware.core.main import execute


class FlaskMiddleware(object):

    def __init__(self, app=None):
        self.app = app

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.after_request(self._after_request)

    def _after_request(self, response):
        """Runs after each request.
        See: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.after_request
        """

        execute(request.path, request.method, request.headers)

        return response
