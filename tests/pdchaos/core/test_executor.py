from pdchaos.middleware.core import executor


def test_chaos_route_unconfigured_action_route_():
    # Arrange
    action_route = ""
    attack_ctx_route = "/users"

    assert executor._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_matched_action_route():
    # Arrange
    action_route = "/users"
    attack_ctx_route = "/users"

    assert executor._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_unmatched_action_route():
    # Arrange
    action_route = "/users"
    attack_ctx_route = "/hello"

    assert not executor._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_matched_asterisk_action_route():
    # Arrange
    action_route = "/users/*/posts/*"
    attack_ctx_route = "/users/53a2-45b1-982e-6042c/posts/57a2-1db1-461e-60d42?utm_source=facebook&utm_medium=social" \
                       "&utm_campaign=facebook "

    assert executor._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_unmatched_asterisk_action_route():
    # Arrange
    action_route = "/user/*/post/*"
    attack_ctx_route = "/users/53a2-45b1-982e-6042c/posts/57a2-1db1-461e-60d42?utm_source=facebook&utm_medium=social" \
                       "&utm_campaign=facebook "

    assert not executor._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_unmatched_asterisk_action_route_empty_string():
    # Arrange
    action_route = "/user/*/post/*"
    attack_ctx_route = ""

    assert executor._is_route_targeted(attack_ctx_route, action_route)


def test_chaos_route_configured_and_unmatched_asterisk_action_route_none():
    # Arrange
    action_route = "/user/*/post/*"
    attack_ctx_route = None

    assert executor._is_route_targeted(attack_ctx_route, action_route)
