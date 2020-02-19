ENV_VAR_QUALTRICS_API_BASE_URL = 'QUALTRICS_API_BASE_URL'
ENV_VAR_QUALTRICS_API_AUTH_TOKEN = 'QUALTRICS_API_AUTH_TOKEN'
ENV_VAR_ABSOLUTE_PATH_TO_DATA_DIR = 'ABSOLUTE_PATH_TO_DATA_DIR'

FILE_EXTENSION_JSON = 'json'
FILE_EXTENSION_ZIP = 'zip'

QUALTRICS_API_BLOCK_TYPE_DEFAULT = 'Default'
QUALTRICS_API_BLOCK_TYPE_STANDARD = 'Standard'
QUALTRICS_API_BLOCK_VISIBILITY_EXPANDED = 'Expanded'

QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT = 5
QUALTRICS_API_EXPORT_RESPONSES_PROGRESS_TIMEOUT = 3

QUALTRICS_API_PATH_BLOCKS = 'blocks'
QUALTRICS_API_PATH_EXPORT_RESPONSES = 'export-responses'
QUALTRICS_API_PATH_QUESTIONS = 'questions'
QUALTRICS_API_PATH_SURVEY_DEFINITIONS = 'survey-definitions'
QUALTRICS_API_PATH_SURVEY_VERSIONS = 'survey-definitions/{}/versions'
QUALTRICS_API_PATH_SURVEYS = 'surveys'
QUALTRICS_API_PUBLISHED_SURVEY_URL_PATTERN = 'https://survey.eu.qualtrics.com/jfe/form/{}'

QUALTRICS_API_QUESTION_TYPE_MC = 'MC'
QUALTRICS_API_QUESTION_TYPE_TE = 'TE'

QUALTRICS_API_REGEX_BLOCK_ID = '^BL_[a-zA-Z0-9]{11,15}$'
QUALTRICS_API_REGEX_QUESTION_ID = '^QID[a-zA-Z0-9]+$'
QUALTRICS_API_REGEX_RESPONSE_ID = '^R_[A-Za-z0-9]{11,15}'
QUALTRICS_API_REGEX_SURVEY_ID = '^SV_[a-zA-Z0-9]{11,15}$'
QUALTRICS_API_REQUIRED_QUESTION_PARAM_KEYS = [
    'text', 'tag_number', 'type', 'answer_selector',
    'label', 'is_mandatory', 'translations',
    'block_number',
]
QUALTRICS_API_REQUIRED_QUESTION_PAYLOAD_KEYS = [
    'QuestionText', 'DataExportTag', 'QuestionType', 'Selector', 'Configuration',
    'QuestionDescription', 'Validation', 'Language',
]

QUALTRICS_API_SUPPORTED_ANSWER_SELECTORS = [
    'DL', 'GRB', 'MACOL', 'MAHR', 'MAVR', 'ML', 'MSB', 'NPS',
    'SACOL', 'SAHR', 'SAVR', 'SB', 'TB', 'TXOT', 'PTB', 'SL',
]
QUALTRICS_API_SUPPORTED_BLOCK_TYPES = ['Standard', 'Default', 'Trash']
QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_CHOICE_LOCATORS = [None, 'SelectableChoice']
QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_CONJUNCTIONS = [None, 'Or', 'And']
QUALTRICS_API_SUPPORTED_DISPLAY_LOGIC_OPERATORS = ['EqualTo', 'Selected', 'Is', 'NotSelected']
QUALTRICS_API_SUPPORTED_LANGUAGE_CODES = [
    'AR', 'ASM', 'AZ-AZ', 'BEL', 'BG', 'BN', 'BS', 'CA', 'CEB', 'CH', 'CS', 'CY', 'DA', 'DE',
    'EL', 'EN-GB', 'EN-US', 'EN', 'EO', 'ES-ES', 'ES', 'ET', 'FA', 'FI', 'FR-CA', 'FR', 'GU',
    'HE', 'HE-ZA', 'HI', 'HIL', 'HR', 'HU', 'HYE', 'ID', 'ISL', 'IT', 'JA', 'KAN', 'KAT', 'KAZ',
    'KM', 'KO', 'LT', 'LV', 'MAL', 'MAR', 'MK', 'MN', 'MS', 'MY', 'NL', 'NO', 'ORI', 'PA-IN',
    'PL', 'PT-BR', 'PT', 'RO', 'RU', 'SIN', 'SK', 'SL', 'SQI', 'SR-ME', 'SR', 'SV', 'SW', 'TA',
    'TEL', 'TGL', 'TH', 'TR', 'UK', 'UR', 'VI', 'ZH-S', 'ZH-T',
]
QUALTRICS_API_SUPPORTED_PROJECT_CATEGORIES = ['CORE', 'CX', 'EX', 'BX', 'PX']
QUALTRICS_API_SUPPORTED_QUESTION_TYPES = [
    'MC', 'Matrix', 'Captcha', 'CS', 'DB', 'DD', 'Draw', 'DynamicMatrix', 'FileUpload', 'GAP',
    'HeatMap', 'HL', 'HotSpot', 'Meta', 'PGR', 'RO', 'SBS', 'Slider', 'SS', 'TE', 'Timing',
]
