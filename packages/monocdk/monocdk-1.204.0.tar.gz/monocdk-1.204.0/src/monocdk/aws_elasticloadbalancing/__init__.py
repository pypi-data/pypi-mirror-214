'''
# Amazon Elastic Load Balancing Construct Library

The `@aws-cdk/aws-elasticloadbalancing` package provides constructs for configuring
classic load balancers.

## Configuring a Load Balancer

Load balancers send traffic to one or more AutoScalingGroups. Create a load
balancer, set up listeners and a health check, and supply the fleet(s) you want
to load balance to in the `targets` property.

```python
# vpc: ec2.IVpc

# my_auto_scaling_group: autoscaling.AutoScalingGroup

lb = elb.LoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True,
    health_check=elb.aws_elasticloadbalancing.HealthCheck(
        port=80
    )
)
lb.add_target(my_auto_scaling_group)
lb.add_listener(
    external_port=80
)
```

The load balancer allows all connections by default. If you want to change that,
pass the `allowConnectionsFrom` property while setting up the listener:

```python
# my_security_group: ec2.SecurityGroup
# lb: elb.LoadBalancer

lb.add_listener(
    external_port=80,
    allow_connections_from=[my_security_group]
)
```
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

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_ec2 import (
    Connections as _Connections_57ccbda9,
    IConnectable as _IConnectable_c1c0e72c,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    Port as _Port_5f4cbf14,
    SubnetSelection as _SubnetSelection_1284e62c,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnLoadBalancer(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer",
):
    '''A CloudFormation ``AWS::ElasticLoadBalancing::LoadBalancer``.

    Specifies a Classic Load Balancer.

    You can specify the ``AvailabilityZones`` or ``Subnets`` property, but not both.

    If this resource has a public IP address and is also in a VPC that is defined in the same template, you must use the `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ to declare a dependency on the VPC-gateway attachment.

    :cloudformationResource: AWS::ElasticLoadBalancing::LoadBalancer
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticloadbalancing as elasticloadbalancing
        
        # attributes: Any
        
        cfn_load_balancer = elasticloadbalancing.CfnLoadBalancer(self, "MyCfnLoadBalancer",
            listeners=[elasticloadbalancing.CfnLoadBalancer.ListenersProperty(
                instance_port="instancePort",
                load_balancer_port="loadBalancerPort",
                protocol="protocol",
        
                # the properties below are optional
                instance_protocol="instanceProtocol",
                policy_names=["policyNames"],
                ssl_certificate_id="sslCertificateId"
            )],
        
            # the properties below are optional
            access_logging_policy=elasticloadbalancing.CfnLoadBalancer.AccessLoggingPolicyProperty(
                enabled=False,
                s3_bucket_name="s3BucketName",
        
                # the properties below are optional
                emit_interval=123,
                s3_bucket_prefix="s3BucketPrefix"
            ),
            app_cookie_stickiness_policy=[elasticloadbalancing.CfnLoadBalancer.AppCookieStickinessPolicyProperty(
                cookie_name="cookieName",
                policy_name="policyName"
            )],
            availability_zones=["availabilityZones"],
            connection_draining_policy=elasticloadbalancing.CfnLoadBalancer.ConnectionDrainingPolicyProperty(
                enabled=False,
        
                # the properties below are optional
                timeout=123
            ),
            connection_settings=elasticloadbalancing.CfnLoadBalancer.ConnectionSettingsProperty(
                idle_timeout=123
            ),
            cross_zone=False,
            health_check=elasticloadbalancing.CfnLoadBalancer.HealthCheckProperty(
                healthy_threshold="healthyThreshold",
                interval="interval",
                target="target",
                timeout="timeout",
                unhealthy_threshold="unhealthyThreshold"
            ),
            instances=["instances"],
            lb_cookie_stickiness_policy=[elasticloadbalancing.CfnLoadBalancer.LBCookieStickinessPolicyProperty(
                cookie_expiration_period="cookieExpirationPeriod",
                policy_name="policyName"
            )],
            load_balancer_name="loadBalancerName",
            policies=[elasticloadbalancing.CfnLoadBalancer.PoliciesProperty(
                attributes=[attributes],
                policy_name="policyName",
                policy_type="policyType",
        
                # the properties below are optional
                instance_ports=["instancePorts"],
                load_balancer_ports=["loadBalancerPorts"]
            )],
            scheme="scheme",
            security_groups=["securityGroups"],
            subnets=["subnets"],
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        listeners: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLoadBalancer.ListenersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        access_logging_policy: typing.Optional[typing.Union[typing.Union["CfnLoadBalancer.AccessLoggingPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        app_cookie_stickiness_policy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLoadBalancer.AppCookieStickinessPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_draining_policy: typing.Optional[typing.Union[typing.Union["CfnLoadBalancer.ConnectionDrainingPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        connection_settings: typing.Optional[typing.Union[typing.Union["CfnLoadBalancer.ConnectionSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cross_zone: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        health_check: typing.Optional[typing.Union[typing.Union["CfnLoadBalancer.HealthCheckProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        lb_cookie_stickiness_policy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLoadBalancer.LBCookieStickinessPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLoadBalancer.PoliciesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ElasticLoadBalancing::LoadBalancer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param listeners: The listeners for the load balancer. You can specify at most one listener per port. If you update the properties for a listener, AWS CloudFormation deletes the existing listener and creates a new one with the specified properties. While the new listener is being created, clients cannot connect to the load balancer.
        :param access_logging_policy: Information about where and how access logs are stored for the load balancer.
        :param app_cookie_stickiness_policy: Information about a policy for application-controlled session stickiness.
        :param availability_zones: The Availability Zones for the load balancer. For load balancers in a VPC, specify ``Subnets`` instead. Update requires replacement if you did not previously specify an Availability Zone or if you are removing all Availability Zones. Otherwise, update requires no interruption.
        :param connection_draining_policy: If enabled, the load balancer allows existing requests to complete before the load balancer shifts traffic away from a deregistered or unhealthy instance. For more information, see `Configure Connection Draining <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-conn-drain.html>`_ in the *Classic Load Balancers Guide* .
        :param connection_settings: If enabled, the load balancer allows the connections to remain idle (no data is sent over the connection) for the specified duration. By default, Elastic Load Balancing maintains a 60-second idle connection timeout for both front-end and back-end connections of your load balancer. For more information, see `Configure Idle Connection Timeout <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html>`_ in the *Classic Load Balancers Guide* .
        :param cross_zone: If enabled, the load balancer routes the request traffic evenly across all instances regardless of the Availability Zones. For more information, see `Configure Cross-Zone Load Balancing <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-disable-crosszone-lb.html>`_ in the *Classic Load Balancers Guide* .
        :param health_check: The health check settings to use when evaluating the health of your EC2 instances. Update requires replacement if you did not previously specify health check settings or if you are removing the health check settings. Otherwise, update requires no interruption.
        :param instances: The IDs of the instances for the load balancer.
        :param lb_cookie_stickiness_policy: Information about a policy for duration-based session stickiness.
        :param load_balancer_name: The name of the load balancer. This name must be unique within your set of load balancers for the region. If you don't specify a name, AWS CloudFormation generates a unique physical ID for the load balancer. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . If you specify a name, you cannot perform updates that require replacement of this resource, but you can perform other updates. To replace the resource, specify a new name.
        :param policies: The policies defined for your Classic Load Balancer. Specify only back-end server policies.
        :param scheme: The type of load balancer. Valid only for load balancers in a VPC. If ``Scheme`` is ``internet-facing`` , the load balancer has a public DNS name that resolves to a public IP address. If ``Scheme`` is ``internal`` , the load balancer has a public DNS name that resolves to a private IP address.
        :param security_groups: The security groups for the load balancer. Valid only for load balancers in a VPC.
        :param subnets: The IDs of the subnets for the load balancer. You can specify at most one subnet per Availability Zone. Update requires replacement if you did not previously specify a subnet or if you are removing all subnets. Otherwise, update requires no interruption. To update to a different subnet in the current Availability Zone, you must first update to a subnet in a different Availability Zone, then update to the new subnet in the original Availability Zone.
        :param tags: The tags associated with a load balancer.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c72e3198bf6eb83996a073ea891efd6a96d06fe98a055fb318c586be915448)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLoadBalancerProps(
            listeners=listeners,
            access_logging_policy=access_logging_policy,
            app_cookie_stickiness_policy=app_cookie_stickiness_policy,
            availability_zones=availability_zones,
            connection_draining_policy=connection_draining_policy,
            connection_settings=connection_settings,
            cross_zone=cross_zone,
            health_check=health_check,
            instances=instances,
            lb_cookie_stickiness_policy=lb_cookie_stickiness_policy,
            load_balancer_name=load_balancer_name,
            policies=policies,
            scheme=scheme,
            security_groups=security_groups,
            subnets=subnets,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e6ed363c861003c8eefe758dbed4240f18b764766ad2fc53ad7502f91f5df1)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d53019ecba4ab40de0108526f1db5fb8dcd7286cf2802c5a8fa91408219ed68)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCanonicalHostedZoneName")
    def attr_canonical_hosted_zone_name(self) -> builtins.str:
        '''The name of the Route 53 hosted zone that is associated with the load balancer.

        Internal-facing load balancers don't use this value, use ``DNSName`` instead.

        :cloudformationAttribute: CanonicalHostedZoneName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCanonicalHostedZoneName"))

    @builtins.property
    @jsii.member(jsii_name="attrCanonicalHostedZoneNameId")
    def attr_canonical_hosted_zone_name_id(self) -> builtins.str:
        '''The ID of the Route 53 hosted zone name that is associated with the load balancer.

        :cloudformationAttribute: CanonicalHostedZoneNameID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCanonicalHostedZoneNameId"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> builtins.str:
        '''The DNS name for the load balancer.

        :cloudformationAttribute: DNSName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsName"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceSecurityGroupGroupName")
    def attr_source_security_group_group_name(self) -> builtins.str:
        '''The name of the security group that you can use as part of your inbound rules for your load balancer's back-end instances.

        :cloudformationAttribute: SourceSecurityGroup.GroupName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceSecurityGroupGroupName"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceSecurityGroupOwnerAlias")
    def attr_source_security_group_owner_alias(self) -> builtins.str:
        '''The owner of the source security group.

        :cloudformationAttribute: SourceSecurityGroup.OwnerAlias
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceSecurityGroupOwnerAlias"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags associated with a load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-elasticloadbalancing-loadbalancer-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def listeners(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", _IResolvable_a771d0ef]]]:
        '''The listeners for the load balancer. You can specify at most one listener per port.

        If you update the properties for a listener, AWS CloudFormation deletes the existing listener and creates a new one with the specified properties. While the new listener is being created, clients cannot connect to the load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-listeners
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", _IResolvable_a771d0ef]]], jsii.get(self, "listeners"))

    @listeners.setter
    def listeners(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3afde5e1a749e7dad95c0ddf9544539f4ebbf9e146e76cd178cb1cd9a2a707d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listeners", value)

    @builtins.property
    @jsii.member(jsii_name="accessLoggingPolicy")
    def access_logging_policy(
        self,
    ) -> typing.Optional[typing.Union["CfnLoadBalancer.AccessLoggingPolicyProperty", _IResolvable_a771d0ef]]:
        '''Information about where and how access logs are stored for the load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-accessloggingpolicy
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLoadBalancer.AccessLoggingPolicyProperty", _IResolvable_a771d0ef]], jsii.get(self, "accessLoggingPolicy"))

    @access_logging_policy.setter
    def access_logging_policy(
        self,
        value: typing.Optional[typing.Union["CfnLoadBalancer.AccessLoggingPolicyProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a409e65b4ad8cad4e8b92819b11ae300493a97a27929e5f3af27e1015ad49b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLoggingPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="appCookieStickinessPolicy")
    def app_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.AppCookieStickinessPolicyProperty", _IResolvable_a771d0ef]]]]:
        '''Information about a policy for application-controlled session stickiness.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-appcookiestickinesspolicy
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.AppCookieStickinessPolicyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "appCookieStickinessPolicy"))

    @app_cookie_stickiness_policy.setter
    def app_cookie_stickiness_policy(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.AppCookieStickinessPolicyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b1185cf04e56a498f991f59286d0c1894df2778ab75d0aabd6a93799644037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appCookieStickinessPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Availability Zones for the load balancer. For load balancers in a VPC, specify ``Subnets`` instead.

        Update requires replacement if you did not previously specify an Availability Zone or if you are removing all Availability Zones. Otherwise, update requires no interruption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-availabilityzones
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cb2d9e085a2c9ff495d9bdc936d065216ea6f2fed596bd2b79cd5c63b00c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingPolicy")
    def connection_draining_policy(
        self,
    ) -> typing.Optional[typing.Union["CfnLoadBalancer.ConnectionDrainingPolicyProperty", _IResolvable_a771d0ef]]:
        '''If enabled, the load balancer allows existing requests to complete before the load balancer shifts traffic away from a deregistered or unhealthy instance.

        For more information, see `Configure Connection Draining <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-conn-drain.html>`_ in the *Classic Load Balancers Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectiondrainingpolicy
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLoadBalancer.ConnectionDrainingPolicyProperty", _IResolvable_a771d0ef]], jsii.get(self, "connectionDrainingPolicy"))

    @connection_draining_policy.setter
    def connection_draining_policy(
        self,
        value: typing.Optional[typing.Union["CfnLoadBalancer.ConnectionDrainingPolicyProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af3216931af6d03d7b174cc080b7376b6c4d0c9dcd759abdea9f1dd82c48ad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionDrainingPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="connectionSettings")
    def connection_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnLoadBalancer.ConnectionSettingsProperty", _IResolvable_a771d0ef]]:
        '''If enabled, the load balancer allows the connections to remain idle (no data is sent over the connection) for the specified duration.

        By default, Elastic Load Balancing maintains a 60-second idle connection timeout for both front-end and back-end connections of your load balancer. For more information, see `Configure Idle Connection Timeout <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html>`_ in the *Classic Load Balancers Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectionsettings
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLoadBalancer.ConnectionSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "connectionSettings"))

    @connection_settings.setter
    def connection_settings(
        self,
        value: typing.Optional[typing.Union["CfnLoadBalancer.ConnectionSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae69191ae901766833cb88c23be6c2b0b897d1cebc2ce4e0e01da02a524f5a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionSettings", value)

    @builtins.property
    @jsii.member(jsii_name="crossZone")
    def cross_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If enabled, the load balancer routes the request traffic evenly across all instances regardless of the Availability Zones.

        For more information, see `Configure Cross-Zone Load Balancing <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-disable-crosszone-lb.html>`_ in the *Classic Load Balancers Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-crosszone
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "crossZone"))

    @cross_zone.setter
    def cross_zone(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8049506f3d3b3ea4d46c04e9cc6c7a93e835ca45a4f1fefae7b56c3e3a42ce1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossZone", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheck")
    def health_check(
        self,
    ) -> typing.Optional[typing.Union["CfnLoadBalancer.HealthCheckProperty", _IResolvable_a771d0ef]]:
        '''The health check settings to use when evaluating the health of your EC2 instances.

        Update requires replacement if you did not previously specify health check settings or if you are removing the health check settings. Otherwise, update requires no interruption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-healthcheck
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLoadBalancer.HealthCheckProperty", _IResolvable_a771d0ef]], jsii.get(self, "healthCheck"))

    @health_check.setter
    def health_check(
        self,
        value: typing.Optional[typing.Union["CfnLoadBalancer.HealthCheckProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f86b984f361f6e0b0e847b0afee313e5f0b1d12090da7798d5826e1001c18de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheck", value)

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the instances for the load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-instances
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7414a41a42d5c1605a5cb00b537700f8f1567c261303a9fceba4f4c72159145c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value)

    @builtins.property
    @jsii.member(jsii_name="lbCookieStickinessPolicy")
    def lb_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.LBCookieStickinessPolicyProperty", _IResolvable_a771d0ef]]]]:
        '''Information about a policy for duration-based session stickiness.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-lbcookiestickinesspolicy
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.LBCookieStickinessPolicyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "lbCookieStickinessPolicy"))

    @lb_cookie_stickiness_policy.setter
    def lb_cookie_stickiness_policy(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.LBCookieStickinessPolicyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7cc1e1c8a87001ce7cd2676d6787d9068e500b0efaa80c5d13755c9159e8a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbCookieStickinessPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''The name of the load balancer.

        This name must be unique within your set of load balancers for the region.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID for the load balancer. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . If you specify a name, you cannot perform updates that require replacement of this resource, but you can perform other updates. To replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-elbname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerName"))

    @load_balancer_name.setter
    def load_balancer_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154f6b38c888696eb45be71944d00e10b5ac95d9695c295c59823ccb684da7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerName", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.PoliciesProperty", _IResolvable_a771d0ef]]]]:
        '''The policies defined for your Classic Load Balancer.

        Specify only back-end server policies.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-policies
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.PoliciesProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoadBalancer.PoliciesProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d5a1125c5300d2a91f9ae22622cbf2f5b168428aad8dcae1ec188376b9c101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. Valid only for load balancers in a VPC.

        If ``Scheme`` is ``internet-facing`` , the load balancer has a public DNS name that resolves to a public IP address.

        If ``Scheme`` is ``internal`` , the load balancer has a public DNS name that resolves to a private IP address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-scheme
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf075e3e30f385c85d823c3ccd2135990eeedc2b7a42b671b9bcc72d898ae01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security groups for the load balancer.

        Valid only for load balancers in a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-securitygroups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9341e513d7d456d3733bdec8866b0670acd69a0662208fdf7fc94e794a3e267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the subnets for the load balancer. You can specify at most one subnet per Availability Zone.

        Update requires replacement if you did not previously specify a subnet or if you are removing all subnets. Otherwise, update requires no interruption. To update to a different subnet in the current Availability Zone, you must first update to a subnet in a different Availability Zone, then update to the new subnet in the original Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-subnets
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86c2bad77351701593bd5996680c6ce040c016adaed5d4c6343e8d595f56c9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer.AccessLoggingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "s3_bucket_name": "s3BucketName",
            "emit_interval": "emitInterval",
            "s3_bucket_prefix": "s3BucketPrefix",
        },
    )
    class AccessLoggingPolicyProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            s3_bucket_name: builtins.str,
            emit_interval: typing.Optional[jsii.Number] = None,
            s3_bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies where and how access logs are stored for your Classic Load Balancer.

            :param enabled: Specifies whether access logs are enabled for the load balancer.
            :param s3_bucket_name: The name of the Amazon S3 bucket where the access logs are stored.
            :param emit_interval: The interval for publishing the access logs. You can specify an interval of either 5 minutes or 60 minutes. Default: 60 minutes
            :param s3_bucket_prefix: The logical hierarchy you created for your Amazon S3 bucket, for example ``my-bucket-prefix/prod`` . If the prefix is not provided, the log is placed at the root level of the bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticloadbalancing as elasticloadbalancing
                
                access_logging_policy_property = elasticloadbalancing.CfnLoadBalancer.AccessLoggingPolicyProperty(
                    enabled=False,
                    s3_bucket_name="s3BucketName",
                
                    # the properties below are optional
                    emit_interval=123,
                    s3_bucket_prefix="s3BucketPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9de56a5e8478c70b75e35f0da32c9fa6a97c038b6d92d5bb6e4f78655a4122c)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument emit_interval", value=emit_interval, expected_type=type_hints["emit_interval"])
                check_type(argname="argument s3_bucket_prefix", value=s3_bucket_prefix, expected_type=type_hints["s3_bucket_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
                "s3_bucket_name": s3_bucket_name,
            }
            if emit_interval is not None:
                self._values["emit_interval"] = emit_interval
            if s3_bucket_prefix is not None:
                self._values["s3_bucket_prefix"] = s3_bucket_prefix

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Specifies whether access logs are enabled for the load balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def s3_bucket_name(self) -> builtins.str:
            '''The name of the Amazon S3 bucket where the access logs are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            assert result is not None, "Required property 's3_bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def emit_interval(self) -> typing.Optional[jsii.Number]:
            '''The interval for publishing the access logs. You can specify an interval of either 5 minutes or 60 minutes.

            Default: 60 minutes

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-emitinterval
            '''
            result = self._values.get("emit_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def s3_bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The logical hierarchy you created for your Amazon S3 bucket, for example ``my-bucket-prefix/prod`` .

            If the prefix is not provided, the log is placed at the root level of the bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-s3bucketprefix
            '''
            result = self._values.get("s3_bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLoggingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer.AppCookieStickinessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cookie_name": "cookieName", "policy_name": "policyName"},
    )
    class AppCookieStickinessPolicyProperty:
        def __init__(
            self,
            *,
            cookie_name: builtins.str,
            policy_name: builtins.str,
        ) -> None:
            '''Specifies a policy for application-controlled session stickiness for your Classic Load Balancer.

            To associate a policy with a listener, use the `PolicyNames <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames>`_ property for the listener.

            :param cookie_name: The name of the application cookie used for stickiness.
            :param policy_name: The mnemonic name for the policy being created. The name must be unique within a set of policies for this load balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticloadbalancing as elasticloadbalancing
                
                app_cookie_stickiness_policy_property = elasticloadbalancing.CfnLoadBalancer.AppCookieStickinessPolicyProperty(
                    cookie_name="cookieName",
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6430ba4a0ef4d91a9f564e198bbccfe864cbf5835b55234513bde33a6752175)
                check_type(argname="argument cookie_name", value=cookie_name, expected_type=type_hints["cookie_name"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cookie_name": cookie_name,
                "policy_name": policy_name,
            }

        @builtins.property
        def cookie_name(self) -> builtins.str:
            '''The name of the application cookie used for stickiness.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html#cfn-elb-appcookiestickinesspolicy-cookiename
            '''
            result = self._values.get("cookie_name")
            assert result is not None, "Required property 'cookie_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def policy_name(self) -> builtins.str:
            '''The mnemonic name for the policy being created.

            The name must be unique within a set of policies for this load balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html#cfn-elb-appcookiestickinesspolicy-policyname
            '''
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppCookieStickinessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer.ConnectionDrainingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "timeout": "timeout"},
    )
    class ConnectionDrainingPolicyProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the connection draining settings for your Classic Load Balancer.

            :param enabled: Specifies whether connection draining is enabled for the load balancer.
            :param timeout: The maximum time, in seconds, to keep the existing connections open before deregistering the instances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticloadbalancing as elasticloadbalancing
                
                connection_draining_policy_property = elasticloadbalancing.CfnLoadBalancer.ConnectionDrainingPolicyProperty(
                    enabled=False,
                
                    # the properties below are optional
                    timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4cadf83e9db71080ce7cfa932f82b8132dc2d982f96c074878e14ef84ce31e2)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Specifies whether connection draining is enabled for the load balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html#cfn-elb-connectiondrainingpolicy-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The maximum time, in seconds, to keep the existing connections open before deregistering the instances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html#cfn-elb-connectiondrainingpolicy-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionDrainingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer.ConnectionSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"idle_timeout": "idleTimeout"},
    )
    class ConnectionSettingsProperty:
        def __init__(self, *, idle_timeout: jsii.Number) -> None:
            '''Specifies the idle timeout value for your Classic Load Balancer.

            :param idle_timeout: The time, in seconds, that the connection is allowed to be idle (no data has been sent over the connection) before it is closed by the load balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectionsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticloadbalancing as elasticloadbalancing
                
                connection_settings_property = elasticloadbalancing.CfnLoadBalancer.ConnectionSettingsProperty(
                    idle_timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e05780d0d99d5ad9f7b08ecbc1d918d7e4dba9af5750e4022075cbb9b856fd7)
                check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "idle_timeout": idle_timeout,
            }

        @builtins.property
        def idle_timeout(self) -> jsii.Number:
            '''The time, in seconds, that the connection is allowed to be idle (no data has been sent over the connection) before it is closed by the load balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectionsettings.html#cfn-elb-connectionsettings-idletimeout
            '''
            result = self._values.get("idle_timeout")
            assert result is not None, "Required property 'idle_timeout' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer.HealthCheckProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval": "interval",
            "target": "target",
            "timeout": "timeout",
            "unhealthy_threshold": "unhealthyThreshold",
        },
    )
    class HealthCheckProperty:
        def __init__(
            self,
            *,
            healthy_threshold: builtins.str,
            interval: builtins.str,
            target: builtins.str,
            timeout: builtins.str,
            unhealthy_threshold: builtins.str,
        ) -> None:
            '''Specifies health check settings for your Classic Load Balancer.

            :param healthy_threshold: The number of consecutive health checks successes required before moving the instance to the ``Healthy`` state.
            :param interval: The approximate interval, in seconds, between health checks of an individual instance.
            :param target: The instance being checked. The protocol is either TCP, HTTP, HTTPS, or SSL. The range of valid ports is one (1) through 65535. TCP is the default, specified as a TCP: port pair, for example "TCP:5000". In this case, a health check simply attempts to open a TCP connection to the instance on the specified port. Failure to connect within the configured timeout is considered unhealthy. SSL is also specified as SSL: port pair, for example, SSL:5000. For HTTP/HTTPS, you must include a ping path in the string. HTTP is specified as a HTTP:port;/;PathToPing; grouping, for example "HTTP:80/weather/us/wa/seattle". In this case, a HTTP GET request is issued to the instance on the given port and path. Any answer other than "200 OK" within the timeout period is considered unhealthy. The total length of the HTTP ping target must be 1024 16-bit Unicode characters or less.
            :param timeout: The amount of time, in seconds, during which no response means a failed health check. This value must be less than the ``Interval`` value.
            :param unhealthy_threshold: The number of consecutive health check failures required before moving the instance to the ``Unhealthy`` state.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticloadbalancing as elasticloadbalancing
                
                health_check_property = elasticloadbalancing.CfnLoadBalancer.HealthCheckProperty(
                    healthy_threshold="healthyThreshold",
                    interval="interval",
                    target="target",
                    timeout="timeout",
                    unhealthy_threshold="unhealthyThreshold"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ee6586584992772f143e52792db475366035885069391910bff721aadd1e0bc)
                check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
                check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "healthy_threshold": healthy_threshold,
                "interval": interval,
                "target": target,
                "timeout": timeout,
                "unhealthy_threshold": unhealthy_threshold,
            }

        @builtins.property
        def healthy_threshold(self) -> builtins.str:
            '''The number of consecutive health checks successes required before moving the instance to the ``Healthy`` state.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            assert result is not None, "Required property 'healthy_threshold' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def interval(self) -> builtins.str:
            '''The approximate interval, in seconds, between health checks of an individual instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-interval
            '''
            result = self._values.get("interval")
            assert result is not None, "Required property 'interval' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target(self) -> builtins.str:
            '''The instance being checked.

            The protocol is either TCP, HTTP, HTTPS, or SSL. The range of valid ports is one (1) through 65535.

            TCP is the default, specified as a TCP: port pair, for example "TCP:5000". In this case, a health check simply attempts to open a TCP connection to the instance on the specified port. Failure to connect within the configured timeout is considered unhealthy.

            SSL is also specified as SSL: port pair, for example, SSL:5000.

            For HTTP/HTTPS, you must include a ping path in the string. HTTP is specified as a HTTP:port;/;PathToPing; grouping, for example "HTTP:80/weather/us/wa/seattle". In this case, a HTTP GET request is issued to the instance on the given port and path. Any answer other than "200 OK" within the timeout period is considered unhealthy.

            The total length of the HTTP ping target must be 1024 16-bit Unicode characters or less.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def timeout(self) -> builtins.str:
            '''The amount of time, in seconds, during which no response means a failed health check.

            This value must be less than the ``Interval`` value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-timeout
            '''
            result = self._values.get("timeout")
            assert result is not None, "Required property 'timeout' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def unhealthy_threshold(self) -> builtins.str:
            '''The number of consecutive health check failures required before moving the instance to the ``Unhealthy`` state.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            assert result is not None, "Required property 'unhealthy_threshold' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer.LBCookieStickinessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cookie_expiration_period": "cookieExpirationPeriod",
            "policy_name": "policyName",
        },
    )
    class LBCookieStickinessPolicyProperty:
        def __init__(
            self,
            *,
            cookie_expiration_period: typing.Optional[builtins.str] = None,
            policy_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a policy for duration-based session stickiness for your Classic Load Balancer.

            To associate a policy with a listener, use the `PolicyNames <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames>`_ property for the listener.

            :param cookie_expiration_period: The time period, in seconds, after which the cookie should be considered stale. If this parameter is not specified, the stickiness session lasts for the duration of the browser session.
            :param policy_name: The name of the policy. This name must be unique within the set of policies for this load balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticloadbalancing as elasticloadbalancing
                
                l_bCookie_stickiness_policy_property = elasticloadbalancing.CfnLoadBalancer.LBCookieStickinessPolicyProperty(
                    cookie_expiration_period="cookieExpirationPeriod",
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__712ebb5a7b9f0c47d324ecd4b8372781a3df3f32aafe84c6c153084706769429)
                check_type(argname="argument cookie_expiration_period", value=cookie_expiration_period, expected_type=type_hints["cookie_expiration_period"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cookie_expiration_period is not None:
                self._values["cookie_expiration_period"] = cookie_expiration_period
            if policy_name is not None:
                self._values["policy_name"] = policy_name

        @builtins.property
        def cookie_expiration_period(self) -> typing.Optional[builtins.str]:
            '''The time period, in seconds, after which the cookie should be considered stale.

            If this parameter is not specified, the stickiness session lasts for the duration of the browser session.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html#cfn-elb-lbcookiestickinesspolicy-cookieexpirationperiod
            '''
            result = self._values.get("cookie_expiration_period")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''The name of the policy.

            This name must be unique within the set of policies for this load balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html#cfn-elb-lbcookiestickinesspolicy-policyname
            '''
            result = self._values.get("policy_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LBCookieStickinessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer.ListenersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_port": "instancePort",
            "load_balancer_port": "loadBalancerPort",
            "protocol": "protocol",
            "instance_protocol": "instanceProtocol",
            "policy_names": "policyNames",
            "ssl_certificate_id": "sslCertificateId",
        },
    )
    class ListenersProperty:
        def __init__(
            self,
            *,
            instance_port: builtins.str,
            load_balancer_port: builtins.str,
            protocol: builtins.str,
            instance_protocol: typing.Optional[builtins.str] = None,
            policy_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            ssl_certificate_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a listener for your Classic Load Balancer.

            Modifying any property replaces the listener.

            :param instance_port: The port on which the instance is listening.
            :param load_balancer_port: The port on which the load balancer is listening. On EC2-VPC, you can specify any port from the range 1-65535. On EC2-Classic, you can specify any port from the following list: 25, 80, 443, 465, 587, 1024-65535.
            :param protocol: The load balancer transport protocol to use for routing: HTTP, HTTPS, TCP, or SSL.
            :param instance_protocol: The protocol to use for routing traffic to instances: HTTP, HTTPS, TCP, or SSL. If the front-end protocol is TCP or SSL, the back-end protocol must be TCP or SSL. If the front-end protocol is HTTP or HTTPS, the back-end protocol must be HTTP or HTTPS. If there is another listener with the same ``InstancePort`` whose ``InstanceProtocol`` is secure, (HTTPS or SSL), the listener's ``InstanceProtocol`` must also be secure. If there is another listener with the same ``InstancePort`` whose ``InstanceProtocol`` is HTTP or TCP, the listener's ``InstanceProtocol`` must be HTTP or TCP.
            :param policy_names: The names of the policies to associate with the listener.
            :param ssl_certificate_id: The Amazon Resource Name (ARN) of the server certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticloadbalancing as elasticloadbalancing
                
                listeners_property = elasticloadbalancing.CfnLoadBalancer.ListenersProperty(
                    instance_port="instancePort",
                    load_balancer_port="loadBalancerPort",
                    protocol="protocol",
                
                    # the properties below are optional
                    instance_protocol="instanceProtocol",
                    policy_names=["policyNames"],
                    ssl_certificate_id="sslCertificateId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f813dccf6d0730b03b99f0352f282b9b0935467a2e88d07d6b52273db85fa1bd)
                check_type(argname="argument instance_port", value=instance_port, expected_type=type_hints["instance_port"])
                check_type(argname="argument load_balancer_port", value=load_balancer_port, expected_type=type_hints["load_balancer_port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument instance_protocol", value=instance_protocol, expected_type=type_hints["instance_protocol"])
                check_type(argname="argument policy_names", value=policy_names, expected_type=type_hints["policy_names"])
                check_type(argname="argument ssl_certificate_id", value=ssl_certificate_id, expected_type=type_hints["ssl_certificate_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_port": instance_port,
                "load_balancer_port": load_balancer_port,
                "protocol": protocol,
            }
            if instance_protocol is not None:
                self._values["instance_protocol"] = instance_protocol
            if policy_names is not None:
                self._values["policy_names"] = policy_names
            if ssl_certificate_id is not None:
                self._values["ssl_certificate_id"] = ssl_certificate_id

        @builtins.property
        def instance_port(self) -> builtins.str:
            '''The port on which the instance is listening.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-instanceport
            '''
            result = self._values.get("instance_port")
            assert result is not None, "Required property 'instance_port' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def load_balancer_port(self) -> builtins.str:
            '''The port on which the load balancer is listening.

            On EC2-VPC, you can specify any port from the range 1-65535. On EC2-Classic, you can specify any port from the following list: 25, 80, 443, 465, 587, 1024-65535.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-loadbalancerport
            '''
            result = self._values.get("load_balancer_port")
            assert result is not None, "Required property 'load_balancer_port' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''The load balancer transport protocol to use for routing: HTTP, HTTPS, TCP, or SSL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def instance_protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol to use for routing traffic to instances: HTTP, HTTPS, TCP, or SSL.

            If the front-end protocol is TCP or SSL, the back-end protocol must be TCP or SSL. If the front-end protocol is HTTP or HTTPS, the back-end protocol must be HTTP or HTTPS.

            If there is another listener with the same ``InstancePort`` whose ``InstanceProtocol`` is secure, (HTTPS or SSL), the listener's ``InstanceProtocol`` must also be secure.

            If there is another listener with the same ``InstancePort`` whose ``InstanceProtocol`` is HTTP or TCP, the listener's ``InstanceProtocol`` must be HTTP or TCP.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-instanceprotocol
            '''
            result = self._values.get("instance_protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of the policies to associate with the listener.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames
            '''
            result = self._values.get("policy_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ssl_certificate_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the server certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-sslcertificateid
            '''
            result = self._values.get("ssl_certificate_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancer.PoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "policy_name": "policyName",
            "policy_type": "policyType",
            "instance_ports": "instancePorts",
            "load_balancer_ports": "loadBalancerPorts",
        },
    )
    class PoliciesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef],
            policy_name: builtins.str,
            policy_type: builtins.str,
            instance_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
            load_balancer_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies policies for your Classic Load Balancer.

            To associate policies with a listener, use the `PolicyNames <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames>`_ property for the listener.

            :param attributes: The policy attributes.
            :param policy_name: The name of the policy.
            :param policy_type: The name of the policy type.
            :param instance_ports: The instance ports for the policy. Required only for some policy types.
            :param load_balancer_ports: The load balancer ports for the policy. Required only for some policy types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticloadbalancing as elasticloadbalancing
                
                # attributes: Any
                
                policies_property = elasticloadbalancing.CfnLoadBalancer.PoliciesProperty(
                    attributes=[attributes],
                    policy_name="policyName",
                    policy_type="policyType",
                
                    # the properties below are optional
                    instance_ports=["instancePorts"],
                    load_balancer_ports=["loadBalancerPorts"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c8783bbbf186413dfc0a1bee50d3873bf2327dfc6d69975690222691431d961)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
                check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
                check_type(argname="argument instance_ports", value=instance_ports, expected_type=type_hints["instance_ports"])
                check_type(argname="argument load_balancer_ports", value=load_balancer_ports, expected_type=type_hints["load_balancer_ports"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attributes": attributes,
                "policy_name": policy_name,
                "policy_type": policy_type,
            }
            if instance_ports is not None:
                self._values["instance_ports"] = instance_ports
            if load_balancer_ports is not None:
                self._values["load_balancer_ports"] = load_balancer_ports

        @builtins.property
        def attributes(
            self,
        ) -> typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]:
            '''The policy attributes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-attributes
            '''
            result = self._values.get("attributes")
            assert result is not None, "Required property 'attributes' is missing"
            return typing.cast(typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef], result)

        @builtins.property
        def policy_name(self) -> builtins.str:
            '''The name of the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-policyname
            '''
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def policy_type(self) -> builtins.str:
            '''The name of the policy type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-policytype
            '''
            result = self._values.get("policy_type")
            assert result is not None, "Required property 'policy_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def instance_ports(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instance ports for the policy.

            Required only for some policy types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-instanceports
            '''
            result = self._values.get("instance_ports")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def load_balancer_ports(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The load balancer ports for the policy.

            Required only for some policy types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-loadbalancerports
            '''
            result = self._values.get("load_balancer_ports")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticloadbalancing.CfnLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "listeners": "listeners",
        "access_logging_policy": "accessLoggingPolicy",
        "app_cookie_stickiness_policy": "appCookieStickinessPolicy",
        "availability_zones": "availabilityZones",
        "connection_draining_policy": "connectionDrainingPolicy",
        "connection_settings": "connectionSettings",
        "cross_zone": "crossZone",
        "health_check": "healthCheck",
        "instances": "instances",
        "lb_cookie_stickiness_policy": "lbCookieStickinessPolicy",
        "load_balancer_name": "loadBalancerName",
        "policies": "policies",
        "scheme": "scheme",
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "tags": "tags",
    },
)
class CfnLoadBalancerProps:
    def __init__(
        self,
        *,
        listeners: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.ListenersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        access_logging_policy: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        app_cookie_stickiness_policy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.AppCookieStickinessPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_draining_policy: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.ConnectionDrainingPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        connection_settings: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.ConnectionSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cross_zone: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        health_check: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.HealthCheckProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        lb_cookie_stickiness_policy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.LBCookieStickinessPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.PoliciesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLoadBalancer``.

        :param listeners: The listeners for the load balancer. You can specify at most one listener per port. If you update the properties for a listener, AWS CloudFormation deletes the existing listener and creates a new one with the specified properties. While the new listener is being created, clients cannot connect to the load balancer.
        :param access_logging_policy: Information about where and how access logs are stored for the load balancer.
        :param app_cookie_stickiness_policy: Information about a policy for application-controlled session stickiness.
        :param availability_zones: The Availability Zones for the load balancer. For load balancers in a VPC, specify ``Subnets`` instead. Update requires replacement if you did not previously specify an Availability Zone or if you are removing all Availability Zones. Otherwise, update requires no interruption.
        :param connection_draining_policy: If enabled, the load balancer allows existing requests to complete before the load balancer shifts traffic away from a deregistered or unhealthy instance. For more information, see `Configure Connection Draining <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-conn-drain.html>`_ in the *Classic Load Balancers Guide* .
        :param connection_settings: If enabled, the load balancer allows the connections to remain idle (no data is sent over the connection) for the specified duration. By default, Elastic Load Balancing maintains a 60-second idle connection timeout for both front-end and back-end connections of your load balancer. For more information, see `Configure Idle Connection Timeout <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html>`_ in the *Classic Load Balancers Guide* .
        :param cross_zone: If enabled, the load balancer routes the request traffic evenly across all instances regardless of the Availability Zones. For more information, see `Configure Cross-Zone Load Balancing <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-disable-crosszone-lb.html>`_ in the *Classic Load Balancers Guide* .
        :param health_check: The health check settings to use when evaluating the health of your EC2 instances. Update requires replacement if you did not previously specify health check settings or if you are removing the health check settings. Otherwise, update requires no interruption.
        :param instances: The IDs of the instances for the load balancer.
        :param lb_cookie_stickiness_policy: Information about a policy for duration-based session stickiness.
        :param load_balancer_name: The name of the load balancer. This name must be unique within your set of load balancers for the region. If you don't specify a name, AWS CloudFormation generates a unique physical ID for the load balancer. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . If you specify a name, you cannot perform updates that require replacement of this resource, but you can perform other updates. To replace the resource, specify a new name.
        :param policies: The policies defined for your Classic Load Balancer. Specify only back-end server policies.
        :param scheme: The type of load balancer. Valid only for load balancers in a VPC. If ``Scheme`` is ``internet-facing`` , the load balancer has a public DNS name that resolves to a public IP address. If ``Scheme`` is ``internal`` , the load balancer has a public DNS name that resolves to a private IP address.
        :param security_groups: The security groups for the load balancer. Valid only for load balancers in a VPC.
        :param subnets: The IDs of the subnets for the load balancer. You can specify at most one subnet per Availability Zone. Update requires replacement if you did not previously specify a subnet or if you are removing all subnets. Otherwise, update requires no interruption. To update to a different subnet in the current Availability Zone, you must first update to a subnet in a different Availability Zone, then update to the new subnet in the original Availability Zone.
        :param tags: The tags associated with a load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticloadbalancing as elasticloadbalancing
            
            # attributes: Any
            
            cfn_load_balancer_props = elasticloadbalancing.CfnLoadBalancerProps(
                listeners=[elasticloadbalancing.CfnLoadBalancer.ListenersProperty(
                    instance_port="instancePort",
                    load_balancer_port="loadBalancerPort",
                    protocol="protocol",
            
                    # the properties below are optional
                    instance_protocol="instanceProtocol",
                    policy_names=["policyNames"],
                    ssl_certificate_id="sslCertificateId"
                )],
            
                # the properties below are optional
                access_logging_policy=elasticloadbalancing.CfnLoadBalancer.AccessLoggingPolicyProperty(
                    enabled=False,
                    s3_bucket_name="s3BucketName",
            
                    # the properties below are optional
                    emit_interval=123,
                    s3_bucket_prefix="s3BucketPrefix"
                ),
                app_cookie_stickiness_policy=[elasticloadbalancing.CfnLoadBalancer.AppCookieStickinessPolicyProperty(
                    cookie_name="cookieName",
                    policy_name="policyName"
                )],
                availability_zones=["availabilityZones"],
                connection_draining_policy=elasticloadbalancing.CfnLoadBalancer.ConnectionDrainingPolicyProperty(
                    enabled=False,
            
                    # the properties below are optional
                    timeout=123
                ),
                connection_settings=elasticloadbalancing.CfnLoadBalancer.ConnectionSettingsProperty(
                    idle_timeout=123
                ),
                cross_zone=False,
                health_check=elasticloadbalancing.CfnLoadBalancer.HealthCheckProperty(
                    healthy_threshold="healthyThreshold",
                    interval="interval",
                    target="target",
                    timeout="timeout",
                    unhealthy_threshold="unhealthyThreshold"
                ),
                instances=["instances"],
                lb_cookie_stickiness_policy=[elasticloadbalancing.CfnLoadBalancer.LBCookieStickinessPolicyProperty(
                    cookie_expiration_period="cookieExpirationPeriod",
                    policy_name="policyName"
                )],
                load_balancer_name="loadBalancerName",
                policies=[elasticloadbalancing.CfnLoadBalancer.PoliciesProperty(
                    attributes=[attributes],
                    policy_name="policyName",
                    policy_type="policyType",
            
                    # the properties below are optional
                    instance_ports=["instancePorts"],
                    load_balancer_ports=["loadBalancerPorts"]
                )],
                scheme="scheme",
                security_groups=["securityGroups"],
                subnets=["subnets"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e91197929e53c2f274c27af955fed246ba162c72663b0c14f056874722e966)
            check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
            check_type(argname="argument access_logging_policy", value=access_logging_policy, expected_type=type_hints["access_logging_policy"])
            check_type(argname="argument app_cookie_stickiness_policy", value=app_cookie_stickiness_policy, expected_type=type_hints["app_cookie_stickiness_policy"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument connection_draining_policy", value=connection_draining_policy, expected_type=type_hints["connection_draining_policy"])
            check_type(argname="argument connection_settings", value=connection_settings, expected_type=type_hints["connection_settings"])
            check_type(argname="argument cross_zone", value=cross_zone, expected_type=type_hints["cross_zone"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument lb_cookie_stickiness_policy", value=lb_cookie_stickiness_policy, expected_type=type_hints["lb_cookie_stickiness_policy"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "listeners": listeners,
        }
        if access_logging_policy is not None:
            self._values["access_logging_policy"] = access_logging_policy
        if app_cookie_stickiness_policy is not None:
            self._values["app_cookie_stickiness_policy"] = app_cookie_stickiness_policy
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if connection_draining_policy is not None:
            self._values["connection_draining_policy"] = connection_draining_policy
        if connection_settings is not None:
            self._values["connection_settings"] = connection_settings
        if cross_zone is not None:
            self._values["cross_zone"] = cross_zone
        if health_check is not None:
            self._values["health_check"] = health_check
        if instances is not None:
            self._values["instances"] = instances
        if lb_cookie_stickiness_policy is not None:
            self._values["lb_cookie_stickiness_policy"] = lb_cookie_stickiness_policy
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if policies is not None:
            self._values["policies"] = policies
        if scheme is not None:
            self._values["scheme"] = scheme
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def listeners(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.ListenersProperty, _IResolvable_a771d0ef]]]:
        '''The listeners for the load balancer. You can specify at most one listener per port.

        If you update the properties for a listener, AWS CloudFormation deletes the existing listener and creates a new one with the specified properties. While the new listener is being created, clients cannot connect to the load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-listeners
        '''
        result = self._values.get("listeners")
        assert result is not None, "Required property 'listeners' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.ListenersProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def access_logging_policy(
        self,
    ) -> typing.Optional[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, _IResolvable_a771d0ef]]:
        '''Information about where and how access logs are stored for the load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-accessloggingpolicy
        '''
        result = self._values.get("access_logging_policy")
        return typing.cast(typing.Optional[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def app_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.AppCookieStickinessPolicyProperty, _IResolvable_a771d0ef]]]]:
        '''Information about a policy for application-controlled session stickiness.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-appcookiestickinesspolicy
        '''
        result = self._values.get("app_cookie_stickiness_policy")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.AppCookieStickinessPolicyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Availability Zones for the load balancer. For load balancers in a VPC, specify ``Subnets`` instead.

        Update requires replacement if you did not previously specify an Availability Zone or if you are removing all Availability Zones. Otherwise, update requires no interruption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_draining_policy(
        self,
    ) -> typing.Optional[typing.Union[CfnLoadBalancer.ConnectionDrainingPolicyProperty, _IResolvable_a771d0ef]]:
        '''If enabled, the load balancer allows existing requests to complete before the load balancer shifts traffic away from a deregistered or unhealthy instance.

        For more information, see `Configure Connection Draining <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-conn-drain.html>`_ in the *Classic Load Balancers Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectiondrainingpolicy
        '''
        result = self._values.get("connection_draining_policy")
        return typing.cast(typing.Optional[typing.Union[CfnLoadBalancer.ConnectionDrainingPolicyProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def connection_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnLoadBalancer.ConnectionSettingsProperty, _IResolvable_a771d0ef]]:
        '''If enabled, the load balancer allows the connections to remain idle (no data is sent over the connection) for the specified duration.

        By default, Elastic Load Balancing maintains a 60-second idle connection timeout for both front-end and back-end connections of your load balancer. For more information, see `Configure Idle Connection Timeout <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html>`_ in the *Classic Load Balancers Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectionsettings
        '''
        result = self._values.get("connection_settings")
        return typing.cast(typing.Optional[typing.Union[CfnLoadBalancer.ConnectionSettingsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cross_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If enabled, the load balancer routes the request traffic evenly across all instances regardless of the Availability Zones.

        For more information, see `Configure Cross-Zone Load Balancing <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-disable-crosszone-lb.html>`_ in the *Classic Load Balancers Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-crosszone
        '''
        result = self._values.get("cross_zone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def health_check(
        self,
    ) -> typing.Optional[typing.Union[CfnLoadBalancer.HealthCheckProperty, _IResolvable_a771d0ef]]:
        '''The health check settings to use when evaluating the health of your EC2 instances.

        Update requires replacement if you did not previously specify health check settings or if you are removing the health check settings. Otherwise, update requires no interruption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-healthcheck
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[typing.Union[CfnLoadBalancer.HealthCheckProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the instances for the load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-instances
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lb_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.LBCookieStickinessPolicyProperty, _IResolvable_a771d0ef]]]]:
        '''Information about a policy for duration-based session stickiness.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-lbcookiestickinesspolicy
        '''
        result = self._values.get("lb_cookie_stickiness_policy")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.LBCookieStickinessPolicyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''The name of the load balancer.

        This name must be unique within your set of load balancers for the region.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID for the load balancer. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . If you specify a name, you cannot perform updates that require replacement of this resource, but you can perform other updates. To replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-elbname
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.PoliciesProperty, _IResolvable_a771d0ef]]]]:
        '''The policies defined for your Classic Load Balancer.

        Specify only back-end server policies.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.PoliciesProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. Valid only for load balancers in a VPC.

        If ``Scheme`` is ``internet-facing`` , the load balancer has a public DNS name that resolves to a public IP address.

        If ``Scheme`` is ``internal`` , the load balancer has a public DNS name that resolves to a private IP address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-scheme
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security groups for the load balancer.

        Valid only for load balancers in a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the subnets for the load balancer. You can specify at most one subnet per Availability Zone.

        Update requires replacement if you did not previously specify a subnet or if you are removing all subnets. Otherwise, update requires no interruption. To update to a different subnet in the current Availability Zone, you must first update to a subnet in a different Availability Zone, then update to the new subnet in the original Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags associated with a load balancer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-elasticloadbalancing-loadbalancer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticloadbalancing.HealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "healthy_threshold": "healthyThreshold",
        "interval": "interval",
        "path": "path",
        "protocol": "protocol",
        "timeout": "timeout",
        "unhealthy_threshold": "unhealthyThreshold",
    },
)
class HealthCheck:
    def __init__(
        self,
        *,
        port: jsii.Number,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_Duration_070aa057] = None,
        path: typing.Optional[builtins.str] = None,
        protocol: typing.Optional["LoadBalancingProtocol"] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Describe the health check to a load balancer.

        :param port: (experimental) What port number to health check on.
        :param healthy_threshold: (experimental) After how many successful checks is an instance considered healthy. Default: 2
        :param interval: (experimental) Number of seconds between health checks. Default: Duration.seconds(30)
        :param path: (experimental) What path to use for HTTP or HTTPS health check (must return 200). For SSL and TCP health checks, accepting connections is enough to be considered healthy. Default: "/"
        :param protocol: (experimental) What protocol to use for health checking. The protocol is automatically determined from the port if it's not supplied. Default: Automatic
        :param timeout: (experimental) Health check timeout. Default: Duration.seconds(5)
        :param unhealthy_threshold: (experimental) After how many unsuccessful checks is an instance considered unhealthy. Default: 5

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.IVpc
            
            # my_auto_scaling_group: autoscaling.AutoScalingGroup
            
            lb = elb.LoadBalancer(self, "LB",
                vpc=vpc,
                internet_facing=True,
                health_check=elb.aws_elasticloadbalancing.HealthCheck(
                    port=80
                )
            )
            lb.add_target(my_auto_scaling_group)
            lb.add_listener(
                external_port=80
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c67c5be1b1d5230ec24736785c780cfa823c71042301a40eb862bd403e0801)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
        }
        if healthy_threshold is not None:
            self._values["healthy_threshold"] = healthy_threshold
        if interval is not None:
            self._values["interval"] = interval
        if path is not None:
            self._values["path"] = path
        if protocol is not None:
            self._values["protocol"] = protocol
        if timeout is not None:
            self._values["timeout"] = timeout
        if unhealthy_threshold is not None:
            self._values["unhealthy_threshold"] = unhealthy_threshold

    @builtins.property
    def port(self) -> jsii.Number:
        '''(experimental) What port number to health check on.

        :stability: experimental
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) After how many successful checks is an instance considered healthy.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("healthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Number of seconds between health checks.

        :default: Duration.seconds(30)

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) What path to use for HTTP or HTTPS health check (must return 200).

        For SSL and TCP health checks, accepting connections is enough to be considered
        healthy.

        :default: "/"

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        '''(experimental) What protocol to use for health checking.

        The protocol is automatically determined from the port if it's not supplied.

        :default: Automatic

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["LoadBalancingProtocol"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Health check timeout.

        :default: Duration.seconds(5)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) After how many unsuccessful checks is an instance considered unhealthy.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("unhealthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_elasticloadbalancing.ILoadBalancerTarget")
class ILoadBalancerTarget(_IConnectable_c1c0e72c, typing_extensions.Protocol):
    '''(experimental) Interface that is going to be implemented by constructs that you can load balance to.

    :stability: experimental
    '''

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: "LoadBalancer") -> None:
        '''(experimental) Attach load-balanced target to a classic ELB.

        :param load_balancer: [disable-awslint:ref-via-interface] The load balancer to attach the target to.

        :stability: experimental
        '''
        ...


class _ILoadBalancerTargetProxy(
    jsii.proxy_for(_IConnectable_c1c0e72c), # type: ignore[misc]
):
    '''(experimental) Interface that is going to be implemented by constructs that you can load balance to.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_elasticloadbalancing.ILoadBalancerTarget"

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: "LoadBalancer") -> None:
        '''(experimental) Attach load-balanced target to a classic ELB.

        :param load_balancer: [disable-awslint:ref-via-interface] The load balancer to attach the target to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5707a61e9e3ee5112fbd96b9b5a7f536a43a7493a79c98a35d0eb3a7a4c58a4)
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
        return typing.cast(None, jsii.invoke(self, "attachToClassicLB", [load_balancer]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILoadBalancerTarget).__jsii_proxy_class__ = lambda : _ILoadBalancerTargetProxy


@jsii.implements(_IConnectable_c1c0e72c)
class ListenerPort(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancing.ListenerPort",
):
    '''(experimental) Reference to a listener's port just created.

    This implements IConnectable with a default port (the port that an ELB
    listener was just created on) for a given security group so that it can be
    conveniently used just like any Connectable. E.g::

       const listener = elb.addListener(...);

       listener.connections.allowDefaultPortFromAnyIPv4();
       // or
       instance.connections.allowToDefaultPort(listener);

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_ec2 as ec2
        from monocdk import aws_elasticloadbalancing as elasticloadbalancing
        
        # port: ec2.Port
        # security_group: ec2.SecurityGroup
        
        listener_port = elasticloadbalancing.ListenerPort(security_group, port)
    '''

    def __init__(
        self,
        security_group: _ISecurityGroup_cdbba9d3,
        default_port: _Port_5f4cbf14,
    ) -> None:
        '''
        :param security_group: -
        :param default_port: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2a8f79a8d10c02d6460fe4cc45a5af1f0399ed5b74ddf367657c18cb7cb3aa)
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument default_port", value=default_port, expected_type=type_hints["default_port"])
        jsii.create(self.__class__, self, [security_group, default_port])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))


@jsii.implements(_IConnectable_c1c0e72c)
class LoadBalancer(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticloadbalancing.LoadBalancer",
):
    '''(experimental) A load balancer with a single listener.

    Routes to a fleet of of instances in a VPC.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # vpc: ec2.IVpc
        
        # my_auto_scaling_group: autoscaling.AutoScalingGroup
        
        lb = elb.LoadBalancer(self, "LB",
            vpc=vpc,
            internet_facing=True,
            health_check=elb.aws_elasticloadbalancing.HealthCheck(
                port=80
            )
        )
        lb.add_target(my_auto_scaling_group)
        lb.add_listener(
            external_port=80
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _IVpc_6d1f76c4,
        access_logging_policy: typing.Optional[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        cross_zone: typing.Optional[builtins.bool] = None,
        health_check: typing.Optional[typing.Union[HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        listeners: typing.Optional[typing.Sequence[typing.Union["LoadBalancerListener", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        targets: typing.Optional[typing.Sequence[ILoadBalancerTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) VPC network of the fleet instances.
        :param access_logging_policy: (experimental) Enable Loadbalancer access logs Can be used to avoid manual work as aws console Required S3 bucket name , enabled flag Can add interval for pushing log Can set bucket prefix in order to provide folder name inside bucket. Default: - disabled
        :param cross_zone: (experimental) Whether cross zone load balancing is enabled. This controls whether the load balancer evenly distributes requests across each availability zone Default: true
        :param health_check: (experimental) Health check settings for the load balancing targets. Not required but recommended. Default: - None.
        :param internet_facing: (experimental) Whether this is an internet-facing Load Balancer. This controls whether the LB has a public IP address assigned. It does not open up the Load Balancer's security groups to public internet access. Default: false
        :param listeners: (experimental) What listeners to set up for the load balancer. Can also be added by .addListener() Default: -
        :param subnet_selection: (experimental) Which subnets to deploy the load balancer. Can be used to define a specific set of subnets to deploy the load balancer to. Useful multiple public or private subnets are covering the same availability zone. Default: - Public subnets if internetFacing, Private subnets otherwise
        :param targets: (experimental) What targets to load balance to. Can also be added by .addTarget() Default: - None.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9e7d2596c04dc272bfd3a9eb8d14b015d6c5d5b840c5d4d752c6fd33921210)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LoadBalancerProps(
            vpc=vpc,
            access_logging_policy=access_logging_policy,
            cross_zone=cross_zone,
            health_check=health_check,
            internet_facing=internet_facing,
            listeners=listeners,
            subnet_selection=subnet_selection,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        *,
        external_port: jsii.Number,
        allow_connections_from: typing.Optional[typing.Sequence[_IConnectable_c1c0e72c]] = None,
        external_protocol: typing.Optional["LoadBalancingProtocol"] = None,
        internal_port: typing.Optional[jsii.Number] = None,
        internal_protocol: typing.Optional["LoadBalancingProtocol"] = None,
        policy_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssl_certificate_arn: typing.Optional[builtins.str] = None,
        ssl_certificate_id: typing.Optional[builtins.str] = None,
    ) -> ListenerPort:
        '''(experimental) Add a backend to the load balancer.

        :param external_port: (experimental) External listening port.
        :param allow_connections_from: (experimental) Allow connections to the load balancer from the given set of connection peers. By default, connections will be allowed from anywhere. Set this to an empty list to deny connections, or supply a custom list of peers to allow connections from (IP ranges or security groups). Default: Anywhere
        :param external_protocol: (experimental) What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the external port is either 80 or 443.
        :param internal_port: (experimental) Instance listening port. Same as the externalPort if not specified. Default: externalPort
        :param internal_protocol: (experimental) What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the internal port is either 80 or 443. The instance protocol is 'tcp' if the front-end protocol is 'tcp' or 'ssl', the instance protocol is 'http' if the front-end protocol is 'https'.
        :param policy_names: (experimental) SSL policy names.
        :param ssl_certificate_arn: (experimental) the ARN of the SSL certificate. Default: - none
        :param ssl_certificate_id: (deprecated) the ARN of the SSL certificate.

        :return: A ListenerPort object that controls connections to the listener port

        :stability: experimental
        '''
        listener = LoadBalancerListener(
            external_port=external_port,
            allow_connections_from=allow_connections_from,
            external_protocol=external_protocol,
            internal_port=internal_port,
            internal_protocol=internal_protocol,
            policy_names=policy_names,
            ssl_certificate_arn=ssl_certificate_arn,
            ssl_certificate_id=ssl_certificate_id,
        )

        return typing.cast(ListenerPort, jsii.invoke(self, "addListener", [listener]))

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: ILoadBalancerTarget) -> None:
        '''
        :param target: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a101e33da3e2dcab52230d415e1f04c0a15ba45797f7711f11c757d993f08b0)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "addTarget", [target]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) Control all connections from and to this load balancer.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="listenerPorts")
    def listener_ports(self) -> typing.List[ListenerPort]:
        '''(experimental) An object controlling specifically the connections for each listener added to this load balancer.

        :stability: experimental
        '''
        return typing.cast(typing.List[ListenerPort], jsii.get(self, "listenerPorts"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneName")
    def load_balancer_canonical_hosted_zone_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerCanonicalHostedZoneName"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneNameId")
    def load_balancer_canonical_hosted_zone_name_id(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerCanonicalHostedZoneNameId"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerDnsName"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerName"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupGroupName")
    def load_balancer_source_security_group_group_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerSourceSecurityGroupGroupName"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupOwnerAlias")
    def load_balancer_source_security_group_owner_alias(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerSourceSecurityGroupOwnerAlias"))


@jsii.data_type(
    jsii_type="monocdk.aws_elasticloadbalancing.LoadBalancerListener",
    jsii_struct_bases=[],
    name_mapping={
        "external_port": "externalPort",
        "allow_connections_from": "allowConnectionsFrom",
        "external_protocol": "externalProtocol",
        "internal_port": "internalPort",
        "internal_protocol": "internalProtocol",
        "policy_names": "policyNames",
        "ssl_certificate_arn": "sslCertificateArn",
        "ssl_certificate_id": "sslCertificateId",
    },
)
class LoadBalancerListener:
    def __init__(
        self,
        *,
        external_port: jsii.Number,
        allow_connections_from: typing.Optional[typing.Sequence[_IConnectable_c1c0e72c]] = None,
        external_protocol: typing.Optional["LoadBalancingProtocol"] = None,
        internal_port: typing.Optional[jsii.Number] = None,
        internal_protocol: typing.Optional["LoadBalancingProtocol"] = None,
        policy_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssl_certificate_arn: typing.Optional[builtins.str] = None,
        ssl_certificate_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a backend to the load balancer.

        :param external_port: (experimental) External listening port.
        :param allow_connections_from: (experimental) Allow connections to the load balancer from the given set of connection peers. By default, connections will be allowed from anywhere. Set this to an empty list to deny connections, or supply a custom list of peers to allow connections from (IP ranges or security groups). Default: Anywhere
        :param external_protocol: (experimental) What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the external port is either 80 or 443.
        :param internal_port: (experimental) Instance listening port. Same as the externalPort if not specified. Default: externalPort
        :param internal_protocol: (experimental) What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the internal port is either 80 or 443. The instance protocol is 'tcp' if the front-end protocol is 'tcp' or 'ssl', the instance protocol is 'http' if the front-end protocol is 'https'.
        :param policy_names: (experimental) SSL policy names.
        :param ssl_certificate_arn: (experimental) the ARN of the SSL certificate. Default: - none
        :param ssl_certificate_id: (deprecated) the ARN of the SSL certificate.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.IVpc
            
            # my_auto_scaling_group: autoscaling.AutoScalingGroup
            
            lb = elb.LoadBalancer(self, "LB",
                vpc=vpc,
                internet_facing=True,
                health_check=elb.aws_elasticloadbalancing.HealthCheck(
                    port=80
                )
            )
            lb.add_target(my_auto_scaling_group)
            lb.add_listener(
                external_port=80
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd800386425f1b48132dedde0913b1c2d7c486ab358b11f8219f7d0cd6f8a95)
            check_type(argname="argument external_port", value=external_port, expected_type=type_hints["external_port"])
            check_type(argname="argument allow_connections_from", value=allow_connections_from, expected_type=type_hints["allow_connections_from"])
            check_type(argname="argument external_protocol", value=external_protocol, expected_type=type_hints["external_protocol"])
            check_type(argname="argument internal_port", value=internal_port, expected_type=type_hints["internal_port"])
            check_type(argname="argument internal_protocol", value=internal_protocol, expected_type=type_hints["internal_protocol"])
            check_type(argname="argument policy_names", value=policy_names, expected_type=type_hints["policy_names"])
            check_type(argname="argument ssl_certificate_arn", value=ssl_certificate_arn, expected_type=type_hints["ssl_certificate_arn"])
            check_type(argname="argument ssl_certificate_id", value=ssl_certificate_id, expected_type=type_hints["ssl_certificate_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "external_port": external_port,
        }
        if allow_connections_from is not None:
            self._values["allow_connections_from"] = allow_connections_from
        if external_protocol is not None:
            self._values["external_protocol"] = external_protocol
        if internal_port is not None:
            self._values["internal_port"] = internal_port
        if internal_protocol is not None:
            self._values["internal_protocol"] = internal_protocol
        if policy_names is not None:
            self._values["policy_names"] = policy_names
        if ssl_certificate_arn is not None:
            self._values["ssl_certificate_arn"] = ssl_certificate_arn
        if ssl_certificate_id is not None:
            self._values["ssl_certificate_id"] = ssl_certificate_id

    @builtins.property
    def external_port(self) -> jsii.Number:
        '''(experimental) External listening port.

        :stability: experimental
        '''
        result = self._values.get("external_port")
        assert result is not None, "Required property 'external_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def allow_connections_from(
        self,
    ) -> typing.Optional[typing.List[_IConnectable_c1c0e72c]]:
        '''(experimental) Allow connections to the load balancer from the given set of connection peers.

        By default, connections will be allowed from anywhere. Set this to an empty list
        to deny connections, or supply a custom list of peers to allow connections from
        (IP ranges or security groups).

        :default: Anywhere

        :stability: experimental
        '''
        result = self._values.get("allow_connections_from")
        return typing.cast(typing.Optional[typing.List[_IConnectable_c1c0e72c]], result)

    @builtins.property
    def external_protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        '''(experimental) What public protocol to use for load balancing.

        Either 'tcp', 'ssl', 'http' or 'https'.

        May be omitted if the external port is either 80 or 443.

        :stability: experimental
        '''
        result = self._values.get("external_protocol")
        return typing.cast(typing.Optional["LoadBalancingProtocol"], result)

    @builtins.property
    def internal_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Instance listening port.

        Same as the externalPort if not specified.

        :default: externalPort

        :stability: experimental
        '''
        result = self._values.get("internal_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def internal_protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        '''(experimental) What public protocol to use for load balancing.

        Either 'tcp', 'ssl', 'http' or 'https'.

        May be omitted if the internal port is either 80 or 443.

        The instance protocol is 'tcp' if the front-end protocol
        is 'tcp' or 'ssl', the instance protocol is 'http' if the
        front-end protocol is 'https'.

        :stability: experimental
        '''
        result = self._values.get("internal_protocol")
        return typing.cast(typing.Optional["LoadBalancingProtocol"], result)

    @builtins.property
    def policy_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) SSL policy names.

        :stability: experimental
        '''
        result = self._values.get("policy_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssl_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) the ARN of the SSL certificate.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("ssl_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_certificate_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) the ARN of the SSL certificate.

        :deprecated: - use sslCertificateArn instead

        :stability: deprecated
        '''
        result = self._values.get("ssl_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerListener(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticloadbalancing.LoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "access_logging_policy": "accessLoggingPolicy",
        "cross_zone": "crossZone",
        "health_check": "healthCheck",
        "internet_facing": "internetFacing",
        "listeners": "listeners",
        "subnet_selection": "subnetSelection",
        "targets": "targets",
    },
)
class LoadBalancerProps:
    def __init__(
        self,
        *,
        vpc: _IVpc_6d1f76c4,
        access_logging_policy: typing.Optional[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        cross_zone: typing.Optional[builtins.bool] = None,
        health_check: typing.Optional[typing.Union[HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        listeners: typing.Optional[typing.Sequence[typing.Union[LoadBalancerListener, typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        targets: typing.Optional[typing.Sequence[ILoadBalancerTarget]] = None,
    ) -> None:
        '''(experimental) Construction properties for a LoadBalancer.

        :param vpc: (experimental) VPC network of the fleet instances.
        :param access_logging_policy: (experimental) Enable Loadbalancer access logs Can be used to avoid manual work as aws console Required S3 bucket name , enabled flag Can add interval for pushing log Can set bucket prefix in order to provide folder name inside bucket. Default: - disabled
        :param cross_zone: (experimental) Whether cross zone load balancing is enabled. This controls whether the load balancer evenly distributes requests across each availability zone Default: true
        :param health_check: (experimental) Health check settings for the load balancing targets. Not required but recommended. Default: - None.
        :param internet_facing: (experimental) Whether this is an internet-facing Load Balancer. This controls whether the LB has a public IP address assigned. It does not open up the Load Balancer's security groups to public internet access. Default: false
        :param listeners: (experimental) What listeners to set up for the load balancer. Can also be added by .addListener() Default: -
        :param subnet_selection: (experimental) Which subnets to deploy the load balancer. Can be used to define a specific set of subnets to deploy the load balancer to. Useful multiple public or private subnets are covering the same availability zone. Default: - Public subnets if internetFacing, Private subnets otherwise
        :param targets: (experimental) What targets to load balance to. Can also be added by .addTarget() Default: - None.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            # task_definition: ecs.TaskDefinition
            # vpc: ec2.Vpc
            
            service = ecs.Ec2Service(self, "Service", cluster=cluster, task_definition=task_definition)
            
            lb = elb.LoadBalancer(self, "LB", vpc=vpc)
            lb.add_listener(external_port=80)
            lb.add_target(service)
        '''
        if isinstance(access_logging_policy, dict):
            access_logging_policy = CfnLoadBalancer.AccessLoggingPolicyProperty(**access_logging_policy)
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b544a710b0a638ba983c3d85ca96c4db7d400b12aae3118d2b29733c22aabe4)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument access_logging_policy", value=access_logging_policy, expected_type=type_hints["access_logging_policy"])
            check_type(argname="argument cross_zone", value=cross_zone, expected_type=type_hints["cross_zone"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument internet_facing", value=internet_facing, expected_type=type_hints["internet_facing"])
            check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if access_logging_policy is not None:
            self._values["access_logging_policy"] = access_logging_policy
        if cross_zone is not None:
            self._values["cross_zone"] = cross_zone
        if health_check is not None:
            self._values["health_check"] = health_check
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if listeners is not None:
            self._values["listeners"] = listeners
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) VPC network of the fleet instances.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def access_logging_policy(
        self,
    ) -> typing.Optional[CfnLoadBalancer.AccessLoggingPolicyProperty]:
        '''(experimental) Enable Loadbalancer access logs Can be used to avoid manual work as aws console Required S3 bucket name , enabled flag Can add interval for pushing log Can set bucket prefix in order to provide folder name inside bucket.

        :default: - disabled

        :stability: experimental
        '''
        result = self._values.get("access_logging_policy")
        return typing.cast(typing.Optional[CfnLoadBalancer.AccessLoggingPolicyProperty], result)

    @builtins.property
    def cross_zone(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether cross zone load balancing is enabled.

        This controls whether the load balancer evenly distributes requests
        across each availability zone

        :default: true

        :stability: experimental
        '''
        result = self._values.get("cross_zone")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        '''(experimental) Health check settings for the load balancing targets.

        Not required but recommended.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[HealthCheck], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this is an internet-facing Load Balancer.

        This controls whether the LB has a public IP address assigned. It does
        not open up the Load Balancer's security groups to public internet access.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List[LoadBalancerListener]]:
        '''(experimental) What listeners to set up for the load balancer.

        Can also be added by .addListener()

        :default: -

        :stability: experimental
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.List[LoadBalancerListener]], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to deploy the load balancer.

        Can be used to define a specific set of subnets to deploy the load balancer to.
        Useful multiple public or private subnets are covering the same availability zone.

        :default: - Public subnets if internetFacing, Private subnets otherwise

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[ILoadBalancerTarget]]:
        '''(experimental) What targets to load balance to.

        Can also be added by .addTarget()

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[ILoadBalancerTarget]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_elasticloadbalancing.LoadBalancingProtocol")
class LoadBalancingProtocol(enum.Enum):
    '''
    :stability: experimental
    '''

    TCP = "TCP"
    '''
    :stability: experimental
    '''
    SSL = "SSL"
    '''
    :stability: experimental
    '''
    HTTP = "HTTP"
    '''
    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''
    :stability: experimental
    '''


__all__ = [
    "CfnLoadBalancer",
    "CfnLoadBalancerProps",
    "HealthCheck",
    "ILoadBalancerTarget",
    "ListenerPort",
    "LoadBalancer",
    "LoadBalancerListener",
    "LoadBalancerProps",
    "LoadBalancingProtocol",
]

publication.publish()

def _typecheckingstub__97c72e3198bf6eb83996a073ea891efd6a96d06fe98a055fb318c586be915448(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    listeners: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.ListenersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    access_logging_policy: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    app_cookie_stickiness_policy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.AppCookieStickinessPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_draining_policy: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.ConnectionDrainingPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    connection_settings: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.ConnectionSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cross_zone: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    health_check: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.HealthCheckProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    lb_cookie_stickiness_policy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.LBCookieStickinessPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.PoliciesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    scheme: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e6ed363c861003c8eefe758dbed4240f18b764766ad2fc53ad7502f91f5df1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d53019ecba4ab40de0108526f1db5fb8dcd7286cf2802c5a8fa91408219ed68(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afde5e1a749e7dad95c0ddf9544539f4ebbf9e146e76cd178cb1cd9a2a707d9(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.ListenersProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a409e65b4ad8cad4e8b92819b11ae300493a97a27929e5f3af27e1015ad49b6f(
    value: typing.Optional[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b1185cf04e56a498f991f59286d0c1894df2778ab75d0aabd6a93799644037(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.AppCookieStickinessPolicyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cb2d9e085a2c9ff495d9bdc936d065216ea6f2fed596bd2b79cd5c63b00c73(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af3216931af6d03d7b174cc080b7376b6c4d0c9dcd759abdea9f1dd82c48ad0(
    value: typing.Optional[typing.Union[CfnLoadBalancer.ConnectionDrainingPolicyProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae69191ae901766833cb88c23be6c2b0b897d1cebc2ce4e0e01da02a524f5a0e(
    value: typing.Optional[typing.Union[CfnLoadBalancer.ConnectionSettingsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8049506f3d3b3ea4d46c04e9cc6c7a93e835ca45a4f1fefae7b56c3e3a42ce1f(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f86b984f361f6e0b0e847b0afee313e5f0b1d12090da7798d5826e1001c18de(
    value: typing.Optional[typing.Union[CfnLoadBalancer.HealthCheckProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7414a41a42d5c1605a5cb00b537700f8f1567c261303a9fceba4f4c72159145c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7cc1e1c8a87001ce7cd2676d6787d9068e500b0efaa80c5d13755c9159e8a23(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.LBCookieStickinessPolicyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154f6b38c888696eb45be71944d00e10b5ac95d9695c295c59823ccb684da7bf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d5a1125c5300d2a91f9ae22622cbf2f5b168428aad8dcae1ec188376b9c101(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLoadBalancer.PoliciesProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf075e3e30f385c85d823c3ccd2135990eeedc2b7a42b671b9bcc72d898ae01(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9341e513d7d456d3733bdec8866b0670acd69a0662208fdf7fc94e794a3e267(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86c2bad77351701593bd5996680c6ce040c016adaed5d4c6343e8d595f56c9b(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9de56a5e8478c70b75e35f0da32c9fa6a97c038b6d92d5bb6e4f78655a4122c(
    *,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    s3_bucket_name: builtins.str,
    emit_interval: typing.Optional[jsii.Number] = None,
    s3_bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6430ba4a0ef4d91a9f564e198bbccfe864cbf5835b55234513bde33a6752175(
    *,
    cookie_name: builtins.str,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4cadf83e9db71080ce7cfa932f82b8132dc2d982f96c074878e14ef84ce31e2(
    *,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e05780d0d99d5ad9f7b08ecbc1d918d7e4dba9af5750e4022075cbb9b856fd7(
    *,
    idle_timeout: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee6586584992772f143e52792db475366035885069391910bff721aadd1e0bc(
    *,
    healthy_threshold: builtins.str,
    interval: builtins.str,
    target: builtins.str,
    timeout: builtins.str,
    unhealthy_threshold: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712ebb5a7b9f0c47d324ecd4b8372781a3df3f32aafe84c6c153084706769429(
    *,
    cookie_expiration_period: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f813dccf6d0730b03b99f0352f282b9b0935467a2e88d07d6b52273db85fa1bd(
    *,
    instance_port: builtins.str,
    load_balancer_port: builtins.str,
    protocol: builtins.str,
    instance_protocol: typing.Optional[builtins.str] = None,
    policy_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssl_certificate_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8783bbbf186413dfc0a1bee50d3873bf2327dfc6d69975690222691431d961(
    *,
    attributes: typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef],
    policy_name: builtins.str,
    policy_type: builtins.str,
    instance_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    load_balancer_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e91197929e53c2f274c27af955fed246ba162c72663b0c14f056874722e966(
    *,
    listeners: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.ListenersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    access_logging_policy: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    app_cookie_stickiness_policy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.AppCookieStickinessPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_draining_policy: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.ConnectionDrainingPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    connection_settings: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.ConnectionSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cross_zone: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    health_check: typing.Optional[typing.Union[typing.Union[CfnLoadBalancer.HealthCheckProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    lb_cookie_stickiness_policy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.LBCookieStickinessPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoadBalancer.PoliciesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    scheme: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c67c5be1b1d5230ec24736785c780cfa823c71042301a40eb862bd403e0801(
    *,
    port: jsii.Number,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_Duration_070aa057] = None,
    path: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[LoadBalancingProtocol] = None,
    timeout: typing.Optional[_Duration_070aa057] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5707a61e9e3ee5112fbd96b9b5a7f536a43a7493a79c98a35d0eb3a7a4c58a4(
    load_balancer: LoadBalancer,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2a8f79a8d10c02d6460fe4cc45a5af1f0399ed5b74ddf367657c18cb7cb3aa(
    security_group: _ISecurityGroup_cdbba9d3,
    default_port: _Port_5f4cbf14,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9e7d2596c04dc272bfd3a9eb8d14b015d6c5d5b840c5d4d752c6fd33921210(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _IVpc_6d1f76c4,
    access_logging_policy: typing.Optional[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_zone: typing.Optional[builtins.bool] = None,
    health_check: typing.Optional[typing.Union[HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
    listeners: typing.Optional[typing.Sequence[typing.Union[LoadBalancerListener, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    targets: typing.Optional[typing.Sequence[ILoadBalancerTarget]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a101e33da3e2dcab52230d415e1f04c0a15ba45797f7711f11c757d993f08b0(
    target: ILoadBalancerTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd800386425f1b48132dedde0913b1c2d7c486ab358b11f8219f7d0cd6f8a95(
    *,
    external_port: jsii.Number,
    allow_connections_from: typing.Optional[typing.Sequence[_IConnectable_c1c0e72c]] = None,
    external_protocol: typing.Optional[LoadBalancingProtocol] = None,
    internal_port: typing.Optional[jsii.Number] = None,
    internal_protocol: typing.Optional[LoadBalancingProtocol] = None,
    policy_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssl_certificate_arn: typing.Optional[builtins.str] = None,
    ssl_certificate_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b544a710b0a638ba983c3d85ca96c4db7d400b12aae3118d2b29733c22aabe4(
    *,
    vpc: _IVpc_6d1f76c4,
    access_logging_policy: typing.Optional[typing.Union[CfnLoadBalancer.AccessLoggingPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_zone: typing.Optional[builtins.bool] = None,
    health_check: typing.Optional[typing.Union[HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
    listeners: typing.Optional[typing.Sequence[typing.Union[LoadBalancerListener, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    targets: typing.Optional[typing.Sequence[ILoadBalancerTarget]] = None,
) -> None:
    """Type checking stubs"""
    pass
