import json
from datetime import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

from calllogdb.core import DB_URL
from calllogdb.types import Call as CallData
from calllogdb.types import Calls

from .models import ApiVars, Base, Call, Date, Event

engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(engine)


class Database:
    def __init__(self) -> None:
        self.create()

    @staticmethod
    def create() -> None:
        # Получаем список существующих таблиц в базе данных
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        # Получаем имена всех таблиц, описанных в metadata
        expected_tables = list(Base.metadata.tables.keys())

        # Если все ожидаемые таблицы уже существуют, выходим из метода
        if all(table in existing_tables for table in expected_tables):
            return

        # Если хотя бы одной из таблиц нет – создаём недостающие
        Base.metadata.create_all(engine)

    @staticmethod
    def prepare_call_objects(call: CallData) -> list[Base]:
        """
        Преобразует данные вызова в список ORM-объектов: Call, Date, Event, ApiVars.
        Предполагается, что все классы (Call, Date, Event, ApiVars) наследуются от Base.
        """
        objects: list[Base] = []
        new_call = Call(**(call.del_events()))
        objects.append(new_call)

        if call.call_date:
            date_obj: datetime = call.call_date
            new_date = Date(
                call_id=new_call.call_id,
                year=date_obj.year,
                month=date_obj.month,
                day=date_obj.day,
                hours=date_obj.hour,
                minutes=date_obj.minute,
                seconds=date_obj.second,
                call=new_call,
            )
            objects.append(new_date)

        for index, event in enumerate(call.events):
            new_event = Event(**(event.del_api_vars()), id=index, call=new_call)
            objects.append(new_event)

            api_vars: dict[str, str] | None = getattr(event, "api_vars", None)
            if api_vars:
                new_apivars = ApiVars(
                    id=index,
                    event_id=new_event.call_id,
                    **{
                        k: api_vars.pop(k, None)
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
                    event=new_event,
                )
                objects.append(new_apivars)

        return objects

    @staticmethod
    def add_objects(session: SQLAlchemySession, objects: list[Base]) -> None:
        """
        Добавляет подготовленные объекты в сессию.
        """
        session.add_all(objects)

    @staticmethod
    def commit_session(session: SQLAlchemySession) -> None:
        """
        Фиксирует изменения в рамках сессии.
        """
        session.commit()

    @staticmethod
    def insert_single(call: CallData) -> None:
        """
        Метод для вставки одного вызова.
        """
        with Session() as session:
            objects = Database.prepare_call_objects(call)
            Database.add_objects(session, objects)
            Database.commit_session(session)

    @staticmethod
    def insert_many(calls: Calls) -> None:
        """
        Метод для пакетной вставки нескольких вызовов.
        """
        with Session() as session:
            all_objects: list[Base] = []
            for call in calls.calls:
                objs = Database.prepare_call_objects(call)
                all_objects.extend(objs)
            Database.add_objects(session, all_objects)
            Database.commit_session(session)
