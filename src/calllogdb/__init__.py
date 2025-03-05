"""
CallLogDB – библиотека для работы с call_log.

Публичный API:
    CallLog – основной класс для работы с call_log.
"""

from .api import APIClient
from .calllog import CallLog as CallLogDB
from .core import Config, config
from .db import CallRepository, init_db
from .types import Call, Calls, EventBase
from .utils import _parse_datetime, _parse_timedelta_seconds

__all__ = [
    "CallLogDB",
    "APIClient",
    "init_db",
    "Call",
    "Calls",
    "EventBase",
    "CallRepository",
]
