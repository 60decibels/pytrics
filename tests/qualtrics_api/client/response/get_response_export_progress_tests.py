import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class GetResponseExportProgressTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_get_response_export_progress_asserts_survey_id_and_progress_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_response_export_progress(None, 'progress_id')

        with self.assertRaises(AssertionError):
            _ = self.client.get_response_export_progress('SV_1234567890a', None)

        with self.assertRaises(AssertionError):
            _ = self.client.get_response_export_progress(None, None)

    def test_get_response_export_progress_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_response_export_file('invalid-format-survey-id', 'file_id')

    @responses.activate
    def test_makes_request_as_expected(self):
        in_progress_json = {
            'result': {
                'fileId': None,
                'percentComplete': 50.0,
                'status': 'inProgress'
            },
            'meta': {
                'requestId': '0842cbb3-0a52-4080-aec2-5d831e167c27',
                'httpStatus': '200 - OK'
            }
        }

        responses.add(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses/ES_9yn5UfrKkuuhxA1', json=in_progress_json
        )

        response, _ = self.client.get_response_export_progress('SV_1234567890a', 'ES_9yn5UfrKkuuhxA1')

        self.assertEqual(response, in_progress_json)
        self.assertIsNone(response['result']['fileId'])
        self.assertEqual(response['result']['status'], 'inProgress')

        complete_json = {
            'result': {
                'fileId': '0a52e70b-9dd7-4c88-b5d4-be21f8cc921b',
                'percentComplete': 100.0,
                'status': 'complete'
            },
            'meta': {
                'requestId': '0842cbb3-0a52-4080-aec2-5d831e167c27',
                'httpStatus': '200 - OK'
            }
        }

        responses.replace(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses/ES_9yn5UfrKkuuhxA1', json=complete_json
        )

        response, file_id = self.client.get_response_export_progress('SV_1234567890a', 'ES_9yn5UfrKkuuhxA1')

        self.assertEqual(response, complete_json)
        self.assertEqual(response['result']['fileId'], file_id)
        self.assertEqual(response['result']['percentComplete'], 100.0)

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses/ES_9yn5UfrKkuuhxA1', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.get_response_export_progress('SV_1234567890a', 'ES_9yn5UfrKkuuhxA1')

        responses.replace(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses/ES_9yn5UfrKkuuhxA1', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.get_response_export_progress('SV_1234567890a', 'ES_9yn5UfrKkuuhxA1')
