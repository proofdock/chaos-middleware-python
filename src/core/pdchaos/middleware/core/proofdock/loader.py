import json
import threading
from typing import Callable, Dict

from logzero import logger
from pdchaos.middleware.core.config import AppConfig
from pdchaos.middleware.core.loader import AttackLoader
from pdchaos.middleware.core.proofdock.session import (client_session,
                                                       get_error_message)


class ProofdockAttackLoader(AttackLoader):

    def __init__(self, app_config: AppConfig):
        self._app_config = app_config

    def load(self, set_attack_func: Callable[[Dict], None]):
        self._trigger_load_timer(set_attack_func)

    def _trigger_load_timer(self, set_attack_func: Callable[[Dict], None]):
        threading.Timer(interval=10.0, function=self._load_task, args=(set_attack_func,)).start()

    def _load_task(self, set_attack_func: Callable[[Dict], None]):
        logger.debug("Fetching attack configuration from Proofdock\'s Chaos API ...")
        if not bool(self._app_config.get(AppConfig.API_TOKEN) and self._app_config.get(AppConfig.APPLICATION_NAME)):
            raise Exception('Please set API token and service name')
        with client_session(self._app_config.get(AppConfig.API_TOKEN), verify_tls=False) as session:
            response = self._request(session)
            logger.debug("Fetched attack configuration")
            set_attack_func(response)
        self._trigger_load_timer(set_attack_func)

    def _request(self, session):
        _api_url = self._app_config.get(AppConfig.API_URL, default="https://api.proofdock.io")
        payload = json.dumps({
            "id": self._app_config.get(AppConfig.APPLICATION_ID),
            "env": self._app_config.get(AppConfig.APPLICATION_ENV),
            "name": self._app_config.get(AppConfig.APPLICATION_NAME)
        })
        response = session.post(_api_url + '/v1/attacks/synchronize', data=payload, timeout=13)
        if response.ok:
            return response.json()
        else:
            # to do probaly we should clear attacks here
            raise Exception(get_error_message(response))
