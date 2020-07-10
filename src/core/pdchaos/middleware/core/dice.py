import random

from logzero import logger


def roll(input_probability: str) -> bool:
    logger.debug("Initiate '{}'".format(roll.__name__))
    try:
        probability = int(input_probability)
        _min = 1
        _max = 100
        if _min <= probability <= _max:
            rolled_value = random.randint(_min, _max)
            return rolled_value <= probability
        else:
            logger.warn("Skipping probability '{}'. Provided number is out of range. Enter a number between 1 and 100."
                        .format(roll.__name__))
            return False
    except ValueError:
        logger.warn("Skipping probability '{}'. '{}' is not a valid value.".format(roll.__name__, input_probability))
        return False
