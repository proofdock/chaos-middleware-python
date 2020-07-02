from unittest.mock import patch

from pdchaos.middleware.core.main import execute_chaos


@patch('pdchaos.middleware.core.main.inject')
def test_core_when_url_is_blocked(inject):
    blocked_url_paths = ['/hello', '/hello/about']
    called_path = '/hello'
    injections = {
        'delay': {'duration': 3},
        'exception': 'DoesNotExistError'
    }

    execute_chaos(called_path, blocked_url_paths, None, injections)

    assert not inject.delay.called, 'Delay should not have been called'
    assert not inject.raise_exception.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_inject_delay(inject):
    called_path = '/hello'
    injections = {
        'delay': {'duration': 3}
    }

    execute_chaos(called_path, None, None, injections)

    inject.delay.assert_called_once_with(injections['delay']['duration'])
    assert not inject.raise_exception.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_inject_exception(inject):
    called_path = '/hello'
    injections = {
        'exception': 'DoesNotExistError'
    }

    execute_chaos(called_path, None, None, injections)

    assert not inject.delay.called, 'Delay should not have been called'
    inject.raise_exception.assert_called_once_with(injections['exception'])
