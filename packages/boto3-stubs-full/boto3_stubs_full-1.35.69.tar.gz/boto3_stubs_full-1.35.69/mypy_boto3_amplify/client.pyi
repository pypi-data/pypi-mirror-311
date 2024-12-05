"""
Type annotations for amplify service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_amplify.client import AmplifyClient

    session = Session()
    client: AmplifyClient = session.client("amplify")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAppsPaginator,
    ListBranchesPaginator,
    ListDomainAssociationsPaginator,
    ListJobsPaginator,
)
from .type_defs import (
    CreateAppRequestRequestTypeDef,
    CreateAppResultTypeDef,
    CreateBackendEnvironmentRequestRequestTypeDef,
    CreateBackendEnvironmentResultTypeDef,
    CreateBranchRequestRequestTypeDef,
    CreateBranchResultTypeDef,
    CreateDeploymentRequestRequestTypeDef,
    CreateDeploymentResultTypeDef,
    CreateDomainAssociationRequestRequestTypeDef,
    CreateDomainAssociationResultTypeDef,
    CreateWebhookRequestRequestTypeDef,
    CreateWebhookResultTypeDef,
    DeleteAppRequestRequestTypeDef,
    DeleteAppResultTypeDef,
    DeleteBackendEnvironmentRequestRequestTypeDef,
    DeleteBackendEnvironmentResultTypeDef,
    DeleteBranchRequestRequestTypeDef,
    DeleteBranchResultTypeDef,
    DeleteDomainAssociationRequestRequestTypeDef,
    DeleteDomainAssociationResultTypeDef,
    DeleteJobRequestRequestTypeDef,
    DeleteJobResultTypeDef,
    DeleteWebhookRequestRequestTypeDef,
    DeleteWebhookResultTypeDef,
    GenerateAccessLogsRequestRequestTypeDef,
    GenerateAccessLogsResultTypeDef,
    GetAppRequestRequestTypeDef,
    GetAppResultTypeDef,
    GetArtifactUrlRequestRequestTypeDef,
    GetArtifactUrlResultTypeDef,
    GetBackendEnvironmentRequestRequestTypeDef,
    GetBackendEnvironmentResultTypeDef,
    GetBranchRequestRequestTypeDef,
    GetBranchResultTypeDef,
    GetDomainAssociationRequestRequestTypeDef,
    GetDomainAssociationResultTypeDef,
    GetJobRequestRequestTypeDef,
    GetJobResultTypeDef,
    GetWebhookRequestRequestTypeDef,
    GetWebhookResultTypeDef,
    ListAppsRequestRequestTypeDef,
    ListAppsResultTypeDef,
    ListArtifactsRequestRequestTypeDef,
    ListArtifactsResultTypeDef,
    ListBackendEnvironmentsRequestRequestTypeDef,
    ListBackendEnvironmentsResultTypeDef,
    ListBranchesRequestRequestTypeDef,
    ListBranchesResultTypeDef,
    ListDomainAssociationsRequestRequestTypeDef,
    ListDomainAssociationsResultTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebhooksRequestRequestTypeDef,
    ListWebhooksResultTypeDef,
    StartDeploymentRequestRequestTypeDef,
    StartDeploymentResultTypeDef,
    StartJobRequestRequestTypeDef,
    StartJobResultTypeDef,
    StopJobRequestRequestTypeDef,
    StopJobResultTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAppRequestRequestTypeDef,
    UpdateAppResultTypeDef,
    UpdateBranchRequestRequestTypeDef,
    UpdateBranchResultTypeDef,
    UpdateDomainAssociationRequestRequestTypeDef,
    UpdateDomainAssociationResultTypeDef,
    UpdateWebhookRequestRequestTypeDef,
    UpdateWebhookResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AmplifyClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DependentServiceFailureException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class AmplifyClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AmplifyClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#close)
        """

    def create_app(
        self, **kwargs: Unpack[CreateAppRequestRequestTypeDef]
    ) -> CreateAppResultTypeDef:
        """
        Creates a new Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/create_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#create_app)
        """

    def create_backend_environment(
        self, **kwargs: Unpack[CreateBackendEnvironmentRequestRequestTypeDef]
    ) -> CreateBackendEnvironmentResultTypeDef:
        """
        Creates a new backend environment for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/create_backend_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#create_backend_environment)
        """

    def create_branch(
        self, **kwargs: Unpack[CreateBranchRequestRequestTypeDef]
    ) -> CreateBranchResultTypeDef:
        """
        Creates a new branch for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/create_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#create_branch)
        """

    def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestRequestTypeDef]
    ) -> CreateDeploymentResultTypeDef:
        """
        Creates a deployment for a manually deployed Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/create_deployment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#create_deployment)
        """

    def create_domain_association(
        self, **kwargs: Unpack[CreateDomainAssociationRequestRequestTypeDef]
    ) -> CreateDomainAssociationResultTypeDef:
        """
        Creates a new domain association for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/create_domain_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#create_domain_association)
        """

    def create_webhook(
        self, **kwargs: Unpack[CreateWebhookRequestRequestTypeDef]
    ) -> CreateWebhookResultTypeDef:
        """
        Creates a new webhook on an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/create_webhook.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#create_webhook)
        """

    def delete_app(
        self, **kwargs: Unpack[DeleteAppRequestRequestTypeDef]
    ) -> DeleteAppResultTypeDef:
        """
        Deletes an existing Amplify app specified by an app ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/delete_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#delete_app)
        """

    def delete_backend_environment(
        self, **kwargs: Unpack[DeleteBackendEnvironmentRequestRequestTypeDef]
    ) -> DeleteBackendEnvironmentResultTypeDef:
        """
        Deletes a backend environment for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/delete_backend_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#delete_backend_environment)
        """

    def delete_branch(
        self, **kwargs: Unpack[DeleteBranchRequestRequestTypeDef]
    ) -> DeleteBranchResultTypeDef:
        """
        Deletes a branch for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/delete_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#delete_branch)
        """

    def delete_domain_association(
        self, **kwargs: Unpack[DeleteDomainAssociationRequestRequestTypeDef]
    ) -> DeleteDomainAssociationResultTypeDef:
        """
        Deletes a domain association for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/delete_domain_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#delete_domain_association)
        """

    def delete_job(
        self, **kwargs: Unpack[DeleteJobRequestRequestTypeDef]
    ) -> DeleteJobResultTypeDef:
        """
        Deletes a job for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/delete_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#delete_job)
        """

    def delete_webhook(
        self, **kwargs: Unpack[DeleteWebhookRequestRequestTypeDef]
    ) -> DeleteWebhookResultTypeDef:
        """
        Deletes a webhook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/delete_webhook.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#delete_webhook)
        """

    def generate_access_logs(
        self, **kwargs: Unpack[GenerateAccessLogsRequestRequestTypeDef]
    ) -> GenerateAccessLogsResultTypeDef:
        """
        Returns the website access logs for a specific time range using a presigned URL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/generate_access_logs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#generate_access_logs)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#generate_presigned_url)
        """

    def get_app(self, **kwargs: Unpack[GetAppRequestRequestTypeDef]) -> GetAppResultTypeDef:
        """
        Returns an existing Amplify app specified by an app ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_app)
        """

    def get_artifact_url(
        self, **kwargs: Unpack[GetArtifactUrlRequestRequestTypeDef]
    ) -> GetArtifactUrlResultTypeDef:
        """
        Returns the artifact info that corresponds to an artifact id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_artifact_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_artifact_url)
        """

    def get_backend_environment(
        self, **kwargs: Unpack[GetBackendEnvironmentRequestRequestTypeDef]
    ) -> GetBackendEnvironmentResultTypeDef:
        """
        Returns a backend environment for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_backend_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_backend_environment)
        """

    def get_branch(
        self, **kwargs: Unpack[GetBranchRequestRequestTypeDef]
    ) -> GetBranchResultTypeDef:
        """
        Returns a branch for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_branch)
        """

    def get_domain_association(
        self, **kwargs: Unpack[GetDomainAssociationRequestRequestTypeDef]
    ) -> GetDomainAssociationResultTypeDef:
        """
        Returns the domain information for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_domain_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_domain_association)
        """

    def get_job(self, **kwargs: Unpack[GetJobRequestRequestTypeDef]) -> GetJobResultTypeDef:
        """
        Returns a job for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_job)
        """

    def get_webhook(
        self, **kwargs: Unpack[GetWebhookRequestRequestTypeDef]
    ) -> GetWebhookResultTypeDef:
        """
        Returns the webhook information that corresponds to a specified webhook ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_webhook.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_webhook)
        """

    def list_apps(self, **kwargs: Unpack[ListAppsRequestRequestTypeDef]) -> ListAppsResultTypeDef:
        """
        Returns a list of the existing Amplify apps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/list_apps.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#list_apps)
        """

    def list_artifacts(
        self, **kwargs: Unpack[ListArtifactsRequestRequestTypeDef]
    ) -> ListArtifactsResultTypeDef:
        """
        Returns a list of artifacts for a specified app, branch, and job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/list_artifacts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#list_artifacts)
        """

    def list_backend_environments(
        self, **kwargs: Unpack[ListBackendEnvironmentsRequestRequestTypeDef]
    ) -> ListBackendEnvironmentsResultTypeDef:
        """
        Lists the backend environments for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/list_backend_environments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#list_backend_environments)
        """

    def list_branches(
        self, **kwargs: Unpack[ListBranchesRequestRequestTypeDef]
    ) -> ListBranchesResultTypeDef:
        """
        Lists the branches of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/list_branches.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#list_branches)
        """

    def list_domain_associations(
        self, **kwargs: Unpack[ListDomainAssociationsRequestRequestTypeDef]
    ) -> ListDomainAssociationsResultTypeDef:
        """
        Returns the domain associations for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/list_domain_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#list_domain_associations)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]) -> ListJobsResultTypeDef:
        """
        Lists the jobs for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/list_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#list_jobs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#list_tags_for_resource)
        """

    def list_webhooks(
        self, **kwargs: Unpack[ListWebhooksRequestRequestTypeDef]
    ) -> ListWebhooksResultTypeDef:
        """
        Returns a list of webhooks for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/list_webhooks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#list_webhooks)
        """

    def start_deployment(
        self, **kwargs: Unpack[StartDeploymentRequestRequestTypeDef]
    ) -> StartDeploymentResultTypeDef:
        """
        Starts a deployment for a manually deployed app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/start_deployment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#start_deployment)
        """

    def start_job(self, **kwargs: Unpack[StartJobRequestRequestTypeDef]) -> StartJobResultTypeDef:
        """
        Starts a new job for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/start_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#start_job)
        """

    def stop_job(self, **kwargs: Unpack[StopJobRequestRequestTypeDef]) -> StopJobResultTypeDef:
        """
        Stops a job that is in progress for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/stop_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#stop_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags the resource with a tag key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Untags a resource with a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#untag_resource)
        """

    def update_app(
        self, **kwargs: Unpack[UpdateAppRequestRequestTypeDef]
    ) -> UpdateAppResultTypeDef:
        """
        Updates an existing Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/update_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#update_app)
        """

    def update_branch(
        self, **kwargs: Unpack[UpdateBranchRequestRequestTypeDef]
    ) -> UpdateBranchResultTypeDef:
        """
        Updates a branch for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/update_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#update_branch)
        """

    def update_domain_association(
        self, **kwargs: Unpack[UpdateDomainAssociationRequestRequestTypeDef]
    ) -> UpdateDomainAssociationResultTypeDef:
        """
        Creates a new domain association for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/update_domain_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#update_domain_association)
        """

    def update_webhook(
        self, **kwargs: Unpack[UpdateWebhookRequestRequestTypeDef]
    ) -> UpdateWebhookResultTypeDef:
        """
        Updates a webhook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/update_webhook.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#update_webhook)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_apps"]) -> ListAppsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_branches"]) -> ListBranchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_domain_associations"]
    ) -> ListDomainAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/client/#get_paginator)
        """
