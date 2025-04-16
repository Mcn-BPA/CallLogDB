from typing import Any

import pytest

from calllogdb.types.calls import Calls


@pytest.fixture
def sample_data() -> list[dict[str, Any]]:
    return [
        {"call_id": 1, "src_name": "Call 1"},
        {"call_id": 2, "src_name": "Call 2"},
    ]


def test_calls_from_dict(monkeypatch: pytest.MonkeyPatch, sample_data: list[dict[str, Any]]) -> None:
    # Заглушка для Call, если нужен минимальный from_dict
    class FakeCall:
        def __init__(self, call_id: int | str, src_name: str) -> None:
            self.call_id: int | str = call_id
            self.src_name: str = src_name

        @classmethod
        def from_dict(cls, data) -> "FakeCall":
            return cls(call_id=data["call_id"], src_name=data["src_name"])

    # Подменяем Call на FakeCall в месте, где он используется
    monkeypatch.setattr("calllogdb.types.calls.Call", FakeCall)

    calls_obj: Calls = Calls.from_dict(sample_data)

    assert isinstance(calls_obj, Calls)
    assert len(calls_obj.calls) == 2
    assert isinstance(calls_obj.calls[0], FakeCall)
    assert calls_obj.calls[0].call_id == 1
    assert calls_obj.calls[1].src_name == "Call 2"
