import json
from typing import Callable, Dict

import requests
from circuitbreaker import circuit, CircuitBreakerError
from logzero import logger
from pdchaos.middleware.core.config import AppConfig
from pdchaos.middleware.core.loader import AttackLoader
from pdchaos.middleware.core.proofdock.session import client_session, get_error_message


class ProofdockAttackLoader(AttackLoader):

    def __init__(self, app_config: AppConfig):
        self._app_config = app_config

    def is_allowed_to_call_endpoint(self):
        return bool(
            self._app_config.get(AppConfig.PROOFDOCK_API_TOKEN) and self._app_config.get(AppConfig.APPLICATION_NAME))

    def run(self, set_attacks_action_func: Callable[[Dict], None]):
        with client_session(self._app_config.get(AppConfig.PROOFDOCK_API_TOKEN), verify_tls=False) as session:
            try:
                self._synchronize(session, set_attacks_action_func)
            except CircuitBreakerError:
                self.reset_attack_actions()
            except Exception as e:
                logger.warn(str(e))

    @circuit(expected_exception=(requests.RequestException, requests.ConnectionError, requests.ConnectTimeout),
             failure_threshold=5, recovery_timeout=120)
    def _synchronize(self, session, set_attacks_action_func):
        # Arrange
        timeout_in_seconds = 13
        api_url = self._app_config.get(AppConfig.PROOFDOCK_API_URL, "https://chaosapi.proofdock.io")
        payload = json.dumps({
            "id": self._app_config.get(AppConfig.APPLICATION_ID),
            "env": self._app_config.get(AppConfig.APPLICATION_ENV),
            "name": self._app_config.get(AppConfig.APPLICATION_NAME)
        })

        # Act
        response = session.post(api_url + '/v1/attacks/synchronize', data=payload, timeout=timeout_in_seconds)
        if response.ok:
            attacks = response.json()
            set_attacks_action_func(attacks)
        else:
            raise Exception(get_error_message(response))
