from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Models.room import ROOM_TYPE

PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "RESERVE": 'reserve',
    "CANCEL": 'cancel',
    "CUSTOMER": "customer"
}

PROMPTS = {
    'operations': [{
        'type': 'list',
        'message': "Reserve/Cancel a room for a guest",
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
    'cancel': [{
        'type': 'list',
        'message': "Which one to cancel?",
        'name': 'cancel',
        'choices': [
        ]
    }],
    "customer": [{
        'type': 'input',
        'message': "Enter the customer's ID",
        'name': 'customer',
    }]
}


class ReservedRoomsView(View):
    room_controller: RoomController
    operation_options: List[Tuple[str, str]] = [
        ("Reserve a room", 'reserve_room'),
        ("Cancel a reservation", 'cancel_reservation'),
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()

    def show(self):
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
            customer_id = self.prompt_and_get_answer(PROMPT_KEY['CUSTOMER'])
            self.room_controller.reserve_room(room_id, customer_id)
            print("\nSuccess!\n")
        self.show()

    def cancel_reservation(self):
        reserved_rooms = self.room_controller.get_reserved_rooms()
        if len(reserved_rooms) == 0:
            print("\nThere are no reserved rooms\n")
        else:
            PROMPTS[PROMPT_KEY["CANCEL"]][0]['choices'] = [
                {
                    "name": room.room_id
                }
                for room in reserved_rooms
            ]
            PROMPTS[PROMPT_KEY["CANCEL"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            room_id = self.prompt_and_get_answer(PROMPT_KEY['CANCEL'])
            if room_id != "Back":
                self.room_controller.cancel_reservation(room_id)
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
