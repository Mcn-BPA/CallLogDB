import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

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
    user: str = field(default_factory=lambda: os.getenv("DB_USER", "root"))
    password: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", "root"))
    database: str = field(default_factory=lambda: os.getenv("DB_NAME", "database"))

    # LOG
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    @property
    def db_url(self) -> str:
        """
        Формирует строку подключения к базе данных.
        """
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


# Экземпляр конфигурации
config = Config()

# Теперь можно получить `DB_URL` через `config.db_url`
DB_URL = config.db_url
