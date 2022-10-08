from sqlmodel import create_engine


DATABASE_ADDRESS = "sqlite:///HotelBooking/Database/Hotel.db"


def get_engine():
    return create_engine(DATABASE_ADDRESS)
