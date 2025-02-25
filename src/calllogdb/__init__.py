"""
CallLogDB – библиотека для работы с call_log.

Публичный API:
    CallLog – основной класс для работы с call_log.
"""

__version__ = "0.1.0"

from .api import APIClient
from .calllog import CallLog
from .core import Config, config
from .db import CallRepository, init_db
from .types import Call, Calls, EventBase
from .utils import parse_datetime, parse_timedelta_seconds

__all__ = [
    "calllog",
    "APIClient",
    "init_db",
    "Call",
    "Calls",
    "EventBase",
    "CallRepository",
]
