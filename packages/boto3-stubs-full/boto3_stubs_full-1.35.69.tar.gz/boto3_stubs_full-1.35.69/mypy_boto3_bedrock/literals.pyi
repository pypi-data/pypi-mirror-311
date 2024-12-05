"""
Type annotations for bedrock service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/literals/)

Usage::

    ```python
    from mypy_boto3_bedrock.literals import CommitmentDurationType

    data: CommitmentDurationType = "OneMonth"
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "BedrockServiceName",
    "CommitmentDurationType",
    "CustomizationTypeType",
    "EvaluationJobStatusType",
    "EvaluationJobTypeType",
    "EvaluationTaskTypeType",
    "FineTuningJobStatusType",
    "FoundationModelLifecycleStatusType",
    "GuardrailContentFilterTypeType",
    "GuardrailContextualGroundingFilterTypeType",
    "GuardrailFilterStrengthType",
    "GuardrailManagedWordsTypeType",
    "GuardrailPiiEntityTypeType",
    "GuardrailSensitiveInformationActionType",
    "GuardrailStatusType",
    "GuardrailTopicTypeType",
    "InferenceProfileStatusType",
    "InferenceProfileTypeType",
    "InferenceTypeType",
    "ListCustomModelsPaginatorName",
    "ListEvaluationJobsPaginatorName",
    "ListGuardrailsPaginatorName",
    "ListImportedModelsPaginatorName",
    "ListInferenceProfilesPaginatorName",
    "ListModelCopyJobsPaginatorName",
    "ListModelCustomizationJobsPaginatorName",
    "ListModelImportJobsPaginatorName",
    "ListModelInvocationJobsPaginatorName",
    "ListProvisionedModelThroughputsPaginatorName",
    "ModelCopyJobStatusType",
    "ModelCustomizationJobStatusType",
    "ModelCustomizationType",
    "ModelImportJobStatusType",
    "ModelInvocationJobStatusType",
    "ModelModalityType",
    "PaginatorName",
    "ProvisionedModelStatusType",
    "RegionName",
    "ResourceServiceName",
    "S3InputFormatType",
    "ServiceName",
    "SortByProvisionedModelsType",
    "SortJobsByType",
    "SortModelsByType",
    "SortOrderType",
)

CommitmentDurationType = Literal["OneMonth", "SixMonths"]
CustomizationTypeType = Literal["CONTINUED_PRE_TRAINING", "FINE_TUNING"]
EvaluationJobStatusType = Literal[
    "Completed", "Deleting", "Failed", "InProgress", "Stopped", "Stopping"
]
EvaluationJobTypeType = Literal["Automated", "Human"]
EvaluationTaskTypeType = Literal[
    "Classification", "Custom", "Generation", "QuestionAndAnswer", "Summarization"
]
FineTuningJobStatusType = Literal["Completed", "Failed", "InProgress", "Stopped", "Stopping"]
FoundationModelLifecycleStatusType = Literal["ACTIVE", "LEGACY"]
GuardrailContentFilterTypeType = Literal[
    "HATE", "INSULTS", "MISCONDUCT", "PROMPT_ATTACK", "SEXUAL", "VIOLENCE"
]
GuardrailContextualGroundingFilterTypeType = Literal["GROUNDING", "RELEVANCE"]
GuardrailFilterStrengthType = Literal["HIGH", "LOW", "MEDIUM", "NONE"]
GuardrailManagedWordsTypeType = Literal["PROFANITY"]
GuardrailPiiEntityTypeType = Literal[
    "ADDRESS",
    "AGE",
    "AWS_ACCESS_KEY",
    "AWS_SECRET_KEY",
    "CA_HEALTH_NUMBER",
    "CA_SOCIAL_INSURANCE_NUMBER",
    "CREDIT_DEBIT_CARD_CVV",
    "CREDIT_DEBIT_CARD_EXPIRY",
    "CREDIT_DEBIT_CARD_NUMBER",
    "DRIVER_ID",
    "EMAIL",
    "INTERNATIONAL_BANK_ACCOUNT_NUMBER",
    "IP_ADDRESS",
    "LICENSE_PLATE",
    "MAC_ADDRESS",
    "NAME",
    "PASSWORD",
    "PHONE",
    "PIN",
    "SWIFT_CODE",
    "UK_NATIONAL_HEALTH_SERVICE_NUMBER",
    "UK_NATIONAL_INSURANCE_NUMBER",
    "UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER",
    "URL",
    "USERNAME",
    "US_BANK_ACCOUNT_NUMBER",
    "US_BANK_ROUTING_NUMBER",
    "US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER",
    "US_PASSPORT_NUMBER",
    "US_SOCIAL_SECURITY_NUMBER",
    "VEHICLE_IDENTIFICATION_NUMBER",
]
GuardrailSensitiveInformationActionType = Literal["ANONYMIZE", "BLOCK"]
GuardrailStatusType = Literal["CREATING", "DELETING", "FAILED", "READY", "UPDATING", "VERSIONING"]
GuardrailTopicTypeType = Literal["DENY"]
InferenceProfileStatusType = Literal["ACTIVE"]
InferenceProfileTypeType = Literal["APPLICATION", "SYSTEM_DEFINED"]
InferenceTypeType = Literal["ON_DEMAND", "PROVISIONED"]
ListCustomModelsPaginatorName = Literal["list_custom_models"]
ListEvaluationJobsPaginatorName = Literal["list_evaluation_jobs"]
ListGuardrailsPaginatorName = Literal["list_guardrails"]
ListImportedModelsPaginatorName = Literal["list_imported_models"]
ListInferenceProfilesPaginatorName = Literal["list_inference_profiles"]
ListModelCopyJobsPaginatorName = Literal["list_model_copy_jobs"]
ListModelCustomizationJobsPaginatorName = Literal["list_model_customization_jobs"]
ListModelImportJobsPaginatorName = Literal["list_model_import_jobs"]
ListModelInvocationJobsPaginatorName = Literal["list_model_invocation_jobs"]
ListProvisionedModelThroughputsPaginatorName = Literal["list_provisioned_model_throughputs"]
ModelCopyJobStatusType = Literal["Completed", "Failed", "InProgress"]
ModelCustomizationJobStatusType = Literal[
    "Completed", "Failed", "InProgress", "Stopped", "Stopping"
]
ModelCustomizationType = Literal["CONTINUED_PRE_TRAINING", "FINE_TUNING"]
ModelImportJobStatusType = Literal["Completed", "Failed", "InProgress"]
ModelInvocationJobStatusType = Literal[
    "Completed",
    "Expired",
    "Failed",
    "InProgress",
    "PartiallyCompleted",
    "Scheduled",
    "Stopped",
    "Stopping",
    "Submitted",
    "Validating",
]
ModelModalityType = Literal["EMBEDDING", "IMAGE", "TEXT"]
ProvisionedModelStatusType = Literal["Creating", "Failed", "InService", "Updating"]
S3InputFormatType = Literal["JSONL"]
SortByProvisionedModelsType = Literal["CreationTime"]
SortJobsByType = Literal["CreationTime"]
SortModelsByType = Literal["CreationTime"]
SortOrderType = Literal["Ascending", "Descending"]
BedrockServiceName = Literal["bedrock"]
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
    "list_custom_models",
    "list_evaluation_jobs",
    "list_guardrails",
    "list_imported_models",
    "list_inference_profiles",
    "list_model_copy_jobs",
    "list_model_customization_jobs",
    "list_model_import_jobs",
    "list_model_invocation_jobs",
    "list_provisioned_model_throughputs",
]
RegionName = Literal[
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-central-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-2",
]
