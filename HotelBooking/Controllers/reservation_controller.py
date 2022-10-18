from datetime import datetime
from tracemalloc import start
from typing import List
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Controllers.controller import Controller
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Models import reservation
from HotelBooking.Models.bill import Bill
from HotelBooking.Models.reservation import Reservation
from HotelBooking.Models.room import Room
from dateutil import parser

from HotelBooking.Models.room_type import RoomType


class ReservationController(Controller):
    room: Room
    room_type: RoomType
    reservation: Reservation
    bill_controller: BillController
    room_controller: RoomController

    def __init__(self) -> None:
        super().__init__()
        self.room = Room()
        self.bill_controller = BillController()
        self.room_type = RoomType()
        self.reservation = Reservation()

    def get_open_reservations(self, user_id=None) -> List[Reservation]:
        return self.reservation.get_reservations_with_status("OPEN", user_id)

    def get_reservations(self, user_id=None) -> List[Reservation]:
        return self.reservation.get_reservations_by_customer_id(user_id)

    def get_stay_history(self, user_id=None) -> List[Reservation]:
        return self.reservation.get_reservations_with_status("CLOSED", user_id)

    def reserve_room(self, room_id: str, customer_id: int, start_date, duration: int, status: str = None):
        self.room.update_room_status(room_id, "RESERVED")
        r = self.room.get_room_by_id(room_id)
        price = float(self.room_type.get_price(r.room_type))
        duration = int(duration)
        bill: Bill = self.bill_controller.create_bill(
            customer_id, price*duration)
        if (status == "IN_PROGRESS"):
            self.reservation.create_reservation(
                status, customer_id, room_id, bill.bill_id, start_date, duration)
            self.room.check_in_room(room_id)
        else:
            self.reservation.create_reservation(
                "OPEN", customer_id, room_id, bill.bill_id, start_date, duration)

    def cancel_reservation(self, room_id: str, reservation_id: int):
        self.room.update_room_status(room_id, "AVAILABLE")
        self.reservation.update_reservation_status(reservation_id, "CANCELED")
        self.bill_controller.cancel_bill(
            self.reservation.get_reservation_by_id(reservation_id).bill_id)

    def modify_reservation_date(self, reservation_id: int, new_start_date: str):
        self.reservation.update_reservation_start_date(
            reservation_id, new_start_date)

    def modify_reservation_duration(self, reservation_id: int, new_duration: int):
        self.reservation.update_reservation_duration(
            reservation_id, new_duration)
        current_reservation = self.reservation.get_reservation_by_id(
            reservation_id)
        price: float = self.room_type.get_price(
            self.room.get_room_by_id(current_reservation.room_id).room_type)
        new_bill_id = self.bill_controller.modify(
            current_reservation.bill_id, price*new_duration)
        self.reservation.update_Bill(reservation_id, new_bill_id)
