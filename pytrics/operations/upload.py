from datetime import datetime

from requests import HTTPError
from progress.bar import Bar

from pytrics.common.constants import (
    QUALTRICS_API_BLOCK_TYPE_DEFAULT,
    QUALTRICS_API_PUBLISHED_SURVEY_URL_PATTERN,
    QUALTRICS_API_BLOCK_TYPE_STANDARD,
)
from pytrics.common.exceptions import QualtricsAPIException

from pytrics.qualtrics_api.client import QualtricsAPIClient
from pytrics.qualtrics_api.common import get_details_for_client


def create_survey(name, blocks, questions, language_code='EN'):
    '''
    Create a new survey with the specified blocks and questions

    1. create survey
    2. update default block (depends on questions supplied)
    3. create additional blocks as required (again depends on questions supplied)
    4. create questions, per question: build payloads (inc. display logic), assign to blocks, call api
    5. return survey_id
    '''
    assert blocks and questions, "You must provide lists of blocks and questions for the survey"

    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    survey_id = default_block_id = None

    try:
        survey_id, default_block_id = api.create_survey(name, language_code)
    except (QualtricsAPIException, AssertionError, HTTPError) as ex:
        raise QualtricsAPIException(ex)

    if not survey_id:
        raise QualtricsAPIException('API call create_survey failed to return survey_id')

    if not default_block_id:
        raise QualtricsAPIException('API call create_survey failed to return default_block_id')

    block_ids_dict = {
        1: default_block_id
    }

    blockBar = Bar('Creating Blocks', max=len(blocks))

    for index, block in enumerate(blocks):
        blockBar.next()

        if index == 0:
            try:
                api.update_block(survey_id, default_block_id, block['description'], QUALTRICS_API_BLOCK_TYPE_DEFAULT)
            except (AssertionError, HTTPError) as ex:
                raise QualtricsAPIException(ex)
        else:
            try:
                _, new_block_id = api.create_block(survey_id, block['description'], QUALTRICS_API_BLOCK_TYPE_STANDARD)

                block_ids_dict[index + 1] = new_block_id
            except (AssertionError, HTTPError) as ex:
                raise QualtricsAPIException(ex)

    blockBar.finish()

    questionBar = Bar('Creating Questions', max=len(questions))

    for question in questions:
        questionBar.next()

        question_payload = api.build_question_payload(question, survey_id, include_display_logic=True)

        try:
            block_id = block_ids_dict[question['block_number']]
        except KeyError:
            block_id = block_ids_dict[1]

        try:
            api.create_question(survey_id, question_payload, block_id)
        except (AssertionError, HTTPError) as ex:
            raise QualtricsAPIException(ex)

    questionBar.finish()

    return survey_id


def publish_survey(survey_id, survey_name):
    '''
    Activate and publish the specified survey so it's available to take online
    '''
    try:
        assert survey_id.strip()
        assert survey_name.strip()
    except (AssertionError, AttributeError):
        raise AssertionError('You must provide string values for survey_id and survey_name')

    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    survey_description = '{}_{}'.format(
        survey_name,
        datetime.now().strftime("%Y-%m-%d_%H.%M.%S%p")
    )

    try:
        api.update_survey(survey_id, True)

        version_id, version_number, creation_date = api.publish_survey(survey_id, survey_description)
    except (AssertionError, HTTPError) as ex:
        raise QualtricsAPIException(ex)

    survey_url = QUALTRICS_API_PUBLISHED_SURVEY_URL_PATTERN.format(survey_id)

    return survey_url, version_id, version_number, creation_date
