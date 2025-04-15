import pytest
from datetime import datetime, timedelta
from calllogdb.utils.utils import _parse_datetime, _parse_timedelta_seconds, _mask_db_url  # Замените на имя вашего модуля


# Тест для _parse_datetime
def test_parse_datetime_valid():
    assert _parse_datetime("2025-04-15 12:30:00") == datetime(2025, 4, 15, 12, 30, 0)


def test_parse_datetime_invalid():
    assert _parse_datetime("2025-04-15 12:30") is None
    assert _parse_datetime("15-04-2025 12:30:00") is None
    assert _parse_datetime("2025/04/15 12:30:00") is None


def test_parse_datetime_empty():
    assert _parse_datetime("") is None


# Тест для _parse_timedelta_seconds
def test_parse_timedelta_seconds_valid_int():
    assert _parse_timedelta_seconds(3600) == timedelta(seconds=3600)


def test_parse_timedelta_seconds_valid_str():
    assert _parse_timedelta_seconds("3600") == timedelta(seconds=3600)


def test_parse_timedelta_seconds_invalid():
    assert _parse_timedelta_seconds(None) is None


def test_parse_timedelta_seconds_empty():
    assert _parse_timedelta_seconds("") is None


# Тест для _mask_db_url
def test_mask_db_url():
    db_url = "postgres://user:password@host:5432/dbname"
    expected = "postgres://user:******@host:5432/dbname"
    assert _mask_db_url(db_url) == expected



def test_mask_db_url_empty():
    db_url = ""
    assert _mask_db_url(db_url) == db_url
