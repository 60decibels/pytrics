import unittest

from qualtrics_api.client import QualtricsAPIClient


class BuildQuestionDisplayLogicTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_asserts_controlling_question_id_param(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(None, [1, 2], 'EqualTo', None, None)

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic('', [1, 2], 'EqualTo', None, None)

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic('InvalidQuestionID-Format', [1, 2], 'EqualTo', None, None)

    def test_asserts_choices_param(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic('nps_company_rating', [], 'Selected', None, None)

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic('nps_company_rating', {}, 'Selected', None, None)

    def test_asserts_operator_is_supported_value_or_none(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic('QID1', ['IsPromoter'], 'InvalidOperator', None, None)

        try:
            self.client.build_question_display_logic('QID1', ['IsPromoter'], 'EqualTo', None, None)
        except AssertionError:
            self.fail('client.build_question_display_logic() failed assertions unexpectedly')

    def test_asserts_conjunction_is_supported_value_or_none(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic('QID5', [1, 2], 'Selected', 'InvalidConjunction', None)

        try:
            self.client.build_question_display_logic('QID5', [1, 2], 'Selected', 'Or', None)
        except AssertionError:
            self.fail('client.build_question_display_logic() failed assertions unexpectedly')

    def test_asserts_locator_is_supported_value_or_none(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic('QID5', [1, 2], 'Selected', 'Or', 'InvalidLocator')

        try:
            self.client.build_question_display_logic('QID5', [1, 2], 'Selected', 'Or', 'SelectableChoice')
        except AssertionError:
            self.fail('client.build_question_display_logic() failed assertions unexpectedly')

    def test_builds_display_logic_for_single_choice(self):
        expected = {
            '0': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID1',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID1/IsPromoter',
                    'Operator': 'EqualTo',
                    'QuestionIDFromLocator': 'QID1',
                    'LeftOperand': 'q://QID1/IsPromoter',
                    'RightOperand': '1',
                    'Type': 'Expression',
                    'Description': 'If QID1 IsPromoter Is True'
                },
                'Type': 'If'
            },
            'Type': 'BooleanExpression',
            'inPage': False
        }


        actual = self.client.build_question_display_logic('QID1', ['IsPromoter'], 'EqualTo', None, None)

        self.assertCountEqual(expected, actual)

    def test_builds_display_logic_for_two_choices(self):
        expected = {
            '0': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID5',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID5/SelectableChoice/1',
                    'Operator': 'Selected',
                    'QuestionIDFromLocator': 'QID5',
                    'LeftOperand': 'q://QID5/SelectableChoice/1',
                    'Type': 'Expression',
                    'Description': 'If QID5 1 Is Selected'
                },
                '1': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID5',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID5/SelectableChoice/2',
                    'Operator': 'Selected',
                    'QuestionIDFromLocator': 'QID5',
                    'LeftOperand': 'q://QID5/SelectableChoice/2',
                    'Type': 'Expression',
                    'Description': 'If QID5 2 Is Selected',
                    'Conjuction': 'Or'
                },
                'Type': 'If'
            },
            'Type': 'BooleanExpression',
            'inPage': False
        }

        actual = self.client.build_question_display_logic('QID5', [1, 2], 'Selected', 'Or', 'SelectableChoice')

        self.assertCountEqual(expected, actual)
