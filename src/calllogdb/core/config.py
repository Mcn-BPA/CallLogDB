import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

DB_URL = "sqlite:///db/database.db"


@dataclass(frozen=True)
class Config:
    # GET
    url: str = field(default_factory=lambda: os.getenv("CALL_LOG_URL", ""))
    token: str = field(default_factory=lambda: os.getenv("TOKEN", ""))
    # DB
    host: str = field(default_factory=lambda: os.getenv("DB_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("DB_PORT", 8080)))
    user: str = field(default_factory=lambda: os.getenv("DB_USER", "root"))
    password: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", "root"))
    # LOG
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))


# Экземпляр настроек, который можно использовать по умолчанию
config = Config()
