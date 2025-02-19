import json
from dataclasses import asdict
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from calllogdb.core import DB_URL
from calllogdb.types import Call as CallData

from .models import ApiVars, Base, Call, Date, Event

engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(engine)


class Database:
    def create(self) -> None:
        Base.metadata.create_all(engine)

    def insert(self, call: CallData) -> None:
        with Session() as session:
            new_call = Call(**asdict(call))
            session.add(new_call)
            session.flush()

            # Преобразуем строку в объект datetime
            date_obj: datetime | None = call.call_date
            if date_obj:
                new_date = Date(
                    call_id=call.call_id,
                    year=date_obj.year,
                    month=date_obj.month,
                    day=date_obj.day,
                    hours=date_obj.hour,
                    minutes=date_obj.minute,
                    seconds=date_obj.second,
                    call=new_call,
                )
                session.add(new_date)

            for index, event in enumerate(call.events):
                new_event = Event(**asdict(event), id=index, call=new_call)
                session.add(new_event)
                session.flush()

                # Добавляем ApiVars, если есть
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
                    session.add(new_apivars)

            # Фиксируем транзакцию
            session.commit()
