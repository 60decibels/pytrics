import unittest
from unittest.mock import MagicMock, mock_open, patch, call

from common.exceptions import QualtricsDataSerialisationException

from operations.download import _unzip_response_file


class UnzipResponseFileTestCase(unittest.TestCase): # pylint: disable=too-many-instance-attributes

    def setUp(self):
        _get_s3_response_file_path_patch = patch('operations.download._get_s3_response_file_path')
        self._get_s3_response_file_path = _get_s3_response_file_path_patch.start()
        self.addCleanup(_get_s3_response_file_path_patch.stop)

        self._get_s3_response_file_path.side_effect = [
            'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip',
            'testing/response/qualtrics/new/SV_abcdefghijk_responses.json',
        ]

        download_patch = patch('operations.download.download')
        self.download = download_patch.start()
        self.addCleanup(download_patch.stop)

        self.download.return_value.__enter__.return_value = 'tmp_file_path'

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

        upload_file_to_s3_patch = patch('operations.download.upload_file_to_s3')
        self.upload_file_to_s3 = upload_file_to_s3_patch.start()
        self.addCleanup(upload_file_to_s3_patch.stop)

        upload_patch = patch('operations.download.upload')
        self.upload = upload_patch.start()
        self.addCleanup(upload_patch.stop)

    def test_calls_various_functions_as_expected(self):
        # run the function
        _unzip_response_file('SV_abcdefghijk')

        # assert it calls the things we expect it to, with expected args
        self._get_s3_response_file_path.assert_has_calls([
            call('SV_abcdefghijk', zipped=True),
            call('SV_abcdefghijk', zipped=False),
        ])

        self.download.assert_called_once_with('60db', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip')

        self.os.rename.assert_called_once_with('/tmp/response_file_name_from_api.zip', '/tmp/SV_abcdefghijk_responses.json')

        self.upload_file_to_s3.assert_called_once_with('/tmp/SV_abcdefghijk_responses.json', '60db', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.json')

        self.os.remove.assert_called_once_with('/tmp/SV_abcdefghijk_responses.json')

        self.logger.info.assert_has_calls([
            call('File %s downloaded from s3 to local tmp file %s', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip', 'tmp_file_path'),
            call('Local tmp file %s passed to ZipFile, contains info list %s', 'tmp_file_path', [self.info]),
            call('Zipped response file contains file with name %s - extracting to /tmp', self.info.filename),
            call('Response file renamed to %s', '/tmp/SV_abcdefghijk_responses.json'),
            call('Extracted file %s uploaded to %s', '/tmp/SV_abcdefghijk_responses.json', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.json'),
        ])

    @patch('operations.download.open')
    def test_writes_empty_json_responses_file_to_s3_when_no_responses_recorded_against_survey(self, mock_plain_open):
        # we've patched the python system open just for this test, not the ZipFile open as we do in setup
        mock_plain_open.return_value = MagicMock()

        # set return value from zipfile to an empty list, represents an empty archive/zip from the call to qualtrics
        self.zipped.infolist.return_value = []

        _unzip_response_file('SV_abcdefghijk')

        # assert it calls the things we expect it to, with expected args
        self._get_s3_response_file_path.assert_has_calls([
            call('SV_abcdefghijk', zipped=True),
            call('SV_abcdefghijk', zipped=False),
        ])

        self.download.assert_called_once_with('60db', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip')

        self.upload.assert_called_once_with('60db', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.json')

        self.logger.info.assert_has_calls([
            call('File %s downloaded from s3 to local tmp file %s', 'testing/response/qualtrics/new/SV_abcdefghijk_responses.zip', 'tmp_file_path'),
            call('Local tmp file %s passed to ZipFile, contains info list %s', 'tmp_file_path', []),
            call('No responses yet recorded, writing empty responses json file to s3 for later processing'),
        ])

    def test_raises_exception_when_upload_file_to_s3_errors(self):
        # set exception as side_effect
        self.upload_file_to_s3.side_effect = [
            QualtricsDataSerialisationException
        ]

        # assert exception raised
        with self.assertRaises(QualtricsDataSerialisationException):
            _unzip_response_file('SV_abcdefghijk')

        # and error logged
        self.logger.error.assert_called_once_with(
            'Error uploading unzipped file to s3 key %s',
            'testing/response/qualtrics/new/SV_abcdefghijk_responses.json'
        )

    def test_raises_exception_when_upload_errors(self):
        self.zipped.infolist.return_value = []

        self.upload.side_effect = [
            QualtricsDataSerialisationException
        ]

        # assert exception raised
        with self.assertRaises(QualtricsDataSerialisationException):
            _unzip_response_file('SV_abcdefghijk')

        # and error logged
        self.logger.error.assert_called_once_with(
            'Error uploading empty responses json file to s3 key %s',
            'testing/response/qualtrics/new/SV_abcdefghijk_responses.json'
        )
