from pdchaos.middleware.core.config import AppConfig


def default():
    return {
        AppConfig.PROOFDOCK_API_TOKEN: "ey...xz8",
        AppConfig.APPLICATION_NAME: "A",
        AppConfig.APPLICATION_ID: "1"
    }


def invalid():
    return {
        "xxx": "aaa"
    }
