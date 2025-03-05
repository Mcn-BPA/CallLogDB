"""
Файл для создания модуля программы
"""

from .config import Config

config = Config()
DB_URL: str = config.db_url

__all__ = ["Config", "config", "DB_URL"]
