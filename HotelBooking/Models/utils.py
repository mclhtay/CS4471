import sys
import os
from sqlmodel import create_engine


def get_database_address():
    """
    Database addresses are different depending on whether the project
    is being executed as a script file or as a frozen system executable.
    """
    if getattr(sys, 'frozen', False):
        # is frozen as executable
        db_address = os.path.join(
            os.path.dirname(sys.executable), 'DB/Hotel.db')
    else:
        db_address = "HotelBooking/Database/Hotel.db"
    return db_address


def get_engine():
    """get the database engine"""
    db_address = get_database_address()
    return create_engine(f"sqlite:///{db_address}")
