from unittest.mock import patch
from HotelBooking.Models.utils import get_engine


class TestUtils:

    def test_create_engine(self):
        with patch('HotelBooking.Models.utils.create_engine') as mock_create_engine:
            mock_create_engine.return_value = type('Engine', (), {})

            engine = get_engine()

            mock_create_engine.assert_called_once()
