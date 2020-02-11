import json
import os
import time
from zipfile import ZipFile

from requests import HTTPError

from common.constants import (
    FILE_EXTENSION_JSON,
    FILE_EXTENSION_ZIP,
    QUALTRICS_API_EXPORT_RESPONSES_PROGRESS_TIMEOUT,
    QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT,
)
from common.exceptions import (
    QualtricsAPIException,
    QualtricsDataSerialisationException,
)

from qualtrics_api.client import QualtricsAPIClient
from qualtrics_api.common import get_details_for_client


def get_survey_data(survey_id):
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    try:
        file_path_and_name = save_survey_to_file(api, survey_id)
    except (QualtricsAPIException, QualtricsDataSerialisationException) as qex:
        raise qex

    return file_path_and_name


def get_survey_and_response_data(survey_id):
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    try:
        survey_file_name = save_survey_to_file(api, survey_id)
    except (QualtricsAPIException, QualtricsDataSerialisationException) as qex:
        raise qex

    try:
        response_file_name = save_responses_to_file(api, survey_id)
    except QualtricsDataSerialisationException as qex:
        raise qex

    try:
        _unzip_response_file(survey_id)
    except QualtricsDataSerialisationException as qex:
        raise qex

    return survey_file_name, response_file_name


def save_survey_to_file(api, survey_id):
    try:
        survey_json = api.get_survey(survey_id)
    except (AssertionError, HTTPError) as ex:
        raise QualtricsAPIException(ex)

    file_path_and_name = _get_survey_file_path(survey_id)

    try:
        with open(file_path_and_name, mode='w+', newline='', encoding='utf-8-sig') as survey_file:
            json.dump(survey_json, survey_file)

    except Exception as ex:
        raise QualtricsDataSerialisationException(ex)

    return file_path_and_name


def save_responses_to_file(api, survey_id, progress_id=None, retries=0):
    file_path_and_name = _get_response_file_path(survey_id)
    response_bytes = None

    if retries == 0:
        _, progress_id = api.create_response_export(survey_id)

    try:
        response_bytes = _await_response_file_creation(api, survey_id, progress_id)
    except (QualtricsDataSerialisationException, HTTPError, KeyError):
        if retries < QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT:
            retries += 1
            # Recurse to get new progress_id and try again
            save_responses_to_file(api, survey_id, progress_id, retries)
        else:
            # Retry limit reached
            raise QualtricsDataSerialisationException('Failed after {0} attempts to get responses for survey_id {1}'.format(
                retries,
                survey_id,
            ))

    if response_bytes:
        try:
            with open(file_path_and_name, mode='wb') as response_file:
                response_file.write(response_bytes)

        except Exception as ex:
            raise QualtricsDataSerialisationException(ex)

    return file_path_and_name


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

        if not infolist:
            empty_responses_json = {"responses":[]}

            try:
                with open(unzipped_response_file_s3_path, mode='w') as empty_response_file:
                    json.dump(empty_responses_json, empty_response_file)
            except QualtricsDataSerialisationException as ex:
                raise QualtricsDataSerialisationException(ex)

        for info in infolist:
            zipped.extract(info.filename, path='/tmp')

            extracted_file_local_path = '{0}/{1}'.format('/tmp', info.filename)
            renamed_response_file_local_path = '/tmp/{0}_responses.{1}'.format(survey_id, FILE_EXTENSION_JSON)

            os.rename(extracted_file_local_path, renamed_response_file_local_path)


def _await_response_file_creation(api, survey_id, progress_id):
    status = 'inProgress'
    file_id = None

    while status not in ['complete', 'failed']:
        time.sleep(QUALTRICS_API_EXPORT_RESPONSES_PROGRESS_TIMEOUT)

        data, file_id = api.get_response_export_progress(survey_id, progress_id)

        status = data['result']['status']

    if status == 'failed' or not file_id:
        raise QualtricsDataSerialisationException('Failed to complete export for progress_id {}'.format(progress_id))

    return api.get_response_export_file(survey_id, file_id)


def _get_survey_file_path(survey_id):
    file_path_and_name = os.path.join(os.path.abspath(os.getcwd()), '../data/', '{}.{}'.format(survey_id, FILE_EXTENSION_JSON))

    return file_path_and_name


def _get_response_file_path(survey_id, zipped=True):
    file_ext = FILE_EXTENSION_ZIP if zipped else FILE_EXTENSION_JSON
    file_path_and_name = os.path.join(os.path.abspath(os.getcwd()), '../data/', '{}_responses.{}'.format(survey_id, file_ext))

    return file_path_and_name
