"""Module Description: This module defines custom exceptions for use within the application.

These exceptions provide more specific error handling and messaging for various failure scenarios,
improving the robustness and clarity of the code.
"""


class InvalidInputException(Exception):
    """Invalid Input Exception ."""

    pass


class SessionExpiredException(Exception):
    """Session Expire Exception."""

    pass
