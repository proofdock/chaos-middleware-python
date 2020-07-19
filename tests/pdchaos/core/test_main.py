from unittest.mock import patch

from pdchaos.middleware import core
from pdchaos.middleware.core import HEADER_ATTACK
from pdchaos.middleware.core.main import attack, loaded_config, loaded_context, register

from tests.data import config_provider, context_provider


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
    loaded_context.set({core.CTX_SERVICE_NAME: 'A'})

    # act
    attack("/hello", headers)

    # clear
    loaded_context.set({})

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_chaos_configuration(inject):
    # arrange
    loaded_config.set(config_provider.default())

    # act
    attack("/hello", None)
    attack("/api", None)

    # clear
    loaded_config.set({})

    # assert
    assert inject.delay.called
    assert not inject.failure.called, 'Failure should not have been called'


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_invalid_chaos_configuration(inject):
    # arrange
    loaded_config.set(config_provider.invalid())

    # act
    attack("/hello", None)

    # clear
    loaded_config.set({})

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    assert not inject.failure.called, 'Failure should not have been called'


@patch('pdchaos.middleware.core.main.asyncio')
@patch('pdchaos.middleware.core.main.loader')
def test_core_and_its_async_poller(loader, asyncio):
    # arrange
    loader.load.return_value = {}

    # act
    register(context_provider.default())

    # clear
    loaded_context.set({})

    # assert
    assert asyncio.get_event_loop.called
