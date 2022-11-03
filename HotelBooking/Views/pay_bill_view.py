from HotelBooking.Controllers.bill_controller import BillController
from HotelBooking.Views.view import View
from typing import Tuple, List
from PyInquirer import prompt
from HotelBooking.Models.room import ROOM_TYPE
PROMPT_KEY = {
    "OPERATIONS": 'operations',
    "PAY_BILL": 'pay_bill',
    "LIST_BILL": "list_bill",
    "BACK": "back",
    "FINAL_CHECK": "final_check"
}

PROMPTS = {
    'operations': [{
        'type': 'list',
        'message': "Check Or pay your Bill",
        'name': 'operations',
        'choices': [
        ]
    }],
    'pay_bill': [{
        'type': 'list',
        'message': "Which bill do you want to pay?",
        'name': 'pay_bill',
        'choices': [
        ],
    }],
    'list_bill': [{
        'type': 'list',
        'message': "List Bill:",
        'name': 'list_bill',
        'choices': [
        ],
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


class PayBillView(View):
    bill_controller: BillController
    user_id: str
    start_date: str
    duration: int
    operation_options: List[Tuple[str, str]] = [
        ("Pay another bill", 'pay_bill'),
        ("Back", 'prev_view')
    ]

    def __init__(self, history=[], caller=None, user_id=None, start_date=None, duration=None) -> None:
        super().__init__(history, caller)
        self.initiate_options()
        self.user_id = user_id
        self.start_date = start_date
        self.duration = duration
        self.bill_controller = BillController()

    def show(self):
        self.pay_bill()

    def show_again(self):
        operation = self.prompt_and_get_answer(PROMPT_KEY['OPERATIONS'])
        callable = [operation_obj[1]
                    for operation_obj in self.operation_options if operation_obj[0] == operation].pop()

        getattr(self, callable)()

    def pay_bill(self):

        self.list_bill()
        print("\nWould you like to pay an outstanding bill?\n")
        available_bill = self.bill_controller.get_available_bills(self.user_id)
        if len(available_bill) == 0:
            print("\nThere are no bills\n")
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
                answer_list: List[str] = answer.replace(':', ',').split(',')
                bill_id = answer_list[1].strip()
                self.bill_controller.pay_bill(bill_id)
                print("\nSuccess!\n")
                self.show_again()
            
        self.prev_view()
        

    def list_bill(self):
        print("\nAll bills:\n")
        all_bill = self.bill_controller.get_all_bills(self.user_id)
        for bill in all_bill:
            print("Bill:"+str(bill.bill_id)+", with amount: " +
                str(bill.bill_amount)+" is "+bill.bill_status+"\n")

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