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
    "PAY_BILL": 'payBill',
    "LIST_BILL": "listBill",
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
    'payBill': [{
        'type': 'list',
        'message': "Which bill do you want to pay?",
        'name': 'payBill',
        'choices': [
        ],
    }],
    'listBill': [{
        'type': 'list',
        'message': "List Bill:",
        'name': 'listBill',
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


class PayBillView(View):
    reservation_controller: ReservationController
    room_controller: RoomController
    bill_controller: BillController
    userID: str
    startDate: str
    duration: int
    roomType: RoomType
    operation_options: List[Tuple[str, str]] = [
        ("Pay a bill", 'payBill'),
        ("List out all the bills", 'listBill'),
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
        self.bill_controller = BillController()
        self.reservation_controller = ReservationController()

    def show(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()

        getattr(self, callable)()

    def payBill(self):
        available_bill = self.bill_controller.get_available_bill(self.userID)
        if len(available_bill) == 0:
            print("\nThere are no bill\n")
            self.prompt_and_get_answer(PROMPT_KEY['BACK'])

        else:
            PROMPTS[PROMPT_KEY["PAY_BILL"]][0]['choices'] = [
                {
                    "name": "Bill:"+str(bill.bill_id)+", with amount: "+str(bill.bill_amount)+" is unpaid"
                }
                for bill in available_bill
            ]
            PROMPTS[PROMPT_KEY["PAY_BILL"]][0]['choices'].append(
                {
                    "name": "Back"
                }
            )
            answer: str = self.prompt_and_get_answer(PROMPT_KEY['PAY_BILL'])
            if answer != "Back":
                answerList: List[str] = answer.replace(':', ',').split(',')
                billID = answerList[1].strip()
                self.bill_controller.pay_bill(billID)
                print("\nSuccess!\n")
        self.show()

    def listBill(self):
        all_bill = self.bill_controller.get_all_bill(self.userID)
        if len(all_bill) == 0:
            print("\nThere are no bill\n")
            self.prompt_and_get_answer(PROMPT_KEY['BACK'])

        else:
            for bill in all_bill:
                print("Bill:"+str(bill.bill_id)+", with amount: " +
                      str(bill.bill_amount)+" is "+bill.bill_status+"\n")

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
