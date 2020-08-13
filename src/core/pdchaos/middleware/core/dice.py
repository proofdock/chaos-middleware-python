import random

from logzero import logger


def roll(input_probability: str) -> bool:
    _min = 1
    _max = 100
    err_msg = "Skipping probability. Provided value '{}' is {}. Enter a number from 1 to 100."

    if not input_probability:
        return True

    try:
        probability = int(input_probability)

        if probability == 100:
            return True
        elif _min <= probability <= _max:
            rolled_value = random.randint(_min, _max)
            return rolled_value <= probability
        else:
            logger.warning(err_msg.format(probability, "out of range"))
            return False
    except ValueError:
        logger.warning(err_msg.format(input_probability, "invalid"))
        return False
