from contextlib import contextmanager
from typing import Generator

from requests import Session


@contextmanager
def client_session(api_token: str, verify_tls: bool = True) -> Generator[Session, None, None]:
    # prepare auth token
    headers = {
        "Authorization": "Bearer {}".format(api_token),
    }

    with Session() as s:
        s.headers.update(headers)
        s.verify = verify_tls
        yield s


def get_error_message(response):
    message = "Server response: {}".format(response.status_code)

    if response.status_code == 404:
        message = "Resource not found. {}".format(message)

    return message
