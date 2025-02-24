from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Literal

from dateutil.relativedelta import relativedelta
from icecream import ic

from calllogdb.api import APIClient
from calllogdb.db import Database
from calllogdb.types import Calls

# TODO берёт за месяц (можно передать год и месяц)
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


class CallLog:
    """
    Основной класс работы с call_log
    """

    @staticmethod
    def get_data_from_month(month: int, *, year: int = DateParams().year) -> None:
        params = RequestParams(
            date_from=DateParams(year=year, month=month, day=1, hour=0).adjust_date(-1, "month"),
            date_to=DateParams(year=year, month=month, day=1, hour=0).date,
            limit=1,
        )
        ic(params)

        with APIClient() as api:
            data = api.get(params=asdict(params))

            data_calls = Calls.from_dict(data.get("items", []))

            db = Database()
            db.insert_many(data_calls)

    @staticmethod
    def get_data_from_day(day: int, *, year: int = ..., month: int = ...) -> None: ...
    @staticmethod
    def get_data_from_hours(hour: int) -> None: ...
    @staticmethod
    def get_data_for_interval(*, date_from: datetime, date_to: datetime) -> None: ...
