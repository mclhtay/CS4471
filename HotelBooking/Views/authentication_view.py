from HotelBooking.Views.utils import error_print
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
    view_options: List[Tuple[str, View]] = [
        ("Customer", View),
        ("Hotel associate", AdminView)
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
        authenticator = self.prompt_and_get_answer(PROMPT_KEY['AUTHENTICATOR'])

        while not self.authenticated:
            self.user_id = self.prompt_and_get_answer(PROMPT_KEY['USER_ID'])
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

        next = AdminView if authenticator == "Hotel associate" else None
        self.next_view(next)

    def initiate_options(self):
        for view_option in self.view_options:
            choice = {
                'name': view_option[0]
            }
            PROMPTS[PROMPT_KEY['AUTHENTICATOR']][0]['choices'].append(choice)

    def prompt_and_get_answer(self, key: PROMPT_KEY):
        answer = prompt(PROMPTS[key])
        return answer[key]
