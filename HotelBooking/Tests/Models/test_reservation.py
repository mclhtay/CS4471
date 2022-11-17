from unittest.mock import patch
from sqlmodel import create_engine, Session, SQLModel
from HotelBooking.Models.reservation import Reservation


class TestReservation:
    def test_get_reservation_with_status(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)

            reservation_1 = Reservation(reservation_id="1", status="OPEN", customer_id="test",
                                        room_id="single1", bill_id="1", reservation_checkin_date="03/11/2000", reservation_stay_date=5, is_accessibility_requested=1)
            reservation_2 = Reservation(reservation_id="2", status="OPEN", customer_id="bob",
                                        room_id="single2", bill_id="2", reservation_checkin_date="03/11/2000", reservation_stay_date=6, is_accessibility_requested=1)
            reservation_3 = Reservation(reservation_id="3", status="IN_PROGRESS", customer_id="test",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/11/2000", reservation_stay_date=7, is_accessibility_requested=1)
            reservation_4 = Reservation(reservation_id="4", status="CLOSED", customer_id="test",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/11/2000", reservation_stay_date=8, is_accessibility_requested=1)
            reservation_5 = Reservation(reservation_id="5", status="CANCELED", customer_id="bob",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/11/2000", reservation_stay_date=9, is_accessibility_requested=1)

            session.add(reservation_1)
            session.add(reservation_2)
            session.add(reservation_3)
            session.add(reservation_4)
            session.add(reservation_5)
            session.commit()
            session.refresh(reservation_1)
            session.refresh(reservation_2)
            session.refresh(reservation_3)
            session.refresh(reservation_4)
            session.refresh(reservation_5)
            session.close()

            open_reservations = Reservation().get_reservations_with_status("OPEN")
            open_bob_reservations = Reservation().get_reservations_with_status("OPEN", "bob")
            in_progress_reservations = Reservation().get_reservations_with_status("IN_PROGRESS")
            closed_reservations = Reservation().get_reservations_with_status("CLOSED")
            canceled_reservations = Reservation().get_reservations_with_status("CANCELED")

            assert len(open_reservations) == 2
            assert len(open_bob_reservations) == 1
            assert len(in_progress_reservations) == 1
            assert len(closed_reservations) == 1
            assert len(canceled_reservations) == 1
            assert reservation_1 in open_reservations
            assert reservation_2 in open_bob_reservations
            assert reservation_2 in open_reservations
            assert reservation_3 in in_progress_reservations
            assert reservation_4 in closed_reservations
            assert reservation_5 in canceled_reservations

    def test_get_reservation_by_customer_id(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)

            reservation_1 = Reservation(reservation_id="1", status="OPEN", customer_id="test",
                                        room_id="single1", bill_id="1", reservation_checkin_date="03/11/2000", reservation_stay_date=5, is_accessibility_requested=1)
            reservation_2 = Reservation(reservation_id="2", status="OPEN", customer_id="bob",
                                        room_id="single2", bill_id="2", reservation_checkin_date="03/11/2000", reservation_stay_date=6, is_accessibility_requested=1)
            reservation_3 = Reservation(reservation_id="3", status="IN_PROGRESS", customer_id="test",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/11/2000", reservation_stay_date=7, is_accessibility_requested=1)
            reservation_4 = Reservation(reservation_id="4", status="CLOSED", customer_id="test",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/11/2000", reservation_stay_date=8, is_accessibility_requested=1)
            reservation_5 = Reservation(reservation_id="5", status="CANCELED", customer_id="bob",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/11/2000", reservation_stay_date=9, is_accessibility_requested=1)

            session.add(reservation_1)
            session.add(reservation_2)
            session.add(reservation_3)
            session.add(reservation_4)
            session.add(reservation_5)
            session.commit()
            session.refresh(reservation_1)
            session.refresh(reservation_2)
            session.refresh(reservation_3)
            session.refresh(reservation_4)
            session.refresh(reservation_5)
            session.close()

            bob_reservations = Reservation().get_reservations_by_customer_id("bob")
            test_reservations = Reservation().get_reservations_by_customer_id("test")

            assert len(bob_reservations) == 2
            assert len(test_reservations) == 3
            assert reservation_1 in test_reservations
            assert reservation_2 in bob_reservations
            assert reservation_3 in test_reservations
            assert reservation_4 in test_reservations
            assert reservation_5 in bob_reservations

    def test_get_reservation_by_id(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)

            reservation_1 = Reservation(reservation_id=1, status="OPEN", customer_id="test",
                                        room_id="single1", bill_id="1", reservation_checkin_date="03/11/2000", reservation_stay_date=5, is_accessibility_requested=1)

            session.add(reservation_1)
            session.commit()
            session.refresh(reservation_1)
            session.close()

            reservation = Reservation().get_reservation_by_id(1)

            assert reservation.reservation_id == 1
            assert reservation.status == "OPEN"
            assert reservation.customer_id == "test"
            assert reservation.room_id == "single1"
            assert reservation.bill_id == 1
            assert reservation.reservation_checkin_date == "03/11/2000"
            assert reservation.reservation_stay_date == 5
            assert reservation.is_accessibility_requested ==1

    def test_update_reservation_status(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            reservation_1 = Reservation(reservation_id="1", status="OPEN", customer_id="test",
                                        room_id="single1", bill_id="1", reservation_checkin_date="03/11/2000", reservation_stay_date=5, is_accessibility_requested=1)
            reservation_2 = Reservation(reservation_id="2", status="OPEN", customer_id="bob",
                                        room_id="single2", bill_id="2", reservation_checkin_date="03/11/2000", reservation_stay_date=6, is_accessibility_requested=1)
            reservation_3 = Reservation(reservation_id="3", status="IN_PROGRESS", customer_id="test",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/11/2000", reservation_stay_date=7, is_accessibility_requested=1)
            session.add(reservation_1)
            session.add(reservation_2)
            session.add(reservation_3)
            session.commit()
            session.close()

            Reservation().update_reservation_status(
                1, "IN_PROGRESS")
            Reservation().update_reservation_status(
                2, "CLOSED")
            Reservation().update_reservation_status(
                3, "CANCELED")

            res_1 = Reservation().get_reservation_by_id(1)
            res_2 = Reservation().get_reservation_by_id(2)
            res_3 = Reservation().get_reservation_by_id(3)
            assert res_1.status == "IN_PROGRESS"
            assert res_2.status == "CLOSED"
            assert res_3.status == "CANCELED"

    def test_update_reservation_start_date(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            reservation_1 = Reservation(reservation_id="1", status="OPEN", customer_id="test",
                                        room_id="single1", bill_id="1", reservation_checkin_date="03/11/2000", reservation_stay_date=5, is_accessibility_requested=1)
            reservation_2 = Reservation(reservation_id="2", status="OPEN", customer_id="bob",
                                        room_id="single2", bill_id="2", reservation_checkin_date="03/12/2000", reservation_stay_date=6, is_accessibility_requested=1)
            reservation_3 = Reservation(reservation_id="3", status="IN_PROGRESS", customer_id="test",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/13/2000", reservation_stay_date=7, is_accessibility_requested=1)
            session.add(reservation_1)
            session.add(reservation_2)
            session.add(reservation_3)
            session.commit()
            session.close()

            Reservation().update_reservation_start_date(
                1, "03/15/2000")
            Reservation().update_reservation_start_date(
                2, "03/16/2000")
            Reservation().update_reservation_start_date(
                3, "03/17/2000")

            res_1 = Reservation().get_reservation_by_id(1)
            res_2 = Reservation().get_reservation_by_id(2)
            res_3 = Reservation().get_reservation_by_id(3)
            assert res_1.reservation_checkin_date == "03/15/2000"
            assert res_2.reservation_checkin_date == "03/16/2000"
            assert res_3.reservation_checkin_date == "03/17/2000"

    def test_update_reservation_stay_date(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            reservation_1 = Reservation(reservation_id="1", status="OPEN", customer_id="test",
                                        room_id="single1", bill_id="1", reservation_checkin_date="03/11/2000", reservation_stay_date=5, is_accessibility_requested=1)
            reservation_2 = Reservation(reservation_id="2", status="OPEN", customer_id="bob",
                                        room_id="single2", bill_id="2", reservation_checkin_date="03/11/2000", reservation_stay_date=6, is_accessibility_requested=1)
            reservation_3 = Reservation(reservation_id="3", status="IN_PROGRESS", customer_id="test",
                                        room_id="single3", bill_id="3", reservation_checkin_date="03/11/2000", reservation_stay_date=7, is_accessibility_requested=1)
            session.add(reservation_1)
            session.add(reservation_2)
            session.add(reservation_3)
            session.commit()
            session.close()

            Reservation().update_reservation_duration(
                1, 2)
            Reservation().update_reservation_duration(
                2, 3)
            Reservation().update_reservation_duration(
                3, 4)

            res_1 = Reservation().get_reservation_by_id(1)
            res_2 = Reservation().get_reservation_by_id(2)
            res_3 = Reservation().get_reservation_by_id(3)
            assert res_1.reservation_stay_date == 2
            assert res_2.reservation_stay_date == 3
            assert res_3.reservation_stay_date == 4

    def test_update_reservation_bill(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            reservation_1 = Reservation(reservation_id="1", status="OPEN", customer_id="test",
                                        room_id="single1", bill_id=1, reservation_checkin_date="03/11/2000", reservation_stay_date=5, is_accessibility_requested=1)
            reservation_2 = Reservation(reservation_id="2", status="OPEN", customer_id="bob",
                                        room_id="single2", bill_id=2, reservation_checkin_date="03/11/2000", reservation_stay_date=6, is_accessibility_requested=1)
            reservation_3 = Reservation(reservation_id="3", status="IN_PROGRESS", customer_id="test",
                                        room_id="single3", bill_id=3, reservation_checkin_date="03/11/2000", reservation_stay_date=7, is_accessibility_requested=1)
            session.add(reservation_1)
            session.add(reservation_2)
            session.add(reservation_3)
            session.commit()
            session.close()

            Reservation().update_Bill(
                1, 5)
            Reservation().update_Bill(
                2, 6)
            Reservation().update_Bill(
                3, 7)

            res_1 = Reservation().get_reservation_by_id(1)
            res_2 = Reservation().get_reservation_by_id(2)
            res_3 = Reservation().get_reservation_by_id(3)

            assert res_1.bill_id == 5
            assert res_2.bill_id == 6
            assert res_3.bill_id == 7

    def test_create_reservation(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            expect_status = "OPEN"
            expect_customer_id = "test"
            expect_room_id = "single1"
            expect_bill_id = 1
            expect_reservation_checkin_date = "2000/11/03"
            expect_reservation_stay_date = 5
            expect_is_accessibility_requested = 1
            reservation_1 = Reservation().create_reservation(expect_status, expect_customer_id, expect_room_id,
                                                             expect_bill_id, expect_reservation_checkin_date, expect_reservation_stay_date, expect_is_accessibility_requested)

            assert reservation_1.status == expect_status
            assert reservation_1.customer_id == expect_customer_id
            assert reservation_1.room_id == expect_room_id
            assert reservation_1.bill_id == expect_bill_id
            assert reservation_1.reservation_checkin_date == expect_reservation_checkin_date
            assert reservation_1.reservation_stay_date == expect_reservation_stay_date
            assert reservation_1.is_accessibility_requested == expect_is_accessibility_requested

    def test_close_reservation_with_room_id(self):
        with patch("HotelBooking.Models.reservation.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            reservation_1 = Reservation(reservation_id="1", status="IN_PROGRESS", customer_id="test",
                                        room_id="single1", bill_id=1, reservation_checkin_date="03/11/2000", reservation_stay_date=5, is_accessibility_requested=1)
            session.add(reservation_1)
            session.commit()
            session.close()

            Reservation().close_reservation_with_room_id(
                "single1")

            res_1 = Reservation().get_reservation_by_id(1)

            assert res_1.status == "CLOSED"
