import json
from datetime import datetime
from typing import Callable, ContextManager

from loguru import logger
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

from calllogdb.core import DB_URL
from calllogdb.types import Call as CallData
from calllogdb.utils import _mask_db_url

from .models import ApiVars, Base, Call, Date, Event

# Создаём движок подключения
engine: Engine = create_engine(DB_URL, echo=False)
logger.debug("Создан движок подключения с DB_URL: {}", _mask_db_url(DB_URL))

# Создаём фабрику сессий
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def init_db() -> None:
    """Явная функция для создания всех таблиц в БД."""
    logger.info("Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    logger.info("База данных создана успешно.")


class DatabaseSession:
    """Менеджер контекста для работы с сессией SQLAlchemy"""

    def __enter__(self) -> SQLAlchemySession:
        self.db: SQLAlchemySession = SessionLocal()
        logger.debug("Создана новая сессия SQLAlchemy: {}", self.db)
        return self.db

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        if exc_type is None:
            try:
                self.db.commit()
                logger.info("Сессия успешно зафиксирована (commit).")
            except Exception as e:
                logger.exception("Ошибка при фиксации сессии: {}. Выполняется откат транзакции.", e)
                self.db.rollback()
                raise
        else:
            logger.error("Исключение в сессии SQLAlchemy: {}. Выполняется откат транзакции.", exc_value)
            self.db.rollback()
        self.db.close()
        logger.debug("Сессия SQLAlchemy закрыта.")


class CallMapper:
    """Отвечает за преобразование CallData в доменный объект Call с дочерними объектами."""

    def map(self, call_data: CallData) -> Call:
        logger.debug("Начало маппинга CallData с call_id: {}", getattr(call_data, "call_id", "неизвестно"))
        new_call = Call(**call_data.del_events())
        logger.debug("Данные Call после удаления событий: {}", new_call)

        if call_data.call_date:
            date_obj: datetime = call_data.call_date
            new_call.date = Date(
                call_id=new_call.call_id,
                year=date_obj.year,
                month=date_obj.month,
                day=date_obj.day,
                hours=date_obj.hour,
                minutes=date_obj.minute,
                seconds=date_obj.second,
            )
            logger.debug("Установлена дата для call_id {}: {}", new_call.call_id, new_call.date)

        new_call.events = []
        for index, event in enumerate(call_data.events):
            new_event = Event(**event.del_api_vars(), id=index, call_id=new_call.call_id)
            new_call.events.append(new_event)
            logger.debug("Событие {} добавлено для call_id {}", index, new_call.call_id)
            api_vars: dict[str, str] | None = getattr(event, "api_vars", None)
            if api_vars:
                new_event.api_vars = [
                    ApiVars(
                        id=new_event.id,
                        event_id=new_call.call_id,
                        **{
                            k: api_vars.get(k)
                            for k in [
                                "account_id",
                                "num_a",
                                "num_b",
                                "num_c",
                                "scenario_id",
                                "scenario_counter",
                                "dest_link_name",
                                "dtmf",
                                "ivr_object_id",
                                "ivr_schema_id",
                                "stt_answer",
                                "stt_question",
                                "intent",
                            ]
                        },
                        other=json.dumps(api_vars, indent=4),
                    )
                ]
                logger.debug("ApiVars установлены для события {}: {}", index, new_event.api_vars)
        logger.info("Маппинг завершен для call_id: {} с {} событиями", new_call.call_id, len(new_call.events))
        return new_call


class CallRepository:
    """
    Отвечает за сохранение объектов Call.
    Для работы использует фабрику сессий, что позволяет подменять реализацию (например, для тестов).
    """

    def __init__(self, session_factory: Callable[[], ContextManager[SQLAlchemySession]] = DatabaseSession) -> None:
        self._session_factory = session_factory
        logger.debug("Инициализация CallRepository с фабрикой сессий: {}", session_factory)
        init_db()

    def save(self, call: Call) -> None:
        """
        Сохраняет один объект Call в базе данных.
        Использует сессию SQLAlchemy.
        """
        logger.info("Начало сохранения объекта Call с call_id: {}", call.call_id)
        with self._session_factory() as session:
            session.merge(call)
            session.commit()
            logger.info("Объект Call с call_id {} успешно сохранен", call.call_id)

    def save_many(self, calls: list[Call]) -> None:
        """
        Сохраняет список объектов Call в базе данных.
        """
        logger.info("Начало сохранения {} объектов Call", len(calls))
        with self._session_factory() as session:
            for call in calls:
                session.merge(call)
                logger.debug("Объект Call с call_id {} добавлен для сохранения", call.call_id)
            session.commit()
            logger.info("Все объекты Call успешно сохранены")
