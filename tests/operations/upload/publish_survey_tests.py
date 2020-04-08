import unittest
from unittest.mock import MagicMock, patch

from freezegun import freeze_time
from requests import HTTPError

from pytrics.common.constants import QUALTRICS_API_PUBLISHED_SURVEY_URL_PATTERN
from pytrics.common.exceptions import QualtricsAPIException

from pytrics.operations.upload import publish_survey


class PublishSurveyTestCase(unittest.TestCase):

    def setUp(self):
        get_details_for_client_patch = patch('pytrics.operations.upload.get_details_for_client')
        self.get_details_for_client = get_details_for_client_patch.start()
        self.addCleanup(get_details_for_client_patch.stop)

        self.get_details_for_client.return_value = ('URL', 'TOKEN')

        QualtricsAPIClient_patch = patch('pytrics.operations.upload.QualtricsAPIClient')
        self.QualtricsAPIClient = QualtricsAPIClient_patch.start()
        self.addCleanup(QualtricsAPIClient_patch.stop)

        self.api = MagicMock(base_api_url='URL', auth_token='TOKEN')
        self.QualtricsAPIClient.return_value = self.api

    def test_raises_custom_exception_when_survey_id_params_invalid(self):
        with self.assertRaises(AssertionError):
            publish_survey(None, 'name')

    def test_raises_custom_exception_when_survey_name_param_invalid(self):
        with self.assertRaises(AssertionError):
            publish_survey('SV_1234567890a', None)

    def test_raises_custom_exception_when_api_call_raises_assertion_error(self):
        self.api.publish_survey.side_effect = AssertionError('oh no!')

        with self.assertRaises(QualtricsAPIException):
            publish_survey('SV_1234567890a', 'name')

    def test_raises_custom_exception_when_api_call_raises_http_error(self):
        self.api.publish_survey.side_effect = HTTPError(MagicMock(status=503), 'internal server error')

        with self.assertRaises(QualtricsAPIException):
            publish_survey('SV_1234567890a', 'name')

    @freeze_time('2019-10-11 12:01:02')
    def test_activates_and_publishes_survey_as_expected(self):
        self.api.publish_survey.return_value = ('version-id', 1, '2019-10-11T12:01:02',)

        expected_description = 'name_2019-10-11_12.01.02PM'
        expected_url = QUALTRICS_API_PUBLISHED_SURVEY_URL_PATTERN.format('SV_1234567890a')

        actual_url, version_id, version_number, creation_date = publish_survey('SV_1234567890a', 'name')

        self.assertEqual(expected_url, actual_url)
        self.assertEqual(version_id, 'version-id')
        self.assertEqual(version_number, 1)
        self.assertEqual(creation_date, '2019-10-11T12:01:02')

        self.api.update_survey.assert_called_with('SV_1234567890a', True)

        self.api.publish_survey.assert_called_with('SV_1234567890a', expected_description)
