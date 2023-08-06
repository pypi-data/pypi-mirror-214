"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import click
import os

from ..command_config import common_option, load_config
from ..code_generators import CsharpCodeGenerator
from ..logger import logger


@click.command(name='generate')
@common_option
@load_config
@click.option('--namespace', '-n', default='', help='The namespace for the generated classes.')
@click.option('--destination', '-d', default='.', help='The directory to save the generated classes.')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing files.')
@click.option('--events', '-e', multiple=True, help='List of specific events to generate.')
@click.option('--language', '-l', type=click.Choice(['csharp'], case_sensitive=False), default='csharp',
              help='The programming language for the generated classes.')
@click.pass_context
def generate(ctx, stella_api, destination, force, events, language, **kwargs):
    """Fetches the latest event specifications from the API and generates corresponding class code in the desired
    programming language."""
    print('Generating...')

    generator_class_name = f"{language.capitalize()}CodeGenerator"
    generator_class = globals().get(generator_class_name)

    if not generator_class:
        raise Exception(f"Code generator for {language} not found.")

    events_not_found = set(events) if events else set()
    events_not_overwritten = set()

    _events = stella_api.get_events()
    for event in _events:
        if events and event.name not in events:
            continue

        events_not_found.discard(event.name)  # remove event from 'not found' list
        print(f'Generating class for event: {event.name}')

        generator = generator_class()

        # Save the code to a file
        file_path = os.path.join(destination, generator.get_file_name_for_event_name(event.name))
        if not force and os.path.exists(file_path):
            logger.warning(f"File {file_path} already exists. Use --force to overwrite.")
            events_not_overwritten.add(event.name)  # add event to 'not overwritten' list
            continue

        code = generator.generate_class(stella_api.get_event_details(event.id), **kwargs)

        with open(file_path, "w") as file:
            file.write(code)

    # Output summary of events not generated
    if events_not_found:
        logger.warning(f"The following events were not found and no classes were generated for them:\n- " +
                       "\n- ".join(events_not_found))
    if events_not_overwritten:
        logger.warning(f"The following events were not generated because they did not overwrite existing files:\n- " +
                       "\n- ".join(events_not_overwritten))


generate_cmd = generate
