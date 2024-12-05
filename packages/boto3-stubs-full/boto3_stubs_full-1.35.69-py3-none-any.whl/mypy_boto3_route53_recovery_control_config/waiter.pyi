"""
Type annotations for route53-recovery-control-config service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53_recovery_control_config.client import Route53RecoveryControlConfigClient
    from mypy_boto3_route53_recovery_control_config.waiter import (
        ClusterCreatedWaiter,
        ClusterDeletedWaiter,
        ControlPanelCreatedWaiter,
        ControlPanelDeletedWaiter,
        RoutingControlCreatedWaiter,
        RoutingControlDeletedWaiter,
    )

    session = Session()
    client: Route53RecoveryControlConfigClient = session.client("route53-recovery-control-config")

    cluster_created_waiter: ClusterCreatedWaiter = client.get_waiter("cluster_created")
    cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
    control_panel_created_waiter: ControlPanelCreatedWaiter = client.get_waiter("control_panel_created")
    control_panel_deleted_waiter: ControlPanelDeletedWaiter = client.get_waiter("control_panel_deleted")
    routing_control_created_waiter: RoutingControlCreatedWaiter = client.get_waiter("routing_control_created")
    routing_control_deleted_waiter: RoutingControlDeletedWaiter = client.get_waiter("routing_control_deleted")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeClusterRequestClusterCreatedWaitTypeDef,
    DescribeClusterRequestClusterDeletedWaitTypeDef,
    DescribeControlPanelRequestControlPanelCreatedWaitTypeDef,
    DescribeControlPanelRequestControlPanelDeletedWaitTypeDef,
    DescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef,
    DescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ClusterCreatedWaiter",
    "ClusterDeletedWaiter",
    "ControlPanelCreatedWaiter",
    "ControlPanelDeletedWaiter",
    "RoutingControlCreatedWaiter",
    "RoutingControlDeletedWaiter",
)

class ClusterCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ClusterCreated.html#Route53RecoveryControlConfig.Waiter.ClusterCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#clustercreatedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeClusterRequestClusterCreatedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ClusterCreated.html#Route53RecoveryControlConfig.Waiter.ClusterCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#clustercreatedwaiter)
        """

class ClusterDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ClusterDeleted.html#Route53RecoveryControlConfig.Waiter.ClusterDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#clusterdeletedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeClusterRequestClusterDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ClusterDeleted.html#Route53RecoveryControlConfig.Waiter.ClusterDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#clusterdeletedwaiter)
        """

class ControlPanelCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ControlPanelCreated.html#Route53RecoveryControlConfig.Waiter.ControlPanelCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#controlpanelcreatedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeControlPanelRequestControlPanelCreatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ControlPanelCreated.html#Route53RecoveryControlConfig.Waiter.ControlPanelCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#controlpanelcreatedwaiter)
        """

class ControlPanelDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ControlPanelDeleted.html#Route53RecoveryControlConfig.Waiter.ControlPanelDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#controlpaneldeletedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeControlPanelRequestControlPanelDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ControlPanelDeleted.html#Route53RecoveryControlConfig.Waiter.ControlPanelDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#controlpaneldeletedwaiter)
        """

class RoutingControlCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/RoutingControlCreated.html#Route53RecoveryControlConfig.Waiter.RoutingControlCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#routingcontrolcreatedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/RoutingControlCreated.html#Route53RecoveryControlConfig.Waiter.RoutingControlCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#routingcontrolcreatedwaiter)
        """

class RoutingControlDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/RoutingControlDeleted.html#Route53RecoveryControlConfig.Waiter.RoutingControlDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#routingcontroldeletedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/RoutingControlDeleted.html#Route53RecoveryControlConfig.Waiter.RoutingControlDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/waiters/#routingcontroldeletedwaiter)
        """
