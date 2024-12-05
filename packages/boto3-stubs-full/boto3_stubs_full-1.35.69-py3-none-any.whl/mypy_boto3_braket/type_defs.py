"""
Type annotations for braket service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/type_defs/)

Usage::

    ```python
    from mypy_boto3_braket.type_defs import ContainerImageTypeDef

    data: ContainerImageTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    CancellationStatusType,
    CompressionTypeType,
    DeviceStatusType,
    DeviceTypeType,
    InstanceTypeType,
    JobEventTypeType,
    JobPrimaryStatusType,
    QuantumTaskStatusType,
    QueueNameType,
    QueuePriorityType,
    SearchJobsFilterOperatorType,
    SearchQuantumTasksFilterOperatorType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AlgorithmSpecificationTypeDef",
    "AssociationTypeDef",
    "CancelJobRequestRequestTypeDef",
    "CancelJobResponseTypeDef",
    "CancelQuantumTaskRequestRequestTypeDef",
    "CancelQuantumTaskResponseTypeDef",
    "ContainerImageTypeDef",
    "CreateJobRequestRequestTypeDef",
    "CreateJobResponseTypeDef",
    "CreateQuantumTaskRequestRequestTypeDef",
    "CreateQuantumTaskResponseTypeDef",
    "DataSourceTypeDef",
    "DeviceConfigTypeDef",
    "DeviceQueueInfoTypeDef",
    "DeviceSummaryTypeDef",
    "GetDeviceRequestRequestTypeDef",
    "GetDeviceResponseTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetJobResponseTypeDef",
    "GetQuantumTaskRequestRequestTypeDef",
    "GetQuantumTaskResponseTypeDef",
    "HybridJobQueueInfoTypeDef",
    "InputFileConfigTypeDef",
    "InstanceConfigTypeDef",
    "JobCheckpointConfigTypeDef",
    "JobEventDetailsTypeDef",
    "JobOutputDataConfigTypeDef",
    "JobStoppingConditionTypeDef",
    "JobSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "QuantumTaskQueueInfoTypeDef",
    "QuantumTaskSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "S3DataSourceTypeDef",
    "ScriptModeConfigTypeDef",
    "SearchDevicesFilterTypeDef",
    "SearchDevicesRequestRequestTypeDef",
    "SearchDevicesRequestSearchDevicesPaginateTypeDef",
    "SearchDevicesResponseTypeDef",
    "SearchJobsFilterTypeDef",
    "SearchJobsRequestRequestTypeDef",
    "SearchJobsRequestSearchJobsPaginateTypeDef",
    "SearchJobsResponseTypeDef",
    "SearchQuantumTasksFilterTypeDef",
    "SearchQuantumTasksRequestRequestTypeDef",
    "SearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef",
    "SearchQuantumTasksResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
)


class ContainerImageTypeDef(TypedDict):
    uri: str


class ScriptModeConfigTypeDef(TypedDict):
    entryPoint: str
    s3Uri: str
    compressionType: NotRequired[CompressionTypeType]


AssociationTypeDef = TypedDict(
    "AssociationTypeDef",
    {
        "arn": str,
        "type": Literal["RESERVATION_TIME_WINDOW_ARN"],
    },
)


class CancelJobRequestRequestTypeDef(TypedDict):
    jobArn: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CancelQuantumTaskRequestRequestTypeDef(TypedDict):
    clientToken: str
    quantumTaskArn: str


class DeviceConfigTypeDef(TypedDict):
    device: str


class InstanceConfigTypeDef(TypedDict):
    instanceType: InstanceTypeType
    volumeSizeInGb: int
    instanceCount: NotRequired[int]


class JobCheckpointConfigTypeDef(TypedDict):
    s3Uri: str
    localPath: NotRequired[str]


class JobOutputDataConfigTypeDef(TypedDict):
    s3Path: str
    kmsKeyId: NotRequired[str]


class JobStoppingConditionTypeDef(TypedDict):
    maxRuntimeInSeconds: NotRequired[int]


class S3DataSourceTypeDef(TypedDict):
    s3Uri: str


class DeviceQueueInfoTypeDef(TypedDict):
    queue: QueueNameType
    queueSize: str
    queuePriority: NotRequired[QueuePriorityType]


class DeviceSummaryTypeDef(TypedDict):
    deviceArn: str
    deviceName: str
    deviceStatus: DeviceStatusType
    deviceType: DeviceTypeType
    providerName: str


class GetDeviceRequestRequestTypeDef(TypedDict):
    deviceArn: str


class GetJobRequestRequestTypeDef(TypedDict):
    jobArn: str
    additionalAttributeNames: NotRequired[Sequence[Literal["QueueInfo"]]]


class HybridJobQueueInfoTypeDef(TypedDict):
    position: str
    queue: QueueNameType
    message: NotRequired[str]


class JobEventDetailsTypeDef(TypedDict):
    eventType: NotRequired[JobEventTypeType]
    message: NotRequired[str]
    timeOfEvent: NotRequired[datetime]


class GetQuantumTaskRequestRequestTypeDef(TypedDict):
    quantumTaskArn: str
    additionalAttributeNames: NotRequired[Sequence[Literal["QueueInfo"]]]


class QuantumTaskQueueInfoTypeDef(TypedDict):
    position: str
    queue: QueueNameType
    message: NotRequired[str]
    queuePriority: NotRequired[QueuePriorityType]


class JobSummaryTypeDef(TypedDict):
    createdAt: datetime
    device: str
    jobArn: str
    jobName: str
    status: JobPrimaryStatusType
    endedAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    tags: NotRequired[Dict[str, str]]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class QuantumTaskSummaryTypeDef(TypedDict):
    createdAt: datetime
    deviceArn: str
    outputS3Bucket: str
    outputS3Directory: str
    quantumTaskArn: str
    shots: int
    status: QuantumTaskStatusType
    endedAt: NotRequired[datetime]
    tags: NotRequired[Dict[str, str]]


class SearchDevicesFilterTypeDef(TypedDict):
    name: str
    values: Sequence[str]


SearchJobsFilterTypeDef = TypedDict(
    "SearchJobsFilterTypeDef",
    {
        "name": str,
        "operator": SearchJobsFilterOperatorType,
        "values": Sequence[str],
    },
)
SearchQuantumTasksFilterTypeDef = TypedDict(
    "SearchQuantumTasksFilterTypeDef",
    {
        "name": str,
        "operator": SearchQuantumTasksFilterOperatorType,
        "values": Sequence[str],
    },
)


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class AlgorithmSpecificationTypeDef(TypedDict):
    containerImage: NotRequired[ContainerImageTypeDef]
    scriptModeConfig: NotRequired[ScriptModeConfigTypeDef]


class CreateQuantumTaskRequestRequestTypeDef(TypedDict):
    action: str
    clientToken: str
    deviceArn: str
    outputS3Bucket: str
    outputS3KeyPrefix: str
    shots: int
    associations: NotRequired[Sequence[AssociationTypeDef]]
    deviceParameters: NotRequired[str]
    jobToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CancelJobResponseTypeDef(TypedDict):
    cancellationStatus: CancellationStatusType
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CancelQuantumTaskResponseTypeDef(TypedDict):
    cancellationStatus: CancellationStatusType
    quantumTaskArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateQuantumTaskResponseTypeDef(TypedDict):
    quantumTaskArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DataSourceTypeDef(TypedDict):
    s3DataSource: S3DataSourceTypeDef


class GetDeviceResponseTypeDef(TypedDict):
    deviceArn: str
    deviceCapabilities: str
    deviceName: str
    deviceQueueInfo: List[DeviceQueueInfoTypeDef]
    deviceStatus: DeviceStatusType
    deviceType: DeviceTypeType
    providerName: str
    ResponseMetadata: ResponseMetadataTypeDef


class SearchDevicesResponseTypeDef(TypedDict):
    devices: List[DeviceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetQuantumTaskResponseTypeDef(TypedDict):
    associations: List[AssociationTypeDef]
    createdAt: datetime
    deviceArn: str
    deviceParameters: str
    endedAt: datetime
    failureReason: str
    jobArn: str
    outputS3Bucket: str
    outputS3Directory: str
    quantumTaskArn: str
    queueInfo: QuantumTaskQueueInfoTypeDef
    shots: int
    status: QuantumTaskStatusType
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SearchJobsResponseTypeDef(TypedDict):
    jobs: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchQuantumTasksResponseTypeDef(TypedDict):
    quantumTasks: List[QuantumTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchDevicesRequestRequestTypeDef(TypedDict):
    filters: Sequence[SearchDevicesFilterTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchDevicesRequestSearchDevicesPaginateTypeDef(TypedDict):
    filters: Sequence[SearchDevicesFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchJobsRequestRequestTypeDef(TypedDict):
    filters: Sequence[SearchJobsFilterTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchJobsRequestSearchJobsPaginateTypeDef(TypedDict):
    filters: Sequence[SearchJobsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchQuantumTasksRequestRequestTypeDef(TypedDict):
    filters: Sequence[SearchQuantumTasksFilterTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef(TypedDict):
    filters: Sequence[SearchQuantumTasksFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class InputFileConfigTypeDef(TypedDict):
    channelName: str
    dataSource: DataSourceTypeDef
    contentType: NotRequired[str]


class CreateJobRequestRequestTypeDef(TypedDict):
    algorithmSpecification: AlgorithmSpecificationTypeDef
    clientToken: str
    deviceConfig: DeviceConfigTypeDef
    instanceConfig: InstanceConfigTypeDef
    jobName: str
    outputDataConfig: JobOutputDataConfigTypeDef
    roleArn: str
    associations: NotRequired[Sequence[AssociationTypeDef]]
    checkpointConfig: NotRequired[JobCheckpointConfigTypeDef]
    hyperParameters: NotRequired[Mapping[str, str]]
    inputDataConfig: NotRequired[Sequence[InputFileConfigTypeDef]]
    stoppingCondition: NotRequired[JobStoppingConditionTypeDef]
    tags: NotRequired[Mapping[str, str]]


class GetJobResponseTypeDef(TypedDict):
    algorithmSpecification: AlgorithmSpecificationTypeDef
    associations: List[AssociationTypeDef]
    billableDuration: int
    checkpointConfig: JobCheckpointConfigTypeDef
    createdAt: datetime
    deviceConfig: DeviceConfigTypeDef
    endedAt: datetime
    events: List[JobEventDetailsTypeDef]
    failureReason: str
    hyperParameters: Dict[str, str]
    inputDataConfig: List[InputFileConfigTypeDef]
    instanceConfig: InstanceConfigTypeDef
    jobArn: str
    jobName: str
    outputDataConfig: JobOutputDataConfigTypeDef
    queueInfo: HybridJobQueueInfoTypeDef
    roleArn: str
    startedAt: datetime
    status: JobPrimaryStatusType
    stoppingCondition: JobStoppingConditionTypeDef
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
