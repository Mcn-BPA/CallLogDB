from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from calllogdb.utils import _parse_datetime

from .event_base import EventBase


# Пример реализации кастомных данных
@dataclass
@EventBase.register("announce")
class AnnounceEvent(EventBase):
    """Приветствие"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AnnounceEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("hangup")
class HangupEvent(EventBase):
    """Повесить трубку"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HangupEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("ivr")
class IvrEvent(EventBase):
    """Сценарий звонков"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IvrEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("gpt")
class GptEvent(EventBase):
    """ИИ"""

    api_vars: dict[str, str]

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        raw_api_vars: str | None = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GptEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("robocall_task")
class RobocallTaskEvent(EventBase):
    """Авто-звонки"""

    api_vars: dict[str, str]

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        raw_api_vars: str | None = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RobocallTaskEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("menu")
class MenuEvent(EventBase):
    """Голосовое меню"""

    exten: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update({"exten": data.get("event_additional_info", {}).get("exten", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MenuEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("queue")
class QueueEvent(EventBase):
    """Очередь"""

    name: str
    number: str
    event_answer_time: datetime

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update(
            {
                "name": data.get("event_additional_info", {}).get("name", ""),
                "number": data.get("event_additional_info", {}).get("number", ""),
                "event_answer_time": _parse_datetime(data.get("event_answer_time", "")),
            }
        )
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QueueEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("queue_member")
class QueueMemberEvent(EventBase):
    event_dst_name: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update(
            {
                "event_dst_name": data.get("event_dst_name", ""),
            }
        )
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QueueMemberEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("timecondition")
class TimeConditionEvent(EventBase):
    """Расписание"""

    exten: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update({"exten": data.get("event_additional_info", {}).get("exten", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TimeConditionEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("http_request")
class HTTPEvent(EventBase):
    api_vars: dict[str, str] = field(default_factory=dict)

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        raw_api_vars: str | None = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HTTPEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("api")
class APIEvent(EventBase):
    api_vars: dict[str, str] = field(default_factory=dict)

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        raw_api_vars: str | None = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "APIEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("sms")
class SmsEvent(EventBase):
    """Отправка SMS"""

    message: str
    target_number: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update(
            {
                "message": data.get("event_additional_info", {}).get("message", ""),
                "target_number": data.get("event_additional_info", {}).get("target_number", ""),
            }
        )
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SmsEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("switch")
class SwitchEvent(EventBase):
    """Проверка условия"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SwitchEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("check")
class CheckEvent(EventBase):
    """Проверка условия"""

    name: str
    result: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update(
            {
                "name": data.get("event_additional_info", {}).get("name", ""),
                "result": data.get("event_additional_info", {}).get("result", ""),
            }
        )
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CheckEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("speech-recog")
class SpeechRecogEvent(EventBase):
    """Вопрос-ответ"""

    question: str
    answer: str | None

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        dialog = data.get("speechkit_dialog", [])
        question: str | Literal[""] = dialog[0].get("dialog_value", "") if dialog else ""
        answer = dialog[-1].get("dialog_value", "") if dialog and len(dialog) > 1 else None
        init_params.update({"question": question, "answer": answer})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpeechRecogEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("synthesis")
class SynthesisEvent(EventBase):
    """Синтез речи"""

    message: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update({"message": data.get("event_additional_info", {}).get("message", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SynthesisEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("code")
class CodeEvent(EventBase):
    api_vars: dict[str, str]

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        raw_api_vars: str | None = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CodeEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("transfered")
class TransferedEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TransferedEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("extnum")
class ExtNumEvent(EventBase):
    api_vars: dict[str, str] = field(default_factory=dict)

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        raw_api_vars: str | None = data.get("event_additional_info", {}).get("api_vars")
        init_params.update({"api_vars": cls.string_from_dict(raw_api_vars)})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExtNumEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("blacklist")
class BlackListEvent(EventBase):
    """Черный список"""

    exten: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update({"exten": data.get("event_additional_info", {}).get("exten", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BlackListEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
@EventBase.register("None")
class NoneEvent(EventBase):
    event_did: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        init_params: dict[str, Any] = super().extract_common_fields(data)
        init_params.update({"event_did": data.get("event_did", "")})
        return init_params

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NoneEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


@dataclass
class UnknownEvent(EventBase):
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UnknownEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        # Сохраняем оставшиеся ключи, которых нет в общих полях
        extra: dict[str, Any] = {k: v for k, v in data.items() if k not in init_params}
        return cls(**init_params, data=extra)
