"""
Main interface for cloud9 service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloud9 import (
        Client,
        Cloud9Client,
        DescribeEnvironmentMembershipsPaginator,
        ListEnvironmentsPaginator,
    )

    session = Session()
    client: Cloud9Client = session.client("cloud9")

    describe_environment_memberships_paginator: DescribeEnvironmentMembershipsPaginator = client.get_paginator("describe_environment_memberships")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import Cloud9Client
from .paginator import DescribeEnvironmentMembershipsPaginator, ListEnvironmentsPaginator

Client = Cloud9Client

__all__ = (
    "Client",
    "Cloud9Client",
    "DescribeEnvironmentMembershipsPaginator",
    "ListEnvironmentsPaginator",
)
