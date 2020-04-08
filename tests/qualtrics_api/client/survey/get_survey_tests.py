import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class GetSurveyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_get_survey_asserts_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_survey(None)

    def test_get_survey_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.get_survey('invalid-format-survey-id')

    @responses.activate
    def test_makes_request_as_expected(self):
        survey_json = {
            'id': 'SV_51PEzLvt33771Mp',
            'name': '19.07.09_Testing Qual Coding',
            'ownerId': 'UR_0v60HMNm5EwZf3T',
            'organizationId': 'singuser159k8vsm',
            'isActive': True,
            'creationDate': '2019-07-09T20:57:29Z',
            'lastModifiedDate': '2019-07-19T14:18:19Z',
            'expiration': {'startDate': None, 'endDate': None},
            'questions': {},
            'exportColumnMap': {},
            'blocks': {},
            'flow': [],
            'embeddedData': [],
            'comments': {},
            'loopAndMerge': {},
            'responseCounts': {'auditable': 9, 'generated': 2, 'deleted': 2}
        }

        responses.add(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_51PEzLvt33771Mp', json=survey_json
        )

        response = self.client.get_survey('SV_51PEzLvt33771Mp')

        self.assertEqual(response, survey_json)

    @responses.activate
    def test_raises_http_error_for_failed_requests(self):
        # Set a not found response
        responses.add(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890a', json={}, status=404
        )
        with self.assertRaises(requests.HTTPError):
            _ = self.client.get_survey('SV_1234567890a')

        # Replace response with a server error
        responses.add(
            responses.GET, 'http://qualtrics.com/api/surveys/SV_1234567890abcde', json={}, status=500
        )
        with self.assertRaises(requests.HTTPError):
            _ = self.client.get_survey('SV_1234567890abcde')
