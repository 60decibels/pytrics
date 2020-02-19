import json
import os
import time
from zipfile import ZipFile

from requests import HTTPError

from pytrics.common.constants import (
    FILE_EXTENSION_JSON,
    FILE_EXTENSION_ZIP,
    QUALTRICS_API_EXPORT_RESPONSES_PROGRESS_TIMEOUT,
    QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT,
)
from pytrics.common.exceptions import (
    QualtricsAPIException,
    QualtricsDataSerialisationException,
)

from pytrics.qualtrics_api.client import QualtricsAPIClient
from pytrics.qualtrics_api.common import get_details_for_client


def get_survey_data(survey_id, abs_path_to_data_dir):
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    try:
        file_path_and_name = save_survey_to_file(api, survey_id, abs_path_to_data_dir)
    except (QualtricsAPIException, QualtricsDataSerialisationException) as qex:
        raise qex

    return file_path_and_name


def get_survey_and_response_data(survey_id, abs_path_to_data_dir, process_responses=False):
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    try:
        survey_file_name = save_survey_to_file(api, survey_id, abs_path_to_data_dir)
    except (QualtricsAPIException, QualtricsDataSerialisationException) as qex:
        raise qex

    try:
        response_file_name = save_responses_to_file(api, survey_id, abs_path_to_data_dir)
    except QualtricsDataSerialisationException as qex:
        raise qex

    try:
        unzipped_response_file_name = _unzip_response_file(survey_id, abs_path_to_data_dir)
    except QualtricsDataSerialisationException as qex:
        raise qex

    processed_response_file_name = None
    if process_responses:
        try:
            processed_response_file_name = _process_response_data(survey_id, abs_path_to_data_dir)
        except QualtricsDataSerialisationException as qex:
            raise qex

    return survey_file_name, response_file_name, unzipped_response_file_name, processed_response_file_name


def save_survey_to_file(api, survey_id, abs_path_to_data_dir):
    try:
        survey_json = api.get_survey(survey_id)
    except (AssertionError, HTTPError) as ex:
        raise QualtricsAPIException(ex)

    file_path_and_name = _get_survey_file_path(survey_id, abs_path_to_data_dir)

    try:
        with open(file_path_and_name, mode='w+', newline='', encoding='utf-8-sig') as survey_file:
            json.dump(survey_json, survey_file)

    except Exception as ex:
        raise QualtricsDataSerialisationException(ex)

    return file_path_and_name


def save_responses_to_file(api, survey_id, abs_path_to_data_dir, progress_id=None, retries=0):
    file_path_and_name = _get_response_file_path(survey_id, abs_path_to_data_dir)
    response_bytes = None

    if retries == 0:
        _, progress_id = api.create_response_export(survey_id)

    try:
        response_bytes = _await_response_file_creation(api, survey_id, progress_id)
    except (QualtricsDataSerialisationException, HTTPError, KeyError):
        if retries < QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT:
            retries += 1
            # Recurse to get new progress_id and try again
            save_responses_to_file(api, survey_id, abs_path_to_data_dir, progress_id, retries)
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


def _get_survey_file_path(survey_id, abs_path_to_data_dir):
    file_path_and_name = '{}/{}.{}'.format(abs_path_to_data_dir, survey_id, FILE_EXTENSION_JSON)

    return file_path_and_name


def _get_response_file_path(survey_id, abs_path_to_data_dir, zipped=True):
    file_ext = FILE_EXTENSION_ZIP if zipped else FILE_EXTENSION_JSON
    file_path_and_name = '{}/{}_responses.{}'.format(abs_path_to_data_dir, survey_id, file_ext)

    return file_path_and_name


def _get_processed_response_file_path(survey_id, abs_path_to_data_dir):
    file_ext = FILE_EXTENSION_JSON
    file_path_and_name = '{}/{}_responses_processed.{}'.format(abs_path_to_data_dir, survey_id, file_ext)

    return file_path_and_name


def _unzip_response_file(survey_id, abs_path_to_data_dir):
    '''
    Response files are zips containing single .json file named after survey in qualtrics

    So extract to .json & rename to associate with the survey .json

    If no responses are yet recorded against a survey the zip is empty. In this case we
    write an empty responses json file to disk to explicitly indicate processing completed
    '''
    response_file_path = _get_response_file_path(survey_id, abs_path_to_data_dir, zipped=True)
    unzipped_response_file_path = _get_response_file_path(survey_id, abs_path_to_data_dir, zipped=False)

    with ZipFile(response_file_path, 'r') as zipped:
        infolist = zipped.infolist()

        if not infolist:
            empty_responses_json = {"responses":[]}

            try:
                with open(unzipped_response_file_path, mode='w') as empty_response_file:
                    json.dump(empty_responses_json, empty_response_file)
            except QualtricsDataSerialisationException as ex:
                raise QualtricsDataSerialisationException(ex)

        for info in infolist:
            extract_path = os.path.join(os.path.abspath(os.getcwd()), '../data')

            zipped.extract(info.filename, path=extract_path)

            extracted_file_local_path = '{0}/{1}'.format(extract_path, info.filename)

            os.rename(extracted_file_local_path, unzipped_response_file_path)

        return unzipped_response_file_path


def _process_response_data(survey_id, abs_path_to_data_dir):
    survey_questions = _get_survey_questions_dict_from_file(survey_id, abs_path_to_data_dir)
    cleaned_responses = _get_cleaned_responses_dict_from_file(survey_id, abs_path_to_data_dir)

    # now process the response data - experimental code hence use of broad except
    try: # pylint: disable=too-many-nested-blocks
        processed_responses = []
        for response in cleaned_responses:
            responseIdAsKey = response.pop('responseId')

            processed = {
                responseIdAsKey: {}
            }

            for k, v in response.items():
                question_id = k.split("_")[0]
                rest_of_identifier = k.replace(question_id, '')

                label = survey_questions[question_id]['questionLabel']

                if len(k.split("_")) == 1:
                    qtype = survey_questions[question_id]['questionType']['type']

                    if qtype == 'MC':
                        choices = survey_questions[question_id]['choices']
                        values = None

                        if isinstance(v, list):
                            for val in v:
                                values = []
                                value = choices[val]['choiceText']
                                values.append(value)
                        else:
                            values = choices[str(v)]['choiceText']

                        processed[responseIdAsKey][label] = values

                    else:
                        processed[responseIdAsKey][question_id] = v

                elif len(k.split("_")) == 3:
                    try:
                        sub_id = int(k.split("_")[1])
                        sub_label = survey_questions[question_id]['choices'][str(sub_id)]['choiceText'].replace(' ', '_').lower()
                        combined_label = '{}_{}'.format(label, sub_label)
                        processed[responseIdAsKey][combined_label] = v
                    except ValueError:
                        new_key = '{}{}'.format(label, rest_of_identifier)
                        processed[responseIdAsKey][new_key] = v

                else:
                    new_key = '{}{}'.format(label, rest_of_identifier)
                    processed[responseIdAsKey][new_key] = v

            processed_responses.append(processed)

        # now write processed_responses to a new json file in same location on disk
        processed_responses_file_path = _get_processed_response_file_path(survey_id, abs_path_to_data_dir)

        # write to json file
        with open(processed_responses_file_path, 'w') as processed_responses_file:
            json.dump(processed_responses, processed_responses_file)

        return processed_responses_file_path
    except Exception as ex:
        print(ex)
        raise QualtricsDataSerialisationException(ex)

    return None


def _get_survey_questions_dict_from_file(survey_id, abs_path_to_data_dir):
    survey_file_path = _get_survey_file_path(survey_id, abs_path_to_data_dir)

    with open(survey_file_path, mode='r', encoding='utf-8-sig') as survey_json_file:
        survey_dict = json.load(survey_json_file)

        return survey_dict['result']['questions']


def _get_cleaned_responses_dict_from_file(survey_id, abs_path_to_data_dir):
    unzipped_response_file_path = _get_response_file_path(survey_id, abs_path_to_data_dir, zipped=False)

    with open(unzipped_response_file_path, mode='r', encoding='utf-8-sig') as response_json_file:
        response_dict = json.load(response_json_file)

        # clean up the responses (remove meta data and extraneous information)
        cleaned_responses = []
        for response in response_dict['responses']:
            raw_values = response['values']
            cleaned_values = {k:raw_values[k] for k in raw_values if k.startswith('QID')}
            cleaned_values['responseId'] = response['responseId']
            cleaned_responses.append(cleaned_values)

        return cleaned_responses
