'''
# AWS::IoTSiteWise Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as iotsitewise
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for IoTSiteWise construct libraries](https://constructs.dev/search?q=iotsitewise)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::IoTSiteWise resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTSiteWise.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::IoTSiteWise](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTSiteWise.html).

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
class CfnAccessPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicy",
):
    '''A CloudFormation ``AWS::IoTSiteWise::AccessPolicy``.

    Creates an access policy that grants the specified identity (IAM Identity Center user, IAM Identity Center group, or IAM user) access to the specified AWS IoT SiteWise Monitor portal or project resource.

    :cloudformationResource: AWS::IoTSiteWise::AccessPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotsitewise as iotsitewise
        
        cfn_access_policy = iotsitewise.CfnAccessPolicy(self, "MyCfnAccessPolicy",
            access_policy_identity=iotsitewise.CfnAccessPolicy.AccessPolicyIdentityProperty(
                iam_role=iotsitewise.CfnAccessPolicy.IamRoleProperty(
                    arn="arn"
                ),
                iam_user=iotsitewise.CfnAccessPolicy.IamUserProperty(
                    arn="arn"
                ),
                user=iotsitewise.CfnAccessPolicy.UserProperty(
                    id="id"
                )
            ),
            access_policy_permission="accessPolicyPermission",
            access_policy_resource=iotsitewise.CfnAccessPolicy.AccessPolicyResourceProperty(
                portal=iotsitewise.CfnAccessPolicy.PortalProperty(
                    id="id"
                ),
                project=iotsitewise.CfnAccessPolicy.ProjectProperty(
                    id="id"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        access_policy_identity: typing.Union[typing.Union["CfnAccessPolicy.AccessPolicyIdentityProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        access_policy_permission: builtins.str,
        access_policy_resource: typing.Union[typing.Union["CfnAccessPolicy.AccessPolicyResourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::IoTSiteWise::AccessPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_policy_identity: The identity for this access policy. Choose an IAM Identity Center user, an IAM Identity Center group, or an IAM user.
        :param access_policy_permission: The permission level for this access policy. Choose either a ``ADMINISTRATOR`` or ``VIEWER`` . Note that a project ``ADMINISTRATOR`` is also known as a project owner.
        :param access_policy_resource: The AWS IoT SiteWise Monitor resource for this access policy. Choose either a portal or a project.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16de32dcc1e1492d37e1562f274d1d99ed757cdff877687a168f0a2dcae2b096)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessPolicyProps(
            access_policy_identity=access_policy_identity,
            access_policy_permission=access_policy_permission,
            access_policy_resource=access_policy_resource,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d435e0e58d17676ac3956511658125b4e3fb22f514ba1a4e560e2d3708ed48e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c6800cff407511c4ca03195c29e299b47dbfc3d88532e192b9823f5ae82cd62)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccessPolicyArn")
    def attr_access_policy_arn(self) -> builtins.str:
        '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the access policy, which has the following format.

        ``arn:${Partition}:iotsitewise:${Region}:${Account}:access-policy/${AccessPolicyId}``

        :cloudformationAttribute: AccessPolicyArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccessPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAccessPolicyId")
    def attr_access_policy_id(self) -> builtins.str:
        '''The ID of the access policy.

        :cloudformationAttribute: AccessPolicyId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccessPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="accessPolicyIdentity")
    def access_policy_identity(
        self,
    ) -> typing.Union["CfnAccessPolicy.AccessPolicyIdentityProperty", _IResolvable_a771d0ef]:
        '''The identity for this access policy.

        Choose an IAM Identity Center user, an IAM Identity Center group, or an IAM user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity
        '''
        return typing.cast(typing.Union["CfnAccessPolicy.AccessPolicyIdentityProperty", _IResolvable_a771d0ef], jsii.get(self, "accessPolicyIdentity"))

    @access_policy_identity.setter
    def access_policy_identity(
        self,
        value: typing.Union["CfnAccessPolicy.AccessPolicyIdentityProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd41f887e0e00135b907e31c33cc2d151825693c168faff879176097569863fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPolicyIdentity", value)

    @builtins.property
    @jsii.member(jsii_name="accessPolicyPermission")
    def access_policy_permission(self) -> builtins.str:
        '''The permission level for this access policy.

        Choose either a ``ADMINISTRATOR`` or ``VIEWER`` . Note that a project ``ADMINISTRATOR`` is also known as a project owner.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicypermission
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPolicyPermission"))

    @access_policy_permission.setter
    def access_policy_permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989d2a2df59e80e7c49d47caeab450b5e4973efaefac9c7ab9c1756b6d1f3c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPolicyPermission", value)

    @builtins.property
    @jsii.member(jsii_name="accessPolicyResource")
    def access_policy_resource(
        self,
    ) -> typing.Union["CfnAccessPolicy.AccessPolicyResourceProperty", _IResolvable_a771d0ef]:
        '''The AWS IoT SiteWise Monitor resource for this access policy.

        Choose either a portal or a project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicyresource
        '''
        return typing.cast(typing.Union["CfnAccessPolicy.AccessPolicyResourceProperty", _IResolvable_a771d0ef], jsii.get(self, "accessPolicyResource"))

    @access_policy_resource.setter
    def access_policy_resource(
        self,
        value: typing.Union["CfnAccessPolicy.AccessPolicyResourceProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e03077e1135be8673b2355aa3158e1a07e6de2c6f8ec0ae13eb43de071f765d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPolicyResource", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicy.AccessPolicyIdentityProperty",
        jsii_struct_bases=[],
        name_mapping={"iam_role": "iamRole", "iam_user": "iamUser", "user": "user"},
    )
    class AccessPolicyIdentityProperty:
        def __init__(
            self,
            *,
            iam_role: typing.Optional[typing.Union[typing.Union["CfnAccessPolicy.IamRoleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            iam_user: typing.Optional[typing.Union[typing.Union["CfnAccessPolicy.IamUserProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            user: typing.Optional[typing.Union[typing.Union["CfnAccessPolicy.UserProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The identity (IAM Identity Center user, IAM Identity Center group, or IAM user) to which this access policy applies.

            :param iam_role: An IAM role identity.
            :param iam_user: An IAM user identity.
            :param user: The IAM Identity Center user to which this access policy maps.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyidentity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                access_policy_identity_property = iotsitewise.CfnAccessPolicy.AccessPolicyIdentityProperty(
                    iam_role=iotsitewise.CfnAccessPolicy.IamRoleProperty(
                        arn="arn"
                    ),
                    iam_user=iotsitewise.CfnAccessPolicy.IamUserProperty(
                        arn="arn"
                    ),
                    user=iotsitewise.CfnAccessPolicy.UserProperty(
                        id="id"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f538d4bd325a7f18f307d2b88c7d5cba6983be568730eaed5d09698d6e38918d)
                check_type(argname="argument iam_role", value=iam_role, expected_type=type_hints["iam_role"])
                check_type(argname="argument iam_user", value=iam_user, expected_type=type_hints["iam_user"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam_role is not None:
                self._values["iam_role"] = iam_role
            if iam_user is not None:
                self._values["iam_user"] = iam_user
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def iam_role(
            self,
        ) -> typing.Optional[typing.Union["CfnAccessPolicy.IamRoleProperty", _IResolvable_a771d0ef]]:
            '''An IAM role identity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyidentity.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity-iamrole
            '''
            result = self._values.get("iam_role")
            return typing.cast(typing.Optional[typing.Union["CfnAccessPolicy.IamRoleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def iam_user(
            self,
        ) -> typing.Optional[typing.Union["CfnAccessPolicy.IamUserProperty", _IResolvable_a771d0ef]]:
            '''An IAM user identity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyidentity.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity-iamuser
            '''
            result = self._values.get("iam_user")
            return typing.cast(typing.Optional[typing.Union["CfnAccessPolicy.IamUserProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def user(
            self,
        ) -> typing.Optional[typing.Union["CfnAccessPolicy.UserProperty", _IResolvable_a771d0ef]]:
            '''The IAM Identity Center user to which this access policy maps.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyidentity.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[typing.Union["CfnAccessPolicy.UserProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessPolicyIdentityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicy.AccessPolicyResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"portal": "portal", "project": "project"},
    )
    class AccessPolicyResourceProperty:
        def __init__(
            self,
            *,
            portal: typing.Optional[typing.Union[typing.Union["CfnAccessPolicy.PortalProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            project: typing.Optional[typing.Union[typing.Union["CfnAccessPolicy.ProjectProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The AWS IoT SiteWise Monitor resource for this access policy.

            Choose either a portal or a project.

            :param portal: The AWS IoT SiteWise Monitor portal for this access policy.
            :param project: The AWS IoT SiteWise Monitor project for this access policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                access_policy_resource_property = iotsitewise.CfnAccessPolicy.AccessPolicyResourceProperty(
                    portal=iotsitewise.CfnAccessPolicy.PortalProperty(
                        id="id"
                    ),
                    project=iotsitewise.CfnAccessPolicy.ProjectProperty(
                        id="id"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0945aabd910f8fb5eb71140494053591c42bac94d6c2d5ac1847a6d15e734a7)
                check_type(argname="argument portal", value=portal, expected_type=type_hints["portal"])
                check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if portal is not None:
                self._values["portal"] = portal
            if project is not None:
                self._values["project"] = project

        @builtins.property
        def portal(
            self,
        ) -> typing.Optional[typing.Union["CfnAccessPolicy.PortalProperty", _IResolvable_a771d0ef]]:
            '''The AWS IoT SiteWise Monitor portal for this access policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyresource.html#cfn-iotsitewise-accesspolicy-accesspolicyresource-portal
            '''
            result = self._values.get("portal")
            return typing.cast(typing.Optional[typing.Union["CfnAccessPolicy.PortalProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def project(
            self,
        ) -> typing.Optional[typing.Union["CfnAccessPolicy.ProjectProperty", _IResolvable_a771d0ef]]:
            '''The AWS IoT SiteWise Monitor project for this access policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyresource.html#cfn-iotsitewise-accesspolicy-accesspolicyresource-project
            '''
            result = self._values.get("project")
            return typing.cast(typing.Optional[typing.Union["CfnAccessPolicy.ProjectProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessPolicyResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicy.IamRoleProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class IamRoleProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains information about an AWS Identity and Access Management role.

            For more information, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *IAM User Guide* .

            :param arn: The ARN of the IAM role. For more information, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-iamrole.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                iam_role_property = iotsitewise.CfnAccessPolicy.IamRoleProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a35db198a3e0aab11301525c513d1aa8d03ecae615853ea6f82eec84b88dadf)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role.

            For more information, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-iamrole.html#cfn-iotsitewise-accesspolicy-iamrole-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamRoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicy.IamUserProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class IamUserProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains information about an AWS Identity and Access Management user.

            :param arn: The ARN of the IAM user. For more information, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* . .. epigraph:: If you delete the IAM user, access policies that contain this identity include an empty ``arn`` . You can delete the access policy for the IAM user that no longer exists.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-iamuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                iam_user_property = iotsitewise.CfnAccessPolicy.IamUserProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6c321cd578cb65161fdca9546cc51f4eae6e74f84ff66009c5f9722a1d2e9fe)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM user. For more information, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* .

            .. epigraph::

               If you delete the IAM user, access policies that contain this identity include an empty ``arn`` . You can delete the access policy for the IAM user that no longer exists.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-iamuser.html#cfn-iotsitewise-accesspolicy-iamuser-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicy.PortalProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class PortalProperty:
        def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
            '''The ``Portal`` property type specifies the AWS IoT SiteWise Monitor portal for an `AWS::IoTSiteWise::AccessPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html>`_ .

            :param id: The ID of the portal.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-portal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                portal_property = iotsitewise.CfnAccessPolicy.PortalProperty(
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2f8a83b12a38cdd97779698ba2879857cccbf0d8947378fe39bb1b48fb5740b)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the portal.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-portal.html#cfn-iotsitewise-accesspolicy-portal-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicy.ProjectProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class ProjectProperty:
        def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
            '''The ``Project`` property type specifies the AWS IoT SiteWise Monitor project for an `AWS::IoTSiteWise::AccessPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html>`_ .

            :param id: The ID of the project.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-project.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                project_property = iotsitewise.CfnAccessPolicy.ProjectProperty(
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f891ae36e22a4610824eb124a3b64d1afec6ccdd3e396835d5eab7f31602c08)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the project.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-project.html#cfn-iotsitewise-accesspolicy-project-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicy.UserProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class UserProperty:
        def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
            '''The ``User`` property type specifies the AWS IoT SiteWise Monitor user for an `AWS::IoTSiteWise::AccessPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html>`_ .

            :param id: The ID of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-user.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                user_property = iotsitewise.CfnAccessPolicy.UserProperty(
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65a396a1319433dd0a0b6030eabce3acf7a7540f5f7989dc619d11fa641c611f)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-user.html#cfn-iotsitewise-accesspolicy-user-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnAccessPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policy_identity": "accessPolicyIdentity",
        "access_policy_permission": "accessPolicyPermission",
        "access_policy_resource": "accessPolicyResource",
    },
)
class CfnAccessPolicyProps:
    def __init__(
        self,
        *,
        access_policy_identity: typing.Union[typing.Union[CfnAccessPolicy.AccessPolicyIdentityProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        access_policy_permission: builtins.str,
        access_policy_resource: typing.Union[typing.Union[CfnAccessPolicy.AccessPolicyResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``CfnAccessPolicy``.

        :param access_policy_identity: The identity for this access policy. Choose an IAM Identity Center user, an IAM Identity Center group, or an IAM user.
        :param access_policy_permission: The permission level for this access policy. Choose either a ``ADMINISTRATOR`` or ``VIEWER`` . Note that a project ``ADMINISTRATOR`` is also known as a project owner.
        :param access_policy_resource: The AWS IoT SiteWise Monitor resource for this access policy. Choose either a portal or a project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotsitewise as iotsitewise
            
            cfn_access_policy_props = iotsitewise.CfnAccessPolicyProps(
                access_policy_identity=iotsitewise.CfnAccessPolicy.AccessPolicyIdentityProperty(
                    iam_role=iotsitewise.CfnAccessPolicy.IamRoleProperty(
                        arn="arn"
                    ),
                    iam_user=iotsitewise.CfnAccessPolicy.IamUserProperty(
                        arn="arn"
                    ),
                    user=iotsitewise.CfnAccessPolicy.UserProperty(
                        id="id"
                    )
                ),
                access_policy_permission="accessPolicyPermission",
                access_policy_resource=iotsitewise.CfnAccessPolicy.AccessPolicyResourceProperty(
                    portal=iotsitewise.CfnAccessPolicy.PortalProperty(
                        id="id"
                    ),
                    project=iotsitewise.CfnAccessPolicy.ProjectProperty(
                        id="id"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298f21d46d2f9a6ea105488e7a8151b724d6f57169d54529166fd57d75310d73)
            check_type(argname="argument access_policy_identity", value=access_policy_identity, expected_type=type_hints["access_policy_identity"])
            check_type(argname="argument access_policy_permission", value=access_policy_permission, expected_type=type_hints["access_policy_permission"])
            check_type(argname="argument access_policy_resource", value=access_policy_resource, expected_type=type_hints["access_policy_resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_policy_identity": access_policy_identity,
            "access_policy_permission": access_policy_permission,
            "access_policy_resource": access_policy_resource,
        }

    @builtins.property
    def access_policy_identity(
        self,
    ) -> typing.Union[CfnAccessPolicy.AccessPolicyIdentityProperty, _IResolvable_a771d0ef]:
        '''The identity for this access policy.

        Choose an IAM Identity Center user, an IAM Identity Center group, or an IAM user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity
        '''
        result = self._values.get("access_policy_identity")
        assert result is not None, "Required property 'access_policy_identity' is missing"
        return typing.cast(typing.Union[CfnAccessPolicy.AccessPolicyIdentityProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def access_policy_permission(self) -> builtins.str:
        '''The permission level for this access policy.

        Choose either a ``ADMINISTRATOR`` or ``VIEWER`` . Note that a project ``ADMINISTRATOR`` is also known as a project owner.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicypermission
        '''
        result = self._values.get("access_policy_permission")
        assert result is not None, "Required property 'access_policy_permission' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_policy_resource(
        self,
    ) -> typing.Union[CfnAccessPolicy.AccessPolicyResourceProperty, _IResolvable_a771d0ef]:
        '''The AWS IoT SiteWise Monitor resource for this access policy.

        Choose either a portal or a project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicyresource
        '''
        result = self._values.get("access_policy_resource")
        assert result is not None, "Required property 'access_policy_resource' is missing"
        return typing.cast(typing.Union[CfnAccessPolicy.AccessPolicyResourceProperty, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAsset(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnAsset",
):
    '''A CloudFormation ``AWS::IoTSiteWise::Asset``.

    Creates an asset from an existing asset model. For more information, see `Creating assets <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-assets.html>`_ in the *AWS IoT SiteWise User Guide* .

    :cloudformationResource: AWS::IoTSiteWise::Asset
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotsitewise as iotsitewise
        
        cfn_asset = iotsitewise.CfnAsset(self, "MyCfnAsset",
            asset_model_id="assetModelId",
            asset_name="assetName",
        
            # the properties below are optional
            asset_description="assetDescription",
            asset_hierarchies=[iotsitewise.CfnAsset.AssetHierarchyProperty(
                child_asset_id="childAssetId",
                logical_id="logicalId"
            )],
            asset_properties=[iotsitewise.CfnAsset.AssetPropertyProperty(
                logical_id="logicalId",
        
                # the properties below are optional
                alias="alias",
                notification_state="notificationState",
                unit="unit"
            )],
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
        asset_model_id: builtins.str,
        asset_name: builtins.str,
        asset_description: typing.Optional[builtins.str] = None,
        asset_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAsset.AssetHierarchyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        asset_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAsset.AssetPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTSiteWise::Asset``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param asset_model_id: The ID of the asset model from which to create the asset.
        :param asset_name: A unique, friendly name for the asset. The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .
        :param asset_description: A description for the asset.
        :param asset_hierarchies: A list of asset hierarchies that each contain a ``hierarchyLogicalId`` . A hierarchy specifies allowed parent/child asset relationships.
        :param asset_properties: The list of asset properties for the asset. This object doesn't include properties that you define in composite models. You can find composite model properties in the ``assetCompositeModels`` object.
        :param tags: A list of key-value pairs that contain metadata for the asset. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c340223f76f17c21718e88f39082be49c3b5b898be421bd885062f8a7e3ef2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssetProps(
            asset_model_id=asset_model_id,
            asset_name=asset_name,
            asset_description=asset_description,
            asset_hierarchies=asset_hierarchies,
            asset_properties=asset_properties,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f9b1984442ea430778b6ee741d2f9ce52bca98d4f82983b491e7dd4a8a4f51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb0bb135aab4775406a2f575d7586326911ceceede54592c26249cdb4f1a891b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssetArn")
    def attr_asset_arn(self) -> builtins.str:
        '''The ARN of the asset.

        :cloudformationAttribute: AssetArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssetArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAssetId")
    def attr_asset_id(self) -> builtins.str:
        '''The ID of the asset.

        :cloudformationAttribute: AssetId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssetId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs that contain metadata for the asset.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="assetModelId")
    def asset_model_id(self) -> builtins.str:
        '''The ID of the asset model from which to create the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetmodelid
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetModelId"))

    @asset_model_id.setter
    def asset_model_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246da2e527d962dab6780483037ba1669fee9174d5a0b3475db567be8d31b7c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetModelId", value)

    @builtins.property
    @jsii.member(jsii_name="assetName")
    def asset_name(self) -> builtins.str:
        '''A unique, friendly name for the asset.

        The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetname
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetName"))

    @asset_name.setter
    def asset_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__732e8b79d671120041b5ed8b15c335d26ffef50cdce0968e536d2b5e18fdd913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetName", value)

    @builtins.property
    @jsii.member(jsii_name="assetDescription")
    def asset_description(self) -> typing.Optional[builtins.str]:
        '''A description for the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetDescription"))

    @asset_description.setter
    def asset_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70256b0e75414b8fb76cb2575b2315b5689112ae0d7f8735ceca50c192855c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetDescription", value)

    @builtins.property
    @jsii.member(jsii_name="assetHierarchies")
    def asset_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetHierarchyProperty", _IResolvable_a771d0ef]]]]:
        '''A list of asset hierarchies that each contain a ``hierarchyLogicalId`` .

        A hierarchy specifies allowed parent/child asset relationships.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assethierarchies
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetHierarchyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "assetHierarchies"))

    @asset_hierarchies.setter
    def asset_hierarchies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetHierarchyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babda67d0008d27c0c8368d941c28ac46b8c3cdd0fc2db6a97faeed177903bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetHierarchies", value)

    @builtins.property
    @jsii.member(jsii_name="assetProperties")
    def asset_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetPropertyProperty", _IResolvable_a771d0ef]]]]:
        '''The list of asset properties for the asset.

        This object doesn't include properties that you define in composite models. You can find composite model properties in the ``assetCompositeModels`` object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetPropertyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "assetProperties"))

    @asset_properties.setter
    def asset_properties(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetPropertyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6597c876851cb97b9f331f9c4260e8b5c094dd502c5c2c3ce02da8179a6b0a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetProperties", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAsset.AssetHierarchyProperty",
        jsii_struct_bases=[],
        name_mapping={"child_asset_id": "childAssetId", "logical_id": "logicalId"},
    )
    class AssetHierarchyProperty:
        def __init__(
            self,
            *,
            child_asset_id: builtins.str,
            logical_id: builtins.str,
        ) -> None:
            '''Describes an asset hierarchy that contains a ``childAssetId`` and ``hierarchyLogicalId`` .

            :param child_asset_id: The Id of the child asset.
            :param logical_id: The ``LogicalID`` of the hierarchy. This ID is a ``hierarchyLogicalId`` . The maximum length is 256 characters, with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                asset_hierarchy_property = iotsitewise.CfnAsset.AssetHierarchyProperty(
                    child_asset_id="childAssetId",
                    logical_id="logicalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e236e130b7ec2f7395108df666806313d606fe31f7789a8e6f4348cce6d3abd)
                check_type(argname="argument child_asset_id", value=child_asset_id, expected_type=type_hints["child_asset_id"])
                check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "child_asset_id": child_asset_id,
                "logical_id": logical_id,
            }

        @builtins.property
        def child_asset_id(self) -> builtins.str:
            '''The Id of the child asset.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html#cfn-iotsitewise-asset-assethierarchy-childassetid
            '''
            result = self._values.get("child_asset_id")
            assert result is not None, "Required property 'child_asset_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def logical_id(self) -> builtins.str:
            '''The ``LogicalID`` of the hierarchy. This ID is a ``hierarchyLogicalId`` .

            The maximum length is 256 characters, with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html#cfn-iotsitewise-asset-assethierarchy-logicalid
            '''
            result = self._values.get("logical_id")
            assert result is not None, "Required property 'logical_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetHierarchyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAsset.AssetPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "logical_id": "logicalId",
            "alias": "alias",
            "notification_state": "notificationState",
            "unit": "unit",
        },
    )
    class AssetPropertyProperty:
        def __init__(
            self,
            *,
            logical_id: builtins.str,
            alias: typing.Optional[builtins.str] = None,
            notification_state: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains asset property information.

            :param logical_id: The ``LogicalID`` of the asset property. The maximum length is 256 characters, with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .
            :param alias: The property alias that identifies the property, such as an OPC-UA server data stream path (for example, ``/company/windfarm/3/turbine/7/temperature`` ). For more information, see `Mapping industrial data streams to asset properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/connect-data-streams.html>`_ in the *AWS IoT SiteWise User Guide* . The property alias must have 1-1000 characters.
            :param notification_state: The MQTT notification state ( ``ENABLED`` or ``DISABLED`` ) for this asset property. When the notification state is ``ENABLED`` , AWS IoT SiteWise publishes property value updates to a unique MQTT topic. For more information, see `Interacting with other services <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/interact-with-other-services.html>`_ in the *AWS IoT SiteWise User Guide* . If you omit this parameter, the notification state is set to ``DISABLED`` . .. epigraph:: You must use all caps for the NotificationState parameter. If you use lower case letters, you will receive a schema validation error.
            :param unit: The unit (such as ``Newtons`` or ``RPM`` ) of the asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                asset_property_property = iotsitewise.CfnAsset.AssetPropertyProperty(
                    logical_id="logicalId",
                
                    # the properties below are optional
                    alias="alias",
                    notification_state="notificationState",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6919fb6f9e78c92c1f30b1747a1b8a1a264c0e7606c58c72debd8593e6d8fd10)
                check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
                check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
                check_type(argname="argument notification_state", value=notification_state, expected_type=type_hints["notification_state"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "logical_id": logical_id,
            }
            if alias is not None:
                self._values["alias"] = alias
            if notification_state is not None:
                self._values["notification_state"] = notification_state
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def logical_id(self) -> builtins.str:
            '''The ``LogicalID`` of the asset property.

            The maximum length is 256 characters, with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-logicalid
            '''
            result = self._values.get("logical_id")
            assert result is not None, "Required property 'logical_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def alias(self) -> typing.Optional[builtins.str]:
            '''The property alias that identifies the property, such as an OPC-UA server data stream path (for example, ``/company/windfarm/3/turbine/7/temperature`` ).

            For more information, see `Mapping industrial data streams to asset properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/connect-data-streams.html>`_ in the *AWS IoT SiteWise User Guide* .

            The property alias must have 1-1000 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-alias
            '''
            result = self._values.get("alias")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_state(self) -> typing.Optional[builtins.str]:
            '''The MQTT notification state ( ``ENABLED`` or ``DISABLED`` ) for this asset property.

            When the notification state is ``ENABLED`` , AWS IoT SiteWise publishes property value updates to a unique MQTT topic. For more information, see `Interacting with other services <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/interact-with-other-services.html>`_ in the *AWS IoT SiteWise User Guide* .

            If you omit this parameter, the notification state is set to ``DISABLED`` .
            .. epigraph::

               You must use all caps for the NotificationState parameter. If you use lower case letters, you will receive a schema validation error.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-notificationstate
            '''
            result = self._values.get("notification_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit (such as ``Newtons`` or ``RPM`` ) of the asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnAssetModel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnAssetModel",
):
    '''A CloudFormation ``AWS::IoTSiteWise::AssetModel``.

    Creates an asset model from specified property and hierarchy definitions. You create assets from asset models. With asset models, you can easily create assets of the same type that have standardized definitions. Each asset created from a model inherits the asset model's property and hierarchy definitions. For more information, see `Defining asset models <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/define-models.html>`_ in the *AWS IoT SiteWise User Guide* .

    :cloudformationResource: AWS::IoTSiteWise::AssetModel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotsitewise as iotsitewise
        
        cfn_asset_model = iotsitewise.CfnAssetModel(self, "MyCfnAssetModel",
            asset_model_name="assetModelName",
        
            # the properties below are optional
            asset_model_composite_models=[iotsitewise.CfnAssetModel.AssetModelCompositeModelProperty(
                name="name",
                type="type",
        
                # the properties below are optional
                composite_model_properties=[iotsitewise.CfnAssetModel.AssetModelPropertyProperty(
                    data_type="dataType",
                    logical_id="logicalId",
                    name="name",
                    type=iotsitewise.CfnAssetModel.PropertyTypeProperty(
                        type_name="typeName",
        
                        # the properties below are optional
                        attribute=iotsitewise.CfnAssetModel.AttributeProperty(
                            default_value="defaultValue"
                        ),
                        metric=iotsitewise.CfnAssetModel.MetricProperty(
                            expression="expression",
                            variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                    property_logical_id="propertyLogicalId",
        
                                    # the properties below are optional
                                    hierarchy_logical_id="hierarchyLogicalId"
                                )
                            )],
                            window=iotsitewise.CfnAssetModel.MetricWindowProperty(
                                tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                                    interval="interval",
        
                                    # the properties below are optional
                                    offset="offset"
                                )
                            )
                        ),
                        transform=iotsitewise.CfnAssetModel.TransformProperty(
                            expression="expression",
                            variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                    property_logical_id="propertyLogicalId",
        
                                    # the properties below are optional
                                    hierarchy_logical_id="hierarchyLogicalId"
                                )
                            )]
                        )
                    ),
        
                    # the properties below are optional
                    data_type_spec="dataTypeSpec",
                    unit="unit"
                )],
                description="description"
            )],
            asset_model_description="assetModelDescription",
            asset_model_hierarchies=[iotsitewise.CfnAssetModel.AssetModelHierarchyProperty(
                child_asset_model_id="childAssetModelId",
                logical_id="logicalId",
                name="name"
            )],
            asset_model_properties=[iotsitewise.CfnAssetModel.AssetModelPropertyProperty(
                data_type="dataType",
                logical_id="logicalId",
                name="name",
                type=iotsitewise.CfnAssetModel.PropertyTypeProperty(
                    type_name="typeName",
        
                    # the properties below are optional
                    attribute=iotsitewise.CfnAssetModel.AttributeProperty(
                        default_value="defaultValue"
                    ),
                    metric=iotsitewise.CfnAssetModel.MetricProperty(
                        expression="expression",
                        variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                            name="name",
                            value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                property_logical_id="propertyLogicalId",
        
                                # the properties below are optional
                                hierarchy_logical_id="hierarchyLogicalId"
                            )
                        )],
                        window=iotsitewise.CfnAssetModel.MetricWindowProperty(
                            tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                                interval="interval",
        
                                # the properties below are optional
                                offset="offset"
                            )
                        )
                    ),
                    transform=iotsitewise.CfnAssetModel.TransformProperty(
                        expression="expression",
                        variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                            name="name",
                            value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                property_logical_id="propertyLogicalId",
        
                                # the properties below are optional
                                hierarchy_logical_id="hierarchyLogicalId"
                            )
                        )]
                    )
                ),
        
                # the properties below are optional
                data_type_spec="dataTypeSpec",
                unit="unit"
            )],
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
        asset_model_name: builtins.str,
        asset_model_composite_models: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssetModel.AssetModelCompositeModelProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        asset_model_description: typing.Optional[builtins.str] = None,
        asset_model_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssetModel.AssetModelHierarchyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        asset_model_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssetModel.AssetModelPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTSiteWise::AssetModel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param asset_model_name: A unique, friendly name for the asset model. The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .
        :param asset_model_composite_models: The composite asset models that are part of this asset model. Composite asset models are asset models that contain specific properties. Each composite model has a type that defines the properties that the composite model supports. You can use composite asset models to define alarms on this asset model.
        :param asset_model_description: A description for the asset model.
        :param asset_model_hierarchies: The hierarchy definitions of the asset model. Each hierarchy specifies an asset model whose assets can be children of any other assets created from this asset model. For more information, see `Defining relationships between assets <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* . You can specify up to 10 hierarchies per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param asset_model_properties: The property definitions of the asset model. For more information, see `Defining data properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html>`_ in the *AWS IoT SiteWise User Guide* . You can specify up to 200 properties per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param tags: A list of key-value pairs that contain metadata for the asset. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f295ebf87c388e854ada0ebcbffd491eb2e59b673fafc9e7f1ee1e7f61b25c79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssetModelProps(
            asset_model_name=asset_model_name,
            asset_model_composite_models=asset_model_composite_models,
            asset_model_description=asset_model_description,
            asset_model_hierarchies=asset_model_hierarchies,
            asset_model_properties=asset_model_properties,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47703a9cf0aa7a9e07e5239de5842936285a20587d4a213500b3d3476789f02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5210678d81330030e70389814236c5dfc343e9dcc7b7c249d49bafab2ff80b3c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssetModelArn")
    def attr_asset_model_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: AssetModelArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssetModelArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAssetModelId")
    def attr_asset_model_id(self) -> builtins.str:
        '''The ID of the asset model.

        :cloudformationAttribute: AssetModelId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssetModelId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs that contain metadata for the asset.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="assetModelName")
    def asset_model_name(self) -> builtins.str:
        '''A unique, friendly name for the asset model.

        The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelname
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetModelName"))

    @asset_model_name.setter
    def asset_model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0773173f58147cba1dd01ef7066f69e75e48e8dd0570bc0f883d08927f3d2d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetModelName", value)

    @builtins.property
    @jsii.member(jsii_name="assetModelCompositeModels")
    def asset_model_composite_models(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelCompositeModelProperty", _IResolvable_a771d0ef]]]]:
        '''The composite asset models that are part of this asset model.

        Composite asset models are asset models that contain specific properties. Each composite model has a type that defines the properties that the composite model supports. You can use composite asset models to define alarms on this asset model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodels
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelCompositeModelProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "assetModelCompositeModels"))

    @asset_model_composite_models.setter
    def asset_model_composite_models(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelCompositeModelProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36b67fbd3e043267a9a9b7d75e0d9d6dde5c669fde7a245d31d5a6206e259e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetModelCompositeModels", value)

    @builtins.property
    @jsii.member(jsii_name="assetModelDescription")
    def asset_model_description(self) -> typing.Optional[builtins.str]:
        '''A description for the asset model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodeldescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetModelDescription"))

    @asset_model_description.setter
    def asset_model_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fa4979bba4382a8c15003d48a39f10ac92fcd49ca37af32cd164a8836a7b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetModelDescription", value)

    @builtins.property
    @jsii.member(jsii_name="assetModelHierarchies")
    def asset_model_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelHierarchyProperty", _IResolvable_a771d0ef]]]]:
        '''The hierarchy definitions of the asset model.

        Each hierarchy specifies an asset model whose assets can be children of any other assets created from this asset model. For more information, see `Defining relationships between assets <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .

        You can specify up to 10 hierarchies per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelhierarchies
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelHierarchyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "assetModelHierarchies"))

    @asset_model_hierarchies.setter
    def asset_model_hierarchies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelHierarchyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55006b72eb7bb5aa28b3791bae2c02afbe6f8fef9deec84c8e2bf85c4d132308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetModelHierarchies", value)

    @builtins.property
    @jsii.member(jsii_name="assetModelProperties")
    def asset_model_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelPropertyProperty", _IResolvable_a771d0ef]]]]:
        '''The property definitions of the asset model.

        For more information, see `Defining data properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html>`_ in the *AWS IoT SiteWise User Guide* .

        You can specify up to 200 properties per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelPropertyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "assetModelProperties"))

    @asset_model_properties.setter
    def asset_model_properties(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelPropertyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1b6ba4aa528b4ba2e6768770eb1b13eca7d8ea367453e861f0f39759b65760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetModelProperties", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.AssetModelCompositeModelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "type": "type",
            "composite_model_properties": "compositeModelProperties",
            "description": "description",
        },
    )
    class AssetModelCompositeModelProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            type: builtins.str,
            composite_model_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssetModel.AssetModelPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            description: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a composite model in an asset model.

            This object contains the asset property definitions that you define in the composite model. You can use composite asset models to define alarms on this asset model.

            If you use the ``AssetModelCompositeModel`` property to create an alarm, you must use the following information to define three asset model properties:

            - Use an asset model property to specify the alarm type.
            - The name must be ``AWS/ALARM_TYPE`` .
            - The data type must be ``STRING`` .
            - For the ``Type`` property, the type name must be ``Attribute`` and the default value must be ``IOT_EVENTS`` .
            - Use an asset model property to specify the alarm source.
            - The name must be ``AWS/ALARM_SOURCE`` .
            - The data type must be ``STRING`` .
            - For the ``Type`` property, the type name must be ``Attribute`` and the default value must be the ARN of the alarm model that you created in AWS IoT Events .

            .. epigraph::

               For the ARN of the alarm model, you can use the ``Fn::Sub`` intrinsic function to substitute the ``AWS::Partition`` , ``AWS::Region`` , and ``AWS::AccountId`` variables in an input string with values that you specify.

               For example, ``Fn::Sub: "arn:${AWS::Partition}:iotevents:${AWS::Region}:${AWS::AccountId}:alarmModel/TestAlarmModel"`` .

               Replace ``TestAlarmModel`` with the name of your alarm model.

               For more information about using the ``Fn::Sub`` intrinsic function, see `Fn::Sub <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-sub.html>`_ .

            - Use an asset model property to specify the state of the alarm.
            - The name must be ``AWS/ALARM_STATE`` .
            - The data type must be ``STRUCT`` .
            - The ``DataTypeSpec`` value must be ``AWS/ALARM_STATE`` .
            - For the ``Type`` property, the type name must be ``Measurement`` .

            At the bottom of this page, we provide a YAML example that you can modify to create an alarm.

            :param name: The name of the composite model.
            :param type: The type of the composite model. For alarm composite models, this type is ``AWS/ALARM`` .
            :param composite_model_properties: The asset property definitions for this composite model.
            :param description: The description of the composite model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                asset_model_composite_model_property = iotsitewise.CfnAssetModel.AssetModelCompositeModelProperty(
                    name="name",
                    type="type",
                
                    # the properties below are optional
                    composite_model_properties=[iotsitewise.CfnAssetModel.AssetModelPropertyProperty(
                        data_type="dataType",
                        logical_id="logicalId",
                        name="name",
                        type=iotsitewise.CfnAssetModel.PropertyTypeProperty(
                            type_name="typeName",
                
                            # the properties below are optional
                            attribute=iotsitewise.CfnAssetModel.AttributeProperty(
                                default_value="defaultValue"
                            ),
                            metric=iotsitewise.CfnAssetModel.MetricProperty(
                                expression="expression",
                                variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                    name="name",
                                    value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                        property_logical_id="propertyLogicalId",
                
                                        # the properties below are optional
                                        hierarchy_logical_id="hierarchyLogicalId"
                                    )
                                )],
                                window=iotsitewise.CfnAssetModel.MetricWindowProperty(
                                    tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                                        interval="interval",
                
                                        # the properties below are optional
                                        offset="offset"
                                    )
                                )
                            ),
                            transform=iotsitewise.CfnAssetModel.TransformProperty(
                                expression="expression",
                                variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                    name="name",
                                    value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                        property_logical_id="propertyLogicalId",
                
                                        # the properties below are optional
                                        hierarchy_logical_id="hierarchyLogicalId"
                                    )
                                )]
                            )
                        ),
                
                        # the properties below are optional
                        data_type_spec="dataTypeSpec",
                        unit="unit"
                    )],
                    description="description"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ddd158fc8e8b323055785206f7a7d06dee04e68dc7a21c36a26f39140bbf803)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument composite_model_properties", value=composite_model_properties, expected_type=type_hints["composite_model_properties"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "type": type,
            }
            if composite_model_properties is not None:
                self._values["composite_model_properties"] = composite_model_properties
            if description is not None:
                self._values["description"] = description

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the composite model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of the composite model.

            For alarm composite models, this type is ``AWS/ALARM`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def composite_model_properties(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelPropertyProperty", _IResolvable_a771d0ef]]]]:
            '''The asset property definitions for this composite model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-compositemodelproperties
            '''
            result = self._values.get("composite_model_properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelPropertyProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the composite model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelCompositeModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.AssetModelHierarchyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "child_asset_model_id": "childAssetModelId",
            "logical_id": "logicalId",
            "name": "name",
        },
    )
    class AssetModelHierarchyProperty:
        def __init__(
            self,
            *,
            child_asset_model_id: builtins.str,
            logical_id: builtins.str,
            name: builtins.str,
        ) -> None:
            '''Describes an asset hierarchy that contains a hierarchy's name, ``LogicalID`` , and child asset model ID that specifies the type of asset that can be in this hierarchy.

            :param child_asset_model_id: The Id of the asset model.
            :param logical_id: The ``LogicalID`` of the asset model hierarchy. This ID is a ``hierarchyLogicalId`` . The maximum length is 256 characters, with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+``
            :param name: The name of the asset model hierarchy. The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                asset_model_hierarchy_property = iotsitewise.CfnAssetModel.AssetModelHierarchyProperty(
                    child_asset_model_id="childAssetModelId",
                    logical_id="logicalId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74e48ad0ed017b244b21ac74eaf5dd542c97e628e5fa798cbb69d78ae462dea8)
                check_type(argname="argument child_asset_model_id", value=child_asset_model_id, expected_type=type_hints["child_asset_model_id"])
                check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "child_asset_model_id": child_asset_model_id,
                "logical_id": logical_id,
                "name": name,
            }

        @builtins.property
        def child_asset_model_id(self) -> builtins.str:
            '''The Id of the asset model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-childassetmodelid
            '''
            result = self._values.get("child_asset_model_id")
            assert result is not None, "Required property 'child_asset_model_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def logical_id(self) -> builtins.str:
            '''The ``LogicalID`` of the asset model hierarchy. This ID is a ``hierarchyLogicalId`` .

            The maximum length is 256 characters, with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-logicalid
            '''
            result = self._values.get("logical_id")
            assert result is not None, "Required property 'logical_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the asset model hierarchy.

            The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelHierarchyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.AssetModelPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_type": "dataType",
            "logical_id": "logicalId",
            "name": "name",
            "type": "type",
            "data_type_spec": "dataTypeSpec",
            "unit": "unit",
        },
    )
    class AssetModelPropertyProperty:
        def __init__(
            self,
            *,
            data_type: builtins.str,
            logical_id: builtins.str,
            name: builtins.str,
            type: typing.Union[typing.Union["CfnAssetModel.PropertyTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            data_type_spec: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an asset model property.

            :param data_type: The data type of the asset model property. The value can be ``STRING`` , ``INTEGER`` , ``DOUBLE`` , ``BOOLEAN`` , or ``STRUCT`` .
            :param logical_id: The ``LogicalID`` of the asset model property. The maximum length is 256 characters, with the pattern ``[^\\\\ u0000-\\\\ u001F\\\\ u007F]+`` .
            :param name: The name of the asset model property. The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .
            :param type: Contains a property type, which can be one of ``Attribute`` , ``Measurement`` , ``Metric`` , or ``Transform`` .
            :param data_type_spec: The data type of the structure for this property. This parameter exists on properties that have the ``STRUCT`` data type.
            :param unit: The unit of the asset model property, such as ``Newtons`` or ``RPM`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                asset_model_property_property = iotsitewise.CfnAssetModel.AssetModelPropertyProperty(
                    data_type="dataType",
                    logical_id="logicalId",
                    name="name",
                    type=iotsitewise.CfnAssetModel.PropertyTypeProperty(
                        type_name="typeName",
                
                        # the properties below are optional
                        attribute=iotsitewise.CfnAssetModel.AttributeProperty(
                            default_value="defaultValue"
                        ),
                        metric=iotsitewise.CfnAssetModel.MetricProperty(
                            expression="expression",
                            variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                    property_logical_id="propertyLogicalId",
                
                                    # the properties below are optional
                                    hierarchy_logical_id="hierarchyLogicalId"
                                )
                            )],
                            window=iotsitewise.CfnAssetModel.MetricWindowProperty(
                                tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                                    interval="interval",
                
                                    # the properties below are optional
                                    offset="offset"
                                )
                            )
                        ),
                        transform=iotsitewise.CfnAssetModel.TransformProperty(
                            expression="expression",
                            variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                    property_logical_id="propertyLogicalId",
                
                                    # the properties below are optional
                                    hierarchy_logical_id="hierarchyLogicalId"
                                )
                            )]
                        )
                    ),
                
                    # the properties below are optional
                    data_type_spec="dataTypeSpec",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85b57a2324b49a1515f146eb2c4b36d67b4dc1be8004ccae56f3ba4cb6ca61c9)
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument data_type_spec", value=data_type_spec, expected_type=type_hints["data_type_spec"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_type": data_type,
                "logical_id": logical_id,
                "name": name,
                "type": type,
            }
            if data_type_spec is not None:
                self._values["data_type_spec"] = data_type_spec
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def data_type(self) -> builtins.str:
            '''The data type of the asset model property.

            The value can be ``STRING`` , ``INTEGER`` , ``DOUBLE`` , ``BOOLEAN`` , or ``STRUCT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-datatype
            '''
            result = self._values.get("data_type")
            assert result is not None, "Required property 'data_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def logical_id(self) -> builtins.str:
            '''The ``LogicalID`` of the asset model property.

            The maximum length is 256 characters, with the pattern ``[^\\\\ u0000-\\\\ u001F\\\\ u007F]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-logicalid
            '''
            result = self._values.get("logical_id")
            assert result is not None, "Required property 'logical_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the asset model property.

            The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(
            self,
        ) -> typing.Union["CfnAssetModel.PropertyTypeProperty", _IResolvable_a771d0ef]:
            '''Contains a property type, which can be one of ``Attribute`` , ``Measurement`` , ``Metric`` , or ``Transform`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(typing.Union["CfnAssetModel.PropertyTypeProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def data_type_spec(self) -> typing.Optional[builtins.str]:
            '''The data type of the structure for this property.

            This parameter exists on properties that have the ``STRUCT`` data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-datatypespec
            '''
            result = self._values.get("data_type_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of the asset model property, such as ``Newtons`` or ``RPM`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue"},
    )
    class AttributeProperty:
        def __init__(
            self,
            *,
            default_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains an asset attribute property.

            For more information, see `Defining data properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html#attributes>`_ in the *AWS IoT SiteWise User Guide* .

            :param default_value: The default value of the asset model property attribute. All assets that you create from the asset model contain this attribute value. You can update an attribute's value after you create an asset. For more information, see `Updating attribute values <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/update-attribute-values.html>`_ in the *AWS IoT SiteWise User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-attribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                attribute_property = iotsitewise.CfnAssetModel.AttributeProperty(
                    default_value="defaultValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39f3f97bd69113e82966bf1e58d78481bb590496dab82a80d0485c06f960ed69)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value is not None:
                self._values["default_value"] = default_value

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the asset model property attribute.

            All assets that you create from the asset model contain this attribute value. You can update an attribute's value after you create an asset. For more information, see `Updating attribute values <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/update-attribute-values.html>`_ in the *AWS IoT SiteWise User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-attribute.html#cfn-iotsitewise-assetmodel-attribute-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.ExpressionVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ExpressionVariableProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            value: typing.Union[typing.Union["CfnAssetModel.VariableValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Contains expression variable information.

            :param name: The friendly name of the variable to be used in the expression. The maximum length is 64 characters with the pattern ``^[a-z][a-z0-9_]*$`` .
            :param value: The variable that identifies an asset property from which to use values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                expression_variable_property = iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                    name="name",
                    value=iotsitewise.CfnAssetModel.VariableValueProperty(
                        property_logical_id="propertyLogicalId",
                
                        # the properties below are optional
                        hierarchy_logical_id="hierarchyLogicalId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b97a07ef390d515bb52b9bc2b26063977795a9aac55c78cc1b02b3fb87dd4b0)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The friendly name of the variable to be used in the expression.

            The maximum length is 64 characters with the pattern ``^[a-z][a-z0-9_]*$`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html#cfn-iotsitewise-assetmodel-expressionvariable-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(
            self,
        ) -> typing.Union["CfnAssetModel.VariableValueProperty", _IResolvable_a771d0ef]:
            '''The variable that identifies an asset property from which to use values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html#cfn-iotsitewise-assetmodel-expressionvariable-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(typing.Union["CfnAssetModel.VariableValueProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpressionVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "variables": "variables",
            "window": "window",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            expression: builtins.str,
            variables: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssetModel.ExpressionVariableProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            window: typing.Union[typing.Union["CfnAssetModel.MetricWindowProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Contains an asset metric property.

            With metrics, you can calculate aggregate functions, such as an average, maximum, or minimum, as specified through an expression. A metric maps several values to a single value (such as a sum).

            The maximum number of dependent/cascading variables used in any one metric calculation is 10. Therefore, a *root* metric can have up to 10 cascading metrics in its computational dependency tree. Additionally, a metric can only have a data type of ``DOUBLE`` and consume properties with data types of ``INTEGER`` or ``DOUBLE`` .

            For more information, see `Defining data properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html#metrics>`_ in the *AWS IoT SiteWise User Guide* .

            :param expression: The mathematical expression that defines the metric aggregation function. You can specify up to 10 variables per expression. You can specify up to 10 functions per expression. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
            :param variables: The list of variables used in the expression.
            :param window: The window (time interval) over which AWS IoT SiteWise computes the metric's aggregation expression. AWS IoT SiteWise computes one data point per ``window`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                metric_property = iotsitewise.CfnAssetModel.MetricProperty(
                    expression="expression",
                    variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                        name="name",
                        value=iotsitewise.CfnAssetModel.VariableValueProperty(
                            property_logical_id="propertyLogicalId",
                
                            # the properties below are optional
                            hierarchy_logical_id="hierarchyLogicalId"
                        )
                    )],
                    window=iotsitewise.CfnAssetModel.MetricWindowProperty(
                        tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                            interval="interval",
                
                            # the properties below are optional
                            offset="offset"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c450c34f57e2a28959a16a27b679bd91d977abf59cb1c4b037f38ba3d3d921aa)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
                check_type(argname="argument window", value=window, expected_type=type_hints["window"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "expression": expression,
                "variables": variables,
                "window": window,
            }

        @builtins.property
        def expression(self) -> builtins.str:
            '''The mathematical expression that defines the metric aggregation function.

            You can specify up to 10 variables per expression. You can specify up to 10 functions per expression.

            For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-expression
            '''
            result = self._values.get("expression")
            assert result is not None, "Required property 'expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def variables(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.ExpressionVariableProperty", _IResolvable_a771d0ef]]]:
            '''The list of variables used in the expression.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-variables
            '''
            result = self._values.get("variables")
            assert result is not None, "Required property 'variables' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.ExpressionVariableProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def window(
            self,
        ) -> typing.Union["CfnAssetModel.MetricWindowProperty", _IResolvable_a771d0ef]:
            '''The window (time interval) over which AWS IoT SiteWise computes the metric's aggregation expression.

            AWS IoT SiteWise computes one data point per ``window`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-window
            '''
            result = self._values.get("window")
            assert result is not None, "Required property 'window' is missing"
            return typing.cast(typing.Union["CfnAssetModel.MetricWindowProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.MetricWindowProperty",
        jsii_struct_bases=[],
        name_mapping={"tumbling": "tumbling"},
    )
    class MetricWindowProperty:
        def __init__(
            self,
            *,
            tumbling: typing.Optional[typing.Union[typing.Union["CfnAssetModel.TumblingWindowProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains a time interval window used for data aggregate computations (for example, average, sum, count, and so on).

            :param tumbling: The tumbling time interval window.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metricwindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                metric_window_property = iotsitewise.CfnAssetModel.MetricWindowProperty(
                    tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                        interval="interval",
                
                        # the properties below are optional
                        offset="offset"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b7cda9b84eede87c5a5704f9d5e4cb2276df17d5c561d1011daf91d051faec2)
                check_type(argname="argument tumbling", value=tumbling, expected_type=type_hints["tumbling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tumbling is not None:
                self._values["tumbling"] = tumbling

        @builtins.property
        def tumbling(
            self,
        ) -> typing.Optional[typing.Union["CfnAssetModel.TumblingWindowProperty", _IResolvable_a771d0ef]]:
            '''The tumbling time interval window.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metricwindow.html#cfn-iotsitewise-assetmodel-metricwindow-tumbling
            '''
            result = self._values.get("tumbling")
            return typing.cast(typing.Optional[typing.Union["CfnAssetModel.TumblingWindowProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.PropertyTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type_name": "typeName",
            "attribute": "attribute",
            "metric": "metric",
            "transform": "transform",
        },
    )
    class PropertyTypeProperty:
        def __init__(
            self,
            *,
            type_name: builtins.str,
            attribute: typing.Optional[typing.Union[typing.Union["CfnAssetModel.AttributeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            metric: typing.Optional[typing.Union[typing.Union["CfnAssetModel.MetricProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            transform: typing.Optional[typing.Union[typing.Union["CfnAssetModel.TransformProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains a property type, which can be one of ``Attribute`` , ``Measurement`` , ``Metric`` , or ``Transform`` .

            :param type_name: The type of property type, which can be one of ``Attribute`` , ``Measurement`` , ``Metric`` , or ``Transform`` .
            :param attribute: Specifies an asset attribute property. An attribute generally contains static information, such as the serial number of an `industrial IoT <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Internet_of_things#Industrial_applications>`_ wind turbine. This is required if the ``TypeName`` is ``Attribute`` and has a ``DefaultValue`` .
            :param metric: Specifies an asset metric property. A metric contains a mathematical expression that uses aggregate functions to process all input data points over a time interval and output a single data point, such as to calculate the average hourly temperature. This is required if the ``TypeName`` is ``Metric`` .
            :param transform: Specifies an asset transform property. A transform contains a mathematical expression that maps a property's data points from one form to another, such as a unit conversion from Celsius to Fahrenheit. This is required if the ``TypeName`` is ``Transform`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                property_type_property = iotsitewise.CfnAssetModel.PropertyTypeProperty(
                    type_name="typeName",
                
                    # the properties below are optional
                    attribute=iotsitewise.CfnAssetModel.AttributeProperty(
                        default_value="defaultValue"
                    ),
                    metric=iotsitewise.CfnAssetModel.MetricProperty(
                        expression="expression",
                        variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                            name="name",
                            value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                property_logical_id="propertyLogicalId",
                
                                # the properties below are optional
                                hierarchy_logical_id="hierarchyLogicalId"
                            )
                        )],
                        window=iotsitewise.CfnAssetModel.MetricWindowProperty(
                            tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                                interval="interval",
                
                                # the properties below are optional
                                offset="offset"
                            )
                        )
                    ),
                    transform=iotsitewise.CfnAssetModel.TransformProperty(
                        expression="expression",
                        variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                            name="name",
                            value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                property_logical_id="propertyLogicalId",
                
                                # the properties below are optional
                                hierarchy_logical_id="hierarchyLogicalId"
                            )
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9acd04ed5417cdd722bd6941db784116cba221fbb9f4f73723df5508f047fb76)
                check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument transform", value=transform, expected_type=type_hints["transform"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type_name": type_name,
            }
            if attribute is not None:
                self._values["attribute"] = attribute
            if metric is not None:
                self._values["metric"] = metric
            if transform is not None:
                self._values["transform"] = transform

        @builtins.property
        def type_name(self) -> builtins.str:
            '''The type of property type, which can be one of ``Attribute`` , ``Measurement`` , ``Metric`` , or ``Transform`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-typename
            '''
            result = self._values.get("type_name")
            assert result is not None, "Required property 'type_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def attribute(
            self,
        ) -> typing.Optional[typing.Union["CfnAssetModel.AttributeProperty", _IResolvable_a771d0ef]]:
            '''Specifies an asset attribute property.

            An attribute generally contains static information, such as the serial number of an `industrial IoT <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Internet_of_things#Industrial_applications>`_ wind turbine.

            This is required if the ``TypeName`` is ``Attribute`` and has a ``DefaultValue`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[typing.Union["CfnAssetModel.AttributeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union["CfnAssetModel.MetricProperty", _IResolvable_a771d0ef]]:
            '''Specifies an asset metric property.

            A metric contains a mathematical expression that uses aggregate functions to process all input data points over a time interval and output a single data point, such as to calculate the average hourly temperature.

            This is required if the ``TypeName`` is ``Metric`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union["CfnAssetModel.MetricProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def transform(
            self,
        ) -> typing.Optional[typing.Union["CfnAssetModel.TransformProperty", _IResolvable_a771d0ef]]:
            '''Specifies an asset transform property.

            A transform contains a mathematical expression that maps a property's data points from one form to another, such as a unit conversion from Celsius to Fahrenheit.

            This is required if the ``TypeName`` is ``Transform`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-transform
            '''
            result = self._values.get("transform")
            return typing.cast(typing.Optional[typing.Union["CfnAssetModel.TransformProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.TransformProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "variables": "variables"},
    )
    class TransformProperty:
        def __init__(
            self,
            *,
            expression: builtins.str,
            variables: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssetModel.ExpressionVariableProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''Contains an asset transform property.

            A transform is a one-to-one mapping of a property's data points from one form to another. For example, you can use a transform to convert a Celsius data stream to Fahrenheit by applying the transformation expression to each data point of the Celsius stream. Transforms can only input properties that are ``INTEGER`` , ``DOUBLE`` , or ``BOOLEAN`` type. Booleans convert to ``0`` ( ``FALSE`` ) and ``1`` ( ``TRUE`` )..

            For more information, see `Defining data properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html#transforms>`_ in the *AWS IoT SiteWise User Guide* .

            :param expression: The mathematical expression that defines the transformation function. You can specify up to 10 variables per expression. You can specify up to 10 functions per expression. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
            :param variables: The list of variables used in the expression.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                transform_property = iotsitewise.CfnAssetModel.TransformProperty(
                    expression="expression",
                    variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                        name="name",
                        value=iotsitewise.CfnAssetModel.VariableValueProperty(
                            property_logical_id="propertyLogicalId",
                
                            # the properties below are optional
                            hierarchy_logical_id="hierarchyLogicalId"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__809bf7a13419f60779522f77ed2f36de6a3c20e0ffc044dfecb51e66e6a8443e)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "expression": expression,
                "variables": variables,
            }

        @builtins.property
        def expression(self) -> builtins.str:
            '''The mathematical expression that defines the transformation function.

            You can specify up to 10 variables per expression. You can specify up to 10 functions per expression.

            For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html#cfn-iotsitewise-assetmodel-transform-expression
            '''
            result = self._values.get("expression")
            assert result is not None, "Required property 'expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def variables(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.ExpressionVariableProperty", _IResolvable_a771d0ef]]]:
            '''The list of variables used in the expression.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html#cfn-iotsitewise-assetmodel-transform-variables
            '''
            result = self._values.get("variables")
            assert result is not None, "Required property 'variables' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.ExpressionVariableProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.TumblingWindowProperty",
        jsii_struct_bases=[],
        name_mapping={"interval": "interval", "offset": "offset"},
    )
    class TumblingWindowProperty:
        def __init__(
            self,
            *,
            interval: builtins.str,
            offset: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains a tumbling window, which is a repeating fixed-sized, non-overlapping, and contiguous time window.

            You can use this window in metrics to aggregate data from properties and other assets.

            You can use ``m`` , ``h`` , ``d`` , and ``w`` when you specify an interval or offset. Note that ``m`` represents minutes, ``h`` represents hours, ``d`` represents days, and ``w`` represents weeks. You can also use ``s`` to represent seconds in ``offset`` .

            The ``interval`` and ``offset`` parameters support the `ISO 8601 format <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/ISO_8601>`_ . For example, ``PT5S`` represents 5 seconds, ``PT5M`` represents 5 minutes, and ``PT5H`` represents 5 hours.

            :param interval: The time interval for the tumbling window. The interval time must be between 1 minute and 1 week. AWS IoT SiteWise computes the ``1w`` interval the end of Sunday at midnight each week (UTC), the ``1d`` interval at the end of each day at midnight (UTC), the ``1h`` interval at the end of each hour, and so on. When AWS IoT SiteWise aggregates data points for metric computations, the start of each interval is exclusive and the end of each interval is inclusive. AWS IoT SiteWise places the computed data point at the end of the interval.
            :param offset: The offset for the tumbling window. The ``offset`` parameter accepts the following:. - The offset time. For example, if you specify ``18h`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways: - If you create the metric before or at 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) on the day when you create the metric. - If you create the metric after 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) the next day. - The ISO 8601 format. For example, if you specify ``PT18H`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways: - If you create the metric before or at 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) on the day when you create the metric. - If you create the metric after 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) the next day. - The 24-hour clock. For example, if you specify ``00:03:00`` for ``offset`` , ``5m`` for ``interval`` , and you create the metric at 2 PM (UTC), you get the first aggregation result at 2:03 PM (UTC). You get the second aggregation result at 2:08 PM (UTC). - The offset time zone. For example, if you specify ``2021-07-23T18:00-08`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways: - If you create the metric before or at 6 PM (PST), you get the first aggregation result at 6 PM (PST) on the day when you create the metric. - If you create the metric after 6 PM (PST), you get the first aggregation result at 6 PM (PST) the next day.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-tumblingwindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                tumbling_window_property = iotsitewise.CfnAssetModel.TumblingWindowProperty(
                    interval="interval",
                
                    # the properties below are optional
                    offset="offset"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4dfe66b39a587839ab295ee47ecee270c08240751bb1b1cf3e9408ea549f8ee9)
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "interval": interval,
            }
            if offset is not None:
                self._values["offset"] = offset

        @builtins.property
        def interval(self) -> builtins.str:
            '''The time interval for the tumbling window. The interval time must be between 1 minute and 1 week.

            AWS IoT SiteWise computes the ``1w`` interval the end of Sunday at midnight each week (UTC), the ``1d`` interval at the end of each day at midnight (UTC), the ``1h`` interval at the end of each hour, and so on.

            When AWS IoT SiteWise aggregates data points for metric computations, the start of each interval is exclusive and the end of each interval is inclusive. AWS IoT SiteWise places the computed data point at the end of the interval.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-tumblingwindow.html#cfn-iotsitewise-assetmodel-tumblingwindow-interval
            '''
            result = self._values.get("interval")
            assert result is not None, "Required property 'interval' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def offset(self) -> typing.Optional[builtins.str]:
            '''The offset for the tumbling window. The ``offset`` parameter accepts the following:.

            - The offset time.

            For example, if you specify ``18h`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways:

            - If you create the metric before or at 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) on the day when you create the metric.
            - If you create the metric after 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) the next day.
            - The ISO 8601 format.

            For example, if you specify ``PT18H`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways:

            - If you create the metric before or at 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) on the day when you create the metric.
            - If you create the metric after 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) the next day.
            - The 24-hour clock.

            For example, if you specify ``00:03:00`` for ``offset`` , ``5m`` for ``interval`` , and you create the metric at 2 PM (UTC), you get the first aggregation result at 2:03 PM (UTC). You get the second aggregation result at 2:08 PM (UTC).

            - The offset time zone.

            For example, if you specify ``2021-07-23T18:00-08`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways:

            - If you create the metric before or at 6 PM (PST), you get the first aggregation result at 6 PM (PST) on the day when you create the metric.
            - If you create the metric after 6 PM (PST), you get the first aggregation result at 6 PM (PST) the next day.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-tumblingwindow.html#cfn-iotsitewise-assetmodel-tumblingwindow-offset
            '''
            result = self._values.get("offset")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TumblingWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.VariableValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "property_logical_id": "propertyLogicalId",
            "hierarchy_logical_id": "hierarchyLogicalId",
        },
    )
    class VariableValueProperty:
        def __init__(
            self,
            *,
            property_logical_id: builtins.str,
            hierarchy_logical_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies a property value used in an expression.

            :param property_logical_id: The ``LogicalID`` of the property to use as the variable.
            :param hierarchy_logical_id: The ``LogicalID`` of the hierarchy to query for the ``PropertyLogicalID`` . You use a ``hierarchyLogicalID`` instead of a model ID because you can have several hierarchies using the same model and therefore the same property. For example, you might have separately grouped assets that come from the same asset model. For more information, see `Defining relationships between assets <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                variable_value_property = iotsitewise.CfnAssetModel.VariableValueProperty(
                    property_logical_id="propertyLogicalId",
                
                    # the properties below are optional
                    hierarchy_logical_id="hierarchyLogicalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c72dd2a8d61935e1e7e54d4c898f28c58721ce700656dc2ebc39972788c30d9c)
                check_type(argname="argument property_logical_id", value=property_logical_id, expected_type=type_hints["property_logical_id"])
                check_type(argname="argument hierarchy_logical_id", value=hierarchy_logical_id, expected_type=type_hints["hierarchy_logical_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "property_logical_id": property_logical_id,
            }
            if hierarchy_logical_id is not None:
                self._values["hierarchy_logical_id"] = hierarchy_logical_id

        @builtins.property
        def property_logical_id(self) -> builtins.str:
            '''The ``LogicalID`` of the property to use as the variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-propertylogicalid
            '''
            result = self._values.get("property_logical_id")
            assert result is not None, "Required property 'property_logical_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def hierarchy_logical_id(self) -> typing.Optional[builtins.str]:
            '''The ``LogicalID`` of the hierarchy to query for the ``PropertyLogicalID`` .

            You use a ``hierarchyLogicalID`` instead of a model ID because you can have several hierarchies using the same model and therefore the same property. For example, you might have separately grouped assets that come from the same asset model. For more information, see `Defining relationships between assets <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-hierarchylogicalid
            '''
            result = self._values.get("hierarchy_logical_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariableValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnAssetModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_model_name": "assetModelName",
        "asset_model_composite_models": "assetModelCompositeModels",
        "asset_model_description": "assetModelDescription",
        "asset_model_hierarchies": "assetModelHierarchies",
        "asset_model_properties": "assetModelProperties",
        "tags": "tags",
    },
)
class CfnAssetModelProps:
    def __init__(
        self,
        *,
        asset_model_name: builtins.str,
        asset_model_composite_models: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelCompositeModelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        asset_model_description: typing.Optional[builtins.str] = None,
        asset_model_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelHierarchyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        asset_model_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAssetModel``.

        :param asset_model_name: A unique, friendly name for the asset model. The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .
        :param asset_model_composite_models: The composite asset models that are part of this asset model. Composite asset models are asset models that contain specific properties. Each composite model has a type that defines the properties that the composite model supports. You can use composite asset models to define alarms on this asset model.
        :param asset_model_description: A description for the asset model.
        :param asset_model_hierarchies: The hierarchy definitions of the asset model. Each hierarchy specifies an asset model whose assets can be children of any other assets created from this asset model. For more information, see `Defining relationships between assets <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* . You can specify up to 10 hierarchies per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param asset_model_properties: The property definitions of the asset model. For more information, see `Defining data properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html>`_ in the *AWS IoT SiteWise User Guide* . You can specify up to 200 properties per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param tags: A list of key-value pairs that contain metadata for the asset. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotsitewise as iotsitewise
            
            cfn_asset_model_props = iotsitewise.CfnAssetModelProps(
                asset_model_name="assetModelName",
            
                # the properties below are optional
                asset_model_composite_models=[iotsitewise.CfnAssetModel.AssetModelCompositeModelProperty(
                    name="name",
                    type="type",
            
                    # the properties below are optional
                    composite_model_properties=[iotsitewise.CfnAssetModel.AssetModelPropertyProperty(
                        data_type="dataType",
                        logical_id="logicalId",
                        name="name",
                        type=iotsitewise.CfnAssetModel.PropertyTypeProperty(
                            type_name="typeName",
            
                            # the properties below are optional
                            attribute=iotsitewise.CfnAssetModel.AttributeProperty(
                                default_value="defaultValue"
                            ),
                            metric=iotsitewise.CfnAssetModel.MetricProperty(
                                expression="expression",
                                variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                    name="name",
                                    value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                        property_logical_id="propertyLogicalId",
            
                                        # the properties below are optional
                                        hierarchy_logical_id="hierarchyLogicalId"
                                    )
                                )],
                                window=iotsitewise.CfnAssetModel.MetricWindowProperty(
                                    tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                                        interval="interval",
            
                                        # the properties below are optional
                                        offset="offset"
                                    )
                                )
                            ),
                            transform=iotsitewise.CfnAssetModel.TransformProperty(
                                expression="expression",
                                variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                    name="name",
                                    value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                        property_logical_id="propertyLogicalId",
            
                                        # the properties below are optional
                                        hierarchy_logical_id="hierarchyLogicalId"
                                    )
                                )]
                            )
                        ),
            
                        # the properties below are optional
                        data_type_spec="dataTypeSpec",
                        unit="unit"
                    )],
                    description="description"
                )],
                asset_model_description="assetModelDescription",
                asset_model_hierarchies=[iotsitewise.CfnAssetModel.AssetModelHierarchyProperty(
                    child_asset_model_id="childAssetModelId",
                    logical_id="logicalId",
                    name="name"
                )],
                asset_model_properties=[iotsitewise.CfnAssetModel.AssetModelPropertyProperty(
                    data_type="dataType",
                    logical_id="logicalId",
                    name="name",
                    type=iotsitewise.CfnAssetModel.PropertyTypeProperty(
                        type_name="typeName",
            
                        # the properties below are optional
                        attribute=iotsitewise.CfnAssetModel.AttributeProperty(
                            default_value="defaultValue"
                        ),
                        metric=iotsitewise.CfnAssetModel.MetricProperty(
                            expression="expression",
                            variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                    property_logical_id="propertyLogicalId",
            
                                    # the properties below are optional
                                    hierarchy_logical_id="hierarchyLogicalId"
                                )
                            )],
                            window=iotsitewise.CfnAssetModel.MetricWindowProperty(
                                tumbling=iotsitewise.CfnAssetModel.TumblingWindowProperty(
                                    interval="interval",
            
                                    # the properties below are optional
                                    offset="offset"
                                )
                            )
                        ),
                        transform=iotsitewise.CfnAssetModel.TransformProperty(
                            expression="expression",
                            variables=[iotsitewise.CfnAssetModel.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise.CfnAssetModel.VariableValueProperty(
                                    property_logical_id="propertyLogicalId",
            
                                    # the properties below are optional
                                    hierarchy_logical_id="hierarchyLogicalId"
                                )
                            )]
                        )
                    ),
            
                    # the properties below are optional
                    data_type_spec="dataTypeSpec",
                    unit="unit"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1505055b5fcb7b4739361ba0bdcd5b44029389cd799fba880df5365eb717ecc)
            check_type(argname="argument asset_model_name", value=asset_model_name, expected_type=type_hints["asset_model_name"])
            check_type(argname="argument asset_model_composite_models", value=asset_model_composite_models, expected_type=type_hints["asset_model_composite_models"])
            check_type(argname="argument asset_model_description", value=asset_model_description, expected_type=type_hints["asset_model_description"])
            check_type(argname="argument asset_model_hierarchies", value=asset_model_hierarchies, expected_type=type_hints["asset_model_hierarchies"])
            check_type(argname="argument asset_model_properties", value=asset_model_properties, expected_type=type_hints["asset_model_properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset_model_name": asset_model_name,
        }
        if asset_model_composite_models is not None:
            self._values["asset_model_composite_models"] = asset_model_composite_models
        if asset_model_description is not None:
            self._values["asset_model_description"] = asset_model_description
        if asset_model_hierarchies is not None:
            self._values["asset_model_hierarchies"] = asset_model_hierarchies
        if asset_model_properties is not None:
            self._values["asset_model_properties"] = asset_model_properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def asset_model_name(self) -> builtins.str:
        '''A unique, friendly name for the asset model.

        The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelname
        '''
        result = self._values.get("asset_model_name")
        assert result is not None, "Required property 'asset_model_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_model_composite_models(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelCompositeModelProperty, _IResolvable_a771d0ef]]]]:
        '''The composite asset models that are part of this asset model.

        Composite asset models are asset models that contain specific properties. Each composite model has a type that defines the properties that the composite model supports. You can use composite asset models to define alarms on this asset model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodels
        '''
        result = self._values.get("asset_model_composite_models")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelCompositeModelProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def asset_model_description(self) -> typing.Optional[builtins.str]:
        '''A description for the asset model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodeldescription
        '''
        result = self._values.get("asset_model_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_model_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelHierarchyProperty, _IResolvable_a771d0ef]]]]:
        '''The hierarchy definitions of the asset model.

        Each hierarchy specifies an asset model whose assets can be children of any other assets created from this asset model. For more information, see `Defining relationships between assets <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .

        You can specify up to 10 hierarchies per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelhierarchies
        '''
        result = self._values.get("asset_model_hierarchies")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelHierarchyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def asset_model_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelPropertyProperty, _IResolvable_a771d0ef]]]]:
        '''The property definitions of the asset model.

        For more information, see `Defining data properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html>`_ in the *AWS IoT SiteWise User Guide* .

        You can specify up to 200 properties per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelproperties
        '''
        result = self._values.get("asset_model_properties")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelPropertyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs that contain metadata for the asset.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssetModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnAssetProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_model_id": "assetModelId",
        "asset_name": "assetName",
        "asset_description": "assetDescription",
        "asset_hierarchies": "assetHierarchies",
        "asset_properties": "assetProperties",
        "tags": "tags",
    },
)
class CfnAssetProps:
    def __init__(
        self,
        *,
        asset_model_id: builtins.str,
        asset_name: builtins.str,
        asset_description: typing.Optional[builtins.str] = None,
        asset_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAsset.AssetHierarchyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        asset_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAsset.AssetPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAsset``.

        :param asset_model_id: The ID of the asset model from which to create the asset.
        :param asset_name: A unique, friendly name for the asset. The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .
        :param asset_description: A description for the asset.
        :param asset_hierarchies: A list of asset hierarchies that each contain a ``hierarchyLogicalId`` . A hierarchy specifies allowed parent/child asset relationships.
        :param asset_properties: The list of asset properties for the asset. This object doesn't include properties that you define in composite models. You can find composite model properties in the ``assetCompositeModels`` object.
        :param tags: A list of key-value pairs that contain metadata for the asset. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotsitewise as iotsitewise
            
            cfn_asset_props = iotsitewise.CfnAssetProps(
                asset_model_id="assetModelId",
                asset_name="assetName",
            
                # the properties below are optional
                asset_description="assetDescription",
                asset_hierarchies=[iotsitewise.CfnAsset.AssetHierarchyProperty(
                    child_asset_id="childAssetId",
                    logical_id="logicalId"
                )],
                asset_properties=[iotsitewise.CfnAsset.AssetPropertyProperty(
                    logical_id="logicalId",
            
                    # the properties below are optional
                    alias="alias",
                    notification_state="notificationState",
                    unit="unit"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f2af6b5589a0f41575ca36917cb9ee3040f98b0b3c274d7c5f3ae787f8b1d1)
            check_type(argname="argument asset_model_id", value=asset_model_id, expected_type=type_hints["asset_model_id"])
            check_type(argname="argument asset_name", value=asset_name, expected_type=type_hints["asset_name"])
            check_type(argname="argument asset_description", value=asset_description, expected_type=type_hints["asset_description"])
            check_type(argname="argument asset_hierarchies", value=asset_hierarchies, expected_type=type_hints["asset_hierarchies"])
            check_type(argname="argument asset_properties", value=asset_properties, expected_type=type_hints["asset_properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset_model_id": asset_model_id,
            "asset_name": asset_name,
        }
        if asset_description is not None:
            self._values["asset_description"] = asset_description
        if asset_hierarchies is not None:
            self._values["asset_hierarchies"] = asset_hierarchies
        if asset_properties is not None:
            self._values["asset_properties"] = asset_properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def asset_model_id(self) -> builtins.str:
        '''The ID of the asset model from which to create the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetmodelid
        '''
        result = self._values.get("asset_model_id")
        assert result is not None, "Required property 'asset_model_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_name(self) -> builtins.str:
        '''A unique, friendly name for the asset.

        The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetname
        '''
        result = self._values.get("asset_name")
        assert result is not None, "Required property 'asset_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_description(self) -> typing.Optional[builtins.str]:
        '''A description for the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetdescription
        '''
        result = self._values.get("asset_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetHierarchyProperty, _IResolvable_a771d0ef]]]]:
        '''A list of asset hierarchies that each contain a ``hierarchyLogicalId`` .

        A hierarchy specifies allowed parent/child asset relationships.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assethierarchies
        '''
        result = self._values.get("asset_hierarchies")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetHierarchyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def asset_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetPropertyProperty, _IResolvable_a771d0ef]]]]:
        '''The list of asset properties for the asset.

        This object doesn't include properties that you define in composite models. You can find composite model properties in the ``assetCompositeModels`` object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetproperties
        '''
        result = self._values.get("asset_properties")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetPropertyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs that contain metadata for the asset.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDashboard(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnDashboard",
):
    '''A CloudFormation ``AWS::IoTSiteWise::Dashboard``.

    Creates a dashboard in an AWS IoT SiteWise Monitor project.

    :cloudformationResource: AWS::IoTSiteWise::Dashboard
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotsitewise as iotsitewise
        
        cfn_dashboard = iotsitewise.CfnDashboard(self, "MyCfnDashboard",
            dashboard_definition="dashboardDefinition",
            dashboard_description="dashboardDescription",
            dashboard_name="dashboardName",
        
            # the properties below are optional
            project_id="projectId",
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
        dashboard_definition: builtins.str,
        dashboard_description: builtins.str,
        dashboard_name: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTSiteWise::Dashboard``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dashboard_definition: The dashboard definition specified in a JSON literal. For detailed information, see `Creating dashboards (CLI) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-dashboards-using-aws-cli.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param dashboard_description: A description for the dashboard.
        :param dashboard_name: A friendly name for the dashboard.
        :param project_id: The ID of the project in which to create the dashboard.
        :param tags: A list of key-value pairs that contain metadata for the dashboard. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3944a8e25443283f66b8ff08fee5e82a8dbff20db3eda9e0a10a49fed95468)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDashboardProps(
            dashboard_definition=dashboard_definition,
            dashboard_description=dashboard_description,
            dashboard_name=dashboard_name,
            project_id=project_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62845268357b4a2f91060a0fa7ca74678bbcd2ad08e371d80e434668c3de10d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__135fe84af566aaeb3a38a4b2855fb24aaf4bd1f0cc7b974ea1938f57ab0979a6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDashboardArn")
    def attr_dashboard_arn(self) -> builtins.str:
        '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the dashboard, which has the following format.

        ``arn:${Partition}:iotsitewise:${Region}:${Account}:dashboard/${DashboardId}``

        :cloudformationAttribute: DashboardArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDashboardArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDashboardId")
    def attr_dashboard_id(self) -> builtins.str:
        '''The ID of the dashboard.

        :cloudformationAttribute: DashboardId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDashboardId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs that contain metadata for the dashboard.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dashboardDefinition")
    def dashboard_definition(self) -> builtins.str:
        '''The dashboard definition specified in a JSON literal.

        For detailed information, see `Creating dashboards (CLI) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-dashboards-using-aws-cli.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboarddefinition
        '''
        return typing.cast(builtins.str, jsii.get(self, "dashboardDefinition"))

    @dashboard_definition.setter
    def dashboard_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d8a55eddfd87f37844fac5bfc0af3311b50ce40562ce79feabdd426f3d7dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardDefinition", value)

    @builtins.property
    @jsii.member(jsii_name="dashboardDescription")
    def dashboard_description(self) -> builtins.str:
        '''A description for the dashboard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboarddescription
        '''
        return typing.cast(builtins.str, jsii.get(self, "dashboardDescription"))

    @dashboard_description.setter
    def dashboard_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fb0c1b10a24ea78c92402fd30755eb29396ab4f47010b34801ee6fee3a5ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardDescription", value)

    @builtins.property
    @jsii.member(jsii_name="dashboardName")
    def dashboard_name(self) -> builtins.str:
        '''A friendly name for the dashboard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboardname
        '''
        return typing.cast(builtins.str, jsii.get(self, "dashboardName"))

    @dashboard_name.setter
    def dashboard_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231fc3b4b2a5a6f08a94f233f682f89d20187d871d8bbe82ce63a2970fd0e3d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardName", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which to create the dashboard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-projectid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2caa58d512b8209d37d4e8552758a43b1a90319755c5b22f3667b74e1bf03cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnDashboardProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_definition": "dashboardDefinition",
        "dashboard_description": "dashboardDescription",
        "dashboard_name": "dashboardName",
        "project_id": "projectId",
        "tags": "tags",
    },
)
class CfnDashboardProps:
    def __init__(
        self,
        *,
        dashboard_definition: builtins.str,
        dashboard_description: builtins.str,
        dashboard_name: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDashboard``.

        :param dashboard_definition: The dashboard definition specified in a JSON literal. For detailed information, see `Creating dashboards (CLI) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-dashboards-using-aws-cli.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param dashboard_description: A description for the dashboard.
        :param dashboard_name: A friendly name for the dashboard.
        :param project_id: The ID of the project in which to create the dashboard.
        :param tags: A list of key-value pairs that contain metadata for the dashboard. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotsitewise as iotsitewise
            
            cfn_dashboard_props = iotsitewise.CfnDashboardProps(
                dashboard_definition="dashboardDefinition",
                dashboard_description="dashboardDescription",
                dashboard_name="dashboardName",
            
                # the properties below are optional
                project_id="projectId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6ee9d942ba586d74957260ddccdb165f88229f9fa89e5ef637d17997fd9b6c)
            check_type(argname="argument dashboard_definition", value=dashboard_definition, expected_type=type_hints["dashboard_definition"])
            check_type(argname="argument dashboard_description", value=dashboard_description, expected_type=type_hints["dashboard_description"])
            check_type(argname="argument dashboard_name", value=dashboard_name, expected_type=type_hints["dashboard_name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dashboard_definition": dashboard_definition,
            "dashboard_description": dashboard_description,
            "dashboard_name": dashboard_name,
        }
        if project_id is not None:
            self._values["project_id"] = project_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dashboard_definition(self) -> builtins.str:
        '''The dashboard definition specified in a JSON literal.

        For detailed information, see `Creating dashboards (CLI) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-dashboards-using-aws-cli.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboarddefinition
        '''
        result = self._values.get("dashboard_definition")
        assert result is not None, "Required property 'dashboard_definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashboard_description(self) -> builtins.str:
        '''A description for the dashboard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboarddescription
        '''
        result = self._values.get("dashboard_description")
        assert result is not None, "Required property 'dashboard_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashboard_name(self) -> builtins.str:
        '''A friendly name for the dashboard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboardname
        '''
        result = self._values.get("dashboard_name")
        assert result is not None, "Required property 'dashboard_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which to create the dashboard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-projectid
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs that contain metadata for the dashboard.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDashboardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnGateway(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnGateway",
):
    '''A CloudFormation ``AWS::IoTSiteWise::Gateway``.

    Creates a gateway, which is a virtual or edge device that delivers industrial data streams from local servers to AWS IoT SiteWise . For more information, see `Ingesting data using a gateway <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/gateway-connector.html>`_ in the *AWS IoT SiteWise User Guide* .

    :cloudformationResource: AWS::IoTSiteWise::Gateway
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotsitewise as iotsitewise
        
        cfn_gateway = iotsitewise.CfnGateway(self, "MyCfnGateway",
            gateway_name="gatewayName",
            gateway_platform=iotsitewise.CfnGateway.GatewayPlatformProperty(
                greengrass=iotsitewise.CfnGateway.GreengrassProperty(
                    group_arn="groupArn"
                ),
                greengrass_v2=iotsitewise.CfnGateway.GreengrassV2Property(
                    core_device_thing_name="coreDeviceThingName"
                )
            ),
        
            # the properties below are optional
            gateway_capability_summaries=[iotsitewise.CfnGateway.GatewayCapabilitySummaryProperty(
                capability_namespace="capabilityNamespace",
        
                # the properties below are optional
                capability_configuration="capabilityConfiguration"
            )],
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
        gateway_name: builtins.str,
        gateway_platform: typing.Union[typing.Union["CfnGateway.GatewayPlatformProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        gateway_capability_summaries: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGateway.GatewayCapabilitySummaryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTSiteWise::Gateway``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param gateway_name: A unique, friendly name for the gateway. The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .
        :param gateway_platform: The gateway's platform. You can only specify one platform in a gateway.
        :param gateway_capability_summaries: A list of gateway capability summaries that each contain a namespace and status. Each gateway capability defines data sources for the gateway. To retrieve a capability configuration's definition, use `DescribeGatewayCapabilityConfiguration <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_DescribeGatewayCapabilityConfiguration.html>`_ .
        :param tags: A list of key-value pairs that contain metadata for the gateway. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d53b74302718d523a743fe57196e047103221fef32f018b73d730533cb593f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGatewayProps(
            gateway_name=gateway_name,
            gateway_platform=gateway_platform,
            gateway_capability_summaries=gateway_capability_summaries,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665e5d8aea349859d06db1ae6130d7cda980b3125ffe4aec449037b56d347f18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4287ff40593a7fbb69bf0ed14a34e82f0bd8bf91fb0d2267bca2a94a16f4e921)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrGatewayId")
    def attr_gateway_id(self) -> builtins.str:
        '''The ID for the gateway.

        :cloudformationAttribute: GatewayId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs that contain metadata for the gateway.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="gatewayName")
    def gateway_name(self) -> builtins.str:
        '''A unique, friendly name for the gateway.

        The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayname
        '''
        return typing.cast(builtins.str, jsii.get(self, "gatewayName"))

    @gateway_name.setter
    def gateway_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1eb9833f5018fbca4447f8e7644dc82a9c077fc5d141cde84f454b89b91aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayName", value)

    @builtins.property
    @jsii.member(jsii_name="gatewayPlatform")
    def gateway_platform(
        self,
    ) -> typing.Union["CfnGateway.GatewayPlatformProperty", _IResolvable_a771d0ef]:
        '''The gateway's platform.

        You can only specify one platform in a gateway.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayplatform
        '''
        return typing.cast(typing.Union["CfnGateway.GatewayPlatformProperty", _IResolvable_a771d0ef], jsii.get(self, "gatewayPlatform"))

    @gateway_platform.setter
    def gateway_platform(
        self,
        value: typing.Union["CfnGateway.GatewayPlatformProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3c93e7da72202ece397b651c9bb82489ad10738ef49489d036b4e3409f8320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayPlatform", value)

    @builtins.property
    @jsii.member(jsii_name="gatewayCapabilitySummaries")
    def gateway_capability_summaries(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGateway.GatewayCapabilitySummaryProperty", _IResolvable_a771d0ef]]]]:
        '''A list of gateway capability summaries that each contain a namespace and status.

        Each gateway capability defines data sources for the gateway. To retrieve a capability configuration's definition, use `DescribeGatewayCapabilityConfiguration <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_DescribeGatewayCapabilityConfiguration.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewaycapabilitysummaries
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGateway.GatewayCapabilitySummaryProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "gatewayCapabilitySummaries"))

    @gateway_capability_summaries.setter
    def gateway_capability_summaries(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGateway.GatewayCapabilitySummaryProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80e2fc5b35e8bcc37f9cecc2c1ecc3fbaeaaf420086ed636cb07f2b52e7e561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayCapabilitySummaries", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnGateway.GatewayCapabilitySummaryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capability_namespace": "capabilityNamespace",
            "capability_configuration": "capabilityConfiguration",
        },
    )
    class GatewayCapabilitySummaryProperty:
        def __init__(
            self,
            *,
            capability_namespace: builtins.str,
            capability_configuration: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains a summary of a gateway capability configuration.

            :param capability_namespace: The namespace of the capability configuration. For example, if you configure OPC-UA sources from the AWS IoT SiteWise console, your OPC-UA capability configuration has the namespace ``iotsitewise:opcuacollector:version`` , where ``version`` is a number such as ``1`` . The maximum length is 512 characters with the pattern ``^[a-zA-Z]+:[a-zA-Z]+:[0-9]+$`` .
            :param capability_configuration: The JSON document that defines the configuration for the gateway capability. For more information, see `Configuring data sources (CLI) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/configure-sources.html#configure-source-cli>`_ in the *AWS IoT SiteWise User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                gateway_capability_summary_property = iotsitewise.CfnGateway.GatewayCapabilitySummaryProperty(
                    capability_namespace="capabilityNamespace",
                
                    # the properties below are optional
                    capability_configuration="capabilityConfiguration"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6702e00a58298464d58b0febd2052fd24368105f1c0ff63929a3a35daebc060b)
                check_type(argname="argument capability_namespace", value=capability_namespace, expected_type=type_hints["capability_namespace"])
                check_type(argname="argument capability_configuration", value=capability_configuration, expected_type=type_hints["capability_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "capability_namespace": capability_namespace,
            }
            if capability_configuration is not None:
                self._values["capability_configuration"] = capability_configuration

        @builtins.property
        def capability_namespace(self) -> builtins.str:
            '''The namespace of the capability configuration.

            For example, if you configure OPC-UA sources from the AWS IoT SiteWise console, your OPC-UA capability configuration has the namespace ``iotsitewise:opcuacollector:version`` , where ``version`` is a number such as ``1`` .

            The maximum length is 512 characters with the pattern ``^[a-zA-Z]+:[a-zA-Z]+:[0-9]+$`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html#cfn-iotsitewise-gateway-gatewaycapabilitysummary-capabilitynamespace
            '''
            result = self._values.get("capability_namespace")
            assert result is not None, "Required property 'capability_namespace' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def capability_configuration(self) -> typing.Optional[builtins.str]:
            '''The JSON document that defines the configuration for the gateway capability.

            For more information, see `Configuring data sources (CLI) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/configure-sources.html#configure-source-cli>`_ in the *AWS IoT SiteWise User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html#cfn-iotsitewise-gateway-gatewaycapabilitysummary-capabilityconfiguration
            '''
            result = self._values.get("capability_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayCapabilitySummaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnGateway.GatewayPlatformProperty",
        jsii_struct_bases=[],
        name_mapping={"greengrass": "greengrass", "greengrass_v2": "greengrassV2"},
    )
    class GatewayPlatformProperty:
        def __init__(
            self,
            *,
            greengrass: typing.Optional[typing.Union[typing.Union["CfnGateway.GreengrassProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            greengrass_v2: typing.Optional[typing.Union[typing.Union["CfnGateway.GreengrassV2Property", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains a gateway's platform information.

            :param greengrass: A gateway that runs on AWS IoT Greengrass .
            :param greengrass_v2: A gateway that runs on AWS IoT Greengrass V2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                gateway_platform_property = iotsitewise.CfnGateway.GatewayPlatformProperty(
                    greengrass=iotsitewise.CfnGateway.GreengrassProperty(
                        group_arn="groupArn"
                    ),
                    greengrass_v2=iotsitewise.CfnGateway.GreengrassV2Property(
                        core_device_thing_name="coreDeviceThingName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7193722bb6bfb21853fb93008af714c6021d79bd089013909ab2f30e099174ba)
                check_type(argname="argument greengrass", value=greengrass, expected_type=type_hints["greengrass"])
                check_type(argname="argument greengrass_v2", value=greengrass_v2, expected_type=type_hints["greengrass_v2"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if greengrass is not None:
                self._values["greengrass"] = greengrass
            if greengrass_v2 is not None:
                self._values["greengrass_v2"] = greengrass_v2

        @builtins.property
        def greengrass(
            self,
        ) -> typing.Optional[typing.Union["CfnGateway.GreengrassProperty", _IResolvable_a771d0ef]]:
            '''A gateway that runs on AWS IoT Greengrass .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html#cfn-iotsitewise-gateway-gatewayplatform-greengrass
            '''
            result = self._values.get("greengrass")
            return typing.cast(typing.Optional[typing.Union["CfnGateway.GreengrassProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def greengrass_v2(
            self,
        ) -> typing.Optional[typing.Union["CfnGateway.GreengrassV2Property", _IResolvable_a771d0ef]]:
            '''A gateway that runs on AWS IoT Greengrass V2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html#cfn-iotsitewise-gateway-gatewayplatform-greengrassv2
            '''
            result = self._values.get("greengrass_v2")
            return typing.cast(typing.Optional[typing.Union["CfnGateway.GreengrassV2Property", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayPlatformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnGateway.GreengrassProperty",
        jsii_struct_bases=[],
        name_mapping={"group_arn": "groupArn"},
    )
    class GreengrassProperty:
        def __init__(self, *, group_arn: builtins.str) -> None:
            '''Contains details for a gateway that runs on AWS IoT Greengrass .

            To create a gateway that runs on AWS IoT Greengrass , you must add the IoT SiteWise connector to a Greengrass group and deploy it. Your Greengrass group must also have permissions to upload data to AWS IoT SiteWise . For more information, see `Ingesting data using a gateway <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/gateway-connector.html>`_ in the *AWS IoT SiteWise User Guide* .

            :param group_arn: The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the Greengrass group. For more information about how to find a group's ARN, see `ListGroups <https://docs.aws.amazon.com/greengrass/latest/apireference/listgroups-get.html>`_ and `GetGroup <https://docs.aws.amazon.com/greengrass/latest/apireference/getgroup-get.html>`_ in the *AWS IoT Greengrass API Reference* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrass.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                greengrass_property = iotsitewise.CfnGateway.GreengrassProperty(
                    group_arn="groupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d7828a2b50e9a8797f05fe36706d5990fba069eb72bb7de3eb21128efe67134)
                check_type(argname="argument group_arn", value=group_arn, expected_type=type_hints["group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "group_arn": group_arn,
            }

        @builtins.property
        def group_arn(self) -> builtins.str:
            '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the Greengrass group. For more information about how to find a group's ARN, see `ListGroups <https://docs.aws.amazon.com/greengrass/latest/apireference/listgroups-get.html>`_ and `GetGroup <https://docs.aws.amazon.com/greengrass/latest/apireference/getgroup-get.html>`_ in the *AWS IoT Greengrass API Reference* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrass.html#cfn-iotsitewise-gateway-greengrass-grouparn
            '''
            result = self._values.get("group_arn")
            assert result is not None, "Required property 'group_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GreengrassProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnGateway.GreengrassV2Property",
        jsii_struct_bases=[],
        name_mapping={"core_device_thing_name": "coreDeviceThingName"},
    )
    class GreengrassV2Property:
        def __init__(self, *, core_device_thing_name: builtins.str) -> None:
            '''Contains details for a gateway that runs on AWS IoT Greengrass V2.

            To create a gateway that runs on AWS IoT Greengrass V2, you must deploy the IoT SiteWise Edge component to your gateway device. Your `Greengrass device role <https://docs.aws.amazon.com/greengrass/v2/developerguide/device-service-role.html>`_ must use the ``AWSIoTSiteWiseEdgeAccess`` policy. For more information, see `Using AWS IoT SiteWise at the edge <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/sw-gateways.html>`_ in the *AWS IoT SiteWise User Guide* .

            :param core_device_thing_name: The name of the AWS IoT thing for your AWS IoT Greengrass V2 core device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrassv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                greengrass_v2_property = iotsitewise.CfnGateway.GreengrassV2Property(
                    core_device_thing_name="coreDeviceThingName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8871ac425610b1143d26c45b21bffb0dd2cd38d24c4ada03f64dfb1e27374123)
                check_type(argname="argument core_device_thing_name", value=core_device_thing_name, expected_type=type_hints["core_device_thing_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "core_device_thing_name": core_device_thing_name,
            }

        @builtins.property
        def core_device_thing_name(self) -> builtins.str:
            '''The name of the AWS IoT thing for your AWS IoT Greengrass V2 core device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrassv2.html#cfn-iotsitewise-gateway-greengrassv2-coredevicethingname
            '''
            result = self._values.get("core_device_thing_name")
            assert result is not None, "Required property 'core_device_thing_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GreengrassV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_name": "gatewayName",
        "gateway_platform": "gatewayPlatform",
        "gateway_capability_summaries": "gatewayCapabilitySummaries",
        "tags": "tags",
    },
)
class CfnGatewayProps:
    def __init__(
        self,
        *,
        gateway_name: builtins.str,
        gateway_platform: typing.Union[typing.Union[CfnGateway.GatewayPlatformProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        gateway_capability_summaries: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGateway.GatewayCapabilitySummaryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGateway``.

        :param gateway_name: A unique, friendly name for the gateway. The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .
        :param gateway_platform: The gateway's platform. You can only specify one platform in a gateway.
        :param gateway_capability_summaries: A list of gateway capability summaries that each contain a namespace and status. Each gateway capability defines data sources for the gateway. To retrieve a capability configuration's definition, use `DescribeGatewayCapabilityConfiguration <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_DescribeGatewayCapabilityConfiguration.html>`_ .
        :param tags: A list of key-value pairs that contain metadata for the gateway. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotsitewise as iotsitewise
            
            cfn_gateway_props = iotsitewise.CfnGatewayProps(
                gateway_name="gatewayName",
                gateway_platform=iotsitewise.CfnGateway.GatewayPlatformProperty(
                    greengrass=iotsitewise.CfnGateway.GreengrassProperty(
                        group_arn="groupArn"
                    ),
                    greengrass_v2=iotsitewise.CfnGateway.GreengrassV2Property(
                        core_device_thing_name="coreDeviceThingName"
                    )
                ),
            
                # the properties below are optional
                gateway_capability_summaries=[iotsitewise.CfnGateway.GatewayCapabilitySummaryProperty(
                    capability_namespace="capabilityNamespace",
            
                    # the properties below are optional
                    capability_configuration="capabilityConfiguration"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f938d14a9b6a4fbc0c4e1da31690ae58ca7becce9d79786d7825803089f4e8)
            check_type(argname="argument gateway_name", value=gateway_name, expected_type=type_hints["gateway_name"])
            check_type(argname="argument gateway_platform", value=gateway_platform, expected_type=type_hints["gateway_platform"])
            check_type(argname="argument gateway_capability_summaries", value=gateway_capability_summaries, expected_type=type_hints["gateway_capability_summaries"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_name": gateway_name,
            "gateway_platform": gateway_platform,
        }
        if gateway_capability_summaries is not None:
            self._values["gateway_capability_summaries"] = gateway_capability_summaries
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def gateway_name(self) -> builtins.str:
        '''A unique, friendly name for the gateway.

        The maximum length is 256 characters with the pattern ``[^\\ u0000-\\ u001F\\ u007F]+`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayname
        '''
        result = self._values.get("gateway_name")
        assert result is not None, "Required property 'gateway_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway_platform(
        self,
    ) -> typing.Union[CfnGateway.GatewayPlatformProperty, _IResolvable_a771d0ef]:
        '''The gateway's platform.

        You can only specify one platform in a gateway.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayplatform
        '''
        result = self._values.get("gateway_platform")
        assert result is not None, "Required property 'gateway_platform' is missing"
        return typing.cast(typing.Union[CfnGateway.GatewayPlatformProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def gateway_capability_summaries(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGateway.GatewayCapabilitySummaryProperty, _IResolvable_a771d0ef]]]]:
        '''A list of gateway capability summaries that each contain a namespace and status.

        Each gateway capability defines data sources for the gateway. To retrieve a capability configuration's definition, use `DescribeGatewayCapabilityConfiguration <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_DescribeGatewayCapabilityConfiguration.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewaycapabilitysummaries
        '''
        result = self._values.get("gateway_capability_summaries")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGateway.GatewayCapabilitySummaryProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs that contain metadata for the gateway.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPortal(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnPortal",
):
    '''A CloudFormation ``AWS::IoTSiteWise::Portal``.

    Creates a portal, which can contain projects and dashboards. Before you can create a portal, you must enable IAM Identity Center . AWS IoT SiteWise Monitor uses IAM Identity Center to manage user permissions. For more information, see `Enabling IAM Identity Center <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-get-started.html#mon-gs-sso>`_ in the *AWS IoT SiteWise User Guide* .
    .. epigraph::

       Before you can sign in to a new portal, you must add at least one IAM Identity Center user or group to that portal. For more information, see `Adding or removing portal administrators <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/administer-portals.html#portal-change-admins>`_ in the *AWS IoT SiteWise User Guide* .

    :cloudformationResource: AWS::IoTSiteWise::Portal
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotsitewise as iotsitewise
        
        # alarms: Any
        
        cfn_portal = iotsitewise.CfnPortal(self, "MyCfnPortal",
            portal_contact_email="portalContactEmail",
            portal_name="portalName",
            role_arn="roleArn",
        
            # the properties below are optional
            alarms=alarms,
            notification_sender_email="notificationSenderEmail",
            portal_auth_mode="portalAuthMode",
            portal_description="portalDescription",
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
        portal_contact_email: builtins.str,
        portal_name: builtins.str,
        role_arn: builtins.str,
        alarms: typing.Any = None,
        notification_sender_email: typing.Optional[builtins.str] = None,
        portal_auth_mode: typing.Optional[builtins.str] = None,
        portal_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTSiteWise::Portal``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param portal_contact_email: The AWS administrator's contact email address.
        :param portal_name: A friendly name for the portal.
        :param role_arn: The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf. For more information, see `Using service roles for AWS IoT SiteWise Monitor <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-service-role.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param alarms: Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range. For more information, see `Monitoring with alarms <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/monitor-alarms.html>`_ in the *AWS IoT SiteWise Application Guide* .
        :param notification_sender_email: The email address that sends alarm notifications. .. epigraph:: If you use the `AWS IoT Events managed Lambda function <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ to manage your emails, you must `verify the sender email address in Amazon SES <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html>`_ .
        :param portal_auth_mode: The service to use to authenticate users to the portal. Choose from the following options:. - ``SSO`` – The portal uses AWS IAM Identity Center (successor to AWS Single Sign-On) to authenticate users and manage user permissions. Before you can create a portal that uses IAM Identity Center , you must enable IAM Identity Center . For more information, see `Enabling IAM Identity Center <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-get-started.html#mon-gs-sso>`_ in the *AWS IoT SiteWise User Guide* . This option is only available in AWS Regions other than the China Regions. - ``IAM`` – The portal uses AWS Identity and Access Management ( IAM ) to authenticate users and manage user permissions. You can't change this value after you create a portal. Default: ``SSO``
        :param portal_description: A description for the portal.
        :param tags: A list of key-value pairs that contain metadata for the portal. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c274b13695fef7c603b4b4b8920779d4dc3a74bd0838e94ada15249d3cdafe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPortalProps(
            portal_contact_email=portal_contact_email,
            portal_name=portal_name,
            role_arn=role_arn,
            alarms=alarms,
            notification_sender_email=notification_sender_email,
            portal_auth_mode=portal_auth_mode,
            portal_description=portal_description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1ac03ae2dd653d135dde67a7bbe52b447a0b669e7d51d3d4de9970c55ce6cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36ff1961d2bcd28a0e9baa513d1d5394b686931aa136ca7f2fd3e35df1c7796f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPortalArn")
    def attr_portal_arn(self) -> builtins.str:
        '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the portal, which has the following format.

        ``arn:${Partition}:iotsitewise:${Region}:${Account}:portal/${PortalId}``

        :cloudformationAttribute: PortalArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPortalArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPortalClientId")
    def attr_portal_client_id(self) -> builtins.str:
        '''The IAM Identity Center application generated client ID (used with IAM Identity Center APIs).

        :cloudformationAttribute: PortalClientId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPortalClientId"))

    @builtins.property
    @jsii.member(jsii_name="attrPortalId")
    def attr_portal_id(self) -> builtins.str:
        '''The ID of the created portal.

        :cloudformationAttribute: PortalId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPortalId"))

    @builtins.property
    @jsii.member(jsii_name="attrPortalStartUrl")
    def attr_portal_start_url(self) -> builtins.str:
        '''The public URL for the AWS IoT SiteWise Monitor portal.

        :cloudformationAttribute: PortalStartUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPortalStartUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs that contain metadata for the portal.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="alarms")
    def alarms(self) -> typing.Any:
        '''Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal.

        You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range. For more information, see `Monitoring with alarms <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/monitor-alarms.html>`_ in the *AWS IoT SiteWise Application Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-alarms
        '''
        return typing.cast(typing.Any, jsii.get(self, "alarms"))

    @alarms.setter
    def alarms(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea621311b98ea517807c4b48c7be95b4dd84a9b1bfdc699bb4657b7df587c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarms", value)

    @builtins.property
    @jsii.member(jsii_name="portalContactEmail")
    def portal_contact_email(self) -> builtins.str:
        '''The AWS administrator's contact email address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalcontactemail
        '''
        return typing.cast(builtins.str, jsii.get(self, "portalContactEmail"))

    @portal_contact_email.setter
    def portal_contact_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22083d4b6f65d19f20d6644e6c34d96c78c5380e5fba248ee71d245f5b8587ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portalContactEmail", value)

    @builtins.property
    @jsii.member(jsii_name="portalName")
    def portal_name(self) -> builtins.str:
        '''A friendly name for the portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalname
        '''
        return typing.cast(builtins.str, jsii.get(self, "portalName"))

    @portal_name.setter
    def portal_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a662556ade4361b0ff1ef68bdaf9d5d5cd98c7851bd054b2230b49d4530435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portalName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf. For more information, see `Using service roles for AWS IoT SiteWise Monitor <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-service-role.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e012188f3b6c360ba0712c202106ad684113fb4fc473d8643987eb3e56e0c763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="notificationSenderEmail")
    def notification_sender_email(self) -> typing.Optional[builtins.str]:
        '''The email address that sends alarm notifications.

        .. epigraph::

           If you use the `AWS IoT Events managed Lambda function <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ to manage your emails, you must `verify the sender email address in Amazon SES <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-notificationsenderemail
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationSenderEmail"))

    @notification_sender_email.setter
    def notification_sender_email(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee99027a1a40c54fa3d597db0b8e6f0c267452c3a61740858cd3a867c92a7e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationSenderEmail", value)

    @builtins.property
    @jsii.member(jsii_name="portalAuthMode")
    def portal_auth_mode(self) -> typing.Optional[builtins.str]:
        '''The service to use to authenticate users to the portal. Choose from the following options:.

        - ``SSO`` – The portal uses AWS IAM Identity Center (successor to AWS Single Sign-On) to authenticate users and manage user permissions. Before you can create a portal that uses IAM Identity Center , you must enable IAM Identity Center . For more information, see `Enabling IAM Identity Center <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-get-started.html#mon-gs-sso>`_ in the *AWS IoT SiteWise User Guide* . This option is only available in AWS Regions other than the China Regions.
        - ``IAM`` – The portal uses AWS Identity and Access Management ( IAM ) to authenticate users and manage user permissions.

        You can't change this value after you create a portal.

        Default: ``SSO``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalauthmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portalAuthMode"))

    @portal_auth_mode.setter
    def portal_auth_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca026081589f8f41e178c5c68c985445d90c0dd2ff63fcbed32ef518536b93e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portalAuthMode", value)

    @builtins.property
    @jsii.member(jsii_name="portalDescription")
    def portal_description(self) -> typing.Optional[builtins.str]:
        '''A description for the portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portaldescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portalDescription"))

    @portal_description.setter
    def portal_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60beb4d77540c6aa0844f34c0e4c69ae0b737ef7c70a33865a48e39862ff86f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portalDescription", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnPortal.AlarmsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarm_role_arn": "alarmRoleArn",
            "notification_lambda_arn": "notificationLambdaArn",
        },
    )
    class AlarmsProperty:
        def __init__(
            self,
            *,
            alarm_role_arn: typing.Optional[builtins.str] = None,
            notification_lambda_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal.

            You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range. For more information, see `Monitoring with alarms <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/monitor-alarms.html>`_ in the *AWS IoT SiteWise Application Guide* .

            :param alarm_role_arn: The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the IAM role that allows the alarm to perform actions and access AWS resources and services, such as AWS IoT Events .
            :param notification_lambda_arn: The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the Lambda function that manages alarm notifications. For more information, see `Managing alarm notifications <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ in the *AWS IoT Events Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-portal-alarms.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotsitewise as iotsitewise
                
                alarms_property = iotsitewise.CfnPortal.AlarmsProperty(
                    alarm_role_arn="alarmRoleArn",
                    notification_lambda_arn="notificationLambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6ee2833e479e93bbfaf58496fc88ee9ea008fde7274c9813d27c7e20dda453f)
                check_type(argname="argument alarm_role_arn", value=alarm_role_arn, expected_type=type_hints["alarm_role_arn"])
                check_type(argname="argument notification_lambda_arn", value=notification_lambda_arn, expected_type=type_hints["notification_lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_role_arn is not None:
                self._values["alarm_role_arn"] = alarm_role_arn
            if notification_lambda_arn is not None:
                self._values["notification_lambda_arn"] = notification_lambda_arn

        @builtins.property
        def alarm_role_arn(self) -> typing.Optional[builtins.str]:
            '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the IAM role that allows the alarm to perform actions and access AWS resources and services, such as AWS IoT Events .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-portal-alarms.html#cfn-iotsitewise-portal-alarms-alarmrolearn
            '''
            result = self._values.get("alarm_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the Lambda function that manages alarm notifications. For more information, see `Managing alarm notifications <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ in the *AWS IoT Events Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-portal-alarms.html#cfn-iotsitewise-portal-alarms-notificationlambdaarn
            '''
            result = self._values.get("notification_lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnPortalProps",
    jsii_struct_bases=[],
    name_mapping={
        "portal_contact_email": "portalContactEmail",
        "portal_name": "portalName",
        "role_arn": "roleArn",
        "alarms": "alarms",
        "notification_sender_email": "notificationSenderEmail",
        "portal_auth_mode": "portalAuthMode",
        "portal_description": "portalDescription",
        "tags": "tags",
    },
)
class CfnPortalProps:
    def __init__(
        self,
        *,
        portal_contact_email: builtins.str,
        portal_name: builtins.str,
        role_arn: builtins.str,
        alarms: typing.Any = None,
        notification_sender_email: typing.Optional[builtins.str] = None,
        portal_auth_mode: typing.Optional[builtins.str] = None,
        portal_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPortal``.

        :param portal_contact_email: The AWS administrator's contact email address.
        :param portal_name: A friendly name for the portal.
        :param role_arn: The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf. For more information, see `Using service roles for AWS IoT SiteWise Monitor <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-service-role.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param alarms: Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range. For more information, see `Monitoring with alarms <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/monitor-alarms.html>`_ in the *AWS IoT SiteWise Application Guide* .
        :param notification_sender_email: The email address that sends alarm notifications. .. epigraph:: If you use the `AWS IoT Events managed Lambda function <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ to manage your emails, you must `verify the sender email address in Amazon SES <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html>`_ .
        :param portal_auth_mode: The service to use to authenticate users to the portal. Choose from the following options:. - ``SSO`` – The portal uses AWS IAM Identity Center (successor to AWS Single Sign-On) to authenticate users and manage user permissions. Before you can create a portal that uses IAM Identity Center , you must enable IAM Identity Center . For more information, see `Enabling IAM Identity Center <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-get-started.html#mon-gs-sso>`_ in the *AWS IoT SiteWise User Guide* . This option is only available in AWS Regions other than the China Regions. - ``IAM`` – The portal uses AWS Identity and Access Management ( IAM ) to authenticate users and manage user permissions. You can't change this value after you create a portal. Default: ``SSO``
        :param portal_description: A description for the portal.
        :param tags: A list of key-value pairs that contain metadata for the portal. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotsitewise as iotsitewise
            
            # alarms: Any
            
            cfn_portal_props = iotsitewise.CfnPortalProps(
                portal_contact_email="portalContactEmail",
                portal_name="portalName",
                role_arn="roleArn",
            
                # the properties below are optional
                alarms=alarms,
                notification_sender_email="notificationSenderEmail",
                portal_auth_mode="portalAuthMode",
                portal_description="portalDescription",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a729c0eef48e5fe2740b3cf099bdccad7e32dffeaccbb83070eecf41d1726a)
            check_type(argname="argument portal_contact_email", value=portal_contact_email, expected_type=type_hints["portal_contact_email"])
            check_type(argname="argument portal_name", value=portal_name, expected_type=type_hints["portal_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
            check_type(argname="argument notification_sender_email", value=notification_sender_email, expected_type=type_hints["notification_sender_email"])
            check_type(argname="argument portal_auth_mode", value=portal_auth_mode, expected_type=type_hints["portal_auth_mode"])
            check_type(argname="argument portal_description", value=portal_description, expected_type=type_hints["portal_description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portal_contact_email": portal_contact_email,
            "portal_name": portal_name,
            "role_arn": role_arn,
        }
        if alarms is not None:
            self._values["alarms"] = alarms
        if notification_sender_email is not None:
            self._values["notification_sender_email"] = notification_sender_email
        if portal_auth_mode is not None:
            self._values["portal_auth_mode"] = portal_auth_mode
        if portal_description is not None:
            self._values["portal_description"] = portal_description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def portal_contact_email(self) -> builtins.str:
        '''The AWS administrator's contact email address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalcontactemail
        '''
        result = self._values.get("portal_contact_email")
        assert result is not None, "Required property 'portal_contact_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def portal_name(self) -> builtins.str:
        '''A friendly name for the portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalname
        '''
        result = self._values.get("portal_name")
        assert result is not None, "Required property 'portal_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf. For more information, see `Using service roles for AWS IoT SiteWise Monitor <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-service-role.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarms(self) -> typing.Any:
        '''Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal.

        You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range. For more information, see `Monitoring with alarms <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/monitor-alarms.html>`_ in the *AWS IoT SiteWise Application Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-alarms
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Any, result)

    @builtins.property
    def notification_sender_email(self) -> typing.Optional[builtins.str]:
        '''The email address that sends alarm notifications.

        .. epigraph::

           If you use the `AWS IoT Events managed Lambda function <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ to manage your emails, you must `verify the sender email address in Amazon SES <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-notificationsenderemail
        '''
        result = self._values.get("notification_sender_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_auth_mode(self) -> typing.Optional[builtins.str]:
        '''The service to use to authenticate users to the portal. Choose from the following options:.

        - ``SSO`` – The portal uses AWS IAM Identity Center (successor to AWS Single Sign-On) to authenticate users and manage user permissions. Before you can create a portal that uses IAM Identity Center , you must enable IAM Identity Center . For more information, see `Enabling IAM Identity Center <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-get-started.html#mon-gs-sso>`_ in the *AWS IoT SiteWise User Guide* . This option is only available in AWS Regions other than the China Regions.
        - ``IAM`` – The portal uses AWS Identity and Access Management ( IAM ) to authenticate users and manage user permissions.

        You can't change this value after you create a portal.

        Default: ``SSO``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalauthmode
        '''
        result = self._values.get("portal_auth_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_description(self) -> typing.Optional[builtins.str]:
        '''A description for the portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portaldescription
        '''
        result = self._values.get("portal_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs that contain metadata for the portal.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortalProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnProject(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnProject",
):
    '''A CloudFormation ``AWS::IoTSiteWise::Project``.

    Creates a project in the specified portal.
    .. epigraph::

       Make sure that the project name and description don't contain confidential information.

    :cloudformationResource: AWS::IoTSiteWise::Project
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotsitewise as iotsitewise
        
        cfn_project = iotsitewise.CfnProject(self, "MyCfnProject",
            portal_id="portalId",
            project_name="projectName",
        
            # the properties below are optional
            asset_ids=["assetIds"],
            project_description="projectDescription",
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
        portal_id: builtins.str,
        project_name: builtins.str,
        asset_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTSiteWise::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param portal_id: The ID of the portal in which to create the project.
        :param project_name: A friendly name for the project.
        :param asset_ids: A list that contains the IDs of each asset associated with the project.
        :param project_description: A description for the project.
        :param tags: A list of key-value pairs that contain metadata for the project. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8512b1288ab049b8c8d4f3586964c19de269fc35eaf89a52b30cfa417e7104a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProjectProps(
            portal_id=portal_id,
            project_name=project_name,
            asset_ids=asset_ids,
            project_description=project_description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f2327468458f28ce86229aeeb63e42179a0b78ed382556d4f074002810155c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a8809d29fb363e2680dfc675882f37177b15af0b49a982d53f2aa2394400c41)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrProjectArn")
    def attr_project_arn(self) -> builtins.str:
        '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the project, which has the following format.

        ``arn:${Partition}:iotsitewise:${Region}:${Account}:project/${ProjectId}``

        :cloudformationAttribute: ProjectArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProjectArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProjectId")
    def attr_project_id(self) -> builtins.str:
        '''The ID of the project.

        :cloudformationAttribute: ProjectId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProjectId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs that contain metadata for the project.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="portalId")
    def portal_id(self) -> builtins.str:
        '''The ID of the portal in which to create the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-portalid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portalId"))

    @portal_id.setter
    def portal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a267773edfca5523fdf4ab8e3a51362a53c0b6e073b22c9a8a23ab2a88ab08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portalId", value)

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        '''A friendly name for the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-projectname
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectName"))

    @project_name.setter
    def project_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3068c0da6dde7760b27d6aeecd6771738cc726b374b50a2b1aa07021fda1e185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectName", value)

    @builtins.property
    @jsii.member(jsii_name="assetIds")
    def asset_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list that contains the IDs of each asset associated with the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-assetids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "assetIds"))

    @asset_ids.setter
    def asset_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cc2575f01de3cac5110362c6e540d140104d101fe2d952d41a319dfbec12f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetIds", value)

    @builtins.property
    @jsii.member(jsii_name="projectDescription")
    def project_description(self) -> typing.Optional[builtins.str]:
        '''A description for the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-projectdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDescription"))

    @project_description.setter
    def project_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80e29d91792a41d8f04f0b8e445819b8e5d677163a5785d437248c72573ef20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectDescription", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "portal_id": "portalId",
        "project_name": "projectName",
        "asset_ids": "assetIds",
        "project_description": "projectDescription",
        "tags": "tags",
    },
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        portal_id: builtins.str,
        project_name: builtins.str,
        asset_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProject``.

        :param portal_id: The ID of the portal in which to create the project.
        :param project_name: A friendly name for the project.
        :param asset_ids: A list that contains the IDs of each asset associated with the project.
        :param project_description: A description for the project.
        :param tags: A list of key-value pairs that contain metadata for the project. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotsitewise as iotsitewise
            
            cfn_project_props = iotsitewise.CfnProjectProps(
                portal_id="portalId",
                project_name="projectName",
            
                # the properties below are optional
                asset_ids=["assetIds"],
                project_description="projectDescription",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9646d2fe343823301252919daec281e87db3b740aba797b2371074f9b99ebfae)
            check_type(argname="argument portal_id", value=portal_id, expected_type=type_hints["portal_id"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument asset_ids", value=asset_ids, expected_type=type_hints["asset_ids"])
            check_type(argname="argument project_description", value=project_description, expected_type=type_hints["project_description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portal_id": portal_id,
            "project_name": project_name,
        }
        if asset_ids is not None:
            self._values["asset_ids"] = asset_ids
        if project_description is not None:
            self._values["project_description"] = project_description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def portal_id(self) -> builtins.str:
        '''The ID of the portal in which to create the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-portalid
        '''
        result = self._values.get("portal_id")
        assert result is not None, "Required property 'portal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_name(self) -> builtins.str:
        '''A friendly name for the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-projectname
        '''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list that contains the IDs of each asset associated with the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-assetids
        '''
        result = self._values.get("asset_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project_description(self) -> typing.Optional[builtins.str]:
        '''A description for the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-projectdescription
        '''
        result = self._values.get("project_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs that contain metadata for the project.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAccessPolicy",
    "CfnAccessPolicyProps",
    "CfnAsset",
    "CfnAssetModel",
    "CfnAssetModelProps",
    "CfnAssetProps",
    "CfnDashboard",
    "CfnDashboardProps",
    "CfnGateway",
    "CfnGatewayProps",
    "CfnPortal",
    "CfnPortalProps",
    "CfnProject",
    "CfnProjectProps",
]

publication.publish()

def _typecheckingstub__16de32dcc1e1492d37e1562f274d1d99ed757cdff877687a168f0a2dcae2b096(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    access_policy_identity: typing.Union[typing.Union[CfnAccessPolicy.AccessPolicyIdentityProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    access_policy_permission: builtins.str,
    access_policy_resource: typing.Union[typing.Union[CfnAccessPolicy.AccessPolicyResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d435e0e58d17676ac3956511658125b4e3fb22f514ba1a4e560e2d3708ed48e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6800cff407511c4ca03195c29e299b47dbfc3d88532e192b9823f5ae82cd62(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd41f887e0e00135b907e31c33cc2d151825693c168faff879176097569863fc(
    value: typing.Union[CfnAccessPolicy.AccessPolicyIdentityProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989d2a2df59e80e7c49d47caeab450b5e4973efaefac9c7ab9c1756b6d1f3c73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e03077e1135be8673b2355aa3158e1a07e6de2c6f8ec0ae13eb43de071f765d(
    value: typing.Union[CfnAccessPolicy.AccessPolicyResourceProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f538d4bd325a7f18f307d2b88c7d5cba6983be568730eaed5d09698d6e38918d(
    *,
    iam_role: typing.Optional[typing.Union[typing.Union[CfnAccessPolicy.IamRoleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iam_user: typing.Optional[typing.Union[typing.Union[CfnAccessPolicy.IamUserProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    user: typing.Optional[typing.Union[typing.Union[CfnAccessPolicy.UserProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0945aabd910f8fb5eb71140494053591c42bac94d6c2d5ac1847a6d15e734a7(
    *,
    portal: typing.Optional[typing.Union[typing.Union[CfnAccessPolicy.PortalProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    project: typing.Optional[typing.Union[typing.Union[CfnAccessPolicy.ProjectProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a35db198a3e0aab11301525c513d1aa8d03ecae615853ea6f82eec84b88dadf(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c321cd578cb65161fdca9546cc51f4eae6e74f84ff66009c5f9722a1d2e9fe(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f8a83b12a38cdd97779698ba2879857cccbf0d8947378fe39bb1b48fb5740b(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f891ae36e22a4610824eb124a3b64d1afec6ccdd3e396835d5eab7f31602c08(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a396a1319433dd0a0b6030eabce3acf7a7540f5f7989dc619d11fa641c611f(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298f21d46d2f9a6ea105488e7a8151b724d6f57169d54529166fd57d75310d73(
    *,
    access_policy_identity: typing.Union[typing.Union[CfnAccessPolicy.AccessPolicyIdentityProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    access_policy_permission: builtins.str,
    access_policy_resource: typing.Union[typing.Union[CfnAccessPolicy.AccessPolicyResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c340223f76f17c21718e88f39082be49c3b5b898be421bd885062f8a7e3ef2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    asset_model_id: builtins.str,
    asset_name: builtins.str,
    asset_description: typing.Optional[builtins.str] = None,
    asset_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAsset.AssetHierarchyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    asset_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAsset.AssetPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f9b1984442ea430778b6ee741d2f9ce52bca98d4f82983b491e7dd4a8a4f51(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0bb135aab4775406a2f575d7586326911ceceede54592c26249cdb4f1a891b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246da2e527d962dab6780483037ba1669fee9174d5a0b3475db567be8d31b7c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732e8b79d671120041b5ed8b15c335d26ffef50cdce0968e536d2b5e18fdd913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70256b0e75414b8fb76cb2575b2315b5689112ae0d7f8735ceca50c192855c3f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babda67d0008d27c0c8368d941c28ac46b8c3cdd0fc2db6a97faeed177903bdd(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetHierarchyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6597c876851cb97b9f331f9c4260e8b5c094dd502c5c2c3ce02da8179a6b0a14(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetPropertyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e236e130b7ec2f7395108df666806313d606fe31f7789a8e6f4348cce6d3abd(
    *,
    child_asset_id: builtins.str,
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6919fb6f9e78c92c1f30b1747a1b8a1a264c0e7606c58c72debd8593e6d8fd10(
    *,
    logical_id: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    notification_state: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f295ebf87c388e854ada0ebcbffd491eb2e59b673fafc9e7f1ee1e7f61b25c79(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    asset_model_name: builtins.str,
    asset_model_composite_models: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelCompositeModelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    asset_model_description: typing.Optional[builtins.str] = None,
    asset_model_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelHierarchyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    asset_model_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47703a9cf0aa7a9e07e5239de5842936285a20587d4a213500b3d3476789f02(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5210678d81330030e70389814236c5dfc343e9dcc7b7c249d49bafab2ff80b3c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0773173f58147cba1dd01ef7066f69e75e48e8dd0570bc0f883d08927f3d2d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36b67fbd3e043267a9a9b7d75e0d9d6dde5c669fde7a245d31d5a6206e259e2(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelCompositeModelProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fa4979bba4382a8c15003d48a39f10ac92fcd49ca37af32cd164a8836a7b4e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55006b72eb7bb5aa28b3791bae2c02afbe6f8fef9deec84c8e2bf85c4d132308(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelHierarchyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1b6ba4aa528b4ba2e6768770eb1b13eca7d8ea367453e861f0f39759b65760(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelPropertyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddd158fc8e8b323055785206f7a7d06dee04e68dc7a21c36a26f39140bbf803(
    *,
    name: builtins.str,
    type: builtins.str,
    composite_model_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e48ad0ed017b244b21ac74eaf5dd542c97e628e5fa798cbb69d78ae462dea8(
    *,
    child_asset_model_id: builtins.str,
    logical_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b57a2324b49a1515f146eb2c4b36d67b4dc1be8004ccae56f3ba4cb6ca61c9(
    *,
    data_type: builtins.str,
    logical_id: builtins.str,
    name: builtins.str,
    type: typing.Union[typing.Union[CfnAssetModel.PropertyTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    data_type_spec: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f3f97bd69113e82966bf1e58d78481bb590496dab82a80d0485c06f960ed69(
    *,
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b97a07ef390d515bb52b9bc2b26063977795a9aac55c78cc1b02b3fb87dd4b0(
    *,
    name: builtins.str,
    value: typing.Union[typing.Union[CfnAssetModel.VariableValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c450c34f57e2a28959a16a27b679bd91d977abf59cb1c4b037f38ba3d3d921aa(
    *,
    expression: builtins.str,
    variables: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.ExpressionVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    window: typing.Union[typing.Union[CfnAssetModel.MetricWindowProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7cda9b84eede87c5a5704f9d5e4cb2276df17d5c561d1011daf91d051faec2(
    *,
    tumbling: typing.Optional[typing.Union[typing.Union[CfnAssetModel.TumblingWindowProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acd04ed5417cdd722bd6941db784116cba221fbb9f4f73723df5508f047fb76(
    *,
    type_name: builtins.str,
    attribute: typing.Optional[typing.Union[typing.Union[CfnAssetModel.AttributeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    metric: typing.Optional[typing.Union[typing.Union[CfnAssetModel.MetricProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    transform: typing.Optional[typing.Union[typing.Union[CfnAssetModel.TransformProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809bf7a13419f60779522f77ed2f36de6a3c20e0ffc044dfecb51e66e6a8443e(
    *,
    expression: builtins.str,
    variables: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.ExpressionVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dfe66b39a587839ab295ee47ecee270c08240751bb1b1cf3e9408ea549f8ee9(
    *,
    interval: builtins.str,
    offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72dd2a8d61935e1e7e54d4c898f28c58721ce700656dc2ebc39972788c30d9c(
    *,
    property_logical_id: builtins.str,
    hierarchy_logical_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1505055b5fcb7b4739361ba0bdcd5b44029389cd799fba880df5365eb717ecc(
    *,
    asset_model_name: builtins.str,
    asset_model_composite_models: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelCompositeModelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    asset_model_description: typing.Optional[builtins.str] = None,
    asset_model_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelHierarchyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    asset_model_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssetModel.AssetModelPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f2af6b5589a0f41575ca36917cb9ee3040f98b0b3c274d7c5f3ae787f8b1d1(
    *,
    asset_model_id: builtins.str,
    asset_name: builtins.str,
    asset_description: typing.Optional[builtins.str] = None,
    asset_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAsset.AssetHierarchyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    asset_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAsset.AssetPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3944a8e25443283f66b8ff08fee5e82a8dbff20db3eda9e0a10a49fed95468(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    dashboard_definition: builtins.str,
    dashboard_description: builtins.str,
    dashboard_name: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62845268357b4a2f91060a0fa7ca74678bbcd2ad08e371d80e434668c3de10d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135fe84af566aaeb3a38a4b2855fb24aaf4bd1f0cc7b974ea1938f57ab0979a6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d8a55eddfd87f37844fac5bfc0af3311b50ce40562ce79feabdd426f3d7dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fb0c1b10a24ea78c92402fd30755eb29396ab4f47010b34801ee6fee3a5ba3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231fc3b4b2a5a6f08a94f233f682f89d20187d871d8bbe82ce63a2970fd0e3d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2caa58d512b8209d37d4e8552758a43b1a90319755c5b22f3667b74e1bf03cdb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6ee9d942ba586d74957260ddccdb165f88229f9fa89e5ef637d17997fd9b6c(
    *,
    dashboard_definition: builtins.str,
    dashboard_description: builtins.str,
    dashboard_name: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d53b74302718d523a743fe57196e047103221fef32f018b73d730533cb593f0(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    gateway_name: builtins.str,
    gateway_platform: typing.Union[typing.Union[CfnGateway.GatewayPlatformProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    gateway_capability_summaries: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGateway.GatewayCapabilitySummaryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665e5d8aea349859d06db1ae6130d7cda980b3125ffe4aec449037b56d347f18(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4287ff40593a7fbb69bf0ed14a34e82f0bd8bf91fb0d2267bca2a94a16f4e921(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1eb9833f5018fbca4447f8e7644dc82a9c077fc5d141cde84f454b89b91aed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3c93e7da72202ece397b651c9bb82489ad10738ef49489d036b4e3409f8320(
    value: typing.Union[CfnGateway.GatewayPlatformProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80e2fc5b35e8bcc37f9cecc2c1ecc3fbaeaaf420086ed636cb07f2b52e7e561(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGateway.GatewayCapabilitySummaryProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6702e00a58298464d58b0febd2052fd24368105f1c0ff63929a3a35daebc060b(
    *,
    capability_namespace: builtins.str,
    capability_configuration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7193722bb6bfb21853fb93008af714c6021d79bd089013909ab2f30e099174ba(
    *,
    greengrass: typing.Optional[typing.Union[typing.Union[CfnGateway.GreengrassProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    greengrass_v2: typing.Optional[typing.Union[typing.Union[CfnGateway.GreengrassV2Property, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7828a2b50e9a8797f05fe36706d5990fba069eb72bb7de3eb21128efe67134(
    *,
    group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8871ac425610b1143d26c45b21bffb0dd2cd38d24c4ada03f64dfb1e27374123(
    *,
    core_device_thing_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f938d14a9b6a4fbc0c4e1da31690ae58ca7becce9d79786d7825803089f4e8(
    *,
    gateway_name: builtins.str,
    gateway_platform: typing.Union[typing.Union[CfnGateway.GatewayPlatformProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    gateway_capability_summaries: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGateway.GatewayCapabilitySummaryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c274b13695fef7c603b4b4b8920779d4dc3a74bd0838e94ada15249d3cdafe(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    portal_contact_email: builtins.str,
    portal_name: builtins.str,
    role_arn: builtins.str,
    alarms: typing.Any = None,
    notification_sender_email: typing.Optional[builtins.str] = None,
    portal_auth_mode: typing.Optional[builtins.str] = None,
    portal_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1ac03ae2dd653d135dde67a7bbe52b447a0b669e7d51d3d4de9970c55ce6cf(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ff1961d2bcd28a0e9baa513d1d5394b686931aa136ca7f2fd3e35df1c7796f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea621311b98ea517807c4b48c7be95b4dd84a9b1bfdc699bb4657b7df587c6a(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22083d4b6f65d19f20d6644e6c34d96c78c5380e5fba248ee71d245f5b8587ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a662556ade4361b0ff1ef68bdaf9d5d5cd98c7851bd054b2230b49d4530435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e012188f3b6c360ba0712c202106ad684113fb4fc473d8643987eb3e56e0c763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee99027a1a40c54fa3d597db0b8e6f0c267452c3a61740858cd3a867c92a7e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca026081589f8f41e178c5c68c985445d90c0dd2ff63fcbed32ef518536b93e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60beb4d77540c6aa0844f34c0e4c69ae0b737ef7c70a33865a48e39862ff86f7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ee2833e479e93bbfaf58496fc88ee9ea008fde7274c9813d27c7e20dda453f(
    *,
    alarm_role_arn: typing.Optional[builtins.str] = None,
    notification_lambda_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a729c0eef48e5fe2740b3cf099bdccad7e32dffeaccbb83070eecf41d1726a(
    *,
    portal_contact_email: builtins.str,
    portal_name: builtins.str,
    role_arn: builtins.str,
    alarms: typing.Any = None,
    notification_sender_email: typing.Optional[builtins.str] = None,
    portal_auth_mode: typing.Optional[builtins.str] = None,
    portal_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8512b1288ab049b8c8d4f3586964c19de269fc35eaf89a52b30cfa417e7104a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    portal_id: builtins.str,
    project_name: builtins.str,
    asset_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    project_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f2327468458f28ce86229aeeb63e42179a0b78ed382556d4f074002810155c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8809d29fb363e2680dfc675882f37177b15af0b49a982d53f2aa2394400c41(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a267773edfca5523fdf4ab8e3a51362a53c0b6e073b22c9a8a23ab2a88ab08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3068c0da6dde7760b27d6aeecd6771738cc726b374b50a2b1aa07021fda1e185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cc2575f01de3cac5110362c6e540d140104d101fe2d952d41a319dfbec12f4(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80e29d91792a41d8f04f0b8e445819b8e5d677163a5785d437248c72573ef20(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9646d2fe343823301252919daec281e87db3b740aba797b2371074f9b99ebfae(
    *,
    portal_id: builtins.str,
    project_name: builtins.str,
    asset_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    project_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
