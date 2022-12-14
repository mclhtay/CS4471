from __future__ import annotations
from typing import Optional, List
from sqlmodel import Field, SQLModel, Session, select
from HotelBooking.Models.bill import Bill
from HotelBooking.Models.room import Room
from HotelBooking.Models.utils import get_engine
from HotelBooking.Models.customer import Customer
from typing import Optional

RESERVATION_STATUS = {
    "IN_PROGRESS": "IN_PROGRESS",
    "CLOSED": "CLOSED",
    "OPEN": "OPEN",
    "CANCELED": "CANCELED"
}


class Reservation(SQLModel, table=True):

    # unique id of the reservation
    reservation_id: int = Field(default=None, primary_key=True)
    # status of the reservation
    status: str

    # customer id who is booking the reservation
    customer_id: Optional[str] = Field(foreign_key=Customer.customer_id)

    # room id of the reservation
    room_id: Optional[str] = Field(foreign_key=Room.room_id)

    # bill id which is related with the reservation
    bill_id: Optional[int] = Field(foreign_key=Bill.bill_id)

    # check-in date of the reservation
    reservation_checkin_date: str

    # length of the reservation
    reservation_stay_date: int

    # is accessibility requested, 1 represent true and 0 represent false
    is_accessibility_requested: int

    def get_reservations_with_status(self, status, user_id=None) -> List[Reservation]:
        """get the all reservation of a user with a given status"""
        engine = get_engine()
        session = Session(engine)
        statement = select(Reservation).where(
            Reservation.status == status)
        if user_id != None:
            statement = statement.where(Reservation.customer_id == user_id)

        reservations = session.exec(statement).all()
        session.close()
        return reservations

    def get_reservations_by_customer_id(self, user_id) -> List[Reservation]:
        """get the all reservation of a user"""
        engine = get_engine()
        session = Session(engine)
        statement = select(Reservation).where(
            Reservation.customer_id == user_id)

        reservations = session.exec(statement).all()
        session.close()
        return reservations

    def get_reservation_by_id(self, reservation_id) -> Reservation:
        """get the reservation object with a reservation id"""
        engine = get_engine()
        session = Session(engine)
        statement = select(Reservation).where(
            Reservation.reservation_id == reservation_id)

        reservation = session.exec(statement).first()
        session.close()
        return reservation

    def update_reservation_status(self, reservation_id, status):
        """change the status of a reservation"""
        reservation = self.get_reservation_by_id(reservation_id)
        reservation.status = status
        engine = get_engine()
        session = Session(engine)
        session.add(reservation)
        session.commit()
        session.close()

    def update_reservation_start_date(self, reservation_id, newStartDate):
        """update the start date of a given reservation"""
        reservation = self.get_reservation_by_id(reservation_id)
        reservation.reservation_checkin_date = newStartDate
        engine = get_engine()
        session = Session(engine)
        session.add(reservation)
        session.commit()
        session.close()

    def update_reservation_duration(self, reservation_id, newDuration):
        """update the duration of a given reservation"""
        reservation = self.get_reservation_by_id(reservation_id)
        reservation.reservation_stay_date = newDuration
        engine = get_engine()
        session = Session(engine)
        session.add(reservation)
        session.commit()
        session.close()

    def update_Bill(self, reservation_id, bill_id):
        """update the bill id of a given reservation"""
        reservation = self.get_reservation_by_id(reservation_id)
        if (reservation.bill_id != bill_id):
            reservation.bill_id = bill_id
        engine = get_engine()
        session = Session(engine)
        session.add(reservation)
        session.commit()
        session.close()

    def create_reservation(self, status, customer_id, room_id, bill_id, reservation_checkin_date, reservation_stay_date, is_accessibility_requested) -> Reservation:
        """create new reservation"""
        engine = get_engine()
        session = Session(engine)
        reservation = Reservation(
            status=status,
            customer_id=customer_id,
            room_id=room_id,
            bill_id=bill_id,
            reservation_checkin_date=reservation_checkin_date,
            reservation_stay_date=reservation_stay_date,
            is_accessibility_requested=is_accessibility_requested
        )
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        session.close()

        return reservation

    def close_reservation_with_room_id(self, room_id):
        """close reservation with a provided room id"""
        engine = get_engine()
        session = Session(engine)
        statement = select(Reservation).where(
            Reservation.room_id == room_id).where(Reservation.status == RESERVATION_STATUS["IN_PROGRESS"])

        reservations = session.exec(statement)
        reservation = reservations.first()
        session.close()
        reservation.status = RESERVATION_STATUS["CLOSED"]
        engine = get_engine()
        session = Session(engine)
        session.add(reservation)
        session.commit()
        session.close()
