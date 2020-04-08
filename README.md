# Pytrics

Python based Qualtrics survey integration.

This repository contains code to work with the Qualtrics API and to create surveys from the provided template definitions and download responses to these surveys for analysis and processing.

## Usage

Pytrics requires Python 3. Once you have that installed or activated you can install and use Pytrics as described below.

```bash
pip install pytrics

export QUALTRICS_API_AUTH_TOKEN=your_api_token

export QUALTRICS_API_BASE_URL=your_base_api_url

export ABSOLUTE_PATH_TO_DATA_DIR=/absolute/path/on/disk/to/store/output
```

```python
from pytrics.tools import Tools
tools = Tools()


tools.create_survey_from_definition('My new agriculture survey', 'et')
Creating Blocks |################################| 19/19
Creating Questions |################################| 60/60
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
Creating Blocks |################################| 19/19
Creating Questions |################################| 60/60
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
nosetests --with-coverage --cover-erase --cover-package=pytrics/. --cover-html --cover-min-percentage=80 -v --rednose
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
