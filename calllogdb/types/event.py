import json
from dataclasses import dataclass, field
from typing import Any

from .event_base import EventBase


# Пример реализации кастомных данных
@EventBase.register("custom")
@dataclass
class CustomEvent(EventBase):
    custom_field: str = ""
    custom_value: int = 0

    @classmethod
    def extract_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        init_params.update({"custom_field": data.get("custom_field", ""), "custom_value": data.get("custom_value", 0)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CustomEvent":
        init_params = cls.extract_fields(data)
        return cls(**init_params)


@EventBase.register("timecondition")
@dataclass
class TimeConditionEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TimeConditionEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@EventBase.register("http")
@dataclass
class HTTPEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HTTPEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@EventBase.register("api")
@dataclass
class APIEvent(EventBase):
    api_vars: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def extract_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        raw_api_vars = data.get("event_additional_info", {}).get("api_vars", "{}")
        try:
            # Пробуем привести строку к корректному JSON (заменяем одинарные кавычки на двойные)
            parsed_api_vars = json.loads(raw_api_vars.replace("'", '"'))
        except json.JSONDecodeError:
            parsed_api_vars = {"error": "Failed to parse api_vars"}
        init_params.update({"api_vars": parsed_api_vars})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "APIEvent":
        init_params = cls.extract_fields(data)
        return cls(**init_params)


@EventBase.register("check")
@dataclass
class CheckEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CheckEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@EventBase.register("speech-recog")
@dataclass
class SpeechRecogEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpeechRecogEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@EventBase.register("synthesis")
@dataclass
class SynthesisEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SynthesisEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@EventBase.register("code")
@dataclass
class CodeEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CodeEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@EventBase.register("extnum")
@dataclass
class ExtNumEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExtNumEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
class UnknownEvent(EventBase):
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UnknownEvent":
        init_params = cls.extract_common_fields(data)
        # Сохраняем оставшиеся ключи, которых нет в общих полях
        extra = {k: v for k, v in data.items() if k not in init_params}
        return cls(**init_params, data=extra)
