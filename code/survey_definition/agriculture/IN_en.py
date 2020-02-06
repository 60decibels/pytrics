'''
These functions define the English (en) version of our Indian (IN) agriculture survey
that can be used by the qualtrics_api module to create a survey in Qualtrics
'''

def get_blocks():
    return [
        {
            'description': 'NPS Block',
            'type': 'Standard',
            'position': 1
        },
        {
            'description': 'QOL Block',
            'type': 'Standard',
            'position': 2
        },
        {
            'description': 'PPI Block A',
            'type': 'Standard',
            'position': 3
        },
        {
            'description': 'PPI Block B',
            'type': 'Standard',
            'position': 4
        },
        {
            'description': 'PPI Block C',
            'type': 'Standard',
            'position': 5
        },
        {
            'description': 'PPI Block D',
            'type': 'Standard',
            'position': 6
        },
        {
            'description': 'PPI Block E',
            'type': 'Standard',
            'position': 7
        }
    ]


def get_questions():
    return [
        {
            'text': 'On a scale of 0-10, how likely are you to recommend [Company]...?',
            'label': 'nps_company_rating',
            'type': 'MC',
            'tag_number': 1,
            'answer_selector': 'SAHR',
            'answer_sub_selector': 'TX',
            'choices': {
                '1': {
                    'Display': '0'
                },
                '2': {
                    'Display': '1'
                },
                '3': {
                    'Display': '2'
                },
                '4': {
                    'Display': '3'
                },
                '5': {
                    'Display': '4'
                },
                '6': {
                    'Display': '5'
                },
                '7': {
                    'Display': '6'
                },
                '8': {
                    'Display': '7'
                },
                '9': {
                    'Display': '8'
                },
                '10': {
                    'Display': '9'
                },
                '11': {
                    'Display': '10'
                },
            },
            'choice_order': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'recode_values': {
                '1': '0',
                '2': '1',
                '3': '2',
                '4': '3',
                '5': '4',
                '6': '5',
                '7': '6',
                '8': '7',
                '9': '8',
                '10': '9',
                '11': '10',
            },
            'is_mandatory': False,
            'translations': [],
            'block_number': 1
        },
        {
            'text': 'If 9-10: What specifically about [Company] would cause you to recommend...?',
            'label': 'nps_company_promoter_oe',
            'type': 'TE',
            'tag_number': 2,
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'block_number': 1,
            'display_logic': {
                'controlling_question_label': 'nps_company_rating',
                'choices': [10, 11],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'text': 'If 7-8: What specifically about [Company] caused you to give it the score...?',
            'label': 'nps_company_passive_oe',
            'type': 'TE',
            'tag_number': 3,
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'block_number': 1,
            'display_logic': {
                'controlling_question_label': 'nps_company_rating',
                'choices': [8, 9],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'text': 'If 0-6: What actions could [Company] take to make you more likely to recommend...?',
            'label': 'nps_company_detractor_oe',
            'type': 'TE',
            'tag_number': 4,
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'block_number': 1,
            'display_logic': {
                'controlling_question_label': 'nps_company_rating',
                'choices': [1, 2, 3, 4, 5, 6, 7],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'text': 'Has your quality of life changed because of [Company]?',
            'label': 'qol_rating',
            'type': 'MC',
            'tag_number': 5,
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
            'translations': [],
            'block_number': 2
        },
        {
            'text': 'If ‘Very much improved’ or ‘Slightly improved’: How has your quality of life improved?',
            'label': 'qol_improve_oe',
            'type': 'TE',
            'tag_number': 6,
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'block_number': 2,
            'display_logic': {
                'controlling_question_label': 'qol_rating',
                'choices': [1, 2],
                'operator': 'Selected',
                'conjunction': 'Or',
                'locator': 'SelectableChoice',
            }
        },
        {
            'text': 'If ‘No change’: Why has it not changed?',
            'label': 'qol_nochange_oe',
            'type': 'TE',
            'tag_number': 7,
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'block_number': 2,
            'display_logic': {
                'controlling_question_label': 'qol_rating',
                'choices': [3],
                'operator': 'Selected',
                'conjunction': None,
                'locator': 'SelectableChoice',
            }
        },
        {
            'text': 'If ‘Got slightly worse’ or ‘Got much worse’: How has your quality of life got worse?',
            'label': 'qol_worse_oe',
            'type': 'TE',
            'tag_number': 8,
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'block_number': 2,
            'display_logic': {
                'controlling_question_label': 'qol_rating',
                'choices': [4, 5],
                'operator': 'Selected',
                'conjunction': 'Or',
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
