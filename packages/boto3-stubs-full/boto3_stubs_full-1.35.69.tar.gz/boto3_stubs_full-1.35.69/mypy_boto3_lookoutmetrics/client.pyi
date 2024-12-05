"""
Type annotations for lookoutmetrics service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lookoutmetrics.client import LookoutMetricsClient

    session = Session()
    client: LookoutMetricsClient = session.client("lookoutmetrics")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    ActivateAnomalyDetectorRequestRequestTypeDef,
    BackTestAnomalyDetectorRequestRequestTypeDef,
    CreateAlertRequestRequestTypeDef,
    CreateAlertResponseTypeDef,
    CreateAnomalyDetectorRequestRequestTypeDef,
    CreateAnomalyDetectorResponseTypeDef,
    CreateMetricSetRequestRequestTypeDef,
    CreateMetricSetResponseTypeDef,
    DeactivateAnomalyDetectorRequestRequestTypeDef,
    DeleteAlertRequestRequestTypeDef,
    DeleteAnomalyDetectorRequestRequestTypeDef,
    DescribeAlertRequestRequestTypeDef,
    DescribeAlertResponseTypeDef,
    DescribeAnomalyDetectionExecutionsRequestRequestTypeDef,
    DescribeAnomalyDetectionExecutionsResponseTypeDef,
    DescribeAnomalyDetectorRequestRequestTypeDef,
    DescribeAnomalyDetectorResponseTypeDef,
    DescribeMetricSetRequestRequestTypeDef,
    DescribeMetricSetResponseTypeDef,
    DetectMetricSetConfigRequestRequestTypeDef,
    DetectMetricSetConfigResponseTypeDef,
    GetAnomalyGroupRequestRequestTypeDef,
    GetAnomalyGroupResponseTypeDef,
    GetDataQualityMetricsRequestRequestTypeDef,
    GetDataQualityMetricsResponseTypeDef,
    GetFeedbackRequestRequestTypeDef,
    GetFeedbackResponseTypeDef,
    GetSampleDataRequestRequestTypeDef,
    GetSampleDataResponseTypeDef,
    ListAlertsRequestRequestTypeDef,
    ListAlertsResponseTypeDef,
    ListAnomalyDetectorsRequestRequestTypeDef,
    ListAnomalyDetectorsResponseTypeDef,
    ListAnomalyGroupRelatedMetricsRequestRequestTypeDef,
    ListAnomalyGroupRelatedMetricsResponseTypeDef,
    ListAnomalyGroupSummariesRequestRequestTypeDef,
    ListAnomalyGroupSummariesResponseTypeDef,
    ListAnomalyGroupTimeSeriesRequestRequestTypeDef,
    ListAnomalyGroupTimeSeriesResponseTypeDef,
    ListMetricSetsRequestRequestTypeDef,
    ListMetricSetsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutFeedbackRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAlertRequestRequestTypeDef,
    UpdateAlertResponseTypeDef,
    UpdateAnomalyDetectorRequestRequestTypeDef,
    UpdateAnomalyDetectorResponseTypeDef,
    UpdateMetricSetRequestRequestTypeDef,
    UpdateMetricSetResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("LookoutMetricsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LookoutMetricsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LookoutMetricsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#exceptions)
        """

    def activate_anomaly_detector(
        self, **kwargs: Unpack[ActivateAnomalyDetectorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Activates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/activate_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#activate_anomaly_detector)
        """

    def back_test_anomaly_detector(
        self, **kwargs: Unpack[BackTestAnomalyDetectorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Runs a backtest for anomaly detection for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/back_test_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#back_test_anomaly_detector)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#close)
        """

    def create_alert(
        self, **kwargs: Unpack[CreateAlertRequestRequestTypeDef]
    ) -> CreateAlertResponseTypeDef:
        """
        Creates an alert for an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/create_alert.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#create_alert)
        """

    def create_anomaly_detector(
        self, **kwargs: Unpack[CreateAnomalyDetectorRequestRequestTypeDef]
    ) -> CreateAnomalyDetectorResponseTypeDef:
        """
        Creates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/create_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#create_anomaly_detector)
        """

    def create_metric_set(
        self, **kwargs: Unpack[CreateMetricSetRequestRequestTypeDef]
    ) -> CreateMetricSetResponseTypeDef:
        """
        Creates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/create_metric_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#create_metric_set)
        """

    def deactivate_anomaly_detector(
        self, **kwargs: Unpack[DeactivateAnomalyDetectorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deactivates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/deactivate_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#deactivate_anomaly_detector)
        """

    def delete_alert(self, **kwargs: Unpack[DeleteAlertRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/delete_alert.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#delete_alert)
        """

    def delete_anomaly_detector(
        self, **kwargs: Unpack[DeleteAnomalyDetectorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/delete_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#delete_anomaly_detector)
        """

    def describe_alert(
        self, **kwargs: Unpack[DescribeAlertRequestRequestTypeDef]
    ) -> DescribeAlertResponseTypeDef:
        """
        Describes an alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/describe_alert.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#describe_alert)
        """

    def describe_anomaly_detection_executions(
        self, **kwargs: Unpack[DescribeAnomalyDetectionExecutionsRequestRequestTypeDef]
    ) -> DescribeAnomalyDetectionExecutionsResponseTypeDef:
        """
        Returns information about the status of the specified anomaly detection jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/describe_anomaly_detection_executions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#describe_anomaly_detection_executions)
        """

    def describe_anomaly_detector(
        self, **kwargs: Unpack[DescribeAnomalyDetectorRequestRequestTypeDef]
    ) -> DescribeAnomalyDetectorResponseTypeDef:
        """
        Describes a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/describe_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#describe_anomaly_detector)
        """

    def describe_metric_set(
        self, **kwargs: Unpack[DescribeMetricSetRequestRequestTypeDef]
    ) -> DescribeMetricSetResponseTypeDef:
        """
        Describes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/describe_metric_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#describe_metric_set)
        """

    def detect_metric_set_config(
        self, **kwargs: Unpack[DetectMetricSetConfigRequestRequestTypeDef]
    ) -> DetectMetricSetConfigResponseTypeDef:
        """
        Detects an Amazon S3 dataset's file format, interval, and offset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/detect_metric_set_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#detect_metric_set_config)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#generate_presigned_url)
        """

    def get_anomaly_group(
        self, **kwargs: Unpack[GetAnomalyGroupRequestRequestTypeDef]
    ) -> GetAnomalyGroupResponseTypeDef:
        """
        Returns details about a group of anomalous metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/get_anomaly_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#get_anomaly_group)
        """

    def get_data_quality_metrics(
        self, **kwargs: Unpack[GetDataQualityMetricsRequestRequestTypeDef]
    ) -> GetDataQualityMetricsResponseTypeDef:
        """
        Returns details about the requested data quality metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/get_data_quality_metrics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#get_data_quality_metrics)
        """

    def get_feedback(
        self, **kwargs: Unpack[GetFeedbackRequestRequestTypeDef]
    ) -> GetFeedbackResponseTypeDef:
        """
        Get feedback for an anomaly group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/get_feedback.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#get_feedback)
        """

    def get_sample_data(
        self, **kwargs: Unpack[GetSampleDataRequestRequestTypeDef]
    ) -> GetSampleDataResponseTypeDef:
        """
        Returns a selection of sample records from an Amazon S3 datasource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/get_sample_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#get_sample_data)
        """

    def list_alerts(
        self, **kwargs: Unpack[ListAlertsRequestRequestTypeDef]
    ) -> ListAlertsResponseTypeDef:
        """
        Lists the alerts attached to a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_alerts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#list_alerts)
        """

    def list_anomaly_detectors(
        self, **kwargs: Unpack[ListAnomalyDetectorsRequestRequestTypeDef]
    ) -> ListAnomalyDetectorsResponseTypeDef:
        """
        Lists the detectors in the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_anomaly_detectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#list_anomaly_detectors)
        """

    def list_anomaly_group_related_metrics(
        self, **kwargs: Unpack[ListAnomalyGroupRelatedMetricsRequestRequestTypeDef]
    ) -> ListAnomalyGroupRelatedMetricsResponseTypeDef:
        """
        Returns a list of measures that are potential causes or effects of an anomaly
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_anomaly_group_related_metrics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#list_anomaly_group_related_metrics)
        """

    def list_anomaly_group_summaries(
        self, **kwargs: Unpack[ListAnomalyGroupSummariesRequestRequestTypeDef]
    ) -> ListAnomalyGroupSummariesResponseTypeDef:
        """
        Returns a list of anomaly groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_anomaly_group_summaries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#list_anomaly_group_summaries)
        """

    def list_anomaly_group_time_series(
        self, **kwargs: Unpack[ListAnomalyGroupTimeSeriesRequestRequestTypeDef]
    ) -> ListAnomalyGroupTimeSeriesResponseTypeDef:
        """
        Gets a list of anomalous metrics for a measure in an anomaly group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_anomaly_group_time_series.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#list_anomaly_group_time_series)
        """

    def list_metric_sets(
        self, **kwargs: Unpack[ListMetricSetsRequestRequestTypeDef]
    ) -> ListMetricSetsResponseTypeDef:
        """
        Lists the datasets in the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_metric_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#list_metric_sets)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of
        [tags](https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html)
        for a detector, dataset, or alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#list_tags_for_resource)
        """

    def put_feedback(self, **kwargs: Unpack[PutFeedbackRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Add feedback for an anomalous metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/put_feedback.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#put_feedback)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds
        [tags](https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html)
        to a detector, dataset, or alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes
        [tags](https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html)
        from a detector, dataset, or alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#untag_resource)
        """

    def update_alert(
        self, **kwargs: Unpack[UpdateAlertRequestRequestTypeDef]
    ) -> UpdateAlertResponseTypeDef:
        """
        Make changes to an existing alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/update_alert.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#update_alert)
        """

    def update_anomaly_detector(
        self, **kwargs: Unpack[UpdateAnomalyDetectorRequestRequestTypeDef]
    ) -> UpdateAnomalyDetectorResponseTypeDef:
        """
        Updates a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/update_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#update_anomaly_detector)
        """

    def update_metric_set(
        self, **kwargs: Unpack[UpdateMetricSetRequestRequestTypeDef]
    ) -> UpdateMetricSetResponseTypeDef:
        """
        Updates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/update_metric_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutmetrics/client/#update_metric_set)
        """
