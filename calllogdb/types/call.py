from typing import Any
from .events import Events


class Call:
    def __init__(self, id_: str, did: str, dst_num: str, events: list[Events], **kwargs: dict[str, Any]) -> None:
        self.id = id_
        self.did = did
        self.dst_num = dst_num
        self.events = events
        self.metadata = kwargs

    def __repr__(self) -> str:
        return f"Call(id={self.id}, did={self.did}, dst_num={self.dst_num}, events_count={len(self.events)})"
