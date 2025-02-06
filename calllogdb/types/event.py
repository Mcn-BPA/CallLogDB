import json
from typing import Any, Optional, cast

from .events import Events


@Events.register("blacklist")
class BlacklistEvent(Events):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("blacklist", **kwargs)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "BlacklistEvent":
        return BlacklistEvent(**data)


@Events.register("timecondition")
class TimeConditionEvent(Events):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("timecondition", **kwargs)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "TimeConditionEvent":
        return TimeConditionEvent(**data)


@Events.register("http")
class HTTPEvent(Events):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("http", **kwargs)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "HTTPEvent":
        return HTTPEvent(**data)


@Events.register("api")
class APIEvent(Events):
    def __init__(self, api_vars: Optional[dict[str, Any]] = None, **kwargs: Any) -> None:
        super().__init__("api", **kwargs)
        self.api_vars = api_vars or {}

    @staticmethod
    def parse_api_vars(api_vars_str: str) -> dict[str, Any]:
        """Безопасное преобразование api_vars из строки в словарь."""
        try:
            # Исправляем возможные ошибки в JSON (например, одинарные кавычки)
            api_vars_str = api_vars_str.replace("'", '"')
            return cast(dict[str, Any], json.loads(api_vars_str))
        except json.JSONDecodeError:
            return {"error": "Failed to parse api_vars"}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "APIEvent":
        """Создает объект APIEvent, парся api_vars."""
        raw_api_vars = data.get("event_additional_info", {}).get("api_vars", "{}")
        parsed_api_vars = APIEvent.parse_api_vars(raw_api_vars)
        return APIEvent(api_vars=parsed_api_vars, **data)


@Events.register("check")
class CheckEvent(Events):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("check", **kwargs)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "CheckEvent":
        return CheckEvent(**data)


@Events.register("speech-recog")
class SpeechRecogEvent(Events):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("speech-recog", **kwargs)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "SpeechRecogEvent":
        return SpeechRecogEvent(**data)


@Events.register("synthesis")
class SynthesisEvent(Events):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("synthesis", **kwargs)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "SynthesisEvent":
        return SynthesisEvent(**data)


@Events.register("code")
class CodeEvent(Events):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("code", **kwargs)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "CodeEvent":
        return CodeEvent(**data)


@Events.register("extnum")
class ExtNumEvent(Events):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("extnum", **kwargs)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ExtNumEvent":
        return ExtNumEvent(**data)


class UnknownEvent(Events):
    """Обрабатывает события с неизвестным типом."""

    def __init__(self, event_type: str = "unknown", **kwargs: Any):
        super().__init__(event_type)
        self.data = kwargs

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "UnknownEvent":
        return UnknownEvent(event_type=data.get("event_type", "unknown"), **data)
