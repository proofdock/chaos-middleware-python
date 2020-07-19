import pytest
from pdchaos.middleware import core
from pdchaos.middleware.core import loader


def test_invalid_loader():
    ctx_var = {core.CTX_API_PROVIDER: "xxx"}
    result = loader.load(ctx_var)

    assert not result


def test_proofdock_loader_unsuccessful():
    ctx_var = {core.CTX_API_PROVIDER: "proofdock"}
    with pytest.raises(Exception):
        loader.load(ctx_var)
