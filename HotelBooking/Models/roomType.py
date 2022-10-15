from __future__ import annotations
from sqlmodel import Field, SQLModel, Session, select
from HotelBooking.Models.utils import get_engine
from typing import Optional


class RoomType(SQLModel, table=True):
    room_type: Optional[str] = Field(default=None, primary_key=True)
    room_price: float

    def get_Price(self, type: str) -> float:
        engine = get_engine()
        session = Session(engine)
        statement = select(RoomType).where(RoomType.room_type == type)
        price = session.exec(statement).first().room_price
        session.close()
        return price
