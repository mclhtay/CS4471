from __future__ import annotations
from sqlmodel import Field, SQLModel, Session, select
from HotelBooking.Models.utils import get_engine
from typing import Optional


class RoomType(SQLModel, table=True):

    # unique name of the room type
    room_type: Optional[str] = Field(default=None, primary_key=True)

    # price per night of the room type
    room_price: float

    def get_price(self, type: str) -> float:
        """get the price of the given rrom type"""
        engine = get_engine()
        session = Session(engine)
        statement = select(RoomType).where(RoomType.room_type == type)
        price = session.exec(statement).first().room_price
        session.close()
        return price
