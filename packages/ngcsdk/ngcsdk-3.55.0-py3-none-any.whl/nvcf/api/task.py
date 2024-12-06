#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#
from __future__ import annotations

from collections.abc import Iterable
from itertools import chain
from typing import Optional, TYPE_CHECKING, Union

from ngcbpc.api.utils import disable_function, DotDict
from ngcbpc.constants import STAGING_ENV
from ngcbpc.util.utils import get_environ_tag

if TYPE_CHECKING:
    import ngcsdk

    import ngccli.api.apiclient

    Client = Union[ngccli.api.apiclient.APIClient, ngcsdk.APIClient]


class TaskAPI:  # noqa: D101
    def __init__(self, api_client: Client = None) -> None:
        self.connection = api_client.connection
        self.config = api_client.config
        self.client = api_client

    @staticmethod
    def _construct_task_endpoint(
        org_name: str,
        task_id: Optional[str] = None,
    ) -> str:
        parts = ["v2/orgs", org_name]

        parts.extend(["nvct", "tasks"])

        if task_id:
            parts.extend([task_id])

        return "/".join(parts)

    def _pagination_helper(self, base_url, org_name: str, operation_name: str, limit: int = 100):
        """Help query for paginated data."""
        cursor = None
        should_fetch_next_page = True
        while should_fetch_next_page:
            query = f"limit={limit}&cursor={cursor}" if cursor else ""
            url = base_url + query
            response = self.connection.make_api_request("GET", url, auth_org=org_name, operation_name=operation_name)
            if response:
                yield response["events"]
                if "cursor" in response:
                    should_fetch_next_page = True
                    cursor = response["cursor"]
                else:
                    should_fetch_next_page = False

    @disable_function(get_environ_tag() > STAGING_ENV)
    def create(self):
        """Create a task with the specification provided by input.

        Returns:
            DotDict: Function Response provided by NVCF
        """
        self.config.validate_configuration()

    @disable_function(get_environ_tag() > STAGING_ENV)
    def list(self) -> list[DotDict]:
        """List tasks available to the organization currently set.

        Returns:
            A list of task DotDicts.
        """
        self.config.validate_configuration()
        return []

    @disable_function(get_environ_tag() > STAGING_ENV)
    def info(self, task_id: str) -> DotDict:
        """Get information about a given task.

        Returns:
            dict: DotDict of task information.
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        url = self._construct_task_endpoint(org_name, task_id)
        response = self.connection.make_api_request("GET", url, auth_org=org_name, operation_name="get task")
        return DotDict(response)

    @disable_function(get_environ_tag() > STAGING_ENV)
    def delete(self):
        """Delete a task."""
        self.config.validate_configuration()

    @disable_function(get_environ_tag() > STAGING_ENV)
    def cancel(self):
        """Cancel a task."""
        self.config.validate_configuration()

    @disable_function(get_environ_tag() > STAGING_ENV)
    def events(self, task_id: str) -> Iterable[DotDict]:
        """Get a list of the task's events.

        Returns:
            dict: DotDict of task information.
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        return self._list_events(task_id, org_name=org_name)

    def _list_events(self, task_id: str, org_name: str) -> iter:
        """Aggregate lists of events for a task."""
        url = self._construct_task_endpoint(org_name, task_id) + "/events"
        return chain(*self._pagination_helper(url, org_name=org_name, operation_name="list task events"))

    @disable_function(get_environ_tag() > STAGING_ENV)
    def get_results(self) -> list[DotDict]:
        """Get a list of the tasks' results."""
        self.config.validate_configuration()
