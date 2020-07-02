from flask import request

from pdchaos.middleware.core.main import execute_chaos


class FlaskMiddleware(object):

    def __init__(self, app=None, blocked_paths=None, injections=None):
        self.app = app
        self.blocked_paths = blocked_paths
        self.injections = injections

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.after_request(self._after_request)

    def _after_request(self, response):
        """Runs after each request.
        See: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.after_request
        """

        execute_chaos(request.path, self.blocked_paths, request.headers, self.injections)

        return response
