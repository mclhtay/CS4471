from HotelBooking.Views.authentication_view import AuthenticationView
from HotelBooking.Views.utils import big_print


if __name__ == "__main__":
    big_print("HOTEL BOOKING")
    AuthenticationView().show()
