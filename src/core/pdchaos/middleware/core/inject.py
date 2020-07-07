import pydoc
import time


def delay(input_seconds):
    """Delay the response"""
    try:
        seconds = int(input_seconds)
    except ValueError:
        return

    if seconds > 0:
        time.sleep(seconds)


class MiddlewareDisruptionException(Exception):
    pass


def failure(exception: str):
    """Raise an exception. If exception is not found then a ChaosMiddlewareException is raised."""
    exception_to_raise = pydoc.locate(exception)

    if exception_to_raise:
        raise exception_to_raise

    raise MiddlewareDisruptionException
