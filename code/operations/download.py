import json
import logging
import os
import getpass
import time
from zipfile import ZipFile

from requests import HTTPError

from common.constants import (
    JSON_FILE_EXTENSION,
    QUALTRICS_API_EXPORT_RESPONSES_PROGRESS_TIMEOUT,
    QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT,
    S3_DEFAULT_BUCKET,
    S3_RESPONSE_QUALTRICS_NEW,
    ZIP_FILE_EXTENSION,
)
from common.exceptions import (
    QualtricsAPIException,
    QualtricsDataSerialisationException,
    S3PutException,
)
from common.logging.configure import setup_logging
from common.s3.contextmanagers import (
    upload,
    download,
)
from common.s3.operations import (
    _get_profile,
    upload_file_to_s3,
)

from qualtrics_api.client import QualtricsAPIClient
from qualtrics_api.common import get_details_for_client


# Configure and create our logger
setup_logging()
logger = logging.getLogger()


def get_survey_data(survey_id):
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    logger.info('Qualtrics API client ready')

    try:
        file_path_and_name = save_survey_to_file(api, survey_id)
    except (QualtricsAPIException, QualtricsDataSerialisationException):
        logger.error('Unable to retrieve and serialise survey with id %s', survey_id)
        raise

    logger.info('Survey data for %s saved to disk', survey_id)

    return file_path_and_name


def get_survey_and_response_data(survey_id):
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    logger.info('Qualtrics API client ready')

    try:
        _ = save_survey_to_file(api, survey_id)
    except (QualtricsAPIException, QualtricsDataSerialisationException):
        logger.error('Unable to retrieve and serialise survey with id %s', survey_id)
        raise

    logger.info('Survey data for %s saved to disk', survey_id)

    try:
        save_responses_to_file(api, survey_id)
    except QualtricsDataSerialisationException:
        logger.error('Unable to retrieve and serialise responses for survey_id %s', survey_id)
        raise

    logger.info('Response data .zip for %s saved to disk', survey_id)

    try:
        _unzip_response_file(survey_id)
    except QualtricsDataSerialisationException:
        logger.error('Unable to unzip response file for survey_id %s', survey_id)
        raise

    logger.info('Response data .json for %s saved to disk', survey_id)


def save_survey_to_file(api, survey_id):
    try:
        logger.info('Getting survey %s from API', survey_id)
        survey_json = api.get_survey(survey_id)
    except (AssertionError, HTTPError) as ex:
        logger.error('Error encountered during API call get_survey')
        raise QualtricsAPIException(ex)

    file_path_and_name = _get_survey_file_path(survey_id)

    try:
        with open(file_path_and_name, mode='w+', newline='', encoding='utf-8-sig') as survey_file:
            logger.info('Saving survey to s3 with key %s', file_path_and_name)
            json.dump(survey_json, survey_file)

    except Exception as ex:
        logger.error('Error encountered during serialisation of qualtrics survey to s3')
        raise QualtricsDataSerialisationException(ex)

    return file_path_and_name


def save_responses_to_file(api, survey_id, progress_id=None, retries=0):
    file_path_and_name = _get_response_file_path(survey_id)
    response_bytes = None

    if retries == 0:
        logger.info('Starting response file export for survey %s', survey_id)
        _, progress_id = api.create_response_export(survey_id)
    else:
        logger.info('Retry #%s of response file export for survey %s', retries, survey_id)

    try:
        response_bytes = _await_response_file_creation(api, survey_id, progress_id)
    except (QualtricsDataSerialisationException, HTTPError, KeyError):
        logger.error('_await_response_file_creation failed')

        if retries < QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT:
            retries += 1
            logger.info('Calling myself to get new progress_id and try again, retry #%s', retries)
            save_responses_to_file(api, survey_id, progress_id, retries)
        else:
            logger.error('Failed after %s attempts to get responses for survey_id %s', retries, survey_id)
            raise QualtricsDataSerialisationException('Failed after {0} attempts to get responses for survey_id {1}'.format(
                retries,
                survey_id,
            ))

    if response_bytes:
        logger.info('Response data received on try #%s for survey %s, uploading to s3 key %s', retries, survey_id, file_path_and_name)

        try:
            with open(file_path_and_name, mode='wb') as response_file:
                response_file.write(response_bytes)

        except Exception as ex:
            logger.error('Error encountered during serialisation of qualtrics survey to s3: %s', ex)
            raise QualtricsDataSerialisationException(ex)


def _unzip_response_file(survey_id):
    '''
    Response files are zips containing single .json file named after survey in qualtrics

    So extract to .json & rename to associate with the survey .json

    If no responses are yet recorded against a survey the zip is empty. In this case we
    write an empty responses json file to disk to explicitly indicate processing completed
    '''
    response_file_s3_path = _get_response_file_path(survey_id, zipped=True)
    unzipped_response_file_s3_path = _get_response_file_path(survey_id, zipped=False)

    with ZipFile(response_file_s3_path, 'r') as zipped:
        infolist = zipped.infolist()

        logger.info('File %s passed to ZipFile, contains info list %s', response_file_s3_path, infolist)

        if not infolist:
            logger.info('No responses yet recorded, writing empty responses json file to disk')

            empty_responses_json = {"responses":[]}

            try:
                with open(unzipped_response_file_s3_path, mode='w') as empty_response_file:
                    json.dump(empty_responses_json, empty_response_file)
            except S3PutException as ex:
                logger.error('Error writing empty responses json file to disk %s', unzipped_response_file_s3_path)
                raise QualtricsDataSerialisationException(ex)

        for info in infolist:
            logger.info('Zipped response file contains file with name %s - extracting to /tmp', info.filename)

            logger.debug("info.filename is: %s, Effective user is: %s, CWD is: %s", info.filename, getpass.getuser(), os.getcwd())

            zipped.extract(info.filename, path='/tmp')

            extracted_file_local_path = '{0}/{1}'.format('/tmp', info.filename)
            renamed_response_file_local_path = '/tmp/{0}_responses.{1}'.format(survey_id, JSON_FILE_EXTENSION)

            os.rename(extracted_file_local_path, renamed_response_file_local_path)
            logger.info('Response file renamed to %s', renamed_response_file_local_path)


def _await_response_file_creation(api, survey_id, progress_id):
    status = 'inProgress'
    file_id = None

    while status not in ['complete', 'failed']:
        time.sleep(QUALTRICS_API_EXPORT_RESPONSES_PROGRESS_TIMEOUT)

        data, file_id = api.get_response_export_progress(survey_id, progress_id)
        logger.info(data)

        status = data['result']['status']

    if status == 'failed' or not file_id:
        logger.error('Error encountered during export for progress_id %s', progress_id)
        raise QualtricsDataSerialisationException('Failed to complete export for progress_id {}'.format(progress_id))

    logger.info('Response file for survey %s complete, returning bytes', survey_id)
    return api.get_response_export_file(survey_id, file_id)


def _get_survey_file_path(survey_id):
    file_name = '{}.{}'.format(survey_id, JSON_FILE_EXTENSION)
    file_path = '{}/{}'.format(_get_profile(), S3_RESPONSE_QUALTRICS_NEW)

    file_path_and_name = '{}/{}'.format(file_path, file_name)

    return file_path_and_name


def _get_response_file_path(survey_id, zipped=True):
    file_ext = ZIP_FILE_EXTENSION if zipped else JSON_FILE_EXTENSION
    file_name = '{}_responses.{}'.format(survey_id, file_ext)
    file_path = '{}/{}'.format(_get_profile(), S3_RESPONSE_QUALTRICS_NEW)

    file_path_and_name = '{}/{}'.format(file_path, file_name)

    return file_path_and_name
