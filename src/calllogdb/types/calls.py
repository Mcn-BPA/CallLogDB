from dataclasses import dataclass, field
from typing import Any

from icecream import ic

from .call import Call

ic.disable()


@dataclass
class Calls:
    calls: list[Call] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: list[dict[str, Any]]) -> "Calls":
        ic(list(data[0].keys()))
        ic(len(list(data[0].keys())))
        return cls(calls=[Call.from_dict(item) for item in data])
