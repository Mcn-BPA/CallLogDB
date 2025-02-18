import json
from datetime import datetime
from types import Call as CallData

from core import Session
from database import engine
from models import ApiVars, Base, Call, Date, Event


class Database:

    def create_db_and_tables(self) -> None:
        Base.metadata.create_all(engine)

    def insert_data_in_tables(self, call: CallData) -> None:
        with Session() as session:

            new_call = Call(
                call_id=call.id,
                answer_date=call.answerdate,
                call_status=call.call_status,
                call_date=call.calldate,
                call_type=call.calltype,
                did=call.did,
                did_num=call.did_num,
                dst_name=call.dst_name,
                dst_num=call.dst_num,
                dst_type=call.dst_type,
                end_time=call.endtime,
                events_count=call.events_count,
                hangup_reason=call.hangup_reason,
                src_name=call.src_name,
                src_num=call.src_num,
                src_type=call.src_type,
                talk_time=call.talk_time,
                total_time=call.total_time,
                transfered_linked_to=call.transfered_linked_to,
                vpbx_id=call.vpbx_id,
                wait_time=call.wait_time,
            )

            # Преобразуем строку в объект datetime
            date_obj = datetime.strptime(call.calldate, "%Y-%m-%d %H:%M:%S")

            new_date = Date(
                call_id=call.id,
                year=date_obj.year,
                month=date_obj.month,
                day=date_obj.day,
                hours=date_obj.hour,
                minutes=date_obj.minute,
                seconds=date_obj.second,
                call=new_call,
            )

            session.add(new_call)
            session.add(new_date)

            for event in call.events:
                new_event = Event(
                    call_id=call.id,
                    event_type=event.event_type,
                    event_status=event.event_status,
                    event_dst_num=event.event_dst_num,
                    event_dst_type=event.event_dst_type,
                    event_start_time=event.event_start_time,
                    event_end_time=event.event_end_time,
                    event_talk_time=event.event_talk_time,
                    event_wait_time=event.event_wait_time,
                    event_total_time=event.event_total_time,
                    exten=getattr(event, "exten", ""),
                    name=getattr(event, "name", ""),
                    result=getattr(event, "result", ""),
                    question=getattr(event, "question", ""),
                    answer=getattr(event, "answer", ""),
                    message=getattr(event, "message", ""),
                    call=new_call,
                )
                session.add(new_event)

                api_vars = getattr(event, "api_vars", "")
                if api_vars:
                    new_apivars = ApiVars(
                        event_id=api_vars.pop("event_id", ""),
                        account_id=api_vars.pop("account_id", ""),
                        num_a=api_vars.pop("num_a", ""),
                        num_b=api_vars.pop("num_b", ""),
                        num_c=api_vars.pop("num_c", ""),
                        scenario_id=api_vars.pop("scenario_id", ""),
                        scenario_counter=api_vars.pop("scenario_counter", ""),
                        dest_link_name=api_vars.pop("dest_link_name", ""),
                        dtmf=api_vars.pop("dtmf", ""),
                        ivr_object_id=api_vars.pop("ivr_object_id", ""),
                        ivr_schema_id=api_vars.pop("ivr_schema_id", ""),
                        stt_answer=api_vars.pop("stt_answer", ""),
                        stt_question=api_vars.pop("stt_question", ""),
                        intent=api_vars.pop("intent", ""),
                        other=json.dumps(api_vars, indent=4),
                        event=new_event,
                    )
                    session.add(new_apivars)

            session.commit()
