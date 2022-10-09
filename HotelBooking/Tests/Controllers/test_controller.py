from HotelBooking.Controllers.controller import Controller


class TestController:
    def test_construct(self):
        controller = Controller()

        assert type(controller) == Controller
