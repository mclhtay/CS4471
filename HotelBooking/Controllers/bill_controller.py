from HotelBooking.Controllers.controller import Controller
from HotelBooking.Models.bill import Bill


class BillController(Controller):
    bill: Bill

    def __init__(self) -> None:
        super().__init__()
        self.bill = Bill()

    def create_bill(self, customer_id: int, amount: float) -> Bill:
        return self.bill.create_bill(customer_id, amount)

    def modify(self, bill_id: int, amount: float) -> Bill:
        return self.bill.modifyBill(bill_id, amount)

    def pay_bill(self, bill_id: int):
        self.bill.pay_bill(bill_id)

    def cancel_bill(self, bill_id: int):
        self.bill.cancel_bill(bill_id)