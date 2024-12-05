"""
Type annotations for qconnect service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qconnect/literals/)

Usage::

    ```python
    from mypy_boto3_qconnect.literals import AIAgentAssociationConfigurationTypeType

    data: AIAgentAssociationConfigurationTypeType = "KNOWLEDGE_BASE"
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AIAgentAssociationConfigurationTypeType",
    "AIAgentTypeType",
    "AIPromptAPIFormatType",
    "AIPromptTemplateTypeType",
    "AIPromptTypeType",
    "AssistantCapabilityTypeType",
    "AssistantStatusType",
    "AssistantTypeType",
    "AssociationTypeType",
    "ChannelSubtypeType",
    "ChunkingStrategyType",
    "ContentAssociationTypeType",
    "ContentDispositionType",
    "ContentStatusType",
    "ExternalSourceType",
    "FilterFieldType",
    "FilterOperatorType",
    "ImportJobStatusType",
    "ImportJobTypeType",
    "KnowledgeBaseSearchTypeType",
    "KnowledgeBaseStatusType",
    "KnowledgeBaseTypeType",
    "ListAIAgentVersionsPaginatorName",
    "ListAIAgentsPaginatorName",
    "ListAIPromptVersionsPaginatorName",
    "ListAIPromptsPaginatorName",
    "ListAssistantAssociationsPaginatorName",
    "ListAssistantsPaginatorName",
    "ListContentAssociationsPaginatorName",
    "ListContentsPaginatorName",
    "ListImportJobsPaginatorName",
    "ListKnowledgeBasesPaginatorName",
    "ListMessageTemplateVersionsPaginatorName",
    "ListMessageTemplatesPaginatorName",
    "ListQuickResponsesPaginatorName",
    "MessageTemplateAttributeTypeType",
    "MessageTemplateFilterOperatorType",
    "MessageTemplateQueryOperatorType",
    "OrderType",
    "OriginType",
    "PaginatorName",
    "ParsingStrategyType",
    "PriorityType",
    "QConnectServiceName",
    "QueryAssistantPaginatorName",
    "QueryConditionComparisonOperatorType",
    "QueryConditionFieldNameType",
    "QueryResultTypeType",
    "QuickResponseFilterOperatorType",
    "QuickResponseQueryOperatorType",
    "QuickResponseStatusType",
    "RecommendationSourceTypeType",
    "RecommendationTriggerTypeType",
    "RecommendationTypeType",
    "ReferenceTypeType",
    "RegionName",
    "RelevanceLevelType",
    "RelevanceType",
    "ResourceServiceName",
    "SearchContentPaginatorName",
    "SearchMessageTemplatesPaginatorName",
    "SearchQuickResponsesPaginatorName",
    "SearchSessionsPaginatorName",
    "ServiceName",
    "SessionDataNamespaceType",
    "SourceContentTypeType",
    "StatusType",
    "SyncStatusType",
    "TargetTypeType",
    "VisibilityStatusType",
    "WebScopeTypeType",
)


AIAgentAssociationConfigurationTypeType = Literal["KNOWLEDGE_BASE"]
AIAgentTypeType = Literal["ANSWER_RECOMMENDATION", "MANUAL_SEARCH"]
AIPromptAPIFormatType = Literal["ANTHROPIC_CLAUDE_MESSAGES", "ANTHROPIC_CLAUDE_TEXT_COMPLETIONS"]
AIPromptTemplateTypeType = Literal["TEXT"]
AIPromptTypeType = Literal["ANSWER_GENERATION", "INTENT_LABELING_GENERATION", "QUERY_REFORMULATION"]
AssistantCapabilityTypeType = Literal["V1", "V2"]
AssistantStatusType = Literal[
    "ACTIVE",
    "CREATE_FAILED",
    "CREATE_IN_PROGRESS",
    "DELETED",
    "DELETE_FAILED",
    "DELETE_IN_PROGRESS",
]
AssistantTypeType = Literal["AGENT"]
AssociationTypeType = Literal["KNOWLEDGE_BASE"]
ChannelSubtypeType = Literal["EMAIL", "SMS"]
ChunkingStrategyType = Literal["FIXED_SIZE", "HIERARCHICAL", "NONE", "SEMANTIC"]
ContentAssociationTypeType = Literal["AMAZON_CONNECT_GUIDE"]
ContentDispositionType = Literal["ATTACHMENT"]
ContentStatusType = Literal[
    "ACTIVE",
    "CREATE_FAILED",
    "CREATE_IN_PROGRESS",
    "DELETED",
    "DELETE_FAILED",
    "DELETE_IN_PROGRESS",
    "UPDATE_FAILED",
]
ExternalSourceType = Literal["AMAZON_CONNECT"]
FilterFieldType = Literal["NAME"]
FilterOperatorType = Literal["EQUALS"]
ImportJobStatusType = Literal[
    "COMPLETE", "DELETED", "DELETE_FAILED", "DELETE_IN_PROGRESS", "FAILED", "START_IN_PROGRESS"
]
ImportJobTypeType = Literal["QUICK_RESPONSES"]
KnowledgeBaseSearchTypeType = Literal["HYBRID", "SEMANTIC"]
KnowledgeBaseStatusType = Literal[
    "ACTIVE",
    "CREATE_FAILED",
    "CREATE_IN_PROGRESS",
    "DELETED",
    "DELETE_FAILED",
    "DELETE_IN_PROGRESS",
]
KnowledgeBaseTypeType = Literal[
    "CUSTOM", "EXTERNAL", "MANAGED", "MESSAGE_TEMPLATES", "QUICK_RESPONSES"
]
ListAIAgentVersionsPaginatorName = Literal["list_ai_agent_versions"]
ListAIAgentsPaginatorName = Literal["list_ai_agents"]
ListAIPromptVersionsPaginatorName = Literal["list_ai_prompt_versions"]
ListAIPromptsPaginatorName = Literal["list_ai_prompts"]
ListAssistantAssociationsPaginatorName = Literal["list_assistant_associations"]
ListAssistantsPaginatorName = Literal["list_assistants"]
ListContentAssociationsPaginatorName = Literal["list_content_associations"]
ListContentsPaginatorName = Literal["list_contents"]
ListImportJobsPaginatorName = Literal["list_import_jobs"]
ListKnowledgeBasesPaginatorName = Literal["list_knowledge_bases"]
ListMessageTemplateVersionsPaginatorName = Literal["list_message_template_versions"]
ListMessageTemplatesPaginatorName = Literal["list_message_templates"]
ListQuickResponsesPaginatorName = Literal["list_quick_responses"]
MessageTemplateAttributeTypeType = Literal["AGENT", "CUSTOM", "CUSTOMER_PROFILE", "SYSTEM"]
MessageTemplateFilterOperatorType = Literal["EQUALS", "PREFIX"]
MessageTemplateQueryOperatorType = Literal["CONTAINS", "CONTAINS_AND_PREFIX"]
OrderType = Literal["ASC", "DESC"]
OriginType = Literal["CUSTOMER", "SYSTEM"]
ParsingStrategyType = Literal["BEDROCK_FOUNDATION_MODEL"]
PriorityType = Literal["HIGH", "LOW", "MEDIUM"]
QueryAssistantPaginatorName = Literal["query_assistant"]
QueryConditionComparisonOperatorType = Literal["EQUALS"]
QueryConditionFieldNameType = Literal["RESULT_TYPE"]
QueryResultTypeType = Literal["GENERATIVE_ANSWER", "INTENT_ANSWER", "KNOWLEDGE_CONTENT"]
QuickResponseFilterOperatorType = Literal["EQUALS", "PREFIX"]
QuickResponseQueryOperatorType = Literal["CONTAINS", "CONTAINS_AND_PREFIX"]
QuickResponseStatusType = Literal[
    "CREATED",
    "CREATE_FAILED",
    "CREATE_IN_PROGRESS",
    "DELETED",
    "DELETE_FAILED",
    "DELETE_IN_PROGRESS",
    "UPDATE_FAILED",
    "UPDATE_IN_PROGRESS",
]
RecommendationSourceTypeType = Literal["ISSUE_DETECTION", "OTHER", "RULE_EVALUATION"]
RecommendationTriggerTypeType = Literal["GENERATIVE", "QUERY"]
RecommendationTypeType = Literal[
    "DETECTED_INTENT", "GENERATIVE_ANSWER", "GENERATIVE_RESPONSE", "KNOWLEDGE_CONTENT"
]
ReferenceTypeType = Literal["KNOWLEDGE_BASE", "WEB_CRAWLER"]
RelevanceLevelType = Literal["HIGH", "LOW", "MEDIUM"]
RelevanceType = Literal["HELPFUL", "NOT_HELPFUL"]
SearchContentPaginatorName = Literal["search_content"]
SearchMessageTemplatesPaginatorName = Literal["search_message_templates"]
SearchQuickResponsesPaginatorName = Literal["search_quick_responses"]
SearchSessionsPaginatorName = Literal["search_sessions"]
SessionDataNamespaceType = Literal["Custom"]
SourceContentTypeType = Literal["KNOWLEDGE_CONTENT"]
StatusType = Literal[
    "ACTIVE",
    "CREATE_FAILED",
    "CREATE_IN_PROGRESS",
    "DELETED",
    "DELETE_FAILED",
    "DELETE_IN_PROGRESS",
]
SyncStatusType = Literal["CREATE_IN_PROGRESS", "SYNCING_IN_PROGRESS", "SYNC_FAILED", "SYNC_SUCCESS"]
TargetTypeType = Literal["RECOMMENDATION", "RESULT"]
VisibilityStatusType = Literal["PUBLISHED", "SAVED"]
WebScopeTypeType = Literal["HOST_ONLY", "SUBDOMAINS"]
QConnectServiceName = Literal["qconnect"]
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
    "list_ai_agent_versions",
    "list_ai_agents",
    "list_ai_prompt_versions",
    "list_ai_prompts",
    "list_assistant_associations",
    "list_assistants",
    "list_content_associations",
    "list_contents",
    "list_import_jobs",
    "list_knowledge_bases",
    "list_message_template_versions",
    "list_message_templates",
    "list_quick_responses",
    "query_assistant",
    "search_content",
    "search_message_templates",
    "search_quick_responses",
    "search_sessions",
]
RegionName = Literal[
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-west-2",
    "us-east-1",
    "us-west-2",
]
