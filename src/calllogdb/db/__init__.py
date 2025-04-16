"""
Файл для создания модуля программы
"""

from .database import CallRepository, init_db

__all__: list[str] = ["CallRepository", "init_db"]
