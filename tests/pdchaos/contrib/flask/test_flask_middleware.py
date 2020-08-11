from unittest import mock
from unittest.mock import ANY, patch

import flask

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

        app.config.setdefault("CHAOS_MIDDLEWARE_ATTACK_LOADER", "non-existing")
        return app

    @patch('pdchaos.middleware.core.chaos.register')
    def test_constructor(self, register):
        app = mock.Mock(config={})
        middleware = flask_middleware.FlaskMiddleware(app=app)

        assert middleware.app == app
        assert app.after_request.call_count == 1
        assert register.call_count == 1

    @patch('pdchaos.middleware.core.chaos.register')
    def test_constructor_and_proper_context(self, register):
        app = mock.Mock()
        middleware = flask_middleware.FlaskMiddleware(app=app)

        assert middleware.app == app
        assert app.after_request.call_count == 1
        app.config.setdefault.assert_called_once_with("CHAOS_MIDDLEWARE_APPLICATION_ID", ANY)

    def test_call_without_proofdock_headers(self):
        app = self.create_app()
        middleware = flask_middleware.FlaskMiddleware(app=app)

        with app.test_request_context(path='/wiki', headers={}):
            app.process_response(None)
            assert middleware.app == app

    def test_call_with_header_attack_delay(self):
        attack_request = '[{"name": "delay", "value": "1"}]'
        app = self.create_app()
        flask_middleware.FlaskMiddleware(app=app)

        with app.test_request_context(path='/wiki', headers={HEADER_ATTACK: attack_request}):
            app.process_response(None)

    def test_call_with_header_attack_fault(self):
        # issue: exception handling ? wrapping?? https://github.com/proofdock/chaos-middleware-python/issues/27
        # attack_request = '{"actions": [{"name": "fault", "value": "DoesNotExistError"}]}'
        # app = self.create_app()
        # flask_middleware.FlaskMiddleware(app=app)

        # with app.test_request_context(path='/wiki', headers={HEADER_ATTACK: attack_request}):
        #     with pytest.raises(MiddlewareDisruptionException):
        #         app.process_response(None)
        pass
