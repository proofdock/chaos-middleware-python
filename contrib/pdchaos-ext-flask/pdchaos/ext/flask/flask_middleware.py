import flask

from pdchaos import url, inject


class FlaskMiddleware(object):

    def __init__(self, app=None, blocked_urls=None, injections=None):
        self.app = app
        self.blocked_urls = blocked_urls
        self.injections = injections

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        # load settings from app config
        settings = self.app.config.get('proofdock', {})
        self.blocked_urls = settings.get('blocked_urls', {})
        self.injections = settings.get('injections', {})

        self.setup_middleware()

    def setup_middleware(self):
        self.app.after_request(self._after_request)

    def _after_request(self, response):
        """Runs after each request.
        See: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.after_request
        """

        # Skip injections if the url is blocked
        if url.is_blocked(flask.request.url, self.blocked_urls):
            return response

        if self.injections and self.injections.get('delay', {}):
            inject.delay(self.injections.get('delay').get('duration'))

        return response
