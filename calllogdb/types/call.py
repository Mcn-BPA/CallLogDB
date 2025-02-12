import json
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import Any

from calllogdb.utils import parse_datetime

from .event_base import EventBase


@dataclass
class Call:
    """
    Класс типа звонка

    """

    id: str = ""
    answerdate: datetime | None = None
    calldate: datetime | None = None
    endtime: datetime | None = None
    calltype: str = ""
    src_type: str = ""
    call_status: str = ""
    hangup_reason: str = ""
    dst_type: str = ""
    dst_num: str = ""
    dst_name: str = ""
    did: str = ""
    did_num: str = ""
    src_name: str = ""
    src_num: str = ""
    total_time: int = 0
    wait_time: int = 0
    talk_time: int = 0
    events_count: int = 0
    transfered_linked_to: bool = False
    vpbx_id: int = 0
    events: list["EventBase"] = field(default_factory=list)

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
        events_data = data.pop("events", [])  # Извлекаем события

        call_fields: set[str] = {field.name for field in fields(cls)}

        # Преобразуем строки в `datetime`
        for date_field in ["answerdate", "calldate", "endtime"]:
            data[date_field] = parse_datetime(data[date_field])

        # Фильтруем только допустимые поля
        filtered_data = {k: v for k, v in data.items() if k in call_fields}

        return cls(
            events=[EventBase.from_dict(ed) for ed in events_data],
            **filtered_data,
        )


# Пример для тестов работоспособности
if __name__ == "__main__":
    with open("test.json", "r", encoding="utf-8") as file:
        call_data = json.load(file)

    call = Call.from_dict(call_data)
    pass
