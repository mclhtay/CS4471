from __future__ import annotations
from typing import Optional, List
from sqlmodel import Field, SQLModel, Session, select
from HotelBooking.Models.bill import Bill
from HotelBooking.Models.room import Room
from HotelBooking.Models.utils import get_engine
from HotelBooking.Models.customer import Customer
from typing import Optional




class Reservation(SQLModel, table=True):
    reservation_id: int = Field(default=None, primary_key=True)
    status:str
    customer_id: Optional[str] = Field(foreign_key=Customer.customer_id)
    room_id: Optional[str] = Field(foreign_key=Room.room_id)
    bill_id: Optional[int] = Field(foreign_key=Bill.bill_id)
    reservation_checkin_date: str
    reservation_stay_date: int

    def get_reservation_with_status(self, status, userID=None) -> List[Reservation]:
        engine = get_engine()
        session = Session(engine)
        statement = select(Reservation).where(
            Reservation.status == status)
        if userID!=None:
            statement=statement.where(Reservation.customer_id==userID)

        reservations = session.exec(statement).all()
        session.close()
        return reservations

    def get_reservation_by_customer_id(self, userID) -> List[Reservation]:
        engine = get_engine()
        session = Session(engine)
        statement = select(Reservation).where(Reservation.customer_id==userID)

        reservations = session.exec(statement).all()
        session.close()
        return reservations

    def get_reservation_by_id(self, reservation_id) -> Reservation:
        engine = get_engine()
        session = Session(engine)
        statement = select(Reservation).where(Reservation.reservation_id==reservation_id)

        reservation = session.exec(statement).first()
        session.close()
        return reservation

    def update_reservation_status(self, reservation_id, status):
        reservation = self.get_reservation_by_id(reservation_id)
        reservation.status = status
        engine = get_engine()
        session = Session(engine)
        session.add(reservation)
        session.commit()
        session.close()


    def create_reservation(self, status, customer_id, room_id, bill_id, reservation_checkin_date, reservation_stay_date) -> Reservation:
        engine = get_engine()
        session = Session(engine)
        reservation = Reservation(
                    status=status, 
                    customer_id=customer_id,
                    room_id=room_id,
                    bill_id=bill_id,
                    reservation_checkin_date=reservation_checkin_date,
                    reservation_stay_date=reservation_stay_date
                    )
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        session.close()

        return reservation