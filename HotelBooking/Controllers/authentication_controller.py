from HotelBooking.Controllers.controller import Controller
from HotelBooking.Models.administrator import Administrator
from HotelBooking.Models.customer import Customer


class AuthenticationController(Controller):
    administrator: Administrator
    customer: Customer

    def __init__(self):
        super().__init__()
        self.administrator = Administrator()
        self.customer = Customer()

    def authenticate_admin(self, id: str, password: str) -> bool:
        return self.administrator.authenticate_admin(id, password)

    def authenticate_customer(self, id: str, password: str) -> bool:
        return self.customer.authenticate_customer(id, password)

    def customer_exists(self, id: str) -> bool:
        return self.customer.customer_exists(id)

    def create_customer(self, customer_id: str, customer_password: str, customer_name: str,
    customer_address: str, customer_cell_number: int, customer_credit_card_number: int):
        return self.customer.create_customer(customer_id, customer_password, customer_name, customer_address, customer_cell_number, customer_credit_card_number)
