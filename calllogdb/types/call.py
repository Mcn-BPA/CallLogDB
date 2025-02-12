import dataclasses
import json
from dataclasses import dataclass, field
from typing import Any

from .event_base import EventBase


@dataclass
class Call:
    """
    Класс, представляющий вызов в системе.

    Attributes:
        id (str): Уникальный идентификатор вызова.
        answerdate (str): Время ответа на вызов.
        calldate (str): Время начала вызова.
        endtime (str): Время завершения вызова.
        calltype (str): Тип вызова (например, входящий, исходящий).
        src_type (str): Тип источника вызова.
        call_status (str): Статус вызова.
        hangup_reason (str): Причина завершения вызова.
        dst_type (str): Тип назначения вызова.
        dst_num (str): Номер назначения.
        dst_name (str): Имя назначения.
        did (str): DID номер.
        did_num (str): Номер DID.
        src_name (str): Имя источника вызова.
        src_num (str): Номер источника вызова.
        total_time (int): Общее время вызова в секундах.
        wait_time (int): Время ожидания в секундах.
        talk_time (int): Время разговора в секундах.
        events_count (int): Количество событий, связанных с вызовом.
        transfered_linked_to (bool): Флаг, указывающий, был ли вызов переведен.
        vpbx_id (int): Идентификатор виртуальной АТС.
        events (list[EventBase]): Список событий, связанных с вызовом.
    """

    id: str = ""
    answerdate: str = ""
    calldate: str = ""
    endtime: str = ""
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
    events: list[EventBase] = field(default_factory=list)

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
        call_fields: set[str] = {field.name for field in dataclasses.fields(cls)}

        # Фильтруем только допустимые поля
        filtered_data = {k: v for k, v in data.items() if k in call_fields}

        return cls(
            events=[EventBase.from_dict(ed) for ed in events_data],
            **filtered_data,  # Передаем только валидные атрибуты
        )


# пример для тестов работоспособности
if __name__ == "__main__":
    with open("test.json", "r", encoding="utf-8") as file:
        call_data = json.load(file)
    call = Call.from_dict(call_data)
    print(call)
