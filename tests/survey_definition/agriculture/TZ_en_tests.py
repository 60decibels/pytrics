import unittest

from pytrics.survey_definition.agriculture import TZ_en


class ETenSurveyDefinitionTestCase(unittest.TestCase):

    def test_get_name_returns_expected_name(self):
        name = TZ_en.get_name()

        self.assertEqual(name, '60dB Standard Agriculture Survey - Tanzania')

    def test_get_blocks_returns_list_of_blocks(self):
        blocks = TZ_en.get_blocks()

        self.assertIsNotNone(blocks)

        self.assertTrue(isinstance(blocks, list))

        self.assertEqual(len(blocks), 20)

    def test_get_questions_returns_list_of_questions(self):
        questions = TZ_en.get_questions()

        self.assertIsNotNone(questions)

        self.assertTrue(isinstance(questions, list))

        self.assertEqual(len(questions), 66)
