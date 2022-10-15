from sqlmodel import Field, SQLModel, Session, select
from typing import Optional
from HotelBooking.Models.utils import get_engine


class Customer(SQLModel, table=True):
    customer_id: str = Field(primary_key=True)
    customer_password: str

    def authenticate_customer(self, id: str, password: str) -> bool:
        engine = get_engine()
        with Session(engine) as session:
            statement = select(Customer).where(
                Customer.customer_id == id).where(Customer.customer_password == password)
            customer = session.exec(statement).first()
            return customer != None
