from unittest.mock import patch, Mock

from pdchaos.middleware.core import HEADER_ATTACK
from pdchaos.middleware.core import chaos
from pdchaos.middleware.core.config import AppConfig

from tests.data import attack_config_provider, app_config_provider


@patch('pdchaos.middleware.core.chaos.inject')
def test_core_with_header_attack_delay(inject):
    headers = {HEADER_ATTACK: '[{"action": "delay", "value": "3"}]'}

    chaos.attack(None, headers)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.chaos.inject')
@patch('pdchaos.middleware.core.chaos.dice')
def test_core_with_header_attack_delay_and_high_probability(dice, inject):
    headers = {HEADER_ATTACK: '[{"action": "delay", "value": "3", "probability": "80"}]'}

    dice.roll.return_value = True
    chaos.attack(None, headers)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.chaos.inject')
@patch('pdchaos.middleware.core.chaos.dice')
def test_core_with_header_attack_delay_and_low_probability(dice, inject):
    headers = {HEADER_ATTACK: '[{"action": "delay", "value": "3", "probability": "1"}]'}

    dice.roll.return_value = False
    chaos.attack(None, headers)

    assert not inject.delay.called, 'Delay injection should not have been called'
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.chaos.inject')
def test_core_with_header_attack_fault(inject):
    failure_value = 'DoesNotExistError'
    headers = {HEADER_ATTACK: '[{"action": "fault", "value": "DoesNotExistError"}]'}
    chaos.attack(None, headers)

    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


@patch('pdchaos.middleware.core.chaos.inject')
def test_core_with_target_based_header_attack_fault(inject):
    # arrange
    failure_value = 'DoesNotExistError'
    headers = {
        HEADER_ATTACK: '[{"action":"fault","value":"DoesNotExistError", "target":{"service":"A", "route":"/hello"}}]'
    }
    chaos.loaded_app_config = {AppConfig.APPLICATION_NAME: 'A'}

    # act
    chaos.attack("/hello", headers)

    # clear
    chaos.loaded_app_config = None

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


@patch('pdchaos.middleware.core.chaos.inject')
def test_core_with_attack_configuration(inject):
    # arrange
    chaos.loaded_attack_config = attack_config_provider.default()

    # act
    chaos.attack("/hello", None)
    chaos.attack("/api", None)

    # clear
    chaos.loaded_attack_config = None

    # assert
    assert inject.delay.called
    assert not inject.failure.called, 'Failure should not have been called'


@patch('pdchaos.middleware.core.chaos.inject')
def test_core_with_invalid_attack_configuration(inject):
    # arrange
    chaos.loaded_app_config = attack_config_provider.invalid()

    # act
    chaos.attack("/hello", None)

    # clear
    chaos.loaded_app_config = None

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    assert not inject.failure.called, 'Failure should not have been called'


@patch('pdchaos.middleware.core.loader')
def test_core_and_its_register(loader_factory):
    # arrange
    loader_mock = Mock()
    loader_factory.get.return_value = loader_mock

    # act
    chaos.register(app_config_provider.default())

    # clear
    chaos.loaded_app_config = None

    # assert
    assert loader_mock.load.called_once_with(app_config_provider.default())
