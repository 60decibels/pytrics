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


def describe_survey(survey_id):
    '''
    Describe an existing survey, outputs a json file containing detailed information
    to assist when creating and forming your own surveys

    1. get_survey
    2. for each block, get_block
    3. for each question, get_question
    4. collate into one big json blob and return
    '''
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    detailed_survey_dict = {
        'survey_id': survey_id,
        'detail': {}
    }

    # 1.
    survey_json = api.get_survey(survey_id)
    detailed_survey_dict['detail']['survey'] = survey_json

    # 2.
    block_ids = []
    blocks = []
    blocks_sub_doc = survey_json['result']['blocks']

    for key, _ in blocks_sub_doc.items():
        block_ids.append(key)

    for bid in block_ids:
        blocks.append(api.get_block(survey_id, bid))

    detailed_survey_dict['detail']['blockIds'] = block_ids
    detailed_survey_dict['detail']['blocks'] = blocks

    # 3.
    question_ids = []
    questions = []
    export_col_map = survey_json['result']['exportColumnMap']

    for _, val in export_col_map.items():
        question_ids.append(val['question'])

    for qid in question_ids:
        questions.append(api.get_question(survey_id, qid))

    detailed_survey_dict['detail']['questionIds'] = question_ids
    detailed_survey_dict['detail']['questions'] = questions

    # 4.
    return detailed_survey_dict


def copy_survey(template_survey_id, new_survey_name, language_code='EN'): # pylint: disable=too-many-branches, too-many-statements
    '''
    Copy an existing survey and give it the specified new name

    1. create new survey
    2. get template survey
    3. copy blocks
    4. copy questions
    5. return new survey_id
    '''
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    new_survey_id = default_block_id = None

    # 1.
    try:
        new_survey_id, default_block_id = api.create_survey(new_survey_name, language_code)
    except (QualtricsAPIException, AssertionError, HTTPError) as ex:
        raise QualtricsAPIException(ex)

    if not new_survey_id:
        raise QualtricsAPIException('API call create_survey failed to return survey_id')

    if not default_block_id:
        raise QualtricsAPIException('API call create_survey failed to return default_block_id')

    # 2.
    template_survey_json = api.get_survey(template_survey_id)

    template_blocks = {}
    blocks_sub_doc = template_survey_json['result']['blocks']

    for key, _ in blocks_sub_doc.items():
        template_blocks[key] = None

    for key, _ in template_blocks.items():
        template_blocks[key] = api.get_block(template_survey_id, key)

    template_questions = {}
    export_col_map = template_survey_json['result']['exportColumnMap']

    for _, val in export_col_map.items():
        template_questions[val['question']] = None

    for key, _ in template_questions.items():
        template_questions[key] = api.get_question(template_survey_id, key)

    # 3.
    index = 0
    block_id_mapping = {}
    question_id_to_new_block_id_mapping = {}
    for key, value in template_blocks.items():
        description = value['result']['Description']

        if index == 0:
            try:
                api.update_block(new_survey_id, default_block_id, description, QUALTRICS_API_BLOCK_TYPE_DEFAULT)
                new_block_id = default_block_id
            except (AssertionError, HTTPError) as ex:
                raise QualtricsAPIException(ex)

        else:
            try:
                block_type = value['result']['Type']
                _, new_block_id = api.create_block(new_survey_id, description, block_type)
            except (AssertionError, HTTPError) as ex:
                raise QualtricsAPIException(ex)

        block_id_mapping[key] = new_block_id

        block_elements = value['result']['BlockElements']
        for block_element in block_elements:
            question_id_to_new_block_id_mapping[block_element['QuestionID']] = new_block_id

        index += 1

    # 4.
    for key, value in template_questions.items():
        new_question_payload = value['result']
        new_question_id = value['result']['QuestionID']
        new_block_id = question_id_to_new_block_id_mapping[new_question_id]

        _, new_question_id = api.create_question(new_survey_id, new_question_payload, new_block_id)

    # 5.
    return new_survey_id


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
