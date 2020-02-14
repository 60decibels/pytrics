# Pytrics

Python based Qualtrics survey integration.

This repository contains code to work with the Qualtrics API and to create surveys from the provided template definitions and download responses to these surveys for anaylsis and processing.

## Getting started

This code is wirtten using Python 3, please ensure you have v3 installed before proceeding.

### Setup

- run `python3 -m venv env` to create a virtual environement named env
- run `source env/bin/activate` to activate the virtualenv
- run `pip3 install -r dev-requirements.txt` to install required packages into your virtual environments, (including those required for development and testing)

### Running the tests

Tests are written using unittest and can be executed via [nose](https://nose.readthedocs.io/en/latest/index.html). Some example commands are below, refer to [the docs](https://nose.readthedocs.io/en/latest/usage.html) for more options and information.

- Run all tests;

```bash
nosetests
```

- Run specific tests;

```bash
nosetests tests/qualtrics_api/client/question/build_question_display_logic_tests.py
```

- Run all tests, collect coverage of the contents of the code dir, produce html coverage report and enforce minimum percentage, with verbose and colourful output;

```bash
nosetests --with-coverage --cover-erase --cover-package=pytrics/. --cover-html --cover-min-percentage=70 -v --rednose
```

### Linting the code

```bash
PYTHONPATH=$PYTHONPATH:$(pwd) pylint -f parseable pytrics/*
```

#### Lint the tests if you like

```bash
PYTHONPATH=$PYTHONPATH:$(pwd) pylint -f parseable tests/*
```

## Working with surveys

The two main use cases for this package are creating surveys on Qualtrics and retirieving responses to these, read on for instructions on how to use this code.

### Qualtrics

You will need a Qualtrics account before you can use this code, assuming you have an active account please [login here](https://login.qualtrics.com/login).

You will need to generate an API Key for access to the Qualtrics Survey Platform, [please read the following page for instructions](https://www.qualtrics.com/support/integrations/api-integration/overview/).

Documentation for the survey platform API [can be found here](https://api.qualtrics.com/reference). This repository implements many of the main API endpoints documented here in order to create and publish surveys as well as retrieve responses.

### Environment Variables

Copy your API authorisation token and set an environment variable named `QUALTRICS_API_AUTH_TOKEN` to the token value;

```bash
export QUALTRICS_API_AUTH_TOKEN=your_api_token
```

Next we need to do the same with the base API url. This varies depending on your Qualtrics account (and the data centre you are using), for more information [see the documentation here](https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/#LocatingtheDatacenterID). Once you figure out your APIs base url add it to an environment variable as per below;

```bash
export QUALTRICS_API_BASE_URL=your_base_api_url
```

### Creating a Survey

This repository provides country specific templates for [60 Decibels](https://www.60decibels.com) Standard Agriculture Survey, which can be created in Qualtrics using the code below.

```python
>>> from pytrics.tools import Tools
>>> tools = Tools()
>>> tools.create_survey_from_definition('My new agriculture survey', 'et')
>>> ('https://survey.eu.qualtrics.com/jfe/form/SV_123456abcdef', '9223370455272972495', 2, '2020-02-12T08:16:43Z')
>>>
```

The above code shows the result of creating a new survey using the Ethiopian template (as denoted by the 2nd parameter of 'et'). This survey is published and ready to accept responses on the returned URL.

#### Supported Countries

We have provided survey definitions for each of the following countries (their two character iso code is provided in brackets for reference);

1. Ethiopia (et)
2. India (in)
3. Kenya (ke)
4. Nigeria (ng)
5. Tanzania (tz)

#### Supported Languages

At present we have only provided survey definitions in English.

#### Extending this code

You can define your own template surveys and create these in Qualtrics using the same process if you fork or clone this repository and make the necessary changes to the code.

The `create_survey_from_definition` function in `pytrics/pytrics.py` could be easily extended to accept further survey types, this could also be extended to support multiple languages quite easily should you wish to do this.

### Collecting Response Data

To gather response data from a specific survey you can use the code below.

```python
>>> from pytrics.tools import Tools
>>> tools = Tools()
>>> tools.retrieve_survey_response_data('SV_123456abcdef')
>>> ('data/SV_123456abcdef.json', 'data/SV_123456abcdef_responses.zip', 'data/SV_123456abcdef_responses.json', 'data/SV_123456abcdef_responses_processed.json')
>>>
```

The function `retrieve_survey_response_data` queries the Qualtrics API and saves data to disk in four JSON files and returns the paths to these.

1. The first file contains the survey defintion
2. The second file contains any recorded responses to this survey in zip form as provided by Qualtrics.
3. The third file is the unzipped response data as provided by Qualtrics.
4. The last file is the processed response data in a form more easily readable and consumable (see below in this README for an example).

All files are returned as you may wish/need to use the survey definition to understand and process the content of the response data file. The processed responses file is provided to help ease the consumption and usage of this data.

### Helper Functions

The `pytrics/pytrics.py` module also contains three helper functions which were particularly useful when implementing the various functionality contained in this repository. These are `copy`, `describe` and `summarise_definition`.

```python
>>> from pytrics.tools import Tools
>>> tools = Tools()
```

- `copy` allows you to copy an existing survey to a new name within your Qualtrics account. It expects two parameters, the Qualtrics survey identifier and a new name for the copy it will create. Example usage below:

```python
>>> tools.copy('SV_123456abcdef', 'My New Survey Name')
```

- `describe` allows you to describe an existing survey in your Qualtrics account to a file on your local disk so you can review the blocks, questions and flow of this survey. It expects one parameter, the Qualtrics survey identifier. Example usage below:

```python
>>> tools.describe('SV_123456abcdef')
```

- `summarise_definition` produces a summary of the specified survey definition so you can easily see the questions that the survey contains and their order. It expects one paramater, a lower case two character iso country code from those supported. Example usage below:

```python
>>> tools.summarise_definition('et')
```

More details of these helper functions can be found in the code at `pytrics/pytrics.py`.

## Improving this Code

Feel free to fork or clone this repository and iterate on the functionality provided to suit your purposes, please ensure you include the `LICENSE` file in all copies or substantial portions of the Software.

## License

This code is not actively maintained but it is provided under [the MIT licence](https://opensource.org/licenses/MIT) and therefore free to copy, use and amend. Please refer to the `LICENSE` file contained in this repository for full terms of use and ensure you include the LICENSE file in all copies or substantial portions of the Software that you create.

## Further Context

The following information provides more information which may be of use to you when working with Qualtrics and surveys.

### Blocks

Questions within Qualtrics surveys can be organised into sections, or Blocks as they are called. 

[Qualtrics documentation](https://www.qualtrics.com/support/survey-platform/survey-module/block-options/block-options-overview/) describes blocks as _“…sets of questions within your survey. Typically, questions are separated into blocks for the purpose of conditionally displaying an entire block of questions, or for randomly presenting entire blocks of questions… Blocks can also be used to organize longer surveys…“_.

We have made use of blocks to organise the survey definitions as they contain many questions and this organisation helps when managing these surveys. We have also implemented some branching display logic within the Information block so as to present relevant questions depending on the answers given by the respondent when they take the survey. Using blocks allows us to more easily contain and manage this display logic.

### Mandatory and Non-Mandatory Questions

We have made some of the questions mandatory, where they relate to metadata around the survey and response, however, the questions asked of respondents are non-mandatory. This is intentional to improve overall response rates. This can be amended in the survey definitions if so desired but we have found that forcing respondents to answer questions reduces response rates and therefore the amount of data captured.

### Summary of Survey Definition

The code in the repository provides a number of helper functions beyond the ability to create a survey and download its responses.

The `summarise_definition` function provides the ability to summarise the survey definition into a more easily readable form, an example of the summarised definition of the Nigerian survey is shown below:

```python
[   ('Block Number', 'Block Name'),
    (1, 'Start Survey'),
    (2, 'Profile & Acquisition'),
    (3, 'First Access'),
    (4, 'Information'),
    (5, 'NPS'),
    (6, 'Way of Farming'),
    (7, 'Quality of Life'),
    (8, 'Change in Confidence'),
    (9, 'Money Spent'),
    (10, 'Alternatives'),
    (11, 'Challenges'),
    (12, 'Retention'),
    (13, 'HH Size'),
    (14, 'Farmed Land & Ownership'),
    (15, 'Share of HH Income - Company'),
    (16, 'Share of HH Income - All Farming'),
    (17, 'Poverty Probability Index - Nigeria'),
    (18, 'Gender'),
    (19, 'Age'),
    (20, 'End Survey')]
[   ('Block Number', 'Question Label', 'Question Text'),
    (1, 'survey_date', 'Date of Interview (yyyy-mm-dd)'),
    (1, 'survey_start_time', 'Survey Start Time (hh:mm)'),
    (1, 'survey_consent_yn', 'Can I continue with the survey?'),
    (2, 'ag_profile_usage_mainperson_mc', 'In your household, who is the main person who manages the {Crop name} crop?'),
    (2, 'acquisition_howhear_mc', 'How did you first hear about {Company} information?'),
    (2, 'respondent_tenure', 'How many months back did you start interacting with {Company}?'),
    (3, 'prioraccess_yn', 'Before you started interacting with {Company}, did you have access to information like that which {Company} provides?'),
    (4, 'ag_experience_training_understand_mc', 'How much of this information was easy to understand?'),
    (4, 'ag_experience_training_useful_mc', 'How much of this information is useful (to your work)?'),
    (4, 'ag_experience_training_apply_mc', 'How much of this information did you apply to your {Crop name} crop?'),
    (4, 'ag_experience_training_apply_time_mc', 'How soon after receiving the information did you apply the lessons (for the first time)?'),
    (4, 'ag_experience_training_apply_easiest_oe', 'Can you please explain what you found easiest to apply?'),
    (4, 'ag_experience_training_apply_hardest_oe', 'Can you please explain what you found hardest to apply?'),
    (4, 'ag_experience_training_apply_barriers_mc', 'Would you mind sharing with me what prevented you from applying the information?'),
    (4, 'ag_experience_training_apply_consider_yn', 'Did you consider (think about) applying the information?'),
    (4, 'ag_experience_training_apply_intention_mc', 'Do you intend to apply the information next year?'),
    (4, 'ag_experience_training_wtp_mc', 'Do you think other farmers would pay for the {Company} information?'),
    (5, 'nps_company_rating', 'On a scale of 0-10, how likely is it that you would recommend the {Company} information to a friend, where 0 is not at all likely and 10 is extremely likely?'),
    (5, 'nps_company_promoter_oe', 'What specifically about {Company} would cause you to recommend it to a friend?'),
    (5, 'nps_company_passive_oe', 'What specifically about {Company} caused you to give it the score that you did?'),
    (5, 'nps_company_detractor_oe', 'What actions could {Company} take to make you more likely to recommend it to a friend?'),
    (6, 'ag_impact_way_of_farming_rating', 'Has your way of farming changed because of {Company} information?'),
    (6, 'ag_impact_way_of_farming_improve_oe', 'How has it improved?'),
    (6, 'ag_impact_way_of_farming_nochange_oe', 'Why has it not changed?'),
    (6, 'ag_impact_way_of_farming_worse_oe', 'How has it become worse?'),
    (7, 'qol_rating', 'Has your quality of life changed because of {Company} information?'),
    (7, 'qol_improve_oe', 'How has it improved?'),
    (7, 'qol_nochange_oe', 'Why has it not changed?'),
    (7, 'qol_worse_oe', 'How has it become worse?'),
    (8, 'ag_impact_confidence_rating', 'Has your confidence that you will be able to grow and sell a healthy {Crop name} crop changed because of {Company} information?'),
    (9, 'impact_moneyspend_rating', 'Has the money you spend on {Crop name} crop changed because you started working with {Company} information?'),
    (9, 'impact_moneyspend_comfort_rating', 'Are you comfortable with this increase?'),
    (10, 'alternatives_yn', 'Could you easily find a good alternative to {Company} information?'),
    (10, 'alternatives_mc', 'Would you be comfortable sharing who these alternatives are?'),
    (10, 'alternatives_comparison_rating', 'Compared to the alternative, do you think {Company} is...'),
    (10, 'alternatives_comparison_oe', 'Please explain how {Company} is better/worse?'),
    (11, 'challenges_yn', 'Have you experienced any challenges with {Company}?'),
    (11, 'challenges_oe', 'Please explain the challenge you have had with {Product/Service}'),
    (11, 'challenges_resolve_yn', 'Has your challenge been resolved?'),
    (12, 'retention_improve_oe', 'What can {Company} do to serve you better?'),
    (12, 'retention_1year_rating', 'Do you see yourself working with {Company} next year?'),
    (12, 'retention_5year_rating', 'Do you see yourself working with {Company} 5 years from now?'),
    (13, 'respondent_hhsize_num', 'Including yourself, how many people live in your home?'),
    (14, 'ag_profile_land_farmedpastyear_num', 'How much total land did you use for farming in the last 12 months? Consider all crops planted. (acres)'),
    (14, 'ag_profile_land_proportioncrop_num', 'How many of these [acres from total] did you farm with {Crop name} in last 12 months? (acres)'),
    (15, 'ag_profile_income_hhshare_company_num', 'In the last 12 months, what proportion (%) of your household’s total income, came from {Crop name} crop using {Company}’s information?'),
    (15, 'ag_profile_income_hhshare_company_mc', '(If unable to give an exact percentage, share these options) In the last 12 months, what proportion (%) of your household’s total income, came from {Crop name} crop using {Company}’s information?'),
    (16, 'ag_profile_income_hhshare_allfarming_num', 'In the last 12 months, what proportion (%) of the total harvest from all your land did you sell?'),
    (16, 'ag_profile_income_hhshare_allfarming_mc', '(If unable to give an exact percentage, share these options) In the last 12 months, what proportion (%) of the total harvest from all your land did you sell?'),
    (17, 'ppi_ng_s_zone', 'Which zone does the household reside in?'),
    (17, 'ppi_ng_s_hhsize', 'How many members does the household have?'),
    (17, 'ppi_ng_s_rice', 'Within the past 7 days, did the members of this household eat any rice or wheat within the household?'),
    (17, 'ppi_ng_s_bread', 'Within the past 7 days, did the members of this household eat any bread within the household?'),
    (17, 'ppi_ng_s_beef', 'Within the past 7 days, did the members of this household eat any beef within the household?'),
    (17, 'ppi_ng_s_fan', 'Does the household own a fan?'),
    (18, 'gn_familydynamics_important_decisions_mc', 'Who in your family made most of the important decisions related to {Crop name} crop?'),
    (18, 'gn_familydynamics_work_burden_oe', 'Who in your family did most of the work related to {Crop name} crop?'),
    (18, 'gn_familydynamics_money_from_sale_mc', 'Who in your family handled the money that came from {Crop name} crops?'),
    (19, 'respondent_age_num', 'What is your age?'),
    (20, 'retention_anythingelse_oe', 'Is there anything else you would like to share?'),
    (20, 'survey_anonymity_yn', 'At the beginning of the call I said we would keep your name and details private. Now that you know what you have shared with me today, are you happy for me to share your name and this information with {Company} or would you prefer to remain anonymous?'),
    (20, 'survey_marketingmaterials_yn', 'Do you mind if some of your answers and your name are used when making marketing materials?'),
    (20, 'respondent_gender_mc', 'Gender of Respondent'),
    (20, 'survey_end_time', 'Survey End Time (hh:mm)')]
```

Each survey is essentially the same, except for the Poverty Probability Index questions in block 17, these vary per country as the measure of poverty is relative depending on geographic location.

### Example of Processed Response Data

The processed response data is written to a json file and when read into python this is a list of dictionaries.

Each dictionary in the list represents one response and has a top-level key that is the unique response identifier from Qualtrics.

The value of each response identifier key is a nested dictionary which has key, value pairs holding answers to each question answered by the respondent during the response.

The key, value pairs take the form of `"question_label": ”Answer selected / entered”`

In some cases, where we have multiple choice questions the value may be a list of answers selected by the user:

`"ag_profile_usage_mainperson_mc": ["Another family member"]`

In other cases where some of the multiple choice answers require the respondent to enter text, we extend the question label used for the key with the option chosen and the value is then the entered text, for example:

`"ag_profile_usage_mainperson_mc_another_family_member": "Child"`

A list containing one example response is shown below, note that some question labels do not appear, as these were not answered by the respondent (as we do not enforce mandatory questions in our survey definitions).

```python
[
  {
    "R_5oiKUFi6JyNQ7ol": {
      "survey_date_TEXT": "2020-02-12",
      "survey_start_time_TEXT": "16:42",
      "survey_consent_yn": "Yes",
      "ag_profile_usage_mainperson_mc": [
        "Another family member"
      ],
      "ag_profile_usage_mainperson_mc_another_family_member": "Child",
      "acquisition_howhear_mc": "Sensitization event / group meeting / community meeting",
      "respondent_tenure": [
        "Months"
      ],
      "respondent_tenure_years": "2",
      "respondent_tenure_months": "3",
      "prioraccess_yn": "No",
      "ag_experience_training_understand_mc": "3- Some",
      "ag_experience_training_useful_mc": "3- Some",
      "ag_experience_training_apply_mc": "1- None",
      "ag_experience_training_apply_barriers_mc": [
        "Recommended materials or equipment not available"
      ],
      "ag_experience_training_apply_consider_yn": "Yes",
      "ag_experience_training_apply_intention_mc": "Yes, maybe",
      "ag_experience_training_wtp_mc": "Yes, maybe",
      "nps_company_rating_NPS_GROUP": 1,
      "nps_company_rating": "6",
      "nps_company_detractor_oe_TEXT": "actions",
      "ag_impact_way_of_farming_rating": "Got slightly worse",
      "ag_impact_way_of_farming_worse_oe_TEXT": "worse",
      "qol_rating": "Slightly improved",
      "qol_improve_oe_TEXT": "slightly",
      "ag_impact_confidence_rating": "No change",
      "impact_moneyspend_rating": "Slightly increased",
      "impact_moneyspend_comfort_rating": "Yes, partly",
      "alternatives_yn": "Maybe",
      "alternatives_mc": "Open market",
      "alternatives_comparison_rating": "Worse",
      "challenges_yn": "Yes",
      "challenges_oe_TEXT": "setsetset",
      "challenges_resolve_yn": "No",
      "retention_improve_oe_TEXT": "qwetwetweqt",
      "retention_1year_rating": "Yes, maybe",
      "retention_5year_rating": "Yes, maybe",
      "respondent_hhsize_num_TEXT": 35,
      "ag_profile_land_farmedpastyear_num_TEXT": 35,
      "ag_profile_land_proportioncrop_num_TEXT": 35,
      "ag_profile_income_hhshare_company_num": "Unable to answer",
      "ag_profile_income_hhshare_allfarming_num": "Don't have land",
      "ppi_ng_s_zone": "South East",
      "ppi_ng_s_hhsize": "5, 6 or 7",
      "gn_familydynamics_important_decisions_mc": [
        "Adult Male HH Member"
      ],
      "gn_familydynamics_work_burden_oe": [
        "Other Female"
      ],
      "gn_familydynamics_work_burden_oe_other_male": "sdfdsfdsf",
      "gn_familydynamics_work_burden_oe_other_female": "fdafsdf",
      "gn_familydynamics_money_from_sale_mc": [
        "Adult Male HH Member"
      ],
      "respondent_age_num_TEXT": 99,
      "retention_anythingelse_oe_TEXT": "nope",
      "survey_anonymity_yn": "No, please keep me anonymous",
      "survey_marketingmaterials_yn": "Yes, you may use",
      "respondent_gender_mc": "Female",
      "survey_end_time_TEXT": "14:49"
    }
  }
]
```

The processed form of the response data links the answers given to the labels of the questions so that this data is more readable and consumable by whatever process or system users of this code are working on.
