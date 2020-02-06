import unittest
from unittest.mock import MagicMock, mock_open, patch, call

from common.exceptions import (
    QualtricsAPIException,
    QualtricsDataSerialisationException,
)

from operations.download import save_survey_to_file


class SaveSurveyToS3TestCase(unittest.TestCase): # pylint: disable=too-many-instance-attributes

    def setUp(self):
        self.api = MagicMock()
        self.survey_json = {
            'id': 'SV_abcdefghijk',
            'name': '19.07.09_Testing Qual Coding',
            'isActive': True,
            'creationDate': '2019-07-09T20:57:29Z',
            'questions': {
                'QID1': {
                    'questionType': {
                        'type': 'TE',
                        'selector': 'SL',
                        'subSelector': None
                    },
                    'questionText': 'What is your first name name?',
                    'questionLabel': 'respondent_first_name',
                    'validation': {
                        'doesForceResponse': False
                    },
                    'questionName': 'Q1'
                }
            }
        }
        self.api.get_survey.return_value = self.survey_json

        _get_survey_file_path_patch = patch('operations.download._get_survey_file_path')
        self._get_survey_file_path = _get_survey_file_path_patch.start()
        self.addCleanup(_get_survey_file_path_patch.stop)

        self.file_path_and_name = 'json/SV_abcdefghijk.json'
        self._get_survey_file_path.return_value = self.file_path_and_name

        self.mock_open = open_patch = patch('operations.download.open', new_callable=mock_open(), create=True)
        self.mock_open = open_patch.start()
        self.addCleanup(open_patch.stop)

        self.survey_file = 'survey_file'
        self.mock_open.return_value.__enter__.return_value = self.survey_file

        json_patch = patch('operations.download.json')
        self.json = json_patch.start()
        self.addCleanup(json_patch.stop)

        logger_patch = patch('operations.download.logger')
        self.logger = logger_patch.start()
        self.addCleanup(logger_patch.stop)

    def test_calls_various_functions_as_expected(self):
        # run the function
        save_survey_to_file(self.api, 'SV_abcdefghijk')

        # assert it calls the things we expect it to, with expected args
        self.api.get_survey.assert_called_once_with('SV_abcdefghijk')

        self._get_survey_file_path.assert_called_once_with('SV_abcdefghijk')

        self.json.dump.assert_called_once_with(self.survey_json, self.survey_file)

        self.logger.info.assert_has_calls([
            call('Getting survey %s from API', 'SV_abcdefghijk'),
            call('Saving survey to s3 with key %s', self.file_path_and_name),
        ])

    def test_raises_exception_when_error_encountered_during_open(self):
        # tell our open patch to raise an Exception
        self.mock_open.return_value = Exception

        # assert expected exception type raised
        with self.assertRaises(QualtricsDataSerialisationException):
            save_survey_to_file(self.api, 'SV_abcdefghijk')

        self.logger.error.assert_called_once_with('Error encountered during serialisation of qualtrics survey to s3')

    def test_raises_exception_when_error_encountered_during_get_survey(self):
        # tell our upload patch to raise an Exception
        self.api.get_survey.side_effect = [
            AssertionError
        ]

        # assert expected exception type raised
        with self.assertRaises(QualtricsAPIException):
            save_survey_to_file(self.api, 'SV_abcdefghijk')

        self.logger.error.assert_called_once_with('Error encountered during API call get_survey')
