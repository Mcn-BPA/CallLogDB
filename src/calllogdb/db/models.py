from datetime import datetime, timedelta

from sqlalchemy import Boolean, DateTime, ForeignKey, ForeignKeyConstraint, Integer, Interval, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Модель звонков
class Call(Base):
    __tablename__ = "call"

    call_id: Mapped[str] = mapped_column(Text, primary_key=True)

    call_status: Mapped[str | None] = mapped_column(Text)
    call_type: Mapped[str | None] = mapped_column(Text)
    did: Mapped[str | None] = mapped_column(Text)
    dst_name: Mapped[str | None] = mapped_column(Text)
    dst_num: Mapped[str | None] = mapped_column(Text)
    dst_type: Mapped[str | None] = mapped_column(Text)
    src_name: Mapped[str | None] = mapped_column(Text)
    src_num: Mapped[str | None] = mapped_column(Text)
    src_type: Mapped[str | None] = mapped_column(Text)
    hangup_reason: Mapped[str | None] = mapped_column(Text)
    call_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    answer_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    events_count: Mapped[int | None] = mapped_column(Integer)
    total_time: Mapped[timedelta | None] = mapped_column(Interval)
    wait_time: Mapped[timedelta | None] = mapped_column(Interval)
    talk_time: Mapped[timedelta | None] = mapped_column(Interval)
    vpbx_id: Mapped[str | None] = mapped_column(Text)
    ls_number: Mapped[str | None] = mapped_column(Text)
    transfered_linked_to: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    # Связь "один-к-одному" с моделью Date
    date: Mapped["Date | None"] = relationship(
        "Date",
        back_populates="call",
        uselist=False,
        cascade="all, delete",
        passive_deletes=True,
    )

    # Связь "один-ко-многим" с моделью Event
    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="call",
        cascade="all, delete",
        passive_deletes=True,
        lazy="selectin",
    )


# Модель даты и времени
class Date(Base):
    __tablename__ = "date"

    call_id: Mapped[str] = mapped_column(Text, ForeignKey("call.call_id", ondelete="CASCADE"), primary_key=True)

    year: Mapped[int] = mapped_column(Integer)
    month: Mapped[int] = mapped_column(Integer)
    day: Mapped[int] = mapped_column(Integer)
    hours: Mapped[int] = mapped_column(Integer)
    minutes: Mapped[int] = mapped_column(Integer)
    seconds: Mapped[int] = mapped_column(Integer)

    # Обратная связь с моделью Call
    call: Mapped["Call"] = relationship("Call", back_populates="date", uselist=False)


# Модель событий звонка
class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_id: Mapped[str] = mapped_column(Text, ForeignKey("call.call_id", ondelete="CASCADE"), primary_key=True)

    event_type: Mapped[str | None] = mapped_column(Text)
    event_status: Mapped[str | None] = mapped_column(Text)
    event_dst_num: Mapped[str | None] = mapped_column(Text)
    event_dst_name: Mapped[str | None] = mapped_column(Text)
    event_dst_type: Mapped[str | None] = mapped_column(Text)
    event_did: Mapped[str | None] = mapped_column(Text)
    event_transfered_from: Mapped[str | None] = mapped_column(Text)
    event_start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    event_end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    event_answer_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    event_total_time: Mapped[timedelta | None] = mapped_column(Interval)
    event_talk_time: Mapped[timedelta | None] = mapped_column(Interval)
    event_wait_time: Mapped[timedelta | None] = mapped_column(Interval)
    target_number: Mapped[str | None] = mapped_column(Text)
    exten: Mapped[str | None] = mapped_column(Text)
    name: Mapped[str | None] = mapped_column(Text)
    result: Mapped[str | None] = mapped_column(Text)
    question: Mapped[str | None] = mapped_column(Text)
    answer: Mapped[str | None] = mapped_column(Text)
    message: Mapped[str | None] = mapped_column(Text)
    number: Mapped[str | None] = mapped_column(Text)

    # Связь "один-ко-многим" с моделью ApiVars
    api_vars: Mapped[list["ApiVars"]] = relationship(
        "ApiVars",
        back_populates="event",
        cascade="all, delete",
        passive_deletes=True,
        lazy="selectin",
    )

    # Обратная связь к модели Call (один-ко-многим)
    call: Mapped["Call"] = relationship("Call", back_populates="events")


# Модель элемента api_vars
class ApiVars(Base):
    __tablename__ = "api_vars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[str] = mapped_column(Text, primary_key=True)

    account_id: Mapped[str | None] = mapped_column(Text)
    num_a: Mapped[str | None] = mapped_column(Text)
    num_b: Mapped[str | None] = mapped_column(Text)
    num_c: Mapped[str | None] = mapped_column(Text)
    scenario_id: Mapped[str | None] = mapped_column(Text)
    scenario_counter: Mapped[str | None] = mapped_column(Text)
    dest_link_name: Mapped[str | None] = mapped_column(Text)
    dtmf: Mapped[str | None] = mapped_column(Text)
    ivr_object_id: Mapped[str | None] = mapped_column(Text)
    ivr_schema_id: Mapped[str | None] = mapped_column(Text)
    stt_answer: Mapped[str | None] = mapped_column(Text)
    stt_question: Mapped[str | None] = mapped_column(Text)
    intent: Mapped[str | None] = mapped_column(Text)
    other: Mapped[dict[str, str] | None] = mapped_column(JSONB)

    __table_args__ = (
        ForeignKeyConstraint(
            ["id", "event_id"],
            ["event.id", "event.call_id"],
            ondelete="CASCADE",
        ),
    )

    # Обратная связь с моделью Event
    event: Mapped["Event"] = relationship("Event", back_populates="api_vars")
