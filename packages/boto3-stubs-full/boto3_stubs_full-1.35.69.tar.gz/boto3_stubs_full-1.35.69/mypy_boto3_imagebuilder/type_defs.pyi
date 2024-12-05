"""
Type annotations for imagebuilder service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/type_defs/)

Usage::

    ```python
    from mypy_boto3_imagebuilder.type_defs import SeverityCountsTypeDef

    data: SeverityCountsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    BuildTypeType,
    ComponentTypeType,
    DiskImageFormatType,
    EbsVolumeTypeType,
    ImageScanStatusType,
    ImageSourceType,
    ImageStatusType,
    ImageTypeType,
    LifecycleExecutionResourceActionNameType,
    LifecycleExecutionResourceStatusType,
    LifecycleExecutionStatusType,
    LifecyclePolicyDetailActionTypeType,
    LifecyclePolicyDetailFilterTypeType,
    LifecyclePolicyResourceTypeType,
    LifecyclePolicyStatusType,
    LifecyclePolicyTimeUnitType,
    OnWorkflowFailureType,
    OwnershipType,
    PipelineExecutionStartConditionType,
    PipelineStatusType,
    PlatformType,
    ResourceStatusType,
    TenancyTypeType,
    WorkflowExecutionStatusType,
    WorkflowStepActionTypeType,
    WorkflowStepExecutionRollbackStatusType,
    WorkflowStepExecutionStatusType,
    WorkflowTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountAggregationTypeDef",
    "AdditionalInstanceConfigurationTypeDef",
    "AmiDistributionConfigurationOutputTypeDef",
    "AmiDistributionConfigurationTypeDef",
    "AmiDistributionConfigurationUnionTypeDef",
    "AmiTypeDef",
    "CancelImageCreationRequestRequestTypeDef",
    "CancelImageCreationResponseTypeDef",
    "CancelLifecycleExecutionRequestRequestTypeDef",
    "CancelLifecycleExecutionResponseTypeDef",
    "ComponentConfigurationOutputTypeDef",
    "ComponentConfigurationTypeDef",
    "ComponentConfigurationUnionTypeDef",
    "ComponentParameterDetailTypeDef",
    "ComponentParameterOutputTypeDef",
    "ComponentParameterTypeDef",
    "ComponentParameterUnionTypeDef",
    "ComponentStateTypeDef",
    "ComponentSummaryTypeDef",
    "ComponentTypeDef",
    "ComponentVersionTypeDef",
    "ContainerDistributionConfigurationOutputTypeDef",
    "ContainerDistributionConfigurationTypeDef",
    "ContainerDistributionConfigurationUnionTypeDef",
    "ContainerRecipeSummaryTypeDef",
    "ContainerRecipeTypeDef",
    "ContainerTypeDef",
    "CreateComponentRequestRequestTypeDef",
    "CreateComponentResponseTypeDef",
    "CreateContainerRecipeRequestRequestTypeDef",
    "CreateContainerRecipeResponseTypeDef",
    "CreateDistributionConfigurationRequestRequestTypeDef",
    "CreateDistributionConfigurationResponseTypeDef",
    "CreateImagePipelineRequestRequestTypeDef",
    "CreateImagePipelineResponseTypeDef",
    "CreateImageRecipeRequestRequestTypeDef",
    "CreateImageRecipeResponseTypeDef",
    "CreateImageRequestRequestTypeDef",
    "CreateImageResponseTypeDef",
    "CreateInfrastructureConfigurationRequestRequestTypeDef",
    "CreateInfrastructureConfigurationResponseTypeDef",
    "CreateLifecyclePolicyRequestRequestTypeDef",
    "CreateLifecyclePolicyResponseTypeDef",
    "CreateWorkflowRequestRequestTypeDef",
    "CreateWorkflowResponseTypeDef",
    "CvssScoreAdjustmentTypeDef",
    "CvssScoreDetailsTypeDef",
    "CvssScoreTypeDef",
    "DeleteComponentRequestRequestTypeDef",
    "DeleteComponentResponseTypeDef",
    "DeleteContainerRecipeRequestRequestTypeDef",
    "DeleteContainerRecipeResponseTypeDef",
    "DeleteDistributionConfigurationRequestRequestTypeDef",
    "DeleteDistributionConfigurationResponseTypeDef",
    "DeleteImagePipelineRequestRequestTypeDef",
    "DeleteImagePipelineResponseTypeDef",
    "DeleteImageRecipeRequestRequestTypeDef",
    "DeleteImageRecipeResponseTypeDef",
    "DeleteImageRequestRequestTypeDef",
    "DeleteImageResponseTypeDef",
    "DeleteInfrastructureConfigurationRequestRequestTypeDef",
    "DeleteInfrastructureConfigurationResponseTypeDef",
    "DeleteLifecyclePolicyRequestRequestTypeDef",
    "DeleteLifecyclePolicyResponseTypeDef",
    "DeleteWorkflowRequestRequestTypeDef",
    "DeleteWorkflowResponseTypeDef",
    "DistributionConfigurationSummaryTypeDef",
    "DistributionConfigurationTypeDef",
    "DistributionOutputTypeDef",
    "DistributionTypeDef",
    "DistributionUnionTypeDef",
    "EbsInstanceBlockDeviceSpecificationTypeDef",
    "EcrConfigurationOutputTypeDef",
    "EcrConfigurationTypeDef",
    "EcrConfigurationUnionTypeDef",
    "FastLaunchConfigurationTypeDef",
    "FastLaunchLaunchTemplateSpecificationTypeDef",
    "FastLaunchSnapshotConfigurationTypeDef",
    "FilterTypeDef",
    "GetComponentPolicyRequestRequestTypeDef",
    "GetComponentPolicyResponseTypeDef",
    "GetComponentRequestRequestTypeDef",
    "GetComponentResponseTypeDef",
    "GetContainerRecipePolicyRequestRequestTypeDef",
    "GetContainerRecipePolicyResponseTypeDef",
    "GetContainerRecipeRequestRequestTypeDef",
    "GetContainerRecipeResponseTypeDef",
    "GetDistributionConfigurationRequestRequestTypeDef",
    "GetDistributionConfigurationResponseTypeDef",
    "GetImagePipelineRequestRequestTypeDef",
    "GetImagePipelineResponseTypeDef",
    "GetImagePolicyRequestRequestTypeDef",
    "GetImagePolicyResponseTypeDef",
    "GetImageRecipePolicyRequestRequestTypeDef",
    "GetImageRecipePolicyResponseTypeDef",
    "GetImageRecipeRequestRequestTypeDef",
    "GetImageRecipeResponseTypeDef",
    "GetImageRequestRequestTypeDef",
    "GetImageResponseTypeDef",
    "GetInfrastructureConfigurationRequestRequestTypeDef",
    "GetInfrastructureConfigurationResponseTypeDef",
    "GetLifecycleExecutionRequestRequestTypeDef",
    "GetLifecycleExecutionResponseTypeDef",
    "GetLifecyclePolicyRequestRequestTypeDef",
    "GetLifecyclePolicyResponseTypeDef",
    "GetWorkflowExecutionRequestRequestTypeDef",
    "GetWorkflowExecutionResponseTypeDef",
    "GetWorkflowRequestRequestTypeDef",
    "GetWorkflowResponseTypeDef",
    "GetWorkflowStepExecutionRequestRequestTypeDef",
    "GetWorkflowStepExecutionResponseTypeDef",
    "ImageAggregationTypeDef",
    "ImagePackageTypeDef",
    "ImagePipelineAggregationTypeDef",
    "ImagePipelineTypeDef",
    "ImageRecipeSummaryTypeDef",
    "ImageRecipeTypeDef",
    "ImageScanFindingAggregationTypeDef",
    "ImageScanFindingTypeDef",
    "ImageScanFindingsFilterTypeDef",
    "ImageScanStateTypeDef",
    "ImageScanningConfigurationOutputTypeDef",
    "ImageScanningConfigurationTypeDef",
    "ImageStateTypeDef",
    "ImageSummaryTypeDef",
    "ImageTestsConfigurationTypeDef",
    "ImageTypeDef",
    "ImageVersionTypeDef",
    "ImportComponentRequestRequestTypeDef",
    "ImportComponentResponseTypeDef",
    "ImportVmImageRequestRequestTypeDef",
    "ImportVmImageResponseTypeDef",
    "InfrastructureConfigurationSummaryTypeDef",
    "InfrastructureConfigurationTypeDef",
    "InspectorScoreDetailsTypeDef",
    "InstanceBlockDeviceMappingTypeDef",
    "InstanceConfigurationOutputTypeDef",
    "InstanceConfigurationTypeDef",
    "InstanceMetadataOptionsTypeDef",
    "LaunchPermissionConfigurationOutputTypeDef",
    "LaunchPermissionConfigurationTypeDef",
    "LaunchPermissionConfigurationUnionTypeDef",
    "LaunchTemplateConfigurationTypeDef",
    "LifecycleExecutionResourceActionTypeDef",
    "LifecycleExecutionResourceStateTypeDef",
    "LifecycleExecutionResourceTypeDef",
    "LifecycleExecutionResourcesImpactedSummaryTypeDef",
    "LifecycleExecutionSnapshotResourceTypeDef",
    "LifecycleExecutionStateTypeDef",
    "LifecycleExecutionTypeDef",
    "LifecyclePolicyDetailActionIncludeResourcesTypeDef",
    "LifecyclePolicyDetailActionTypeDef",
    "LifecyclePolicyDetailExclusionRulesAmisLastLaunchedTypeDef",
    "LifecyclePolicyDetailExclusionRulesAmisOutputTypeDef",
    "LifecyclePolicyDetailExclusionRulesAmisTypeDef",
    "LifecyclePolicyDetailExclusionRulesAmisUnionTypeDef",
    "LifecyclePolicyDetailExclusionRulesOutputTypeDef",
    "LifecyclePolicyDetailExclusionRulesTypeDef",
    "LifecyclePolicyDetailExclusionRulesUnionTypeDef",
    "LifecyclePolicyDetailFilterTypeDef",
    "LifecyclePolicyDetailOutputTypeDef",
    "LifecyclePolicyDetailTypeDef",
    "LifecyclePolicyDetailUnionTypeDef",
    "LifecyclePolicyResourceSelectionOutputTypeDef",
    "LifecyclePolicyResourceSelectionRecipeTypeDef",
    "LifecyclePolicyResourceSelectionTypeDef",
    "LifecyclePolicySummaryTypeDef",
    "LifecyclePolicyTypeDef",
    "ListComponentBuildVersionsRequestRequestTypeDef",
    "ListComponentBuildVersionsResponseTypeDef",
    "ListComponentsRequestRequestTypeDef",
    "ListComponentsResponseTypeDef",
    "ListContainerRecipesRequestRequestTypeDef",
    "ListContainerRecipesResponseTypeDef",
    "ListDistributionConfigurationsRequestRequestTypeDef",
    "ListDistributionConfigurationsResponseTypeDef",
    "ListImageBuildVersionsRequestRequestTypeDef",
    "ListImageBuildVersionsResponseTypeDef",
    "ListImagePackagesRequestRequestTypeDef",
    "ListImagePackagesResponseTypeDef",
    "ListImagePipelineImagesRequestRequestTypeDef",
    "ListImagePipelineImagesResponseTypeDef",
    "ListImagePipelinesRequestRequestTypeDef",
    "ListImagePipelinesResponseTypeDef",
    "ListImageRecipesRequestRequestTypeDef",
    "ListImageRecipesResponseTypeDef",
    "ListImageScanFindingAggregationsRequestRequestTypeDef",
    "ListImageScanFindingAggregationsResponseTypeDef",
    "ListImageScanFindingsRequestRequestTypeDef",
    "ListImageScanFindingsResponseTypeDef",
    "ListImagesRequestRequestTypeDef",
    "ListImagesResponseTypeDef",
    "ListInfrastructureConfigurationsRequestRequestTypeDef",
    "ListInfrastructureConfigurationsResponseTypeDef",
    "ListLifecycleExecutionResourcesRequestRequestTypeDef",
    "ListLifecycleExecutionResourcesResponseTypeDef",
    "ListLifecycleExecutionsRequestRequestTypeDef",
    "ListLifecycleExecutionsResponseTypeDef",
    "ListLifecyclePoliciesRequestRequestTypeDef",
    "ListLifecyclePoliciesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWaitingWorkflowStepsRequestRequestTypeDef",
    "ListWaitingWorkflowStepsResponseTypeDef",
    "ListWorkflowBuildVersionsRequestRequestTypeDef",
    "ListWorkflowBuildVersionsResponseTypeDef",
    "ListWorkflowExecutionsRequestRequestTypeDef",
    "ListWorkflowExecutionsResponseTypeDef",
    "ListWorkflowStepExecutionsRequestRequestTypeDef",
    "ListWorkflowStepExecutionsResponseTypeDef",
    "ListWorkflowsRequestRequestTypeDef",
    "ListWorkflowsResponseTypeDef",
    "LoggingTypeDef",
    "OutputResourcesTypeDef",
    "PackageVulnerabilityDetailsTypeDef",
    "PlacementTypeDef",
    "PutComponentPolicyRequestRequestTypeDef",
    "PutComponentPolicyResponseTypeDef",
    "PutContainerRecipePolicyRequestRequestTypeDef",
    "PutContainerRecipePolicyResponseTypeDef",
    "PutImagePolicyRequestRequestTypeDef",
    "PutImagePolicyResponseTypeDef",
    "PutImageRecipePolicyRequestRequestTypeDef",
    "PutImageRecipePolicyResponseTypeDef",
    "RemediationRecommendationTypeDef",
    "RemediationTypeDef",
    "ResourceStateTypeDef",
    "ResourceStateUpdateExclusionRulesTypeDef",
    "ResourceStateUpdateIncludeResourcesTypeDef",
    "ResponseMetadataTypeDef",
    "S3ExportConfigurationTypeDef",
    "S3LogsTypeDef",
    "ScheduleTypeDef",
    "SendWorkflowStepActionRequestRequestTypeDef",
    "SendWorkflowStepActionResponseTypeDef",
    "SeverityCountsTypeDef",
    "StartImagePipelineExecutionRequestRequestTypeDef",
    "StartImagePipelineExecutionResponseTypeDef",
    "StartResourceStateUpdateRequestRequestTypeDef",
    "StartResourceStateUpdateResponseTypeDef",
    "SystemsManagerAgentTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TargetContainerRepositoryTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDistributionConfigurationRequestRequestTypeDef",
    "UpdateDistributionConfigurationResponseTypeDef",
    "UpdateImagePipelineRequestRequestTypeDef",
    "UpdateImagePipelineResponseTypeDef",
    "UpdateInfrastructureConfigurationRequestRequestTypeDef",
    "UpdateInfrastructureConfigurationResponseTypeDef",
    "UpdateLifecyclePolicyRequestRequestTypeDef",
    "UpdateLifecyclePolicyResponseTypeDef",
    "VulnerabilityIdAggregationTypeDef",
    "VulnerablePackageTypeDef",
    "WorkflowConfigurationOutputTypeDef",
    "WorkflowConfigurationTypeDef",
    "WorkflowConfigurationUnionTypeDef",
    "WorkflowExecutionMetadataTypeDef",
    "WorkflowParameterDetailTypeDef",
    "WorkflowParameterOutputTypeDef",
    "WorkflowParameterTypeDef",
    "WorkflowParameterUnionTypeDef",
    "WorkflowStateTypeDef",
    "WorkflowStepExecutionTypeDef",
    "WorkflowStepMetadataTypeDef",
    "WorkflowSummaryTypeDef",
    "WorkflowTypeDef",
    "WorkflowVersionTypeDef",
)

SeverityCountsTypeDef = TypedDict(
    "SeverityCountsTypeDef",
    {
        "all": NotRequired[int],
        "critical": NotRequired[int],
        "high": NotRequired[int],
        "medium": NotRequired[int],
    },
)

class SystemsManagerAgentTypeDef(TypedDict):
    uninstallAfterBuild: NotRequired[bool]

class LaunchPermissionConfigurationOutputTypeDef(TypedDict):
    userIds: NotRequired[List[str]]
    userGroups: NotRequired[List[str]]
    organizationArns: NotRequired[List[str]]
    organizationalUnitArns: NotRequired[List[str]]

class ImageStateTypeDef(TypedDict):
    status: NotRequired[ImageStatusType]
    reason: NotRequired[str]

class CancelImageCreationRequestRequestTypeDef(TypedDict):
    imageBuildVersionArn: str
    clientToken: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CancelLifecycleExecutionRequestRequestTypeDef(TypedDict):
    lifecycleExecutionId: str
    clientToken: str

class ComponentParameterOutputTypeDef(TypedDict):
    name: str
    value: List[str]

ComponentParameterDetailTypeDef = TypedDict(
    "ComponentParameterDetailTypeDef",
    {
        "name": str,
        "type": str,
        "defaultValue": NotRequired[List[str]],
        "description": NotRequired[str],
    },
)

class ComponentParameterTypeDef(TypedDict):
    name: str
    value: Sequence[str]

class ComponentStateTypeDef(TypedDict):
    status: NotRequired[Literal["DEPRECATED"]]
    reason: NotRequired[str]

ComponentVersionTypeDef = TypedDict(
    "ComponentVersionTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "version": NotRequired[str],
        "description": NotRequired[str],
        "platform": NotRequired[PlatformType],
        "supportedOsVersions": NotRequired[List[str]],
        "type": NotRequired[ComponentTypeType],
        "owner": NotRequired[str],
        "dateCreated": NotRequired[str],
    },
)

class TargetContainerRepositoryTypeDef(TypedDict):
    service: Literal["ECR"]
    repositoryName: str

class ContainerRecipeSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    containerType: NotRequired[Literal["DOCKER"]]
    name: NotRequired[str]
    platform: NotRequired[PlatformType]
    owner: NotRequired[str]
    parentImage: NotRequired[str]
    dateCreated: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class ContainerTypeDef(TypedDict):
    region: NotRequired[str]
    imageUris: NotRequired[List[str]]

class CreateComponentRequestRequestTypeDef(TypedDict):
    name: str
    semanticVersion: str
    platform: PlatformType
    clientToken: str
    description: NotRequired[str]
    changeDescription: NotRequired[str]
    supportedOsVersions: NotRequired[Sequence[str]]
    data: NotRequired[str]
    uri: NotRequired[str]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ImageTestsConfigurationTypeDef(TypedDict):
    imageTestsEnabled: NotRequired[bool]
    timeoutMinutes: NotRequired[int]

class ScheduleTypeDef(TypedDict):
    scheduleExpression: NotRequired[str]
    timezone: NotRequired[str]
    pipelineExecutionStartCondition: NotRequired[PipelineExecutionStartConditionType]

class InstanceMetadataOptionsTypeDef(TypedDict):
    httpTokens: NotRequired[str]
    httpPutResponseHopLimit: NotRequired[int]

class PlacementTypeDef(TypedDict):
    availabilityZone: NotRequired[str]
    tenancy: NotRequired[TenancyTypeType]
    hostId: NotRequired[str]
    hostResourceGroupArn: NotRequired[str]

CreateWorkflowRequestRequestTypeDef = TypedDict(
    "CreateWorkflowRequestRequestTypeDef",
    {
        "name": str,
        "semanticVersion": str,
        "clientToken": str,
        "type": WorkflowTypeType,
        "description": NotRequired[str],
        "changeDescription": NotRequired[str],
        "data": NotRequired[str],
        "uri": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

class CvssScoreAdjustmentTypeDef(TypedDict):
    metric: NotRequired[str]
    reason: NotRequired[str]

class CvssScoreTypeDef(TypedDict):
    baseScore: NotRequired[float]
    scoringVector: NotRequired[str]
    version: NotRequired[str]
    source: NotRequired[str]

class DeleteComponentRequestRequestTypeDef(TypedDict):
    componentBuildVersionArn: str

class DeleteContainerRecipeRequestRequestTypeDef(TypedDict):
    containerRecipeArn: str

class DeleteDistributionConfigurationRequestRequestTypeDef(TypedDict):
    distributionConfigurationArn: str

class DeleteImagePipelineRequestRequestTypeDef(TypedDict):
    imagePipelineArn: str

class DeleteImageRecipeRequestRequestTypeDef(TypedDict):
    imageRecipeArn: str

class DeleteImageRequestRequestTypeDef(TypedDict):
    imageBuildVersionArn: str

class DeleteInfrastructureConfigurationRequestRequestTypeDef(TypedDict):
    infrastructureConfigurationArn: str

class DeleteLifecyclePolicyRequestRequestTypeDef(TypedDict):
    lifecyclePolicyArn: str

class DeleteWorkflowRequestRequestTypeDef(TypedDict):
    workflowBuildVersionArn: str

class DistributionConfigurationSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    dateCreated: NotRequired[str]
    dateUpdated: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    regions: NotRequired[List[str]]

class LaunchTemplateConfigurationTypeDef(TypedDict):
    launchTemplateId: str
    accountId: NotRequired[str]
    setDefaultVersion: NotRequired[bool]

class S3ExportConfigurationTypeDef(TypedDict):
    roleName: str
    diskImageFormat: DiskImageFormatType
    s3Bucket: str
    s3Prefix: NotRequired[str]

class EbsInstanceBlockDeviceSpecificationTypeDef(TypedDict):
    encrypted: NotRequired[bool]
    deleteOnTermination: NotRequired[bool]
    iops: NotRequired[int]
    kmsKeyId: NotRequired[str]
    snapshotId: NotRequired[str]
    volumeSize: NotRequired[int]
    volumeType: NotRequired[EbsVolumeTypeType]
    throughput: NotRequired[int]

class EcrConfigurationOutputTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    containerTags: NotRequired[List[str]]

class EcrConfigurationTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    containerTags: NotRequired[Sequence[str]]

class FastLaunchLaunchTemplateSpecificationTypeDef(TypedDict):
    launchTemplateId: NotRequired[str]
    launchTemplateName: NotRequired[str]
    launchTemplateVersion: NotRequired[str]

class FastLaunchSnapshotConfigurationTypeDef(TypedDict):
    targetResourceCount: NotRequired[int]

class FilterTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[Sequence[str]]

class GetComponentPolicyRequestRequestTypeDef(TypedDict):
    componentArn: str

class GetComponentRequestRequestTypeDef(TypedDict):
    componentBuildVersionArn: str

class GetContainerRecipePolicyRequestRequestTypeDef(TypedDict):
    containerRecipeArn: str

class GetContainerRecipeRequestRequestTypeDef(TypedDict):
    containerRecipeArn: str

class GetDistributionConfigurationRequestRequestTypeDef(TypedDict):
    distributionConfigurationArn: str

class GetImagePipelineRequestRequestTypeDef(TypedDict):
    imagePipelineArn: str

class GetImagePolicyRequestRequestTypeDef(TypedDict):
    imageArn: str

class GetImageRecipePolicyRequestRequestTypeDef(TypedDict):
    imageRecipeArn: str

class GetImageRecipeRequestRequestTypeDef(TypedDict):
    imageRecipeArn: str

class GetImageRequestRequestTypeDef(TypedDict):
    imageBuildVersionArn: str

class GetInfrastructureConfigurationRequestRequestTypeDef(TypedDict):
    infrastructureConfigurationArn: str

class GetLifecycleExecutionRequestRequestTypeDef(TypedDict):
    lifecycleExecutionId: str

class GetLifecyclePolicyRequestRequestTypeDef(TypedDict):
    lifecyclePolicyArn: str

class GetWorkflowExecutionRequestRequestTypeDef(TypedDict):
    workflowExecutionId: str

class GetWorkflowRequestRequestTypeDef(TypedDict):
    workflowBuildVersionArn: str

class GetWorkflowStepExecutionRequestRequestTypeDef(TypedDict):
    stepExecutionId: str

class ImagePackageTypeDef(TypedDict):
    packageName: NotRequired[str]
    packageVersion: NotRequired[str]

class ImageRecipeSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    platform: NotRequired[PlatformType]
    owner: NotRequired[str]
    parentImage: NotRequired[str]
    dateCreated: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class ImageScanFindingsFilterTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[Sequence[str]]

class ImageScanStateTypeDef(TypedDict):
    status: NotRequired[ImageScanStatusType]
    reason: NotRequired[str]

ImageVersionTypeDef = TypedDict(
    "ImageVersionTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[ImageTypeType],
        "version": NotRequired[str],
        "platform": NotRequired[PlatformType],
        "osVersion": NotRequired[str],
        "owner": NotRequired[str],
        "dateCreated": NotRequired[str],
        "buildType": NotRequired[BuildTypeType],
        "imageSource": NotRequired[ImageSourceType],
    },
)
ImportComponentRequestRequestTypeDef = TypedDict(
    "ImportComponentRequestRequestTypeDef",
    {
        "name": str,
        "semanticVersion": str,
        "type": ComponentTypeType,
        "format": Literal["SHELL"],
        "platform": PlatformType,
        "clientToken": str,
        "description": NotRequired[str],
        "changeDescription": NotRequired[str],
        "data": NotRequired[str],
        "uri": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

class ImportVmImageRequestRequestTypeDef(TypedDict):
    name: str
    semanticVersion: str
    platform: PlatformType
    vmImportTaskId: str
    clientToken: str
    description: NotRequired[str]
    osVersion: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class LaunchPermissionConfigurationTypeDef(TypedDict):
    userIds: NotRequired[Sequence[str]]
    userGroups: NotRequired[Sequence[str]]
    organizationArns: NotRequired[Sequence[str]]
    organizationalUnitArns: NotRequired[Sequence[str]]

class LifecycleExecutionResourceActionTypeDef(TypedDict):
    name: NotRequired[LifecycleExecutionResourceActionNameType]
    reason: NotRequired[str]

class LifecycleExecutionResourceStateTypeDef(TypedDict):
    status: NotRequired[LifecycleExecutionResourceStatusType]
    reason: NotRequired[str]

class LifecycleExecutionResourcesImpactedSummaryTypeDef(TypedDict):
    hasImpactedResources: NotRequired[bool]

class LifecycleExecutionStateTypeDef(TypedDict):
    status: NotRequired[LifecycleExecutionStatusType]
    reason: NotRequired[str]

class LifecyclePolicyDetailActionIncludeResourcesTypeDef(TypedDict):
    amis: NotRequired[bool]
    snapshots: NotRequired[bool]
    containers: NotRequired[bool]

class LifecyclePolicyDetailExclusionRulesAmisLastLaunchedTypeDef(TypedDict):
    value: int
    unit: LifecyclePolicyTimeUnitType

LifecyclePolicyDetailFilterTypeDef = TypedDict(
    "LifecyclePolicyDetailFilterTypeDef",
    {
        "type": LifecyclePolicyDetailFilterTypeType,
        "value": int,
        "unit": NotRequired[LifecyclePolicyTimeUnitType],
        "retainAtLeast": NotRequired[int],
    },
)

class LifecyclePolicyResourceSelectionRecipeTypeDef(TypedDict):
    name: str
    semanticVersion: str

class LifecyclePolicySummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[LifecyclePolicyStatusType]
    executionRole: NotRequired[str]
    resourceType: NotRequired[LifecyclePolicyResourceTypeType]
    dateCreated: NotRequired[datetime]
    dateUpdated: NotRequired[datetime]
    dateLastRun: NotRequired[datetime]
    tags: NotRequired[Dict[str, str]]

class ListComponentBuildVersionsRequestRequestTypeDef(TypedDict):
    componentVersionArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImagePackagesRequestRequestTypeDef(TypedDict):
    imageBuildVersionArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListLifecycleExecutionResourcesRequestRequestTypeDef(TypedDict):
    lifecycleExecutionId: str
    parentResourceId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListLifecycleExecutionsRequestRequestTypeDef(TypedDict):
    resourceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListWaitingWorkflowStepsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class WorkflowStepExecutionTypeDef(TypedDict):
    stepExecutionId: NotRequired[str]
    imageBuildVersionArn: NotRequired[str]
    workflowExecutionId: NotRequired[str]
    workflowBuildVersionArn: NotRequired[str]
    name: NotRequired[str]
    action: NotRequired[str]
    startTime: NotRequired[str]

class ListWorkflowBuildVersionsRequestRequestTypeDef(TypedDict):
    workflowVersionArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListWorkflowExecutionsRequestRequestTypeDef(TypedDict):
    imageBuildVersionArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

WorkflowExecutionMetadataTypeDef = TypedDict(
    "WorkflowExecutionMetadataTypeDef",
    {
        "workflowBuildVersionArn": NotRequired[str],
        "workflowExecutionId": NotRequired[str],
        "type": NotRequired[WorkflowTypeType],
        "status": NotRequired[WorkflowExecutionStatusType],
        "message": NotRequired[str],
        "totalStepCount": NotRequired[int],
        "totalStepsSucceeded": NotRequired[int],
        "totalStepsFailed": NotRequired[int],
        "totalStepsSkipped": NotRequired[int],
        "startTime": NotRequired[str],
        "endTime": NotRequired[str],
        "parallelGroup": NotRequired[str],
    },
)

class ListWorkflowStepExecutionsRequestRequestTypeDef(TypedDict):
    workflowExecutionId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class WorkflowStepMetadataTypeDef(TypedDict):
    stepExecutionId: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    action: NotRequired[str]
    status: NotRequired[WorkflowStepExecutionStatusType]
    rollbackStatus: NotRequired[WorkflowStepExecutionRollbackStatusType]
    message: NotRequired[str]
    inputs: NotRequired[str]
    outputs: NotRequired[str]
    startTime: NotRequired[str]
    endTime: NotRequired[str]

WorkflowVersionTypeDef = TypedDict(
    "WorkflowVersionTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "version": NotRequired[str],
        "description": NotRequired[str],
        "type": NotRequired[WorkflowTypeType],
        "owner": NotRequired[str],
        "dateCreated": NotRequired[str],
    },
)

class S3LogsTypeDef(TypedDict):
    s3BucketName: NotRequired[str]
    s3KeyPrefix: NotRequired[str]

class VulnerablePackageTypeDef(TypedDict):
    name: NotRequired[str]
    version: NotRequired[str]
    sourceLayerHash: NotRequired[str]
    epoch: NotRequired[int]
    release: NotRequired[str]
    arch: NotRequired[str]
    packageManager: NotRequired[str]
    filePath: NotRequired[str]
    fixedInVersion: NotRequired[str]
    remediation: NotRequired[str]

class PutComponentPolicyRequestRequestTypeDef(TypedDict):
    componentArn: str
    policy: str

class PutContainerRecipePolicyRequestRequestTypeDef(TypedDict):
    containerRecipeArn: str
    policy: str

class PutImagePolicyRequestRequestTypeDef(TypedDict):
    imageArn: str
    policy: str

class PutImageRecipePolicyRequestRequestTypeDef(TypedDict):
    imageRecipeArn: str
    policy: str

class RemediationRecommendationTypeDef(TypedDict):
    text: NotRequired[str]
    url: NotRequired[str]

class ResourceStateTypeDef(TypedDict):
    status: NotRequired[ResourceStatusType]

class ResourceStateUpdateIncludeResourcesTypeDef(TypedDict):
    amis: NotRequired[bool]
    snapshots: NotRequired[bool]
    containers: NotRequired[bool]

class SendWorkflowStepActionRequestRequestTypeDef(TypedDict):
    stepExecutionId: str
    imageBuildVersionArn: str
    action: WorkflowStepActionTypeType
    clientToken: str
    reason: NotRequired[str]

class StartImagePipelineExecutionRequestRequestTypeDef(TypedDict):
    imagePipelineArn: str
    clientToken: str

TimestampTypeDef = Union[datetime, str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class WorkflowParameterOutputTypeDef(TypedDict):
    name: str
    value: List[str]

WorkflowParameterDetailTypeDef = TypedDict(
    "WorkflowParameterDetailTypeDef",
    {
        "name": str,
        "type": str,
        "defaultValue": NotRequired[List[str]],
        "description": NotRequired[str],
    },
)

class WorkflowParameterTypeDef(TypedDict):
    name: str
    value: Sequence[str]

class WorkflowStateTypeDef(TypedDict):
    status: NotRequired[Literal["DEPRECATED"]]
    reason: NotRequired[str]

class AccountAggregationTypeDef(TypedDict):
    accountId: NotRequired[str]
    severityCounts: NotRequired[SeverityCountsTypeDef]

class ImageAggregationTypeDef(TypedDict):
    imageBuildVersionArn: NotRequired[str]
    severityCounts: NotRequired[SeverityCountsTypeDef]

class ImagePipelineAggregationTypeDef(TypedDict):
    imagePipelineArn: NotRequired[str]
    severityCounts: NotRequired[SeverityCountsTypeDef]

class VulnerabilityIdAggregationTypeDef(TypedDict):
    vulnerabilityId: NotRequired[str]
    severityCounts: NotRequired[SeverityCountsTypeDef]

class AdditionalInstanceConfigurationTypeDef(TypedDict):
    systemsManagerAgent: NotRequired[SystemsManagerAgentTypeDef]
    userDataOverride: NotRequired[str]

class AmiDistributionConfigurationOutputTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    targetAccountIds: NotRequired[List[str]]
    amiTags: NotRequired[Dict[str, str]]
    kmsKeyId: NotRequired[str]
    launchPermission: NotRequired[LaunchPermissionConfigurationOutputTypeDef]

class AmiTypeDef(TypedDict):
    region: NotRequired[str]
    image: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    state: NotRequired[ImageStateTypeDef]
    accountId: NotRequired[str]

class CancelImageCreationResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    imageBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CancelLifecycleExecutionResponseTypeDef(TypedDict):
    lifecycleExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateComponentResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    componentBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateContainerRecipeResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    containerRecipeArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDistributionConfigurationResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    distributionConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateImagePipelineResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    imagePipelineArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateImageRecipeResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    imageRecipeArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateImageResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    imageBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInfrastructureConfigurationResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    infrastructureConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLifecyclePolicyResponseTypeDef(TypedDict):
    clientToken: str
    lifecyclePolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorkflowResponseTypeDef(TypedDict):
    clientToken: str
    workflowBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteComponentResponseTypeDef(TypedDict):
    requestId: str
    componentBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteContainerRecipeResponseTypeDef(TypedDict):
    requestId: str
    containerRecipeArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDistributionConfigurationResponseTypeDef(TypedDict):
    requestId: str
    distributionConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteImagePipelineResponseTypeDef(TypedDict):
    requestId: str
    imagePipelineArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteImageRecipeResponseTypeDef(TypedDict):
    requestId: str
    imageRecipeArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteImageResponseTypeDef(TypedDict):
    requestId: str
    imageBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInfrastructureConfigurationResponseTypeDef(TypedDict):
    requestId: str
    infrastructureConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteLifecyclePolicyResponseTypeDef(TypedDict):
    lifecyclePolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteWorkflowResponseTypeDef(TypedDict):
    workflowBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetComponentPolicyResponseTypeDef(TypedDict):
    requestId: str
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetContainerRecipePolicyResponseTypeDef(TypedDict):
    requestId: str
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetImagePolicyResponseTypeDef(TypedDict):
    requestId: str
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetImageRecipePolicyResponseTypeDef(TypedDict):
    requestId: str
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

GetWorkflowExecutionResponseTypeDef = TypedDict(
    "GetWorkflowExecutionResponseTypeDef",
    {
        "requestId": str,
        "workflowBuildVersionArn": str,
        "workflowExecutionId": str,
        "imageBuildVersionArn": str,
        "type": WorkflowTypeType,
        "status": WorkflowExecutionStatusType,
        "message": str,
        "totalStepCount": int,
        "totalStepsSucceeded": int,
        "totalStepsFailed": int,
        "totalStepsSkipped": int,
        "startTime": str,
        "endTime": str,
        "parallelGroup": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetWorkflowStepExecutionResponseTypeDef(TypedDict):
    requestId: str
    stepExecutionId: str
    workflowBuildVersionArn: str
    workflowExecutionId: str
    imageBuildVersionArn: str
    name: str
    description: str
    action: str
    status: WorkflowStepExecutionStatusType
    rollbackStatus: WorkflowStepExecutionRollbackStatusType
    message: str
    inputs: str
    outputs: str
    startTime: str
    endTime: str
    onFailure: str
    timeoutSeconds: int
    ResponseMetadata: ResponseMetadataTypeDef

class ImportComponentResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    componentBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportVmImageResponseTypeDef(TypedDict):
    requestId: str
    imageArn: str
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutComponentPolicyResponseTypeDef(TypedDict):
    requestId: str
    componentArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutContainerRecipePolicyResponseTypeDef(TypedDict):
    requestId: str
    containerRecipeArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutImagePolicyResponseTypeDef(TypedDict):
    requestId: str
    imageArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutImageRecipePolicyResponseTypeDef(TypedDict):
    requestId: str
    imageRecipeArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class SendWorkflowStepActionResponseTypeDef(TypedDict):
    stepExecutionId: str
    imageBuildVersionArn: str
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartImagePipelineExecutionResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    imageBuildVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartResourceStateUpdateResponseTypeDef(TypedDict):
    lifecycleExecutionId: str
    resourceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDistributionConfigurationResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    distributionConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateImagePipelineResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    imagePipelineArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateInfrastructureConfigurationResponseTypeDef(TypedDict):
    requestId: str
    clientToken: str
    infrastructureConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLifecyclePolicyResponseTypeDef(TypedDict):
    lifecyclePolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ComponentConfigurationOutputTypeDef(TypedDict):
    componentArn: str
    parameters: NotRequired[List[ComponentParameterOutputTypeDef]]

ComponentParameterUnionTypeDef = Union[ComponentParameterTypeDef, ComponentParameterOutputTypeDef]
ComponentSummaryTypeDef = TypedDict(
    "ComponentSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "version": NotRequired[str],
        "platform": NotRequired[PlatformType],
        "supportedOsVersions": NotRequired[List[str]],
        "state": NotRequired[ComponentStateTypeDef],
        "type": NotRequired[ComponentTypeType],
        "owner": NotRequired[str],
        "description": NotRequired[str],
        "changeDescription": NotRequired[str],
        "dateCreated": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "publisher": NotRequired[str],
        "obfuscate": NotRequired[bool],
    },
)
ComponentTypeDef = TypedDict(
    "ComponentTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "version": NotRequired[str],
        "description": NotRequired[str],
        "changeDescription": NotRequired[str],
        "type": NotRequired[ComponentTypeType],
        "platform": NotRequired[PlatformType],
        "supportedOsVersions": NotRequired[List[str]],
        "state": NotRequired[ComponentStateTypeDef],
        "parameters": NotRequired[List[ComponentParameterDetailTypeDef]],
        "owner": NotRequired[str],
        "data": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "encrypted": NotRequired[bool],
        "dateCreated": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "publisher": NotRequired[str],
        "obfuscate": NotRequired[bool],
    },
)

class ListComponentsResponseTypeDef(TypedDict):
    requestId: str
    componentVersionList: List[ComponentVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ContainerDistributionConfigurationOutputTypeDef(TypedDict):
    targetRepository: TargetContainerRepositoryTypeDef
    description: NotRequired[str]
    containerTags: NotRequired[List[str]]

class ContainerDistributionConfigurationTypeDef(TypedDict):
    targetRepository: TargetContainerRepositoryTypeDef
    description: NotRequired[str]
    containerTags: NotRequired[Sequence[str]]

class ListContainerRecipesResponseTypeDef(TypedDict):
    requestId: str
    containerRecipeSummaryList: List[ContainerRecipeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class InfrastructureConfigurationSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    dateCreated: NotRequired[str]
    dateUpdated: NotRequired[str]
    resourceTags: NotRequired[Dict[str, str]]
    tags: NotRequired[Dict[str, str]]
    instanceTypes: NotRequired[List[str]]
    instanceProfileName: NotRequired[str]
    placement: NotRequired[PlacementTypeDef]

class CvssScoreDetailsTypeDef(TypedDict):
    scoreSource: NotRequired[str]
    cvssSource: NotRequired[str]
    version: NotRequired[str]
    score: NotRequired[float]
    scoringVector: NotRequired[str]
    adjustments: NotRequired[List[CvssScoreAdjustmentTypeDef]]

class ListDistributionConfigurationsResponseTypeDef(TypedDict):
    requestId: str
    distributionConfigurationSummaryList: List[DistributionConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class InstanceBlockDeviceMappingTypeDef(TypedDict):
    deviceName: NotRequired[str]
    ebs: NotRequired[EbsInstanceBlockDeviceSpecificationTypeDef]
    virtualName: NotRequired[str]
    noDevice: NotRequired[str]

class ImageScanningConfigurationOutputTypeDef(TypedDict):
    imageScanningEnabled: NotRequired[bool]
    ecrConfiguration: NotRequired[EcrConfigurationOutputTypeDef]

EcrConfigurationUnionTypeDef = Union[EcrConfigurationTypeDef, EcrConfigurationOutputTypeDef]

class FastLaunchConfigurationTypeDef(TypedDict):
    enabled: bool
    snapshotConfiguration: NotRequired[FastLaunchSnapshotConfigurationTypeDef]
    maxParallelLaunches: NotRequired[int]
    launchTemplate: NotRequired[FastLaunchLaunchTemplateSpecificationTypeDef]
    accountId: NotRequired[str]

class ListComponentsRequestRequestTypeDef(TypedDict):
    owner: NotRequired[OwnershipType]
    filters: NotRequired[Sequence[FilterTypeDef]]
    byName: NotRequired[bool]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListContainerRecipesRequestRequestTypeDef(TypedDict):
    owner: NotRequired[OwnershipType]
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDistributionConfigurationsRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImageBuildVersionsRequestRequestTypeDef(TypedDict):
    imageVersionArn: str
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImagePipelineImagesRequestRequestTypeDef(TypedDict):
    imagePipelineArn: str
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImagePipelinesRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImageRecipesRequestRequestTypeDef(TypedDict):
    owner: NotRequired[OwnershipType]
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ListImageScanFindingAggregationsRequestRequestTypeDef = TypedDict(
    "ListImageScanFindingAggregationsRequestRequestTypeDef",
    {
        "filter": NotRequired[FilterTypeDef],
        "nextToken": NotRequired[str],
    },
)

class ListImagesRequestRequestTypeDef(TypedDict):
    owner: NotRequired[OwnershipType]
    filters: NotRequired[Sequence[FilterTypeDef]]
    byName: NotRequired[bool]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    includeDeprecated: NotRequired[bool]

class ListInfrastructureConfigurationsRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListLifecyclePoliciesRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListWorkflowsRequestRequestTypeDef(TypedDict):
    owner: NotRequired[OwnershipType]
    filters: NotRequired[Sequence[FilterTypeDef]]
    byName: NotRequired[bool]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImagePackagesResponseTypeDef(TypedDict):
    requestId: str
    imagePackageList: List[ImagePackageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListImageRecipesResponseTypeDef(TypedDict):
    requestId: str
    imageRecipeSummaryList: List[ImageRecipeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListImageScanFindingsRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[ImageScanFindingsFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListImagesResponseTypeDef(TypedDict):
    requestId: str
    imageVersionList: List[ImageVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

LaunchPermissionConfigurationUnionTypeDef = Union[
    LaunchPermissionConfigurationTypeDef, LaunchPermissionConfigurationOutputTypeDef
]

class LifecycleExecutionSnapshotResourceTypeDef(TypedDict):
    snapshotId: NotRequired[str]
    state: NotRequired[LifecycleExecutionResourceStateTypeDef]

class LifecycleExecutionTypeDef(TypedDict):
    lifecycleExecutionId: NotRequired[str]
    lifecyclePolicyArn: NotRequired[str]
    resourcesImpactedSummary: NotRequired[LifecycleExecutionResourcesImpactedSummaryTypeDef]
    state: NotRequired[LifecycleExecutionStateTypeDef]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]

LifecyclePolicyDetailActionTypeDef = TypedDict(
    "LifecyclePolicyDetailActionTypeDef",
    {
        "type": LifecyclePolicyDetailActionTypeType,
        "includeResources": NotRequired[LifecyclePolicyDetailActionIncludeResourcesTypeDef],
    },
)

class LifecyclePolicyDetailExclusionRulesAmisOutputTypeDef(TypedDict):
    isPublic: NotRequired[bool]
    regions: NotRequired[List[str]]
    sharedAccounts: NotRequired[List[str]]
    lastLaunched: NotRequired[LifecyclePolicyDetailExclusionRulesAmisLastLaunchedTypeDef]
    tagMap: NotRequired[Dict[str, str]]

class LifecyclePolicyDetailExclusionRulesAmisTypeDef(TypedDict):
    isPublic: NotRequired[bool]
    regions: NotRequired[Sequence[str]]
    sharedAccounts: NotRequired[Sequence[str]]
    lastLaunched: NotRequired[LifecyclePolicyDetailExclusionRulesAmisLastLaunchedTypeDef]
    tagMap: NotRequired[Mapping[str, str]]

class LifecyclePolicyResourceSelectionOutputTypeDef(TypedDict):
    recipes: NotRequired[List[LifecyclePolicyResourceSelectionRecipeTypeDef]]
    tagMap: NotRequired[Dict[str, str]]

class LifecyclePolicyResourceSelectionTypeDef(TypedDict):
    recipes: NotRequired[Sequence[LifecyclePolicyResourceSelectionRecipeTypeDef]]
    tagMap: NotRequired[Mapping[str, str]]

class ListLifecyclePoliciesResponseTypeDef(TypedDict):
    lifecyclePolicySummaryList: List[LifecyclePolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWaitingWorkflowStepsResponseTypeDef(TypedDict):
    steps: List[WorkflowStepExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorkflowExecutionsResponseTypeDef(TypedDict):
    requestId: str
    workflowExecutions: List[WorkflowExecutionMetadataTypeDef]
    imageBuildVersionArn: str
    message: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorkflowStepExecutionsResponseTypeDef(TypedDict):
    requestId: str
    steps: List[WorkflowStepMetadataTypeDef]
    workflowBuildVersionArn: str
    workflowExecutionId: str
    imageBuildVersionArn: str
    message: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorkflowsResponseTypeDef(TypedDict):
    workflowVersionList: List[WorkflowVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class LoggingTypeDef(TypedDict):
    s3Logs: NotRequired[S3LogsTypeDef]

class PackageVulnerabilityDetailsTypeDef(TypedDict):
    vulnerabilityId: str
    vulnerablePackages: NotRequired[List[VulnerablePackageTypeDef]]
    source: NotRequired[str]
    cvss: NotRequired[List[CvssScoreTypeDef]]
    relatedVulnerabilities: NotRequired[List[str]]
    sourceUrl: NotRequired[str]
    vendorSeverity: NotRequired[str]
    vendorCreatedAt: NotRequired[datetime]
    vendorUpdatedAt: NotRequired[datetime]
    referenceUrls: NotRequired[List[str]]

class RemediationTypeDef(TypedDict):
    recommendation: NotRequired[RemediationRecommendationTypeDef]

class WorkflowConfigurationOutputTypeDef(TypedDict):
    workflowArn: str
    parameters: NotRequired[List[WorkflowParameterOutputTypeDef]]
    parallelGroup: NotRequired[str]
    onFailure: NotRequired[OnWorkflowFailureType]

WorkflowParameterUnionTypeDef = Union[WorkflowParameterTypeDef, WorkflowParameterOutputTypeDef]
WorkflowSummaryTypeDef = TypedDict(
    "WorkflowSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "version": NotRequired[str],
        "description": NotRequired[str],
        "changeDescription": NotRequired[str],
        "type": NotRequired[WorkflowTypeType],
        "owner": NotRequired[str],
        "state": NotRequired[WorkflowStateTypeDef],
        "dateCreated": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
WorkflowTypeDef = TypedDict(
    "WorkflowTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "version": NotRequired[str],
        "description": NotRequired[str],
        "changeDescription": NotRequired[str],
        "type": NotRequired[WorkflowTypeType],
        "state": NotRequired[WorkflowStateTypeDef],
        "owner": NotRequired[str],
        "data": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "dateCreated": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "parameters": NotRequired[List[WorkflowParameterDetailTypeDef]],
    },
)

class ImageScanFindingAggregationTypeDef(TypedDict):
    accountAggregation: NotRequired[AccountAggregationTypeDef]
    imageAggregation: NotRequired[ImageAggregationTypeDef]
    imagePipelineAggregation: NotRequired[ImagePipelineAggregationTypeDef]
    vulnerabilityIdAggregation: NotRequired[VulnerabilityIdAggregationTypeDef]

class OutputResourcesTypeDef(TypedDict):
    amis: NotRequired[List[AmiTypeDef]]
    containers: NotRequired[List[ContainerTypeDef]]

class ComponentConfigurationTypeDef(TypedDict):
    componentArn: str
    parameters: NotRequired[Sequence[ComponentParameterUnionTypeDef]]

class ListComponentBuildVersionsResponseTypeDef(TypedDict):
    requestId: str
    componentSummaryList: List[ComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetComponentResponseTypeDef(TypedDict):
    requestId: str
    component: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ContainerDistributionConfigurationUnionTypeDef = Union[
    ContainerDistributionConfigurationTypeDef, ContainerDistributionConfigurationOutputTypeDef
]

class ListInfrastructureConfigurationsResponseTypeDef(TypedDict):
    requestId: str
    infrastructureConfigurationSummaryList: List[InfrastructureConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class InspectorScoreDetailsTypeDef(TypedDict):
    adjustedCvss: NotRequired[CvssScoreDetailsTypeDef]

ImageRecipeTypeDef = TypedDict(
    "ImageRecipeTypeDef",
    {
        "arn": NotRequired[str],
        "type": NotRequired[ImageTypeType],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "platform": NotRequired[PlatformType],
        "owner": NotRequired[str],
        "version": NotRequired[str],
        "components": NotRequired[List[ComponentConfigurationOutputTypeDef]],
        "parentImage": NotRequired[str],
        "blockDeviceMappings": NotRequired[List[InstanceBlockDeviceMappingTypeDef]],
        "dateCreated": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "workingDirectory": NotRequired[str],
        "additionalInstanceConfiguration": NotRequired[AdditionalInstanceConfigurationTypeDef],
    },
)

class InstanceConfigurationOutputTypeDef(TypedDict):
    image: NotRequired[str]
    blockDeviceMappings: NotRequired[List[InstanceBlockDeviceMappingTypeDef]]

class InstanceConfigurationTypeDef(TypedDict):
    image: NotRequired[str]
    blockDeviceMappings: NotRequired[Sequence[InstanceBlockDeviceMappingTypeDef]]

class ImageScanningConfigurationTypeDef(TypedDict):
    imageScanningEnabled: NotRequired[bool]
    ecrConfiguration: NotRequired[EcrConfigurationUnionTypeDef]

class DistributionOutputTypeDef(TypedDict):
    region: str
    amiDistributionConfiguration: NotRequired[AmiDistributionConfigurationOutputTypeDef]
    containerDistributionConfiguration: NotRequired[ContainerDistributionConfigurationOutputTypeDef]
    licenseConfigurationArns: NotRequired[List[str]]
    launchTemplateConfigurations: NotRequired[List[LaunchTemplateConfigurationTypeDef]]
    s3ExportConfiguration: NotRequired[S3ExportConfigurationTypeDef]
    fastLaunchConfigurations: NotRequired[List[FastLaunchConfigurationTypeDef]]

class AmiDistributionConfigurationTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    targetAccountIds: NotRequired[Sequence[str]]
    amiTags: NotRequired[Mapping[str, str]]
    kmsKeyId: NotRequired[str]
    launchPermission: NotRequired[LaunchPermissionConfigurationUnionTypeDef]

class LifecycleExecutionResourceTypeDef(TypedDict):
    accountId: NotRequired[str]
    resourceId: NotRequired[str]
    state: NotRequired[LifecycleExecutionResourceStateTypeDef]
    action: NotRequired[LifecycleExecutionResourceActionTypeDef]
    region: NotRequired[str]
    snapshots: NotRequired[List[LifecycleExecutionSnapshotResourceTypeDef]]
    imageUris: NotRequired[List[str]]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]

class GetLifecycleExecutionResponseTypeDef(TypedDict):
    lifecycleExecution: LifecycleExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLifecycleExecutionsResponseTypeDef(TypedDict):
    lifecycleExecutions: List[LifecycleExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class LifecyclePolicyDetailExclusionRulesOutputTypeDef(TypedDict):
    tagMap: NotRequired[Dict[str, str]]
    amis: NotRequired[LifecyclePolicyDetailExclusionRulesAmisOutputTypeDef]

LifecyclePolicyDetailExclusionRulesAmisUnionTypeDef = Union[
    LifecyclePolicyDetailExclusionRulesAmisTypeDef,
    LifecyclePolicyDetailExclusionRulesAmisOutputTypeDef,
]

class CreateInfrastructureConfigurationRequestRequestTypeDef(TypedDict):
    name: str
    instanceProfileName: str
    clientToken: str
    description: NotRequired[str]
    instanceTypes: NotRequired[Sequence[str]]
    securityGroupIds: NotRequired[Sequence[str]]
    subnetId: NotRequired[str]
    logging: NotRequired[LoggingTypeDef]
    keyPair: NotRequired[str]
    terminateInstanceOnFailure: NotRequired[bool]
    snsTopicArn: NotRequired[str]
    resourceTags: NotRequired[Mapping[str, str]]
    instanceMetadataOptions: NotRequired[InstanceMetadataOptionsTypeDef]
    tags: NotRequired[Mapping[str, str]]
    placement: NotRequired[PlacementTypeDef]

class InfrastructureConfigurationTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    instanceTypes: NotRequired[List[str]]
    instanceProfileName: NotRequired[str]
    securityGroupIds: NotRequired[List[str]]
    subnetId: NotRequired[str]
    logging: NotRequired[LoggingTypeDef]
    keyPair: NotRequired[str]
    terminateInstanceOnFailure: NotRequired[bool]
    snsTopicArn: NotRequired[str]
    dateCreated: NotRequired[str]
    dateUpdated: NotRequired[str]
    resourceTags: NotRequired[Dict[str, str]]
    instanceMetadataOptions: NotRequired[InstanceMetadataOptionsTypeDef]
    tags: NotRequired[Dict[str, str]]
    placement: NotRequired[PlacementTypeDef]

class UpdateInfrastructureConfigurationRequestRequestTypeDef(TypedDict):
    infrastructureConfigurationArn: str
    instanceProfileName: str
    clientToken: str
    description: NotRequired[str]
    instanceTypes: NotRequired[Sequence[str]]
    securityGroupIds: NotRequired[Sequence[str]]
    subnetId: NotRequired[str]
    logging: NotRequired[LoggingTypeDef]
    keyPair: NotRequired[str]
    terminateInstanceOnFailure: NotRequired[bool]
    snsTopicArn: NotRequired[str]
    resourceTags: NotRequired[Mapping[str, str]]
    instanceMetadataOptions: NotRequired[InstanceMetadataOptionsTypeDef]
    placement: NotRequired[PlacementTypeDef]

class ImagePipelineTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    platform: NotRequired[PlatformType]
    enhancedImageMetadataEnabled: NotRequired[bool]
    imageRecipeArn: NotRequired[str]
    containerRecipeArn: NotRequired[str]
    infrastructureConfigurationArn: NotRequired[str]
    distributionConfigurationArn: NotRequired[str]
    imageTestsConfiguration: NotRequired[ImageTestsConfigurationTypeDef]
    schedule: NotRequired[ScheduleTypeDef]
    status: NotRequired[PipelineStatusType]
    dateCreated: NotRequired[str]
    dateUpdated: NotRequired[str]
    dateLastRun: NotRequired[str]
    dateNextRun: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    imageScanningConfiguration: NotRequired[ImageScanningConfigurationOutputTypeDef]
    executionRole: NotRequired[str]
    workflows: NotRequired[List[WorkflowConfigurationOutputTypeDef]]

class WorkflowConfigurationTypeDef(TypedDict):
    workflowArn: str
    parameters: NotRequired[Sequence[WorkflowParameterUnionTypeDef]]
    parallelGroup: NotRequired[str]
    onFailure: NotRequired[OnWorkflowFailureType]

class ListWorkflowBuildVersionsResponseTypeDef(TypedDict):
    workflowSummaryList: List[WorkflowSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetWorkflowResponseTypeDef(TypedDict):
    workflow: WorkflowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListImageScanFindingAggregationsResponseTypeDef(TypedDict):
    requestId: str
    aggregationType: str
    responses: List[ImageScanFindingAggregationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ImageSummaryTypeDef = TypedDict(
    "ImageSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[ImageTypeType],
        "version": NotRequired[str],
        "platform": NotRequired[PlatformType],
        "osVersion": NotRequired[str],
        "state": NotRequired[ImageStateTypeDef],
        "owner": NotRequired[str],
        "dateCreated": NotRequired[str],
        "outputResources": NotRequired[OutputResourcesTypeDef],
        "tags": NotRequired[Dict[str, str]],
        "buildType": NotRequired[BuildTypeType],
        "imageSource": NotRequired[ImageSourceType],
        "deprecationTime": NotRequired[datetime],
        "lifecycleExecutionId": NotRequired[str],
    },
)
ComponentConfigurationUnionTypeDef = Union[
    ComponentConfigurationTypeDef, ComponentConfigurationOutputTypeDef
]

class CreateImageRecipeRequestRequestTypeDef(TypedDict):
    name: str
    semanticVersion: str
    components: Sequence[ComponentConfigurationTypeDef]
    parentImage: str
    clientToken: str
    description: NotRequired[str]
    blockDeviceMappings: NotRequired[Sequence[InstanceBlockDeviceMappingTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    workingDirectory: NotRequired[str]
    additionalInstanceConfiguration: NotRequired[AdditionalInstanceConfigurationTypeDef]

ImageScanFindingTypeDef = TypedDict(
    "ImageScanFindingTypeDef",
    {
        "awsAccountId": NotRequired[str],
        "imageBuildVersionArn": NotRequired[str],
        "imagePipelineArn": NotRequired[str],
        "type": NotRequired[str],
        "description": NotRequired[str],
        "title": NotRequired[str],
        "remediation": NotRequired[RemediationTypeDef],
        "severity": NotRequired[str],
        "firstObservedAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "inspectorScore": NotRequired[float],
        "inspectorScoreDetails": NotRequired[InspectorScoreDetailsTypeDef],
        "packageVulnerabilityDetails": NotRequired[PackageVulnerabilityDetailsTypeDef],
        "fixAvailable": NotRequired[str],
    },
)

class GetImageRecipeResponseTypeDef(TypedDict):
    requestId: str
    imageRecipe: ImageRecipeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ContainerRecipeTypeDef(TypedDict):
    arn: NotRequired[str]
    containerType: NotRequired[Literal["DOCKER"]]
    name: NotRequired[str]
    description: NotRequired[str]
    platform: NotRequired[PlatformType]
    owner: NotRequired[str]
    version: NotRequired[str]
    components: NotRequired[List[ComponentConfigurationOutputTypeDef]]
    instanceConfiguration: NotRequired[InstanceConfigurationOutputTypeDef]
    dockerfileTemplateData: NotRequired[str]
    kmsKeyId: NotRequired[str]
    encrypted: NotRequired[bool]
    parentImage: NotRequired[str]
    dateCreated: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    workingDirectory: NotRequired[str]
    targetRepository: NotRequired[TargetContainerRepositoryTypeDef]

class DistributionConfigurationTypeDef(TypedDict):
    timeoutMinutes: int
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    distributions: NotRequired[List[DistributionOutputTypeDef]]
    dateCreated: NotRequired[str]
    dateUpdated: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

AmiDistributionConfigurationUnionTypeDef = Union[
    AmiDistributionConfigurationTypeDef, AmiDistributionConfigurationOutputTypeDef
]

class ListLifecycleExecutionResourcesResponseTypeDef(TypedDict):
    lifecycleExecutionId: str
    lifecycleExecutionState: LifecycleExecutionStateTypeDef
    resources: List[LifecycleExecutionResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

LifecyclePolicyDetailOutputTypeDef = TypedDict(
    "LifecyclePolicyDetailOutputTypeDef",
    {
        "action": LifecyclePolicyDetailActionTypeDef,
        "filter": LifecyclePolicyDetailFilterTypeDef,
        "exclusionRules": NotRequired[LifecyclePolicyDetailExclusionRulesOutputTypeDef],
    },
)

class LifecyclePolicyDetailExclusionRulesTypeDef(TypedDict):
    tagMap: NotRequired[Mapping[str, str]]
    amis: NotRequired[LifecyclePolicyDetailExclusionRulesAmisUnionTypeDef]

class ResourceStateUpdateExclusionRulesTypeDef(TypedDict):
    amis: NotRequired[LifecyclePolicyDetailExclusionRulesAmisUnionTypeDef]

class GetInfrastructureConfigurationResponseTypeDef(TypedDict):
    requestId: str
    infrastructureConfiguration: InfrastructureConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetImagePipelineResponseTypeDef(TypedDict):
    requestId: str
    imagePipeline: ImagePipelineTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListImagePipelinesResponseTypeDef(TypedDict):
    requestId: str
    imagePipelineList: List[ImagePipelineTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateImagePipelineRequestRequestTypeDef(TypedDict):
    name: str
    infrastructureConfigurationArn: str
    clientToken: str
    description: NotRequired[str]
    imageRecipeArn: NotRequired[str]
    containerRecipeArn: NotRequired[str]
    distributionConfigurationArn: NotRequired[str]
    imageTestsConfiguration: NotRequired[ImageTestsConfigurationTypeDef]
    enhancedImageMetadataEnabled: NotRequired[bool]
    schedule: NotRequired[ScheduleTypeDef]
    status: NotRequired[PipelineStatusType]
    tags: NotRequired[Mapping[str, str]]
    imageScanningConfiguration: NotRequired[ImageScanningConfigurationTypeDef]
    workflows: NotRequired[Sequence[WorkflowConfigurationTypeDef]]
    executionRole: NotRequired[str]

class UpdateImagePipelineRequestRequestTypeDef(TypedDict):
    imagePipelineArn: str
    infrastructureConfigurationArn: str
    clientToken: str
    description: NotRequired[str]
    imageRecipeArn: NotRequired[str]
    containerRecipeArn: NotRequired[str]
    distributionConfigurationArn: NotRequired[str]
    imageTestsConfiguration: NotRequired[ImageTestsConfigurationTypeDef]
    enhancedImageMetadataEnabled: NotRequired[bool]
    schedule: NotRequired[ScheduleTypeDef]
    status: NotRequired[PipelineStatusType]
    imageScanningConfiguration: NotRequired[ImageScanningConfigurationTypeDef]
    workflows: NotRequired[Sequence[WorkflowConfigurationTypeDef]]
    executionRole: NotRequired[str]

WorkflowConfigurationUnionTypeDef = Union[
    WorkflowConfigurationTypeDef, WorkflowConfigurationOutputTypeDef
]

class ListImageBuildVersionsResponseTypeDef(TypedDict):
    requestId: str
    imageSummaryList: List[ImageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListImagePipelineImagesResponseTypeDef(TypedDict):
    requestId: str
    imageSummaryList: List[ImageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateContainerRecipeRequestRequestTypeDef(TypedDict):
    containerType: Literal["DOCKER"]
    name: str
    semanticVersion: str
    components: Sequence[ComponentConfigurationUnionTypeDef]
    parentImage: str
    targetRepository: TargetContainerRepositoryTypeDef
    clientToken: str
    description: NotRequired[str]
    instanceConfiguration: NotRequired[InstanceConfigurationTypeDef]
    dockerfileTemplateData: NotRequired[str]
    dockerfileTemplateUri: NotRequired[str]
    platformOverride: NotRequired[PlatformType]
    imageOsVersionOverride: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    workingDirectory: NotRequired[str]
    kmsKeyId: NotRequired[str]

class ListImageScanFindingsResponseTypeDef(TypedDict):
    requestId: str
    findings: List[ImageScanFindingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetContainerRecipeResponseTypeDef(TypedDict):
    requestId: str
    containerRecipe: ContainerRecipeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDistributionConfigurationResponseTypeDef(TypedDict):
    requestId: str
    distributionConfiguration: DistributionConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "arn": NotRequired[str],
        "type": NotRequired[ImageTypeType],
        "name": NotRequired[str],
        "version": NotRequired[str],
        "platform": NotRequired[PlatformType],
        "enhancedImageMetadataEnabled": NotRequired[bool],
        "osVersion": NotRequired[str],
        "state": NotRequired[ImageStateTypeDef],
        "imageRecipe": NotRequired[ImageRecipeTypeDef],
        "containerRecipe": NotRequired[ContainerRecipeTypeDef],
        "sourcePipelineName": NotRequired[str],
        "sourcePipelineArn": NotRequired[str],
        "infrastructureConfiguration": NotRequired[InfrastructureConfigurationTypeDef],
        "distributionConfiguration": NotRequired[DistributionConfigurationTypeDef],
        "imageTestsConfiguration": NotRequired[ImageTestsConfigurationTypeDef],
        "dateCreated": NotRequired[str],
        "outputResources": NotRequired[OutputResourcesTypeDef],
        "tags": NotRequired[Dict[str, str]],
        "buildType": NotRequired[BuildTypeType],
        "imageSource": NotRequired[ImageSourceType],
        "scanState": NotRequired[ImageScanStateTypeDef],
        "imageScanningConfiguration": NotRequired[ImageScanningConfigurationOutputTypeDef],
        "deprecationTime": NotRequired[datetime],
        "lifecycleExecutionId": NotRequired[str],
        "executionRole": NotRequired[str],
        "workflows": NotRequired[List[WorkflowConfigurationOutputTypeDef]],
    },
)

class DistributionTypeDef(TypedDict):
    region: str
    amiDistributionConfiguration: NotRequired[AmiDistributionConfigurationUnionTypeDef]
    containerDistributionConfiguration: NotRequired[ContainerDistributionConfigurationUnionTypeDef]
    licenseConfigurationArns: NotRequired[Sequence[str]]
    launchTemplateConfigurations: NotRequired[Sequence[LaunchTemplateConfigurationTypeDef]]
    s3ExportConfiguration: NotRequired[S3ExportConfigurationTypeDef]
    fastLaunchConfigurations: NotRequired[Sequence[FastLaunchConfigurationTypeDef]]

class LifecyclePolicyTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[LifecyclePolicyStatusType]
    executionRole: NotRequired[str]
    resourceType: NotRequired[LifecyclePolicyResourceTypeType]
    policyDetails: NotRequired[List[LifecyclePolicyDetailOutputTypeDef]]
    resourceSelection: NotRequired[LifecyclePolicyResourceSelectionOutputTypeDef]
    dateCreated: NotRequired[datetime]
    dateUpdated: NotRequired[datetime]
    dateLastRun: NotRequired[datetime]
    tags: NotRequired[Dict[str, str]]

LifecyclePolicyDetailExclusionRulesUnionTypeDef = Union[
    LifecyclePolicyDetailExclusionRulesTypeDef, LifecyclePolicyDetailExclusionRulesOutputTypeDef
]

class StartResourceStateUpdateRequestRequestTypeDef(TypedDict):
    resourceArn: str
    state: ResourceStateTypeDef
    clientToken: str
    executionRole: NotRequired[str]
    includeResources: NotRequired[ResourceStateUpdateIncludeResourcesTypeDef]
    exclusionRules: NotRequired[ResourceStateUpdateExclusionRulesTypeDef]
    updateAt: NotRequired[TimestampTypeDef]

class CreateImageRequestRequestTypeDef(TypedDict):
    infrastructureConfigurationArn: str
    clientToken: str
    imageRecipeArn: NotRequired[str]
    containerRecipeArn: NotRequired[str]
    distributionConfigurationArn: NotRequired[str]
    imageTestsConfiguration: NotRequired[ImageTestsConfigurationTypeDef]
    enhancedImageMetadataEnabled: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]
    imageScanningConfiguration: NotRequired[ImageScanningConfigurationTypeDef]
    workflows: NotRequired[Sequence[WorkflowConfigurationUnionTypeDef]]
    executionRole: NotRequired[str]

class GetImageResponseTypeDef(TypedDict):
    requestId: str
    image: ImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

DistributionUnionTypeDef = Union[DistributionTypeDef, DistributionOutputTypeDef]

class UpdateDistributionConfigurationRequestRequestTypeDef(TypedDict):
    distributionConfigurationArn: str
    distributions: Sequence[DistributionTypeDef]
    clientToken: str
    description: NotRequired[str]

class GetLifecyclePolicyResponseTypeDef(TypedDict):
    lifecyclePolicy: LifecyclePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

LifecyclePolicyDetailTypeDef = TypedDict(
    "LifecyclePolicyDetailTypeDef",
    {
        "action": LifecyclePolicyDetailActionTypeDef,
        "filter": LifecyclePolicyDetailFilterTypeDef,
        "exclusionRules": NotRequired[LifecyclePolicyDetailExclusionRulesUnionTypeDef],
    },
)

class CreateDistributionConfigurationRequestRequestTypeDef(TypedDict):
    name: str
    distributions: Sequence[DistributionUnionTypeDef]
    clientToken: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

LifecyclePolicyDetailUnionTypeDef = Union[
    LifecyclePolicyDetailTypeDef, LifecyclePolicyDetailOutputTypeDef
]

class UpdateLifecyclePolicyRequestRequestTypeDef(TypedDict):
    lifecyclePolicyArn: str
    executionRole: str
    resourceType: LifecyclePolicyResourceTypeType
    policyDetails: Sequence[LifecyclePolicyDetailTypeDef]
    resourceSelection: LifecyclePolicyResourceSelectionTypeDef
    clientToken: str
    description: NotRequired[str]
    status: NotRequired[LifecyclePolicyStatusType]

class CreateLifecyclePolicyRequestRequestTypeDef(TypedDict):
    name: str
    executionRole: str
    resourceType: LifecyclePolicyResourceTypeType
    policyDetails: Sequence[LifecyclePolicyDetailUnionTypeDef]
    resourceSelection: LifecyclePolicyResourceSelectionTypeDef
    clientToken: str
    description: NotRequired[str]
    status: NotRequired[LifecyclePolicyStatusType]
    tags: NotRequired[Mapping[str, str]]
