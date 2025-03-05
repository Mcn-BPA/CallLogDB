from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Any, Literal

from dateutil.relativedelta import relativedelta

from calllogdb.api import APIClient
from calllogdb.db import CallRepository
from calllogdb.db.database import CallMapper
from calllogdb.db.models import Call
from calllogdb.types import Calls


@dataclass(kw_only=True)
class DateParams:
    year: int = field(default_factory=lambda: datetime.now().year)
    month: int = field(default_factory=lambda: datetime.now().month)
    day: int = field(default_factory=lambda: datetime.now().day)
    hour: int = field(default_factory=lambda: datetime.now().hour)
    minute: int = 0

    date: datetime = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.date = datetime(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
        )

    def adjust_date(self, delta: int, field: Literal["year", "month", "day", "hour", "minute"]) -> datetime:
        adjustments: dict[str, timedelta | relativedelta] = {
            "day": timedelta(days=delta),
            "hour": timedelta(hours=delta),
            "minute": timedelta(minutes=delta),
            "month": relativedelta(months=delta),
            "year": relativedelta(years=delta),
        }
        return self.date + adjustments[field]


@dataclass(kw_only=True)
class RequestParams:
    date_from: datetime = field(default_factory=lambda: DateParams().date)
    date_to: datetime = field(default_factory=lambda: DateParams().date)
    request_detailed: str = "1"
    limit: int = 1000
    offset: int = 0

    def increase(self, step: int = 1000) -> None:
        self.offset += step
        self.limit += step


class CallLog:
    """
    Основной класс работы с call_log
    """

    @staticmethod
    def __requests(params: RequestParams) -> None:
        with APIClient() as api:
            response_list: list[dict[str, Any]] = []
            while True:
                response: dict[str, Any] = api.get(params=asdict(params))
                response_list.extend(response.get("items", []))
                if len(response.get("items", [])) < (params.limit - params.offset):
                    break
                params.increase()

        data_calls: Calls = Calls.from_dict(response_list)

        mapper = CallMapper()
        mapped_calls: list[Call] = [mapper.map(call_data) for call_data in data_calls.calls]
        CallRepository().save_many(mapped_calls)

    def get_data_from_month(self, month: int, *, year: int = DateParams().year) -> None:
        params = RequestParams(
            date_from=DateParams(year=year, month=month, day=1, hour=0).date,
            date_to=DateParams(year=year, month=month, day=2, hour=0).adjust_date(1, "month"),
        )
        self.__requests(params)

    def get_data_from_day(self, day: int, *, year: int = DateParams().year, month: int = DateParams().month) -> None:
        params = RequestParams(
            date_from=DateParams(year=year, month=month, day=day, hour=0).date,
            date_to=DateParams(year=year, month=month, day=day, hour=0).adjust_date(1, "day"),
        )
        self.__requests(params)

    def get_data_from_hours(self, hour: int = 1) -> None:
        params = RequestParams(
            date_from=DateParams().date,
            date_to=DateParams().adjust_date(hour, "hour"),
        )
        self.__requests(params)

    def get_data_for_interval(self, *, date_from: datetime, date_to: datetime) -> None:
        params = RequestParams(
            date_from=date_from,
            date_to=date_to,
        )
        self.__requests(params)
