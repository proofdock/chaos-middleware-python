from typing import List

from pdchaos.middleware.core import url, inject


def execute_chaos(called_path: str, blocked_paths: List[str], requested_headers: dict, injections: dict):
    """Execute chaos"""
    if blocked_paths and url.is_blocked(called_path, blocked_paths):
        return

    if injections and injections.get('delay'):
        inject.delay(injections.get('delay').get('duration'))

    if injections and injections.get('exception'):
        inject.raise_exception(injections.get('exception'))
