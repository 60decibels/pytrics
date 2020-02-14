import os

from pytrics.common.constants import (
    ENV_VAR_QUALTRICS_API_BASE_URL,
    ENV_VAR_QUALTRICS_API_AUTH_TOKEN,
)
from pytrics.common.exceptions import QualtricsAPIException


def get_details_for_client():
    base_url = os.environ.get(ENV_VAR_QUALTRICS_API_BASE_URL, '')
    if not base_url:
        raise QualtricsAPIException('Unable to find base api url in ENV')

    token = os.environ.get(ENV_VAR_QUALTRICS_API_AUTH_TOKEN, '')

    if not token:
        raise QualtricsAPIException('Unable to find api auth token in ENV')

    return base_url, token
