# Pytrics

Python based Qualtrics survey integration.

This repository contains code to work with the Qualtrics API and to create surveys from the provided template definitions and download responses to these surveys for analysis and processing.

## Usage

```bash
python3 -m venv env

source env/bin/activate

pip3 install -r dev-requirements.txt

pip3 install pytrics

export QUALTRICS_API_AUTH_TOKEN=your_api_token

export QUALTRICS_API_BASE_URL=your_base_api_url

export ABSOLUTE_PATH_TO_DATA_DIR=/absolute/path/on/disk/to/store/output

```

```python
from pytrics.tools import Tools
tools = Tools()


tools.create_survey_from_definition('My new agriculture survey', 'et')
Creating Blocks |################################| 20/20
Creating Questions |################################| 66/66
('https://survey.eu.qualtrics.com/jfe/form/SV_123456abcdef', '9223370455272972495', 2, '2020-02-12T08:16:43Z')


tools.retrieve_survey_response_data('SV_123456abcdef')
('data/SV_123456abcdef.json', 'data/SV_123456abcdef_responses.zip', 'data/SV_123456abcdef_responses.json', 'data/SV_123456abcdef_responses_processed.json')


tools.summarise_definition('et')
'data/et_definition_summary.json'
```

Read on for more information about working with surveys using Qualtrics and this package.

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

Next we need to create an environment variable for your base API url called `QUALTRICS_API_BASE_URL`. 

This varies depending on your Qualtrics account (and the data centre you are using), for more information [see the documentation here](https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/#LocatingtheDatacenterID). Once you figure out your APIs base url add it to an environment variable as per below;

```bash
export QUALTRICS_API_BASE_URL=your_base_api_url
```

Finally we need to set an environment variable called `ABSOLUTE_PATH_TO_DATA_DIR` to tell this package where on disk it should store output data files:

```bash
export ABSOLUTE_PATH_TO_DATA_DIR=/absolute/path/on/disk/to/store/output
```

### Creating a Survey

This repository provides country specific templates for [60 Decibels](https://www.60decibels.com) Standard Agriculture Survey, which can be created in Qualtrics using the code below.

```python
>>> from pytrics.tools import Tools
>>> tools = Tools()
>>> 
>>> tools.create_survey_from_definition('My new agriculture survey', 'et')
Creating Blocks |################################| 20/20
Creating Questions |################################| 66/66
('https://survey.eu.qualtrics.com/jfe/form/SV_123456abcdef', '9223370455272972495', 2, '2020-02-12T08:16:43Z')
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
>>> 
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

### Summarising a Survey Definition

The `summarise_definition` function produces a summary of the specified survey definition so you can easily see the questions that the survey contains and their order. This can be used to generate a call script for researchers to use when delivering the survey via telephone. It expects one paramater, a lower case two character iso country code from those supported. Example usage below:

```python
>>> tools.summarise_definition('et')
```

## PPI (Poverty Probability Index)

Part of our standard surveys is a series of questions designed to allow you to measure the likelihood that a given household is living below the poverty line. The questions we use have been sourced from [The Poverty Index](https://www.povertyindex.org).

Tools to calculate the PPI (on a per country basis) based on the answers to the questions in our surveys are available to download for free from [The Poverty Index](https://www.povertyindex.org/ppi-country) (requires registration of free account).

## Extending and improving this Code

Feel free to fork or clone this repository and iterate on the functionality provided to suit your purposes, please ensure you include the `LICENSE.txt` file in all copies or substantial portions of the Software.

### Getting started

This code is written using Python 3, please ensure you have v3 installed before proceeding.

#### Setup

- run `python3 -m venv env` to create a virtual environement named env
- run `source env/bin/activate` to activate the virtualenv
- run `pip3 install -r dev-requirements.txt` to install required packages into your virtual environment, (including those required for development and testing)

#### Running the tests

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

#### Linting the code

```bash
PYTHONPATH=$PYTHONPATH:$(pwd) pylint -f parseable pytrics/*
```

#### Lint the tests if you like

```bash
PYTHONPATH=$PYTHONPATH:$(pwd) pylint -f parseable tests/*
```

## License

This code is not actively maintained but it is provided under [the GPLv2 licence](https://opensource.org/licenses/GPL-2.0). Please refer to the `LICENSE.txt` file contained in this repository for full terms of use and ensure you include the LICENSE.txt file in all copies or substantial portions of the Software that you create.

## Further Context

The following section provides more information which may be of use to you when working with Qualtrics and surveys.

### Blocks

Questions within Qualtrics surveys can be organised into sections, or Blocks as they are called.

[Qualtrics documentation](https://www.qualtrics.com/support/survey-platform/survey-module/block-options/block-options-overview/) describes blocks as _“…sets of questions within your survey. Typically, questions are separated into blocks for the purpose of conditionally displaying an entire block of questions, or for randomly presenting entire blocks of questions… Blocks can also be used to organize longer surveys…“_.

We have made use of blocks to organise the survey definitions as they contain many questions and this organisation helps when managing these surveys. We have also implemented some branching display logic within the Information block so as to present relevant questions depending on the answers given by the respondent when they take the survey. Using blocks allows us to more easily contain and manage this display logic.

### Mandatory and Non-Mandatory Questions

We have made some of the questions mandatory, where they relate to metadata around the survey and response, however, the questions asked of respondents are non-mandatory. This is intentional to improve overall response rates.

This can be amended in the survey definitions if so desired but we have found that forcing respondents to answer questions reduces response rates and therefore the amount of data captured.

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
