import json

from django.conf import settings
from logzero import logger

from pdchaos.middleware import core
from pdchaos.middleware.contrib.django.django_config import DjangoConfig
from pdchaos.middleware.core import chaos


class DjangoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        try:
            if settings.CHAOS_MIDDLEWARE:
                config = DjangoConfig(settings.CHAOS_MIDDLEWARE)
                chaos.register(config)

        except Exception as ex:
            logger.error("Unable to configure chaos middleware. Error: %s", ex, stack_info=True)

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        response = self.get_response(request)
        try:
            if settings.CHAOS_MIDDLEWARE:
                headers = request.headers
                attack = json.loads(headers.get(core.HEADER_ATTACK)) if (core.HEADER_ATTACK in headers) else None
                attack_ctx = {core.ATTACK_KEY_ROUTE: request.path}
                chaos.attack(attack, attack_ctx)

        except Exception as ex:
            logger.error("Unable to apply chaos middleware. Error: %s", ex, stack_info=True)

        return response
