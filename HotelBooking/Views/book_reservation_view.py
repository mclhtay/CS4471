from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Models.room import ROOM_TYPE
PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "RESERVE": 'reserve',
    "START_DATE": "start_date",
    "DURATION": "duration",
    "ACCOMMODATION": "accommodation",
    "BACK": "back",
    "FINAL_CHECK": "final_check"
}

PROMPTS = {
    'operations': [{
        'type': 'list',
        'message': "Reserve a room",
        'name': 'operations',
        'choices': [
        ]
    }],
    'reserve': [{
        'type': 'list',
        'message': "What type of room?",
        'name': 'reserve',
        'choices': [
        ],
        'filter': lambda choice: choice.split(" ")[0].upper(),
    }],
    "customer": [{
        'type': 'input',
        'message': "Enter the customer's ID",
        'name': 'customer',
    }],
    "start_date": [{
        'type': 'input',
        'message': "Enter the start date",
        'name': 'start_date',
    }],
    "duration": [{
        'type': 'input',
        'message': "Enter the number of days you want to reserve",
        'name': 'duration',
    }],
    "accommodation": [{
        'type': 'input',
        'message': "Do you require accessibility accommodations? Y/N",
        'name': 'accommodation',
    }],
    "final_check": [{
        'type': 'list',
        'message': "The total is ",
        'name': 'final_check',
        'choices': [
        ],
    }],
    "back": [{
        'type': 'list',
        'message': "Click Enter to go back",
        'name': 'back',
        'choices': [
        ],
    }],
}


class BookReservationView(View):
    reservation_controller: ReservationController
    room_controller: RoomController
    user_id: str
    start_date: str
    duration: int
    is_accessibility_requested: int
    operation_options: List[Tuple[str, str]] = [
        ("Reserve another room", 'reserve_room'),
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None, user_id=None, start_date=None, duration=None, is_accessibility_requested=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()
        self.user_id = user_id
        self.start_date = start_date
        self.duration = duration
        self.reservation_controller = ReservationController()
        self.is_accessibility_requested = is_accessibility_requested

    def show(self):
        self.reserve_room()

    def show_again(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()
        getattr(self, callable)()

    def reserve_room(self):
        available_rooms = self.room_controller.get_available_rooms()
        singles = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["SINGLE"]]
        doubles = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["DOUBLE"]]
        deluxes = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["DELUXE"]]
        presidentials = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["PRESIDENTIAL"]]

        PROMPTS[PROMPT_KEY["RESERVE"]][0]['choices'] = [
            {
                "name": f'Single ({len(singles)} available)',
                'disabled': "Not available" if len(singles) == 0 else False
            },
            {
                "name": f'Double ({len(doubles)} available)',
                'disabled': "Not available" if len(doubles) == 0 else False
            },
            {
                "name": f'Deluxe ({len(deluxes)} available)',
                'disabled': "Not available" if len(deluxes) == 0 else False
            },
            {
                "name": f'Presidential ({len(presidentials)} available)',
                'disabled': "Not available" if len(presidentials) == 0 else False
            },
            {
                "name": "Back"
            }
        ]

        room_choice = self.prompt_and_get_answer(PROMPT_KEY['RESERVE'])
        if room_choice != "BACK":
            room_id = [
                room.room_id for room in available_rooms if room.room_type == room_choice].pop()
            if self.user_id == None:
                self.user_id = self.prompt_and_get_answer(
                    PROMPT_KEY['CUSTOMER'])
            self.start_date = self.prompt_and_get_answer(
                PROMPT_KEY['START_DATE'])
            self.duration = int(
                self.prompt_and_get_answer(PROMPT_KEY['DURATION']))
            accommodation = self.prompt_and_get_answer(PROMPT_KEY['ACCOMMODATION'])
            self.is_accessibility_requested = 1 if accommodation == "Y" else 0

            current_room_type = self.room_controller.get_room(
                room_id).room_type
            PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['message'] = "The total is " + \
                str(self.duration * self.room_controller.get_price(current_room_type))

            if self.prompt_and_get_answer(PROMPT_KEY['FINAL_CHECK']) == "Continue":
                self.reservation_controller.reserve_room(
                    room_id, self.user_id, self.start_date, self.duration, self.is_accessibility_requested)
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
        PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices'] = []
        PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices'].append(
            {
                "name": "Continue"
            }
        )
        PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices'].append(
            {
                "name": "Back"
            }
        )