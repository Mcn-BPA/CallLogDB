import os
import sys
from dataclasses import dataclass, field
from typing import Literal

from dotenv import load_dotenv
from loguru import logger

# Загружаем переменные окружения из .env
load_dotenv()


@dataclass(frozen=True)
class Config:
    # GET
    url: str = field(default_factory=lambda: os.getenv("CALL_LOG_URL", ""))
    token: str = field(default_factory=lambda: os.getenv("TOKEN", ""))

    # DB
    host: str = field(default_factory=lambda: os.getenv("DB_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("DB_PORT", 5432)))
    user: str = field(default_factory=lambda: os.getenv("DB_USER", ""))
    password: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", ""))
    database: str = field(default_factory=lambda: os.getenv("DB_NAME", ""))
    schema: str = field(default_factory=lambda: os.getenv("DB_SCHEMA", ""))

    # LOG
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    def __post_init__(self) -> None:
        # Проверяем, что обязательные переменные заданы
        missing = []
        if not self.user:
            missing.append("DB_USER")
        if not self.password:
            missing.append("DB_PASSWORD")
        if not self.database:
            missing.append("DB_NAME")
        if missing:
            raise ValueError(
                f"""Отсутствуют обязательные переменные конфигурации: {", ".join(missing)}.
                Проверьте наличие файла .env и его содержимое."""
            )

    @property
    def db_url(self) -> str:
        """
        Формирует строку подключения к базе данных.
        """
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


def setup_logging(
    log_level: Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"] = "ERROR",
    log_file: str | None = None,
) -> None:
    logger.remove()

    if log_file:
        logger.add(log_file, rotation="1 MB", retention="7 days", compression="zip", level=log_level)
    else:
        logger.add(sys.stderr, level=log_level)
