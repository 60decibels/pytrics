# pylint: disable=protected-access
import unittest

from pytrics.qualtrics_api.client import QualtricsAPIClient
from pytrics.common.exceptions import QualtricsAPIException


class BuildHeadersTestCase(unittest.TestCase):

    def test_build_headers_applies_x_api_token_header(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        expected_header_value = 'token-456'

        actual_header_value = client._build_headers('GET')['X-API-TOKEN']

        self.assertEqual(expected_header_value, actual_header_value)

    def test_build_headers_applies_json_content_type_header_for_post_requests(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        expected_header_value = 'application/json'

        actual_header_value = client._build_headers('POST')['Content-Type']

        self.assertEqual(expected_header_value, actual_header_value)

    def test_build_headers_applies_json_content_type_header_for_put_requests(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        expected_header_value = 'application/json'

        actual_header_value = client._build_headers('PUT')['Content-Type']

        self.assertEqual(expected_header_value, actual_header_value)

    def test_build_headers_does_not_apply_json_content_type_header_for_get_requests(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        with self.assertRaises(KeyError):
            _ = client._build_headers('GET')['Content-Type']

    def test_build_headers_does_not_apply_json_content_type_header_for_delete_requests(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        with self.assertRaises(KeyError):
            _ = client._build_headers('DELETE')['Content-Type']

    def test_build_headers_does_not_support_methods_beyond_get_delete_post_and_put(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        with self.assertRaises(QualtricsAPIException):
            _ = client._build_headers('OPTIONS')['Content-Type']

        with self.assertRaises(QualtricsAPIException):
            _ = client._build_headers('HEAD')['Content-Type']

        with self.assertRaises(QualtricsAPIException):
            _ = client._build_headers('CONNECT')['Content-Type']

        with self.assertRaises(QualtricsAPIException):
            _ = client._build_headers('TRACE')['Content-Type']

        with self.assertRaises(QualtricsAPIException):
            _ = client._build_headers('Random-Method-String')['Content-Type']

        with self.assertRaises(QualtricsAPIException):
            _ = client._build_headers(None)['Content-Type']

        with self.assertRaises(QualtricsAPIException):
            _ = client._build_headers(123)['Content-Type']
