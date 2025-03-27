from typing import Any, cast

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from calllogdb.core import config


class APIClient:
    def __init__(self, url: str = config.url, token: str = config.token, retries_enabled: bool = True) -> None:
        """
        Инициализация клиента для работы с API.
        """
        self.url: str = url
        self.token: str = token
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"{self.token}",
            }
        )

        # Настройка повторных попыток при неудачных запросах
        if retries_enabled:
            retries = Retry(
                total=5,
                backoff_factor=1.0,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["GET", "OPTIONS", "HEAD"],
            )
            adapter = HTTPAdapter(max_retries=retries)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

        logger.info("APIClient инициализирован с URL: {}", self.url)

    def get(self, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Отправляет GET-запрос с указанными параметрами и возвращает результат в формате JSON.
        """
        logger.debug("Отправка GET-запроса к {} с параметрами: {}", self.url, params)
        try:
            response: requests.Response = self.session.get(self.url, params=params)
            response.raise_for_status()
            logger.debug("Получен успешный ответ: {} - {}", response.status_code, response.text[:100])
            return cast(dict[str, Any], response.json())
        except requests.Timeout:
            logger.error("Таймаут запроса к {}", self.url)
            return {}
        except requests.HTTPError as e:
            logger.error("HTTP ошибка при GET-запросе: {}", e)
            if e.response is not None and e.response.status_code in [500, 502, 503, 504]:
                return {}
            raise
        except requests.RequestException as e:
            logger.error("Ошибка запроса: {}", e)
            raise e

    def close(self) -> None:
        logger.info("Закрытие сессии APIClient")
        self.session.close()

    def __enter__(self) -> "APIClient":
        logger.debug("Вход в контекстный менеджер APIClient")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> bool | None:
        if exc_type:
            logger.error("Исключение в контекстном менеджере APIClient: {}: {}", exc_type, exc_value)
        logger.debug("Выход из контекстного менеджера APIClient")
        self.close()
        return None
