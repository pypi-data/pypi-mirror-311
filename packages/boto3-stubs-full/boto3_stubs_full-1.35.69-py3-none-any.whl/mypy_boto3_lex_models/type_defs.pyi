"""
Type annotations for lex-models service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/type_defs/)

Usage::

    ```python
    from mypy_boto3_lex_models.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ChannelStatusType,
    ChannelTypeType,
    ContentTypeType,
    DestinationType,
    ExportStatusType,
    ExportTypeType,
    FulfillmentActivityTypeType,
    ImportStatusType,
    LocaleType,
    LogTypeType,
    MergeStrategyType,
    MigrationAlertTypeType,
    MigrationSortAttributeType,
    MigrationStatusType,
    MigrationStrategyType,
    ObfuscationSettingType,
    ProcessBehaviorType,
    ResourceTypeType,
    SlotConstraintType,
    SlotValueSelectionStrategyType,
    SortOrderType,
    StatusType,
    StatusTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BlobTypeDef",
    "BotAliasMetadataTypeDef",
    "BotChannelAssociationTypeDef",
    "BotMetadataTypeDef",
    "BuiltinIntentMetadataTypeDef",
    "BuiltinIntentSlotTypeDef",
    "BuiltinSlotTypeMetadataTypeDef",
    "CodeHookTypeDef",
    "ConversationLogsRequestTypeDef",
    "ConversationLogsResponseTypeDef",
    "CreateBotVersionRequestRequestTypeDef",
    "CreateBotVersionResponseTypeDef",
    "CreateIntentVersionRequestRequestTypeDef",
    "CreateIntentVersionResponseTypeDef",
    "CreateSlotTypeVersionRequestRequestTypeDef",
    "CreateSlotTypeVersionResponseTypeDef",
    "DeleteBotAliasRequestRequestTypeDef",
    "DeleteBotChannelAssociationRequestRequestTypeDef",
    "DeleteBotRequestRequestTypeDef",
    "DeleteBotVersionRequestRequestTypeDef",
    "DeleteIntentRequestRequestTypeDef",
    "DeleteIntentVersionRequestRequestTypeDef",
    "DeleteSlotTypeRequestRequestTypeDef",
    "DeleteSlotTypeVersionRequestRequestTypeDef",
    "DeleteUtterancesRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnumerationValueOutputTypeDef",
    "EnumerationValueTypeDef",
    "EnumerationValueUnionTypeDef",
    "FollowUpPromptOutputTypeDef",
    "FollowUpPromptTypeDef",
    "FulfillmentActivityTypeDef",
    "GetBotAliasRequestRequestTypeDef",
    "GetBotAliasResponseTypeDef",
    "GetBotAliasesRequestGetBotAliasesPaginateTypeDef",
    "GetBotAliasesRequestRequestTypeDef",
    "GetBotAliasesResponseTypeDef",
    "GetBotChannelAssociationRequestRequestTypeDef",
    "GetBotChannelAssociationResponseTypeDef",
    "GetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef",
    "GetBotChannelAssociationsRequestRequestTypeDef",
    "GetBotChannelAssociationsResponseTypeDef",
    "GetBotRequestRequestTypeDef",
    "GetBotResponseTypeDef",
    "GetBotVersionsRequestGetBotVersionsPaginateTypeDef",
    "GetBotVersionsRequestRequestTypeDef",
    "GetBotVersionsResponseTypeDef",
    "GetBotsRequestGetBotsPaginateTypeDef",
    "GetBotsRequestRequestTypeDef",
    "GetBotsResponseTypeDef",
    "GetBuiltinIntentRequestRequestTypeDef",
    "GetBuiltinIntentResponseTypeDef",
    "GetBuiltinIntentsRequestGetBuiltinIntentsPaginateTypeDef",
    "GetBuiltinIntentsRequestRequestTypeDef",
    "GetBuiltinIntentsResponseTypeDef",
    "GetBuiltinSlotTypesRequestGetBuiltinSlotTypesPaginateTypeDef",
    "GetBuiltinSlotTypesRequestRequestTypeDef",
    "GetBuiltinSlotTypesResponseTypeDef",
    "GetExportRequestRequestTypeDef",
    "GetExportResponseTypeDef",
    "GetImportRequestRequestTypeDef",
    "GetImportResponseTypeDef",
    "GetIntentRequestRequestTypeDef",
    "GetIntentResponseTypeDef",
    "GetIntentVersionsRequestGetIntentVersionsPaginateTypeDef",
    "GetIntentVersionsRequestRequestTypeDef",
    "GetIntentVersionsResponseTypeDef",
    "GetIntentsRequestGetIntentsPaginateTypeDef",
    "GetIntentsRequestRequestTypeDef",
    "GetIntentsResponseTypeDef",
    "GetMigrationRequestRequestTypeDef",
    "GetMigrationResponseTypeDef",
    "GetMigrationsRequestRequestTypeDef",
    "GetMigrationsResponseTypeDef",
    "GetSlotTypeRequestRequestTypeDef",
    "GetSlotTypeResponseTypeDef",
    "GetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef",
    "GetSlotTypeVersionsRequestRequestTypeDef",
    "GetSlotTypeVersionsResponseTypeDef",
    "GetSlotTypesRequestGetSlotTypesPaginateTypeDef",
    "GetSlotTypesRequestRequestTypeDef",
    "GetSlotTypesResponseTypeDef",
    "GetUtterancesViewRequestRequestTypeDef",
    "GetUtterancesViewResponseTypeDef",
    "InputContextTypeDef",
    "IntentMetadataTypeDef",
    "IntentTypeDef",
    "KendraConfigurationTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogSettingsRequestTypeDef",
    "LogSettingsResponseTypeDef",
    "MessageTypeDef",
    "MigrationAlertTypeDef",
    "MigrationSummaryTypeDef",
    "OutputContextTypeDef",
    "PaginatorConfigTypeDef",
    "PromptOutputTypeDef",
    "PromptTypeDef",
    "PromptUnionTypeDef",
    "PutBotAliasRequestRequestTypeDef",
    "PutBotAliasResponseTypeDef",
    "PutBotRequestRequestTypeDef",
    "PutBotResponseTypeDef",
    "PutIntentRequestRequestTypeDef",
    "PutIntentResponseTypeDef",
    "PutSlotTypeRequestRequestTypeDef",
    "PutSlotTypeResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SlotDefaultValueSpecOutputTypeDef",
    "SlotDefaultValueSpecTypeDef",
    "SlotDefaultValueSpecUnionTypeDef",
    "SlotDefaultValueTypeDef",
    "SlotOutputTypeDef",
    "SlotTypeConfigurationTypeDef",
    "SlotTypeDef",
    "SlotTypeMetadataTypeDef",
    "SlotTypeRegexConfigurationTypeDef",
    "SlotUnionTypeDef",
    "StartImportRequestRequestTypeDef",
    "StartImportResponseTypeDef",
    "StartMigrationRequestRequestTypeDef",
    "StartMigrationResponseTypeDef",
    "StatementOutputTypeDef",
    "StatementTypeDef",
    "StatementUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UtteranceDataTypeDef",
    "UtteranceListTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
BotChannelAssociationTypeDef = TypedDict(
    "BotChannelAssociationTypeDef",
    {
        "name": NotRequired[str],
        "description": NotRequired[str],
        "botAlias": NotRequired[str],
        "botName": NotRequired[str],
        "createdDate": NotRequired[datetime],
        "type": NotRequired[ChannelTypeType],
        "botConfiguration": NotRequired[Dict[str, str]],
        "status": NotRequired[ChannelStatusType],
        "failureReason": NotRequired[str],
    },
)

class BotMetadataTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[StatusType]
    lastUpdatedDate: NotRequired[datetime]
    createdDate: NotRequired[datetime]
    version: NotRequired[str]

class BuiltinIntentMetadataTypeDef(TypedDict):
    signature: NotRequired[str]
    supportedLocales: NotRequired[List[LocaleType]]

class BuiltinIntentSlotTypeDef(TypedDict):
    name: NotRequired[str]

class BuiltinSlotTypeMetadataTypeDef(TypedDict):
    signature: NotRequired[str]
    supportedLocales: NotRequired[List[LocaleType]]

class CodeHookTypeDef(TypedDict):
    uri: str
    messageVersion: str

class LogSettingsRequestTypeDef(TypedDict):
    logType: LogTypeType
    destination: DestinationType
    resourceArn: str
    kmsKeyArn: NotRequired[str]

class LogSettingsResponseTypeDef(TypedDict):
    logType: NotRequired[LogTypeType]
    destination: NotRequired[DestinationType]
    kmsKeyArn: NotRequired[str]
    resourceArn: NotRequired[str]
    resourcePrefix: NotRequired[str]

class CreateBotVersionRequestRequestTypeDef(TypedDict):
    name: str
    checksum: NotRequired[str]

class IntentTypeDef(TypedDict):
    intentName: str
    intentVersion: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateIntentVersionRequestRequestTypeDef(TypedDict):
    name: str
    checksum: NotRequired[str]

class InputContextTypeDef(TypedDict):
    name: str

class KendraConfigurationTypeDef(TypedDict):
    kendraIndex: str
    role: str
    queryFilterString: NotRequired[str]

class OutputContextTypeDef(TypedDict):
    name: str
    timeToLiveInSeconds: int
    turnsToLive: int

class CreateSlotTypeVersionRequestRequestTypeDef(TypedDict):
    name: str
    checksum: NotRequired[str]

class EnumerationValueOutputTypeDef(TypedDict):
    value: str
    synonyms: NotRequired[List[str]]

class DeleteBotAliasRequestRequestTypeDef(TypedDict):
    name: str
    botName: str

class DeleteBotChannelAssociationRequestRequestTypeDef(TypedDict):
    name: str
    botName: str
    botAlias: str

class DeleteBotRequestRequestTypeDef(TypedDict):
    name: str

class DeleteBotVersionRequestRequestTypeDef(TypedDict):
    name: str
    version: str

class DeleteIntentRequestRequestTypeDef(TypedDict):
    name: str

class DeleteIntentVersionRequestRequestTypeDef(TypedDict):
    name: str
    version: str

class DeleteSlotTypeRequestRequestTypeDef(TypedDict):
    name: str

class DeleteSlotTypeVersionRequestRequestTypeDef(TypedDict):
    name: str
    version: str

class DeleteUtterancesRequestRequestTypeDef(TypedDict):
    botName: str
    userId: str

class EnumerationValueTypeDef(TypedDict):
    value: str
    synonyms: NotRequired[Sequence[str]]

class GetBotAliasRequestRequestTypeDef(TypedDict):
    name: str
    botName: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetBotAliasesRequestRequestTypeDef(TypedDict):
    botName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    nameContains: NotRequired[str]

class GetBotChannelAssociationRequestRequestTypeDef(TypedDict):
    name: str
    botName: str
    botAlias: str

class GetBotChannelAssociationsRequestRequestTypeDef(TypedDict):
    botName: str
    botAlias: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    nameContains: NotRequired[str]

class GetBotRequestRequestTypeDef(TypedDict):
    name: str
    versionOrAlias: str

class GetBotVersionsRequestRequestTypeDef(TypedDict):
    name: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetBotsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    nameContains: NotRequired[str]

class GetBuiltinIntentRequestRequestTypeDef(TypedDict):
    signature: str

class GetBuiltinIntentsRequestRequestTypeDef(TypedDict):
    locale: NotRequired[LocaleType]
    signatureContains: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetBuiltinSlotTypesRequestRequestTypeDef(TypedDict):
    locale: NotRequired[LocaleType]
    signatureContains: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetExportRequestRequestTypeDef(TypedDict):
    name: str
    version: str
    resourceType: ResourceTypeType
    exportType: ExportTypeType

class GetImportRequestRequestTypeDef(TypedDict):
    importId: str

class GetIntentRequestRequestTypeDef(TypedDict):
    name: str
    version: str

class GetIntentVersionsRequestRequestTypeDef(TypedDict):
    name: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class IntentMetadataTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedDate: NotRequired[datetime]
    createdDate: NotRequired[datetime]
    version: NotRequired[str]

class GetIntentsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    nameContains: NotRequired[str]

class GetMigrationRequestRequestTypeDef(TypedDict):
    migrationId: str

MigrationAlertTypeDef = TypedDict(
    "MigrationAlertTypeDef",
    {
        "type": NotRequired[MigrationAlertTypeType],
        "message": NotRequired[str],
        "details": NotRequired[List[str]],
        "referenceURLs": NotRequired[List[str]],
    },
)

class GetMigrationsRequestRequestTypeDef(TypedDict):
    sortByAttribute: NotRequired[MigrationSortAttributeType]
    sortByOrder: NotRequired[SortOrderType]
    v1BotNameContains: NotRequired[str]
    migrationStatusEquals: NotRequired[MigrationStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class MigrationSummaryTypeDef(TypedDict):
    migrationId: NotRequired[str]
    v1BotName: NotRequired[str]
    v1BotVersion: NotRequired[str]
    v1BotLocale: NotRequired[LocaleType]
    v2BotId: NotRequired[str]
    v2BotRole: NotRequired[str]
    migrationStatus: NotRequired[MigrationStatusType]
    migrationStrategy: NotRequired[MigrationStrategyType]
    migrationTimestamp: NotRequired[datetime]

class GetSlotTypeRequestRequestTypeDef(TypedDict):
    name: str
    version: str

class GetSlotTypeVersionsRequestRequestTypeDef(TypedDict):
    name: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class SlotTypeMetadataTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedDate: NotRequired[datetime]
    createdDate: NotRequired[datetime]
    version: NotRequired[str]

class GetSlotTypesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    nameContains: NotRequired[str]

class GetUtterancesViewRequestRequestTypeDef(TypedDict):
    botName: str
    botVersions: Sequence[str]
    statusType: StatusTypeType

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class TagTypeDef(TypedDict):
    key: str
    value: str

class MessageTypeDef(TypedDict):
    contentType: ContentTypeType
    content: str
    groupNumber: NotRequired[int]

class SlotDefaultValueTypeDef(TypedDict):
    defaultValue: str

class SlotTypeRegexConfigurationTypeDef(TypedDict):
    pattern: str

class StartMigrationRequestRequestTypeDef(TypedDict):
    v1BotName: str
    v1BotVersion: str
    v2BotName: str
    v2BotRole: str
    migrationStrategy: MigrationStrategyType

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UtteranceDataTypeDef(TypedDict):
    utteranceString: NotRequired[str]
    count: NotRequired[int]
    distinctUsers: NotRequired[int]
    firstUtteredDate: NotRequired[datetime]
    lastUtteredDate: NotRequired[datetime]

FulfillmentActivityTypeDef = TypedDict(
    "FulfillmentActivityTypeDef",
    {
        "type": FulfillmentActivityTypeType,
        "codeHook": NotRequired[CodeHookTypeDef],
    },
)

class ConversationLogsRequestTypeDef(TypedDict):
    logSettings: Sequence[LogSettingsRequestTypeDef]
    iamRoleArn: str

class ConversationLogsResponseTypeDef(TypedDict):
    logSettings: NotRequired[List[LogSettingsResponseTypeDef]]
    iamRoleArn: NotRequired[str]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

GetBotChannelAssociationResponseTypeDef = TypedDict(
    "GetBotChannelAssociationResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botAlias": str,
        "botName": str,
        "createdDate": datetime,
        "type": ChannelTypeType,
        "botConfiguration": Dict[str, str],
        "status": ChannelStatusType,
        "failureReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetBotChannelAssociationsResponseTypeDef(TypedDict):
    botChannelAssociations: List[BotChannelAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetBotVersionsResponseTypeDef(TypedDict):
    bots: List[BotMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetBotsResponseTypeDef(TypedDict):
    bots: List[BotMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetBuiltinIntentResponseTypeDef(TypedDict):
    signature: str
    supportedLocales: List[LocaleType]
    slots: List[BuiltinIntentSlotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetBuiltinIntentsResponseTypeDef(TypedDict):
    intents: List[BuiltinIntentMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetBuiltinSlotTypesResponseTypeDef(TypedDict):
    slotTypes: List[BuiltinSlotTypeMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetExportResponseTypeDef(TypedDict):
    name: str
    version: str
    resourceType: ResourceTypeType
    exportType: ExportTypeType
    exportStatus: ExportStatusType
    failureReason: str
    url: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetImportResponseTypeDef(TypedDict):
    name: str
    resourceType: ResourceTypeType
    mergeStrategy: MergeStrategyType
    importId: str
    importStatus: ImportStatusType
    failureReason: List[str]
    createdDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StartMigrationResponseTypeDef(TypedDict):
    v1BotName: str
    v1BotVersion: str
    v1BotLocale: LocaleType
    v2BotId: str
    v2BotRole: str
    migrationId: str
    migrationStrategy: MigrationStrategyType
    migrationTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

EnumerationValueUnionTypeDef = Union[EnumerationValueTypeDef, EnumerationValueOutputTypeDef]

class GetBotAliasesRequestGetBotAliasesPaginateTypeDef(TypedDict):
    botName: str
    nameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef(TypedDict):
    botName: str
    botAlias: str
    nameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetBotVersionsRequestGetBotVersionsPaginateTypeDef(TypedDict):
    name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetBotsRequestGetBotsPaginateTypeDef(TypedDict):
    nameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetBuiltinIntentsRequestGetBuiltinIntentsPaginateTypeDef(TypedDict):
    locale: NotRequired[LocaleType]
    signatureContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetBuiltinSlotTypesRequestGetBuiltinSlotTypesPaginateTypeDef(TypedDict):
    locale: NotRequired[LocaleType]
    signatureContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetIntentVersionsRequestGetIntentVersionsPaginateTypeDef(TypedDict):
    name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetIntentsRequestGetIntentsPaginateTypeDef(TypedDict):
    nameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef(TypedDict):
    name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetSlotTypesRequestGetSlotTypesPaginateTypeDef(TypedDict):
    nameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetIntentVersionsResponseTypeDef(TypedDict):
    intents: List[IntentMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetIntentsResponseTypeDef(TypedDict):
    intents: List[IntentMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetMigrationResponseTypeDef(TypedDict):
    migrationId: str
    v1BotName: str
    v1BotVersion: str
    v1BotLocale: LocaleType
    v2BotId: str
    v2BotRole: str
    migrationStatus: MigrationStatusType
    migrationStrategy: MigrationStrategyType
    migrationTimestamp: datetime
    alerts: List[MigrationAlertTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetMigrationsResponseTypeDef(TypedDict):
    migrationSummaries: List[MigrationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetSlotTypeVersionsResponseTypeDef(TypedDict):
    slotTypes: List[SlotTypeMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetSlotTypesResponseTypeDef(TypedDict):
    slotTypes: List[SlotTypeMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartImportRequestRequestTypeDef(TypedDict):
    payload: BlobTypeDef
    resourceType: ResourceTypeType
    mergeStrategy: MergeStrategyType
    tags: NotRequired[Sequence[TagTypeDef]]

class StartImportResponseTypeDef(TypedDict):
    name: str
    resourceType: ResourceTypeType
    mergeStrategy: MergeStrategyType
    importId: str
    importStatus: ImportStatusType
    tags: List[TagTypeDef]
    createdDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class PromptOutputTypeDef(TypedDict):
    messages: List[MessageTypeDef]
    maxAttempts: int
    responseCard: NotRequired[str]

class PromptTypeDef(TypedDict):
    messages: Sequence[MessageTypeDef]
    maxAttempts: int
    responseCard: NotRequired[str]

class StatementOutputTypeDef(TypedDict):
    messages: List[MessageTypeDef]
    responseCard: NotRequired[str]

class StatementTypeDef(TypedDict):
    messages: Sequence[MessageTypeDef]
    responseCard: NotRequired[str]

class SlotDefaultValueSpecOutputTypeDef(TypedDict):
    defaultValueList: List[SlotDefaultValueTypeDef]

class SlotDefaultValueSpecTypeDef(TypedDict):
    defaultValueList: Sequence[SlotDefaultValueTypeDef]

class SlotTypeConfigurationTypeDef(TypedDict):
    regexConfiguration: NotRequired[SlotTypeRegexConfigurationTypeDef]

class UtteranceListTypeDef(TypedDict):
    botVersion: NotRequired[str]
    utterances: NotRequired[List[UtteranceDataTypeDef]]

class PutBotAliasRequestRequestTypeDef(TypedDict):
    name: str
    botVersion: str
    botName: str
    description: NotRequired[str]
    checksum: NotRequired[str]
    conversationLogs: NotRequired[ConversationLogsRequestTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]

class BotAliasMetadataTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    botVersion: NotRequired[str]
    botName: NotRequired[str]
    lastUpdatedDate: NotRequired[datetime]
    createdDate: NotRequired[datetime]
    checksum: NotRequired[str]
    conversationLogs: NotRequired[ConversationLogsResponseTypeDef]

class GetBotAliasResponseTypeDef(TypedDict):
    name: str
    description: str
    botVersion: str
    botName: str
    lastUpdatedDate: datetime
    createdDate: datetime
    checksum: str
    conversationLogs: ConversationLogsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutBotAliasResponseTypeDef(TypedDict):
    name: str
    description: str
    botVersion: str
    botName: str
    lastUpdatedDate: datetime
    createdDate: datetime
    checksum: str
    conversationLogs: ConversationLogsResponseTypeDef
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

PromptUnionTypeDef = Union[PromptTypeDef, PromptOutputTypeDef]

class CreateBotVersionResponseTypeDef(TypedDict):
    name: str
    description: str
    intents: List[IntentTypeDef]
    clarificationPrompt: PromptOutputTypeDef
    abortStatement: StatementOutputTypeDef
    status: StatusType
    failureReason: str
    lastUpdatedDate: datetime
    createdDate: datetime
    idleSessionTTLInSeconds: int
    voiceId: str
    checksum: str
    version: str
    locale: LocaleType
    childDirected: bool
    enableModelImprovements: bool
    detectSentiment: bool
    ResponseMetadata: ResponseMetadataTypeDef

class FollowUpPromptOutputTypeDef(TypedDict):
    prompt: PromptOutputTypeDef
    rejectionStatement: StatementOutputTypeDef

class GetBotResponseTypeDef(TypedDict):
    name: str
    description: str
    intents: List[IntentTypeDef]
    enableModelImprovements: bool
    nluIntentConfidenceThreshold: float
    clarificationPrompt: PromptOutputTypeDef
    abortStatement: StatementOutputTypeDef
    status: StatusType
    failureReason: str
    lastUpdatedDate: datetime
    createdDate: datetime
    idleSessionTTLInSeconds: int
    voiceId: str
    checksum: str
    version: str
    locale: LocaleType
    childDirected: bool
    detectSentiment: bool
    ResponseMetadata: ResponseMetadataTypeDef

class PutBotResponseTypeDef(TypedDict):
    name: str
    description: str
    intents: List[IntentTypeDef]
    enableModelImprovements: bool
    nluIntentConfidenceThreshold: float
    clarificationPrompt: PromptOutputTypeDef
    abortStatement: StatementOutputTypeDef
    status: StatusType
    failureReason: str
    lastUpdatedDate: datetime
    createdDate: datetime
    idleSessionTTLInSeconds: int
    voiceId: str
    checksum: str
    version: str
    locale: LocaleType
    childDirected: bool
    createVersion: bool
    detectSentiment: bool
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutBotRequestRequestTypeDef(TypedDict):
    name: str
    locale: LocaleType
    childDirected: bool
    description: NotRequired[str]
    intents: NotRequired[Sequence[IntentTypeDef]]
    enableModelImprovements: NotRequired[bool]
    nluIntentConfidenceThreshold: NotRequired[float]
    clarificationPrompt: NotRequired[PromptTypeDef]
    abortStatement: NotRequired[StatementTypeDef]
    idleSessionTTLInSeconds: NotRequired[int]
    voiceId: NotRequired[str]
    checksum: NotRequired[str]
    processBehavior: NotRequired[ProcessBehaviorType]
    detectSentiment: NotRequired[bool]
    createVersion: NotRequired[bool]
    tags: NotRequired[Sequence[TagTypeDef]]

StatementUnionTypeDef = Union[StatementTypeDef, StatementOutputTypeDef]

class SlotOutputTypeDef(TypedDict):
    name: str
    slotConstraint: SlotConstraintType
    description: NotRequired[str]
    slotType: NotRequired[str]
    slotTypeVersion: NotRequired[str]
    valueElicitationPrompt: NotRequired[PromptOutputTypeDef]
    priority: NotRequired[int]
    sampleUtterances: NotRequired[List[str]]
    responseCard: NotRequired[str]
    obfuscationSetting: NotRequired[ObfuscationSettingType]
    defaultValueSpec: NotRequired[SlotDefaultValueSpecOutputTypeDef]

SlotDefaultValueSpecUnionTypeDef = Union[
    SlotDefaultValueSpecTypeDef, SlotDefaultValueSpecOutputTypeDef
]

class CreateSlotTypeVersionResponseTypeDef(TypedDict):
    name: str
    description: str
    enumerationValues: List[EnumerationValueOutputTypeDef]
    lastUpdatedDate: datetime
    createdDate: datetime
    version: str
    checksum: str
    valueSelectionStrategy: SlotValueSelectionStrategyType
    parentSlotTypeSignature: str
    slotTypeConfigurations: List[SlotTypeConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSlotTypeResponseTypeDef(TypedDict):
    name: str
    description: str
    enumerationValues: List[EnumerationValueOutputTypeDef]
    lastUpdatedDate: datetime
    createdDate: datetime
    version: str
    checksum: str
    valueSelectionStrategy: SlotValueSelectionStrategyType
    parentSlotTypeSignature: str
    slotTypeConfigurations: List[SlotTypeConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutSlotTypeRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    enumerationValues: NotRequired[Sequence[EnumerationValueUnionTypeDef]]
    checksum: NotRequired[str]
    valueSelectionStrategy: NotRequired[SlotValueSelectionStrategyType]
    createVersion: NotRequired[bool]
    parentSlotTypeSignature: NotRequired[str]
    slotTypeConfigurations: NotRequired[Sequence[SlotTypeConfigurationTypeDef]]

class PutSlotTypeResponseTypeDef(TypedDict):
    name: str
    description: str
    enumerationValues: List[EnumerationValueOutputTypeDef]
    lastUpdatedDate: datetime
    createdDate: datetime
    version: str
    checksum: str
    valueSelectionStrategy: SlotValueSelectionStrategyType
    createVersion: bool
    parentSlotTypeSignature: str
    slotTypeConfigurations: List[SlotTypeConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetUtterancesViewResponseTypeDef(TypedDict):
    botName: str
    utterances: List[UtteranceListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetBotAliasesResponseTypeDef(TypedDict):
    BotAliases: List[BotAliasMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FollowUpPromptTypeDef(TypedDict):
    prompt: PromptUnionTypeDef
    rejectionStatement: StatementUnionTypeDef

class CreateIntentVersionResponseTypeDef(TypedDict):
    name: str
    description: str
    slots: List[SlotOutputTypeDef]
    sampleUtterances: List[str]
    confirmationPrompt: PromptOutputTypeDef
    rejectionStatement: StatementOutputTypeDef
    followUpPrompt: FollowUpPromptOutputTypeDef
    conclusionStatement: StatementOutputTypeDef
    dialogCodeHook: CodeHookTypeDef
    fulfillmentActivity: FulfillmentActivityTypeDef
    parentIntentSignature: str
    lastUpdatedDate: datetime
    createdDate: datetime
    version: str
    checksum: str
    kendraConfiguration: KendraConfigurationTypeDef
    inputContexts: List[InputContextTypeDef]
    outputContexts: List[OutputContextTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetIntentResponseTypeDef(TypedDict):
    name: str
    description: str
    slots: List[SlotOutputTypeDef]
    sampleUtterances: List[str]
    confirmationPrompt: PromptOutputTypeDef
    rejectionStatement: StatementOutputTypeDef
    followUpPrompt: FollowUpPromptOutputTypeDef
    conclusionStatement: StatementOutputTypeDef
    dialogCodeHook: CodeHookTypeDef
    fulfillmentActivity: FulfillmentActivityTypeDef
    parentIntentSignature: str
    lastUpdatedDate: datetime
    createdDate: datetime
    version: str
    checksum: str
    kendraConfiguration: KendraConfigurationTypeDef
    inputContexts: List[InputContextTypeDef]
    outputContexts: List[OutputContextTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutIntentResponseTypeDef(TypedDict):
    name: str
    description: str
    slots: List[SlotOutputTypeDef]
    sampleUtterances: List[str]
    confirmationPrompt: PromptOutputTypeDef
    rejectionStatement: StatementOutputTypeDef
    followUpPrompt: FollowUpPromptOutputTypeDef
    conclusionStatement: StatementOutputTypeDef
    dialogCodeHook: CodeHookTypeDef
    fulfillmentActivity: FulfillmentActivityTypeDef
    parentIntentSignature: str
    lastUpdatedDate: datetime
    createdDate: datetime
    version: str
    checksum: str
    createVersion: bool
    kendraConfiguration: KendraConfigurationTypeDef
    inputContexts: List[InputContextTypeDef]
    outputContexts: List[OutputContextTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SlotTypeDef(TypedDict):
    name: str
    slotConstraint: SlotConstraintType
    description: NotRequired[str]
    slotType: NotRequired[str]
    slotTypeVersion: NotRequired[str]
    valueElicitationPrompt: NotRequired[PromptUnionTypeDef]
    priority: NotRequired[int]
    sampleUtterances: NotRequired[Sequence[str]]
    responseCard: NotRequired[str]
    obfuscationSetting: NotRequired[ObfuscationSettingType]
    defaultValueSpec: NotRequired[SlotDefaultValueSpecUnionTypeDef]

SlotUnionTypeDef = Union[SlotTypeDef, SlotOutputTypeDef]

class PutIntentRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    slots: NotRequired[Sequence[SlotUnionTypeDef]]
    sampleUtterances: NotRequired[Sequence[str]]
    confirmationPrompt: NotRequired[PromptTypeDef]
    rejectionStatement: NotRequired[StatementTypeDef]
    followUpPrompt: NotRequired[FollowUpPromptTypeDef]
    conclusionStatement: NotRequired[StatementTypeDef]
    dialogCodeHook: NotRequired[CodeHookTypeDef]
    fulfillmentActivity: NotRequired[FulfillmentActivityTypeDef]
    parentIntentSignature: NotRequired[str]
    checksum: NotRequired[str]
    createVersion: NotRequired[bool]
    kendraConfiguration: NotRequired[KendraConfigurationTypeDef]
    inputContexts: NotRequired[Sequence[InputContextTypeDef]]
    outputContexts: NotRequired[Sequence[OutputContextTypeDef]]
