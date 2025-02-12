"""
Файл для создания модуля программы
"""

from .call import Call
from .calls import Calls
from .event import UnknownEvent
from .event_base import EventBase

__all__ = [
    "Call",
    "Calls",
    "EventBase",
    "UnknownEvent",
]
