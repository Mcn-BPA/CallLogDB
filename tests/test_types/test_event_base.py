from datetime import datetime, timedelta
from typing import Any

import pytest

from calllogdb.types.event_base import EventBase


# Вспомогательный класс для тестирования
@EventBase.register("test_event")
class TestEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestEvent":
        init_params: dict[str, Any] = cls.extract_common_fields(data)
        return cls(**init_params)


# ==== Тесты регистрации и фабрики ====
def test_class_registration() -> None:
    assert "test_event" in EventBase._registry
    assert issubclass(EventBase._registry["test_event"], EventBase)


def test_from_dict_with_registered_class() -> None:
    test_data: dict[str, str] = {
        "event_type": "test_event",
        "event_status": "answered",
        "event_dst_num": "123",
        "event_dst_type": "test",
        "event_transfered_from": "",
        "event_start_time": "2024-01-01T00:00:00",
        "event_end_time": "2024-01-01T00:05:00",
    }
    event: EventBase = EventBase.from_dict(test_data)
    assert isinstance(event, TestEvent)


def test_from_dict_with_unregistered_type() -> None:
    with pytest.raises(ValueError) as exc_info:
        EventBase.from_dict({"event_type": "unknown_type"})
    assert "Неизвестный тип события: unknown_type" in str(exc_info.value)


# ==== Тесты extract_common_fields ====
@pytest.fixture
def sample_data() -> dict[str, str]:
    return {
        "event_type": "call",
        "event_status": "answered",
        "event_dst_num": "100",
        "event_dst_type": "queue",
        "event_transfered_from": "200",
        "event_start_time": "2024-01-01 12:00:00",
        "event_end_time": "2024-01-01 12:05:00",
        "event_talk_time": "300",
        "event_wait_time": "45",
        "event_total_time": "345",
    }


def test_extract_common_fields_full_data(sample_data: dict[str, str]) -> None:
    result: dict[str, Any] = EventBase.extract_common_fields(sample_data)
    assert result["event_type"] == "call"
    assert result["event_status"] == "answered"
    assert result["event_dst_num"] == "100"
    assert result["event_dst_type"] == "queue"
    assert result["event_transfered_from"] == "200"
    assert result["event_start_time"] == datetime(2024, 1, 1, 12, 0)
    assert result["event_end_time"] == datetime(2024, 1, 1, 12, 5)
    assert result["event_talk_time"] == timedelta(seconds=300)
    assert result["event_wait_time"] == timedelta(seconds=45)
    assert result["event_total_time"] == timedelta(seconds=345)


def test_extract_common_fields_missing_data() -> None:
    result: dict[str, Any] = EventBase.extract_common_fields({})
    assert result["event_type"] == ""
    assert result["event_status"] == ""
    assert result["event_dst_num"] == ""
    assert result["event_transfered_from"] == ""
    assert result["event_start_time"] is None
    assert result["event_talk_time"] is None


# ==== Тесты del_api_vars ====
def test_del_api_vars_without_extra_fields() -> None:
    event = TestEvent(
        event_type="test",
        event_status="",
        event_dst_num="",
        event_dst_type="",
        event_transfered_from="",
        event_start_time=None,
        event_end_time=None,
        event_talk_time=None,
        event_wait_time=None,
        event_total_time=None,
    )
    result: dict[str, Any] = event.del_api_vars()
    assert "api_vars" not in result


# ==== Полная трансформация ====
def test_complete_object_creation(sample_data: dict[str, str]) -> None:
    event: TestEvent = TestEvent.from_dict(sample_data)
    assert event.event_start_time == datetime(2024, 1, 1, 12, 0)
    assert event.event_talk_time == timedelta(minutes=5)
    assert event.event_total_time == timedelta(seconds=345)
    assert event.event_dst_num == "100"


# ==== Обработка пустых значений времени ====
def test_empty_time_processing() -> None:
    data: dict[str, str] = {
        "event_type": "test_event",
        "event_start_time": "",
        "event_talk_time": "",
        "event_wait_time": "",
        "event_total_time": "",
    }
    event: TestEvent = TestEvent.from_dict(data)
    assert event.event_start_time is None
    assert event.event_talk_time is None
