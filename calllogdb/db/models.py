from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase): ...


# Модель звонков
class Call(Base):
    __tablename__ = "call"

    call_id = Column(Text, primary_key=True)
    answer_date = Column(DateTime)
    call_status = Column(Text)
    call_date = Column(DateTime)
    call_type = Column(Text)
    did = Column(Text)
    did_num = Column(Text)
    dst_name = Column(Text)
    dst_num = Column(Text)
    dst_type = Column(Text)
    end_time = Column(DateTime)
    events_count = Column(Integer)
    hangup_reason = Column(Text)
    src_name = Column(Text)
    src_num = Column(Text)
    src_type = Column(Text)
    talk_time = Column(Integer)
    total_time = Column(Integer)
    transfered_linked_to = Column(Boolean)
    vpbx_id = Column(Text)
    wait_time = Column(Integer)

    # Связь "один-к-одному" с моделью Date
    date = relationship(
        "Date",
        back_populates="call",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Связь "один-ко-многим" с моделью Event
    events = relationship(
        "Event",
        back_populates="call",
        cascade="all, delete",
        passive_deletes=True,
    )


# Модель даты и времени
class Date(Base):
    __tablename__ = "date"

    id = Column(Integer, primary_key=True, unique=True)
    call_id = Column(Text, ForeignKey("call.call_id", ondelete="CASCADE"), unique=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    hours = Column(Integer)
    minutes = Column(Integer)
    seconds = Column(Integer)

    # Обратная связь
    call = relationship("Call", back_populates="date")


# Модель событий звонка
class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, unique=True)
    call_id = Column(Text, ForeignKey("call.call_id", ondelete="CASCADE"), unique=True)
    event_type = Column(Text)
    event_status = Column(Text)
    event_dst_num = Column(Text)
    event_dst_type = Column(Text)
    event_start_time = Column(DateTime)
    event_end_time = Column(DateTime)
    event_talk_time = Column(Integer)
    event_wait_time = Column(Integer)
    event_total_time = Column(Integer)
    exten = Column(Text)
    name = Column(Text)
    result = Column(Text)
    question = Column(Text)
    answer = Column(Text)
    message = Column(Text)

    # Связь "один-ко-многим"
    api_vars = relationship("ApiVars", back_populates="event", cascade="all, delete", passive_deletes=True)

    # Обратная связь
    call = relationship("Call", back_populates="event")


# Модель элемента api_vars
class ApiVars(Base):
    __tablename__ = "api_vars"

    id = Column(Integer, primary_key=True, unique=True)
    event_id = Column(Integer, ForeignKey("event.id", ondelete="CASCADE"), unique=True)
    account_id = Column(Text)
    num_a = Column(Text)
    num_b = Column(Text)
    num_c = Column(Text)
    scenario_id = Column(Text)
    scenario_counter = Column(Text)
    dest_link_name = Column(Text)
    dtmf = Column(Text)
    ivr_object_id = Column(Text)
    ivr_schema_id = Column(Text)
    stt_answer = Column(Text)
    stt_question = Column(Text)
    intent = Column(Text)
    other = Column(JSON)

    # Обратная связь
    event = relationship("Event", back_populates="api_vars")
