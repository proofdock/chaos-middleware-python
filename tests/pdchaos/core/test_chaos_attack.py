from unittest.mock import patch

import pytest
from pdchaos.middleware.core import chaos
from pdchaos.middleware.core.config import AppConfig
from pdchaos.middleware.core.inject import ChaosMiddlewareError

from tests.data import attack_config_provider


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_attack_that_is_not_targeted_by_name(inject):
    attack = {
        "actions": [{"name": "delay", "value": "3"}],
        "target": {"application": "B"}
    }

    chaos.loaded_app_config = {
        AppConfig.APPLICATION_NAME: "A"
    }
    chaos.attack(attack)

    assert not inject.delay.called, 'Delay should not have been called'


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_attack_that_is_not_targeted_by_env(inject):
    attack = {
        "actions": [{"name": "delay", "value": "3"}],
        "target": {"application": "A", "environment": "sandbox"}
    }

    chaos.loaded_app_config = {
        AppConfig.APPLICATION_NAME: "A",
        AppConfig.APPLICATION_ENV: "prod"
    }
    chaos.attack(attack)

    assert not inject.delay.called, 'Delay should not have been called'


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_attack_that_is_targeted(inject):
    attack = {
        "actions": [{"name": "delay", "value": "3"}],
        "target": {"application": "A", "environment": "sandbox"}
    }

    chaos.loaded_app_config = {
        AppConfig.APPLICATION_NAME: "A",
        AppConfig.APPLICATION_ENV: "sandbox"
    }
    chaos.attack(attack)

    assert inject.delay.called, 'Delay should not have been called'


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_with_header_attack_delay(inject):
    attack = {"actions": [{"name": "delay", "value": "3"}]}

    chaos.attack(attack)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.executor.inject')
@patch('pdchaos.middleware.core.executor.dice')
def test_chaos_with_header_attack_delay_and_high_probability(dice, inject):
    attack = {"actions": [{"name": "delay", "value": "3", "probability": "80"}]}

    dice.roll.return_value = True
    chaos.attack(attack)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.executor.inject')
@patch('pdchaos.middleware.core.executor.dice')
def test_chaos_with_header_attack_delay_and_low_probability(dice, inject):
    attack = {"actions": [{"name": "delay", "value": "3", "probability": "1"}]}

    dice.roll.return_value = False
    chaos.attack(attack)

    assert not inject.delay.called, 'Delay injection should not have been called'
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_with_header_attack_fault(inject):
    failure_value = 'DoesNotExistError'
    attack = {"actions": [{"name": "fault", "value": "DoesNotExistError"}]}
    chaos.attack(attack)

    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


def test_chaos_with_header_attack_fault_and_arithmetic_error():
    fault_value = 'ArithmeticError'
    attack = {"actions": [{"name": "fault", "value": fault_value}]}

    with pytest.raises(ArithmeticError):
        chaos.attack(attack)


def test_chaos_with_header_attack_fault_and_unavailable_error():
    fault_value = 'DoesNotExistError'
    attack = {"actions": [{"name": "fault", "value": fault_value}]}

    with pytest.raises(ChaosMiddlewareError):
        chaos.attack(attack)


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_with_target_and_route_based_header_attack_fault(inject):
    # arrange
    failure_value = 'DoesNotExistError'
    attack = {
        "target": {"application": "A"},
        "actions": [
            {"name": "fault", "value": "DoesNotExistError", "route": "/hello"}
        ]}
    chaos.loaded_app_config = {AppConfig.APPLICATION_NAME: 'A'}

    # act
    chaos.attack(attack, {"route": "/hello"})

    # clear
    chaos.loaded_app_config = None

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_with_attack_configuration(inject):
    # arrange
    chaos.loaded_attack_actions = attack_config_provider.default()

    # act
    chaos.attack(attack_ctx={"route": "/hello"})
    chaos.attack(attack_ctx={"route": "/api"})

    # clear
    chaos.loaded_attack_actions = None

    # assert
    assert inject.delay.call_count == 2
    assert inject.failure.call_count == 0, 'Failure should not have been called'


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_with_invalid_attack_configuration(inject):
    # arrange
    chaos.loaded_app_config = attack_config_provider.invalid()

    # act
    chaos.attack(None, {"route": "/hello"})

    # clear
    chaos.loaded_app_config = None

    # assert
    assert not inject.delay.called, 'Delay should not have been called'
    assert not inject.failure.called, 'Failure should not have been called'


@patch('pdchaos.middleware.core.executor.inject')
def test_chaos_attack_with_regex_route(inject):
    attack = {
        "actions": [{"name": "delay", "value": "3", "route": "/v1/*/method"}]
    }

    # act
    chaos.attack(attack_input=attack, attack_ctx={"route": "/v1/attacks/method"})

    # clear
    chaos.loaded_attack_actions = None

    # assert
    assert inject.delay.call_count == 1
