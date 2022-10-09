from __future__ import annotations
from typing import Optional, List
from sqlmodel import Field, SQLModel, Session, select
from HotelBooking.Models.utils import get_engine
from HotelBooking.Models.customer import Customer
from typing import Optional

ROOM_TYPE = {
    "SINGLE": "SINGLE",
    "DOUBLE": "DOUBLE",
    "DELUXE": "DELUXE",
    "PRESIDENTIAL": "PRESIDENTIAL"
}

ROOM_STATUS = {
    "CHECKED-IN": "CHECKED-IN",
    "RESERVED": "RESERVED",
    "AVAILABLE": "AVAILABLE"
}


class Room(SQLModel, table=True):
    room_id: Optional[str] = Field(primary_key=True)
    room_type: str
    room_status: str = Field(default="AVAILABLE")
    status_time: Optional[str]
    customer_id: Optional[int] = Field(foreign_key=Customer.customer_id)

    def get_room_with_status(self, room_status: ROOM_STATUS) -> List[Room]:
        engine = get_engine()
        session = Session(engine)
        statement = select(Room).where(
            Room.room_status == room_status)

        rooms = session.exec(statement).all()
        session.close()
        return rooms

    def get_room_by_id(self, room_id: str) -> Room:
        engine = get_engine()
        session = Session(engine)
        statement = select(Room).where(
            Room.room_id == room_id)

        room = session.exec(statement).first()
        session.close()
        return room

    def update_room_status(self, room_id: str, room_status: ROOM_STATUS, customer_id=None, status_time=None):
        room = self.get_room_by_id(room_id)
        room.room_status = room_status
        room.customer_id = customer_id
        room.status_time = status_time

        engine = get_engine()
        session = Session(engine)
        session.add(room)
        session.commit()
        session.close()

    def get_checked_in_rooms(self) -> List[Room]:
        return self.get_room_with_status(ROOM_STATUS["CHECKED-IN"])

    def get_reserved_rooms(self) -> List[Room]:
        return self.get_room_with_status(ROOM_STATUS["RESERVED"])

    def get_available_rooms(self) -> List[Room]:
        return self.get_room_with_status(ROOM_STATUS["AVAILABLE"])

    def check_in_room(self, room_id: str, customer_id: int, checked_in_time: str):
        self.update_room_status(
            room_id, ROOM_STATUS["CHECKED-IN"], customer_id, checked_in_time)

    def check_out_room(self, room_id: str):
        self.update_room_status(room_id, ROOM_STATUS["AVAILABLE"])

    def reserve_room(self, room_id: str, customer_id: int, reserved_time: str):
        self.update_room_status(
            room_id, ROOM_STATUS["RESERVED"], customer_id, reserved_time)

    def cancel_reservation(self, room_id: str):
        self.update_room_status(room_id, ROOM_STATUS["AVAILABLE"])
