"""
Main interface for ivs service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ivs import (
        Client,
        IVSClient,
        ListChannelsPaginator,
        ListPlaybackKeyPairsPaginator,
        ListRecordingConfigurationsPaginator,
        ListStreamKeysPaginator,
        ListStreamsPaginator,
    )

    session = Session()
    client: IVSClient = session.client("ivs")

    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_playback_key_pairs_paginator: ListPlaybackKeyPairsPaginator = client.get_paginator("list_playback_key_pairs")
    list_recording_configurations_paginator: ListRecordingConfigurationsPaginator = client.get_paginator("list_recording_configurations")
    list_stream_keys_paginator: ListStreamKeysPaginator = client.get_paginator("list_stream_keys")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IVSClient
from .paginator import (
    ListChannelsPaginator,
    ListPlaybackKeyPairsPaginator,
    ListRecordingConfigurationsPaginator,
    ListStreamKeysPaginator,
    ListStreamsPaginator,
)

Client = IVSClient


__all__ = (
    "Client",
    "IVSClient",
    "ListChannelsPaginator",
    "ListPlaybackKeyPairsPaginator",
    "ListRecordingConfigurationsPaginator",
    "ListStreamKeysPaginator",
    "ListStreamsPaginator",
)
