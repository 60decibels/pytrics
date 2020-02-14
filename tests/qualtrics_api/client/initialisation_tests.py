
import unittest

from pytrics.common.exceptions import QualtricsAPIException
from pytrics.qualtrics_api.client import QualtricsAPIClient


class InitialisationTestCase(unittest.TestCase):

    def test_raises_exception_when_base_api_url_is_none(self):
        with self.assertRaises(QualtricsAPIException):
            QualtricsAPIClient(None, 'token-456')

    def test_raises_exception_when_auth_token_is_none(self):
        with self.assertRaises(QualtricsAPIException):
            QualtricsAPIClient('http://qualtrics.com/api', None)
