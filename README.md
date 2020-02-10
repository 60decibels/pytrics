# Pytrics

Python based Qualtrics survey integration.

This repository contains code to work with the Qualtrics API and to create surveys from template definitions and download responses to these for anaylsis and processing.

## Getting started

This code is wirtten using Python 3, please ensure you have v3 installed before proceeding.

### Setup

- run `python3 -m venv env` to create a virtual environement named env
- run `source env/bin/activate` to activate the virtualenv
- run `pip3 install -r dev-requirements.txt` to install required packages into your virtual environments, (including those required for development and testing)

## Running the tests

Tests are written using unittest and can be executed via [nose](https://nose.readthedocs.io/en/latest/index.html). Some example commands are below, refer to [the docs](https://nose.readthedocs.io/en/latest/usage.html) for more options and information.

- Run all tests;

```bash
nosetests -w pytrics
```

- Run all tests, collect coverage of the contents of the code dir, produce html coverage report and enforce minimum percentage, with colourful output;

```bash
nosetests -w pytrics --with-coverage --cover-erase --cover-package=pytrics/. --cover-html --cover-min-percentage=80 -v --rednose
```

## Linting the code

```bash
PYTHONPATH=$PYTHONPATH:$(pwd) pylint -f parseable pytrics/*
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
export QUALTRICS_API_AUTH_TOKEN=<your_token_value>
```

Next we need to do the same with the base API url. This varies depending on your Qualtrics account (and the data centre you are using), for more information [see the documentation here](https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/#LocatingtheDatacenterID). Once you figure out your APIs base url add it to an environment variable as per below;

```bash
export QUALTRICS_API_BASE_URL=<your_base_api_url>
```

### Creating a Survey

This repository provides country specific templates for [60 Decibels](www.60decibels.com) Standard Agriculture Survey, which can be created in Qualtrics using the code below.

```python
>>> from pytrics import create_survey_from_definition
>>> create_survey_from_definition('My new agriculture survey', 'et')
>>> https://survey.eu.qualtrics.com/jfe/form/SV_123456abcdef
>>>
```

The above code shows the result of creating a new survey using the Ethiopian template. This survey is published and ready to accept responses on the returned URL.

We have provided survey definitions for each of the following countries;

1. Ethiopia
2. India
3. Kenya
4. Nigeria
5. Tanzania

#### Extending this code

You can define your own template surveys and create these in Qualtrics using the same process if you fork or clone this repository and make the necessary changes to the code.

The `create_survey_from_definition` function in `pytrics/pytrics.py` could be easily extended to accept further survey types, this could also be extended to support multiple languages quite easily should you wish to do this.

### Collecting Response Data

To gather response data from a specific survey you can use the code below.

```python
>>> from pytrics import retrieve_survey_response_data
>>> retrieve_survey_response_data('SV_123456abcdef')
>>> 'data/SV_123456abcdef.json', 'data/SV_123456abcdef_responses.json'
>>>
```

The function `retrieve_survey_response_data` saves data to disk and in two JSON files and returns the paths to these. The first file contains the survey defintion, the second contains any recorded responses to this survey. Both files are returned as you may wish/need to use the survey definition to understand and process the content of the response data file.

### Helper Functions

The `pytrics/pytrics.py` module also contains two helper functions which were particularly useful when implementing the various functionality contained in this repository. These are `copy` and `describe`. As you may expect these allow you to copy an existing survey to a new name within your Qualtrics account and also to describe an existing survey to file on your local disk so you can review the blocks, questions and flow of any survey within your Qualtrics account.

## Improving this Code

Feel free to fork or clone this repository and iterate on the functionality provided to suit your purposes. This code is not actively maintained but it is provided under [the MIT licence](https://opensource.org/licenses/MIT) and therefore free to copy, use and amend etc. Please refer to the `LICENSE` file contained in this repository for full terms of use.
