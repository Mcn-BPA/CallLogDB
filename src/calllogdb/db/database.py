import json
import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Callable, ContextManager, Iterator

from loguru import logger
from sqlalchemy import Engine, create_engine
from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

from calllogdb.core import Config
from calllogdb.types import Call as CallData

from .models import ApiVars, Base, Call, Date, Event

# ---------- Снижаем уровень логирования для драйвера psycopg ----------
logging.getLogger("psycopg").setLevel(logging.CRITICAL)


def call_to_dict(call: Call) -> dict[str, Any]:
    """
    Преобразует объект Call в словарь, используя определения колонок таблицы.
    """
    return {column.name: getattr(call, column.name) for column in call.__table__.columns}


class CallMapper:
    """Преобразует данные CallData в доменный объект Call с дочерними объектами."""

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
                        account_id=api_vars.get("account_id"),
                        num_a=api_vars.get("num_a"),
                        num_b=api_vars.get("num_b"),
                        num_c=api_vars.get("num_c"),
                        scenario_id=api_vars.get("scenario_id"),
                        scenario_counter=api_vars.get("scenario_counter"),
                        dest_link_name=api_vars.get("dest_link_name"),
                        dtmf=api_vars.get("dtmf"),
                        ivr_object_id=api_vars.get("ivr_object_id"),
                        ivr_schema_id=api_vars.get("ivr_schema_id"),
                        stt_answer=api_vars.get("stt_answer"),
                        stt_question=api_vars.get("stt_question"),
                        intent=api_vars.get("intent"),
                        other=json.dumps(api_vars, separators=(",", ":")),
                    )
                ]
                logger.debug("ApiVars установлены для события {}: {}", index, new_event.api_vars)

        logger.debug(
            "Маппинг завершен для call_id: {} с {} событиями",
            new_call.call_id,
            len(new_call.events),
        )
        return new_call


class CallRepository:
    """
    Отвечает за сохранение объектов Call.
    Использует фабрику сессий, что позволяет подменять реализацию (например, для тестов).
    """

    def __init__(self, config: Config) -> None:
        self._engine: Engine = create_engine(
            config.db_url,
            echo=False,
            connect_args={"options": f"-c search_path={config.schema}"},
        )
        self._session_factory = self._create_session_factory()
        logger.debug("Инициализация CallRepository с фабрикой сессий")
        self._init_db()

    def _create_session_factory(self) -> Callable[[], ContextManager[SQLAlchemySession]]:
        # ---------- настройка ссессиии ----------
        SessionLocal = sessionmaker(  # noqa: N806
            bind=self._engine,
            autocommit=False,
            autoflush=False,
        )

        # ---------- генератор сессий ----------
        @contextmanager
        def session() -> Iterator[SQLAlchemySession]:
            db_session: SQLAlchemySession = SessionLocal()
            logger.info("Создана новая сессия SQLAlchemy")
            try:
                yield db_session
            except Exception as e:
                db_session.rollback()
                logger.exception("Ошибка в сессии, выполняется откат транзакции: {}", e)
                raise
            finally:
                db_session.close()
                logger.debug("Сессия SQLAlchemy закрыта.")

        return session

    def _init_db(self) -> None:
        """Инициализация базы данных, создание таблиц."""
        Base.metadata.create_all(bind=self._engine)
        logger.info("База данных создана успешно.")

    def _is_duplicate_error(self, err: IntegrityError) -> bool:
        """
        Простейшая проверка ошибки на наличие сообщения о дублировании ключа.
        """
        return "duplicate key" in str(err.orig).lower()

    def save(self, call: Call) -> None:
        """
        Сохраняет один объект Call в базе данных.
        При возникновении ошибки дублирования выполняется fallback на merge.
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
        Сохраняет список объектов Call в базе данных с пакетной вставкой.
        При обнаружении ошибки дублирования в пакете выполняется merge для каждого объекта.
        """
        logger.info("Начало сохранения {} объектов Call", len(calls))
        with self._session_factory() as session:
            for i in range(0, len(calls), batch_size):
                batch = calls[i : i + batch_size]
                try:
                    session.add_all(batch)
                    session.commit()
                    logger.info("Сохранено {} записей (пакет {}–{})", len(batch), i, i + len(batch))
                except IntegrityError as err:
                    session.rollback()
                    if self._is_duplicate_error(err):
                        logger.warning("Найден дубликат в пакете {}–{}, выполняется merge", i, i + len(batch))
                        try:
                            for call in batch:
                                session.merge(call)
                            session.commit()
                            logger.info("Merge успешно выполнен для пакета {}–{}", i, i + len(batch))
                        except IntegrityError as merge_err:
                            session.rollback()
                            logger.error("Ошибка при merge пакета {}–{}: {}", i, i + len(batch), merge_err)
                    else:
                        logger.error("Ошибка при сохранении пакета {}–{}: {}", i, i + len(batch), err)
                        session.rollback()

    def save_many_optimized(self, calls: list[Call]) -> None:
        """
        Оптимизированное сохранение объектов Call с использованием upsert (INSERT ... ON CONFLICT).
        Предназначено для PostgreSQL: при конфликте обновляются все поля, кроме 'call_id'.
        """
        if not calls:
            logger.info("Нет объектов для сохранения.")
            return

        call_dicts = [call_to_dict(call) for call in calls]

        from sqlalchemy.dialects.postgresql import insert

        stmt: Insert = insert(Call).values(call_dicts)
        update_dict = {
            col.name: getattr(stmt.excluded, col.name) for col in Call.__table__.columns if col.name != "call_id"
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=["call_id"],
            set_=update_dict,
        )

        with self._session_factory() as session:
            try:
                session.execute(stmt)
                session.commit()
                logger.info("Оптимизированное сохранение {} объектов Call выполнено успешно", len(calls))
            except Exception as e:
                session.rollback()
                logger.exception("Ошибка при оптимизированном сохранении объектов Call: {}", e)
                raise
