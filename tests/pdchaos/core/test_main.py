from unittest.mock import patch, Mock

from pdchaos.middleware.core import HEADER_ATTACK
from pdchaos.middleware.core.main import attack, loaded_app_config, loaded_attack_config, register
from pdchaos.middleware.core.config import AppConfig

from tests.data import attack_config_provider, app_config_provider


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
    loaded_app_config.set({AppConfig.APPLICATION_NAME: 'A'})

    # act
    attack("/hello", headers)

    # clear
    loaded_app_config.set({})

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_attack_configuration(inject):
    # arrange
    loaded_attack_config.set(attack_config_provider.default())

    # act
    attack("/hello", None)
    attack("/api", None)

    # clear
    loaded_attack_config.set({})

    # assert
    assert inject.delay.called
    assert not inject.failure.called, 'Failure should not have been called'


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_invalid_attack_configuration(inject):
    # arrange
    loaded_app_config.set(attack_config_provider.invalid())

    # act
    attack("/hello", None)

    # clear
    loaded_app_config.set({})

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    assert not inject.failure.called, 'Failure should not have been called'


@patch('pdchaos.middleware.core.loader')
def test_core_and_its_register(loader_factory):
    # arrange
    loader_mock = Mock()
    loader_factory.get.return_value = loader_mock

    # act
    register(app_config_provider.default())

    # clear
    loaded_app_config.set({})

    # assert
    assert loader_mock.load.called_once_with(app_config_provider.default())
