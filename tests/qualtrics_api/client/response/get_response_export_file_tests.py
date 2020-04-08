import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class GetResponseExportFileTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_get_response_export_file_asserts_survey_id_and_file_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_response_export_file(None, 'file_id')

        with self.assertRaises(AssertionError):
            _ = self.client.get_response_export_file('SV_1234567890a', None)

        with self.assertRaises(AssertionError):
            _ = self.client.get_response_export_file(None, None)

    def test_get_response_export_file_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_response_export_file('invalid-format-survey-id', 'file_id')

    @responses.activate
    def test_makes_request_as_expected(self):
        file_bytes = bytes('Lorem ipsum dolor sit amet', 'utf-8')

        responses.add(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses/file-0987/file', body=file_bytes
        )

        response = self.client.get_response_export_file('SV_1234567890a', 'file-0987')

        self.assertEqual(response, file_bytes)

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses/file-0987/file', body='', status=404, json={'error': 'oh noes!'}
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.get_response_export_file('SV_1234567890a', 'file-0987')

        responses.replace(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890a/export-responses/file-0987/file', body='', status=500, json={'error': 'oh noes!'}
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.get_response_export_file('SV_1234567890a', 'file-0987')
