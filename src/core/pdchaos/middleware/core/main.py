from pdchaos.middleware.core import HEADER_ATTACK, model, inject


def execute_chaos(called_path: str, requested_headers: dict):
    """Execute chaos"""
    if requested_headers:
        if HEADER_ATTACK in requested_headers:
            attack = model.parse_attack(requested_headers.get(HEADER_ATTACK))
            for a in attack:
                if a['type'] == 'delay':
                    inject.delay(a['value'])

                if a['type'] == 'failure':
                    inject.failure(a['value'])
