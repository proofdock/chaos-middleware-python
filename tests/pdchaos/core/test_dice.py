from unittest.mock import patch

from pdchaos.middleware.core import dice


def test_dice_roll_with_invalid_value():
    result = dice.roll("x")
    assert not result


def test_dice_roll_with_too_high_number():
    result = dice.roll("101")
    assert not result


def test_dice_roll_100_percent():
    result = dice.roll("100")
    assert result


@patch('pdchaos.middleware.core.dice.random')
def test_dice_roll_below_fifty_percent(random):
    random.randint.return_value = 49
    result = dice.roll("50")
    assert result


@patch('pdchaos.middleware.core.dice.random')
def test_dice_roll_above_fifty_percent(random):
    random.randint.return_value = 99
    result = dice.roll("50")
    assert not result
