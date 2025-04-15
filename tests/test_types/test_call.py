import pytest
from datetime import datetime, timedelta
from calllogdb.types.call import Call
from calllogdb.types.event_base import EventBase
from dataclasses import dataclass


@dataclass
class MockEvent:
    event_type: str
    timestamp: datetime


@pytest.fixture(autouse=True)
def patch_eventbase(monkeypatch):
    monkeypatch.setattr("calllogdb.types.call.EventBase", MockEvent)


def test_from_dict_basic():
    data = {
        "callid": "abc123",
        "status": "completed",
        "type": "inbound",
        "call_date": "2024-02-10 12:30:00",
        "end_date": "2024-02-10 12:32:00",
        "answer_date": "2024-02-10 12:30:10",
        "talktime": 100,
        "waittime": 10,
        "billsec": 110,
        "events": [
            {"event_type": "answered", "timestamp": "2024-02-10 12:30:10"}
        ]
    }

    call = Call.from_dict(data)

    assert call.call_id == "abc123"
    assert call.call_status == "completed"
    assert call.call_type == "inbound"
    assert call.call_date == datetime(2024, 2, 10, 12, 30, 0)
    assert call.end_time == datetime(2024, 2, 10, 12, 32, 0)
    assert call.answer_date == datetime(2024, 2, 10, 12, 30, 10)
    assert call.talk_time == timedelta(seconds=100)
    assert call.wait_time == timedelta(seconds=10)
    assert call.total_time == timedelta(seconds=110)
    assert len(call.events) == 1
    assert isinstance(call.events[0], MockEvent)
    assert call.events[0].event_type == "answered"


def test_del_events():
    call = Call(
        call_id="test1",
        call_status="completed",
        call_type="outbound",
        events=[MockEvent("test", datetime.now())]
    )

    data = call.del_events()

    assert "events" not in data
    assert data["call_id"] == "test1"
    assert data["call_status"] == "completed"
    assert data["call_type"] == "outbound"


def test_from_dict_ignores_extra_fields():
    data = {
        "callid": "xyz789",
        "unknown_field": "should be ignored",
        "call_date": "2024-03-01 15:00:00",
    }

    call = Call.from_dict(data)

    assert call.call_id == "xyz789"
    assert call.call_date == datetime(2024, 3, 1, 15, 0, 0)
    assert not hasattr(call, "unknown_field")


def test_from_dict_missing_optional_fields():
    data = {
        "callid": "noextras",
    }

    call = Call.from_dict(data)

    assert call.call_id == "noextras"
    assert call.call_status is None
    assert call.call_date is None
    assert call.events == []
