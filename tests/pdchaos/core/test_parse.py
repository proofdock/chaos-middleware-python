from pdchaos.middleware import core
from pdchaos.middleware.core import parse


def test_attacks_schema_plain():
    _input = '[{"action": "delay", "value": "3", "probability": "80"}]'
    result = parse.attack_as_str(_input)

    assert result[0][core.ATTACK_KEY_ACTION] == core.ATTACK_ACTION_DELAY
    assert result[0][core.ATTACK_KEY_VALUE] == '3'
    assert result[0][core.ATTACK_KEY_PROBABILITY] == '80'


def test_attacks_schema_full():
    _input = '[{"action": "delay", "value": "3", "probability": "80", "target":{"service":"A","route":"/path/to"} }]'
    result = parse.attack_as_str(_input)

    assert result[0][core.ATTACK_KEY_ACTION] == 'delay'
    assert result[0][core.ATTACK_KEY_VALUE] == '3'
    assert result[0][core.ATTACK_KEY_PROBABILITY] == '80'


def test_invalid_attacks_schema():
    _input = '[{"xxx": "80"}]'
    result = parse.attack_as_str(_input)

    assert not result
