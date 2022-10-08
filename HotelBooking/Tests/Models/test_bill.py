from unittest.mock import patch
from sqlmodel import create_engine, Session, SQLModel
from HotelBooking.Models.bill import BILL_STATUS, Bill


class TestBill:
    def test_get_bill(self):
        with patch("HotelBooking.Models.bill.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            expected_bill_amount = 99.99
            expected_customer_id = 99
            bill_1 = Bill(bill_amount=expected_bill_amount,
                          customer_id=expected_customer_id)
            session.add(bill_1)
            session.commit()
            session.close()

            res_1 = Bill().get_bill(1)
            res_2 = Bill().get_bill(2)

            assert res_1.bill_amount == expected_bill_amount
            assert res_1.customer_id == expected_customer_id
            assert res_2 == None

    def test_create_bill(self):
        with patch("HotelBooking.Models.bill.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            expected_bill_amount = 99.99
            expected_customer_id = 99
            expected_bill_id = 1
            expected_bill_status = BILL_STATUS["OUTSTANDING"]

            res = Bill().create_bill(expected_customer_id, expected_bill_amount)

            assert res.bill_amount == expected_bill_amount
            assert res.bill_id == expected_bill_id
            assert res.bill_status == expected_bill_status
            assert res.customer_id == expected_customer_id

    def test_pay_bill(self):
        with patch("HotelBooking.Models.bill.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            bill_1 = Bill(bill_amount=99,
                          customer_id=1)
            session.add(bill_1)
            session.commit()
            session.close()
            expected_bill_status = BILL_STATUS["PAID"]

            Bill().pay_bill(1)
            res = Bill().get_bill(1)

            assert res.bill_status == expected_bill_status
