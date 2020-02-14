import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class CreateResponseExportTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_create_response_export_asserts_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_response_export(None)

    def test_create_response_export_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_response_export('invalid-format-survey-id')

    @responses.activate
    def test_makes_request_as_expected(self):
        response_export_json = {
            'result': {
                'progressId': 'SV_1234567890a',
                'percentComplete': 0.0,
                'status': 'inProgress'
            },
            'meta': {
                'requestId': 'e4c3138f-53bd-4de8-8784-95d23745a8a2',
                'httpStatus': '200 - OK'
            }
        }

        responses.add(
            responses.POST, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses', json=response_export_json
        )

        response, progress_id = self.client.create_response_export('SV_1234567890a')

        self.assertEqual(response, response_export_json)
        self.assertEqual(progress_id, response_export_json['result']['progressId'])

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.POST, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.create_response_export('SV_1234567890a')

        responses.replace(
            responses.POST, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.create_response_export('SV_1234567890a')
