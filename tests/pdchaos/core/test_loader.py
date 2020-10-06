import pytest
from pdchaos.middleware.core.config import AppConfig
from pdchaos.middleware.core import loader
from pdchaos.middleware.core.proofdock.loader import ProofdockAttackLoader


def test_invalid_loader():
    config_var = {AppConfig.ATTACK_LOADER: "xxx"}
    result = loader.init(config_var, None)

    assert not result


def test_proofdock_loader_unsuccessful():
    ctx_var = {AppConfig.ATTACK_LOADER: "proofdock"}
    with pytest.raises(Exception):
        loader.load(ctx_var)


def test_proofdock_loader():
    config_var = {AppConfig.ATTACK_LOADER: "proofdock"}
    result = loader.init(config_var, None)

    assert not result
