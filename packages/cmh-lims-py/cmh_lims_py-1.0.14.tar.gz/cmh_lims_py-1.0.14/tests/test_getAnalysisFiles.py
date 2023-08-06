import unittest
from unittest.mock import patch
import pandas as pd
import pymysql
from cmhlims.getAnalysisFiles import get_analysis_files

class TestGetAnalysisFiles(unittest.TestCase):
    '''
    @patch('connectToLIMS.connect_to_lims')
    @patch.object(pymysql.cursors.Cursor, 'execute')
    @patch.object(pymysql.cursors.Cursor, 'description')
    @patch.object(pymysql.connections.Connection, '__enter__')
    @patch.object(pymysql.connections.Connection, '__exit__')
    def test_get_analysis_files(self, mock_exit, mock_enter, mock_description, mock_execute, mock_connect_to_lims):
    '''

    @patch.object(pymysql.cursors.Cursor, 'fetchall')
    def test_get_analysis_files(self, mock_fetchall):
        # Mocking the return values
        analysis_ids = [1, 2]

        # Mocking the result of the SQL query
        query_result = [
            ('file1', 1, 'file_type1', 'abbrev1'),
            ('file2', 2, 'file_type2', 'abbrev2')
        ]
        #mock_execute.return_value = None
        #mock_description.return_value = [('file_path',), ('analysis_id',), ('file_type_label',), ('file_type_abbrev',)]
        #mock_enter.return_value.__iter__.return_value = query_result
        mock_fetchall.return_value = query_result
        # Calling the function
        files_df = get_analysis_files(analysis_ids)
        print(files_df)

        # Assertions
        #mock_connect_to_lims.assert_called_once()
        #mock_execute.assert_called_once()
        self.assertIsInstance(files_df, pd.DataFrame)
        self.assertEqual(len(files_df), 2)
        self.assertListEqual(files_df.columns.tolist(), ['file_path', 'analysis_id', 'file_type_label', 'file_type_abbrev'])
        self.assertListEqual(files_df['file_path'].tolist(), ['file1', 'file2'])
        self.assertListEqual(files_df['analysis_id'].tolist(), [1, 2])

if __name__ == '__main__':
    unittest.main()
