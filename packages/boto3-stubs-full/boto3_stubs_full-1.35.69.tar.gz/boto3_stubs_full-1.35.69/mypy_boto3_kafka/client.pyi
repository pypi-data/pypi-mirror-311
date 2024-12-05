"""
Type annotations for kafka service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kafka.client import KafkaClient

    session = Session()
    client: KafkaClient = session.client("kafka")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListClientVpcConnectionsPaginator,
    ListClusterOperationsPaginator,
    ListClusterOperationsV2Paginator,
    ListClustersPaginator,
    ListClustersV2Paginator,
    ListConfigurationRevisionsPaginator,
    ListConfigurationsPaginator,
    ListKafkaVersionsPaginator,
    ListNodesPaginator,
    ListReplicatorsPaginator,
    ListScramSecretsPaginator,
    ListVpcConnectionsPaginator,
)
from .type_defs import (
    BatchAssociateScramSecretRequestRequestTypeDef,
    BatchAssociateScramSecretResponseTypeDef,
    BatchDisassociateScramSecretRequestRequestTypeDef,
    BatchDisassociateScramSecretResponseTypeDef,
    CreateClusterRequestRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateClusterV2RequestRequestTypeDef,
    CreateClusterV2ResponseTypeDef,
    CreateConfigurationRequestRequestTypeDef,
    CreateConfigurationResponseTypeDef,
    CreateReplicatorRequestRequestTypeDef,
    CreateReplicatorResponseTypeDef,
    CreateVpcConnectionRequestRequestTypeDef,
    CreateVpcConnectionResponseTypeDef,
    DeleteClusterPolicyRequestRequestTypeDef,
    DeleteClusterRequestRequestTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteConfigurationRequestRequestTypeDef,
    DeleteConfigurationResponseTypeDef,
    DeleteReplicatorRequestRequestTypeDef,
    DeleteReplicatorResponseTypeDef,
    DeleteVpcConnectionRequestRequestTypeDef,
    DeleteVpcConnectionResponseTypeDef,
    DescribeClusterOperationRequestRequestTypeDef,
    DescribeClusterOperationResponseTypeDef,
    DescribeClusterOperationV2RequestRequestTypeDef,
    DescribeClusterOperationV2ResponseTypeDef,
    DescribeClusterRequestRequestTypeDef,
    DescribeClusterResponseTypeDef,
    DescribeClusterV2RequestRequestTypeDef,
    DescribeClusterV2ResponseTypeDef,
    DescribeConfigurationRequestRequestTypeDef,
    DescribeConfigurationResponseTypeDef,
    DescribeConfigurationRevisionRequestRequestTypeDef,
    DescribeConfigurationRevisionResponseTypeDef,
    DescribeReplicatorRequestRequestTypeDef,
    DescribeReplicatorResponseTypeDef,
    DescribeVpcConnectionRequestRequestTypeDef,
    DescribeVpcConnectionResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetBootstrapBrokersRequestRequestTypeDef,
    GetBootstrapBrokersResponseTypeDef,
    GetClusterPolicyRequestRequestTypeDef,
    GetClusterPolicyResponseTypeDef,
    GetCompatibleKafkaVersionsRequestRequestTypeDef,
    GetCompatibleKafkaVersionsResponseTypeDef,
    ListClientVpcConnectionsRequestRequestTypeDef,
    ListClientVpcConnectionsResponseTypeDef,
    ListClusterOperationsRequestRequestTypeDef,
    ListClusterOperationsResponseTypeDef,
    ListClusterOperationsV2RequestRequestTypeDef,
    ListClusterOperationsV2ResponseTypeDef,
    ListClustersRequestRequestTypeDef,
    ListClustersResponseTypeDef,
    ListClustersV2RequestRequestTypeDef,
    ListClustersV2ResponseTypeDef,
    ListConfigurationRevisionsRequestRequestTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsRequestRequestTypeDef,
    ListConfigurationsResponseTypeDef,
    ListKafkaVersionsRequestRequestTypeDef,
    ListKafkaVersionsResponseTypeDef,
    ListNodesRequestRequestTypeDef,
    ListNodesResponseTypeDef,
    ListReplicatorsRequestRequestTypeDef,
    ListReplicatorsResponseTypeDef,
    ListScramSecretsRequestRequestTypeDef,
    ListScramSecretsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVpcConnectionsRequestRequestTypeDef,
    ListVpcConnectionsResponseTypeDef,
    PutClusterPolicyRequestRequestTypeDef,
    PutClusterPolicyResponseTypeDef,
    RebootBrokerRequestRequestTypeDef,
    RebootBrokerResponseTypeDef,
    RejectClientVpcConnectionRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBrokerCountRequestRequestTypeDef,
    UpdateBrokerCountResponseTypeDef,
    UpdateBrokerStorageRequestRequestTypeDef,
    UpdateBrokerStorageResponseTypeDef,
    UpdateBrokerTypeRequestRequestTypeDef,
    UpdateBrokerTypeResponseTypeDef,
    UpdateClusterConfigurationRequestRequestTypeDef,
    UpdateClusterConfigurationResponseTypeDef,
    UpdateClusterKafkaVersionRequestRequestTypeDef,
    UpdateClusterKafkaVersionResponseTypeDef,
    UpdateConfigurationRequestRequestTypeDef,
    UpdateConfigurationResponseTypeDef,
    UpdateConnectivityRequestRequestTypeDef,
    UpdateConnectivityResponseTypeDef,
    UpdateMonitoringRequestRequestTypeDef,
    UpdateMonitoringResponseTypeDef,
    UpdateReplicationInfoRequestRequestTypeDef,
    UpdateReplicationInfoResponseTypeDef,
    UpdateSecurityRequestRequestTypeDef,
    UpdateSecurityResponseTypeDef,
    UpdateStorageRequestRequestTypeDef,
    UpdateStorageResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("KafkaClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class KafkaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KafkaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#exceptions)
        """

    def batch_associate_scram_secret(
        self, **kwargs: Unpack[BatchAssociateScramSecretRequestRequestTypeDef]
    ) -> BatchAssociateScramSecretResponseTypeDef:
        """
        Associates one or more Scram Secrets with an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/batch_associate_scram_secret.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#batch_associate_scram_secret)
        """

    def batch_disassociate_scram_secret(
        self, **kwargs: Unpack[BatchDisassociateScramSecretRequestRequestTypeDef]
    ) -> BatchDisassociateScramSecretResponseTypeDef:
        """
        Disassociates one or more Scram Secrets from an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/batch_disassociate_scram_secret.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#batch_disassociate_scram_secret)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#close)
        """

    def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a new MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_cluster)
        """

    def create_cluster_v2(
        self, **kwargs: Unpack[CreateClusterV2RequestRequestTypeDef]
    ) -> CreateClusterV2ResponseTypeDef:
        """
        Creates a new MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_cluster_v2.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_cluster_v2)
        """

    def create_configuration(
        self, **kwargs: Unpack[CreateConfigurationRequestRequestTypeDef]
    ) -> CreateConfigurationResponseTypeDef:
        """
        Creates a new MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_configuration)
        """

    def create_replicator(
        self, **kwargs: Unpack[CreateReplicatorRequestRequestTypeDef]
    ) -> CreateReplicatorResponseTypeDef:
        """
        Creates the replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_replicator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_replicator)
        """

    def create_vpc_connection(
        self, **kwargs: Unpack[CreateVpcConnectionRequestRequestTypeDef]
    ) -> CreateVpcConnectionResponseTypeDef:
        """
        Creates a new MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_vpc_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_vpc_connection)
        """

    def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterRequestRequestTypeDef]
    ) -> DeleteClusterResponseTypeDef:
        """
        Deletes the MSK cluster specified by the Amazon Resource Name (ARN) in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_cluster)
        """

    def delete_cluster_policy(
        self, **kwargs: Unpack[DeleteClusterPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the MSK cluster policy specified by the Amazon Resource Name (ARN) in
        the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_cluster_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_cluster_policy)
        """

    def delete_configuration(
        self, **kwargs: Unpack[DeleteConfigurationRequestRequestTypeDef]
    ) -> DeleteConfigurationResponseTypeDef:
        """
        Deletes an MSK Configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_configuration)
        """

    def delete_replicator(
        self, **kwargs: Unpack[DeleteReplicatorRequestRequestTypeDef]
    ) -> DeleteReplicatorResponseTypeDef:
        """
        Deletes a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_replicator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_replicator)
        """

    def delete_vpc_connection(
        self, **kwargs: Unpack[DeleteVpcConnectionRequestRequestTypeDef]
    ) -> DeleteVpcConnectionResponseTypeDef:
        """
        Deletes a MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_vpc_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_vpc_connection)
        """

    def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterRequestRequestTypeDef]
    ) -> DescribeClusterResponseTypeDef:
        """
        Returns a description of the MSK cluster whose Amazon Resource Name (ARN) is
        specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_cluster)
        """

    def describe_cluster_operation(
        self, **kwargs: Unpack[DescribeClusterOperationRequestRequestTypeDef]
    ) -> DescribeClusterOperationResponseTypeDef:
        """
        Returns a description of the cluster operation specified by the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_cluster_operation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_cluster_operation)
        """

    def describe_cluster_operation_v2(
        self, **kwargs: Unpack[DescribeClusterOperationV2RequestRequestTypeDef]
    ) -> DescribeClusterOperationV2ResponseTypeDef:
        """
        Returns a description of the cluster operation specified by the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_cluster_operation_v2.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_cluster_operation_v2)
        """

    def describe_cluster_v2(
        self, **kwargs: Unpack[DescribeClusterV2RequestRequestTypeDef]
    ) -> DescribeClusterV2ResponseTypeDef:
        """
        Returns a description of the MSK cluster whose Amazon Resource Name (ARN) is
        specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_cluster_v2.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_cluster_v2)
        """

    def describe_configuration(
        self, **kwargs: Unpack[DescribeConfigurationRequestRequestTypeDef]
    ) -> DescribeConfigurationResponseTypeDef:
        """
        Returns a description of this MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_configuration)
        """

    def describe_configuration_revision(
        self, **kwargs: Unpack[DescribeConfigurationRevisionRequestRequestTypeDef]
    ) -> DescribeConfigurationRevisionResponseTypeDef:
        """
        Returns a description of this revision of the configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_configuration_revision.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_configuration_revision)
        """

    def describe_replicator(
        self, **kwargs: Unpack[DescribeReplicatorRequestRequestTypeDef]
    ) -> DescribeReplicatorResponseTypeDef:
        """
        Describes a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_replicator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_replicator)
        """

    def describe_vpc_connection(
        self, **kwargs: Unpack[DescribeVpcConnectionRequestRequestTypeDef]
    ) -> DescribeVpcConnectionResponseTypeDef:
        """
        Returns a description of this MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_vpc_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_vpc_connection)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#generate_presigned_url)
        """

    def get_bootstrap_brokers(
        self, **kwargs: Unpack[GetBootstrapBrokersRequestRequestTypeDef]
    ) -> GetBootstrapBrokersResponseTypeDef:
        """
        A list of brokers that a client application can use to bootstrap.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_bootstrap_brokers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_bootstrap_brokers)
        """

    def get_cluster_policy(
        self, **kwargs: Unpack[GetClusterPolicyRequestRequestTypeDef]
    ) -> GetClusterPolicyResponseTypeDef:
        """
        Get the MSK cluster policy specified by the Amazon Resource Name (ARN) in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_cluster_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_cluster_policy)
        """

    def get_compatible_kafka_versions(
        self, **kwargs: Unpack[GetCompatibleKafkaVersionsRequestRequestTypeDef]
    ) -> GetCompatibleKafkaVersionsResponseTypeDef:
        """
        Gets the Apache Kafka versions to which you can update the MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_compatible_kafka_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_compatible_kafka_versions)
        """

    def list_client_vpc_connections(
        self, **kwargs: Unpack[ListClientVpcConnectionsRequestRequestTypeDef]
    ) -> ListClientVpcConnectionsResponseTypeDef:
        """
        Returns a list of all the VPC connections in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_client_vpc_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_client_vpc_connections)
        """

    def list_cluster_operations(
        self, **kwargs: Unpack[ListClusterOperationsRequestRequestTypeDef]
    ) -> ListClusterOperationsResponseTypeDef:
        """
        Returns a list of all the operations that have been performed on the specified
        MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_cluster_operations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_cluster_operations)
        """

    def list_cluster_operations_v2(
        self, **kwargs: Unpack[ListClusterOperationsV2RequestRequestTypeDef]
    ) -> ListClusterOperationsV2ResponseTypeDef:
        """
        Returns a list of all the operations that have been performed on the specified
        MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_cluster_operations_v2.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_cluster_operations_v2)
        """

    def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of all the MSK clusters in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_clusters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_clusters)
        """

    def list_clusters_v2(
        self, **kwargs: Unpack[ListClustersV2RequestRequestTypeDef]
    ) -> ListClustersV2ResponseTypeDef:
        """
        Returns a list of all the MSK clusters in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_clusters_v2.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_clusters_v2)
        """

    def list_configuration_revisions(
        self, **kwargs: Unpack[ListConfigurationRevisionsRequestRequestTypeDef]
    ) -> ListConfigurationRevisionsResponseTypeDef:
        """
        Returns a list of all the MSK configurations in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_configuration_revisions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_configuration_revisions)
        """

    def list_configurations(
        self, **kwargs: Unpack[ListConfigurationsRequestRequestTypeDef]
    ) -> ListConfigurationsResponseTypeDef:
        """
        Returns a list of all the MSK configurations in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_configurations)
        """

    def list_kafka_versions(
        self, **kwargs: Unpack[ListKafkaVersionsRequestRequestTypeDef]
    ) -> ListKafkaVersionsResponseTypeDef:
        """
        Returns a list of Apache Kafka versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_kafka_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_kafka_versions)
        """

    def list_nodes(
        self, **kwargs: Unpack[ListNodesRequestRequestTypeDef]
    ) -> ListNodesResponseTypeDef:
        """
        Returns a list of the broker nodes in the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_nodes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_nodes)
        """

    def list_replicators(
        self, **kwargs: Unpack[ListReplicatorsRequestRequestTypeDef]
    ) -> ListReplicatorsResponseTypeDef:
        """
        Lists the replicators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_replicators.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_replicators)
        """

    def list_scram_secrets(
        self, **kwargs: Unpack[ListScramSecretsRequestRequestTypeDef]
    ) -> ListScramSecretsResponseTypeDef:
        """
        Returns a list of the Scram Secrets associated with an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_scram_secrets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_scram_secrets)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_tags_for_resource)
        """

    def list_vpc_connections(
        self, **kwargs: Unpack[ListVpcConnectionsRequestRequestTypeDef]
    ) -> ListVpcConnectionsResponseTypeDef:
        """
        Returns a list of all the VPC connections in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_vpc_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_vpc_connections)
        """

    def put_cluster_policy(
        self, **kwargs: Unpack[PutClusterPolicyRequestRequestTypeDef]
    ) -> PutClusterPolicyResponseTypeDef:
        """
        Creates or updates the MSK cluster policy specified by the cluster Amazon
        Resource Name (ARN) in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/put_cluster_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#put_cluster_policy)
        """

    def reboot_broker(
        self, **kwargs: Unpack[RebootBrokerRequestRequestTypeDef]
    ) -> RebootBrokerResponseTypeDef:
        """
        Reboots brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/reboot_broker.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#reboot_broker)
        """

    def reject_client_vpc_connection(
        self, **kwargs: Unpack[RejectClientVpcConnectionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Returns empty response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/reject_client_vpc_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#reject_client_vpc_connection)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to the specified MSK resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the tags associated with the keys that are provided in the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#untag_resource)
        """

    def update_broker_count(
        self, **kwargs: Unpack[UpdateBrokerCountRequestRequestTypeDef]
    ) -> UpdateBrokerCountResponseTypeDef:
        """
        Updates the number of broker nodes in the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_broker_count.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_broker_count)
        """

    def update_broker_storage(
        self, **kwargs: Unpack[UpdateBrokerStorageRequestRequestTypeDef]
    ) -> UpdateBrokerStorageResponseTypeDef:
        """
        Updates the EBS storage associated with MSK brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_broker_storage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_broker_storage)
        """

    def update_broker_type(
        self, **kwargs: Unpack[UpdateBrokerTypeRequestRequestTypeDef]
    ) -> UpdateBrokerTypeResponseTypeDef:
        """
        Updates EC2 instance type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_broker_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_broker_type)
        """

    def update_cluster_configuration(
        self, **kwargs: Unpack[UpdateClusterConfigurationRequestRequestTypeDef]
    ) -> UpdateClusterConfigurationResponseTypeDef:
        """
        Updates the cluster with the configuration that is specified in the request
        body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_cluster_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_cluster_configuration)
        """

    def update_cluster_kafka_version(
        self, **kwargs: Unpack[UpdateClusterKafkaVersionRequestRequestTypeDef]
    ) -> UpdateClusterKafkaVersionResponseTypeDef:
        """
        Updates the Apache Kafka version for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_cluster_kafka_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_cluster_kafka_version)
        """

    def update_configuration(
        self, **kwargs: Unpack[UpdateConfigurationRequestRequestTypeDef]
    ) -> UpdateConfigurationResponseTypeDef:
        """
        Updates an MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_configuration)
        """

    def update_connectivity(
        self, **kwargs: Unpack[UpdateConnectivityRequestRequestTypeDef]
    ) -> UpdateConnectivityResponseTypeDef:
        """
        Updates the cluster's connectivity configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_connectivity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_connectivity)
        """

    def update_monitoring(
        self, **kwargs: Unpack[UpdateMonitoringRequestRequestTypeDef]
    ) -> UpdateMonitoringResponseTypeDef:
        """
        Updates the monitoring settings for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_monitoring.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_monitoring)
        """

    def update_replication_info(
        self, **kwargs: Unpack[UpdateReplicationInfoRequestRequestTypeDef]
    ) -> UpdateReplicationInfoResponseTypeDef:
        """
        Updates replication info of a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_replication_info.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_replication_info)
        """

    def update_security(
        self, **kwargs: Unpack[UpdateSecurityRequestRequestTypeDef]
    ) -> UpdateSecurityResponseTypeDef:
        """
        Updates the security settings for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_security.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_security)
        """

    def update_storage(
        self, **kwargs: Unpack[UpdateStorageRequestRequestTypeDef]
    ) -> UpdateStorageResponseTypeDef:
        """
        Updates cluster broker volume size (or) sets cluster storage mode to TIERED.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_storage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_storage)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_client_vpc_connections"]
    ) -> ListClientVpcConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cluster_operations"]
    ) -> ListClusterOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cluster_operations_v2"]
    ) -> ListClusterOperationsV2Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters_v2"]) -> ListClustersV2Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configuration_revisions"]
    ) -> ListConfigurationRevisionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configurations"]
    ) -> ListConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_kafka_versions"]
    ) -> ListKafkaVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_nodes"]) -> ListNodesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_replicators"]
    ) -> ListReplicatorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_scram_secrets"]
    ) -> ListScramSecretsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_vpc_connections"]
    ) -> ListVpcConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """
