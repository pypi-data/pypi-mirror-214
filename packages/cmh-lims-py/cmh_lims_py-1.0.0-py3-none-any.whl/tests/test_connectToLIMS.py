import unittest
import yaml
from unittest.mock import patch
from pymysql import connect

# Import the function to be tested
from cmhlims.connectToLIMS import connect_to_lims

class TestConnectToLIMS(unittest.TestCase):

    def test_connect_to_lims_valid_config(self):
        # Define the mock lims_config
        mock_lims_config = {
            'production': {
                'username': 'lims_lab@test-gmc-mysql-private-01',
                'password': '@Gajz2lvc^yulW3H',
                'host': 'test-gmc-mysql-private-01.mysql.database.azure.com',
                'database': 'lims_test',
                'sslca': '/Users/mkumar1/Desktop/cmhlims_py/combined.pem'
            }
        }

        # Save the mock lims_config to a temporary YAML file
        with open('mock_lims_config.yaml', 'w') as file:
            yaml.dump(mock_lims_config, file)
            print(mock_lims_config)

        db_con = connect_to_lims(config='mock_lims_config.yaml', environment='production')
        # Call the function with the mock config and environment
        #with patch('pymysql.connect', return_value=connect()) as mock_connect:
        #    db_con = connect_to_lims(config='mock_lims_config.yaml', environment='production')
            #print(db_con)

        # Assertions
        self.assertIsInstance(db_con, connect)  # Check if the return value is an instance of pymysql.connect
        #self.assertEqual(mock_connect.call_count, 1)  # Check if pymysql.connect is called once
        #self.assertEqual(mock_connect.call_args[1]['user'], 'test_user')  # Check if the correct username is used
        #self.assertEqual(mock_connect.call_args[1]['password'], 'test_password')  # Check if the correct password is used
        #self.assertEqual(mock_connect.call_args[1]['host'], 'test_host')  # Check if the correct host is used
        #self.assertEqual(mock_connect.call_args[1]['database'], 'test_database')  # Check if the correct database is used
        #self.assertEqual(mock_connect.call_args[1]['ssl']['ca'], 'test_sslca')  # Check if the correct sslca is used

'''
    def test_connect_to_lims_missing_config(self):
        # Call the function without specifying the config and environment
        with self.assertRaises(ValueError):
            connect_to_lims()

    def test_connect_to_lims_invalid_environment(self):
        # Define the mock lims_config
        mock_lims_config =  {
            'production': {
                'username': 'lims_lab@test-gmc-mysql-private-01',
                'password': '@Gajz2lvc^yulW3H',
                'host': 'test-gmc-mysql-private-01.mysql.database.azure.com',
                'database': 'lims_test',
                'sslca': '/software/lims/combined.pem'
            }
        }

        # Save the mock lims_config to a temporary YAML file
        with open('mock_lims_config_v2.yaml', 'w') as file:
            yaml.dump(mock_lims_config, file)

        # Call the function with an invalid environment
        with self.assertRaises(ValueError):
            connect_to_lims(config='mock_lims_config_v2.yaml', environment='invalid_environment')

    def tearDown(self):
        # Clean up the temporary YAML file
        import os
        #if os.path.exists('mock_lims_config.yaml'):
        #    os.remove('mock_lims_config.yaml')
'''
# Run the tests
if __name__ == '__main__':
    unittest.main()

