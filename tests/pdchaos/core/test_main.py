from unittest import mock
from unittest.mock import patch

from pdchaos.middleware.core import HEADER_ATTACK
from pdchaos.middleware.core.main import execute, loaded_config

from tests.data import config_provider


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_header_attack_delay(inject):
    headers = {HEADER_ATTACK: '[{"type": "delay", "value": "3"}]'}

    execute(None, None, headers)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
@patch('pdchaos.middleware.core.main.dice')
def test_core_with_header_attack_delay_and_high_probability(dice, inject):
    headers = {HEADER_ATTACK: '[{"type": "delay", "value": "3", "probability": "80"}]'}

    dice.roll.return_value = True
    execute(None, None, headers)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
@patch('pdchaos.middleware.core.main.dice')
def test_core_with_header_attack_delay_and_low_probability(dice, inject):
    headers = {HEADER_ATTACK: '[{"type": "delay", "value": "3", "probability": "1"}]'}

    dice.roll.return_value = False
    execute(None, None, headers)

    assert not inject.delay.called, 'Delay injection should not have been called'
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_header_attack_fault(inject):
    failure_value = 'DoesNotExistError'
    headers = {HEADER_ATTACK: '[{"type": "failure", "value": "DoesNotExistError"}]'}
    execute(None, None, headers)

    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


@patch('pdchaos.middleware.core.main.os')
def test_core_with_chaos_configuration(os):
    os.path.exists.return_value = True
    loaded_config.set(None)

    with patch("builtins.open", mock.mock_open(read_data=config_provider.default())) as mock_file:
        execute("/hello", "GET", None)
        mock_file.assert_called_with("chaos-config.yml")

        loaded_config.set({})


@patch('pdchaos.middleware.core.main.os')
def test_core_with_chaos_configuration_and_not_fittin_method(os):
    os.path.exists.return_value = True
    loaded_config.set(None)

    with patch("builtins.open", mock.mock_open(read_data=config_provider.default())) as mock_file:
        execute("/hello", "DELETE", None)
        mock_file.assert_called_with("chaos-config.yml")

        loaded_config.set({})
