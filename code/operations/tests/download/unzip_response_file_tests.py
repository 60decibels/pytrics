import unittest
from unittest.mock import MagicMock, mock_open, patch, call

from operations.download import _unzip_response_file


class UnzipResponseFileTestCase(unittest.TestCase): # pylint: disable=too-many-instance-attributes

    def setUp(self):
        _get_response_file_path_patch = patch('operations.download._get_response_file_path')
        self._get_response_file_path = _get_response_file_path_patch.start()
        self.addCleanup(_get_response_file_path_patch.stop)

        self._get_response_file_path.side_effect = [
            'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip',
            'testing/response/qualtrics/new/SV_abcdefghijk_responses.json',
        ]

        self.mock_open = open_patch = patch('operations.download.ZipFile', new_callable=mock_open(), create=True)
        self.mock_open = open_patch.start()
        self.addCleanup(open_patch.stop)

        self.zipped = MagicMock()
        self.mock_open.return_value.__enter__.return_value = self.zipped

        self.info = MagicMock(filename='response_file_name_from_api.zip')
        self.zipped.infolist.return_value = [self.info]

        logger_patch = patch('operations.download.logger')
        self.logger = logger_patch.start()
        self.addCleanup(logger_patch.stop)

        os_patch = patch('operations.download.os')
        self.os = os_patch.start()
        self.addCleanup(os_patch.stop)

        self.os.getcwd.return_value = '/'

    def test_calls_various_functions_as_expected(self):
        # run the function
        _unzip_response_file('SV_abcdefghijk')

        # assert it calls the things we expect it to, with expected args
        self._get_response_file_path.assert_has_calls([
            call('SV_abcdefghijk', zipped=True),
            call('SV_abcdefghijk', zipped=False),
        ])

        self.os.rename.assert_called_once_with('/tmp/response_file_name_from_api.zip', '/tmp/SV_abcdefghijk_responses.json')

        self.logger.info.assert_has_calls([
            call('File %s passed to ZipFile, contains info list %s', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip', [self.info]),
            call('Zipped response file contains file with name %s - extracting to /tmp', self.info.filename),
            call('Response file renamed to %s', '/tmp/SV_abcdefghijk_responses.json'),
        ])

    @patch('operations.download.open')
    def test_writes_empty_json_responses_file_to_disk_when_no_responses_recorded_against_survey(self, mock_plain_open):
        # we've patched the python system open just for this test, not the ZipFile open as we do in setup
        mock_plain_open.return_value = MagicMock()

        # set return value from zipfile to an empty list, represents an empty archive/zip from the call to qualtrics
        self.zipped.infolist.return_value = []

        _unzip_response_file('SV_abcdefghijk')

        # assert it calls the things we expect it to, with expected args
        self._get_response_file_path.assert_has_calls([
            call('SV_abcdefghijk', zipped=True),
            call('SV_abcdefghijk', zipped=False),
        ])

        self.logger.info.assert_has_calls([
            call('File %s passed to ZipFile, contains info list %s', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip', []),
            call('No responses yet recorded, writing empty responses json file to disk'),
        ])
