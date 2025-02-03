from .events import Events
from typing import List


class Call:
    def __init__(self, id_: str, did: str, dst_num: str, events: List[Events], **kwargs):
        self.id = id_
        self.did = did
        self.dst_num = dst_num
        self.events = events
        self.metadata = kwargs  # Сохраняем оставшуюся информацию о звонке

    def __repr__(self):
        return f"Call(id={self.id}, did={self.did}, dst_num={self.dst_num}, events_count={len(self.events)})"
