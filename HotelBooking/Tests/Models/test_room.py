from unittest.mock import patch
from sqlmodel import create_engine, Session, SQLModel
from HotelBooking.Models.room import Room, ROOM_STATUS, ROOM_TYPE


class TestRoom:
    def test_get_room_with_status(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            room_1 = Room(room_id="double1", room_type=ROOM_TYPE["DOUBLE"])
            room_2 = Room(room_id="presidential1",
                          room_type=ROOM_TYPE["PRESIDENTIAL"])
            room_3 = Room(room_id="single1", room_type=ROOM_TYPE["SINGLE"])
            room_4 = Room(room_id="single2", room_type=ROOM_TYPE["SINGLE"], room_status=ROOM_STATUS[
                          "RESERVED"], customer_id=1)
            room_5 = Room(room_id="deluxe1", room_type=ROOM_TYPE["DELUXE"], room_status=ROOM_STATUS[
                          "CHECKED-IN"], customer_id=2)
            session.add(room_1)
            session.add(room_2)
            session.add(room_3)
            session.add(room_4)
            session.add(room_5)
            session.commit()
            session.refresh(room_1)
            session.refresh(room_2)
            session.refresh(room_3)
            session.refresh(room_4)
            session.refresh(room_5)
            session.close()

            available_rooms = Room().get_room_with_status(
                ROOM_STATUS["AVAILABLE"])
            reserved_rooms = Room().get_room_with_status(
                ROOM_STATUS["RESERVED"])
            checked_in_rooms = Room().get_room_with_status(
                ROOM_STATUS["CHECKED-IN"])

            assert len(available_rooms) == 3
            assert len(reserved_rooms) == 1
            assert len(checked_in_rooms) == 1
            assert room_1 in available_rooms
            assert room_2 in available_rooms
            assert room_3 in available_rooms
            assert room_4 in reserved_rooms
            assert room_5 in checked_in_rooms

    def test_get_room_by_id(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            expected_id_1 = "double1"
            expected_id_2 = "presidential1"
            room_1 = Room(room_id=expected_id_1, room_type=ROOM_TYPE["DOUBLE"])
            room_2 = Room(room_id=expected_id_2,
                          room_type=ROOM_TYPE["PRESIDENTIAL"])
            session.add(room_1)
            session.add(room_2)
            session.commit()
            session.refresh(room_1)
            session.refresh(room_2)
            session.close()

            res_1 = Room().get_room_by_id(expected_id_1)
            res_2 = Room().get_room_by_id(expected_id_2)

            assert res_1 == room_1
            assert res_2 == room_2

    def test_update_room_status(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            expected_id_1 = "double1"
            expected_id_2 = "presidential1"
            expected_id_3 = "deluxe1"
            room_1 = Room(room_id=expected_id_1, room_type=ROOM_TYPE["DOUBLE"])
            room_2 = Room(room_id=expected_id_2,
                          room_type=ROOM_TYPE["PRESIDENTIAL"], room_status=ROOM_STATUS["CHECKED-IN"], customer_id=1)
            room_3 = Room(room_id=expected_id_3,
                          room_type=ROOM_TYPE["DELUXE"], room_status=ROOM_STATUS["RESERVED"], customer_id=2)
            session.add(room_1)
            session.add(room_2)
            session.add(room_3)
            session.commit()
            session.close()

            Room().update_room_status(
                expected_id_1, ROOM_STATUS["RESERVED"], 9)
            Room().update_room_status(expected_id_2, ROOM_STATUS["AVAILABLE"])
            Room().update_room_status(
                expected_id_3, ROOM_STATUS["CHECKED-IN"], 2)

            res_1 = Room().get_room_by_id(expected_id_1)
            res_2 = Room().get_room_by_id(expected_id_2)
            res_3 = Room().get_room_by_id(expected_id_3)

            assert res_1.room_status == ROOM_STATUS["RESERVED"]
            assert res_1.customer_id == 9
            assert res_2.room_status == ROOM_STATUS["AVAILABLE"]
            assert res_2.customer_id == None
            assert res_3.room_status == ROOM_STATUS["CHECKED-IN"]
            assert res_3.customer_id == 2

    def test_get_checked_in_rooms(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            room_1 = Room(room_id="double1", room_type=ROOM_TYPE["DOUBLE"])
            room_2 = Room(room_id="presidential1",
                          room_type=ROOM_TYPE["PRESIDENTIAL"])
            room_3 = Room(room_id="single1", room_type=ROOM_TYPE["SINGLE"])
            room_4 = Room(room_id="single2", room_type=ROOM_TYPE["SINGLE"], room_status=ROOM_STATUS[
                          "RESERVED"], customer_id=1)
            room_5 = Room(room_id="deluxe1", room_type=ROOM_TYPE["DELUXE"], room_status=ROOM_STATUS[
                          "CHECKED-IN"], customer_id=2)
            session.add(room_1)
            session.add(room_2)
            session.add(room_3)
            session.add(room_4)
            session.add(room_5)
            session.commit()
            session.refresh(room_1)
            session.refresh(room_2)
            session.refresh(room_3)
            session.refresh(room_4)
            session.refresh(room_5)
            session.close()

            res = Room().get_checked_in_rooms()

            assert len(res) == 1
            assert room_5 in res

    def test_get_reserved_rooms(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            room_1 = Room(room_id="double1", room_type=ROOM_TYPE["DOUBLE"])
            room_2 = Room(room_id="presidential1",
                          room_type=ROOM_TYPE["PRESIDENTIAL"])
            room_3 = Room(room_id="single1", room_type=ROOM_TYPE["SINGLE"])
            room_4 = Room(room_id="single2", room_type=ROOM_TYPE["SINGLE"], room_status=ROOM_STATUS[
                          "RESERVED"], customer_id=1)
            room_5 = Room(room_id="deluxe1", room_type=ROOM_TYPE["DELUXE"], room_status=ROOM_STATUS[
                          "CHECKED-IN"], customer_id=2)
            session.add(room_1)
            session.add(room_2)
            session.add(room_3)
            session.add(room_4)
            session.add(room_5)
            session.commit()
            session.refresh(room_1)
            session.refresh(room_2)
            session.refresh(room_3)
            session.refresh(room_4)
            session.refresh(room_5)
            session.close()

            res = Room().get_reserved_rooms()

            assert len(res) == 1
            assert room_4 in res

    def test_get_reserved_room(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            room_1 = Room(room_id="double1", room_type=ROOM_TYPE["DOUBLE"])
            room_2 = Room(room_id="presidential1",
                          room_type=ROOM_TYPE["PRESIDENTIAL"])
            room_3 = Room(room_id="single1", room_type=ROOM_TYPE["SINGLE"])
            room_4 = Room(room_id="single2", room_type=ROOM_TYPE["SINGLE"], room_status=ROOM_STATUS[
                          "RESERVED"], customer_id=1)
            room_5 = Room(room_id="deluxe1", room_type=ROOM_TYPE["DELUXE"], room_status=ROOM_STATUS[
                          "CHECKED-IN"], customer_id=2)
            session.add(room_1)
            session.add(room_2)
            session.add(room_3)
            session.add(room_4)
            session.add(room_5)
            session.commit()
            session.refresh(room_1)
            session.refresh(room_2)
            session.refresh(room_3)
            session.refresh(room_4)
            session.refresh(room_5)
            session.close()

            res = Room().get_reserved_room(1)
            res2 = Room().get_reserved_room(2)

            assert res.customer_id == 1
            assert res.room_status == ROOM_STATUS["RESERVED"]
            assert res2 == None

    def test_get_available_rooms(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            room_1 = Room(room_id="double1", room_type=ROOM_TYPE["DOUBLE"])
            room_2 = Room(room_id="presidential1",
                          room_type=ROOM_TYPE["PRESIDENTIAL"])
            room_3 = Room(room_id="single1", room_type=ROOM_TYPE["SINGLE"])
            room_4 = Room(room_id="single2", room_type=ROOM_TYPE["SINGLE"], room_status=ROOM_STATUS[
                          "RESERVED"], customer_id=1)
            room_5 = Room(room_id="deluxe1", room_type=ROOM_TYPE["DELUXE"], room_status=ROOM_STATUS[
                          "CHECKED-IN"], customer_id=2)
            session.add(room_1)
            session.add(room_2)
            session.add(room_3)
            session.add(room_4)
            session.add(room_5)
            session.commit()
            session.refresh(room_1)
            session.refresh(room_2)
            session.refresh(room_3)
            session.refresh(room_4)
            session.refresh(room_5)
            session.close()

            res = Room().get_available_rooms()

            assert len(res) == 3
            assert room_1 in res
            assert room_2 in res
            assert room_3 in res

    def test_check_in_room(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            expected_room_id = "double1"
            expected_customer_id = 1
            expected_room_status = ROOM_STATUS["CHECKED-IN"]
            expected_check_in_time = "2022-10-08 01:01:01"
            room_1 = Room(room_id=expected_room_id,
                          room_type=ROOM_TYPE["DOUBLE"])
            session.add(room_1)
            session.commit()
            session.refresh(room_1)
            session.close()

            Room().check_in_room(expected_room_id, expected_customer_id, expected_check_in_time)
            res = Room().get_room_by_id(expected_room_id)

            assert res.room_id == expected_room_id
            assert res.customer_id == expected_customer_id
            assert res.room_status == expected_room_status
            assert res.status_time == expected_check_in_time

    def test_check_out_room(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            expected_room_id = "double1"
            expected_customer_id = 1
            expected_room_status = ROOM_STATUS["AVAILABLE"]
            room_1 = Room(room_id=expected_room_id,
                          room_type=ROOM_TYPE["DOUBLE"], room_status=ROOM_STATUS["CHECKED-IN"], customer_id=expected_customer_id, status_time="2022-10-08 01:01:01")
            session.add(room_1)
            session.commit()
            session.refresh(room_1)
            session.close()

            Room().check_out_room(expected_room_id)
            res = Room().get_room_by_id(expected_room_id)

            assert res.room_id == expected_room_id
            assert res.customer_id == None
            assert res.room_status == expected_room_status
            assert res.status_time == None

    def test_reserve_room(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            expected_room_id = "double1"
            expected_customer_id = 1
            expected_room_status = ROOM_STATUS["RESERVED"]
            expected_reservation_time = "2022-10-08 01:01:01"
            room_1 = Room(room_id=expected_room_id,
                          room_type=ROOM_TYPE["DOUBLE"], room_status=ROOM_STATUS["AVAILABLE"])
            session.add(room_1)
            session.commit()
            session.refresh(room_1)
            session.close()

            Room().reserve_room(expected_room_id, expected_customer_id, expected_reservation_time)
            res = Room().get_room_by_id(expected_room_id)

            assert res.room_id == expected_room_id
            assert res.customer_id == expected_customer_id
            assert res.room_status == expected_room_status
            assert res.status_time == expected_reservation_time

    def test_cancel_reservation(self):
        with patch("HotelBooking.Models.room.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            expected_room_id = "double1"
            expected_customer_id = 1
            expected_room_status = ROOM_STATUS["AVAILABLE"]
            room_1 = Room(room_id=expected_room_id,
                          room_type=ROOM_TYPE["DOUBLE"], room_status=ROOM_STATUS["RESERVED"], customer_id=expected_customer_id)
            session.add(room_1)
            session.commit()
            session.refresh(room_1)
            session.close()

            Room().cancel_reservation(expected_room_id)
            res = Room().get_room_by_id(expected_room_id)

            assert res.room_id == expected_room_id
            assert res.customer_id == None
            assert res.room_status == expected_room_status
            assert res.status_time == None
