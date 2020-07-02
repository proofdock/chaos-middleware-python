from unittest.mock import patch

import pytest
from pdchaos.middleware.core import inject


@patch('pdchaos.middleware.core.inject.time')
def test_successful_inject_delay(time):
    inject.delay(5)
    time.sleep.assert_called_once_with(5)


@patch('pdchaos.middleware.core.inject.time')
def test_failed_inject_delay(time):
    inject.delay(-5)
    assert not time.sleep.called, 'Delay should not have been called'


def test_successful_inject_specified_exception():
    with pytest.raises(NotImplementedError):
        inject.raise_exception('NotImplementedError')


def test_successful_inject_default_exception():
    with pytest.raises(inject.MiddlewareDisruptionException):
        inject.raise_exception('DoesNotExistError')