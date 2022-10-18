from HotelBooking.Controllers.controller import Controller
from HotelBooking.Models.bill import Bill
from typing import List


class BillController(Controller):
    bill: Bill

    def __init__(self) -> None:
        super().__init__()
        self.bill = Bill()

    def create_bill(self, customer_id: int, amount: float) -> Bill:
        return self.bill.create_bill(customer_id, amount)

    def modify(self, bill_id: int, amount: float) -> int:
        return self.bill.modify_bill(bill_id, amount)

    def get_bill(self, bill_id: int) -> Bill:
        return self.bill.get_bill(bill_id)

    def pay_bill(self, bill_id: int):
        self.bill.pay_bill(bill_id)

    def cancel_bill(self, bill_id: int):
        self.bill.cancel_bill(bill_id)

    def get_available_bills(self, customer_id) -> List[Bill]:
        return self.bill.get_available_bills(customer_id)

    def get_all_bills(self, customer_id) -> List[Bill]:
        return self.bill.get_all_bills(customer_id)
