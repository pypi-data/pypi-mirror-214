'''
# Endpoints for AWS Global Accelerator

This library contains integration classes to reference endpoints in AWS
Global Accelerator. Instances of these classes should be passed to the
`endpointGroup.addEndpoint()` method.

See the README of the `@aws-cdk/aws-globalaccelerator` library for more information on
AWS Global Accelerator, and examples of all the integration classes available in
this module.
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

from ..aws_ec2 import CfnEIP as _CfnEIP_41f4ee0e, IInstance as _IInstance_3a12995c
from ..aws_elasticloadbalancingv2 import (
    IApplicationLoadBalancer as _IApplicationLoadBalancer_2b335873,
    INetworkLoadBalancer as _INetworkLoadBalancer_ead0b7fa,
)
from ..aws_globalaccelerator import IEndpoint as _IEndpoint_9178919e


@jsii.implements(_IEndpoint_9178919e)
class ApplicationLoadBalancerEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_globalaccelerator_endpoints.ApplicationLoadBalancerEndpoint",
):
    '''(experimental) Use an Application Load Balancer as a Global Accelerator Endpoint.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # alb: elbv2.ApplicationLoadBalancer
        # listener: globalaccelerator.Listener
        
        
        listener.add_endpoint_group("Group",
            endpoints=[
                ga_endpoints.ApplicationLoadBalancerEndpoint(alb,
                    weight=128,
                    preserve_client_ip=True
                )
            ]
        )
    '''

    def __init__(
        self,
        load_balancer: _IApplicationLoadBalancer_2b335873,
        *,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param load_balancer: -
        :param preserve_client_ip: (experimental) Forward the client IP address in an ``X-Forwarded-For`` header. GlobalAccelerator will create Network Interfaces in your VPC in order to preserve the client IP address. Client IP address preservation is supported only in specific AWS Regions. See the GlobalAccelerator Developer Guide for a list. Default: true if available
        :param weight: (experimental) Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3f7d093600ca4fd23f2285950af5aa39080f5bbcfbf0a64c561f0ed3d76d0c)
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
        options = ApplicationLoadBalancerEndpointOptions(
            preserve_client_ip=preserve_client_ip, weight=weight
        )

        jsii.create(self.__class__, self, [load_balancer, options])

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(self) -> typing.Any:
        '''(experimental) Render the endpoint to an endpoint configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderEndpointConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the endpoint is located.

        If the region cannot be determined, ``undefined`` is returned

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="monocdk.aws_globalaccelerator_endpoints.ApplicationLoadBalancerEndpointOptions",
    jsii_struct_bases=[],
    name_mapping={"preserve_client_ip": "preserveClientIp", "weight": "weight"},
)
class ApplicationLoadBalancerEndpointOptions:
    def __init__(
        self,
        *,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for a ApplicationLoadBalancerEndpoint.

        :param preserve_client_ip: (experimental) Forward the client IP address in an ``X-Forwarded-For`` header. GlobalAccelerator will create Network Interfaces in your VPC in order to preserve the client IP address. Client IP address preservation is supported only in specific AWS Regions. See the GlobalAccelerator Developer Guide for a list. Default: true if available
        :param weight: (experimental) Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # alb: elbv2.ApplicationLoadBalancer
            # listener: globalaccelerator.Listener
            
            
            listener.add_endpoint_group("Group",
                endpoints=[
                    ga_endpoints.ApplicationLoadBalancerEndpoint(alb,
                        weight=128,
                        preserve_client_ip=True
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f292d7ab187661a5dfe138f7ffd3a73fb1a00de2bc15b060b92d28ff71b58d)
            check_type(argname="argument preserve_client_ip", value=preserve_client_ip, expected_type=type_hints["preserve_client_ip"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if preserve_client_ip is not None:
            self._values["preserve_client_ip"] = preserve_client_ip
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def preserve_client_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Forward the client IP address in an ``X-Forwarded-For`` header.

        GlobalAccelerator will create Network Interfaces in your VPC in order
        to preserve the client IP address.

        Client IP address preservation is supported only in specific AWS Regions.
        See the GlobalAccelerator Developer Guide for a list.

        :default: true if available

        :stability: experimental
        '''
        result = self._values.get("preserve_client_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Endpoint weight across all endpoints in the group.

        Must be a value between 0 and 255.

        :default: 128

        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerEndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEndpoint_9178919e)
class CfnEipEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_globalaccelerator_endpoints.CfnEipEndpoint",
):
    '''(experimental) Use an EC2 Instance as a Global Accelerator Endpoint.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # listener: globalaccelerator.Listener
        # eip: ec2.CfnEIP
        
        
        listener.add_endpoint_group("Group",
            endpoints=[
                ga_endpoints.CfnEipEndpoint(eip,
                    weight=128
                )
            ]
        )
    '''

    def __init__(
        self,
        eip: _CfnEIP_41f4ee0e,
        *,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param eip: -
        :param weight: (experimental) Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604a96cce9921c161560d15ee20f201d30c3cb6e99c9f3e76daa280f036f450f)
            check_type(argname="argument eip", value=eip, expected_type=type_hints["eip"])
        options = CfnEipEndpointProps(weight=weight)

        jsii.create(self.__class__, self, [eip, options])

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(self) -> typing.Any:
        '''(experimental) Render the endpoint to an endpoint configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderEndpointConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the endpoint is located.

        If the region cannot be determined, ``undefined`` is returned

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="monocdk.aws_globalaccelerator_endpoints.CfnEipEndpointProps",
    jsii_struct_bases=[],
    name_mapping={"weight": "weight"},
)
class CfnEipEndpointProps:
    def __init__(self, *, weight: typing.Optional[jsii.Number] = None) -> None:
        '''(experimental) Properties for a NetworkLoadBalancerEndpoint.

        :param weight: (experimental) Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # listener: globalaccelerator.Listener
            # eip: ec2.CfnEIP
            
            
            listener.add_endpoint_group("Group",
                endpoints=[
                    ga_endpoints.CfnEipEndpoint(eip,
                        weight=128
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5585c9c68707cae9ad439e4e75cc3fa118e920412158a1495a7e47edd5779174)
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Endpoint weight across all endpoints in the group.

        Must be a value between 0 and 255.

        :default: 128

        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEipEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEndpoint_9178919e)
class InstanceEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_globalaccelerator_endpoints.InstanceEndpoint",
):
    '''(experimental) Use an EC2 Instance as a Global Accelerator Endpoint.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # listener: globalaccelerator.Listener
        # instance: ec2.Instance
        
        
        listener.add_endpoint_group("Group",
            endpoints=[
                ga_endpoints.InstanceEndpoint(instance,
                    weight=128,
                    preserve_client_ip=True
                )
            ]
        )
    '''

    def __init__(
        self,
        instance: _IInstance_3a12995c,
        *,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance: -
        :param preserve_client_ip: (experimental) Forward the client IP address. GlobalAccelerator will create Network Interfaces in your VPC in order to preserve the client IP address. Client IP address preservation is supported only in specific AWS Regions. See the GlobalAccelerator Developer Guide for a list. Default: true if available
        :param weight: (experimental) Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bb642cebfe86bb15b6f4d6e560306a4228222ae2cd1e66c563c83fa6128263)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
        options = InstanceEndpointProps(
            preserve_client_ip=preserve_client_ip, weight=weight
        )

        jsii.create(self.__class__, self, [instance, options])

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(self) -> typing.Any:
        '''(experimental) Render the endpoint to an endpoint configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderEndpointConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the endpoint is located.

        If the region cannot be determined, ``undefined`` is returned

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="monocdk.aws_globalaccelerator_endpoints.InstanceEndpointProps",
    jsii_struct_bases=[],
    name_mapping={"preserve_client_ip": "preserveClientIp", "weight": "weight"},
)
class InstanceEndpointProps:
    def __init__(
        self,
        *,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for a NetworkLoadBalancerEndpoint.

        :param preserve_client_ip: (experimental) Forward the client IP address. GlobalAccelerator will create Network Interfaces in your VPC in order to preserve the client IP address. Client IP address preservation is supported only in specific AWS Regions. See the GlobalAccelerator Developer Guide for a list. Default: true if available
        :param weight: (experimental) Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # listener: globalaccelerator.Listener
            # instance: ec2.Instance
            
            
            listener.add_endpoint_group("Group",
                endpoints=[
                    ga_endpoints.InstanceEndpoint(instance,
                        weight=128,
                        preserve_client_ip=True
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff2962cecf205350e22bd16219d2ac621e747cbd4bc51b59187b23ea457091e)
            check_type(argname="argument preserve_client_ip", value=preserve_client_ip, expected_type=type_hints["preserve_client_ip"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if preserve_client_ip is not None:
            self._values["preserve_client_ip"] = preserve_client_ip
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def preserve_client_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Forward the client IP address.

        GlobalAccelerator will create Network Interfaces in your VPC in order
        to preserve the client IP address.

        Client IP address preservation is supported only in specific AWS Regions.
        See the GlobalAccelerator Developer Guide for a list.

        :default: true if available

        :stability: experimental
        '''
        result = self._values.get("preserve_client_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Endpoint weight across all endpoints in the group.

        Must be a value between 0 and 255.

        :default: 128

        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEndpoint_9178919e)
class NetworkLoadBalancerEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_globalaccelerator_endpoints.NetworkLoadBalancerEndpoint",
):
    '''(experimental) Use a Network Load Balancer as a Global Accelerator Endpoint.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Create an Accelerator
        accelerator = globalaccelerator.Accelerator(self, "Accelerator")
        
        # Create a Listener
        listener = accelerator.add_listener("Listener",
            port_ranges=[globalaccelerator.aws_globalaccelerator.PortRange(from_port=80), globalaccelerator.aws_globalaccelerator.PortRange(from_port=443)
            ]
        )
        
        # Import the Load Balancers
        nlb1 = elbv2.NetworkLoadBalancer.from_network_load_balancer_attributes(self, "NLB1",
            load_balancer_arn="arn:aws:elasticloadbalancing:us-west-2:111111111111:loadbalancer/app/my-load-balancer1/e16bef66805b"
        )
        nlb2 = elbv2.NetworkLoadBalancer.from_network_load_balancer_attributes(self, "NLB2",
            load_balancer_arn="arn:aws:elasticloadbalancing:ap-south-1:111111111111:loadbalancer/app/my-load-balancer2/5513dc2ea8a1"
        )
        
        # Add one EndpointGroup for each Region we are targeting
        listener.add_endpoint_group("Group1",
            endpoints=[ga_endpoints.NetworkLoadBalancerEndpoint(nlb1)]
        )
        listener.add_endpoint_group("Group2",
            # Imported load balancers automatically calculate their Region from the ARN.
            # If you are load balancing to other resources, you must also pass a `region`
            # parameter here.
            endpoints=[ga_endpoints.NetworkLoadBalancerEndpoint(nlb2)]
        )
    '''

    def __init__(
        self,
        load_balancer: _INetworkLoadBalancer_ead0b7fa,
        *,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param load_balancer: -
        :param weight: (experimental) Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ec907dbd5e766c904b274cc64ee22a9c3a8e2f1ea2a162970f67b02b8a227b)
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
        options = NetworkLoadBalancerEndpointProps(weight=weight)

        jsii.create(self.__class__, self, [load_balancer, options])

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(self) -> typing.Any:
        '''(experimental) Render the endpoint to an endpoint configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderEndpointConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the endpoint is located.

        If the region cannot be determined, ``undefined`` is returned

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="monocdk.aws_globalaccelerator_endpoints.NetworkLoadBalancerEndpointProps",
    jsii_struct_bases=[],
    name_mapping={"weight": "weight"},
)
class NetworkLoadBalancerEndpointProps:
    def __init__(self, *, weight: typing.Optional[jsii.Number] = None) -> None:
        '''(experimental) Properties for a NetworkLoadBalancerEndpoint.

        :param weight: (experimental) Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # nlb: elbv2.NetworkLoadBalancer
            # listener: globalaccelerator.Listener
            
            
            listener.add_endpoint_group("Group",
                endpoints=[
                    ga_endpoints.NetworkLoadBalancerEndpoint(nlb,
                        weight=128
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4fa949092cce6f26911ddede604bd970d5a4d9f3068bfb3f9d04968dd10d3d1)
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Endpoint weight across all endpoints in the group.

        Must be a value between 0 and 255.

        :default: 128

        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApplicationLoadBalancerEndpoint",
    "ApplicationLoadBalancerEndpointOptions",
    "CfnEipEndpoint",
    "CfnEipEndpointProps",
    "InstanceEndpoint",
    "InstanceEndpointProps",
    "NetworkLoadBalancerEndpoint",
    "NetworkLoadBalancerEndpointProps",
]

publication.publish()

def _typecheckingstub__7e3f7d093600ca4fd23f2285950af5aa39080f5bbcfbf0a64c561f0ed3d76d0c(
    load_balancer: _IApplicationLoadBalancer_2b335873,
    *,
    preserve_client_ip: typing.Optional[builtins.bool] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f292d7ab187661a5dfe138f7ffd3a73fb1a00de2bc15b060b92d28ff71b58d(
    *,
    preserve_client_ip: typing.Optional[builtins.bool] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604a96cce9921c161560d15ee20f201d30c3cb6e99c9f3e76daa280f036f450f(
    eip: _CfnEIP_41f4ee0e,
    *,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5585c9c68707cae9ad439e4e75cc3fa118e920412158a1495a7e47edd5779174(
    *,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bb642cebfe86bb15b6f4d6e560306a4228222ae2cd1e66c563c83fa6128263(
    instance: _IInstance_3a12995c,
    *,
    preserve_client_ip: typing.Optional[builtins.bool] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff2962cecf205350e22bd16219d2ac621e747cbd4bc51b59187b23ea457091e(
    *,
    preserve_client_ip: typing.Optional[builtins.bool] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ec907dbd5e766c904b274cc64ee22a9c3a8e2f1ea2a162970f67b02b8a227b(
    load_balancer: _INetworkLoadBalancer_ead0b7fa,
    *,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fa949092cce6f26911ddede604bd970d5a4d9f3068bfb3f9d04968dd10d3d1(
    *,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
