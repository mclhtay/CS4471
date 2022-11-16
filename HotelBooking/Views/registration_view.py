from HotelBooking.Controllers.authentication_controller import AuthenticationController
from HotelBooking.Views.utils import big_print, medium_print
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "USERNAME": 'username',
    "PASSWORD": "password",
    "FULLNAME": "full_name",
    "ADDRESS": "address",
    "CELLNUMBER": "cell_number",
    "CREDITCARD": "creditcard_number",
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
        'type': 'input',
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
    }],
    "creditcard_number": [{
        'type': 'input',
        'message': "Enter your credit card number",
        'name': 'creditcard_number',
    }],
}


class RegistrationView(View):
    authentication_controller: AuthenticationController
    customer_id: str
    customer_password: str
    customer_name: str
    customer_address: str
    customer_cellnumber: int
    customer_creditcardnumber: int

    def __init__(self, history=[], caller=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.authentication_controller = AuthenticationController()

    def show(self):
        big_print("Registration PORTAL")
        self.create_customer()

    def create_customer(self):
        customer_id = self.prompt_and_get_answer(PROMPT_KEY['USERNAME'])
        customer_password = self.prompt_and_get_answer(PROMPT_KEY['PASSWORD'])
        customer_name = self.prompt_and_get_answer(PROMPT_KEY['FULLNAME'])
        customer_address = self.prompt_and_get_answer(PROMPT_KEY['ADDRESS'])
        customer_cellnumber = self.prompt_and_get_answer(PROMPT_KEY['CELLNUMBER'])
        customer_creditcardnumber = self.prompt_and_get_answer(PROMPT_KEY['CREDITCARD'])
        self.authentication_controller.create_customer(customer_id, customer_password, customer_name, customer_address, customer_cellnumber, customer_creditcardnumber)

    def prompt_and_get_answer(self, key: PROMPT_KEY):
        answer = prompt(PROMPTS[key])
        return answer[key]

