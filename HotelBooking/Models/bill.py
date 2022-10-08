from sqlmodel import Field, SQLModel
from Models.customer import Customer


class Bill(SQLModel, table=True):
    billId: str = Field(primary_key=True)
    billStatus: str = Field(default='OUTSTANDING')
    billAmount: float
    customerId: int = Field(foreign_key=Customer.customerId)
