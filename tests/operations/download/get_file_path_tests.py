import unittest
from unittest.mock import patch

from pytrics.operations.download import (
    _get_survey_file_path,
    _get_response_file_path,
    _get_processed_response_file_path,
)


class GetFilePathTestCase(unittest.TestCase):

    @patch('pytrics.operations.download.os.path.abspath')
    def test_returns_expected_survey_file_path_for_given_survey_id(self, mock_abspath):
        mock_abspath.return_value = '/testing'

        expected = '/testing/../data/SV_abcdefghijk.json'

        actual = _get_survey_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)

    @patch('pytrics.operations.download.os.path.abspath')
    def test_returns_expected_zipped_response_file_path_for_given_survey_id(self, mock_abspath):
        mock_abspath.return_value = '/testing'

        expected = '/testing/../data/SV_abcdefghijk_responses.zip'

        actual = _get_response_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)

    @patch('pytrics.operations.download.os.path.abspath')
    def test_returns_expected_unzipped_response_file_path_for_given_survey_id(self, mock_abspath):
        mock_abspath.return_value = '/testing'

        expected = '/testing/../data/SV_abcdefghijk_responses.json'

        actual = _get_response_file_path('SV_abcdefghijk', zipped=False)

        self.assertEqual(expected, actual)

    @patch('pytrics.operations.download.os.path.abspath')
    def test_returns_expected_processed_response_file_path_for_given_survey_id(self, mock_abspath):
        mock_abspath.return_value = '/testing'

        expected = '/testing/../data/SV_abcdefghijk_responses_processed.json'

        actual = _get_processed_response_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)
