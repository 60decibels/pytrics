# pylint: disable=protected-access
import unittest

from pytrics.qualtrics_api.client import QualtricsAPIClient


class ValidateQuestionPayloadTestCase(unittest.TestCase):

    def setUp(self):
        self.valid_minimal_question_payload_shape = {
            'QuestionText': '',
            'DataExportTag': '',
            'QuestionType': '',
            'Selector': '',
            'Configuration': {},
            'QuestionDescription': '',
            'Validation': {},
            'Language': []
        }

        self.valid_multi_choice_payload = {
            'ChoiceOrder': [1, 2, 3, 4, 5],
            'Choices': {
                '1': {
                    'Display': 'Very much improved'
                },
                '2': {
                    'Display': 'Slightly improved'
                },
                '3': {
                    'Display': 'No change'
                },
                '4': {
                    'Display': 'Got slightly worse'
                },
                '5': {
                    'Display': 'Got much worse'
                }
            },
            'Configuration': {
                'QuestionDescriptionOption': 'SpecifyLabel'
            },
            'DataExportTag': 'Q5',
            'Language': [],
            'QuestionDescription': 'qol_rating',
            'QuestionText': 'Has your quality of life changed because of [Company]?',
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'SubSelector': 'TX',
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'ON',
                    'Type': 'None'
                }
            },
            'VariableNaming': {
                '1': 'Very much improved',
                '2': 'Slightly improved',
                '3': 'No change',
                '4': 'Got slightly worse',
                '5': 'Got much worse'
            }
        }

        self.valid_text_entry_payload = {
            'Configuration': {
                'QuestionDescriptionOption':  'SpecifyLabel'
            },
            'DataExportTag': 'Q9',
            'Language': [],
            'QuestionDescription': 'ppi_in_s_hhsize',
            'QuestionID': 'QID9',
            'QuestionText':'Including yourself, how many people live in your home?',
            'QuestionType': 'TE',
            'Selector': 'SL',
            'Validation': {
                'Settings': {
                    'ContentType': 'ValidNumber',
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'ON',
                    'Type': 'ContentType'
                }
            }
        }

    def test_validate_question_payload_raises_assertion_error_if_no_payload(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        with self.assertRaises(AssertionError):
            client._validate_question_payload()

    def test_validate_question_payload_raises_assertion_error_if_keys_missing(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        self.valid_minimal_question_payload_shape.pop('QuestionText', {})

        with self.assertRaises(AssertionError):
            client._validate_question_payload(self.valid_minimal_question_payload_shape)

    def test_raises_error_when_choices_but_no_choice_order(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        self.valid_multi_choice_payload.pop('ChoiceOrder', {})

        with self.assertRaises(AssertionError):
            client._validate_question_payload(self.valid_multi_choice_payload)

    def test_raises_error_when_choice_order_but_no_choices(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        self.valid_multi_choice_payload.pop('Choices', {})

        with self.assertRaises(AssertionError):
            client._validate_question_payload(self.valid_multi_choice_payload)

    def test_raises_error_when_sub_selector_missing_when_expected(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        self.valid_multi_choice_payload.pop('SubSelector', {})

        with self.assertRaises(AssertionError):
            client._validate_question_payload(self.valid_multi_choice_payload)

    def test_raises_error_when_sub_selector_is_incorrect(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        self.valid_multi_choice_payload['SubSelector'] = 'INVALID'

        with self.assertRaises(AssertionError):
            client._validate_question_payload(self.valid_multi_choice_payload)

    def test_does_not_raise_error_when_valid_payload_shape_supplied(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        try:
            client._validate_question_payload(self.valid_minimal_question_payload_shape)
        except AssertionError:
            self.fail('_validate_question_payload() raised AssertionErrror for minimal correctly shaped payload unexpectedly')

    def test_does_not_raise_error_when_valid_multi_choice_payload_supplied(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        try:
            client._validate_question_payload(self.valid_multi_choice_payload)
        except AssertionError:
            self.fail('_validate_question_payload() raised AssertionErrror for multi-choice payload unexpectedly')

    def test_does_not_raise_error_when_valid_text_entry_payload_supplied(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        try:
            client._validate_question_payload(self.valid_text_entry_payload)
        except AssertionError:
            self.fail('_validate_question_payload() raised AssertionErrror text-entry payload unexpectedly')
