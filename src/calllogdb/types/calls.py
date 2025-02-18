from dataclasses import dataclass, field

from .call import Call


@dataclass
class Calls:
    calls: list[Call] = field(default_factory=list)
