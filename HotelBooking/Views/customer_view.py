from HotelBooking.Views.modify_reservation_view import ModifyReservationView
from HotelBooking.Views.pay_bill_view import PayBillView
from HotelBooking.Views.reserved_history_view import ReservationHistoryView
from HotelBooking.Views.utils import big_print, medium_print
from HotelBooking.Views.view import View
from HotelBooking.Views.reserved_rooms_view import ReservedRoomsView
from typing import Tuple, List
from PyInquirer import prompt

PROMPT_KEY = {
    "OPERATIONS": "operations"
}

PROMPTS = {
    "operations": [{
        'type': 'list',
        'message': "Customer operations",
        'name': 'operations',
        'choices': [
        ]
    }]
}


class CustomerView(View):
    userID: str
    view_options: List[Tuple[str, View]] = [
        ("Book/Cancel reservation", ReservedRoomsView),
        ("Modify reservation", ModifyReservationView),
        ("Check/Pay Bill", PayBillView),
        ("Check reservation/stay history", ReservationHistoryView)

    ]
    operation_options: List[Tuple[str, str]] = [
        ("Quit", 'quit_system'),
    ]

    def __init__(self, history=[], caller=None, userID=None) -> None:
        super().__init__(history, caller)
        self.userID = userID
        self.initiate_options()

    def show(self):
        big_print("Customer PORTAL")
        medium_print("Userid: "+self.userID)
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        operations = [op[0] for op in self.operation_options]

        if operation in operations:
            callable = [operation_obj[1]
                        for operation_obj in self.operation_options if operation_obj[0] == operation].pop()
            getattr(self, callable)
        else:
            next = [view_obj[1]
                    for view_obj in self.view_options if view_obj[0] == operation].pop()
            next(self.history, self, self.userID).show()

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
