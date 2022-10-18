from unittest.mock import patch
from sqlmodel import create_engine, Session, SQLModel
from HotelBooking.Models.customer import Customer


class TestCustomer:

    def test_authenticate_customer(self):
        with patch("HotelBooking.Models.customer.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            user_1 = Customer(
                customer_id="test1", customer_password="test1")
            user_2 = Customer(
                customer_id="test2", customer_password="test2")
            session.add(user_1)
            session.add(user_2)
            session.commit()
            session.close()
            expected_res_1 = True
            expected_res_2 = False

            res_1 = Customer().authenticate_customer("test1", "test1")
            res_2 = Customer().authenticate_customer("test2", "test1")

            assert res_1 == expected_res_1
            assert res_2 == expected_res_2
