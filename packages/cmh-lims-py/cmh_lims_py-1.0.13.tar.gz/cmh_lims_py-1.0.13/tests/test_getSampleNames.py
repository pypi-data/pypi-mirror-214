import unittest
from unittest.mock import patch
import pymysql
from cmhlims.getSampleNames import get_sample_names


class TestGetSampleNames(unittest.TestCase):

    @patch('cmhlims.connectToLIMS.connect_to_lims')
    @patch.object(pymysql.cursors.Cursor, 'execute')
    @patch.object(pymysql.cursors.Cursor, 'fetchall')
    @patch.object(pymysql.connections.Connection, '__enter__')
    @patch.object(pymysql.connections.Connection, '__exit__')
    def test_get_sample_names(self, mock_exit, mock_enter, mock_fetchall, mock_execute, mock_connect_to_lims):
        # Mocking the return values
        query_result = [('sample1',), ('sample2',), ('sample3',)]
        mock_execute.return_value = None
        mock_fetchall.return_value = query_result

        # Calling the function
        sample_names = get_sample_names()

        # Assertions
        mock_connect_to_lims.assert_called_once()
        mock_execute.assert_called_once()
        mock_fetchall.assert_called_once()
        self.assertEqual(len(sample_names), 3)
        self.assertListEqual(sample_names, ['sample1', 'sample2', 'sample3'])

if __name__ == '__main__':
    unittest.main()
