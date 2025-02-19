"""
CallLogDB – библиотека для работы с call_log.

Публичный API:
    CallLog – основной класс для работы с call_log.
"""

__version__ = "0.1.0"

from .api import APIClient
from .call_log import CallLog
from .core import Config, config
from .db import Database
from .types import Call, Calls, EventBase
from .utils import parse_datetime

__all__ = [
    "CallLog",
    "APIClient",
    "Call",
    "Calls",
    "EventBase",
    "Database",
]
