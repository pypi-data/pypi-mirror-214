import unittest
import pymysql
import pandas as pd
from unittest.mock import patch

# Import the functions to be tested
from cmhlims.getAnalysisFiles import get_analysis_files, connect_to_lims

class TestGetAnalysisFiles(unittest.TestCase):

    def test_get_analysis_files(self):
        # Create analysis IDs
        analysis_ids = [1, 2, 3]

        # Create a mock db_con connection
        mock_db_con = pymysql.connect()

        # Patch the connect_to_lims function to return the mock db_con
        with patch('mymodule.connect_to_lims', return_value=mock_db_con) as mock_connect_to_lims:
            # Patch the cursor() method to return a mock cursor
            with patch.object(mock_db_con, 'cursor') as mock_cursor:
                # Patch the execute() method to return mock data
                mock_cursor.return_value.fetchall.return_value = [('/path/to/file1', 1, 'label1', 'abbrev1'), 
                                                                 ('/path/to/file2', 2, 'label2', 'abbrev2'), 
                                                                 ('/path/to/file3', 3, 'label3', 'abbrev3')]
                mock_cursor.description = [('file_path',), ('analysis_id',), ('file_type_label',), ('file_type_abbrev',)]

                # Call the function and capture the result
                result = get_analysis_files(analysis_ids)

        # Assertions
        expected_columns = ['file_path', 'analysis_id', 'file_type_label', 'file_type_abbrev']
        expected_data = [('/path/to/file1', 1, 'label1', 'abbrev1'), 
                         ('/path/to/file2', 2, 'label2', 'abbrev2'), 
                         ('/path/to/file3', 3, 'label3', 'abbrev3')]
        expected_df = pd.DataFrame(expected_data, columns=expected_columns)
        pd.testing.assert_frame_equal(result, expected_df)  # Check if the result matches the expected DataFrame
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

