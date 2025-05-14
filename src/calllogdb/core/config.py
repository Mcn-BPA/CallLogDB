import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml
from dotenv import load_dotenv
from loguru import logger

# Загружаем переменные окружения из .env
load_dotenv()


@dataclass(slots=True)
class Config:
    # --- API ---
    url: str | None = None
    token: str | None = None

    # --- DB ---
    host: str | None = None
    port: int | None = None
    user: str | None = None
    password: str | None = None
    database: str | None = None
    schema: str | None = None

    # --- FLAG ---
    ls_number: str | None = None

    # --- NEW ---
    _profile: str = field(default="default", repr=False)  # имя секции YAML
    _source: str = field(default="env", repr=False)  # env | yaml

    # ---------- Инициализация из ENV ----------
    def __post_init__(self) -> None:
        if self._source == "env":
            self.url = self.url or os.getenv("URL")
            self.token = self.token or os.getenv("TOKEN")
            self.host = self.host or os.getenv("HOST", "localhost")
            self.port = self.port or int(os.getenv("PORT", 5432))
            self.user = self.user or os.getenv("USER")
            self.database = self.database or os.getenv("DATABASE")
            self.password = self.password or os.getenv("PASSWORD")
            self.schema = self.schema or os.getenv("SCHEMA", "public")
            self.ls_number = self.ls_number or os.getenv("LS_NUMBER")

        missing: list[str] = [n for n in ("user", "password", "database") if not getattr(self, n)]
        if missing:
            raise ValueError(f"Отсутствуют ключевые параметры: {', '.join(missing)}")

    # ---------- Инициализация из YAML ----------
    @classmethod
    def from_yaml(
        cls,
        path: str | os.PathLike[str],
        profile: str = "default",
    ) -> "Config":
        data: dict[str, Any] = yaml.safe_load(Path(path).read_text())
        if profile not in data:
            raise KeyError(f"В YAML нет секции «{profile}»")
        values = data[profile]
        # плоская структура или «db: …» — обрабатываем обе
        if "db" in values:
            values = {**values, **values.pop("db")}
        return cls(_profile=profile, _source="yaml", **values)

    # ---------- Удобная строка подключения ----------
    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


def setup_logging(
    log_level: Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"] = "ERROR",
    log_file: str | None = None,
) -> None:
    logger.remove()

    if log_file:
        log_dir: str = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        # ---------- Установка времени миграции логов ----------
        logger.add(
            log_file,
            rotation="00:00",  # Ротация каждый день в полночь
            retention="7 days",  # Храним 7 дней логи
            compression="zip",  # Архивируем старые логи
            level=log_level,
            enqueue=True,  # Логируем через очередь
            backtrace=True,  # Красивый полный traceback при ошибках
            diagnose=True,  # Подробный вывод локальных переменных при ошибках
        )
    else:
        logger.add(sys.stderr, level=log_level, backtrace=True, diagnose=True)
