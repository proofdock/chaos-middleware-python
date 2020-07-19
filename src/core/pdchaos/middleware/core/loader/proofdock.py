from logzero import logger
from pdchaos.middleware import core
from pdchaos.middleware.core.loader.session import client_session, get_error_message


def load(ctx: dict) -> dict:
    logger.debug("Fetching configuration from Proofdock Chaos API ...")

    with client_session(ctx.get(core.CTX_API_TOKEN), verify_tls=False) as session:
        response = _request(session, ctx)
        logger.debug("Fetched configuration")
        return response


def _request(session, ctx):
    _api_url = ctx.get(core.CTX_API_URL)
    _id = ctx.get(core.CTX_SERVICE_ID)
    response = session.get(_api_url + 'v1/attacks/{}'.format(_id), timeout=13)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))
