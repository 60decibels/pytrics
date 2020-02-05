import unittest

from operations.download import (
    _get_survey_file_path,
    _get_response_file_path,
)


class GetFilePathTestCase(unittest.TestCase):

    def test_returns_expected_survey_file_path_for_given_survey_id(self):
        expected = 'json/SV_abcdefghijk.json'

        actual = _get_survey_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)

    def test_returns_expected_zipped_response_file_path_for_given_survey_id(self):
        expected = 'json/SV_abcdefghijk_responses.zip'

        actual = _get_response_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)

    def test_returns_expected_unzipped_response_file_path_for_given_survey_id(self):
        expected = 'json/SV_abcdefghijk_responses.json'

        actual = _get_response_file_path('SV_abcdefghijk', zipped=False)

        self.assertEqual(expected, actual)
