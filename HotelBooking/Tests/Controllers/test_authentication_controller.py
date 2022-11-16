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
    
    @patch.object(Customer, "customer_exists")
    def test_customer_exists(self, mock_customer_exists):
        mock_id = "test"

        controller = AuthenticationController()
        controller.customer_exists(mock_id)

        mock_customer_exists.assert_called_once_with(mock_id)

    @patch.object(Customer, "create_customer")
    def test_create_customer(self, mock_create_customer):
        customer_id="username1"
        customer_password="mypass"
        customer_name="Jane Doe"
        customer_address= "123 Western Rd"
        customer_cell_number=1234567890
        customer_credit_card_number = 134212

        controller = AuthenticationController()
        controller.create_customer(customer_id, customer_password, customer_name, customer_address, customer_cell_number, customer_credit_card_number)
        mock_create_customer.assert_called_once_with(customer_id, customer_password, customer_name, customer_address, customer_cell_number, customer_credit_card_number)
