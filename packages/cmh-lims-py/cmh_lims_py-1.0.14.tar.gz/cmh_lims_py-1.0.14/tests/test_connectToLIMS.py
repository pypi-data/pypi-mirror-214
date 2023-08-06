import unittest
from unittest.mock import patch
from cmhlims.connectToLIMS import connect_to_lims

class TestConnectToLims(unittest.TestCase):

    @patch('pymysql.connect')
    def test_connect_to_lims(self, mock_connect):
        # Mocking the return values
        expected_config = {
            'host': 'test-gmc-mysql-private-01.mysql.database.azure.com',
            'user': 'lims_lab@test-gmc-mysql-private-01',
            'password': '@Gajz2lvc^yulW3H',
            'database': 'lims_test',
            'ssl_ca' : 'combined.pem',
            'autocommit' : True
        }
        mock_connection = mock_connect.return_value
        print(mock_connection)
        # Calling the function
        lims_db = connect_to_lims()

        # Assertions
        mock_connect.assert_called_once_with(**expected_config)
        self.assertEqual(lims_db, mock_connection)

if __name__ == '__main__':
    unittest.main()
