from dataclasses import dataclass, field
from typing import Any

from .call import Call


@dataclass
class Calls:
    calls: list[Call] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: list[dict[str, Any]]) -> "Calls":
        return cls(calls=[Call.from_dict(item) for item in data])
