from typing import Dict, List

import marshmallow
from logzero import logger
from pdchaos.middleware.core import model

WARN_MSG = "Invalid chaos attack schema. Skipping attack. Reason: {%s}"


def attack(_input: Dict) -> model.AttackSchema:
    """Parses the attack schema. Returns an empty object if schema is invalid."""
    if not _input:
        return {}
    try:
        result = model.attack_schema.load(_input)
    except marshmallow.ValidationError as x:
        logger.warning(WARN_MSG, x)
        result = {}
    return result


def attack_actions(_input: List[Dict]) -> List[model.AttackActionSchema]:
    """Parses the attack action schema. Returns an empty list if schema is invalid."""
    if not _input:
        return []
    try:
        result = model.attack_actions_schema.load(_input)
    except marshmallow.ValidationError as x:
        logger.warning(WARN_MSG, x)
        result = []
    return result
