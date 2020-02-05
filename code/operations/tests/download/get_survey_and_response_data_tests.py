import unittest
from unittest.mock import MagicMock, patch, call

from common.exceptions import (
    QualtricsAPIException,
    QualtricsDataSerialisationException,
)

from operations.download import get_survey_and_response_data


class GetSurveyAndResponseDataTestCase(unittest.TestCase):

    def setUp(self):
        get_details_for_client_patch = patch('operations.download.get_details_for_client')
        self.get_details_for_client = get_details_for_client_patch.start()
        self.addCleanup(get_details_for_client_patch.stop)

        self.get_details_for_client.return_value = ('URL', 'TOKEN')

        save_survey_to_s3_patch = patch('operations.download.save_survey_to_s3')
        self.save_survey_to_s3 = save_survey_to_s3_patch.start()
        self.addCleanup(save_survey_to_s3_patch.stop)

        save_responses_to_s3_patch = patch('operations.download.save_responses_to_s3')
        self.save_responses_to_s3 = save_responses_to_s3_patch.start()
        self.addCleanup(save_responses_to_s3_patch.stop)

        _unzip_response_file_patch = patch('operations.download._unzip_response_file')
        self._unzip_response_file = _unzip_response_file_patch.start()
        self.addCleanup(_unzip_response_file_patch.stop)

        QualtricsAPIClient_patch = patch('operations.download.QualtricsAPIClient')
        self.QualtricsAPIClient = QualtricsAPIClient_patch.start()
        self.addCleanup(QualtricsAPIClient_patch.stop)

        self.api = MagicMock(base_api_url='URL', auth_token='TOKEN')
        self.QualtricsAPIClient.return_value = self.api

        logger_patch = patch('operations.download.logger')
        self.logger = logger_patch.start()
        self.addCleanup(logger_patch.stop)

    def test_calls_expected_functions_when_successful(self):
        # run the function
        get_survey_and_response_data('SV_abcdefghijk')

        # assert expected calls made by internal logic of function
        self.get_details_for_client.assert_called_once()

        self.save_survey_to_s3.assert_called_once_with(self.api, 'SV_abcdefghijk')

        self.save_responses_to_s3.assert_called_once_with(self.api, 'SV_abcdefghijk')

        self._unzip_response_file.assert_called_once_with('SV_abcdefghijk')

        logger_calls = [
            call('Qualtrics API client ready'),
            call('Survey data for %s uploaded to s3', 'SV_abcdefghijk'),
            call('Response data .zip for %s uploaded to s3', 'SV_abcdefghijk'),
            call('Response data .json for %s uploaded to s3', 'SV_abcdefghijk'),
        ]

        self.logger.info.assert_has_calls(logger_calls)

    def test_raises_exception_when_save_survey_to_s3_raises_api_error(self):
        # tell our patch to raise an Exception
        self.save_survey_to_s3.side_effect = [
            QualtricsAPIException,
        ]

        # assert expected exception type raised
        with self.assertRaises(QualtricsAPIException):
            get_survey_and_response_data('SV_abcdefghijk')

    def test_raises_exception_when_save_survey_to_s3_raises_serialisation_error(self):
        # tell our patch to raise an Exception
        self.save_survey_to_s3.side_effect = [
            QualtricsDataSerialisationException,
        ]

        # assert expected exception type raised
        with self.assertRaises(QualtricsDataSerialisationException):
            get_survey_and_response_data('SV_abcdefghijk')

    def test_raises_exception_when_save_responses_to_s3_raises_serialisation_error(self):
        # tell our patch to raise an Exception
        self.save_responses_to_s3.side_effect = [
            QualtricsDataSerialisationException,
        ]

        # assert expected exception type raised
        with self.assertRaises(QualtricsDataSerialisationException):
            get_survey_and_response_data('SV_abcdefghijk')

    def test_raises_exception_when__unzip_response_file_raises_serialisation_error(self):
        # tell our patch to raise an Exception
        self._unzip_response_file.side_effect = [
            QualtricsDataSerialisationException,
        ]

        # assert expected exception type raised
        with self.assertRaises(QualtricsDataSerialisationException):
            get_survey_and_response_data('SV_abcdefghijk')
