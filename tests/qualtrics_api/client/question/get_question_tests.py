import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class GetBlockTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_get_question_asserts_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_question(None, 'QID1')

    def test_get_question_asserts_question_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_question('survey_id', None)

    def test_get_question_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_question('invalid-format-survey-id', 'QID1')

    def test_get_question_validates_question_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_question('SV_abcdefghijk', 'invalid-format-question-id')

    @responses.activate
    def test_makes_request_as_expected(self):
        question_json = {
            "meta": {
                "httpStatus": "200 - OK",
                "requestId": "54d71b59-615a-4a4e-bc34-45665ca3e122"
            },
            "result": {
                'QID': 'QID1',
                'QuestionText': 'What is love?',
                'DataExportTag': 'Q1',
                'QuestionType': 'MC',
                'Selector': 'SAVR',
                'SubSelector': None,
                'Configuration': {
                    'QuestionDescriptionOption': 'UseText'
                },
                'QuestionDescription': 'respondent_what_is_love_mc',
                'Choices': {
                    '1': 'Baby don\'t hurt me',
                    '2': 'Don\'t hurt me',
                    '3': 'No more'
                },
                'ChoiceOrder': [
                    '1',
                    '2',
                    '3'
                ],
                'Validation': {
                    'Settings': {
                        'ForceResponse': 'OFF',
                        'ForceResponseType': 'OFF',
                        'Type': 'None'
                    }
                },
                'Language': []
            }
        }

        responses.add(
            responses.GET, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghijk/questions/QID1', json=question_json
        )

        response = self.client.get_question('SV_abcdefghijk', 'QID1')

        self.assertEqual(response, question_json)

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        # Set a not found response
        responses.add(
            responses.GET, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghi01/questions/QID1', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            _ = self.client.get_question('SV_abcdefghi01', 'QID1')

        # Replace response with a server error
        responses.add(
            responses.GET, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghi02/questions/QID1', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            _ = self.client.get_question('SV_abcdefghi02', 'QID1')
