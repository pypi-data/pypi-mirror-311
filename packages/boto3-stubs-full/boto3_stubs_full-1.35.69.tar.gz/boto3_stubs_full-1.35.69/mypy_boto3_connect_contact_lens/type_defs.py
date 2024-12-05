"""
Type annotations for connect-contact-lens service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect_contact_lens/type_defs/)

Usage::

    ```python
    from mypy_boto3_connect_contact_lens.type_defs import PointOfInterestTypeDef

    data: PointOfInterestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List

from .literals import (
    PostContactSummaryFailureCodeType,
    PostContactSummaryStatusType,
    SentimentValueType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CategoriesTypeDef",
    "CategoryDetailsTypeDef",
    "CharacterOffsetsTypeDef",
    "IssueDetectedTypeDef",
    "ListRealtimeContactAnalysisSegmentsRequestRequestTypeDef",
    "ListRealtimeContactAnalysisSegmentsResponseTypeDef",
    "PointOfInterestTypeDef",
    "PostContactSummaryTypeDef",
    "RealtimeContactAnalysisSegmentTypeDef",
    "ResponseMetadataTypeDef",
    "TranscriptTypeDef",
)


class PointOfInterestTypeDef(TypedDict):
    BeginOffsetMillis: int
    EndOffsetMillis: int


class CharacterOffsetsTypeDef(TypedDict):
    BeginOffsetChar: int
    EndOffsetChar: int


class ListRealtimeContactAnalysisSegmentsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class PostContactSummaryTypeDef(TypedDict):
    Status: PostContactSummaryStatusType
    Content: NotRequired[str]
    FailureCode: NotRequired[PostContactSummaryFailureCodeType]


class CategoryDetailsTypeDef(TypedDict):
    PointsOfInterest: List[PointOfInterestTypeDef]


class IssueDetectedTypeDef(TypedDict):
    CharacterOffsets: CharacterOffsetsTypeDef


class CategoriesTypeDef(TypedDict):
    MatchedCategories: List[str]
    MatchedDetails: Dict[str, CategoryDetailsTypeDef]


class TranscriptTypeDef(TypedDict):
    Id: str
    ParticipantId: str
    ParticipantRole: str
    Content: str
    BeginOffsetMillis: int
    EndOffsetMillis: int
    Sentiment: SentimentValueType
    IssuesDetected: NotRequired[List[IssueDetectedTypeDef]]


class RealtimeContactAnalysisSegmentTypeDef(TypedDict):
    Transcript: NotRequired[TranscriptTypeDef]
    Categories: NotRequired[CategoriesTypeDef]
    PostContactSummary: NotRequired[PostContactSummaryTypeDef]


class ListRealtimeContactAnalysisSegmentsResponseTypeDef(TypedDict):
    Segments: List[RealtimeContactAnalysisSegmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
