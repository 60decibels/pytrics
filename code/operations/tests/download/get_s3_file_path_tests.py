import unittest
from unittest.mock import patch

from qualtrics_api.operations.download import (
    _get_s3_survey_file_path,
    _get_s3_response_file_path,
)


class GetS3FilePathTestCase(unittest.TestCase):

    def setUp(self):
        _get_profile_patch = patch('qualtrics_api.operations.download._get_profile')
        self._get_profile = _get_profile_patch.start()
        self.addCleanup(_get_profile_patch.stop)

        self._get_profile.return_value = 'testing'

    def test_returns_expected_survey_file_path_for_given_survey_id(self):
        expected = 'testing/response/qualtrics/new/SV_abcdefghijk.json'

        actual = _get_s3_survey_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)

    def test_returns_expected_zipped_response_file_path_for_given_survey_id(self):
        expected = 'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip'

        actual = _get_s3_response_file_path('SV_abcdefghijk')

        self.assertEqual(expected, actual)

    def test_returns_expected_unzipped_response_file_path_for_given_survey_id(self):
        expected = 'testing/response/qualtrics/new/SV_abcdefghijk_responses.json'

        actual = _get_s3_response_file_path('SV_abcdefghijk', zipped=False)

        self.assertEqual(expected, actual)
