from __future__ import annotations
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Models.room import ROOM_TYPE

PROMPT_KEY = {
    "OPERATIONS": "operations",
    "CHECK-IN": 'check-in',
    "ROOM-CHECK-IN": 'room-check-in',
    "CHECK-OUT": 'check-out',
    "CUSTOMER": "customer"
}

PROMPTS = {
    "operations": [{
        'type': 'list',
        'message': "Check-in/out for a guest",
        'name': 'operations',
        'choices': [
        ]
    }],
    "check-in": [{
        'type': 'confirm',
        'message': 'Did the customer make a reservation?',
        'name': 'check-in',
    }],
    "room-check-in": [{
        'type': 'list',
        'message': 'What type of room?',
        'name': 'room-check-in',
        'choices': [],
        'filter': lambda choice: choice.split(" ")[0].upper(),
    }],
    "check-out": [{
        'type': 'list',
        'message': 'Which one to check-out?',
        'name': 'check-out',
        'choices': [],
    }],
    "customer": [{
        'type': 'input',
        'message': "Enter the customer's ID",
        'name': 'customer',
    }]
}


class CheckedInRoomsView(View):
    operation_options: List[Tuple[str, str]] = [
        ("Check-in a customer", 'check_in_customer'),
        ("Check-out a customer", 'check_out_customer'),
        ("Back", 'prev_view'),
    ]
    room_controller: RoomController

    def __init__(self, history=[], caller=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()

    def show(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()
        getattr(self, callable)()

    def check_in_customer(self):
        check_in_choice = self.prompt_and_get_answer(
            PROMPT_KEY['CHECK-IN'])
        if check_in_choice:
            self.reserved_check_in()
        else:
            self.new_check_in()

    def check_out_customer(self):
        checked_in_rooms = self.room_controller.get_checked_in_rooms()
        if len(checked_in_rooms) == 0:
            print("\nThere are no checked in rooms\n")
        else:
            PROMPTS[PROMPT_KEY["CHECK-OUT"]][0]['choices'] = [
                {
                    "name": room.room_id
                }
                for room in checked_in_rooms
            ]
            PROMPTS[PROMPT_KEY["CHECK-OUT"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            room_id = self.prompt_and_get_answer(PROMPT_KEY['CHECK-OUT'])
            if room_id != "Back":
                self.room_controller.check_out_room(room_id)
                print("\nSuccess!\n")
            self.show()

    def new_check_in(self):
        available_rooms = self.room_controller.get_available_rooms()
        singles = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["SINGLE"]]
        doubles = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["DOUBLE"]]
        deluxes = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["DELUXE"]]
        presidentials = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["PRESIDENTIAL"]]

        PROMPTS[PROMPT_KEY["ROOM-CHECK-IN"]][0]['choices'] = [
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
        room_choice = self.prompt_and_get_answer(PROMPT_KEY['ROOM-CHECK-IN'])
        if room_choice != "BACK":
            room_id = [
                room.room_id for room in available_rooms if room.room_type == room_choice].pop()
            customer_id = self.prompt_and_get_answer(PROMPT_KEY['CUSTOMER'])
            self.room_controller.check_in_room(room_id, customer_id)
            print("\nSuccess!\n")
        self.show()

    def reserved_check_in(self):
        customer_id = self.prompt_and_get_answer(PROMPT_KEY['CUSTOMER'])
        room = self.room_controller.get_reserved_room(customer_id)
        if room is None:
            print("This customer does not have a reservation!")
        else:
            self.room_controller.check_in_room(room.room_id, customer_id)
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
