from typing import Any, Callable, Type, TypeVar

T = TypeVar("T", bound="Events")


class Events:
    """
    Базовый класс для событий.

    Этот класс используется для представления событий различного типа,
    а также предоставляет механизм регистрации подклассов и создания
    экземпляров на основе переданных данных.

    Args:
        event_type (str): Тип события.
        event_start_time (str): Дата и время начала события.
        event_end_time (str): Дата и время окончания события.
        event_talk_time (str): Длительность разговора.
        event_wait_time (str): Время ожидания.
        event_total_time (str): Общее время события.
        event_answer_time (str): Время до ответа.
        event_rec_filename (str): Имя файла записи разговора.
        event_transfered_from (str): Номер, с которого произведена переадресация.
        event_leg_link_uniqueid_orig (str): Уникальный идентификатор исходной ветви события.

    Example:
        >>> # регистрация подкласса
        >>> @Events.register("call")
        ... class CallEvent(Events):
        ...     def __init__(self, **kwargs: Any) -> None:
        ...         super().__init__("call", **kwargs)
        ...
        ...     @classmethod
        ...     def from_dict(cls, data: dict[str, Any]) -> "CallEvent":
        ...         return cls(**data)
        >>>
        >>> data = {
        ...     "type": "call",
        ...     "event_start_time": "2025-02-09T10:00:00",
        ...     "event_end_time": "2025-02-09T10:05:00"
        ... }
        >>> event = Events.from_dict(data)
        >>> print(event.event_start_time)
        "2025-02-09T10:00:00"
    """

    _registry: dict[str, Type["Events"]] = {}

    def __init__(self, event_type: str, **kwargs: Any) -> None:

        self.event_type = event_type
        self.event_start_time = kwargs.get("event_start_time", "")
        self.event_end_time = kwargs.get("event_end_time", "")
        self.event_talk_time = kwargs.get("event_talk_time", "")
        self.event_wait_time = kwargs.get("event_wait_time", "")
        self.event_total_time = kwargs.get("event_total_time", "")
        self.event_answer_time = kwargs.get("event_answer_time", "")
        self.event_rec_filename = kwargs.get("event_rec_filename", "")
        self.event_transfered_from = kwargs.get("event_transfered_from", "")
        self.event_leg_link_uniqueid_orig = kwargs.get("event_leg_link_uniqueid_orig", "")

    @classmethod
    def register(cls, event_type: str) -> Callable[[Type[T]], Type[T]]:
        """
        Декоратор для регистрации подклассов событий.

        Позволяет автоматически привязывать подклассы событий к их типам,
        что упрощает их создание через `from_dict`.

        Args:
            event_type (str): Тип события, под которым будет зарегистрирован класс.

        Returns:
            Callable ([[Type[T]], Type[T]]): Функция-декоратор для регистрации класса.

        Example:
            >>> @Events.register("message")
            ... class MessageEvent(Events):
            ...     def __init__(self, **kwargs: Any) -> None:
            ...         super().__init__("message", **kwargs)
        """

        def wrapper(subclass: Type[T]) -> Type[T]:
            cls._registry[event_type] = subclass
            return subclass

        return wrapper

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Events":
        """
        Создаёт экземпляр события из словаря.

        Использует зарегистрированные подклассы для создания конкретного типа события.

        Args:
            data (dict[str, Any]): Словарь с данными события. Обязательно содержит ключ `"type"`.

        Raises:
            ValueError: Если тип события не зарегистрирован.

        Returns:
            Events: Экземпляр соответствующего подкласса.

        Example:
            >>> # предварительно зарегистрируйте подкласс
            >>> data = {
            ...     "type": "call",
            ...     "event_start_time": "2025-02-09T10:00:00",
            ...     "event_end_time": "2025-02-09T10:05:00"
            ... }
            >>> event = Events.from_dict(data)
            >>> print(event.event_start_time)
            "2025-02-09T10:00:00"
        """
        event_type = data.get("type")
        if event_type not in cls._registry:
            raise ValueError(f"Неизвестный тип события: {event_type}")
        return cls._registry[event_type].from_dict(data)
