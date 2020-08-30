from unittest.mock import patch

from django.conf import settings as django_settings

from pdchaos.middleware.contrib.django.django_middleware import DjangoConfig


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
    @patch('pdchaos.middleware.core.chaos.attack')
    def test_django_configuration(self, attack, register):
        config = DjangoConfig({
            'CHAOS_MIDDLEWARE_APPLICATION_NAME': 'webshop',
            'CHAOS_MIDDLEWARE_APPLICATION_ENV': 'sandbox',
            'CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN': 'eyJ0eXAi...05'
        })
        assert config.get('CHAOS_MIDDLEWARE_APPLICATION_NAME') == 'webshop'
        assert config.get('CHAOS_MIDDLEWARE_APPLICATION_ENV') == 'sandbox'
        assert config.get('CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN') == 'eyJ0eXAi...05'

    @patch('pdchaos.middleware.core.chaos.register')
    @patch('pdchaos.middleware.core.chaos.attack')
    def test_django_unexpected_configuration(self, attack, register):
        config = DjangoConfig({
            'CHAOS_MIDDLEWARE_APPLICATION_NAME': 'webshop',
            'CHAOS_MIDDLEWARE_APPLICATION_ENV': 'sandbox',
            'CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN': 'eyJ0eXAi...05'
        })
        assert config.get('UNEXPECTED') is None
