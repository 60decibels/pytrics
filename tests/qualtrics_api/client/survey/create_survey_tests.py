import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class CreateSurveyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_create_survey_asserts_survey_name_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_survey(None)

        with self.assertRaises(AssertionError):
            _ = self.client.create_survey('')

        with self.assertRaises(AssertionError):
            _ = self.client.create_survey(1)

    def test_create_survey_asserts_language_code_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_survey('Survey Name', language_code='XX')

    def test_create_survey_asserts_project_category_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_survey('Survey Name', project_category='ZZ')

    @responses.activate
    def test_makes_request_as_expected(self):
        create_survey_json = {
            'result': {
                "SurveyID": "SV_sUrV3Y1d",
                "DefaultBlockID": "BL_d3FaUlT8L0cK1d",
            },
            'meta': {
                'requestId': '888a0f7d-1cf7-4eea-8b61-850edfcf409d',
                'httpStatus': '200 - OK'
            }
        }

        responses.add(
            responses.POST, 'http://qualtrics.com/api/survey-definitions', json=create_survey_json
        )

        survey_id, default_block_id = self.client.create_survey('My New Survey Name')

        self.assertEqual(survey_id, create_survey_json['result']['SurveyID'])
        self.assertEqual(default_block_id, create_survey_json['result']['DefaultBlockID'])

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.POST, 'http://qualtrics.com/api/survey-definitions', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.create_survey('400 Survey Name')

        responses.replace(
            responses.POST, 'http://qualtrics.com/api/survey-definitions', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.create_survey('500 Survey Name')
