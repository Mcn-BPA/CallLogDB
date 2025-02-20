from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, ClassVar, TypeVar

T = TypeVar("T", bound="EventBase")

@dataclass
class EventBase:
    event_type: str
    event_status: str
    event_dst_num: str
    event_dst_type: str
    event_transfered_from: str
    event_start_time: datetime | None
    event_end_time: datetime | None
    event_talk_time: int
    event_wait_time: int
    event_total_time: int

    _registry: ClassVar[dict[str, type["EventBase"]]] = {}

    @staticmethod
    def string_from_dict(string: str | None) -> dict[str, str]: ...
    @classmethod
    def register(cls, event_type: str) -> Callable[[type[T]], type[T]]: ...
    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EventBase": ...
