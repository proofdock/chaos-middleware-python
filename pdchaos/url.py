from typing import List


def is_blocked(url: str, blocked_urls: List[str]) -> bool:
    return any(url in blocked for blocked in blocked_urls)
