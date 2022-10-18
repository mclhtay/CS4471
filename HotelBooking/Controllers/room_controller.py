from typing import List
from HotelBooking.Controllers.controller import Controller
from HotelBooking.Models.bill import Bill
from HotelBooking.Models.reservation import Reservation
from HotelBooking.Models.room import Room
from HotelBooking.Models.room_type import RoomType


class RoomController(Controller):
    room: Room
    room_type: RoomType
    reservation: Reservation
    bill: Bill

    def __init__(self) -> None:
        super().__init__()
        self.room = Room()
        self.bill = Bill()
        self.room_type = RoomType()
        self.reservation = Reservation()

    def get_checked_in_rooms(self) -> List[Room]:
        return self.room.get_checked_in_rooms()

    def get_reserved_rooms(self) -> List[Room]:
        return self.room.get_reserved_rooms()

    def get_available_rooms(self) -> List[Room]:
        return self.room.get_available_rooms()

    def get_price(self, room_type: str) -> float:
        return self.room_type.get_price(room_type)

    def get_room(self, id) -> Room:
        return self.room.get_room_by_id(id)

    def check_in_room(self, room_id: str, reservation_id: int):
        self.room.check_in_room(room_id)
        self.reservation.update_reservation_status(
            reservation_id, "IN_PROGRESS")

    def check_out_room(self, room_id: str):
        self.room.check_out_room(room_id)
        self.reservation.close_reservation_with_room_id(
            room_id)
