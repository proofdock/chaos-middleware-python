import asyncio
import contextvars

from logzero import logger
from pdchaos.middleware import core
from pdchaos.middleware.core import inject, dice, parse, loader

loaded_context = contextvars.ContextVar('loaded_context', default={})
loaded_config = contextvars.ContextVar('loaded_config', default=None)


async def _load_configuration(interval=30):
    while True:
        try:
            # Fetch
            config = loader.load(loaded_context.get())

            # Validate
            parse.attack_as_dict(config)

            # Configure
            loaded_config.set(config)
        except Exception as e:
            logger.warning("Unable to load attack configuration. Reason: {}".format(e))

        await asyncio.sleep(interval)


def register(service_app_context: dict):
    """Register a service application"""
    _provide_default_context(service_app_context)
    loaded_context.set(service_app_context)
    _init_poller()


def _provide_default_context(service_app_context):
    if not service_app_context.get(core.CTX_API_PROVIDER):
        service_app_context[core.CTX_API_PROVIDER] = 'proofdock'

    if not service_app_context.get(core.CTX_API_URL):
        service_app_context[core.CTX_API_URL] = 'https://chaosapi.proofdock.io/'


def _init_poller():
    ctx = loaded_context.get()
    is_qualified_to_poll = bool(ctx.get(core.CTX_API_TOKEN) and ctx.get(core.CTX_SERVICE_NAME))

    if is_qualified_to_poll:
        interval = 30
        logger.debug("Synchronize attack configuration every %s seconds" % interval)
        loop = asyncio.get_event_loop()
        loop.create_task(_load_configuration(interval))
        loop.run_forever()

    else:
        logger.warn("Skip synchronizing attack configuration. Reason: Application is not qualified to synchronize."
                    " Please provide essential information, e.g. service name and API token.")


def attack(called_path: str, requested_headers: dict):
    """Execute chaos"""
    # Client side configuration
    if requested_headers and core.HEADER_ATTACK in requested_headers:
        attacks = parse.attack_as_str(requested_headers.get(core.HEADER_ATTACK))
        if attacks:
            _execute_attacks(attacks, called_path)

    # Server side configuration
    elif loaded_config.get():
        attacks = parse.attack_as_dict(loaded_config.get())
        if attacks:
            _execute_attacks(attacks, called_path)


def _execute_attacks(attacks, called_path):
    for _attack in attacks:
        _is_lucky_to_be_attacked = dice.roll(_attack.get(core.ATTACK_KEY_PROBABILITY))

        if not _is_lucky_to_be_attacked:
            continue

        if not _is_aimed_for_attack(_attack, called_path):
            continue

        if _attack[core.ATTACK_KEY_ACTION] == core.ATTACK_ACTION_DELAY:
            inject.delay(_attack[core.ATTACK_KEY_VALUE])

        if _attack[core.ATTACK_KEY_ACTION] == core.ATTACK_ACTION_FAULT:
            inject.failure(_attack[core.ATTACK_KEY_VALUE])


def _is_aimed_for_attack(_attack, called_route):
    target = _attack.get(core.ATTACK_KEY_TARGET)

    if not target:
        return True

    service = target.get(core.ATTACK_KEY_TARGET_SERVICE)
    is_svc_targeted = (service and service == loaded_context.get().get(core.CTX_SERVICE_NAME)) or not service

    route = target.get(core.ATTACK_KEY_TARGET_ROUTE)
    is_route_targeted = (route and route == called_route) or not route

    return is_svc_targeted and is_route_targeted
