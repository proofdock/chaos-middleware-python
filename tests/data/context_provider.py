from pdchaos.middleware import core


def default():
    return {
        core.CTX_API_TOKEN: "ey...xz8",
        core.CTX_SERVICE_NAME: "A",
        core.CTX_SERVICE_ID: "1"
    }


def invalid():
    return {
        "xxx": "aaa"
    }
