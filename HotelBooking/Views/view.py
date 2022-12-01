from __future__ import annotations
from typing import Tuple, List
from sys import exit
from HotelBooking.Views.utils import big_print


class View:
    view_options: List[Tuple[str, View]]
    operation_options: List[Tuple[str, str]]
    parent_view: View
    history: List[View]

    def __init__(self, history: List[View] = [], caller: View = None) -> None:
        self.history = history
        if caller != None:
            # Append caller to history stack
            self.history.append(caller)

    def prev_view(self) -> None:
        """
        inheriting caller history as a stack, pop caller and show to trace back to 
        previous view
        """
        prev = self.history.pop()
        prev.show()

    def next_view(self, next: View) -> None:
        next(self.history, self).show()

    def quit_system(self) -> None:
        big_print("Good Bye!")
        exit()

    def show(self) -> None:
        pass

    def initiate_options(self) -> None:
        pass

    def prompt_and_get_answer(self) -> None:
        pass
