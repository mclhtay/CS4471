from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Models.room import ROOM_TYPE
from HotelBooking.Models.roomType import RoomType
PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "LIST_RESERVATION": "listReservation",
    "LIST_STAY": "listStay",
    "BACK": "back",
    "FINAL_CHECK": "finalCheck"
}

PROMPTS = {
    'operations': [{
        'type': 'list',
        'message': "Check Or pay your Bill",
        'name': 'operations',
        'choices': [
        ]
    }],
    'listReservation': [{
        'type': 'list',
        'message': "List Reservation:",
        'name': 'listReservation',
        'choices': [
        ],
    }],
    'listStay': [{
        'type': 'list',
        'message': "List Stay:",
        'name': 'listStay',
        'choices': [
        ],
    }],
    "finalCheck": [{
        'type': 'list',
        'message': "The total is ",
        'name': 'finalCheck',
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


class ReservationHistoryView(View):
    reservation_controller: ReservationController
    room_controller: RoomController
    bill_controller: BillController
    userID: str
    startDate: str
    duration: int
    roomType: RoomType
    operation_options: List[Tuple[str, str]] = [
        ("List all reservation", 'listReservation'),
        ("List stay", 'listStay'),
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None, userID=None, startDate=None, duration=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()
        self.userID = userID
        self.startDate = startDate
        self.duration = duration
        self.roomType = RoomType()
        self.reservation_controller = ReservationController()
        self.bill_controller = BillController()

    def show(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()

        getattr(self, callable)()

    def listStay(self):
        reservations = self.reservation_controller.get_stay(self.userID)
        if len(reservations) == 0:
            print("\nThere are no stay history\n")
            self.prompt_and_get_answer(PROMPT_KEY['BACK'])

        else:
            for reservation in reservations:
                print("stay with reservation id:"+str(reservation.reservation_id)+", with bill: "+str(reservation.bill_id)+", with room id:" +
                      str(reservation.room_id)+", with check-in date: "+reservation.reservation_checkin_date+", with stay date: "+str(reservation.reservation_stay_date)+"\n")

            self.prompt_and_get_answer(PROMPT_KEY['BACK'])
        self.show()

    def listReservation(self):
        reservations = self.reservation_controller.get_reservation(self.userID)
        if len(reservations) == 0:
            print("\nThere are no reservation\n")
            self.prompt_and_get_answer(PROMPT_KEY['BACK'])

        else:
            for reservation in reservations:
                print("reservation:"+str(reservation.reservation_id)+", with bill: "+str(reservation.bill_id)+", with status: "+reservation.status+", with room id:" +
                      str(reservation.room_id)+", with check-in date: "+reservation.reservation_checkin_date+", with stay date: "+str(reservation.reservation_stay_date)+"\n")

            self.prompt_and_get_answer(PROMPT_KEY['BACK'])
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
        PROMPTS[PROMPT_KEY["BACK"]][0]['choices'] = []
        PROMPTS[PROMPT_KEY["BACK"]][0]['choices'].append(
            {
                "name": "Back"
            }
        )
        PROMPTS[PROMPT_KEY['OPERATIONS']][0]['choices'] = choices
