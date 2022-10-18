from unittest.mock import patch
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Models.bill import Bill


class TestBillController:
    @patch.object(Bill, "create_bill")
    def test_create_bill(self, mock_create_bill):
        mock_id = 1
        mock_amount = 1.0

        controller = BillController()
        controller.create_bill(mock_id, mock_amount)

        mock_create_bill.assert_called_once_with(mock_id, mock_amount)

    @patch.object(Bill, "pay_bill")
    def test_pay_bill(self, mock_pay_bill):
        mock_id = 1

        controller = BillController()
        controller.pay_bill(mock_id)

        mock_pay_bill.assert_called_once_with(mock_id)

    @patch.object(Bill, "modify_bill")
    def test_modify(self, mock_modify_bill):
        mock_id = 1
        mock_amount = 100
        controller = BillController()
        controller.modify(mock_id, mock_amount)

        mock_modify_bill.assert_called_once_with(mock_id, mock_amount)

    @patch.object(Bill, "get_bill")
    def test_get_bill(self, mock_get_bill):
        mock_id = 1
        controller = BillController()
        controller.get_bill(mock_id)

        mock_get_bill.assert_called_once_with(mock_id)

    @patch.object(Bill, "cancel_bill")
    def test_cancel_bill(self, mock_cancel_bill):
        mock_id = 1
        controller = BillController()
        controller.cancel_bill(mock_id)

        mock_cancel_bill.assert_called_once_with(mock_id)

    @patch.object(Bill, "get_available_bills")
    def test_get_available_bills(self, mock_get_available_bills):
        mock_id = 1
        controller = BillController()
        controller.get_available_bills(mock_id)

        mock_get_available_bills.assert_called_once_with(mock_id)

    @patch.object(Bill, "get_all_bills")
    def test_get_all_bills(self, mock_get_all_bills):
        mock_id = 1
        controller = BillController()
        controller.get_all_bills(mock_id)

        mock_get_all_bills.assert_called_once_with(mock_id)
