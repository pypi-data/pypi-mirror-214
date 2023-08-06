"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

from typing import List

from .StellaNowCLIException import StellaNowCLIException


class StellaAPIError(StellaNowCLIException):
    """Exception raised for errors in the Stella API."""


class StellaAPIForbiddenError(StellaAPIError):
    """Exception raised for when trying to access the Stella API from blacklisted address."""

    def __init__(self):
        super().__init__("Forbidden", {})


class StellaAPINotFoundError(StellaAPIError):
    """Exception raised for when a requested object does not exist in the Stella API."""

    def __init__(self, details):
        super().__init__("Not Found", details)


class StellaAPIUnauthorisedError(StellaAPIError):
    """Exception raised for when request is not authorised to be performed by requesting entity in the Stella API."""

    def __init__(self, details):
        super().__init__("Unauthorised", details)


class StellaAPIWrongCredentialsError(StellaAPIError):
    """Exception raised for wrong credentials during auth in the Stella API."""

    def __init__(self):
        super().__init__("Unauthorized: Provided username or password is invalid.", {})
