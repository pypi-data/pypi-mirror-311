"""
Type annotations for codeconnections service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codeconnections.client import CodeConnectionsClient

    session = Session()
    client: CodeConnectionsClient = session.client("codeconnections")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateConnectionInputRequestTypeDef,
    CreateConnectionOutputTypeDef,
    CreateHostInputRequestTypeDef,
    CreateHostOutputTypeDef,
    CreateRepositoryLinkInputRequestTypeDef,
    CreateRepositoryLinkOutputTypeDef,
    CreateSyncConfigurationInputRequestTypeDef,
    CreateSyncConfigurationOutputTypeDef,
    DeleteConnectionInputRequestTypeDef,
    DeleteHostInputRequestTypeDef,
    DeleteRepositoryLinkInputRequestTypeDef,
    DeleteSyncConfigurationInputRequestTypeDef,
    GetConnectionInputRequestTypeDef,
    GetConnectionOutputTypeDef,
    GetHostInputRequestTypeDef,
    GetHostOutputTypeDef,
    GetRepositoryLinkInputRequestTypeDef,
    GetRepositoryLinkOutputTypeDef,
    GetRepositorySyncStatusInputRequestTypeDef,
    GetRepositorySyncStatusOutputTypeDef,
    GetResourceSyncStatusInputRequestTypeDef,
    GetResourceSyncStatusOutputTypeDef,
    GetSyncBlockerSummaryInputRequestTypeDef,
    GetSyncBlockerSummaryOutputTypeDef,
    GetSyncConfigurationInputRequestTypeDef,
    GetSyncConfigurationOutputTypeDef,
    ListConnectionsInputRequestTypeDef,
    ListConnectionsOutputTypeDef,
    ListHostsInputRequestTypeDef,
    ListHostsOutputTypeDef,
    ListRepositoryLinksInputRequestTypeDef,
    ListRepositoryLinksOutputTypeDef,
    ListRepositorySyncDefinitionsInputRequestTypeDef,
    ListRepositorySyncDefinitionsOutputTypeDef,
    ListSyncConfigurationsInputRequestTypeDef,
    ListSyncConfigurationsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateHostInputRequestTypeDef,
    UpdateRepositoryLinkInputRequestTypeDef,
    UpdateRepositoryLinkOutputTypeDef,
    UpdateSyncBlockerInputRequestTypeDef,
    UpdateSyncBlockerOutputTypeDef,
    UpdateSyncConfigurationInputRequestTypeDef,
    UpdateSyncConfigurationOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("CodeConnectionsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConditionalCheckFailedException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    RetryLatestCommitFailedException: Type[BotocoreClientError]
    SyncBlockerDoesNotExistException: Type[BotocoreClientError]
    SyncConfigurationStillExistsException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]
    UnsupportedProviderTypeException: Type[BotocoreClientError]
    UpdateOutOfSyncException: Type[BotocoreClientError]


class CodeConnectionsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections.html#CodeConnections.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeConnectionsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections.html#CodeConnections.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#close)
        """

    def create_connection(
        self, **kwargs: Unpack[CreateConnectionInputRequestTypeDef]
    ) -> CreateConnectionOutputTypeDef:
        """
        Creates a connection that can then be given to other Amazon Web Services
        services like CodePipeline so that it can access third-party code repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/create_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#create_connection)
        """

    def create_host(
        self, **kwargs: Unpack[CreateHostInputRequestTypeDef]
    ) -> CreateHostOutputTypeDef:
        """
        Creates a resource that represents the infrastructure where a third-party
        provider is installed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/create_host.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#create_host)
        """

    def create_repository_link(
        self, **kwargs: Unpack[CreateRepositoryLinkInputRequestTypeDef]
    ) -> CreateRepositoryLinkOutputTypeDef:
        """
        Creates a link to a specified external Git repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/create_repository_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#create_repository_link)
        """

    def create_sync_configuration(
        self, **kwargs: Unpack[CreateSyncConfigurationInputRequestTypeDef]
    ) -> CreateSyncConfigurationOutputTypeDef:
        """
        Creates a sync configuration which allows Amazon Web Services to sync content
        from a Git repository to update a specified Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/create_sync_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#create_sync_configuration)
        """

    def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The connection to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/delete_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#delete_connection)
        """

    def delete_host(self, **kwargs: Unpack[DeleteHostInputRequestTypeDef]) -> Dict[str, Any]:
        """
        The host to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/delete_host.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#delete_host)
        """

    def delete_repository_link(
        self, **kwargs: Unpack[DeleteRepositoryLinkInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the association between your connection and a specified external Git
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/delete_repository_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#delete_repository_link)
        """

    def delete_sync_configuration(
        self, **kwargs: Unpack[DeleteSyncConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the sync configuration for a specified repository and connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/delete_sync_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#delete_sync_configuration)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#generate_presigned_url)
        """

    def get_connection(
        self, **kwargs: Unpack[GetConnectionInputRequestTypeDef]
    ) -> GetConnectionOutputTypeDef:
        """
        Returns the connection ARN and details such as status, owner, and provider type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/get_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#get_connection)
        """

    def get_host(self, **kwargs: Unpack[GetHostInputRequestTypeDef]) -> GetHostOutputTypeDef:
        """
        Returns the host ARN and details such as status, provider type, endpoint, and,
        if applicable, the VPC configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/get_host.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#get_host)
        """

    def get_repository_link(
        self, **kwargs: Unpack[GetRepositoryLinkInputRequestTypeDef]
    ) -> GetRepositoryLinkOutputTypeDef:
        """
        Returns details about a repository link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/get_repository_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#get_repository_link)
        """

    def get_repository_sync_status(
        self, **kwargs: Unpack[GetRepositorySyncStatusInputRequestTypeDef]
    ) -> GetRepositorySyncStatusOutputTypeDef:
        """
        Returns details about the sync status for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/get_repository_sync_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#get_repository_sync_status)
        """

    def get_resource_sync_status(
        self, **kwargs: Unpack[GetResourceSyncStatusInputRequestTypeDef]
    ) -> GetResourceSyncStatusOutputTypeDef:
        """
        Returns the status of the sync with the Git repository for a specific Amazon
        Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/get_resource_sync_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#get_resource_sync_status)
        """

    def get_sync_blocker_summary(
        self, **kwargs: Unpack[GetSyncBlockerSummaryInputRequestTypeDef]
    ) -> GetSyncBlockerSummaryOutputTypeDef:
        """
        Returns a list of the most recent sync blockers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/get_sync_blocker_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#get_sync_blocker_summary)
        """

    def get_sync_configuration(
        self, **kwargs: Unpack[GetSyncConfigurationInputRequestTypeDef]
    ) -> GetSyncConfigurationOutputTypeDef:
        """
        Returns details about a sync configuration, including the sync type and
        resource name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/get_sync_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#get_sync_configuration)
        """

    def list_connections(
        self, **kwargs: Unpack[ListConnectionsInputRequestTypeDef]
    ) -> ListConnectionsOutputTypeDef:
        """
        Lists the connections associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/list_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#list_connections)
        """

    def list_hosts(self, **kwargs: Unpack[ListHostsInputRequestTypeDef]) -> ListHostsOutputTypeDef:
        """
        Lists the hosts associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/list_hosts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#list_hosts)
        """

    def list_repository_links(
        self, **kwargs: Unpack[ListRepositoryLinksInputRequestTypeDef]
    ) -> ListRepositoryLinksOutputTypeDef:
        """
        Lists the repository links created for connections in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/list_repository_links.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#list_repository_links)
        """

    def list_repository_sync_definitions(
        self, **kwargs: Unpack[ListRepositorySyncDefinitionsInputRequestTypeDef]
    ) -> ListRepositorySyncDefinitionsOutputTypeDef:
        """
        Lists the repository sync definitions for repository links in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/list_repository_sync_definitions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#list_repository_sync_definitions)
        """

    def list_sync_configurations(
        self, **kwargs: Unpack[ListSyncConfigurationsInputRequestTypeDef]
    ) -> ListSyncConfigurationsOutputTypeDef:
        """
        Returns a list of sync configurations for a specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/list_sync_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#list_sync_configurations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Gets the set of key-value pairs (metadata) that are used to manage the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#untag_resource)
        """

    def update_host(self, **kwargs: Unpack[UpdateHostInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a specified host with the provided configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/update_host.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#update_host)
        """

    def update_repository_link(
        self, **kwargs: Unpack[UpdateRepositoryLinkInputRequestTypeDef]
    ) -> UpdateRepositoryLinkOutputTypeDef:
        """
        Updates the association between your connection and a specified external Git
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/update_repository_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#update_repository_link)
        """

    def update_sync_blocker(
        self, **kwargs: Unpack[UpdateSyncBlockerInputRequestTypeDef]
    ) -> UpdateSyncBlockerOutputTypeDef:
        """
        Allows you to update the status of a sync blocker, resolving the blocker and
        allowing syncing to continue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/update_sync_blocker.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#update_sync_blocker)
        """

    def update_sync_configuration(
        self, **kwargs: Unpack[UpdateSyncConfigurationInputRequestTypeDef]
    ) -> UpdateSyncConfigurationOutputTypeDef:
        """
        Updates the sync configuration for your connection and a specified external Git
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeconnections/client/update_sync_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeconnections/client/#update_sync_configuration)
        """
