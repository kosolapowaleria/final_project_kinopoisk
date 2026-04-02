import requests
import allure
from config import API_BASE_URL, API_TOKEN, API_VERSION, API_TIMEOUT


class BaseAPI:
    """Базовый класс для API‑клиентов."""

    def __init__(self):
        """Инициализация с настройками из конфигурации."""
        self.base_url = f'{API_BASE_URL}/{API_VERSION}'
        self.headers = {
            'X-API-KEY': API_TOKEN,
            'Content-Type': 'application/json'
        }

    @allure.step('Выполнение GET-запроса к {endpoint}')
    def get(self, endpoint, params=None, api_version=None):
        """
        Выполнение GET‑запроса с логированием в Allure.

        :param endpoint: str — эндпоинт API
        :param params: dict — параметры запроса (опционально)
        :param api_version: str — версия API для этого запроса (опционально)
        :return: requests.Response — ответ сервера
        """
        if api_version:
            base_url = f'{API_BASE_URL}/{api_version}'
        else:
            base_url = self.base_url

        url = f'{base_url}/{endpoint.lstrip("/")}'

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=API_TIMEOUT
        )

        return response
