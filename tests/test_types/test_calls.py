import pytest
from calllogdb.types.calls import Calls
from calllogdb.types.call import Call

@pytest.fixture
def sample_data():
    return [
        {"call_id": 1, "name": "Call 1"},
        {"call_id": 2, "name": "Call 2"},
    ]
    
def test_calls_from_dict(monkeypatch, sample_data):
    # Заглушка для Call, если нужен минимальный from_dict
    class FakeCall:
        def __init__(self, call_id, name):
            self.call_id = call_id
            self.name = name

        @classmethod
        def from_dict(cls, data):
            return cls(call_id=data["call_id"], name=data["name"])

    # Подменяем Call на FakeCall в месте, где он используется
    monkeypatch.setattr("calllogdb.types.calls.Call", FakeCall)

    calls_obj = Calls.from_dict(sample_data)

    assert isinstance(calls_obj, Calls)
    assert len(calls_obj.calls) == 2
    assert isinstance(calls_obj.calls[0], FakeCall)
    assert calls_obj.calls[0].call_id == 1
    assert calls_obj.calls[1].name == "Call 2"

