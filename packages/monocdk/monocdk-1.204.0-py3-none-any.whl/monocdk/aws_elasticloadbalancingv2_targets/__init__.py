'''
# Targets for AWS Elastic Load Balancing V2

This package contains targets for ELBv2. See the README of the `@aws-cdk/aws-elasticloadbalancingv2` library.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

from ..aws_ec2 import Instance as _Instance_d6f39d19
from ..aws_elasticloadbalancingv2 import (
    ApplicationLoadBalancer as _ApplicationLoadBalancer_16524503,
    IApplicationLoadBalancerTarget as _IApplicationLoadBalancerTarget_db0fdc70,
    IApplicationTargetGroup as _IApplicationTargetGroup_5a474b2b,
    INetworkLoadBalancerTarget as _INetworkLoadBalancerTarget_6691f661,
    INetworkTargetGroup as _INetworkTargetGroup_6938b578,
    LoadBalancerTargetProps as _LoadBalancerTargetProps_8b99f223,
)
from ..aws_lambda import IFunction as _IFunction_6e14f09e


@jsii.implements(_INetworkLoadBalancerTarget_6691f661)
class AlbArnTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancingv2_targets.AlbArnTarget",
):
    '''(experimental) A single Application Load Balancer as the target for load balancing.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets
        
        alb_arn_target = elasticloadbalancingv2_targets.AlbArnTarget("albArn", 123)
    '''

    def __init__(self, alb_arn: builtins.str, port: jsii.Number) -> None:
        '''(experimental) Create a new alb target.

        :param alb_arn: The ARN of the application load balancer to load balance to.
        :param port: The port on which the target is listening.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236dca1181461675b3ebae78bfe346c92a6183783edbff49b9ba84b0669675af)
            check_type(argname="argument alb_arn", value=alb_arn, expected_type=type_hints["alb_arn"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [alb_arn, port])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: _INetworkTargetGroup_6938b578,
    ) -> _LoadBalancerTargetProps_8b99f223:
        '''(experimental) Register this alb target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89241be9a0d350fa36fceac9a66ec3d015a681f37e1ef9e3888f9fc096bddd5a)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_LoadBalancerTargetProps_8b99f223, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


class AlbTarget(
    AlbArnTarget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancingv2_targets.AlbTarget",
):
    '''(experimental) A single Application Load Balancer as the target for load balancing.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as targets
        import monocdk as ecs
        import monocdk as patterns
        
        # vpc: ec2.Vpc
        
        
        task = ecs.FargateTaskDefinition(self, "Task", cpu=256, memory_limit_mi_b=512)
        task.add_container("nginx",
            image=ecs.ContainerImage.from_registry("public.ecr.aws/nginx/nginx:latest"),
            port_mappings=[targets.aws_ecs.PortMapping(container_port=80)]
        )
        
        svc = patterns.ApplicationLoadBalancedFargateService(self, "Service",
            vpc=vpc,
            task_definition=task,
            public_load_balancer=False
        )
        
        nlb = elbv2.NetworkLoadBalancer(self, "Nlb",
            vpc=vpc,
            cross_zone_enabled=True,
            internet_facing=True
        )
        
        listener = nlb.add_listener("listener", port=80)
        
        listener.add_targets("Targets",
            targets=[targets.AlbTarget(svc.load_balancer, 80)],
            port=80
        )
        
        CfnOutput(self, "NlbEndpoint", value=f"http://{nlb.loadBalancerDnsName}")
    '''

    def __init__(
        self,
        alb: _ApplicationLoadBalancer_16524503,
        port: jsii.Number,
    ) -> None:
        '''
        :param alb: The application load balancer to load balance to.
        :param port: The port on which the target is listening.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e609fd8724782a74da9316d87f9e7046243a8c07c3eb2e376101e4d1fa321a55)
            check_type(argname="argument alb", value=alb, expected_type=type_hints["alb"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [alb, port])


@jsii.implements(_IApplicationLoadBalancerTarget_db0fdc70, _INetworkLoadBalancerTarget_6691f661)
class InstanceIdTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancingv2_targets.InstanceIdTarget",
):
    '''(experimental) An EC2 instance that is the target for load balancing.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can connect to the instance.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets
        
        instance_id_target = elasticloadbalancingv2_targets.InstanceIdTarget("instanceId", 123)
    '''

    def __init__(
        self,
        instance_id: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Create a new Instance target.

        :param instance_id: Instance ID of the instance to register to.
        :param port: Override the default port for the target group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328bdea46d0052c84fe931c577835c6d7ae42c8284cdaa130320c20aff3ffff3)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: _IApplicationTargetGroup_5a474b2b,
    ) -> _LoadBalancerTargetProps_8b99f223:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__410ebd5cb281379994e46fffbac14b622a74648f7ba44accfd95cdc8ee9666c8)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_LoadBalancerTargetProps_8b99f223, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: _INetworkTargetGroup_6938b578,
    ) -> _LoadBalancerTargetProps_8b99f223:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e45cd5772cdc5d00b0221cf55c3f0288f646ce058bc8ea0ad1ef3c052b0b0bf7)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_LoadBalancerTargetProps_8b99f223, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


class InstanceTarget(
    InstanceIdTarget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancingv2_targets.InstanceTarget",
):
    '''
    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_ec2 as ec2
        from monocdk import aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets
        
        # instance: ec2.Instance
        
        instance_target = elasticloadbalancingv2_targets.InstanceTarget(instance, 123)
    '''

    def __init__(
        self,
        instance: _Instance_d6f39d19,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Create a new Instance target.

        :param instance: Instance to register to.
        :param port: Override the default port for the target group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c94c1c734c10708f155a7814b2ebdbbf2a57251e26c08021a33617039f64bab9)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [instance, port])


@jsii.implements(_IApplicationLoadBalancerTarget_db0fdc70, _INetworkLoadBalancerTarget_6691f661)
class IpTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancingv2_targets.IpTarget",
):
    '''(experimental) An IP address that is a target for load balancing.

    Specify IP addresses from the subnets of the virtual private cloud (VPC) for
    the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and
    192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify
    publicly routable IP addresses.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can send packets to the IP address.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets
        
        ip_target = elasticloadbalancingv2_targets.IpTarget("ipAddress", 123, "availabilityZone")
    '''

    def __init__(
        self,
        ip_address: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Create a new IPAddress target.

        The availabilityZone parameter determines whether the target receives
        traffic from the load balancer nodes in the specified Availability Zone
        or from all enabled Availability Zones for the load balancer.

        This parameter is not supported if the target type of the target group
        is instance. If the IP address is in a subnet of the VPC for the target
        group, the Availability Zone is automatically detected and this
        parameter is optional. If the IP address is outside the VPC, this
        parameter is required.

        With an Application Load Balancer, if the IP address is outside the VPC
        for the target group, the only supported value is all.

        Default is automatic.

        :param ip_address: The IP Address to load balance to.
        :param port: Override the group's default port.
        :param availability_zone: Availability zone to send traffic from.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1736664149ee1323d3de56a0193e0194dc79460c70ab26d217d1fb37bbc7aaa0)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
        jsii.create(self.__class__, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: _IApplicationTargetGroup_5a474b2b,
    ) -> _LoadBalancerTargetProps_8b99f223:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83dd31abaefc33118254a08656dce005a86aee3dd1144b28178deef813f915f6)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_LoadBalancerTargetProps_8b99f223, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: _INetworkTargetGroup_6938b578,
    ) -> _LoadBalancerTargetProps_8b99f223:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed942d833e0b3b0d4a19d6f49f89c7fe18cd9a5bab538108e9358ccc0a23134)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_LoadBalancerTargetProps_8b99f223, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


@jsii.implements(_IApplicationLoadBalancerTarget_db0fdc70)
class LambdaTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancingv2_targets.LambdaTarget",
):
    '''
    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as lambda_
        import monocdk as targets
        
        # lambda_function: lambda.Function
        # lb: elbv2.ApplicationLoadBalancer
        
        
        listener = lb.add_listener("Listener", port=80)
        listener.add_targets("Targets",
            targets=[targets.LambdaTarget(lambda_function)],
        
            # For Lambda Targets, you need to explicitly enable health checks if you
            # want them.
            health_check=lambda.aws_elasticloadbalancingv2.HealthCheck(
                enabled=True
            )
        )
    '''

    def __init__(self, fn: _IFunction_6e14f09e) -> None:
        '''(experimental) Create a new Lambda target.

        :param fn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202a137514dd59fa3aa3716e333e03322f9fb6f08ed2001c1b8eea07b6eac7f0)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        jsii.create(self.__class__, self, [fn])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: _IApplicationTargetGroup_5a474b2b,
    ) -> _LoadBalancerTargetProps_8b99f223:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637aeca7ff7492e73cc86108d4baef92663a155c9ea77a93fa7048ddc6c4454d)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_LoadBalancerTargetProps_8b99f223, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: _INetworkTargetGroup_6938b578,
    ) -> _LoadBalancerTargetProps_8b99f223:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c588c2a2f7741c4fc61e8a899c34772cd2f36450be5c2a36fb1bfde79f8b6e)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_LoadBalancerTargetProps_8b99f223, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


__all__ = [
    "AlbArnTarget",
    "AlbTarget",
    "InstanceIdTarget",
    "InstanceTarget",
    "IpTarget",
    "LambdaTarget",
]

publication.publish()

def _typecheckingstub__236dca1181461675b3ebae78bfe346c92a6183783edbff49b9ba84b0669675af(
    alb_arn: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89241be9a0d350fa36fceac9a66ec3d015a681f37e1ef9e3888f9fc096bddd5a(
    target_group: _INetworkTargetGroup_6938b578,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e609fd8724782a74da9316d87f9e7046243a8c07c3eb2e376101e4d1fa321a55(
    alb: _ApplicationLoadBalancer_16524503,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328bdea46d0052c84fe931c577835c6d7ae42c8284cdaa130320c20aff3ffff3(
    instance_id: builtins.str,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410ebd5cb281379994e46fffbac14b622a74648f7ba44accfd95cdc8ee9666c8(
    target_group: _IApplicationTargetGroup_5a474b2b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45cd5772cdc5d00b0221cf55c3f0288f646ce058bc8ea0ad1ef3c052b0b0bf7(
    target_group: _INetworkTargetGroup_6938b578,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94c1c734c10708f155a7814b2ebdbbf2a57251e26c08021a33617039f64bab9(
    instance: _Instance_d6f39d19,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1736664149ee1323d3de56a0193e0194dc79460c70ab26d217d1fb37bbc7aaa0(
    ip_address: builtins.str,
    port: typing.Optional[jsii.Number] = None,
    availability_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dd31abaefc33118254a08656dce005a86aee3dd1144b28178deef813f915f6(
    target_group: _IApplicationTargetGroup_5a474b2b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed942d833e0b3b0d4a19d6f49f89c7fe18cd9a5bab538108e9358ccc0a23134(
    target_group: _INetworkTargetGroup_6938b578,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202a137514dd59fa3aa3716e333e03322f9fb6f08ed2001c1b8eea07b6eac7f0(
    fn: _IFunction_6e14f09e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637aeca7ff7492e73cc86108d4baef92663a155c9ea77a93fa7048ddc6c4454d(
    target_group: _IApplicationTargetGroup_5a474b2b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c588c2a2f7741c4fc61e8a899c34772cd2f36450be5c2a36fb1bfde79f8b6e(
    target_group: _INetworkTargetGroup_6938b578,
) -> None:
    """Type checking stubs"""
    pass
