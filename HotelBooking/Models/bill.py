from __future__ import annotations
from sqlmodel import Field, SQLModel, Session, select, update
from HotelBooking.Models.customer import Customer
from HotelBooking.Models.utils import get_engine
from typing import Optional

BILL_STATUS = {
    "OUTSTANDING": "OUTSTANDING",
    "PAID": "PAID",
    "CANCELED" : "CANCELED"
}


class Bill(SQLModel, table=True):
    bill_id: Optional[int] = Field(default=None, primary_key=True)
    bill_status: str = Field(default='OUTSTANDING')
    bill_amount: float
    customer_id: str = Field(foreign_key=Customer.customer_id)

    def get_bill(self, bill_id: int) -> Bill:
        engine = get_engine()
        session = Session(engine)
        statement = select(Bill).where(Bill.bill_id == bill_id)
        bill = session.exec(statement).first()
        session.close()
        return bill

    def create_bill(self, customer_id: str, amount: float) -> Bill:
        engine = get_engine()
        session = Session(engine)
        bill = Bill(bill_amount=amount,
                    customer_id=customer_id)

        session.add(bill)
        session.commit()
        session.refresh(bill)
        session.close()

        return bill

    def pay_bill(self, bill_id: int):
        bill = self.get_bill(bill_id)
        engine = get_engine()
        session = Session(engine)
        bill.bill_status = BILL_STATUS["PAID"]
        session.add(bill)
        session.commit()
        session.close()
        
    def cancel_bill(self, bill_id: int):
        bill = self.get_bill(bill_id)
        engine = get_engine()
        session = Session(engine)
        bill.bill_status = BILL_STATUS["CANCELED"]
        session.add(bill)
        session.commit()
        session.close()