import unittest
from unittest.mock import MagicMock, patch, call

from freezegun import freeze_time
from requests import HTTPError

from common.constants import QUALTRICS_API_PUBLISHED_SURVEY_URL_PATTERN
from common.exceptions import QualtricsAPIException

from qualtrics_api.operations.upload import publish_survey


class PublishSurveyTestCase(unittest.TestCase):

    def setUp(self):
        logger_patch = patch('qualtrics_api.operations.upload.logger')
        self.logger = logger_patch.start()
        self.addCleanup(logger_patch.stop)

        get_details_for_client_patch = patch('qualtrics_api.operations.upload.get_details_for_client')
        self.get_details_for_client = get_details_for_client_patch.start()
        self.addCleanup(get_details_for_client_patch.stop)

        self.get_details_for_client.return_value = ('URL', 'TOKEN')

        QualtricsAPIClient_patch = patch('qualtrics_api.operations.upload.QualtricsAPIClient')
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

        logger_calls = [
            call('Publishing survey with survey_id: %s and description: %s', 'SV_1234567890a', expected_description),
            call('Published survey: %s on: %s, with version_id: %s and version_number: %s Available at URL: %s', 'SV_1234567890a', '2019-10-11T12:01:02', 'version-id', 1, expected_url),
        ]

        actual_url = publish_survey('SV_1234567890a', 'name')

        self.assertEqual(expected_url, actual_url)

        self.logger.info.assert_has_calls(logger_calls, any_order=True)

        self.api.update_survey.assert_called_with('SV_1234567890a', True)

        self.api.publish_survey.assert_called_with('SV_1234567890a', expected_description)
