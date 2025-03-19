from datetime import datetime, timedelta
from typing import Any

import pytest

from calllogdb.types.event_base import EventBase

# Вспомогательные классы для тестирования регистрации и наследования


@EventBase.register("test_event")
class TestEvent(EventBase):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestEvent":
        init_params = cls.extract_common_fields(data)
        return cls(**init_params)


# Тесты для метода string_from_dict


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("{key1: value1, key2: value2}", {"key1": "value1", "key2": "value2"}),
        ("[('key', 'value')]", {"key": "value"}),
        ("(key:val)", {"key": "val"}),
        ("", {}),
        (None, {}),
        ("invalid_string", {}),
        ("key1:val1, key2:val2", {"key1": "val1", "key2": "val2"}),
    ],
)
def test_string_from_dict(input_str, expected):
    assert EventBase.string_from_dict(input_str) == expected


# Тесты для регистрации подклассов и фабричного метода


def test_class_registration():
    assert "test_event" in EventBase._registry
    assert issubclass(EventBase._registry["test_event"], EventBase)


def test_from_dict_with_registered_class():
    test_data = {
        "event_type": "test_event",
        "event_status": "answered",
        "event_dst_num": "123",
        "event_dst_type": "test",
        "event_transfered_from": "",
        "event_start_time": "2024-01-01T00:00:00",
        "event_end_time": "2024-01-01T00:05:00",
    }

    event = EventBase.from_dict(test_data)
    assert isinstance(event, TestEvent)


def test_from_dict_with_unregistered_type():
    with pytest.raises(ValueError) as exc_info:
        EventBase.from_dict({"event_type": "unknown_type"})

    assert "Неизвестный тип события: unknown_type" in str(exc_info.value)


# Тесты для extract_common_fields


@pytest.fixture
def sample_data():
    return {
        "event_type": "call",
        "event_status": "answered",
        "event_dst_num": "100",
        "event_dst_type": "queue",
        "event_transfered_from": "200",
        "event_start_time": "2024-01-01T12:00:00",
        "event_end_time": "2024-01-01T12:05:00",
        "event_talk_time": "300",
        "event_wait_time": "45",
        "event_total_time": "345",
    }


def test_extract_common_fields_full_data(sample_data):
    result = EventBase.extract_common_fields(sample_data)

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


def test_extract_common_fields_missing_data():
    result = EventBase.extract_common_fields({})

    assert result["event_type"] == ""
    assert result["event_status"] == ""
    assert result["event_dst_num"] == ""
    assert result["event_transfered_from"] == ""
    assert result["event_start_time"] is None
    assert result["event_talk_time"] is None


# Тесты для del_api_vars


def test_del_api_vars_without_extra_fields():
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

    result = event.del_api_vars()
    assert "api_vars" not in result


# Тесты обработки временных полей


@pytest.mark.parametrize(
    "field, value, expected",
    [
        ("event_start_time", "invalid_date", None),
        ("event_talk_time", "not_a_number", None),
        ("event_wait_time", "", None),
    ],
)
def test_field_parsing_error_handling(sample_data, field, value, expected):
    sample_data[field] = value
    result = EventBase.extract_common_fields(sample_data)
    assert result[field] is expected


# Тест полной трансформации данных


def test_complete_object_creation(sample_data):
    event = TestEvent.from_dict(sample_data)

    assert event.event_start_time == datetime(2024, 1, 1, 12, 0)
    assert event.event_talk_time == timedelta(minutes=5)
    assert event.event_total_time == timedelta(seconds=345)
    assert event.event_dst_num == "100"


# Тест обработки пустых значений времени


def test_empty_time_processing():
    data = {
        "event_type": "test_event",
        "event_start_time": "",
        "event_talk_time": "",
    }

    event = TestEvent.from_dict(data)
    assert event.event_start_time is None
    assert event.event_talk_time is None
