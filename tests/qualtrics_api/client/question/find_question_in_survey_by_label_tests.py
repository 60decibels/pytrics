import unittest
from unittest.mock import MagicMock

import os
import json

from pytrics.qualtrics_api.client import QualtricsAPIClient


class FindQuestionInSurveyJsonTestCase(unittest.TestCase):
    def setUp(self):
        self.example_survey_as_json = None

        example_survey_json_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.', 'example_survey.json')

        with open(example_survey_json_file_path) as survey_json_file:
            self.example_survey_as_json = json.loads(survey_json_file.read())

        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        self.client.get_survey = MagicMock()
        self.client.get_survey.return_value = self.example_survey_as_json

    def test_finds_question_in_survey_by_label_when_present(self):
        expected_id = 'QID1'
        expected_dict = {
            'questionType': {
                'type': 'MC',
                'selector': 'NPS',
                'subSelector': None
            },
            'questionText': 'On a scale of 0-10, how likely are you to recommend [COMPANY] to a friend or family member, where 0 is not at all likely and 10 is extremely likely?',
            'questionLabel': 'nps_company_rating',
            'validation': {
                'doesForceResponse': False,
                'doesRequestResponse': True
            },
            'questionName': 'Q1',
            'choices': {
                '0': {},
                '1': {},
                '2': {},
                '3': {},
                '4': {},
                '5': {},
                '6': {},
                '7': {},
                '8': {},
                '9': {},
                '10': {}
            }
        } # Note that 'choices' has been simplified for this test case, see json file for full shape of this data

        actual_id, actual_dict = self.client.find_question_in_survey_by_label('SV_b9JZIZmEZ11t6D3', 'nps_company_rating')

        self.assertEqual(expected_id, actual_id)
        self.assertCountEqual(expected_dict['questionType'], actual_dict['questionType'])
        self.assertCountEqual(expected_dict['questionText'], actual_dict['questionText'])

    def test_returns_tuple_of_none_and_none_when_question_not_present(self):
        expected = (None, None,)

        actual = self.client.find_question_in_survey_by_label('SV_b9JZIZmEZ11t6D3', 'non_existent_label')

        self.assertEqual(expected, actual)
