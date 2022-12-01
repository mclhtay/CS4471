from sqlmodel import Field, SQLModel, Session, select
from typing import Optional
from HotelBooking.Models.utils import get_engine


class Customer(SQLModel, table=True):

    # unique id of the customer
    customer_id: str = Field(primary_key=True)

    # customer password
    customer_password: str
    # name of the customer
    customer_name: str
    # address of the customer
    customer_address: str
    # cellphone number of the customer
    customer_cell_number: int
    # credit card number of the customer
    customer_credit_card_number: int

    def create_customer(self, customer_id, customer_password, customer_name, customer_address, customer_cell_number, customer_credit_card_number):
        """create a new customer object with the provided information and insert it to the database"""
        engine = get_engine()
        session = Session(engine)
        customer = Customer(
            customer_id=customer_id,
            customer_password=customer_password,
            customer_name=customer_name,
            customer_address=customer_address,
            customer_cell_number=customer_cell_number,
            customer_credit_card_number=customer_credit_card_number
        )
        session.add(customer)
        session.commit()
        session.refresh(customer)
        session.close()

        return customer

    def authenticate_customer(self, id: str, password: str) -> bool:
        """check if the provided id and password are in the database"""
        engine = get_engine()
        with Session(engine) as session:
            statement = select(Customer).where(
                Customer.customer_id == id).where(Customer.customer_password == password)
            customer = session.exec(statement).first()
            return customer != None

    def customer_exists(self, id: str) -> bool:
        """check if the provided customer exist in the database"""
        engine = get_engine()
        with Session(engine) as session:
            statement = select(Customer).where(Customer.customer_id == id)
            customer = session.exec(statement).first()
            return customer != None
