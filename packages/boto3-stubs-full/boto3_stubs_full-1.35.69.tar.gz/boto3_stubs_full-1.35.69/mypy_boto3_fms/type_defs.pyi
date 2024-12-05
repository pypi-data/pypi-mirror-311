"""
Type annotations for fms service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/type_defs/)

Usage::

    ```python
    from mypy_boto3_fms.type_defs import AccountScopeOutputTypeDef

    data: AccountScopeOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccountRoleStatusType,
    CustomerPolicyScopeIdTypeType,
    CustomerPolicyStatusType,
    DependentServiceNameType,
    DestinationTypeType,
    EntryTypeType,
    EntryViolationReasonType,
    FailedItemReasonType,
    FirewallDeploymentModelType,
    MarketplaceSubscriptionOnboardingStatusType,
    NetworkAclRuleActionType,
    OrganizationStatusType,
    PolicyComplianceStatusTypeType,
    RemediationActionTypeType,
    ResourceSetStatusType,
    RuleOrderType,
    SecurityServiceTypeType,
    StreamExceptionPolicyType,
    TargetTypeType,
    ThirdPartyFirewallAssociationStatusType,
    ThirdPartyFirewallType,
    ViolationReasonType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountScopeOutputTypeDef",
    "AccountScopeTypeDef",
    "AccountScopeUnionTypeDef",
    "ActionTargetTypeDef",
    "AdminAccountSummaryTypeDef",
    "AdminScopeOutputTypeDef",
    "AdminScopeTypeDef",
    "AppTypeDef",
    "AppsListDataOutputTypeDef",
    "AppsListDataSummaryTypeDef",
    "AppsListDataTypeDef",
    "AssociateAdminAccountRequestRequestTypeDef",
    "AssociateThirdPartyFirewallRequestRequestTypeDef",
    "AssociateThirdPartyFirewallResponseTypeDef",
    "AwsEc2InstanceViolationTypeDef",
    "AwsEc2NetworkInterfaceViolationTypeDef",
    "AwsVPCSecurityGroupViolationTypeDef",
    "BatchAssociateResourceRequestRequestTypeDef",
    "BatchAssociateResourceResponseTypeDef",
    "BatchDisassociateResourceRequestRequestTypeDef",
    "BatchDisassociateResourceResponseTypeDef",
    "ComplianceViolatorTypeDef",
    "CreateNetworkAclActionTypeDef",
    "CreateNetworkAclEntriesActionTypeDef",
    "DeleteAppsListRequestRequestTypeDef",
    "DeleteNetworkAclEntriesActionTypeDef",
    "DeletePolicyRequestRequestTypeDef",
    "DeleteProtocolsListRequestRequestTypeDef",
    "DeleteResourceSetRequestRequestTypeDef",
    "DisassociateThirdPartyFirewallRequestRequestTypeDef",
    "DisassociateThirdPartyFirewallResponseTypeDef",
    "DiscoveredResourceTypeDef",
    "DnsDuplicateRuleGroupViolationTypeDef",
    "DnsRuleGroupLimitExceededViolationTypeDef",
    "DnsRuleGroupPriorityConflictViolationTypeDef",
    "EC2AssociateRouteTableActionTypeDef",
    "EC2CopyRouteTableActionTypeDef",
    "EC2CreateRouteActionTypeDef",
    "EC2CreateRouteTableActionTypeDef",
    "EC2DeleteRouteActionTypeDef",
    "EC2ReplaceRouteActionTypeDef",
    "EC2ReplaceRouteTableAssociationActionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EntryDescriptionTypeDef",
    "EntryViolationTypeDef",
    "EvaluationResultTypeDef",
    "ExpectedRouteTypeDef",
    "FMSPolicyUpdateFirewallCreationConfigActionTypeDef",
    "FailedItemTypeDef",
    "FirewallSubnetIsOutOfScopeViolationTypeDef",
    "FirewallSubnetMissingVPCEndpointViolationTypeDef",
    "GetAdminAccountResponseTypeDef",
    "GetAdminScopeRequestRequestTypeDef",
    "GetAdminScopeResponseTypeDef",
    "GetAppsListRequestRequestTypeDef",
    "GetAppsListResponseTypeDef",
    "GetComplianceDetailRequestRequestTypeDef",
    "GetComplianceDetailResponseTypeDef",
    "GetNotificationChannelResponseTypeDef",
    "GetPolicyRequestRequestTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProtectionStatusRequestRequestTypeDef",
    "GetProtectionStatusResponseTypeDef",
    "GetProtocolsListRequestRequestTypeDef",
    "GetProtocolsListResponseTypeDef",
    "GetResourceSetRequestRequestTypeDef",
    "GetResourceSetResponseTypeDef",
    "GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef",
    "GetThirdPartyFirewallAssociationStatusResponseTypeDef",
    "GetViolationDetailsRequestRequestTypeDef",
    "GetViolationDetailsResponseTypeDef",
    "InvalidNetworkAclEntriesViolationTypeDef",
    "ListAdminAccountsForOrganizationRequestListAdminAccountsForOrganizationPaginateTypeDef",
    "ListAdminAccountsForOrganizationRequestRequestTypeDef",
    "ListAdminAccountsForOrganizationResponseTypeDef",
    "ListAdminsManagingAccountRequestListAdminsManagingAccountPaginateTypeDef",
    "ListAdminsManagingAccountRequestRequestTypeDef",
    "ListAdminsManagingAccountResponseTypeDef",
    "ListAppsListsRequestListAppsListsPaginateTypeDef",
    "ListAppsListsRequestRequestTypeDef",
    "ListAppsListsResponseTypeDef",
    "ListComplianceStatusRequestListComplianceStatusPaginateTypeDef",
    "ListComplianceStatusRequestRequestTypeDef",
    "ListComplianceStatusResponseTypeDef",
    "ListDiscoveredResourcesRequestRequestTypeDef",
    "ListDiscoveredResourcesResponseTypeDef",
    "ListMemberAccountsRequestListMemberAccountsPaginateTypeDef",
    "ListMemberAccountsRequestRequestTypeDef",
    "ListMemberAccountsResponseTypeDef",
    "ListPoliciesRequestListPoliciesPaginateTypeDef",
    "ListPoliciesRequestRequestTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListProtocolsListsRequestListProtocolsListsPaginateTypeDef",
    "ListProtocolsListsRequestRequestTypeDef",
    "ListProtocolsListsResponseTypeDef",
    "ListResourceSetResourcesRequestRequestTypeDef",
    "ListResourceSetResourcesResponseTypeDef",
    "ListResourceSetsRequestRequestTypeDef",
    "ListResourceSetsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesResponseTypeDef",
    "NetworkAclCommonPolicyOutputTypeDef",
    "NetworkAclCommonPolicyTypeDef",
    "NetworkAclCommonPolicyUnionTypeDef",
    "NetworkAclEntrySetOutputTypeDef",
    "NetworkAclEntrySetTypeDef",
    "NetworkAclEntrySetUnionTypeDef",
    "NetworkAclEntryTypeDef",
    "NetworkAclIcmpTypeCodeTypeDef",
    "NetworkAclPortRangeTypeDef",
    "NetworkFirewallBlackHoleRouteDetectedViolationTypeDef",
    "NetworkFirewallInternetTrafficNotInspectedViolationTypeDef",
    "NetworkFirewallInvalidRouteConfigurationViolationTypeDef",
    "NetworkFirewallMissingExpectedRTViolationTypeDef",
    "NetworkFirewallMissingExpectedRoutesViolationTypeDef",
    "NetworkFirewallMissingFirewallViolationTypeDef",
    "NetworkFirewallMissingSubnetViolationTypeDef",
    "NetworkFirewallPolicyDescriptionTypeDef",
    "NetworkFirewallPolicyModifiedViolationTypeDef",
    "NetworkFirewallPolicyTypeDef",
    "NetworkFirewallStatefulRuleGroupOverrideTypeDef",
    "NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef",
    "NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef",
    "OrganizationalUnitScopeOutputTypeDef",
    "OrganizationalUnitScopeTypeDef",
    "OrganizationalUnitScopeUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PartialMatchTypeDef",
    "PolicyComplianceDetailTypeDef",
    "PolicyComplianceStatusTypeDef",
    "PolicyOptionOutputTypeDef",
    "PolicyOptionTypeDef",
    "PolicyOptionUnionTypeDef",
    "PolicyOutputTypeDef",
    "PolicySummaryTypeDef",
    "PolicyTypeDef",
    "PolicyTypeScopeOutputTypeDef",
    "PolicyTypeScopeTypeDef",
    "PolicyTypeScopeUnionTypeDef",
    "PossibleRemediationActionTypeDef",
    "PossibleRemediationActionsTypeDef",
    "ProtocolsListDataOutputTypeDef",
    "ProtocolsListDataSummaryTypeDef",
    "ProtocolsListDataTypeDef",
    "PutAdminAccountRequestRequestTypeDef",
    "PutAppsListRequestRequestTypeDef",
    "PutAppsListResponseTypeDef",
    "PutNotificationChannelRequestRequestTypeDef",
    "PutPolicyRequestRequestTypeDef",
    "PutPolicyResponseTypeDef",
    "PutProtocolsListRequestRequestTypeDef",
    "PutProtocolsListResponseTypeDef",
    "PutResourceSetRequestRequestTypeDef",
    "PutResourceSetResponseTypeDef",
    "RegionScopeOutputTypeDef",
    "RegionScopeTypeDef",
    "RegionScopeUnionTypeDef",
    "RemediationActionTypeDef",
    "RemediationActionWithOrderTypeDef",
    "ReplaceNetworkAclAssociationActionTypeDef",
    "ResourceSetOutputTypeDef",
    "ResourceSetSummaryTypeDef",
    "ResourceSetTypeDef",
    "ResourceTagTypeDef",
    "ResourceTypeDef",
    "ResourceViolationTypeDef",
    "ResponseMetadataTypeDef",
    "RouteHasOutOfScopeEndpointViolationTypeDef",
    "RouteTypeDef",
    "SecurityGroupRemediationActionTypeDef",
    "SecurityGroupRuleDescriptionTypeDef",
    "SecurityServicePolicyDataOutputTypeDef",
    "SecurityServicePolicyDataTypeDef",
    "SecurityServicePolicyDataUnionTypeDef",
    "StatefulEngineOptionsTypeDef",
    "StatefulRuleGroupTypeDef",
    "StatelessRuleGroupTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ThirdPartyFirewallFirewallPolicyTypeDef",
    "ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef",
    "ThirdPartyFirewallMissingFirewallViolationTypeDef",
    "ThirdPartyFirewallMissingSubnetViolationTypeDef",
    "ThirdPartyFirewallPolicyTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ViolationDetailTypeDef",
    "WebACLHasIncompatibleConfigurationViolationTypeDef",
    "WebACLHasOutOfScopeResourcesViolationTypeDef",
)

class AccountScopeOutputTypeDef(TypedDict):
    Accounts: NotRequired[List[str]]
    AllAccountsEnabled: NotRequired[bool]
    ExcludeSpecifiedAccounts: NotRequired[bool]

class AccountScopeTypeDef(TypedDict):
    Accounts: NotRequired[Sequence[str]]
    AllAccountsEnabled: NotRequired[bool]
    ExcludeSpecifiedAccounts: NotRequired[bool]

class ActionTargetTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    Description: NotRequired[str]

class AdminAccountSummaryTypeDef(TypedDict):
    AdminAccount: NotRequired[str]
    DefaultAdmin: NotRequired[bool]
    Status: NotRequired[OrganizationStatusType]

class OrganizationalUnitScopeOutputTypeDef(TypedDict):
    OrganizationalUnits: NotRequired[List[str]]
    AllOrganizationalUnitsEnabled: NotRequired[bool]
    ExcludeSpecifiedOrganizationalUnits: NotRequired[bool]

class PolicyTypeScopeOutputTypeDef(TypedDict):
    PolicyTypes: NotRequired[List[SecurityServiceTypeType]]
    AllPolicyTypesEnabled: NotRequired[bool]

class RegionScopeOutputTypeDef(TypedDict):
    Regions: NotRequired[List[str]]
    AllRegionsEnabled: NotRequired[bool]

AppTypeDef = TypedDict(
    "AppTypeDef",
    {
        "AppName": str,
        "Protocol": str,
        "Port": int,
    },
)
TimestampTypeDef = Union[datetime, str]

class AssociateAdminAccountRequestRequestTypeDef(TypedDict):
    AdminAccount: str

class AssociateThirdPartyFirewallRequestRequestTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AwsEc2NetworkInterfaceViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolatingSecurityGroups: NotRequired[List[str]]

class PartialMatchTypeDef(TypedDict):
    Reference: NotRequired[str]
    TargetViolationReasons: NotRequired[List[str]]

class BatchAssociateResourceRequestRequestTypeDef(TypedDict):
    ResourceSetIdentifier: str
    Items: Sequence[str]

class FailedItemTypeDef(TypedDict):
    URI: NotRequired[str]
    Reason: NotRequired[FailedItemReasonType]

class BatchDisassociateResourceRequestRequestTypeDef(TypedDict):
    ResourceSetIdentifier: str
    Items: Sequence[str]

class ComplianceViolatorTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    ViolationReason: NotRequired[ViolationReasonType]
    ResourceType: NotRequired[str]
    Metadata: NotRequired[Dict[str, str]]

class DeleteAppsListRequestRequestTypeDef(TypedDict):
    ListId: str

class DeletePolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str
    DeleteAllPolicyResources: NotRequired[bool]

class DeleteProtocolsListRequestRequestTypeDef(TypedDict):
    ListId: str

class DeleteResourceSetRequestRequestTypeDef(TypedDict):
    Identifier: str

class DisassociateThirdPartyFirewallRequestRequestTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType

DiscoveredResourceTypeDef = TypedDict(
    "DiscoveredResourceTypeDef",
    {
        "URI": NotRequired[str],
        "AccountId": NotRequired[str],
        "Type": NotRequired[str],
        "Name": NotRequired[str],
    },
)

class DnsDuplicateRuleGroupViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolationTargetDescription: NotRequired[str]

class DnsRuleGroupLimitExceededViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolationTargetDescription: NotRequired[str]
    NumberOfRuleGroupsAlreadyAssociated: NotRequired[int]

class DnsRuleGroupPriorityConflictViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolationTargetDescription: NotRequired[str]
    ConflictingPriority: NotRequired[int]
    ConflictingPolicyId: NotRequired[str]
    UnavailablePriorities: NotRequired[List[int]]

class EvaluationResultTypeDef(TypedDict):
    ComplianceStatus: NotRequired[PolicyComplianceStatusTypeType]
    ViolatorCount: NotRequired[int]
    EvaluationLimitExceeded: NotRequired[bool]

class ExpectedRouteTypeDef(TypedDict):
    IpV4Cidr: NotRequired[str]
    PrefixListId: NotRequired[str]
    IpV6Cidr: NotRequired[str]
    ContributingSubnets: NotRequired[List[str]]
    AllowedTargets: NotRequired[List[str]]
    RouteTableId: NotRequired[str]

class FMSPolicyUpdateFirewallCreationConfigActionTypeDef(TypedDict):
    Description: NotRequired[str]
    FirewallCreationConfig: NotRequired[str]

class FirewallSubnetIsOutOfScopeViolationTypeDef(TypedDict):
    FirewallSubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]
    SubnetAvailabilityZoneId: NotRequired[str]
    VpcEndpointId: NotRequired[str]

class FirewallSubnetMissingVPCEndpointViolationTypeDef(TypedDict):
    FirewallSubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]
    SubnetAvailabilityZoneId: NotRequired[str]

class GetAdminScopeRequestRequestTypeDef(TypedDict):
    AdminAccount: str

class GetAppsListRequestRequestTypeDef(TypedDict):
    ListId: str
    DefaultList: NotRequired[bool]

class GetComplianceDetailRequestRequestTypeDef(TypedDict):
    PolicyId: str
    MemberAccount: str

class GetPolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str

class GetProtocolsListRequestRequestTypeDef(TypedDict):
    ListId: str
    DefaultList: NotRequired[bool]

class ProtocolsListDataOutputTypeDef(TypedDict):
    ListName: str
    ProtocolsList: List[str]
    ListId: NotRequired[str]
    ListUpdateToken: NotRequired[str]
    CreateTime: NotRequired[datetime]
    LastUpdateTime: NotRequired[datetime]
    PreviousProtocolsList: NotRequired[Dict[str, List[str]]]

class GetResourceSetRequestRequestTypeDef(TypedDict):
    Identifier: str

class ResourceSetOutputTypeDef(TypedDict):
    Name: str
    ResourceTypeList: List[str]
    Id: NotRequired[str]
    Description: NotRequired[str]
    UpdateToken: NotRequired[str]
    LastUpdateTime: NotRequired[datetime]
    ResourceSetStatus: NotRequired[ResourceSetStatusType]

class GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType

class GetViolationDetailsRequestRequestTypeDef(TypedDict):
    PolicyId: str
    MemberAccount: str
    ResourceId: str
    ResourceType: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAdminAccountsForOrganizationRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListAdminsManagingAccountRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListAppsListsRequestRequestTypeDef(TypedDict):
    MaxResults: int
    DefaultLists: NotRequired[bool]
    NextToken: NotRequired[str]

class ListComplianceStatusRequestRequestTypeDef(TypedDict):
    PolicyId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListDiscoveredResourcesRequestRequestTypeDef(TypedDict):
    MemberAccountIds: Sequence[str]
    ResourceType: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListMemberAccountsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListPoliciesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class PolicySummaryTypeDef(TypedDict):
    PolicyArn: NotRequired[str]
    PolicyId: NotRequired[str]
    PolicyName: NotRequired[str]
    ResourceType: NotRequired[str]
    SecurityServiceType: NotRequired[SecurityServiceTypeType]
    RemediationEnabled: NotRequired[bool]
    DeleteUnusedFMManagedResources: NotRequired[bool]
    PolicyStatus: NotRequired[CustomerPolicyStatusType]

class ListProtocolsListsRequestRequestTypeDef(TypedDict):
    MaxResults: int
    DefaultLists: NotRequired[bool]
    NextToken: NotRequired[str]

class ProtocolsListDataSummaryTypeDef(TypedDict):
    ListArn: NotRequired[str]
    ListId: NotRequired[str]
    ListName: NotRequired[str]
    ProtocolsList: NotRequired[List[str]]

class ListResourceSetResourcesRequestRequestTypeDef(TypedDict):
    Identifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ResourceTypeDef(TypedDict):
    URI: str
    AccountId: NotRequired[str]

class ListResourceSetsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ResourceSetSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    LastUpdateTime: NotRequired[datetime]
    ResourceSetStatus: NotRequired[ResourceSetStatusType]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType
    MaxResults: int
    NextToken: NotRequired[str]

class ThirdPartyFirewallFirewallPolicyTypeDef(TypedDict):
    FirewallPolicyId: NotRequired[str]
    FirewallPolicyName: NotRequired[str]

NetworkAclIcmpTypeCodeTypeDef = TypedDict(
    "NetworkAclIcmpTypeCodeTypeDef",
    {
        "Code": NotRequired[int],
        "Type": NotRequired[int],
    },
)

class NetworkAclPortRangeTypeDef(TypedDict):
    From: NotRequired[int]
    To: NotRequired[int]

class RouteTypeDef(TypedDict):
    DestinationType: NotRequired[DestinationTypeType]
    TargetType: NotRequired[TargetTypeType]
    Destination: NotRequired[str]
    Target: NotRequired[str]

class NetworkFirewallMissingExpectedRTViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    CurrentRouteTable: NotRequired[str]
    ExpectedRouteTable: NotRequired[str]

class NetworkFirewallMissingFirewallViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    TargetViolationReason: NotRequired[str]

class NetworkFirewallMissingSubnetViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    TargetViolationReason: NotRequired[str]

class StatefulEngineOptionsTypeDef(TypedDict):
    RuleOrder: NotRequired[RuleOrderType]
    StreamExceptionPolicy: NotRequired[StreamExceptionPolicyType]

class StatelessRuleGroupTypeDef(TypedDict):
    RuleGroupName: NotRequired[str]
    ResourceId: NotRequired[str]
    Priority: NotRequired[int]

class NetworkFirewallPolicyTypeDef(TypedDict):
    FirewallDeploymentModel: NotRequired[FirewallDeploymentModelType]

class NetworkFirewallStatefulRuleGroupOverrideTypeDef(TypedDict):
    Action: NotRequired[Literal["DROP_TO_ALERT"]]

class OrganizationalUnitScopeTypeDef(TypedDict):
    OrganizationalUnits: NotRequired[Sequence[str]]
    AllOrganizationalUnitsEnabled: NotRequired[bool]
    ExcludeSpecifiedOrganizationalUnits: NotRequired[bool]

class ThirdPartyFirewallPolicyTypeDef(TypedDict):
    FirewallDeploymentModel: NotRequired[FirewallDeploymentModelType]

class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]

class PolicyTypeScopeTypeDef(TypedDict):
    PolicyTypes: NotRequired[Sequence[SecurityServiceTypeType]]
    AllPolicyTypesEnabled: NotRequired[bool]

class PutNotificationChannelRequestRequestTypeDef(TypedDict):
    SnsTopicArn: str
    SnsRoleName: str

class RegionScopeTypeDef(TypedDict):
    Regions: NotRequired[Sequence[str]]
    AllRegionsEnabled: NotRequired[bool]

class ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    CurrentRouteTable: NotRequired[str]
    ExpectedRouteTable: NotRequired[str]

class ThirdPartyFirewallMissingFirewallViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    TargetViolationReason: NotRequired[str]

class ThirdPartyFirewallMissingSubnetViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    TargetViolationReason: NotRequired[str]

class WebACLHasIncompatibleConfigurationViolationTypeDef(TypedDict):
    WebACLArn: NotRequired[str]
    Description: NotRequired[str]

class WebACLHasOutOfScopeResourcesViolationTypeDef(TypedDict):
    WebACLArn: NotRequired[str]
    OutOfScopeResourceList: NotRequired[List[str]]

SecurityGroupRuleDescriptionTypeDef = TypedDict(
    "SecurityGroupRuleDescriptionTypeDef",
    {
        "IPV4Range": NotRequired[str],
        "IPV6Range": NotRequired[str],
        "PrefixListId": NotRequired[str],
        "Protocol": NotRequired[str],
        "FromPort": NotRequired[int],
        "ToPort": NotRequired[int],
    },
)

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

AccountScopeUnionTypeDef = Union[AccountScopeTypeDef, AccountScopeOutputTypeDef]

class CreateNetworkAclActionTypeDef(TypedDict):
    Description: NotRequired[str]
    Vpc: NotRequired[ActionTargetTypeDef]
    FMSCanRemediate: NotRequired[bool]

class EC2AssociateRouteTableActionTypeDef(TypedDict):
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]
    SubnetId: NotRequired[ActionTargetTypeDef]
    GatewayId: NotRequired[ActionTargetTypeDef]

class EC2CopyRouteTableActionTypeDef(TypedDict):
    VpcId: ActionTargetTypeDef
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]

class EC2CreateRouteActionTypeDef(TypedDict):
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]
    DestinationCidrBlock: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    VpcEndpointId: NotRequired[ActionTargetTypeDef]
    GatewayId: NotRequired[ActionTargetTypeDef]

class EC2CreateRouteTableActionTypeDef(TypedDict):
    VpcId: ActionTargetTypeDef
    Description: NotRequired[str]

class EC2DeleteRouteActionTypeDef(TypedDict):
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]
    DestinationCidrBlock: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]

class EC2ReplaceRouteActionTypeDef(TypedDict):
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]
    DestinationCidrBlock: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    GatewayId: NotRequired[ActionTargetTypeDef]

class EC2ReplaceRouteTableAssociationActionTypeDef(TypedDict):
    AssociationId: ActionTargetTypeDef
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]

class ReplaceNetworkAclAssociationActionTypeDef(TypedDict):
    Description: NotRequired[str]
    AssociationId: NotRequired[ActionTargetTypeDef]
    NetworkAclId: NotRequired[ActionTargetTypeDef]
    FMSCanRemediate: NotRequired[bool]

class AdminScopeOutputTypeDef(TypedDict):
    AccountScope: NotRequired[AccountScopeOutputTypeDef]
    OrganizationalUnitScope: NotRequired[OrganizationalUnitScopeOutputTypeDef]
    RegionScope: NotRequired[RegionScopeOutputTypeDef]
    PolicyTypeScope: NotRequired[PolicyTypeScopeOutputTypeDef]

class AppsListDataOutputTypeDef(TypedDict):
    ListName: str
    AppsList: List[AppTypeDef]
    ListId: NotRequired[str]
    ListUpdateToken: NotRequired[str]
    CreateTime: NotRequired[datetime]
    LastUpdateTime: NotRequired[datetime]
    PreviousAppsList: NotRequired[Dict[str, List[AppTypeDef]]]

class AppsListDataSummaryTypeDef(TypedDict):
    ListArn: NotRequired[str]
    ListId: NotRequired[str]
    ListName: NotRequired[str]
    AppsList: NotRequired[List[AppTypeDef]]

class AppsListDataTypeDef(TypedDict):
    ListName: str
    AppsList: Sequence[AppTypeDef]
    ListId: NotRequired[str]
    ListUpdateToken: NotRequired[str]
    CreateTime: NotRequired[TimestampTypeDef]
    LastUpdateTime: NotRequired[TimestampTypeDef]
    PreviousAppsList: NotRequired[Mapping[str, Sequence[AppTypeDef]]]

class GetProtectionStatusRequestRequestTypeDef(TypedDict):
    PolicyId: str
    MemberAccountId: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ProtocolsListDataTypeDef(TypedDict):
    ListName: str
    ProtocolsList: Sequence[str]
    ListId: NotRequired[str]
    ListUpdateToken: NotRequired[str]
    CreateTime: NotRequired[TimestampTypeDef]
    LastUpdateTime: NotRequired[TimestampTypeDef]
    PreviousProtocolsList: NotRequired[Mapping[str, Sequence[str]]]

class ResourceSetTypeDef(TypedDict):
    Name: str
    ResourceTypeList: Sequence[str]
    Id: NotRequired[str]
    Description: NotRequired[str]
    UpdateToken: NotRequired[str]
    LastUpdateTime: NotRequired[TimestampTypeDef]
    ResourceSetStatus: NotRequired[ResourceSetStatusType]

class AssociateThirdPartyFirewallResponseTypeDef(TypedDict):
    ThirdPartyFirewallStatus: ThirdPartyFirewallAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateThirdPartyFirewallResponseTypeDef(TypedDict):
    ThirdPartyFirewallStatus: ThirdPartyFirewallAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAdminAccountResponseTypeDef(TypedDict):
    AdminAccount: str
    RoleStatus: AccountRoleStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetNotificationChannelResponseTypeDef(TypedDict):
    SnsTopicArn: str
    SnsRoleName: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetProtectionStatusResponseTypeDef(TypedDict):
    AdminAccountId: str
    ServiceType: SecurityServiceTypeType
    Data: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetThirdPartyFirewallAssociationStatusResponseTypeDef(TypedDict):
    ThirdPartyFirewallStatus: ThirdPartyFirewallAssociationStatusType
    MarketplaceOnboardingStatus: MarketplaceSubscriptionOnboardingStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListAdminAccountsForOrganizationResponseTypeDef(TypedDict):
    AdminAccounts: List[AdminAccountSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAdminsManagingAccountResponseTypeDef(TypedDict):
    AdminAccounts: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMemberAccountsResponseTypeDef(TypedDict):
    MemberAccounts: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class AwsEc2InstanceViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    AwsEc2NetworkInterfaceViolations: NotRequired[List[AwsEc2NetworkInterfaceViolationTypeDef]]

class BatchAssociateResourceResponseTypeDef(TypedDict):
    ResourceSetIdentifier: str
    FailedItems: List[FailedItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDisassociateResourceResponseTypeDef(TypedDict):
    ResourceSetIdentifier: str
    FailedItems: List[FailedItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PolicyComplianceDetailTypeDef(TypedDict):
    PolicyOwner: NotRequired[str]
    PolicyId: NotRequired[str]
    MemberAccount: NotRequired[str]
    Violators: NotRequired[List[ComplianceViolatorTypeDef]]
    EvaluationLimitExceeded: NotRequired[bool]
    ExpiredAt: NotRequired[datetime]
    IssueInfoMap: NotRequired[Dict[DependentServiceNameType, str]]

class ListDiscoveredResourcesResponseTypeDef(TypedDict):
    Items: List[DiscoveredResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PolicyComplianceStatusTypeDef(TypedDict):
    PolicyOwner: NotRequired[str]
    PolicyId: NotRequired[str]
    PolicyName: NotRequired[str]
    MemberAccount: NotRequired[str]
    EvaluationResults: NotRequired[List[EvaluationResultTypeDef]]
    LastUpdated: NotRequired[datetime]
    IssueInfoMap: NotRequired[Dict[DependentServiceNameType, str]]

class NetworkFirewallMissingExpectedRoutesViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ExpectedRoutes: NotRequired[List[ExpectedRouteTypeDef]]
    VpcId: NotRequired[str]

class GetProtocolsListResponseTypeDef(TypedDict):
    ProtocolsList: ProtocolsListDataOutputTypeDef
    ProtocolsListArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutProtocolsListResponseTypeDef(TypedDict):
    ProtocolsList: ProtocolsListDataOutputTypeDef
    ProtocolsListArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceSetResponseTypeDef(TypedDict):
    ResourceSet: ResourceSetOutputTypeDef
    ResourceSetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutResourceSetResponseTypeDef(TypedDict):
    ResourceSet: ResourceSetOutputTypeDef
    ResourceSetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAdminAccountsForOrganizationRequestListAdminAccountsForOrganizationPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAdminsManagingAccountRequestListAdminsManagingAccountPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAppsListsRequestListAppsListsPaginateTypeDef(TypedDict):
    DefaultLists: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComplianceStatusRequestListComplianceStatusPaginateTypeDef(TypedDict):
    PolicyId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMemberAccountsRequestListMemberAccountsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPoliciesRequestListPoliciesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProtocolsListsRequestListProtocolsListsPaginateTypeDef(TypedDict):
    DefaultLists: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef(
    TypedDict
):
    ThirdPartyFirewall: ThirdPartyFirewallType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPoliciesResponseTypeDef(TypedDict):
    PolicyList: List[PolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListProtocolsListsResponseTypeDef(TypedDict):
    ProtocolsLists: List[ProtocolsListDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListResourceSetResourcesResponseTypeDef(TypedDict):
    Items: List[ResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListResourceSetsResponseTypeDef(TypedDict):
    ResourceSets: List[ResourceSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagList: Sequence[TagTypeDef]

class ListThirdPartyFirewallFirewallPoliciesResponseTypeDef(TypedDict):
    ThirdPartyFirewallFirewallPolicies: List[ThirdPartyFirewallFirewallPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

NetworkAclEntryTypeDef = TypedDict(
    "NetworkAclEntryTypeDef",
    {
        "Protocol": str,
        "RuleAction": NetworkAclRuleActionType,
        "Egress": bool,
        "IcmpTypeCode": NotRequired[NetworkAclIcmpTypeCodeTypeDef],
        "PortRange": NotRequired[NetworkAclPortRangeTypeDef],
        "CidrBlock": NotRequired[str],
        "Ipv6CidrBlock": NotRequired[str],
    },
)

class NetworkFirewallBlackHoleRouteDetectedViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    RouteTableId: NotRequired[str]
    VpcId: NotRequired[str]
    ViolatingRoutes: NotRequired[List[RouteTypeDef]]

class NetworkFirewallInternetTrafficNotInspectedViolationTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]
    RouteTableId: NotRequired[str]
    ViolatingRoutes: NotRequired[List[RouteTypeDef]]
    IsRouteTableUsedInDifferentAZ: NotRequired[bool]
    CurrentFirewallSubnetRouteTable: NotRequired[str]
    ExpectedFirewallEndpoint: NotRequired[str]
    FirewallSubnetId: NotRequired[str]
    ExpectedFirewallSubnetRoutes: NotRequired[List[ExpectedRouteTypeDef]]
    ActualFirewallSubnetRoutes: NotRequired[List[RouteTypeDef]]
    InternetGatewayId: NotRequired[str]
    CurrentInternetGatewayRouteTable: NotRequired[str]
    ExpectedInternetGatewayRoutes: NotRequired[List[ExpectedRouteTypeDef]]
    ActualInternetGatewayRoutes: NotRequired[List[RouteTypeDef]]
    VpcId: NotRequired[str]

class NetworkFirewallInvalidRouteConfigurationViolationTypeDef(TypedDict):
    AffectedSubnets: NotRequired[List[str]]
    RouteTableId: NotRequired[str]
    IsRouteTableUsedInDifferentAZ: NotRequired[bool]
    ViolatingRoute: NotRequired[RouteTypeDef]
    CurrentFirewallSubnetRouteTable: NotRequired[str]
    ExpectedFirewallEndpoint: NotRequired[str]
    ActualFirewallEndpoint: NotRequired[str]
    ExpectedFirewallSubnetId: NotRequired[str]
    ActualFirewallSubnetId: NotRequired[str]
    ExpectedFirewallSubnetRoutes: NotRequired[List[ExpectedRouteTypeDef]]
    ActualFirewallSubnetRoutes: NotRequired[List[RouteTypeDef]]
    InternetGatewayId: NotRequired[str]
    CurrentInternetGatewayRouteTable: NotRequired[str]
    ExpectedInternetGatewayRoutes: NotRequired[List[ExpectedRouteTypeDef]]
    ActualInternetGatewayRoutes: NotRequired[List[RouteTypeDef]]
    VpcId: NotRequired[str]

class NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef(TypedDict):
    FirewallSubnetId: NotRequired[str]
    ViolatingRoutes: NotRequired[List[RouteTypeDef]]
    RouteTableId: NotRequired[str]
    FirewallEndpoint: NotRequired[str]
    VpcId: NotRequired[str]

class NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef(TypedDict):
    GatewayId: NotRequired[str]
    ViolatingRoutes: NotRequired[List[RouteTypeDef]]
    RouteTableId: NotRequired[str]
    VpcId: NotRequired[str]

class RouteHasOutOfScopeEndpointViolationTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    RouteTableId: NotRequired[str]
    ViolatingRoutes: NotRequired[List[RouteTypeDef]]
    SubnetAvailabilityZone: NotRequired[str]
    SubnetAvailabilityZoneId: NotRequired[str]
    CurrentFirewallSubnetRouteTable: NotRequired[str]
    FirewallSubnetId: NotRequired[str]
    FirewallSubnetRoutes: NotRequired[List[RouteTypeDef]]
    InternetGatewayId: NotRequired[str]
    CurrentInternetGatewayRouteTable: NotRequired[str]
    InternetGatewayRoutes: NotRequired[List[RouteTypeDef]]

class StatefulRuleGroupTypeDef(TypedDict):
    RuleGroupName: NotRequired[str]
    ResourceId: NotRequired[str]
    Priority: NotRequired[int]
    Override: NotRequired[NetworkFirewallStatefulRuleGroupOverrideTypeDef]

OrganizationalUnitScopeUnionTypeDef = Union[
    OrganizationalUnitScopeTypeDef, OrganizationalUnitScopeOutputTypeDef
]
PolicyTypeScopeUnionTypeDef = Union[PolicyTypeScopeTypeDef, PolicyTypeScopeOutputTypeDef]
RegionScopeUnionTypeDef = Union[RegionScopeTypeDef, RegionScopeOutputTypeDef]

class SecurityGroupRemediationActionTypeDef(TypedDict):
    RemediationActionType: NotRequired[RemediationActionTypeType]
    Description: NotRequired[str]
    RemediationResult: NotRequired[SecurityGroupRuleDescriptionTypeDef]
    IsDefaultAction: NotRequired[bool]

class GetAdminScopeResponseTypeDef(TypedDict):
    AdminScope: AdminScopeOutputTypeDef
    Status: OrganizationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppsListResponseTypeDef(TypedDict):
    AppsList: AppsListDataOutputTypeDef
    AppsListArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutAppsListResponseTypeDef(TypedDict):
    AppsList: AppsListDataOutputTypeDef
    AppsListArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAppsListsResponseTypeDef(TypedDict):
    AppsLists: List[AppsListDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutAppsListRequestRequestTypeDef(TypedDict):
    AppsList: AppsListDataTypeDef
    TagList: NotRequired[Sequence[TagTypeDef]]

class PutProtocolsListRequestRequestTypeDef(TypedDict):
    ProtocolsList: ProtocolsListDataTypeDef
    TagList: NotRequired[Sequence[TagTypeDef]]

class PutResourceSetRequestRequestTypeDef(TypedDict):
    ResourceSet: ResourceSetTypeDef
    TagList: NotRequired[Sequence[TagTypeDef]]

class GetComplianceDetailResponseTypeDef(TypedDict):
    PolicyComplianceDetail: PolicyComplianceDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListComplianceStatusResponseTypeDef(TypedDict):
    PolicyComplianceStatusList: List[PolicyComplianceStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class EntryDescriptionTypeDef(TypedDict):
    EntryDetail: NotRequired[NetworkAclEntryTypeDef]
    EntryRuleNumber: NotRequired[int]
    EntryType: NotRequired[EntryTypeType]

class NetworkAclEntrySetOutputTypeDef(TypedDict):
    ForceRemediateForFirstEntries: bool
    ForceRemediateForLastEntries: bool
    FirstEntries: NotRequired[List[NetworkAclEntryTypeDef]]
    LastEntries: NotRequired[List[NetworkAclEntryTypeDef]]

class NetworkAclEntrySetTypeDef(TypedDict):
    ForceRemediateForFirstEntries: bool
    ForceRemediateForLastEntries: bool
    FirstEntries: NotRequired[Sequence[NetworkAclEntryTypeDef]]
    LastEntries: NotRequired[Sequence[NetworkAclEntryTypeDef]]

class NetworkFirewallPolicyDescriptionTypeDef(TypedDict):
    StatelessRuleGroups: NotRequired[List[StatelessRuleGroupTypeDef]]
    StatelessDefaultActions: NotRequired[List[str]]
    StatelessFragmentDefaultActions: NotRequired[List[str]]
    StatelessCustomActions: NotRequired[List[str]]
    StatefulRuleGroups: NotRequired[List[StatefulRuleGroupTypeDef]]
    StatefulDefaultActions: NotRequired[List[str]]
    StatefulEngineOptions: NotRequired[StatefulEngineOptionsTypeDef]

class AdminScopeTypeDef(TypedDict):
    AccountScope: NotRequired[AccountScopeUnionTypeDef]
    OrganizationalUnitScope: NotRequired[OrganizationalUnitScopeUnionTypeDef]
    RegionScope: NotRequired[RegionScopeUnionTypeDef]
    PolicyTypeScope: NotRequired[PolicyTypeScopeUnionTypeDef]

class AwsVPCSecurityGroupViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolationTargetDescription: NotRequired[str]
    PartialMatches: NotRequired[List[PartialMatchTypeDef]]
    PossibleSecurityGroupRemediationActions: NotRequired[
        List[SecurityGroupRemediationActionTypeDef]
    ]

class CreateNetworkAclEntriesActionTypeDef(TypedDict):
    Description: NotRequired[str]
    NetworkAclId: NotRequired[ActionTargetTypeDef]
    NetworkAclEntriesToBeCreated: NotRequired[List[EntryDescriptionTypeDef]]
    FMSCanRemediate: NotRequired[bool]

class DeleteNetworkAclEntriesActionTypeDef(TypedDict):
    Description: NotRequired[str]
    NetworkAclId: NotRequired[ActionTargetTypeDef]
    NetworkAclEntriesToBeDeleted: NotRequired[List[EntryDescriptionTypeDef]]
    FMSCanRemediate: NotRequired[bool]

class EntryViolationTypeDef(TypedDict):
    ExpectedEntry: NotRequired[EntryDescriptionTypeDef]
    ExpectedEvaluationOrder: NotRequired[str]
    ActualEvaluationOrder: NotRequired[str]
    EntryAtExpectedEvaluationOrder: NotRequired[EntryDescriptionTypeDef]
    EntriesWithConflicts: NotRequired[List[EntryDescriptionTypeDef]]
    EntryViolationReasons: NotRequired[List[EntryViolationReasonType]]

class NetworkAclCommonPolicyOutputTypeDef(TypedDict):
    NetworkAclEntrySet: NetworkAclEntrySetOutputTypeDef

NetworkAclEntrySetUnionTypeDef = Union[NetworkAclEntrySetTypeDef, NetworkAclEntrySetOutputTypeDef]

class NetworkFirewallPolicyModifiedViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    CurrentPolicyDescription: NotRequired[NetworkFirewallPolicyDescriptionTypeDef]
    ExpectedPolicyDescription: NotRequired[NetworkFirewallPolicyDescriptionTypeDef]

class PutAdminAccountRequestRequestTypeDef(TypedDict):
    AdminAccount: str
    AdminScope: NotRequired[AdminScopeTypeDef]

class RemediationActionTypeDef(TypedDict):
    Description: NotRequired[str]
    EC2CreateRouteAction: NotRequired[EC2CreateRouteActionTypeDef]
    EC2ReplaceRouteAction: NotRequired[EC2ReplaceRouteActionTypeDef]
    EC2DeleteRouteAction: NotRequired[EC2DeleteRouteActionTypeDef]
    EC2CopyRouteTableAction: NotRequired[EC2CopyRouteTableActionTypeDef]
    EC2ReplaceRouteTableAssociationAction: NotRequired[EC2ReplaceRouteTableAssociationActionTypeDef]
    EC2AssociateRouteTableAction: NotRequired[EC2AssociateRouteTableActionTypeDef]
    EC2CreateRouteTableAction: NotRequired[EC2CreateRouteTableActionTypeDef]
    FMSPolicyUpdateFirewallCreationConfigAction: NotRequired[
        FMSPolicyUpdateFirewallCreationConfigActionTypeDef
    ]
    CreateNetworkAclAction: NotRequired[CreateNetworkAclActionTypeDef]
    ReplaceNetworkAclAssociationAction: NotRequired[ReplaceNetworkAclAssociationActionTypeDef]
    CreateNetworkAclEntriesAction: NotRequired[CreateNetworkAclEntriesActionTypeDef]
    DeleteNetworkAclEntriesAction: NotRequired[DeleteNetworkAclEntriesActionTypeDef]

class InvalidNetworkAclEntriesViolationTypeDef(TypedDict):
    Vpc: NotRequired[str]
    Subnet: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]
    CurrentAssociatedNetworkAcl: NotRequired[str]
    EntryViolations: NotRequired[List[EntryViolationTypeDef]]

class PolicyOptionOutputTypeDef(TypedDict):
    NetworkFirewallPolicy: NotRequired[NetworkFirewallPolicyTypeDef]
    ThirdPartyFirewallPolicy: NotRequired[ThirdPartyFirewallPolicyTypeDef]
    NetworkAclCommonPolicy: NotRequired[NetworkAclCommonPolicyOutputTypeDef]

class NetworkAclCommonPolicyTypeDef(TypedDict):
    NetworkAclEntrySet: NetworkAclEntrySetUnionTypeDef

class RemediationActionWithOrderTypeDef(TypedDict):
    RemediationAction: NotRequired[RemediationActionTypeDef]
    Order: NotRequired[int]

SecurityServicePolicyDataOutputTypeDef = TypedDict(
    "SecurityServicePolicyDataOutputTypeDef",
    {
        "Type": SecurityServiceTypeType,
        "ManagedServiceData": NotRequired[str],
        "PolicyOption": NotRequired[PolicyOptionOutputTypeDef],
    },
)
NetworkAclCommonPolicyUnionTypeDef = Union[
    NetworkAclCommonPolicyTypeDef, NetworkAclCommonPolicyOutputTypeDef
]

class PossibleRemediationActionTypeDef(TypedDict):
    OrderedRemediationActions: List[RemediationActionWithOrderTypeDef]
    Description: NotRequired[str]
    IsDefaultAction: NotRequired[bool]

class PolicyOutputTypeDef(TypedDict):
    PolicyName: str
    SecurityServicePolicyData: SecurityServicePolicyDataOutputTypeDef
    ResourceType: str
    ExcludeResourceTags: bool
    RemediationEnabled: bool
    PolicyId: NotRequired[str]
    PolicyUpdateToken: NotRequired[str]
    ResourceTypeList: NotRequired[List[str]]
    ResourceTags: NotRequired[List[ResourceTagTypeDef]]
    DeleteUnusedFMManagedResources: NotRequired[bool]
    IncludeMap: NotRequired[Dict[CustomerPolicyScopeIdTypeType, List[str]]]
    ExcludeMap: NotRequired[Dict[CustomerPolicyScopeIdTypeType, List[str]]]
    ResourceSetIds: NotRequired[List[str]]
    PolicyDescription: NotRequired[str]
    PolicyStatus: NotRequired[CustomerPolicyStatusType]

class PolicyOptionTypeDef(TypedDict):
    NetworkFirewallPolicy: NotRequired[NetworkFirewallPolicyTypeDef]
    ThirdPartyFirewallPolicy: NotRequired[ThirdPartyFirewallPolicyTypeDef]
    NetworkAclCommonPolicy: NotRequired[NetworkAclCommonPolicyUnionTypeDef]

class PossibleRemediationActionsTypeDef(TypedDict):
    Description: NotRequired[str]
    Actions: NotRequired[List[PossibleRemediationActionTypeDef]]

class GetPolicyResponseTypeDef(TypedDict):
    Policy: PolicyOutputTypeDef
    PolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutPolicyResponseTypeDef(TypedDict):
    Policy: PolicyOutputTypeDef
    PolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

PolicyOptionUnionTypeDef = Union[PolicyOptionTypeDef, PolicyOptionOutputTypeDef]

class ResourceViolationTypeDef(TypedDict):
    AwsVPCSecurityGroupViolation: NotRequired[AwsVPCSecurityGroupViolationTypeDef]
    AwsEc2NetworkInterfaceViolation: NotRequired[AwsEc2NetworkInterfaceViolationTypeDef]
    AwsEc2InstanceViolation: NotRequired[AwsEc2InstanceViolationTypeDef]
    NetworkFirewallMissingFirewallViolation: NotRequired[
        NetworkFirewallMissingFirewallViolationTypeDef
    ]
    NetworkFirewallMissingSubnetViolation: NotRequired[NetworkFirewallMissingSubnetViolationTypeDef]
    NetworkFirewallMissingExpectedRTViolation: NotRequired[
        NetworkFirewallMissingExpectedRTViolationTypeDef
    ]
    NetworkFirewallPolicyModifiedViolation: NotRequired[
        NetworkFirewallPolicyModifiedViolationTypeDef
    ]
    NetworkFirewallInternetTrafficNotInspectedViolation: NotRequired[
        NetworkFirewallInternetTrafficNotInspectedViolationTypeDef
    ]
    NetworkFirewallInvalidRouteConfigurationViolation: NotRequired[
        NetworkFirewallInvalidRouteConfigurationViolationTypeDef
    ]
    NetworkFirewallBlackHoleRouteDetectedViolation: NotRequired[
        NetworkFirewallBlackHoleRouteDetectedViolationTypeDef
    ]
    NetworkFirewallUnexpectedFirewallRoutesViolation: NotRequired[
        NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef
    ]
    NetworkFirewallUnexpectedGatewayRoutesViolation: NotRequired[
        NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef
    ]
    NetworkFirewallMissingExpectedRoutesViolation: NotRequired[
        NetworkFirewallMissingExpectedRoutesViolationTypeDef
    ]
    DnsRuleGroupPriorityConflictViolation: NotRequired[DnsRuleGroupPriorityConflictViolationTypeDef]
    DnsDuplicateRuleGroupViolation: NotRequired[DnsDuplicateRuleGroupViolationTypeDef]
    DnsRuleGroupLimitExceededViolation: NotRequired[DnsRuleGroupLimitExceededViolationTypeDef]
    FirewallSubnetIsOutOfScopeViolation: NotRequired[FirewallSubnetIsOutOfScopeViolationTypeDef]
    RouteHasOutOfScopeEndpointViolation: NotRequired[RouteHasOutOfScopeEndpointViolationTypeDef]
    ThirdPartyFirewallMissingFirewallViolation: NotRequired[
        ThirdPartyFirewallMissingFirewallViolationTypeDef
    ]
    ThirdPartyFirewallMissingSubnetViolation: NotRequired[
        ThirdPartyFirewallMissingSubnetViolationTypeDef
    ]
    ThirdPartyFirewallMissingExpectedRouteTableViolation: NotRequired[
        ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef
    ]
    FirewallSubnetMissingVPCEndpointViolation: NotRequired[
        FirewallSubnetMissingVPCEndpointViolationTypeDef
    ]
    InvalidNetworkAclEntriesViolation: NotRequired[InvalidNetworkAclEntriesViolationTypeDef]
    PossibleRemediationActions: NotRequired[PossibleRemediationActionsTypeDef]
    WebACLHasIncompatibleConfigurationViolation: NotRequired[
        WebACLHasIncompatibleConfigurationViolationTypeDef
    ]
    WebACLHasOutOfScopeResourcesViolation: NotRequired[WebACLHasOutOfScopeResourcesViolationTypeDef]

SecurityServicePolicyDataTypeDef = TypedDict(
    "SecurityServicePolicyDataTypeDef",
    {
        "Type": SecurityServiceTypeType,
        "ManagedServiceData": NotRequired[str],
        "PolicyOption": NotRequired[PolicyOptionUnionTypeDef],
    },
)

class ViolationDetailTypeDef(TypedDict):
    PolicyId: str
    MemberAccount: str
    ResourceId: str
    ResourceType: str
    ResourceViolations: List[ResourceViolationTypeDef]
    ResourceTags: NotRequired[List[TagTypeDef]]
    ResourceDescription: NotRequired[str]

SecurityServicePolicyDataUnionTypeDef = Union[
    SecurityServicePolicyDataTypeDef, SecurityServicePolicyDataOutputTypeDef
]

class GetViolationDetailsResponseTypeDef(TypedDict):
    ViolationDetail: ViolationDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PolicyTypeDef(TypedDict):
    PolicyName: str
    SecurityServicePolicyData: SecurityServicePolicyDataUnionTypeDef
    ResourceType: str
    ExcludeResourceTags: bool
    RemediationEnabled: bool
    PolicyId: NotRequired[str]
    PolicyUpdateToken: NotRequired[str]
    ResourceTypeList: NotRequired[Sequence[str]]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
    DeleteUnusedFMManagedResources: NotRequired[bool]
    IncludeMap: NotRequired[Mapping[CustomerPolicyScopeIdTypeType, Sequence[str]]]
    ExcludeMap: NotRequired[Mapping[CustomerPolicyScopeIdTypeType, Sequence[str]]]
    ResourceSetIds: NotRequired[Sequence[str]]
    PolicyDescription: NotRequired[str]
    PolicyStatus: NotRequired[CustomerPolicyStatusType]

class PutPolicyRequestRequestTypeDef(TypedDict):
    Policy: PolicyTypeDef
    TagList: NotRequired[Sequence[TagTypeDef]]
