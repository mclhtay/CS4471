from HotelBooking.Controllers.controller import Controller
from HotelBooking.Models.administrator import Administrator
from HotelBooking.Models.customer import Customer


class AuthenticationController(Controller):
    """
    Authentication controller class used for login of customers and admin, and registration of customers
    """
    administrator: Administrator
    customer: Customer

    def __init__(self):
        super().__init__()
        self.administrator = Administrator()
        self.customer = Customer()

    def authenticate_admin(self, id: str, password: str) -> bool:
        """
        Authenticates an admin using an id and password
        """
        return self.administrator.authenticate_admin(id, password)

    def authenticate_customer(self, id: str, password: str) -> bool:
        """
        Authenticates a customer using an id and password
        """
        return self.customer.authenticate_customer(id, password)

    def customer_exists(self, id: str) -> bool:
        """
        Verifies if a customer with a given ID exists
        """
        return self.customer.customer_exists(id)

    def create_customer(self, customer_id: str, customer_password: str, customer_name: str,
    customer_address: str, customer_cell_number: int, customer_credit_card_number: int):
        """
        Creates a new customer with given ID, password, and personal information
        """
        return self.customer.create_customer(customer_id, customer_password, customer_name, customer_address, customer_cell_number, customer_credit_card_number)
