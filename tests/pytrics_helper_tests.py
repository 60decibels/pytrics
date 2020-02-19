import unittest
from unittest.mock import patch

from pytrics.common.exceptions import QualtricsAPIException

from pytrics.tools import Tools


class CopyTestCase(unittest.TestCase):

    def setUp(self):
        copy_survey_patch = patch('pytrics.tools.copy_survey')
        self.copy_survey = copy_survey_patch.start()
        self.addCleanup(copy_survey_patch.stop)

        os_patch = patch('pytrics.tools.os')
        self.os = os_patch.start()
        self.addCleanup(os_patch.stop)

        self.os.environ.get.return_value = '/data'

        self.tools = Tools()

    def test_asserts_template_survey_id_param(self):
        with self.assertRaises(AssertionError):
            self.tools.copy(None, 'New Survey Name')

        with self.assertRaises(AssertionError):
            self.tools.copy(123, 'New Survey Name')

    def test_asserts_new_survey_name_param(self):
        with self.assertRaises(AssertionError):
            self.tools.copy('SV_123456abcdef', None)

        with self.assertRaises(AssertionError):
            self.tools.copy('SV_123456abcdef', '   ')

    def test_raises_custom_error_when_copy_survey_raises_error(self):
        self.copy_survey.side_effect = QualtricsAPIException

        with self.assertRaises(QualtricsAPIException):
            self.tools.copy('SV_123456abcdef', 'New Survey Name')

    def test_returns_new_survey_id_when_successful(self):
        self.copy_survey.return_value = 'SV_098765zyxwvu'

        new_survey_id = self.tools.copy('SV_123456abcdef', 'New Survey Name')

        self.assertEqual(new_survey_id, 'SV_098765zyxwvu')
