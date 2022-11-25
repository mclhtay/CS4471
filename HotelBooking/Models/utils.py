import sys
import os
from sqlmodel import create_engine


def get_database_address():
    if getattr(sys, 'frozen', False):
        db_address = os.path.join(
            os.path.dirname(sys.executable), 'DB/Hotel.db')
    else:
        db_address = "HotelBooking/Database/Hotel.db"
    return db_address


def get_engine():
    db_address = get_database_address()
    return create_engine(f"sqlite:///{db_address}")
