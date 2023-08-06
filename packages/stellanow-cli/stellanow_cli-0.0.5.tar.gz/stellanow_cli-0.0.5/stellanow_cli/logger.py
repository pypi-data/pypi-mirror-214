"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import logging

# Setting up the logger
logger = logging.getLogger('stellanow_cli')


def setup_logger(verbose: bool):
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # Handler level is set to DEBUG

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)
