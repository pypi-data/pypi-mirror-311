"""
Type annotations for xray service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_xray.client import XRayClient

    session = Session()
    client: XRayClient = session.client("xray")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    BatchGetTracesPaginator,
    GetGroupsPaginator,
    GetSamplingRulesPaginator,
    GetSamplingStatisticSummariesPaginator,
    GetServiceGraphPaginator,
    GetTimeSeriesServiceStatisticsPaginator,
    GetTraceGraphPaginator,
    GetTraceSummariesPaginator,
    ListResourcePoliciesPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    BatchGetTracesRequestRequestTypeDef,
    BatchGetTracesResultTypeDef,
    CancelTraceRetrievalRequestRequestTypeDef,
    CreateGroupRequestRequestTypeDef,
    CreateGroupResultTypeDef,
    CreateSamplingRuleRequestRequestTypeDef,
    CreateSamplingRuleResultTypeDef,
    DeleteGroupRequestRequestTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteSamplingRuleRequestRequestTypeDef,
    DeleteSamplingRuleResultTypeDef,
    GetEncryptionConfigResultTypeDef,
    GetGroupRequestRequestTypeDef,
    GetGroupResultTypeDef,
    GetGroupsRequestRequestTypeDef,
    GetGroupsResultTypeDef,
    GetIndexingRulesRequestRequestTypeDef,
    GetIndexingRulesResultTypeDef,
    GetInsightEventsRequestRequestTypeDef,
    GetInsightEventsResultTypeDef,
    GetInsightImpactGraphRequestRequestTypeDef,
    GetInsightImpactGraphResultTypeDef,
    GetInsightRequestRequestTypeDef,
    GetInsightResultTypeDef,
    GetInsightSummariesRequestRequestTypeDef,
    GetInsightSummariesResultTypeDef,
    GetRetrievedTracesGraphRequestRequestTypeDef,
    GetRetrievedTracesGraphResultTypeDef,
    GetSamplingRulesRequestRequestTypeDef,
    GetSamplingRulesResultTypeDef,
    GetSamplingStatisticSummariesRequestRequestTypeDef,
    GetSamplingStatisticSummariesResultTypeDef,
    GetSamplingTargetsRequestRequestTypeDef,
    GetSamplingTargetsResultTypeDef,
    GetServiceGraphRequestRequestTypeDef,
    GetServiceGraphResultTypeDef,
    GetTimeSeriesServiceStatisticsRequestRequestTypeDef,
    GetTimeSeriesServiceStatisticsResultTypeDef,
    GetTraceGraphRequestRequestTypeDef,
    GetTraceGraphResultTypeDef,
    GetTraceSegmentDestinationResultTypeDef,
    GetTraceSummariesRequestRequestTypeDef,
    GetTraceSummariesResultTypeDef,
    ListResourcePoliciesRequestRequestTypeDef,
    ListResourcePoliciesResultTypeDef,
    ListRetrievedTracesRequestRequestTypeDef,
    ListRetrievedTracesResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutEncryptionConfigRequestRequestTypeDef,
    PutEncryptionConfigResultTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResultTypeDef,
    PutTelemetryRecordsRequestRequestTypeDef,
    PutTraceSegmentsRequestRequestTypeDef,
    PutTraceSegmentsResultTypeDef,
    StartTraceRetrievalRequestRequestTypeDef,
    StartTraceRetrievalResultTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateGroupRequestRequestTypeDef,
    UpdateGroupResultTypeDef,
    UpdateIndexingRuleRequestRequestTypeDef,
    UpdateIndexingRuleResultTypeDef,
    UpdateSamplingRuleRequestRequestTypeDef,
    UpdateSamplingRuleResultTypeDef,
    UpdateTraceSegmentDestinationRequestRequestTypeDef,
    UpdateTraceSegmentDestinationResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("XRayClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidPolicyRevisionIdException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LockoutPreventionException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    PolicyCountLimitExceededException: Type[BotocoreClientError]
    PolicySizeLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    RuleLimitExceededException: Type[BotocoreClientError]
    ThrottledException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class XRayClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        XRayClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#exceptions)
        """

    def batch_get_traces(
        self, **kwargs: Unpack[BatchGetTracesRequestRequestTypeDef]
    ) -> BatchGetTracesResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/batch_get_traces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#batch_get_traces)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#can_paginate)
        """

    def cancel_trace_retrieval(
        self, **kwargs: Unpack[CancelTraceRetrievalRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels an ongoing trace retrieval job initiated by `StartTraceRetrieval` using
        the provided `RetrievalToken`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/cancel_trace_retrieval.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#cancel_trace_retrieval)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#close)
        """

    def create_group(
        self, **kwargs: Unpack[CreateGroupRequestRequestTypeDef]
    ) -> CreateGroupResultTypeDef:
        """
        Creates a group resource with a name and a filter expression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/create_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#create_group)
        """

    def create_sampling_rule(
        self, **kwargs: Unpack[CreateSamplingRuleRequestRequestTypeDef]
    ) -> CreateSamplingRuleResultTypeDef:
        """
        Creates a rule to control sampling behavior for instrumented applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/create_sampling_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#create_sampling_rule)
        """

    def delete_group(self, **kwargs: Unpack[DeleteGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a group resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/delete_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#delete_group)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a resource policy from the target Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/delete_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#delete_resource_policy)
        """

    def delete_sampling_rule(
        self, **kwargs: Unpack[DeleteSamplingRuleRequestRequestTypeDef]
    ) -> DeleteSamplingRuleResultTypeDef:
        """
        Deletes a sampling rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/delete_sampling_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#delete_sampling_rule)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#generate_presigned_url)
        """

    def get_encryption_config(self) -> GetEncryptionConfigResultTypeDef:
        """
        Retrieves the current encryption configuration for X-Ray data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_encryption_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_encryption_config)
        """

    def get_group(self, **kwargs: Unpack[GetGroupRequestRequestTypeDef]) -> GetGroupResultTypeDef:
        """
        Retrieves group resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_group)
        """

    def get_groups(
        self, **kwargs: Unpack[GetGroupsRequestRequestTypeDef]
    ) -> GetGroupsResultTypeDef:
        """
        Retrieves all active group details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_groups)
        """

    def get_indexing_rules(
        self, **kwargs: Unpack[GetIndexingRulesRequestRequestTypeDef]
    ) -> GetIndexingRulesResultTypeDef:
        """
        Retrieves all indexing rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_indexing_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_indexing_rules)
        """

    def get_insight(
        self, **kwargs: Unpack[GetInsightRequestRequestTypeDef]
    ) -> GetInsightResultTypeDef:
        """
        Retrieves the summary information of an insight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_insight.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_insight)
        """

    def get_insight_events(
        self, **kwargs: Unpack[GetInsightEventsRequestRequestTypeDef]
    ) -> GetInsightEventsResultTypeDef:
        """
        X-Ray reevaluates insights periodically until they're resolved, and records
        each intermediate state as an event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_insight_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_insight_events)
        """

    def get_insight_impact_graph(
        self, **kwargs: Unpack[GetInsightImpactGraphRequestRequestTypeDef]
    ) -> GetInsightImpactGraphResultTypeDef:
        """
        Retrieves a service graph structure filtered by the specified insight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_insight_impact_graph.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_insight_impact_graph)
        """

    def get_insight_summaries(
        self, **kwargs: Unpack[GetInsightSummariesRequestRequestTypeDef]
    ) -> GetInsightSummariesResultTypeDef:
        """
        Retrieves the summaries of all insights in the specified group matching the
        provided filter values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_insight_summaries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_insight_summaries)
        """

    def get_retrieved_traces_graph(
        self, **kwargs: Unpack[GetRetrievedTracesGraphRequestRequestTypeDef]
    ) -> GetRetrievedTracesGraphResultTypeDef:
        """
        Retrieves a service graph for traces based on the specified `RetrievalToken`
        from the CloudWatch log group generated by Transaction Search.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_retrieved_traces_graph.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_retrieved_traces_graph)
        """

    def get_sampling_rules(
        self, **kwargs: Unpack[GetSamplingRulesRequestRequestTypeDef]
    ) -> GetSamplingRulesResultTypeDef:
        """
        Retrieves all sampling rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_sampling_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_sampling_rules)
        """

    def get_sampling_statistic_summaries(
        self, **kwargs: Unpack[GetSamplingStatisticSummariesRequestRequestTypeDef]
    ) -> GetSamplingStatisticSummariesResultTypeDef:
        """
        Retrieves information about recent sampling results for all sampling rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_sampling_statistic_summaries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_sampling_statistic_summaries)
        """

    def get_sampling_targets(
        self, **kwargs: Unpack[GetSamplingTargetsRequestRequestTypeDef]
    ) -> GetSamplingTargetsResultTypeDef:
        """
        Requests a sampling quota for rules that the service is using to sample
        requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_sampling_targets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_sampling_targets)
        """

    def get_service_graph(
        self, **kwargs: Unpack[GetServiceGraphRequestRequestTypeDef]
    ) -> GetServiceGraphResultTypeDef:
        """
        Retrieves a document that describes services that process incoming requests,
        and downstream services that they call as a result.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_service_graph.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_service_graph)
        """

    def get_time_series_service_statistics(
        self, **kwargs: Unpack[GetTimeSeriesServiceStatisticsRequestRequestTypeDef]
    ) -> GetTimeSeriesServiceStatisticsResultTypeDef:
        """
        Get an aggregation of service statistics defined by a specific time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_time_series_service_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_time_series_service_statistics)
        """

    def get_trace_graph(
        self, **kwargs: Unpack[GetTraceGraphRequestRequestTypeDef]
    ) -> GetTraceGraphResultTypeDef:
        """
        Retrieves a service graph for one or more specific trace IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_trace_graph.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_trace_graph)
        """

    def get_trace_segment_destination(self) -> GetTraceSegmentDestinationResultTypeDef:
        """
        Retrieves the current destination of data sent to `PutTraceSegments` and
        *OpenTelemetry* API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_trace_segment_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_trace_segment_destination)
        """

    def get_trace_summaries(
        self, **kwargs: Unpack[GetTraceSummariesRequestRequestTypeDef]
    ) -> GetTraceSummariesResultTypeDef:
        """
        Retrieves IDs and annotations for traces available for a specified time frame
        using an optional filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_trace_summaries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_trace_summaries)
        """

    def list_resource_policies(
        self, **kwargs: Unpack[ListResourcePoliciesRequestRequestTypeDef]
    ) -> ListResourcePoliciesResultTypeDef:
        """
        Returns the list of resource policies in the target Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/list_resource_policies.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#list_resource_policies)
        """

    def list_retrieved_traces(
        self, **kwargs: Unpack[ListRetrievedTracesRequestRequestTypeDef]
    ) -> ListRetrievedTracesResultTypeDef:
        """
        Retrieves a list of traces for a given `RetrievalToken` from the CloudWatch log
        group generated by Transaction Search.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/list_retrieved_traces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#list_retrieved_traces)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags that are applied to the specified Amazon Web Services
        X-Ray group or sampling rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#list_tags_for_resource)
        """

    def put_encryption_config(
        self, **kwargs: Unpack[PutEncryptionConfigRequestRequestTypeDef]
    ) -> PutEncryptionConfigResultTypeDef:
        """
        Updates the encryption configuration for X-Ray data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/put_encryption_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#put_encryption_config)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResultTypeDef:
        """
        Sets the resource policy to grant one or more Amazon Web Services services and
        accounts permissions to access X-Ray.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/put_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#put_resource_policy)
        """

    def put_telemetry_records(
        self, **kwargs: Unpack[PutTelemetryRecordsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used by the Amazon Web Services X-Ray daemon to upload telemetry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/put_telemetry_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#put_telemetry_records)
        """

    def put_trace_segments(
        self, **kwargs: Unpack[PutTraceSegmentsRequestRequestTypeDef]
    ) -> PutTraceSegmentsResultTypeDef:
        """
        Uploads segment documents to Amazon Web Services X-Ray.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/put_trace_segments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#put_trace_segments)
        """

    def start_trace_retrieval(
        self, **kwargs: Unpack[StartTraceRetrievalRequestRequestTypeDef]
    ) -> StartTraceRetrievalResultTypeDef:
        """
        Initiates a trace retrieval process using the specified time range and for the
        give trace IDs on Transaction Search generated by the CloudWatch log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/start_trace_retrieval.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#start_trace_retrieval)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Applies tags to an existing Amazon Web Services X-Ray group or sampling rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from an Amazon Web Services X-Ray group or sampling rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#untag_resource)
        """

    def update_group(
        self, **kwargs: Unpack[UpdateGroupRequestRequestTypeDef]
    ) -> UpdateGroupResultTypeDef:
        """
        Updates a group resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/update_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#update_group)
        """

    def update_indexing_rule(
        self, **kwargs: Unpack[UpdateIndexingRuleRequestRequestTypeDef]
    ) -> UpdateIndexingRuleResultTypeDef:
        """
        Modifies an indexing rule's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/update_indexing_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#update_indexing_rule)
        """

    def update_sampling_rule(
        self, **kwargs: Unpack[UpdateSamplingRuleRequestRequestTypeDef]
    ) -> UpdateSamplingRuleResultTypeDef:
        """
        Modifies a sampling rule's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/update_sampling_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#update_sampling_rule)
        """

    def update_trace_segment_destination(
        self, **kwargs: Unpack[UpdateTraceSegmentDestinationRequestRequestTypeDef]
    ) -> UpdateTraceSegmentDestinationResultTypeDef:
        """
        Modifies the destination of data sent to `PutTraceSegments`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/update_trace_segment_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#update_trace_segment_destination)
        """

    @overload
    def get_paginator(self, operation_name: Literal["batch_get_traces"]) -> BatchGetTracesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_groups"]) -> GetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_sampling_rules"]
    ) -> GetSamplingRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_sampling_statistic_summaries"]
    ) -> GetSamplingStatisticSummariesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_service_graph"]
    ) -> GetServiceGraphPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_time_series_service_statistics"]
    ) -> GetTimeSeriesServiceStatisticsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_trace_graph"]) -> GetTraceGraphPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_trace_summaries"]
    ) -> GetTraceSummariesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_policies"]
    ) -> ListResourcePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/client/#get_paginator)
        """
