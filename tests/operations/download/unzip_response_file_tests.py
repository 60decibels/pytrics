import unittest
from unittest.mock import MagicMock, mock_open, patch, call

from pytrics.operations.download import _unzip_response_file


class UnzipResponseFileTestCase(unittest.TestCase): # pylint: disable=too-many-instance-attributes

    def setUp(self):
        _get_response_file_path_patch = patch('pytrics.operations.download._get_response_file_path')
        self._get_response_file_path = _get_response_file_path_patch.start()
        self.addCleanup(_get_response_file_path_patch.stop)

        self._get_response_file_path.side_effect = [
            'testing/SV_abcdefghijk_responses.zip',
            'testing/SV_abcdefghijk_responses.json',
        ]

        self.mock_open = open_patch = patch('pytrics.operations.download.ZipFile', new_callable=mock_open(), create=True)
        self.mock_open = open_patch.start()
        self.addCleanup(open_patch.stop)

        self.zipped = MagicMock()
        self.mock_open.return_value.__enter__.return_value = self.zipped

        self.info = MagicMock(filename='response_file_name_from_api.zip')
        self.zipped.infolist.return_value = [self.info]

        os_patch = patch('pytrics.operations.download.os')
        self.os = os_patch.start()
        self.addCleanup(os_patch.stop)

        self.os.getcwd.return_value = '/'
        self.os.path.join.return_value = 'testing'

    def test_calls_various_functions_as_expected(self):
        # run the function
        _unzip_response_file('SV_abcdefghijk', '/testing')

        # assert it calls the things we expect it to, with expected args
        self._get_response_file_path.assert_has_calls([
            call('SV_abcdefghijk', '/testing', zipped=True),
            call('SV_abcdefghijk', '/testing', zipped=False),
        ])

        self.os.rename.assert_called_once_with('testing/response_file_name_from_api.zip', 'testing/SV_abcdefghijk_responses.json')

    @patch('pytrics.operations.download.open')
    def test_writes_empty_json_responses_file_to_disk_when_no_responses_recorded_against_survey(self, mock_plain_open):
        # we've patched the python system open just for this test, not the ZipFile open as we do in setup
        mock_plain_open.return_value = MagicMock()

        # set return value from zipfile to an empty list, represents an empty archive/zip from the call to qualtrics
        self.zipped.infolist.return_value = []

        _unzip_response_file('SV_abcdefghijk', '/testing')

        # assert it calls the things we expect it to, with expected args
        self._get_response_file_path.assert_has_calls([
            call('SV_abcdefghijk', '/testing', zipped=True),
            call('SV_abcdefghijk', '/testing', zipped=False),
        ])
