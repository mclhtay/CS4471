from __future__ import annotations
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Views.reserved_rooms_admin_view import ReservedRoomsAdminView
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Models.room import ROOM_TYPE, Room

PROMPT_KEY = {
    "OPERATIONS": "operations",
    "CHECK_OUT": 'check_out',
    "CUSTOMER": "customer",
    "BACK": "back",
    "LIST_RESERVATION": "list_out_reservation"
}

PROMPTS = {
    "operations": [{
        'type': 'list',
        'message': "Check_in/out for a guest",
        'name': 'operations',
        'choices': [
        ]
    }],
    "check_out": [{
        'type': 'list',
        'message': 'Which one to check-out?',
        'name': 'check_out',
        'choices': [],
    }],
    "customer": [{
        'type': 'input',
        'message': "Enter the customer's ID",
        'name': 'customer',
    }],
    "back": [{
        'type': 'list',
        'message': "Click Enter to go back",
        'name': 'back',
        'choices': [
        ]
    }],
    'list_out_reservation': [{
        'type': 'list',
        'message': "Which reservation do you want to change",
        'name': 'list_out_reservation',
        'choices': [
        ]
    }],
}


class CheckedInRoomsView(View):
    operation_options: List[Tuple[str, str]] = [
        ("Check-in a customer", 'check_in_customer'),
        ("Check-out a customer", 'check_out_customer'),
        ("Back", 'prev_view'),
    ]
    room_controller: RoomController
    reservation_controller: ReservationController
    bill_controller: BillController

    def __init__(self, history=[], caller=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()
        self.reservation_controller = ReservationController()
        self.bill_controller = BillController()

    def show(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()
        getattr(self, callable)()

    def check_in_customer(self):
        customer_id = self.prompt_and_get_answer(PROMPT_KEY['CUSTOMER'])
        reservations = self.reservation_controller.get_open_reservations(
            customer_id)
        if len(reservations) == 0:
            print("\nThere are no reservation\n")

            self.prompt_and_get_answer(PROMPT_KEY['BACK'])

        else:
            PROMPTS[PROMPT_KEY["LIST_RESERVATION"]][0]['choices'] = [
                {
                    "name": reservation.room_id+", with reservation id: "+str(reservation.reservation_id)+", start on: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+" days, "+("with" if reservation.is_accessibility_requested==1 else "without")+" accessibility accommodation, price: "+str(self.bill_controller.get_bill(reservation.bill_id).bill_amount)
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
                roomID = answer_list[0].strip()
                reservation_id = answer_list[2].strip()
                room: Room = self.room_controller.get_room(
                    roomID)
                if room is None:
                    print("This customer does not have a reservation!")
                else:
                    self.room_controller.check_in_room(
                        room.room_id, reservation_id)

                    print("\nSuccess!\n")
        self.show()

    def check_out_customer(self):
        checked_in_rooms = self.room_controller.get_checked_in_rooms()
        if len(checked_in_rooms) == 0:
            print("\nThere are no checked in rooms\n")
        else:
            PROMPTS[PROMPT_KEY["CHECK_OUT"]][0]['choices'] = [
                {
                    "name": room.room_id
                }
                for room in checked_in_rooms
            ]
            PROMPTS[PROMPT_KEY["CHECK_OUT"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            room_id = self.prompt_and_get_answer(PROMPT_KEY['CHECK_OUT'])
            if room_id != "Back":
                self.room_controller.check_out_room(room_id)
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
        PROMPTS[PROMPT_KEY["BACK"]][0]['choices'] = []
        PROMPTS[PROMPT_KEY["BACK"]][0]['choices'].append(
            {
                "name": "Back"
            }
        )
