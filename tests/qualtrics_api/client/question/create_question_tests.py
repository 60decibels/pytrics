import unittest
from datetime import datetime

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class CreateBlockTestCase(unittest.TestCase):

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

    def test_create_question_asserts_survey_id_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_question(None, self.question_payload)

        with self.assertRaises(AssertionError):
            _ = self.client.create_question('', self.question_payload)

        with self.assertRaises(AssertionError):
            _ = self.client.create_question(1, self.question_payload)

    def test_create_question_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            self.client.create_question('invalid_survey_id', self.question_payload)

    def test_create_question_asserts_question_payload_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_question('SV_abcdefghijk', None)

        with self.assertRaises(AssertionError):
            _ = self.client.create_question('SV_abcdefghijk', datetime(2019, 8, 16))

        with self.assertRaises(AssertionError):
            _ = self.client.create_question('SV_abcdefghijk', ['a', 'b'])

    def test_create_question_validates_question_payload_parameter(self):
        payload_without_question_text_key = self.question_payload
        payload_without_question_text_key.pop('QuestionText')

        with self.assertRaises(AssertionError):
            _ = self.client.create_question('SV_abcdefghijk', payload_without_question_text_key)

        with self.assertRaises(AssertionError):
            _ = self.client.create_question('SV_abcdefghijk', {})

    def test_create_question_asserts_optional_block_id_is_string_if_supplied(self):
        with self.assertRaises(AssertionError):
            self.client.create_question('SV_1234567890a', self.question_payload, block_id=123)

    def test_create_question_validates_optional_block_id_if_supplied(self):
        with self.assertRaises(AssertionError):
            self.client.create_question('SV_1234567890a', self.question_payload, block_id='invalid_block_id')

    @responses.activate
    def test_makes_request_as_expected(self):
        create_question_json = {
            'result': {
                'QuestionID': 'QID1'
            },
            'meta': {
                'requestId': 'be14851c-7d92-4b1c-a541-a9e03228b15e',
                'httpStatus': '200 - OK'
            }
        }

        responses.add(
            responses.POST, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghijk/questions?blockId=BL_1234567890a', json=create_question_json
        )

        result, question_id = self.client.create_question('SV_abcdefghijk', self.question_payload, block_id='BL_1234567890a')

        self.assertEqual(result, create_question_json)
        self.assertEqual(question_id, create_question_json['result']['QuestionID'])

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.POST, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghijk/questions', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.create_question('SV_abcdefghijk', self.question_payload)

        responses.replace(
            responses.POST, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghijk/questions', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.create_question('SV_abcdefghijk', self.question_payload)
