"""
Файл для создания модуля программы
"""

from .config import Config, _setup_logging

config = Config()
DB_URL: str = config.db_url

__all__ = ["Config", "config", "DB_URL", "_setup_logging"]
