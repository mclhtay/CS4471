from unittest.mock import patch
from sqlmodel import create_engine, Session, SQLModel
from HotelBooking.Models.customer import Customer


class TestCustomer:

    def test_create_customer(self):
        with patch("HotelBooking.Models.customer.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)

            customer_id="username1"
            customer_password="mypass"
            customer_name="Jane Doe"
            customer_address= "123 Western Rd"
            customer_cell_number=1234567890
            customer_credit_card_number = 134212
            
            user_1 = Customer().create_customer(customer_id, customer_password, customer_name, customer_address, customer_cell_number, customer_credit_card_number)

            assert user_1.customer_id == customer_id
            assert user_1.customer_password == customer_password
            assert user_1.customer_name == customer_name
            assert user_1.customer_address == customer_address
            assert user_1.customer_cell_number == customer_cell_number
            assert user_1.customer_credit_card_number == customer_credit_card_number

            






    def test_authenticate_customer(self):
        with patch("HotelBooking.Models.customer.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            user_1 = Customer(
                customer_id="user1", customer_password="mypass1", customer_name="jane doe", customer_address="123 elmo st", customer_cell_number=123456789, customer_credit_card_number=4352231)
            user_2 = Customer(
                customer_id="user2", customer_password="mypass2", customer_name="john doe", customer_address="123 elmo st", customer_cell_number=123456789, customer_credit_card_number=4352231)
            session.add(user_1)
            session.add(user_2)
            session.commit()
            session.close()
            expected_res_1 = True
            expected_res_2 = False

            res_1 = Customer().authenticate_customer("user1", "mypass1")
            res_2 = Customer().authenticate_customer("user2", "mypass1")

            assert res_1 == expected_res_1
            assert res_2 == expected_res_2
    
    def test_customer_exists(self):
        with patch("HotelBooking.Models.customer.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            user_1 = Customer(
                customer_id="user1", customer_password="mypass1", customer_name="jane doe", customer_address="123 elmo st", customer_cell_number=123456789, customer_credit_card_number=4352231)
            session.add(user_1)
            session.commit()
            session.close()
            expected_res_1 = True
            expected_res_2 = False

            res_1 = Customer().customer_exists("user1")
            res_2 = Customer().customer_exists("user2")

            assert res_1 == expected_res_1
            assert res_2 == expected_res_2