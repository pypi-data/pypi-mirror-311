"""
Type annotations for backup service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/literals/)

Usage::

    ```python
    from mypy_boto3_backup.literals import AggregationPeriodType

    data: AggregationPeriodType = "FOURTEEN_DAYS"
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AggregationPeriodType",
    "BackupJobStateType",
    "BackupJobStatusType",
    "BackupServiceName",
    "BackupVaultEventType",
    "ConditionTypeType",
    "CopyJobStateType",
    "CopyJobStatusType",
    "LegalHoldStatusType",
    "ListBackupJobsPaginatorName",
    "ListBackupPlanTemplatesPaginatorName",
    "ListBackupPlanVersionsPaginatorName",
    "ListBackupPlansPaginatorName",
    "ListBackupSelectionsPaginatorName",
    "ListBackupVaultsPaginatorName",
    "ListCopyJobsPaginatorName",
    "ListLegalHoldsPaginatorName",
    "ListProtectedResourcesByBackupVaultPaginatorName",
    "ListProtectedResourcesPaginatorName",
    "ListRecoveryPointsByBackupVaultPaginatorName",
    "ListRecoveryPointsByLegalHoldPaginatorName",
    "ListRecoveryPointsByResourcePaginatorName",
    "ListRestoreJobsByProtectedResourcePaginatorName",
    "ListRestoreJobsPaginatorName",
    "ListRestoreTestingPlansPaginatorName",
    "ListRestoreTestingSelectionsPaginatorName",
    "PaginatorName",
    "RecoveryPointStatusType",
    "RegionName",
    "ResourceServiceName",
    "RestoreDeletionStatusType",
    "RestoreJobStateType",
    "RestoreJobStatusType",
    "RestoreTestingRecoveryPointSelectionAlgorithmType",
    "RestoreTestingRecoveryPointTypeType",
    "RestoreValidationStatusType",
    "ServiceName",
    "StorageClassType",
    "VaultStateType",
    "VaultTypeType",
)


AggregationPeriodType = Literal["FOURTEEN_DAYS", "ONE_DAY", "SEVEN_DAYS"]
BackupJobStateType = Literal[
    "ABORTED",
    "ABORTING",
    "COMPLETED",
    "CREATED",
    "EXPIRED",
    "FAILED",
    "PARTIAL",
    "PENDING",
    "RUNNING",
]
BackupJobStatusType = Literal[
    "ABORTED",
    "ABORTING",
    "AGGREGATE_ALL",
    "ANY",
    "COMPLETED",
    "CREATED",
    "EXPIRED",
    "FAILED",
    "PARTIAL",
    "PENDING",
    "RUNNING",
]
BackupVaultEventType = Literal[
    "BACKUP_JOB_COMPLETED",
    "BACKUP_JOB_EXPIRED",
    "BACKUP_JOB_FAILED",
    "BACKUP_JOB_STARTED",
    "BACKUP_JOB_SUCCESSFUL",
    "BACKUP_PLAN_CREATED",
    "BACKUP_PLAN_MODIFIED",
    "COPY_JOB_FAILED",
    "COPY_JOB_STARTED",
    "COPY_JOB_SUCCESSFUL",
    "RECOVERY_POINT_MODIFIED",
    "RESTORE_JOB_COMPLETED",
    "RESTORE_JOB_FAILED",
    "RESTORE_JOB_STARTED",
    "RESTORE_JOB_SUCCESSFUL",
    "S3_BACKUP_OBJECT_FAILED",
    "S3_RESTORE_OBJECT_FAILED",
]
ConditionTypeType = Literal["STRINGEQUALS"]
CopyJobStateType = Literal["COMPLETED", "CREATED", "FAILED", "PARTIAL", "RUNNING"]
CopyJobStatusType = Literal[
    "ABORTED",
    "ABORTING",
    "AGGREGATE_ALL",
    "ANY",
    "COMPLETED",
    "COMPLETING",
    "CREATED",
    "FAILED",
    "FAILING",
    "PARTIAL",
    "RUNNING",
]
LegalHoldStatusType = Literal["ACTIVE", "CANCELED", "CANCELING", "CREATING"]
ListBackupJobsPaginatorName = Literal["list_backup_jobs"]
ListBackupPlanTemplatesPaginatorName = Literal["list_backup_plan_templates"]
ListBackupPlanVersionsPaginatorName = Literal["list_backup_plan_versions"]
ListBackupPlansPaginatorName = Literal["list_backup_plans"]
ListBackupSelectionsPaginatorName = Literal["list_backup_selections"]
ListBackupVaultsPaginatorName = Literal["list_backup_vaults"]
ListCopyJobsPaginatorName = Literal["list_copy_jobs"]
ListLegalHoldsPaginatorName = Literal["list_legal_holds"]
ListProtectedResourcesByBackupVaultPaginatorName = Literal[
    "list_protected_resources_by_backup_vault"
]
ListProtectedResourcesPaginatorName = Literal["list_protected_resources"]
ListRecoveryPointsByBackupVaultPaginatorName = Literal["list_recovery_points_by_backup_vault"]
ListRecoveryPointsByLegalHoldPaginatorName = Literal["list_recovery_points_by_legal_hold"]
ListRecoveryPointsByResourcePaginatorName = Literal["list_recovery_points_by_resource"]
ListRestoreJobsByProtectedResourcePaginatorName = Literal["list_restore_jobs_by_protected_resource"]
ListRestoreJobsPaginatorName = Literal["list_restore_jobs"]
ListRestoreTestingPlansPaginatorName = Literal["list_restore_testing_plans"]
ListRestoreTestingSelectionsPaginatorName = Literal["list_restore_testing_selections"]
RecoveryPointStatusType = Literal["COMPLETED", "DELETING", "EXPIRED", "PARTIAL"]
RestoreDeletionStatusType = Literal["DELETING", "FAILED", "SUCCESSFUL"]
RestoreJobStateType = Literal[
    "ABORTED", "AGGREGATE_ALL", "ANY", "COMPLETED", "CREATED", "FAILED", "PENDING", "RUNNING"
]
RestoreJobStatusType = Literal["ABORTED", "COMPLETED", "FAILED", "PENDING", "RUNNING"]
RestoreTestingRecoveryPointSelectionAlgorithmType = Literal[
    "LATEST_WITHIN_WINDOW", "RANDOM_WITHIN_WINDOW"
]
RestoreTestingRecoveryPointTypeType = Literal["CONTINUOUS", "SNAPSHOT"]
RestoreValidationStatusType = Literal["FAILED", "SUCCESSFUL", "TIMED_OUT", "VALIDATING"]
StorageClassType = Literal["COLD", "DELETED", "WARM"]
VaultStateType = Literal["AVAILABLE", "CREATING", "FAILED"]
VaultTypeType = Literal["BACKUP_VAULT", "LOGICALLY_AIR_GAPPED_BACKUP_VAULT"]
BackupServiceName = Literal["backup"]
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
    "list_backup_jobs",
    "list_backup_plan_templates",
    "list_backup_plan_versions",
    "list_backup_plans",
    "list_backup_selections",
    "list_backup_vaults",
    "list_copy_jobs",
    "list_legal_holds",
    "list_protected_resources",
    "list_protected_resources_by_backup_vault",
    "list_recovery_points_by_backup_vault",
    "list_recovery_points_by_legal_hold",
    "list_recovery_points_by_resource",
    "list_restore_jobs",
    "list_restore_jobs_by_protected_resource",
    "list_restore_testing_plans",
    "list_restore_testing_selections",
]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ap-southeast-5",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
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
