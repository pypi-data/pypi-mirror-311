"""
Type annotations for transfer service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_transfer.client import TransferClient
    from mypy_boto3_transfer.paginator import (
        ListAccessesPaginator,
        ListAgreementsPaginator,
        ListCertificatesPaginator,
        ListConnectorsPaginator,
        ListExecutionsPaginator,
        ListFileTransferResultsPaginator,
        ListProfilesPaginator,
        ListSecurityPoliciesPaginator,
        ListServersPaginator,
        ListTagsForResourcePaginator,
        ListUsersPaginator,
        ListWorkflowsPaginator,
    )

    session = Session()
    client: TransferClient = session.client("transfer")

    list_accesses_paginator: ListAccessesPaginator = client.get_paginator("list_accesses")
    list_agreements_paginator: ListAgreementsPaginator = client.get_paginator("list_agreements")
    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_file_transfer_results_paginator: ListFileTransferResultsPaginator = client.get_paginator("list_file_transfer_results")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    list_security_policies_paginator: ListSecurityPoliciesPaginator = client.get_paginator("list_security_policies")
    list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccessesRequestListAccessesPaginateTypeDef,
    ListAccessesResponseTypeDef,
    ListAgreementsRequestListAgreementsPaginateTypeDef,
    ListAgreementsResponseTypeDef,
    ListCertificatesRequestListCertificatesPaginateTypeDef,
    ListCertificatesResponseTypeDef,
    ListConnectorsRequestListConnectorsPaginateTypeDef,
    ListConnectorsResponseTypeDef,
    ListExecutionsRequestListExecutionsPaginateTypeDef,
    ListExecutionsResponseTypeDef,
    ListFileTransferResultsRequestListFileTransferResultsPaginateTypeDef,
    ListFileTransferResultsResponseTypeDef,
    ListProfilesRequestListProfilesPaginateTypeDef,
    ListProfilesResponseTypeDef,
    ListSecurityPoliciesRequestListSecurityPoliciesPaginateTypeDef,
    ListSecurityPoliciesResponseTypeDef,
    ListServersRequestListServersPaginateTypeDef,
    ListServersResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
    ListWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccessesPaginator",
    "ListAgreementsPaginator",
    "ListCertificatesPaginator",
    "ListConnectorsPaginator",
    "ListExecutionsPaginator",
    "ListFileTransferResultsPaginator",
    "ListProfilesPaginator",
    "ListSecurityPoliciesPaginator",
    "ListServersPaginator",
    "ListTagsForResourcePaginator",
    "ListUsersPaginator",
    "ListWorkflowsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccessesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListAccesses.html#Transfer.Paginator.ListAccesses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listaccessespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccessesRequestListAccessesPaginateTypeDef]
    ) -> _PageIterator[ListAccessesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListAccesses.html#Transfer.Paginator.ListAccesses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listaccessespaginator)
        """

class ListAgreementsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListAgreements.html#Transfer.Paginator.ListAgreements)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listagreementspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAgreementsRequestListAgreementsPaginateTypeDef]
    ) -> _PageIterator[ListAgreementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListAgreements.html#Transfer.Paginator.ListAgreements.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listagreementspaginator)
        """

class ListCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListCertificates.html#Transfer.Paginator.ListCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCertificatesRequestListCertificatesPaginateTypeDef]
    ) -> _PageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListCertificates.html#Transfer.Paginator.ListCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listcertificatespaginator)
        """

class ListConnectorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListConnectors.html#Transfer.Paginator.ListConnectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listconnectorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConnectorsRequestListConnectorsPaginateTypeDef]
    ) -> _PageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListConnectors.html#Transfer.Paginator.ListConnectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listconnectorspaginator)
        """

class ListExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListExecutions.html#Transfer.Paginator.ListExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListExecutionsRequestListExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListExecutions.html#Transfer.Paginator.ListExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listexecutionspaginator)
        """

class ListFileTransferResultsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListFileTransferResults.html#Transfer.Paginator.ListFileTransferResults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listfiletransferresultspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFileTransferResultsRequestListFileTransferResultsPaginateTypeDef]
    ) -> _PageIterator[ListFileTransferResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListFileTransferResults.html#Transfer.Paginator.ListFileTransferResults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listfiletransferresultspaginator)
        """

class ListProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListProfiles.html#Transfer.Paginator.ListProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProfilesRequestListProfilesPaginateTypeDef]
    ) -> _PageIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListProfiles.html#Transfer.Paginator.ListProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listprofilespaginator)
        """

class ListSecurityPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListSecurityPolicies.html#Transfer.Paginator.ListSecurityPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listsecuritypoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSecurityPoliciesRequestListSecurityPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListSecurityPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListSecurityPolicies.html#Transfer.Paginator.ListSecurityPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listsecuritypoliciespaginator)
        """

class ListServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListServers.html#Transfer.Paginator.ListServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listserverspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServersRequestListServersPaginateTypeDef]
    ) -> _PageIterator[ListServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListServers.html#Transfer.Paginator.ListServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listserverspaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListTagsForResource.html#Transfer.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListTagsForResource.html#Transfer.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listtagsforresourcepaginator)
        """

class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListUsers.html#Transfer.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListUsers.html#Transfer.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listuserspaginator)
        """

class ListWorkflowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListWorkflows.html#Transfer.Paginator.ListWorkflows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listworkflowspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> _PageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListWorkflows.html#Transfer.Paginator.ListWorkflows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/paginators/#listworkflowspaginator)
        """
