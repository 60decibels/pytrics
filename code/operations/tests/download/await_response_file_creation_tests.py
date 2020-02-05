import unittest
from unittest.mock import MagicMock, patch, call

from common.exceptions import QualtricsDataSerialisationException

from qualtrics_api.operations.download import _await_response_file_creation


class AwaitResponseFileCreationTestCase(unittest.TestCase):

    def setUp(self):
        _get_profile_patch = patch('qualtrics_api.operations.download._get_profile')
        self._get_profile = _get_profile_patch.start()
        self.addCleanup(_get_profile_patch.stop)

        self._get_profile.return_value = 'testing'

        self.api = MagicMock()
        self.api.get_response_export_file.return_value = {'response': 'export'}

        logger_patch = patch('qualtrics_api.operations.download.logger')
        self.logger = logger_patch.start()
        self.addCleanup(logger_patch.stop)

    def test_logs_info_and_returns_result_as_expected_on_success(self):
        self.api.get_response_export_progress.side_effect = [
            ({'result': {'status': 'inProgress', 'fileId': None}}, None),
            ({'result': {'status': 'inProgress', 'fileId': None}}, None),
            ({'result': {'status': 'complete', 'fileId': 'file-id-123'}}, 'file-id-123'),
        ]

        expected_calls = [
            call({'result': {'status': 'inProgress', 'fileId': None}}),
            call({'result': {'status': 'inProgress', 'fileId': None}}),
            call({'result': {'status': 'complete', 'fileId': 'file-id-123'}}),
            call('Response file for survey %s complete, returning bytes', 'SV_abcdefghijk'),
        ]

        expected_result = {'response': 'export'}

        actual_result = _await_response_file_creation(self.api, 'SV_abcdefghijk', 'prog-ress-id')

        self.assertEqual(actual_result, expected_result)

        self.logger.info.assert_has_calls(expected_calls)

    def test_logs_error_and_raises_exception_on_failure(self):
        self.api.get_response_export_progress.side_effect = [
            ({'result': {'status': 'inProgress', 'fileId': None}}, None),
            ({'result': {'status': 'failed', 'fileId': None}}, None),
        ]

        expected_info_calls = [
            call({'result': {'status': 'inProgress', 'fileId': None}}),
            call({'result': {'status': 'failed', 'fileId': None}}),
        ]

        with self.assertRaises(QualtricsDataSerialisationException):
            _ = _await_response_file_creation(self.api, 'SV_abcdefghijk', 'prog-ress-id')

        self.logger.info.assert_has_calls(expected_info_calls)
        self.logger.error.assert_called_once_with('Error encountered during export for progress_id %s', 'prog-ress-id')
