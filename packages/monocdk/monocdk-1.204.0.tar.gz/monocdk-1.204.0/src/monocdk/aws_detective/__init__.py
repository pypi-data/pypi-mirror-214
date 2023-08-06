'''
# AWS::Detective Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as detective
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Detective construct libraries](https://constructs.dev/search?q=detective)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Detective resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Detective.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Detective](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Detective.html).

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
class CfnGraph(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_detective.CfnGraph",
):
    '''A CloudFormation ``AWS::Detective::Graph``.

    The ``AWS::Detective::Graph`` resource is an Amazon Detective resource type that creates a Detective behavior graph. The requesting account becomes the administrator account for the behavior graph.

    :cloudformationResource: AWS::Detective::Graph
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_detective as detective
        
        cfn_graph = detective.CfnGraph(self, "MyCfnGraph",
            auto_enable_members=False,
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
        auto_enable_members: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Detective::Graph``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_enable_members: Indicates whether to automatically enable new organization accounts as member accounts in the organization behavior graph. By default, this property is set to ``false`` . If you want to change the value of this property, you must be the Detective administrator for the organization. For more information on setting a Detective administrator account, see `AWS::Detective::OrganizationAdmin <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html>`_
        :param tags: The tag values to assign to the new behavior graph.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c518764be28d6fdb669797aa748d4ecfc82ecb21eca53419397dc4c2cc8c905e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGraphProps(auto_enable_members=auto_enable_members, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0a763ba37985e90d8a45fa6daef3a914e1c83a566d7fb7f6bb7e4e3cbbc7d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8380a3fe2b2a51a42593f439f3a60f49006532441c4655fdcea8fd5ec7f77b2e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The ARN of the new behavior graph.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tag values to assign to the new behavior graph.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html#cfn-detective-graph-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="autoEnableMembers")
    def auto_enable_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether to automatically enable new organization accounts as member accounts in the organization behavior graph.

        By default, this property is set to ``false`` . If you want to change the value of this property, you must be the Detective administrator for the organization. For more information on setting a Detective administrator account, see `AWS::Detective::OrganizationAdmin <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html#cfn-detective-graph-autoenablemembers
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "autoEnableMembers"))

    @auto_enable_members.setter
    def auto_enable_members(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19ffb49922ef1bd973db6d94ecfe021d4b9daa8574089acdcb12a797de63113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoEnableMembers", value)


@jsii.data_type(
    jsii_type="monocdk.aws_detective.CfnGraphProps",
    jsii_struct_bases=[],
    name_mapping={"auto_enable_members": "autoEnableMembers", "tags": "tags"},
)
class CfnGraphProps:
    def __init__(
        self,
        *,
        auto_enable_members: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGraph``.

        :param auto_enable_members: Indicates whether to automatically enable new organization accounts as member accounts in the organization behavior graph. By default, this property is set to ``false`` . If you want to change the value of this property, you must be the Detective administrator for the organization. For more information on setting a Detective administrator account, see `AWS::Detective::OrganizationAdmin <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html>`_
        :param tags: The tag values to assign to the new behavior graph.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_detective as detective
            
            cfn_graph_props = detective.CfnGraphProps(
                auto_enable_members=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f2498f2e348aae5a6310e4b3547638b5c1ed75560e6b9c5cc5c77c34fc9083)
            check_type(argname="argument auto_enable_members", value=auto_enable_members, expected_type=type_hints["auto_enable_members"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_enable_members is not None:
            self._values["auto_enable_members"] = auto_enable_members
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_enable_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether to automatically enable new organization accounts as member accounts in the organization behavior graph.

        By default, this property is set to ``false`` . If you want to change the value of this property, you must be the Detective administrator for the organization. For more information on setting a Detective administrator account, see `AWS::Detective::OrganizationAdmin <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html#cfn-detective-graph-autoenablemembers
        '''
        result = self._values.get("auto_enable_members")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tag values to assign to the new behavior graph.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html#cfn-detective-graph-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGraphProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnMemberInvitation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_detective.CfnMemberInvitation",
):
    '''A CloudFormation ``AWS::Detective::MemberInvitation``.

    The ``AWS::Detective::MemberInvitation`` resource is an Amazon Detective resource type that creates an invitation to join a Detective behavior graph. The administrator account can choose whether to send an email notification of the invitation to the root user email address of the AWS account.

    :cloudformationResource: AWS::Detective::MemberInvitation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_detective as detective
        
        cfn_member_invitation = detective.CfnMemberInvitation(self, "MyCfnMemberInvitation",
            graph_arn="graphArn",
            member_email_address="memberEmailAddress",
            member_id="memberId",
        
            # the properties below are optional
            disable_email_notification=False,
            message="message"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        graph_arn: builtins.str,
        member_email_address: builtins.str,
        member_id: builtins.str,
        disable_email_notification: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Detective::MemberInvitation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param graph_arn: The ARN of the behavior graph to invite the account to contribute data to.
        :param member_email_address: The root user email address of the invited account. If the email address provided is not the root user email address for the provided account, the invitation creation fails.
        :param member_id: The AWS account identifier of the invited account.
        :param disable_email_notification: Whether to send an invitation email to the member account. If set to true, the member account does not receive an invitation email.
        :param message: Customized text to include in the invitation email message.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f71d189903c02589ebf8ad03bd526a7c11114a9f3b052dff426ec9b89321b7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMemberInvitationProps(
            graph_arn=graph_arn,
            member_email_address=member_email_address,
            member_id=member_id,
            disable_email_notification=disable_email_notification,
            message=message,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb62c339bf815b6c8f9aa6736acfe136bddc76ea87446dd4cb3ca6ffdd874a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c9eda357a36fda00554f96f165c3b5a2f1316caa8c7ae0eb92ba241d60d5bbb)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="graphArn")
    def graph_arn(self) -> builtins.str:
        '''The ARN of the behavior graph to invite the account to contribute data to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-grapharn
        '''
        return typing.cast(builtins.str, jsii.get(self, "graphArn"))

    @graph_arn.setter
    def graph_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c21daf1e77d394122a22f9299fb1526fb20d4d3a0dfaa978fab18c4211c0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graphArn", value)

    @builtins.property
    @jsii.member(jsii_name="memberEmailAddress")
    def member_email_address(self) -> builtins.str:
        '''The root user email address of the invited account.

        If the email address provided is not the root user email address for the provided account, the invitation creation fails.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberemailaddress
        '''
        return typing.cast(builtins.str, jsii.get(self, "memberEmailAddress"))

    @member_email_address.setter
    def member_email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3174d4b3374c59280572ce7e307c81258b722200d7e0538222d5baff3127cd3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberEmailAddress", value)

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(self) -> builtins.str:
        '''The AWS account identifier of the invited account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberid
        '''
        return typing.cast(builtins.str, jsii.get(self, "memberId"))

    @member_id.setter
    def member_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c94a6f080e1d8ed5bf679b0b563e58e7641ee684b805b0a5c1120db5fcdce217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberId", value)

    @builtins.property
    @jsii.member(jsii_name="disableEmailNotification")
    def disable_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to send an invitation email to the member account.

        If set to true, the member account does not receive an invitation email.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-disableemailnotification
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "disableEmailNotification"))

    @disable_email_notification.setter
    def disable_email_notification(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24414ab70755e8b91eed46de7f75de0016ff625e5299e6b0bdb1f38c66fba564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableEmailNotification", value)

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> typing.Optional[builtins.str]:
        '''Customized text to include in the invitation email message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-message
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "message"))

    @message.setter
    def message(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac5eac86c5a7127fb9fd022684854af7338137626e854c3e9d39f38e2847320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value)


@jsii.data_type(
    jsii_type="monocdk.aws_detective.CfnMemberInvitationProps",
    jsii_struct_bases=[],
    name_mapping={
        "graph_arn": "graphArn",
        "member_email_address": "memberEmailAddress",
        "member_id": "memberId",
        "disable_email_notification": "disableEmailNotification",
        "message": "message",
    },
)
class CfnMemberInvitationProps:
    def __init__(
        self,
        *,
        graph_arn: builtins.str,
        member_email_address: builtins.str,
        member_id: builtins.str,
        disable_email_notification: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMemberInvitation``.

        :param graph_arn: The ARN of the behavior graph to invite the account to contribute data to.
        :param member_email_address: The root user email address of the invited account. If the email address provided is not the root user email address for the provided account, the invitation creation fails.
        :param member_id: The AWS account identifier of the invited account.
        :param disable_email_notification: Whether to send an invitation email to the member account. If set to true, the member account does not receive an invitation email.
        :param message: Customized text to include in the invitation email message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_detective as detective
            
            cfn_member_invitation_props = detective.CfnMemberInvitationProps(
                graph_arn="graphArn",
                member_email_address="memberEmailAddress",
                member_id="memberId",
            
                # the properties below are optional
                disable_email_notification=False,
                message="message"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8b61ce6d8fad65cb60c8200d72e7b3e377809bc173dfa9ffecb2006b9de1c6)
            check_type(argname="argument graph_arn", value=graph_arn, expected_type=type_hints["graph_arn"])
            check_type(argname="argument member_email_address", value=member_email_address, expected_type=type_hints["member_email_address"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
            check_type(argname="argument disable_email_notification", value=disable_email_notification, expected_type=type_hints["disable_email_notification"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "graph_arn": graph_arn,
            "member_email_address": member_email_address,
            "member_id": member_id,
        }
        if disable_email_notification is not None:
            self._values["disable_email_notification"] = disable_email_notification
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def graph_arn(self) -> builtins.str:
        '''The ARN of the behavior graph to invite the account to contribute data to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-grapharn
        '''
        result = self._values.get("graph_arn")
        assert result is not None, "Required property 'graph_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def member_email_address(self) -> builtins.str:
        '''The root user email address of the invited account.

        If the email address provided is not the root user email address for the provided account, the invitation creation fails.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberemailaddress
        '''
        result = self._values.get("member_email_address")
        assert result is not None, "Required property 'member_email_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def member_id(self) -> builtins.str:
        '''The AWS account identifier of the invited account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberid
        '''
        result = self._values.get("member_id")
        assert result is not None, "Required property 'member_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disable_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to send an invitation email to the member account.

        If set to true, the member account does not receive an invitation email.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-disableemailnotification
        '''
        result = self._values.get("disable_email_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Customized text to include in the invitation email message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-message
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMemberInvitationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnOrganizationAdmin(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_detective.CfnOrganizationAdmin",
):
    '''A CloudFormation ``AWS::Detective::OrganizationAdmin``.

    The ``AWS::Detective::OrganizationAdmin`` resource is an Amazon Detective resource type that designates the Detective administrator account for the organization in the current region. If the account does not have Detective enabled, then this resource enables Detective for that account and creates a new behavior graph.

    :cloudformationResource: AWS::Detective::OrganizationAdmin
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_detective as detective
        
        cfn_organization_admin = detective.CfnOrganizationAdmin(self, "MyCfnOrganizationAdmin",
            account_id="accountId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        account_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Detective::OrganizationAdmin``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_id: The AWS account identifier of the account to designate as the Detective administrator account for the organization.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8cce984a557be3ff2b8d7115d4282c6c3f4f101fae40942fd5e42a35c045eec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnOrganizationAdminProps(account_id=account_id)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09fc59ea7e08cf65091c7d2fc8a2b53d07da2fd577316d5c01be4672a751322b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce5c4c0c9cf39c861670e0693521f0cee64ca8d24d8c2bed648b89037c05d9aa)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrGraphArn")
    def attr_graph_arn(self) -> builtins.str:
        '''The ARN of the behavior graph to invite the account to contribute data to.

        :cloudformationAttribute: GraphArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGraphArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        '''The AWS account identifier of the account to designate as the Detective administrator account for the organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html#cfn-detective-organizationadmin-accountid
        '''
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9639e3f4827d26c529a035f56afa7f6ab58f221dbc3fcb9633b6fc6b26fc31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_detective.CfnOrganizationAdminProps",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId"},
)
class CfnOrganizationAdminProps:
    def __init__(self, *, account_id: builtins.str) -> None:
        '''Properties for defining a ``CfnOrganizationAdmin``.

        :param account_id: The AWS account identifier of the account to designate as the Detective administrator account for the organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_detective as detective
            
            cfn_organization_admin_props = detective.CfnOrganizationAdminProps(
                account_id="accountId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9171c492756ac66ee94a4ebfa027b7ecf96b9be079ce07b6d3325a5ae366bf0)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The AWS account identifier of the account to designate as the Detective administrator account for the organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html#cfn-detective-organizationadmin-accountid
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationAdminProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGraph",
    "CfnGraphProps",
    "CfnMemberInvitation",
    "CfnMemberInvitationProps",
    "CfnOrganizationAdmin",
    "CfnOrganizationAdminProps",
]

publication.publish()

def _typecheckingstub__c518764be28d6fdb669797aa748d4ecfc82ecb21eca53419397dc4c2cc8c905e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    auto_enable_members: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0a763ba37985e90d8a45fa6daef3a914e1c83a566d7fb7f6bb7e4e3cbbc7d6(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8380a3fe2b2a51a42593f439f3a60f49006532441c4655fdcea8fd5ec7f77b2e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19ffb49922ef1bd973db6d94ecfe021d4b9daa8574089acdcb12a797de63113(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f2498f2e348aae5a6310e4b3547638b5c1ed75560e6b9c5cc5c77c34fc9083(
    *,
    auto_enable_members: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f71d189903c02589ebf8ad03bd526a7c11114a9f3b052dff426ec9b89321b7f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    graph_arn: builtins.str,
    member_email_address: builtins.str,
    member_id: builtins.str,
    disable_email_notification: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb62c339bf815b6c8f9aa6736acfe136bddc76ea87446dd4cb3ca6ffdd874a0(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9eda357a36fda00554f96f165c3b5a2f1316caa8c7ae0eb92ba241d60d5bbb(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c21daf1e77d394122a22f9299fb1526fb20d4d3a0dfaa978fab18c4211c0ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3174d4b3374c59280572ce7e307c81258b722200d7e0538222d5baff3127cd3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94a6f080e1d8ed5bf679b0b563e58e7641ee684b805b0a5c1120db5fcdce217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24414ab70755e8b91eed46de7f75de0016ff625e5299e6b0bdb1f38c66fba564(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac5eac86c5a7127fb9fd022684854af7338137626e854c3e9d39f38e2847320(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8b61ce6d8fad65cb60c8200d72e7b3e377809bc173dfa9ffecb2006b9de1c6(
    *,
    graph_arn: builtins.str,
    member_email_address: builtins.str,
    member_id: builtins.str,
    disable_email_notification: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cce984a557be3ff2b8d7115d4282c6c3f4f101fae40942fd5e42a35c045eec(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09fc59ea7e08cf65091c7d2fc8a2b53d07da2fd577316d5c01be4672a751322b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5c4c0c9cf39c861670e0693521f0cee64ca8d24d8c2bed648b89037c05d9aa(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9639e3f4827d26c529a035f56afa7f6ab58f221dbc3fcb9633b6fc6b26fc31c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9171c492756ac66ee94a4ebfa027b7ecf96b9be079ce07b6d3325a5ae366bf0(
    *,
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
