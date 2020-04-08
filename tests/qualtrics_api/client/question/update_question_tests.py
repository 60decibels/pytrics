import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class UpdateQuestionTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')
        self.question_payload = {
            'QuestionText': 'What is love?',
            'DataExportTag': 'Q1',
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'SubSelector': 'TX',
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

    def test_update_question_asserts_survey_id_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_question(None, 'QID1', {})

        with self.assertRaises(AssertionError):
            self.client.update_question('', 'QID1', {})

        with self.assertRaises(AssertionError):
            self.client.update_question(1, 'QID1', {})

    def test_update_question_asserts_question_id_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_question('SV_1234567890a', None, {})

        with self.assertRaises(AssertionError):
            self.client.update_question('SV_1234567890a', [1, 2, 3], {})

        with self.assertRaises(AssertionError):
            self.client.update_question('SV_1234567890a', 123.45, {})

    def test_update_question_asserts_question_payload_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_question('SV_1234567890a', 'QID1', None)

        with self.assertRaises(AssertionError):
            self.client.update_question('SV_1234567890a', 'QID1', [])

    def test_update_question_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            self.client.update_question('invalid_survey_id', 'QID1', {})

    def test_update_question_validates_question_id(self):
        with self.assertRaises(AssertionError):
            self.client.update_question('SV_1234567890a', 'invalid_question_id', {})

    def test_update_question_validates_question_payload_parameter(self):
        payload_without_question_text_key = self.question_payload
        payload_without_question_text_key.pop('QuestionText')

        with self.assertRaises(AssertionError):
            self.client.update_question('SV_abcdefghijk', 'QID1', payload_without_question_text_key)

        with self.assertRaises(AssertionError):
            self.client.update_question('SV_abcdefghijk', 'QID1', {})

    @responses.activate
    def test_makes_request_as_expected(self):
        update_question_json = {
            'meta': {
                'requestId': '82997a4-9493-41e1-be49-6f02e5afbb42',
                'httpStatus': '200 - OK'
            }
        }

        responses.add(
            responses.PUT, 'http://qualtrics.com/api/survey-definitions/SV_1234567890a/questions/QID1', json=update_question_json
        )

        try:
            self.client.update_question('SV_1234567890a', 'QID1', self.question_payload)

        except AssertionError as ae:
            self.fail("update_question() raised AssertionError unexpectedly: {}".format(ae))

        except Exception as ex: # pylint: disable=broad-except
            self.fail("update_question() raised Exception unexpectedly: {}".format(ex))

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.PUT, 'http://qualtrics.com/api/survey-definitions/SV_1234567890a/questions/QID1', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            self.client.update_question('SV_1234567890a', 'QID1', self.question_payload)

        responses.replace(
            responses.PUT, 'http://qualtrics.com/api/survey-definitions/SV_1234567890a/questions/QID1', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            self.client.update_question('SV_1234567890a', 'QID1', self.question_payload)
