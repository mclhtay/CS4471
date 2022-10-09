from HotelBooking.Views.utils import big_print
from HotelBooking.Views.view import View
from HotelBooking.Views.checked_in_rooms_view import CheckedInRoomsView
from HotelBooking.Views.reserved_rooms_view import ReservedRoomsView
from typing import Tuple, List
from PyInquirer import prompt

PROMPT_KEY = {
    "OPERATIONS": "operations"
}

PROMPTS = {
    "operations": [{
        'type': 'list',
        'message': "Admin operations",
        'name': 'operations',
        'choices': [
        ]
    }]
}


class AdminView(View):
    view_options: List[Tuple[str, View]] = [
        ("Check-in/out for a guest", CheckedInRoomsView),
        ("Book/Cancel reservation for a guest", ReservedRoomsView)
    ]
    operation_options: List[Tuple[str, str]] = [
        ("Quit", 'quit_system'),
    ]
    history: List[View]

    def __init__(self, history=[], caller=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()

    def show(self):
        big_print("ADMIN  PORTAL")

        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        operations = [op[0] for op in self.operation_options]

        if operation in operations:
            callable = [operation_obj[1]
                        for operation_obj in self.operation_options if operation_obj[0] == operation].pop()
            getattr(self, callable)
        else:
            next = [view_obj[1]
                    for view_obj in self.view_options if view_obj[0] == operation].pop()
            self.next_view(next)

    def initiate_options(self):
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
        PROMPTS[PROMPT_KEY['OPERATIONS']][0]['choices'] = choices

    def prompt_and_get_answer(self, key: PROMPT_KEY):
        answer = prompt(PROMPTS[key])
        return answer[key]
