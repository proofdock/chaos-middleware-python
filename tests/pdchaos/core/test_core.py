from unittest.mock import patch

from pdchaos.middleware.core import HEADER_ATTACK
from pdchaos.middleware.core.main import execute_chaos


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_header_attack_delay(inject):
    headers = {HEADER_ATTACK: '[{"type": "delay", "value": "3"}]'}

    execute_chaos(None, headers)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
@patch('pdchaos.middleware.core.main.dice')
def test_core_with_header_attack_delay_and_high_probability(dice, inject):
    headers = {HEADER_ATTACK: '[{"type": "delay", "value": "3", "probability": "80"}]'}

    dice.roll.return_value = True
    execute_chaos(None, headers)

    inject.delay.assert_called_once_with('3')
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
@patch('pdchaos.middleware.core.main.dice')
def test_core_with_header_attack_delay_and_low_probability(dice, inject):
    headers = {HEADER_ATTACK: '[{"type": "delay", "value": "3", "probability": "1"}]'}

    dice.roll.return_value = False
    execute_chaos(None, headers)

    assert not inject.delay.called, 'Delay injection should not have been called'
    assert not inject.failure.called, 'Raise exception should not have been called'


@patch('pdchaos.middleware.core.main.inject')
def test_core_with_header_attack_fault(inject):
    failure_value = 'DoesNotExistError'
    headers = {HEADER_ATTACK: '[{"type": "failure", "value": "DoesNotExistError"}]'}
    execute_chaos(None, headers)

    assert not inject.delay.called, 'Delay should not have been called'
    inject.failure.assert_called_once_with(failure_value)
