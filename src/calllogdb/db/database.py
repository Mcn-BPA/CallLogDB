import json
import logging
from datetime import datetime
from typing import Any, Callable, ContextManager

from loguru import logger
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

from calllogdb.core import DB_URL
from calllogdb.types import Call as CallData
from calllogdb.utils import _mask_db_url

from .models import ApiVars, Base, Call, Date, Event

logging.getLogger("psycopg").setLevel(logging.CRITICAL)

# Создаём движок подключения
engine: Engine = create_engine(DB_URL, echo=False)

# Создаём фабрику сессий
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def call_to_dict(call: Call) -> dict[str, Any]:
    """
    Преобразует объект Call в словарь, используя определения колонок таблицы.
    """
    return {column.name: getattr(call, column.name) for column in call.__table__.columns}


def init_db() -> None:
    """Явная функция для создания всех таблиц в БД."""
    logger.info("Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    logger.info("База данных создана успешно.")


class DatabaseSession:
    """Менеджер контекста для работы с сессией SQLAlchemy"""

    def __enter__(self) -> SQLAlchemySession:
        logger.info("Создан движок подключения с DB_URL: {}", _mask_db_url(DB_URL))
        self.db: SQLAlchemySession = SessionLocal()
        logger.debug("Создана новая сессия SQLAlchemy: {}", self.db)
        return self.db

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        bind_obj: Engine | Connection = self.db.get_bind()
        # Если это Connection, получаем его engine через атрибут engine
        if isinstance(bind_obj, Engine):
            engine: Engine = bind_obj
        else:
            engine = bind_obj.engine
        if exc_type is None:
            try:
                self.db.commit()
                logger.info("Сессия успешно зафиксирована (commit).")
            except Exception as e:
                logger.exception("Ошибка при фиксации сессии: {}. Выполняется откат транзакции.", e)
                self.db.rollback()
                # Сбрасываем все соединения через engine.dispose()
                try:
                    engine.dispose()
                    logger.info("Engine успешно сброшен после ошибки фиксации.")
                except Exception as ex:
                    logger.exception("Ошибка при сбросе Engine: {}", ex)
                raise
        else:
            logger.error("Исключение в сессии SQLAlchemy: {}. Выполняется откат транзакции.", exc_value)
            self.db.rollback()
            try:
                engine.dispose()
                logger.info("Engine успешно сброшен после исключения в сессии.")
            except Exception as ex:
                logger.exception("Ошибка при сбросе Engine: {}", ex)
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
        logger.debug("Маппинг завершен для call_id: {} с {} событиями", new_call.call_id, len(new_call.events))
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

    def _is_duplicate_error(self, err: IntegrityError) -> bool:
        """
        Простейшая проверка ошибки на наличие сообщения о дублировании ключа.
        В зависимости от СУБД может потребоваться более тонкая обработка.
        """
        return "duplicate key" in str(err.orig).lower()

    def save(self, call: Call) -> None:
        """
        Сохраняет один объект Call в базе данных.
        Сначала пытается выполнить вставку через session.add,
        а при конфликте дублирования выполняет merge.
        """
        logger.info("Начало сохранения объекта Call с call_id: {}", call.call_id)
        with self._session_factory() as session:
            try:
                session.add(call)
                session.commit()
                logger.info("Объект Call с call_id {} успешно сохранен", call.call_id)
            except IntegrityError as err:
                session.rollback()
                if self._is_duplicate_error(err):
                    logger.warning("Найден дубликат для call_id {}, выполняется merge", call.call_id)
                    try:
                        session.merge(call)
                        session.commit()
                        logger.info("Merge успешно выполнен для call_id {}", call.call_id)
                    except IntegrityError as merge_err:
                        session.rollback()
                        logger.error("Ошибка при merge объекта Call с call_id {}: {}", call.call_id, merge_err)
                else:
                    logger.error("Ошибка при сохранении объекта Call с call_id {}: {}", call.call_id, err)

    def save_many(self, calls: list[Call], batch_size: int = 500) -> None:
        """
        Сохраняет список объектов Call в базе данных с промежуточными коммитами.
        Сначала пытается массовую вставку через session.add.
        При обнаружении ошибки дублирования в пакете выполняет merge для каждого объекта.
        При иной ошибке выполняется rollback.
        """
        logger.info("Начало сохранения {} объектов Call", len(calls))
        with self._session_factory() as session:
            for i in range(0, len(calls), batch_size):
                batch: list[Call] = calls[i : i + batch_size]
                try:
                    for call in batch:
                        session.add(call)
                    session.commit()
                    logger.info("Сохранено {} записей (пакет {}-{})", len(batch), i, i + len(batch))
                except IntegrityError as err:
                    session.rollback()
                    if self._is_duplicate_error(err):
                        logger.warning("Найден дубликат в пакете {}-{}, выполняется merge", i, i + len(batch))
                        try:
                            for call in batch:
                                session.merge(call)
                            session.commit()
                            logger.info("Merge успешно выполнен для пакета {}-{}", i, i + len(batch))
                        except IntegrityError as merge_err:
                            session.rollback()
                            logger.error("Ошибка при merge пакета {}-{}: {}", i, i + len(batch), merge_err)
                    else:
                        logger.error("Ошибка при сохранении пакета {}-{}: {}", i, i + len(batch), err)
                        session.rollback()
