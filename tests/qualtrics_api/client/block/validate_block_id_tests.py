# pylint: disable=protected-access
import unittest

from pytrics.qualtrics_api.client import QualtricsAPIClient


class ValidateBlockIdTestCase(unittest.TestCase):

    def test_validate_block_id_raises_assertion_error_if_block_id_format_invalid(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        with self.assertRaises(AssertionError):
            client._validate_block_id('invalid-format-block-id')

    def test_validate_block_id_does_not_raise_error_when_block_id_valid(self):
        client = QualtricsAPIClient('http://qualtrics.com/api', 'token-456')

        try:
            client._validate_block_id('BL_0123456789a')
        except AssertionError:
            self.fail("_validate_block_id() raised AssertionErrror unexpectedly")
