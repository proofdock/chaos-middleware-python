from pdchaos.middleware import core
from pdchaos.middleware.core import parse


def test_attacks_schema_full():
    _input = {
        "actions": [{"name": "delay", "value": "3", "probability": "80", "route": "/path/to"}],
        "target": {"application": "A"}
    }
    result = parse.attack(_input)

    assert result["actions"][0]["name"] == 'delay'
    assert result["actions"][0]["value"] == '3'
    assert result["actions"][0]["probability"] == '80'
    assert result["target"]["application"] == 'A'


def test_invalid_attacks_schema():
    _input = '[{"xxx": "80"}]'
    result = parse.attack(_input)

    assert not result


def test_attack_actions_schema():
    _input = [{"name": "delay", "value": "3", "probability": "80"}]
    result = parse.attack_actions(_input)

    assert result[0][core.ATTACK_KEY_ACTION_NAME] == core.ATTACK_ACTION_DELAY
    assert result[0][core.ATTACK_KEY_VALUE] == '3'
    assert result[0][core.ATTACK_KEY_PROBABILITY] == '80'


def test_empty_attack_actions():
    _input = []
    result = parse.attack_actions(_input)

    assert not result


def test_invalid_attack_actions_schema():
    _input = [{"xxx": "80"}]
    result = parse.attack_actions(_input)

    assert not result
