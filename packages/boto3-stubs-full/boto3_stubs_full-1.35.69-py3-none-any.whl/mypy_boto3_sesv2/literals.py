"""
Type annotations for sesv2 service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/literals/)

Usage::

    ```python
    from mypy_boto3_sesv2.literals import BehaviorOnMxFailureType

    data: BehaviorOnMxFailureType = "REJECT_MESSAGE"
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "BehaviorOnMxFailureType",
    "BounceTypeType",
    "BulkEmailStatusType",
    "ContactLanguageType",
    "ContactListImportActionType",
    "DataFormatType",
    "DeliverabilityDashboardAccountStatusType",
    "DeliverabilityTestStatusType",
    "DeliveryEventTypeType",
    "DimensionValueSourceType",
    "DkimSigningAttributesOriginType",
    "DkimSigningKeyLengthType",
    "DkimStatusType",
    "EngagementEventTypeType",
    "EventTypeType",
    "ExportSourceTypeType",
    "FeatureStatusType",
    "HttpsPolicyType",
    "IdentityTypeType",
    "ImportDestinationTypeType",
    "JobStatusType",
    "ListRecommendationsFilterKeyType",
    "MailFromDomainStatusType",
    "MailTypeType",
    "MetricAggregationType",
    "MetricDimensionNameType",
    "MetricNamespaceType",
    "MetricType",
    "QueryErrorCodeType",
    "RecommendationImpactType",
    "RecommendationStatusType",
    "RecommendationTypeType",
    "RegionName",
    "ResourceServiceName",
    "ReviewStatusType",
    "SESV2ServiceName",
    "ScalingModeType",
    "ServiceName",
    "SubscriptionStatusType",
    "SuppressionListImportActionType",
    "SuppressionListReasonType",
    "TlsPolicyType",
    "VerificationErrorType",
    "VerificationStatusType",
    "WarmupStatusType",
)


BehaviorOnMxFailureType = Literal["REJECT_MESSAGE", "USE_DEFAULT_VALUE"]
BounceTypeType = Literal["PERMANENT", "TRANSIENT", "UNDETERMINED"]
BulkEmailStatusType = Literal[
    "ACCOUNT_DAILY_QUOTA_EXCEEDED",
    "ACCOUNT_SENDING_PAUSED",
    "ACCOUNT_SUSPENDED",
    "ACCOUNT_THROTTLED",
    "CONFIGURATION_SET_NOT_FOUND",
    "CONFIGURATION_SET_SENDING_PAUSED",
    "FAILED",
    "INVALID_PARAMETER",
    "INVALID_SENDING_POOL_NAME",
    "MAIL_FROM_DOMAIN_NOT_VERIFIED",
    "MESSAGE_REJECTED",
    "SUCCESS",
    "TEMPLATE_NOT_FOUND",
    "TRANSIENT_FAILURE",
]
ContactLanguageType = Literal["EN", "JA"]
ContactListImportActionType = Literal["DELETE", "PUT"]
DataFormatType = Literal["CSV", "JSON"]
DeliverabilityDashboardAccountStatusType = Literal["ACTIVE", "DISABLED", "PENDING_EXPIRATION"]
DeliverabilityTestStatusType = Literal["COMPLETED", "IN_PROGRESS"]
DeliveryEventTypeType = Literal[
    "COMPLAINT", "DELIVERY", "PERMANENT_BOUNCE", "SEND", "TRANSIENT_BOUNCE", "UNDETERMINED_BOUNCE"
]
DimensionValueSourceType = Literal["EMAIL_HEADER", "LINK_TAG", "MESSAGE_TAG"]
DkimSigningAttributesOriginType = Literal["AWS_SES", "EXTERNAL"]
DkimSigningKeyLengthType = Literal["RSA_1024_BIT", "RSA_2048_BIT"]
DkimStatusType = Literal["FAILED", "NOT_STARTED", "PENDING", "SUCCESS", "TEMPORARY_FAILURE"]
EngagementEventTypeType = Literal["CLICK", "OPEN"]
EventTypeType = Literal[
    "BOUNCE",
    "CLICK",
    "COMPLAINT",
    "DELIVERY",
    "DELIVERY_DELAY",
    "OPEN",
    "REJECT",
    "RENDERING_FAILURE",
    "SEND",
    "SUBSCRIPTION",
]
ExportSourceTypeType = Literal["MESSAGE_INSIGHTS", "METRICS_DATA"]
FeatureStatusType = Literal["DISABLED", "ENABLED"]
HttpsPolicyType = Literal["OPTIONAL", "REQUIRE", "REQUIRE_OPEN_ONLY"]
IdentityTypeType = Literal["DOMAIN", "EMAIL_ADDRESS", "MANAGED_DOMAIN"]
ImportDestinationTypeType = Literal["CONTACT_LIST", "SUPPRESSION_LIST"]
JobStatusType = Literal["CANCELLED", "COMPLETED", "CREATED", "FAILED", "PROCESSING"]
ListRecommendationsFilterKeyType = Literal["IMPACT", "RESOURCE_ARN", "STATUS", "TYPE"]
MailFromDomainStatusType = Literal["FAILED", "PENDING", "SUCCESS", "TEMPORARY_FAILURE"]
MailTypeType = Literal["MARKETING", "TRANSACTIONAL"]
MetricAggregationType = Literal["RATE", "VOLUME"]
MetricDimensionNameType = Literal["CONFIGURATION_SET", "EMAIL_IDENTITY", "ISP"]
MetricNamespaceType = Literal["VDM"]
MetricType = Literal[
    "CLICK",
    "COMPLAINT",
    "DELIVERY",
    "DELIVERY_CLICK",
    "DELIVERY_COMPLAINT",
    "DELIVERY_OPEN",
    "OPEN",
    "PERMANENT_BOUNCE",
    "SEND",
    "TRANSIENT_BOUNCE",
]
QueryErrorCodeType = Literal["ACCESS_DENIED", "INTERNAL_FAILURE"]
RecommendationImpactType = Literal["HIGH", "LOW"]
RecommendationStatusType = Literal["FIXED", "OPEN"]
RecommendationTypeType = Literal["BIMI", "DKIM", "DMARC", "SPF"]
ReviewStatusType = Literal["DENIED", "FAILED", "GRANTED", "PENDING"]
ScalingModeType = Literal["MANAGED", "STANDARD"]
SubscriptionStatusType = Literal["OPT_IN", "OPT_OUT"]
SuppressionListImportActionType = Literal["DELETE", "PUT"]
SuppressionListReasonType = Literal["BOUNCE", "COMPLAINT"]
TlsPolicyType = Literal["OPTIONAL", "REQUIRE"]
VerificationErrorType = Literal[
    "DNS_SERVER_ERROR", "HOST_NOT_FOUND", "INVALID_VALUE", "SERVICE_ERROR", "TYPE_NOT_FOUND"
]
VerificationStatusType = Literal["FAILED", "NOT_STARTED", "PENDING", "SUCCESS", "TEMPORARY_FAILURE"]
WarmupStatusType = Literal["DONE", "IN_PROGRESS"]
SESV2ServiceName = Literal["sesv2"]
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
RegionName = Literal[
    "af-south-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ca-central-1",
    "eu-central-1",
    "eu-north-1",
    "eu-south-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
