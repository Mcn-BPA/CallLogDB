import time
from typing import Any, cast

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from requests.exceptions import ChunkedEncodingError
from urllib3.util.retry import Retry

from calllogdb.core import Config


class APIClient:
    def __init__(self, config: Config, retries_enabled: bool = True, max_manual_retries: int = 3) -> None:
        """
        Инициализация клиента для работы с API.
        """
        self.config: Config = config
        self.url: str = config.url or ""
        self.token: str = config.token or ""
        self.max_manual_retries: int = max_manual_retries
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"{self.token}",
            }
        )

        # Настройка повторных попыток при неудачных запросах по статусу
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

        for attempt in range(1, self.max_manual_retries + 1):
            try:
                response: requests.Response = self.session.get(self.url, params=params, timeout=60)
                response.raise_for_status()
                logger.debug("Получен успешный ответ: {} - {}", response.status_code, response.text[:100])
                return cast(dict[str, Any], response.json())
            except ChunkedEncodingError as e:
                logger.warning("ChunkedEncodingError на попытке {} из {}: {}", attempt, self.max_manual_retries, e)
                if attempt == self.max_manual_retries:
                    logger.error("Достигнуто максимальное количество попыток из-за ChunkedEncodingError.")
                    raise
                time.sleep(2)
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
        return {}

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
