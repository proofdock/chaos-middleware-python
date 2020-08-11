import pytest
from pdchaos.middleware.core.config import AppConfig
from pdchaos.middleware.core import loader


def test_invalid_loader():
    config_var = {AppConfig.ATTACK_LOADER: "xxx"}
    result = loader.get(config_var)

    assert not result


def test_proofdock_loader_unsuccessful():
    ctx_var = {AppConfig.ATTACK_LOADER: "proofdock"}
    with pytest.raises(Exception):
        loader.load(ctx_var)
