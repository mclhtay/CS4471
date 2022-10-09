from HotelBooking.Controllers.controller import Controller
from HotelBooking.Models.administrator import Administrator


class AuthenticationController(Controller):
    administrator: Administrator

    def __init__(self):
        super().__init__()
        self.administrator = Administrator()

    def authenticate_admin(self, id: str, password: str) -> bool:
        return self.administrator.authenticate_admin(id, password)
