from unittest import mock
from unittest.mock import patch

from pdchaos.middleware.core import HEADER_ATTACK
from pdchaos.middleware.core.main import attack, loaded_config, loaded_context

from tests.data import config_provider


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_header_attack_delay(inject):
    headers = {HEADER_ATTACK: '[{"action": "delay", "value": "3"}]'}

    attack(None, headers)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
@patch('pdchaos.middleware.core.main.dice')
def test_core_with_header_attack_delay_and_high_probability(dice, inject):
    headers = {HEADER_ATTACK: '[{"action": "delay", "value": "3", "probability": "80"}]'}

    dice.roll.return_value = True
    attack(None, headers)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
@patch('pdchaos.middleware.core.main.dice')
def test_core_with_header_attack_delay_and_low_probability(dice, inject):
    headers = {HEADER_ATTACK: '[{"action": "delay", "value": "3", "probability": "1"}]'}

    dice.roll.return_value = False
    attack(None, headers)

    assert not inject.delay.called, 'Delay injection should not have been called'
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_header_attack_fault(inject):
    failure_value = 'DoesNotExistError'
    headers = {HEADER_ATTACK: '[{"action": "fault", "value": "DoesNotExistError"}]'}
    attack(None, headers)

    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_target_based_header_attack_fault(inject):
    # arrange
    failure_value = 'DoesNotExistError'
    headers = {
        HEADER_ATTACK: '[{"action":"fault","value":"DoesNotExistError", "target":{"service":"A", "route":"/hello"}}]'
    }
    loaded_context.set({'SERVICE_NAME': 'A'})

    # act
    attack("/hello", headers)

    # clear
    loaded_context.set({})

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


@patch('pdchaos.middleware.core.main.os')
def test_core_with_chaos_configuration(os):
    os.path.exists.return_value = True
    loaded_config.set(None)

    with patch("builtins.open", mock.mock_open(read_data=config_provider.default())) as mock_file:
        attack("/hello", None)
        mock_file.assert_called_with("chaos-config.json")

        loaded_config.set({})


@patch('pdchaos.middleware.core.main.os')
def test_core_with_invalid_chaos_configuration(os):
    os.path.exists.return_value = True
    loaded_config.set(None)

    with patch("builtins.open", mock.mock_open(read_data=config_provider.invalid())) as mock_file:
        attack("/hello", None)
        mock_file.assert_called_with("chaos-config.json")

        loaded_config.set({})
