# Pytrics

Python based Qualtrics survey integration.

This repository contains code to work with the Qualtrics API and to create surveys from template definitions and download responses to these for anaylsis and or processing.

## Getting started

### Setup

- run `python3 -m venv env` to create a virtual environement named env
- run `source env/bin/activate` to activate the virtualenv
- run `pip3 install -r dev-requirements.txt` to install required packages into your virtual environments

## Running the tests

Tests are written using unittest and can be executed via [nose](https://nose.readthedocs.io/en/latest/index.html). Some example commands are below, refer to [the docs](https://nose.readthedocs.io/en/latest/usage.html) for more options and information.

- Run all tests;

```bash
nosetests -w code
```

- Run all tests, collect coverage of the contents of the code dir, produce html coverage report and enforce minimum percentage, with colourful output;

```bash
nosetests -w code --with-coverage --cover-erase --cover-package=code/. --cover-html --cover-min-percentage=80 -v --rednose
```

## Linting the code

```bash
PYTHONPATH=$PYTHONPATH:$(pwd) pylint -f parseable code/*
```

## Working with surveys

Pending

### Qualtrics

You will need a Qualtrics account before you cna use this code, so [signup for one here](qualtrics-signup-link).

Once you have an account you will need to generate an API Key, [follow these instructions](generate-api-key-instructions-link).

Copy your API authorisation token and set an environment variable named `QUALTRICS_API_AUTH_TOKEN` to the token value;

```bash
export QUALTRICS_API_AUTH_TOKEN=<your_token_value>
```

## Useful Tidbits

Are cached files messing with your head, can you not see your latest changes when you run code/tests? You can remove all the cached files with this command;

```bash
find . -name "*.pyc" -exec rm -f {} \;
```
