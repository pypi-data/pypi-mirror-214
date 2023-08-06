import unittest
import pymysql
from unittest.mock import patch

# Import the functions to be tested
from cmhlims.getSampleNames import get_sample_names, connect_to_lims

class TestGetSampleNames(unittest.TestCase):

    def test_get_sample_names(self):
        # Create a mock lims_db connection
        mock_lims_db = pymysql.connect()

        # Patch the connect_to_lims function to return the mock lims_db
        with patch('mymodule.connect_to_lims', return_value=mock_lims_db) as mock_connect_to_lims:
            # Patch the cursor() method to return a mock cursor
            with patch.object(mock_lims_db, 'cursor') as mock_cursor:
                # Patch the execute() method to return mock data
                mock_cursor.return_value.fetchall.return_value = [('sample1',), ('sample2',)]

                # Call the function and capture the result
                result = get_sample_names()

        # Assertions
        self.assertEqual(result, ['sample1', 'sample2'])  # Check if the result matches the expected output
        self.assertEqual(mock_connect_to_lims.call_count, 1)  # Check if connect_to_lims is called once
        self.assertEqual(mock_cursor.call_count, 1)  # Check if cursor() is called once
        self.assertEqual(mock_cursor.return_value.execute.call_count, 1)  # Check if execute() is called once

    def tearDown(self):
        # Clean up any mock objects or resources if needed
        pass

class TestConnectToLIMS(unittest.TestCase):

    def test_connect_to_lims(self):
        # Call the function and capture the result
        result = connect_to_lims()

        # Assertions
        self.assertIsInstance(result, pymysql.connections.Connection)  # Check if the return value is an instance of pymysql.connections.Connection

    def tearDown(self):
        # Clean up any resources if needed
        pass

# Run the tests
if __name__ == '__main__':
    unittest.main()

