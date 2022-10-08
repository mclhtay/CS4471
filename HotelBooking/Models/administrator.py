from sqlmodel import Field, SQLModel


class Administrator(SQLModel, table=True):
    administratorId: str = Field(primary_key=True)
    administratorPassword: str
