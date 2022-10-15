from HotelBooking.Controllers.reservation_controller import ReservationController
from HotelBooking.Controllers.room_controller import RoomController
from HotelBooking.Models.bill import Bill
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Models.room import ROOM_TYPE
from HotelBooking.Models.roomType import RoomType
PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "CHANGE_START_DATE": 'changeStartDate',
    "CHANGE_DURATION": 'duration',
    "BACK": "back",
    "FINAL_CHECK":"finalCheck",
    "LIST_RESERVATION":"listOutReservation"
}

PROMPTS = {
    'operations': [{
        'type': 'list',
        'message': "",
        'name': 'operations',
        'choices': [
        ]
    }],
    'changeStartDate': [{
        'type': 'input',
        'message': "Enter a new start date",
        'name': 'changeStartDate'
    }],
    'duration': [{
        'type': 'input',
        'message': "Enter a new duration",
        'name': 'duration'
    }],
    'listOutReservation': [{
        'type': 'list',
        'message': "Which reservation do you want to change",
        'name': 'listOutReservation',
        'choices': [
        ]
    }],
    "finalCheck": [{
        'type': 'list',
        'message': "The total is ",
        'name': 'finalCheck',
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
    userID: str
    bill:Bill
    roomType: RoomType
    reservationID:int
    operation_options: List[Tuple[str, str]] = [
        ("Change the start date", 'changeStartDate'),
        ("Change the duration", 'changeDuration'),
        ("Back", 'prev_view'),
    ]

    def __init__(self, history=[], caller=None, userID=None, startDate=None, duration=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.room_controller = RoomController()
        self.userID=userID
        self.roomType=RoomType()
        self.bill=Bill()
        self.reservation_controller=ReservationController()

    def show(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()

        
        getattr(self, callable)()

    def changeStartDate(self):
        reservations = self.reservation_controller.get_open_reservation(self.userID)
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
                    "name": reservation.room_id+", with reservation id: "+str(reservation.reservation_id)+", start on: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+" days, price: "+str(self.bill.get_bill(reservation.bill_id).bill_amount)
                }
                for reservation in reservations
            ]
            PROMPTS[PROMPT_KEY["LIST_RESERVATION"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            answer:str=self.prompt_and_get_answer(PROMPT_KEY['LIST_RESERVATION'])
            if answer != "Back":
                answerList:List[str] = answer.replace(':', ',').split(',')
                newDate=self.prompt_and_get_answer(PROMPT_KEY['CHANGE_START_DATE'])
                reservationID=answerList[2].strip()
                self.reservation_controller.modify_reservation_date(reservationID, newDate)
                print("\nSuccess!\n")
        self.show()

    def changeDuration(self):
        reservations = self.reservation_controller.get_open_reservation(self.userID)
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
                    "name": reservation.room_id+", with reservation id: "+str(reservation.reservation_id)+", start on: "+reservation.reservation_checkin_date+", stay for: "+str(reservation.reservation_stay_date)+" days, price: "+str(self.bill.get_bill(reservation.bill_id).bill_amount)
                }
                for reservation in reservations
            ]
            PROMPTS[PROMPT_KEY["LIST_RESERVATION"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            
            answer:str=self.prompt_and_get_answer(PROMPT_KEY['LIST_RESERVATION'])
            if answer != "Back":
                answerList:List[str] = answer.replace(':', ',').split(',')
                duration=int(self.prompt_and_get_answer(PROMPT_KEY['CHANGE_DURATION']))

                reservationID=answerList[2].strip()
                roomID=answerList[0].strip()
                current_room_type=self.room_controller.get_room(roomID).room_type
                i:int=duration* self.roomType.get_Price(current_room_type)
                PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['message']="The total is "+str(i)
                
                if self.prompt_and_get_answer(PROMPT_KEY['FINAL_CHECK']) =="Continue":
                    self.reservation_controller.modify_reservation_duration(reservationID, duration)
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
        PROMPTS[PROMPT_KEY["FINAL_CHECK"]][0]['choices']=[]
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
