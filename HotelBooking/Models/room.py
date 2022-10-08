from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
from Models.customer import Customer
from typing import Optional


class Room(SQLModel, table=True):
    room_id: Optional[str] = Field(primary_key=True)
    room_type: str
    room_status: str = Field(default="AVAILABLE")
    customer_id: Optional[int] = Field(foreign_key=Customer.customer_id)
