from sqlmodel import Field, SQLModel


class Customer(SQLModel, table=True):
    customerId: int = Field(primary_key=True)
