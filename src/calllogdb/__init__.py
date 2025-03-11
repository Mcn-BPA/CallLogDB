"""
CallLogDB – библиотека для работы с call_log.

Публичный API:
    CallLog – основной класс для работы с call_log.
"""

from .api import APIClient
from .calllog import CallLog as calllogdb  # noqa: N813
from .core import Config, config, setup_logging
from .db import CallRepository, init_db
from .types import Call, Calls, EventBase
from .utils import _parse_datetime, _parse_timedelta_seconds

setup_logging("WARNING")

__all__ = [
    "calllogdb",
    "APIClient",
    "init_db",
    "Call",
    "Calls",
    "EventBase",
    "CallRepository",
    "setup_logging",
]
