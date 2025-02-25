from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Any, Literal

from dateutil.relativedelta import relativedelta
from loguru import logger

from calllogdb.api import APIClient
from calllogdb.db import CallRepository
from calllogdb.db.database import CallMapper
from calllogdb.types import Calls

# TODO берёт за конкретный день (можно передать год месяц и день)

# TODO берёт от текущего до указанного в часах и минутах (можно передать только количество часов и минут)

# TODO берёт от и до (принимает 2 параметра метки времени)


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
    def get_data_from_month(month: int, *, year: int = DateParams().year) -> None:
        params = RequestParams(
            date_from=DateParams(year=year, month=month, day=1, hour=0).date,
            date_to=DateParams(year=year, month=month, day=2, hour=0).date, #.adjust_date(1, "month"),
            limit=1000,
        )
        logger.info(params)

        with APIClient() as api:
            response_list: list[dict[str, Any]] = []
            while True:
                response = api.get(params=asdict(params))
                response_list.extend(response.get("items", []))
                if len(response.get("items", [])) < (params.limit - params.offset):
                    break
                params.increase()
                logger.info(f"{len(response.get("items", []))}")

        data_calls = Calls.from_dict(response_list)

        mapper = CallMapper()
        mapped_calls = [mapper.map(call_data) for call_data in data_calls.calls]
        CallRepository().save_many(mapped_calls)

    @staticmethod
    def get_data_from_day(day: int, *, year: int = ..., month: int = ...) -> None: ...
    @staticmethod
    def get_data_from_hours(hour: int) -> None: ...
    @staticmethod
    def get_data_for_interval(*, date_from: datetime, date_to: datetime) -> None: ...
