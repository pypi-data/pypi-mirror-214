import unittest
from unittest.mock import patch
import pandas as pd
import pymysql
from cmhlims.getAnalysis import get_analyses


class TestGetAnalyses(unittest.TestCase):

    @patch('cmhlims.connectToLIMS.connect_to_lims')
    @patch.object(pymysql.cursors.Cursor, 'execute')
    @patch.object(pymysql.connections.Connection, '__enter__')
    @patch.object(pymysql.connections.Connection, '__exit__')
    def test_get_analyses(self, mock_exit, mock_enter,  mock_execute, mock_connect_to_lims):
        # Mocking the return values
        sample_names = ['sample1', 'sample2']
        reference_genome = ['ref_genome']

        # Mocking the result of the SQL query
        query_result = [
            ('sample1', 1, 'analysis1', 'dir1', '2022-01-01', 'sequence_type1', 'analysis_type1', 'ref_genome'),
            ('sample2', 2, 'analysis2', 'dir2', '2022-01-02', 'sequence_type2', 'analysis_type2', 'ref_genome')
        ]
        mock_execute.return_value = None
        #mock_description.return_value = [('sample_name',), ('analysis_id',), ('analysis_name',), ('analysis_dir',), ('analysis_date',), ('sequence_type',), ('analysis_type',), ('reference_genome',)]
        mock_enter.return_value.__iter__.return_value = query_result

        # Calling the function
        analyses_df = get_analyses(sample_names, reference_genome)
        print(analyses_df)
        print(pd.DataFrame)

        # Assertions
        mock_connect_to_lims.assert_called_once()
        mock_execute.assert_called_once()
        self.assertIsInstance(analyses_df, pd.DataFrame)
        self.assertEqual(len(analyses_df), 2)
        self.assertListEqual(analyses_df.columns.tolist(), ['sample_name', 'analysis_id', 'analysis_name', 'analysis_dir', 'analysis_date', 'sequence_type', 'analysis_type', 'reference_genome'])
        self.assertListEqual(analyses_df['sample_name'].tolist(), ['sample1', 'sample2'])
        self.assertListEqual(analyses_df['analysis_id'].tolist(), [1, 2])

if __name__ == '__main__':
    unittest.main()
