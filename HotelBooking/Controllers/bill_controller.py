from HotelBooking.Controllers.controller import Controller
from HotelBooking.Models.bill import Bill
from typing import List


class BillController(Controller):
    """
    Bill controller class used for all actions associated with billing
    """
    bill: Bill

    def __init__(self) -> None:
        super().__init__()
        self.bill = Bill()

    def create_bill(self, customer_id: int, amount: float) -> Bill:
        """
        Creates a bill using a customer ID and bill amount
        """
        return self.bill.create_bill(customer_id, amount)

    def modify(self, bill_id: int, amount: float) -> int:
        """
        Modifies a bill amount with the given bill ID
        """
        return self.bill.modify_bill(bill_id, amount)

    def get_bill(self, bill_id: int) -> Bill:
        """
        Gets the bill with the given bill ID
        """
        return self.bill.get_bill(bill_id)

    def pay_bill(self, bill_id: int):
        """
        Pays the bill with the given bill ID
        """
        self.bill.pay_bill(bill_id)

    def cancel_bill(self, bill_id: int):
        """
        Cancels the bill with the given bill ID
        """
        self.bill.cancel_bill(bill_id)

    def get_available_bills(self, customer_id) -> List[Bill]:
        """
        Gets all available bills for the given customer id
        """
        return self.bill.get_available_bills(customer_id)

    def get_all_bills(self, customer_id) -> List[Bill]:
        """
        Gets all bills with the given customr id
        """
        return self.bill.get_all_bills(customer_id)
