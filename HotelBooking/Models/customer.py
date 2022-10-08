from sqlmodel import Field, SQLModel
from typing import Optional


class Customer(SQLModel, table=True):
    customer_id: Optional[int] = Field(default=None, primary_key=True)
