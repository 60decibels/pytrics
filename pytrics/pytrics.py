'''
Intended to hold code that uses qualtrics_api to create surveys
So we can encapsulate our use of the qualtrics_api module
and keep that module clean for provision to Gates/OS
'''
import os
import json

from common.exceptions import QualtricsAPIException

from operations.upload import (
    copy_survey,
    create_survey,
    describe_survey,
    publish_survey,
)
from survey_definition.core_insights import (
    IN_en,
    IN_hi,
)


language_to_definition = {
    'en': IN_en,
    'hi': IN_hi,
}


def copy(template_survey_id, new_survey_name):
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
    detailed_survey_json = describe_survey(survey_id)
    survey_name = detailed_survey_json['detail']['survey']['result']['name']

    detailed_survey_json_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../data/', '{}_{}.json'.format(survey_name, survey_id))
    # os.path.join(os.path.abspath(os.getcwd()), '/data/')

    with open(detailed_survey_json_file_path, 'w') as detailed_survey_json_file:
        json.dump(detailed_survey_json, detailed_survey_json_file, indent=4, sort_keys=True)


def serialise_in_qualtrics_from_definition(survey_name, language_iso_2):
    definition_class = language_to_definition[language_iso_2]

    blocks = definition_class.get_blocks()
    questions = definition_class.get_questions()

    try:
        survey_id = create_survey(survey_name, blocks, questions)
        survey_url = publish_survey(survey_id, survey_name)
    except QualtricsAPIException as qex:
        raise qex

    return survey_url
