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
            expected_customer_id = "99"
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

    def test_get_available_bills(self):
        with patch("HotelBooking.Models.bill.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            bill_1 = Bill(customer_id="test", bill_amount=100)
            bill_2 = Bill(customer_id="test", bill_amount=1000)
            bill_3 = Bill(customer_id="bob", bill_amount=1020)
            bill_4 = Bill(customer_id="test", bill_amount=1040)
            bill_closed = Bill(customer_id="test", bill_amount=1040,
                               bill_status="CLOSED")
            bill_cancel = Bill(customer_id="bob", bill_amount=1040,
                               bill_status="CANCELED")
            bill_5 = Bill(customer_id="test", bill_amount=2090)
            session.add(bill_1)
            session.add(bill_2)
            session.add(bill_3)
            session.add(bill_4)
            session.add(bill_closed)
            session.add(bill_cancel)
            session.add(bill_5)
            session.commit()
            session.refresh(bill_1)
            session.refresh(bill_2)
            session.refresh(bill_3)
            session.refresh(bill_closed)
            session.refresh(bill_cancel)
            session.refresh(bill_4)
            session.refresh(bill_5)
            session.close()

            test_bills = Bill().get_available_bills("test")
            bob_bills = Bill().get_available_bills("bob")
            assert len(test_bills) == 4
            assert len(bob_bills) == 1
            assert bill_1 in test_bills
            assert bill_2 in test_bills
            assert bill_3 in bob_bills
            assert bill_4 in test_bills
            assert bill_5 in test_bills

    def test_get_all_bills(self):
        with patch("HotelBooking.Models.bill.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            bill_1 = Bill(customer_id="test", bill_amount=100)
            bill_2 = Bill(customer_id="test", bill_amount=1000)
            bill_3 = Bill(customer_id="bob", bill_amount=1020)
            bill_4 = Bill(customer_id="test", bill_amount=1040)
            bill_closed = Bill(customer_id="test", bill_amount=1040,
                               bill_status="CLOSED")
            bill_cancel = Bill(customer_id="bob", bill_amount=1040,
                               bill_status="CANCELED")
            bill_5 = Bill(customer_id="test", bill_amount=2090)
            session.add(bill_1)
            session.add(bill_2)
            session.add(bill_3)
            session.add(bill_4)
            session.add(bill_closed)
            session.add(bill_cancel)
            session.add(bill_5)
            session.commit()
            session.refresh(bill_1)
            session.refresh(bill_2)
            session.refresh(bill_3)
            session.refresh(bill_closed)
            session.refresh(bill_cancel)
            session.refresh(bill_4)
            session.refresh(bill_5)
            session.close()

            test_bills = Bill().get_available_bills("test")
            bob_bills = Bill().get_available_bills("bob")
            assert len(test_bills) == 4
            assert len(bob_bills) == 1
            assert bill_1 in test_bills
            assert bill_2 in test_bills
            assert bill_3 in bob_bills
            assert bill_4 in test_bills
            assert bill_5 in test_bills

    def test_create_bill(self):
        with patch("HotelBooking.Models.bill.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            SQLModel.metadata.create_all(engine)
            expected_bill_amount = 99.99
            expected_customer_id = "99"
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

    def test_cancel_bill(self):
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
            expected_bill_status = BILL_STATUS["CANCELED"]

            Bill().cancel_bill(1)
            res = Bill().get_bill(1)

            assert res.bill_status == expected_bill_status

    def test_refund_bill(self):
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
            expected_bill_status = BILL_STATUS["REFUNDED"]

            Bill().refund_bill(1)
            res = Bill().get_bill(1)

            assert res.bill_status == expected_bill_status

    def test_modify_bill(self):
        with patch("HotelBooking.Models.bill.get_engine") as mock_get_engine:
            mock_get_engine.return_value = create_engine("sqlite:///:memory:")
            engine = mock_get_engine()
            new_bill = 100
            SQLModel.metadata.create_all(engine)
            session = Session(engine)
            bill_1 = Bill(bill_amount=99,
                          customer_id=1)
            session.add(bill_1)
            session.commit()
            session.close()

            Bill().modify_bill(1, new_bill)
            res = Bill().get_bill(1)

            assert res.bill_amount == new_bill
