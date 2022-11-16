from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Models.room import ROOM_TYPE
PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "CANCEL": 'cancel',
    "BACK": "back"
}

PROMPTS = {
    'operations': [{
        'type': 'list',
        'message': "Cancel a room",
        'name': 'operations',
        'choices': [
        ]
    }],
    'cancel': [{
        'type': 'list',
        'message': "Which one to cancel?",
        'name': 'cancel',
        'choices': [
        ]
    }],
    "back": [{
        'type': 'list',
        'message': "Click Enter to go back",
        'name': 'back',
        'choices': [
        ],
    }],
}


class CancelReservationView(View):
    reservation_controller: ReservationController
    room_controller: RoomController
    bill_controller: BillController
    user_id: str
    start_date: str
    duration: int
    is_accessibility_requested: int
    operation_options: List[Tuple[str, str]] = [
        ("Cancel another reservation", 'cancel_reservation'),
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None, user_id=None, start_date=None, duration=None, is_accessibility_requested=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()
        self.user_id = user_id
        self.start_date = start_date
        self.duration = duration
        self.is_accessibility_requested=is_accessibility_requested
        self.bill_controller = BillController()
        self.reservation_controller = ReservationController()

    def show(self):
        self.cancel_reservation()

    def show_again(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()
        getattr(self, callable)()

    

    def cancel_reservation(self):
        reservations = self.reservation_controller.get_open_reservations(
            self.user_id)
        if len(reservations) == 0:
            print("\nThere are no reservation\n")
            PROMPTS[PROMPT_KEY["BACK"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            self.prompt_and_get_answer(PROMPT_KEY['BACK'])

        else:
            PROMPTS[PROMPT_KEY["CANCEL"]][0]['choices'] = [
                {
                    "name": reservation.room_id+", with reservation id: "+str(reservation.reservation_id)+", start on: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+" days, "+("with" if reservation.is_accessibility_requested==1 else "without")+" accessibility accommodations, price: "+str(self.bill_controller.get_bill(reservation.bill_id).bill_amount)
                }
                for reservation in reservations
            ]
            PROMPTS[PROMPT_KEY["CANCEL"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            answer: str = self.prompt_and_get_answer(PROMPT_KEY['CANCEL'])
            if answer != "Back":
                answer_list: List[str] = answer.replace(':', ',').split(',')
                self.reservation_controller.cancel_reservation(
                    answer_list[0].strip(), answer_list[2].strip())
                print("\nSuccess!\n")
        self.show_again()

    def prompt_and_get_answer(self, key: PROMPT_KEY):
        answer = prompt(PROMPTS[key])
        return answer[key]

    def initiate_options(self):
        choices = []
        for operation_option in self.operation_options:
            choice = {
                'name': operation_option[0]
            }
            choices.append(choice)
        PROMPTS[PROMPT_KEY['OPERATIONS']][0]['choices'] = choices
        
