from HotelBooking.Controllers.authentication_controller import AuthenticationController
from HotelBooking.Views.utils import big_print
from HotelBooking.Views.view import View
from PyInquirer import prompt

PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "USERNAME": 'username',
    "PASSWORD": "password",
    "FULLNAME": "full_name",
    "ADDRESS": "address",
    "CELLNUMBER": "cell_number",
    "CREDITCARD": "credit_card_number",
}

PROMPTS = {
    'operations': [{
        'type': 'list',
        'message': "Create new account",
        'name': 'operations',
        'choices': [
        ]
    }],
    'username': [{
        'type': 'input',
        'message': "Enter a username",
        'name': 'username',
    }],
    "password": [{
        'type': 'password',
        'message': "Enter a password",
        'name': 'password',
    }],
    "full_name": [{
        'type': 'input',
        'message': "Enter your full name",
        'name': 'full_name',
    }],
    "address": [{
        'type': 'input',
        'message': "Enter your address",
        'name': 'address',
    }],
    "cell_number": [{
        'type': 'input',
        'message': "Enter your cell number",
        'name': 'cell_number',
        'validate': lambda x: x.isdigit() or "Please erase value and enter a only numbers!"
    }],
    "credit_card_number": [{
        'type': 'input',
        'message': "Enter your credit card number",
        'name': 'credit_card_number',
        'validate': lambda x: x.isdigit() or "Please erase value and enter only numbers!"
    }],
}


class RegistrationView(View):
    """
    This view presents registration menu to the customer when they select they want to register.
    """
    authentication_controller: AuthenticationController
    customer_id: str
    customer_password: str
    customer_name: str
    customer_address: str
    customer_cell_number: int
    customer_credit_card_number: int

    def __init__(self, history=[], caller=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.authentication_controller = AuthenticationController()

    def show(self):
        """
        Shows prompts for user input, then immediately return to authentication to
        allow for more dynamic user flow
        """
        big_print("Registration PORTAL")
        self.create_customer()
        self.prev_view()

    def create_customer(self):
        """
        This operation prompts for all user information required to register.
        """
        customer_id = self.prompt_and_get_answer(PROMPT_KEY['USERNAME'])
        is_duplicate_username = self.authentication_controller.customer_exists(
            customer_id)
        while is_duplicate_username:
            print("Username taken, please enter a different username: ")
            customer_id = self.prompt_and_get_answer(PROMPT_KEY['USERNAME'])
            is_duplicate_username = self.authentication_controller.customer_exists(
                customer_id)
        customer_password = self.prompt_and_get_answer(PROMPT_KEY['PASSWORD'])
        customer_name = self.prompt_and_get_answer(PROMPT_KEY['FULLNAME'])
        customer_address = self.prompt_and_get_answer(PROMPT_KEY['ADDRESS'])
        customer_cell_number = self.prompt_and_get_answer(
            PROMPT_KEY['CELLNUMBER'])
        customer_credit_card_number = self.prompt_and_get_answer(
            PROMPT_KEY['CREDITCARD'])
        self.authentication_controller.create_customer(
            customer_id, customer_password, customer_name, customer_address, customer_cell_number, customer_credit_card_number)

    def prompt_and_get_answer(self, key: PROMPT_KEY):
        answer = prompt(PROMPTS[key])
        return answer[key]
