"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import json
import requests

from dataclasses import dataclass
from sys import maxsize
from typing import Generator, List

from ..logger import logger
from ..config import Config


@dataclass
class StellaEntity:
    id: str
    name: str


@dataclass
class StellaField:
    id: str
    name: str
    valueType: str


@dataclass
class StellaEvent:
    id: str
    name: str
    isActive: bool
    createdAt: str
    updatedAt: str


@dataclass
class StellaEventDetailed(StellaEvent):
    description: str
    fields: List[StellaField]
    entities: List[StellaEntity]


class StellaAPIError(Exception):
    """Exception raised for errors in the Stella API."""

    def __init__(self, message, errors):
        self.message = message
        self.errors = errors
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.errors}'


class StellaAPI:
    def __init__(self, env_config: Config, access_key: str, access_token: str, organization_id: str, project_id: str):
        self.env_config = env_config

        self.access_key = access_key
        self.access_token = access_token
        self.organization_id = organization_id
        self.project_id = project_id
        self.auth_token = None
        self.refresh_token = None

        self.authenticate()

    def _handle_response(self, response):
        try:
            details = response.json().get("details")
        except json.JSONDecodeError:
            details = None

        match response.status_code:
            case 401:
                # Normalize to always have a list of errors
                errors = details.get("errors") if isinstance(details, dict) else details

                for error in errors:
                    match error.get("errorCode"):
                        case "inactiveAuthToken":
                            self.auth_refresh()
                            return
                        case "wrongUsernameOrPassword":
                            raise StellaAPIError('Unauthorized: Provided username or password is invalid.', details)
                        case _:
                            raise StellaAPIError('Unauthorized', details)
            case 403:
                raise StellaAPIError(
                    "Forbidden: Access to the API is restricted only to whitelisted connections.",
                    details
                )
            case 404:
                raise StellaAPIError('Not Found', details)
            case _:
                response.raise_for_status()

    def authenticate(self):
        logger.info("Authenticating to the API ... ")

        if self.refresh_token is not None:
            self.auth_refresh()
        else:
            body = {
                "realm_id": self.organization_id,
                "username": self.access_key,
                "email": self.access_key,
                "password": self.access_token,
                "client_id": "backoffice"
            }

            self.auth_token = None
            self.refresh_token = None

            response = requests.post(self.env_config.auth_url, json=body)
            self._handle_response(response)

            self.auth_token = response.json().get("details").get("access_token")
            self.refresh_token = response.json().get("details").get("refresh_token")

        logger.info("Authentication Successful")

    def auth_refresh(self):
        if self.refresh_token is None:
            self.authenticate()
        else:
            logger.info("API Token Refreshing ...")

            body = {"refresh_token": self.refresh_token}

            self.auth_token = None
            self.refresh_token = None

            response = requests.post(self.env_config.auth_refresh_url, json=body)
            self._handle_response(response)

            self.auth_token = response.json().get("details").get("access_token")
            self.refresh_token = response.json().get("details").get("refresh_token")

            logger.info("API Token Refresh Successful")

    def get_events(self) -> Generator[StellaEvent, None, None]:
        page_number = 1
        number_of_pages = maxsize
        while page_number < number_of_pages:
            url = self.env_config.events_url.format(projectId=self.project_id) + f"?pageNumber={page_number}&pageSize=1000"
            headers = {"Authorization": f"Bearer {self.auth_token}"}

            response = requests.get(url, headers=headers)
            self._handle_response(response)

            events = response.json().get("details", {}).get("results", [])
            number_of_pages = response.json().get("details", {}).get("numberOfPages", 0)
            if not events:
                break

            for event in events:
                yield StellaEvent(
                    id=event.get('id'),
                    name=event.get('name'),
                    isActive=event.get('isActive'),
                    createdAt=event.get('createdAt'),
                    updatedAt=event.get('updatedAt')
                )

            page_number += 1

    def get_event_details(self, event_id: str) -> StellaEventDetailed:
        url = self.env_config.event_url.format(projectId=self.project_id, eventId=event_id)
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        response = requests.get(url, headers=headers)
        self._handle_response(response)

        details = response.json().get("details", {})

        # create StellaEntity objects from the 'entities' list
        entities = [StellaEntity(**entity) for entity in details.get('entities', [])]

        # create StellaField objects from the 'fields' list
        fields = [StellaField(**field) for field in details.get('fields', [])]

        # create and return StellaEventDetailed object
        return StellaEventDetailed(
            id=details.get('id'),
            name=details.get('name'),
            description=details.get('description'),
            isActive=details.get('isActive'),
            createdAt=details.get('createdAt'),
            updatedAt=details.get('updatedAt'),
            fields=fields,
            entities=entities,
        )
