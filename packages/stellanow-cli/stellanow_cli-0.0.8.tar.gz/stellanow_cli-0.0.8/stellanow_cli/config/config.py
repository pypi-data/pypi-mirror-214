"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

from dataclasses import dataclass


@dataclass
class Config:
    base_url: str = ""

    @property
    def auth_url(self):
        return f"{self.base_url}/ipm/login"

    @property
    def auth_refresh_url(self):
        return f"{self.base_url}/ipm/refresh"

    @property
    def events_url(self):
        return f"{self.base_url}/workflow-management/projects/{{projectId}}/events"

    @property
    def event_url(self):
        return f"{self.base_url}/workflow-management/projects/{{projectId}}/events/{{eventId}}"
