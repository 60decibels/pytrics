'''
To reduce LOC in test files, I have put some helper functions in here
that provide reference data for the tests
'''

def get_test_blocks():
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


def get_test_question_params():
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
                }
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
                '11': '10'
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
                    'Display': 'Got much worse'
                }
            },
            'choice_order': [1, 2, 3, 4, 5],
            'variable_naming': {
                '1': 'Very much improved',
                '2': 'Slightly improved',
                '3': 'No change',
                '4': 'Got slightly worse',
                '5': 'Got much worse'
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


def get_test_question_payloads():
    return [
        {
            'QuestionText': 'On a scale of 0-10, how likely are you to recommend [Company]...?',
            'DataExportTag': 'Q1',
            'QuestionType': 'MC',
            'Selector': 'SAHR',
            'SubSelector': 'TX',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'nps_company_rating',
            'Choices': {
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
                }
            },
            'ChoiceOrder': [
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8',
                '9',
                '10'
            ],
            'RecodeValues': {
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
                '11': '10'
            },
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': []
        },
        {
            'QuestionText': 'If 9-10: What specifically about [Company] would cause you to recommend...?',
            'DataExportTag': 'Q2',
            'QuestionType': 'TE',
            'Selector': 'SL',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'nps_company_promoter_oe',
            'Choices': {},
            'ChoiceOrder': [],
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': [],
            'DisplayLogic': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID1',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID1/IsPromoter',
                    'Operator': 'EqualTo',
                    'QuestionIDFromLocator': 'QID1',
                    'LeftOperand': 'q://QID1/IsPromoter',
                    'Type': 'Expression',
                    'Description': 'If QID1 IsPromoter Is True'
                },
                'Type': 'BooleanExpression',
                'inPage': False
            }
        },
        {
            'QuestionText': 'If 7-8: What specifically about [Company] caused you to give it the score...?',
            'DataExportTag': 'Q3',
            'QuestionType': 'TE',
            'Selector': 'SL',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'nps_company_passive_oe',
            'Choices': {},
            'ChoiceOrder': [],
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': [],
            'DisplayLogic': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID1',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID1/IsPassive',
                    'Operator': 'EqualTo',
                    'QuestionIDFromLocator': 'QID1',
                    'LeftOperand': 'q://QID1/IsPassive',
                    'Type': 'Expression',
                    'Description': 'If QID1 IsPassive Is True'
                },
                'Type': 'BooleanExpression',
                'inPage': False
            }
        },
        {
            'QuestionText': 'If 0-6: What actions could [Company] take to make you more likely to recommend...?',
            'DataExportTag': 'Q4',
            'QuestionType': 'TE',
            'Selector': 'SL',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'nps_company_detractor_oe',
            'Choices': {},
            'ChoiceOrder': [],
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': [],
            'DisplayLogic': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID1',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID1/IsDetractor',
                    'Operator': 'EqualTo',
                    'QuestionIDFromLocator': 'QID1',
                    'LeftOperand': 'q://QID1/IsDetractor',
                    'Type': 'Expression',
                    'Description': 'If QID1 IsDetractor Is True'
                },
                'Type': 'BooleanExpression',
                'inPage': False
            }
        },
        {
            'QuestionText': 'Has your quality of life changed because of [Company]?',
            'DataExportTag': 'Q5',
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'SubSelector': None,
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'qol_rating',
            'Choices': {
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
            'ChoiceOrder': [
                1,
                2,
                3,
                4,
                5
            ],
            'VariableNaming': {
                '1': 'Very much improved',
                '2': 'Slightly improved',
                '3': 'No change',
                '4': 'Got slightly worse',
                '5': 'Got much worse'
            },
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': []
        },
        {
            'QuestionText': 'If ‘Very much improved’ or ‘Slightly improved’: How has your quality of life improved?',
            'DataExportTag': 'Q6',
            'QuestionType': 'TE',
            'Selector': 'SL',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'qol_improve_oe',
            'Choices': {},
            'ChoiceOrder': [],
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': [],
            'DisplayLogic': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID5',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID5/Selected/1',
                    'Operator': 'SelectableChoice',
                    'QuestionIDFromLocator': 'QID5',
                    'LeftOperand': 'q://QID5/Selected/1',
                    'Type': 'Expression',
                    'Description': 'If QID5 1 Is Selected'
                },
                '1': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID5',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID5/Selected/2',
                    'Operator': 'SelectableChoice',
                    'QuestionIDFromLocator': 'QID5',
                    'LeftOperand': 'q://QID5/Selected/2',
                    'Type': 'Expression',
                    'Description': 'If QID5 2 Is Selected',
                    'Conjuction': 'Or'
                },
                'Type': 'BooleanExpression',
                'inPage': False
            }
        },
        {
            'QuestionText': 'If ‘No change’: Why has it not changed?',
            'DataExportTag': 'Q7',
            'QuestionType': 'TE',
            'Selector': 'SL',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'qol_nochange_oe',
            'Choices': {},
            'ChoiceOrder': [],
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': [],
            'DisplayLogic': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID5',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID5/Selected/3',
                    'Operator': 'SelectableChoice',
                    'QuestionIDFromLocator': 'QID5',
                    'LeftOperand': 'q://QID5/Selected/3',
                    'Type': 'Expression',
                    'Description': 'If QID5 3 Is Selected'
                },
                'Type': 'BooleanExpression',
                'inPage': False
            }
        },
        {
            'QuestionText': 'If ‘Got slightly worse’ or ‘Got much worse’: How has your quality of life got worse?',
            'DataExportTag': 'Q8',
            'QuestionType': 'TE',
            'Selector': 'SL',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'qol_worse_oe',
            'Choices': {},
            'ChoiceOrder': [],
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'Language': [],
            'DisplayLogic': {
                '0': {
                    'LogicType': 'Question',
                    'QuestionID': 'QID5',
                    'QuestionIsInLoop': 'no',
                    'ChoiceLocator': 'q://QID5/Selected/4',
                    'Operator': 'SelectableChoice',
                    'QuestionIDFromLocator': 'QID5',
                    'LeftOperand': 'q://QID5/Selected/4',
                    'Type': 'Expression',
                    'Description': 'If QID5 4 Is Selected'
                },
                'Type': 'BooleanExpression',
                'inPage': False
            }
        },
        {
            'QuestionText': 'Including yourself, how many people live in your home?',
            'DataExportTag': 'Q9',
            'QuestionType': 'TE',
            'Selector': 'SL',
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'ppi_in_s_hhsize',
            'Validation': {
                'Settings': {
                    'ContentType': 'ValidNumber',
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'ON',
                    'Type': 'ContentType',
                }
            },
            'Language': []
        },
        {
            'QuestionText': 'Did anyone in your household consume milk or milk products in the last 30 days?',
            'DataExportTag': 'Q10',
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'SubSelector': 'TX',
            'ChoiceOrder': [
                1,
                2
            ],
            'Choices': {
                '1': {
                    'Display': 'Yes'
                },
                '2': {
                    'Display': 'No'
                }
            },
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'ppi_in_s_milk',
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'VariableNaming': {
                '1': 'Yes',
                '2': 'No'
            },
            'Language': []
        },
        {
            'QuestionText': 'Does the household have an electric fan?',
            'DataExportTag': 'Q11',
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'SubSelector': 'TX',
            'ChoiceOrder': [
                1,
                2
            ],
            'Choices': {
                '1': {
                    'Display': 'Yes'
                },
                '2': {
                    'Display': 'No'
                }
            },
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'ppi_in_s_fan',
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'VariableNaming': {
                '1': 'Yes',
                '2': 'No'
            },
            'Language': []
        },
        {
            'QuestionText': 'Does the household have a stove or gas burner?',
            'DataExportTag': 'Q12',
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'SubSelector': 'TX',
            'ChoiceOrder': [
                1,
                2
            ],
            'Choices': {
                '1': {
                    'Display': 'Yes'
                },
                '2': {
                    'Display': 'No'
                }
            },
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'ppi_in_s_stove',
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'VariableNaming': {
                '1': 'Yes',
                '2': 'No'
            },
            'Language': []
        },
        {
            'QuestionText': 'Does the household have a pressure cooker or pressure pan?',
            'DataExportTag': 'Q13',
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'SubSelector': 'TX',
            'ChoiceOrder': [
                1,
                2
            ],
            'Choices': {
                '1': {
                    'Display': 'Yes'
                },
                '2': {
                    'Display': 'No'
                }
            },
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
            },
            'QuestionDescription': 'ppi_in_s_pressurecooker',
            'Validation': {
                'Settings': {
                    'ForceResponse': 'OFF',
                    'ForceResponseType': 'OFF',
                    'Type': 'None'
                }
            },
            'VariableNaming': {
                '1': 'Yes',
                '2': 'No'
            },
            'Language': []
        },
    ]
