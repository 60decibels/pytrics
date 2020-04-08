import unittest
from datetime import datetime

from pytrics.common.constants import (
    QUALTRICS_API_SUPPORTED_ANSWER_SELECTORS,
    QUALTRICS_API_SUPPORTED_QUESTION_TYPES,
)
from pytrics.qualtrics_api.client import QualtricsAPIClient


class BuildQuestionPayloadTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        self.valid_question_params = {
            'text': 'What is love?',
            'label': 'respondent_what_is_love_mc',
            'type': 'MC',
            'tag_number': 1,
            'answer_selector': 'SAVR',
            'choices': {
                '1': {
                    'Display': 'Baby don\'t hurt me'
                },
                '2': {
                    'Display': 'Don\'t hurt me'
                },
                '3': {
                    'Display': 'No more'
                }
            },
            'choice_order': [1, 2, 3],
            'is_mandatory': False,
            'translations': [],
            'block_number':  1
        }

    def test_asserts_question_params_argument(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_payload(None)

    def test_asserts_question_params_keys_present(self):
        with self.assertRaises(AssertionError):
            params_without_text_key = self.valid_question_params
            params_without_text_key.pop('text')

            self.client.build_question_payload(params_without_text_key)

        with self.assertRaises(AssertionError):
            params_without_is_mandatory_key = self.valid_question_params
            params_without_is_mandatory_key.pop('is_mandatory')

            self.client.build_question_payload(params_without_is_mandatory_key)

    def test_asserts_text_is_non_empty_string(self):
        params_with_changed_text = self.valid_question_params

        with self.assertRaises(AssertionError):
            params_with_changed_text['text'] = ''
            self.client.build_question_payload(params_with_changed_text)

        with self.assertRaises(AssertionError):
            params_with_changed_text['text'] = None
            self.client.build_question_payload(params_with_changed_text)

        with self.assertRaises(AssertionError):
            params_with_changed_text['text'] = 123
            self.client.build_question_payload(params_with_changed_text)

        with self.assertRaises(AssertionError):
            params_with_changed_text['text'] = datetime(2019, 8, 16)
            self.client.build_question_payload(params_with_changed_text)

    def test_asserts_tag_number_is_integer(self):
        params_with_changed_tag_number = self.valid_question_params

        with self.assertRaises(AssertionError):
            params_with_changed_tag_number['tag_number'] = 1.23
            self.client.build_question_payload(params_with_changed_tag_number)

        with self.assertRaises(AssertionError):
            params_with_changed_tag_number['tag_number'] = []
            self.client.build_question_payload(params_with_changed_tag_number)

        with self.assertRaises(AssertionError):
            params_with_changed_tag_number['tag_number'] = {}
            self.client.build_question_payload(params_with_changed_tag_number)

    def test_asserts_type_is_string_and_a_supported_value(self):
        params_with_changed_type = self.valid_question_params

        with self.assertRaises(AssertionError):
            params_with_changed_type['type'] = None
            self.client.build_question_payload(params_with_changed_type)

        with self.assertRaises(AssertionError):
            params_with_changed_type['type'] = 'XX'
            self.client.build_question_payload(params_with_changed_type)

        try:
            params_with_changed_type['type'] = QUALTRICS_API_SUPPORTED_QUESTION_TYPES[0]
            self.client.build_question_payload(params_with_changed_type)
        except AssertionError:
            self.fail("build_question_payload() raised AssertionErrror unexpectedly")

    def test_asserts_answer_selector_is_string_and_a_supported_value(self):
        params_with_changed_answer_selector = self.valid_question_params

        with self.assertRaises(AssertionError):
            params_with_changed_answer_selector['answer_selector'] = None
            self.client.build_question_payload(params_with_changed_answer_selector)

        with self.assertRaises(AssertionError):
            params_with_changed_answer_selector['answer_selector'] = 'ZZ'
            self.client.build_question_payload(params_with_changed_answer_selector)

        try:
            params_with_changed_answer_selector['answer_selector'] = QUALTRICS_API_SUPPORTED_ANSWER_SELECTORS[0]
            self.client.build_question_payload(params_with_changed_answer_selector)
        except AssertionError:
            self.fail("build_question_payload() raised AssertionErrror unexpectedly")

    def test_asserts_label_is_non_empty_string(self):
        params_with_changed_label = self.valid_question_params

        with self.assertRaises(AssertionError):
            params_with_changed_label['label'] = ''
            self.client.build_question_payload(params_with_changed_label)

    def test_asserts_block_number_is_integer(self):
        params_with_changed_block_number = self.valid_question_params

        with self.assertRaises(AssertionError):
            params_with_changed_block_number['block_number'] = 1.23
            self.client.build_question_payload(params_with_changed_block_number)

        with self.assertRaises(AssertionError):
            params_with_changed_block_number['block_number'] = []
            self.client.build_question_payload(params_with_changed_block_number)

        with self.assertRaises(AssertionError):
            params_with_changed_block_number['block_number'] = {}
            self.client.build_question_payload(params_with_changed_block_number)

    def test_returns_valid_payload_for_given_params(self):
        expected_payload = {
            'QuestionText': 'What is love?',
            'DataExportTag': 'Q1',
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'respondent_what_is_love_mc',
            'Choices': {
                '1': 'Baby don\'t hurt me',
                '2': 'Don\'t hurt me',
                '3': 'No more'
            },
            'ChoiceOrder': [
                '1',
                '2',
                '3'
            ],
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': []
        }

        actual_payload = self.client.build_question_payload(self.valid_question_params)

        # have to use assertCountEqual as order of keys may not be the same
        self.assertCountEqual(actual_payload, expected_payload)
