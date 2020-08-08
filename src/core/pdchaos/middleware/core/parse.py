from typing import Dict

import marshmallow
from logzero import logger
from pdchaos.middleware.core import model

WARN_MSG = "Invalid chaos attack schema. Skipping attack. Reason: {%s}"


def attack_as_str(_input: str):
    """Parses the attack schema. Returns an empty list if schema is invalid."""
    try:
        result = model.attack_schemas.loads(_input)

    except marshmallow.ValidationError as x:
        logger.warning(WARN_MSG, x)
        result = []

    return result


def attack_as_dict(_input: Dict):
    """Parses the attack schema. Returns an empty list if schema is invalid."""
    try:
        result = model.attack_schemas.load(_input)

    except marshmallow.ValidationError as x:
        logger.warning(WARN_MSG, x)
        result = []

    return result
