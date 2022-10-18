from __future__ import annotations
from sqlmodel import Field, SQLModel, Session, select, update
from HotelBooking.Models.customer import Customer
from HotelBooking.Models.utils import get_engine
from typing import List, Optional

BILL_STATUS = {
    "OUTSTANDING": "OUTSTANDING",
    "PAID": "PAID",
    "CANCELED": "CANCELED",
    "REFUNDED": "REFUNDED"
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

    def get_available_bills(self, user_id) -> List[Bill]:
        engine = get_engine()
        session = Session(engine)
        statement = select(Bill).where(
            Bill.bill_status == BILL_STATUS["OUTSTANDING"]).where(Bill.customer_id == user_id)
        bill = session.exec(statement).all()
        session.close()
        return bill

    def get_all_bills(self, user_id) -> List[Bill]:
        engine = get_engine()
        session = Session(engine)
        statement = select(Bill).where(Bill.customer_id == user_id)
        bill = session.exec(statement).all()
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

    def refund_bill(self, bill_id: int):
        bill = self.get_bill(bill_id)
        engine = get_engine()
        session = Session(engine)
        bill.bill_status = BILL_STATUS["REFUNDED"]
        session.add(bill)
        session.commit()
        session.close()

    def modify_bill(self, bill_id: int, bill_amount: float):
        bill = self.get_bill(bill_id)
        if (bill.bill_status == BILL_STATUS["PAID"]):
            self.refund_bill(bill.bill_id)
            return self.create_bill(bill.customer_id, bill_amount).bill_id
        bill.bill_amount = bill_amount
        engine = get_engine()
        session = Session(engine)
        session.add(bill)
        session.commit()
        self.bill_id = bill.bill_id
        session.close()
        return self.bill_id
