from typing import List


def is_blocked(url_path: str, blocked_url_paths: List[str]) -> bool:
    return any(url_path in blocked for blocked in blocked_url_paths)
