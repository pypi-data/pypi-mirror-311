"""
Type annotations for finspace service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/type_defs/)

Usage::

    ```python
    from mypy_boto3_finspace.type_defs import AutoScalingConfigurationTypeDef

    data: AutoScalingConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ChangesetStatusType,
    ChangeTypeType,
    DnsStatusType,
    EnvironmentStatusType,
    ErrorDetailsType,
    FederationModeType,
    KxAzModeType,
    KxClusterCodeDeploymentStrategyType,
    KxClusterStatusType,
    KxClusterTypeType,
    KxDataviewStatusType,
    KxDeploymentStrategyType,
    KxNAS1TypeType,
    KxNodeStatusType,
    KxScalingGroupStatusType,
    KxVolumeStatusType,
    RuleActionType,
    TgwStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AutoScalingConfigurationTypeDef",
    "CapacityConfigurationTypeDef",
    "ChangeRequestTypeDef",
    "CodeConfigurationTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "CreateKxChangesetRequestRequestTypeDef",
    "CreateKxChangesetResponseTypeDef",
    "CreateKxClusterRequestRequestTypeDef",
    "CreateKxClusterResponseTypeDef",
    "CreateKxDatabaseRequestRequestTypeDef",
    "CreateKxDatabaseResponseTypeDef",
    "CreateKxDataviewRequestRequestTypeDef",
    "CreateKxDataviewResponseTypeDef",
    "CreateKxEnvironmentRequestRequestTypeDef",
    "CreateKxEnvironmentResponseTypeDef",
    "CreateKxScalingGroupRequestRequestTypeDef",
    "CreateKxScalingGroupResponseTypeDef",
    "CreateKxUserRequestRequestTypeDef",
    "CreateKxUserResponseTypeDef",
    "CreateKxVolumeRequestRequestTypeDef",
    "CreateKxVolumeResponseTypeDef",
    "CustomDNSServerTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeleteKxClusterNodeRequestRequestTypeDef",
    "DeleteKxClusterRequestRequestTypeDef",
    "DeleteKxDatabaseRequestRequestTypeDef",
    "DeleteKxDataviewRequestRequestTypeDef",
    "DeleteKxEnvironmentRequestRequestTypeDef",
    "DeleteKxScalingGroupRequestRequestTypeDef",
    "DeleteKxUserRequestRequestTypeDef",
    "DeleteKxVolumeRequestRequestTypeDef",
    "EnvironmentTypeDef",
    "ErrorInfoTypeDef",
    "FederationParametersOutputTypeDef",
    "FederationParametersTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetEnvironmentResponseTypeDef",
    "GetKxChangesetRequestRequestTypeDef",
    "GetKxChangesetResponseTypeDef",
    "GetKxClusterRequestRequestTypeDef",
    "GetKxClusterResponseTypeDef",
    "GetKxConnectionStringRequestRequestTypeDef",
    "GetKxConnectionStringResponseTypeDef",
    "GetKxDatabaseRequestRequestTypeDef",
    "GetKxDatabaseResponseTypeDef",
    "GetKxDataviewRequestRequestTypeDef",
    "GetKxDataviewResponseTypeDef",
    "GetKxEnvironmentRequestRequestTypeDef",
    "GetKxEnvironmentResponseTypeDef",
    "GetKxScalingGroupRequestRequestTypeDef",
    "GetKxScalingGroupResponseTypeDef",
    "GetKxUserRequestRequestTypeDef",
    "GetKxUserResponseTypeDef",
    "GetKxVolumeRequestRequestTypeDef",
    "GetKxVolumeResponseTypeDef",
    "IcmpTypeCodeTypeDef",
    "KxAttachedClusterTypeDef",
    "KxCacheStorageConfigurationTypeDef",
    "KxChangesetListEntryTypeDef",
    "KxClusterCodeDeploymentConfigurationTypeDef",
    "KxClusterTypeDef",
    "KxCommandLineArgumentTypeDef",
    "KxDatabaseCacheConfigurationOutputTypeDef",
    "KxDatabaseCacheConfigurationTypeDef",
    "KxDatabaseCacheConfigurationUnionTypeDef",
    "KxDatabaseConfigurationOutputTypeDef",
    "KxDatabaseConfigurationTypeDef",
    "KxDatabaseConfigurationUnionTypeDef",
    "KxDatabaseListEntryTypeDef",
    "KxDataviewActiveVersionTypeDef",
    "KxDataviewConfigurationOutputTypeDef",
    "KxDataviewConfigurationTypeDef",
    "KxDataviewConfigurationUnionTypeDef",
    "KxDataviewListEntryTypeDef",
    "KxDataviewSegmentConfigurationOutputTypeDef",
    "KxDataviewSegmentConfigurationTypeDef",
    "KxDataviewSegmentConfigurationUnionTypeDef",
    "KxDeploymentConfigurationTypeDef",
    "KxEnvironmentTypeDef",
    "KxNAS1ConfigurationTypeDef",
    "KxNodeTypeDef",
    "KxSavedownStorageConfigurationTypeDef",
    "KxScalingGroupConfigurationTypeDef",
    "KxScalingGroupTypeDef",
    "KxUserTypeDef",
    "KxVolumeTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "ListKxChangesetsRequestRequestTypeDef",
    "ListKxChangesetsResponseTypeDef",
    "ListKxClusterNodesRequestRequestTypeDef",
    "ListKxClusterNodesResponseTypeDef",
    "ListKxClustersRequestRequestTypeDef",
    "ListKxClustersResponseTypeDef",
    "ListKxDatabasesRequestRequestTypeDef",
    "ListKxDatabasesResponseTypeDef",
    "ListKxDataviewsRequestRequestTypeDef",
    "ListKxDataviewsResponseTypeDef",
    "ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef",
    "ListKxEnvironmentsRequestRequestTypeDef",
    "ListKxEnvironmentsResponseTypeDef",
    "ListKxScalingGroupsRequestRequestTypeDef",
    "ListKxScalingGroupsResponseTypeDef",
    "ListKxUsersRequestRequestTypeDef",
    "ListKxUsersResponseTypeDef",
    "ListKxVolumesRequestRequestTypeDef",
    "ListKxVolumesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NetworkACLEntryTypeDef",
    "PaginatorConfigTypeDef",
    "PortRangeTypeDef",
    "ResponseMetadataTypeDef",
    "SuperuserParametersTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TickerplantLogConfigurationOutputTypeDef",
    "TickerplantLogConfigurationTypeDef",
    "TransitGatewayConfigurationOutputTypeDef",
    "TransitGatewayConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "UpdateEnvironmentResponseTypeDef",
    "UpdateKxClusterCodeConfigurationRequestRequestTypeDef",
    "UpdateKxClusterDatabasesRequestRequestTypeDef",
    "UpdateKxDatabaseRequestRequestTypeDef",
    "UpdateKxDatabaseResponseTypeDef",
    "UpdateKxDataviewRequestRequestTypeDef",
    "UpdateKxDataviewResponseTypeDef",
    "UpdateKxEnvironmentNetworkRequestRequestTypeDef",
    "UpdateKxEnvironmentNetworkResponseTypeDef",
    "UpdateKxEnvironmentRequestRequestTypeDef",
    "UpdateKxEnvironmentResponseTypeDef",
    "UpdateKxUserRequestRequestTypeDef",
    "UpdateKxUserResponseTypeDef",
    "UpdateKxVolumeRequestRequestTypeDef",
    "UpdateKxVolumeResponseTypeDef",
    "VolumeTypeDef",
    "VpcConfigurationOutputTypeDef",
    "VpcConfigurationTypeDef",
)

class AutoScalingConfigurationTypeDef(TypedDict):
    minNodeCount: NotRequired[int]
    maxNodeCount: NotRequired[int]
    autoScalingMetric: NotRequired[Literal["CPU_UTILIZATION_PERCENTAGE"]]
    metricTarget: NotRequired[float]
    scaleInCooldownSeconds: NotRequired[float]
    scaleOutCooldownSeconds: NotRequired[float]

class CapacityConfigurationTypeDef(TypedDict):
    nodeType: NotRequired[str]
    nodeCount: NotRequired[int]

class ChangeRequestTypeDef(TypedDict):
    changeType: ChangeTypeType
    dbPath: str
    s3Path: NotRequired[str]

class CodeConfigurationTypeDef(TypedDict):
    s3Bucket: NotRequired[str]
    s3Key: NotRequired[str]
    s3ObjectVersion: NotRequired[str]

class FederationParametersTypeDef(TypedDict):
    samlMetadataDocument: NotRequired[str]
    samlMetadataURL: NotRequired[str]
    applicationCallBackURL: NotRequired[str]
    federationURN: NotRequired[str]
    federationProviderName: NotRequired[str]
    attributeMap: NotRequired[Mapping[str, str]]

class SuperuserParametersTypeDef(TypedDict):
    emailAddress: str
    firstName: str
    lastName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ErrorInfoTypeDef(TypedDict):
    errorMessage: NotRequired[str]
    errorType: NotRequired[ErrorDetailsType]

KxCacheStorageConfigurationTypeDef = TypedDict(
    "KxCacheStorageConfigurationTypeDef",
    {
        "type": str,
        "size": int,
    },
)

class KxCommandLineArgumentTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

KxSavedownStorageConfigurationTypeDef = TypedDict(
    "KxSavedownStorageConfigurationTypeDef",
    {
        "type": NotRequired[Literal["SDS01"]],
        "size": NotRequired[int],
        "volumeName": NotRequired[str],
    },
)

class KxScalingGroupConfigurationTypeDef(TypedDict):
    scalingGroupName: str
    memoryReservation: int
    nodeCount: int
    memoryLimit: NotRequired[int]
    cpu: NotRequired[float]

class TickerplantLogConfigurationTypeDef(TypedDict):
    tickerplantLogVolumes: NotRequired[Sequence[str]]

class VpcConfigurationTypeDef(TypedDict):
    vpcId: NotRequired[str]
    securityGroupIds: NotRequired[Sequence[str]]
    subnetIds: NotRequired[Sequence[str]]
    ipAddressType: NotRequired[Literal["IP_V4"]]

class TickerplantLogConfigurationOutputTypeDef(TypedDict):
    tickerplantLogVolumes: NotRequired[List[str]]

class VolumeTypeDef(TypedDict):
    volumeName: NotRequired[str]
    volumeType: NotRequired[Literal["NAS_1"]]

class VpcConfigurationOutputTypeDef(TypedDict):
    vpcId: NotRequired[str]
    securityGroupIds: NotRequired[List[str]]
    subnetIds: NotRequired[List[str]]
    ipAddressType: NotRequired[Literal["IP_V4"]]

class CreateKxDatabaseRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    clientToken: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class KxDataviewSegmentConfigurationOutputTypeDef(TypedDict):
    dbPaths: List[str]
    volumeName: str
    onDemand: NotRequired[bool]

class CreateKxEnvironmentRequestRequestTypeDef(TypedDict):
    name: str
    kmsKeyId: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class CreateKxScalingGroupRequestRequestTypeDef(TypedDict):
    clientToken: str
    environmentId: str
    scalingGroupName: str
    hostType: str
    availabilityZoneId: str
    tags: NotRequired[Mapping[str, str]]

class CreateKxUserRequestRequestTypeDef(TypedDict):
    environmentId: str
    userName: str
    iamRole: str
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

KxNAS1ConfigurationTypeDef = TypedDict(
    "KxNAS1ConfigurationTypeDef",
    {
        "type": NotRequired[KxNAS1TypeType],
        "size": NotRequired[int],
    },
)

class CustomDNSServerTypeDef(TypedDict):
    customDNSServerName: str
    customDNSServerIP: str

class DeleteEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str

class DeleteKxClusterNodeRequestRequestTypeDef(TypedDict):
    environmentId: str
    clusterName: str
    nodeId: str

class DeleteKxClusterRequestRequestTypeDef(TypedDict):
    environmentId: str
    clusterName: str
    clientToken: NotRequired[str]

class DeleteKxDatabaseRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    clientToken: str

class DeleteKxDataviewRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    dataviewName: str
    clientToken: str

class DeleteKxEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str
    clientToken: NotRequired[str]

class DeleteKxScalingGroupRequestRequestTypeDef(TypedDict):
    environmentId: str
    scalingGroupName: str
    clientToken: NotRequired[str]

class DeleteKxUserRequestRequestTypeDef(TypedDict):
    userName: str
    environmentId: str
    clientToken: NotRequired[str]

class DeleteKxVolumeRequestRequestTypeDef(TypedDict):
    environmentId: str
    volumeName: str
    clientToken: NotRequired[str]

class FederationParametersOutputTypeDef(TypedDict):
    samlMetadataDocument: NotRequired[str]
    samlMetadataURL: NotRequired[str]
    applicationCallBackURL: NotRequired[str]
    federationURN: NotRequired[str]
    federationProviderName: NotRequired[str]
    attributeMap: NotRequired[Dict[str, str]]

class GetEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str

class GetKxChangesetRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    changesetId: str

class GetKxClusterRequestRequestTypeDef(TypedDict):
    environmentId: str
    clusterName: str

class GetKxConnectionStringRequestRequestTypeDef(TypedDict):
    userArn: str
    environmentId: str
    clusterName: str

class GetKxDatabaseRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str

class GetKxDataviewRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    dataviewName: str

class GetKxEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str

class GetKxScalingGroupRequestRequestTypeDef(TypedDict):
    environmentId: str
    scalingGroupName: str

class GetKxUserRequestRequestTypeDef(TypedDict):
    userName: str
    environmentId: str

class GetKxVolumeRequestRequestTypeDef(TypedDict):
    environmentId: str
    volumeName: str

class KxAttachedClusterTypeDef(TypedDict):
    clusterName: NotRequired[str]
    clusterType: NotRequired[KxClusterTypeType]
    clusterStatus: NotRequired[KxClusterStatusType]

IcmpTypeCodeTypeDef = TypedDict(
    "IcmpTypeCodeTypeDef",
    {
        "type": int,
        "code": int,
    },
)

class KxChangesetListEntryTypeDef(TypedDict):
    changesetId: NotRequired[str]
    createdTimestamp: NotRequired[datetime]
    activeFromTimestamp: NotRequired[datetime]
    lastModifiedTimestamp: NotRequired[datetime]
    status: NotRequired[ChangesetStatusType]

class KxClusterCodeDeploymentConfigurationTypeDef(TypedDict):
    deploymentStrategy: KxClusterCodeDeploymentStrategyType

class KxDatabaseCacheConfigurationOutputTypeDef(TypedDict):
    cacheType: str
    dbPaths: List[str]
    dataviewName: NotRequired[str]

class KxDatabaseCacheConfigurationTypeDef(TypedDict):
    cacheType: str
    dbPaths: Sequence[str]
    dataviewName: NotRequired[str]

class KxDatabaseListEntryTypeDef(TypedDict):
    databaseName: NotRequired[str]
    createdTimestamp: NotRequired[datetime]
    lastModifiedTimestamp: NotRequired[datetime]

class KxDataviewSegmentConfigurationTypeDef(TypedDict):
    dbPaths: Sequence[str]
    volumeName: str
    onDemand: NotRequired[bool]

class KxDeploymentConfigurationTypeDef(TypedDict):
    deploymentStrategy: KxDeploymentStrategyType

class KxNodeTypeDef(TypedDict):
    nodeId: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    launchTime: NotRequired[datetime]
    status: NotRequired[KxNodeStatusType]

class KxScalingGroupTypeDef(TypedDict):
    scalingGroupName: NotRequired[str]
    hostType: NotRequired[str]
    clusters: NotRequired[List[str]]
    availabilityZoneId: NotRequired[str]
    status: NotRequired[KxScalingGroupStatusType]
    statusReason: NotRequired[str]
    lastModifiedTimestamp: NotRequired[datetime]
    createdTimestamp: NotRequired[datetime]

class KxUserTypeDef(TypedDict):
    userArn: NotRequired[str]
    userName: NotRequired[str]
    iamRole: NotRequired[str]
    createTimestamp: NotRequired[datetime]
    updateTimestamp: NotRequired[datetime]

class KxVolumeTypeDef(TypedDict):
    volumeName: NotRequired[str]
    volumeType: NotRequired[Literal["NAS_1"]]
    status: NotRequired[KxVolumeStatusType]
    description: NotRequired[str]
    statusReason: NotRequired[str]
    azMode: NotRequired[KxAzModeType]
    availabilityZoneIds: NotRequired[List[str]]
    createdTimestamp: NotRequired[datetime]
    lastModifiedTimestamp: NotRequired[datetime]

class ListEnvironmentsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListKxChangesetsRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListKxClusterNodesRequestRequestTypeDef(TypedDict):
    environmentId: str
    clusterName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListKxClustersRequestRequestTypeDef(TypedDict):
    environmentId: str
    clusterType: NotRequired[KxClusterTypeType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListKxDatabasesRequestRequestTypeDef(TypedDict):
    environmentId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListKxDataviewsRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListKxEnvironmentsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListKxScalingGroupsRequestRequestTypeDef(TypedDict):
    environmentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListKxUsersRequestRequestTypeDef(TypedDict):
    environmentId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListKxVolumesRequestRequestTypeDef(TypedDict):
    environmentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    volumeType: NotRequired[Literal["NAS_1"]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "from": int,
        "to": int,
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateKxDatabaseRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    clientToken: str
    description: NotRequired[str]

class UpdateKxEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str
    name: NotRequired[str]
    description: NotRequired[str]
    clientToken: NotRequired[str]

class UpdateKxUserRequestRequestTypeDef(TypedDict):
    environmentId: str
    userName: str
    iamRole: str
    clientToken: NotRequired[str]

class CreateKxChangesetRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    changeRequests: Sequence[ChangeRequestTypeDef]
    clientToken: str

class UpdateEnvironmentRequestRequestTypeDef(TypedDict):
    environmentId: str
    name: NotRequired[str]
    description: NotRequired[str]
    federationMode: NotRequired[FederationModeType]
    federationParameters: NotRequired[FederationParametersTypeDef]

class CreateEnvironmentRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    federationMode: NotRequired[FederationModeType]
    federationParameters: NotRequired[FederationParametersTypeDef]
    superuserParameters: NotRequired[SuperuserParametersTypeDef]
    dataBundles: NotRequired[Sequence[str]]

class CreateEnvironmentResponseTypeDef(TypedDict):
    environmentId: str
    environmentArn: str
    environmentUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateKxDatabaseResponseTypeDef(TypedDict):
    databaseName: str
    databaseArn: str
    environmentId: str
    description: str
    createdTimestamp: datetime
    lastModifiedTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateKxEnvironmentResponseTypeDef(TypedDict):
    name: str
    status: EnvironmentStatusType
    environmentId: str
    description: str
    environmentArn: str
    kmsKeyId: str
    creationTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateKxScalingGroupResponseTypeDef(TypedDict):
    environmentId: str
    scalingGroupName: str
    hostType: str
    availabilityZoneId: str
    status: KxScalingGroupStatusType
    lastModifiedTimestamp: datetime
    createdTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateKxUserResponseTypeDef(TypedDict):
    userName: str
    userArn: str
    environmentId: str
    iamRole: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetKxConnectionStringResponseTypeDef(TypedDict):
    signedConnectionString: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetKxDatabaseResponseTypeDef(TypedDict):
    databaseName: str
    databaseArn: str
    environmentId: str
    description: str
    createdTimestamp: datetime
    lastModifiedTimestamp: datetime
    lastCompletedChangesetId: str
    numBytes: int
    numChangesets: int
    numFiles: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetKxScalingGroupResponseTypeDef(TypedDict):
    scalingGroupName: str
    scalingGroupArn: str
    hostType: str
    clusters: List[str]
    availabilityZoneId: str
    status: KxScalingGroupStatusType
    statusReason: str
    lastModifiedTimestamp: datetime
    createdTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetKxUserResponseTypeDef(TypedDict):
    userName: str
    userArn: str
    environmentId: str
    iamRole: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKxDatabaseResponseTypeDef(TypedDict):
    databaseName: str
    environmentId: str
    description: str
    lastModifiedTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKxUserResponseTypeDef(TypedDict):
    userName: str
    userArn: str
    environmentId: str
    iamRole: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateKxChangesetResponseTypeDef(TypedDict):
    changesetId: str
    databaseName: str
    environmentId: str
    changeRequests: List[ChangeRequestTypeDef]
    createdTimestamp: datetime
    lastModifiedTimestamp: datetime
    status: ChangesetStatusType
    errorInfo: ErrorInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetKxChangesetResponseTypeDef(TypedDict):
    changesetId: str
    databaseName: str
    environmentId: str
    changeRequests: List[ChangeRequestTypeDef]
    createdTimestamp: datetime
    activeFromTimestamp: datetime
    lastModifiedTimestamp: datetime
    status: ChangesetStatusType
    errorInfo: ErrorInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class KxClusterTypeDef(TypedDict):
    status: NotRequired[KxClusterStatusType]
    statusReason: NotRequired[str]
    clusterName: NotRequired[str]
    clusterType: NotRequired[KxClusterTypeType]
    clusterDescription: NotRequired[str]
    releaseLabel: NotRequired[str]
    volumes: NotRequired[List[VolumeTypeDef]]
    initializationScript: NotRequired[str]
    executionRole: NotRequired[str]
    azMode: NotRequired[KxAzModeType]
    availabilityZoneId: NotRequired[str]
    lastModifiedTimestamp: NotRequired[datetime]
    createdTimestamp: NotRequired[datetime]

class CreateKxDataviewResponseTypeDef(TypedDict):
    dataviewName: str
    databaseName: str
    environmentId: str
    azMode: KxAzModeType
    availabilityZoneId: str
    changesetId: str
    segmentConfigurations: List[KxDataviewSegmentConfigurationOutputTypeDef]
    description: str
    autoUpdate: bool
    readWrite: bool
    createdTimestamp: datetime
    lastModifiedTimestamp: datetime
    status: KxDataviewStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class KxDataviewActiveVersionTypeDef(TypedDict):
    changesetId: NotRequired[str]
    segmentConfigurations: NotRequired[List[KxDataviewSegmentConfigurationOutputTypeDef]]
    attachedClusters: NotRequired[List[str]]
    createdTimestamp: NotRequired[datetime]
    versionId: NotRequired[str]

class KxDataviewConfigurationOutputTypeDef(TypedDict):
    dataviewName: NotRequired[str]
    dataviewVersionId: NotRequired[str]
    changesetId: NotRequired[str]
    segmentConfigurations: NotRequired[List[KxDataviewSegmentConfigurationOutputTypeDef]]

class CreateKxVolumeRequestRequestTypeDef(TypedDict):
    environmentId: str
    volumeType: Literal["NAS_1"]
    volumeName: str
    azMode: KxAzModeType
    availabilityZoneIds: Sequence[str]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    nas1Configuration: NotRequired[KxNAS1ConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]

class CreateKxVolumeResponseTypeDef(TypedDict):
    environmentId: str
    volumeName: str
    volumeType: Literal["NAS_1"]
    volumeArn: str
    nas1Configuration: KxNAS1ConfigurationTypeDef
    status: KxVolumeStatusType
    statusReason: str
    azMode: KxAzModeType
    description: str
    availabilityZoneIds: List[str]
    createdTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKxVolumeRequestRequestTypeDef(TypedDict):
    environmentId: str
    volumeName: str
    description: NotRequired[str]
    clientToken: NotRequired[str]
    nas1Configuration: NotRequired[KxNAS1ConfigurationTypeDef]

class EnvironmentTypeDef(TypedDict):
    name: NotRequired[str]
    environmentId: NotRequired[str]
    awsAccountId: NotRequired[str]
    status: NotRequired[EnvironmentStatusType]
    environmentUrl: NotRequired[str]
    description: NotRequired[str]
    environmentArn: NotRequired[str]
    sageMakerStudioDomainUrl: NotRequired[str]
    kmsKeyId: NotRequired[str]
    dedicatedServiceAccountId: NotRequired[str]
    federationMode: NotRequired[FederationModeType]
    federationParameters: NotRequired[FederationParametersOutputTypeDef]

class GetKxVolumeResponseTypeDef(TypedDict):
    environmentId: str
    volumeName: str
    volumeType: Literal["NAS_1"]
    volumeArn: str
    nas1Configuration: KxNAS1ConfigurationTypeDef
    status: KxVolumeStatusType
    statusReason: str
    createdTimestamp: datetime
    description: str
    azMode: KxAzModeType
    availabilityZoneIds: List[str]
    lastModifiedTimestamp: datetime
    attachedClusters: List[KxAttachedClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKxVolumeResponseTypeDef(TypedDict):
    environmentId: str
    volumeName: str
    volumeType: Literal["NAS_1"]
    volumeArn: str
    nas1Configuration: KxNAS1ConfigurationTypeDef
    status: KxVolumeStatusType
    description: str
    statusReason: str
    createdTimestamp: datetime
    azMode: KxAzModeType
    availabilityZoneIds: List[str]
    lastModifiedTimestamp: datetime
    attachedClusters: List[KxAttachedClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListKxChangesetsResponseTypeDef(TypedDict):
    kxChangesets: List[KxChangesetListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateKxClusterCodeConfigurationRequestRequestTypeDef(TypedDict):
    environmentId: str
    clusterName: str
    code: CodeConfigurationTypeDef
    clientToken: NotRequired[str]
    initializationScript: NotRequired[str]
    commandLineArguments: NotRequired[Sequence[KxCommandLineArgumentTypeDef]]
    deploymentConfiguration: NotRequired[KxClusterCodeDeploymentConfigurationTypeDef]

KxDatabaseCacheConfigurationUnionTypeDef = Union[
    KxDatabaseCacheConfigurationTypeDef, KxDatabaseCacheConfigurationOutputTypeDef
]

class ListKxDatabasesResponseTypeDef(TypedDict):
    kxDatabases: List[KxDatabaseListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

KxDataviewSegmentConfigurationUnionTypeDef = Union[
    KxDataviewSegmentConfigurationTypeDef, KxDataviewSegmentConfigurationOutputTypeDef
]

class UpdateKxDataviewRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    dataviewName: str
    clientToken: str
    description: NotRequired[str]
    changesetId: NotRequired[str]
    segmentConfigurations: NotRequired[Sequence[KxDataviewSegmentConfigurationTypeDef]]

class ListKxClusterNodesResponseTypeDef(TypedDict):
    nodes: List[KxNodeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListKxScalingGroupsResponseTypeDef(TypedDict):
    scalingGroups: List[KxScalingGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListKxUsersResponseTypeDef(TypedDict):
    users: List[KxUserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListKxVolumesResponseTypeDef(TypedDict):
    kxVolumeSummaries: List[KxVolumeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class NetworkACLEntryTypeDef(TypedDict):
    ruleNumber: int
    protocol: str
    ruleAction: RuleActionType
    cidrBlock: str
    portRange: NotRequired[PortRangeTypeDef]
    icmpTypeCode: NotRequired[IcmpTypeCodeTypeDef]

class ListKxClustersResponseTypeDef(TypedDict):
    kxClusterSummaries: List[KxClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetKxDataviewResponseTypeDef(TypedDict):
    databaseName: str
    dataviewName: str
    azMode: KxAzModeType
    availabilityZoneId: str
    changesetId: str
    segmentConfigurations: List[KxDataviewSegmentConfigurationOutputTypeDef]
    activeVersions: List[KxDataviewActiveVersionTypeDef]
    description: str
    autoUpdate: bool
    readWrite: bool
    environmentId: str
    createdTimestamp: datetime
    lastModifiedTimestamp: datetime
    status: KxDataviewStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class KxDataviewListEntryTypeDef(TypedDict):
    environmentId: NotRequired[str]
    databaseName: NotRequired[str]
    dataviewName: NotRequired[str]
    azMode: NotRequired[KxAzModeType]
    availabilityZoneId: NotRequired[str]
    changesetId: NotRequired[str]
    segmentConfigurations: NotRequired[List[KxDataviewSegmentConfigurationOutputTypeDef]]
    activeVersions: NotRequired[List[KxDataviewActiveVersionTypeDef]]
    status: NotRequired[KxDataviewStatusType]
    description: NotRequired[str]
    autoUpdate: NotRequired[bool]
    readWrite: NotRequired[bool]
    createdTimestamp: NotRequired[datetime]
    lastModifiedTimestamp: NotRequired[datetime]
    statusReason: NotRequired[str]

class UpdateKxDataviewResponseTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    dataviewName: str
    azMode: KxAzModeType
    availabilityZoneId: str
    changesetId: str
    segmentConfigurations: List[KxDataviewSegmentConfigurationOutputTypeDef]
    activeVersions: List[KxDataviewActiveVersionTypeDef]
    status: KxDataviewStatusType
    autoUpdate: bool
    readWrite: bool
    description: str
    createdTimestamp: datetime
    lastModifiedTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class KxDatabaseConfigurationOutputTypeDef(TypedDict):
    databaseName: str
    cacheConfigurations: NotRequired[List[KxDatabaseCacheConfigurationOutputTypeDef]]
    changesetId: NotRequired[str]
    dataviewName: NotRequired[str]
    dataviewConfiguration: NotRequired[KxDataviewConfigurationOutputTypeDef]

class GetEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEnvironmentsResponseTypeDef(TypedDict):
    environments: List[EnvironmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateKxDataviewRequestRequestTypeDef(TypedDict):
    environmentId: str
    databaseName: str
    dataviewName: str
    azMode: KxAzModeType
    clientToken: str
    availabilityZoneId: NotRequired[str]
    changesetId: NotRequired[str]
    segmentConfigurations: NotRequired[Sequence[KxDataviewSegmentConfigurationUnionTypeDef]]
    autoUpdate: NotRequired[bool]
    readWrite: NotRequired[bool]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class KxDataviewConfigurationTypeDef(TypedDict):
    dataviewName: NotRequired[str]
    dataviewVersionId: NotRequired[str]
    changesetId: NotRequired[str]
    segmentConfigurations: NotRequired[Sequence[KxDataviewSegmentConfigurationUnionTypeDef]]

class TransitGatewayConfigurationOutputTypeDef(TypedDict):
    transitGatewayID: str
    routableCIDRSpace: str
    attachmentNetworkAclConfiguration: NotRequired[List[NetworkACLEntryTypeDef]]

class TransitGatewayConfigurationTypeDef(TypedDict):
    transitGatewayID: str
    routableCIDRSpace: str
    attachmentNetworkAclConfiguration: NotRequired[Sequence[NetworkACLEntryTypeDef]]

class ListKxDataviewsResponseTypeDef(TypedDict):
    kxDataviews: List[KxDataviewListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateKxClusterResponseTypeDef(TypedDict):
    environmentId: str
    status: KxClusterStatusType
    statusReason: str
    clusterName: str
    clusterType: KxClusterTypeType
    tickerplantLogConfiguration: TickerplantLogConfigurationOutputTypeDef
    volumes: List[VolumeTypeDef]
    databases: List[KxDatabaseConfigurationOutputTypeDef]
    cacheStorageConfigurations: List[KxCacheStorageConfigurationTypeDef]
    autoScalingConfiguration: AutoScalingConfigurationTypeDef
    clusterDescription: str
    capacityConfiguration: CapacityConfigurationTypeDef
    releaseLabel: str
    vpcConfiguration: VpcConfigurationOutputTypeDef
    initializationScript: str
    commandLineArguments: List[KxCommandLineArgumentTypeDef]
    code: CodeConfigurationTypeDef
    executionRole: str
    lastModifiedTimestamp: datetime
    savedownStorageConfiguration: KxSavedownStorageConfigurationTypeDef
    azMode: KxAzModeType
    availabilityZoneId: str
    createdTimestamp: datetime
    scalingGroupConfiguration: KxScalingGroupConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetKxClusterResponseTypeDef(TypedDict):
    status: KxClusterStatusType
    statusReason: str
    clusterName: str
    clusterType: KxClusterTypeType
    tickerplantLogConfiguration: TickerplantLogConfigurationOutputTypeDef
    volumes: List[VolumeTypeDef]
    databases: List[KxDatabaseConfigurationOutputTypeDef]
    cacheStorageConfigurations: List[KxCacheStorageConfigurationTypeDef]
    autoScalingConfiguration: AutoScalingConfigurationTypeDef
    clusterDescription: str
    capacityConfiguration: CapacityConfigurationTypeDef
    releaseLabel: str
    vpcConfiguration: VpcConfigurationOutputTypeDef
    initializationScript: str
    commandLineArguments: List[KxCommandLineArgumentTypeDef]
    code: CodeConfigurationTypeDef
    executionRole: str
    lastModifiedTimestamp: datetime
    savedownStorageConfiguration: KxSavedownStorageConfigurationTypeDef
    azMode: KxAzModeType
    availabilityZoneId: str
    createdTimestamp: datetime
    scalingGroupConfiguration: KxScalingGroupConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

KxDataviewConfigurationUnionTypeDef = Union[
    KxDataviewConfigurationTypeDef, KxDataviewConfigurationOutputTypeDef
]

class GetKxEnvironmentResponseTypeDef(TypedDict):
    name: str
    environmentId: str
    awsAccountId: str
    status: EnvironmentStatusType
    tgwStatus: TgwStatusType
    dnsStatus: DnsStatusType
    errorMessage: str
    description: str
    environmentArn: str
    kmsKeyId: str
    dedicatedServiceAccountId: str
    transitGatewayConfiguration: TransitGatewayConfigurationOutputTypeDef
    customDNSConfiguration: List[CustomDNSServerTypeDef]
    creationTimestamp: datetime
    updateTimestamp: datetime
    availabilityZoneIds: List[str]
    certificateAuthorityArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class KxEnvironmentTypeDef(TypedDict):
    name: NotRequired[str]
    environmentId: NotRequired[str]
    awsAccountId: NotRequired[str]
    status: NotRequired[EnvironmentStatusType]
    tgwStatus: NotRequired[TgwStatusType]
    dnsStatus: NotRequired[DnsStatusType]
    errorMessage: NotRequired[str]
    description: NotRequired[str]
    environmentArn: NotRequired[str]
    kmsKeyId: NotRequired[str]
    dedicatedServiceAccountId: NotRequired[str]
    transitGatewayConfiguration: NotRequired[TransitGatewayConfigurationOutputTypeDef]
    customDNSConfiguration: NotRequired[List[CustomDNSServerTypeDef]]
    creationTimestamp: NotRequired[datetime]
    updateTimestamp: NotRequired[datetime]
    availabilityZoneIds: NotRequired[List[str]]
    certificateAuthorityArn: NotRequired[str]

class UpdateKxEnvironmentNetworkResponseTypeDef(TypedDict):
    name: str
    environmentId: str
    awsAccountId: str
    status: EnvironmentStatusType
    tgwStatus: TgwStatusType
    dnsStatus: DnsStatusType
    errorMessage: str
    description: str
    environmentArn: str
    kmsKeyId: str
    dedicatedServiceAccountId: str
    transitGatewayConfiguration: TransitGatewayConfigurationOutputTypeDef
    customDNSConfiguration: List[CustomDNSServerTypeDef]
    creationTimestamp: datetime
    updateTimestamp: datetime
    availabilityZoneIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKxEnvironmentResponseTypeDef(TypedDict):
    name: str
    environmentId: str
    awsAccountId: str
    status: EnvironmentStatusType
    tgwStatus: TgwStatusType
    dnsStatus: DnsStatusType
    errorMessage: str
    description: str
    environmentArn: str
    kmsKeyId: str
    dedicatedServiceAccountId: str
    transitGatewayConfiguration: TransitGatewayConfigurationOutputTypeDef
    customDNSConfiguration: List[CustomDNSServerTypeDef]
    creationTimestamp: datetime
    updateTimestamp: datetime
    availabilityZoneIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKxEnvironmentNetworkRequestRequestTypeDef(TypedDict):
    environmentId: str
    transitGatewayConfiguration: NotRequired[TransitGatewayConfigurationTypeDef]
    customDNSConfiguration: NotRequired[Sequence[CustomDNSServerTypeDef]]
    clientToken: NotRequired[str]

class KxDatabaseConfigurationTypeDef(TypedDict):
    databaseName: str
    cacheConfigurations: NotRequired[Sequence[KxDatabaseCacheConfigurationUnionTypeDef]]
    changesetId: NotRequired[str]
    dataviewName: NotRequired[str]
    dataviewConfiguration: NotRequired[KxDataviewConfigurationUnionTypeDef]

class ListKxEnvironmentsResponseTypeDef(TypedDict):
    environments: List[KxEnvironmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

KxDatabaseConfigurationUnionTypeDef = Union[
    KxDatabaseConfigurationTypeDef, KxDatabaseConfigurationOutputTypeDef
]

class UpdateKxClusterDatabasesRequestRequestTypeDef(TypedDict):
    environmentId: str
    clusterName: str
    databases: Sequence[KxDatabaseConfigurationTypeDef]
    clientToken: NotRequired[str]
    deploymentConfiguration: NotRequired[KxDeploymentConfigurationTypeDef]

class CreateKxClusterRequestRequestTypeDef(TypedDict):
    environmentId: str
    clusterName: str
    clusterType: KxClusterTypeType
    releaseLabel: str
    vpcConfiguration: VpcConfigurationTypeDef
    azMode: KxAzModeType
    clientToken: NotRequired[str]
    tickerplantLogConfiguration: NotRequired[TickerplantLogConfigurationTypeDef]
    databases: NotRequired[Sequence[KxDatabaseConfigurationUnionTypeDef]]
    cacheStorageConfigurations: NotRequired[Sequence[KxCacheStorageConfigurationTypeDef]]
    autoScalingConfiguration: NotRequired[AutoScalingConfigurationTypeDef]
    clusterDescription: NotRequired[str]
    capacityConfiguration: NotRequired[CapacityConfigurationTypeDef]
    initializationScript: NotRequired[str]
    commandLineArguments: NotRequired[Sequence[KxCommandLineArgumentTypeDef]]
    code: NotRequired[CodeConfigurationTypeDef]
    executionRole: NotRequired[str]
    savedownStorageConfiguration: NotRequired[KxSavedownStorageConfigurationTypeDef]
    availabilityZoneId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    scalingGroupConfiguration: NotRequired[KxScalingGroupConfigurationTypeDef]
