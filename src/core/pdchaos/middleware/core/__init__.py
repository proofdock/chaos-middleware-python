import threading
from concurrent.futures.thread import ThreadPoolExecutor

HEADER_ATTACK = "x-proofdock-attack"

# Attack actions keys
ATTACK_KEY_ACTIONS = "actions"
ATTACK_KEY_ACTION_NAME = "name"
ATTACK_KEY_VALUE = "value"
ATTACK_KEY_ROUTE = "route"
ATTACK_ACTION_FAULT = "fault"
ATTACK_ACTION_DELAY = "delay"
ATTACK_KEY_PROBABILITY = "probability"

# Target keys
ATTACK_KEY_TARGET = "target"
ATTACK_KEY_TARGET_APPLICATION = "application"


def call_repeatedly(interval, func, *args):
    stopped = threading.Event()

    def loop():
        while not stopped.wait(interval):
            func(*args)

    future = ThreadPoolExecutor(max_workers=1).submit(loop)
    return stopped.set, future
