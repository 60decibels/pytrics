import unittest
from unittest.mock import MagicMock

from pytrics.common.exceptions import QualtricsDataSerialisationException

from pytrics.operations.download import _await_response_file_creation


class AwaitResponseFileCreationTestCase(unittest.TestCase):

    def setUp(self):
        self.api = MagicMock()
        self.api.get_response_export_file.return_value = {'response': 'export'}

    def test_returns_result_as_expected_on_success(self):
        self.api.get_response_export_progress.side_effect = [
            ({'result': {'status': 'inProgress', 'fileId': None}}, None),
            ({'result': {'status': 'inProgress', 'fileId': None}}, None),
            ({'result': {'status': 'complete', 'fileId': 'file-id-123'}}, 'file-id-123'),
        ]

        expected_result = {'response': 'export'}

        actual_result = _await_response_file_creation(self.api, 'SV_abcdefghijk', 'prog-ress-id')

        self.assertEqual(actual_result, expected_result)

    def test_raises_exception_on_failure(self):
        self.api.get_response_export_progress.side_effect = [
            ({'result': {'status': 'inProgress', 'fileId': None}}, None),
            ({'result': {'status': 'failed', 'fileId': None}}, None),
        ]

        with self.assertRaises(QualtricsDataSerialisationException):
            _ = _await_response_file_creation(self.api, 'SV_abcdefghijk', 'prog-ress-id')
