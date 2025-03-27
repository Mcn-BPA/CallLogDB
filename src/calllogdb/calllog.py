from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Any, Literal

from dateutil.relativedelta import relativedelta
from loguru import logger

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
        adjusted_date: datetime = self.date + adjustments[field]
        logger.debug("Дата {} скорректирована на {}: {}", field, delta, adjusted_date)
        return adjusted_date


@dataclass(kw_only=True)
class RequestParams:
    date_from: datetime = field(default_factory=lambda: DateParams().date)
    date_to: datetime = field(default_factory=lambda: DateParams().date)
    request_detailed: int = 1
    limit: int = 2000
    offset: int = 0

    def increase(self) -> None:
        old_offset: int = self.offset
        self.offset += self.limit
        logger.debug(
            "Параметры запроса увеличены: offset {} -> {}",
            old_offset,
            self.offset,
        )


@dataclass(kw_only=True)
class CallLog:
    """
    Основной класс работы с call_log
    """

    @staticmethod
    def __requests(params: RequestParams) -> None:
        logger.info("Начало запроса данных с параметрами: {}", asdict(params))
        with APIClient() as api:
            response_list: list[dict[str, Any]] = []
            while True:
                logger.debug("Отправка запроса с параметрами: {}", asdict(params))
                response: dict[str, Any] = api.get(params=asdict(params))
                items = response.get("items", [])
                logger.debug("Получено {} элементов", len(items))
                response_list.extend(items)
                if len(items) < params.limit:
                    logger.info("Получено {} элементов, меньше чем ожидалось, завершаем запрос", len(items))
                    break
                params.increase()
        logger.info("Общее количество полученных элементов: {}", len(response_list))

        data_calls: Calls = Calls.from_dict(response_list)
        logger.info("Преобразование данных в объект Calls завершено")

        mapper = CallMapper()
        logger.info("Старт маппинга для: {} объектов Call", len(data_calls.calls))
        mapped_calls: list[Call] = [mapper.map(call_data) for call_data in data_calls.calls]
        logger.info("Маппинг завершен: получено {} объектов Call", len(mapped_calls))

        CallRepository().save_many(mapped_calls)
        logger.info("Сохранение объектов Call завершено")

    def get_data_from_month(self, month: int, *, year: int = DateParams().year) -> None:
        logger.info("Получение данных за {} месяц(а) {} года", month, year)
        params = RequestParams(
            date_from=DateParams(year=year, month=month, day=1, hour=0).date,
            date_to=DateParams(year=year, month=month, day=1, hour=0).adjust_date(1, "month"),
        )
        logger.debug("Параметры запроса для месяца: {}", asdict(params))
        self.__requests(params)

    def get_data_from_day(self, day: int, *, year: int = DateParams().year, month: int = DateParams().month) -> None:
        logger.info("Получение данных за день: {}-{}-{}", year, month, day)
        params = RequestParams(
            date_from=DateParams(year=year, month=month, day=day, hour=0).date,
            date_to=DateParams(year=year, month=month, day=day, hour=0).adjust_date(1, "day"),
        )
        logger.debug("Параметры запроса для дня: {}", asdict(params))
        self.__requests(params)

    def get_data_from_hours(self, hour: int = 1) -> None:
        logger.info("Получение данных за последние {} часов", hour)
        params = RequestParams(
            date_from=DateParams().adjust_date(-hour, "hour"),
            date_to=DateParams().date,
        )
        logger.debug("Параметры запроса для часов: {}", asdict(params))
        self.__requests(params)

    def get_data_for_interval(self, *, date_from: datetime, date_to: datetime) -> None:
        logger.info("Получение данных за интервал с {} по {}", date_from, date_to)
        params = RequestParams(
            date_from=date_from,
            date_to=date_to,
        )
        logger.debug("Параметры запроса для интервала: {}", asdict(params))
        self.__requests(params)
