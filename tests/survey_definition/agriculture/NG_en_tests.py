import unittest

from pytrics.survey_definition.agriculture import NG_en


class ETenSurveyDefinitionTestCase(unittest.TestCase):

    def test_get_name_returns_expected_name(self):
        name = NG_en.get_name()

        self.assertEqual(name, '60dB Standard Agriculture Survey - Nigeria')

    def test_get_blocks_returns_list_of_blocks(self):
        blocks = NG_en.get_blocks()

        self.assertIsNotNone(blocks)

        self.assertTrue(isinstance(blocks, list))

        self.assertEqual(len(blocks), 20)

    def test_get_questions_returns_list_of_questions(self):
        questions = NG_en.get_questions()

        self.assertIsNotNone(questions)

        self.assertTrue(isinstance(questions, list))

        self.assertEqual(len(questions), 66)
