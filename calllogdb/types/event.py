import json
from typing import Any, Dict, Optional
from .events import Events


@Events.register("blacklist")
class BlacklistEvent(Events):
    def __init__(self, **kwargs):
        super().__init__("blacklist", **kwargs)

    @staticmethod
    def from_dict(data: dict):
        return BlacklistEvent(**data)


@Events.register("timecondition")
class TimeConditionEvent(Events):
    def __init__(self, **kwargs):
        super().__init__("timecondition", **kwargs)

    @staticmethod
    def from_dict(data: dict):
        return TimeConditionEvent(**data)


@Events.register("api")
class APIEvent(Events):
    def __init__(self, api_vars: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__("api", **kwargs)
        self.api_vars = api_vars or {}

    @staticmethod
    def parse_api_vars(api_vars_str: str) -> Dict[str, Any]:
        """Безопасное преобразование api_vars из строки в словарь."""
        try:
            # Исправляем возможные ошибки в JSON (например, одинарные кавычки)
            api_vars_str = api_vars_str.replace("'", "\"")
            return json.loads(api_vars_str)
        except json.JSONDecodeError:
            return {"error": "Failed to parse api_vars"}

    @staticmethod
    def from_dict(data: dict):
        """Создает объект APIEvent, парся api_vars."""
        raw_api_vars = data.get("event_additional_info",
                                {}).get("api_vars", "{}")
        parsed_api_vars = APIEvent.parse_api_vars(raw_api_vars)
        return APIEvent(api_vars=parsed_api_vars, **data)


@Events.register("check")
class CheckEvent(Events):
    def __init__(self, **kwargs):
        super().__init__("check", **kwargs)

    @staticmethod
    def from_dict(data: dict):
        return CheckEvent(**data)


@Events.register("speech-recog")
class SpeechRecogEvent(Events):
    def __init__(self, **kwargs):
        super().__init__("speech-recog", **kwargs)

    @staticmethod
    def from_dict(data: dict):
        return SpeechRecogEvent(**data)


@Events.register("synthesis")
class SynthesisEvent(Events):
    def __init__(self, **kwargs):
        super().__init__("synthesis", **kwargs)

    @staticmethod
    def from_dict(data: dict):
        return SynthesisEvent(**data)


@Events.register("code")
class CodeEvent(Events):
    def __init__(self, **kwargs):
        super().__init__("code", **kwargs)

    @staticmethod
    def from_dict(data: dict):
        return CodeEvent(**data)


@Events.register("extnum")
class ExtNumEvent(Events):
    def __init__(self, **kwargs):
        super().__init__("extnum", **kwargs)

    @staticmethod
    def from_dict(data: dict):
        return ExtNumEvent(**data)


class UnknownEvent(Events):
    """Обрабатывает события с неизвестным типом."""

    def __init__(self, event_type: str, **kwargs):
        super().__init__(event_type, **kwargs)

    @staticmethod
    def from_dict(data: dict):
        return UnknownEvent(event_type=data.get("event_type", "unknown"), **data)
