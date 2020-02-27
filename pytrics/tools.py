'''
The main entry point to this module, allows for the creation of surveys
and the retrieval of responses. Also provides some helper functions.
'''
import json
import os

from pytrics.common.constants import (
    ENV_VAR_ABSOLUTE_PATH_TO_DATA_DIR,
    FILE_EXTENSION_JSON,
)
from pytrics.common.exceptions import (
    QualtricsAPIException,
    QualtricsDataSerialisationException,
)

from pytrics.operations.download import get_survey_and_response_data
from pytrics.operations.upload import (
    copy_survey,
    create_survey,
    describe_survey,
    publish_survey,
)
from pytrics.survey_definition.agriculture import (
    ET_en,
    IN_en,
    KE_en,
    NG_en,
    TZ_en,
)


class Tools:

    def __init__(self):
        self.country_to_definition = {
            'et': ET_en,
            'in': IN_en,
            'ke': KE_en,
            'ng': NG_en,
            'tz': TZ_en,
        }
        self.abs_path_to_data = os.environ.get(ENV_VAR_ABSOLUTE_PATH_TO_DATA_DIR, '')
        if not self.abs_path_to_data:
            raise QualtricsDataSerialisationException('Unable to find absolute path to data directory in ENV')

    def create_survey_from_definition(self, survey_name, country_iso_2):
        '''
        Create a survey from the specified pre-defined template.

        The survey will appear in Qualtrics with the specified survey_name.

        The PPI (Poverty Probability Index) questions will vary depending
        on the country_iso_2 code provided.

        Expects a name and lower case two character iso country code from one of the
        countries we have provided survey definitions for.

        Example usage: create_survey_from_definition('My New Survey Name', 'et')
        '''
        definition_class = self.country_to_definition[country_iso_2]

        blocks = definition_class.get_blocks()
        questions = definition_class.get_questions()

        try:
            survey_id = create_survey(survey_name, blocks, questions)
            survey_url = publish_survey(survey_id, survey_name)
        except QualtricsAPIException as qex:
            raise qex

        return survey_url

    def retrieve_survey_response_data(self, survey_id, process_responses=True):
        '''
        Downloads both the survey definition and any recorded responses.

        Saves both to local disk.

        Both files are returned as you may wish/need to use the survey definition
        to understand and process the content of the response data file.

        Expects the the Qualtrics survey identifier.

        Optional 2nd argument can be passed as False to NOT process the responses into
        a more readable/usable form. Default is True for this parameter.

        Example usage: retrieve_survey_response_data('SV_123456abcdef')
        '''
        survey_file_name = response_file_name = None

        try:
            survey_file_name, response_file_name, unzipped_response_file_name, processed_response_file_name = get_survey_and_response_data(survey_id, self.abs_path_to_data, process_responses)
        except QualtricsAPIException as qex:
            raise qex

        return survey_file_name, response_file_name, unzipped_response_file_name, processed_response_file_name

    @staticmethod
    def copy(template_survey_id, new_survey_name):
        '''
        Create a copy of an existing survey in your Qualtrics account.

        Expects the the Qualtrics survey identifier, allows you to specify the new survey name.

        Example usage: copy('SV_123456abcdef', 'My New Survey Name')
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

    def describe(self, survey_id):
        '''
        Describe an existing survey, expects the Qualtrics survey identifier.

        Creates a JSON file on your local disk for review and analysis.

        Example usage: describe('SV_123456abcdef')
        '''
        detailed_survey_json = describe_survey(survey_id)
        survey_name = detailed_survey_json['detail']['survey']['result']['name']

        detailed_survey_json_file_path = '{}/{}_{}.json'.format(self.abs_path_to_data, survey_name, survey_id)

        with open(detailed_survey_json_file_path, 'w') as detailed_survey_json_file:
            json.dump(detailed_survey_json, detailed_survey_json_file, indent=4, sort_keys=True)

    def summarise_definition(self, country_iso_2):
        '''
        Given a lower case two character iso country code from those supported this
        function writes a summary of the relevant survey definition to disk in a json file.

        This could be used as a call script for researchers, or to help visualise the
        shape and size of the survey and the order of it's questions.

        Example usage: summarise_definition('et')
        '''
        definition_class = self.country_to_definition[country_iso_2]

        name = definition_class.get_name()
        blocks = definition_class.get_blocks()
        questions = definition_class.get_questions()

        summarised_blocks = {}
        summarised_questions = {}

        for block in blocks:
            key = block['position']
            value = block['description']
            summarised_blocks[key] = value

        for question in questions:
            key = question['tag_number']
            value = {
                'block': question['block_number'],
                'label': question['label'],
                'text': question['text']
            }
            summarised_questions[key] = value

        summary = {
            'survey': name,
            'blocks': summarised_blocks,
            'questions': summarised_questions
        }

        summary_file_path_and_name = '{}/{}_definition_summary.{}'.format(self.abs_path_to_data, country_iso_2, FILE_EXTENSION_JSON)

        with open(summary_file_path_and_name, 'w') as summary_json_file:
            json.dump(summary, summary_json_file, indent=4, sort_keys=False)
