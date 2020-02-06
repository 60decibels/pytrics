import unittest
import os

from operations.download import (
    _get_survey_file_path,
    _get_response_file_path,
)


class GetFilePathTestCase(unittest.TestCase):

    def setUp(self):
        self.file_path = os.path.join(os.path.abspath(os.getcwd()), '/data/')

    def test_returns_expected_survey_file_path_for_given_survey_id(self):
        expected = '{}SV_abcdefghijk.json'.format(self.file_path)

        actual = _get_survey_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)

    def test_returns_expected_zipped_response_file_path_for_given_survey_id(self):
        expected = '{}SV_abcdefghijk_responses.zip'.format(self.file_path)

        actual = _get_response_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)

    def test_returns_expected_unzipped_response_file_path_for_given_survey_id(self):
        expected = '{}SV_abcdefghijk_responses.json'.format(self.file_path)

        actual = _get_response_file_path('SV_abcdefghijk', zipped=False)

        self.assertEqual(expected, actual)
