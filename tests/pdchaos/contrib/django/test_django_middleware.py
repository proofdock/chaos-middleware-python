from unittest import mock
from unittest.mock import patch

from django.conf import settings as django_settings
from django.test import RequestFactory

from pdchaos.middleware.contrib.django import django_middleware


class TestDjangoMiddleware:

    def setup_method(self):
        from django.test.utils import setup_test_environment

        if not django_settings.configured:
            django_settings.configure()
        setup_test_environment()

    def teardown_method(self):
        from django.test.utils import teardown_test_environment

        del django_settings.CHAOS_MIDDLEWARE
        teardown_test_environment()

    @patch('pdchaos.middleware.core.chaos.register')
    def test_unconfigured_configuration(self, register):
        django_middleware.DjangoMiddleware(None)
        assert register.call_count == 0

    @patch('pdchaos.middleware.core.chaos.register')
    def test_empty_configuration(self, register):
        django_settings.CHAOS_MIDDLEWARE = {}
        django_middleware.DjangoMiddleware(None)

        assert register.call_count == 0

    @patch('pdchaos.middleware.core.chaos.register')
    def test_configuration(self, register):
        django_settings.CHAOS_MIDDLEWARE = {
            'CHAOS_MIDDLEWARE_APPLICATION_NAME': 'webshop',
            'CHAOS_MIDDLEWARE_APPLICATION_ENV': 'sandbox',
            'CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN': 'eyJ0eXAi...05'
        }
        django_middleware.DjangoMiddleware(None)

        assert register.call_count == 1

    @patch('pdchaos.middleware.core.chaos.register')
    @patch('pdchaos.middleware.core.chaos.attack')
    def test_request(self, attack, register):
        django_settings.CHAOS_MIDDLEWARE = {
            'CHAOS_MIDDLEWARE_APPLICATION_NAME': 'webshop',
            'CHAOS_MIDDLEWARE_APPLICATION_ENV': 'sandbox',
            'CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN': 'eyJ0eXAi...05'
        }

        get_response = mock.MagicMock()
        django_request = RequestFactory().get('/wiki/Rabbit')
        middleware = django_middleware.DjangoMiddleware(get_response)
        middleware(django_request)

        assert register.call_count == 1
        assert attack.call_count == 1

    @patch('pdchaos.middleware.core.chaos.register')
    @patch('pdchaos.middleware.core.chaos.attack')
    def test_unconfigured_request(self, attack, register):
        get_response = mock.MagicMock()
        django_request = RequestFactory().get('/wiki/Rabbit')
        middleware = django_middleware.DjangoMiddleware(get_response)
        middleware(django_request)

        assert register.call_count == 0
        assert attack.call_count == 0
