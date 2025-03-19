from dataclasses import asdict, dataclass, field, fields
from datetime import datetime, timedelta
from typing import Any

from calllogdb.utils import _parse_datetime

from .event_base import EventBase

_ALIASES: dict[str, str] = {
    "callid": "call_id",
    "date": "call_date",
    "end_date": "end_time",
    "talktime": "talk_time",
    "waittime": "wait_time",
    "billsec": "total_time",
    "status": "call_status",
    "type": "call_type",
}


@dataclass
class Call:
    """
    Класс типа звонка
    """

    call_id: str
    call_status: str | None = None
    call_type: str | None = None
    did: str | None = None
    dst_num: str | None = None
    dst_name: str | None = None
    dst_type: str | None = None
    src_name: str | None = None
    src_num: str | None = None
    src_type: str | None = None
    hangup_reason: str | None = None
    answer_date: datetime | None = None
    call_date: datetime | None = None
    end_time: datetime | None = None
    events_count: int | None = None
    total_time: timedelta | None = None
    wait_time: timedelta | None = None
    talk_time: timedelta | None = None
    vpbx_id: int | None = None
    transfered_linked_to: bool = False
    events: list["EventBase"] = field(default_factory=list)

    def __post_init__(self) -> None:
        pass

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Call":
        """
        Создает объект Call из словаря.

        Args:
            data (dict[str, Any]): Словарь с данными о вызове.

        Returns:
            Call: Объект вызова, созданный из переданных данных.

        Example:
            >>> call_data: dict[str, Any] = {
            ...     "id": "123",
            ...     "calldate": "2024-02-10 12:30:00",
            ...     "total_time": 120,
            ...     "events": [{"event_type": "answered", "timestamp": "2024-02-10 12:30:05"}]
            ... }
            >>> call = Call.from_dict(call_data)
            >>> print(call.id)
            123
        """
        call_fields: set[str] = {field.name for field in fields(cls)}

        # Переименовываем ключи, если они есть в ALIASES
        mapped_data: dict[str, Any] = {_ALIASES.get(k, k): v for k, v in data.items()}
        # удаляем events чтобы он не попал в filtered_data
        events_data = mapped_data.pop("events", [])

        # Конвертируем даты
        for date_field in ["answer_date", "call_date", "end_time"]:
            if date_field in mapped_data:
                mapped_data[date_field] = _parse_datetime(mapped_data[date_field])

        # Конвертируем временные интервалы
        for time_field in ["total_time", "wait_time", "talk_time"]:
            if time_field in mapped_data:
                mapped_data[time_field] = timedelta(seconds=int(mapped_data[time_field]))

        # Фильтруем только допустимые поля
        filtered_data: dict[str, Any] = {k: v for k, v in mapped_data.items() if k in call_fields}

        return cls(
            events=[EventBase.from_dict(ed) for ed in events_data],
            **filtered_data,
        )

    def del_events(self) -> dict[str, Any]:
        data: dict[str, Any] = asdict(self)
        data.pop("events", None)
        return data
