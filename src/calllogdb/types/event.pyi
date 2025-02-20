from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .event_base import EventBase

@dataclass
@EventBase.register("announce")
class AnnounceEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AnnounceEvent": ...

@dataclass
@EventBase.register("hangup")
class HangupEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HangupEvent": ...

@dataclass
@EventBase.register("ivr")
class IvrEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IvrEvent": ...

@dataclass
@EventBase.register("gpt")
class GptEvent(EventBase):

    api_vars: dict[str, str]

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GptEvent": ...

@dataclass
@EventBase.register("robocall_task")
class RobocallTaskEvent(EventBase):

    api_vars: dict[str, str]

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RobocallTaskEvent": ...

@dataclass
@EventBase.register("menu")
class MenuEvent(EventBase):

    exten: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MenuEvent": ...

@dataclass
@EventBase.register("queue")
class QueueEvent(EventBase):

    name: str
    number: str
    event_answer_time: datetime

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QueueEvent": ...

@dataclass
@EventBase.register("queue_member")
class QueueMemberEvent(EventBase):
    event_dst_name: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QueueMemberEvent": ...

@dataclass
@EventBase.register("timecondition")
class TimeConditionEvent(EventBase):

    exten: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TimeConditionEvent": ...

@dataclass
@EventBase.register("http_request")
class HTTPEvent(EventBase):
    api_vars: dict[str, str] = ...

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HTTPEvent": ...

@dataclass
@EventBase.register("api")
class APIEvent(EventBase):
    api_vars: dict[str, str] = ...

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "APIEvent": ...

@dataclass
@EventBase.register("sms")
class SmsEvent(EventBase):

    message: str
    target_number: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SmsEvent": ...

@dataclass
@EventBase.register("switch")
class SwitchEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SwitchEvent": ...

@dataclass
@EventBase.register("check")
class CheckEvent(EventBase):

    name: str
    result: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CheckEvent": ...

@dataclass
@EventBase.register("speech-recog")
class SpeechRecogEvent(EventBase):

    question: str
    answer: str | None

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpeechRecogEvent": ...

@dataclass
@EventBase.register("synthesis")
class SynthesisEvent(EventBase):

    message: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SynthesisEvent": ...

@dataclass
@EventBase.register("code")
class CodeEvent(EventBase):
    api_vars: dict[str, str]

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CodeEvent": ...

@dataclass
@EventBase.register("transfered")
class TransferedEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TransferedEvent": ...

@dataclass
@EventBase.register("extnum")
class ExtNumEvent(EventBase):
    api_vars: dict[str, str] = ...

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExtNumEvent": ...

@dataclass
@EventBase.register("blacklist")
class BlackListEvent(EventBase):

    exten: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BlackListEvent": ...

@dataclass
@EventBase.register("None")
class NoneEvent(EventBase):
    event_did: str

    @classmethod
    def extract_common_fields(cls, data: dict[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NoneEvent": ...

@dataclass
class UnknownEvent(EventBase):
    data: dict[str, Any] = ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UnknownEvent": ...
