from unittest import mock

import flask

from pdchaos.middleware.contrib.flask import flask_middleware


class FlaskTestException(Exception):
    pass


class TestFlaskMiddleware:

    @staticmethod
    def create_app():
        app = flask.Flask(__name__)

        @app.route('/')
        def index():
            return 'test flask trace'  # pragma: NO COVER

        @app.route('/wiki/<entry>')
        def wiki(entry):
            return 'test flask trace'  # pragma: NO COVER

        @app.route('/_ah/health')
        def health_check():
            return 'test health check'  # pragma: NO COVER

        @app.route('/error')
        def error():
            raise FlaskTestException('error')

        return app

    def test_constructor_default(self):
        app = mock.Mock(config={})

        middleware = flask_middleware.FlaskMiddleware(app=app)

        assert middleware.app == app
        assert middleware.blocked_paths is None
        assert middleware.injections is None
        assert app.after_request.called

    def test_constructor_explicit(self):
        app = mock.Mock(config={})
        blocked_urls = mock.Mock()
        injections = mock.Mock()

        middleware = flask_middleware.FlaskMiddleware(
            app=app, blocked_paths=blocked_urls, injections=injections)

        assert middleware.app == app
        assert middleware.blocked_paths == blocked_urls
        assert middleware.injections == injections
        assert app.after_request.called
