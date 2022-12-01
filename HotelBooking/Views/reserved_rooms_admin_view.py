from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Models.room import ROOM_TYPE
from HotelBooking.Views.utils import validate_date

PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "RESERVE": 'reserve',
    "CANCEL": 'cancel',
    "START_DATE": "start_date",
    "DURATION": "duration",
    "ACCOMMODATION": "accommodation",
    "BACK": "back",
    "FINAL_CHECK": "final_check",
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
    }],
    "start_date": [{
        'type': 'input',
        'message': "Enter the start date in format (mm/dd/yyyy)",
        'name': 'start_date',
        'validate': lambda x: validate_date(x) or "Please erase value and enter a valid date in (mm/dd/yyyy) format."
    }],
    "duration": [{
        'type': 'input',
        'message': "Enter the number of days you want to reserve",
        'name': 'duration',
        'validate': lambda x: x.isdigit() or "Please erase value and enter a valid number!"

    }],
    "accommodation": [{
        'type': 'confirm',
        'message': "Do you require accessibility accommodations?",
        'name': 'accommodation',
        'filter': lambda val: 1 if val else 0
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


class ReservedRoomsAdminView(View):
    """
    This view presents room reservation controls for an admin.
    The operations are more straight forward for the admin in comparison to the customer version,
    though many operations do similar tasks.
    """
    reservation_controller: ReservationController
    room_controller: RoomController
    bill_controller: BillController
    user_id: str
    start_date: str
    duration: int
    is_accessibility_requested: int
    operation_options: List[Tuple[str, str]] = [
        ("Reserve a room", 'reserve_room'),
        ("Reserve a room and check in", 'reserve_room_and_check_in'),
        ("Cancel a reservation", 'cancel_reservation'),
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None, user_id=None, start_date=None, duration=None, is_accessibility_requested=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()
        self.user_id = user_id
        self.start_date = start_date
        self.duration = duration
        self.is_accessibility_requested = is_accessibility_requested
        self.bill_controller = BillController()
        self.reservation_controller = ReservationController()

    def show(self):
        if self.user_id == None:
            # To reserve a room, the customer's user id has is required
            self.user_id = self.prompt_and_get_answer(PROMPT_KEY['CUSTOMER'])
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        # if user selected an operation, operations are mapped to in-file python methods
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()
        # activate dynamically with getattr
        getattr(self, callable)()

    def reserve_room_and_check_in(self):
        """
        Operation to check in a walk-in customer.
        """
        available_rooms = self.room_controller.get_available_rooms()
        # categorize obtained avaiable rooms to better present to the user
        singles = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["SINGLE"]]
        doubles = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["DOUBLE"]]
        deluxes = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["DELUXE"]]
        presidentials = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["PRESIDENTIAL"]]

        PROMPTS[PROMPT_KEY["RESERVE"]][0]['choices'] = [
            # fill pyinquirer compatible prompts so user can select from console
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
            # obtain user requirements for a new room reservation
            room_id = [
                room.room_id for room in available_rooms if room.room_type == room_choice].pop()
            if self.user_id == None:
                self.user_id = self.prompt_and_get_answer(
                    PROMPT_KEY['CUSTOMER'])
            self.start_date = self.prompt_and_get_answer(
                PROMPT_KEY['START_DATE'])
            self.duration = int(
                self.prompt_and_get_answer(PROMPT_KEY['DURATION']))
            self.is_accessibility_requested = self.prompt_and_get_answer(
                PROMPT_KEY['ACCOMMODATION'])

            current_room_type = self.room_controller.get_room(
                room_id).room_type
            PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['message'] = "The total is " + \
                str(self.duration * self.room_controller.get_price(current_room_type))

            if self.prompt_and_get_answer(PROMPT_KEY['FINAL_CHECK']) == "Continue":
                self.reservation_controller.reserve_room(
                    room_id, self.user_id, self.start_date, self.duration, self.is_accessibility_requested, "IN_PROGRESS")
                print("\nSuccess!\n")
        self.show()

    def reserve_room(self):
        """
        Operation to just reserve a room
        """
        available_rooms = self.room_controller.get_available_rooms()
        # categorize obtained avaiable rooms to better present to the user
        singles = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["SINGLE"]]
        doubles = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["DOUBLE"]]
        deluxes = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["DELUXE"]]
        presidentials = [
            room for room in available_rooms if room.room_type == ROOM_TYPE["PRESIDENTIAL"]]

        PROMPTS[PROMPT_KEY["RESERVE"]][0]['choices'] = [
            # fill pyinquirer compatible prompts so user can select from console
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
            self.is_accessibility_requested = self.prompt_and_get_answer(
                PROMPT_KEY['ACCOMMODATION'])

            current_room_type = self.room_controller.get_room(
                room_id).room_type
            PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['message'] = "The total is " + \
                str(self.duration * self.room_controller.get_price(current_room_type))

            if self.prompt_and_get_answer(PROMPT_KEY['FINAL_CHECK']) == "Continue":
                self.reservation_controller.reserve_room(
                    room_id, self.user_id, self.start_date, self.duration, self.is_accessibility_requested)
                print("\nSuccess!\n")
        self.show()

    def cancel_reservation(self):
        """
        Operation to cancel a reservation and cancel the bill associated
        """
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
                    "name": reservation.room_id+", with reservation id: "+str(reservation.reservation_id)+", start on: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+" days, "+("with" if reservation.is_accessibility_requested == 1 else "without")+" accessibility accommodations, price: "+str(self.bill_controller.get_bill(reservation.bill_id).bill_amount)
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
        self.show()

    def prompt_and_get_answer(self, key: PROMPT_KEY):
        answer = prompt(PROMPTS[key])
        return answer[key]

    def initiate_options(self):
        """
        Fill view and operation options into pyinquirer compatible choices.
        """
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
