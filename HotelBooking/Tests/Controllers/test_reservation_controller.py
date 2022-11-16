from unittest.mock import patch, ANY
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Models.bill import Bill
from HotelBooking.Models.reservation import Reservation
from HotelBooking.Models.room import Room, ROOM_STATUS, ROOM_TYPE
from sqlmodel import create_engine, Session, SQLModel

from HotelBooking.Models.room_type import RoomType


class TestRoomController:
    @patch.object(Reservation, "get_reservations_with_status")
    def test_get_open_reservations(self, mock_get_reservations_with_status):
        mock_id = 1
        controller = ReservationController()
        controller.get_open_reservations(mock_id)

        mock_get_reservations_with_status.assert_called_once_with(
            "OPEN", mock_id)

    @patch.object(Reservation, "get_reservations_by_customer_id")
    def test_get_reservations(self, mock_get_reservations_by_customer_id):
        mock_id = 1
        controller = ReservationController()
        controller.get_reservations(mock_id)

        mock_get_reservations_by_customer_id.assert_called_once_with(
            mock_id)

    @patch.object(Reservation, "get_reservations_with_status")
    def test_get_stay_history(self, mock_get_reservations_with_status):
        mock_id = 1
        controller = ReservationController()
        controller.get_stay_history(mock_id)

        mock_get_reservations_with_status.assert_called_once_with(
            "CLOSED", mock_id)

    @patch.object(Room, "update_room_status")
    @patch.object(Room, "get_room_by_id")
    @patch.object(RoomType, "get_price")
    @patch.object(Bill, "create_bill")
    @patch.object(Reservation, "create_reservation")
    def test_reserve_room(self, mock_create_reservation, mock_create_bill, mock_get_price, mock_get_room_by_id, mock_update_room_status):
        controller = ReservationController()
        mock_room_id = "single1"
        mock_customer_id = "test"
        mock_start_date = "testDate"
        mock_duration = 5
        mock_status = "OPEN"
        mock_bill_id = 2
        mock_room_price = 20.1
        mock_is_accessibility_requested=1
        mock_room_type = ROOM_TYPE["SINGLE"]
        mock_create_bill.return_value = Bill(
            bill_id=mock_bill_id, bill_status="CANCELED", bill_amount=1100)
        mock_get_price.return_value = mock_room_price

        mock_get_room_by_id.return_value = Room(
            room_id=mock_room_id, room_type=mock_room_type)
        controller.reserve_room(
            mock_room_id, mock_customer_id, mock_start_date, mock_duration, mock_is_accessibility_requested, mock_status)

        mock_create_reservation.assert_called_once_with(
            mock_status, mock_customer_id, mock_room_id, mock_bill_id, mock_start_date, mock_duration, mock_is_accessibility_requested
        )
        mock_create_bill.assert_called_once_with(
            mock_customer_id, mock_duration*mock_room_price)
        mock_get_price.assert_called_once_with(mock_room_type)
        mock_get_room_by_id.assert_called_once_with(mock_room_id)
        mock_update_room_status.assert_called_once_with(
            mock_room_id, "RESERVED")

    @patch.object(Room, "update_room_status")
    @patch.object(Reservation, "update_reservation_status")
    @patch.object(Bill, "cancel_bill")
    @patch.object(Reservation, "get_reservation_by_id")
    def test_cancel_reservation(self, mock_get_reservation_by_id, mock_cancel_bill, mock_update_reservation_status, mock_update_room_status):
        mock_reservation_id = 1
        mock_bill_id = 2
        mock_room_id = "single1"

        res = Reservation(reservation_id=mock_reservation_id, status="OPEN", customer_id="test",
                          room_id=mock_room_id, bill_id=mock_bill_id, reservation_checkin_date="2000/11/03", reservation_stay_date=5, is_accessibility_requested=1)
        mock_get_reservation_by_id.return_value = res

        controller = ReservationController()
        controller.cancel_reservation(mock_room_id, mock_reservation_id)
        mock_get_reservation_by_id.assert_called_once_with(mock_reservation_id)
        mock_cancel_bill.assert_called_once_with(mock_bill_id)
        mock_update_reservation_status.assert_called_once_with(
            mock_reservation_id, "CANCELED")
        mock_update_room_status.assert_called_once_with(
            mock_room_id, "AVAILABLE")

    @ patch.object(Reservation, "update_reservation_start_date")
    def test_modify_reservation_date(self, mock_update_reservation_start_date):
        mock_id = 1
        mock_start_date = "testDate"
        controller = ReservationController()
        controller.modify_reservation_date(mock_id, mock_start_date)

        mock_update_reservation_start_date.assert_called_once_with(
            mock_id, mock_start_date)

    @patch.object(Reservation, "update_reservation_duration")
    @patch.object(Reservation, "get_reservation_by_id")
    @patch.object(RoomType, "get_price")
    @patch.object(Room, "get_room_by_id")
    @patch.object(BillController, "modify")
    @patch.object(Reservation, "update_Bill")
    def test_modify_reservation_duration(self, mock_update_Bill, mock_modify, mock_get_room_by_id, mock_get_price, mock_get_reservation_by_id, mock_update_reservation_duration):
        controller = ReservationController()
        mock_room_id = "single1"
        mock_room_price = 20.1
        mock_duration = 5
        mock_reservation_id = 6
        mock_customer_id = "test"
        mock_start_date = "testDate"
        mock_status = "OPEN"
        mock_bill_id = 2
        mock_room_type = ROOM_TYPE["SINGLE"]

        mock_modify.return_value = mock_bill_id

        mock_get_price.return_value = mock_room_price

        mock_get_room_by_id.return_value = Room(
            room_id=mock_room_id, room_type=mock_room_type)

        res = Reservation(reservation_id=mock_reservation_id, status="OPEN", customer_id="test",
                          room_id=mock_room_id, bill_id=mock_bill_id, reservation_checkin_date="2000/11/03", reservation_stay_date=5, is_accessibility_requested=1)
        mock_get_reservation_by_id.return_value = res

        controller.modify_reservation_duration(
            mock_reservation_id, mock_duration)

        mock_update_Bill.assert_called_once_with(
            mock_reservation_id, mock_bill_id)

        mock_modify.assert_called_once_with(
            mock_bill_id, mock_duration*mock_room_price)

        mock_get_room_by_id.assert_called_once_with(mock_room_id)

        mock_get_price.assert_called_once_with(mock_room_type)
        mock_get_reservation_by_id.assert_called_once_with(mock_reservation_id)

        mock_update_reservation_duration.assert_called_once_with(
            mock_reservation_id, mock_duration)
