import unittest
from unittest.mock import patch

from pytrics.common.exceptions import QualtricsAPIException

from pytrics.qualtrics_api.common import get_details_for_client


class GetDetailsForClientTestCase(unittest.TestCase):

    def setUp(self):
        os_patch = patch('pytrics.qualtrics_api.common.os')
        self.os = os_patch.start()
        self.addCleanup(os_patch.stop)

    def test_raises_exception_when_base_url_not_found_in_env(self):
        self.os.environ.get.side_effect = [
            None,
            'token-456',
        ]

        with self.assertRaises(QualtricsAPIException):
            get_details_for_client()

    def test_raises_exception_when_auth_token_not_found_in_env(self):
        self.os.environ.get.side_effect = [
            'http://qualtrics.com/api',
            None,
        ]

        with self.assertRaises(QualtricsAPIException):
            get_details_for_client()

    def test_returns_expected_env_vars_when_available(self):
        self.os.environ.get.side_effect = [
            'http://qualtrics.com/api',
            'token-456',
        ]

        base_url, auth_token = get_details_for_client()

        self.assertEqual(base_url, 'http://qualtrics.com/api')
        self.assertEqual(auth_token, 'token-456')
