from unittest.mock import patch, ANY
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Models.bill import Bill
from HotelBooking.Models.reservation import Reservation
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
    @patch.object(Reservation, "update_reservation_status")
    def test_check_in_room(self, mock_update_reservation_status, mock_check_in_room):
        expected_room_id = "single1"
        expected_res_id = 1

        controller = RoomController()

        controller.check_in_room(expected_room_id, expected_res_id)

        mock_check_in_room.assert_called_once_with(
            expected_room_id)
        mock_update_reservation_status.assert_called_once_with(
            expected_res_id, "IN_PROGRESS")

    @patch.object(Room, "check_out_room")
    @patch.object(Reservation, "close_reservation_with_room_id")
    def test_check_out_room(self, mock_check_out_room, mock_close_reservation_with_room_id):
        expected_room_id = "single1"

        controller = RoomController()
        controller.check_out_room(expected_room_id)

        mock_close_reservation_with_room_id.assert_called_once_with(
            expected_room_id)
        mock_check_out_room.assert_called_once_with(
            expected_room_id)
