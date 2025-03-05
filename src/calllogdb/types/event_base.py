import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Callable, ClassVar, TypeVar

from calllogdb.utils import _parse_datetime, _parse_timedelta_seconds

T = TypeVar("T", bound="EventBase")


# Базовый класс для событий с общими полями
@dataclass
class EventBase:
    """
    Базовый класс events

    Этот класс используется для представления событий различного типа,
    а также предоставляет механизм регистрации подклассов и создания
    экземпляров на основе переданных данных

    Args:
        event_type (str): Тип события
        event_status (str): Статус
        event_dst_num (str): Сокращённый номер
        event_dst_type (str): Тип события
        event_start_time (datetime): Дата и время начала события
        event_end_time (datetime): Дата и время окончания события
        event_talk_time (timedelta): Время разговора в событии
        event_wait_time (timedelta): Время ожидания в событии
        event_total_time (timedelta): Общее время события
    """

    event_type: str
    event_status: str
    event_dst_num: str
    event_dst_type: str
    event_transfered_from: str
    event_start_time: datetime | None
    event_end_time: datetime | None
    event_talk_time: timedelta | None
    event_wait_time: timedelta | None
    event_total_time: timedelta | None

    # Реестр для регистрации подклассов по event_type
    _registry: ClassVar[dict[str, type["EventBase"]]] = {}

    @staticmethod
    def string_from_dict(string: str | None) -> dict[str, str]:
        if string is None:
            return {}
        cleaned_string: str = re.sub(r"[{}()\[\]']", "", string)
        pairs: list[str] = [pair.strip() for pair in cleaned_string.split(",") if ":" in pair]

        result_dict: dict[str, str] = {}
        for pair in pairs:
            key, value = map(str.strip, pair.split(":", maxsplit=1))
            result_dict[key] = value
        return result_dict

    @classmethod
    def register(cls, event_type: str) -> Callable[[type[T]], type[T]]:
        """Декоратор для регистрации подклассов событий.

        Позволяет автоматически привязывать подклассы событий к их типам,
        что упрощает их создание через `from_dict`.

        Args:
            event_type (str): Тип события, под которым будет зарегистрирован класс.

        Returns:
            Callable ([[Type[T]], Type[T]]): Функция-декоратор для регистрации класса.

        Example:
            >>> @dataclass
            ... @EventBase.register("timecondition")
            ... class TimeConditionEvent(EventBase):
            ...     @classmethod
            ...     def from_dict(cls, data: dict[str, Any]) -> "TimeConditionEvent":
            ...         init_params = cls.extract_common_fields(data)
            ...         return cls(**init_params)
        """

        def wrapper(subcls: type[T]) -> type[T]:
            cls._registry[event_type] = subcls
            return subcls

        return wrapper

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Извлекает общие для всех событий поля."""
        return {
            "event_type": data.get("event_type", ""),
            "event_status": data.get("event_status", ""),
            "event_dst_num": data.get("event_dst_num", ""),
            "event_dst_type": data.get("event_dst_type", ""),
            "event_transfered_from": data.get("event_transfered_from", ""),
            "event_start_time": _parse_datetime(data.get("event_start_time", "")),
            "event_end_time": _parse_datetime(data.get("event_end_time", "")),
            "event_talk_time": _parse_timedelta_seconds(data.get("event_talk_time")),
            "event_wait_time": _parse_timedelta_seconds(data.get("event_wait_time")),
            "event_total_time": _parse_timedelta_seconds(data.get("event_total_time")),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EventBase":
        """
        Создаёт экземпляр события из словаря.

        Использует зарегистрированные подклассы для создания конкретного типа события.

        Args:
            data (dict[str, Any]): Словарь с данными события. Обязательно содержит ключ `"type"`.

        Raises:
            ValueError: Если тип события не зарегистрирован.

        Returns:
            EventBase: Экземпляр соответствующего подкласса.

        Example:
            >>> # предварительно зарегистрируйте подкласс
            >>> data = {
            ...     "event_type": "api",
            ...     "event_start_time": "2025-02-09T10:00:00",
            ...     "event_end_time": "2025-02-09T10:05:00"
            ... }
            >>> event = EventBase.from_dict(data)
            >>> print(EventBase.event_start_time)
            "2025-02-09T10:00:00"
        """
        etype = data.get("event_type", "")
        if etype is None:
            etype = "None"
        if etype not in cls._registry:
            raise ValueError(f"Неизвестный тип события: {etype}")
        return cls._registry[etype].from_dict(data)

    def del_api_vars(self) -> dict[str, Any]:
        data: dict[str, Any] = asdict(self)
        data.pop("api_vars", None)
        return data
