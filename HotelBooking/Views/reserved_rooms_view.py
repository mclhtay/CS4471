from HotelBooking.Controllers import room_controller
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Models.bill import Bill
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Models.room import ROOM_TYPE
from HotelBooking.Models.roomType import RoomType
PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "RESERVE": 'reserve',
    "CANCEL": 'cancel',
    "STARTDATE": "startDate", 
    "DURATION": "duration",
    "BACK": "back",
    "FINAL_CHECK":"finalCheck"
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
    "startDate": [{
        'type': 'input',
        'message': "Enter the start date",
        'name': 'startDate',
    }],
    "duration": [{
        'type': 'input',
        'message': "Enter the amount of date you want to reserve",
        'name': 'duration',
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


class ReservedRoomsView(View):
    room_controller: RoomController
    userID: str
    startDate: str
    duration: int
    bill:Bill
    roomType: RoomType
    operation_options: List[Tuple[str, str]] = [
        ("Reserve a room", 'reserve_room'),
        ("Cancel a reservation", 'cancel_reservation'),
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None, userID=None, startDate=None, duration=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()
        self.userID=userID
        self.startDate=startDate
        self.duration=duration
        self.roomType=RoomType()
        self.bill=Bill()

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
            if self.userID==None:
                self.userID = self.prompt_and_get_answer(PROMPT_KEY['CUSTOMER'])
            if self.startDate==None:
                self.startDate = self.prompt_and_get_answer(PROMPT_KEY['STARTDATE'])
            if self.duration==None:
                self.duration = int(self.prompt_and_get_answer(PROMPT_KEY['DURATION']))
            PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices'].append(
                {
                    "name": "Continue"
                }
            )
            current_room_type=self.room_controller.get_room(room_id).room_type
            PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['message']+=str(self.duration* self.roomType.get_Price(current_room_type))
            PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            if self.prompt_and_get_answer(PROMPT_KEY['FINAL_CHECK']) =="Continue":
                self.room_controller.reserve_room(room_id, self.userID, self.startDate, self.duration)
                print("\nSuccess!\n")
        self.show()

    def cancel_reservation(self):
        reservations = self.room_controller.get_reservation(self.userID)
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
                    "name": reservation.room_id+", with reservation id: "+str(reservation.reservation_id)+", start on: "+reservation.reservation_checkin_date+", price: "+str(self.bill.get_bill(reservation.bill_id).bill_amount)
                }
                for reservation in reservations
            ]
            PROMPTS[PROMPT_KEY["CANCEL"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            answer:str=self.prompt_and_get_answer(PROMPT_KEY['CANCEL'])
            if answer != "Back":
                answerList:List[str] = answer.replace(':', ',').split(',')
                self.room_controller.cancel_reservation(answerList[0].strip(), answerList[2].strip())
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
