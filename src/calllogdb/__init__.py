"""
CallLogDB – библиотека для работы с call_log.

Публичный API:
    CallLog – основной класс для работы с call_log.
"""

from .api import APIClient
from .calllog import CallLog as calllogdb  # noqa: N813
from .core import Config, setup_logging
from .db import CallRepository
from .types import Call, Calls, EventBase

setup_logging("WARNING")

__all__ = [
    "calllogdb",
    "APIClient",
    "Call",
    "Calls",
    "EventBase",
    "CallRepository",
    "setup_logging",
    "Config",
]
