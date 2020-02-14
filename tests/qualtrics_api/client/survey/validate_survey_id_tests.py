# pylint: disable=protected-access
import unittest

from pytrics.qualtrics_api.client import QualtricsAPIClient


class ValidateSurveyIdTestCase(unittest.TestCase):

    def test_validate_survey_id_raises_assertion_error_if_survey_id_format_invalid(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        with self.assertRaises(AssertionError):
            client._validate_survey_id('invalid-format-survey-id')

    def test_validate_survey_id_does_not_raise_error_when_survey_id_valid(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        try:
            client._validate_survey_id('SV_0123456789a')
        except AssertionError:
            self.fail("_validate_survey_id() raised AssertionErrror unexpectedly")
