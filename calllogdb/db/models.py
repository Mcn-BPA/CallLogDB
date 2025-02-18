from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase): ...


# Модель звонков
class Call(Base):
    __tablename__ = "call"

    call_id: Mapped[str] = mapped_column(Text, primary_key=True)
    answer_date: Mapped[datetime | None] = mapped_column()
    call_status: Mapped[str | None] = mapped_column()
    call_date: Mapped[datetime | None] = mapped_column()
    call_type: Mapped[str | None] = mapped_column()
    did: Mapped[str | None] = mapped_column()
    did_num: Mapped[str | None] = mapped_column()
    dst_name: Mapped[str | None] = mapped_column()
    dst_num: Mapped[str | None] = mapped_column()
    dst_type: Mapped[str | None] = mapped_column()
    end_time: Mapped[datetime | None] = mapped_column()
    events_count: Mapped[int | None] = mapped_column()
    hangup_reason: Mapped[str | None] = mapped_column()
    src_name: Mapped[str | None] = mapped_column()
    src_num: Mapped[str | None] = mapped_column()
    src_type: Mapped[str | None] = mapped_column()
    talk_time: Mapped[int | None] = mapped_column()
    total_time: Mapped[int | None] = mapped_column()
    transfered_linked_to: Mapped[bool] = mapped_column()
    vpbx_id: Mapped[str | None] = mapped_column()
    wait_time: Mapped[int | None] = mapped_column()

    # Связь "один-к-одному" с моделью Date
    date: Mapped["Date | None"] = relationship(
        "Date",
        back_populates="call",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Связь "один-ко-многим" с моделью Event
    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="call",
        cascade="all, delete",
        passive_deletes=True,
    )

    # магический метод для debug
    def __repr__(self) -> str:
        return (
            f"Call(call_id={self.call_id!r}, answer_date={self.answer_date!r}, "
            f"call_status={self.call_status!r}, call_date={self.call_date!r})"
        )


# Модель даты и времени
class Date(Base):
    __tablename__ = "date"

    id: Mapped[int] = mapped_column(primary_key=True)
    call_id: Mapped[str] = mapped_column(Text, ForeignKey("call.call_id", ondelete="CASCADE"))
    year: Mapped[int] = mapped_column()
    month: Mapped[int] = mapped_column()
    day: Mapped[int] = mapped_column()
    hours: Mapped[int] = mapped_column()
    minutes: Mapped[int] = mapped_column()
    seconds: Mapped[int] = mapped_column()

    # Обратная связь с моделью Call
    call: Mapped["Call"] = relationship("Call", back_populates="date")


# Модель событий звонка
class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    call_id: Mapped[str] = mapped_column(Text, ForeignKey("call.call_id", ondelete="CASCADE"), primary_key=True)
    event_type: Mapped[str | None] = mapped_column()
    event_status: Mapped[str | None] = mapped_column()
    event_dst_num: Mapped[str | None] = mapped_column()
    event_dst_type: Mapped[str | None] = mapped_column()
    event_start_time: Mapped[DateTime | None] = mapped_column()
    event_end_time: Mapped[DateTime | None] = mapped_column()
    event_talk_time: Mapped[int | None] = mapped_column()
    event_wait_time: Mapped[int | None] = mapped_column()
    event_total_time: Mapped[int | None] = mapped_column()
    exten: Mapped[str | None] = mapped_column()
    name: Mapped[str | None] = mapped_column()
    result: Mapped[str | None] = mapped_column()
    question: Mapped[str | None] = mapped_column()
    answer: Mapped[str | None] = mapped_column()
    message: Mapped[str | None] = mapped_column()

    # Связь "один-ко-многим" с моделью ApiVars
    api_vars: Mapped[list["ApiVars"]] = relationship(
        "ApiVars",
        back_populates="event",
        cascade="all, delete",
        passive_deletes=True,
    )

    # Обратная связь к модели Call (один-ко-многим)
    call: Mapped["Call"] = relationship("Call", back_populates="events")

    def __repr__(self) -> str:
        return (
            f"Event(id={self.id!r}, call_id={self.call_id!r}, event_type={self.event_type!r}, "
            f"event_status={self.event_status!r})"
        )


# Модель элемента api_vars
class ApiVars(Base):
    __tablename__ = "api_vars"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id", ondelete="CASCADE"), primary_key=True)
    account_id: Mapped[str | None] = mapped_column()
    num_a: Mapped[str | None] = mapped_column()
    num_b: Mapped[str | None] = mapped_column()
    num_c: Mapped[str | None] = mapped_column()
    scenario_id: Mapped[str | None] = mapped_column()
    scenario_counter: Mapped[str | None] = mapped_column()
    dest_link_name: Mapped[str | None] = mapped_column()
    dtmf: Mapped[str | None] = mapped_column()
    ivr_object_id: Mapped[str | None] = mapped_column()
    ivr_schema_id: Mapped[str | None] = mapped_column()
    stt_answer: Mapped[str | None] = mapped_column()
    stt_question: Mapped[str | None] = mapped_column()
    intent: Mapped[str | None] = mapped_column()
    other: Mapped[dict[str, str] | None] = mapped_column(JSONB)

    # Обратная связь с моделью Event
    event: Mapped["Event"] = relationship("Event", back_populates="api_vars")
