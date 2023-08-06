'''
# AWS::Signer Construct Library

AWS Signer is a fully managed code-signing service to ensure the trust and integrity of your code. Organizations validate code against
a digital signature to confirm that the code is unaltered and from a trusted publisher. For more information, see [What Is AWS
Signer?](https://docs.aws.amazon.com/signer/latest/developerguide/Welcome.html)

## Table of Contents

* [Signing Platform](#signing-platform)
* [Signing Profile](#signing-profile)

## Signing Platform

A signing platform is a predefined set of instructions that specifies the signature format and signing algorithms that AWS Signer should use
to sign a zip file. For more information go to [Signing Platforms in AWS Signer](https://docs.aws.amazon.com/signer/latest/developerguide/gs-platform.html).

AWS Signer provides a pre-defined set of signing platforms. They are available in the CDK as -

```text
Platform.AWS_IOT_DEVICE_MANAGEMENT_SHA256_ECDSA
Platform.AWS_LAMBDA_SHA384_ECDSA
Platform.AMAZON_FREE_RTOS_TI_CC3220SF
Platform.AMAZON_FREE_RTOS_DEFAULT
```

## Signing Profile

A signing profile is a code-signing template that can be used to pre-define the signature specifications for a signing job.
A signing profile includes a signing platform to designate the file type to be signed, the signature format, and the signature algorithms.
For more information, visit [Signing Profiles in AWS Signer](https://docs.aws.amazon.com/signer/latest/developerguide/gs-profile.html).

The following code sets up a signing profile for signing lambda code bundles -

```python
signing_profile = signer.SigningProfile(self, "SigningProfile",
    platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA
)
```

A signing profile is valid by default for 135 months. This can be modified by specifying the `signatureValidityPeriod` property.
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
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnProfilePermission(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_signer.CfnProfilePermission",
):
    '''A CloudFormation ``AWS::Signer::ProfilePermission``.

    Adds cross-account permissions to a signing profile.

    :cloudformationResource: AWS::Signer::ProfilePermission
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_signer as signer
        
        cfn_profile_permission = signer.CfnProfilePermission(self, "MyCfnProfilePermission",
            action="action",
            principal="principal",
            profile_name="profileName",
            statement_id="statementId",
        
            # the properties below are optional
            profile_version="profileVersion"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        action: builtins.str,
        principal: builtins.str,
        profile_name: builtins.str,
        statement_id: builtins.str,
        profile_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Signer::ProfilePermission``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: The AWS Signer action permitted as part of cross-account permissions.
        :param principal: The AWS principal receiving cross-account permissions. This may be an IAM role or another AWS account ID.
        :param profile_name: The human-readable name of the signing profile.
        :param statement_id: A unique identifier for the cross-account permission statement.
        :param profile_version: The version of the signing profile.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caaf21b5777859d36ee4d014aef1155691dc35d9544ed307a994009a84b0e6de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProfilePermissionProps(
            action=action,
            principal=principal,
            profile_name=profile_name,
            statement_id=statement_id,
            profile_version=profile_version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170c67cc15c5c7c91dfc1b442e6f8abb136cb24b3bb0f4cf8da3d191b11444e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c3663a5fe38bc8aa13555cf5684f98505b48610742b8dcf6a6cc792c30e5b2f)
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
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        '''The AWS Signer action permitted as part of cross-account permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-action
        '''
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd3d1bff7fff3d1877ce3093571a002bd520f8161d1c367903cb284570588010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        '''The AWS principal receiving cross-account permissions.

        This may be an IAM role or another AWS account ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-principal
        '''
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea70f9fe9d64668c5454b507a8f3e2f7bab7e81c03e3acaeb5cd2d924d302190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="profileName")
    def profile_name(self) -> builtins.str:
        '''The human-readable name of the signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-profilename
        '''
        return typing.cast(builtins.str, jsii.get(self, "profileName"))

    @profile_name.setter
    def profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b984ea6fa71d05fd0641de19fcf9aec4dbffab7bf0e9b504876c2784c342274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileName", value)

    @builtins.property
    @jsii.member(jsii_name="statementId")
    def statement_id(self) -> builtins.str:
        '''A unique identifier for the cross-account permission statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-statementid
        '''
        return typing.cast(builtins.str, jsii.get(self, "statementId"))

    @statement_id.setter
    def statement_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28eabd0c20825ec7c5dd3d3833d1f3c78975bdb003a5b878cd1612f2ca38bb90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementId", value)

    @builtins.property
    @jsii.member(jsii_name="profileVersion")
    def profile_version(self) -> typing.Optional[builtins.str]:
        '''The version of the signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-profileversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileVersion"))

    @profile_version.setter
    def profile_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719f9a9a07622a0d3bdb52e1e7b6cc81f79700cff8a88402ce423082658573e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileVersion", value)


@jsii.data_type(
    jsii_type="monocdk.aws_signer.CfnProfilePermissionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "principal": "principal",
        "profile_name": "profileName",
        "statement_id": "statementId",
        "profile_version": "profileVersion",
    },
)
class CfnProfilePermissionProps:
    def __init__(
        self,
        *,
        action: builtins.str,
        principal: builtins.str,
        profile_name: builtins.str,
        statement_id: builtins.str,
        profile_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnProfilePermission``.

        :param action: The AWS Signer action permitted as part of cross-account permissions.
        :param principal: The AWS principal receiving cross-account permissions. This may be an IAM role or another AWS account ID.
        :param profile_name: The human-readable name of the signing profile.
        :param statement_id: A unique identifier for the cross-account permission statement.
        :param profile_version: The version of the signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_signer as signer
            
            cfn_profile_permission_props = signer.CfnProfilePermissionProps(
                action="action",
                principal="principal",
                profile_name="profileName",
                statement_id="statementId",
            
                # the properties below are optional
                profile_version="profileVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33858a67e8e4762b2fd9b2fcdedc543185f3006436941a08c4b53b46df9774c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument profile_name", value=profile_name, expected_type=type_hints["profile_name"])
            check_type(argname="argument statement_id", value=statement_id, expected_type=type_hints["statement_id"])
            check_type(argname="argument profile_version", value=profile_version, expected_type=type_hints["profile_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "principal": principal,
            "profile_name": profile_name,
            "statement_id": statement_id,
        }
        if profile_version is not None:
            self._values["profile_version"] = profile_version

    @builtins.property
    def action(self) -> builtins.str:
        '''The AWS Signer action permitted as part of cross-account permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-action
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''The AWS principal receiving cross-account permissions.

        This may be an IAM role or another AWS account ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-principal
        '''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_name(self) -> builtins.str:
        '''The human-readable name of the signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-profilename
        '''
        result = self._values.get("profile_name")
        assert result is not None, "Required property 'profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statement_id(self) -> builtins.str:
        '''A unique identifier for the cross-account permission statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-statementid
        '''
        result = self._values.get("statement_id")
        assert result is not None, "Required property 'statement_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_version(self) -> typing.Optional[builtins.str]:
        '''The version of the signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-profileversion
        '''
        result = self._values.get("profile_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfilePermissionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSigningProfile(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_signer.CfnSigningProfile",
):
    '''A CloudFormation ``AWS::Signer::SigningProfile``.

    Creates a signing profile. A signing profile is a code-signing template that can be used to carry out a pre-defined signing job.

    :cloudformationResource: AWS::Signer::SigningProfile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_signer as signer
        
        cfn_signing_profile = signer.CfnSigningProfile(self, "MyCfnSigningProfile",
            platform_id="platformId",
        
            # the properties below are optional
            signature_validity_period=signer.CfnSigningProfile.SignatureValidityPeriodProperty(
                type="type",
                value=123
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
        platform_id: builtins.str,
        signature_validity_period: typing.Optional[typing.Union[typing.Union["CfnSigningProfile.SignatureValidityPeriodProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Signer::SigningProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param platform_id: The ID of a platform that is available for use by a signing profile.
        :param signature_validity_period: The validity period override for any signature generated using this signing profile. If unspecified, the default is 135 months.
        :param tags: A list of tags associated with the signing profile.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15df35dab0900561aa23ebb2a202ecdaae3e2b57b9f997f79218d99dc46a5d36)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSigningProfileProps(
            platform_id=platform_id,
            signature_validity_period=signature_validity_period,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9889314b94aa7c1e195e9426d187bb2df0375edd95d792387bb2558dbb3450)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65f0f8dba15477a3c2c704a7a20c43db528f952bd77539c374fac2a3275ac525)
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
        '''The Amazon Resource Name (ARN) of the signing profile created.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileName")
    def attr_profile_name(self) -> builtins.str:
        '''The name of the signing profile created.

        :cloudformationAttribute: ProfileName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileName"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileVersion")
    def attr_profile_version(self) -> builtins.str:
        '''The version of the signing profile created.

        :cloudformationAttribute: ProfileVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileVersionArn")
    def attr_profile_version_arn(self) -> builtins.str:
        '''The signing profile ARN, including the profile version.

        :cloudformationAttribute: ProfileVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags associated with the signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="platformId")
    def platform_id(self) -> builtins.str:
        '''The ID of a platform that is available for use by a signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-platformid
        '''
        return typing.cast(builtins.str, jsii.get(self, "platformId"))

    @platform_id.setter
    def platform_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0580cc6837a072647f927718458b71913ad8bd82562491c22f577d0645909fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformId", value)

    @builtins.property
    @jsii.member(jsii_name="signatureValidityPeriod")
    def signature_validity_period(
        self,
    ) -> typing.Optional[typing.Union["CfnSigningProfile.SignatureValidityPeriodProperty", _IResolvable_a771d0ef]]:
        '''The validity period override for any signature generated using this signing profile.

        If unspecified, the default is 135 months.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-signaturevalidityperiod
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSigningProfile.SignatureValidityPeriodProperty", _IResolvable_a771d0ef]], jsii.get(self, "signatureValidityPeriod"))

    @signature_validity_period.setter
    def signature_validity_period(
        self,
        value: typing.Optional[typing.Union["CfnSigningProfile.SignatureValidityPeriodProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67eab55e625fe1e664dcd2711c25337a000173c8944680e3a8413bfd3b36b99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureValidityPeriod", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_signer.CfnSigningProfile.SignatureValidityPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class SignatureValidityPeriodProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The validity period for the signing job.

            :param type: The time unit for signature validity: DAYS | MONTHS | YEARS.
            :param value: The numerical value of the time unit for signature validity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingprofile-signaturevalidityperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_signer as signer
                
                signature_validity_period_property = signer.CfnSigningProfile.SignatureValidityPeriodProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6e9aebf0afed5b4877fbb73feae575f22e40042ca3af644767b6afac3d8e4c3)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The time unit for signature validity: DAYS | MONTHS | YEARS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingprofile-signaturevalidityperiod.html#cfn-signer-signingprofile-signaturevalidityperiod-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The numerical value of the time unit for signature validity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingprofile-signaturevalidityperiod.html#cfn-signer-signingprofile-signaturevalidityperiod-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignatureValidityPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_signer.CfnSigningProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "platform_id": "platformId",
        "signature_validity_period": "signatureValidityPeriod",
        "tags": "tags",
    },
)
class CfnSigningProfileProps:
    def __init__(
        self,
        *,
        platform_id: builtins.str,
        signature_validity_period: typing.Optional[typing.Union[typing.Union[CfnSigningProfile.SignatureValidityPeriodProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSigningProfile``.

        :param platform_id: The ID of a platform that is available for use by a signing profile.
        :param signature_validity_period: The validity period override for any signature generated using this signing profile. If unspecified, the default is 135 months.
        :param tags: A list of tags associated with the signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_signer as signer
            
            cfn_signing_profile_props = signer.CfnSigningProfileProps(
                platform_id="platformId",
            
                # the properties below are optional
                signature_validity_period=signer.CfnSigningProfile.SignatureValidityPeriodProperty(
                    type="type",
                    value=123
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45773c80085173170b820c348b4f674be33a4f3ab5d90580b678ec3271cc7ee4)
            check_type(argname="argument platform_id", value=platform_id, expected_type=type_hints["platform_id"])
            check_type(argname="argument signature_validity_period", value=signature_validity_period, expected_type=type_hints["signature_validity_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "platform_id": platform_id,
        }
        if signature_validity_period is not None:
            self._values["signature_validity_period"] = signature_validity_period
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def platform_id(self) -> builtins.str:
        '''The ID of a platform that is available for use by a signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-platformid
        '''
        result = self._values.get("platform_id")
        assert result is not None, "Required property 'platform_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signature_validity_period(
        self,
    ) -> typing.Optional[typing.Union[CfnSigningProfile.SignatureValidityPeriodProperty, _IResolvable_a771d0ef]]:
        '''The validity period override for any signature generated using this signing profile.

        If unspecified, the default is 135 months.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-signaturevalidityperiod
        '''
        result = self._values.get("signature_validity_period")
        return typing.cast(typing.Optional[typing.Union[CfnSigningProfile.SignatureValidityPeriodProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags associated with the signing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSigningProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_signer.ISigningProfile")
class ISigningProfile(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A Signer Profile.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="signingProfileArn")
    def signing_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the signing profile.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="signingProfileName")
    def signing_profile_name(self) -> builtins.str:
        '''(experimental) The name of signing profile.

        :stability: experimental
        :attribute: ProfileName
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersion")
    def signing_profile_version(self) -> builtins.str:
        '''(experimental) The version of signing profile.

        :stability: experimental
        :attribute: ProfileVersion
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersionArn")
    def signing_profile_version_arn(self) -> builtins.str:
        '''(experimental) The ARN of signing profile version.

        :stability: experimental
        :attribute: ProfileVersionArn
        '''
        ...


class _ISigningProfileProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A Signer Profile.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_signer.ISigningProfile"

    @builtins.property
    @jsii.member(jsii_name="signingProfileArn")
    def signing_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the signing profile.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileName")
    def signing_profile_name(self) -> builtins.str:
        '''(experimental) The name of signing profile.

        :stability: experimental
        :attribute: ProfileName
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileName"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersion")
    def signing_profile_version(self) -> builtins.str:
        '''(experimental) The version of signing profile.

        :stability: experimental
        :attribute: ProfileVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersion"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersionArn")
    def signing_profile_version_arn(self) -> builtins.str:
        '''(experimental) The ARN of signing profile version.

        :stability: experimental
        :attribute: ProfileVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersionArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISigningProfile).__jsii_proxy_class__ = lambda : _ISigningProfileProxy


class Platform(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_signer.Platform"):
    '''(experimental) Platforms that are allowed with signing config.

    :see: https://docs.aws.amazon.com/signer/latest/developerguide/gs-platform.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as signer
        
        
        signing_profile = signer.SigningProfile(self, "SigningProfile",
            platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA
        )
        
        code_signing_config = lambda_.CodeSigningConfig(self, "CodeSigningConfig",
            signing_profiles=[signing_profile]
        )
        
        lambda_.Function(self, "Function",
            code_signing_config=code_signing_config,
            runtime=lambda_.Runtime.NODEJS_16_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
        )
    '''

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_FREE_RTOS_DEFAULT")
    def AMAZON_FREE_RTOS_DEFAULT(cls) -> "Platform":
        '''(experimental) Specification of signature format and signing algorithms with SHA256 hash and ECDSA encryption for Amazon FreeRTOS.

        :stability: experimental
        '''
        return typing.cast("Platform", jsii.sget(cls, "AMAZON_FREE_RTOS_DEFAULT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_FREE_RTOS_TI_CC3220SF")
    def AMAZON_FREE_RTOS_TI_CC3220_SF(cls) -> "Platform":
        '''(experimental) Specification of signature format and signing algorithms with SHA1 hash and RSA encryption for Amazon FreeRTOS.

        :stability: experimental
        '''
        return typing.cast("Platform", jsii.sget(cls, "AMAZON_FREE_RTOS_TI_CC3220SF"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AWS_IOT_DEVICE_MANAGEMENT_SHA256_ECDSA")
    def AWS_IOT_DEVICE_MANAGEMENT_SHA256_ECDSA(cls) -> "Platform":
        '''(experimental) Specification of signature format and signing algorithms for AWS IoT Device.

        :stability: experimental
        '''
        return typing.cast("Platform", jsii.sget(cls, "AWS_IOT_DEVICE_MANAGEMENT_SHA256_ECDSA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AWS_LAMBDA_SHA384_ECDSA")
    def AWS_LAMBDA_SHA384_ECDSA(cls) -> "Platform":
        '''(experimental) Specification of signature format and signing algorithms for AWS Lambda.

        :stability: experimental
        '''
        return typing.cast("Platform", jsii.sget(cls, "AWS_LAMBDA_SHA384_ECDSA"))

    @builtins.property
    @jsii.member(jsii_name="platformId")
    def platform_id(self) -> builtins.str:
        '''(experimental) The id of signing platform.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-platformid
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "platformId"))


@jsii.implements(ISigningProfile)
class SigningProfile(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_signer.SigningProfile",
):
    '''(experimental) Defines a Signing Profile.

    :stability: experimental
    :resource: AWS::Signer::SigningProfile
    :exampleMetadata: infused

    Example::

        import monocdk as signer
        
        
        signing_profile = signer.SigningProfile(self, "SigningProfile",
            platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA
        )
        
        code_signing_config = lambda_.CodeSigningConfig(self, "CodeSigningConfig",
            signing_profiles=[signing_profile]
        )
        
        lambda_.Function(self, "Function",
            code_signing_config=code_signing_config,
            runtime=lambda_.Runtime.NODEJS_16_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        platform: Platform,
        signature_validity: typing.Optional[_Duration_070aa057] = None,
        signing_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param platform: (experimental) The Signing Platform available for signing profile.
        :param signature_validity: (experimental) The validity period for signatures generated using this signing profile. Default: - 135 months
        :param signing_profile_name: (experimental) Physical name of this Signing Profile. Default: - Assigned by CloudFormation (recommended).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cde27332c8b255d1f61c33cd58210b9de1151ec3e78aacf67ed85b4cf2ef42)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SigningProfileProps(
            platform=platform,
            signature_validity=signature_validity,
            signing_profile_name=signing_profile_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSigningProfileAttributes")
    @builtins.classmethod
    def from_signing_profile_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        signing_profile_name: builtins.str,
        signing_profile_version: builtins.str,
    ) -> ISigningProfile:
        '''(experimental) Creates a Signing Profile construct that represents an external Signing Profile.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param signing_profile_name: (experimental) The name of signing profile.
        :param signing_profile_version: (experimental) The version of signing profile.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3d9e0d0932cf8c7fddb3d79164f9296ae351076b1dfee04e51bab5b3d0d5b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = SigningProfileAttributes(
            signing_profile_name=signing_profile_name,
            signing_profile_version=signing_profile_version,
        )

        return typing.cast(ISigningProfile, jsii.sinvoke(cls, "fromSigningProfileAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="signingProfileArn")
    def signing_profile_arn(self) -> builtins.str:
        '''(experimental) The ARN of the signing profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileName")
    def signing_profile_name(self) -> builtins.str:
        '''(experimental) The name of signing profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileName"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersion")
    def signing_profile_version(self) -> builtins.str:
        '''(experimental) The version of signing profile.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersion"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersionArn")
    def signing_profile_version_arn(self) -> builtins.str:
        '''(experimental) The ARN of signing profile version.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersionArn"))


@jsii.data_type(
    jsii_type="monocdk.aws_signer.SigningProfileAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "signing_profile_name": "signingProfileName",
        "signing_profile_version": "signingProfileVersion",
    },
)
class SigningProfileAttributes:
    def __init__(
        self,
        *,
        signing_profile_name: builtins.str,
        signing_profile_version: builtins.str,
    ) -> None:
        '''(experimental) A reference to a Signing Profile.

        :param signing_profile_name: (experimental) The name of signing profile.
        :param signing_profile_version: (experimental) The version of signing profile.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_signer as signer
            
            signing_profile_attributes = signer.SigningProfileAttributes(
                signing_profile_name="signingProfileName",
                signing_profile_version="signingProfileVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7113571747bd941b4b1e3578a032ce2d96908142a4a5feda43f7aa06d27e452)
            check_type(argname="argument signing_profile_name", value=signing_profile_name, expected_type=type_hints["signing_profile_name"])
            check_type(argname="argument signing_profile_version", value=signing_profile_version, expected_type=type_hints["signing_profile_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "signing_profile_name": signing_profile_name,
            "signing_profile_version": signing_profile_version,
        }

    @builtins.property
    def signing_profile_name(self) -> builtins.str:
        '''(experimental) The name of signing profile.

        :stability: experimental
        '''
        result = self._values.get("signing_profile_name")
        assert result is not None, "Required property 'signing_profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_profile_version(self) -> builtins.str:
        '''(experimental) The version of signing profile.

        :stability: experimental
        '''
        result = self._values.get("signing_profile_version")
        assert result is not None, "Required property 'signing_profile_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SigningProfileAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_signer.SigningProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "platform": "platform",
        "signature_validity": "signatureValidity",
        "signing_profile_name": "signingProfileName",
    },
)
class SigningProfileProps:
    def __init__(
        self,
        *,
        platform: Platform,
        signature_validity: typing.Optional[_Duration_070aa057] = None,
        signing_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties for a Signing Profile object.

        :param platform: (experimental) The Signing Platform available for signing profile.
        :param signature_validity: (experimental) The validity period for signatures generated using this signing profile. Default: - 135 months
        :param signing_profile_name: (experimental) Physical name of this Signing Profile. Default: - Assigned by CloudFormation (recommended).

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as signer
            
            
            signing_profile = signer.SigningProfile(self, "SigningProfile",
                platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA
            )
            
            code_signing_config = lambda_.CodeSigningConfig(self, "CodeSigningConfig",
                signing_profiles=[signing_profile]
            )
            
            lambda_.Function(self, "Function",
                code_signing_config=code_signing_config,
                runtime=lambda_.Runtime.NODEJS_16_X,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46954a7092a77c28a1cf5142f1a7eb92ec438b4c1c968d2ef8111b35e08b33af)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument signature_validity", value=signature_validity, expected_type=type_hints["signature_validity"])
            check_type(argname="argument signing_profile_name", value=signing_profile_name, expected_type=type_hints["signing_profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "platform": platform,
        }
        if signature_validity is not None:
            self._values["signature_validity"] = signature_validity
        if signing_profile_name is not None:
            self._values["signing_profile_name"] = signing_profile_name

    @builtins.property
    def platform(self) -> Platform:
        '''(experimental) The Signing Platform available for signing profile.

        :see: https://docs.aws.amazon.com/signer/latest/developerguide/gs-platform.html
        :stability: experimental
        '''
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(Platform, result)

    @builtins.property
    def signature_validity(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The validity period for signatures generated using this signing profile.

        :default: - 135 months

        :stability: experimental
        '''
        result = self._values.get("signature_validity")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def signing_profile_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Physical name of this Signing Profile.

        :default: - Assigned by CloudFormation (recommended).

        :stability: experimental
        '''
        result = self._values.get("signing_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SigningProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnProfilePermission",
    "CfnProfilePermissionProps",
    "CfnSigningProfile",
    "CfnSigningProfileProps",
    "ISigningProfile",
    "Platform",
    "SigningProfile",
    "SigningProfileAttributes",
    "SigningProfileProps",
]

publication.publish()

def _typecheckingstub__caaf21b5777859d36ee4d014aef1155691dc35d9544ed307a994009a84b0e6de(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    action: builtins.str,
    principal: builtins.str,
    profile_name: builtins.str,
    statement_id: builtins.str,
    profile_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170c67cc15c5c7c91dfc1b442e6f8abb136cb24b3bb0f4cf8da3d191b11444e3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3663a5fe38bc8aa13555cf5684f98505b48610742b8dcf6a6cc792c30e5b2f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3d1bff7fff3d1877ce3093571a002bd520f8161d1c367903cb284570588010(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea70f9fe9d64668c5454b507a8f3e2f7bab7e81c03e3acaeb5cd2d924d302190(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b984ea6fa71d05fd0641de19fcf9aec4dbffab7bf0e9b504876c2784c342274(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28eabd0c20825ec7c5dd3d3833d1f3c78975bdb003a5b878cd1612f2ca38bb90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719f9a9a07622a0d3bdb52e1e7b6cc81f79700cff8a88402ce423082658573e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33858a67e8e4762b2fd9b2fcdedc543185f3006436941a08c4b53b46df9774c(
    *,
    action: builtins.str,
    principal: builtins.str,
    profile_name: builtins.str,
    statement_id: builtins.str,
    profile_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15df35dab0900561aa23ebb2a202ecdaae3e2b57b9f997f79218d99dc46a5d36(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    platform_id: builtins.str,
    signature_validity_period: typing.Optional[typing.Union[typing.Union[CfnSigningProfile.SignatureValidityPeriodProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9889314b94aa7c1e195e9426d187bb2df0375edd95d792387bb2558dbb3450(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f0f8dba15477a3c2c704a7a20c43db528f952bd77539c374fac2a3275ac525(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0580cc6837a072647f927718458b71913ad8bd82562491c22f577d0645909fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67eab55e625fe1e664dcd2711c25337a000173c8944680e3a8413bfd3b36b99b(
    value: typing.Optional[typing.Union[CfnSigningProfile.SignatureValidityPeriodProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e9aebf0afed5b4877fbb73feae575f22e40042ca3af644767b6afac3d8e4c3(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45773c80085173170b820c348b4f674be33a4f3ab5d90580b678ec3271cc7ee4(
    *,
    platform_id: builtins.str,
    signature_validity_period: typing.Optional[typing.Union[typing.Union[CfnSigningProfile.SignatureValidityPeriodProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cde27332c8b255d1f61c33cd58210b9de1151ec3e78aacf67ed85b4cf2ef42(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    platform: Platform,
    signature_validity: typing.Optional[_Duration_070aa057] = None,
    signing_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3d9e0d0932cf8c7fddb3d79164f9296ae351076b1dfee04e51bab5b3d0d5b4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    signing_profile_name: builtins.str,
    signing_profile_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7113571747bd941b4b1e3578a032ce2d96908142a4a5feda43f7aa06d27e452(
    *,
    signing_profile_name: builtins.str,
    signing_profile_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46954a7092a77c28a1cf5142f1a7eb92ec438b4c1c968d2ef8111b35e08b33af(
    *,
    platform: Platform,
    signature_validity: typing.Optional[_Duration_070aa057] = None,
    signing_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
