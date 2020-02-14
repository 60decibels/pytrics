import unittest
from datetime import datetime

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class CreateBlockTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_create_block_asserts_survey_id_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_block(None, 'description', 'Standard')

        with self.assertRaises(AssertionError):
            _ = self.client.create_block('', 'description', 'Standard')

        with self.assertRaises(AssertionError):
            _ = self.client.create_block(1, 'description', 'Standard')

    def test_create_block_asserts_description_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_block('SV_abcdefghijk', datetime(2019, 8, 16), 'Standard')

        with self.assertRaises(AssertionError):
            _ = self.client.create_block('SV_abcdefghijk', [], 'Standard')

        with self.assertRaises(AssertionError):
            _ = self.client.create_block('SV_abcdefghijk', {}, 'Standard')

    def test_create_block_asserts_block_type_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.create_block('SV_abcdefghijk', 'description', 'unsupported-block-type-value')

    @responses.activate
    def test_makes_request_as_expected(self):
        create_block_json = {
            'result': {
                'BlockID': 'BL_abcdefghijk',
                'FlowID': 'FL_1'
            },
            'meta': {
                'requestId': '888a0f7d-1cf7-4eea-8b61-850edfcf409d',
                'httpStatus': '200 - OK'
            }
        }

        responses.add(
            responses.POST, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghijk/blocks', json=create_block_json
        )

        result, block_id = self.client.create_block('SV_abcdefghijk', 'My block description', 'Standard')

        self.assertEqual(result, create_block_json)
        self.assertEqual(block_id, create_block_json['result']['BlockID'])

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.POST, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghijk/blocks', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.create_block('SV_abcdefghijk', 'My block description', 'Standard')

        responses.replace(
            responses.POST, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghijk/blocks', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            _, _ = self.client.create_block('SV_abcdefghijk', 'My block description', 'Standard')
