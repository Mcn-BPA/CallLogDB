from typing import Any, Optional, cast

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from calllogdb.core import config


class APIClient:
    def __init__(self, url: str = config.url, token: str = config.token):
        """
        Инициализация клиента для работы с API.
        """
        self.url = url
        self.token = token
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            }
        )

        # Настройка повторных попыток при неудачных запросах
        retries = Retry(
            total=1,
            backoff_factor=1.0,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "OPTIONS", "HEAD"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        Отправляет GET-запрос с указанными параметрами и возвращает результат в формате JSON.
        """
        try:
            response = self.session.get(self.url, params=params)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except requests.RequestException:
            return {}

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "APIClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> bool | None:
        self.close()
        return None


# Пример использования
if __name__ == "__main__":
    params = {
        "date_from": "2025-02-12 10:00:00",
        "date_to": "2025-02-12 12:00:00",
        "request_detailed": "1",
        "limit": 1000,
        "offset": 0,
    }
    # GET-запрос
    with APIClient() as api:
        response = api.get(params=params)
        pass
