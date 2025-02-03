class Events:
    _registry = {}

    def __init__(self, type: str):
        self.type = type

    @classmethod
    def register(cls, type: str):
        """
        Декоратор для регистрации подклассов в реестр.
        """
        def wrapper(subclass):
            cls._registry[type] = subclass
            return subclass
        return wrapper

    @classmethod
    def from_dict(cls, data: dict):
        """
        Фабричный метод для создания экземпляров классов по типу.
        """
        type = data["type"]
        if type not in cls._registry:
            raise ValueError(f"Неизвестный тип события: {type}")
        return cls._registry[type].from_dict(data)
