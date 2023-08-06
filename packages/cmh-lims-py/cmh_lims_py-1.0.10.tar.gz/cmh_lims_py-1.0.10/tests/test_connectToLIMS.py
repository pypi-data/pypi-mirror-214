import unittest
from unittest.mock import patch
import pymysql
import connectToLIMS as cl
from your_module import connect_to_lims

class TestConnectToLims(unittest.TestCase):

    @patch('pymysql.connect')
    def test_connect_to_lims(self, mock_connect):
        # Mocking the return values
        expected_config = {
            'host': 'localhost',
            'user': 'your_username',
            'password': 'your_password',
            'database': 'your_database'
        }
        mock_connection = mock_connect.return_value

        # Calling the function
        lims_db = cl.connect_to_lims()

        # Assertions
        mock_connect.assert_called_once_with(**expected_config)
        self.assertEqual(lims_db, mock_connection)

if __name__ == '__main__':
    unittest.main()
