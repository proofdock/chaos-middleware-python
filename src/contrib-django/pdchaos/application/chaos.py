import json

from pdchaos.middleware import core


def attack(request):
    headers = request.headers
    attack_request = json.loads(headers.get(core.HEADER_ATTACK)) if (core.HEADER_ATTACK in headers) else None
    attack_context = {core.ATTACK_KEY_ROUTE: request.path}
    core.chaos.attack(attack_request, attack_context)
