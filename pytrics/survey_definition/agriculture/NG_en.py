'''
These functions define the English (en) version of our Nigerian (NG) agriculture survey
'''

# TODO change this from core insights to the ag survey we just described into the /data folder at root of this repo :-)
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
            'description': 'PPI - Nigeria',
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
            'text': 'Survey Start Time (hh:mm)',
            'label': 'survey_start_time',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': True,
            'translations': [],
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
            'is_mandatory': True,
            'translations': [],
        },
        {
            'block_number': 2,
            'tag_number': 4,
            'text': 'In your household, who is the main person who manages the {Crop name} crop?',
            'label': 'ag_profile_usage_mainperson_mc',
            'type': 'MC',
            'answer_selector': 'MAVR',
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
            'is_mandatory': True,
            'translations': [],
        },
        {
            'block_number': 2,
            'tag_number': 5,
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
            'is_mandatory': True,
            'translations': [],
        },
        {
            'block_number': 2,
            'tag_number': 6,
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
            'tag_number': 7,
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
            'is_mandatory': True,
            'translations': [],
        },


        {
            'block_number': 4,
            'tag_number': 8,
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
            'is_mandatory': True,
            'translations': [],
        },
        {
            'block_number': 4,
            'tag_number': 9,
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
            'is_mandatory': True,
            'translations': [],
        },
        {
            'block_number': 4,
            'tag_number': 10,
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
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'ag_experience_training_useful_mc',
                'choices': [2, 3, 4, 5],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'block_number': 4,
            'tag_number': 11,
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
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 4,
            'tag_number': 12,
            'text': 'Can you please explain what you found easiest to apply?',
            'label': 'ag_experience_training_apply_easiest_oe',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': True,
            'translations': [],
        },
        {
            'block_number': 4,
            'tag_number': 13,
            'text': 'Can you please explain what you found hardest to apply?',
            'label': 'ag_experience_training_apply_hardest_oe',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': True,
            'translations': [],
        },
        {
            'block_number': 4,
            'tag_number': 14,
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
        },
        {
            'block_number': 4,
            'tag_number': 15,
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
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 4,
            'tag_number': 16,
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
            'is_mandatory': True,
            'translations': []
        },


        {
            'block_number': 5,
            'tag_number': 17,
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
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 5,
            'tag_number': 18,
            'text': 'What specifically about {Company} would cause you to recommend it to a friend?',
            'label': 'nps_company_promoter_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'nps_company_rating',
                'choices': ['IsPromoter'],
                'operator': 'EqualTo',
                'conjunction': None,
                'locator': None,
            }
        },
        {
            'block_number': 5,
            'tag_number': 19,
            'text': 'What specifically about {Company} caused you to give it the score that you did?',
            'label': 'nps_company_passive_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'nps_company_rating',
                'choices': ['IsPassive'],
                'operator': 'EqualTo',
                'conjunction': None,
                'locator': None,
            }
        },
        {
            'block_number': 5,
            'tag_number': 20,
            'text': 'What actions could {Company} take to make you more likely to recommend it to a friend?',
            'label': 'nps_company_detractor_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'nps_company_rating',
                'choices': ['IsDetractor'],
                'operator': 'EqualTo',
                'conjunction': None,
                'locator': None,
            }
        },


        {
            'block_number': 6,
            'tag_number': 21,
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
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 6,
            'tag_number': 22,
            'text': 'How has it improved?',
            'label': 'ag_impact_way_of_farming_improve_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'ag_impact_way_of_farming_rating',
                'choices': [1, 2],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'block_number': 6,
            'tag_number': 23,
            'text': 'Why has it not changed?',
            'label': 'ag_impact_way_of_farming_nochange_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'ag_impact_way_of_farming_rating',
                'choices': [3],
                'operator': 'Selected',
                'conjunction': None,
                'locator': 'SelectableChoice',
            }
        },
        {
            'block_number': 6,
            'tag_number': 24,
            'text': 'How has it become worse?',
            'label': 'qol_worse_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'ag_impact_way_of_farming_rating',
                'choices': [4, 5],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },


        {
            'block_number': 7,
            'tag_number': 25,
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
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 7,
            'tag_number': 26,
            'text': 'How has it improved?',
            'label': 'qol_improve_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],            
            'display_logic': {
                'controlling_question_label': 'qol_rating',
                'choices': [1, 2],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'block_number': 7,
            'tag_number': 27,
            'text': 'Why has it not changed?',
            'label': 'qol_nochange_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'qol_rating',
                'choices': [3],
                'operator': 'Selected',
                'conjunction': None,
                'locator': 'SelectableChoice',
            }
        },
        {
            'block_number': 7,
            'tag_number': 28,
            'text': 'How has it become worse?',
            'label': 'qol_worse_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'qol_rating',
                'choices': [4, 5],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },


        {
            'block_number': 8,
            'tag_number': 29,
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
            'is_mandatory': True,
            'translations': []
        },


        {
            'block_number': 9,
            'tag_number': 30,
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
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 9,
            'tag_number': 31,
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
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'impact_moneyspend_rating',
                'choices': [4, 5],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },


        {
            'block_number': 10,
            'tag_number': 32,
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
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 10,
            'tag_number': 33,
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
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'alternatives_yn',
                'choices': [1, 2],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'block_number': 10,
            'tag_number': 34,
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
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'alternatives_yn',
                'choices': [1, 2],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'block_number': 10,
            'tag_number': 35,
            'text': 'Please explain how {Company} is better/worse?',
            'label': 'alternatives_comparison_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'alternatives_yn',
                'choices': [3],
                'operator': 'Selected',
                'conjunction': None,
                'locator': 'SelectableChoice',
            }
        },


        {
            'block_number': 11,
            'tag_number': 36,
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
            'is_mandatory': True,
            'translations': []
        },
        {
            'block_number': 11,
            'tag_number': 37,
            'text': 'Please explain the challenge you have had with {Product/Service}',
            'label': 'challenges_oe',
            'type': 'TE',
            'answer_selector': 'ML',
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'challenges_yn',
                'choices': [1],
                'operator': 'Selected',
                'conjunction': None,
                'locator': 'SelectableChoice',
            }
        },
        {
            'block_number': 11,
            'tag_number': 38,
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
            'is_mandatory': True,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'challenges_yn',
                'choices': [1],
                'operator': 'Selected',
                'conjunction': None,
                'locator': 'SelectableChoice',
            }
        },


























        {
            'text': 'Including yourself, how many people live in your home?',
            'label': 'ppi_in_s_hhsize',
            'type': 'TE',
            'tag_number': 9,
            'answer_selector': 'SL',
            'is_mandatory': False,
            'additional_validation_settings': {
                'ContentType': 'ValidNumber',
                'Type': 'ContentType'
            },
            'translations': [],
            'block_number': 3
        },
        {
            'text': 'Did anyone in your household consume milk or milk products in the last 30 days?',
            'label': 'ppi_in_s_milk',
            'type': 'MC',
            'tag_number': 10,
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
                '2': 'No'
            },
            'is_mandatory': False,
            'translations': [],
            'block_number': 4
        },
        {
            'text': 'Does the household have an electric fan?',
            'label': 'ppi_in_s_fan',
            'type': 'MC',
            'tag_number': 11,
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
                '2': 'No'
            },
            'is_mandatory': False,
            'translations': [],
            'block_number': 5
        },
        {
            'text': 'Does the household have a stove or gas burner?',
            'label': 'ppi_in_s_stove',
            'type': 'MC',
            'tag_number': 12,
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
                '2': 'No'
            },
            'is_mandatory': False,
            'translations': [],
            'block_number': 6
        },
        {
            'text': 'Does the household have a pressure cooker or pressure pan?',
            'label': 'ppi_in_s_pressurecooker',
            'type': 'MC',
            'tag_number': 13,
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
                '2': 'No'
            },
            'is_mandatory': False,
            'translations': [],
            'block_number': 7
        },
    ]
