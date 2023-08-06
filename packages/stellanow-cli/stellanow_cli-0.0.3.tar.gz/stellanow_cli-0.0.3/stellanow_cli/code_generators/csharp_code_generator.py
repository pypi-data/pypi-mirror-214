"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import difflib
import json
import re

from dataclasses import asdict
from datetime import datetime
from typing import Iterator

from .code_generator import CodeGenerator
from ..api import StellaEventDetailed
from ..utils import snake_to_camel, snake_to_lower_camel, remove_comments


class NamespaceNotFoundError(Exception):
    """Exception raised when a namespace is not found in a file."""

    def __init__(self):
        self.message = f"No Namespace Found"
        super().__init__(self.message)


class CsharpCodeGenerator(CodeGenerator):
    @staticmethod
    def generate_class(event: StellaEventDetailed, **kwargs) -> str:
        template = CsharpCodeGenerator.load_template('csharp')

        namespace = kwargs.get('namespace', 'StellaNowSDK.Messages')

        constructor_arguments = ', '.join([
            ', '.join([f'string {snake_to_lower_camel(entity.name)}Id' for entity in event.entities]),
            ', '.join([f'string {snake_to_lower_camel(field.name)}' for field in event.fields])
        ])
        entities_list = ', '.join([f'new EntityType("{entity.name}", {entity.name}Id)' for entity in event.entities])

        event_json = json.dumps(asdict(event), indent=4)

        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        rendered = template.render(
            className=snake_to_camel(event.name),
            eventName=event.name,
            constructorArguments=constructor_arguments,
            entitiesList=entities_list,
            fields=[{'name': field.name, 'camel_name': snake_to_lower_camel(field.name)} for field in event.fields],
            namespace=namespace,
            eventJson=event_json,
            eventId=event.id,
            timestamp=timestamp
        )

        return rendered

    @staticmethod
    def get_file_name_for_event_name(event_name: str) -> str:
        return f"{snake_to_camel(event_name)}Message.cs"

    @classmethod
    def get_diff(cls, event: StellaEventDetailed, existing_code: str) -> Iterator[str]:
        # Extract namespace from the existing code
        namespace_search = re.search(r'namespace (.*);', existing_code)
        if namespace_search is None:
            raise NamespaceNotFoundError()

        namespace = namespace_search.group(1)

        new_code = cls.generate_class(event, **{'namespace': namespace})

        existing_code_no_comments = remove_comments(existing_code)
        new_code_no_comments = remove_comments(new_code)

        # Use difflib to compare the new and existing code
        diff = difflib.unified_diff(existing_code_no_comments.splitlines(keepends=True),
                                    new_code_no_comments.splitlines(keepends=True))

        return (line for line in diff if line.startswith('- ') or line.startswith('+ ') and not (
                    line.startswith('---') or line.startswith('+++')))
