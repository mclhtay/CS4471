from unittest.mock import patch, ANY
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Models.bill import Bill
from HotelBooking.Models.room import Room, ROOM_STATUS, ROOM_TYPE
from sqlmodel import create_engine, Session, SQLModel


class TestRoomController:
    @patch.object(Room, "get_checked_in_rooms")
    def test_get_checked_in_rooms(self, mock_get_checked_in_rooms):
        controller = RoomController()
        controller.get_checked_in_rooms()

        mock_get_checked_in_rooms.assert_called_once()

    @patch.object(Room, "get_reserved_rooms")
    def test_get_checked_in_rooms(self, mock_get_reserved_rooms):
        controller = RoomController()
        controller.get_reserved_rooms()

        mock_get_reserved_rooms.assert_called_once()

    @patch.object(Room, "get_available_rooms")
    def test_get_available_rooms(self, mock_get_available_rooms):
        controller = RoomController()
        controller.get_available_rooms()

        mock_get_available_rooms.assert_called_once()

    @patch.object(Room, "check_in_room")
    def test_check_in_room(self, mock_check_in_room):
        mock_id = "1"

        controller = RoomController()
        controller.check_in_room(mock_id, mock_id)

        mock_check_in_room.assert_called_once_with(mock_id, mock_id, ANY)

    @patch.object(Room, "get_room_by_id")
    @patch.object(Room, "check_out_room")
    @patch.object(BillController, "create_bill")
    def test_check_out_room(self, mock_create_bill, mock_check_out_room, mock_get_room_by_id, ):
        expected_room_id = "single1"
        mock_get_room_by_id.return_value = Room(
            room_id=expected_room_id, room_type=ROOM_TYPE["SINGLE"], status_time="2022-10-01, 1:1:1", customer_id=1)

        controller = RoomController()
        controller.check_out_room(expected_room_id)

        mock_get_room_by_id.assert_called_once_with(expected_room_id)
        mock_create_bill.assert_called_once_with(1, ANY)
        mock_check_out_room.assert_called_once_with(expected_room_id)

    @patch.object(Room, "reserve_room")
    def test_reserve_room(self, mock_reserve_room):
        mock_id = "1"

        controller = RoomController()
        controller.reserve_room(mock_id, mock_id)

        mock_reserve_room.assert_called_once_with(mock_id, mock_id, ANY)

    @patch.object(Room, "cancel_reservation")
    def test_cancel_reservation(self, mock_cancel_reservation):
        mock_id = "1"

        controller = RoomController()
        controller.cancel_reservation(mock_id)

        mock_cancel_reservation.assert_called_once_with(mock_id)
