from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Views.utils import validate_date

PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "CHANGE_START_DATE": 'change_start_date',
    "CHANGE_DURATION": 'duration',
    "BACK": "back",
    "FINAL_CHECK": "final_check",
    "LIST_RESERVATION": "list_out_reservation"
}

PROMPTS = {
    'operations': [{
        'type': 'list',
        'message': "",
        'name': 'operations',
        'choices': [
        ]
    }],
    'change_start_date': [{
        'type': 'input',
        'message': "Enter a new start date in format (mm/dd/yyyy)",
        'name': 'change_start_date',
        'validate': lambda x: validate_date(x) or "Please erase value and enter a valid date in (mm/dd/yyyy) format."
    }],
    'duration': [{
        'type': 'input',
        'message': "Enter a new duration",
        'name': 'duration',
        'validate': lambda x: x.isdigit() or "Please erase value and enter a valid number!"
    }],
    'list_out_reservation': [{
        'type': 'list',
        'message': "Which reservation do you want to change",
        'name': 'list_out_reservation',
        'choices': [
        ]
    }],
    "final_check": [{
        'type': 'list',
        'message': "The total is ",
        'name': 'final_check',
        'choices': [
        ]
    }],
    "back": [{
        'type': 'list',
        'message': "Click Enter to go back",
        'name': 'back',
        'choices': [
        ]
    }],
}


class ModifyReservationView(View):
    reservation_controller: ReservationController
    room_controller: RoomController
    user_id: str
    bill_controller: BillController
    reservation_id: int
    operation_options: List[Tuple[str, str]] = [
        ("Change the start date", 'change_start_date'),
        ("Change the duration", 'change_duration'),
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None, user_id=None, start_date=None, duration=None, is_accessibility_requested=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()
        self.user_id = user_id
        self.bill_controller = BillController()
        self.reservation_controller = ReservationController()
        self.is_accessibility_requested=is_accessibility_requested

    def show(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()

        getattr(self, callable)()

    def change_start_date(self):
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
            PROMPTS[PROMPT_KEY["LIST_RESERVATION"]][0]['choices'] = [
                {
                    "name": reservation.room_id+", with reservation id: "+str(reservation.reservation_id)+", start on: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+" days, "+("with" if reservation.is_accessibility_requested==1 else "without")+" accessibility accommodations, price: "+str(self.bill_controller.get_bill(reservation.bill_id).bill_amount)
                }
                for reservation in reservations
            ]
            PROMPTS[PROMPT_KEY["LIST_RESERVATION"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            answer: str = self.prompt_and_get_answer(
                PROMPT_KEY['LIST_RESERVATION'])
            if answer != "Back":
                answer_list: List[str] = answer.replace(':', ',').split(',')
                newDate = self.prompt_and_get_answer(
                    PROMPT_KEY['CHANGE_START_DATE'])
                reservation_id = answer_list[2].strip()
                self.reservation_controller.modify_reservation_date(
                    reservation_id, newDate)
                print("\nSuccess!\n")
        self.show()

    def change_duration(self):
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
            PROMPTS[PROMPT_KEY["LIST_RESERVATION"]][0]['choices'] = [
                {
                    "name": reservation.room_id+", with reservation id: "+str(reservation.reservation_id)+", start on: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+" days, "+("with" if reservation.is_accessibility_requested==1 else "without")+" accessibility accommodations, price: "+str(self.bill_controller.get_bill(reservation.bill_id).bill_amount)
                }
                for reservation in reservations
            ]
            PROMPTS[PROMPT_KEY["LIST_RESERVATION"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )

            answer: str = self.prompt_and_get_answer(
                PROMPT_KEY['LIST_RESERVATION'])
            if answer != "Back":
                answer_list: List[str] = answer.replace(':', ',').split(',')
                duration = int(
                    self.prompt_and_get_answer(PROMPT_KEY['CHANGE_DURATION']))


                reservation_id = answer_list[2].strip()
                room_id = answer_list[0].strip()
                current_room_type = self.room_controller.get_room(
                    room_id).room_type
                i: int = duration * \
                    self.room_controller.get_price(current_room_type)
                PROMPTS[PROMPT_KEY["FINAL_CHECK"]
                        ][0]['message'] = "The total is "+str(i)

                if self.prompt_and_get_answer(PROMPT_KEY['FINAL_CHECK']) == "Continue":
                    self.reservation_controller.modify_reservation_duration(
                        reservation_id, duration)
                    print("\nSuccess!\n")
        self.show()

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
        PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices'] = []
        PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices'].append(
            {
                "name": "Continue"
            }
        )
        PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices'].append(
            {
                "name": "Back",
            }
        )
