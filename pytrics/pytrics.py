'''
The main entry point to this module, allows for the creation of surveys
and the retrieval of responses.
'''
import json
import os
import pprint

from common.exceptions import QualtricsAPIException

from operations.download import get_survey_and_response_data
from operations.upload import (
    copy_survey,
    create_survey,
    describe_survey,
    publish_survey,
)
from survey_definition.agriculture import (
    ET_en,
    IN_en,
    KE_en,
    NG_en,
    TZ_en,
    XX_en,
)


country_to_definition = {
    'et': ET_en,
    'in': IN_en,
    'ke': KE_en,
    'ng': NG_en,
    'tz': TZ_en,
    'xx': XX_en,
}


def create_survey_from_definition(survey_name, country_iso_2):
    '''
    Create a survey from the specified pre-defined template.

    The survey will appear in Qualtrics with the specified survey_name.

    The PPI (Poverty Probability Index) questions will vary depending
    on the country_iso_2 code provided.
    '''
    definition_class = country_to_definition[country_iso_2]

    blocks = definition_class.get_blocks()
    questions = definition_class.get_questions()

    try:
        survey_id = create_survey(survey_name, blocks, questions)
        survey_url = publish_survey(survey_id, survey_name)
    except QualtricsAPIException as qex:
        raise qex

    return survey_url


def retrieve_survey_response_data(survey_id, process_responses=False):
    '''
    Downloads both the survey definition and any recorded responses.

    Saves both to local disk.

    Both files are returned as you may wish/need to use the survey definition
    to understand and process the content of the response data file.
    '''
    survey_file_name = response_file_name = None

    try:
        survey_file_name, response_file_name, unzipped_response_file_name, processed_response_file_name = get_survey_and_response_data(survey_id, process_responses)
    except QualtricsAPIException as qex:
        raise qex

    return survey_file_name, response_file_name, unzipped_response_file_name, processed_response_file_name


def copy(template_survey_id, new_survey_name):
    '''
    Create a copy of an existing survey in your Qualtrics account.

    Allows you to specify the new survey name.
    '''
    try:
        assert template_survey_id.strip()
        assert new_survey_name.strip()
    except (AssertionError, AttributeError):
        raise AssertionError('You must provide string values for both template_survey_id and new_survey_name')

    try:
        new_survey_id = copy_survey(template_survey_id, new_survey_name)
    except QualtricsAPIException as qex:
        raise qex

    return new_survey_id


def describe(survey_id):
    '''
    Describe an existing survey.

    Creates a JSON file on your local disk for review and analysis.
    '''
    detailed_survey_json = describe_survey(survey_id)
    survey_name = detailed_survey_json['detail']['survey']['result']['name']

    detailed_survey_json_file_path = os.path.join(os.path.abspath(os.getcwd()), '../data/', '{}_{}.json'.format(survey_name, survey_id))

    with open(detailed_survey_json_file_path, 'w') as detailed_survey_json_file:
        json.dump(detailed_survey_json, detailed_survey_json_file, indent=4, sort_keys=True)


def summarise_definition(country_iso_2):
    definition_class = country_to_definition[country_iso_2]

    blocks = definition_class.get_blocks()
    questions = definition_class.get_questions()

    pp = pprint.PrettyPrinter(indent=4)

    summarised_blocks = [('Block Number', 'Block Name')]
    summarised_questions = [('Block Number', 'Question Label', 'Question Text')]

    for block in blocks:
        summarised_blocks.append((block['position'], block['description'],))

    for question in questions:
        summarised_questions.append((question['block_number'], question['label'], question['text']))

    pp.pprint(summarised_blocks)

    pp.pprint(summarised_questions)
