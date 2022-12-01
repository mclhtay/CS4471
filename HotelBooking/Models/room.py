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

    # unique id of the room
    room_id: Optional[str] = Field(primary_key=True)

    # type of the room
    room_type: str

    # status of the room
    room_status: str = Field(default="AVAILABLE")

    def get_room_with_status(self, room_status: ROOM_STATUS) -> List[Room]:
        """get list of room with a given status"""
        engine = get_engine()
        session = Session(engine)
        statement = select(Room).where(
            Room.room_status == room_status)

        rooms = session.exec(statement).all()
        session.close()
        return rooms

    def get_room_by_id(self, room_id: str) -> Room:
        """get room object given room id"""
        engine = get_engine()
        session = Session(engine)
        statement = select(Room).where(
            Room.room_id == room_id)
        room = session.exec(statement).first()

        session.close()
        return room

    def update_room_status(self, room_id: str, room_status: ROOM_STATUS):
        """update the status of a room"""
        room = self.get_room_by_id(room_id)
        room.room_status = room_status

        engine = get_engine()
        session = Session(engine)
        session.add(room)
        session.commit()
        session.close()

    def get_checked_in_rooms(self) -> List[Room]:
        """get all check-in rooms"""
        return self.get_room_with_status(ROOM_STATUS["CHECKED-IN"])

    def get_reserved_rooms(self) -> List[Room]:
        """get all reserved rooms"""
        return self.get_room_with_status(ROOM_STATUS["RESERVED"])

    def get_available_rooms(self) -> List[Room]:
        """get all available rooms"""
        return self.get_room_with_status(ROOM_STATUS["AVAILABLE"])

    def check_in_room(self, room_id: str):
        """change the status of a given room to check-in"""
        self.update_room_status(
            room_id, ROOM_STATUS["CHECKED-IN"])

    def check_out_room(self, room_id: str):
        """change the status of a given room to available"""
        self.update_room_status(room_id, ROOM_STATUS["AVAILABLE"])
