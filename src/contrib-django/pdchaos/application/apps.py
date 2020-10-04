from django.apps import AppConfig
from django.conf import settings
from logzero import logger

from pdchaos.application import patch
from pdchaos.application.config import DjangoConfig
from pdchaos.middleware.core import chaos


class ChaosConfig(AppConfig):
    name = 'pdchaos.application'
    label = 'chaos'
    verbose_name = 'Chaos'
    logger.info("Registering Proofdock chaos")

    def ready(self):
        logger.info("Ready to register Proofdock chaos")
        try:
            if settings.CHAOS_MIDDLEWARE:
                config = DjangoConfig(settings.CHAOS_MIDDLEWARE)
                chaos.register(config)
                patch.get_response()
                patch.get_response_async()
                logger.info("Registered Proofdock chaos without errors")

        except Exception as ex:
            logger.error("Unable to configure chaos middleware. Error: %s", ex, stack_info=True)
