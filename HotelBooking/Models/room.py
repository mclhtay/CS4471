from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
from Models.customer import Customer


class Room(SQLModel, table=True):
    roomId: str = Field(primary_key=True)
    roomType: str
    roomStatus: str = Field(default="AVAILABLE")
    customerId: Optional[int] = Field(foreign_key=Customer.customerId)

    def get_available_rooms(self):
        # TODO: Remove this test block
        engine = create_engine("sqlite:///Database/Hotel.db")
        with Session(engine) as session:
            roomStatement = select(Room).where(Room.customerId != None)
            rooms = session.exec(roomStatement).all()
            print(rooms)
