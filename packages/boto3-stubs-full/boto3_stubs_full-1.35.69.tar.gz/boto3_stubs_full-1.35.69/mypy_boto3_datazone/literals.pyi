"""
Type annotations for datazone service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/literals/)

Usage::

    ```python
    from mypy_boto3_datazone.literals import AcceptRuleBehaviorType

    data: AcceptRuleBehaviorType = "ALL"
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "AcceptRuleBehaviorType",
    "AuthTypeType",
    "ChangeActionType",
    "ConfigurableActionTypeAuthorizationType",
    "DataAssetActivityStatusType",
    "DataProductItemTypeType",
    "DataProductStatusType",
    "DataSourceErrorTypeType",
    "DataSourceRunStatusType",
    "DataSourceRunTypeType",
    "DataSourceStatusType",
    "DataZoneEntityTypeType",
    "DataZoneServiceName",
    "DeploymentStatusType",
    "DeploymentTypeType",
    "DomainStatusType",
    "DomainUnitDesignationType",
    "EdgeDirectionType",
    "EnableSettingType",
    "EntityTypeType",
    "EnvironmentStatusType",
    "FilterExpressionTypeType",
    "FilterStatusType",
    "FormTypeStatusType",
    "GlossaryStatusType",
    "GlossaryTermStatusType",
    "GroupProfileStatusType",
    "GroupSearchTypeType",
    "InventorySearchScopeType",
    "ListAssetFiltersPaginatorName",
    "ListAssetRevisionsPaginatorName",
    "ListDataProductRevisionsPaginatorName",
    "ListDataSourceRunActivitiesPaginatorName",
    "ListDataSourceRunsPaginatorName",
    "ListDataSourcesPaginatorName",
    "ListDomainUnitsForParentPaginatorName",
    "ListDomainsPaginatorName",
    "ListEntityOwnersPaginatorName",
    "ListEnvironmentActionsPaginatorName",
    "ListEnvironmentBlueprintConfigurationsPaginatorName",
    "ListEnvironmentBlueprintsPaginatorName",
    "ListEnvironmentProfilesPaginatorName",
    "ListEnvironmentsPaginatorName",
    "ListLineageNodeHistoryPaginatorName",
    "ListMetadataGenerationRunsPaginatorName",
    "ListNotificationsPaginatorName",
    "ListPolicyGrantsPaginatorName",
    "ListProjectMembershipsPaginatorName",
    "ListProjectsPaginatorName",
    "ListRulesPaginatorName",
    "ListSubscriptionGrantsPaginatorName",
    "ListSubscriptionRequestsPaginatorName",
    "ListSubscriptionTargetsPaginatorName",
    "ListSubscriptionsPaginatorName",
    "ListTimeSeriesDataPointsPaginatorName",
    "ListingStatusType",
    "ManagedPolicyTypeType",
    "MetadataGenerationRunStatusType",
    "MetadataGenerationRunTypeType",
    "MetadataGenerationTargetTypeType",
    "NotificationResourceTypeType",
    "NotificationRoleType",
    "NotificationTypeType",
    "PaginatorName",
    "ProjectDesignationType",
    "ProjectStatusType",
    "RegionName",
    "RejectRuleBehaviorType",
    "ResourceServiceName",
    "RuleActionType",
    "RuleScopeSelectionModeType",
    "RuleTargetTypeType",
    "RuleTypeType",
    "SearchGroupProfilesPaginatorName",
    "SearchListingsPaginatorName",
    "SearchOutputAdditionalAttributeType",
    "SearchPaginatorName",
    "SearchTypesPaginatorName",
    "SearchUserProfilesPaginatorName",
    "SelfGrantStatusType",
    "ServiceName",
    "SortFieldProjectType",
    "SortKeyType",
    "SortOrderType",
    "SubscriptionGrantOverallStatusType",
    "SubscriptionGrantStatusType",
    "SubscriptionRequestStatusType",
    "SubscriptionStatusType",
    "TargetEntityTypeType",
    "TaskStatusType",
    "TimeSeriesEntityTypeType",
    "TimezoneType",
    "TypesSearchScopeType",
    "UserAssignmentType",
    "UserDesignationType",
    "UserProfileStatusType",
    "UserProfileTypeType",
    "UserSearchTypeType",
    "UserTypeType",
)

AcceptRuleBehaviorType = Literal["ALL", "NONE"]
AuthTypeType = Literal["DISABLED", "IAM_IDC"]
ChangeActionType = Literal["PUBLISH", "UNPUBLISH"]
ConfigurableActionTypeAuthorizationType = Literal["HTTPS", "IAM"]
DataAssetActivityStatusType = Literal[
    "FAILED",
    "PUBLISHING_FAILED",
    "SKIPPED_ALREADY_IMPORTED",
    "SKIPPED_ARCHIVED",
    "SKIPPED_NO_ACCESS",
    "SUCCEEDED_CREATED",
    "SUCCEEDED_UPDATED",
    "UNCHANGED",
]
DataProductItemTypeType = Literal["ASSET"]
DataProductStatusType = Literal["CREATED", "CREATE_FAILED", "CREATING"]
DataSourceErrorTypeType = Literal[
    "ACCESS_DENIED_EXCEPTION",
    "CONFLICT_EXCEPTION",
    "INTERNAL_SERVER_EXCEPTION",
    "RESOURCE_NOT_FOUND_EXCEPTION",
    "SERVICE_QUOTA_EXCEEDED_EXCEPTION",
    "THROTTLING_EXCEPTION",
    "VALIDATION_EXCEPTION",
]
DataSourceRunStatusType = Literal[
    "FAILED", "PARTIALLY_SUCCEEDED", "REQUESTED", "RUNNING", "SUCCESS"
]
DataSourceRunTypeType = Literal["PRIORITIZED", "SCHEDULED"]
DataSourceStatusType = Literal[
    "CREATING",
    "DELETING",
    "FAILED_CREATION",
    "FAILED_DELETION",
    "FAILED_UPDATE",
    "READY",
    "RUNNING",
    "UPDATING",
]
DataZoneEntityTypeType = Literal["DOMAIN_UNIT"]
DeploymentStatusType = Literal["FAILED", "IN_PROGRESS", "PENDING_DEPLOYMENT", "SUCCESSFUL"]
DeploymentTypeType = Literal["CREATE", "DELETE", "UPDATE"]
DomainStatusType = Literal[
    "AVAILABLE", "CREATING", "CREATION_FAILED", "DELETED", "DELETING", "DELETION_FAILED"
]
DomainUnitDesignationType = Literal["OWNER"]
EdgeDirectionType = Literal["DOWNSTREAM", "UPSTREAM"]
EnableSettingType = Literal["DISABLED", "ENABLED"]
EntityTypeType = Literal["ASSET", "DATA_PRODUCT"]
EnvironmentStatusType = Literal[
    "ACTIVE",
    "CREATE_FAILED",
    "CREATING",
    "DELETED",
    "DELETE_FAILED",
    "DELETING",
    "DISABLED",
    "EXPIRED",
    "INACCESSIBLE",
    "SUSPENDED",
    "UPDATE_FAILED",
    "UPDATING",
    "VALIDATION_FAILED",
]
FilterExpressionTypeType = Literal["EXCLUDE", "INCLUDE"]
FilterStatusType = Literal["INVALID", "VALID"]
FormTypeStatusType = Literal["DISABLED", "ENABLED"]
GlossaryStatusType = Literal["DISABLED", "ENABLED"]
GlossaryTermStatusType = Literal["DISABLED", "ENABLED"]
GroupProfileStatusType = Literal["ASSIGNED", "NOT_ASSIGNED"]
GroupSearchTypeType = Literal["DATAZONE_SSO_GROUP", "SSO_GROUP"]
InventorySearchScopeType = Literal["ASSET", "DATA_PRODUCT", "GLOSSARY", "GLOSSARY_TERM"]
ListAssetFiltersPaginatorName = Literal["list_asset_filters"]
ListAssetRevisionsPaginatorName = Literal["list_asset_revisions"]
ListDataProductRevisionsPaginatorName = Literal["list_data_product_revisions"]
ListDataSourceRunActivitiesPaginatorName = Literal["list_data_source_run_activities"]
ListDataSourceRunsPaginatorName = Literal["list_data_source_runs"]
ListDataSourcesPaginatorName = Literal["list_data_sources"]
ListDomainUnitsForParentPaginatorName = Literal["list_domain_units_for_parent"]
ListDomainsPaginatorName = Literal["list_domains"]
ListEntityOwnersPaginatorName = Literal["list_entity_owners"]
ListEnvironmentActionsPaginatorName = Literal["list_environment_actions"]
ListEnvironmentBlueprintConfigurationsPaginatorName = Literal[
    "list_environment_blueprint_configurations"
]
ListEnvironmentBlueprintsPaginatorName = Literal["list_environment_blueprints"]
ListEnvironmentProfilesPaginatorName = Literal["list_environment_profiles"]
ListEnvironmentsPaginatorName = Literal["list_environments"]
ListLineageNodeHistoryPaginatorName = Literal["list_lineage_node_history"]
ListMetadataGenerationRunsPaginatorName = Literal["list_metadata_generation_runs"]
ListNotificationsPaginatorName = Literal["list_notifications"]
ListPolicyGrantsPaginatorName = Literal["list_policy_grants"]
ListProjectMembershipsPaginatorName = Literal["list_project_memberships"]
ListProjectsPaginatorName = Literal["list_projects"]
ListRulesPaginatorName = Literal["list_rules"]
ListSubscriptionGrantsPaginatorName = Literal["list_subscription_grants"]
ListSubscriptionRequestsPaginatorName = Literal["list_subscription_requests"]
ListSubscriptionTargetsPaginatorName = Literal["list_subscription_targets"]
ListSubscriptionsPaginatorName = Literal["list_subscriptions"]
ListTimeSeriesDataPointsPaginatorName = Literal["list_time_series_data_points"]
ListingStatusType = Literal["ACTIVE", "CREATING", "INACTIVE"]
ManagedPolicyTypeType = Literal[
    "ADD_TO_PROJECT_MEMBER_POOL",
    "CREATE_ASSET_TYPE",
    "CREATE_DOMAIN_UNIT",
    "CREATE_ENVIRONMENT",
    "CREATE_ENVIRONMENT_PROFILE",
    "CREATE_FORM_TYPE",
    "CREATE_GLOSSARY",
    "CREATE_PROJECT",
    "DELEGATE_CREATE_ENVIRONMENT_PROFILE",
    "OVERRIDE_DOMAIN_UNIT_OWNERS",
    "OVERRIDE_PROJECT_OWNERS",
]
MetadataGenerationRunStatusType = Literal[
    "CANCELED", "FAILED", "IN_PROGRESS", "SUBMITTED", "SUCCEEDED"
]
MetadataGenerationRunTypeType = Literal["BUSINESS_DESCRIPTIONS"]
MetadataGenerationTargetTypeType = Literal["ASSET"]
NotificationResourceTypeType = Literal["PROJECT"]
NotificationRoleType = Literal[
    "DOMAIN_OWNER", "PROJECT_CONTRIBUTOR", "PROJECT_OWNER", "PROJECT_SUBSCRIBER", "PROJECT_VIEWER"
]
NotificationTypeType = Literal["EVENT", "TASK"]
ProjectDesignationType = Literal["CONTRIBUTOR", "OWNER", "PROJECT_CATALOG_STEWARD"]
ProjectStatusType = Literal["ACTIVE", "DELETE_FAILED", "DELETING"]
RejectRuleBehaviorType = Literal["ALL", "NONE"]
RuleActionType = Literal["CREATE_SUBSCRIPTION_REQUEST"]
RuleScopeSelectionModeType = Literal["ALL", "SPECIFIC"]
RuleTargetTypeType = Literal["DOMAIN_UNIT"]
RuleTypeType = Literal["METADATA_FORM_ENFORCEMENT"]
SearchGroupProfilesPaginatorName = Literal["search_group_profiles"]
SearchListingsPaginatorName = Literal["search_listings"]
SearchOutputAdditionalAttributeType = Literal["FORMS", "TIME_SERIES_DATA_POINT_FORMS"]
SearchPaginatorName = Literal["search"]
SearchTypesPaginatorName = Literal["search_types"]
SearchUserProfilesPaginatorName = Literal["search_user_profiles"]
SelfGrantStatusType = Literal[
    "GRANTED",
    "GRANT_FAILED",
    "GRANT_IN_PROGRESS",
    "GRANT_PENDING",
    "REVOKE_FAILED",
    "REVOKE_IN_PROGRESS",
    "REVOKE_PENDING",
]
SortFieldProjectType = Literal["NAME"]
SortKeyType = Literal["CREATED_AT", "UPDATED_AT"]
SortOrderType = Literal["ASCENDING", "DESCENDING"]
SubscriptionGrantOverallStatusType = Literal[
    "COMPLETED",
    "GRANT_AND_REVOKE_FAILED",
    "GRANT_FAILED",
    "INACCESSIBLE",
    "IN_PROGRESS",
    "PENDING",
    "REVOKE_FAILED",
]
SubscriptionGrantStatusType = Literal[
    "GRANTED",
    "GRANT_FAILED",
    "GRANT_IN_PROGRESS",
    "GRANT_PENDING",
    "REVOKED",
    "REVOKE_FAILED",
    "REVOKE_IN_PROGRESS",
    "REVOKE_PENDING",
]
SubscriptionRequestStatusType = Literal["ACCEPTED", "PENDING", "REJECTED"]
SubscriptionStatusType = Literal["APPROVED", "CANCELLED", "REVOKED"]
TargetEntityTypeType = Literal[
    "DOMAIN_UNIT", "ENVIRONMENT_BLUEPRINT_CONFIGURATION", "ENVIRONMENT_PROFILE"
]
TaskStatusType = Literal["ACTIVE", "INACTIVE"]
TimeSeriesEntityTypeType = Literal["ASSET", "LISTING"]
TimezoneType = Literal[
    "AFRICA_JOHANNESBURG",
    "AMERICA_MONTREAL",
    "AMERICA_SAO_PAULO",
    "ASIA_BAHRAIN",
    "ASIA_BANGKOK",
    "ASIA_CALCUTTA",
    "ASIA_DUBAI",
    "ASIA_HONG_KONG",
    "ASIA_JAKARTA",
    "ASIA_KUALA_LUMPUR",
    "ASIA_SEOUL",
    "ASIA_SHANGHAI",
    "ASIA_SINGAPORE",
    "ASIA_TAIPEI",
    "ASIA_TOKYO",
    "AUSTRALIA_MELBOURNE",
    "AUSTRALIA_SYDNEY",
    "CANADA_CENTRAL",
    "CET",
    "CST6CDT",
    "ETC_GMT",
    "ETC_GMT0",
    "ETC_GMT_ADD_0",
    "ETC_GMT_ADD_1",
    "ETC_GMT_ADD_10",
    "ETC_GMT_ADD_11",
    "ETC_GMT_ADD_12",
    "ETC_GMT_ADD_2",
    "ETC_GMT_ADD_3",
    "ETC_GMT_ADD_4",
    "ETC_GMT_ADD_5",
    "ETC_GMT_ADD_6",
    "ETC_GMT_ADD_7",
    "ETC_GMT_ADD_8",
    "ETC_GMT_ADD_9",
    "ETC_GMT_NEG_0",
    "ETC_GMT_NEG_1",
    "ETC_GMT_NEG_10",
    "ETC_GMT_NEG_11",
    "ETC_GMT_NEG_12",
    "ETC_GMT_NEG_13",
    "ETC_GMT_NEG_14",
    "ETC_GMT_NEG_2",
    "ETC_GMT_NEG_3",
    "ETC_GMT_NEG_4",
    "ETC_GMT_NEG_5",
    "ETC_GMT_NEG_6",
    "ETC_GMT_NEG_7",
    "ETC_GMT_NEG_8",
    "ETC_GMT_NEG_9",
    "EUROPE_DUBLIN",
    "EUROPE_LONDON",
    "EUROPE_PARIS",
    "EUROPE_STOCKHOLM",
    "EUROPE_ZURICH",
    "ISRAEL",
    "MEXICO_GENERAL",
    "MST7MDT",
    "PACIFIC_AUCKLAND",
    "US_CENTRAL",
    "US_EASTERN",
    "US_MOUNTAIN",
    "US_PACIFIC",
    "UTC",
]
TypesSearchScopeType = Literal["ASSET_TYPE", "FORM_TYPE", "LINEAGE_NODE_TYPE"]
UserAssignmentType = Literal["AUTOMATIC", "MANUAL"]
UserDesignationType = Literal[
    "PROJECT_CATALOG_CONSUMER",
    "PROJECT_CATALOG_STEWARD",
    "PROJECT_CATALOG_VIEWER",
    "PROJECT_CONTRIBUTOR",
    "PROJECT_OWNER",
]
UserProfileStatusType = Literal["ACTIVATED", "ASSIGNED", "DEACTIVATED", "NOT_ASSIGNED"]
UserProfileTypeType = Literal["IAM", "SSO"]
UserSearchTypeType = Literal["DATAZONE_IAM_USER", "DATAZONE_SSO_USER", "DATAZONE_USER", "SSO_USER"]
UserTypeType = Literal["IAM_ROLE", "IAM_USER", "SSO_USER"]
DataZoneServiceName = Literal["datazone"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appfabric",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "application-signals",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "apptest",
    "arc-zonal-shift",
    "artifact",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "b2bi",
    "backup",
    "backup-gateway",
    "batch",
    "bcm-data-exports",
    "bcm-pricing-calculator",
    "bedrock",
    "bedrock-agent",
    "bedrock-agent-runtime",
    "bedrock-runtime",
    "billing",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chatbot",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-media-pipelines",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "chime-sdk-voice",
    "cleanrooms",
    "cleanroomsml",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudfront-keyvaluestore",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudtrail-data",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecatalyst",
    "codecommit",
    "codeconnections",
    "codedeploy",
    "codeguru-reviewer",
    "codeguru-security",
    "codeguruprofiler",
    "codepipeline",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectcampaigns",
    "connectcampaignsv2",
    "connectcases",
    "connectparticipant",
    "controlcatalog",
    "controltower",
    "cost-optimization-hub",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "datazone",
    "dax",
    "deadline",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "docdb-elastic",
    "drs",
    "ds",
    "ds-data",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "eks-auth",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "emr-serverless",
    "entityresolution",
    "es",
    "events",
    "evidently",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "freetier",
    "fsx",
    "gamelift",
    "geo-maps",
    "geo-places",
    "geo-routes",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector-scan",
    "inspector2",
    "internetmonitor",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotfleetwise",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "ivs-realtime",
    "ivschat",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kendra-ranking",
    "keyspaces",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesis-video-webrtc-storage",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "launch-wizard",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "license-manager-linux-subscriptions",
    "license-manager-user-subscriptions",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "m2",
    "machinelearning",
    "macie2",
    "mailmanager",
    "managedblockchain",
    "managedblockchain-query",
    "marketplace-agreement",
    "marketplace-catalog",
    "marketplace-deployment",
    "marketplace-entitlement",
    "marketplace-reporting",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediapackagev2",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "medical-imaging",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhuborchestrator",
    "migrationhubstrategy",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "neptune-graph",
    "neptunedata",
    "network-firewall",
    "networkmanager",
    "networkmonitor",
    "notifications",
    "notificationscontacts",
    "oam",
    "omics",
    "opensearch",
    "opensearchserverless",
    "opsworks",
    "opsworkscm",
    "organizations",
    "osis",
    "outposts",
    "panorama",
    "partnercentral-selling",
    "payment-cryptography",
    "payment-cryptography-data",
    "pca-connector-ad",
    "pca-connector-scep",
    "pcs",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "pinpoint-sms-voice-v2",
    "pipes",
    "polly",
    "pricing",
    "privatenetworks",
    "proton",
    "qapps",
    "qbusiness",
    "qconnect",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "redshift-serverless",
    "rekognition",
    "repostspace",
    "resiliencehub",
    "resource-explorer-2",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "rolesanywhere",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53profiles",
    "route53resolver",
    "rum",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-geospatial",
    "sagemaker-metrics",
    "sagemaker-runtime",
    "savingsplans",
    "scheduler",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "securitylake",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "simspaceweaver",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "socialmessaging",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "ssm-quicksetup",
    "ssm-sap",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "supplychain",
    "support",
    "support-app",
    "swf",
    "synthetics",
    "taxsettings",
    "textract",
    "timestream-influxdb",
    "timestream-query",
    "timestream-write",
    "tnb",
    "transcribe",
    "transfer",
    "translate",
    "trustedadvisor",
    "verifiedpermissions",
    "voice-id",
    "vpc-lattice",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-thin-client",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation",
    "cloudwatch",
    "dynamodb",
    "ec2",
    "glacier",
    "iam",
    "opsworks",
    "s3",
    "sns",
    "sqs",
]
PaginatorName = Literal[
    "list_asset_filters",
    "list_asset_revisions",
    "list_data_product_revisions",
    "list_data_source_run_activities",
    "list_data_source_runs",
    "list_data_sources",
    "list_domain_units_for_parent",
    "list_domains",
    "list_entity_owners",
    "list_environment_actions",
    "list_environment_blueprint_configurations",
    "list_environment_blueprints",
    "list_environment_profiles",
    "list_environments",
    "list_lineage_node_history",
    "list_metadata_generation_runs",
    "list_notifications",
    "list_policy_grants",
    "list_project_memberships",
    "list_projects",
    "list_rules",
    "list_subscription_grants",
    "list_subscription_requests",
    "list_subscription_targets",
    "list_subscriptions",
    "list_time_series_data_points",
    "search",
    "search_group_profiles",
    "search_listings",
    "search_types",
    "search_user_profiles",
]
RegionName = Literal[
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ap-southeast-5",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-north-1",
    "eu-south-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
