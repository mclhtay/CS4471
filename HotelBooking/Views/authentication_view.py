from HotelBooking.Views.customer_view import CustomerView
from HotelBooking.Views.registration_view import RegistrationView
from HotelBooking.Views.utils import big_print, error_print
from HotelBooking.Views.view import View
from HotelBooking.Views.admin_view import AdminView
from HotelBooking.Controllers.authentication_controller import AuthenticationController
from PyInquirer import prompt
from typing import Tuple, List

PROMPT_KEY = {
    "AUTHENTICATOR": 'authenticator',
    "USER_ID": 'user_id',
    "USER_PASSWORD": 'user_password'
}

PROMPTS = {
    "authenticator": [{
        'type': 'list',
        'message': 'Are you a hotel associate or a customer?',
        'name': 'authenticator',
        'choices': [
        ]
    }],
    "user_id": [{
        'type': 'input',
        'message': "Enter your id",
        'name': 'user_id',
    }],
    "user_password": [{
        "type": 'password',
        'message': 'Enter your password',
        'name': 'user_password',
    }],
}


class AuthenticationView(View):
    """
    This first view the user is presented with.
    Authentication view also directs the user to whichever portal the user wishes to see.
    """
    view_options: List[Tuple[str, View]] = [
        ("New Customer", RegistrationView),
        ("Existing Customer", CustomerView),
        ("Hotel associate", AdminView),
    ]
    operation_options: List[Tuple[str, str]] = [
        ("Quit", 'quit_system'),
    ]
    authentication_controller: AuthenticationController
    user_id: str
    user_password: str
    authenticated: bool

    def __init__(self, history: List[View] = [], caller: View = None):
        super().__init__(history, caller)
        self.authentication_controller = AuthenticationController()
        self.user_id = ""
        self.user_password = ""
        self.authenticated = False
        self.initiate_options()

    def show(self):
        """
        Other views may trace back into this view and attempt to access a different portal,
        the authenticated class variable must be turned to False every time to revoke access.
        """
        self.authenticated = False
        big_print("HOTEL BOOKING")

        authenticator = self.prompt_and_get_answer(PROMPT_KEY['AUTHENTICATOR'])
        if authenticator == "Quit":
            self.quit_system()
        elif authenticator == "New Customer":
            # take the user to register for a new customer, the view itself will trace back
            RegistrationView(self.history, self).show()
        else:
            while not self.authenticated:
                # keep prompting for retries if the user fails to authenticate themselves.
                self.user_id = self.prompt_and_get_answer(
                    PROMPT_KEY['USER_ID'])
                self.user_password = self.prompt_and_get_answer(
                    PROMPT_KEY['USER_PASSWORD'])
                authenticated = False
                if authenticator == "Hotel associate":
                    authenticated = self.authentication_controller.authenticate_admin(
                        self.user_id, self.user_password)
                else:
                    authenticated = self.authentication_controller.authenticate_customer(
                        self.user_id, self.user_password)

                self.authenticated = authenticated
                if not authenticated:
                    error_print("Authentication Failed!\t")

            if authenticator == "Hotel associate":
                AdminView(self.history, self).show()
            else:
                CustomerView(self.history, self, self.user_id).show()

    def initiate_options(self):
        """
        Fill view and operation options into pyinquirer compatible choices.
        """        
        choices = []
        for view_option in self.view_options:
            choice = {
                'name': view_option[0]
            }
            choices.append(choice)
        for operation_option in self.operation_options:
            choice = {
                'name': operation_option[0]
            }
            choices.append(choice)
        PROMPTS[PROMPT_KEY['AUTHENTICATOR']][0]['choices'] = choices

    def prompt_and_get_answer(self, key: PROMPT_KEY):
        answer = prompt(PROMPTS[key])
        return answer[key]
