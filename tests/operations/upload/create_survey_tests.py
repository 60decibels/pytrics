import unittest
from unittest.mock import MagicMock, patch, call

from pytrics.common.constants import QUALTRICS_API_BLOCK_TYPE_STANDARD
from pytrics.common.exceptions import QualtricsAPIException

from pytrics.operations.upload import create_survey
from .reference_data import (
    get_test_blocks,
    get_test_question_params,
    get_test_question_payloads,
)


class CreateSurveyTestCase(unittest.TestCase):

    def setUp(self):
        get_details_for_client_patch = patch('pytrics.operations.upload.get_details_for_client')
        self.get_details_for_client = get_details_for_client_patch.start()
        self.addCleanup(get_details_for_client_patch.stop)

        self.get_details_for_client.return_value = ('URL', 'TOKEN')

        QualtricsAPIClient_patch = patch('pytrics.operations.upload.QualtricsAPIClient')
        self.QualtricsAPIClient = QualtricsAPIClient_patch.start()
        self.addCleanup(QualtricsAPIClient_patch.stop)

        self.api = MagicMock(base_api_url='URL', auth_token='TOKEN')
        self.QualtricsAPIClient.return_value = self.api

        self.api.create_survey.return_value = ('SV_0123456789a', 'BL_0123456789a')

        self.blocks = get_test_blocks()

        self.api.create_block.side_effect = [
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "ec428cb1-5426-48d1-84db-0127f79bfec3"
                    },
                    "result": {
                        "BlockID": "BL_0123456789b",
                        "FlowID": "FL_2"
                    }
                },
                'BL_0123456789b'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "722c603e-ed67-4e0f-bcbe-a624f27ff17d"
                    },
                    "result": {
                        "BlockID": "BL_0123456789c",
                        "FlowID": "FL_3"
                    }
                },
                'BL_0123456789c'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "722c603e-ed67-4e0f-bcbe-a624f27ff17d"
                    },
                    "result": {
                        "BlockID": "BL_0123456789d",
                        "FlowID": "FL_4"
                    }
                },
                'BL_0123456789c'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "722c603e-ed67-4e0f-bcbe-a624f27ff17d"
                    },
                    "result": {
                        "BlockID": "BL_0123456789e",
                        "FlowID": "FL_5"
                    }
                },
                'BL_0123456789c'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "722c603e-ed67-4e0f-bcbe-a624f27ff17d"
                    },
                    "result": {
                        "BlockID": "BL_0123456789f",
                        "FlowID": "FL_6"
                    }
                },
                'BL_0123456789c'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "722c603e-ed67-4e0f-bcbe-a624f27ff17d"
                    },
                    "result": {
                        "BlockID": "BL_0123456789g",
                        "FlowID": "FL_7"
                    }
                },
                'BL_0123456789c'
            )
        ]

        self.question_params = get_test_question_params()

        self.api.build_question_payload.side_effect = get_test_question_payloads()

        self.api.find_question_in_survey_by_label.side_effect = [
            ('QID1', {},),
            ('QID1', {},),
            ('QID1', {},),
            ('QID5', {},),
            ('QID5', {},),
            ('QID5', {},),
        ]

        self.api.create_question.side_effect = [
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "3a17080d-4265-4915-b55c-492838390f50"
                    },
                    "result": {
                        "QuestionID": "QID1"
                    }
                },
                'QID1'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "bff915d4-295c-4d54-9a49-b10f0cff005a"
                    },
                    "result": {
                        "QuestionID": "QID2"
                    }
                },
                'QID2'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "356c8ea0-c203-4068-9ee0-5045880020a9"
                    },
                    "result": {
                        "QuestionID": "QID3"
                    }
                },
                'QID3'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "4af6602b-1505-423d-ae53-63fcbcdd8da0"
                    },
                    "result": {
                        "QuestionID": "QID4"
                    }
                },
                'QID4'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "614a9bfa-c89b-4650-8cb1-b11e89b4c527"
                    },
                    "result": {
                        "QuestionID": "QID5"
                    }
                },
                'QID5'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "79e15242-52d4-464d-b66a-210a77392b66"
                    },
                    "result": {
                        "QuestionID": "QID6"
                    }
                },
                'QID6'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "f1b63147-5b60-422b-8e25-9fb24da43710"
                    },
                    "result": {
                        "QuestionID": "QID7"
                    }
                },
                'QID7'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "da0db5c9-7308-47e8-875a-3848b1ed2c10"
                    },
                    "result": {
                        "QuestionID": "QID8"
                    }
                },
                'QID8'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "11ce2805-dabe-4177-a754-13a376795dd7"
                    },
                    "result": {
                        "QuestionID": "QID9"
                    }
                },
                'QID9'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "00a079f8-7161-4644-a47e-c74f8772fba0"
                    },
                    "result": {
                        "QuestionID": "QID10"
                    }
                },
                'QID10'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "b61d6120-38da-4c83-8b0d-c311d964c0c9"
                    },
                    "result": {
                        "QuestionID": "QID11"
                    }
                },
                'QID11'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "dcec0efa-2dd4-4831-83d3-27af27c6e528"
                    },
                    "result": {
                        "QuestionID": "QID12"
                    }
                },
                'QID12'
            ),
            (
                {
                    "meta": {
                        "httpStatus": "200 - OK",
                        "requestId": "fe955bba-8ca9-4032-b898-b4daac452a8a"
                    },
                    "result": {
                        "QuestionID": "QID13"
                    }
                },
                'QID13'
            )
        ]

    def test_asserts_blocks_and_questions_params(self):
        with self.assertRaises(AssertionError):
            create_survey('name', None, None)

            create_survey('name', [], [])

            create_survey('name', [{}], [])

            create_survey('name', [], [{}])

    def test_calls_client_create_survey(self):
        # use 1st block (but put it in a list as a list is expected)
        # and the NPS questions only (assigned to block 1 in reference data)
        create_survey('My Survey Name', [self.blocks[0]], self.question_params[0:3])

        self.api.create_survey.assert_called_once_with('My Survey Name', 'EN')

    def test_raises_custom_exception_when_client_create_survey_fails_to_return_expected_values(self):
        self.api.create_survey.return_value = ('SV_0123456789a', None)
        with self.assertRaises(QualtricsAPIException):
            create_survey('My Survey Name', [{}], [{}])

        self.api.create_survey.return_value = (None, 'BL_0123456789a')
        with self.assertRaises(QualtricsAPIException):
            create_survey('My Survey Name', [{}], [{}])

    def test_calls_client_update_block_on_default_survey_block(self):
        # 1st block only, NPS questions
        create_survey('My Survey Name', self.blocks[0:1], self.question_params[0:3])

        # note for 1st block we use the type of 'Default', as a survey has to have a default block, and is created with one (the 1st block of a survey)
        self.api.update_block.assert_called_once_with('SV_0123456789a', 'BL_0123456789a', self.blocks[0]['description'], 'Default')

    def test_assigns_question_to_default_block_when_block_specified_on_question_not_provided(self):
        question_payloads = get_test_question_payloads()

        create_survey('My Survey Name', self.blocks[0:1], self.question_params[0:8])

        # note that all these calls use the default block ID as no 2nd block provided
        # (despite question params specifying block 2)
        create_question_calls = [
            call('SV_0123456789a', question_payloads[0], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[1], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[2], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[3], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[4], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[5], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[6], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[7], 'BL_0123456789a'),
        ]

        self.api.update_block.assert_called_once_with('SV_0123456789a', 'BL_0123456789a', self.blocks[0]['description'], 'Default')

        self.api.create_block.assert_not_called()

        self.api.create_question.assert_has_calls(create_question_calls)

    def test_calls_create_block_for_blocks_two_onwards_in_params(self):
        # all 3 blocks, all questions
        create_survey('My Survey Name', self.blocks, self.question_params)

        create_block_calls = [
            call('SV_0123456789a', 'QOL Block', QUALTRICS_API_BLOCK_TYPE_STANDARD),
            call('SV_0123456789a', 'PPI Block A', QUALTRICS_API_BLOCK_TYPE_STANDARD),
            call('SV_0123456789a', 'PPI Block B', QUALTRICS_API_BLOCK_TYPE_STANDARD),
            call('SV_0123456789a', 'PPI Block C', QUALTRICS_API_BLOCK_TYPE_STANDARD),
            call('SV_0123456789a', 'PPI Block D', QUALTRICS_API_BLOCK_TYPE_STANDARD),
            call('SV_0123456789a', 'PPI Block E', QUALTRICS_API_BLOCK_TYPE_STANDARD)
        ]

        self.api.create_block.assert_has_calls(create_block_calls)

    def test_calls_create_question_but_not_update_question_as_expected(self):
        question_payloads = get_test_question_payloads()

        # all blocks, all questions
        create_survey('My Survey Name', self.blocks, self.question_params)

        build_question_payload_calls = [
            call(question_param, 'SV_0123456789a', include_display_logic=True) for question_param in self.question_params
        ]

        self.api.build_question_payload.assert_has_calls(build_question_payload_calls)

        create_question_calls = [
            call('SV_0123456789a', question_payloads[0], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[1], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[2], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[3], 'BL_0123456789a'),
            call('SV_0123456789a', question_payloads[4], 'BL_0123456789b'),
            call('SV_0123456789a', question_payloads[5], 'BL_0123456789b'),
            call('SV_0123456789a', question_payloads[6], 'BL_0123456789b'),
            call('SV_0123456789a', question_payloads[7], 'BL_0123456789b'),
            call('SV_0123456789a', question_payloads[8], 'BL_0123456789c'),
            call('SV_0123456789a', question_payloads[9], 'BL_0123456789c'),
            call('SV_0123456789a', question_payloads[10], 'BL_0123456789c'),
            call('SV_0123456789a', question_payloads[11], 'BL_0123456789c'),
            call('SV_0123456789a', question_payloads[12], 'BL_0123456789c'),
        ]

        self.api.create_question.assert_has_calls(create_question_calls)

        self.api.update_question.assert_not_called()
