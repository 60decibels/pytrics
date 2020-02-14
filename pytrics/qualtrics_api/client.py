import json
import re
import requests

from pytrics.common.constants import (
    QUALTRICS_API_BLOCK_VISIBILITY_EXPANDED,
    QUALTRICS_API_PATH_BLOCKS,
    QUALTRICS_API_PATH_EXPORT_RESPONSES,
    QUALTRICS_API_PATH_QUESTIONS,
    QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
    QUALTRICS_API_PATH_SURVEY_VERSIONS,
    QUALTRICS_API_PATH_SURVEYS,
    QUALTRICS_API_REGEX_BLOCK_ID,
    QUALTRICS_API_REGEX_QUESTION_ID,
    QUALTRICS_API_REGEX_SURVEY_ID,
    QUALTRICS_API_REQUIRED_QUESTION_PARAM_KEYS,
    QUALTRICS_API_REQUIRED_QUESTION_PAYLOAD_KEYS,
    QUALTRICS_API_SUPPORTED_ANSWER_SELECTORS,
    QUALTRICS_API_SUPPORTED_BLOCK_TYPES,
    QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_CHOICE_LOCATORS,
    QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_CONJUNCTIONS,
    QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_OPERATORS,
    QUALTRICS_API_SUPPORTED_LANGUAGE_CODES,
    QUALTRICS_API_SUPPORTED_PROJECT_CATEGORIES,
    QUALTRICS_API_SUPPORTED_QUESTION_TYPES,
)
from pytrics.common.exceptions import QualtricsAPIException


class QualtricsAPIClient():
    """
    Wrapper for interacting with the Qualtrics API
    """
    def __init__(self, base_api_url, auth_token):
        if not base_api_url:
            raise QualtricsAPIException('base_api_url cannot be null')

        if not auth_token:
            raise QualtricsAPIException('auth_token cannot be null')

        self.base_api_url = base_api_url
        self.auth_token = auth_token

        self._survey_id_regex = re.compile(QUALTRICS_API_REGEX_SURVEY_ID)
        self._question_id_regex = re.compile(QUALTRICS_API_REGEX_QUESTION_ID)
        self._block_id_regex = re.compile(QUALTRICS_API_REGEX_BLOCK_ID)

    def build_question_display_logic(self, controlling_question_ids, choices, operators, conjunctions, locators): # pylint: disable=too-many-arguments
        try:
            assert controlling_question_ids
            assert choices
            assert len(controlling_question_ids) == len(choices) == len(operators) == len(conjunctions) == len(locators)
            for operator in operators:
                assert operator.strip() in QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_OPERATORS
            for conjunction in conjunctions:
                assert conjunction in QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_CONJUNCTIONS
            for locator in locators:
                assert locator in QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_CHOICE_LOCATORS
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide valid lists of matching length for controlling_question_ids, choices, operators, conjunctions and locators parameters')

        for controlling_question_id in controlling_question_ids:
            self._validate_question_id(controlling_question_id)

        display_logic = {
            '0': {},
            'Type': 'BooleanExpression',
            'inPage': False
        }

        for index, controlling_question_id in enumerate(controlling_question_ids):
            locator = locators[index]
            choice = choices[index]
            operator = operators[index]
            conjunction = conjunctions[index]

            if locator:
                locator_string = 'q://{controlling_question_id}/{locator}/{choice}'.format(
                    controlling_question_id=controlling_question_id,
                    locator=locator,
                    choice=choice
                )
                conditional = 'is Selected'
            else:
                locator_string = 'q://{controlling_question_id}/{choice}'.format(
                    controlling_question_id=controlling_question_id,
                    choice=choice
                )
                conditional = 'is True'

            description = 'If {controlling_question_id} {choice} {conditional}'.format(
                controlling_question_id=controlling_question_id,
                choice=choice,
                conditional=conditional
            )

            condition = {
                'ChoiceLocator': locator_string,
                'Description': description,
                'LeftOperand': locator_string,
                'LogicType': 'Question',
                'Operator': operator,
                'QuestionID': controlling_question_id,
                "QuestionIDFromLocator": controlling_question_id,
                "QuestionIsInLoop": "no",
                'Type': 'Expression'
            }

            if operator == 'EqualTo':
                condition['RightOperand'] = '1'

            if index > 0:
                condition['Conjuction'] = conjunction

            display_logic['0'][str(index)] = condition

        display_logic['0']['Type'] = 'If'

        return display_logic

    def build_question_payload(self, question_params=None, survey_id=None, include_display_logic=True): # pylint: disable=too-many-branches, too-many-statements
        try:
            assert question_params

            keys_present = True
            for required_key in QUALTRICS_API_REQUIRED_QUESTION_PARAM_KEYS:
                if required_key not in question_params.keys():
                    keys_present = False

            assert keys_present

            assert question_params['text'].strip()
            assert isinstance(question_params['tag_number'], int)
            assert question_params['type'].strip() in QUALTRICS_API_SUPPORTED_QUESTION_TYPES
            assert question_params['answer_selector'].strip() in QUALTRICS_API_SUPPORTED_ANSWER_SELECTORS
            assert question_params['label'].strip()
            assert isinstance(question_params['block_number'], int)
        except (KeyError, AssertionError, AttributeError):
            raise AssertionError('Please ensure the question_params dictionary argument is valid...')

        # Constructing question payload dictionary
        payload = {
            'QuestionText': question_params['text'].strip(),
            'DataExportTag': 'Q{}'.format(question_params['tag_number']),
            'QuestionType': question_params['type'],
            'Selector': question_params['answer_selector'],
            'Configuration': {
                'QuestionDescriptionOption': 'SpecifyLabel'
            },
            'QuestionDescription': question_params['label'].strip(),
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF' if not question_params['is_mandatory'] else 'ON',
                    'ForceResponseType': 'ON',
                    'Type': 'None'
                }
            },
            'Language': question_params['translations']
        }

        if 'answer_sub_selector' in question_params.keys():
            payload['SubSelector'] = question_params['answer_sub_selector']

        if 'additional_validation_settings' in question_params.keys():
            for key, value in question_params['additional_validation_settings'].items():
                payload['Validation']['Settings'][key] = value

        # Applying choices, order, recoding and variable naming to payload dictionary

        if 'choices' in question_params.keys():
            payload['Choices'] = question_params['choices']

        if 'choice_order' in question_params.keys():
            payload['ChoiceOrder'] = question_params['choice_order']

        if 'recode_values' in question_params.keys():
            payload['RecodeValues'] = question_params['recode_values']

        if 'variable_naming' in question_params.keys():
            payload['VariableNaming'] = question_params['variable_naming']

        if 'column_labels' in question_params.keys():
            payload['ColumnLabels'] = question_params['column_labels']

        # Processing question display_logic
        if include_display_logic:
            if 'display_logic' in question_params.keys():
                question_display_logic_dict = question_params['display_logic']

                if question_display_logic_dict:
                    # unpack dict entries for use as params below
                    controlling_question_labels = question_display_logic_dict['controlling_question_labels']
                    choices = question_display_logic_dict['choices']
                    operators = question_display_logic_dict['operators']
                    conjunctions = question_display_logic_dict['conjunctions']
                    locators = question_display_logic_dict['locators']

                    # the QIDn of this question could vary, so get this from the survey by the question label
                    controlling_question_ids = []
                    for controlling_question_label in controlling_question_labels:
                        controlling_question_id, _ = self.find_question_in_survey_by_label(survey_id, controlling_question_label)
                        controlling_question_ids.append(controlling_question_id)

                    # finally add a 'DisplayLogic' key with a value of the built display logic to this question payload
                    payload['DisplayLogic'] = self.build_question_display_logic(controlling_question_ids, choices, operators, conjunctions, locators)

        return payload

    def create_block(self, survey_id, description, block_type):
        try:
            assert survey_id.strip()
            assert description.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and description')

        assert block_type in QUALTRICS_API_SUPPORTED_BLOCK_TYPES, 'Supplied block type is not supported.'

        self._validate_survey_id(survey_id)

        url = '{0}/{1}/{2}/{3}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
            survey_id,
            QUALTRICS_API_PATH_BLOCKS
        )

        body = json.dumps({
            'Type': block_type,
            'Description': description,
            'Options': {
                'BlockLocking': 'false',
                'RandomizeQuestions': 'false',
                'BlockVisibility': QUALTRICS_API_BLOCK_VISIBILITY_EXPANDED
            }
        })

        response = requests.post(
            url,
            data=body,
            headers=self._build_headers('POST')
        )

        response.raise_for_status()

        result = response.json()

        block_id = result['result']['BlockID']

        return result, block_id

    def create_question(self, survey_id, question_payload, block_id=None):
        try:
            assert survey_id.strip()
            assert question_payload
            assert isinstance(question_payload, dict)
            if block_id:
                assert block_id.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide a string value for survey_id and a dict for question_data')

        self._validate_survey_id(survey_id)
        self._validate_question_payload(question_payload)
        if block_id:
            self._validate_block_id(block_id)

        url = '{0}/{1}/{2}/{3}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
            survey_id,
            QUALTRICS_API_PATH_QUESTIONS
        )

        if block_id:
            url = '{0}?blockId={1}'.format(url, block_id)

        body = json.dumps(question_payload)

        response = requests.post(
            url,
            data=body,
            headers=self._build_headers('POST')
        )

        response.raise_for_status()

        result = response.json()

        question_id = result['result']['QuestionID']

        return result, question_id

    def create_response_export(self, survey_id):
        try:
            assert survey_id.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide a string value for survey_id')

        self._validate_survey_id(survey_id)

        url = '{0}/{1}/{2}/{3}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEYS,
            survey_id,
            QUALTRICS_API_PATH_EXPORT_RESPONSES,
        )

        body = json.dumps({
            'format': 'json'
        })

        response = requests.post(
            url,
            data=body,
            headers=self._build_headers('POST')
        )

        response.raise_for_status()

        result = response.json()
        progress_id = result['result']['progressId']

        return result, progress_id

    def create_survey(self, survey_name, language_code='EN', project_category='CORE'):
        try:
            assert survey_name.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide a string value for survey_name')

        assert language_code in QUALTRICS_API_SUPPORTED_LANGUAGE_CODES, 'Supplied language_code is not supported.'
        assert project_category in QUALTRICS_API_SUPPORTED_PROJECT_CATEGORIES, 'Supplied project_category is not supported.'

        url = '{0}/{1}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
        )

        body = json.dumps({
            'SurveyName': survey_name,
            'Language': language_code.upper(),
            'ProjectCategory': project_category.upper(),
        })

        response = requests.post(
            url,
            data=body,
            headers=self._build_headers('POST')
        )

        response.raise_for_status()

        result = response.json()

        survey_id = result['result']['SurveyID']
        default_block_id = result['result']['DefaultBlockID']

        return survey_id, default_block_id

    def delete_block(self, survey_id, block_id):
        try:
            assert survey_id.strip()
            assert block_id.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and block_id')

        self._validate_survey_id(survey_id)
        self._validate_block_id(block_id)

        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
            survey_id,
            QUALTRICS_API_PATH_BLOCKS,
            block_id,
        )

        response = requests.delete(
            url,
            headers=self._build_headers('DELETE')
        )

        response.raise_for_status()

    def find_question_in_survey_by_label(self, survey_id, question_label):
        survey_json = self.get_survey(survey_id)
        survey_dict = survey_json['result']

        for key, value in survey_dict['questions'].items():
            if value['questionLabel'] == question_label:
                return key, value

        return None, None

    def get_block(self, survey_id, block_id):
        try:
            assert survey_id.strip()
            assert block_id.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and block_id')

        self._validate_survey_id(survey_id)
        self._validate_block_id(block_id)

        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
            survey_id,
            QUALTRICS_API_PATH_BLOCKS,
            block_id,
        )

        response = requests.get(
            url,
            headers=self._build_headers('GET')
        )

        response.raise_for_status()

        return response.json()

    def get_question(self, survey_id, question_id):
        try:
            assert survey_id.strip()
            assert question_id.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and question_id')

        self._validate_survey_id(survey_id)
        self._validate_question_id(question_id)

        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
            survey_id,
            QUALTRICS_API_PATH_QUESTIONS,
            question_id,
        )

        response = requests.get(
            url,
            headers=self._build_headers('GET')
        )

        response.raise_for_status()

        return response.json()

    def get_response_export_file(self, survey_id, file_id):
        try:
            assert survey_id.strip()
            assert file_id.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and file_id')

        self._validate_survey_id(survey_id)

        url = '{0}/{1}/{2}/{3}/{4}/file'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEYS,
            survey_id,
            QUALTRICS_API_PATH_EXPORT_RESPONSES,
            file_id,
        )

        response = requests.get(
            url,
            headers=self._build_headers('GET')
        )

        response.raise_for_status()

        return response.content

    def get_response_export_progress(self, survey_id, progress_id):
        try:
            assert survey_id.strip()
            assert progress_id.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and progress_id')

        self._validate_survey_id(survey_id)

        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEYS,
            survey_id,
            QUALTRICS_API_PATH_EXPORT_RESPONSES,
            progress_id,
        )

        response = requests.get(
            url,
            headers=self._build_headers('GET')
        )

        response.raise_for_status()

        result = response.json()
        file_id = result['result']['fileId']

        return result, file_id

    def get_survey(self, survey_id):
        try:
            assert survey_id.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide a string value for survey_id')

        self._validate_survey_id(survey_id)

        url = '{0}/{1}/{2}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEYS,
            survey_id,
        )

        response = requests.get(
            url,
            headers=self._build_headers('GET')
        )

        response.raise_for_status()

        return response.json()

    def publish_survey(self, survey_id, description):
        try:
            assert survey_id.strip()
            assert description.strip()
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and description')

        self._validate_survey_id(survey_id)

        url = '{0}/{1}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_VERSIONS.format(survey_id),
        )

        body = json.dumps({
            'Description': description,
            'Published': True,
        })

        response = requests.post(
            url,
            data=body,
            headers=self._build_headers('POST')
        )

        response.raise_for_status()

        result = response.json()

        version_id = result['result']['metadata']['versionID']
        version_number = result['result']['metadata']['versionNumber']
        creation_date = result['result']['metadata']['creationDate']

        return version_id, version_number, creation_date

    def update_block(self, survey_id, block_id, block_description, block_type):
        try:
            assert survey_id.strip()
            assert block_id.strip()
            assert block_description.strip()
            assert block_type.strip() in QUALTRICS_API_SUPPORTED_BLOCK_TYPES
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and block_id')

        self._validate_survey_id(survey_id)
        self._validate_block_id(block_id)

        body = json.dumps({
            'Type': block_type,
            'Description': block_description,
            'Options': {
                'BlockLocking': 'false',
                'RandomizeQuestions': 'false',
                'BlockVisibility': QUALTRICS_API_BLOCK_VISIBILITY_EXPANDED
            }
        })

        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
            survey_id,
            QUALTRICS_API_PATH_BLOCKS,
            block_id,
        )

        response = requests.put(
            url,
            data=body,
            headers=self._build_headers('PUT')
        )

        response.raise_for_status()

    def update_question(self, survey_id, question_id, question_payload):
        try:
            assert survey_id.strip()
            assert question_id.strip()
            assert question_payload
            assert isinstance(question_payload, dict)
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide string values for survey_id and question_id and a dict for question_payload')

        self._validate_survey_id(survey_id)
        self._validate_question_id(question_id)
        self._validate_question_payload(question_payload)

        body = json.dumps(question_payload)

        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEY_DEFINITIONS,
            survey_id,
            QUALTRICS_API_PATH_QUESTIONS,
            question_id,
        )

        response = requests.put(
            url,
            data=body,
            headers=self._build_headers('PUT')
        )

        response.raise_for_status()

    def update_survey(self, survey_id, is_active):
        try:
            assert survey_id.strip()
            assert isinstance(is_active, bool)
        except (AssertionError, AttributeError):
            raise AssertionError('You must provide a string value for survey_id and a bool for is_active')

        self._validate_survey_id(survey_id)

        body = json.dumps({
            'isActive': is_active
        })

        url = '{0}/{1}/{2}'.format(
            self.base_api_url,
            QUALTRICS_API_PATH_SURVEYS,
            survey_id,
        )

        response = requests.put(
            url,
            data=body,
            headers=self._build_headers('PUT')
        )

        response.raise_for_status()

    def _build_headers(self, method):
        """
        Constructs a dictionary which will be used as the request headers for all API interactions
        """
        if method not in ['GET', 'DELETE', 'POST', 'PUT']:
            raise QualtricsAPIException('Client only supports GET, DELETE, POST and PUT methods.')

        headers = {
            'X-API-TOKEN': self.auth_token,
        }

        if method in ['POST', 'PUT']:
            headers['Content-Type'] = 'application/json'

        return headers

    def _validate_block_id(self, block_id):
        block_id_match = self._block_id_regex.match(block_id)
        if not block_id_match:
            raise AssertionError('The format of block_id is incorrect.')

    def _validate_question_id(self, question_id):
        question_id_match = self._question_id_regex.match(question_id)
        if not question_id_match:
            raise AssertionError('The format of question_id is incorrect.')

    @staticmethod
    def _validate_question_payload(question_payload=None):
        if not question_payload:
            raise AssertionError('The question payload is falsy.')

        missing_keys = []
        for required_key in QUALTRICS_API_REQUIRED_QUESTION_PAYLOAD_KEYS:
            if required_key not in question_payload.keys():
                missing_keys.append(required_key)

        if missing_keys:
            raise AssertionError('The question payload is invalid, keys missing: {}'.format(missing_keys))

        if 'Choices' in question_payload.keys():
            if 'ChoiceOrder' not in question_payload.keys():
                raise AssertionError('The question payload has Choices but no ChoiceOrder')

        if 'ChoiceOrder' in question_payload.keys():
            if 'Choices' not in question_payload.keys():
                raise AssertionError('The question payload has ChoiceOrder but no Choices')

        question_type = question_payload['QuestionType']
        selector = question_payload['Selector']

        if question_type == 'MC' and selector in ['SAVR', 'SAHR']:
            sub_selector = None

            if 'SubSelector' not in question_payload.keys():
                raise AssertionError('SubSelector missing from payload when expected')

            sub_selector = question_payload['SubSelector']

            if sub_selector != 'TX':
                raise AssertionError('The sub_selector: {} is invalid for question_type: {} and selector: {}'.format(
                    sub_selector,
                    question_type,
                    selector
                ))

    def _validate_survey_id(self, survey_id):
        survey_id_match = self._survey_id_regex.match(survey_id)
        if not survey_id_match:
            raise AssertionError('The format of survey_id is incorrect.')
