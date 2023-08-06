"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""


class StellaNowCLIException(Exception):
    """Exception raised for errors in the Stella Now CLI."""

    def __init__(self, message, details):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.details}'


class StellaNowCLILanguageNotSupportedException(StellaNowCLIException):
    """Exception raised for unsupported languages by the CLI."""

    def __init__(self, language):
        super().__init__(f"Code generator for {language} not found.", {})
