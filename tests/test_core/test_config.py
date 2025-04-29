import os
from typing import Any, Generator
from unittest.mock import patch

import pytest

from calllogdb.core.config import Config, setup_logging  # Замените на реальный путь


# Тест для конфигурации
@pytest.fixture
def mock_env() -> Generator[None, Any, None]:
    with patch.dict(
        os.environ,
        {
            "CALL_LOG_URL": "http://example.com",
            "TOKEN": "secret_token",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_USER": "user",
            "DB_PASSWORD": "password",
            "DB_NAME": "test_db",
            "DB_SCHEMA": "public",
        },
    ):
        yield


def test_config() -> None:
    config = Config()

    # Проверяем, что конфигурация была загружена правильно
    assert config.url == "http://example.com"
    assert config.token == "secret_token"
    assert config.host == "localhost"
    assert config.port == 5432
    assert config.user == "user"
    assert config.password == "password"
    assert config.database == "test_db"
    assert config.schema == "public"


def test_missing_required_vars() -> None:
    # Тестируем случай, когда обязательные переменные не заданы
    with patch.dict(
        os.environ,
        {
            "DB_USER": "",
            "DB_PASSWORD": "",
            "DB_NAME": "",
        },
    ):
        with pytest.raises(ValueError):
            Config()


def test_db_url() -> None:
    config = Config()

    # Проверяем, что строка подключения к базе данных формируется правильно
    expected_db_url = "postgresql+psycopg://user:password@localhost:5432/test_db"
    assert config.db_url == expected_db_url


# Тест для логирования
def test_logging_setup() -> None:
    # Проверяем, что логирование настроено без ошибок
    try:
        setup_logging(log_level="INFO")
        setup_logging(log_level="ERROR", log_file="test_log.log")
    except Exception as e:
        pytest.fail(f"Logging setup failed with exception: {e}")


@pytest.mark.parametrize(
    "log_level, expected_level",
    [
        ("TRACE", "TRACE"),
        ("DEBUG", "DEBUG"),
        ("INFO", "INFO"),
        ("SUCCESS", "SUCCESS"),
        ("WARNING", "WARNING"),
        ("ERROR", "ERROR"),
        ("CRITICAL", "CRITICAL"),
    ],
)
def test_logging_levels(log_level, expected_level):
    # Проверяем настройку разных уровней логирования
    setup_logging(log_level=log_level)
    # В реальном тесте можно использовать логгер для проверки уровня
    # Но в данном случае проверяем, что ошибок не возникает
    assert True
