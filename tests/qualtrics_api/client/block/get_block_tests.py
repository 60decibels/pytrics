import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class GetBlockTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_get_block_asserts_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_block(None, 'block_id')

    def test_get_block_asserts_block_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_block('survey_id', None)

    def test_get_block_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_block('invalid-format-survey-id', 'BL_abcdefghijk')

    def test_get_block_validates_block_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_block('SV_abcdefghijk', 'invalid-format-block-id')

    @responses.activate
    def test_makes_request_as_expected(self):
        block_json = {
            "meta": {
                "httpStatus": "200 - OK",
                "requestId": "54d71b59-615a-4a4e-bc34-45665ca3e122"
            },
            "result": {
                "Type": "Default",
                "Description": "NPS Block",
                "ID": "BL_8BOLx7IFtYLKJyB",
                "BlockElements": [],
                "Options": {
                    "BlockLocking": "false",
                    "RandomizeQuestions": "false",
                    "BlockVisibility": "Expanded"
                }
            }
        }

        responses.add(
            responses.GET, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghijk/blocks/BL_abcdefghijk', json=block_json
        )

        response = self.client.get_block('SV_abcdefghijk', 'BL_abcdefghijk')

        self.assertEqual(response, block_json)

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        # Set a not found response
        responses.add(
            responses.GET, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghi01/blocks/BL_abcdefghi01', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            _ = self.client.get_block('SV_abcdefghi01', 'BL_abcdefghi01')

        # Replace response with a server error
        responses.add(
            responses.GET, 'http://qualtrics.com/api/survey-definitions/SV_abcdefghi02/blocks/BL_abcdefghi02', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            _ = self.client.get_block('SV_abcdefghi02', 'BL_abcdefghi02')
