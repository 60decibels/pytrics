import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class UpdateBlockTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_update_block_asserts_survey_id_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_block(None, 'BL_1234567890a', 'description', 'Standard')

        with self.assertRaises(AssertionError):
            self.client.update_block('', 'BL_1234567890a', 'description', 'Standard')

        with self.assertRaises(AssertionError):
            self.client.update_block(1, 'BL_1234567890a', 'description', 'Standard')

    def test_update_block_asserts_block_id_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_block('SV_1234567890a', None, 'description', 'Standard')

        with self.assertRaises(AssertionError):
            self.client.update_block('SV_1234567890a', [1, 2, 3], 'description', 'Standard')

        with self.assertRaises(AssertionError):
            self.client.update_block('SV_1234567890a', 123.45, 'description', 'Standard')

    def test_update_block_asserts_block_description_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_block('SV_1234567890a', 'BL_1234567890a', '', 'Standard')

        with self.assertRaises(AssertionError):
            self.client.update_block('SV_1234567890a', 'BL_1234567890a', None, 'Standard')

    def test_update_block_asserts_block_type_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_block('SV_1234567890a', 'BL_1234567890a', 'description', None)

        with self.assertRaises(AssertionError):
            self.client.update_block('SV_1234567890a', 'BL_1234567890a', 'description', 'Unsupported_Block_Type')

    def test_update_block_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            self.client.update_block('invalid_survey_id', 'BL_1234567890a', 'description', 'Standard')

    def test_update_block_validates_block_id(self):
        with self.assertRaises(AssertionError):
            self.client.update_block('SV_1234567890a', 'invalid_block_id', 'description', 'Standard')

    @responses.activate
    def test_makes_request_as_expected(self):
        responses.add(
            responses.PUT, 'http://qualtrics.com/api/survey-definitions/SV_1234567890a/blocks/BL_1234567890a'
        )

        try:
            self.client.update_block('SV_1234567890a', 'BL_1234567890a', 'Block Description', 'Standard')

        except AssertionError as ae:
            self.fail("update_block() raised AssertionError unexpectedly: {}".format(ae))

        except Exception as ex: # pylint: disable=broad-except
            self.fail("update_block() raised Exception unexpectedly: {}".format(ex))

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.PUT, 'http://qualtrics.com/api/survey-definitions/SV_1234567890a/blocks/BL_1234567890a', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            self.client.update_block('SV_1234567890a', 'BL_1234567890a', 'I\'m still, i\'m still Jenny from the...', 'Standard')

        responses.replace(
            responses.PUT, 'http://qualtrics.com/api/survey-definitions/SV_1234567890a/blocks/BL_1234567890a', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            self.client.update_block('SV_1234567890a', 'BL_1234567890a', 'Back with another one of those... rocking beats', 'Standard')
