from sqlmodel import create_engine, Session, select

from Models.room import Room


def test_db_connection():
    # TODO: Remove this test block
    Room().get_available_rooms()


test_db_connection()
