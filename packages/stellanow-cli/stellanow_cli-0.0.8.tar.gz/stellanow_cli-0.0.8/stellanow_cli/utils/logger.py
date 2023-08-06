"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import logging


def setup_logger(verbose: bool):
    root_logger = logging.getLogger()

    if verbose:
        root_logger.setLevel(logging.INFO)
    else:
        root_logger.setLevel(logging.WARNING)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # Handler level is set to DEBUG

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    root_logger.addHandler(ch)
