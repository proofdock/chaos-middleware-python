from pdchaos.middleware.core import url


def test_url_path_is_blocked():
    blocked_url_paths = ['/hello', '/hello/about']
    url_path = '/hello'

    assert url.is_blocked(url_path, blocked_url_paths)


def test_url_path_is_not_blocked():
    blocked_url_paths = ['/hello', '/hello/about']
    url_path = '/salut'

    assert not url.is_blocked(url_path, blocked_url_paths)
