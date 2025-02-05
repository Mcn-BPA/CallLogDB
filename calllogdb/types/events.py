from typing import Any, Callable, Type, TypeVar

T = TypeVar("T", bound="Events")  # Тип-потомок Events


class Events:
    _registry: dict[str, Type["Events"]] = {}  # ✅ Явно указываем тип хранимых классов

    def __init__(self, event_type: str) -> None:
        self.event_type = event_type

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
