from dataclasses import dataclass
from typing import Any, Callable, ClassVar, TypeVar

T = TypeVar("T", bound="EventBase")


# Базовый класс для событий с 5 общими полями
@dataclass
class EventBase:
    """
    Базовый класс events

    Этот класс используется для представления событий различного типа,
    а также предоставляет механизм регистрации подклассов и создания
    экземпляров на основе переданных данных

    Args:
        event_type (str): Тип события
    """

    event_type: str

    # Реестр для регистрации подклассов по event_type
    _registry: ClassVar[dict[str, type["EventBase"]]] = {}

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
            >>> @EventBase.register("timecondition")
            ... @dataclass
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
        if etype not in cls._registry:
            raise ValueError(f"Неизвестный тип события: {etype}")
        return cls._registry[etype].from_dict(data)
