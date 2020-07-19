from logzero import logger
from pdchaos.middleware import core
from pdchaos.middleware.core.loader import proofdock


def load(ctx: dict):
    """Load the chaos configuration from the API provider"""
    provider = ctx.get(core.CTX_API_PROVIDER)

    if provider == "proofdock":
        return proofdock.load(ctx)

    else:
        logger.warn(
            "Unable to find API provider '{}'. Please provide a valid API provider, e.g. 'proofdock'".format(provider))
        return {}
