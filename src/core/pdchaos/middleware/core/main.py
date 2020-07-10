from pdchaos.middleware.core import HEADER_ATTACK, model, inject, dice


def execute_chaos(called_path: str, requested_headers: dict):
    """Execute chaos"""
    if requested_headers:
        if HEADER_ATTACK in requested_headers:
            attack = model.parse_attack(requested_headers.get(HEADER_ATTACK))
            for a in attack:
                is_active = True

                if a.get('probability'):
                    is_active = dice.roll(a['probability'])

                if a['type'] == 'delay' and is_active:
                    inject.delay(a['value'])

                if a['type'] == 'failure' and is_active:
                    inject.failure(a['value'])
