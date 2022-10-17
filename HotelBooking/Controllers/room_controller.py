from datetime import datetime
from tracemalloc import start
from typing import List
from HotelBooking.Controllers.controller import Controller
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Models import reservation
from HotelBooking.Models.bill import Bill
from HotelBooking.Models.reservation import Reservation
from HotelBooking.Models.room import Room
from dateutil import parser

from HotelBooking.Models.roomType import RoomType

# Cost per hour of stay
ROOM_PRICING = {
    "SINGLE": 10,
    "DOUBLE": 12.5,
    "DELUXE": 15,
    "PRESIDENTIAL": 20
}


class RoomController(Controller):
    # TODO: Add customer validation logic when reserving/checking-in rooms
    room: Room
    roomType: RoomType
    reservation: Reservation
    bill: Bill

    def __init__(self) -> None:
        super().__init__()
        self.room = Room()
        self.bill = Bill()
        self.roomType = RoomType()
        self.reservation = Reservation()

    def get_checked_in_rooms(self) -> List[Room]:
        return self.room.get_checked_in_rooms()

    def get_reserved_rooms(self, userID=None) -> List[Room]:
        return self.room.get_reserved_rooms(userID)

    def get_available_rooms(self) -> List[Room]:
        return self.room.get_available_rooms()

    def get_room(self, id) -> Room:
        return self.room.get_room_by_id(id)

    def get_reserved_room(self, customer_id: int) -> Room:
        return self.room.get_reserved_room(customer_id)

    def check_in_room(self, room_id: str, customer_id: int, reservation_id: int):
        self.room.check_in_room(room_id, customer_id)
        self.reservation.update_reservation_status(
            reservation_id, "IN_PROGRESS")

    def check_out_room(self, room_id: str):
        self.room.check_out_room(room_id)
        self.reservation.close_reservation_with_room_id(
            room_id)
