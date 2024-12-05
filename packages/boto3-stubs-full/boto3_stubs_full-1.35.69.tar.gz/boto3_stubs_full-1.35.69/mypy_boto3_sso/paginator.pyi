"""
Type annotations for sso service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sso.client import SSOClient
    from mypy_boto3_sso.paginator import (
        ListAccountRolesPaginator,
        ListAccountsPaginator,
    )

    session = Session()
    client: SSOClient = session.client("sso")

    list_account_roles_paginator: ListAccountRolesPaginator = client.get_paginator("list_account_roles")
    list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccountRolesRequestListAccountRolesPaginateTypeDef,
    ListAccountRolesResponseTypeDef,
    ListAccountsRequestListAccountsPaginateTypeDef,
    ListAccountsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAccountRolesPaginator", "ListAccountsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccountRolesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso/paginator/ListAccountRoles.html#SSO.Paginator.ListAccountRoles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/#listaccountrolespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountRolesRequestListAccountRolesPaginateTypeDef]
    ) -> _PageIterator[ListAccountRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso/paginator/ListAccountRoles.html#SSO.Paginator.ListAccountRoles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/#listaccountrolespaginator)
        """

class ListAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso/paginator/ListAccounts.html#SSO.Paginator.ListAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/#listaccountspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountsRequestListAccountsPaginateTypeDef]
    ) -> _PageIterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso/paginator/ListAccounts.html#SSO.Paginator.ListAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/#listaccountspaginator)
        """
