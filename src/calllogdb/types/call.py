from dataclasses import field, fields
from datetime import datetime
from typing import Any

from icecream import ic
from pydantic import Field
from pydantic.dataclasses import dataclass

from calllogdb.utils import parse_datetime

from .event_base import EventBase

ic.disable()


@dataclass
class Call:
    """
    Класс типа звонка
    """

    call_id: str = Field("", alias="callid")
    call_date: datetime | None = Field(None, alias="date")
    answer_date: datetime | None = Field(None, alias="answer_date")
    end_time: datetime | None = Field(None, alias="end_date")
    call_type: str | None = Field(None, alias="type")
    src_type: str | None = Field(None, alias="src_type")
    call_status: str | None = Field(None, alias="status")
    hangup_reason: str | None = Field(None, alias="hangup_reason")
    dst_type: str | None = Field(None, alias="dst_type")
    dst_num: str | None = Field(None, alias="dst_num")
    dst_name: str | None = Field(None, alias="dst_name")
    did: str | None = Field(None, alias="did")
    did_num: str | None = Field(None, alias="did_num")
    src_name: str | None = Field(None, alias="src_name")
    src_num: str | None = Field(None, alias="src_num")
    total_time: int | None = Field(None, alias="billsec")
    wait_time: int | None = Field(None, alias="waittime")
    talk_time: int | None = Field(None, alias="talktime")
    events_count: int | None = Field(None, alias="events_count")
    transfered_linked_to: bool = Field(False, alias="transfered_linked_to")
    vpbx_id: int | None = Field(None, alias="vpbx_id")
    events: list[EventBase] = field(default_factory=list, metadata={"alias": "events"})

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
        for date_field in ["answer_date", "date", "end_date"]:
            data[date_field] = parse_datetime(data[date_field])

        # Фильтруем только допустимые поля
        filtered_data = {k: v for k, v in data.items() if k in call_fields}
        ic(list(filtered_data.keys()))
        ic(len(list(filtered_data.keys())))
        return cls(
            events=[EventBase.from_dict(ed) for ed in events_data],
            **filtered_data,
        )
