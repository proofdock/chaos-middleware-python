from unittest import mock

import flask
import pytest
from pdchaos.middleware.contrib.flask import flask_middleware
from pdchaos.middleware.core import HEADER_ATTACK
from pdchaos.middleware.core.inject import MiddlewareDisruptionException


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

    def test_constructor(self):
        app = mock.Mock(config={})
        middleware = flask_middleware.FlaskMiddleware(app=app)

        assert middleware.app == app
        assert app.after_request.called

    def test_call_without_proofdock_headers(self):
        app = self.create_app()
        middleware = flask_middleware.FlaskMiddleware(app=app)

        with app.test_request_context(path='/wiki', headers={}):
            app.process_response(None)
            assert middleware.app == app

    def test_call_with_header_attack_delay(self):
        attack_request = '[{"type": "delay", "value": "1"}]'
        app = self.create_app()
        flask_middleware.FlaskMiddleware(app=app)

        with app.test_request_context(path='/wiki', headers={HEADER_ATTACK: attack_request}):
            app.process_response(None)

    def test_call_with_header_attack_fault(self):
        attack_request = '[{"type": "failure", "value": "DoesNotExistError"}]'
        app = self.create_app()
        flask_middleware.FlaskMiddleware(app=app)

        with app.test_request_context(path='/wiki', headers={HEADER_ATTACK: attack_request}):
            with pytest.raises(MiddlewareDisruptionException):
                app.process_response(None)
