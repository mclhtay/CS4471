from datetime import datetime
from typing import List
from HotelBooking.Controllers.controller import Controller
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Models.room import Room
from dateutil import parser

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
    bill_controller: BillController

    def __init__(self) -> None:
        super().__init__()
        self.room = Room()
        self.bill_controller = BillController()

    def get_checked_in_rooms(self) -> List[Room]:
        return self.room.get_checked_in_rooms()

    def get_reserved_rooms(self) -> List[Room]:
        return self.room.get_reserved_rooms()

    def get_available_rooms(self) -> List[Room]:
        return self.room.get_available_rooms()

    def get_reserved_room(self, customer_id: int) -> Room:
        return self.room.get_reserved_room(customer_id)

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

    def reserve_room(self, room_id: str, customer_id: int):
        self.room.reserve_room(room_id, customer_id,
                               datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def cancel_reservation(self, room_id: str):
        self.room.cancel_reservation(room_id)
