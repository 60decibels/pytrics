import unittest
from unittest.mock import MagicMock, mock_open, patch, call

from common.constants import QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT
from common.exceptions import QualtricsDataSerialisationException

from qualtrics_api.operations.download import save_responses_to_s3


class SaveSurveyToS3TestCase(unittest.TestCase): # pylint: disable=too-many-instance-attributes

    def setUp(self):
        _get_s3_response_file_path_patch = patch('qualtrics_api.operations.download._get_s3_response_file_path')
        self._get_s3_response_file_path = _get_s3_response_file_path_patch.start()
        self.addCleanup(_get_s3_response_file_path_patch.stop)

        self.file_path_and_name = 'testing/response/qualtrics/new/SV_abcdefgh_responses.zip'
        self._get_s3_response_file_path.return_value = self.file_path_and_name

        self.api = MagicMock()
        self.create_response_export_result = {
            'result': {
                'progressId': 'ES_d4DVIiKEHQ9rBWZ',
                'percentComplete': 0.0,
                'status': 'inProgress'
            },
            'meta': {
                'requestId': '75eef7c1-75eb-48c4-b60c-26b695a35af3',
                'httpStatus': '200 - OK'
            }
        }
        self.api.create_response_export.return_value = (self.create_response_export_result, 'ES_d4DVIiKEHQ9rBWZ')

        _await_response_file_creation_patch = patch('qualtrics_api.operations.download._await_response_file_creation')
        self._await_response_file_creation = _await_response_file_creation_patch.start()
        self.addCleanup(_await_response_file_creation_patch.stop)

        upload_patch = patch('qualtrics_api.operations.download.upload')
        self.upload = upload_patch.start()
        self.addCleanup(upload_patch.stop)

        self.mock_open = open_patch = patch('qualtrics_api.operations.download.open', new_callable=mock_open(), create=True)
        self.mock_open = open_patch.start()
        self.addCleanup(open_patch.stop)

        self.response_file = MagicMock()
        self.mock_open.return_value.__enter__.return_value = self.response_file

        logger_patch = patch('qualtrics_api.operations.download.logger')
        self.logger = logger_patch.start()
        self.addCleanup(logger_patch.stop)

    def test_calls_various_functions_as_expected(self):
        # _await_response_file_creation either:
        # 1. raises an exception as export not yet ready, or
        # 2. returns bytes representing the zipped response file when ready

        # so set return value of create export to complete immediately
        self._await_response_file_creation.return_value = 'b504b 0304 1400 0808 0800 1458 f74e 0000'

        # run the function
        save_responses_to_s3(self.api, 'SV_abcdefghijk')

        # assert it calls the things we expect it to, with expected args
        self.api.create_response_export.assert_called_once_with('SV_abcdefghijk')

        self._get_s3_response_file_path.assert_called_once_with('SV_abcdefghijk')

        self._await_response_file_creation.assert_called_once_with(self.api, 'SV_abcdefghijk', 'ES_d4DVIiKEHQ9rBWZ')

        self.upload.assert_called_once_with('60db', self.file_path_and_name)

        self.response_file.write.assert_called_once_with('b504b 0304 1400 0808 0800 1458 f74e 0000')

        logger_calls = [
            call('Starting response file export for survey %s', 'SV_abcdefghijk'),
            call('Response data received on try #%s for survey %s, uploading to s3 key %s', 0, 'SV_abcdefghijk', self.file_path_and_name),
        ]

        self.logger.info.assert_has_calls(logger_calls)

    def test_recurses_when_export_not_immediately_ready_download(self):
        # _await_response_file_creation either:
        # 1. raises an exception as export not yet ready, or
        # 2. returns bytes representing the zipped response file when ready

        # so set to return the exception 1st time it's called, and the bytes 2nd time
        self._await_response_file_creation.side_effect = [
            QualtricsDataSerialisationException,
            'b504b 0304 1400 0808 0800 1458 f74e 0000',
        ]

        # run the function
        save_responses_to_s3(self.api, 'SV_abcdefghijk')

        # now assert via logging (and other functions) that we ran the function twice,
        # this proves it called itself and recursed as expected

        self.api.create_response_export.assert_called_once_with('SV_abcdefghijk')

        # ensure that 2nd call to _await_response_file_creation uses the same progress_id
        self._await_response_file_creation.assert_has_calls([
            call(self.api, 'SV_abcdefghijk', 'ES_d4DVIiKEHQ9rBWZ'),
            call(self.api, 'SV_abcdefghijk', 'ES_d4DVIiKEHQ9rBWZ'),
        ])

        self.upload.assert_called_once_with('60db', self.file_path_and_name)

        self.response_file.write.assert_called_once_with('b504b 0304 1400 0808 0800 1458 f74e 0000')

        info_calls = [
            call('Starting response file export for survey %s', 'SV_abcdefghijk'),
            call('Calling myself to get new progress_id and try again, retry #%s', 1),
            call('Retry #%s of response file export for survey %s', 1, 'SV_abcdefghijk'),
            call('Response data received on try #%s for survey %s, uploading to s3 key %s', 1, 'SV_abcdefghijk', self.file_path_and_name),
        ]

        self.logger.info.assert_has_calls(info_calls)

        self.logger.error.assert_called_once_with('_await_response_file_creation failed')

    def test_raises_exception_when_maximum_retries_reached(self):
        # _await_response_file_creation either:
        # 1. raises an exception as export not yet ready, or
        # 2. returns bytes representing the zipped response file when ready

        # so set to return exception for the final try as we start at this by calling the function with retries=5
        # (QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT == 5)
        # this should force the code to raise it's 'final' exception and give up
        # note use of side_effect not return_value even though only one call
        # side_effect is required to ensure the patched function raises the exception
        self._await_response_file_creation.side_effect = [
            QualtricsDataSerialisationException
        ]

        # assert expected exception type raised
        with self.assertRaises(QualtricsDataSerialisationException):
            save_responses_to_s3(self.api, 'SV_abcdefghijk', progress_id='fake-progress-id', retries=QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT)

        self.logger.info.assert_called_once_with('Retry #%s of response file export for survey %s', 5, 'SV_abcdefghijk')

        error_calls = [
            call('_await_response_file_creation failed'),
            call('Failed after %s attempts to get responses for survey_id %s', 5, 'SV_abcdefghijk')
        ]

        self.logger.error.assert_has_calls(error_calls)

    def test_raises_exception_when_error_encountered_during_upload(self):
        # don't need to set a return value for _await_response_file_creation
        # as we'll error out of the function before we need to use this

        # tell our upload patch to raise an Exception
        self.upload.return_value = Exception

        # assert expected exception type raised
        with self.assertRaises(QualtricsDataSerialisationException):
            save_responses_to_s3(self.api, 'SV_abcdefghijk')

    def test_raises_exception_when_error_encountered_during_open(self):
        # again, don't need to set a return value for _await_response_file_creation
        # as we'll error out of the function before we need to use this

        # tell our open patch to raise an Exception
        self.mock_open.return_value = Exception

        # assert expected exception type raised
        with self.assertRaises(QualtricsDataSerialisationException):
            save_responses_to_s3(self.api, 'SV_abcdefghijk')
