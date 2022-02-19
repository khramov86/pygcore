"""Авторизация."""
import json

import requests

from settings import GCORE_AUTH_URL, API_TIMEOUT, USERNAME, PASSWORD
import time


class GCoreAuth:

    _HEADERS_PART = {'Content-type': 'application/json'}

    def __init__(self, username, password):
        self._gcore_auth = {'username': username, 'password': password}
        self._headers_timestamp = self.headers = None

    def _update_header_timestamp(self):
        self._headers_timestamp = time.time()

    def _auth(self):
        return requests.post(
            GCORE_AUTH_URL,
            data=(json.dumps(self._gcore_auth)),
            headers=self._HEADERS_PART,
        ).json()

    def _check_session_is_valid(self) -> bool:
        """Проверка закончилась ли сессия."""
        result = False
        if not self.headers and not self._headers_timestamp:
            result = False
        elif self._headers_timestamp - time.time() < API_TIMEOUT:
            result = True
        return result

    def get_headers(self) -> dict:
        if not self._check_session_is_valid():
            auth_response = self._auth()
            access = auth_response.get('access', None)
            if not access:
                raise Exception('Ошибка авторизации!')
            self.headers = {
                'Authorization': 'Bearer {}'.format(access),
                **self._HEADERS_PART,
            }
            self._update_header_timestamp()
        return self.headers


gcore_auth = GCoreAuth(USERNAME, PASSWORD)
# Потом можно использовать
# client = gcore_auth.get_headers
# client()

# А пока так:
client = gcore_auth.get_headers()
print(client)






