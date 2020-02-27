# pylint: disable=too-many-lines
'''
These functions define the English (en) version of our Tanzanian (TZ) agriculture survey
'''

def get_name():
    return '60dB Standard Agriculture Survey - Tanzania'


def get_blocks():
    return [
        {
            'description': 'Start Survey',
            'type': 'Standard',
            'position': 1
        },
        {
            'description': 'Profile & Acquisition',
            'type': 'Standard',
            'position': 2
        },
        {
            'description': 'First Access',
            'type': 'Standard',
            'position': 3
        },
        {
            'description': 'Information',
            'type': 'Standard',
            'position': 4
        },
        {
            'description': 'NPS',
            'type': 'Standard',
            'position': 5
        },
        {
            'description': 'Way of Farming',
            'type': 'Standard',
            'position': 6
        },
        {
            'description': 'Quality of Life',
            'type': 'Standard',
            'position': 7
        },
        {
            'description': 'Change in Confidence',
            'type': 'Standard',
            'position': 8
        },
        {
            'description': 'Money Spent',
            'type': 'Standard',
            'position': 9
        },
        {
            'description': 'Alternatives',
            'type': 'Standard',
            'position': 10
        },
        {
            'description': 'Challenges',
            'type': 'Standard',
            'position': 11
        },
        {
            'description': 'Retention',
            'type': 'Standard',
            'position': 12
        },
        {
            'description': 'HH Size',
            'type': 'Standard',
            'position': 13
        },
        {
            'description': 'Farmed Land & Ownership',
            'type': 'Standard',
            'position': 14
        },
        {
            'description': 'Share of HH Income - Company',
            'type': 'Standard',
            'position': 15
        },
        {
            'description': 'Share of HH Income - All Farming',
            'type': 'Standard',
            'position': 16
        },
        {
            'description': 'Poverty Probability Index - Tanzania',
            'type': 'Standard',
            'position': 17
        },
        {
            'description': 'Gender',
            'type': 'Standard',
            'position': 18
        },
        {
            'description': 'Age',
            'type': 'Standard',
            'position': 19
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
            'text': 'Survey Start Time (hh:mm) please enter in 24hr format',
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
            'text': 'Researcher name',
            'label': 'researcher_name',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
        },
        {
            'block_number': 1,
            'tag_number': 4,
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
            'block_number': 1,
            'tag_number': 5,
            'text': 'Can you please tell me your name?',
            'label': 'respondent_name',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
        },
        {
            'block_number': 2,
            'tag_number': 6,
            'text': 'In your household, who is the main person who manages the {Crop name} crop?',
            'label': 'ag_profile_usage_mainperson_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Myself'
                },
                '2': {
                    'Display': 'My spouse'
                },
                '3': {
                    'Display': 'Another family member',
                    'TextEntry': 'true'
                },
                '4': {
                    'Display': 'Other',
                    'TextEntry': 'true'
                }
            },
            'choice_order': [1, 2, 3, 4],
            'variable_naming': {
                '1': 'Myself',
                '2': 'My spouse',
                '3': 'Another family member',
                '4': 'Other',
            },
            'is_mandatory': False,
            'translations': [],
        },
        {
            'block_number': 2,
            'tag_number': 7,
            'text': 'How did you first hear about {Company} information?',
            'label': 'acquisition_howhear_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Friends/Family'
                },
                '2': {
                    'Display': 'Demonstration on Field'
                },
                '3': {
                    'Display': 'Field Day'
                },
                '4': {
                    'Display': 'Sensitization event / group meeting / community meeting'
                },
                '5': {
                    'Display': 'Other:',
                    'TextEntry': 'true',
                    'TextEntrySize': 'Small'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'variable_naming': {
                '1': 'Friends/Family',
                '2': 'Demonstration on Field',
                '3': 'Another family member',
                '4': 'Other',
            },
            'is_mandatory': False,
            'translations': [],
        },
        {
            'block_number': 2,
            'tag_number': 8,
            'text': 'How many months back did you start interacting with {Company}?',
            'label': 'respondent_tenure',
            'type': 'MC',
            'answer_selector': 'MAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Years',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                },
                '2': {
                    'Display': 'Months',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                },
                '3': {
                    'Display': "Don't know / can't say"
                }
            },
            'choice_order': [1, 2, 3],
            'is_mandatory': False,
            'translations': [],
        },
        {
            'block_number': 3,
            'tag_number': 9,
            'text': 'Before you started interacting with {Company}, did you have access to information like that which {Company} provides?',
            'label': 'prioraccess_yn',
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
            'is_mandatory': False,
            'translations': [],
        },
        {
            'block_number': 4,
            'tag_number': 10,
            'text': 'How much of this information was easy to understand?',
            'label': 'ag_experience_training_understand_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': '1- None'
                },
                '2': {
                    'Display': '2- Very Little'
                },
                '3': {
                    'Display': '3- Some'
                },
                '4': {
                    'Display': '4- Most'
                },
                '5': {
                    'Display': '5- All'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'is_mandatory': False,
            'translations': [],
        },
        {
            'block_number': 4,
            'tag_number': 11,
            'text': 'How much of this information is useful (to your work)?',
            'label': 'ag_experience_training_useful_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': '1- None'
                },
                '2': {
                    'Display': '2- Very Little'
                },
                '3': {
                    'Display': '3- Some'
                },
                '4': {
                    'Display': '4- Most'
                },
                '5': {
                    'Display': '5- All'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'is_mandatory': False,
            'translations': [],
        },
        {
            'block_number': 4,
            'tag_number': 12,
            'text': 'How much of this information did you apply to your {Crop name} crop?',
            'label': 'ag_experience_training_apply_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': '1- None'
                },
                '2': {
                    'Display': '2- Very Little'
                },
                '3': {
                    'Display': '3- Some'
                },
                '4': {
                    'Display': '4- Most'
                },
                '5': {
                    'Display': '5- All'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc'],
                'choices': [1],
                'operators': ['NotSelected'],
                'conjunctions': [None],
                'locators': ['SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 13,
            'text': 'How soon after receiving the information did you apply the lessons (for the first time)?',
            'label': 'ag_experience_training_apply_time_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Same day'
                },
                '2': {
                    'Display': 'Within days'
                },
                '3': {
                    'Display': 'Within weeks'
                },
                '4': {
                    'Display': 'Within months'
                },
                '5': {
                    'Display': 'A year or more later'
                },
                '6': {
                    'Display': "Don't know / can't say"
                }
            },
            'choice_order': [1, 2, 3, 4, 5, 6],
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'NotSelected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 14,
            'text': 'Can you please explain what you found easiest to apply?',
            'label': 'ag_experience_training_apply_easiest_oe',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'NotSelected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 15,
            'text': 'Can you please explain what you found hardest to apply?',
            'label': 'ag_experience_training_apply_hardest_oe',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'NotSelected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 16,
            'text': 'Would you mind sharing with me what prevented you from applying the information?',
            'label': 'ag_experience_training_apply_barriers_mc',
            'type': 'MC',
            'answer_selector': 'MAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'No credit or money'
                },
                '2': {
                    'Display': 'Information not clear'
                },
                '3': {
                    'Display': 'Recommended materials or equipment not available'
                },
                '4': {
                    'Display': 'Do not trust information'
                },
                '5': {
                    'Display': 'Other',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True,
                    'TextEntrySize': 'Medium'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 17,
            'text': 'Did you consider (think about) applying the information?',
            'label': 'ag_experience_training_apply_consider_yn',
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
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'Selected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 18,
            'text': 'Do you intend to apply the information next year?',
            'label': 'ag_experience_training_apply_intention_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'No'
                },
                '2': {
                    'Display': 'Yes, maybe'
                },
                '3': {
                    'Display': 'Yes, definitely'
                }
            },
            'choice_order': [1, 2, 3],
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'Selected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 19,
            'text': 'Do you think other farmers would pay for the {Company} information?',
            'label': 'ag_experience_training_wtp_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'No'
                },
                '2': {
                    'Display': 'Yes, maybe'
                },
                '3': {
                    'Display': 'Yes, definitely'
                }
            },
            'choice_order': [1, 2, 3],
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 5,
            'tag_number': 20,
            'text': 'On a scale of 0-10, how likely is it that you would recommend the {Company} information to a friend, where 0 is not at all likely and 10 is extremely likely?',
            'label': 'nps_company_rating',
            'type': 'MC',
            'answer_selector': 'NPS',
            'choices': [
                {
                    'Display': '0'
                },
                {
                    'Display': '1'
                },
                {
                    'Display': '2'
                },
                {
                    'Display': '3'
                },
                {
                    'Display': '4'
                },
                {
                    'Display': '5'
                },
                {
                    'Display': '6'
                },
                {
                    'Display': '7'
                },
                {
                    'Display': '8'
                },
                {
                    'Display': '9'
                },
                {
                    'Display': '10'
                }
            ],
            'choice_order': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            'column_labels': [
                {
                    'Display': 'Not at all likely',
                    'IsLabelDefault': True
                },
                {
                    'Display': 'Extremely likely',
                    'IsLabelDefault': True
                }
            ],
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 5,
            'tag_number': 21,
            'text': 'What specifically about {Company} would cause you to recommend it to a friend?',
            'label': 'nps_company_promoter_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['nps_company_rating'],
                'choices': ['IsPromoter'],
                'operators': ['EqualTo'],
                'conjunctions': [None],
                'locators': [None],
            }
        },
        {
            'block_number': 5,
            'tag_number': 22,
            'text': 'What specifically about {Company} caused you to give it the score that you did?',
            'label': 'nps_company_passive_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['nps_company_rating'],
                'choices': ['IsPassive'],
                'operators': ['EqualTo'],
                'conjunctions': [None],
                'locators': [None],
            }
        },
        {
            'block_number': 5,
            'tag_number': 23,
            'text': 'What actions could {Company} take to make you more likely to recommend it to a friend?',
            'label': 'nps_company_detractor_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['nps_company_rating'],
                'choices': ['IsDetractor'],
                'operators': ['EqualTo'],
                'conjunctions': [None],
                'locators': [None],
            }
        },
        {
            'block_number': 6,
            'tag_number': 24,
            'text': 'Has your way of farming changed because of {Company} information?',
            'label': 'ag_impact_way_of_farming_rating',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Very much improved'
                },
                '2': {
                    'Display': 'Slightly improved'
                },
                '3': {
                    'Display': 'No change'
                },
                '4': {
                    'Display': 'Got slightly worse'
                },
                '5': {
                    'Display': 'Got much worse'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'variable_naming': {
                '1': 'Very much improved',
                '2': 'Slightly improved',
                '3': 'No change',
                '4': 'Got slightly worse',
                '5': 'Got much worse',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 6,
            'tag_number': 25,
            'text': 'How has it improved?',
            'label': 'ag_impact_way_of_farming_improve_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_impact_way_of_farming_rating', 'ag_impact_way_of_farming_rating'],
                'choices': [1, 2],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 6,
            'tag_number': 26,
            'text': 'Why has it not changed?',
            'label': 'ag_impact_way_of_farming_nochange_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_impact_way_of_farming_rating'],
                'choices': [3],
                'operators': ['Selected'],
                'conjunctions': [None],
                'locators': ['SelectableChoice'],
            }
        },
        {
            'block_number': 6,
            'tag_number': 27,
            'text': 'How has it become worse?',
            'label': 'ag_impact_way_of_farming_worse_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_impact_way_of_farming_rating', 'ag_impact_way_of_farming_rating'],
                'choices': [4, 5],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 7,
            'tag_number': 28,
            'text': 'Has your quality of life changed because of {Company} information?',
            'label': 'qol_rating',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Very much improved'
                },
                '2': {
                    'Display': 'Slightly improved'
                },
                '3': {
                    'Display': 'No change'
                },
                '4': {
                    'Display': 'Got slightly worse'
                },
                '5': {
                    'Display': 'Got much worse',
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'variable_naming': {
                '1': 'Very much improved',
                '2': 'Slightly improved',
                '3': 'No change',
                '4': 'Got slightly worse',
                '5': 'Got much worse',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 7,
            'tag_number': 29,
            'text': 'How has it improved?',
            'label': 'qol_improve_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['qol_rating', 'qol_rating'],
                'choices': [1, 2],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 7,
            'tag_number': 30,
            'text': 'Why has it not changed?',
            'label': 'qol_nochange_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['qol_rating'],
                'choices': [3],
                'operators': ['Selected'],
                'conjunctions': [None],
                'locators': ['SelectableChoice'],
            }
        },
        {
            'block_number': 7,
            'tag_number': 31,
            'text': 'How has it become worse?',
            'label': 'qol_worse_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['qol_rating', 'qol_rating'],
                'choices': [4, 5],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 8,
            'tag_number': 32,
            'text': 'Has your confidence that you will be able to grow and sell a healthy {Crop name} crop changed because of {Company} information?',
            'label': 'ag_impact_confidence_rating',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Got much worse'
                },
                '2': {
                    'Display': 'Got slightly worse'
                },
                '3': {
                    'Display': 'No change'
                },
                '4': {
                    'Display': 'Slightly improved'
                },
                '5': {
                    'Display': 'Very much improved'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'variable_naming': {
                '1': 'Got much worse',
                '2': 'Got slightly worse',
                '3': 'No change',
                '4': 'Slightly improved',
                '5': 'Very much improved',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 9,
            'tag_number': 33,
            'text': 'Has the money you spend on {Crop name} crop changed because you started working with {Company} information?',
            'label': 'impact_moneyspend_rating',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Very much decreased'
                },
                '2': {
                    'Display': 'Slightly decreased'
                },
                '3': {
                    'Display': 'No change'
                },
                '4': {
                    'Display': 'Slightly increased'
                },
                '5': {
                    'Display': 'Very much increased'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'variable_naming': {
                '1': 'Very much decreased',
                '2': 'Slightly decreased',
                '3': 'No change',
                '4': 'Slightly increased',
                '5': 'Very much increased',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 9,
            'tag_number': 34,
            'text': 'Are you comfortable with this increase?',
            'label': 'impact_moneyspend_comfort_rating',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'No'
                },
                '2': {
                    'Display': 'Yes, partly'
                },
                '3': {
                    'Display': 'Yes, completely'
                },
                '4': {
                    'Display': 'Cannot say'
                }
            },
            'choice_order': [1, 2, 3, 4],
            'variable_naming': {
                '1': 'No',
                '2': 'Yes, partly',
                '3': 'Yes, completely',
                '4': 'Cannot say',
            },
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['impact_moneyspend_rating', 'impact_moneyspend_rating'],
                'choices': [4, 5],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 10,
            'tag_number': 35,
            'text': 'Could you easily find a good alternative to {Company} information?',
            'label': 'alternatives_yn',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Yes'
                },
                '2': {
                    'Display': 'Maybe'
                },
                '3': {
                    'Display': 'No'
                }
            },
            'choice_order': [1, 2, 3],
            'variable_naming': {
                '1': 'Yes',
                '2': 'Maybe',
                '3': 'No',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 10,
            'tag_number': 36,
            'text': 'Would you be comfortable sharing who these alternatives are?',
            'label': 'alternatives_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Another Company',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                },
                '2': {
                    'Display': 'Govt market'
                },
                '3': {
                    'Display': 'Open market'
                },
                '4': {
                    'Display': 'Individual buyer'
                },
                '5': {
                    'Display': 'Other',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'variable_naming': {
                '1': 'No',
                '2': 'Yes, partly',
                '3': 'Yes, completely',
                '4': 'Cannot say',
            },
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['alternatives_yn', 'alternatives_yn'],
                'choices': [1, 2],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 10,
            'tag_number': 37,
            'text': 'Compared to the alternative, do you think {Company} is...',
            'label': 'alternatives_comparison_rating',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Much worse than the alternative'
                },
                '2': {
                    'Display': 'Worse'
                },
                '3': {
                    'Display': 'Same as the alternative'
                },
                '4': {
                    'Display': 'Better'
                },
                '5': {
                    'Display': 'Much better than the alternative'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'variable_naming': {
                '1': 'Much worse than the alternative',
                '2': 'Worse',
                '3': 'Same as the alternative',
                '4': 'Better',
                '5': 'Much better than the alternative',
            },
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['alternatives_yn', 'alternatives_yn'],
                'choices': [1, 2],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 10,
            'tag_number': 38,
            'text': 'Please explain how {Company} is better/worse?',
            'label': 'alternatives_comparison_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['alternatives_comparison_rating', 'alternatives_yn'],
                'choices': [3, 3],
                'operators': ['NotSelected', 'NotSelected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 11,
            'tag_number': 39,
            'text': 'Have you experienced any challenges with {Company}?',
            'label': 'challenges_yn',
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
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 11,
            'tag_number': 40,
            'text': 'Please explain the challenge you have had with {Product/Service}',
            'label': 'challenges_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['challenges_yn'],
                'choices': [1],
                'operators': ['Selected'],
                'conjunctions': [None],
                'locators': ['SelectableChoice'],
            }
        },
        {
            'block_number': 11,
            'tag_number': 41,
            'text': 'Has your challenge been resolved?',
            'label': 'challenges_resolve_yn',
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
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['challenges_yn'],
                'choices': [1],
                'operators': ['Selected'],
                'conjunctions': [None],
                'locators': ['SelectableChoice'],
            }
        },
        {
            'block_number': 12,
            'tag_number': 42,
            'text': 'What can {Company} do to serve you better?',
            'label': 'retention_improve_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 12,
            'tag_number': 43,
            'text': 'Do you see yourself working with {Company} next year?',
            'label': 'retention_1year_rating',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'No'
                },
                '2': {
                    'Display': 'Yes, maybe'
                },
                '3': {
                    'Display': 'Yes, definitely'
                }
            },
            'choice_order': [1, 2, 3],
            'variable_naming': {
                '1': 'No',
                '2': 'Yes, maybe',
                '3': 'Yes, definitely',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 12,
            'tag_number': 44,
            'text': 'Do you see yourself working with {Company} 5 years from now?',
            'label': 'retention_5year_rating',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'No'
                },
                '2': {
                    'Display': 'Yes, maybe'
                },
                '3': {
                    'Display': 'Yes, definitely'
                }
            },
            'choice_order': [1, 2, 3],
            'variable_naming': {
                '1': 'No',
                '2': 'Yes, maybe',
                '3': 'Yes, definitely',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 13,
            'tag_number': 45,
            'text': 'Including yourself, how many people live in your home?',
            'label': 'respondent_hhsize_num',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'additional_validation_settings': {
                'ContentType': 'ValidNumber',
                'Type': 'ContentType',
                'ValidNumber': {
                    'Max': '50',
                    'Min': '1',
                    'NumDecimals': '0'
                }
            }
        },
        {
            'block_number': 14,
            'tag_number': 46,
            'text': 'How much total land did you use for farming in the last 12 months? Consider all crops planted. (acres)',
            'label': 'ag_profile_land_farmedpastyear_num',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'additional_validation_settings': {
                'ContentType': 'ValidNumber',
                'Type': 'ContentType'
            }
        },
        {
            'block_number': 14,
            'tag_number': 47,
            'text': 'How many of these [acres from total] did you farm with {Crop name} in last 12 months? (acres)',
            'label': 'ag_profile_land_proportioncrop_num',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'additional_validation_settings': {
                'ContentType': 'ValidNumber',
                'Type': 'ContentType'
            }
        },
        {
            'block_number': 15,
            'tag_number': 48,
            'text': 'In the last 12 months, what proportion (%) of your household\u2019s total income, came from {Crop name} crop using {Company}\u2019s information?',
            'label': 'ag_profile_income_hhshare_company_num',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Enter Percentage',
                    'TextEntry': 'true'
                },
                '2': {
                    'Display': 'Unable to give exact percentage'
                },
                '3': {
                    'Display': 'Unable to answer'
                }
            },
            'choice_order': [1, 2, 3],
            'variable_naming': {
                '1': 'Enter Percentage',
                '2': 'Unable to give exact percentage',
                '3': 'Unable to answer',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 15,
            'tag_number': 49,
            'text': '(If unable to give an exact percentage, share these options) In the last 12 months, what proportion (%) of your household\u2019s total income, came from {Crop name} crop using {Company}\u2019s information?',
            'label': 'ag_profile_income_hhshare_company_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'A little bit (1-25%)'
                },
                '2': {
                    'Display': 'Less than half (25-50%)'
                },
                '3': {
                    'Display': 'More than half (50-75%)'
                },
                '4': {
                    'Display': 'Almost all (75-100%)'
                }
            },
            'choice_order': [1, 2, 3, 4],
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_profile_income_hhshare_company_num'],
                'choices': [2],
                'operators': ['Selected'],
                'conjunctions': [None],
                'locators': ['SelectableChoice'],
            }
        },
        {
            'block_number': 16,
            'tag_number': 50,
            'text': 'In the last 12 months, what proportion (%) of the total harvest from all your land did you sell?',
            'label': 'ag_profile_income_hhshare_allfarming_num',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Enter Percentage',
                    'TextEntry': 'true'
                },
                '2': {
                    'Display': 'Unable to give exact percentage'
                },
                '3': {
                    'Display': "Don't have land"
                },
                '4': {
                    'Display': 'Unable to answer'
                }
            },
            'choice_order': [1, 2, 3, 4],
            'variable_naming': {
                '1': 'Enter Percentage',
                '2': 'Unable to give exact percentage',
                '3': "Don't have land",
                '4': 'Unable to answer',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 16,
            'tag_number': 51,
            'text': '(If unable to give an exact percentage, share these options) In the last 12 months, what proportion (%) of the total harvest from all your land did you sell?',
            'label': 'ag_profile_income_hhshare_allfarming_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'A little bit (1-25%)'
                },
                '2': {
                    'Display': 'Less than half (25-50%)'
                },
                '3': {
                    'Display': 'More than half (50-75%)'
                },
                '4': {
                    'Display': 'Almost all (75-100%)'
                }
            },
            'choice_order': [1, 2, 3, 4],
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_labels': ['ag_profile_income_hhshare_allfarming_num'],
                'choices': [2],
                'operators': ['Selected'],
                'conjunctions': [None],
                'locators': ['SelectableChoice'],
            }
        },
        {
            'block_number': 17,
            'tag_number': 52,
            'text': 'Does the household reside in Dar es Salaam?',
            'label': 'ppi_tz_s_dar',
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
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 17,
            'tag_number': 53,
            'text': 'What is the main building material of the floor?',
            'label': 'ppi_tz_s_floor',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Cement, Ceramic tiles/marumaru, Parquet or polished wood, Vinyl or asphalt strips, Wood planks, Palm/bamboo'
                },
                '2': {
                    'Display': 'Earth/sand, Dung, Other'
                }
            },
            'choice_order': [1, 2],
            'variable_naming': {
                '1': 'Cement, Ceramic tiles/marumaru, Parquet or polished wood, Vinyl or asphalt strips, Wood planks, Palm/bamboo',
                '2': 'Earth/sand, Dung, Other',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 17,
            'tag_number': 54,
            'text': 'What is the building material used for the roof of the main building',
            'label': 'ppi_tz_s_floor',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Iron sheets, Tiles, Concrete, Asbestos sheets'
                },
                '2': {
                    'Display': 'Grass/leaves, Mud and leaves, Other'
                }
            },
            'choice_order': [1, 2],
            'variable_naming': {
                '1': 'Iron sheets, Tiles, Concrete, Asbestos sheets',
                '2': 'Grass/leaves, Mud and leaves, Other',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 17,
            'tag_number': 55,
            'text': 'What is the main fuel used for cooking?',
            'label': 'ppi_tz_s_cookingfuel',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Electricity, Solar, Generator/private sources, Gas (Industrial/Biogas), Kerosene/Paraffin, Coal, Charcoal'
                },
                '2': {
                    'Display': 'Firewood, Wood/farm residuals, Other'
                }
            },
            'choice_order': [1, 2],
            'variable_naming': {
                '1': 'Electricity, Solar, Generator/private sources, Gas (Industrial/Biogas), Kerosene/Paraffin, Coal, Charcoal',
                '2': 'Firewood, Wood/farm residuals, Other',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 17,
            'tag_number': 56,
            'text': 'Does your household have a charcoal stove?',
            'label': 'ppi_tz_s_charcoal',
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
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 17,
            'tag_number': 57,
            'text': 'How many members does the household have?',
            'label': 'ppi_tz_s_hhsize',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Less than 5'
                },
                '2': {
                    'Display': '5 or 6'
                },
                '3': {
                    'Display': '7 or more'
                }
            },
            'choice_order': [1, 2, 3],
            'variable_naming': {
                '1': 'Less than 5',
                '2': '5 or 6',
                '3': '7 or more',
            },
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 18,
            'tag_number': 58,
            'text': 'Who in your family made most of the important decisions related to {Crop name} crop?',
            'label': 'gn_familydynamics_important_decisions_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Adult Female HH Member'
                },
                '2': {
                    'Display': 'Adult Male HH Member'
                },
                '3': {
                    'Display': 'Other Male',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                },
                '4': {
                    'Display': 'Other Female',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                }
            },
            'choice_order': [1, 2, 3, 4],
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 18,
            'tag_number': 59,
            'text': 'Who in your family did most of the work related to {Crop name} crop?',
            'label': 'gn_familydynamics_work_burden_oe',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Adult Female HH Member'
                },
                '2': {
                    'Display': 'Adult Male HH Member'
                },
                '3': {
                    'Display': 'Other Male',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                },
                '4': {
                    'Display': 'Other Female',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                }
            },
            'choice_order': [1, 2, 3, 4],
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 18,
            'tag_number': 60,
            'text': 'Who in your family handled the money that came from {Crop name} crops?',
            'label': 'gn_familydynamics_money_from_sale_mc',
            'type': 'MC',
            'answer_selector': 'SAVR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': 'Adult Female HH Member'
                },
                '2': {
                    'Display': 'Adult Male HH Member'
                },
                '3': {
                    'Display': 'Other Male',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                },
                '4': {
                    'Display': 'Other Female',
                    'TextEntry': 'true',
                    'TextEntryForceResponse': True
                }
            },
            'choice_order': [1, 2, 3, 4],
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 19,
            'tag_number': 61,
            'text': 'What is your age?',
            'label': 'respondent_age_num',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'additional_validation_settings': {
                'ContentType': 'ValidNumber',
                'Type': 'ContentType',
                'ValidNumber': {
                    'Max': '200',
                    'Min': '0',
                    'NumDecimals': '0'
                },
            }
        },
        {
            'block_number': 20,
            'tag_number': 62,
            'text': 'Is there anything else you would like to share?',
            'label': 'retention_anythingelse_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': False,
            'translations': []
        },
        {
            'block_number': 20,
            'tag_number': 63,
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
            'tag_number': 64,
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
            'tag_number': 65,
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
            'tag_number': 66,
            'text': 'Survey End Time (hh:mm) please enter in 24hr format',
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
                                'ChoiceLocator': 'q://QID66/ChoiceTextEntryValue',
                                'Description': 'Matches Regex for hh:mm',
                                'LeftOperand': 'q://QID66/ChoiceTextEntryValue',
                                'LogicType': 'Question',
                                'Operator': 'MatchesRegex',
                                'QuestionID': 'QID66',
                                'QuestionIDFromLocator': 'QID66',
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
