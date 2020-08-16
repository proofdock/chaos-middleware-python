import pydoc
import time

from logzero import logger


def delay(input_seconds):
    """Delay the response"""
    try:
        seconds = int(input_seconds)
        if seconds > 0:
            logger.debug("Injecting delay for {} second(s)".format(input_seconds))
            time.sleep(seconds)
        else:
            logger.warning("Skipping attack '{}'. Enter a positive number.".format(delay.__name__))
            return
    except ValueError:
        logger.warning("Skipping attack '{}'. '{}' is not a valid value.".format(delay.__name__, input_seconds))
        return


class ChaosMiddlewareError(Exception):
    pass


def failure(input_exception: str):
    """Raise an exception. If exception is not found then a MiddlewareDisruptionException is raised."""
    exception = pydoc.locate(input_exception)

    if exception:
        logger.debug("Raising exception '{}'".format(input_exception))
        raise ChaosMiddlewareError from exception

    logger.warning("'{}' is not a valid exception. Raising default exception '{}'.".format(
        input_exception, ChaosMiddlewareError.__name__))
    raise ChaosMiddlewareError
