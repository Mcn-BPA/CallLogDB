from typing import Any, Callable, Type, TypeVar

T = TypeVar("T", bound="Events")  # Тип-потомок Events


class Events:
    """_summary_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    _registry: dict[str, Type["Events"]] = {}  # ✅ Явно указываем тип хранимых классов

    def __init__(self, event_type: str, **kwargs: Any) -> None:
        self.event_type = event_type  # ☝🤓 Тип события
        self.event_end_time = kwargs.get("event_end_time", "")  # ☝🤓 Дата и время окончания события
        self.event_talk_time = kwargs.get("event_talk_time", "")  # ☝🤓 Время разговора в событии
        self.event_wait_time = kwargs.get("event_wait_time", "")  # ☝🤓 Время ожидания в событии
        self.event_start_time = kwargs.get("event_start_time", "")  # ☝🤓 Дата и время начала события
        self.event_total_time = kwargs.get("event_total_time", "")  # ☝🤓 Общее время события
        self.event_answer_time = kwargs.get("event_answer_time", "")  # ☝🤓 Время до ответа на звонок
        self.event_rec_filename = kwargs.get("event_rec_filename", "")  # ☝🤓 Имя файла записи разговора
        self.event_transfered_from = kwargs.get("event_transfered_from", "")  # ☝🤓 Номер, с которого был переадресован
        self.event_leg_link_uniqueid_orig = kwargs.get(
            "event_leg_link_uniqueid_orig", ""
        )  # ☝🤓 Ссылка на ветвь события uniqueid orig

    @classmethod
    def register(cls, event_type: str) -> Callable[[Type[T]], Type[T]]:
        """Декоратор для регистрации подклассов в реестр."""

        def wrapper(subclass: Type[T]) -> Type[T]:  # ✅ subclass — это подкласс Events
            cls._registry[event_type] = subclass
            return subclass

        return wrapper

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Events":
        """Фабричный метод для создания экземпляров классов по типу."""
        event_type = data["type"]
        if event_type not in cls._registry:
            raise ValueError(f"Неизвестный тип события: {event_type}")
        return cls._registry[event_type].from_dict(data)
