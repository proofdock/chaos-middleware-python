from pdchaos.middleware.core import chaos


def test_chaos_route_unconfigured_action_route_():
    # Arrange
    action_route = ""
    attack_ctx_route = "/users"

    assert chaos._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_matched_action_route():
    # Arrange
    action_route = "/users"
    attack_ctx_route = "/users"

    assert chaos._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_unmatched_action_route():
    # Arrange
    action_route = "/users"
    attack_ctx_route = "/hello"

    assert not chaos._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_matched_asterisk_action_route():
    # Arrange
    action_route = "/users/*/posts/*"
    attack_ctx_route = "/users/53a2-45b1-982e-6042c/posts/57a2-1db1-461e-60d42?utm_source=facebook&utm_medium=social" \
                       "&utm_campaign=facebook "

    assert chaos._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_unmatched_asterisk_action_route():
    # Arrange
    action_route = "/user/*/post/*"
    attack_ctx_route = "/users/53a2-45b1-982e-6042c/posts/57a2-1db1-461e-60d42?utm_source=facebook&utm_medium=social" \
                       "&utm_campaign=facebook "

    assert not chaos._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_unmatched_asterisk_action_route_empty_string():
    # Arrange
    action_route = "/user/*/post/*"
    attack_ctx_route = ""

    assert chaos._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_unmatched_asterisk_action_route_none():
    # Arrange
    action_route = "/user/*/post/*"
    attack_ctx_route = None

    assert chaos._is_route_targeted(attack_ctx_route, action_route)


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
