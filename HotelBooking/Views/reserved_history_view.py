from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt

PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "LIST_RESERVATION": "list_reservation",
    "LIST_STAY": "list_stay",
    "BACK": "back",
    "FINAL_CHECK": "final_check"
}

PROMPTS = {

    'list_reservation': [{
        'type': 'list',
        'message': "List Reservation:",
        'name': 'list_reservation',
        'choices': [
        ],
    }],
    'list_stay': [{
        'type': 'list',
        'message': "List Stay:",
        'name': 'list_stay',
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
    """
    This view presents all reservation history for a customer
    """
    reservation_controller: ReservationController
    user_id: str
    start_date: str
    is_accessibility_requested: int
    duration: int
    operation_options: List[Tuple[str, str]] = [
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None, user_id=None, start_date=None, duration=None, is_accessibility_requested=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.user_id = user_id
        self.start_date = start_date
        self.duration = duration
        self.is_accessibility_requested = is_accessibility_requested
        self.reservation_controller = ReservationController()

    def show(self):
        self.list_reservation()
        self.list_stay()

        operation = self.prompt_and_get_answer(PROMPT_KEY['BACK'])
        # if user selected an operation, operations are mapped to in-file python methods
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()
        # activate dynamically with getattr
        getattr(self, callable)()

    def list_stay(self):
        """
        This operation presents all the instances where a customer checked-in.
        """
        print("\nStay history:\n")
        reservations = self.reservation_controller.get_stay_history(
            self.user_id)
        if len(reservations) == 0:
            print("\nThere are no stay history\n")
        else:
            for reservation in reservations:
                print("stay with reservation id:"+str(reservation.reservation_id)+", with bill: "+str(reservation.bill_id)+", with room id:" +
                      str(reservation.room_id)+", with check-in date: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+(" with" if reservation.is_accessibility_requested == 1 else " without")+" accessibility accommodations"+"\n")

    def list_reservation(self):
        """
        This operation presents all the instances where a customer reserved a room.
        """
        print("\nAll reservations:\n")
        reservations = self.reservation_controller.get_reservations(
            self.user_id)
        if len(reservations) == 0:
            print("\nThere are no reservation\n")
        else:
            for reservation in reservations:
                print("reservation:"+str(reservation.reservation_id)+", with bill: "+str(reservation.bill_id)+", with status: "+reservation.status+", with room id:" +
                      str(reservation.room_id)+", with check-in date: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+(", with" if reservation.is_accessibility_requested == 1 else ", without")+" accessibility accommodations"+"\n")

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
        PROMPTS[PROMPT_KEY["BACK"]][0]['choices'] = []
        PROMPTS[PROMPT_KEY["BACK"]][0]['choices'].append(
            {
                "name": "Back"
            }
        )
