from unittest.mock import patch

from pdchaos.middleware.core import dice


def test_dice_roll_with_invalid_value():
    result = dice.roll("x")
    assert not result


def test_dice_roll_with_too_high_number():
    result = dice.roll("101")
    assert not result


@patch('pdchaos.middleware.core.dice.random')
def test_dice_roll(random):
    random.randint.return_value = 49
    result = dice.roll("50")
    assert result


@patch('pdchaos.middleware.core.dice.random')
def test_dice_roll(random):
    random.randint.return_value = 99
    result = dice.roll("50")
    assert not result
