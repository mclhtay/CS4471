from sqlmodel import Field, SQLModel, Session, select
from HotelBooking.Models.utils import get_engine


class Administrator(SQLModel, table=True):

    administrator_id: str = Field(primary_key=True)
    administrator_password: str

    def authenticate_admin(self, id: str, password: str) -> bool:
        """check if the given id and password are in the database"""

        engine = get_engine()
        with Session(engine) as session:
            statement = select(Administrator).where(
                Administrator.administrator_id == id).where(Administrator.administrator_password == password)
            admin = session.exec(statement).first()
            return admin != None
