'''
These functions define just the information block and questions for use in development of required display logic
'''

def get_blocks():
    return [
        {
            'description': 'Information',
            'type': 'Standard',
            'position': 4
        }
    ]


def get_questions():
    return [
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
            'is_mandatory': False,
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
            'is_mandatory': False,
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
            'is_mandatory': False,
            'translations': [],
            'display_logic': {
                'controlling_question_label': 'ag_experience_training_useful_mc',
                'choices': [1],
                'operator': 'NotSelected',
                'conjunction': None,
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
            'is_mandatory': False,
            'translations': [],
            'complex_display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'NotSelected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 12,
            'text': 'Can you please explain what you found easiest to apply?',
            'label': 'ag_experience_training_apply_easiest_oe',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'complex_display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'NotSelected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 13,
            'text': 'Can you please explain what you found hardest to apply?',
            'label': 'ag_experience_training_apply_hardest_oe',
            'type': 'TE',
            'answer_selector': 'SL',
            'is_mandatory': False,
            'translations': [],
            'complex_display_logic': {
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
            'complex_display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['Selected', 'Selected'],
                'conjunctions': [None, 'Or'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
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
            'is_mandatory': False,
            'translations': [],
            'complex_display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'Selected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 16,
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
            'complex_display_logic': {
                'controlling_question_labels': ['ag_experience_training_useful_mc', 'ag_experience_training_apply_mc'],
                'choices': [1, 1],
                'operators': ['NotSelected', 'Selected'],
                'conjunctions': [None, 'And'],
                'locators': ['SelectableChoice', 'SelectableChoice'],
            }
        },
        {
            'block_number': 4,
            'tag_number': 17,
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
        }
    ]
