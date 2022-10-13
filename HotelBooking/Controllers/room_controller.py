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
    room: Room
    roomType: RoomType
    reservation: Reservation
    bill_controller: BillController

    def __init__(self) -> None:
        super().__init__()
        self.room = Room()
        self.bill_controller = BillController()
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

    def check_in_room(self, room_id: str, customer_id: int):
        self.room.check_in_room(room_id, customer_id,
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def check_out_room(self, room_id: str):
        check_out_time = datetime.now()
        checked_in_room = self.room.get_room_by_id(room_id)
        stay_duration = check_out_time - \
            parser.parse(checked_in_room.status_time)
        cost = round(
            stay_duration.total_seconds() / 3600.0 * ROOM_PRICING[checked_in_room.room_type], 2)
        self.bill_controller.create_bill(checked_in_room.customer_id, cost)
        self.room.check_out_room(room_id)

