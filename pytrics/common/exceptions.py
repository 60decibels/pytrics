# pylint: disable=unnecessary-pass
"""
Contains custom exceptions used in this project
"""

class HttpException(Exception):
    '''
    Generic Http Error encompassing all sorts of failures of Http operations
    '''
    pass


class QualtricsAPIException(Exception):
    """
    Raised when an issue is found during execution of request to the Qualtrics API
    """
    pass


class QualtricsDataSerialisationException(Exception):
    """
    Raised when an issue is found during serialisation of data retrieved by the Qualtrics API
    """
    pass
