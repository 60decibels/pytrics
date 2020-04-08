import unittest

import responses
import requests

from pytrics.qualtrics_api.client import QualtricsAPIClient


class PublishSurveyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_publish_survey_asserts_survey_id_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.publish_survey(None, 'description')

        with self.assertRaises(AssertionError):
            _ = self.client.publish_survey('', 'description')

        with self.assertRaises(AssertionError):
            _ = self.client.publish_survey(1.23, 'description')

    def test_publish_survey_asserts_description_parameter(self):
        with self.assertRaises(AssertionError):
            _ = self.client.publish_survey('SV_51PEzLvt33771Mp', '')

        with self.assertRaises(AssertionError):
            _ = self.client.publish_survey('SV_51PEzLvt33771Mp', {})

    def test_publish_survey_validates_survey_id(self):
        with self.assertRaises(AssertionError):
            _ = self.client.publish_survey('invalid-format-survey-id', 'description')

    @responses.activate
    def test_makes_request_as_expected(self):
        publish_survey_json = {
            "meta": {
                "httpStatus": "200 - OK",
                "requestId": "7999edd9-a232-4735-ae70-1c8cc7e30e09"
            },
            "result": {
                "metadata": {
                    "surveyID": "SV_51PEzLvt33771Mp",
                    "versionID": "9223370492291465912",
                    "versionNumber": 2,
                    "description": "2019 New Survey Version",
                    "userID": "UR_3fIVFlGaWYcfVml",
                    "creationDate": "2019-27-09T07:48:49Z",
                    "published": True,
                    "wasPublished": True,
                    "publishEvents": [
                        {
                            "date": "2019-26-09T21:21:50Z",
                            "userID": "UR_3fIVFlGaWYcfVml"
                        }
                    ]
                }
            }
        }

        responses.add(
            responses.POST, 'http://qualtrics.com/api/survey-definitions/SV_51PEzLvt33771Mp/versions', json=publish_survey_json
        )

        version_id, version_number, creation_date = self.client.publish_survey('SV_51PEzLvt33771Mp', '2019 v2 of My Survey')

        self.assertEqual(version_id, publish_survey_json['result']['metadata']['versionID'])
        self.assertEqual(version_number, publish_survey_json['result']['metadata']['versionNumber'])
        self.assertEqual(creation_date, publish_survey_json['result']['metadata']['creationDate'])

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
