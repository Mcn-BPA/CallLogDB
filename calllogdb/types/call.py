from dataclasses import dataclass, field
from typing import Any

from .event_base import EventBase


@dataclass
class Call:
    id: str
    answerdate: str
    calldate: str
    endtime: str
    calltype: str
    src_type: str
    call_status: str
    hangup_reason: str
    dst_type: str
    dst_num: str
    dst_name: str
    did: str
    did_num: str
    src_name: str
    src_num: str
    total_time: int
    wait_time: int
    talk_time: int
    events_count: int
    transfered_linked_to: bool
    vpbx_id: int

    events: list[EventBase] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Call":
        return cls(
            id=data.get("id", ""),
            answerdate=data.get("answerdate", ""),
            calldate=data.get("calldate", ""),
            endtime=data.get("endtime", ""),
            calltype=data.get("calltype", ""),
            src_type=data.get("src_type", ""),
            call_status=data.get("call_status", ""),
            hangup_reason=data.get("hangup_reason", ""),
            dst_type=data.get("dst_type", ""),
            dst_num=data.get("dst_num", ""),
            dst_name=data.get("dst_name", ""),
            did=data.get("did", ""),
            did_num=data.get("did_num", ""),
            src_name=data.get("src_name", ""),
            src_num=data.get("src_num", ""),
            total_time=data.get("total_time", 0),
            wait_time=data.get("wait_time", 0),
            talk_time=data.get("talk_time", 0),
            events_count=data.get("events_count", 0),
            transfered_linked_to=data.get("transfered_linked_to", False),
            vpbx_id=data.get("vpbx_id", 0),
            events=[EventBase.from_dict(ed) for ed in data.get("events", [])],
        )
