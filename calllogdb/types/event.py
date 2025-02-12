from dataclasses import dataclass, field
from typing import Any

from .event_base import EventBase


# Пример реализации кастомных данных
@dataclass
@EventBase.register("custom")
class CustomEvent(EventBase):
    custom_field: str = ""
    custom_value: int = 0

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        init_params.update(
            {
                "custom_field": data.get("custom_field", ""),
                "custom_value": data.get("custom_value", 0),
            }
        )
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CustomEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("timecondition")
class TimeConditionEvent(EventBase):
    exten: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        init_params.update({"exten": data.get("event_additional_info", {}).get("exten", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TimeConditionEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("http_request")
class HTTPEvent(EventBase):
    api_vars: dict[str, str] = field(default_factory=dict)

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        raw_api_vars = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HTTPEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("api")
class APIEvent(EventBase):
    api_vars: dict[str, str] = field(default_factory=dict)

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        raw_api_vars = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "APIEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("check")
class CheckEvent(EventBase):
    name: str
    result: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        init_params.update(
            {
                "name": data.get("event_additional_info", {}).get("name", ""),
                "result": data.get("event_additional_info", {}).get("result", ""),
            }
        )
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CheckEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("speech-recog")
class SpeechRecogEvent(EventBase):
    """
    Дата-класс speech-recog хранит элементы вопрос-ответ

    Args:
        question (str): Вопрос
        answer (str | None): Ответ
    """

    question: str
    answer: str | None

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        dialog = data.get("speechkit_dialog", [])
        question = dialog[0].get("dialog_value", "") if dialog else ""
        answer = dialog[-1].get("dialog_value", "") if dialog and len(dialog) > 1 else None
        init_params.update({"question": question, "answer": answer})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpeechRecogEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("synthesis")
class SynthesisEvent(EventBase):
    message: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        init_params.update({"message": data.get("event_additional_info", {}).get("message", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SynthesisEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("code")
class CodeEvent(EventBase):
    api_vars: dict[str, str]

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        raw_api_vars = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CodeEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("extnum")
class ExtNumEvent(EventBase):
    api_vars: dict[str, str] = field(default_factory=dict)

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        raw_api_vars = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExtNumEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("blacklist")
class BlackListEvent(EventBase):
    exten: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        init_params.update({"exten": data.get("event_additional_info", {}).get("exten", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BlackListEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("None")
class NoneEvent(EventBase):
    event_did: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params = super().extract_common_fields(data)
        init_params.update({"event_did": data.get("event_did", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NoneEvent":
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
