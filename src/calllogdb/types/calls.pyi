from dataclasses import dataclass
from typing import Any

from .call import Call

@dataclass
class Calls:
    calls: list[Call] = ...

    @classmethod
    def from_dict(cls, data: list[dict[str, Any]]) -> "Calls": ...
