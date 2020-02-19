import unittest
from unittest.mock import MagicMock, patch

from pytrics.common.exceptions import (
    QualtricsAPIException,
    QualtricsDataSerialisationException,
)

from pytrics.operations.download import get_survey_data


class GetSurveyDataTestCase(unittest.TestCase):

    def setUp(self):
        get_details_for_client_patch = patch('pytrics.operations.download.get_details_for_client')
        self.get_details_for_client = get_details_for_client_patch.start()
        self.addCleanup(get_details_for_client_patch.stop)

        self.get_details_for_client.return_value = ('URL', 'TOKEN')

        save_survey_to_file_patch = patch('pytrics.operations.download.save_survey_to_file')
        self.save_survey_to_file = save_survey_to_file_patch.start()
        self.addCleanup(save_survey_to_file_patch.stop)

        QualtricsAPIClient_patch = patch('pytrics.operations.download.QualtricsAPIClient')
        self.QualtricsAPIClient = QualtricsAPIClient_patch.start()
        self.addCleanup(QualtricsAPIClient_patch.stop)

        self.api = MagicMock(base_api_url='URL', auth_token='TOKEN')
        self.QualtricsAPIClient.return_value = self.api

    def test_calls_expected_functions_when_successful(self):
        # run the function
        get_survey_data('SV_abcdefghijk', '/testing')

        # assert expected calls made by internal logic of function
        self.get_details_for_client.assert_called_once()

        self.save_survey_to_file.assert_called_once_with(self.api, 'SV_abcdefghijk', '/testing')

    def test_raises_exception_when_save_survey_to_file_raises_api_error(self):
        # tell our patch to raise an Exception
        self.save_survey_to_file.side_effect = [
            QualtricsAPIException,
        ]

        # assert expected exception type raised
        with self.assertRaises(QualtricsAPIException):
            get_survey_data('SV_abcdefghijk', '/testing')

    def test_raises_exception_when_save_survey_to_file_raises_serialisation_error(self):
        # tell our patch to raise an Exception
        self.save_survey_to_file.side_effect = [
            QualtricsDataSerialisationException,
        ]

        # assert expected exception type raised
        with self.assertRaises(QualtricsDataSerialisationException):
            get_survey_data('SV_abcdefghijk', '/testing')
