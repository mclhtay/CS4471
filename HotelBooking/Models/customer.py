from sqlmodel import Field, SQLModel, Session, select
from typing import Optional
from HotelBooking.Models.utils import get_engine


class Customer(SQLModel, table=True):
    customer_id: str = Field(primary_key=True)
    customer_password: str
    customer_name: str
    customer_address: str
    customer_cellnumber: int
    customer_creditcardnumber: int

    def create_customer(self, customer_id, customer_password, customer_name, customer_address, customer_cellnumber, customer_creditcardnumber):
        engine = get_engine()
        session = Session(engine)
        customer = Customer(
            customer_id=customer_id,
            customer_password=customer_password,
            customer_name=customer_name,
            customer_address=customer_address,
            customer_cellnumber=customer_cellnumber,
            customer_creditcardnumber=customer_creditcardnumber
        )
        session.add(customer)
        session.commit()
        session.refresh(customer)
        session.close()

        return customer

    def authenticate_customer(self, id: str, password: str) -> bool:
        engine = get_engine()
        with Session(engine) as session:
            statement = select(Customer).where(
                Customer.customer_id == id).where(Customer.customer_password == password)
            customer = session.exec(statement).first()
            return customer != None
