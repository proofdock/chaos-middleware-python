import pydoc
import time


def delay(seconds: int):
    """Delay the response"""
    if seconds > 0:
        time.sleep(seconds)


class MiddlewareDisruptionException(Exception):
    pass


def raise_exception(exception: str):
    """Raise an exception. If exception is not found then a ChaosMiddlewareException is raised."""
    exception_to_raise = pydoc.locate(exception)

    if exception_to_raise:
        raise exception_to_raise

    raise MiddlewareDisruptionException
