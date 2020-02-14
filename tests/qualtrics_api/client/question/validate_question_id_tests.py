# pylint: disable=protected-access
import unittest

from pytrics.qualtrics_api.client import QualtricsAPIClient


class ValidateQuestionIdTestCase(unittest.TestCase):

    def test_validate_question_id_raises_assertion_error_if_question_id_format_invalid(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        with self.assertRaises(AssertionError):
            client._validate_question_id('invalid-format-question-id')

    def test_validate_question_id_does_not_raise_error_when_question_id_valid(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        try:
            client._validate_question_id('QID1')
        except AssertionError:
            self.fail("_validate_question_id() raised AssertionErrror unexpectedly")
