import pydoc
import time

from logzero import logger


def delay(input_seconds):
    """Delay the response"""
    logger.debug("Initiate attack '{}'".format(delay.__name__))
    try:
        seconds = int(input_seconds)
        if seconds > 0:
            logger.debug("Delay {} second(s)".format(input_seconds))
            time.sleep(seconds)
        else:
            logger.warning("Skipping attack '{}'. Enter a positive number.".format(delay.__name__))
            return
    except ValueError:
        logger.warning("Skipping attack '{}'. '{}' is not a valid value.".format(delay.__name__, input_seconds))
        return


class MiddlewareDisruptionException(Exception):
    pass


def failure(input_exception: str):
    """Raise an exception. If exception is not found then a ChaosMiddlewareException is raised."""
    logger.debug("Initiate attack '{}'".format(failure.__name__))
    exception = pydoc.locate(input_exception)

    if exception:
        logger.debug("Raise exception '{}'".format(input_exception))
        raise exception

    logger.warning("'{}' is not a valid exception. Raising default exception '{}'.".format(
        MiddlewareDisruptionException.__name__, input_exception))
    raise MiddlewareDisruptionException
