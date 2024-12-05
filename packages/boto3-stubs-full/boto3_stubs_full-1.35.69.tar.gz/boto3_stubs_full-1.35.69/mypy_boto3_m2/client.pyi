"""
Type annotations for m2 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_m2.client import MainframeModernizationClient

    session = Session()
    client: MainframeModernizationClient = session.client("m2")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListApplicationsPaginator,
    ListApplicationVersionsPaginator,
    ListBatchJobDefinitionsPaginator,
    ListBatchJobExecutionsPaginator,
    ListDataSetImportHistoryPaginator,
    ListDataSetsPaginator,
    ListDeploymentsPaginator,
    ListEngineVersionsPaginator,
    ListEnvironmentsPaginator,
)
from .type_defs import (
    CancelBatchJobExecutionRequestRequestTypeDef,
    CreateApplicationRequestRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateDataSetImportTaskRequestRequestTypeDef,
    CreateDataSetImportTaskResponseTypeDef,
    CreateDeploymentRequestRequestTypeDef,
    CreateDeploymentResponseTypeDef,
    CreateEnvironmentRequestRequestTypeDef,
    CreateEnvironmentResponseTypeDef,
    DeleteApplicationFromEnvironmentRequestRequestTypeDef,
    DeleteApplicationRequestRequestTypeDef,
    DeleteEnvironmentRequestRequestTypeDef,
    GetApplicationRequestRequestTypeDef,
    GetApplicationResponseTypeDef,
    GetApplicationVersionRequestRequestTypeDef,
    GetApplicationVersionResponseTypeDef,
    GetBatchJobExecutionRequestRequestTypeDef,
    GetBatchJobExecutionResponseTypeDef,
    GetDataSetDetailsRequestRequestTypeDef,
    GetDataSetDetailsResponseTypeDef,
    GetDataSetImportTaskRequestRequestTypeDef,
    GetDataSetImportTaskResponseTypeDef,
    GetDeploymentRequestRequestTypeDef,
    GetDeploymentResponseTypeDef,
    GetEnvironmentRequestRequestTypeDef,
    GetEnvironmentResponseTypeDef,
    GetSignedBluinsightsUrlResponseTypeDef,
    ListApplicationsRequestRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsRequestRequestTypeDef,
    ListApplicationVersionsResponseTypeDef,
    ListBatchJobDefinitionsRequestRequestTypeDef,
    ListBatchJobDefinitionsResponseTypeDef,
    ListBatchJobExecutionsRequestRequestTypeDef,
    ListBatchJobExecutionsResponseTypeDef,
    ListBatchJobRestartPointsRequestRequestTypeDef,
    ListBatchJobRestartPointsResponseTypeDef,
    ListDataSetImportHistoryRequestRequestTypeDef,
    ListDataSetImportHistoryResponseTypeDef,
    ListDataSetsRequestRequestTypeDef,
    ListDataSetsResponseTypeDef,
    ListDeploymentsRequestRequestTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEngineVersionsRequestRequestTypeDef,
    ListEngineVersionsResponseTypeDef,
    ListEnvironmentsRequestRequestTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartApplicationRequestRequestTypeDef,
    StartBatchJobRequestRequestTypeDef,
    StartBatchJobResponseTypeDef,
    StopApplicationRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateApplicationRequestRequestTypeDef,
    UpdateApplicationResponseTypeDef,
    UpdateEnvironmentRequestRequestTypeDef,
    UpdateEnvironmentResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("MainframeModernizationClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ExecutionTimeoutException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class MainframeModernizationClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MainframeModernizationClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#can_paginate)
        """

    def cancel_batch_job_execution(
        self, **kwargs: Unpack[CancelBatchJobExecutionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the running of a specific batch job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/cancel_batch_job_execution.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#cancel_batch_job_execution)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#close)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates a new application with given parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/create_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#create_application)
        """

    def create_data_set_import_task(
        self, **kwargs: Unpack[CreateDataSetImportTaskRequestRequestTypeDef]
    ) -> CreateDataSetImportTaskResponseTypeDef:
        """
        Starts a data set import task for a specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/create_data_set_import_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#create_data_set_import_task)
        """

    def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestRequestTypeDef]
    ) -> CreateDeploymentResponseTypeDef:
        """
        Creates and starts a deployment to deploy an application into a runtime
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/create_deployment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#create_deployment)
        """

    def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentRequestRequestTypeDef]
    ) -> CreateEnvironmentResponseTypeDef:
        """
        Creates a runtime environment for a given runtime engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/create_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#create_environment)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/delete_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#delete_application)
        """

    def delete_application_from_environment(
        self, **kwargs: Unpack[DeleteApplicationFromEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specific application from the specific runtime environment where it
        was previously deployed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/delete_application_from_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#delete_application_from_environment)
        """

    def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specific runtime environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/delete_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#delete_environment)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#generate_presigned_url)
        """

    def get_application(
        self, **kwargs: Unpack[GetApplicationRequestRequestTypeDef]
    ) -> GetApplicationResponseTypeDef:
        """
        Describes the details of a specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_application)
        """

    def get_application_version(
        self, **kwargs: Unpack[GetApplicationVersionRequestRequestTypeDef]
    ) -> GetApplicationVersionResponseTypeDef:
        """
        Returns details about a specific version of a specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_application_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_application_version)
        """

    def get_batch_job_execution(
        self, **kwargs: Unpack[GetBatchJobExecutionRequestRequestTypeDef]
    ) -> GetBatchJobExecutionResponseTypeDef:
        """
        Gets the details of a specific batch job execution for a specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_batch_job_execution.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_batch_job_execution)
        """

    def get_data_set_details(
        self, **kwargs: Unpack[GetDataSetDetailsRequestRequestTypeDef]
    ) -> GetDataSetDetailsResponseTypeDef:
        """
        Gets the details of a specific data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_data_set_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_data_set_details)
        """

    def get_data_set_import_task(
        self, **kwargs: Unpack[GetDataSetImportTaskRequestRequestTypeDef]
    ) -> GetDataSetImportTaskResponseTypeDef:
        """
        Gets the status of a data set import task initiated with the
        CreateDataSetImportTask operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_data_set_import_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_data_set_import_task)
        """

    def get_deployment(
        self, **kwargs: Unpack[GetDeploymentRequestRequestTypeDef]
    ) -> GetDeploymentResponseTypeDef:
        """
        Gets details of a specific deployment with a given deployment identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_deployment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_deployment)
        """

    def get_environment(
        self, **kwargs: Unpack[GetEnvironmentRequestRequestTypeDef]
    ) -> GetEnvironmentResponseTypeDef:
        """
        Describes a specific runtime environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_environment)
        """

    def get_signed_bluinsights_url(self) -> GetSignedBluinsightsUrlResponseTypeDef:
        """
        Gets a single sign-on URL that can be used to connect to AWS Blu Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_signed_bluinsights_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_signed_bluinsights_url)
        """

    def list_application_versions(
        self, **kwargs: Unpack[ListApplicationVersionsRequestRequestTypeDef]
    ) -> ListApplicationVersionsResponseTypeDef:
        """
        Returns a list of the application versions for a specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_application_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_application_versions)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists the applications associated with a specific Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_applications)
        """

    def list_batch_job_definitions(
        self, **kwargs: Unpack[ListBatchJobDefinitionsRequestRequestTypeDef]
    ) -> ListBatchJobDefinitionsResponseTypeDef:
        """
        Lists all the available batch job definitions based on the batch job resources
        uploaded during the application creation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_batch_job_definitions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_batch_job_definitions)
        """

    def list_batch_job_executions(
        self, **kwargs: Unpack[ListBatchJobExecutionsRequestRequestTypeDef]
    ) -> ListBatchJobExecutionsResponseTypeDef:
        """
        Lists historical, current, and scheduled batch job executions for a specific
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_batch_job_executions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_batch_job_executions)
        """

    def list_batch_job_restart_points(
        self, **kwargs: Unpack[ListBatchJobRestartPointsRequestRequestTypeDef]
    ) -> ListBatchJobRestartPointsResponseTypeDef:
        """
        Lists all the job steps for a JCL file to restart a batch job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_batch_job_restart_points.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_batch_job_restart_points)
        """

    def list_data_set_import_history(
        self, **kwargs: Unpack[ListDataSetImportHistoryRequestRequestTypeDef]
    ) -> ListDataSetImportHistoryResponseTypeDef:
        """
        Lists the data set imports for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_data_set_import_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_data_set_import_history)
        """

    def list_data_sets(
        self, **kwargs: Unpack[ListDataSetsRequestRequestTypeDef]
    ) -> ListDataSetsResponseTypeDef:
        """
        Lists the data sets imported for a specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_data_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_data_sets)
        """

    def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsRequestRequestTypeDef]
    ) -> ListDeploymentsResponseTypeDef:
        """
        Returns a list of all deployments of a specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_deployments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_deployments)
        """

    def list_engine_versions(
        self, **kwargs: Unpack[ListEngineVersionsRequestRequestTypeDef]
    ) -> ListEngineVersionsResponseTypeDef:
        """
        Lists the available engine versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_engine_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_engine_versions)
        """

    def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsRequestRequestTypeDef]
    ) -> ListEnvironmentsResponseTypeDef:
        """
        Lists the runtime environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_environments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_environments)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#list_tags_for_resource)
        """

    def start_application(
        self, **kwargs: Unpack[StartApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts an application that is currently stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/start_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#start_application)
        """

    def start_batch_job(
        self, **kwargs: Unpack[StartBatchJobRequestRequestTypeDef]
    ) -> StartBatchJobResponseTypeDef:
        """
        Starts a batch job and returns the unique identifier of this execution of the
        batch job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/start_batch_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#start_batch_job)
        """

    def stop_application(
        self, **kwargs: Unpack[StopApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a running application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/stop_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#stop_application)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#untag_resource)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestRequestTypeDef]
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates an application and creates a new version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/update_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#update_application)
        """

    def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentRequestRequestTypeDef]
    ) -> UpdateEnvironmentResponseTypeDef:
        """
        Updates the configuration details for a specific runtime environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/update_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#update_environment)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_versions"]
    ) -> ListApplicationVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_batch_job_definitions"]
    ) -> ListBatchJobDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_batch_job_executions"]
    ) -> ListBatchJobExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_set_import_history"]
    ) -> ListDataSetImportHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_data_sets"]) -> ListDataSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_engine_versions"]
    ) -> ListEngineVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/client/#get_paginator)
        """
