import unittest
import pymysql
import pandas as pd
from unittest.mock import patch

# Import the functions to be tested
from cmhlims.getAnalysis import get_analyses, connect_to_lims

class TestGetAnalyses(unittest.TestCase):

    def test_get_analyses(self):
        # Create sample names and reference genome
        sample_names = ['sample1', 'sample2']
        reference_genome = ['ref1']

        # Create a mock lims_db connection
        mock_lims_db = pymysql.connect()

        # Patch the connect_to_lims function to return the mock lims_db
        with patch('mymodule.connect_to_lims', return_value=mock_lims_db) as mock_connect_to_lims:
            # Patch the cursor() method to return a mock cursor
            with patch.object(mock_lims_db, 'cursor') as mock_cursor:
                # Patch the execute() method to return mock data
                mock_cursor.return_value.fetchall.return_value = [('sample1', 1, 'analysis1', '/path/to/analysis1', '2023-01-01', 'type1', 'analysis_type1', 'ref1'), 
                                                                 ('sample2', 2, 'analysis2', '/path/to/analysis2', '2023-01-02', 'type2', 'analysis_type2', 'ref1')]
                mock_cursor.description = [('sample_name',), ('analysis_id',), ('analysis_name',), ('analysis_dir',), 
                                           ('analysis_date',), ('sequence_type',), ('analysis_type',), ('reference_genome',)]

                # Call the function and capture the result
                result = get_analyses(sample_names, reference_genome)

        # Assertions
        expected_columns = ['sample_name', 'analysis_id', 'analysis_name', 'analysis_dir', 'analysis_date', 'sequence_type', 'analysis_type', 'reference_genome']
        expected_data = [('sample1', 1, 'analysis1', '/path/to/analysis1', '2023-01-01', 'type1', 'analysis_type1', 'ref1'), 
                         ('sample2', 2, 'analysis2', '/path/to/analysis2', '2023-01-02', 'type2', 'analysis_type2', 'ref1')]
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

