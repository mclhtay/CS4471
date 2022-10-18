from unittest.mock import patch

from HotelBooking.Controllers.authentication_controller import AuthenticationController
from HotelBooking.Models.administrator import Administrator
from HotelBooking.Models.customer import Customer


class TestAuthenticationController:
    @patch.object(Administrator, "authenticate_admin")
    def test_authenticate_user(self, mock_authenticate_admin):
        mock_id = "test"
        mock_pw = "test"

        controller = AuthenticationController()
        controller.authenticate_admin(mock_id, mock_pw)

        mock_authenticate_admin.assert_called_once_with(
            mock_id, mock_pw)

    @patch.object(Customer, "authenticate_customer")
    def test_authenticate_customer(self, mock_authenticate_customer):
        mock_id = "test"
        mock_pw = "test"

        controller = AuthenticationController()
        controller.authenticate_customer(mock_id, mock_pw)

        mock_authenticate_customer.assert_called_once_with(
            mock_id, mock_pw)
