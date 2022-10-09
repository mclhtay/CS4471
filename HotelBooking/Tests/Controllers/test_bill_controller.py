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
