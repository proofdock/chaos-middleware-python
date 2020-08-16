from unittest.mock import patch, Mock

import pytest
from pdchaos.middleware.core import chaos

from tests.data import app_config_provider


@patch('pdchaos.middleware.core.chaos.loader')
def test_chaos_and_its_register(loader_factory):
    # arrange
    loader_mock = Mock()
    loader_factory.get.return_value = loader_mock

    # act
    chaos.register(app_config_provider.default())

    # clear
    chaos.loaded_app_config = None

    # assert
    assert loader_mock.load.called_once_with(app_config_provider.default())


def test_chaos_register_with_empty_config():
    with pytest.raises(Exception):
        chaos.register(None)
