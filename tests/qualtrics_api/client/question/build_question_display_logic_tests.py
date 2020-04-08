import unittest

from pytrics.qualtrics_api.client import QualtricsAPIClient


class BuildQuestionDisplayLogicTestCase(unittest.TestCase):

    def setUp(self):
        self.client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

    def test_asserts_controlling_question_ids_param(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(None, [1], ['EqualTo'], [None], [None])

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic('', [1], ['EqualTo'], [None], [None])

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(['InvalidQuestionID-Format'], [1], ['EqualTo'], [None], [None])

    def test_asserts_choices_param(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(['nps_company_rating'], [], ['Selected'], [None], [None])

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(['nps_company_rating'], {}, ['Selected'], [None], [None])

    def test_asserts_operators_are_supported_values_or_none(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(['QID1'], ['IsPromoter'], ['InvalidOperator'], [None], [None])

        try:
            self.client.build_question_display_logic(['QID1'], ['IsPromoter'], ['EqualTo'], [None], [None])
        except AssertionError:
            self.fail('client.build_question_display_logic() failed assertions unexpectedly')

    def test_asserts_conjunctions_are_supported_values_or_none(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(['QID5', 'QID5'], [1, 2], ['Selected', 'Selected'], [None, 'InvalidConjunction'], [None, None])

        try:
            self.client.build_question_display_logic(['QID5', 'QID5'], [1, 2], ['Selected', 'Selected'], [None, 'Or'], [None, None])
        except AssertionError:
            self.fail('client.build_question_display_logic() failed assertions unexpectedly')

        try:
            self.client.build_question_display_logic(['QID5', 'QID5'], [1, 2], ['Selected', 'Selected'], [None, 'And'], [None, None])
        except AssertionError:
            self.fail('client.build_question_display_logic() failed assertions unexpectedly')

    def test_asserts_locators_are_supported_values_or_none(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(['QID5', 'QID5'], [1, 2], ['Selected', 'Selected'], [None, 'Or'], ['InvalidLocator', 'AnotherInvalidLocator'])

        try:
            self.client.build_question_display_logic(['QID5', 'QID5'], [1, 2], ['Selected', 'Selected'], [None, 'Or'], ['SelectableChoice', None])
        except AssertionError:
            self.fail('client.build_question_display_logic() failed assertions unexpectedly')

    def test_asserts_all_param_lists_must_have_equal_length(self):
        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(
                ['QID6'],
                [1, 2],
                ['Selected', 'NotSelected'],
                [None, 'And'],
                ['SelectableChoice', 'SelectableChoice']
            )

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(
                ['QID6', 'QID7'],
                [1],
                ['Selected', 'NotSelected'],
                [None, 'And'],
                ['SelectableChoice', 'SelectableChoice']
            )

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(
                ['QID6', 'QID7'],
                [1, 2],
                ['Selected'],
                [None, 'And'],
                ['SelectableChoice', 'SelectableChoice']
            )

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(
                ['QID6', 'QID7'],
                [1, 2],
                ['Selected', 'NotSelected'],
                [None],
                ['SelectableChoice', 'SelectableChoice']
            )

        with self.assertRaises(AssertionError):
            self.client.build_question_display_logic(
                ['QID6', 'QID7'],
                [1, 2],
                ['Selected', 'NotSelected'],
                [None, 'And'],
                ['SelectableChoice']
            )

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

        actual = self.client.build_question_display_logic(['QID1'], ['IsPromoter'], ['EqualTo'], [None], [None])

        self.assertCountEqual(expected, actual)

    def test_builds_display_logic_for_two_choices_with_an_or_conjunction(self):
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

        actual = self.client.build_question_display_logic(['QID5', 'QID5'], [1, 2], ['Selected', 'Selected'], [None, 'Or'], ['SelectableChoice', 'SelectableChoice'])

        self.assertCountEqual(expected, actual)

    def test_builds_display_logic_for_two_choices_of_different_questions_with_an_and_conjunction_and_different_operators(self):
        expected = {
            '0': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID6',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID6/SelectableChoice/1',
                    'Operator': 'Selected',
                    'QuestionIDFromLocator': 'QID6',
                    'LeftOperand': 'q://QID6/SelectableChoice/1',
                    'Type': 'Expression',
                    'Description': 'If QID6 1 Is Selected'
                },
                '1': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID7',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID7/SelectableChoice/2',
                    'Operator': 'NotSelected',
                    'QuestionIDFromLocator': 'QID7',
                    'LeftOperand': 'q://QID7/SelectableChoice/2',
                    'Type': 'Expression',
                    'Description': 'If QID7 2 Is Not Selected',
                    'Conjuction': 'And'
                },
                'Type': 'If'
            },
            'Type': 'BooleanExpression',
            'inPage': False
        }

        actual = self.client.build_question_display_logic(['QID6', 'QID7'], [1, 2], ['Selected', 'NotSelected'], [None, 'And'], ['SelectableChoice', 'SelectableChoice'])

        self.assertCountEqual(expected, actual)
