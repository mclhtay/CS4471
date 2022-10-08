from sqlmodel import Field, SQLModel, create_engine, Session, select
from Models.utils import get_engine
from typing import Optional


class Administrator(SQLModel, table=True):
    administrator_id: str = Field(primary_key=True)
    administrator_password: str

    def authenticate_admin(id: str, password: str) -> bool:
        engine = get_engine()
        with Session(engine) as session:
            statement = select(Administrator).where(
                Administrator.administrator_id == id).where(Administrator.administrator_password == password)
            admin = session.exec(statement).first()
            return admin != None
