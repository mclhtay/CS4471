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


class ReservationController(Controller):
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

    def get_open_reservation(self, userID=None) -> List[Reservation]:
        return self.reservation.get_reservation_with_status("OPEN",userID)
    def get_reservation(self, userID=None) -> List[Reservation]:
        return self.reservation.get_reservation_by_customer_id(userID)
    def get_stay(self, userID=None) -> List[Reservation]:
        return self.reservation.get_reservation_with_status("CLOSED",userID)
    def reserve_room(self, room_id: str, customer_id: int, startDate, duration: int):
        self.room.update_room_status(room_id, "RESERVED", customer_id)
        r = self.room.get_room_by_id(room_id)
        price = float(self.roomType.get_Price(r.room_type))
        duration = int(duration)
        bill:Bill = self.bill_controller.create_bill(customer_id, price*duration)
        self.reservation.create_reservation("OPEN", customer_id, room_id, bill.bill_id, startDate, duration)

    def cancel_reservation(self, room_id: str, reservation_id:int):
        self.room.update_room_status(room_id, "AVAILABLE")
        self.reservation.update_reservation_status(reservation_id, "CANCELED")
        self.bill_controller.cancel_bill(self.reservation.get_reservation_by_id(reservation_id).bill_id)

    def modify_reservation_date(self, reservation_id:int, newStartDate:str):
        self.reservation.update_reservation_start_date(reservation_id, newStartDate)
        self.bill_controller

    def modify_reservation_duration(self, reservation_id:int, newDuration:int):
        self.reservation.update_reservation_duration(reservation_id, newDuration)
        currentReservation = self.reservation.get_reservation_by_id(reservation_id)
        price:float=self.roomType.get_Price(self.room.get_room_by_id(currentReservation.room_id).room_type)
        self.bill_controller
        newBillID=self.bill_controller.modify(self.reservation.get_reservation_by_id(reservation_id).bill_id, price*newDuration)
        self.reservation.update_Bill(reservation_id, newBillID)

