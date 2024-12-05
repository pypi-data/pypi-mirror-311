"""
Type annotations for cloud9 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloud9.client import Cloud9Client

    session = Session()
    client: Cloud9Client = session.client("cloud9")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import DescribeEnvironmentMembershipsPaginator, ListEnvironmentsPaginator
from .type_defs import (
    CreateEnvironmentEC2RequestRequestTypeDef,
    CreateEnvironmentEC2ResultTypeDef,
    CreateEnvironmentMembershipRequestRequestTypeDef,
    CreateEnvironmentMembershipResultTypeDef,
    DeleteEnvironmentMembershipRequestRequestTypeDef,
    DeleteEnvironmentRequestRequestTypeDef,
    DescribeEnvironmentMembershipsRequestRequestTypeDef,
    DescribeEnvironmentMembershipsResultTypeDef,
    DescribeEnvironmentsRequestRequestTypeDef,
    DescribeEnvironmentsResultTypeDef,
    DescribeEnvironmentStatusRequestRequestTypeDef,
    DescribeEnvironmentStatusResultTypeDef,
    ListEnvironmentsRequestRequestTypeDef,
    ListEnvironmentsResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateEnvironmentMembershipRequestRequestTypeDef,
    UpdateEnvironmentMembershipResultTypeDef,
    UpdateEnvironmentRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("Cloud9Client",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentAccessException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class Cloud9Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Cloud9Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#close)
        """

    def create_environment_ec2(
        self, **kwargs: Unpack[CreateEnvironmentEC2RequestRequestTypeDef]
    ) -> CreateEnvironmentEC2ResultTypeDef:
        """
        Creates an Cloud9 development environment, launches an Amazon Elastic Compute
        Cloud (Amazon EC2) instance, and then connects from the instance to the
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/create_environment_ec2.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#create_environment_ec2)
        """

    def create_environment_membership(
        self, **kwargs: Unpack[CreateEnvironmentMembershipRequestRequestTypeDef]
    ) -> CreateEnvironmentMembershipResultTypeDef:
        """
        Adds an environment member to an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/create_environment_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#create_environment_membership)
        """

    def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/delete_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#delete_environment)
        """

    def delete_environment_membership(
        self, **kwargs: Unpack[DeleteEnvironmentMembershipRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an environment member from a development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/delete_environment_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#delete_environment_membership)
        """

    def describe_environment_memberships(
        self, **kwargs: Unpack[DescribeEnvironmentMembershipsRequestRequestTypeDef]
    ) -> DescribeEnvironmentMembershipsResultTypeDef:
        """
        Gets information about environment members for an Cloud9 development
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/describe_environment_memberships.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#describe_environment_memberships)
        """

    def describe_environment_status(
        self, **kwargs: Unpack[DescribeEnvironmentStatusRequestRequestTypeDef]
    ) -> DescribeEnvironmentStatusResultTypeDef:
        """
        Gets status information for an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/describe_environment_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#describe_environment_status)
        """

    def describe_environments(
        self, **kwargs: Unpack[DescribeEnvironmentsRequestRequestTypeDef]
    ) -> DescribeEnvironmentsResultTypeDef:
        """
        Gets information about Cloud9 development environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/describe_environments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#describe_environments)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#generate_presigned_url)
        """

    def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsRequestRequestTypeDef]
    ) -> ListEnvironmentsResultTypeDef:
        """
        Gets a list of Cloud9 development environment identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/list_environments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#list_environments)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of the tags associated with an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#untag_resource)
        """

    def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the settings of an existing Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/update_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#update_environment)
        """

    def update_environment_membership(
        self, **kwargs: Unpack[UpdateEnvironmentMembershipRequestRequestTypeDef]
    ) -> UpdateEnvironmentMembershipResultTypeDef:
        """
        Changes the settings of an existing environment member for an Cloud9
        development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/update_environment_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#update_environment_membership)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_environment_memberships"]
    ) -> DescribeEnvironmentMembershipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#get_paginator)
        """
