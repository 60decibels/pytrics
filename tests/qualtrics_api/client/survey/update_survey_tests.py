import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class UpdateQuestionTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_update_survey_asserts_survey_id_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_survey(None, True)

        with self.assertRaises(AssertionError):
            self.client.update_survey('', True)

        with self.assertRaises(AssertionError):
            self.client.update_survey(1, True)

    def test_update_survey_asserts_is_active_parameter(self):
        with self.assertRaises(AssertionError):
            self.client.update_survey('SV_1234567890a', None)

        with self.assertRaises(AssertionError):
            self.client.update_survey('SV_1234567890a', [1, 2, 3])

        with self.assertRaises(AssertionError):
            self.client.update_survey('SV_1234567890a', 123.45)

        with self.assertRaises(AssertionError):
            self.client.update_survey('SV_1234567890a', {})

    def test_update_survey_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            self.client.update_survey('invalid_survey_id', False)

    @responses.activate
    def test_makes_request_as_expected(self):
        update_survey_json = {
            'meta': {
                'requestId': '82997a4-9493-41e1-be49-6f02e5afbb42',
                'httpStatus': '200 - OK'
            }
        }

        responses.add(
            responses.PUT, 'http://qualtrics.com/api/surveys/SV_1234567890a', json=update_survey_json
        )

        try:
            self.client.update_survey('SV_1234567890a', True)

        except AssertionError as ae:
            self.fail("update_survey() raised AssertionError unexpectedly: {}".format(ae))

        except Exception as ex: # pylint: disable=broad-except
            self.fail("update_survey() raised Exception unexpectedly: {}".format(ex))

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        responses.add(
            responses.PUT, 'http://qualtrics.com/api/surveys/SV_1234567890a', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            self.client.update_survey('SV_1234567890a', False)

        responses.replace(
            responses.PUT, 'http://qualtrics.com/api/surveys/SV_1234567890a', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            self.client.update_survey('SV_1234567890a', False)
