"""
Файл для создания модуля программы
"""

from .config import Config, setup_logging

config = Config()
DB_URL: str = config.db_url

__all__ = ["Config", "config", "DB_URL", "setup_logging"]
