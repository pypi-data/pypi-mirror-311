"""
Main interface for b2bi service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_b2bi import (
        B2BIClient,
        Client,
        ListCapabilitiesPaginator,
        ListPartnershipsPaginator,
        ListProfilesPaginator,
        ListTransformersPaginator,
    )

    session = Session()
    client: B2BIClient = session.client("b2bi")

    list_capabilities_paginator: ListCapabilitiesPaginator = client.get_paginator("list_capabilities")
    list_partnerships_paginator: ListPartnershipsPaginator = client.get_paginator("list_partnerships")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    list_transformers_paginator: ListTransformersPaginator = client.get_paginator("list_transformers")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import B2BIClient
from .paginator import (
    ListCapabilitiesPaginator,
    ListPartnershipsPaginator,
    ListProfilesPaginator,
    ListTransformersPaginator,
)

Client = B2BIClient


__all__ = (
    "B2BIClient",
    "Client",
    "ListCapabilitiesPaginator",
    "ListPartnershipsPaginator",
    "ListProfilesPaginator",
    "ListTransformersPaginator",
)
