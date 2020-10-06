from pdchaos.middleware.core import chaos


def test_chaos_set_attack_action():
    # Arrange
    _input = [{"name": "delay", "value": "3", "probability": "80"}]

    chaos._set_attack_action(_input)
    assert chaos.loaded_attack_actions == _input


def test_chaos_set_attack_action_with_invalid_input():
    # Arrange
    _input = [{"xxx": "yyy"}]

    chaos._set_attack_action(_input)
    assert chaos.loaded_attack_actions == []
