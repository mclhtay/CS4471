from unittest.mock import patch
from sqlmodel import create_engine, Session, SQLModel
from HotelBooking.Models.room_type import RoomType


class TestBill:
    def test_get_price(self):
        with patch("HotelBooking.Models.room_type.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            expected_room_type_amount = 99.99
            room_type_1 = RoomType(room_type="testType", room_price=99.99)
            session.add(room_type_1)
            session.commit()
            session.close()

            res_1 = RoomType().get_price("testType")

            assert res_1 == expected_room_type_amount
