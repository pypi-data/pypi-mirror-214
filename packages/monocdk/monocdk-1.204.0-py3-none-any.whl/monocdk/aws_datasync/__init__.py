'''
# AWS::DataSync Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as datasync
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DataSync construct libraries](https://constructs.dev/search?q=datasync)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DataSync resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataSync.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DataSync](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataSync.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAgent(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnAgent",
):
    '''A CloudFormation ``AWS::DataSync::Agent``.

    The ``AWS::DataSync::Agent`` resource activates an AWS DataSync agent that you've deployed for storage discovery or data transfers. The activation process associates the agent with your AWS account .

    For more information, see the following topics in the *AWS DataSync User Guide* :

    - `DataSync agent requirements <https://docs.aws.amazon.com/datasync/latest/userguide/agent-requirements.html>`_
    - `DataSync network requirements <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html>`_
    - `Create a DataSync agent <https://docs.aws.amazon.com/datasync/latest/userguide/configure-agent.html>`_

    :cloudformationResource: AWS::DataSync::Agent
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_agent = datasync.CfnAgent(self, "MyCfnAgent",
            activation_key="activationKey",
            agent_name="agentName",
            security_group_arns=["securityGroupArns"],
            subnet_arns=["subnetArns"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_endpoint_id="vpcEndpointId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        activation_key: typing.Optional[builtins.str] = None,
        agent_name: typing.Optional[builtins.str] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::Agent``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param activation_key: Specifies your DataSync agent's activation key. If you don't have an activation key, see `Activate your agent <https://docs.aws.amazon.com/datasync/latest/userguide/activate-agent.html>`_ .
        :param agent_name: Specifies a name for your agent. You can see this name in the DataSync console.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets. See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ . *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``
        :param subnet_arns: Specifies the ARN of the subnet where you want to run your DataSync task when using a VPC endpoint. This is the subnet where DataSync creates and manages the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces>`_ for your transfer.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least one tag for your agent.
        :param vpc_endpoint_id: The ID of the virtual private cloud (VPC) endpoint that the agent has access to. This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* . For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.* A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40bc48416d05a3c3798c480bd2f171f08d8a07e79853a97bb307684e0ea877bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAgentProps(
            activation_key=activation_key,
            agent_name=agent_name,
            security_group_arns=security_group_arns,
            subnet_arns=subnet_arns,
            tags=tags,
            vpc_endpoint_id=vpc_endpoint_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fac63d091edc871757ceb6b42d8d16ec0e0f5ed142f2819463db008241e0fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c98969645c2929b5277accfc3b22b59fcb0edf7737b384eb8ea319ebbdbbcfe)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentArn")
    def attr_agent_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the agent.

        Use the ``ListAgents`` operation to return a list of agents for your account and AWS Region .

        :cloudformationAttribute: AgentArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpointType")
    def attr_endpoint_type(self) -> builtins.str:
        '''The type of endpoint that your agent is connected to.

        If the endpoint is a VPC endpoint, the agent is not accessible over the public internet.

        :cloudformationAttribute: EndpointType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpointType"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least one tag for your agent.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="activationKey")
    def activation_key(self) -> typing.Optional[builtins.str]:
        '''Specifies your DataSync agent's activation key.

        If you don't have an activation key, see `Activate your agent <https://docs.aws.amazon.com/datasync/latest/userguide/activate-agent.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-activationkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activationKey"))

    @activation_key.setter
    def activation_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855ee5b59f119637d4b3a87aaeb01c689211b340948ad9244c252a429e716251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationKey", value)

    @builtins.property
    @jsii.member(jsii_name="agentName")
    def agent_name(self) -> typing.Optional[builtins.str]:
        '''Specifies a name for your agent.

        You can see this name in the DataSync console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-agentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentName"))

    @agent_name.setter
    def agent_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cebc85eba53bd252bd30db3d4c49f02e548604de36e7bacdde94c0d0eacbc6c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentName", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets.

        See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ .

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-securitygrouparns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f381110d1ada03ebd723605ebffd98363d0af0827baf314dc81e64cf2e2571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="subnetArns")
    def subnet_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the ARN of the subnet where you want to run your DataSync task when using a VPC endpoint.

        This is the subnet where DataSync creates and manages the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces>`_ for your transfer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-subnetarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetArns"))

    @subnet_arns.setter
    def subnet_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aabd9b71947098dba7058d8316d41a3dbeced628b5561dd305e996da698812ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetArns", value)

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC) endpoint that the agent has access to.

        This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* .

        For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.*

        A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-vpcendpointid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcEndpointId"))

    @vpc_endpoint_id.setter
    def vpc_endpoint_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d631d58bf8f884042ad043282b84a5ad556ef004d3c0bd70353d8b6a845b5127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcEndpointId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnAgentProps",
    jsii_struct_bases=[],
    name_mapping={
        "activation_key": "activationKey",
        "agent_name": "agentName",
        "security_group_arns": "securityGroupArns",
        "subnet_arns": "subnetArns",
        "tags": "tags",
        "vpc_endpoint_id": "vpcEndpointId",
    },
)
class CfnAgentProps:
    def __init__(
        self,
        *,
        activation_key: typing.Optional[builtins.str] = None,
        agent_name: typing.Optional[builtins.str] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAgent``.

        :param activation_key: Specifies your DataSync agent's activation key. If you don't have an activation key, see `Activate your agent <https://docs.aws.amazon.com/datasync/latest/userguide/activate-agent.html>`_ .
        :param agent_name: Specifies a name for your agent. You can see this name in the DataSync console.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets. See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ . *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``
        :param subnet_arns: Specifies the ARN of the subnet where you want to run your DataSync task when using a VPC endpoint. This is the subnet where DataSync creates and manages the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces>`_ for your transfer.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least one tag for your agent.
        :param vpc_endpoint_id: The ID of the virtual private cloud (VPC) endpoint that the agent has access to. This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* . For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.* A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_agent_props = datasync.CfnAgentProps(
                activation_key="activationKey",
                agent_name="agentName",
                security_group_arns=["securityGroupArns"],
                subnet_arns=["subnetArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_endpoint_id="vpcEndpointId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5d239366e36c20331a336f351cd02f2e7bf390c150321a0edaaf99d9674858)
            check_type(argname="argument activation_key", value=activation_key, expected_type=type_hints["activation_key"])
            check_type(argname="argument agent_name", value=agent_name, expected_type=type_hints["agent_name"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument subnet_arns", value=subnet_arns, expected_type=type_hints["subnet_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activation_key is not None:
            self._values["activation_key"] = activation_key
        if agent_name is not None:
            self._values["agent_name"] = agent_name
        if security_group_arns is not None:
            self._values["security_group_arns"] = security_group_arns
        if subnet_arns is not None:
            self._values["subnet_arns"] = subnet_arns
        if tags is not None:
            self._values["tags"] = tags
        if vpc_endpoint_id is not None:
            self._values["vpc_endpoint_id"] = vpc_endpoint_id

    @builtins.property
    def activation_key(self) -> typing.Optional[builtins.str]:
        '''Specifies your DataSync agent's activation key.

        If you don't have an activation key, see `Activate your agent <https://docs.aws.amazon.com/datasync/latest/userguide/activate-agent.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-activationkey
        '''
        result = self._values.get("activation_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_name(self) -> typing.Optional[builtins.str]:
        '''Specifies a name for your agent.

        You can see this name in the DataSync console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-agentname
        '''
        result = self._values.get("agent_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets.

        See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ .

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the ARN of the subnet where you want to run your DataSync task when using a VPC endpoint.

        This is the subnet where DataSync creates and manages the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces>`_ for your transfer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-subnetarns
        '''
        result = self._values.get("subnet_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least one tag for your agent.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC) endpoint that the agent has access to.

        This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* .

        For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.*

        A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-vpcendpointid
        '''
        result = self._values.get("vpc_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationEFS(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationEFS",
):
    '''A CloudFormation ``AWS::DataSync::LocationEFS``.

    The ``AWS::DataSync::LocationEFS`` resource creates an endpoint for an Amazon EFS file system. AWS DataSync can access this endpoint as a source or destination location.

    :cloudformationResource: AWS::DataSync::LocationEFS
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_eFS = datasync.CfnLocationEFS(self, "MyCfnLocationEFS",
            ec2_config=datasync.CfnLocationEFS.Ec2ConfigProperty(
                security_group_arns=["securityGroupArns"],
                subnet_arn="subnetArn"
            ),
        
            # the properties below are optional
            access_point_arn="accessPointArn",
            efs_filesystem_arn="efsFilesystemArn",
            file_system_access_role_arn="fileSystemAccessRoleArn",
            in_transit_encryption="inTransitEncryption",
            subdirectory="subdirectory",
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
        ec2_config: typing.Union[typing.Union["CfnLocationEFS.Ec2ConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        access_point_arn: typing.Optional[builtins.str] = None,
        efs_filesystem_arn: typing.Optional[builtins.str] = None,
        file_system_access_role_arn: typing.Optional[builtins.str] = None,
        in_transit_encryption: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationEFS``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ec2_config: Specifies the subnet and security groups DataSync uses to access your Amazon EFS file system.
        :param access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        :param efs_filesystem_arn: Specifies the ARN for the Amazon EFS file system.
        :param file_system_access_role_arn: Specifies an AWS Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        :param in_transit_encryption: Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it copies data to or from the Amazon EFS file system. If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .
        :param subdirectory: Specifies a mount path for your Amazon EFS file system. This is where DataSync reads or writes data (depending on if this is a source or destination location). By default, DataSync uses the root directory, but you can also include subdirectories. .. epigraph:: You must specify a value with forward slashes (for example, ``/path/to/folder`` ).
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc162613eb797739f51c27be788dbee2cca8a981bb5b5606c69ddb389349fe3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationEFSProps(
            ec2_config=ec2_config,
            access_point_arn=access_point_arn,
            efs_filesystem_arn=efs_filesystem_arn,
            file_system_access_role_arn=file_system_access_role_arn,
            in_transit_encryption=in_transit_encryption,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6445c297e92df989cc02841ee3cec279cac26038774c8bb67b7ae01298ab040c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b00dc83501a5f304f9996698254823a75ab287b2e681691e3e2f7aebd9113743)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon EFS file system.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the Amazon EFS file system.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="ec2Config")
    def ec2_config(
        self,
    ) -> typing.Union["CfnLocationEFS.Ec2ConfigProperty", _IResolvable_a771d0ef]:
        '''Specifies the subnet and security groups DataSync uses to access your Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-ec2config
        '''
        return typing.cast(typing.Union["CfnLocationEFS.Ec2ConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "ec2Config"))

    @ec2_config.setter
    def ec2_config(
        self,
        value: typing.Union["CfnLocationEFS.Ec2ConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d81363b55f67611c7312d9c1e71c9a726892d9884f7b1e8dc12ca77ab31a359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2Config", value)

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-accesspointarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPointArn"))

    @access_point_arn.setter
    def access_point_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749c58e7fecfb149d42c2ef0b7c983122358638facdc1343d6a2be7166b18c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPointArn", value)

    @builtins.property
    @jsii.member(jsii_name="efsFilesystemArn")
    def efs_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN for the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-efsfilesystemarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "efsFilesystemArn"))

    @efs_filesystem_arn.setter
    def efs_filesystem_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e138dbcc026bb9bc8aebf11eece197f9e9bdb7e57c230dfbf617e9353268af72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "efsFilesystemArn", value)

    @builtins.property
    @jsii.member(jsii_name="fileSystemAccessRoleArn")
    def file_system_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies an AWS Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-filesystemaccessrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileSystemAccessRoleArn"))

    @file_system_access_role_arn.setter
    def file_system_access_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7d2471216a8beac6dde92a009e1142d4db21addc1eed1e16760e8bca2ac836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemAccessRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="inTransitEncryption")
    def in_transit_encryption(self) -> typing.Optional[builtins.str]:
        '''Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it copies data to or from the Amazon EFS file system.

        If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-intransitencryption
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inTransitEncryption"))

    @in_transit_encryption.setter
    def in_transit_encryption(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2e1c32665fb4f3d90df0ee53d5bfa764f6444aa3593805e8437a42627af188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inTransitEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your Amazon EFS file system.

        This is where DataSync reads or writes data (depending on if this is a source or destination location). By default, DataSync uses the root directory, but you can also include subdirectories.
        .. epigraph::

           You must specify a value with forward slashes (for example, ``/path/to/folder`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d9b09853b2663323c4ddf4e98d501f0b5eca8e58e36dec14ceb2c3fbabe6be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationEFS.Ec2ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_arns": "securityGroupArns",
            "subnet_arn": "subnetArn",
        },
    )
    class Ec2ConfigProperty:
        def __init__(
            self,
            *,
            security_group_arns: typing.Sequence[builtins.str],
            subnet_arn: builtins.str,
        ) -> None:
            '''The subnet and security groups that AWS DataSync uses to access your Amazon EFS file system.

            :param security_group_arns: Specifies the Amazon Resource Names (ARNs) of the security groups associated with an Amazon EFS file system's mount target.
            :param subnet_arn: Specifies the ARN of a subnet where DataSync creates the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces>`_ for managing traffic during your transfer. The subnet must be located: - In the same virtual private cloud (VPC) as the Amazon EFS file system. - In the same Availability Zone as at least one mount target for the Amazon EFS file system. .. epigraph:: You don't need to specify a subnet that includes a file system mount target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                ec2_config_property = datasync.CfnLocationEFS.Ec2ConfigProperty(
                    security_group_arns=["securityGroupArns"],
                    subnet_arn="subnetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1db60c61de85615884ad364040e6c0ce7a82dd368a5227be71985cdb724453a1)
                check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
                check_type(argname="argument subnet_arn", value=subnet_arn, expected_type=type_hints["subnet_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "security_group_arns": security_group_arns,
                "subnet_arn": subnet_arn,
            }

        @builtins.property
        def security_group_arns(self) -> typing.List[builtins.str]:
            '''Specifies the Amazon Resource Names (ARNs) of the security groups associated with an Amazon EFS file system's mount target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html#cfn-datasync-locationefs-ec2config-securitygrouparns
            '''
            result = self._values.get("security_group_arns")
            assert result is not None, "Required property 'security_group_arns' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_arn(self) -> builtins.str:
            '''Specifies the ARN of a subnet where DataSync creates the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces>`_ for managing traffic during your transfer.

            The subnet must be located:

            - In the same virtual private cloud (VPC) as the Amazon EFS file system.
            - In the same Availability Zone as at least one mount target for the Amazon EFS file system.

            .. epigraph::

               You don't need to specify a subnet that includes a file system mount target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html#cfn-datasync-locationefs-ec2config-subnetarn
            '''
            result = self._values.get("subnet_arn")
            assert result is not None, "Required property 'subnet_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Ec2ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationEFSProps",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_config": "ec2Config",
        "access_point_arn": "accessPointArn",
        "efs_filesystem_arn": "efsFilesystemArn",
        "file_system_access_role_arn": "fileSystemAccessRoleArn",
        "in_transit_encryption": "inTransitEncryption",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationEFSProps:
    def __init__(
        self,
        *,
        ec2_config: typing.Union[typing.Union[CfnLocationEFS.Ec2ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        access_point_arn: typing.Optional[builtins.str] = None,
        efs_filesystem_arn: typing.Optional[builtins.str] = None,
        file_system_access_role_arn: typing.Optional[builtins.str] = None,
        in_transit_encryption: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationEFS``.

        :param ec2_config: Specifies the subnet and security groups DataSync uses to access your Amazon EFS file system.
        :param access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        :param efs_filesystem_arn: Specifies the ARN for the Amazon EFS file system.
        :param file_system_access_role_arn: Specifies an AWS Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        :param in_transit_encryption: Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it copies data to or from the Amazon EFS file system. If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .
        :param subdirectory: Specifies a mount path for your Amazon EFS file system. This is where DataSync reads or writes data (depending on if this is a source or destination location). By default, DataSync uses the root directory, but you can also include subdirectories. .. epigraph:: You must specify a value with forward slashes (for example, ``/path/to/folder`` ).
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_eFSProps = datasync.CfnLocationEFSProps(
                ec2_config=datasync.CfnLocationEFS.Ec2ConfigProperty(
                    security_group_arns=["securityGroupArns"],
                    subnet_arn="subnetArn"
                ),
            
                # the properties below are optional
                access_point_arn="accessPointArn",
                efs_filesystem_arn="efsFilesystemArn",
                file_system_access_role_arn="fileSystemAccessRoleArn",
                in_transit_encryption="inTransitEncryption",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed2e9e823f1b413430cee26b90b5675f99c28f45ff4121afdf9c69d002cb600)
            check_type(argname="argument ec2_config", value=ec2_config, expected_type=type_hints["ec2_config"])
            check_type(argname="argument access_point_arn", value=access_point_arn, expected_type=type_hints["access_point_arn"])
            check_type(argname="argument efs_filesystem_arn", value=efs_filesystem_arn, expected_type=type_hints["efs_filesystem_arn"])
            check_type(argname="argument file_system_access_role_arn", value=file_system_access_role_arn, expected_type=type_hints["file_system_access_role_arn"])
            check_type(argname="argument in_transit_encryption", value=in_transit_encryption, expected_type=type_hints["in_transit_encryption"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_config": ec2_config,
        }
        if access_point_arn is not None:
            self._values["access_point_arn"] = access_point_arn
        if efs_filesystem_arn is not None:
            self._values["efs_filesystem_arn"] = efs_filesystem_arn
        if file_system_access_role_arn is not None:
            self._values["file_system_access_role_arn"] = file_system_access_role_arn
        if in_transit_encryption is not None:
            self._values["in_transit_encryption"] = in_transit_encryption
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ec2_config(
        self,
    ) -> typing.Union[CfnLocationEFS.Ec2ConfigProperty, _IResolvable_a771d0ef]:
        '''Specifies the subnet and security groups DataSync uses to access your Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-ec2config
        '''
        result = self._values.get("ec2_config")
        assert result is not None, "Required property 'ec2_config' is missing"
        return typing.cast(typing.Union[CfnLocationEFS.Ec2ConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def access_point_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-accesspointarn
        '''
        result = self._values.get("access_point_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def efs_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN for the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-efsfilesystemarn
        '''
        result = self._values.get("efs_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies an AWS Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-filesystemaccessrolearn
        '''
        result = self._values.get("file_system_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_transit_encryption(self) -> typing.Optional[builtins.str]:
        '''Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it copies data to or from the Amazon EFS file system.

        If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-intransitencryption
        '''
        result = self._values.get("in_transit_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your Amazon EFS file system.

        This is where DataSync reads or writes data (depending on if this is a source or destination location). By default, DataSync uses the root directory, but you can also include subdirectories.
        .. epigraph::

           You must specify a value with forward slashes (for example, ``/path/to/folder`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationEFSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationFSxLustre(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationFSxLustre",
):
    '''A CloudFormation ``AWS::DataSync::LocationFSxLustre``.

    The ``AWS::DataSync::LocationFSxLustre`` resource specifies an endpoint for an Amazon FSx for Lustre file system.

    :cloudformationResource: AWS::DataSync::LocationFSxLustre
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_fSx_lustre = datasync.CfnLocationFSxLustre(self, "MyCfnLocationFSxLustre",
            security_group_arns=["securityGroupArns"],
        
            # the properties below are optional
            fsx_filesystem_arn="fsxFilesystemArn",
            subdirectory="subdirectory",
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
        security_group_arns: typing.Sequence[builtins.str],
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationFSxLustre``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for Lustre file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) for the FSx for Lustre file system.
        :param subdirectory: A subdirectory in the location's path. This subdirectory in the FSx for Lustre file system is used to read data from the FSx for Lustre source location or write data to the FSx for Lustre destination.
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd32d83f0c3b357d68a9f963e8a45f21075c64a0ab2e40e6196531d5d252ae87)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationFSxLustreProps(
            security_group_arns=security_group_arns,
            fsx_filesystem_arn=fsx_filesystem_arn,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c6c7b5beeff0929ad128a7f973a0a858e3b83a565920168a323ec0bec4b9b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28d8def9336950dd9eb5cbc2386481f66a0d2d9bbd8ae97bf224509e6528f10c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The ARN of the specified FSx for Lustre file system location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified FSx for Lustre file system location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the security groups that are used to configure the FSx for Lustre file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-securitygrouparns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59bfd375e78fc94425db568200ec70706da862bafb0e55ce2e757fb18ea7f4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the FSx for Lustre file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-fsxfilesystemarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsxFilesystemArn"))

    @fsx_filesystem_arn.setter
    def fsx_filesystem_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe59799dabf0ad2068f48001f36299770df58be45fc2155ea071b7445a9e471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsxFilesystemArn", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path.

        This subdirectory in the FSx for Lustre file system is used to read data from the FSx for Lustre source location or write data to the FSx for Lustre destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8658f048c47a9207d282569b549cdadb52d74cd861bd7ae476939f25ea93609a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationFSxLustreProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_arns": "securityGroupArns",
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxLustreProps:
    def __init__(
        self,
        *,
        security_group_arns: typing.Sequence[builtins.str],
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationFSxLustre``.

        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for Lustre file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) for the FSx for Lustre file system.
        :param subdirectory: A subdirectory in the location's path. This subdirectory in the FSx for Lustre file system is used to read data from the FSx for Lustre source location or write data to the FSx for Lustre destination.
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_fSx_lustre_props = datasync.CfnLocationFSxLustreProps(
                security_group_arns=["securityGroupArns"],
            
                # the properties below are optional
                fsx_filesystem_arn="fsxFilesystemArn",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792275b282f304487c5a4b06403a199ab68d38b462ec9f94741c1bfd9fa82155)
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_arns": security_group_arns,
        }
        if fsx_filesystem_arn is not None:
            self._values["fsx_filesystem_arn"] = fsx_filesystem_arn
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the security groups that are used to configure the FSx for Lustre file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        assert result is not None, "Required property 'security_group_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the FSx for Lustre file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path.

        This subdirectory in the FSx for Lustre file system is used to read data from the FSx for Lustre source location or write data to the FSx for Lustre destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxLustreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationFSxONTAP(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationFSxONTAP",
):
    '''A CloudFormation ``AWS::DataSync::LocationFSxONTAP``.

    The ``AWS::DataSync::LocationFSxONTAP`` resource creates an endpoint for an Amazon FSx for NetApp ONTAP file system. AWS DataSync can access this endpoint as a source or destination location.

    :cloudformationResource: AWS::DataSync::LocationFSxONTAP
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_fSx_oNTAP = datasync.CfnLocationFSxONTAP(self, "MyCfnLocationFSxONTAP",
            security_group_arns=["securityGroupArns"],
            storage_virtual_machine_arn="storageVirtualMachineArn",
        
            # the properties below are optional
            protocol=datasync.CfnLocationFSxONTAP.ProtocolProperty(
                nfs=datasync.CfnLocationFSxONTAP.NFSProperty(
                    mount_options=datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                        version="version"
                    )
                ),
                smb=datasync.CfnLocationFSxONTAP.SMBProperty(
                    mount_options=datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                        version="version"
                    ),
                    password="password",
                    user="user",
        
                    # the properties below are optional
                    domain="domain"
                )
            ),
            subdirectory="subdirectory",
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
        security_group_arns: typing.Sequence[builtins.str],
        storage_virtual_machine_arn: builtins.str,
        protocol: typing.Optional[typing.Union[typing.Union["CfnLocationFSxONTAP.ProtocolProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationFSxONTAP``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param security_group_arns: Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system. You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using): - *Network File System (NFS)* : TCP ports 111, 635, and 2049 - *Server Message Block (SMB)* : TCP port 445 Your file system's security groups must also allow inbound traffic on the same port.
        :param storage_virtual_machine_arn: Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.
        :param protocol: Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.
        :param subdirectory: Specifies a path to the file share in the SVM where you'll copy your data. You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` . .. epigraph:: Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c87647dd911c3e60e1a74bcab6e1dfdb8554bb842fea3f9b1c2305615d574f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationFSxONTAPProps(
            security_group_arns=security_group_arns,
            storage_virtual_machine_arn=storage_virtual_machine_arn,
            protocol=protocol,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e18edd30a179abaf9d3c41e38abbea11345de5e46f2bd5930f015d96c5aeeab7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acba653484180997668246fa72329c36723e18f8fe0533ea6b1f200176a8a52f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFsxFilesystemArn")
    def attr_fsx_filesystem_arn(self) -> builtins.str:
        '''The ARN of the FSx for ONTAP file system in the specified location.

        :cloudformationAttribute: FsxFilesystemArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFsxFilesystemArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The ARN of the specified location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system.

        You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using):

        - *Network File System (NFS)* : TCP ports 111, 635, and 2049
        - *Server Message Block (SMB)* : TCP port 445

        Your file system's security groups must also allow inbound traffic on the same port.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-securitygrouparns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b95aee6a95daee3c1284cd80c24423e751f2cd256c6b4d3091df71e2af93728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="storageVirtualMachineArn")
    def storage_virtual_machine_arn(self) -> builtins.str:
        '''Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-storagevirtualmachinearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "storageVirtualMachineArn"))

    @storage_virtual_machine_arn.setter
    def storage_virtual_machine_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71be64b1fa6e8590cba70c6190c0c0373b88d4ec729addafffc4ec2ef5e76eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageVirtualMachineArn", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(
        self,
    ) -> typing.Optional[typing.Union["CfnLocationFSxONTAP.ProtocolProperty", _IResolvable_a771d0ef]]:
        '''Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-protocol
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLocationFSxONTAP.ProtocolProperty", _IResolvable_a771d0ef]], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(
        self,
        value: typing.Optional[typing.Union["CfnLocationFSxONTAP.ProtocolProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a673de5207486b5cf52ce87c6880b61b5cc8c8f923e5d26d1eddb071d438be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a path to the file share in the SVM where you'll copy your data.

        You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` .
        .. epigraph::

           Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6005a208092b0b882059f89195765eee42f4a89f41ec18b1a9d3cb424d8f5b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationFSxONTAP.NFSProperty",
        jsii_struct_bases=[],
        name_mapping={"mount_options": "mountOptions"},
    )
    class NFSProperty:
        def __init__(
            self,
            *,
            mount_options: typing.Union[typing.Union["CfnLocationFSxONTAP.NfsMountOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Specifies the Network File System (NFS) protocol configuration that AWS DataSync uses to access a storage virtual machine (SVM) on your Amazon FSx for NetApp ONTAP file system.

            For more information, see `Accessing FSx for ONTAP file systems <https://docs.aws.amazon.com/datasync/latest/userguide/create-ontap-location.html#create-ontap-location-access>`_ .

            :param mount_options: Specifies how DataSync can access a location using the NFS protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                n_fSProperty = datasync.CfnLocationFSxONTAP.NFSProperty(
                    mount_options=datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__69421f575c92d98338eb8fb55467c9f226d5f0db895550ec04c2af1d47bdfc63)
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mount_options": mount_options,
            }

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Union["CfnLocationFSxONTAP.NfsMountOptionsProperty", _IResolvable_a771d0ef]:
            '''Specifies how DataSync can access a location using the NFS protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfs.html#cfn-datasync-locationfsxontap-nfs-mountoptions
            '''
            result = self._values.get("mount_options")
            assert result is not None, "Required property 'mount_options' is missing"
            return typing.cast(typing.Union["CfnLocationFSxONTAP.NfsMountOptionsProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NFSProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class NfsMountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies how DataSync can access a location using the NFS protocol.

            :param version: Specifies the NFS version that you want DataSync to use when mounting your NFS share. If the server refuses to use the version specified, the task fails. You can specify the following options: - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1. - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server. - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0. .. epigraph:: DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfsmountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                nfs_mount_options_property = datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb5373a064e61da2c55c153af08d4c6dec6ee9178d25765b02ae65cbc73501cc)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Specifies the NFS version that you want DataSync to use when mounting your NFS share.

            If the server refuses to use the version specified, the task fails.

            You can specify the following options:

            - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1.
            - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server.
            - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0.

            .. epigraph::

               DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfsmountoptions.html#cfn-datasync-locationfsxontap-nfsmountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NfsMountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationFSxONTAP.ProtocolProperty",
        jsii_struct_bases=[],
        name_mapping={"nfs": "nfs", "smb": "smb"},
    )
    class ProtocolProperty:
        def __init__(
            self,
            *,
            nfs: typing.Optional[typing.Union[typing.Union["CfnLocationFSxONTAP.NFSProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            smb: typing.Optional[typing.Union[typing.Union["CfnLocationFSxONTAP.SMBProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the data transfer protocol that AWS DataSync uses to access your Amazon FSx file system.

            :param nfs: Specifies the Network File System (NFS) protocol configuration that DataSync uses to access your FSx for ONTAP file system's storage virtual machine (SVM).
            :param smb: Specifies the Server Message Block (SMB) protocol configuration that DataSync uses to access your FSx for ONTAP file system's SVM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                protocol_property = datasync.CfnLocationFSxONTAP.ProtocolProperty(
                    nfs=datasync.CfnLocationFSxONTAP.NFSProperty(
                        mount_options=datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                            version="version"
                        )
                    ),
                    smb=datasync.CfnLocationFSxONTAP.SMBProperty(
                        mount_options=datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                            version="version"
                        ),
                        password="password",
                        user="user",
                
                        # the properties below are optional
                        domain="domain"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b0857b642acee602478ea1a63c3799bf12ae1581f0e197285ca7d321640557c)
                check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
                check_type(argname="argument smb", value=smb, expected_type=type_hints["smb"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nfs is not None:
                self._values["nfs"] = nfs
            if smb is not None:
                self._values["smb"] = smb

        @builtins.property
        def nfs(
            self,
        ) -> typing.Optional[typing.Union["CfnLocationFSxONTAP.NFSProperty", _IResolvable_a771d0ef]]:
            '''Specifies the Network File System (NFS) protocol configuration that DataSync uses to access your FSx for ONTAP file system's storage virtual machine (SVM).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html#cfn-datasync-locationfsxontap-protocol-nfs
            '''
            result = self._values.get("nfs")
            return typing.cast(typing.Optional[typing.Union["CfnLocationFSxONTAP.NFSProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def smb(
            self,
        ) -> typing.Optional[typing.Union["CfnLocationFSxONTAP.SMBProperty", _IResolvable_a771d0ef]]:
            '''Specifies the Server Message Block (SMB) protocol configuration that DataSync uses to access your FSx for ONTAP file system's SVM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html#cfn-datasync-locationfsxontap-protocol-smb
            '''
            result = self._values.get("smb")
            return typing.cast(typing.Optional[typing.Union["CfnLocationFSxONTAP.SMBProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationFSxONTAP.SMBProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mount_options": "mountOptions",
            "password": "password",
            "user": "user",
            "domain": "domain",
        },
    )
    class SMBProperty:
        def __init__(
            self,
            *,
            mount_options: typing.Union[typing.Union["CfnLocationFSxONTAP.SmbMountOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            password: builtins.str,
            user: builtins.str,
            domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Server Message Block (SMB) protocol configuration that AWS DataSync uses to access a storage virtual machine (SVM) on your Amazon FSx for NetApp ONTAP file system.

            For more information, see `Accessing FSx for ONTAP file systems <https://docs.aws.amazon.com/datasync/latest/userguide/create-ontap-location.html#create-ontap-location-access>`_ .

            :param mount_options: Specifies how DataSync can access a location using the SMB protocol.
            :param password: Specifies the password of a user who has permission to access your SVM.
            :param user: Specifies a user name that can mount the location and access the files, folders, and metadata that you need in the SVM. If you provide a user in your Active Directory, note the following: - If you're using AWS Directory Service for Microsoft Active Directory , the user must be a member of the AWS Delegated FSx Administrators group. - If you're using a self-managed Active Directory, the user must be a member of either the Domain Admins group or a custom group that you specified for file system administration when you created your file system. Make sure that the user has the permissions it needs to copy the data you want: - ``SE_TCB_NAME`` : Required to set object ownership and file metadata. With this privilege, you also can copy NTFS discretionary access lists (DACLs). - ``SE_SECURITY_NAME`` : May be needed to copy NTFS system access control lists (SACLs). This operation specifically requires the Windows privilege, which is granted to members of the Domain Admins group. If you configure your task to copy SACLs, make sure that the user has the required privileges. For information about copying SACLs, see `Ownership and permissions-related options <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html#configure-ownership-and-permissions>`_ .
            :param domain: Specifies the fully qualified domain name (FQDN) of the Microsoft Active Directory that your storage virtual machine (SVM) belongs to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                s_mBProperty = datasync.CfnLocationFSxONTAP.SMBProperty(
                    mount_options=datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                        version="version"
                    ),
                    password="password",
                    user="user",
                
                    # the properties below are optional
                    domain="domain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9be45210dbec0f4a494cbc2d958f8c1464c4fd85e40155f60dbde82bfcd7b2fa)
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
                check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mount_options": mount_options,
                "password": password,
                "user": user,
            }
            if domain is not None:
                self._values["domain"] = domain

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Union["CfnLocationFSxONTAP.SmbMountOptionsProperty", _IResolvable_a771d0ef]:
            '''Specifies how DataSync can access a location using the SMB protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-mountoptions
            '''
            result = self._values.get("mount_options")
            assert result is not None, "Required property 'mount_options' is missing"
            return typing.cast(typing.Union["CfnLocationFSxONTAP.SmbMountOptionsProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def password(self) -> builtins.str:
            '''Specifies the password of a user who has permission to access your SVM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user(self) -> builtins.str:
            '''Specifies a user name that can mount the location and access the files, folders, and metadata that you need in the SVM.

            If you provide a user in your Active Directory, note the following:

            - If you're using AWS Directory Service for Microsoft Active Directory , the user must be a member of the AWS Delegated FSx Administrators group.
            - If you're using a self-managed Active Directory, the user must be a member of either the Domain Admins group or a custom group that you specified for file system administration when you created your file system.

            Make sure that the user has the permissions it needs to copy the data you want:

            - ``SE_TCB_NAME`` : Required to set object ownership and file metadata. With this privilege, you also can copy NTFS discretionary access lists (DACLs).
            - ``SE_SECURITY_NAME`` : May be needed to copy NTFS system access control lists (SACLs). This operation specifically requires the Windows privilege, which is granted to members of the Domain Admins group. If you configure your task to copy SACLs, make sure that the user has the required privileges. For information about copying SACLs, see `Ownership and permissions-related options <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html#configure-ownership-and-permissions>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-user
            '''
            result = self._values.get("user")
            assert result is not None, "Required property 'user' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def domain(self) -> typing.Optional[builtins.str]:
            '''Specifies the fully qualified domain name (FQDN) of the Microsoft Active Directory that your storage virtual machine (SVM) belongs to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-domain
            '''
            result = self._values.get("domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SMBProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class SmbMountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the version of the Server Message Block (SMB) protocol that AWS DataSync uses to access an SMB file server.

            :param version: By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server. You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically. These are the following options for configuring the SMB version: - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate the highest version of SMB that they mutually support between 2.1 and 3.1.1. This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error. - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2. - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1. - ``SMB2_0`` : Restricts the protocol negotiation to only SMB version 2.0. - ``SMB1`` : Restricts the protocol negotiation to only SMB version 1.0. .. epigraph:: The ``SMB1`` option isn't available when `creating an Amazon FSx for NetApp ONTAP location <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateLocationFsxOntap.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smbmountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                smb_mount_options_property = datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09c40acf2ff035e2e8f122fdee9288ee483b4c6f45088e5101eee443a2e8114f)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server.

            You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically.

            These are the following options for configuring the SMB version:

            - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate the highest version of SMB that they mutually support between 2.1 and 3.1.1.

            This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error.

            - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2.
            - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1.
            - ``SMB2_0`` : Restricts the protocol negotiation to only SMB version 2.0.
            - ``SMB1`` : Restricts the protocol negotiation to only SMB version 1.0.

            .. epigraph::

               The ``SMB1`` option isn't available when `creating an Amazon FSx for NetApp ONTAP location <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateLocationFsxOntap.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smbmountoptions.html#cfn-datasync-locationfsxontap-smbmountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmbMountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationFSxONTAPProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_arns": "securityGroupArns",
        "storage_virtual_machine_arn": "storageVirtualMachineArn",
        "protocol": "protocol",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxONTAPProps:
    def __init__(
        self,
        *,
        security_group_arns: typing.Sequence[builtins.str],
        storage_virtual_machine_arn: builtins.str,
        protocol: typing.Optional[typing.Union[typing.Union[CfnLocationFSxONTAP.ProtocolProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationFSxONTAP``.

        :param security_group_arns: Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system. You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using): - *Network File System (NFS)* : TCP ports 111, 635, and 2049 - *Server Message Block (SMB)* : TCP port 445 Your file system's security groups must also allow inbound traffic on the same port.
        :param storage_virtual_machine_arn: Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.
        :param protocol: Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.
        :param subdirectory: Specifies a path to the file share in the SVM where you'll copy your data. You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` . .. epigraph:: Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_fSx_oNTAPProps = datasync.CfnLocationFSxONTAPProps(
                security_group_arns=["securityGroupArns"],
                storage_virtual_machine_arn="storageVirtualMachineArn",
            
                # the properties below are optional
                protocol=datasync.CfnLocationFSxONTAP.ProtocolProperty(
                    nfs=datasync.CfnLocationFSxONTAP.NFSProperty(
                        mount_options=datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                            version="version"
                        )
                    ),
                    smb=datasync.CfnLocationFSxONTAP.SMBProperty(
                        mount_options=datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                            version="version"
                        ),
                        password="password",
                        user="user",
            
                        # the properties below are optional
                        domain="domain"
                    )
                ),
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c4f29b9e1a05ef19d9873052161a00c3c2687d6a9aacbec31e076ba650f89c)
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument storage_virtual_machine_arn", value=storage_virtual_machine_arn, expected_type=type_hints["storage_virtual_machine_arn"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_arns": security_group_arns,
            "storage_virtual_machine_arn": storage_virtual_machine_arn,
        }
        if protocol is not None:
            self._values["protocol"] = protocol
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system.

        You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using):

        - *Network File System (NFS)* : TCP ports 111, 635, and 2049
        - *Server Message Block (SMB)* : TCP port 445

        Your file system's security groups must also allow inbound traffic on the same port.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        assert result is not None, "Required property 'security_group_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def storage_virtual_machine_arn(self) -> builtins.str:
        '''Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-storagevirtualmachinearn
        '''
        result = self._values.get("storage_virtual_machine_arn")
        assert result is not None, "Required property 'storage_virtual_machine_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[typing.Union[CfnLocationFSxONTAP.ProtocolProperty, _IResolvable_a771d0ef]]:
        '''Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[typing.Union[CfnLocationFSxONTAP.ProtocolProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a path to the file share in the SVM where you'll copy your data.

        You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` .
        .. epigraph::

           Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxONTAPProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationFSxOpenZFS(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationFSxOpenZFS",
):
    '''A CloudFormation ``AWS::DataSync::LocationFSxOpenZFS``.

    The ``AWS::DataSync::LocationFSxOpenZFS`` resource specifies an endpoint for an Amazon FSx for OpenZFS file system.

    :cloudformationResource: AWS::DataSync::LocationFSxOpenZFS
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_fSx_open_zFS = datasync.CfnLocationFSxOpenZFS(self, "MyCfnLocationFSxOpenZFS",
            protocol=datasync.CfnLocationFSxOpenZFS.ProtocolProperty(
                nfs=datasync.CfnLocationFSxOpenZFS.NFSProperty(
                    mount_options=datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                        version="version"
                    )
                )
            ),
            security_group_arns=["securityGroupArns"],
        
            # the properties below are optional
            fsx_filesystem_arn="fsxFilesystemArn",
            subdirectory="subdirectory",
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
        protocol: typing.Union[typing.Union["CfnLocationFSxOpenZFS.ProtocolProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        security_group_arns: typing.Sequence[builtins.str],
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationFSxOpenZFS``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param protocol: The type of protocol that AWS DataSync uses to access your file system.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for OpenZFS file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.
        :param subdirectory: A subdirectory in the location's path that must begin with ``/fsx`` . DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50927092fddbeca2a5071f8416224612501feb5a2839215d5a1359b7019eeae5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationFSxOpenZFSProps(
            protocol=protocol,
            security_group_arns=security_group_arns,
            fsx_filesystem_arn=fsx_filesystem_arn,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73678c93e26d3b543c63bb000267f1374699faac6a88e474a79dd56ca30c7992)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6dff8cec29c326569ac68c2a3281bc54416bf6713569b4df7dc78c2dc0eea45)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The ARN of the specified FSx for OpenZFS file system location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified FSx for OpenZFS file system location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(
        self,
    ) -> typing.Union["CfnLocationFSxOpenZFS.ProtocolProperty", _IResolvable_a771d0ef]:
        '''The type of protocol that AWS DataSync uses to access your file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-protocol
        '''
        return typing.cast(typing.Union["CfnLocationFSxOpenZFS.ProtocolProperty", _IResolvable_a771d0ef], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(
        self,
        value: typing.Union["CfnLocationFSxOpenZFS.ProtocolProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08861b23aa64937ddb506fdf3ae6c77efb03578bffd65c7a88d3f0e872c51210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the security groups that are used to configure the FSx for OpenZFS file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-securitygrouparns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434f123f3cc99d3e11a864de10add1c62f723eb7026130785a4028bb83a5f47c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-fsxfilesystemarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsxFilesystemArn"))

    @fsx_filesystem_arn.setter
    def fsx_filesystem_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c310c478a6c1389ca2127db9404c753fc0b9c9f1a38ac7558510f6f0ec6bd379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsxFilesystemArn", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path that must begin with ``/fsx`` .

        DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702768cbd42a27cc1ca27b968c43405883cc9bf5a7b6950b4314eb3fa2bf4bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationFSxOpenZFS.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Represents the mount options that are available for DataSync to access a Network File System (NFS) location.

            :param version: The specific NFS version that you want DataSync to use to mount your NFS share. If the server refuses to use the version specified, the sync will fail. If you don't specify a version, DataSync defaults to ``AUTOMATIC`` . That is, DataSync automatically selects a version based on negotiation with the NFS server. You can specify the following NFS versions: - *`NFSv3 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc1813>`_* : Stateless protocol version that allows for asynchronous writes on the server. - *`NFSv4.0 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3530>`_* : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - *`NFSv4.1 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5661>`_* : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. Version 4.1 also includes all features available in version 4.0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                mount_options_property = datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__075207572b6e79a5e25670a0322d63430f8846efb423875489b22d6c21c6d36b)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The specific NFS version that you want DataSync to use to mount your NFS share.

            If the server refuses to use the version specified, the sync will fail. If you don't specify a version, DataSync defaults to ``AUTOMATIC`` . That is, DataSync automatically selects a version based on negotiation with the NFS server.

            You can specify the following NFS versions:

            - *`NFSv3 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc1813>`_* : Stateless protocol version that allows for asynchronous writes on the server.
            - *`NFSv4.0 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3530>`_* : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - *`NFSv4.1 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5661>`_* : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. Version 4.1 also includes all features available in version 4.0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-mountoptions.html#cfn-datasync-locationfsxopenzfs-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationFSxOpenZFS.NFSProperty",
        jsii_struct_bases=[],
        name_mapping={"mount_options": "mountOptions"},
    )
    class NFSProperty:
        def __init__(
            self,
            *,
            mount_options: typing.Union[typing.Union["CfnLocationFSxOpenZFS.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Represents the Network File System (NFS) protocol that AWS DataSync uses to access your Amazon FSx for OpenZFS file system.

            :param mount_options: Represents the mount options that are available for DataSync to access an NFS location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-nfs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                n_fSProperty = datasync.CfnLocationFSxOpenZFS.NFSProperty(
                    mount_options=datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80577da58ebbe623c2037b3094ca2863d31f6029ecf9eaded51b58d7953c5a97)
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mount_options": mount_options,
            }

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Union["CfnLocationFSxOpenZFS.MountOptionsProperty", _IResolvable_a771d0ef]:
            '''Represents the mount options that are available for DataSync to access an NFS location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-nfs.html#cfn-datasync-locationfsxopenzfs-nfs-mountoptions
            '''
            result = self._values.get("mount_options")
            assert result is not None, "Required property 'mount_options' is missing"
            return typing.cast(typing.Union["CfnLocationFSxOpenZFS.MountOptionsProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NFSProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationFSxOpenZFS.ProtocolProperty",
        jsii_struct_bases=[],
        name_mapping={"nfs": "nfs"},
    )
    class ProtocolProperty:
        def __init__(
            self,
            *,
            nfs: typing.Optional[typing.Union[typing.Union["CfnLocationFSxOpenZFS.NFSProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Represents the protocol that AWS DataSync uses to access your Amazon FSx for OpenZFS file system.

            :param nfs: Represents the Network File System (NFS) protocol that DataSync uses to access your FSx for OpenZFS file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-protocol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                protocol_property = datasync.CfnLocationFSxOpenZFS.ProtocolProperty(
                    nfs=datasync.CfnLocationFSxOpenZFS.NFSProperty(
                        mount_options=datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                            version="version"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__021d831c2a3e37b25d4300be9f4bf657d230cdc873806952db54ef7e6e2d2e88)
                check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nfs is not None:
                self._values["nfs"] = nfs

        @builtins.property
        def nfs(
            self,
        ) -> typing.Optional[typing.Union["CfnLocationFSxOpenZFS.NFSProperty", _IResolvable_a771d0ef]]:
            '''Represents the Network File System (NFS) protocol that DataSync uses to access your FSx for OpenZFS file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-protocol.html#cfn-datasync-locationfsxopenzfs-protocol-nfs
            '''
            result = self._values.get("nfs")
            return typing.cast(typing.Optional[typing.Union["CfnLocationFSxOpenZFS.NFSProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationFSxOpenZFSProps",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "security_group_arns": "securityGroupArns",
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxOpenZFSProps:
    def __init__(
        self,
        *,
        protocol: typing.Union[typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        security_group_arns: typing.Sequence[builtins.str],
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationFSxOpenZFS``.

        :param protocol: The type of protocol that AWS DataSync uses to access your file system.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for OpenZFS file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.
        :param subdirectory: A subdirectory in the location's path that must begin with ``/fsx`` . DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_fSx_open_zFSProps = datasync.CfnLocationFSxOpenZFSProps(
                protocol=datasync.CfnLocationFSxOpenZFS.ProtocolProperty(
                    nfs=datasync.CfnLocationFSxOpenZFS.NFSProperty(
                        mount_options=datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                            version="version"
                        )
                    )
                ),
                security_group_arns=["securityGroupArns"],
            
                # the properties below are optional
                fsx_filesystem_arn="fsxFilesystemArn",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55f455d7c9c6fac0041c26256fb0c102fb58ac3daf594ccd68f263f5eedf0e3)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "protocol": protocol,
            "security_group_arns": security_group_arns,
        }
        if fsx_filesystem_arn is not None:
            self._values["fsx_filesystem_arn"] = fsx_filesystem_arn
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def protocol(
        self,
    ) -> typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, _IResolvable_a771d0ef]:
        '''The type of protocol that AWS DataSync uses to access your file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the security groups that are used to configure the FSx for OpenZFS file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        assert result is not None, "Required property 'security_group_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path that must begin with ``/fsx`` .

        DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxOpenZFSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationFSxWindows(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationFSxWindows",
):
    '''A CloudFormation ``AWS::DataSync::LocationFSxWindows``.

    The ``AWS::DataSync::LocationFSxWindows`` resource specifies an endpoint for an Amazon FSx for Windows Server file system.

    :cloudformationResource: AWS::DataSync::LocationFSxWindows
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_fSx_windows = datasync.CfnLocationFSxWindows(self, "MyCfnLocationFSxWindows",
            security_group_arns=["securityGroupArns"],
            user="user",
        
            # the properties below are optional
            domain="domain",
            fsx_filesystem_arn="fsxFilesystemArn",
            password="password",
            subdirectory="subdirectory",
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
        security_group_arns: typing.Sequence[builtins.str],
        user: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationFSxWindows``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param user: The user who has the permissions to access files and folders in the FSx for Windows File Server file system. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .
        :param domain: Specifies the name of the Windows domain that the FSx for Windows File Server belongs to.
        :param fsx_filesystem_arn: Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.
        :param password: Specifies the password of the user who has the permissions to access files and folders in the file system.
        :param subdirectory: Specifies a mount path for your file system using forward slashes. This is where DataSync reads or writes data (depending on if this is a source or destination location).
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3424d14fff59929204f383f9349cf1fae31500d32c77138b1a7c64bd46b25f5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationFSxWindowsProps(
            security_group_arns=security_group_arns,
            user=user,
            domain=domain,
            fsx_filesystem_arn=fsx_filesystem_arn,
            password=password,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2849e2934f4dd441e4864a825c17682fa1ebf1c23fc46bf46e67d164c0ae7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c75a9d3503e984248f3b76356fc7806ab3d4c1b72ed69fba0ea877efa6dd83c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The ARN of the specified FSx for Windows Server file system location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified FSx for Windows Server file system location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-securitygrouparns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ab167b6a2695f33ce496d3f0d76b5d16316c5583c24b0f4cd4860b179ee71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        '''The user who has the permissions to access files and folders in the FSx for Windows File Server file system.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-user
        '''
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a6debb870153f415685fa350adfed0b505df5cfc5ed7857ddb383698ac98bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the Windows domain that the FSx for Windows File Server belongs to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-domain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abbb58aa2260ccdd250a7aaca5a31ba4d06af58a24e280310c47dbb6184c95e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-fsxfilesystemarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsxFilesystemArn"))

    @fsx_filesystem_arn.setter
    def fsx_filesystem_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0509fa1e7c1076fe0e2030a27933b61ab7b897e814568d9e985f8708d552168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsxFilesystemArn", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        '''Specifies the password of the user who has the permissions to access files and folders in the file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-password
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1e2f82232bc9708abed64ef186170dc3867d2bd45bb3962cf689ee1933369a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your file system using forward slashes.

        This is where DataSync reads or writes data (depending on if this is a source or destination location).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79536f03b7b73a6b1464bc6e9348c45514f39cde7ca46bd9e06570e41066142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationFSxWindowsProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_arns": "securityGroupArns",
        "user": "user",
        "domain": "domain",
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "password": "password",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxWindowsProps:
    def __init__(
        self,
        *,
        security_group_arns: typing.Sequence[builtins.str],
        user: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        fsx_filesystem_arn: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationFSxWindows``.

        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param user: The user who has the permissions to access files and folders in the FSx for Windows File Server file system. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .
        :param domain: Specifies the name of the Windows domain that the FSx for Windows File Server belongs to.
        :param fsx_filesystem_arn: Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.
        :param password: Specifies the password of the user who has the permissions to access files and folders in the file system.
        :param subdirectory: Specifies a mount path for your file system using forward slashes. This is where DataSync reads or writes data (depending on if this is a source or destination location).
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_fSx_windows_props = datasync.CfnLocationFSxWindowsProps(
                security_group_arns=["securityGroupArns"],
                user="user",
            
                # the properties below are optional
                domain="domain",
                fsx_filesystem_arn="fsxFilesystemArn",
                password="password",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3e427b916c9e05c492d78b4aba687d24efe4193c99bd5592a4e19dc25988c2)
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_arns": security_group_arns,
            "user": user,
        }
        if domain is not None:
            self._values["domain"] = domain
        if fsx_filesystem_arn is not None:
            self._values["fsx_filesystem_arn"] = fsx_filesystem_arn
        if password is not None:
            self._values["password"] = password
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        assert result is not None, "Required property 'security_group_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def user(self) -> builtins.str:
        '''The user who has the permissions to access files and folders in the FSx for Windows File Server file system.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-user
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the Windows domain that the FSx for Windows File Server belongs to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fsx_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Specifies the password of the user who has the permissions to access files and folders in the file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your file system using forward slashes.

        This is where DataSync reads or writes data (depending on if this is a source or destination location).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxWindowsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationHDFS(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationHDFS",
):
    '''A CloudFormation ``AWS::DataSync::LocationHDFS``.

    The ``AWS::DataSync::LocationHDFS`` resource specifies an endpoint for a Hadoop Distributed File System (HDFS).

    :cloudformationResource: AWS::DataSync::LocationHDFS
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_hDFS = datasync.CfnLocationHDFS(self, "MyCfnLocationHDFS",
            agent_arns=["agentArns"],
            authentication_type="authenticationType",
            name_nodes=[datasync.CfnLocationHDFS.NameNodeProperty(
                hostname="hostname",
                port=123
            )],
        
            # the properties below are optional
            block_size=123,
            kerberos_keytab="kerberosKeytab",
            kerberos_krb5_conf="kerberosKrb5Conf",
            kerberos_principal="kerberosPrincipal",
            kms_key_provider_uri="kmsKeyProviderUri",
            qop_configuration=datasync.CfnLocationHDFS.QopConfigurationProperty(
                data_transfer_protection="dataTransferProtection",
                rpc_protection="rpcProtection"
            ),
            replication_factor=123,
            simple_user="simpleUser",
            subdirectory="subdirectory",
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
        agent_arns: typing.Sequence[builtins.str],
        authentication_type: builtins.str,
        name_nodes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLocationHDFS.NameNodeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        block_size: typing.Optional[jsii.Number] = None,
        kerberos_keytab: typing.Optional[builtins.str] = None,
        kerberos_krb5_conf: typing.Optional[builtins.str] = None,
        kerberos_principal: typing.Optional[builtins.str] = None,
        kms_key_provider_uri: typing.Optional[builtins.str] = None,
        qop_configuration: typing.Optional[typing.Union[typing.Union["CfnLocationHDFS.QopConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
        simple_user: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationHDFS``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param agent_arns: The Amazon Resource Names (ARNs) of the agents that are used to connect to the HDFS cluster.
        :param authentication_type: ``AWS::DataSync::LocationHDFS.AuthenticationType``.
        :param name_nodes: The NameNode that manages the HDFS namespace. The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.
        :param block_size: The size of data blocks to write into the HDFS cluster. The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).
        :param kerberos_keytab: The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys. Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_krb5_conf: The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_principal: The Kerberos principal with access to the files and folders on the HDFS cluster. .. epigraph:: If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.
        :param kms_key_provider_uri: The URI of the HDFS cluster's Key Management Server (KMS).
        :param qop_configuration: The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster. If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.
        :param replication_factor: The number of DataNodes to replicate the data to when writing to the HDFS cluster. By default, data is replicated to three DataNodes.
        :param simple_user: The user name used to identify the client on the host operating system. .. epigraph:: If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.
        :param subdirectory: A subdirectory in the HDFS cluster. This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f6ef4bb0c9ae5bc8d6f3333813a7bcbb069baf62dc17574d39818bd30e8d2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationHDFSProps(
            agent_arns=agent_arns,
            authentication_type=authentication_type,
            name_nodes=name_nodes,
            block_size=block_size,
            kerberos_keytab=kerberos_keytab,
            kerberos_krb5_conf=kerberos_krb5_conf,
            kerberos_principal=kerberos_principal,
            kms_key_provider_uri=kms_key_provider_uri,
            qop_configuration=qop_configuration,
            replication_factor=replication_factor,
            simple_user=simple_user,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b4a49830a9c24375890fec0bab0309c39044d689e43dec9fa2aaf2767c0b54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc001038d0023cc64db49f6bd5aba445766be60a409e6dad449f7da8c022705f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the HDFS cluster location to describe.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the HDFS cluster location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentArns")
    def agent_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the agents that are used to connect to the HDFS cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-agentarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "agentArns"))

    @agent_arns.setter
    def agent_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168b5df29b93b8ebefdbcbfc7e7fbf03ca05a884c385897828925c7a47c018f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentArns", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        '''``AWS::DataSync::LocationHDFS.AuthenticationType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-authenticationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079801bcd8ef86ba2ab9121c13a4487e69a9c4ef80a719cfc03cda267141fcc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value)

    @builtins.property
    @jsii.member(jsii_name="nameNodes")
    def name_nodes(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLocationHDFS.NameNodeProperty", _IResolvable_a771d0ef]]]:
        '''The NameNode that manages the HDFS namespace.

        The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-namenodes
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLocationHDFS.NameNodeProperty", _IResolvable_a771d0ef]]], jsii.get(self, "nameNodes"))

    @name_nodes.setter
    def name_nodes(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLocationHDFS.NameNodeProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7949f1beae555a53a14c60cd4457784030b81c85815059c84c8946fd6433f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameNodes", value)

    @builtins.property
    @jsii.member(jsii_name="blockSize")
    def block_size(self) -> typing.Optional[jsii.Number]:
        '''The size of data blocks to write into the HDFS cluster.

        The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-blocksize
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "blockSize"))

    @block_size.setter
    def block_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1ad140fc1986c2663b401a9eb570e6dd303372d8a5c03471a9e70e81c953fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockSize", value)

    @builtins.property
    @jsii.member(jsii_name="kerberosKeytab")
    def kerberos_keytab(self) -> typing.Optional[builtins.str]:
        '''The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys.

        Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskeytab
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kerberosKeytab"))

    @kerberos_keytab.setter
    def kerberos_keytab(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2701788ca3c169873a5308f4af822a3cf92f504692b64d6452f51f0299004ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosKeytab", value)

    @builtins.property
    @jsii.member(jsii_name="kerberosKrb5Conf")
    def kerberos_krb5_conf(self) -> typing.Optional[builtins.str]:
        '''The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskrb5conf
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kerberosKrb5Conf"))

    @kerberos_krb5_conf.setter
    def kerberos_krb5_conf(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a6652087b4316c978bee37603c2100d95cdc57a53112ce5e7132c7f672170b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosKrb5Conf", value)

    @builtins.property
    @jsii.member(jsii_name="kerberosPrincipal")
    def kerberos_principal(self) -> typing.Optional[builtins.str]:
        '''The Kerberos principal with access to the files and folders on the HDFS cluster.

        .. epigraph::

           If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberosprincipal
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kerberosPrincipal"))

    @kerberos_principal.setter
    def kerberos_principal(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1ac3eed258aab9a691ee3d4f143678ee679fc95810436d29d566eb784af0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosPrincipal", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyProviderUri")
    def kms_key_provider_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the HDFS cluster's Key Management Server (KMS).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kmskeyprovideruri
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyProviderUri"))

    @kms_key_provider_uri.setter
    def kms_key_provider_uri(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284429aa3d6990a514e681fc7e188755e3966353968563db5a57631a151dc4d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyProviderUri", value)

    @builtins.property
    @jsii.member(jsii_name="qopConfiguration")
    def qop_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnLocationHDFS.QopConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster.

        If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-qopconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLocationHDFS.QopConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "qopConfiguration"))

    @qop_configuration.setter
    def qop_configuration(
        self,
        value: typing.Optional[typing.Union["CfnLocationHDFS.QopConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09eaeddd6540f54252618401b33394208316430f1b909037e4006982c4ad9dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qopConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="replicationFactor")
    def replication_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of DataNodes to replicate the data to when writing to the HDFS cluster.

        By default, data is replicated to three DataNodes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-replicationfactor
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicationFactor"))

    @replication_factor.setter
    def replication_factor(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae43ff2ca2772f30172d0d2c4dcd2149fd5062c94912c36fd4d78824c7779c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationFactor", value)

    @builtins.property
    @jsii.member(jsii_name="simpleUser")
    def simple_user(self) -> typing.Optional[builtins.str]:
        '''The user name used to identify the client on the host operating system.

        .. epigraph::

           If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-simpleuser
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "simpleUser"))

    @simple_user.setter
    def simple_user(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d5bce832d5ce55eaba558357da33dcb5a13280da8f1515f4732407161d8192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simpleUser", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the HDFS cluster.

        This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f06762d92688779b6ef9fa1406765e978919d1f82c1df21fdee241134f6ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationHDFS.NameNodeProperty",
        jsii_struct_bases=[],
        name_mapping={"hostname": "hostname", "port": "port"},
    )
    class NameNodeProperty:
        def __init__(self, *, hostname: builtins.str, port: jsii.Number) -> None:
            '''The NameNode of the Hadoop Distributed File System (HDFS).

            The NameNode manages the file system's namespace and performs operations such as opening, closing, and renaming files and directories. The NameNode also contains the information to map blocks of data to the DataNodes.

            :param hostname: The hostname of the NameNode in the HDFS cluster. This value is the IP address or Domain Name Service (DNS) name of the NameNode. An agent that's installed on-premises uses this hostname to communicate with the NameNode in the network.
            :param port: The port that the NameNode uses to listen to client requests.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                name_node_property = datasync.CfnLocationHDFS.NameNodeProperty(
                    hostname="hostname",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33b0b45b2c07b77c7ed970ce045db04168be953509519c8b10e71519cfff27be)
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hostname": hostname,
                "port": port,
            }

        @builtins.property
        def hostname(self) -> builtins.str:
            '''The hostname of the NameNode in the HDFS cluster.

            This value is the IP address or Domain Name Service (DNS) name of the NameNode. An agent that's installed on-premises uses this hostname to communicate with the NameNode in the network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html#cfn-datasync-locationhdfs-namenode-hostname
            '''
            result = self._values.get("hostname")
            assert result is not None, "Required property 'hostname' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def port(self) -> jsii.Number:
            '''The port that the NameNode uses to listen to client requests.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html#cfn-datasync-locationhdfs-namenode-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NameNodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationHDFS.QopConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_transfer_protection": "dataTransferProtection",
            "rpc_protection": "rpcProtection",
        },
    )
    class QopConfigurationProperty:
        def __init__(
            self,
            *,
            data_transfer_protection: typing.Optional[builtins.str] = None,
            rpc_protection: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer privacy settings configured on the Hadoop Distributed File System (HDFS) cluster.

            :param data_transfer_protection: The data transfer protection setting configured on the HDFS cluster. This setting corresponds to your ``dfs.data.transfer.protection`` setting in the ``hdfs-site.xml`` file on your Hadoop cluster.
            :param rpc_protection: The Remote Procedure Call (RPC) protection setting configured on the HDFS cluster. This setting corresponds to your ``hadoop.rpc.protection`` setting in your ``core-site.xml`` file on your Hadoop cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                qop_configuration_property = datasync.CfnLocationHDFS.QopConfigurationProperty(
                    data_transfer_protection="dataTransferProtection",
                    rpc_protection="rpcProtection"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__552100dcbe7592582e84a98af9b6b62f7488119783bf6b166029d05eb7efb255)
                check_type(argname="argument data_transfer_protection", value=data_transfer_protection, expected_type=type_hints["data_transfer_protection"])
                check_type(argname="argument rpc_protection", value=rpc_protection, expected_type=type_hints["rpc_protection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_transfer_protection is not None:
                self._values["data_transfer_protection"] = data_transfer_protection
            if rpc_protection is not None:
                self._values["rpc_protection"] = rpc_protection

        @builtins.property
        def data_transfer_protection(self) -> typing.Optional[builtins.str]:
            '''The data transfer protection setting configured on the HDFS cluster.

            This setting corresponds to your ``dfs.data.transfer.protection`` setting in the ``hdfs-site.xml`` file on your Hadoop cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html#cfn-datasync-locationhdfs-qopconfiguration-datatransferprotection
            '''
            result = self._values.get("data_transfer_protection")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rpc_protection(self) -> typing.Optional[builtins.str]:
            '''The Remote Procedure Call (RPC) protection setting configured on the HDFS cluster.

            This setting corresponds to your ``hadoop.rpc.protection`` setting in your ``core-site.xml`` file on your Hadoop cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html#cfn-datasync-locationhdfs-qopconfiguration-rpcprotection
            '''
            result = self._values.get("rpc_protection")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QopConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationHDFSProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "authentication_type": "authenticationType",
        "name_nodes": "nameNodes",
        "block_size": "blockSize",
        "kerberos_keytab": "kerberosKeytab",
        "kerberos_krb5_conf": "kerberosKrb5Conf",
        "kerberos_principal": "kerberosPrincipal",
        "kms_key_provider_uri": "kmsKeyProviderUri",
        "qop_configuration": "qopConfiguration",
        "replication_factor": "replicationFactor",
        "simple_user": "simpleUser",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationHDFSProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Sequence[builtins.str],
        authentication_type: builtins.str,
        name_nodes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLocationHDFS.NameNodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        block_size: typing.Optional[jsii.Number] = None,
        kerberos_keytab: typing.Optional[builtins.str] = None,
        kerberos_krb5_conf: typing.Optional[builtins.str] = None,
        kerberos_principal: typing.Optional[builtins.str] = None,
        kms_key_provider_uri: typing.Optional[builtins.str] = None,
        qop_configuration: typing.Optional[typing.Union[typing.Union[CfnLocationHDFS.QopConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
        simple_user: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationHDFS``.

        :param agent_arns: The Amazon Resource Names (ARNs) of the agents that are used to connect to the HDFS cluster.
        :param authentication_type: ``AWS::DataSync::LocationHDFS.AuthenticationType``.
        :param name_nodes: The NameNode that manages the HDFS namespace. The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.
        :param block_size: The size of data blocks to write into the HDFS cluster. The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).
        :param kerberos_keytab: The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys. Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_krb5_conf: The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_principal: The Kerberos principal with access to the files and folders on the HDFS cluster. .. epigraph:: If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.
        :param kms_key_provider_uri: The URI of the HDFS cluster's Key Management Server (KMS).
        :param qop_configuration: The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster. If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.
        :param replication_factor: The number of DataNodes to replicate the data to when writing to the HDFS cluster. By default, data is replicated to three DataNodes.
        :param simple_user: The user name used to identify the client on the host operating system. .. epigraph:: If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.
        :param subdirectory: A subdirectory in the HDFS cluster. This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_hDFSProps = datasync.CfnLocationHDFSProps(
                agent_arns=["agentArns"],
                authentication_type="authenticationType",
                name_nodes=[datasync.CfnLocationHDFS.NameNodeProperty(
                    hostname="hostname",
                    port=123
                )],
            
                # the properties below are optional
                block_size=123,
                kerberos_keytab="kerberosKeytab",
                kerberos_krb5_conf="kerberosKrb5Conf",
                kerberos_principal="kerberosPrincipal",
                kms_key_provider_uri="kmsKeyProviderUri",
                qop_configuration=datasync.CfnLocationHDFS.QopConfigurationProperty(
                    data_transfer_protection="dataTransferProtection",
                    rpc_protection="rpcProtection"
                ),
                replication_factor=123,
                simple_user="simpleUser",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99584bc996b49aecfca6efbc3eb837f0530fa9e260a9cb573acee398b52b8fc)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument name_nodes", value=name_nodes, expected_type=type_hints["name_nodes"])
            check_type(argname="argument block_size", value=block_size, expected_type=type_hints["block_size"])
            check_type(argname="argument kerberos_keytab", value=kerberos_keytab, expected_type=type_hints["kerberos_keytab"])
            check_type(argname="argument kerberos_krb5_conf", value=kerberos_krb5_conf, expected_type=type_hints["kerberos_krb5_conf"])
            check_type(argname="argument kerberos_principal", value=kerberos_principal, expected_type=type_hints["kerberos_principal"])
            check_type(argname="argument kms_key_provider_uri", value=kms_key_provider_uri, expected_type=type_hints["kms_key_provider_uri"])
            check_type(argname="argument qop_configuration", value=qop_configuration, expected_type=type_hints["qop_configuration"])
            check_type(argname="argument replication_factor", value=replication_factor, expected_type=type_hints["replication_factor"])
            check_type(argname="argument simple_user", value=simple_user, expected_type=type_hints["simple_user"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_arns": agent_arns,
            "authentication_type": authentication_type,
            "name_nodes": name_nodes,
        }
        if block_size is not None:
            self._values["block_size"] = block_size
        if kerberos_keytab is not None:
            self._values["kerberos_keytab"] = kerberos_keytab
        if kerberos_krb5_conf is not None:
            self._values["kerberos_krb5_conf"] = kerberos_krb5_conf
        if kerberos_principal is not None:
            self._values["kerberos_principal"] = kerberos_principal
        if kms_key_provider_uri is not None:
            self._values["kms_key_provider_uri"] = kms_key_provider_uri
        if qop_configuration is not None:
            self._values["qop_configuration"] = qop_configuration
        if replication_factor is not None:
            self._values["replication_factor"] = replication_factor
        if simple_user is not None:
            self._values["simple_user"] = simple_user
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the agents that are used to connect to the HDFS cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-agentarns
        '''
        result = self._values.get("agent_arns")
        assert result is not None, "Required property 'agent_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''``AWS::DataSync::LocationHDFS.AuthenticationType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-authenticationtype
        '''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_nodes(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLocationHDFS.NameNodeProperty, _IResolvable_a771d0ef]]]:
        '''The NameNode that manages the HDFS namespace.

        The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-namenodes
        '''
        result = self._values.get("name_nodes")
        assert result is not None, "Required property 'name_nodes' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLocationHDFS.NameNodeProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def block_size(self) -> typing.Optional[jsii.Number]:
        '''The size of data blocks to write into the HDFS cluster.

        The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-blocksize
        '''
        result = self._values.get("block_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kerberos_keytab(self) -> typing.Optional[builtins.str]:
        '''The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys.

        Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskeytab
        '''
        result = self._values.get("kerberos_keytab")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_krb5_conf(self) -> typing.Optional[builtins.str]:
        '''The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskrb5conf
        '''
        result = self._values.get("kerberos_krb5_conf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_principal(self) -> typing.Optional[builtins.str]:
        '''The Kerberos principal with access to the files and folders on the HDFS cluster.

        .. epigraph::

           If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberosprincipal
        '''
        result = self._values.get("kerberos_principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_provider_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the HDFS cluster's Key Management Server (KMS).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kmskeyprovideruri
        '''
        result = self._values.get("kms_key_provider_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qop_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnLocationHDFS.QopConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster.

        If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-qopconfiguration
        '''
        result = self._values.get("qop_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnLocationHDFS.QopConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def replication_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of DataNodes to replicate the data to when writing to the HDFS cluster.

        By default, data is replicated to three DataNodes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-replicationfactor
        '''
        result = self._values.get("replication_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def simple_user(self) -> typing.Optional[builtins.str]:
        '''The user name used to identify the client on the host operating system.

        .. epigraph::

           If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-simpleuser
        '''
        result = self._values.get("simple_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the HDFS cluster.

        This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationHDFSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationNFS(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationNFS",
):
    '''A CloudFormation ``AWS::DataSync::LocationNFS``.

    The ``AWS::DataSync::LocationNFS`` resource specifies a file system on a Network File System (NFS) server that can be read from or written to.

    :cloudformationResource: AWS::DataSync::LocationNFS
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_nFS = datasync.CfnLocationNFS(self, "MyCfnLocationNFS",
            on_prem_config=datasync.CfnLocationNFS.OnPremConfigProperty(
                agent_arns=["agentArns"]
            ),
        
            # the properties below are optional
            mount_options=datasync.CfnLocationNFS.MountOptionsProperty(
                version="version"
            ),
            server_hostname="serverHostname",
            subdirectory="subdirectory",
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
        on_prem_config: typing.Union[typing.Union["CfnLocationNFS.OnPremConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        mount_options: typing.Optional[typing.Union[typing.Union["CfnLocationNFS.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationNFS``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param on_prem_config: Contains a list of Amazon Resource Names (ARNs) of agents that are used to connect to an NFS server. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.
        :param mount_options: The NFS mount options that DataSync can use to mount your NFS share.
        :param server_hostname: The name of the NFS server. This value is the IP address or Domain Name Service (DNS) name of the NFS server. An agent that is installed on-premises uses this hostname to mount the NFS server in a network. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information. .. epigraph:: This name must either be DNS-compliant or must be an IP version 4 (IPv4) address.
        :param subdirectory: The subdirectory in the NFS file system that is used to read data from the NFS source location or write data to the NFS destination. The NFS path should be a path that's exported by the NFS server, or a subdirectory of that path. The path should be such that it can be mounted by other NFS clients in your network. To see all the paths exported by your NFS server, run " ``showmount -e nfs-server-name`` " from an NFS client that has access to your server. You can specify any directory that appears in the results, and any subdirectory of that directory. Ensure that the NFS export is accessible without Kerberos authentication. To transfer all the data in the folder you specified, DataSync needs to have permissions to read all the data. To ensure this, either configure the NFS export with ``no_root_squash,`` or ensure that the permissions for all of the files that you want DataSync allow read access for all users. Doing either enables the agent to read the files. For the agent to access directories, you must additionally enable all execute access. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information. For information about NFS export configuration, see `18.7. The /etc/exports Configuration File <https://docs.aws.amazon.com/http://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-nfs-server-config-exports.html>`_ in the Red Hat Enterprise Linux documentation.
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edfa9018ee3004925e3bae4da711868f2593454f177d933365112d06b2036653)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationNFSProps(
            on_prem_config=on_prem_config,
            mount_options=mount_options,
            server_hostname=server_hostname,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a367ea4303fd5de5b7024de97b254527490287e0bd010a1f9a3321a75910264)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71f6f39d0fe7ff37baa70fd740189b4019f693ce5ffc64e8bb47ea471f774c96)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the specified source NFS file system location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified source NFS location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="onPremConfig")
    def on_prem_config(
        self,
    ) -> typing.Union["CfnLocationNFS.OnPremConfigProperty", _IResolvable_a771d0ef]:
        '''Contains a list of Amazon Resource Names (ARNs) of agents that are used to connect to an NFS server.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-onpremconfig
        '''
        return typing.cast(typing.Union["CfnLocationNFS.OnPremConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "onPremConfig"))

    @on_prem_config.setter
    def on_prem_config(
        self,
        value: typing.Union["CfnLocationNFS.OnPremConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286a2d4e7e29bde1f6f20bc92f6bfb2050984a0b871cba1ff0e200b02325b356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremConfig", value)

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union["CfnLocationNFS.MountOptionsProperty", _IResolvable_a771d0ef]]:
        '''The NFS mount options that DataSync can use to mount your NFS share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-mountoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLocationNFS.MountOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(
        self,
        value: typing.Optional[typing.Union["CfnLocationNFS.MountOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a91bce482fbb58ed9f74a75c9e1023bc980d00085c55390e1d496979f59496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value)

    @builtins.property
    @jsii.member(jsii_name="serverHostname")
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''The name of the NFS server.

        This value is the IP address or Domain Name Service (DNS) name of the NFS server. An agent that is installed on-premises uses this hostname to mount the NFS server in a network.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.
        .. epigraph::

           This name must either be DNS-compliant or must be an IP version 4 (IPv4) address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-serverhostname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverHostname"))

    @server_hostname.setter
    def server_hostname(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499352201816f8a4e3fcdd26e14c2ac853e98fd29340c03544a014d43d872afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverHostname", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''The subdirectory in the NFS file system that is used to read data from the NFS source location or write data to the NFS destination.

        The NFS path should be a path that's exported by the NFS server, or a subdirectory of that path. The path should be such that it can be mounted by other NFS clients in your network.

        To see all the paths exported by your NFS server, run " ``showmount -e nfs-server-name`` " from an NFS client that has access to your server. You can specify any directory that appears in the results, and any subdirectory of that directory. Ensure that the NFS export is accessible without Kerberos authentication.

        To transfer all the data in the folder you specified, DataSync needs to have permissions to read all the data. To ensure this, either configure the NFS export with ``no_root_squash,`` or ensure that the permissions for all of the files that you want DataSync allow read access for all users. Doing either enables the agent to read the files. For the agent to access directories, you must additionally enable all execute access.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.

        For information about NFS export configuration, see `18.7. The /etc/exports Configuration File <https://docs.aws.amazon.com/http://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-nfs-server-config-exports.html>`_ in the Red Hat Enterprise Linux documentation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60a5e51319c795366753fa2f0824c39f9fe8ed303464653fc3decb19567a2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationNFS.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''The NFS mount options that DataSync can use to mount your NFS share.

            :param version: Specifies the NFS version that you want DataSync to use when mounting your NFS share. If the server refuses to use the version specified, the task fails. You can specify the following options: - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1. - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server. - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0. .. epigraph:: DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                mount_options_property = datasync.CfnLocationNFS.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2706cfd9206cb86a7a9edabf87c147f99f4067816d4ff655617cc7b8799d9723)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Specifies the NFS version that you want DataSync to use when mounting your NFS share.

            If the server refuses to use the version specified, the task fails.

            You can specify the following options:

            - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1.
            - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server.
            - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0.

            .. epigraph::

               DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-mountoptions.html#cfn-datasync-locationnfs-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationNFS.OnPremConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"agent_arns": "agentArns"},
    )
    class OnPremConfigProperty:
        def __init__(self, *, agent_arns: typing.Sequence[builtins.str]) -> None:
            '''A list of Amazon Resource Names (ARNs) of agents to use for a Network File System (NFS) location.

            :param agent_arns: ARNs of the agents to use for an NFS location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-onpremconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                on_prem_config_property = datasync.CfnLocationNFS.OnPremConfigProperty(
                    agent_arns=["agentArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6aaec0394de708d3cb0fe1fa4b16e93b76400717fccfc8053ce9588cf7ac935)
                check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "agent_arns": agent_arns,
            }

        @builtins.property
        def agent_arns(self) -> typing.List[builtins.str]:
            '''ARNs of the agents to use for an NFS location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-onpremconfig.html#cfn-datasync-locationnfs-onpremconfig-agentarns
            '''
            result = self._values.get("agent_arns")
            assert result is not None, "Required property 'agent_arns' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationNFSProps",
    jsii_struct_bases=[],
    name_mapping={
        "on_prem_config": "onPremConfig",
        "mount_options": "mountOptions",
        "server_hostname": "serverHostname",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationNFSProps:
    def __init__(
        self,
        *,
        on_prem_config: typing.Union[typing.Union[CfnLocationNFS.OnPremConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        mount_options: typing.Optional[typing.Union[typing.Union[CfnLocationNFS.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationNFS``.

        :param on_prem_config: Contains a list of Amazon Resource Names (ARNs) of agents that are used to connect to an NFS server. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.
        :param mount_options: The NFS mount options that DataSync can use to mount your NFS share.
        :param server_hostname: The name of the NFS server. This value is the IP address or Domain Name Service (DNS) name of the NFS server. An agent that is installed on-premises uses this hostname to mount the NFS server in a network. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information. .. epigraph:: This name must either be DNS-compliant or must be an IP version 4 (IPv4) address.
        :param subdirectory: The subdirectory in the NFS file system that is used to read data from the NFS source location or write data to the NFS destination. The NFS path should be a path that's exported by the NFS server, or a subdirectory of that path. The path should be such that it can be mounted by other NFS clients in your network. To see all the paths exported by your NFS server, run " ``showmount -e nfs-server-name`` " from an NFS client that has access to your server. You can specify any directory that appears in the results, and any subdirectory of that directory. Ensure that the NFS export is accessible without Kerberos authentication. To transfer all the data in the folder you specified, DataSync needs to have permissions to read all the data. To ensure this, either configure the NFS export with ``no_root_squash,`` or ensure that the permissions for all of the files that you want DataSync allow read access for all users. Doing either enables the agent to read the files. For the agent to access directories, you must additionally enable all execute access. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information. For information about NFS export configuration, see `18.7. The /etc/exports Configuration File <https://docs.aws.amazon.com/http://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-nfs-server-config-exports.html>`_ in the Red Hat Enterprise Linux documentation.
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_nFSProps = datasync.CfnLocationNFSProps(
                on_prem_config=datasync.CfnLocationNFS.OnPremConfigProperty(
                    agent_arns=["agentArns"]
                ),
            
                # the properties below are optional
                mount_options=datasync.CfnLocationNFS.MountOptionsProperty(
                    version="version"
                ),
                server_hostname="serverHostname",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41eafc7de2388808e13a420839ef37400f5e9df21865d238fcfb4f10011bfadf)
            check_type(argname="argument on_prem_config", value=on_prem_config, expected_type=type_hints["on_prem_config"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "on_prem_config": on_prem_config,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if server_hostname is not None:
            self._values["server_hostname"] = server_hostname
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def on_prem_config(
        self,
    ) -> typing.Union[CfnLocationNFS.OnPremConfigProperty, _IResolvable_a771d0ef]:
        '''Contains a list of Amazon Resource Names (ARNs) of agents that are used to connect to an NFS server.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-onpremconfig
        '''
        result = self._values.get("on_prem_config")
        assert result is not None, "Required property 'on_prem_config' is missing"
        return typing.cast(typing.Union[CfnLocationNFS.OnPremConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union[CfnLocationNFS.MountOptionsProperty, _IResolvable_a771d0ef]]:
        '''The NFS mount options that DataSync can use to mount your NFS share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-mountoptions
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.Union[CfnLocationNFS.MountOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''The name of the NFS server.

        This value is the IP address or Domain Name Service (DNS) name of the NFS server. An agent that is installed on-premises uses this hostname to mount the NFS server in a network.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.
        .. epigraph::

           This name must either be DNS-compliant or must be an IP version 4 (IPv4) address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-serverhostname
        '''
        result = self._values.get("server_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''The subdirectory in the NFS file system that is used to read data from the NFS source location or write data to the NFS destination.

        The NFS path should be a path that's exported by the NFS server, or a subdirectory of that path. The path should be such that it can be mounted by other NFS clients in your network.

        To see all the paths exported by your NFS server, run " ``showmount -e nfs-server-name`` " from an NFS client that has access to your server. You can specify any directory that appears in the results, and any subdirectory of that directory. Ensure that the NFS export is accessible without Kerberos authentication.

        To transfer all the data in the folder you specified, DataSync needs to have permissions to read all the data. To ensure this, either configure the NFS export with ``no_root_squash,`` or ensure that the permissions for all of the files that you want DataSync allow read access for all users. Doing either enables the agent to read the files. For the agent to access directories, you must additionally enable all execute access.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.

        For information about NFS export configuration, see `18.7. The /etc/exports Configuration File <https://docs.aws.amazon.com/http://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-nfs-server-config-exports.html>`_ in the Red Hat Enterprise Linux documentation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationNFSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationObjectStorage(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationObjectStorage",
):
    '''A CloudFormation ``AWS::DataSync::LocationObjectStorage``.

    The ``AWS::DataSync::LocationObjectStorage`` resource specifies an endpoint for a self-managed object storage bucket. For more information about self-managed object storage locations, see `Creating a Location for Object Storage <https://docs.aws.amazon.com/datasync/latest/userguide/create-object-location.html>`_ .

    :cloudformationResource: AWS::DataSync::LocationObjectStorage
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_object_storage = datasync.CfnLocationObjectStorage(self, "MyCfnLocationObjectStorage",
            agent_arns=["agentArns"],
        
            # the properties below are optional
            access_key="accessKey",
            bucket_name="bucketName",
            secret_key="secretKey",
            server_certificate="serverCertificate",
            server_hostname="serverHostname",
            server_port=123,
            server_protocol="serverProtocol",
            subdirectory="subdirectory",
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
        agent_arns: typing.Sequence[builtins.str],
        access_key: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        server_certificate: typing.Optional[builtins.str] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        server_port: typing.Optional[jsii.Number] = None,
        server_protocol: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationObjectStorage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param agent_arns: Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can securely connect with your location.
        :param access_key: Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.
        :param bucket_name: Specifies the name of the object storage bucket involved in the transfer.
        :param secret_key: Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.
        :param server_certificate: Specifies a file with the certificates that are used to sign the object storage server's certificate (for example, ``file:///home/user/.ssh/storage_sys_certificate.pem`` ). The file you specify must include the following:. - The certificate of the signing certificate authority (CA) - Any intermediate certificates - base64 encoding - A ``.pem`` extension The file can be up to 32768 bytes (before base64 encoding). To use this parameter, configure ``ServerProtocol`` to ``HTTPS`` .
        :param server_hostname: Specifies the domain name or IP address of the object storage server. A DataSync agent uses this hostname to mount the object storage server in a network.
        :param server_port: Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).
        :param server_protocol: Specifies the protocol that your object storage server uses to communicate.
        :param subdirectory: Specifies the object prefix for your object storage server. If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a6fd215d00252471bfb683d082f005a7bc74e2b5a891dd2eb9a0541dc8a424)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationObjectStorageProps(
            agent_arns=agent_arns,
            access_key=access_key,
            bucket_name=bucket_name,
            secret_key=secret_key,
            server_certificate=server_certificate,
            server_hostname=server_hostname,
            server_port=server_port,
            server_protocol=server_protocol,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a6d250c544d2b1da5f007518162682ca7db336bcba745c05871eb4ef72ace13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b2f1d00b76586ca028c2448c103a3741dd188a86a9837bbdb3014dd9b0bc0d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the specified object storage location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified object storage location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentArns")
    def agent_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can securely connect with your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-agentarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "agentArns"))

    @agent_arns.setter
    def agent_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1643ff81c32c848efc860cdf7fed986fa0b221abf21f9b7dcefe00c76f8959b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentArns", value)

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-accesskey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f06bcb4165b4bd531f65bd84d026b9df215dc7204444973eff8dfe0082a4ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value)

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the object storage bucket involved in the transfer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-bucketname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d911359f2b03d7de9ceda147024231036bb3fb82a3ef93b315c50d0057f6abc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-secretkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ef65931ac379ac9bdc8131eee8c7906acf7989759f01072871fe628bfad369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value)

    @builtins.property
    @jsii.member(jsii_name="serverCertificate")
    def server_certificate(self) -> typing.Optional[builtins.str]:
        '''Specifies a file with the certificates that are used to sign the object storage server's certificate (for example, ``file:///home/user/.ssh/storage_sys_certificate.pem`` ). The file you specify must include the following:.

        - The certificate of the signing certificate authority (CA)
        - Any intermediate certificates
        - base64 encoding
        - A ``.pem`` extension

        The file can be up to 32768 bytes (before base64 encoding).

        To use this parameter, configure ``ServerProtocol`` to ``HTTPS`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-servercertificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverCertificate"))

    @server_certificate.setter
    def server_certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8e2dd675132944df1a24c24fbfa7880a5ed587c5b637005f6d24188f2d290f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCertificate", value)

    @builtins.property
    @jsii.member(jsii_name="serverHostname")
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''Specifies the domain name or IP address of the object storage server.

        A DataSync agent uses this hostname to mount the object storage server in a network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverhostname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverHostname"))

    @server_hostname.setter
    def server_hostname(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df89ec0f9132f1b4a112efc62a23948da674fe38fc10353387f7c762f35a0a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverHostname", value)

    @builtins.property
    @jsii.member(jsii_name="serverPort")
    def server_port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverport
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serverPort"))

    @server_port.setter
    def server_port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34e3c141cd60920163b890c4ba6f66277289fcb3545eac4c594d7cc40b4285e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverPort", value)

    @builtins.property
    @jsii.member(jsii_name="serverProtocol")
    def server_protocol(self) -> typing.Optional[builtins.str]:
        '''Specifies the protocol that your object storage server uses to communicate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverprotocol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverProtocol"))

    @server_protocol.setter
    def server_protocol(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2adac1cc0a4dbffff03e09cf20a9dfb39e3304bad59875f87a521ff9d1a5f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies the object prefix for your object storage server.

        If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c3b44d5726feb22ae4dc222ae27fae16cd81ddb98d4d830e46baeef7a106f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationObjectStorageProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "access_key": "accessKey",
        "bucket_name": "bucketName",
        "secret_key": "secretKey",
        "server_certificate": "serverCertificate",
        "server_hostname": "serverHostname",
        "server_port": "serverPort",
        "server_protocol": "serverProtocol",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationObjectStorageProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Sequence[builtins.str],
        access_key: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        server_certificate: typing.Optional[builtins.str] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        server_port: typing.Optional[jsii.Number] = None,
        server_protocol: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationObjectStorage``.

        :param agent_arns: Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can securely connect with your location.
        :param access_key: Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.
        :param bucket_name: Specifies the name of the object storage bucket involved in the transfer.
        :param secret_key: Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.
        :param server_certificate: Specifies a file with the certificates that are used to sign the object storage server's certificate (for example, ``file:///home/user/.ssh/storage_sys_certificate.pem`` ). The file you specify must include the following:. - The certificate of the signing certificate authority (CA) - Any intermediate certificates - base64 encoding - A ``.pem`` extension The file can be up to 32768 bytes (before base64 encoding). To use this parameter, configure ``ServerProtocol`` to ``HTTPS`` .
        :param server_hostname: Specifies the domain name or IP address of the object storage server. A DataSync agent uses this hostname to mount the object storage server in a network.
        :param server_port: Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).
        :param server_protocol: Specifies the protocol that your object storage server uses to communicate.
        :param subdirectory: Specifies the object prefix for your object storage server. If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_object_storage_props = datasync.CfnLocationObjectStorageProps(
                agent_arns=["agentArns"],
            
                # the properties below are optional
                access_key="accessKey",
                bucket_name="bucketName",
                secret_key="secretKey",
                server_certificate="serverCertificate",
                server_hostname="serverHostname",
                server_port=123,
                server_protocol="serverProtocol",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2d2de26a1b1ab4df2e89b7711896433b90b7c9b00ea16b8d51d138c11ad8de)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument server_certificate", value=server_certificate, expected_type=type_hints["server_certificate"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument server_port", value=server_port, expected_type=type_hints["server_port"])
            check_type(argname="argument server_protocol", value=server_protocol, expected_type=type_hints["server_protocol"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_arns": agent_arns,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if server_certificate is not None:
            self._values["server_certificate"] = server_certificate
        if server_hostname is not None:
            self._values["server_hostname"] = server_hostname
        if server_port is not None:
            self._values["server_port"] = server_port
        if server_protocol is not None:
            self._values["server_protocol"] = server_protocol
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can securely connect with your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-agentarns
        '''
        result = self._values.get("agent_arns")
        assert result is not None, "Required property 'agent_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-accesskey
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the object storage bucket involved in the transfer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-secretkey
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_certificate(self) -> typing.Optional[builtins.str]:
        '''Specifies a file with the certificates that are used to sign the object storage server's certificate (for example, ``file:///home/user/.ssh/storage_sys_certificate.pem`` ). The file you specify must include the following:.

        - The certificate of the signing certificate authority (CA)
        - Any intermediate certificates
        - base64 encoding
        - A ``.pem`` extension

        The file can be up to 32768 bytes (before base64 encoding).

        To use this parameter, configure ``ServerProtocol`` to ``HTTPS`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-servercertificate
        '''
        result = self._values.get("server_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''Specifies the domain name or IP address of the object storage server.

        A DataSync agent uses this hostname to mount the object storage server in a network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverhostname
        '''
        result = self._values.get("server_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverport
        '''
        result = self._values.get("server_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_protocol(self) -> typing.Optional[builtins.str]:
        '''Specifies the protocol that your object storage server uses to communicate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverprotocol
        '''
        result = self._values.get("server_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies the object prefix for your object storage server.

        If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationObjectStorageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationS3(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationS3",
):
    '''A CloudFormation ``AWS::DataSync::LocationS3``.

    The ``AWS::DataSync::LocationS3`` resource specifies an endpoint for an Amazon S3 bucket.

    For more information, see `Create an Amazon S3 location <https://docs.aws.amazon.com/datasync/latest/userguide/create-locations-cli.html#create-location-s3-cli>`_ in the *AWS DataSync User Guide* .

    :cloudformationResource: AWS::DataSync::LocationS3
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_s3 = datasync.CfnLocationS3(self, "MyCfnLocationS3",
            s3_config=datasync.CfnLocationS3.S3ConfigProperty(
                bucket_access_role_arn="bucketAccessRoleArn"
            ),
        
            # the properties below are optional
            s3_bucket_arn="s3BucketArn",
            s3_storage_class="s3StorageClass",
            subdirectory="subdirectory",
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
        s3_config: typing.Union[typing.Union["CfnLocationS3.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        s3_bucket_arn: typing.Optional[builtins.str] = None,
        s3_storage_class: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationS3``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param s3_config: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket. For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .
        :param s3_bucket_arn: The ARN of the Amazon S3 bucket.
        :param s3_storage_class: The Amazon S3 storage class that you want to store your files in when this location is used as a task destination. For buckets in AWS Regions , the storage class defaults to S3 Standard. For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .
        :param subdirectory: A subdirectory in the Amazon S3 bucket. This subdirectory in Amazon S3 is used to read data from the S3 source location or write data to the S3 destination.
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bebb2347f0afeb7e697def1cff9b241efd883d908d116d175d8696f35c7c2a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationS3Props(
            s3_config=s3_config,
            s3_bucket_arn=s3_bucket_arn,
            s3_storage_class=s3_storage_class,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b29abbcddb92aa49d3bab5eb0003737a67a4e4c724c317756df1e7bd7aa9c26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a62996d286811bed9ad89bd3c622a3cb0ca6b76f0480020fd79d513c668f8f7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the specified Amazon S3 location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified Amazon S3 location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="s3Config")
    def s3_config(
        self,
    ) -> typing.Union["CfnLocationS3.S3ConfigProperty", _IResolvable_a771d0ef]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket.

        For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3config
        '''
        return typing.cast(typing.Union["CfnLocationS3.S3ConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "s3Config"))

    @s3_config.setter
    def s3_config(
        self,
        value: typing.Union["CfnLocationS3.S3ConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df70c971ec20390e87ae208e2bd8e9ccf0e0a964475d17879981cd3a43fe56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Config", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketArn")
    def s3_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3bucketarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketArn"))

    @s3_bucket_arn.setter
    def s3_bucket_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883b1276eefeb8b5fb1e78baf4e0d547871f893da1a2e850029e8617df4a4c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="s3StorageClass")
    def s3_storage_class(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 storage class that you want to store your files in when this location is used as a task destination.

        For buckets in AWS Regions , the storage class defaults to S3 Standard.

        For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3storageclass
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3StorageClass"))

    @s3_storage_class.setter
    def s3_storage_class(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c59da0f6d9be5bb7012775e4f14d902185b88cf2a54a5c9a9cb029ab9eac931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3StorageClass", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the Amazon S3 bucket.

        This subdirectory in Amazon S3 is used to read data from the S3 source location or write data to the S3 destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85d6a1a9e0c0595d3ece72d2a405c8a10d7ecf2b210c36e3d7832f83d6fd74a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationS3.S3ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_access_role_arn": "bucketAccessRoleArn"},
    )
    class S3ConfigProperty:
        def __init__(self, *, bucket_access_role_arn: builtins.str) -> None:
            '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role used to access an Amazon S3 bucket.

            For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .

            :param bucket_access_role_arn: The ARN of the IAM role for accessing the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locations3-s3config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                s3_config_property = datasync.CfnLocationS3.S3ConfigProperty(
                    bucket_access_role_arn="bucketAccessRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d9878f7df7fbcbb5ef6bbc29012ecaa83910692295323848c04ae4188d0c926)
                check_type(argname="argument bucket_access_role_arn", value=bucket_access_role_arn, expected_type=type_hints["bucket_access_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_access_role_arn": bucket_access_role_arn,
            }

        @builtins.property
        def bucket_access_role_arn(self) -> builtins.str:
            '''The ARN of the IAM role for accessing the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locations3-s3config.html#cfn-datasync-locations3-s3config-bucketaccessrolearn
            '''
            result = self._values.get("bucket_access_role_arn")
            assert result is not None, "Required property 'bucket_access_role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationS3Props",
    jsii_struct_bases=[],
    name_mapping={
        "s3_config": "s3Config",
        "s3_bucket_arn": "s3BucketArn",
        "s3_storage_class": "s3StorageClass",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationS3Props:
    def __init__(
        self,
        *,
        s3_config: typing.Union[typing.Union[CfnLocationS3.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        s3_bucket_arn: typing.Optional[builtins.str] = None,
        s3_storage_class: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationS3``.

        :param s3_config: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket. For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .
        :param s3_bucket_arn: The ARN of the Amazon S3 bucket.
        :param s3_storage_class: The Amazon S3 storage class that you want to store your files in when this location is used as a task destination. For buckets in AWS Regions , the storage class defaults to S3 Standard. For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .
        :param subdirectory: A subdirectory in the Amazon S3 bucket. This subdirectory in Amazon S3 is used to read data from the S3 source location or write data to the S3 destination.
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_s3_props = datasync.CfnLocationS3Props(
                s3_config=datasync.CfnLocationS3.S3ConfigProperty(
                    bucket_access_role_arn="bucketAccessRoleArn"
                ),
            
                # the properties below are optional
                s3_bucket_arn="s3BucketArn",
                s3_storage_class="s3StorageClass",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbeaa280acbad6d9c18a975bebfa32477a2fad7aed60ed19eeaa8b269f8a159)
            check_type(argname="argument s3_config", value=s3_config, expected_type=type_hints["s3_config"])
            check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            check_type(argname="argument s3_storage_class", value=s3_storage_class, expected_type=type_hints["s3_storage_class"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_config": s3_config,
        }
        if s3_bucket_arn is not None:
            self._values["s3_bucket_arn"] = s3_bucket_arn
        if s3_storage_class is not None:
            self._values["s3_storage_class"] = s3_storage_class
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def s3_config(
        self,
    ) -> typing.Union[CfnLocationS3.S3ConfigProperty, _IResolvable_a771d0ef]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket.

        For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3config
        '''
        result = self._values.get("s3_config")
        assert result is not None, "Required property 's3_config' is missing"
        return typing.cast(typing.Union[CfnLocationS3.S3ConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def s3_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3bucketarn
        '''
        result = self._values.get("s3_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_storage_class(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 storage class that you want to store your files in when this location is used as a task destination.

        For buckets in AWS Regions , the storage class defaults to S3 Standard.

        For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3storageclass
        '''
        result = self._values.get("s3_storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the Amazon S3 bucket.

        This subdirectory in Amazon S3 is used to read data from the S3 source location or write data to the S3 destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationS3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLocationSMB(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnLocationSMB",
):
    '''A CloudFormation ``AWS::DataSync::LocationSMB``.

    The ``AWS::DataSync::LocationSMB`` resource specifies a Server Message Block (SMB) location.

    :cloudformationResource: AWS::DataSync::LocationSMB
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_location_sMB = datasync.CfnLocationSMB(self, "MyCfnLocationSMB",
            agent_arns=["agentArns"],
            user="user",
        
            # the properties below are optional
            domain="domain",
            mount_options=datasync.CfnLocationSMB.MountOptionsProperty(
                version="version"
            ),
            password="password",
            server_hostname="serverHostname",
            subdirectory="subdirectory",
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
        agent_arns: typing.Sequence[builtins.str],
        user: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        mount_options: typing.Optional[typing.Union[typing.Union["CfnLocationSMB.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        password: typing.Optional[builtins.str] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationSMB``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param agent_arns: The Amazon Resource Names (ARNs) of agents to use for a Server Message Block (SMB) location.
        :param user: The user who can mount the share and has the permissions to access files and folders in the SMB share. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .
        :param domain: Specifies the Windows domain name that your SMB file server belongs to. For more information, see `required permissions <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ for SMB locations.
        :param mount_options: Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.
        :param password: The password of the user who can mount the share and has the permissions to access files and folders in the SMB share.
        :param server_hostname: Specifies the Domain Name Service (DNS) name or IP address of the SMB file server that your DataSync agent will mount. .. epigraph:: You can't specify an IP version 6 (IPv6) address.
        :param subdirectory: The subdirectory in the SMB file system that is used to read data from the SMB source location or write data to the SMB destination. The SMB path should be a path that's exported by the SMB server, or a subdirectory of that path. The path should be such that it can be mounted by other SMB clients in your network. .. epigraph:: ``Subdirectory`` must be specified with forward slashes. For example, ``/path/to/folder`` . To transfer all the data in the folder you specified, DataSync must have permissions to mount the SMB share, as well as to access all the data in that share. To ensure this, either make sure that the user name and password specified belongs to the user who can mount the share, and who has the appropriate permissions for all of the files and directories that you want DataSync to access, or use credentials of a member of the Backup Operators group to mount the share. Doing either one enables the agent to access the data. For the agent to access directories, you must additionally enable all execute access.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a85bfbe3eed46263ccdb15ef31da1b91298ceb8c58830289e3941ab6808c72)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationSMBProps(
            agent_arns=agent_arns,
            user=user,
            domain=domain,
            mount_options=mount_options,
            password=password,
            server_hostname=server_hostname,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0aca94953e4cd5e100f9ecebc6b561181eab3417857ed5bb50fb9c79c2cb2be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18a9d35dbc35634edd8998eb9caa294d8c691ec483a159fbd3034c6b73f75dad)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the specified SMB file system.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified SMB location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentArns")
    def agent_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of agents to use for a Server Message Block (SMB) location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-agentarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "agentArns"))

    @agent_arns.setter
    def agent_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db9129d5ab70beaf0fb00d39911c0706c25345a3eeca9a2dd8c8c98a8908de7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentArns", value)

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        '''The user who can mount the share and has the permissions to access files and folders in the SMB share.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-user
        '''
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de05707f447a2c173f2de62ce95604e01356d115fc8937210fd2c9a2d615841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the Windows domain name that your SMB file server belongs to.

        For more information, see `required permissions <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ for SMB locations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-domain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ce3150f921c2e07d4c0f92292644b56d98ef8d879d79742ca262f5a7150c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union["CfnLocationSMB.MountOptionsProperty", _IResolvable_a771d0ef]]:
        '''Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-mountoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLocationSMB.MountOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(
        self,
        value: typing.Optional[typing.Union["CfnLocationSMB.MountOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb30696d6be749e067285f47afc3da9ad3bbfae60c1c7982176aa86c25f50f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        '''The password of the user who can mount the share and has the permissions to access files and folders in the SMB share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-password
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042547a34873640a9d27a07c9d4be4b112f6032d9e549af489c4ef9656285f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="serverHostname")
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''Specifies the Domain Name Service (DNS) name or IP address of the SMB file server that your DataSync agent will mount.

        .. epigraph::

           You can't specify an IP version 6 (IPv6) address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-serverhostname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverHostname"))

    @server_hostname.setter
    def server_hostname(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca635bb23b6e1a9313ace5e1345ab4abc7a64a7fd7fca0d7e0e1edb8265b98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverHostname", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''The subdirectory in the SMB file system that is used to read data from the SMB source location or write data to the SMB destination.

        The SMB path should be a path that's exported by the SMB server, or a subdirectory of that path. The path should be such that it can be mounted by other SMB clients in your network.
        .. epigraph::

           ``Subdirectory`` must be specified with forward slashes. For example, ``/path/to/folder`` .

        To transfer all the data in the folder you specified, DataSync must have permissions to mount the SMB share, as well as to access all the data in that share. To ensure this, either make sure that the user name and password specified belongs to the user who can mount the share, and who has the appropriate permissions for all of the files and directories that you want DataSync to access, or use credentials of a member of the Backup Operators group to mount the share. Doing either one enables the agent to access the data. For the agent to access directories, you must additionally enable all execute access.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7917e47ea9d1726e38d244ae48e200d276e1b28608e48444f8afde41b04b2b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnLocationSMB.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.

            :param version: By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server. You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically. These are the following options for configuring the SMB version: - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate the highest version of SMB that they mutually support between 2.1 and 3.1.1. This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error. - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2. - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1. - ``SMB2_0`` : Restricts the protocol negotiation to only SMB version 2.0. - ``SMB1`` : Restricts the protocol negotiation to only SMB version 1.0. .. epigraph:: The ``SMB1`` option isn't available when `creating an Amazon FSx for NetApp ONTAP location <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateLocationFsxOntap.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                mount_options_property = datasync.CfnLocationSMB.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e27b74819a9647ebadd5a97b0afc22318515fb5d7293f7c855f6bdba1055ca9)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server.

            You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically.

            These are the following options for configuring the SMB version:

            - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate the highest version of SMB that they mutually support between 2.1 and 3.1.1.

            This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error.

            - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2.
            - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1.
            - ``SMB2_0`` : Restricts the protocol negotiation to only SMB version 2.0.
            - ``SMB1`` : Restricts the protocol negotiation to only SMB version 1.0.

            .. epigraph::

               The ``SMB1`` option isn't available when `creating an Amazon FSx for NetApp ONTAP location <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateLocationFsxOntap.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-mountoptions.html#cfn-datasync-locationsmb-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnLocationSMBProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "user": "user",
        "domain": "domain",
        "mount_options": "mountOptions",
        "password": "password",
        "server_hostname": "serverHostname",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationSMBProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Sequence[builtins.str],
        user: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        mount_options: typing.Optional[typing.Union[typing.Union[CfnLocationSMB.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        password: typing.Optional[builtins.str] = None,
        server_hostname: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationSMB``.

        :param agent_arns: The Amazon Resource Names (ARNs) of agents to use for a Server Message Block (SMB) location.
        :param user: The user who can mount the share and has the permissions to access files and folders in the SMB share. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .
        :param domain: Specifies the Windows domain name that your SMB file server belongs to. For more information, see `required permissions <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ for SMB locations.
        :param mount_options: Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.
        :param password: The password of the user who can mount the share and has the permissions to access files and folders in the SMB share.
        :param server_hostname: Specifies the Domain Name Service (DNS) name or IP address of the SMB file server that your DataSync agent will mount. .. epigraph:: You can't specify an IP version 6 (IPv6) address.
        :param subdirectory: The subdirectory in the SMB file system that is used to read data from the SMB source location or write data to the SMB destination. The SMB path should be a path that's exported by the SMB server, or a subdirectory of that path. The path should be such that it can be mounted by other SMB clients in your network. .. epigraph:: ``Subdirectory`` must be specified with forward slashes. For example, ``/path/to/folder`` . To transfer all the data in the folder you specified, DataSync must have permissions to mount the SMB share, as well as to access all the data in that share. To ensure this, either make sure that the user name and password specified belongs to the user who can mount the share, and who has the appropriate permissions for all of the files and directories that you want DataSync to access, or use credentials of a member of the Backup Operators group to mount the share. Doing either one enables the agent to access the data. For the agent to access directories, you must additionally enable all execute access.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_location_sMBProps = datasync.CfnLocationSMBProps(
                agent_arns=["agentArns"],
                user="user",
            
                # the properties below are optional
                domain="domain",
                mount_options=datasync.CfnLocationSMB.MountOptionsProperty(
                    version="version"
                ),
                password="password",
                server_hostname="serverHostname",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6646299a18353ff73b3655b548db8b72ee415cb8c806d919574a11b95078d18)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_arns": agent_arns,
            "user": user,
        }
        if domain is not None:
            self._values["domain"] = domain
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if password is not None:
            self._values["password"] = password
        if server_hostname is not None:
            self._values["server_hostname"] = server_hostname
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of agents to use for a Server Message Block (SMB) location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-agentarns
        '''
        result = self._values.get("agent_arns")
        assert result is not None, "Required property 'agent_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def user(self) -> builtins.str:
        '''The user who can mount the share and has the permissions to access files and folders in the SMB share.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-user
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the Windows domain name that your SMB file server belongs to.

        For more information, see `required permissions <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ for SMB locations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union[CfnLocationSMB.MountOptionsProperty, _IResolvable_a771d0ef]]:
        '''Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-mountoptions
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.Union[CfnLocationSMB.MountOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password of the user who can mount the share and has the permissions to access files and folders in the SMB share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_hostname(self) -> typing.Optional[builtins.str]:
        '''Specifies the Domain Name Service (DNS) name or IP address of the SMB file server that your DataSync agent will mount.

        .. epigraph::

           You can't specify an IP version 6 (IPv6) address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-serverhostname
        '''
        result = self._values.get("server_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''The subdirectory in the SMB file system that is used to read data from the SMB source location or write data to the SMB destination.

        The SMB path should be a path that's exported by the SMB server, or a subdirectory of that path. The path should be such that it can be mounted by other SMB clients in your network.
        .. epigraph::

           ``Subdirectory`` must be specified with forward slashes. For example, ``/path/to/folder`` .

        To transfer all the data in the folder you specified, DataSync must have permissions to mount the SMB share, as well as to access all the data in that share. To ensure this, either make sure that the user name and password specified belongs to the user who can mount the share, and who has the appropriate permissions for all of the files and directories that you want DataSync to access, or use credentials of a member of the Backup Operators group to mount the share. Doing either one enables the agent to access the data. For the agent to access directories, you must additionally enable all execute access.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationSMBProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStorageSystem(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnStorageSystem",
):
    '''A CloudFormation ``AWS::DataSync::StorageSystem``.

    The ``AWS::DataSync::StorageSystem`` resource creates an AWS resource for an on-premises storage system that you want DataSync Discovery to collect information about. For more information, see `discovering your storage with DataSync Discovery. <https://docs.aws.amazon.com/datasync/latest/userguide/understanding-your-storage.html>`_

    :cloudformationResource: AWS::DataSync::StorageSystem
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_storage_system = datasync.CfnStorageSystem(self, "MyCfnStorageSystem",
            agent_arns=["agentArns"],
            server_configuration=datasync.CfnStorageSystem.ServerConfigurationProperty(
                server_hostname="serverHostname",
        
                # the properties below are optional
                server_port=123
            ),
            system_type="systemType",
        
            # the properties below are optional
            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
            name="name",
            server_credentials=datasync.CfnStorageSystem.ServerCredentialsProperty(
                password="password",
                username="username"
            ),
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
        agent_arns: typing.Sequence[builtins.str],
        server_configuration: typing.Union[typing.Union["CfnStorageSystem.ServerConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        system_type: builtins.str,
        cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        server_credentials: typing.Optional[typing.Union[typing.Union["CfnStorageSystem.ServerCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::StorageSystem``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param agent_arns: Specifies the Amazon Resource Name (ARN) of the DataSync agent that connects to and reads from your on-premises storage system's management interface.
        :param server_configuration: Specifies the server name and network port required to connect with the management interface of your on-premises storage system.
        :param system_type: Specifies the type of on-premises storage system that you want DataSync Discovery to collect information about. .. epigraph:: DataSync Discovery currently supports NetApp Fabric-Attached Storage (FAS) and All Flash FAS (AFF) systems running ONTAP 9.7 or later.
        :param cloud_watch_log_group_arn: Specifies the ARN of the Amazon CloudWatch log group for monitoring and logging discovery job events.
        :param name: Specifies a familiar name for your on-premises storage system.
        :param server_credentials: Specifies the user name and password for accessing your on-premises storage system's management interface.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your on-premises storage system.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3608275a7dd972e375d31feddf14c4fcae4b3b23888af0ab07655707aa36853d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStorageSystemProps(
            agent_arns=agent_arns,
            server_configuration=server_configuration,
            system_type=system_type,
            cloud_watch_log_group_arn=cloud_watch_log_group_arn,
            name=name,
            server_credentials=server_credentials,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3229fcb53782f9f7814acf8253a6f76ab10964f9c4c80901a4141ec782c6b03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0e0492cac30c9dc63bc68328ce32c902c1cad2ccf512a420547782e37b41400)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConnectivityStatus")
    def attr_connectivity_status(self) -> builtins.str:
        '''Indicates whether your DataSync agent can connect to your on-premises storage system.

        :cloudformationAttribute: ConnectivityStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectivityStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrSecretsManagerArn")
    def attr_secrets_manager_arn(self) -> builtins.str:
        '''The ARN of the secret that stores your on-premises storage system's credentials.

        DataSync Discovery stores these credentials in `AWS Secrets Manager <https://docs.aws.amazon.com/datasync/latest/userguide/discovery-configure-storage.html#discovery-add-storage>`_ .

        :cloudformationAttribute: SecretsManagerArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSecretsManagerArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStorageSystemArn")
    def attr_storage_system_arn(self) -> builtins.str:
        '''The ARN of the on-premises storage system that you're using with DataSync Discovery.

        :cloudformationAttribute: StorageSystemArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStorageSystemArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your on-premises storage system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentArns")
    def agent_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of the DataSync agent that connects to and reads from your on-premises storage system's management interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-agentarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "agentArns"))

    @agent_arns.setter
    def agent_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c8a6363f0a1c5e95eed9a5bed8fbabf5ebf6b66a731538b3fa02805b69b914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentArns", value)

    @builtins.property
    @jsii.member(jsii_name="serverConfiguration")
    def server_configuration(
        self,
    ) -> typing.Union["CfnStorageSystem.ServerConfigurationProperty", _IResolvable_a771d0ef]:
        '''Specifies the server name and network port required to connect with the management interface of your on-premises storage system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-serverconfiguration
        '''
        return typing.cast(typing.Union["CfnStorageSystem.ServerConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "serverConfiguration"))

    @server_configuration.setter
    def server_configuration(
        self,
        value: typing.Union["CfnStorageSystem.ServerConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c922863e5e839113af66531c623ab5668c7ad9d8bac946c378e192c94732f64b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="systemType")
    def system_type(self) -> builtins.str:
        '''Specifies the type of on-premises storage system that you want DataSync Discovery to collect information about.

        .. epigraph::

           DataSync Discovery currently supports NetApp Fabric-Attached Storage (FAS) and All Flash FAS (AFF) systems running ONTAP 9.7 or later.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-systemtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "systemType"))

    @system_type.setter
    def system_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38948210ba65e5dae35556624b88670fbbfd4b71ea48fcd0ebf88940217b117e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemType", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN of the Amazon CloudWatch log group for monitoring and logging discovery job events.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-cloudwatchloggrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWatchLogGroupArn"))

    @cloud_watch_log_group_arn.setter
    def cloud_watch_log_group_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d2e4d06cdf10cd401925c755f5b1008f82a92145843341458c4582784458b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchLogGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''Specifies a familiar name for your on-premises storage system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3963efddbe63c1cab58d227cd99237b0b28e138cc02091ebc1325e9d8477be49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="serverCredentials")
    def server_credentials(
        self,
    ) -> typing.Optional[typing.Union["CfnStorageSystem.ServerCredentialsProperty", _IResolvable_a771d0ef]]:
        '''Specifies the user name and password for accessing your on-premises storage system's management interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-servercredentials
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStorageSystem.ServerCredentialsProperty", _IResolvable_a771d0ef]], jsii.get(self, "serverCredentials"))

    @server_credentials.setter
    def server_credentials(
        self,
        value: typing.Optional[typing.Union["CfnStorageSystem.ServerCredentialsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be26c384ba2ba40e30f1fc04ace93633361b945bfe39d6a60d08e493a32a1aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCredentials", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnStorageSystem.ServerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "server_hostname": "serverHostname",
            "server_port": "serverPort",
        },
    )
    class ServerConfigurationProperty:
        def __init__(
            self,
            *,
            server_hostname: builtins.str,
            server_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The network settings that DataSync Discovery uses to connect with your on-premises storage system's management interface.

            :param server_hostname: The domain name or IP address of your storage system's management interface.
            :param server_port: The network port for accessing the storage system's management interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-storagesystem-serverconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                server_configuration_property = datasync.CfnStorageSystem.ServerConfigurationProperty(
                    server_hostname="serverHostname",
                
                    # the properties below are optional
                    server_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a54d1ed122670eaf4422d3003bbcaebfde21be61237756fe6dc86a9fa4fcb846)
                check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
                check_type(argname="argument server_port", value=server_port, expected_type=type_hints["server_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "server_hostname": server_hostname,
            }
            if server_port is not None:
                self._values["server_port"] = server_port

        @builtins.property
        def server_hostname(self) -> builtins.str:
            '''The domain name or IP address of your storage system's management interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-storagesystem-serverconfiguration.html#cfn-datasync-storagesystem-serverconfiguration-serverhostname
            '''
            result = self._values.get("server_hostname")
            assert result is not None, "Required property 'server_hostname' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def server_port(self) -> typing.Optional[jsii.Number]:
            '''The network port for accessing the storage system's management interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-storagesystem-serverconfiguration.html#cfn-datasync-storagesystem-serverconfiguration-serverport
            '''
            result = self._values.get("server_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnStorageSystem.ServerCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class ServerCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''The credentials that provide DataSync Discovery read access to your on-premises storage system's management interface.

            DataSync Discovery stores these credentials in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ . For more information, see `Accessing your on-premises storage system <https://docs.aws.amazon.com/datasync/latest/userguide/discovery-configure-storage.html>`_ .

            :param password: Specifies the password for your storage system's management interface.
            :param username: Specifies the user name for your storage system's management interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-storagesystem-servercredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                server_credentials_property = datasync.CfnStorageSystem.ServerCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__271ca39e9b59361434ea87ec8de3ebae5e90c64bf1bf96f3c1d1e1e91e4fd0fb)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''Specifies the password for your storage system's management interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-storagesystem-servercredentials.html#cfn-datasync-storagesystem-servercredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''Specifies the user name for your storage system's management interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-storagesystem-servercredentials.html#cfn-datasync-storagesystem-servercredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnStorageSystemProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "server_configuration": "serverConfiguration",
        "system_type": "systemType",
        "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
        "name": "name",
        "server_credentials": "serverCredentials",
        "tags": "tags",
    },
)
class CfnStorageSystemProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Sequence[builtins.str],
        server_configuration: typing.Union[typing.Union[CfnStorageSystem.ServerConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        system_type: builtins.str,
        cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        server_credentials: typing.Optional[typing.Union[typing.Union[CfnStorageSystem.ServerCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStorageSystem``.

        :param agent_arns: Specifies the Amazon Resource Name (ARN) of the DataSync agent that connects to and reads from your on-premises storage system's management interface.
        :param server_configuration: Specifies the server name and network port required to connect with the management interface of your on-premises storage system.
        :param system_type: Specifies the type of on-premises storage system that you want DataSync Discovery to collect information about. .. epigraph:: DataSync Discovery currently supports NetApp Fabric-Attached Storage (FAS) and All Flash FAS (AFF) systems running ONTAP 9.7 or later.
        :param cloud_watch_log_group_arn: Specifies the ARN of the Amazon CloudWatch log group for monitoring and logging discovery job events.
        :param name: Specifies a familiar name for your on-premises storage system.
        :param server_credentials: Specifies the user name and password for accessing your on-premises storage system's management interface.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your on-premises storage system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_storage_system_props = datasync.CfnStorageSystemProps(
                agent_arns=["agentArns"],
                server_configuration=datasync.CfnStorageSystem.ServerConfigurationProperty(
                    server_hostname="serverHostname",
            
                    # the properties below are optional
                    server_port=123
                ),
                system_type="systemType",
            
                # the properties below are optional
                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                name="name",
                server_credentials=datasync.CfnStorageSystem.ServerCredentialsProperty(
                    password="password",
                    username="username"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b7193913f0014df0f9eeadb500bd4415e4c28a24f8fbc0398081477692709a)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument server_configuration", value=server_configuration, expected_type=type_hints["server_configuration"])
            check_type(argname="argument system_type", value=system_type, expected_type=type_hints["system_type"])
            check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument server_credentials", value=server_credentials, expected_type=type_hints["server_credentials"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_arns": agent_arns,
            "server_configuration": server_configuration,
            "system_type": system_type,
        }
        if cloud_watch_log_group_arn is not None:
            self._values["cloud_watch_log_group_arn"] = cloud_watch_log_group_arn
        if name is not None:
            self._values["name"] = name
        if server_credentials is not None:
            self._values["server_credentials"] = server_credentials
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of the DataSync agent that connects to and reads from your on-premises storage system's management interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-agentarns
        '''
        result = self._values.get("agent_arns")
        assert result is not None, "Required property 'agent_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def server_configuration(
        self,
    ) -> typing.Union[CfnStorageSystem.ServerConfigurationProperty, _IResolvable_a771d0ef]:
        '''Specifies the server name and network port required to connect with the management interface of your on-premises storage system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-serverconfiguration
        '''
        result = self._values.get("server_configuration")
        assert result is not None, "Required property 'server_configuration' is missing"
        return typing.cast(typing.Union[CfnStorageSystem.ServerConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def system_type(self) -> builtins.str:
        '''Specifies the type of on-premises storage system that you want DataSync Discovery to collect information about.

        .. epigraph::

           DataSync Discovery currently supports NetApp Fabric-Attached Storage (FAS) and All Flash FAS (AFF) systems running ONTAP 9.7 or later.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-systemtype
        '''
        result = self._values.get("system_type")
        assert result is not None, "Required property 'system_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN of the Amazon CloudWatch log group for monitoring and logging discovery job events.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-cloudwatchloggrouparn
        '''
        result = self._values.get("cloud_watch_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Specifies a familiar name for your on-premises storage system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_credentials(
        self,
    ) -> typing.Optional[typing.Union[CfnStorageSystem.ServerCredentialsProperty, _IResolvable_a771d0ef]]:
        '''Specifies the user name and password for accessing your on-premises storage system's management interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-servercredentials
        '''
        result = self._values.get("server_credentials")
        return typing.cast(typing.Optional[typing.Union[CfnStorageSystem.ServerCredentialsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your on-premises storage system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-storagesystem.html#cfn-datasync-storagesystem-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStorageSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTask(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_datasync.CfnTask",
):
    '''A CloudFormation ``AWS::DataSync::Task``.

    The ``AWS::DataSync::Task`` resource specifies a task. A task is a set of two locations (source and destination) and a set of ``Options`` that you use to control the behavior of a task. If you don't specify ``Options`` when you create a task, AWS DataSync populates them with service defaults.

    :cloudformationResource: AWS::DataSync::Task
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_datasync as datasync
        
        cfn_task = datasync.CfnTask(self, "MyCfnTask",
            destination_location_arn="destinationLocationArn",
            source_location_arn="sourceLocationArn",
        
            # the properties below are optional
            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
            excludes=[datasync.CfnTask.FilterRuleProperty(
                filter_type="filterType",
                value="value"
            )],
            includes=[datasync.CfnTask.FilterRuleProperty(
                filter_type="filterType",
                value="value"
            )],
            name="name",
            options=datasync.CfnTask.OptionsProperty(
                atime="atime",
                bytes_per_second=123,
                gid="gid",
                log_level="logLevel",
                mtime="mtime",
                object_tags="objectTags",
                overwrite_mode="overwriteMode",
                posix_permissions="posixPermissions",
                preserve_deleted_files="preserveDeletedFiles",
                preserve_devices="preserveDevices",
                security_descriptor_copy_flags="securityDescriptorCopyFlags",
                task_queueing="taskQueueing",
                transfer_mode="transferMode",
                uid="uid",
                verify_mode="verifyMode"
            ),
            schedule=datasync.CfnTask.TaskScheduleProperty(
                schedule_expression="scheduleExpression"
            ),
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
        destination_location_arn: builtins.str,
        source_location_arn: builtins.str,
        cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
        excludes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTask.FilterRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        includes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTask.FilterRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union[typing.Union["CfnTask.OptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        schedule: typing.Optional[typing.Union[typing.Union["CfnTask.TaskScheduleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::Task``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_location_arn: The Amazon Resource Name (ARN) of an AWS storage resource's location.
        :param source_location_arn: The Amazon Resource Name (ARN) of the source location for the task.
        :param cloud_watch_log_group_arn: The Amazon Resource Name (ARN) of the Amazon CloudWatch log group that is used to monitor and log events in the task. For more information about how to use CloudWatch Logs with DataSync, see `Monitoring Your Task <https://docs.aws.amazon.com/datasync/latest/userguide/monitor-datasync.html#cloudwatchlogs>`_ in the *AWS DataSync User Guide.* For more information about these groups, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ in the *Amazon CloudWatch Logs User Guide* .
        :param excludes: Specifies a list of filter rules that exclude specific data during your transfer. For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param includes: Specifies a list of filter rules that include specific data during your transfer. For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param name: The name of a task. This value is a text reference that is used to identify the task in the console.
        :param options: Specifies the configuration options for a task. Some options include preserving file or object metadata and verifying data integrity. You can also override these options before starting an individual run of a task (also known as a *task execution* ). For more information, see `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .
        :param schedule: Specifies a schedule used to periodically transfer files from a source to a destination location. The schedule should be specified in UTC time. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .
        :param tags: Specifies the tags that you want to apply to the Amazon Resource Name (ARN) representing the task. *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a249420f561a6f9523fafef5cccaa91658a60eac07bf2c98ccb8c8e42cee98a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTaskProps(
            destination_location_arn=destination_location_arn,
            source_location_arn=source_location_arn,
            cloud_watch_log_group_arn=cloud_watch_log_group_arn,
            excludes=excludes,
            includes=includes,
            name=name,
            options=options,
            schedule=schedule,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b634717b9327800846f83ccf76e2fc0ea89aed34422b1c8f8c89373e8ed0989)
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
            type_hints = typing.get_type_hints(_typecheckingstub__946e93faf8a19ca4126e3ee45ef218c32c4aa91042b8b57e4e64efa8853c5cc7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDestinationNetworkInterfaceArns")
    def attr_destination_network_interface_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the destination elastic network interfaces (ENIs) that were created for your subnet.

        :cloudformationAttribute: DestinationNetworkInterfaceArns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrDestinationNetworkInterfaceArns"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceNetworkInterfaceArns")
    def attr_source_network_interface_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the source ENIs that were created for your subnet.

        :cloudformationAttribute: SourceNetworkInterfaceArns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrSourceNetworkInterfaceArns"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the task that was described.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrTaskArn")
    def attr_task_arn(self) -> builtins.str:
        '''The ARN of the task.

        :cloudformationAttribute: TaskArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTaskArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Specifies the tags that you want to apply to the Amazon Resource Name (ARN) representing the task.

        *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="destinationLocationArn")
    def destination_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of an AWS storage resource's location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-destinationlocationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationLocationArn"))

    @destination_location_arn.setter
    def destination_location_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b5a796bbd0fa27501cedff341336796d679606fca290a513e4ae67dd9c9414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationLocationArn", value)

    @builtins.property
    @jsii.member(jsii_name="sourceLocationArn")
    def source_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the source location for the task.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-sourcelocationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceLocationArn"))

    @source_location_arn.setter
    def source_location_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fda068271936dc842fee855ee4b84fd2e02fcb4e13baa4dc457b467a0d1187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceLocationArn", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon CloudWatch log group that is used to monitor and log events in the task.

        For more information about how to use CloudWatch Logs with DataSync, see `Monitoring Your Task <https://docs.aws.amazon.com/datasync/latest/userguide/monitor-datasync.html#cloudwatchlogs>`_ in the *AWS DataSync User Guide.*

        For more information about these groups, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ in the *Amazon CloudWatch Logs User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-cloudwatchloggrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWatchLogGroupArn"))

    @cloud_watch_log_group_arn.setter
    def cloud_watch_log_group_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4613fba08fe6907fb92ab247241ae851c4f34fff1a82d210b3cb5e8edb827bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchLogGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTask.FilterRuleProperty", _IResolvable_a771d0ef]]]]:
        '''Specifies a list of filter rules that exclude specific data during your transfer.

        For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-excludes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTask.FilterRuleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTask.FilterRuleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab290047311d9ecac04ad6a1e93f70deda93ee97e08258ff96884d5a406e8949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value)

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTask.FilterRuleProperty", _IResolvable_a771d0ef]]]]:
        '''Specifies a list of filter rules that include specific data during your transfer.

        For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-includes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTask.FilterRuleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "includes"))

    @includes.setter
    def includes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTask.FilterRuleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3b44f184cb844de208a74a298780e976f85cd35fc6894709af192949247a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a task.

        This value is a text reference that is used to identify the task in the console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ef1b40a3983d238fc61334307e091b207d0581a5d1303bf7a650c6059a4d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(
        self,
    ) -> typing.Optional[typing.Union["CfnTask.OptionsProperty", _IResolvable_a771d0ef]]:
        '''Specifies the configuration options for a task. Some options include preserving file or object metadata and verifying data integrity.

        You can also override these options before starting an individual run of a task (also known as a *task execution* ). For more information, see `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-options
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTask.OptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "options"))

    @options.setter
    def options(
        self,
        value: typing.Optional[typing.Union["CfnTask.OptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b1be93fc55e5f12af3a464c502b3fc10994908bda89af8fb1abf67b7fcf7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> typing.Optional[typing.Union["CfnTask.TaskScheduleProperty", _IResolvable_a771d0ef]]:
        '''Specifies a schedule used to periodically transfer files from a source to a destination location.

        The schedule should be specified in UTC time. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-schedule
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTask.TaskScheduleProperty", _IResolvable_a771d0ef]], jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(
        self,
        value: typing.Optional[typing.Union["CfnTask.TaskScheduleProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2391c8b26899243674d4d39e60701ebb4cef23891bc8c014b371e3dcaa7fcdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnTask.FilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"filter_type": "filterType", "value": "value"},
    )
    class FilterRuleProperty:
        def __init__(
            self,
            *,
            filter_type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies which files, folders, and objects to include or exclude when transferring files from source to destination.

            :param filter_type: The type of filter rule to apply. AWS DataSync only supports the SIMPLE_PATTERN rule type.
            :param value: A single filter string that consists of the patterns to include or exclude. The patterns are delimited by "|" (that is, a pipe), for example: ``/folder1|/folder2``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                filter_rule_property = datasync.CfnTask.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65e203eeb807b58bff47b459899f8bc9bef6bf2b7c814c17d1bc93bcb83d481c)
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter_type is not None:
                self._values["filter_type"] = filter_type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The type of filter rule to apply.

            AWS DataSync only supports the SIMPLE_PATTERN rule type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html#cfn-datasync-task-filterrule-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A single filter string that consists of the patterns to include or exclude.

            The patterns are delimited by "|" (that is, a pipe), for example: ``/folder1|/folder2``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html#cfn-datasync-task-filterrule-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnTask.OptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "atime": "atime",
            "bytes_per_second": "bytesPerSecond",
            "gid": "gid",
            "log_level": "logLevel",
            "mtime": "mtime",
            "object_tags": "objectTags",
            "overwrite_mode": "overwriteMode",
            "posix_permissions": "posixPermissions",
            "preserve_deleted_files": "preserveDeletedFiles",
            "preserve_devices": "preserveDevices",
            "security_descriptor_copy_flags": "securityDescriptorCopyFlags",
            "task_queueing": "taskQueueing",
            "transfer_mode": "transferMode",
            "uid": "uid",
            "verify_mode": "verifyMode",
        },
    )
    class OptionsProperty:
        def __init__(
            self,
            *,
            atime: typing.Optional[builtins.str] = None,
            bytes_per_second: typing.Optional[jsii.Number] = None,
            gid: typing.Optional[builtins.str] = None,
            log_level: typing.Optional[builtins.str] = None,
            mtime: typing.Optional[builtins.str] = None,
            object_tags: typing.Optional[builtins.str] = None,
            overwrite_mode: typing.Optional[builtins.str] = None,
            posix_permissions: typing.Optional[builtins.str] = None,
            preserve_deleted_files: typing.Optional[builtins.str] = None,
            preserve_devices: typing.Optional[builtins.str] = None,
            security_descriptor_copy_flags: typing.Optional[builtins.str] = None,
            task_queueing: typing.Optional[builtins.str] = None,
            transfer_mode: typing.Optional[builtins.str] = None,
            uid: typing.Optional[builtins.str] = None,
            verify_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the options that are available to control the behavior of a `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ operation. This behavior includes preserving metadata, such as user ID (UID), group ID (GID), and file permissions; overwriting files in the destination; data integrity verification; and so on.

            A task has a set of default options associated with it. If you don't specify an option in `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ , the default value is used. You can override the default options on each task execution by specifying an overriding ``Options`` value to `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .

            :param atime: A file metadata value that shows the last time that a file was accessed (that is, when the file was read or written to). If you set ``Atime`` to ``BEST_EFFORT`` , AWS DataSync attempts to preserve the original ``Atime`` attribute on all source files (that is, the version before the PREPARING phase). However, ``Atime`` 's behavior is not fully standard across platforms, so AWS DataSync can only do this on a best-effort basis. Default value: ``BEST_EFFORT`` ``BEST_EFFORT`` : Attempt to preserve the per-file ``Atime`` value (recommended). ``NONE`` : Ignore ``Atime`` . .. epigraph:: If ``Atime`` is set to ``BEST_EFFORT`` , ``Mtime`` must be set to ``PRESERVE`` . If ``Atime`` is set to ``NONE`` , ``Mtime`` must also be ``NONE`` .
            :param bytes_per_second: A value that limits the bandwidth used by AWS DataSync . For example, if you want AWS DataSync to use a maximum of 1 MB, set this value to ``1048576`` (=1024*1024).
            :param gid: The group ID (GID) of the file's owners. Default value: ``INT_VALUE`` ``INT_VALUE`` : Preserve the integer value of the user ID (UID) and group ID (GID) (recommended). ``NAME`` : Currently not supported. ``NONE`` : Ignore the UID and GID.
            :param log_level: Specifies the type of logs that DataSync publishes to a Amazon CloudWatch Logs log group. To specify the log group, see `CloudWatchLogGroupArn <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateTask.html#DataSync-CreateTask-request-CloudWatchLogGroupArn>`_ . If you set ``LogLevel`` to ``OFF`` , no logs are published. ``BASIC`` publishes logs on errors for individual files transferred. ``TRANSFER`` publishes logs for every file or object that is transferred and integrity checked.
            :param mtime: A value that indicates the last time that a file was modified (that is, a file was written to) before the PREPARING phase. This option is required for cases when you need to run the same task more than one time. Default value: ``PRESERVE`` ``PRESERVE`` : Preserve original ``Mtime`` (recommended) ``NONE`` : Ignore ``Mtime`` . .. epigraph:: If ``Mtime`` is set to ``PRESERVE`` , ``Atime`` must be set to ``BEST_EFFORT`` . If ``Mtime`` is set to ``NONE`` , ``Atime`` must also be set to ``NONE`` .
            :param object_tags: Specifies whether object tags are preserved when transferring between object storage systems. If you want your DataSync task to ignore object tags, specify the ``NONE`` value. Default Value: ``PRESERVE``
            :param overwrite_mode: Specifies whether data at the destination location should be overwritten or preserved. If set to ``NEVER`` , a destination file for example will not be replaced by a source file (even if the destination file differs from the source file). If you modify files in the destination and you sync the files, you can use this value to protect against overwriting those changes. Some storage classes have specific behaviors that can affect your Amazon S3 storage cost. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .
            :param posix_permissions: A value that determines which users or groups can access a file for a specific purpose, such as reading, writing, or execution of the file. This option should be set only for Network File System (NFS), Amazon EFS, and Amazon S3 locations. For more information about what metadata is copied by DataSync, see `Metadata Copied by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html#metadata-copied>`_ . Default value: ``PRESERVE`` ``PRESERVE`` : Preserve POSIX-style permissions (recommended). ``NONE`` : Ignore permissions. .. epigraph:: AWS DataSync can preserve extant permissions of a source location.
            :param preserve_deleted_files: A value that specifies whether files in the destination that don't exist in the source file system are preserved. This option can affect your storage costs. If your task deletes objects, you might incur minimum storage duration charges for certain storage classes. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ in the *AWS DataSync User Guide* . Default value: ``PRESERVE`` ``PRESERVE`` : Ignore destination files that aren't present in the source (recommended). ``REMOVE`` : Delete destination files that aren't present in the source.
            :param preserve_devices: A value that determines whether AWS DataSync should preserve the metadata of block and character devices in the source file system, and re-create the files with that device name and metadata on the destination. DataSync does not copy the contents of such devices, only the name and metadata. .. epigraph:: AWS DataSync can't sync the actual contents of such devices, because they are nonterminal and don't return an end-of-file (EOF) marker. Default value: ``NONE`` ``NONE`` : Ignore special devices (recommended). ``PRESERVE`` : Preserve character and block device metadata. This option isn't currently supported for Amazon EFS.
            :param security_descriptor_copy_flags: A value that determines which components of the SMB security descriptor are copied from source to destination objects. This value is only used for transfers between SMB and Amazon FSx for Windows File Server locations, or between two Amazon FSx for Windows File Server locations. For more information about how DataSync handles metadata, see `How DataSync Handles Metadata and Special Files <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html>`_ . Default value: ``OWNER_DACL`` ``OWNER_DACL`` : For each copied object, DataSync copies the following metadata: - Object owner. - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object. When you use option, DataSync does NOT copy the NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object. ``OWNER_DACL_SACL`` : For each copied object, DataSync copies the following metadata: - Object owner. - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object. - NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object. Copying SACLs requires granting additional permissions to the Windows user that DataSync uses to access your SMB location. For information about choosing a user that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ . ``NONE`` : None of the SMB security descriptor components are copied. Destination objects are owned by the user that was provided for accessing the destination location. DACLs and SACLs are set based on the destination server’s configuration.
            :param task_queueing: Specifies whether your transfer tasks should be put into a queue during certain scenarios when `running multiple tasks <https://docs.aws.amazon.com/datasync/latest/userguide/run-task.html#running-multiple-tasks>`_ . This is ``ENABLED`` by default.
            :param transfer_mode: A value that determines whether DataSync transfers only the data and metadata that differ between the source and the destination location, or whether DataSync transfers all the content from the source, without comparing it to the destination location. ``CHANGED`` : DataSync copies only data or metadata that is new or different from the source location to the destination location. ``ALL`` : DataSync copies all source location content to the destination, without comparing it to existing content on the destination.
            :param uid: The user ID (UID) of the file's owner. Default value: ``INT_VALUE`` ``INT_VALUE`` : Preserve the integer value of the UID and group ID (GID) (recommended). ``NAME`` : Currently not supported ``NONE`` : Ignore the UID and GID.
            :param verify_mode: A value that determines whether a data integrity verification is performed at the end of a task execution after all data and metadata have been transferred. For more information, see `Configure task settings <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html>`_ . Default value: ``POINT_IN_TIME_CONSISTENT`` ``ONLY_FILES_TRANSFERRED`` (recommended): Perform verification only on files that were transferred. ``POINT_IN_TIME_CONSISTENT`` : Scan the entire source and entire destination at the end of the transfer to verify that the source and destination are fully synchronized. This option isn't supported when transferring to S3 Glacier or S3 Glacier Deep Archive storage classes. ``NONE`` : No additional verification is done at the end of the transfer, but all data transmissions are integrity-checked with checksum verification during the transfer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                options_property = datasync.CfnTask.OptionsProperty(
                    atime="atime",
                    bytes_per_second=123,
                    gid="gid",
                    log_level="logLevel",
                    mtime="mtime",
                    object_tags="objectTags",
                    overwrite_mode="overwriteMode",
                    posix_permissions="posixPermissions",
                    preserve_deleted_files="preserveDeletedFiles",
                    preserve_devices="preserveDevices",
                    security_descriptor_copy_flags="securityDescriptorCopyFlags",
                    task_queueing="taskQueueing",
                    transfer_mode="transferMode",
                    uid="uid",
                    verify_mode="verifyMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06911fffe11f38d6c882e5bd46c116d7504b898861312faed8368f48883087f4)
                check_type(argname="argument atime", value=atime, expected_type=type_hints["atime"])
                check_type(argname="argument bytes_per_second", value=bytes_per_second, expected_type=type_hints["bytes_per_second"])
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
                check_type(argname="argument mtime", value=mtime, expected_type=type_hints["mtime"])
                check_type(argname="argument object_tags", value=object_tags, expected_type=type_hints["object_tags"])
                check_type(argname="argument overwrite_mode", value=overwrite_mode, expected_type=type_hints["overwrite_mode"])
                check_type(argname="argument posix_permissions", value=posix_permissions, expected_type=type_hints["posix_permissions"])
                check_type(argname="argument preserve_deleted_files", value=preserve_deleted_files, expected_type=type_hints["preserve_deleted_files"])
                check_type(argname="argument preserve_devices", value=preserve_devices, expected_type=type_hints["preserve_devices"])
                check_type(argname="argument security_descriptor_copy_flags", value=security_descriptor_copy_flags, expected_type=type_hints["security_descriptor_copy_flags"])
                check_type(argname="argument task_queueing", value=task_queueing, expected_type=type_hints["task_queueing"])
                check_type(argname="argument transfer_mode", value=transfer_mode, expected_type=type_hints["transfer_mode"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
                check_type(argname="argument verify_mode", value=verify_mode, expected_type=type_hints["verify_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if atime is not None:
                self._values["atime"] = atime
            if bytes_per_second is not None:
                self._values["bytes_per_second"] = bytes_per_second
            if gid is not None:
                self._values["gid"] = gid
            if log_level is not None:
                self._values["log_level"] = log_level
            if mtime is not None:
                self._values["mtime"] = mtime
            if object_tags is not None:
                self._values["object_tags"] = object_tags
            if overwrite_mode is not None:
                self._values["overwrite_mode"] = overwrite_mode
            if posix_permissions is not None:
                self._values["posix_permissions"] = posix_permissions
            if preserve_deleted_files is not None:
                self._values["preserve_deleted_files"] = preserve_deleted_files
            if preserve_devices is not None:
                self._values["preserve_devices"] = preserve_devices
            if security_descriptor_copy_flags is not None:
                self._values["security_descriptor_copy_flags"] = security_descriptor_copy_flags
            if task_queueing is not None:
                self._values["task_queueing"] = task_queueing
            if transfer_mode is not None:
                self._values["transfer_mode"] = transfer_mode
            if uid is not None:
                self._values["uid"] = uid
            if verify_mode is not None:
                self._values["verify_mode"] = verify_mode

        @builtins.property
        def atime(self) -> typing.Optional[builtins.str]:
            '''A file metadata value that shows the last time that a file was accessed (that is, when the file was read or written to).

            If you set ``Atime`` to ``BEST_EFFORT`` , AWS DataSync attempts to preserve the original ``Atime`` attribute on all source files (that is, the version before the PREPARING phase). However, ``Atime`` 's behavior is not fully standard across platforms, so AWS DataSync can only do this on a best-effort basis.

            Default value: ``BEST_EFFORT``

            ``BEST_EFFORT`` : Attempt to preserve the per-file ``Atime`` value (recommended).

            ``NONE`` : Ignore ``Atime`` .
            .. epigraph::

               If ``Atime`` is set to ``BEST_EFFORT`` , ``Mtime`` must be set to ``PRESERVE`` .

               If ``Atime`` is set to ``NONE`` , ``Mtime`` must also be ``NONE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-atime
            '''
            result = self._values.get("atime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bytes_per_second(self) -> typing.Optional[jsii.Number]:
            '''A value that limits the bandwidth used by AWS DataSync .

            For example, if you want AWS DataSync to use a maximum of 1 MB, set this value to ``1048576`` (=1024*1024).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-bytespersecond
            '''
            result = self._values.get("bytes_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gid(self) -> typing.Optional[builtins.str]:
            '''The group ID (GID) of the file's owners.

            Default value: ``INT_VALUE``

            ``INT_VALUE`` : Preserve the integer value of the user ID (UID) and group ID (GID) (recommended).

            ``NAME`` : Currently not supported.

            ``NONE`` : Ignore the UID and GID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of logs that DataSync publishes to a Amazon CloudWatch Logs log group.

            To specify the log group, see `CloudWatchLogGroupArn <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateTask.html#DataSync-CreateTask-request-CloudWatchLogGroupArn>`_ .

            If you set ``LogLevel`` to ``OFF`` , no logs are published. ``BASIC`` publishes logs on errors for individual files transferred. ``TRANSFER`` publishes logs for every file or object that is transferred and integrity checked.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mtime(self) -> typing.Optional[builtins.str]:
            '''A value that indicates the last time that a file was modified (that is, a file was written to) before the PREPARING phase.

            This option is required for cases when you need to run the same task more than one time.

            Default value: ``PRESERVE``

            ``PRESERVE`` : Preserve original ``Mtime`` (recommended)

            ``NONE`` : Ignore ``Mtime`` .
            .. epigraph::

               If ``Mtime`` is set to ``PRESERVE`` , ``Atime`` must be set to ``BEST_EFFORT`` .

               If ``Mtime`` is set to ``NONE`` , ``Atime`` must also be set to ``NONE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-mtime
            '''
            result = self._values.get("mtime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_tags(self) -> typing.Optional[builtins.str]:
            '''Specifies whether object tags are preserved when transferring between object storage systems.

            If you want your DataSync task to ignore object tags, specify the ``NONE`` value.

            Default Value: ``PRESERVE``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-objecttags
            '''
            result = self._values.get("object_tags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether data at the destination location should be overwritten or preserved.

            If set to ``NEVER`` , a destination file for example will not be replaced by a source file (even if the destination file differs from the source file). If you modify files in the destination and you sync the files, you can use this value to protect against overwriting those changes.

            Some storage classes have specific behaviors that can affect your Amazon S3 storage cost. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-overwritemode
            '''
            result = self._values.get("overwrite_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def posix_permissions(self) -> typing.Optional[builtins.str]:
            '''A value that determines which users or groups can access a file for a specific purpose, such as reading, writing, or execution of the file.

            This option should be set only for Network File System (NFS), Amazon EFS, and Amazon S3 locations. For more information about what metadata is copied by DataSync, see `Metadata Copied by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html#metadata-copied>`_ .

            Default value: ``PRESERVE``

            ``PRESERVE`` : Preserve POSIX-style permissions (recommended).

            ``NONE`` : Ignore permissions.
            .. epigraph::

               AWS DataSync can preserve extant permissions of a source location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-posixpermissions
            '''
            result = self._values.get("posix_permissions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preserve_deleted_files(self) -> typing.Optional[builtins.str]:
            '''A value that specifies whether files in the destination that don't exist in the source file system are preserved.

            This option can affect your storage costs. If your task deletes objects, you might incur minimum storage duration charges for certain storage classes. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ in the *AWS DataSync User Guide* .

            Default value: ``PRESERVE``

            ``PRESERVE`` : Ignore destination files that aren't present in the source (recommended).

            ``REMOVE`` : Delete destination files that aren't present in the source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-preservedeletedfiles
            '''
            result = self._values.get("preserve_deleted_files")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preserve_devices(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether AWS DataSync should preserve the metadata of block and character devices in the source file system, and re-create the files with that device name and metadata on the destination.

            DataSync does not copy the contents of such devices, only the name and metadata.
            .. epigraph::

               AWS DataSync can't sync the actual contents of such devices, because they are nonterminal and don't return an end-of-file (EOF) marker.

            Default value: ``NONE``

            ``NONE`` : Ignore special devices (recommended).

            ``PRESERVE`` : Preserve character and block device metadata. This option isn't currently supported for Amazon EFS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-preservedevices
            '''
            result = self._values.get("preserve_devices")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_descriptor_copy_flags(self) -> typing.Optional[builtins.str]:
            '''A value that determines which components of the SMB security descriptor are copied from source to destination objects.

            This value is only used for transfers between SMB and Amazon FSx for Windows File Server locations, or between two Amazon FSx for Windows File Server locations. For more information about how DataSync handles metadata, see `How DataSync Handles Metadata and Special Files <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html>`_ .

            Default value: ``OWNER_DACL``

            ``OWNER_DACL`` : For each copied object, DataSync copies the following metadata:

            - Object owner.
            - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object.

            When you use option, DataSync does NOT copy the NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object.

            ``OWNER_DACL_SACL`` : For each copied object, DataSync copies the following metadata:

            - Object owner.
            - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object.
            - NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object.

            Copying SACLs requires granting additional permissions to the Windows user that DataSync uses to access your SMB location. For information about choosing a user that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .

            ``NONE`` : None of the SMB security descriptor components are copied. Destination objects are owned by the user that was provided for accessing the destination location. DACLs and SACLs are set based on the destination server’s configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-securitydescriptorcopyflags
            '''
            result = self._values.get("security_descriptor_copy_flags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def task_queueing(self) -> typing.Optional[builtins.str]:
            '''Specifies whether your transfer tasks should be put into a queue during certain scenarios when `running multiple tasks <https://docs.aws.amazon.com/datasync/latest/userguide/run-task.html#running-multiple-tasks>`_ . This is ``ENABLED`` by default.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-taskqueueing
            '''
            result = self._values.get("task_queueing")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transfer_mode(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether DataSync transfers only the data and metadata that differ between the source and the destination location, or whether DataSync transfers all the content from the source, without comparing it to the destination location.

            ``CHANGED`` : DataSync copies only data or metadata that is new or different from the source location to the destination location.

            ``ALL`` : DataSync copies all source location content to the destination, without comparing it to existing content on the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-transfermode
            '''
            result = self._values.get("transfer_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uid(self) -> typing.Optional[builtins.str]:
            '''The user ID (UID) of the file's owner.

            Default value: ``INT_VALUE``

            ``INT_VALUE`` : Preserve the integer value of the UID and group ID (GID) (recommended).

            ``NAME`` : Currently not supported

            ``NONE`` : Ignore the UID and GID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def verify_mode(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether a data integrity verification is performed at the end of a task execution after all data and metadata have been transferred.

            For more information, see `Configure task settings <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html>`_ .

            Default value: ``POINT_IN_TIME_CONSISTENT``

            ``ONLY_FILES_TRANSFERRED`` (recommended): Perform verification only on files that were transferred.

            ``POINT_IN_TIME_CONSISTENT`` : Scan the entire source and entire destination at the end of the transfer to verify that the source and destination are fully synchronized. This option isn't supported when transferring to S3 Glacier or S3 Glacier Deep Archive storage classes.

            ``NONE`` : No additional verification is done at the end of the transfer, but all data transmissions are integrity-checked with checksum verification during the transfer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-verifymode
            '''
            result = self._values.get("verify_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_datasync.CfnTask.TaskScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression"},
    )
    class TaskScheduleProperty:
        def __init__(self, *, schedule_expression: builtins.str) -> None:
            '''Specifies the schedule you want your task to use for repeated executions.

            For more information, see `Schedule Expressions for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ .

            :param schedule_expression: A cron expression that specifies when AWS DataSync initiates a scheduled transfer from a source to a destination location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_datasync as datasync
                
                task_schedule_property = datasync.CfnTask.TaskScheduleProperty(
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__daaf938d2193de36be5eb8a578bb6067dc5c1b0d33cc11cccca4de72f90d9f6c)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule_expression": schedule_expression,
            }

        @builtins.property
        def schedule_expression(self) -> builtins.str:
            '''A cron expression that specifies when AWS DataSync initiates a scheduled transfer from a source to a destination location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskschedule.html#cfn-datasync-task-taskschedule-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            assert result is not None, "Required property 'schedule_expression' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_datasync.CfnTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_location_arn": "destinationLocationArn",
        "source_location_arn": "sourceLocationArn",
        "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
        "excludes": "excludes",
        "includes": "includes",
        "name": "name",
        "options": "options",
        "schedule": "schedule",
        "tags": "tags",
    },
)
class CfnTaskProps:
    def __init__(
        self,
        *,
        destination_location_arn: builtins.str,
        source_location_arn: builtins.str,
        cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
        excludes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        includes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union[typing.Union[CfnTask.OptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        schedule: typing.Optional[typing.Union[typing.Union[CfnTask.TaskScheduleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTask``.

        :param destination_location_arn: The Amazon Resource Name (ARN) of an AWS storage resource's location.
        :param source_location_arn: The Amazon Resource Name (ARN) of the source location for the task.
        :param cloud_watch_log_group_arn: The Amazon Resource Name (ARN) of the Amazon CloudWatch log group that is used to monitor and log events in the task. For more information about how to use CloudWatch Logs with DataSync, see `Monitoring Your Task <https://docs.aws.amazon.com/datasync/latest/userguide/monitor-datasync.html#cloudwatchlogs>`_ in the *AWS DataSync User Guide.* For more information about these groups, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ in the *Amazon CloudWatch Logs User Guide* .
        :param excludes: Specifies a list of filter rules that exclude specific data during your transfer. For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param includes: Specifies a list of filter rules that include specific data during your transfer. For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param name: The name of a task. This value is a text reference that is used to identify the task in the console.
        :param options: Specifies the configuration options for a task. Some options include preserving file or object metadata and verifying data integrity. You can also override these options before starting an individual run of a task (also known as a *task execution* ). For more information, see `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .
        :param schedule: Specifies a schedule used to periodically transfer files from a source to a destination location. The schedule should be specified in UTC time. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .
        :param tags: Specifies the tags that you want to apply to the Amazon Resource Name (ARN) representing the task. *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_datasync as datasync
            
            cfn_task_props = datasync.CfnTaskProps(
                destination_location_arn="destinationLocationArn",
                source_location_arn="sourceLocationArn",
            
                # the properties below are optional
                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                excludes=[datasync.CfnTask.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )],
                includes=[datasync.CfnTask.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )],
                name="name",
                options=datasync.CfnTask.OptionsProperty(
                    atime="atime",
                    bytes_per_second=123,
                    gid="gid",
                    log_level="logLevel",
                    mtime="mtime",
                    object_tags="objectTags",
                    overwrite_mode="overwriteMode",
                    posix_permissions="posixPermissions",
                    preserve_deleted_files="preserveDeletedFiles",
                    preserve_devices="preserveDevices",
                    security_descriptor_copy_flags="securityDescriptorCopyFlags",
                    task_queueing="taskQueueing",
                    transfer_mode="transferMode",
                    uid="uid",
                    verify_mode="verifyMode"
                ),
                schedule=datasync.CfnTask.TaskScheduleProperty(
                    schedule_expression="scheduleExpression"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce887b5075af1d1a50f94b91f518b2d36bd5976b4be71e96439938bdd0f5ff2e)
            check_type(argname="argument destination_location_arn", value=destination_location_arn, expected_type=type_hints["destination_location_arn"])
            check_type(argname="argument source_location_arn", value=source_location_arn, expected_type=type_hints["source_location_arn"])
            check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_location_arn": destination_location_arn,
            "source_location_arn": source_location_arn,
        }
        if cloud_watch_log_group_arn is not None:
            self._values["cloud_watch_log_group_arn"] = cloud_watch_log_group_arn
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes
        if name is not None:
            self._values["name"] = name
        if options is not None:
            self._values["options"] = options
        if schedule is not None:
            self._values["schedule"] = schedule
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of an AWS storage resource's location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-destinationlocationarn
        '''
        result = self._values.get("destination_location_arn")
        assert result is not None, "Required property 'destination_location_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the source location for the task.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-sourcelocationarn
        '''
        result = self._values.get("source_location_arn")
        assert result is not None, "Required property 'source_location_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon CloudWatch log group that is used to monitor and log events in the task.

        For more information about how to use CloudWatch Logs with DataSync, see `Monitoring Your Task <https://docs.aws.amazon.com/datasync/latest/userguide/monitor-datasync.html#cloudwatchlogs>`_ in the *AWS DataSync User Guide.*

        For more information about these groups, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ in the *Amazon CloudWatch Logs User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-cloudwatchloggrouparn
        '''
        result = self._values.get("cloud_watch_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excludes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTask.FilterRuleProperty, _IResolvable_a771d0ef]]]]:
        '''Specifies a list of filter rules that exclude specific data during your transfer.

        For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-excludes
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTask.FilterRuleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def includes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTask.FilterRuleProperty, _IResolvable_a771d0ef]]]]:
        '''Specifies a list of filter rules that include specific data during your transfer.

        For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTask.FilterRuleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a task.

        This value is a text reference that is used to identify the task in the console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[CfnTask.OptionsProperty, _IResolvable_a771d0ef]]:
        '''Specifies the configuration options for a task. Some options include preserving file or object metadata and verifying data integrity.

        You can also override these options before starting an individual run of a task (also known as a *task execution* ). For more information, see `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[CfnTask.OptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[CfnTask.TaskScheduleProperty, _IResolvable_a771d0ef]]:
        '''Specifies a schedule used to periodically transfer files from a source to a destination location.

        The schedule should be specified in UTC time. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[CfnTask.TaskScheduleProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Specifies the tags that you want to apply to the Amazon Resource Name (ARN) representing the task.

        *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAgent",
    "CfnAgentProps",
    "CfnLocationEFS",
    "CfnLocationEFSProps",
    "CfnLocationFSxLustre",
    "CfnLocationFSxLustreProps",
    "CfnLocationFSxONTAP",
    "CfnLocationFSxONTAPProps",
    "CfnLocationFSxOpenZFS",
    "CfnLocationFSxOpenZFSProps",
    "CfnLocationFSxWindows",
    "CfnLocationFSxWindowsProps",
    "CfnLocationHDFS",
    "CfnLocationHDFSProps",
    "CfnLocationNFS",
    "CfnLocationNFSProps",
    "CfnLocationObjectStorage",
    "CfnLocationObjectStorageProps",
    "CfnLocationS3",
    "CfnLocationS3Props",
    "CfnLocationSMB",
    "CfnLocationSMBProps",
    "CfnStorageSystem",
    "CfnStorageSystemProps",
    "CfnTask",
    "CfnTaskProps",
]

publication.publish()

def _typecheckingstub__40bc48416d05a3c3798c480bd2f171f08d8a07e79853a97bb307684e0ea877bd(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    activation_key: typing.Optional[builtins.str] = None,
    agent_name: typing.Optional[builtins.str] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fac63d091edc871757ceb6b42d8d16ec0e0f5ed142f2819463db008241e0fa(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c98969645c2929b5277accfc3b22b59fcb0edf7737b384eb8ea319ebbdbbcfe(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855ee5b59f119637d4b3a87aaeb01c689211b340948ad9244c252a429e716251(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebc85eba53bd252bd30db3d4c49f02e548604de36e7bacdde94c0d0eacbc6c1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f381110d1ada03ebd723605ebffd98363d0af0827baf314dc81e64cf2e2571(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabd9b71947098dba7058d8316d41a3dbeced628b5561dd305e996da698812ee(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d631d58bf8f884042ad043282b84a5ad556ef004d3c0bd70353d8b6a845b5127(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5d239366e36c20331a336f351cd02f2e7bf390c150321a0edaaf99d9674858(
    *,
    activation_key: typing.Optional[builtins.str] = None,
    agent_name: typing.Optional[builtins.str] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc162613eb797739f51c27be788dbee2cca8a981bb5b5606c69ddb389349fe3(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    ec2_config: typing.Union[typing.Union[CfnLocationEFS.Ec2ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    access_point_arn: typing.Optional[builtins.str] = None,
    efs_filesystem_arn: typing.Optional[builtins.str] = None,
    file_system_access_role_arn: typing.Optional[builtins.str] = None,
    in_transit_encryption: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6445c297e92df989cc02841ee3cec279cac26038774c8bb67b7ae01298ab040c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00dc83501a5f304f9996698254823a75ab287b2e681691e3e2f7aebd9113743(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d81363b55f67611c7312d9c1e71c9a726892d9884f7b1e8dc12ca77ab31a359(
    value: typing.Union[CfnLocationEFS.Ec2ConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749c58e7fecfb149d42c2ef0b7c983122358638facdc1343d6a2be7166b18c74(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e138dbcc026bb9bc8aebf11eece197f9e9bdb7e57c230dfbf617e9353268af72(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7d2471216a8beac6dde92a009e1142d4db21addc1eed1e16760e8bca2ac836(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2e1c32665fb4f3d90df0ee53d5bfa764f6444aa3593805e8437a42627af188(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d9b09853b2663323c4ddf4e98d501f0b5eca8e58e36dec14ceb2c3fbabe6be(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db60c61de85615884ad364040e6c0ce7a82dd368a5227be71985cdb724453a1(
    *,
    security_group_arns: typing.Sequence[builtins.str],
    subnet_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed2e9e823f1b413430cee26b90b5675f99c28f45ff4121afdf9c69d002cb600(
    *,
    ec2_config: typing.Union[typing.Union[CfnLocationEFS.Ec2ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    access_point_arn: typing.Optional[builtins.str] = None,
    efs_filesystem_arn: typing.Optional[builtins.str] = None,
    file_system_access_role_arn: typing.Optional[builtins.str] = None,
    in_transit_encryption: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd32d83f0c3b357d68a9f963e8a45f21075c64a0ab2e40e6196531d5d252ae87(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    security_group_arns: typing.Sequence[builtins.str],
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c6c7b5beeff0929ad128a7f973a0a858e3b83a565920168a323ec0bec4b9b7(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d8def9336950dd9eb5cbc2386481f66a0d2d9bbd8ae97bf224509e6528f10c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bfd375e78fc94425db568200ec70706da862bafb0e55ce2e757fb18ea7f4d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe59799dabf0ad2068f48001f36299770df58be45fc2155ea071b7445a9e471(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8658f048c47a9207d282569b549cdadb52d74cd861bd7ae476939f25ea93609a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792275b282f304487c5a4b06403a199ab68d38b462ec9f94741c1bfd9fa82155(
    *,
    security_group_arns: typing.Sequence[builtins.str],
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c87647dd911c3e60e1a74bcab6e1dfdb8554bb842fea3f9b1c2305615d574f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    security_group_arns: typing.Sequence[builtins.str],
    storage_virtual_machine_arn: builtins.str,
    protocol: typing.Optional[typing.Union[typing.Union[CfnLocationFSxONTAP.ProtocolProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18edd30a179abaf9d3c41e38abbea11345de5e46f2bd5930f015d96c5aeeab7(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acba653484180997668246fa72329c36723e18f8fe0533ea6b1f200176a8a52f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b95aee6a95daee3c1284cd80c24423e751f2cd256c6b4d3091df71e2af93728(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71be64b1fa6e8590cba70c6190c0c0373b88d4ec729addafffc4ec2ef5e76eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a673de5207486b5cf52ce87c6880b61b5cc8c8f923e5d26d1eddb071d438be(
    value: typing.Optional[typing.Union[CfnLocationFSxONTAP.ProtocolProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6005a208092b0b882059f89195765eee42f4a89f41ec18b1a9d3cb424d8f5b69(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69421f575c92d98338eb8fb55467c9f226d5f0db895550ec04c2af1d47bdfc63(
    *,
    mount_options: typing.Union[typing.Union[CfnLocationFSxONTAP.NfsMountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5373a064e61da2c55c153af08d4c6dec6ee9178d25765b02ae65cbc73501cc(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0857b642acee602478ea1a63c3799bf12ae1581f0e197285ca7d321640557c(
    *,
    nfs: typing.Optional[typing.Union[typing.Union[CfnLocationFSxONTAP.NFSProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    smb: typing.Optional[typing.Union[typing.Union[CfnLocationFSxONTAP.SMBProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be45210dbec0f4a494cbc2d958f8c1464c4fd85e40155f60dbde82bfcd7b2fa(
    *,
    mount_options: typing.Union[typing.Union[CfnLocationFSxONTAP.SmbMountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    password: builtins.str,
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c40acf2ff035e2e8f122fdee9288ee483b4c6f45088e5101eee443a2e8114f(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c4f29b9e1a05ef19d9873052161a00c3c2687d6a9aacbec31e076ba650f89c(
    *,
    security_group_arns: typing.Sequence[builtins.str],
    storage_virtual_machine_arn: builtins.str,
    protocol: typing.Optional[typing.Union[typing.Union[CfnLocationFSxONTAP.ProtocolProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50927092fddbeca2a5071f8416224612501feb5a2839215d5a1359b7019eeae5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    protocol: typing.Union[typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    security_group_arns: typing.Sequence[builtins.str],
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73678c93e26d3b543c63bb000267f1374699faac6a88e474a79dd56ca30c7992(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6dff8cec29c326569ac68c2a3281bc54416bf6713569b4df7dc78c2dc0eea45(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08861b23aa64937ddb506fdf3ae6c77efb03578bffd65c7a88d3f0e872c51210(
    value: typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434f123f3cc99d3e11a864de10add1c62f723eb7026130785a4028bb83a5f47c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c310c478a6c1389ca2127db9404c753fc0b9c9f1a38ac7558510f6f0ec6bd379(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702768cbd42a27cc1ca27b968c43405883cc9bf5a7b6950b4314eb3fa2bf4bbe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075207572b6e79a5e25670a0322d63430f8846efb423875489b22d6c21c6d36b(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80577da58ebbe623c2037b3094ca2863d31f6029ecf9eaded51b58d7953c5a97(
    *,
    mount_options: typing.Union[typing.Union[CfnLocationFSxOpenZFS.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021d831c2a3e37b25d4300be9f4bf657d230cdc873806952db54ef7e6e2d2e88(
    *,
    nfs: typing.Optional[typing.Union[typing.Union[CfnLocationFSxOpenZFS.NFSProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55f455d7c9c6fac0041c26256fb0c102fb58ac3daf594ccd68f263f5eedf0e3(
    *,
    protocol: typing.Union[typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    security_group_arns: typing.Sequence[builtins.str],
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3424d14fff59929204f383f9349cf1fae31500d32c77138b1a7c64bd46b25f5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    security_group_arns: typing.Sequence[builtins.str],
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2849e2934f4dd441e4864a825c17682fa1ebf1c23fc46bf46e67d164c0ae7d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c75a9d3503e984248f3b76356fc7806ab3d4c1b72ed69fba0ea877efa6dd83c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ab167b6a2695f33ce496d3f0d76b5d16316c5583c24b0f4cd4860b179ee71e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a6debb870153f415685fa350adfed0b505df5cfc5ed7857ddb383698ac98bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbb58aa2260ccdd250a7aaca5a31ba4d06af58a24e280310c47dbb6184c95e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0509fa1e7c1076fe0e2030a27933b61ab7b897e814568d9e985f8708d552168(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1e2f82232bc9708abed64ef186170dc3867d2bd45bb3962cf689ee1933369a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79536f03b7b73a6b1464bc6e9348c45514f39cde7ca46bd9e06570e41066142(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3e427b916c9e05c492d78b4aba687d24efe4193c99bd5592a4e19dc25988c2(
    *,
    security_group_arns: typing.Sequence[builtins.str],
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    fsx_filesystem_arn: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f6ef4bb0c9ae5bc8d6f3333813a7bcbb069baf62dc17574d39818bd30e8d2b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    agent_arns: typing.Sequence[builtins.str],
    authentication_type: builtins.str,
    name_nodes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLocationHDFS.NameNodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    block_size: typing.Optional[jsii.Number] = None,
    kerberos_keytab: typing.Optional[builtins.str] = None,
    kerberos_krb5_conf: typing.Optional[builtins.str] = None,
    kerberos_principal: typing.Optional[builtins.str] = None,
    kms_key_provider_uri: typing.Optional[builtins.str] = None,
    qop_configuration: typing.Optional[typing.Union[typing.Union[CfnLocationHDFS.QopConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    replication_factor: typing.Optional[jsii.Number] = None,
    simple_user: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b4a49830a9c24375890fec0bab0309c39044d689e43dec9fa2aaf2767c0b54(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc001038d0023cc64db49f6bd5aba445766be60a409e6dad449f7da8c022705f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168b5df29b93b8ebefdbcbfc7e7fbf03ca05a884c385897828925c7a47c018f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079801bcd8ef86ba2ab9121c13a4487e69a9c4ef80a719cfc03cda267141fcc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7949f1beae555a53a14c60cd4457784030b81c85815059c84c8946fd6433f8(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLocationHDFS.NameNodeProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1ad140fc1986c2663b401a9eb570e6dd303372d8a5c03471a9e70e81c953fa(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2701788ca3c169873a5308f4af822a3cf92f504692b64d6452f51f0299004ae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a6652087b4316c978bee37603c2100d95cdc57a53112ce5e7132c7f672170b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1ac3eed258aab9a691ee3d4f143678ee679fc95810436d29d566eb784af0a2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284429aa3d6990a514e681fc7e188755e3966353968563db5a57631a151dc4d4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09eaeddd6540f54252618401b33394208316430f1b909037e4006982c4ad9dd7(
    value: typing.Optional[typing.Union[CfnLocationHDFS.QopConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae43ff2ca2772f30172d0d2c4dcd2149fd5062c94912c36fd4d78824c7779c6(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d5bce832d5ce55eaba558357da33dcb5a13280da8f1515f4732407161d8192(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f06762d92688779b6ef9fa1406765e978919d1f82c1df21fdee241134f6ba5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b0b45b2c07b77c7ed970ce045db04168be953509519c8b10e71519cfff27be(
    *,
    hostname: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552100dcbe7592582e84a98af9b6b62f7488119783bf6b166029d05eb7efb255(
    *,
    data_transfer_protection: typing.Optional[builtins.str] = None,
    rpc_protection: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99584bc996b49aecfca6efbc3eb837f0530fa9e260a9cb573acee398b52b8fc(
    *,
    agent_arns: typing.Sequence[builtins.str],
    authentication_type: builtins.str,
    name_nodes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLocationHDFS.NameNodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    block_size: typing.Optional[jsii.Number] = None,
    kerberos_keytab: typing.Optional[builtins.str] = None,
    kerberos_krb5_conf: typing.Optional[builtins.str] = None,
    kerberos_principal: typing.Optional[builtins.str] = None,
    kms_key_provider_uri: typing.Optional[builtins.str] = None,
    qop_configuration: typing.Optional[typing.Union[typing.Union[CfnLocationHDFS.QopConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    replication_factor: typing.Optional[jsii.Number] = None,
    simple_user: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edfa9018ee3004925e3bae4da711868f2593454f177d933365112d06b2036653(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    on_prem_config: typing.Union[typing.Union[CfnLocationNFS.OnPremConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    mount_options: typing.Optional[typing.Union[typing.Union[CfnLocationNFS.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a367ea4303fd5de5b7024de97b254527490287e0bd010a1f9a3321a75910264(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f6f39d0fe7ff37baa70fd740189b4019f693ce5ffc64e8bb47ea471f774c96(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286a2d4e7e29bde1f6f20bc92f6bfb2050984a0b871cba1ff0e200b02325b356(
    value: typing.Union[CfnLocationNFS.OnPremConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a91bce482fbb58ed9f74a75c9e1023bc980d00085c55390e1d496979f59496(
    value: typing.Optional[typing.Union[CfnLocationNFS.MountOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499352201816f8a4e3fcdd26e14c2ac853e98fd29340c03544a014d43d872afa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60a5e51319c795366753fa2f0824c39f9fe8ed303464653fc3decb19567a2dc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2706cfd9206cb86a7a9edabf87c147f99f4067816d4ff655617cc7b8799d9723(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6aaec0394de708d3cb0fe1fa4b16e93b76400717fccfc8053ce9588cf7ac935(
    *,
    agent_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41eafc7de2388808e13a420839ef37400f5e9df21865d238fcfb4f10011bfadf(
    *,
    on_prem_config: typing.Union[typing.Union[CfnLocationNFS.OnPremConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    mount_options: typing.Optional[typing.Union[typing.Union[CfnLocationNFS.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a6fd215d00252471bfb683d082f005a7bc74e2b5a891dd2eb9a0541dc8a424(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    agent_arns: typing.Sequence[builtins.str],
    access_key: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    server_certificate: typing.Optional[builtins.str] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    server_port: typing.Optional[jsii.Number] = None,
    server_protocol: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6d250c544d2b1da5f007518162682ca7db336bcba745c05871eb4ef72ace13(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b2f1d00b76586ca028c2448c103a3741dd188a86a9837bbdb3014dd9b0bc0d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1643ff81c32c848efc860cdf7fed986fa0b221abf21f9b7dcefe00c76f8959b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f06bcb4165b4bd531f65bd84d026b9df215dc7204444973eff8dfe0082a4ab(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d911359f2b03d7de9ceda147024231036bb3fb82a3ef93b315c50d0057f6abc2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ef65931ac379ac9bdc8131eee8c7906acf7989759f01072871fe628bfad369(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8e2dd675132944df1a24c24fbfa7880a5ed587c5b637005f6d24188f2d290f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df89ec0f9132f1b4a112efc62a23948da674fe38fc10353387f7c762f35a0a41(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34e3c141cd60920163b890c4ba6f66277289fcb3545eac4c594d7cc40b4285e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2adac1cc0a4dbffff03e09cf20a9dfb39e3304bad59875f87a521ff9d1a5f47(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c3b44d5726feb22ae4dc222ae27fae16cd81ddb98d4d830e46baeef7a106f8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2d2de26a1b1ab4df2e89b7711896433b90b7c9b00ea16b8d51d138c11ad8de(
    *,
    agent_arns: typing.Sequence[builtins.str],
    access_key: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    server_certificate: typing.Optional[builtins.str] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    server_port: typing.Optional[jsii.Number] = None,
    server_protocol: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bebb2347f0afeb7e697def1cff9b241efd883d908d116d175d8696f35c7c2a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    s3_config: typing.Union[typing.Union[CfnLocationS3.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    s3_bucket_arn: typing.Optional[builtins.str] = None,
    s3_storage_class: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b29abbcddb92aa49d3bab5eb0003737a67a4e4c724c317756df1e7bd7aa9c26(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a62996d286811bed9ad89bd3c622a3cb0ca6b76f0480020fd79d513c668f8f7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df70c971ec20390e87ae208e2bd8e9ccf0e0a964475d17879981cd3a43fe56b(
    value: typing.Union[CfnLocationS3.S3ConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883b1276eefeb8b5fb1e78baf4e0d547871f893da1a2e850029e8617df4a4c74(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c59da0f6d9be5bb7012775e4f14d902185b88cf2a54a5c9a9cb029ab9eac931(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85d6a1a9e0c0595d3ece72d2a405c8a10d7ecf2b210c36e3d7832f83d6fd74a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9878f7df7fbcbb5ef6bbc29012ecaa83910692295323848c04ae4188d0c926(
    *,
    bucket_access_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbeaa280acbad6d9c18a975bebfa32477a2fad7aed60ed19eeaa8b269f8a159(
    *,
    s3_config: typing.Union[typing.Union[CfnLocationS3.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    s3_bucket_arn: typing.Optional[builtins.str] = None,
    s3_storage_class: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a85bfbe3eed46263ccdb15ef31da1b91298ceb8c58830289e3941ab6808c72(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    agent_arns: typing.Sequence[builtins.str],
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[typing.Union[typing.Union[CfnLocationSMB.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    password: typing.Optional[builtins.str] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0aca94953e4cd5e100f9ecebc6b561181eab3417857ed5bb50fb9c79c2cb2be(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a9d35dbc35634edd8998eb9caa294d8c691ec483a159fbd3034c6b73f75dad(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db9129d5ab70beaf0fb00d39911c0706c25345a3eeca9a2dd8c8c98a8908de7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de05707f447a2c173f2de62ce95604e01356d115fc8937210fd2c9a2d615841(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ce3150f921c2e07d4c0f92292644b56d98ef8d879d79742ca262f5a7150c27(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb30696d6be749e067285f47afc3da9ad3bbfae60c1c7982176aa86c25f50f0(
    value: typing.Optional[typing.Union[CfnLocationSMB.MountOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042547a34873640a9d27a07c9d4be4b112f6032d9e549af489c4ef9656285f67(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca635bb23b6e1a9313ace5e1345ab4abc7a64a7fd7fca0d7e0e1edb8265b98b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7917e47ea9d1726e38d244ae48e200d276e1b28608e48444f8afde41b04b2b50(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e27b74819a9647ebadd5a97b0afc22318515fb5d7293f7c855f6bdba1055ca9(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6646299a18353ff73b3655b548db8b72ee415cb8c806d919574a11b95078d18(
    *,
    agent_arns: typing.Sequence[builtins.str],
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[typing.Union[typing.Union[CfnLocationSMB.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    password: typing.Optional[builtins.str] = None,
    server_hostname: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3608275a7dd972e375d31feddf14c4fcae4b3b23888af0ab07655707aa36853d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    agent_arns: typing.Sequence[builtins.str],
    server_configuration: typing.Union[typing.Union[CfnStorageSystem.ServerConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    system_type: builtins.str,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    server_credentials: typing.Optional[typing.Union[typing.Union[CfnStorageSystem.ServerCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3229fcb53782f9f7814acf8253a6f76ab10964f9c4c80901a4141ec782c6b03(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e0492cac30c9dc63bc68328ce32c902c1cad2ccf512a420547782e37b41400(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c8a6363f0a1c5e95eed9a5bed8fbabf5ebf6b66a731538b3fa02805b69b914(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c922863e5e839113af66531c623ab5668c7ad9d8bac946c378e192c94732f64b(
    value: typing.Union[CfnStorageSystem.ServerConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38948210ba65e5dae35556624b88670fbbfd4b71ea48fcd0ebf88940217b117e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d2e4d06cdf10cd401925c755f5b1008f82a92145843341458c4582784458b2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3963efddbe63c1cab58d227cd99237b0b28e138cc02091ebc1325e9d8477be49(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be26c384ba2ba40e30f1fc04ace93633361b945bfe39d6a60d08e493a32a1aff(
    value: typing.Optional[typing.Union[CfnStorageSystem.ServerCredentialsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54d1ed122670eaf4422d3003bbcaebfde21be61237756fe6dc86a9fa4fcb846(
    *,
    server_hostname: builtins.str,
    server_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271ca39e9b59361434ea87ec8de3ebae5e90c64bf1bf96f3c1d1e1e91e4fd0fb(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b7193913f0014df0f9eeadb500bd4415e4c28a24f8fbc0398081477692709a(
    *,
    agent_arns: typing.Sequence[builtins.str],
    server_configuration: typing.Union[typing.Union[CfnStorageSystem.ServerConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    system_type: builtins.str,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    server_credentials: typing.Optional[typing.Union[typing.Union[CfnStorageSystem.ServerCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a249420f561a6f9523fafef5cccaa91658a60eac07bf2c98ccb8c8e42cee98a9(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    destination_location_arn: builtins.str,
    source_location_arn: builtins.str,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    excludes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    includes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    name: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[typing.Union[CfnTask.OptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    schedule: typing.Optional[typing.Union[typing.Union[CfnTask.TaskScheduleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b634717b9327800846f83ccf76e2fc0ea89aed34422b1c8f8c89373e8ed0989(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946e93faf8a19ca4126e3ee45ef218c32c4aa91042b8b57e4e64efa8853c5cc7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b5a796bbd0fa27501cedff341336796d679606fca290a513e4ae67dd9c9414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fda068271936dc842fee855ee4b84fd2e02fcb4e13baa4dc457b467a0d1187(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4613fba08fe6907fb92ab247241ae851c4f34fff1a82d210b3cb5e8edb827bfb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab290047311d9ecac04ad6a1e93f70deda93ee97e08258ff96884d5a406e8949(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTask.FilterRuleProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3b44f184cb844de208a74a298780e976f85cd35fc6894709af192949247a5d(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTask.FilterRuleProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ef1b40a3983d238fc61334307e091b207d0581a5d1303bf7a650c6059a4d57(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b1be93fc55e5f12af3a464c502b3fc10994908bda89af8fb1abf67b7fcf7d2(
    value: typing.Optional[typing.Union[CfnTask.OptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2391c8b26899243674d4d39e60701ebb4cef23891bc8c014b371e3dcaa7fcdf(
    value: typing.Optional[typing.Union[CfnTask.TaskScheduleProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e203eeb807b58bff47b459899f8bc9bef6bf2b7c814c17d1bc93bcb83d481c(
    *,
    filter_type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06911fffe11f38d6c882e5bd46c116d7504b898861312faed8368f48883087f4(
    *,
    atime: typing.Optional[builtins.str] = None,
    bytes_per_second: typing.Optional[jsii.Number] = None,
    gid: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    mtime: typing.Optional[builtins.str] = None,
    object_tags: typing.Optional[builtins.str] = None,
    overwrite_mode: typing.Optional[builtins.str] = None,
    posix_permissions: typing.Optional[builtins.str] = None,
    preserve_deleted_files: typing.Optional[builtins.str] = None,
    preserve_devices: typing.Optional[builtins.str] = None,
    security_descriptor_copy_flags: typing.Optional[builtins.str] = None,
    task_queueing: typing.Optional[builtins.str] = None,
    transfer_mode: typing.Optional[builtins.str] = None,
    uid: typing.Optional[builtins.str] = None,
    verify_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daaf938d2193de36be5eb8a578bb6067dc5c1b0d33cc11cccca4de72f90d9f6c(
    *,
    schedule_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce887b5075af1d1a50f94b91f518b2d36bd5976b4be71e96439938bdd0f5ff2e(
    *,
    destination_location_arn: builtins.str,
    source_location_arn: builtins.str,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    excludes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    includes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    name: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[typing.Union[CfnTask.OptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    schedule: typing.Optional[typing.Union[typing.Union[CfnTask.TaskScheduleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
