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
    """
    Reservation controller class used for all actions associated with reservations
    """
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
        """
        Gets all reservations with open status for the given customer ID
        """
        return self.reservation.get_reservations_with_status("OPEN", user_id)

    def get_reservations(self, user_id=None) -> List[Reservation]:
        """
        Gets all reservations for the given customer ID
        """
        return self.reservation.get_reservations_by_customer_id(user_id)

    def get_stay_history(self, user_id=None) -> List[Reservation]:
        """
        Gets all reservations with closed status for the given customer ID
        """
        return self.reservation.get_reservations_with_status("CLOSED", user_id)

    def reserve_room(self, room_id: str, customer_id: int, start_date, duration: int, is_accessibility_requested: int, status: str = None):
        """
        Reserves a room for a customer with the given parameters
        """
        self.room.update_room_status(room_id, "RESERVED")
        r = self.room.get_room_by_id(room_id)
        price = float(self.room_type.get_price(r.room_type))
        duration = int(duration)
        bill: Bill = self.bill_controller.create_bill(
            customer_id, price*duration)
        if (status == "IN_PROGRESS"):
            self.reservation.create_reservation(
                status, customer_id, room_id, bill.bill_id, start_date, duration, is_accessibility_requested)
            self.room.check_in_room(room_id)
        else:
            self.reservation.create_reservation(
                "OPEN", customer_id, room_id, bill.bill_id, start_date, duration, is_accessibility_requested)

    def cancel_reservation(self, room_id: str, reservation_id: int):
        """
        Cancels a reservation with the given room and reservation IDs
        """
        self.room.update_room_status(room_id, "AVAILABLE")
        self.reservation.update_reservation_status(reservation_id, "CANCELED")
        self.bill_controller.cancel_bill(
            self.reservation.get_reservation_by_id(reservation_id).bill_id)

    def modify_reservation_date(self, reservation_id: int, new_start_date: str):
        """
        Modifies a reservation start date for the given reservation ID
        """
        self.reservation.update_reservation_start_date(
            reservation_id, new_start_date)

    def modify_reservation_duration(self, reservation_id: int, new_duration: int):
        """
        Modifies a reservation duration for the given reservation ID
        """
        self.reservation.update_reservation_duration(
            reservation_id, new_duration)
        current_reservation = self.reservation.get_reservation_by_id(
            reservation_id)
        price: float = self.room_type.get_price(
            self.room.get_room_by_id(current_reservation.room_id).room_type)
        new_bill_id = self.bill_controller.modify(
            current_reservation.bill_id, price*new_duration)
        self.reservation.update_Bill(reservation_id, new_bill_id)
