from sqlmodel import create_engine, Session, select

from Models.room import Room
from Models.bill import Bill


def test_db_connection():
    # TODO: Remove this test block

    Bill().pay_bill(6)


test_db_connection()
