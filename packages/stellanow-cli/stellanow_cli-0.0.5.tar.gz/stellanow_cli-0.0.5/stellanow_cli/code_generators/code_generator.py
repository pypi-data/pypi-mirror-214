"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

from ..api import StellaEventDetailed


class CodeGenerator:
    @staticmethod
    def load_template(language: str) -> Template:
        # Get the current file path
        current_file_path = Path(__file__).parent

        # Define the relative path to the templates directory
        templates_relative_path = Path('templates')

        # Get the absolute path to the templates directory
        templates_path = current_file_path / templates_relative_path

        # Create a Jinja2 environment with the FileSystemLoader
        env = Environment(loader=FileSystemLoader(templates_path))

        # Get the template
        template = env.get_template(f'{language}.template')

        return template

    @staticmethod
    def generate_class(event: StellaEventDetailed, **kwargs) -> str:
        raise NotImplemented

    @staticmethod
    def get_file_name_for_event_name(event_name: str) -> str:
        raise NotImplemented

    @staticmethod
    def get_diff(event: StellaEventDetailed, destination: str) -> str:
        raise NotImplemented
