from sqlalchemy import Integer, String, DateTime, func, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MsgLog(Base):
    __tablename__ = 'msg_log'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    msg_id: Mapped[int] = mapped_column(Integer, index=True)
    from_call_id: Mapped[str] = mapped_column(String(50))
    from_display_name: Mapped[str] = mapped_column(String(50))
    time_stamp: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    send: Mapped[int] = mapped_column(Integer)
    date_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
