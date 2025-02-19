from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class DateParams:
    year: int | None = None
    month: int | None = None
    day: int | None = None
    hour: int = 0
    minute: int = 0
    second: int = 0

    def __post_init__(self) -> None:
        """Обрабатывает значения, если они не были переданы, используя текущие значения"""
        current_time = datetime.now()

        # Если значение не передано (None), используем текущие значения
        self.year = self.year if self.year is not None else current_time.year
        self.month = self.month if self.month is not None else current_time.month
        self.day = self.day if self.day is not None else current_time.day

    def to_datetime(self) -> datetime:
        """Преобразует DateParams в объект datetime"""
        if self.year is None or self.month is None or self.day is None:
            raise ValueError("Missing required date parameters")
        return datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)


@dataclass
class RequestParams:
    date_from: datetime = field(default_factory=lambda: DateParams().to_datetime())
    date_to: datetime = field(default_factory=lambda: DateParams().to_datetime())
    request_detailed: str = "1"
    limit: int = 1000
    offset: int = 0
    num_hours: int = 1


class CallLog:
    """
    Основной класс работы с call_log
    """

    @staticmethod
    def get_data_hh(**kwargs: Any) -> None:
        """
        Принимает структуру

        Args:
            year: int | None = None
            month: int | None = None
            day: int | None = None
            hour: int = 0
            minute: int = 0
            second: int = 0
        """
        date_params = DateParams(**kwargs)

        date_from = date_params.to_datetime()
        print(f"Generated DateTime: {date_from}")

    def get_data_dd(self, num_days: int = 1, *, year: int | None = None) -> None: ...

    def get_data_mm(self, num_months: int = 1, *, year: int | None = None) -> None: ...
