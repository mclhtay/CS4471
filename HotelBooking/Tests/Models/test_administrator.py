from unittest.mock import patch
from sqlmodel import create_engine, Session, SQLModel
from HotelBooking.Models.administrator import Administrator


class TestAdministrator:

    def test_authenticate_admin(self):
        with patch("HotelBooking.Models.administrator.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            admin_1 = Administrator(
                administrator_id="test1", administrator_password="test1")
            admin_2 = Administrator(
                administrator_id="test2", administrator_password="test2")
            session.add(admin_1)
            session.add(admin_2)
            session.commit()
            session.close()
            expected_res_1 = True
            expected_res_2 = False

            res_1 = Administrator().authenticate_admin("test1", "test1")
            res_2 = Administrator().authenticate_admin("test2", "test1")

            assert res_1 == expected_res_1
            assert res_2 == expected_res_2
