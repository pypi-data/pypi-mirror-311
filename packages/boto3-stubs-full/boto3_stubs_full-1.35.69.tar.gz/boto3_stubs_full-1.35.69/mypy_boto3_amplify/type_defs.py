"""
Type annotations for amplify service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/type_defs/)

Usage::

    ```python
    from mypy_boto3_amplify.type_defs import AutoBranchCreationConfigOutputTypeDef

    data: AutoBranchCreationConfigOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    CacheConfigTypeType,
    CertificateTypeType,
    DomainStatusType,
    JobStatusType,
    JobTypeType,
    PlatformType,
    RepositoryCloneMethodType,
    SourceUrlTypeType,
    StageType,
    UpdateStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AppTypeDef",
    "ArtifactTypeDef",
    "AutoBranchCreationConfigOutputTypeDef",
    "AutoBranchCreationConfigTypeDef",
    "BackendEnvironmentTypeDef",
    "BackendTypeDef",
    "BranchTypeDef",
    "CacheConfigTypeDef",
    "CertificateSettingsTypeDef",
    "CertificateTypeDef",
    "CreateAppRequestRequestTypeDef",
    "CreateAppResultTypeDef",
    "CreateBackendEnvironmentRequestRequestTypeDef",
    "CreateBackendEnvironmentResultTypeDef",
    "CreateBranchRequestRequestTypeDef",
    "CreateBranchResultTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "CreateDeploymentResultTypeDef",
    "CreateDomainAssociationRequestRequestTypeDef",
    "CreateDomainAssociationResultTypeDef",
    "CreateWebhookRequestRequestTypeDef",
    "CreateWebhookResultTypeDef",
    "CustomRuleTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteAppResultTypeDef",
    "DeleteBackendEnvironmentRequestRequestTypeDef",
    "DeleteBackendEnvironmentResultTypeDef",
    "DeleteBranchRequestRequestTypeDef",
    "DeleteBranchResultTypeDef",
    "DeleteDomainAssociationRequestRequestTypeDef",
    "DeleteDomainAssociationResultTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteJobResultTypeDef",
    "DeleteWebhookRequestRequestTypeDef",
    "DeleteWebhookResultTypeDef",
    "DomainAssociationTypeDef",
    "GenerateAccessLogsRequestRequestTypeDef",
    "GenerateAccessLogsResultTypeDef",
    "GetAppRequestRequestTypeDef",
    "GetAppResultTypeDef",
    "GetArtifactUrlRequestRequestTypeDef",
    "GetArtifactUrlResultTypeDef",
    "GetBackendEnvironmentRequestRequestTypeDef",
    "GetBackendEnvironmentResultTypeDef",
    "GetBranchRequestRequestTypeDef",
    "GetBranchResultTypeDef",
    "GetDomainAssociationRequestRequestTypeDef",
    "GetDomainAssociationResultTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetJobResultTypeDef",
    "GetWebhookRequestRequestTypeDef",
    "GetWebhookResultTypeDef",
    "JobSummaryTypeDef",
    "JobTypeDef",
    "ListAppsRequestListAppsPaginateTypeDef",
    "ListAppsRequestRequestTypeDef",
    "ListAppsResultTypeDef",
    "ListArtifactsRequestRequestTypeDef",
    "ListArtifactsResultTypeDef",
    "ListBackendEnvironmentsRequestRequestTypeDef",
    "ListBackendEnvironmentsResultTypeDef",
    "ListBranchesRequestListBranchesPaginateTypeDef",
    "ListBranchesRequestRequestTypeDef",
    "ListBranchesResultTypeDef",
    "ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef",
    "ListDomainAssociationsRequestRequestTypeDef",
    "ListDomainAssociationsResultTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListJobsResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWebhooksRequestRequestTypeDef",
    "ListWebhooksResultTypeDef",
    "PaginatorConfigTypeDef",
    "ProductionBranchTypeDef",
    "ResponseMetadataTypeDef",
    "StartDeploymentRequestRequestTypeDef",
    "StartDeploymentResultTypeDef",
    "StartJobRequestRequestTypeDef",
    "StartJobResultTypeDef",
    "StepTypeDef",
    "StopJobRequestRequestTypeDef",
    "StopJobResultTypeDef",
    "SubDomainSettingTypeDef",
    "SubDomainTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppRequestRequestTypeDef",
    "UpdateAppResultTypeDef",
    "UpdateBranchRequestRequestTypeDef",
    "UpdateBranchResultTypeDef",
    "UpdateDomainAssociationRequestRequestTypeDef",
    "UpdateDomainAssociationResultTypeDef",
    "UpdateWebhookRequestRequestTypeDef",
    "UpdateWebhookResultTypeDef",
    "WebhookTypeDef",
)


class AutoBranchCreationConfigOutputTypeDef(TypedDict):
    stage: NotRequired[StageType]
    framework: NotRequired[str]
    enableAutoBuild: NotRequired[bool]
    environmentVariables: NotRequired[Dict[str, str]]
    basicAuthCredentials: NotRequired[str]
    enableBasicAuth: NotRequired[bool]
    enablePerformanceMode: NotRequired[bool]
    buildSpec: NotRequired[str]
    enablePullRequestPreview: NotRequired[bool]
    pullRequestEnvironmentName: NotRequired[str]


CacheConfigTypeDef = TypedDict(
    "CacheConfigTypeDef",
    {
        "type": CacheConfigTypeType,
    },
)


class CustomRuleTypeDef(TypedDict):
    source: str
    target: str
    status: NotRequired[str]
    condition: NotRequired[str]


class ProductionBranchTypeDef(TypedDict):
    lastDeployTime: NotRequired[datetime]
    status: NotRequired[str]
    thumbnailUrl: NotRequired[str]
    branchName: NotRequired[str]


class ArtifactTypeDef(TypedDict):
    artifactFileName: str
    artifactId: str


class AutoBranchCreationConfigTypeDef(TypedDict):
    stage: NotRequired[StageType]
    framework: NotRequired[str]
    enableAutoBuild: NotRequired[bool]
    environmentVariables: NotRequired[Mapping[str, str]]
    basicAuthCredentials: NotRequired[str]
    enableBasicAuth: NotRequired[bool]
    enablePerformanceMode: NotRequired[bool]
    buildSpec: NotRequired[str]
    enablePullRequestPreview: NotRequired[bool]
    pullRequestEnvironmentName: NotRequired[str]


class BackendEnvironmentTypeDef(TypedDict):
    backendEnvironmentArn: str
    environmentName: str
    createTime: datetime
    updateTime: datetime
    stackName: NotRequired[str]
    deploymentArtifacts: NotRequired[str]


class BackendTypeDef(TypedDict):
    stackArn: NotRequired[str]


CertificateSettingsTypeDef = TypedDict(
    "CertificateSettingsTypeDef",
    {
        "type": CertificateTypeType,
        "customCertificateArn": NotRequired[str],
    },
)
CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "type": CertificateTypeType,
        "customCertificateArn": NotRequired[str],
        "certificateVerificationDNSRecord": NotRequired[str],
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateBackendEnvironmentRequestRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    stackName: NotRequired[str]
    deploymentArtifacts: NotRequired[str]


class CreateDeploymentRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    fileMap: NotRequired[Mapping[str, str]]


class SubDomainSettingTypeDef(TypedDict):
    prefix: str
    branchName: str


class CreateWebhookRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    description: NotRequired[str]


class WebhookTypeDef(TypedDict):
    webhookArn: str
    webhookId: str
    webhookUrl: str
    branchName: str
    description: str
    createTime: datetime
    updateTime: datetime


class DeleteAppRequestRequestTypeDef(TypedDict):
    appId: str


class DeleteBackendEnvironmentRequestRequestTypeDef(TypedDict):
    appId: str
    environmentName: str


class DeleteBranchRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str


class DeleteDomainAssociationRequestRequestTypeDef(TypedDict):
    appId: str
    domainName: str


class DeleteJobRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    jobId: str


class JobSummaryTypeDef(TypedDict):
    jobArn: str
    jobId: str
    commitId: str
    commitMessage: str
    commitTime: datetime
    startTime: datetime
    status: JobStatusType
    jobType: JobTypeType
    endTime: NotRequired[datetime]
    sourceUrl: NotRequired[str]
    sourceUrlType: NotRequired[SourceUrlTypeType]


class DeleteWebhookRequestRequestTypeDef(TypedDict):
    webhookId: str


TimestampTypeDef = Union[datetime, str]


class GetAppRequestRequestTypeDef(TypedDict):
    appId: str


class GetArtifactUrlRequestRequestTypeDef(TypedDict):
    artifactId: str


class GetBackendEnvironmentRequestRequestTypeDef(TypedDict):
    appId: str
    environmentName: str


class GetBranchRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str


class GetDomainAssociationRequestRequestTypeDef(TypedDict):
    appId: str
    domainName: str


class GetJobRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    jobId: str


class GetWebhookRequestRequestTypeDef(TypedDict):
    webhookId: str


class StepTypeDef(TypedDict):
    stepName: str
    startTime: datetime
    status: JobStatusType
    endTime: datetime
    logUrl: NotRequired[str]
    artifactsUrl: NotRequired[str]
    testArtifactsUrl: NotRequired[str]
    testConfigUrl: NotRequired[str]
    screenshots: NotRequired[Dict[str, str]]
    statusReason: NotRequired[str]
    context: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAppsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListArtifactsRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    jobId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBackendEnvironmentsRequestRequestTypeDef(TypedDict):
    appId: str
    environmentName: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBranchesRequestRequestTypeDef(TypedDict):
    appId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDomainAssociationsRequestRequestTypeDef(TypedDict):
    appId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListJobsRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListWebhooksRequestRequestTypeDef(TypedDict):
    appId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class StartDeploymentRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    jobId: NotRequired[str]
    sourceUrl: NotRequired[str]
    sourceUrlType: NotRequired[SourceUrlTypeType]


class StopJobRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    jobId: str


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateWebhookRequestRequestTypeDef(TypedDict):
    webhookId: str
    branchName: NotRequired[str]
    description: NotRequired[str]


class AppTypeDef(TypedDict):
    appId: str
    appArn: str
    name: str
    description: str
    repository: str
    platform: PlatformType
    createTime: datetime
    updateTime: datetime
    environmentVariables: Dict[str, str]
    defaultDomain: str
    enableBranchAutoBuild: bool
    enableBasicAuth: bool
    tags: NotRequired[Dict[str, str]]
    iamServiceRoleArn: NotRequired[str]
    enableBranchAutoDeletion: NotRequired[bool]
    basicAuthCredentials: NotRequired[str]
    customRules: NotRequired[List[CustomRuleTypeDef]]
    productionBranch: NotRequired[ProductionBranchTypeDef]
    buildSpec: NotRequired[str]
    customHeaders: NotRequired[str]
    enableAutoBranchCreation: NotRequired[bool]
    autoBranchCreationPatterns: NotRequired[List[str]]
    autoBranchCreationConfig: NotRequired[AutoBranchCreationConfigOutputTypeDef]
    repositoryCloneMethod: NotRequired[RepositoryCloneMethodType]
    cacheConfig: NotRequired[CacheConfigTypeDef]


class CreateAppRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    repository: NotRequired[str]
    platform: NotRequired[PlatformType]
    iamServiceRoleArn: NotRequired[str]
    oauthToken: NotRequired[str]
    accessToken: NotRequired[str]
    environmentVariables: NotRequired[Mapping[str, str]]
    enableBranchAutoBuild: NotRequired[bool]
    enableBranchAutoDeletion: NotRequired[bool]
    enableBasicAuth: NotRequired[bool]
    basicAuthCredentials: NotRequired[str]
    customRules: NotRequired[Sequence[CustomRuleTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    buildSpec: NotRequired[str]
    customHeaders: NotRequired[str]
    enableAutoBranchCreation: NotRequired[bool]
    autoBranchCreationPatterns: NotRequired[Sequence[str]]
    autoBranchCreationConfig: NotRequired[AutoBranchCreationConfigTypeDef]
    cacheConfig: NotRequired[CacheConfigTypeDef]


class UpdateAppRequestRequestTypeDef(TypedDict):
    appId: str
    name: NotRequired[str]
    description: NotRequired[str]
    platform: NotRequired[PlatformType]
    iamServiceRoleArn: NotRequired[str]
    environmentVariables: NotRequired[Mapping[str, str]]
    enableBranchAutoBuild: NotRequired[bool]
    enableBranchAutoDeletion: NotRequired[bool]
    enableBasicAuth: NotRequired[bool]
    basicAuthCredentials: NotRequired[str]
    customRules: NotRequired[Sequence[CustomRuleTypeDef]]
    buildSpec: NotRequired[str]
    customHeaders: NotRequired[str]
    enableAutoBranchCreation: NotRequired[bool]
    autoBranchCreationPatterns: NotRequired[Sequence[str]]
    autoBranchCreationConfig: NotRequired[AutoBranchCreationConfigTypeDef]
    repository: NotRequired[str]
    oauthToken: NotRequired[str]
    accessToken: NotRequired[str]
    cacheConfig: NotRequired[CacheConfigTypeDef]


class BranchTypeDef(TypedDict):
    branchArn: str
    branchName: str
    description: str
    stage: StageType
    displayName: str
    enableNotification: bool
    createTime: datetime
    updateTime: datetime
    environmentVariables: Dict[str, str]
    enableAutoBuild: bool
    customDomains: List[str]
    framework: str
    activeJobId: str
    totalNumberOfJobs: str
    enableBasicAuth: bool
    ttl: str
    enablePullRequestPreview: bool
    tags: NotRequired[Dict[str, str]]
    enablePerformanceMode: NotRequired[bool]
    thumbnailUrl: NotRequired[str]
    basicAuthCredentials: NotRequired[str]
    buildSpec: NotRequired[str]
    associatedResources: NotRequired[List[str]]
    pullRequestEnvironmentName: NotRequired[str]
    destinationBranch: NotRequired[str]
    sourceBranch: NotRequired[str]
    backendEnvironmentArn: NotRequired[str]
    backend: NotRequired[BackendTypeDef]


class CreateBranchRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    description: NotRequired[str]
    stage: NotRequired[StageType]
    framework: NotRequired[str]
    enableNotification: NotRequired[bool]
    enableAutoBuild: NotRequired[bool]
    environmentVariables: NotRequired[Mapping[str, str]]
    basicAuthCredentials: NotRequired[str]
    enableBasicAuth: NotRequired[bool]
    enablePerformanceMode: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]
    buildSpec: NotRequired[str]
    ttl: NotRequired[str]
    displayName: NotRequired[str]
    enablePullRequestPreview: NotRequired[bool]
    pullRequestEnvironmentName: NotRequired[str]
    backendEnvironmentArn: NotRequired[str]
    backend: NotRequired[BackendTypeDef]


class UpdateBranchRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    description: NotRequired[str]
    framework: NotRequired[str]
    stage: NotRequired[StageType]
    enableNotification: NotRequired[bool]
    enableAutoBuild: NotRequired[bool]
    environmentVariables: NotRequired[Mapping[str, str]]
    basicAuthCredentials: NotRequired[str]
    enableBasicAuth: NotRequired[bool]
    enablePerformanceMode: NotRequired[bool]
    buildSpec: NotRequired[str]
    ttl: NotRequired[str]
    displayName: NotRequired[str]
    enablePullRequestPreview: NotRequired[bool]
    pullRequestEnvironmentName: NotRequired[str]
    backendEnvironmentArn: NotRequired[str]
    backend: NotRequired[BackendTypeDef]


class CreateBackendEnvironmentResultTypeDef(TypedDict):
    backendEnvironment: BackendEnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDeploymentResultTypeDef(TypedDict):
    jobId: str
    fileUploadUrls: Dict[str, str]
    zipUploadUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBackendEnvironmentResultTypeDef(TypedDict):
    backendEnvironment: BackendEnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateAccessLogsResultTypeDef(TypedDict):
    logUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetArtifactUrlResultTypeDef(TypedDict):
    artifactId: str
    artifactUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetBackendEnvironmentResultTypeDef(TypedDict):
    backendEnvironment: BackendEnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListArtifactsResultTypeDef(TypedDict):
    artifacts: List[ArtifactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBackendEnvironmentsResultTypeDef(TypedDict):
    backendEnvironments: List[BackendEnvironmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainAssociationRequestRequestTypeDef(TypedDict):
    appId: str
    domainName: str
    subDomainSettings: Sequence[SubDomainSettingTypeDef]
    enableAutoSubDomain: NotRequired[bool]
    autoSubDomainCreationPatterns: NotRequired[Sequence[str]]
    autoSubDomainIAMRole: NotRequired[str]
    certificateSettings: NotRequired[CertificateSettingsTypeDef]


class SubDomainTypeDef(TypedDict):
    subDomainSetting: SubDomainSettingTypeDef
    verified: bool
    dnsRecord: str


class UpdateDomainAssociationRequestRequestTypeDef(TypedDict):
    appId: str
    domainName: str
    enableAutoSubDomain: NotRequired[bool]
    subDomainSettings: NotRequired[Sequence[SubDomainSettingTypeDef]]
    autoSubDomainCreationPatterns: NotRequired[Sequence[str]]
    autoSubDomainIAMRole: NotRequired[str]
    certificateSettings: NotRequired[CertificateSettingsTypeDef]


class CreateWebhookResultTypeDef(TypedDict):
    webhook: WebhookTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWebhookResultTypeDef(TypedDict):
    webhook: WebhookTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetWebhookResultTypeDef(TypedDict):
    webhook: WebhookTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListWebhooksResultTypeDef(TypedDict):
    webhooks: List[WebhookTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateWebhookResultTypeDef(TypedDict):
    webhook: WebhookTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteJobResultTypeDef(TypedDict):
    jobSummary: JobSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListJobsResultTypeDef(TypedDict):
    jobSummaries: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartDeploymentResultTypeDef(TypedDict):
    jobSummary: JobSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartJobResultTypeDef(TypedDict):
    jobSummary: JobSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopJobResultTypeDef(TypedDict):
    jobSummary: JobSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateAccessLogsRequestRequestTypeDef(TypedDict):
    domainName: str
    appId: str
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]


class StartJobRequestRequestTypeDef(TypedDict):
    appId: str
    branchName: str
    jobType: JobTypeType
    jobId: NotRequired[str]
    jobReason: NotRequired[str]
    commitId: NotRequired[str]
    commitMessage: NotRequired[str]
    commitTime: NotRequired[TimestampTypeDef]


class JobTypeDef(TypedDict):
    summary: JobSummaryTypeDef
    steps: List[StepTypeDef]


class ListAppsRequestListAppsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBranchesRequestListBranchesPaginateTypeDef(TypedDict):
    appId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef(TypedDict):
    appId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobsRequestListJobsPaginateTypeDef(TypedDict):
    appId: str
    branchName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class CreateAppResultTypeDef(TypedDict):
    app: AppTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAppResultTypeDef(TypedDict):
    app: AppTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAppResultTypeDef(TypedDict):
    app: AppTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAppsResultTypeDef(TypedDict):
    apps: List[AppTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateAppResultTypeDef(TypedDict):
    app: AppTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBranchResultTypeDef(TypedDict):
    branch: BranchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBranchResultTypeDef(TypedDict):
    branch: BranchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetBranchResultTypeDef(TypedDict):
    branch: BranchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListBranchesResultTypeDef(TypedDict):
    branches: List[BranchTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateBranchResultTypeDef(TypedDict):
    branch: BranchTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DomainAssociationTypeDef(TypedDict):
    domainAssociationArn: str
    domainName: str
    enableAutoSubDomain: bool
    domainStatus: DomainStatusType
    statusReason: str
    subDomains: List[SubDomainTypeDef]
    autoSubDomainCreationPatterns: NotRequired[List[str]]
    autoSubDomainIAMRole: NotRequired[str]
    updateStatus: NotRequired[UpdateStatusType]
    certificateVerificationDNSRecord: NotRequired[str]
    certificate: NotRequired[CertificateTypeDef]


class GetJobResultTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainAssociationResultTypeDef(TypedDict):
    domainAssociation: DomainAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDomainAssociationResultTypeDef(TypedDict):
    domainAssociation: DomainAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDomainAssociationResultTypeDef(TypedDict):
    domainAssociation: DomainAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDomainAssociationsResultTypeDef(TypedDict):
    domainAssociations: List[DomainAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateDomainAssociationResultTypeDef(TypedDict):
    domainAssociation: DomainAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
