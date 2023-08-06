"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import click

from prettytable import PrettyTable

from .command_config import common_option, load_config


@click.command(name='events')
@common_option
@load_config
@click.pass_context
def events(ctx, stella_api, organization_id, project_id, **kwargs):
    """Fetches the latest event specifications from the API and output a list of the events into the terminal prompt."""

    print(f"\n\nOrganizationId: {organization_id}\nProjectId: {project_id}\n\n")

    _events = stella_api.get_events()

    table = PrettyTable(['EventID', 'Event Name', "Is Active", "Created At", "Updated At"])

    # Populate the table with data from your SkippedFile instances
    for event in _events:
        table.add_row([event.id, event.name, event.isActive, event.createdAt, event.updatedAt])

    print(table)

    for event in _events:
        print(f'ID: {event.id}, Name: {event.name}')


events_cmd = events
