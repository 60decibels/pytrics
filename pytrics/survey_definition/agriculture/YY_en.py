# pylint: disable=too-many-lines
'''
These functions define just the start and end blocks (and questions) for use in development of further validation
'''

def get_blocks():
    return [
        {
            'description': 'Start Survey',
            'type': 'Standard',
            'position': 1
        },
        {
            'description': 'End Survey',
            'type': 'Standard',
            'position': 20
        }
    ]


def get_questions():
    return [
        {
            'block_number': 1,
            'tag_number': 1,
            'text': 'Date of Interview (yyyy-mm-dd)',
            'label': 'survey_date',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': True,
            'translations': [],
            'additional_validation_settings': {
                'ContentType': 'ValidDate',
                'Type': 'ContentType',
                'ValidDateType': 'DateIntlFormat',
            },
        },
        {
            'block_number': 1,
            'tag_number': 2,
            'text': 'Survey Start Time (hh:mm)',
            'label': 'survey_start_time',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': True,
            'translations': [],
            'additional_validation_settings': {
                'Type': 'CustomValidation',
                'CustomValidation': {
                    'Logic': {
                        '0': {
                            '0': {
                                'ChoiceLocator': 'q://QID2/ChoiceTextEntryValue',
                                'Description': 'Matches Regex for hh:mm',
                                'LeftOperand': 'q://QID2/ChoiceTextEntryValue',
                                'LogicType': 'Question',
                                'Operator': 'MatchesRegex',
                                'QuestionID': 'QID2',
                                'QuestionIDFromLocator': 'QID2',
                                'QuestionIsInLoop': 'no',
                                'RightOperand': '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',
                                'Type': 'Expression'
                            },
                            'Type': 'If'
                        },
                        'Type': 'BooleanExpression'
                    },
                    'Message': {
                        'description': 'Validation Failed',
                        'libraryID': None,
                        'messageID': None,
                        'subMessageID': 'VE_VALIDATION_FAILED'
                    }
                },
            }
        },
        {
            'block_number': 1,
            'tag_number': 3,
            'text': 'Can I continue with the survey?',
            'label': 'survey_consent_yn',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Yes'
                },
                '2': {
                    'Display': 'No'
                }
            },
            'choice_order': [1, 2],
            'variable_naming': {
                '1': 'Yes',
                '2': 'No',
            },
            'is_mandatory': True,
            'translations': [],
        },
        {
            'block_number': 20,
            'tag_number': 60,
            'text': 'Is there anything else you would like to share?',
            'label': 'retention_anythingelse_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 20,
            'tag_number': 61,
            'text': 'At the beginning of the call I said we would keep your name and details private. Now that you know what you have shared with me today, are you happy for me to share your name and this information with {Company} or would you prefer to remain anonymous?',
            'label': 'survey_anonymity_yn',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Yes, you may share'
                },
                '2': {
                    'Display': 'No, please keep me anonymous'
                }
            },
            'choice_order': [1, 2],
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 20,
            'tag_number': 62,
            'text': 'Do you mind if some of your answers and your name are used when making marketing materials?',
            'label': 'survey_marketingmaterials_yn',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Yes, you may use'
                },
                '2': {
                    'Display': 'No, please do not use'
                }
            },
            'choice_order': [1, 2],
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 20,
            'tag_number': 63,
            'text': 'Gender of Respondent',
            'label': 'respondent_gender_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Male'
                },
                '2': {
                    'Display': 'Female'
                }
            },
            'choice_order': [1, 2],
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 20,
            'tag_number': 64,
            'text': 'Survey End Time (hh:mm)',
            'label': 'survey_end_time',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': True,
            'translations': [],
            'additional_validation_settings': {
                'Type': 'CustomValidation',
                'CustomValidation': {
                    'Logic': {
                        '0': {
                            '0': {
                                'ChoiceLocator': 'q://QID64/ChoiceTextEntryValue',
                                'Description': 'Matches Regex for hh:mm',
                                'LeftOperand': 'q://QID64/ChoiceTextEntryValue',
                                'LogicType': 'Question',
                                'Operator': 'MatchesRegex',
                                'QuestionID': 'QID64',
                                'QuestionIDFromLocator': 'QID64',
                                'QuestionIsInLoop': 'no',
                                'RightOperand': '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',
                                'Type': 'Expression'
                            },
                            'Type': 'If'
                        },
                        'Type': 'BooleanExpression'
                    },
                    'Message': {
                        'description': 'Validation Failed',
                        'libraryID': None,
                        'messageID': None,
                        'subMessageID': 'VE_VALIDATION_FAILED'
                    }
                },
            }
        },
    ]
