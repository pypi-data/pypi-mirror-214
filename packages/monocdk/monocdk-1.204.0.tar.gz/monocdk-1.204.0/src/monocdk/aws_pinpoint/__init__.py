'''
# Amazon Pinpoint Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as pinpoint
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Pinpoint construct libraries](https://constructs.dev/search?q=pinpoint)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Pinpoint resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Pinpoint.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Pinpoint](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Pinpoint.html).

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
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnADMChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnADMChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::ADMChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the ADM channel to send push notifications through the Amazon Device Messaging (ADM) service to apps that run on Amazon devices, such as Kindle Fire tablets. Before you can use Amazon Pinpoint to send messages to Amazon devices, you have to enable the ADM channel for an Amazon Pinpoint application.

    The ADMChannel resource represents the status and authentication settings for the ADM channel for an application.

    :cloudformationResource: AWS::Pinpoint::ADMChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_aDMChannel = pinpoint.CfnADMChannel(self, "MyCfnADMChannel",
            application_id="applicationId",
            client_id="clientId",
            client_secret="clientSecret",
        
            # the properties below are optional
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::ADMChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.
        :param client_id: The Client ID that you received from Amazon to send messages by using ADM.
        :param client_secret: The Client Secret that you received from Amazon to send messages by using ADM.
        :param enabled: Specifies whether to enable the ADM channel for the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f08ea26f317f5c538495ea0d7494bdd8ac7b3c8c2aeddc570532d2ae7204b56)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnADMChannelProps(
            application_id=application_id,
            client_id=client_id,
            client_secret=client_secret,
            enabled=enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575bbba65644ea9f3f5e16a98dc810e1a54e42cff16434c1d78d937c8233d616)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be87d1beaaf3cc5bbe59b1effb7fef86a7c4124e1137c7b36056659b098810b4)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7170e880d4caaac7e88c3f885e52b861a7fc5f4e97d8e145520b8c102752e3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        '''The Client ID that you received from Amazon to send messages by using ADM.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientid
        '''
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6389dbbe5fec78e7da51c5ae11295c44f1027e0c850e3623bd8bbfe76e4ae8e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        '''The Client Secret that you received from Amazon to send messages by using ADM.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientsecret
        '''
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460edc798ddf4bc7148c8195a0d30068525a114c2bfad899d52da753823ebcd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the ADM channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1b2a5c3a9428c2354a95bb0f8f5523812fca0d00fe601a0820ed88a21dfa95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnADMChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "enabled": "enabled",
    },
)
class CfnADMChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnADMChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.
        :param client_id: The Client ID that you received from Amazon to send messages by using ADM.
        :param client_secret: The Client Secret that you received from Amazon to send messages by using ADM.
        :param enabled: Specifies whether to enable the ADM channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_aDMChannel_props = pinpoint.CfnADMChannelProps(
                application_id="applicationId",
                client_id="clientId",
                client_secret="clientSecret",
            
                # the properties below are optional
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab29ace345c1bc763addd0ef24129475660792ee9790e2bccb3a67db999ae704)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the ADM channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The Client ID that you received from Amazon to send messages by using ADM.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientid
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''The Client Secret that you received from Amazon to send messages by using ADM.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientsecret
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the ADM channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnADMChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAPNSChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnAPNSChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::APNSChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the APNs channel to send push notification messages to the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send notifications to APNs, you have to enable the APNs channel for an Amazon Pinpoint application.

    The APNSChannel resource represents the status and authentication settings for the APNs channel for an application.

    :cloudformationResource: AWS::Pinpoint::APNSChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_aPNSChannel = pinpoint.CfnAPNSChannel(self, "MyCfnAPNSChannel",
            application_id="applicationId",
        
            # the properties below are optional
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::APNSChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs channel for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebaa63b7127a31f6e03bdd047e0bf11ce9802532ce3813d7672a23c66689ecd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAPNSChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db77dcf665327ca220280e80f37e93a7790625be1f2d6c6987cc5461d309825)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bac8ec59dba336e509df5e8ab2c88397c1b9411a1d3cb281d91b2bad342c6572)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68db3be042adf3ca0e6450202e9bdc16520a72fdf3e1b118ad1de8c65f467c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-bundleid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4510303941b3afed742a91cbc53b3fc8a50acdc697ccdc7b6e93b8116138d340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802cb1b5a39327c7a490458c49b8341d2524a7a8b35a5215ffa3d0f01910064e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-defaultauthenticationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAuthenticationMethod"))

    @default_authentication_method.setter
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65ee12a28bf1149de653598cb771755e1d77c92f10260bd30c2e232d764e9d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the APNs channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6808f7fcad0e6964a15fe969da5f81b7c9fc820e301c813b6d37012caf3f7c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bad353341ab31a5932a8f4411e5514087d6fbe165f59178d7f94b7da84ffd89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-teamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ebfc296fdee694ade57710d766c35e3abbf19c83bd824dad3c5a5ca4949402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKey"))

    @token_key.setter
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d0fb9736cc3069225623721ad2a50288d05812005f25c2e9520c30ebfe0a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKey", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKeyId"))

    @token_key_id.setter
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ab52fd5f8ceeb6df54ea75d265fb59954b2d40c8d2c92c20cb386d7fe0c08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnAPNSChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAPNSChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs channel for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_aPNSChannel_props = pinpoint.CfnAPNSChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db76aa8db8a67a5190cb7616bdb65778a6ba1599a4a212f2b0ea5a22d6020a1)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the APNs channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAPNSSandboxChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnAPNSSandboxChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::APNSSandboxChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the APNs sandbox channel to send push notification messages to the sandbox environment of the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send notifications to the APNs sandbox environment, you have to enable the APNs sandbox channel for an Amazon Pinpoint application.

    The APNSSandboxChannel resource represents the status and authentication settings of the APNs sandbox channel for an application.

    :cloudformationResource: AWS::Pinpoint::APNSSandboxChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_aPNSSandbox_channel = pinpoint.CfnAPNSSandboxChannel(self, "MyCfnAPNSSandboxChannel",
            application_id="applicationId",
        
            # the properties below are optional
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::APNSSandboxChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a4bb7874d53a993e09ceb2eaa5b6a0b08f977ac716e229741fc96befbddf1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAPNSSandboxChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb98732e17bf5babad2a6a571cf0aea4152818c7b740708f05a63c4d97e723b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e0a2a4cd2a41fb8fd03f8f89e95e70fb40466ccb195adb6d7a5bd9d6205c7ce)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96fd58145978490eca0bcc2cec5c57076937a4c75a1accb9db6caf0d501f624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-bundleid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee77226a87e6dbbae33e212be5ecb211cd69ed88beedcceb3a57581f167cf249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c44c7d932eae06e32d7b1bae7896501d6576c547cc4c79fe9eee4a66b51803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-defaultauthenticationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAuthenticationMethod"))

    @default_authentication_method.setter
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2da7a6b04526de603b21eb7e028ee4ff9995576fce69a0de80fd944b87e31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a0609830eb8550ebd9b04b7ef24a9b95346f35732ce3c06014ce47d160b311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392ac333731be67812fe8bc70ec6da2bf70634599e760996b2410f58bbf31536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-teamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013dc4adc1b1223b178fd2015ebe77b8b959521d080c472ac67e627059fa6c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKey"))

    @token_key.setter
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb7bcce604e851f493b3ddc3fd09ff4ece60f5714f47a8f11aa9c92d9fe33ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKey", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKeyId"))

    @token_key_id.setter
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad79920fe5da8de3b9ad171c5b14ed43dde94e707a671d84423a76e8209e711f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnAPNSSandboxChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSSandboxChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAPNSSandboxChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_aPNSSandbox_channel_props = pinpoint.CfnAPNSSandboxChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79476d9be557ee88417e9eff066b492d77bd04d7028228320626991975f387a9)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs sandbox channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the APNs Sandbox channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSSandboxChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAPNSVoipChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnAPNSVoipChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::APNSVoipChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the APNs VoIP channel to send VoIP notification messages to the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send VoIP notifications to APNs, you have to enable the APNs VoIP channel for an Amazon Pinpoint application.

    The APNSVoipChannel resource represents the status and authentication settings of the APNs VoIP channel for an application.

    :cloudformationResource: AWS::Pinpoint::APNSVoipChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_aPNSVoip_channel = pinpoint.CfnAPNSVoipChannel(self, "MyCfnAPNSVoipChannel",
            application_id="applicationId",
        
            # the properties below are optional
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::APNSVoipChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e07b56d81ac05cf51196c2880bd2c35dea391d56cda8eb3216729843b3d725b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAPNSVoipChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e546229b07b6e8b44cab5a99e0e40cab45d18855ae0e649864ea7cdb535e1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c2a766d747975e8948f040319e6fb13bc06c85fa135e9b563d3c7d2a01d6ba4)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d2442635f63552380f5691b4f2f5e344a6fad8955e9e206810165986399ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-bundleid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1831a835b34e97543fe3b9157a1b3630456957f26f33a5b25b507858298de88f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038b2adfac5a995ff3837e62842990e3fee635b0d670bd232358c8a5ca101e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-defaultauthenticationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAuthenticationMethod"))

    @default_authentication_method.setter
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9819a284e81f1a911bc16420bac69bb5903eba3dfc985142a28bb95abc86b548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63fee5ffd3f00f9f2e7f64f1a643c366c65fcf3aa423809f049fe0951bf7947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3e4965799fb51b3bcc16f143bd95d098db055b2f476fb02833d56c2421a2f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-teamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08db0ae93c70e78a761c2dfbb5fa270e31be8308cbbc76537e046c6d7a5adaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKey"))

    @token_key.setter
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be5b165157762e262c2137b8b4695dda3e6499be18a96e396a2f4a366ef49ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKey", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKeyId"))

    @token_key_id.setter
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5444f4be86adaf5bf170720b1388b1456bd90bb9235a1670199a3638b5d10ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnAPNSVoipChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSVoipChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAPNSVoipChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.
        :param team_id: The identifier that's assigned to your Apple Developer Account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_aPNSVoip_channel_props = pinpoint.CfnAPNSVoipChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134537b920b31565c0f7ec9cd6ba57697dab1a130a1bb3a74fda9fa1399d2bfa)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the APNs VoIP channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the APNs VoIP channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with APNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple Developer Account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with APNs by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSVoipChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAPNSVoipSandboxChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnAPNSVoipSandboxChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::APNSVoipSandboxChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the APNs VoIP sandbox channel to send VoIP notification messages to the sandbox environment of the Apple Push Notification service (APNs). Before you can use Amazon Pinpoint to send VoIP notifications to the APNs sandbox environment, you have to enable the APNs VoIP sandbox channel for an Amazon Pinpoint application.

    The APNSVoipSandboxChannel resource represents the status and authentication settings of the APNs VoIP sandbox channel for an application.

    :cloudformationResource: AWS::Pinpoint::APNSVoipSandboxChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_aPNSVoip_sandbox_channel = pinpoint.CfnAPNSVoipSandboxChannel(self, "MyCfnAPNSVoipSandboxChannel",
            application_id="applicationId",
        
            # the properties below are optional
            bundle_id="bundleId",
            certificate="certificate",
            default_authentication_method="defaultAuthenticationMethod",
            enabled=False,
            private_key="privateKey",
            team_id="teamId",
            token_key="tokenKey",
            token_key_id="tokenKeyId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::APNSVoipSandboxChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the application that the APNs VoIP sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether the APNs VoIP sandbox channel is enabled for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.
        :param team_id: The identifier that's assigned to your Apple developer account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f179fbcf21a1f0bd086b007f6b3edfd1faa7db6677fabfd7d067f0ee747021cb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAPNSVoipSandboxChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe2a21ef757b8e163b647d6b1d70a4c2345d9f5315ca4e0815a15ffc5b0f580)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3d65c28cd0326ea6e65fb5868e735ea34c636cdfc688bb0f913e80a26427be9)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the application that the APNs VoIP sandbox channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50b6a55c5531fe21ad78c887cef888aa704c421cd650221646998d78dbafd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-bundleid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9881543928cce337163f0f450692e4fd7326cf3f0b8252bf5b168929bee3b5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-certificate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fcf424773c2af13b79834dd52f424060a5c697d129ae8faeffe149aa3c90896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-defaultauthenticationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAuthenticationMethod"))

    @default_authentication_method.setter
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58080bed9756bc4a99898d77018138745b9b0a26022499f2af15249f9d83d700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the APNs VoIP sandbox channel is enabled for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61006cf9d0526af7bb68eb1471d0e66d6212ca7ac755853a51a0e1a7247f5c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2342d333e8522b11fbc5632207031d0fe6534c61052091aa91f2f47a829cae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple developer account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-teamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf635ab764d8fa26e3f387d2be0732d000f40ccb22056928f67e712a879feb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKey"))

    @token_key.setter
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f692f7e650c09f565a3c4a8fbe55591eb9f1c688a2a5c2db9aa6dafae628eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKey", value)

    @builtins.property
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenKeyId"))

    @token_key_id.setter
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ff9330b5f2085a236382d5839b13b3ba54fb14222590b737bac3b599ac9094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnAPNSVoipSandboxChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSVoipSandboxChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAPNSVoipSandboxChannel``.

        :param application_id: The unique identifier for the application that the APNs VoIP sandbox channel applies to.
        :param bundle_id: The bundle identifier that's assigned to your iOS app. This identifier is used for APNs tokens.
        :param certificate: The APNs client certificate that you received from Apple. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.
        :param default_authentication_method: The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs. Valid options are ``key`` or ``certificate`` .
        :param enabled: Specifies whether the APNs VoIP sandbox channel is enabled for the application.
        :param private_key: The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.
        :param team_id: The identifier that's assigned to your Apple developer account team. This identifier is used for APNs tokens.
        :param token_key: The authentication key to use for APNs tokens.
        :param token_key_id: The key identifier that's assigned to your APNs signing key. Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_aPNSVoip_sandbox_channel_props = pinpoint.CfnAPNSVoipSandboxChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                bundle_id="bundleId",
                certificate="certificate",
                default_authentication_method="defaultAuthenticationMethod",
                enabled=False,
                private_key="privateKey",
                team_id="teamId",
                token_key="tokenKey",
                token_key_id="tokenKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164ac1be5ac1acc295bbf91bd3a9cbb438574c1f2ffc2b6c66256f52b3cfebae)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument default_authentication_method", value=default_authentication_method, expected_type=type_hints["default_authentication_method"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument token_key", value=token_key, expected_type=type_hints["token_key"])
            check_type(argname="argument token_key_id", value=token_key_id, expected_type=type_hints["token_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the application that the APNs VoIP sandbox channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle identifier that's assigned to your iOS app.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The APNs client certificate that you received from Apple.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using an APNs certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        '''The default authentication method that you want Amazon Pinpoint to use when authenticating with APNs.

        Valid options are ``key`` or ``certificate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-defaultauthenticationmethod
        '''
        result = self._values.get("default_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the APNs VoIP sandbox channel is enabled for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key for the APNs client certificate that you want Amazon Pinpoint to use to communicate with the APNs sandbox environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that's assigned to your Apple developer account team.

        This identifier is used for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        '''The authentication key to use for APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkey
        '''
        result = self._values.get("token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        '''The key identifier that's assigned to your APNs signing key.

        Specify this value if you want Amazon Pinpoint to communicate with the APNs sandbox environment by using APNs tokens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkeyid
        '''
        result = self._values.get("token_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSVoipSandboxChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApp(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnApp",
):
    '''A CloudFormation ``AWS::Pinpoint::App``.

    An *app* is an Amazon Pinpoint application, also referred to as a *project* . An application is a collection of related settings, customer information, segments, campaigns, and other types of Amazon Pinpoint resources.

    The App resource represents an Amazon Pinpoint application.

    :cloudformationResource: AWS::Pinpoint::App
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        # tags: Any
        
        cfn_app = pinpoint.CfnApp(self, "MyCfnApp",
            name="name",
        
            # the properties below are optional
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The display name of the application.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4791d7f10900a0dd87af81d7d79fe9cc68511c7ca55baede5018fb42bcd441)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppProps(name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874c740239b175c3fc973b48bbd36af37de2636672d22473d6b6465e98ba012f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7d21055c937b6040cc9efebf7057788e8e4b04f1ab17059daccd3edd1d9c218)
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
        '''The Amazon Resource Name (ARN) of the application.

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
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The display name of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e28be3f71054300a87dc2762b21dea3474a3f7dd5bd1374138d89cad2fb1981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnAppProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnAppProps:
    def __init__(self, *, name: builtins.str, tags: typing.Any = None) -> None:
        '''Properties for defining a ``CfnApp``.

        :param name: The display name of the application.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            # tags: Any
            
            cfn_app_props = pinpoint.CfnAppProps(
                name="name",
            
                # the properties below are optional
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b841a739e748aadf8d0f90e76b7b6e27464c35a344204d56e26247ab9ce7e1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The display name of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplicationSettings(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnApplicationSettings",
):
    '''A CloudFormation ``AWS::Pinpoint::ApplicationSettings``.

    Specifies the settings for an Amazon Pinpoint application. In Amazon Pinpoint, an *application* (also referred to as an *app* or *project* ) is a collection of related settings, customer information, segments, and campaigns, and other types of Amazon Pinpoint resources.

    :cloudformationResource: AWS::Pinpoint::ApplicationSettings
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_application_settings = pinpoint.CfnApplicationSettings(self, "MyCfnApplicationSettings",
            application_id="applicationId",
        
            # the properties below are optional
            campaign_hook=pinpoint.CfnApplicationSettings.CampaignHookProperty(
                lambda_function_name="lambdaFunctionName",
                mode="mode",
                web_url="webUrl"
            ),
            cloud_watch_metrics_enabled=False,
            limits=pinpoint.CfnApplicationSettings.LimitsProperty(
                daily=123,
                maximum_duration=123,
                messages_per_second=123,
                total=123
            ),
            quiet_time=pinpoint.CfnApplicationSettings.QuietTimeProperty(
                end="end",
                start="start"
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        campaign_hook: typing.Optional[typing.Union[typing.Union["CfnApplicationSettings.CampaignHookProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        limits: typing.Optional[typing.Union[typing.Union["CfnApplicationSettings.LimitsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        quiet_time: typing.Optional[typing.Union[typing.Union["CfnApplicationSettings.QuietTimeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::ApplicationSettings``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application.
        :param campaign_hook: The settings for the Lambda function to use by default as a code hook for campaigns in the application. To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.
        :param cloud_watch_metrics_enabled: Specifies whether to enable application-related alarms in Amazon CloudWatch.
        :param limits: The default sending limits for campaigns in the application. To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.
        :param quiet_time: The default quiet time for campaigns in the application. Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met: - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value. - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings). - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings). If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled. To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf25db5a2f39b69aca8a33454894fd1766efd2f43a0cd55cdaa9251dc9fdb87)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationSettingsProps(
            application_id=application_id,
            campaign_hook=campaign_hook,
            cloud_watch_metrics_enabled=cloud_watch_metrics_enabled,
            limits=limits,
            quiet_time=quiet_time,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c641cd4454890886c658d8c1e8a76d47c548fe8e0e8bfb71bb9c6a91ad63db2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a9c7eb41d98d0764c8ac28670fd74b732246b97ed0b71b838c46069d42f9ccf)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015ae3c07c563e6ba464406bf9ac01e8a1657aa88bb062c959dd08db07da3939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="campaignHook")
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union["CfnApplicationSettings.CampaignHookProperty", _IResolvable_a771d0ef]]:
        '''The settings for the Lambda function to use by default as a code hook for campaigns in the application.

        To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-campaignhook
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplicationSettings.CampaignHookProperty", _IResolvable_a771d0ef]], jsii.get(self, "campaignHook"))

    @campaign_hook.setter
    def campaign_hook(
        self,
        value: typing.Optional[typing.Union["CfnApplicationSettings.CampaignHookProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6a67df9c75da42632465499ead12facf7534e831ce801e5a400bff659b1dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "campaignHook", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchMetricsEnabled")
    def cloud_watch_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable application-related alarms in Amazon CloudWatch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-cloudwatchmetricsenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "cloudWatchMetricsEnabled"))

    @cloud_watch_metrics_enabled.setter
    def cloud_watch_metrics_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5098168cb1b5c2cad35f1ccfd68fb61fe1b6f513e7b8ece1603972b36ad8b80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchMetricsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> typing.Optional[typing.Union["CfnApplicationSettings.LimitsProperty", _IResolvable_a771d0ef]]:
        '''The default sending limits for campaigns in the application.

        To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-limits
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplicationSettings.LimitsProperty", _IResolvable_a771d0ef]], jsii.get(self, "limits"))

    @limits.setter
    def limits(
        self,
        value: typing.Optional[typing.Union["CfnApplicationSettings.LimitsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d34a8c378db2f5ff8ceb0ab049ca8c88506629509b003996f182269c306e4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value)

    @builtins.property
    @jsii.member(jsii_name="quietTime")
    def quiet_time(
        self,
    ) -> typing.Optional[typing.Union["CfnApplicationSettings.QuietTimeProperty", _IResolvable_a771d0ef]]:
        '''The default quiet time for campaigns in the application.

        Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met:

        - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value.
        - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings).
        - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings).

        If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled.

        To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-quiettime
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplicationSettings.QuietTimeProperty", _IResolvable_a771d0ef]], jsii.get(self, "quietTime"))

    @quiet_time.setter
    def quiet_time(
        self,
        value: typing.Optional[typing.Union["CfnApplicationSettings.QuietTimeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c88848954a038aba6196f0f54a67afa5930823a874680db5bf7209c98b0bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quietTime", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnApplicationSettings.CampaignHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_name": "lambdaFunctionName",
            "mode": "mode",
            "web_url": "webUrl",
        },
    )
    class CampaignHookProperty:
        def __init__(
            self,
            *,
            lambda_function_name: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            web_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Lambda function to use by default as a code hook for campaigns in the application.

            :param lambda_function_name: The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to send messages for campaigns in the application.
            :param mode: The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:. - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign. - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.
            :param web_url: The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                campaign_hook_property = pinpoint.CfnApplicationSettings.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__103885ff0e884277f249b55613135a29a3e4a2adcef62644b26f74831be6b410)
                check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument web_url", value=web_url, expected_type=type_hints["web_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if mode is not None:
                self._values["mode"] = mode
            if web_url is not None:
                self._values["web_url"] = web_url

        @builtins.property
        def lambda_function_name(self) -> typing.Optional[builtins.str]:
            '''The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to send messages for campaigns in the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-lambdafunctionname
            '''
            result = self._values.get("lambda_function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:.

            - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign.
            - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def web_url(self) -> typing.Optional[builtins.str]:
            '''The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-weburl
            '''
            result = self._values.get("web_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnApplicationSettings.LimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "maximum_duration": "maximumDuration",
            "messages_per_second": "messagesPerSecond",
            "total": "total",
        },
    )
    class LimitsProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[jsii.Number] = None,
            maximum_duration: typing.Optional[jsii.Number] = None,
            messages_per_second: typing.Optional[jsii.Number] = None,
            total: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the default sending limits for campaigns in the application.

            :param daily: The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period. The maximum value is 100.
            :param maximum_duration: The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign. The minimum value is 60 seconds.
            :param messages_per_second: The maximum number of messages that a campaign can send each second. The minimum value is 1. The maximum value is 20,000.
            :param total: The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign. The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                limits_property = pinpoint.CfnApplicationSettings.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    total=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32f9fe931904ce2a93dc77dafa29289eae10d3c15aa373b0bd5ab70765245543)
                check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
                check_type(argname="argument maximum_duration", value=maximum_duration, expected_type=type_hints["maximum_duration"])
                check_type(argname="argument messages_per_second", value=messages_per_second, expected_type=type_hints["messages_per_second"])
                check_type(argname="argument total", value=total, expected_type=type_hints["total"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if maximum_duration is not None:
                self._values["maximum_duration"] = maximum_duration
            if messages_per_second is not None:
                self._values["messages_per_second"] = messages_per_second
            if total is not None:
                self._values["total"] = total

        @builtins.property
        def daily(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period.

            The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-daily
            '''
            result = self._values.get("daily")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_duration(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign.

            The minimum value is 60 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-maximumduration
            '''
            result = self._values.get("maximum_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def messages_per_second(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send each second.

            The minimum value is 1. The maximum value is 20,000.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-messagespersecond
            '''
            result = self._values.get("messages_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign.

            The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-total
            '''
            result = self._values.get("total")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnApplicationSettings.QuietTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class QuietTimeProperty:
        def __init__(self, *, end: builtins.str, start: builtins.str) -> None:
            '''Specifies the start and end times that define a time range when messages aren't sent to endpoints.

            :param end: The specific time when quiet time ends. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.
            :param start: The specific time when quiet time begins. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                quiet_time_property = pinpoint.CfnApplicationSettings.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27b22c680a7b9da065ed90da5bfd19b3c5a4d698e93abe2c2f6a123c37a14197)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "end": end,
                "start": start,
            }

        @builtins.property
        def end(self) -> builtins.str:
            '''The specific time when quiet time ends.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html#cfn-pinpoint-applicationsettings-quiettime-end
            '''
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def start(self) -> builtins.str:
            '''The specific time when quiet time begins.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html#cfn-pinpoint-applicationsettings-quiettime-start
            '''
            result = self._values.get("start")
            assert result is not None, "Required property 'start' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuietTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnApplicationSettingsProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "campaign_hook": "campaignHook",
        "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
        "limits": "limits",
        "quiet_time": "quietTime",
    },
)
class CfnApplicationSettingsProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        campaign_hook: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        limits: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.LimitsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        quiet_time: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplicationSettings``.

        :param application_id: The unique identifier for the Amazon Pinpoint application.
        :param campaign_hook: The settings for the Lambda function to use by default as a code hook for campaigns in the application. To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.
        :param cloud_watch_metrics_enabled: Specifies whether to enable application-related alarms in Amazon CloudWatch.
        :param limits: The default sending limits for campaigns in the application. To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.
        :param quiet_time: The default quiet time for campaigns in the application. Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met: - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value. - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings). - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings). If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled. To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_application_settings_props = pinpoint.CfnApplicationSettingsProps(
                application_id="applicationId",
            
                # the properties below are optional
                campaign_hook=pinpoint.CfnApplicationSettings.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                ),
                cloud_watch_metrics_enabled=False,
                limits=pinpoint.CfnApplicationSettings.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    total=123
                ),
                quiet_time=pinpoint.CfnApplicationSettings.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fd7593767843fc4f35f1601dfafc1114297acdb348a8d18225e340f91a1d61)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument campaign_hook", value=campaign_hook, expected_type=type_hints["campaign_hook"])
            check_type(argname="argument cloud_watch_metrics_enabled", value=cloud_watch_metrics_enabled, expected_type=type_hints["cloud_watch_metrics_enabled"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument quiet_time", value=quiet_time, expected_type=type_hints["quiet_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if campaign_hook is not None:
            self._values["campaign_hook"] = campaign_hook
        if cloud_watch_metrics_enabled is not None:
            self._values["cloud_watch_metrics_enabled"] = cloud_watch_metrics_enabled
        if limits is not None:
            self._values["limits"] = limits
        if quiet_time is not None:
            self._values["quiet_time"] = quiet_time

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[CfnApplicationSettings.CampaignHookProperty, _IResolvable_a771d0ef]]:
        '''The settings for the Lambda function to use by default as a code hook for campaigns in the application.

        To override these settings for a specific campaign, use the Campaign resource to define custom Lambda function settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-campaignhook
        '''
        result = self._values.get("campaign_hook")
        return typing.cast(typing.Optional[typing.Union[CfnApplicationSettings.CampaignHookProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cloud_watch_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable application-related alarms in Amazon CloudWatch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-cloudwatchmetricsenabled
        '''
        result = self._values.get("cloud_watch_metrics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional[typing.Union[CfnApplicationSettings.LimitsProperty, _IResolvable_a771d0ef]]:
        '''The default sending limits for campaigns in the application.

        To override these limits for a specific campaign, use the Campaign resource to define custom limits for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-limits
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Union[CfnApplicationSettings.LimitsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def quiet_time(
        self,
    ) -> typing.Optional[typing.Union[CfnApplicationSettings.QuietTimeProperty, _IResolvable_a771d0ef]]:
        '''The default quiet time for campaigns in the application.

        Quiet time is a specific time range when campaigns don't send messages to endpoints, if all the following conditions are met:

        - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value.
        - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the application (or a campaign that has custom quiet time settings).
        - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the application (or a campaign that has custom quiet time settings).

        If any of the preceding conditions isn't met, the endpoint will receive messages from a campaign, even if quiet time is enabled.

        To override the default quiet time settings for a specific campaign, use the Campaign resource to define a custom quiet time for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-quiettime
        '''
        result = self._values.get("quiet_time")
        return typing.cast(typing.Optional[typing.Union[CfnApplicationSettings.QuietTimeProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationSettingsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnBaiduChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnBaiduChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::BaiduChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the Baidu channel to send notifications to the Baidu Cloud Push notification service. Before you can use Amazon Pinpoint to send notifications to the Baidu Cloud Push service, you have to enable the Baidu channel for an Amazon Pinpoint application.

    The BaiduChannel resource represents the status and authentication settings of the Baidu channel for an application.

    :cloudformationResource: AWS::Pinpoint::BaiduChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_baidu_channel = pinpoint.CfnBaiduChannel(self, "MyCfnBaiduChannel",
            api_key="apiKey",
            application_id="applicationId",
            secret_key="secretKey",
        
            # the properties below are optional
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        secret_key: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::BaiduChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key: The API key that you received from the Baidu Cloud Push service to communicate with the service.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.
        :param secret_key: The secret key that you received from the Baidu Cloud Push service to communicate with the service.
        :param enabled: Specifies whether to enable the Baidu channel for the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f961110d7709f1c61c69f6ac0c6b9f921b4aae71b4bb27e98289ef3a2139ab77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBaiduChannelProps(
            api_key=api_key,
            application_id=application_id,
            secret_key=secret_key,
            enabled=enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3462693540d17552e574646088d3ce486e384d711274971451db8f8ca432e8e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34d50d36649e060d572c159366f5637f53752b3bb34e852f95cd895568b12d25)
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
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        '''The API key that you received from the Baidu Cloud Push service to communicate with the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-apikey
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c88f9b34391f99adc6c07c7335015361cb903cfc103c459396b53aee1ef814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value)

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0defa188185f6baa5aefa85dd6e30ece25d260dae6c76f3e83949b8848f778f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        '''The secret key that you received from the Baidu Cloud Push service to communicate with the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-secretkey
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fa330dd617578faaa68678a9263894bd2179eadb43b78759b4dfd14d764b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the Baidu channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3374dd9a64c3da8f251c9e59cd630c71be0077de39ee64bb3c54c6c0ac70f9c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnBaiduChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_id": "applicationId",
        "secret_key": "secretKey",
        "enabled": "enabled",
    },
)
class CfnBaiduChannelProps:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        secret_key: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnBaiduChannel``.

        :param api_key: The API key that you received from the Baidu Cloud Push service to communicate with the service.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.
        :param secret_key: The secret key that you received from the Baidu Cloud Push service to communicate with the service.
        :param enabled: Specifies whether to enable the Baidu channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_baidu_channel_props = pinpoint.CfnBaiduChannelProps(
                api_key="apiKey",
                application_id="applicationId",
                secret_key="secretKey",
            
                # the properties below are optional
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275b83d64f2fe22f6e2406c0bbe52e8e31106a87e9a916666c52a01df0f6e4b2)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "application_id": application_id,
            "secret_key": secret_key,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def api_key(self) -> builtins.str:
        '''The API key that you received from the Baidu Cloud Push service to communicate with the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-apikey
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you're configuring the Baidu channel for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_key(self) -> builtins.str:
        '''The secret key that you received from the Baidu Cloud Push service to communicate with the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-secretkey
        '''
        result = self._values.get("secret_key")
        assert result is not None, "Required property 'secret_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the Baidu channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBaiduChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnCampaign(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnCampaign",
):
    '''A CloudFormation ``AWS::Pinpoint::Campaign``.

    Specifies the settings for a campaign. A *campaign* is a messaging initiative that engages a specific segment of users for an Amazon Pinpoint application.

    :cloudformationResource: AWS::Pinpoint::Campaign
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        # attributes: Any
        # custom_config: Any
        # metrics: Any
        # tags: Any
        
        cfn_campaign = pinpoint.CfnCampaign(self, "MyCfnCampaign",
            application_id="applicationId",
            name="name",
            schedule=pinpoint.CfnCampaign.ScheduleProperty(
                end_time="endTime",
                event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                    dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                        attributes=attributes,
                        event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        metrics=metrics
                    ),
                    filter_type="filterType"
                ),
                frequency="frequency",
                is_local_time=False,
                quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                    end="end",
                    start="start"
                ),
                start_time="startTime",
                time_zone="timeZone"
            ),
            segment_id="segmentId",
        
            # the properties below are optional
            additional_treatments=[pinpoint.CfnCampaign.WriteTreatmentResourceProperty(
                custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                ),
                message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                    adm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                        content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                ),
                schedule=pinpoint.CfnCampaign.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                        dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                ),
                size_percent=123,
                template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                    email_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    )
                ),
                treatment_description="treatmentDescription",
                treatment_name="treatmentName"
            )],
            campaign_hook=pinpoint.CfnCampaign.CampaignHookProperty(
                lambda_function_name="lambdaFunctionName",
                mode="mode",
                web_url="webUrl"
            ),
            custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                delivery_uri="deliveryUri",
                endpoint_types=["endpointTypes"]
            ),
            description="description",
            holdout_percent=123,
            is_paused=False,
            limits=pinpoint.CfnCampaign.LimitsProperty(
                daily=123,
                maximum_duration=123,
                messages_per_second=123,
                session=123,
                total=123
            ),
            message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                adm_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                apns_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                baidu_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                    data="data"
                ),
                default_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                    body="body",
                    from_address="fromAddress",
                    html_body="htmlBody",
                    title="title"
                ),
                gcm_message=pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                ),
                in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                    content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                        background_color="backgroundColor",
                        body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                            alignment="alignment",
                            body="body",
                            text_color="textColor"
                        ),
                        header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                            alignment="alignment",
                            header="header",
                            text_color="textColor"
                        ),
                        image_url="imageUrl",
                        primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                            android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        ),
                        secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                            android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        )
                    )],
                    custom_config=custom_config,
                    layout="layout"
                ),
                sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                    body="body",
                    entity_id="entityId",
                    message_type="messageType",
                    origination_number="originationNumber",
                    sender_id="senderId",
                    template_id="templateId"
                )
            ),
            priority=123,
            segment_version=123,
            tags=tags,
            template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                email_template=pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                ),
                push_template=pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                ),
                sms_template=pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                ),
                voice_template=pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                )
            ),
            treatment_description="treatmentDescription",
            treatment_name="treatmentName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        name: builtins.str,
        schedule: typing.Union[typing.Union["CfnCampaign.ScheduleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        segment_id: builtins.str,
        additional_treatments: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnCampaign.WriteTreatmentResourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        campaign_hook: typing.Optional[typing.Union[typing.Union["CfnCampaign.CampaignHookProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        custom_delivery_configuration: typing.Optional[typing.Union[typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        holdout_percent: typing.Optional[jsii.Number] = None,
        is_paused: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        limits: typing.Optional[typing.Union[typing.Union["CfnCampaign.LimitsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        message_configuration: typing.Optional[typing.Union[typing.Union["CfnCampaign.MessageConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        priority: typing.Optional[jsii.Number] = None,
        segment_version: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        template_configuration: typing.Optional[typing.Union[typing.Union["CfnCampaign.TemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        treatment_description: typing.Optional[builtins.str] = None,
        treatment_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::Campaign``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the campaign is associated with.
        :param name: The name of the campaign.
        :param schedule: The schedule settings for the campaign.
        :param segment_id: The unique identifier for the segment to associate with the campaign.
        :param additional_treatments: An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.
        :param campaign_hook: Specifies the Lambda function to use as a code hook for a campaign.
        :param custom_delivery_configuration: ``AWS::Pinpoint::Campaign.CustomDeliveryConfiguration``.
        :param description: A custom description of the campaign.
        :param holdout_percent: The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.
        :param is_paused: Specifies whether to pause the campaign. A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it. If a campaign is running it will complete and then pause. Pause only pauses or skips the next run for a recurring future scheduled campaign. A campaign scheduled for immediate can't be paused.
        :param limits: The messaging limits for the campaign.
        :param message_configuration: The message configuration settings for the campaign.
        :param priority: An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest. If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.
        :param segment_version: The version of the segment to associate with the campaign.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_configuration: ``AWS::Pinpoint::Campaign.TemplateConfiguration``.
        :param treatment_description: A custom description of the default treatment for the campaign.
        :param treatment_name: A custom name of the default treatment for the campaign, if the campaign has multiple treatments. A *treatment* is a variation of a campaign that's used for A/B testing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4541773d796cd7bd1e9fdd1f6954c7a8d9e17c8cda7251d42b134f503799027b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCampaignProps(
            application_id=application_id,
            name=name,
            schedule=schedule,
            segment_id=segment_id,
            additional_treatments=additional_treatments,
            campaign_hook=campaign_hook,
            custom_delivery_configuration=custom_delivery_configuration,
            description=description,
            holdout_percent=holdout_percent,
            is_paused=is_paused,
            limits=limits,
            message_configuration=message_configuration,
            priority=priority,
            segment_version=segment_version,
            tags=tags,
            template_configuration=template_configuration,
            treatment_description=treatment_description,
            treatment_name=treatment_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f210abf917deba3041a8482b86e650ccd1b1f07ddf7070ea8629ed48f6d22ab8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17cfee3021ccbd47251a0edb2583ee52835b5216c92bddc4f9f1017472f5921c)
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
        '''The Amazon Resource Name (ARN) of the campaign.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCampaignId")
    def attr_campaign_id(self) -> builtins.str:
        '''The unique identifier for the campaign.

        :cloudformationAttribute: CampaignId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCampaignId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the campaign is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b5499cc86281e48eae8e0c5014fca230153dba487c974ee9ef2c0ea55fcfd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40b6cda7b00aa16047609a8f929fc6de794647c87c16760e311329450c8d80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_a771d0ef]:
        '''The schedule settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-schedule
        '''
        return typing.cast(typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_a771d0ef], jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(
        self,
        value: typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21ed579b6432231d83d6d12d71c59b699e46c3c96cb385dbd819dd6c833309f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="segmentId")
    def segment_id(self) -> builtins.str:
        '''The unique identifier for the segment to associate with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentid
        '''
        return typing.cast(builtins.str, jsii.get(self, "segmentId"))

    @segment_id.setter
    def segment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9c90984d99d4aaf7c4e41fd9cb559df394ac074b4f8dc3e783a38248f9abb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentId", value)

    @builtins.property
    @jsii.member(jsii_name="additionalTreatments")
    def additional_treatments(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCampaign.WriteTreatmentResourceProperty", _IResolvable_a771d0ef]]]]:
        '''An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-additionaltreatments
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCampaign.WriteTreatmentResourceProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "additionalTreatments"))

    @additional_treatments.setter
    def additional_treatments(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCampaign.WriteTreatmentResourceProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c89f6e9524ba088b21d464f3efdd773c66ae19ba8ad98cb7a99b8c216ac8ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalTreatments", value)

    @builtins.property
    @jsii.member(jsii_name="campaignHook")
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union["CfnCampaign.CampaignHookProperty", _IResolvable_a771d0ef]]:
        '''Specifies the Lambda function to use as a code hook for a campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-campaignhook
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCampaign.CampaignHookProperty", _IResolvable_a771d0ef]], jsii.get(self, "campaignHook"))

    @campaign_hook.setter
    def campaign_hook(
        self,
        value: typing.Optional[typing.Union["CfnCampaign.CampaignHookProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e7cb85d8c4b219975f6688174dfe88308fd0d38da3b0446b28fc78dbfd230d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "campaignHook", value)

    @builtins.property
    @jsii.member(jsii_name="customDeliveryConfiguration")
    def custom_delivery_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Pinpoint::Campaign.CustomDeliveryConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-customdeliveryconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "customDeliveryConfiguration"))

    @custom_delivery_configuration.setter
    def custom_delivery_configuration(
        self,
        value: typing.Optional[typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f5dfd8720435a9ce21c9a4f0a5bec8ab2146fd0d570bf23bbd1820828851ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDeliveryConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d45fcab699ece8198987f3f9add8c9514454744c755380f96679d2ed5d446b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="holdoutPercent")
    def holdout_percent(self) -> typing.Optional[jsii.Number]:
        '''The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-holdoutpercent
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "holdoutPercent"))

    @holdout_percent.setter
    def holdout_percent(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c91861545140f23d40fd6874edf2bec082e7dc2de4cca50c9720af02f837d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "holdoutPercent", value)

    @builtins.property
    @jsii.member(jsii_name="isPaused")
    def is_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to pause the campaign.

        A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it. If a campaign is running it will complete and then pause. Pause only pauses or skips the next run for a recurring future scheduled campaign. A campaign scheduled for immediate can't be paused.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-ispaused
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "isPaused"))

    @is_paused.setter
    def is_paused(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eab9380b78222bd724427e8d35207323ba2ea74d8181f0500b030fcd46c538e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPaused", value)

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> typing.Optional[typing.Union["CfnCampaign.LimitsProperty", _IResolvable_a771d0ef]]:
        '''The messaging limits for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-limits
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCampaign.LimitsProperty", _IResolvable_a771d0ef]], jsii.get(self, "limits"))

    @limits.setter
    def limits(
        self,
        value: typing.Optional[typing.Union["CfnCampaign.LimitsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07ddf54c74d6b24a96c24baa21fe9db78e1afe191fd98c8968b47ead90a5f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value)

    @builtins.property
    @jsii.member(jsii_name="messageConfiguration")
    def message_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The message configuration settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-messageconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "messageConfiguration"))

    @message_configuration.setter
    def message_configuration(
        self,
        value: typing.Optional[typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f39a9cdc96948eef8b79f16b10b629af2c69def79d27da4424d904be2c0fdf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> typing.Optional[jsii.Number]:
        '''An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest.

        If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-priority
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59984b4ef6210c445c94031b8a23fa7d2ca6dea33eb2fe80ada9efdf83e4e030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="segmentVersion")
    def segment_version(self) -> typing.Optional[jsii.Number]:
        '''The version of the segment to associate with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentversion
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "segmentVersion"))

    @segment_version.setter
    def segment_version(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69decea91b1db2db0c9e7a6177cd9ad407a99573af706b7a8c7be74719426398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentVersion", value)

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    def template_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnCampaign.TemplateConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Pinpoint::Campaign.TemplateConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-templateconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCampaign.TemplateConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "templateConfiguration"))

    @template_configuration.setter
    def template_configuration(
        self,
        value: typing.Optional[typing.Union["CfnCampaign.TemplateConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d125de3376c65c4042b017d6790f2d2e9de8743b494ca3aa66650320b8e03683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="treatmentDescription")
    def treatment_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the default treatment for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "treatmentDescription"))

    @treatment_description.setter
    def treatment_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8eda1a6bb530d88122f882e6d3548d0e40858795e49c079934fb92fe621af5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "treatmentDescription", value)

    @builtins.property
    @jsii.member(jsii_name="treatmentName")
    def treatment_name(self) -> typing.Optional[builtins.str]:
        '''A custom name of the default treatment for the campaign, if the campaign has multiple treatments.

        A *treatment* is a variation of a campaign that's used for A/B testing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "treatmentName"))

    @treatment_name.setter
    def treatment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e07911e6911fe8240669e042679c32b24f4c78de54a29f946184770fa824b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "treatmentName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.AttributeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_type": "attributeType", "values": "values"},
    )
    class AttributeDimensionProperty:
        def __init__(
            self,
            *,
            attribute_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies attribute-based criteria for including or excluding endpoints from a segment.

            :param attribute_type: The type of segment dimension to use. Valid values are:. - ``INCLUSIVE`` – endpoints that have attributes matching the values are included in the segment. - ``EXCLUSIVE`` – endpoints that have attributes matching the values are excluded from the segment. - ``CONTAINS`` – endpoints that have attributes' substrings match the values are included in the segment. - ``BEFORE`` – endpoints with attributes read as ISO_INSTANT datetimes before the value are included in the segment. - ``AFTER`` – endpoints with attributes read as ISO_INSTANT datetimes after the value are included in the segment. - ``BETWEEN`` – endpoints with attributes read as ISO_INSTANT datetimes between the values are included in the segment. - ``ON`` – endpoints with attributes read as ISO_INSTANT dates on the value are included in the segment. Time is ignored in this comparison.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``AttributeType`` property, endpoints are included or excluded from the segment if their attribute values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                attribute_dimension_property = pinpoint.CfnCampaign.AttributeDimensionProperty(
                    attribute_type="attributeType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5596bbd839989137298ae6c67b14ecd834c8241dca10424e932ed6dcaa2f96fe)
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use. Valid values are:.

            - ``INCLUSIVE`` – endpoints that have attributes matching the values are included in the segment.
            - ``EXCLUSIVE`` – endpoints that have attributes matching the values are excluded from the segment.
            - ``CONTAINS`` – endpoints that have attributes' substrings match the values are included in the segment.
            - ``BEFORE`` – endpoints with attributes read as ISO_INSTANT datetimes before the value are included in the segment.
            - ``AFTER`` – endpoints with attributes read as ISO_INSTANT datetimes after the value are included in the segment.
            - ``BETWEEN`` – endpoints with attributes read as ISO_INSTANT datetimes between the values are included in the segment.
            - ``ON`` – endpoints with attributes read as ISO_INSTANT dates on the value are included in the segment. Time is ignored in this comparison.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html#cfn-pinpoint-campaign-attributedimension-attributetype
            '''
            result = self._values.get("attribute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``AttributeType`` property, endpoints are included or excluded from the segment if their attribute values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html#cfn-pinpoint-campaign-attributedimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.CampaignCustomMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"data": "data"},
    )
    class CampaignCustomMessageProperty:
        def __init__(self, *, data: typing.Optional[builtins.str] = None) -> None:
            '''
            :param data: ``CfnCampaign.CampaignCustomMessageProperty.Data``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigncustommessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                campaign_custom_message_property = pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b88fe61f00e69c95ac6b075367b95aff4ccb51711a2f7ed1e21b513184ec0a2)
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data is not None:
                self._values["data"] = data

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''``CfnCampaign.CampaignCustomMessageProperty.Data``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigncustommessage.html#cfn-pinpoint-campaign-campaigncustommessage-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignCustomMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.CampaignEmailMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body": "body",
            "from_address": "fromAddress",
            "html_body": "htmlBody",
            "title": "title",
        },
    )
    class CampaignEmailMessageProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[builtins.str] = None,
            from_address: typing.Optional[builtins.str] = None,
            html_body: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and "From" address for an email message that's sent to recipients of a campaign.

            :param body: The body of the email for recipients whose email clients don't render HTML content.
            :param from_address: The verified email address to send the email from. The default address is the ``FromAddress`` specified for the email channel for the application.
            :param html_body: The body of the email, in HTML format, for recipients whose email clients render HTML content.
            :param title: The subject line, or title, of the email.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                campaign_email_message_property = pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                    body="body",
                    from_address="fromAddress",
                    html_body="htmlBody",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cad9fd05af7ff052dc96c7041a287b6124f54cb7e95dc06682fe0eb4dfa9e78)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument from_address", value=from_address, expected_type=type_hints["from_address"])
                check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if from_address is not None:
                self._values["from_address"] = from_address
            if html_body is not None:
                self._values["html_body"] = html_body
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the email for recipients whose email clients don't render HTML content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def from_address(self) -> typing.Optional[builtins.str]:
            '''The verified email address to send the email from.

            The default address is the ``FromAddress`` specified for the email channel for the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-fromaddress
            '''
            result = self._values.get("from_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def html_body(self) -> typing.Optional[builtins.str]:
            '''The body of the email, in HTML format, for recipients whose email clients render HTML content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-htmlbody
            '''
            result = self._values.get("html_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The subject line, or title, of the email.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignEmailMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.CampaignEventFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions", "filter_type": "filterType"},
    )
    class CampaignEventFilterProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[typing.Union["CfnCampaign.EventDimensionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            filter_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the settings for events that cause a campaign to be sent.

            :param dimensions: The dimension settings of the event filter for the campaign.
            :param filter_type: The type of event that causes the campaign to be sent. Valid values are: ``SYSTEM`` , sends the campaign when a system event occurs; and, ``ENDPOINT`` , sends the campaign when an endpoint event (Events resource) occurs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                
                campaign_event_filter_property = pinpoint.CfnCampaign.CampaignEventFilterProperty(
                    dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                        attributes=attributes,
                        event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        metrics=metrics
                    ),
                    filter_type="filterType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__419b0f2785f3cdb6cd28dda11583fd7808e2ac5ef4dde6993f922a8619d70ba7)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if filter_type is not None:
                self._values["filter_type"] = filter_type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.EventDimensionsProperty", _IResolvable_a771d0ef]]:
            '''The dimension settings of the event filter for the campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html#cfn-pinpoint-campaign-campaigneventfilter-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.EventDimensionsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The type of event that causes the campaign to be sent.

            Valid values are: ``SYSTEM`` , sends the campaign when a system event occurs; and, ``ENDPOINT`` , sends the campaign when an endpoint event (Events resource) occurs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html#cfn-pinpoint-campaign-campaigneventfilter-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignEventFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.CampaignHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_name": "lambdaFunctionName",
            "mode": "mode",
            "web_url": "webUrl",
        },
    )
    class CampaignHookProperty:
        def __init__(
            self,
            *,
            lambda_function_name: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            web_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies settings for invoking an Lambda function that customizes a segment for a campaign.

            :param lambda_function_name: The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to customize a segment for a campaign.
            :param mode: The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:. - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign. - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.
            :param web_url: The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                campaign_hook_property = pinpoint.CfnCampaign.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f04c20564ffd54414ab3a3a0a1fabff2e898032bd3f88f3a49ed921ff7aa80d8)
                check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument web_url", value=web_url, expected_type=type_hints["web_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if mode is not None:
                self._values["mode"] = mode
            if web_url is not None:
                self._values["web_url"] = web_url

        @builtins.property
        def lambda_function_name(self) -> typing.Optional[builtins.str]:
            '''The name or Amazon Resource Name (ARN) of the Lambda function that Amazon Pinpoint invokes to customize a segment for a campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-lambdafunctionname
            '''
            result = self._values.get("lambda_function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The mode that Amazon Pinpoint uses to invoke the Lambda function. Possible values are:.

            - ``FILTER`` - Invoke the function to customize the segment that's used by a campaign.
            - ``DELIVERY`` - (Deprecated) Previously, invoked the function to send a campaign through a custom channel. This functionality is not supported anymore. To send a campaign through a custom channel, use the ``CustomDeliveryConfiguration`` and ``CampaignCustomMessage`` objects of the campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def web_url(self) -> typing.Optional[builtins.str]:
            '''The web URL that Amazon Pinpoint calls to invoke the Lambda function over HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-weburl
            '''
            result = self._values.get("web_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.CampaignInAppMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content": "content",
            "custom_config": "customConfig",
            "layout": "layout",
        },
    )
    class CampaignInAppMessageProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnCampaign.InAppMessageContentProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            custom_config: typing.Any = None,
            layout: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the appearance of an in-app message, including the message type, the title and body text, text and background colors, and the configurations of buttons that appear in the message.

            :param content: An array that contains configurtion information about the in-app message for the campaign, including title and body text, text colors, background colors, image URLs, and button configurations.
            :param custom_config: Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.
            :param layout: A string that describes how the in-app message will appear. You can specify one of the following:. - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page. - ``TOP_BANNER`` – a message that appears as a banner at the top of the page. - ``OVERLAYS`` – a message that covers entire screen. - ``MOBILE_FEED`` – a message that appears in a window in front of the page. - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page. - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # custom_config: Any
                
                campaign_in_app_message_property = pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                    content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                        background_color="backgroundColor",
                        body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                            alignment="alignment",
                            body="body",
                            text_color="textColor"
                        ),
                        header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                            alignment="alignment",
                            header="header",
                            text_color="textColor"
                        ),
                        image_url="imageUrl",
                        primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                            android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        ),
                        secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                            android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                background_color="backgroundColor",
                                border_radius=123,
                                button_action="buttonAction",
                                link="link",
                                text="text",
                                text_color="textColor"
                            ),
                            ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            ),
                            web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                button_action="buttonAction",
                                link="link"
                            )
                        )
                    )],
                    custom_config=custom_config,
                    layout="layout"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b922b87e0ba762479c27b5931d14e4a1b0cd53149a192e4d0a1aeca132496424)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
                check_type(argname="argument layout", value=layout, expected_type=type_hints["layout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if custom_config is not None:
                self._values["custom_config"] = custom_config
            if layout is not None:
                self._values["layout"] = layout

        @builtins.property
        def content(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCampaign.InAppMessageContentProperty", _IResolvable_a771d0ef]]]]:
            '''An array that contains configurtion information about the in-app message for the campaign, including title and body text, text colors, background colors, image URLs, and button configurations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCampaign.InAppMessageContentProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def custom_config(self) -> typing.Any:
            '''Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-customconfig
            '''
            result = self._values.get("custom_config")
            return typing.cast(typing.Any, result)

        @builtins.property
        def layout(self) -> typing.Optional[builtins.str]:
            '''A string that describes how the in-app message will appear. You can specify one of the following:.

            - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page.
            - ``TOP_BANNER`` – a message that appears as a banner at the top of the page.
            - ``OVERLAYS`` – a message that covers entire screen.
            - ``MOBILE_FEED`` – a message that appears in a window in front of the page.
            - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page.
            - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigninappmessage.html#cfn-pinpoint-campaign-campaigninappmessage-layout
            '''
            result = self._values.get("layout")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignInAppMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.CampaignSmsMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body": "body",
            "entity_id": "entityId",
            "message_type": "messageType",
            "origination_number": "originationNumber",
            "sender_id": "senderId",
            "template_id": "templateId",
        },
    )
    class CampaignSmsMessageProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[builtins.str] = None,
            entity_id: typing.Optional[builtins.str] = None,
            message_type: typing.Optional[builtins.str] = None,
            origination_number: typing.Optional[builtins.str] = None,
            sender_id: typing.Optional[builtins.str] = None,
            template_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and settings for an SMS message that's sent to recipients of a campaign.

            :param body: The body of the SMS message.
            :param entity_id: The entity ID or Principal Entity (PE) id received from the regulatory body for sending SMS in your country.
            :param message_type: The SMS message type. Valid values are ``TRANSACTIONAL`` (for messages that are critical or time-sensitive, such as a one-time passwords) and ``PROMOTIONAL`` (for messsages that aren't critical or time-sensitive, such as marketing messages).
            :param origination_number: The long code to send the SMS message from. This value should be one of the dedicated long codes that's assigned to your AWS account. Although it isn't required, we recommend that you specify the long code using an E.164 format to ensure prompt and accurate delivery of the message. For example, +12065550100.
            :param sender_id: The alphabetic Sender ID to display as the sender of the message on a recipient's device. Support for sender IDs varies by country or region. To specify a phone number as the sender, omit this parameter and use ``OriginationNumber`` instead. For more information about support for Sender ID by country, see the `Amazon Pinpoint User Guide <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ .
            :param template_id: The template ID received from the regulatory body for sending SMS in your country.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                campaign_sms_message_property = pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                    body="body",
                    entity_id="entityId",
                    message_type="messageType",
                    origination_number="originationNumber",
                    sender_id="senderId",
                    template_id="templateId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf74bae8597ffb16a4a8163894d2fa81ae2bd4802ead658243b34f656002ac24)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
                check_type(argname="argument message_type", value=message_type, expected_type=type_hints["message_type"])
                check_type(argname="argument origination_number", value=origination_number, expected_type=type_hints["origination_number"])
                check_type(argname="argument sender_id", value=sender_id, expected_type=type_hints["sender_id"])
                check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if entity_id is not None:
                self._values["entity_id"] = entity_id
            if message_type is not None:
                self._values["message_type"] = message_type
            if origination_number is not None:
                self._values["origination_number"] = origination_number
            if sender_id is not None:
                self._values["sender_id"] = sender_id
            if template_id is not None:
                self._values["template_id"] = template_id

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the SMS message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entity_id(self) -> typing.Optional[builtins.str]:
            '''The entity ID or Principal Entity (PE) id received from the regulatory body for sending SMS in your country.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-entityid
            '''
            result = self._values.get("entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_type(self) -> typing.Optional[builtins.str]:
            '''The SMS message type.

            Valid values are ``TRANSACTIONAL`` (for messages that are critical or time-sensitive, such as a one-time passwords) and ``PROMOTIONAL`` (for messsages that aren't critical or time-sensitive, such as marketing messages).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-messagetype
            '''
            result = self._values.get("message_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def origination_number(self) -> typing.Optional[builtins.str]:
            '''The long code to send the SMS message from.

            This value should be one of the dedicated long codes that's assigned to your AWS account. Although it isn't required, we recommend that you specify the long code using an E.164 format to ensure prompt and accurate delivery of the message. For example, +12065550100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-originationnumber
            '''
            result = self._values.get("origination_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sender_id(self) -> typing.Optional[builtins.str]:
            '''The alphabetic Sender ID to display as the sender of the message on a recipient's device.

            Support for sender IDs varies by country or region. To specify a phone number as the sender, omit this parameter and use ``OriginationNumber`` instead. For more information about support for Sender ID by country, see the `Amazon Pinpoint User Guide <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-senderid
            '''
            result = self._values.get("sender_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def template_id(self) -> typing.Optional[builtins.str]:
            '''The template ID received from the regulatory body for sending SMS in your country.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-templateid
            '''
            result = self._values.get("template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignSmsMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_uri": "deliveryUri",
            "endpoint_types": "endpointTypes",
        },
    )
    class CustomDeliveryConfigurationProperty:
        def __init__(
            self,
            *,
            delivery_uri: typing.Optional[builtins.str] = None,
            endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param delivery_uri: ``CfnCampaign.CustomDeliveryConfigurationProperty.DeliveryUri``.
            :param endpoint_types: ``CfnCampaign.CustomDeliveryConfigurationProperty.EndpointTypes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                custom_delivery_configuration_property = pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__457128f545655310f7a89d972abb8697e0e15d643d6824bbdebf6b7cb1a6fad7)
                check_type(argname="argument delivery_uri", value=delivery_uri, expected_type=type_hints["delivery_uri"])
                check_type(argname="argument endpoint_types", value=endpoint_types, expected_type=type_hints["endpoint_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_uri is not None:
                self._values["delivery_uri"] = delivery_uri
            if endpoint_types is not None:
                self._values["endpoint_types"] = endpoint_types

        @builtins.property
        def delivery_uri(self) -> typing.Optional[builtins.str]:
            '''``CfnCampaign.CustomDeliveryConfigurationProperty.DeliveryUri``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html#cfn-pinpoint-campaign-customdeliveryconfiguration-deliveryuri
            '''
            result = self._values.get("delivery_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnCampaign.CustomDeliveryConfigurationProperty.EndpointTypes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-customdeliveryconfiguration.html#cfn-pinpoint-campaign-customdeliveryconfiguration-endpointtypes
            '''
            result = self._values.get("endpoint_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomDeliveryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.DefaultButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "border_radius": "borderRadius",
            "button_action": "buttonAction",
            "link": "link",
            "text": "text",
            "text_color": "textColor",
        },
    )
    class DefaultButtonConfigurationProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            border_radius: typing.Optional[jsii.Number] = None,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
            text: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default behavior for a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :param background_color: The background color of a button, expressed as a hex color code (such as #000000 for black).
            :param border_radius: The border radius of a button.
            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.
            :param text: The text that appears on a button in an in-app message.
            :param text_color: The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                default_button_configuration_property = pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                    background_color="backgroundColor",
                    border_radius=123,
                    button_action="buttonAction",
                    link="link",
                    text="text",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da1f98760b3d524ab9a096f012a64082defee479e8c8b565543c76199314ffad)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument border_radius", value=border_radius, expected_type=type_hints["border_radius"])
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if border_radius is not None:
                self._values["border_radius"] = border_radius
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link
            if text is not None:
                self._values["text"] = text
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color of a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def border_radius(self) -> typing.Optional[jsii.Number]:
            '''The border radius of a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-borderradius
            '''
            result = self._values.get("border_radius")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text that appears on a button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-defaultbuttonconfiguration.html#cfn-pinpoint-campaign-defaultbuttonconfiguration-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.EventDimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "event_type": "eventType",
            "metrics": "metrics",
        },
    )
    class EventDimensionsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            event_type: typing.Optional[typing.Union[typing.Union["CfnCampaign.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            metrics: typing.Any = None,
        ) -> None:
            '''Specifies the dimensions for an event filter that determines when a campaign is sent or a journey activity is performed.

            :param attributes: One or more custom attributes that your application reports to Amazon Pinpoint. You can use these attributes as selection criteria when you create an event filter.
            :param event_type: The name of the event that causes the campaign to be sent or the journey activity to be performed. This can be a standard event that Amazon Pinpoint generates, such as ``_email.delivered`` or ``_custom.delivered`` . For campaigns, this can also be a custom event that's specific to your application. For information about standard events, see `Streaming Amazon Pinpoint Events <https://docs.aws.amazon.com/pinpoint/latest/developerguide/event-streams.html>`_ in the *Amazon Pinpoint Developer Guide* .
            :param metrics: One or more custom metrics that your application reports to Amazon Pinpoint . You can use these metrics as selection criteria when you create an event filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                
                event_dimensions_property = pinpoint.CfnCampaign.EventDimensionsProperty(
                    attributes=attributes,
                    event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    metrics=metrics
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24d0bc16432023257772621c71b46b5e384599a7acb4be254ee5726e3da00788)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if event_type is not None:
                self._values["event_type"] = event_type
            if metrics is not None:
                self._values["metrics"] = metrics

        @builtins.property
        def attributes(self) -> typing.Any:
            '''One or more custom attributes that your application reports to Amazon Pinpoint.

            You can use these attributes as selection criteria when you create an event filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_type(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.SetDimensionProperty", _IResolvable_a771d0ef]]:
            '''The name of the event that causes the campaign to be sent or the journey activity to be performed.

            This can be a standard event that Amazon Pinpoint generates, such as ``_email.delivered`` or ``_custom.delivered`` . For campaigns, this can also be a custom event that's specific to your application. For information about standard events, see `Streaming Amazon Pinpoint Events <https://docs.aws.amazon.com/pinpoint/latest/developerguide/event-streams.html>`_ in the *Amazon Pinpoint Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-eventtype
            '''
            result = self._values.get("event_type")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.SetDimensionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def metrics(self) -> typing.Any:
            '''One or more custom metrics that your application reports to Amazon Pinpoint .

            You can use these metrics as selection criteria when you create an event filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventDimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.InAppMessageBodyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "body": "body",
            "text_color": "textColor",
        },
    )
    class InAppMessageBodyConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of main body text of the in-app message.

            :param alignment: The text alignment of the main body text of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param body: The main body text of the message.
            :param text_color: The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                in_app_message_body_config_property = pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d97be6df17335dc55972a4299d970b8279e70fa18a8f123e3e54c28326b72a9)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if body is not None:
                self._values["body"] = body
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the main body text of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The main body text of the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebodyconfig.html#cfn-pinpoint-campaign-inappmessagebodyconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageBodyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.InAppMessageButtonProperty",
        jsii_struct_bases=[],
        name_mapping={
            "android": "android",
            "default_config": "defaultConfig",
            "ios": "ios",
            "web": "web",
        },
    )
    class InAppMessageButtonProperty:
        def __init__(
            self,
            *,
            android: typing.Optional[typing.Union[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            default_config: typing.Optional[typing.Union[typing.Union["CfnCampaign.DefaultButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ios: typing.Optional[typing.Union[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            web: typing.Optional[typing.Union[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the configuration of a button that appears in an in-app message.

            :param android: An object that defines the default behavior for a button in in-app messages sent to Android.
            :param default_config: An object that defines the default behavior for a button in an in-app message.
            :param ios: An object that defines the default behavior for a button in in-app messages sent to iOS devices.
            :param web: An object that defines the default behavior for a button in in-app messages for web applications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                in_app_message_button_property = pinpoint.CfnCampaign.InAppMessageButtonProperty(
                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86f46dc3b29cc02420636386554d38e013b0cb0344ed7546c14f953589f35f6a)
                check_type(argname="argument android", value=android, expected_type=type_hints["android"])
                check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
                check_type(argname="argument ios", value=ios, expected_type=type_hints["ios"])
                check_type(argname="argument web", value=web, expected_type=type_hints["web"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if android is not None:
                self._values["android"] = android
            if default_config is not None:
                self._values["default_config"] = default_config
            if ios is not None:
                self._values["ios"] = ios
            if web is not None:
                self._values["web"] = web

        @builtins.property
        def android(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]]:
            '''An object that defines the default behavior for a button in in-app messages sent to Android.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-android
            '''
            result = self._values.get("android")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def default_config(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.DefaultButtonConfigurationProperty", _IResolvable_a771d0ef]]:
            '''An object that defines the default behavior for a button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-defaultconfig
            '''
            result = self._values.get("default_config")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.DefaultButtonConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ios(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]]:
            '''An object that defines the default behavior for a button in in-app messages sent to iOS devices.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-ios
            '''
            result = self._values.get("ios")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def web(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]]:
            '''An object that defines the default behavior for a button in in-app messages for web applications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagebutton.html#cfn-pinpoint-campaign-inappmessagebutton-web
            '''
            result = self._values.get("web")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageButtonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.InAppMessageContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "body_config": "bodyConfig",
            "header_config": "headerConfig",
            "image_url": "imageUrl",
            "primary_btn": "primaryBtn",
            "secondary_btn": "secondaryBtn",
        },
    )
    class InAppMessageContentProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            body_config: typing.Optional[typing.Union[typing.Union["CfnCampaign.InAppMessageBodyConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            header_config: typing.Optional[typing.Union[typing.Union["CfnCampaign.InAppMessageHeaderConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            image_url: typing.Optional[builtins.str] = None,
            primary_btn: typing.Optional[typing.Union[typing.Union["CfnCampaign.InAppMessageButtonProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            secondary_btn: typing.Optional[typing.Union[typing.Union["CfnCampaign.InAppMessageButtonProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the configuration and contents of an in-app message.

            :param background_color: The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).
            :param body_config: Specifies the configuration of main body text in an in-app message template.
            :param header_config: Specifies the configuration and content of the header or title text of the in-app message.
            :param image_url: The URL of the image that appears on an in-app message banner.
            :param primary_btn: An object that contains configuration information about the primary button in an in-app message.
            :param secondary_btn: An object that contains configuration information about the secondary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                in_app_message_content_property = pinpoint.CfnCampaign.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                        android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                        android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8e540cc8d61a5c8a43891207bc6f002221365fb0f8a822d2f3c7ad5ff1a8c98)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument body_config", value=body_config, expected_type=type_hints["body_config"])
                check_type(argname="argument header_config", value=header_config, expected_type=type_hints["header_config"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument primary_btn", value=primary_btn, expected_type=type_hints["primary_btn"])
                check_type(argname="argument secondary_btn", value=secondary_btn, expected_type=type_hints["secondary_btn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if body_config is not None:
                self._values["body_config"] = body_config
            if header_config is not None:
                self._values["header_config"] = header_config
            if image_url is not None:
                self._values["image_url"] = image_url
            if primary_btn is not None:
                self._values["primary_btn"] = primary_btn
            if secondary_btn is not None:
                self._values["secondary_btn"] = secondary_btn

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body_config(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.InAppMessageBodyConfigProperty", _IResolvable_a771d0ef]]:
            '''Specifies the configuration of main body text in an in-app message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-bodyconfig
            '''
            result = self._values.get("body_config")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.InAppMessageBodyConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def header_config(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.InAppMessageHeaderConfigProperty", _IResolvable_a771d0ef]]:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-headerconfig
            '''
            result = self._values.get("header_config")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.InAppMessageHeaderConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image that appears on an in-app message banner.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_btn(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.InAppMessageButtonProperty", _IResolvable_a771d0ef]]:
            '''An object that contains configuration information about the primary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-primarybtn
            '''
            result = self._values.get("primary_btn")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.InAppMessageButtonProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def secondary_btn(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.InAppMessageButtonProperty", _IResolvable_a771d0ef]]:
            '''An object that contains configuration information about the secondary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessagecontent.html#cfn-pinpoint-campaign-inappmessagecontent-secondarybtn
            '''
            result = self._values.get("secondary_btn")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.InAppMessageButtonProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "header": "header",
            "text_color": "textColor",
        },
    )
    class InAppMessageHeaderConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            header: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :param alignment: The text alignment of the title of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param header: The header or title text of the in-app message.
            :param text_color: The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                in_app_message_header_config_property = pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07df763c8998b67257b3253b3f32a17df82b5b4e1d1d333bd08c41fb06749b5b)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if header is not None:
                self._values["header"] = header
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the title of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header(self) -> typing.Optional[builtins.str]:
            '''The header or title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-header
            '''
            result = self._values.get("header")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a string consisting of a hex color code (such as "#000000" for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-inappmessageheaderconfig.html#cfn-pinpoint-campaign-inappmessageheaderconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.LimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "maximum_duration": "maximumDuration",
            "messages_per_second": "messagesPerSecond",
            "session": "session",
            "total": "total",
        },
    )
    class LimitsProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[jsii.Number] = None,
            maximum_duration: typing.Optional[jsii.Number] = None,
            messages_per_second: typing.Optional[jsii.Number] = None,
            session: typing.Optional[jsii.Number] = None,
            total: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the limits on the messages that a campaign can send.

            :param daily: The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period. The maximum value is 100.
            :param maximum_duration: The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign. The minimum value is 60 seconds.
            :param messages_per_second: The maximum number of messages that a campaign can send each second. The minimum value is 1. The maximum value is 20,000.
            :param session: ``CfnCampaign.LimitsProperty.Session``.
            :param total: The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign. The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                limits_property = pinpoint.CfnCampaign.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    session=123,
                    total=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__950e7bce3ae6a11f6165ab433327d1873f0700c161184daa580c0540d079dc2b)
                check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
                check_type(argname="argument maximum_duration", value=maximum_duration, expected_type=type_hints["maximum_duration"])
                check_type(argname="argument messages_per_second", value=messages_per_second, expected_type=type_hints["messages_per_second"])
                check_type(argname="argument session", value=session, expected_type=type_hints["session"])
                check_type(argname="argument total", value=total, expected_type=type_hints["total"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if maximum_duration is not None:
                self._values["maximum_duration"] = maximum_duration
            if messages_per_second is not None:
                self._values["messages_per_second"] = messages_per_second
            if session is not None:
                self._values["session"] = session
            if total is not None:
                self._values["total"] = total

        @builtins.property
        def daily(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during a 24-hour period.

            The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-daily
            '''
            result = self._values.get("daily")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_duration(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, that a campaign can attempt to deliver a message after the scheduled start time for the campaign.

            The minimum value is 60 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-maximumduration
            '''
            result = self._values.get("maximum_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def messages_per_second(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send each second.

            The minimum value is 1. The maximum value is 20,000.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-messagespersecond
            '''
            result = self._values.get("messages_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def session(self) -> typing.Optional[jsii.Number]:
            '''``CfnCampaign.LimitsProperty.Session``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-session
            '''
            result = self._values.get("session")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of messages that a campaign can send to a single endpoint during the course of the campaign.

            The maximum value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-total
            '''
            result = self._values.get("total")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.MessageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "adm_message": "admMessage",
            "apns_message": "apnsMessage",
            "baidu_message": "baiduMessage",
            "custom_message": "customMessage",
            "default_message": "defaultMessage",
            "email_message": "emailMessage",
            "gcm_message": "gcmMessage",
            "in_app_message": "inAppMessage",
            "sms_message": "smsMessage",
        },
    )
    class MessageConfigurationProperty:
        def __init__(
            self,
            *,
            adm_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            apns_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            baidu_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            custom_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.CampaignCustomMessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            default_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            email_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.CampaignEmailMessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            gcm_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.MessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            in_app_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.CampaignInAppMessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sms_message: typing.Optional[typing.Union[typing.Union["CfnCampaign.CampaignSmsMessageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the message configuration settings for a campaign.

            :param adm_message: The message that the campaign sends through the ADM (Amazon Device Messaging) channel. If specified, this message overrides the default message.
            :param apns_message: The message that the campaign sends through the APNs (Apple Push Notification service) channel. If specified, this message overrides the default message.
            :param baidu_message: The message that the campaign sends through the Baidu (Baidu Cloud Push) channel. If specified, this message overrides the default message.
            :param custom_message: ``CfnCampaign.MessageConfigurationProperty.CustomMessage``.
            :param default_message: The default message that the campaign sends through all the channels that are configured for the campaign.
            :param email_message: The message that the campaign sends through the email channel. If specified, this message overrides the default message.
            :param gcm_message: The message that the campaign sends through the GCM channel, which enables Amazon Pinpoint to send push notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service. If specified, this message overrides the default message.
            :param in_app_message: The default message for the in-app messaging channel. This message overrides the default message ( ``DefaultMessage`` ).
            :param sms_message: The message that the campaign sends through the SMS channel. If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # custom_config: Any
                
                message_configuration_property = pinpoint.CfnCampaign.MessageConfigurationProperty(
                    adm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                        content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f506a41a1fea37142d32aa60cd1ded4d78d34489b5d634fb8261fd7484ad2321)
                check_type(argname="argument adm_message", value=adm_message, expected_type=type_hints["adm_message"])
                check_type(argname="argument apns_message", value=apns_message, expected_type=type_hints["apns_message"])
                check_type(argname="argument baidu_message", value=baidu_message, expected_type=type_hints["baidu_message"])
                check_type(argname="argument custom_message", value=custom_message, expected_type=type_hints["custom_message"])
                check_type(argname="argument default_message", value=default_message, expected_type=type_hints["default_message"])
                check_type(argname="argument email_message", value=email_message, expected_type=type_hints["email_message"])
                check_type(argname="argument gcm_message", value=gcm_message, expected_type=type_hints["gcm_message"])
                check_type(argname="argument in_app_message", value=in_app_message, expected_type=type_hints["in_app_message"])
                check_type(argname="argument sms_message", value=sms_message, expected_type=type_hints["sms_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if adm_message is not None:
                self._values["adm_message"] = adm_message
            if apns_message is not None:
                self._values["apns_message"] = apns_message
            if baidu_message is not None:
                self._values["baidu_message"] = baidu_message
            if custom_message is not None:
                self._values["custom_message"] = custom_message
            if default_message is not None:
                self._values["default_message"] = default_message
            if email_message is not None:
                self._values["email_message"] = email_message
            if gcm_message is not None:
                self._values["gcm_message"] = gcm_message
            if in_app_message is not None:
                self._values["in_app_message"] = in_app_message
            if sms_message is not None:
                self._values["sms_message"] = sms_message

        @builtins.property
        def adm_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]]:
            '''The message that the campaign sends through the ADM (Amazon Device Messaging) channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-admmessage
            '''
            result = self._values.get("adm_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def apns_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]]:
            '''The message that the campaign sends through the APNs (Apple Push Notification service) channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-apnsmessage
            '''
            result = self._values.get("apns_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def baidu_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]]:
            '''The message that the campaign sends through the Baidu (Baidu Cloud Push) channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-baidumessage
            '''
            result = self._values.get("baidu_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def custom_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CampaignCustomMessageProperty", _IResolvable_a771d0ef]]:
            '''``CfnCampaign.MessageConfigurationProperty.CustomMessage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-custommessage
            '''
            result = self._values.get("custom_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.CampaignCustomMessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def default_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]]:
            '''The default message that the campaign sends through all the channels that are configured for the campaign.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-defaultmessage
            '''
            result = self._values.get("default_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def email_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CampaignEmailMessageProperty", _IResolvable_a771d0ef]]:
            '''The message that the campaign sends through the email channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-emailmessage
            '''
            result = self._values.get("email_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.CampaignEmailMessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def gcm_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]]:
            '''The message that the campaign sends through the GCM channel, which enables Amazon Pinpoint to send push notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-gcmmessage
            '''
            result = self._values.get("gcm_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def in_app_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CampaignInAppMessageProperty", _IResolvable_a771d0ef]]:
            '''The default message for the in-app messaging channel.

            This message overrides the default message ( ``DefaultMessage`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-inappmessage
            '''
            result = self._values.get("in_app_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.CampaignInAppMessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sms_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CampaignSmsMessageProperty", _IResolvable_a771d0ef]]:
            '''The message that the campaign sends through the SMS channel.

            If specified, this message overrides the default message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-smsmessage
            '''
            result = self._values.get("sms_message")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.CampaignSmsMessageProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.MessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "image_icon_url": "imageIconUrl",
            "image_small_icon_url": "imageSmallIconUrl",
            "image_url": "imageUrl",
            "json_body": "jsonBody",
            "media_url": "mediaUrl",
            "raw_content": "rawContent",
            "silent_push": "silentPush",
            "time_to_live": "timeToLive",
            "title": "title",
            "url": "url",
        },
    )
    class MessageProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            image_icon_url: typing.Optional[builtins.str] = None,
            image_small_icon_url: typing.Optional[builtins.str] = None,
            image_url: typing.Optional[builtins.str] = None,
            json_body: typing.Optional[builtins.str] = None,
            media_url: typing.Optional[builtins.str] = None,
            raw_content: typing.Optional[builtins.str] = None,
            silent_push: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            time_to_live: typing.Optional[jsii.Number] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the content and settings for a push notification that's sent to recipients of a campaign.

            :param action: The action to occur if a recipient taps the push notification. Valid values are:. - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of iOS and Android. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The body of the notification message. The maximum number of characters is 200.
            :param image_icon_url: The URL of the image to display as the push notification icon, such as the icon for the app.
            :param image_small_icon_url: The URL of the image to display as the small, push notification icon, such as a small version of the icon for the app.
            :param image_url: The URL of an image to display in the push notification.
            :param json_body: The JSON payload to use for a silent push notification.
            :param media_url: The URL of the image or video to display in the push notification.
            :param raw_content: The raw, JSON-formatted string to use as the payload for the notification message. If specified, this value overrides all other content for the message.
            :param silent_push: Specifies whether the notification is a silent push notification, which is a push notification that doesn't display on a recipient's device. Silent push notifications can be used for cases such as updating an app's configuration, displaying messages in an in-app message center, or supporting phone home functionality.
            :param time_to_live: The number of seconds that the push notification service should keep the message, if the service is unable to deliver the notification the first time. This value is converted to an expiration value when it's sent to a push notification service. If this value is ``0`` , the service treats the notification as if it expires immediately and the service doesn't store or try to deliver the notification again. This value doesn't apply to messages that are sent through the Amazon Device Messaging (ADM) service.
            :param title: The title to display above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps the push notification and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                message_property = pinpoint.CfnCampaign.MessageProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_small_icon_url="imageSmallIconUrl",
                    image_url="imageUrl",
                    json_body="jsonBody",
                    media_url="mediaUrl",
                    raw_content="rawContent",
                    silent_push=False,
                    time_to_live=123,
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6703765b5d18a108e2935f8935f7d525f1aa48f210691dcb247e0fc2bf2e9ea4)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument image_icon_url", value=image_icon_url, expected_type=type_hints["image_icon_url"])
                check_type(argname="argument image_small_icon_url", value=image_small_icon_url, expected_type=type_hints["image_small_icon_url"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument json_body", value=json_body, expected_type=type_hints["json_body"])
                check_type(argname="argument media_url", value=media_url, expected_type=type_hints["media_url"])
                check_type(argname="argument raw_content", value=raw_content, expected_type=type_hints["raw_content"])
                check_type(argname="argument silent_push", value=silent_push, expected_type=type_hints["silent_push"])
                check_type(argname="argument time_to_live", value=time_to_live, expected_type=type_hints["time_to_live"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if image_icon_url is not None:
                self._values["image_icon_url"] = image_icon_url
            if image_small_icon_url is not None:
                self._values["image_small_icon_url"] = image_small_icon_url
            if image_url is not None:
                self._values["image_url"] = image_url
            if json_body is not None:
                self._values["json_body"] = json_body
            if media_url is not None:
                self._values["media_url"] = media_url
            if raw_content is not None:
                self._values["raw_content"] = raw_content
            if silent_push is not None:
                self._values["silent_push"] = silent_push
            if time_to_live is not None:
                self._values["time_to_live"] = time_to_live
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps the push notification. Valid values are:.

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of iOS and Android.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The body of the notification message.

            The maximum number of characters is 200.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image to display as the push notification icon, such as the icon for the app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imageiconurl
            '''
            result = self._values.get("image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_small_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image to display as the small, push notification icon, such as a small version of the icon for the app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imagesmalliconurl
            '''
            result = self._values.get("image_small_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image to display in the push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def json_body(self) -> typing.Optional[builtins.str]:
            '''The JSON payload to use for a silent push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-jsonbody
            '''
            result = self._values.get("json_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def media_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image or video to display in the push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-mediaurl
            '''
            result = self._values.get("media_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def raw_content(self) -> typing.Optional[builtins.str]:
            '''The raw, JSON-formatted string to use as the payload for the notification message.

            If specified, this value overrides all other content for the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-rawcontent
            '''
            result = self._values.get("raw_content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def silent_push(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether the notification is a silent push notification, which is a push notification that doesn't display on a recipient's device.

            Silent push notifications can be used for cases such as updating an app's configuration, displaying messages in an in-app message center, or supporting phone home functionality.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-silentpush
            '''
            result = self._values.get("silent_push")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def time_to_live(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds that the push notification service should keep the message, if the service is unable to deliver the notification the first time.

            This value is converted to an expiration value when it's sent to a push notification service. If this value is ``0`` , the service treats the notification as if it expires immediately and the service doesn't store or try to deliver the notification again.

            This value doesn't apply to messages that are sent through the Amazon Device Messaging (ADM) service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-timetolive
            '''
            result = self._values.get("time_to_live")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to display above the notification message on a recipient's device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps the push notification and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison_operator": "comparisonOperator", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies metric-based criteria for including or excluding endpoints from a segment.

            These criteria derive from custom metrics that you define for endpoints.

            :param comparison_operator: The operator to use when comparing metric values. Valid values are: ``GREATER_THAN`` , ``LESS_THAN`` , ``GREATER_THAN_OR_EQUAL`` , ``LESS_THAN_OR_EQUAL`` , and ``EQUAL`` .
            :param value: The value to compare.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                metric_dimension_property = pinpoint.CfnCampaign.MetricDimensionProperty(
                    comparison_operator="comparisonOperator",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71dd3123da0599764a0023bdd6a9ae644343acb314a3274b2d7f55ddd775edc4)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''The operator to use when comparing metric values.

            Valid values are: ``GREATER_THAN`` , ``LESS_THAN`` , ``GREATER_THAN_OR_EQUAL`` , ``LESS_THAN_OR_EQUAL`` , and ``EQUAL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html#cfn-pinpoint-campaign-metricdimension-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value to compare.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html#cfn-pinpoint-campaign-metricdimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.OverrideButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"button_action": "buttonAction", "link": "link"},
    )
    class OverrideButtonConfigurationProperty:
        def __init__(
            self,
            *,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of a button with settings that are specific to a certain device type.

            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                override_button_configuration_property = pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                    button_action="buttonAction",
                    link="link"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5556ee2f86b9a70c0cb7d02d2c3ab85cb46316beb654288c4ea34242460e614b)
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html#cfn-pinpoint-campaign-overridebuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-overridebuttonconfiguration.html#cfn-pinpoint-campaign-overridebuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.QuietTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class QuietTimeProperty:
        def __init__(self, *, end: builtins.str, start: builtins.str) -> None:
            '''Specifies the start and end times that define a time range when messages aren't sent to endpoints.

            :param end: The specific time when quiet time ends. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.
            :param start: The specific time when quiet time begins. This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                quiet_time_property = pinpoint.CfnCampaign.QuietTimeProperty(
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__437d4e16c16916f75e859e32a3fa46726fbb88b1b9949eb8a443fb6aa28f192d)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "end": end,
                "start": start,
            }

        @builtins.property
        def end(self) -> builtins.str:
            '''The specific time when quiet time ends.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html#cfn-pinpoint-campaign-schedule-quiettime-end
            '''
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def start(self) -> builtins.str:
            '''The specific time when quiet time begins.

            This value has to use 24-hour notation and be in HH:MM format, where HH is the hour (with a leading zero, if applicable) and MM is the minutes. For example, use ``02:30`` to represent 2:30 AM, or ``14:30`` to represent 2:30 PM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html#cfn-pinpoint-campaign-schedule-quiettime-start
            '''
            result = self._values.get("start")
            assert result is not None, "Required property 'start' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuietTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_time": "endTime",
            "event_filter": "eventFilter",
            "frequency": "frequency",
            "is_local_time": "isLocalTime",
            "quiet_time": "quietTime",
            "start_time": "startTime",
            "time_zone": "timeZone",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[builtins.str] = None,
            event_filter: typing.Optional[typing.Union[typing.Union["CfnCampaign.CampaignEventFilterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            frequency: typing.Optional[builtins.str] = None,
            is_local_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            quiet_time: typing.Optional[typing.Union[typing.Union["CfnCampaign.QuietTimeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            start_time: typing.Optional[builtins.str] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the schedule settings for a campaign.

            :param end_time: The scheduled time, in ISO 8601 format, when the campaign ended or will end.
            :param event_filter: The type of event that causes the campaign to be sent, if the value of the ``Frequency`` property is ``EVENT`` .
            :param frequency: Specifies how often the campaign is sent or whether the campaign is sent in response to a specific event.
            :param is_local_time: Specifies whether the start and end times for the campaign schedule use each recipient's local time. To base the schedule on each recipient's local time, set this value to ``true`` .
            :param quiet_time: The default quiet time for the campaign. Quiet time is a specific time range when a campaign doesn't send messages to endpoints, if all the following conditions are met: - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value. - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the campaign. - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the campaign. If any of the preceding conditions isn't met, the endpoint will receive messages from the campaign, even if quiet time is enabled.
            :param start_time: The scheduled time when the campaign began or will begin. Valid values are: ``IMMEDIATE`` , to start the campaign immediately; or, a specific time in ISO 8601 format.
            :param time_zone: The starting UTC offset for the campaign schedule, if the value of the ``IsLocalTime`` property is ``true`` . Valid values are: ``UTC, UTC+01, UTC+02, UTC+03, UTC+03:30, UTC+04, UTC+04:30, UTC+05, UTC+05:30, UTC+05:45, UTC+06, UTC+06:30, UTC+07, UTC+08, UTC+09, UTC+09:30, UTC+10, UTC+10:30, UTC+11, UTC+12, UTC+13, UTC-02, UTC-03, UTC-04, UTC-05, UTC-06, UTC-07, UTC-08, UTC-09, UTC-10,`` and ``UTC-11`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                
                schedule_property = pinpoint.CfnCampaign.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                        dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67a56fc7789bdbf066bcd444531c6bb3ed53397542d90500faa322a3936d6ebd)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
                check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
                check_type(argname="argument is_local_time", value=is_local_time, expected_type=type_hints["is_local_time"])
                check_type(argname="argument quiet_time", value=quiet_time, expected_type=type_hints["quiet_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if event_filter is not None:
                self._values["event_filter"] = event_filter
            if frequency is not None:
                self._values["frequency"] = frequency
            if is_local_time is not None:
                self._values["is_local_time"] = is_local_time
            if quiet_time is not None:
                self._values["quiet_time"] = quiet_time
            if start_time is not None:
                self._values["start_time"] = start_time
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def end_time(self) -> typing.Optional[builtins.str]:
            '''The scheduled time, in ISO 8601 format, when the campaign ended or will end.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_filter(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CampaignEventFilterProperty", _IResolvable_a771d0ef]]:
            '''The type of event that causes the campaign to be sent, if the value of the ``Frequency`` property is ``EVENT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-eventfilter
            '''
            result = self._values.get("event_filter")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.CampaignEventFilterProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def frequency(self) -> typing.Optional[builtins.str]:
            '''Specifies how often the campaign is sent or whether the campaign is sent in response to a specific event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-frequency
            '''
            result = self._values.get("frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_local_time(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether the start and end times for the campaign schedule use each recipient's local time.

            To base the schedule on each recipient's local time, set this value to ``true`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-islocaltime
            '''
            result = self._values.get("is_local_time")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def quiet_time(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.QuietTimeProperty", _IResolvable_a771d0ef]]:
            '''The default quiet time for the campaign.

            Quiet time is a specific time range when a campaign doesn't send messages to endpoints, if all the following conditions are met:

            - The ``EndpointDemographic.Timezone`` property of the endpoint is set to a valid value.
            - The current time in the endpoint's time zone is later than or equal to the time specified by the ``QuietTime.Start`` property for the campaign.
            - The current time in the endpoint's time zone is earlier than or equal to the time specified by the ``QuietTime.End`` property for the campaign.

            If any of the preceding conditions isn't met, the endpoint will receive messages from the campaign, even if quiet time is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-quiettime
            '''
            result = self._values.get("quiet_time")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.QuietTimeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''The scheduled time when the campaign began or will begin.

            Valid values are: ``IMMEDIATE`` , to start the campaign immediately; or, a specific time in ISO 8601 format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            '''The starting UTC offset for the campaign schedule, if the value of the ``IsLocalTime`` property is ``true`` .

            Valid values are: ``UTC, UTC+01, UTC+02, UTC+03, UTC+03:30, UTC+04, UTC+04:30, UTC+05, UTC+05:30, UTC+05:45, UTC+06, UTC+06:30, UTC+07, UTC+08, UTC+09, UTC+09:30, UTC+10, UTC+10:30, UTC+11, UTC+12, UTC+13, UTC-02, UTC-03, UTC-04, UTC-05, UTC-06, UTC-07, UTC-08, UTC-09, UTC-10,`` and ``UTC-11`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-timezone
            '''
            result = self._values.get("time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.SetDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class SetDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the dimension type and values for a segment dimension.

            :param dimension_type: The type of segment dimension to use. Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                set_dimension_property = pinpoint.CfnCampaign.SetDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d86fbae36e2fe97df4c2a1aad64dc1ac67d24e71f102e9af687b319fa5b3fb6)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use.

            Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html#cfn-pinpoint-campaign-setdimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html#cfn-pinpoint-campaign-setdimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.TemplateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email_template": "emailTemplate",
            "push_template": "pushTemplate",
            "sms_template": "smsTemplate",
            "voice_template": "voiceTemplate",
        },
    )
    class TemplateConfigurationProperty:
        def __init__(
            self,
            *,
            email_template: typing.Optional[typing.Union[typing.Union["CfnCampaign.TemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            push_template: typing.Optional[typing.Union[typing.Union["CfnCampaign.TemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sms_template: typing.Optional[typing.Union[typing.Union["CfnCampaign.TemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            voice_template: typing.Optional[typing.Union[typing.Union["CfnCampaign.TemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param email_template: ``CfnCampaign.TemplateConfigurationProperty.EmailTemplate``.
            :param push_template: ``CfnCampaign.TemplateConfigurationProperty.PushTemplate``.
            :param sms_template: ``CfnCampaign.TemplateConfigurationProperty.SMSTemplate``.
            :param voice_template: ``CfnCampaign.TemplateConfigurationProperty.VoiceTemplate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                template_configuration_property = pinpoint.CfnCampaign.TemplateConfigurationProperty(
                    email_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1cbc60e3a9a24dad439717c2092e5c1de05f9f6a98cdf2275f08cc4fc10d03e2)
                check_type(argname="argument email_template", value=email_template, expected_type=type_hints["email_template"])
                check_type(argname="argument push_template", value=push_template, expected_type=type_hints["push_template"])
                check_type(argname="argument sms_template", value=sms_template, expected_type=type_hints["sms_template"])
                check_type(argname="argument voice_template", value=voice_template, expected_type=type_hints["voice_template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_template is not None:
                self._values["email_template"] = email_template
            if push_template is not None:
                self._values["push_template"] = push_template
            if sms_template is not None:
                self._values["sms_template"] = sms_template
            if voice_template is not None:
                self._values["voice_template"] = voice_template

        @builtins.property
        def email_template(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.TemplateProperty", _IResolvable_a771d0ef]]:
            '''``CfnCampaign.TemplateConfigurationProperty.EmailTemplate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-emailtemplate
            '''
            result = self._values.get("email_template")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.TemplateProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def push_template(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.TemplateProperty", _IResolvable_a771d0ef]]:
            '''``CfnCampaign.TemplateConfigurationProperty.PushTemplate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-pushtemplate
            '''
            result = self._values.get("push_template")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.TemplateProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sms_template(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.TemplateProperty", _IResolvable_a771d0ef]]:
            '''``CfnCampaign.TemplateConfigurationProperty.SMSTemplate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-smstemplate
            '''
            result = self._values.get("sms_template")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.TemplateProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def voice_template(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.TemplateProperty", _IResolvable_a771d0ef]]:
            '''``CfnCampaign.TemplateConfigurationProperty.VoiceTemplate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-templateconfiguration.html#cfn-pinpoint-campaign-templateconfiguration-voicetemplate
            '''
            result = self._values.get("voice_template")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.TemplateProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.TemplateProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class TemplateProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: ``CfnCampaign.TemplateProperty.Name``.
            :param version: ``CfnCampaign.TemplateProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                template_property = pinpoint.CfnCampaign.TemplateProperty(
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a66f7c9150a4441f8aeccc9ff31d527733cb6659c205e1a83167ec30bfd22207)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnCampaign.TemplateProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html#cfn-pinpoint-campaign-template-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''``CfnCampaign.TemplateProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-template.html#cfn-pinpoint-campaign-template-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnCampaign.WriteTreatmentResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_delivery_configuration": "customDeliveryConfiguration",
            "message_configuration": "messageConfiguration",
            "schedule": "schedule",
            "size_percent": "sizePercent",
            "template_configuration": "templateConfiguration",
            "treatment_description": "treatmentDescription",
            "treatment_name": "treatmentName",
        },
    )
    class WriteTreatmentResourceProperty:
        def __init__(
            self,
            *,
            custom_delivery_configuration: typing.Optional[typing.Union[typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            message_configuration: typing.Optional[typing.Union[typing.Union["CfnCampaign.MessageConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            schedule: typing.Optional[typing.Union[typing.Union["CfnCampaign.ScheduleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            size_percent: typing.Optional[jsii.Number] = None,
            template_configuration: typing.Optional[typing.Union[typing.Union["CfnCampaign.TemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            treatment_description: typing.Optional[builtins.str] = None,
            treatment_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the settings for a campaign treatment.

            A *treatment* is a variation of a campaign that's used for A/B testing of a campaign.

            :param custom_delivery_configuration: ``CfnCampaign.WriteTreatmentResourceProperty.CustomDeliveryConfiguration``.
            :param message_configuration: The message configuration settings for the treatment.
            :param schedule: The schedule settings for the treatment.
            :param size_percent: The allocated percentage of users (segment members) to send the treatment to.
            :param template_configuration: ``CfnCampaign.WriteTreatmentResourceProperty.TemplateConfiguration``.
            :param treatment_description: A custom description of the treatment.
            :param treatment_name: A custom name for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # attributes: Any
                # custom_config: Any
                # metrics: Any
                
                write_treatment_resource_property = pinpoint.CfnCampaign.WriteTreatmentResourceProperty(
                    custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                        delivery_uri="deliveryUri",
                        endpoint_types=["endpointTypes"]
                    ),
                    message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                        adm_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        apns_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        baidu_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                            data="data"
                        ),
                        default_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                            body="body",
                            from_address="fromAddress",
                            html_body="htmlBody",
                            title="title"
                        ),
                        gcm_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                            content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                                background_color="backgroundColor",
                                body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                    alignment="alignment",
                                    body="body",
                                    text_color="textColor"
                                ),
                                header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                    alignment="alignment",
                                    header="header",
                                    text_color="textColor"
                                ),
                                image_url="imageUrl",
                                primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                ),
                                secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                )
                            )],
                            custom_config=custom_config,
                            layout="layout"
                        ),
                        sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                            body="body",
                            entity_id="entityId",
                            message_type="messageType",
                            origination_number="originationNumber",
                            sender_id="senderId",
                            template_id="templateId"
                        )
                    ),
                    schedule=pinpoint.CfnCampaign.ScheduleProperty(
                        end_time="endTime",
                        event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                            dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                                attributes=attributes,
                                event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                metrics=metrics
                            ),
                            filter_type="filterType"
                        ),
                        frequency="frequency",
                        is_local_time=False,
                        quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                            end="end",
                            start="start"
                        ),
                        start_time="startTime",
                        time_zone="timeZone"
                    ),
                    size_percent=123,
                    template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                        email_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        push_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        sms_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        voice_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        )
                    ),
                    treatment_description="treatmentDescription",
                    treatment_name="treatmentName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__08b80281097b61385e992001b7076f2ac2467552d16ccf164fa3ec27df87c225)
                check_type(argname="argument custom_delivery_configuration", value=custom_delivery_configuration, expected_type=type_hints["custom_delivery_configuration"])
                check_type(argname="argument message_configuration", value=message_configuration, expected_type=type_hints["message_configuration"])
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument size_percent", value=size_percent, expected_type=type_hints["size_percent"])
                check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
                check_type(argname="argument treatment_description", value=treatment_description, expected_type=type_hints["treatment_description"])
                check_type(argname="argument treatment_name", value=treatment_name, expected_type=type_hints["treatment_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_delivery_configuration is not None:
                self._values["custom_delivery_configuration"] = custom_delivery_configuration
            if message_configuration is not None:
                self._values["message_configuration"] = message_configuration
            if schedule is not None:
                self._values["schedule"] = schedule
            if size_percent is not None:
                self._values["size_percent"] = size_percent
            if template_configuration is not None:
                self._values["template_configuration"] = template_configuration
            if treatment_description is not None:
                self._values["treatment_description"] = treatment_description
            if treatment_name is not None:
                self._values["treatment_name"] = treatment_name

        @builtins.property
        def custom_delivery_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnCampaign.WriteTreatmentResourceProperty.CustomDeliveryConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-customdeliveryconfiguration
            '''
            result = self._values.get("custom_delivery_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.CustomDeliveryConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def message_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_a771d0ef]]:
            '''The message configuration settings for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-messageconfiguration
            '''
            result = self._values.get("message_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def schedule(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_a771d0ef]]:
            '''The schedule settings for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def size_percent(self) -> typing.Optional[jsii.Number]:
            '''The allocated percentage of users (segment members) to send the treatment to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-sizepercent
            '''
            result = self._values.get("size_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def template_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.TemplateConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnCampaign.WriteTreatmentResourceProperty.TemplateConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-templateconfiguration
            '''
            result = self._values.get("template_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.TemplateConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def treatment_description(self) -> typing.Optional[builtins.str]:
            '''A custom description of the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-treatmentdescription
            '''
            result = self._values.get("treatment_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def treatment_name(self) -> typing.Optional[builtins.str]:
            '''A custom name for the treatment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-treatmentname
            '''
            result = self._values.get("treatment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WriteTreatmentResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnCampaignProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "name": "name",
        "schedule": "schedule",
        "segment_id": "segmentId",
        "additional_treatments": "additionalTreatments",
        "campaign_hook": "campaignHook",
        "custom_delivery_configuration": "customDeliveryConfiguration",
        "description": "description",
        "holdout_percent": "holdoutPercent",
        "is_paused": "isPaused",
        "limits": "limits",
        "message_configuration": "messageConfiguration",
        "priority": "priority",
        "segment_version": "segmentVersion",
        "tags": "tags",
        "template_configuration": "templateConfiguration",
        "treatment_description": "treatmentDescription",
        "treatment_name": "treatmentName",
    },
)
class CfnCampaignProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        name: builtins.str,
        schedule: typing.Union[typing.Union[CfnCampaign.ScheduleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        segment_id: builtins.str,
        additional_treatments: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCampaign.WriteTreatmentResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        campaign_hook: typing.Optional[typing.Union[typing.Union[CfnCampaign.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        custom_delivery_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        holdout_percent: typing.Optional[jsii.Number] = None,
        is_paused: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        limits: typing.Optional[typing.Union[typing.Union[CfnCampaign.LimitsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        message_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        priority: typing.Optional[jsii.Number] = None,
        segment_version: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        template_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        treatment_description: typing.Optional[builtins.str] = None,
        treatment_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCampaign``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the campaign is associated with.
        :param name: The name of the campaign.
        :param schedule: The schedule settings for the campaign.
        :param segment_id: The unique identifier for the segment to associate with the campaign.
        :param additional_treatments: An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.
        :param campaign_hook: Specifies the Lambda function to use as a code hook for a campaign.
        :param custom_delivery_configuration: ``AWS::Pinpoint::Campaign.CustomDeliveryConfiguration``.
        :param description: A custom description of the campaign.
        :param holdout_percent: The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.
        :param is_paused: Specifies whether to pause the campaign. A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it. If a campaign is running it will complete and then pause. Pause only pauses or skips the next run for a recurring future scheduled campaign. A campaign scheduled for immediate can't be paused.
        :param limits: The messaging limits for the campaign.
        :param message_configuration: The message configuration settings for the campaign.
        :param priority: An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest. If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.
        :param segment_version: The version of the segment to associate with the campaign.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_configuration: ``AWS::Pinpoint::Campaign.TemplateConfiguration``.
        :param treatment_description: A custom description of the default treatment for the campaign.
        :param treatment_name: A custom name of the default treatment for the campaign, if the campaign has multiple treatments. A *treatment* is a variation of a campaign that's used for A/B testing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            # attributes: Any
            # custom_config: Any
            # metrics: Any
            # tags: Any
            
            cfn_campaign_props = pinpoint.CfnCampaignProps(
                application_id="applicationId",
                name="name",
                schedule=pinpoint.CfnCampaign.ScheduleProperty(
                    end_time="endTime",
                    event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                        dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                            attributes=attributes,
                            event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            metrics=metrics
                        ),
                        filter_type="filterType"
                    ),
                    frequency="frequency",
                    is_local_time=False,
                    quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                        end="end",
                        start="start"
                    ),
                    start_time="startTime",
                    time_zone="timeZone"
                ),
                segment_id="segmentId",
            
                # the properties below are optional
                additional_treatments=[pinpoint.CfnCampaign.WriteTreatmentResourceProperty(
                    custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                        delivery_uri="deliveryUri",
                        endpoint_types=["endpointTypes"]
                    ),
                    message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                        adm_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        apns_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        baidu_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                            data="data"
                        ),
                        default_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                            body="body",
                            from_address="fromAddress",
                            html_body="htmlBody",
                            title="title"
                        ),
                        gcm_message=pinpoint.CfnCampaign.MessageProperty(
                            action="action",
                            body="body",
                            image_icon_url="imageIconUrl",
                            image_small_icon_url="imageSmallIconUrl",
                            image_url="imageUrl",
                            json_body="jsonBody",
                            media_url="mediaUrl",
                            raw_content="rawContent",
                            silent_push=False,
                            time_to_live=123,
                            title="title",
                            url="url"
                        ),
                        in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                            content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                                background_color="backgroundColor",
                                body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                    alignment="alignment",
                                    body="body",
                                    text_color="textColor"
                                ),
                                header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                    alignment="alignment",
                                    header="header",
                                    text_color="textColor"
                                ),
                                image_url="imageUrl",
                                primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                ),
                                secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                    android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                        background_color="backgroundColor",
                                        border_radius=123,
                                        button_action="buttonAction",
                                        link="link",
                                        text="text",
                                        text_color="textColor"
                                    ),
                                    ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    ),
                                    web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                        button_action="buttonAction",
                                        link="link"
                                    )
                                )
                            )],
                            custom_config=custom_config,
                            layout="layout"
                        ),
                        sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                            body="body",
                            entity_id="entityId",
                            message_type="messageType",
                            origination_number="originationNumber",
                            sender_id="senderId",
                            template_id="templateId"
                        )
                    ),
                    schedule=pinpoint.CfnCampaign.ScheduleProperty(
                        end_time="endTime",
                        event_filter=pinpoint.CfnCampaign.CampaignEventFilterProperty(
                            dimensions=pinpoint.CfnCampaign.EventDimensionsProperty(
                                attributes=attributes,
                                event_type=pinpoint.CfnCampaign.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                metrics=metrics
                            ),
                            filter_type="filterType"
                        ),
                        frequency="frequency",
                        is_local_time=False,
                        quiet_time=pinpoint.CfnCampaign.QuietTimeProperty(
                            end="end",
                            start="start"
                        ),
                        start_time="startTime",
                        time_zone="timeZone"
                    ),
                    size_percent=123,
                    template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                        email_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        push_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        sms_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        ),
                        voice_template=pinpoint.CfnCampaign.TemplateProperty(
                            name="name",
                            version="version"
                        )
                    ),
                    treatment_description="treatmentDescription",
                    treatment_name="treatmentName"
                )],
                campaign_hook=pinpoint.CfnCampaign.CampaignHookProperty(
                    lambda_function_name="lambdaFunctionName",
                    mode="mode",
                    web_url="webUrl"
                ),
                custom_delivery_configuration=pinpoint.CfnCampaign.CustomDeliveryConfigurationProperty(
                    delivery_uri="deliveryUri",
                    endpoint_types=["endpointTypes"]
                ),
                description="description",
                holdout_percent=123,
                is_paused=False,
                limits=pinpoint.CfnCampaign.LimitsProperty(
                    daily=123,
                    maximum_duration=123,
                    messages_per_second=123,
                    session=123,
                    total=123
                ),
                message_configuration=pinpoint.CfnCampaign.MessageConfigurationProperty(
                    adm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    apns_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    baidu_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    custom_message=pinpoint.CfnCampaign.CampaignCustomMessageProperty(
                        data="data"
                    ),
                    default_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    email_message=pinpoint.CfnCampaign.CampaignEmailMessageProperty(
                        body="body",
                        from_address="fromAddress",
                        html_body="htmlBody",
                        title="title"
                    ),
                    gcm_message=pinpoint.CfnCampaign.MessageProperty(
                        action="action",
                        body="body",
                        image_icon_url="imageIconUrl",
                        image_small_icon_url="imageSmallIconUrl",
                        image_url="imageUrl",
                        json_body="jsonBody",
                        media_url="mediaUrl",
                        raw_content="rawContent",
                        silent_push=False,
                        time_to_live=123,
                        title="title",
                        url="url"
                    ),
                    in_app_message=pinpoint.CfnCampaign.CampaignInAppMessageProperty(
                        content=[pinpoint.CfnCampaign.InAppMessageContentProperty(
                            background_color="backgroundColor",
                            body_config=pinpoint.CfnCampaign.InAppMessageBodyConfigProperty(
                                alignment="alignment",
                                body="body",
                                text_color="textColor"
                            ),
                            header_config=pinpoint.CfnCampaign.InAppMessageHeaderConfigProperty(
                                alignment="alignment",
                                header="header",
                                text_color="textColor"
                            ),
                            image_url="imageUrl",
                            primary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            ),
                            secondary_btn=pinpoint.CfnCampaign.InAppMessageButtonProperty(
                                android=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                default_config=pinpoint.CfnCampaign.DefaultButtonConfigurationProperty(
                                    background_color="backgroundColor",
                                    border_radius=123,
                                    button_action="buttonAction",
                                    link="link",
                                    text="text",
                                    text_color="textColor"
                                ),
                                ios=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                ),
                                web=pinpoint.CfnCampaign.OverrideButtonConfigurationProperty(
                                    button_action="buttonAction",
                                    link="link"
                                )
                            )
                        )],
                        custom_config=custom_config,
                        layout="layout"
                    ),
                    sms_message=pinpoint.CfnCampaign.CampaignSmsMessageProperty(
                        body="body",
                        entity_id="entityId",
                        message_type="messageType",
                        origination_number="originationNumber",
                        sender_id="senderId",
                        template_id="templateId"
                    )
                ),
                priority=123,
                segment_version=123,
                tags=tags,
                template_configuration=pinpoint.CfnCampaign.TemplateConfigurationProperty(
                    email_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    push_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    sms_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    ),
                    voice_template=pinpoint.CfnCampaign.TemplateProperty(
                        name="name",
                        version="version"
                    )
                ),
                treatment_description="treatmentDescription",
                treatment_name="treatmentName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a604c4cf0736947cde446186f88845d2d3fcd92bb46dcd583e0eabba82cc572f)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument segment_id", value=segment_id, expected_type=type_hints["segment_id"])
            check_type(argname="argument additional_treatments", value=additional_treatments, expected_type=type_hints["additional_treatments"])
            check_type(argname="argument campaign_hook", value=campaign_hook, expected_type=type_hints["campaign_hook"])
            check_type(argname="argument custom_delivery_configuration", value=custom_delivery_configuration, expected_type=type_hints["custom_delivery_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument holdout_percent", value=holdout_percent, expected_type=type_hints["holdout_percent"])
            check_type(argname="argument is_paused", value=is_paused, expected_type=type_hints["is_paused"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument message_configuration", value=message_configuration, expected_type=type_hints["message_configuration"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument segment_version", value=segment_version, expected_type=type_hints["segment_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
            check_type(argname="argument treatment_description", value=treatment_description, expected_type=type_hints["treatment_description"])
            check_type(argname="argument treatment_name", value=treatment_name, expected_type=type_hints["treatment_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "name": name,
            "schedule": schedule,
            "segment_id": segment_id,
        }
        if additional_treatments is not None:
            self._values["additional_treatments"] = additional_treatments
        if campaign_hook is not None:
            self._values["campaign_hook"] = campaign_hook
        if custom_delivery_configuration is not None:
            self._values["custom_delivery_configuration"] = custom_delivery_configuration
        if description is not None:
            self._values["description"] = description
        if holdout_percent is not None:
            self._values["holdout_percent"] = holdout_percent
        if is_paused is not None:
            self._values["is_paused"] = is_paused
        if limits is not None:
            self._values["limits"] = limits
        if message_configuration is not None:
            self._values["message_configuration"] = message_configuration
        if priority is not None:
            self._values["priority"] = priority
        if segment_version is not None:
            self._values["segment_version"] = segment_version
        if tags is not None:
            self._values["tags"] = tags
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration
        if treatment_description is not None:
            self._values["treatment_description"] = treatment_description
        if treatment_name is not None:
            self._values["treatment_name"] = treatment_name

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the campaign is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[CfnCampaign.ScheduleProperty, _IResolvable_a771d0ef]:
        '''The schedule settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-schedule
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(typing.Union[CfnCampaign.ScheduleProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def segment_id(self) -> builtins.str:
        '''The unique identifier for the segment to associate with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentid
        '''
        result = self._values.get("segment_id")
        assert result is not None, "Required property 'segment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_treatments(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCampaign.WriteTreatmentResourceProperty, _IResolvable_a771d0ef]]]]:
        '''An array of requests that defines additional treatments for the campaign, in addition to the default treatment for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-additionaltreatments
        '''
        result = self._values.get("additional_treatments")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCampaign.WriteTreatmentResourceProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[CfnCampaign.CampaignHookProperty, _IResolvable_a771d0ef]]:
        '''Specifies the Lambda function to use as a code hook for a campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-campaignhook
        '''
        result = self._values.get("campaign_hook")
        return typing.cast(typing.Optional[typing.Union[CfnCampaign.CampaignHookProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def custom_delivery_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Pinpoint::Campaign.CustomDeliveryConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-customdeliveryconfiguration
        '''
        result = self._values.get("custom_delivery_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def holdout_percent(self) -> typing.Optional[jsii.Number]:
        '''The allocated percentage of users (segment members) who shouldn't receive messages from the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-holdoutpercent
        '''
        result = self._values.get("holdout_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to pause the campaign.

        A paused campaign doesn't run unless you resume it by changing this value to ``false`` . If you restart a campaign, the campaign restarts from the beginning and not at the point you paused it. If a campaign is running it will complete and then pause. Pause only pauses or skips the next run for a recurring future scheduled campaign. A campaign scheduled for immediate can't be paused.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-ispaused
        '''
        result = self._values.get("is_paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional[typing.Union[CfnCampaign.LimitsProperty, _IResolvable_a771d0ef]]:
        '''The messaging limits for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-limits
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Union[CfnCampaign.LimitsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def message_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnCampaign.MessageConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The message configuration settings for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-messageconfiguration
        '''
        result = self._values.get("message_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnCampaign.MessageConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''An integer between 1 and 5, inclusive, that represents the priority of the in-app message campaign, where 1 is the highest priority and 5 is the lowest.

        If there are multiple messages scheduled to be displayed at the same time, the priority determines the order in which those messages are displayed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def segment_version(self) -> typing.Optional[jsii.Number]:
        '''The version of the segment to associate with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentversion
        '''
        result = self._values.get("segment_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnCampaign.TemplateConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Pinpoint::Campaign.TemplateConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-templateconfiguration
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnCampaign.TemplateConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def treatment_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the default treatment for the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentdescription
        '''
        result = self._values.get("treatment_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def treatment_name(self) -> typing.Optional[builtins.str]:
        '''A custom name of the default treatment for the campaign, if the campaign has multiple treatments.

        A *treatment* is a variation of a campaign that's used for A/B testing.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentname
        '''
        result = self._values.get("treatment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCampaignProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEmailChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnEmailChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::EmailChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the email channel to send email to users. Before you can use Amazon Pinpoint to send email, you must enable the email channel for an Amazon Pinpoint application.

    The EmailChannel resource represents the status, identity, and other settings of the email channel for an application

    :cloudformationResource: AWS::Pinpoint::EmailChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_email_channel = pinpoint.CfnEmailChannel(self, "MyCfnEmailChannel",
            application_id="applicationId",
            from_address="fromAddress",
            identity="identity",
        
            # the properties below are optional
            configuration_set="configurationSet",
            enabled=False,
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        from_address: builtins.str,
        identity: builtins.str,
        configuration_set: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::EmailChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.
        :param from_address: The verified email address that you want to send email from when you send email through the channel.
        :param identity: The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.
        :param configuration_set: The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.
        :param enabled: Specifies whether to enable the email channel for the application.
        :param role_arn: The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef0d86926d29015a7352241112aeead73ce2b022b237cc772dd7a2ae18bd38c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEmailChannelProps(
            application_id=application_id,
            from_address=from_address,
            identity=identity,
            configuration_set=configuration_set,
            enabled=enabled,
            role_arn=role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb989a766331b66e6649d2c5124e542c30d53c7d32c747f107a92c6c595df12c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eee75605f28ff32d95ed0946b9c8ab06b43d7123af9f0b9bc88103600d0b800)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bfa930689b8dd7e328a261f2d7845bbbf81d1ae30595dc377c8e5e2108e3b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="fromAddress")
    def from_address(self) -> builtins.str:
        '''The verified email address that you want to send email from when you send email through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-fromaddress
        '''
        return typing.cast(builtins.str, jsii.get(self, "fromAddress"))

    @from_address.setter
    def from_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3857e2bbccc6bcaad81662819e77a5c0b2c63899283edc24aa15f8aed4b4750c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromAddress", value)

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-identity
        '''
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @identity.setter
    def identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c24bee1c19e53d401f7004d2f7a5867920f5553f2d9302b389b81543279a5289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value)

    @builtins.property
    @jsii.member(jsii_name="configurationSet")
    def configuration_set(self) -> typing.Optional[builtins.str]:
        '''The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-configurationset
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationSet"))

    @configuration_set.setter
    def configuration_set(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df420ecb7c550bd85c8508e299a1b5758f18ec30993f0d6e58526e200b4c81ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSet", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the email channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5bcdbcb464e9ab4c3ff080558d18ff517746d6be746bad3896d6809d5a8640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728b583166e75452c0eebebe8ef11628608faa63bbfcf156a28127681fe703d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnEmailChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "from_address": "fromAddress",
        "identity": "identity",
        "configuration_set": "configurationSet",
        "enabled": "enabled",
        "role_arn": "roleArn",
    },
)
class CfnEmailChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        from_address: builtins.str,
        identity: builtins.str,
        configuration_set: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEmailChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.
        :param from_address: The verified email address that you want to send email from when you send email through the channel.
        :param identity: The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.
        :param configuration_set: The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.
        :param enabled: Specifies whether to enable the email channel for the application.
        :param role_arn: The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_email_channel_props = pinpoint.CfnEmailChannelProps(
                application_id="applicationId",
                from_address="fromAddress",
                identity="identity",
            
                # the properties below are optional
                configuration_set="configurationSet",
                enabled=False,
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67dbc1410fcea3a0e159db5d3881724a5d570289c48acdb4850cc9f2481bd82)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument from_address", value=from_address, expected_type=type_hints["from_address"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument configuration_set", value=configuration_set, expected_type=type_hints["configuration_set"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "from_address": from_address,
            "identity": identity,
        }
        if configuration_set is not None:
            self._values["configuration_set"] = configuration_set
        if enabled is not None:
            self._values["enabled"] = enabled
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you're specifying the email channel for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def from_address(self) -> builtins.str:
        '''The verified email address that you want to send email from when you send email through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-fromaddress
        '''
        result = self._values.get("from_address")
        assert result is not None, "Required property 'from_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the identity, verified with Amazon Simple Email Service (Amazon SES), that you want to use when you send email through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-identity
        '''
        result = self._values.get("identity")
        assert result is not None, "Required property 'identity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_set(self) -> typing.Optional[builtins.str]:
        '''The `Amazon SES configuration set <https://docs.aws.amazon.com/ses/latest/APIReference/API_ConfigurationSet.html>`_ that you want to apply to messages that you send through the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-configurationset
        '''
        result = self._values.get("configuration_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the email channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Identity and Access Management (IAM) role that you want Amazon Pinpoint to use when it submits email-related event data for the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEmailTemplate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnEmailTemplate",
):
    '''A CloudFormation ``AWS::Pinpoint::EmailTemplate``.

    Creates a message template that you can use in messages that are sent through the email channel. A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :cloudformationResource: AWS::Pinpoint::EmailTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        # tags: Any
        
        cfn_email_template = pinpoint.CfnEmailTemplate(self, "MyCfnEmailTemplate",
            subject="subject",
            template_name="templateName",
        
            # the properties below are optional
            default_substitutions="defaultSubstitutions",
            html_part="htmlPart",
            tags=tags,
            template_description="templateDescription",
            text_part="textPart"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        subject: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        html_part: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        text_part: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::EmailTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subject: The subject line, or title, to use in email messages that are based on the message template.
        :param template_name: The name of the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param html_part: The message body, in HTML format, to use in email messages that are based on the message template. We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        :param text_part: The message body, in plain text format, to use in email messages that are based on the message template. We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d927c3809ecb0286cc5e6d528d3f64570343d6ba9b73b738355aee0b45f5e3c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEmailTemplateProps(
            subject=subject,
            template_name=template_name,
            default_substitutions=default_substitutions,
            html_part=html_part,
            tags=tags,
            template_description=template_description,
            text_part=text_part,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be23f59f6986c71eae8932e912916f3c2f9dca01b11cc5e836b4984703ed8ff3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1c6d2fa656fb31e6645d928fd15cbbc90bd8c288de17c7e5e13a78e8f1cbffc)
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
        '''The Amazon Resource Name (ARN) of the message template.

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
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        '''The subject line, or title, to use in email messages that are based on the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-subject
        '''
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2b2dd810de41c517f3ec909a7b138adcaf76ba40d16b5dd29c93d1aa35f9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatename
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a450a65be3406036009229b94484eace8f3c068b5d1099d6a23c23e3e12b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-defaultsubstitutions
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSubstitutions"))

    @default_substitutions.setter
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9107d5e87077d7c3257764776931b738c66021e83269ba203f9eef3fecc4d74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property
    @jsii.member(jsii_name="htmlPart")
    def html_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in HTML format, to use in email messages that are based on the message template.

        We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-htmlpart
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlPart"))

    @html_part.setter
    def html_part(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e06ca8dee809f3b6754574694dc4ac6d2cc2cb6e2317bc5f0132b14bff6b8e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlPart", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatedescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5675fdd1bc484c321236765d8bae32ea24df6875286ea9a4d6f14400c9922f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)

    @builtins.property
    @jsii.member(jsii_name="textPart")
    def text_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in plain text format, to use in email messages that are based on the message template.

        We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-textpart
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textPart"))

    @text_part.setter
    def text_part(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051427f2b32ea625ef33877b4c5000034f8455c9271656bc095b184968ee6759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textPart", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnEmailTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "subject": "subject",
        "template_name": "templateName",
        "default_substitutions": "defaultSubstitutions",
        "html_part": "htmlPart",
        "tags": "tags",
        "template_description": "templateDescription",
        "text_part": "textPart",
    },
)
class CfnEmailTemplateProps:
    def __init__(
        self,
        *,
        subject: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        html_part: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        text_part: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEmailTemplate``.

        :param subject: The subject line, or title, to use in email messages that are based on the message template.
        :param template_name: The name of the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param html_part: The message body, in HTML format, to use in email messages that are based on the message template. We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        :param text_part: The message body, in plain text format, to use in email messages that are based on the message template. We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            # tags: Any
            
            cfn_email_template_props = pinpoint.CfnEmailTemplateProps(
                subject="subject",
                template_name="templateName",
            
                # the properties below are optional
                default_substitutions="defaultSubstitutions",
                html_part="htmlPart",
                tags=tags,
                template_description="templateDescription",
                text_part="textPart"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865d643fd6c8b54e2c1caf3d92331d297d025bc33c2efc1b80da3e82fb9f527c)
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument html_part", value=html_part, expected_type=type_hints["html_part"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
            check_type(argname="argument text_part", value=text_part, expected_type=type_hints["text_part"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject": subject,
            "template_name": template_name,
        }
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if html_part is not None:
            self._values["html_part"] = html_part
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description
        if text_part is not None:
            self._values["text_part"] = text_part

    @builtins.property
    def subject(self) -> builtins.str:
        '''The subject line, or title, to use in email messages that are based on the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-subject
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def html_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in HTML format, to use in email messages that are based on the message template.

        We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-htmlpart
        '''
        result = self._values.get("html_part")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text_part(self) -> typing.Optional[builtins.str]:
        '''The message body, in plain text format, to use in email messages that are based on the message template.

        We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-textpart
        '''
        result = self._values.get("text_part")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEventStream(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnEventStream",
):
    '''A CloudFormation ``AWS::Pinpoint::EventStream``.

    Creates a new event stream for an application or updates the settings of an existing event stream for an application.

    :cloudformationResource: AWS::Pinpoint::EventStream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_event_stream = pinpoint.CfnEventStream(self, "MyCfnEventStream",
            application_id="applicationId",
            destination_stream_arn="destinationStreamArn",
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        destination_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::EventStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that you want to export data from.
        :param destination_stream_arn: The Amazon Resource Name (ARN) of the Amazon Kinesis data stream or Amazon Kinesis Data Firehose delivery stream that you want to publish event data to. For a Kinesis data stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name`` For a Kinesis Data Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``
        :param role_arn: The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8debffb2d6bd1384c9a45a30fd5a7e265dd2718027b92936eddf91051b1305)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEventStreamProps(
            application_id=application_id,
            destination_stream_arn=destination_stream_arn,
            role_arn=role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48bc8429903b60b948086e4ffbca6adfd48d93adcbc68b03a5bbe1acd1f0299)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dfa16da52f3264a612af98b2a6bb15334278362a34a26441f3fd1e576ed5513)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you want to export data from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef12f4b9591b522df320c027f65471f2452eccb0704bd2711f512042548b8b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="destinationStreamArn")
    def destination_stream_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Kinesis data stream or Amazon Kinesis Data Firehose delivery stream that you want to publish event data to.

        For a Kinesis data stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name``

        For a Kinesis Data Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-destinationstreamarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationStreamArn"))

    @destination_stream_arn.setter
    def destination_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35eeab46bba4556c1ea4dd98df7745d70d13c2a0e898ab2b22ab120ca105d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationStreamArn", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64661d3ed931a57188f870a3f3fce4b8ac6891342d012e56ab211d84974064f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnEventStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "destination_stream_arn": "destinationStreamArn",
        "role_arn": "roleArn",
    },
)
class CfnEventStreamProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        destination_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnEventStream``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that you want to export data from.
        :param destination_stream_arn: The Amazon Resource Name (ARN) of the Amazon Kinesis data stream or Amazon Kinesis Data Firehose delivery stream that you want to publish event data to. For a Kinesis data stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name`` For a Kinesis Data Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``
        :param role_arn: The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_event_stream_props = pinpoint.CfnEventStreamProps(
                application_id="applicationId",
                destination_stream_arn="destinationStreamArn",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cef0e4cdeda75a978529882134ae584c4ec71dfbf32a41923b239742ae4fb2)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument destination_stream_arn", value=destination_stream_arn, expected_type=type_hints["destination_stream_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "destination_stream_arn": destination_stream_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that you want to export data from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_stream_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Kinesis data stream or Amazon Kinesis Data Firehose delivery stream that you want to publish event data to.

        For a Kinesis data stream, the ARN format is: ``arn:aws:kinesis: region : account-id :stream/ stream_name``

        For a Kinesis Data Firehose delivery stream, the ARN format is: ``arn:aws:firehose: region : account-id :deliverystream/ stream_name``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-destinationstreamarn
        '''
        result = self._values.get("destination_stream_arn")
        assert result is not None, "Required property 'destination_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The AWS Identity and Access Management (IAM) role that authorizes Amazon Pinpoint to publish event data to the stream in your AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnGCMChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnGCMChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::GCMChannel``.

    A *channel* is a type of platform that you can deliver messages to. You can use the GCM channel to send push notification messages to the Firebase Cloud Messaging (FCM) service, which replaced the Google Cloud Messaging (GCM) service. Before you use Amazon Pinpoint to send notifications to FCM, you have to enable the GCM channel for an Amazon Pinpoint application.

    The GCMChannel resource represents the status and authentication settings of the GCM channel for an application.

    :cloudformationResource: AWS::Pinpoint::GCMChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_gCMChannel = pinpoint.CfnGCMChannel(self, "MyCfnGCMChannel",
            api_key="apiKey",
            application_id="applicationId",
        
            # the properties below are optional
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::GCMChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key: The Web API key, also called the *server key* , that you received from Google to communicate with Google services.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.
        :param enabled: Specifies whether to enable the GCM channel for the Amazon Pinpoint application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05f6d6de0d6c0a814a6340975dec01c58d9950fa4b9e49790fa8f55af42e6c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGCMChannelProps(
            api_key=api_key, application_id=application_id, enabled=enabled
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f6492f1ea7c853403286924b2c9104fd48d2df3a11055e583acb7ddc044487)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a76fa7ef6049936b484d0327ebcfe29e954e3421d02879361597ada73c91517c)
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
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        '''The Web API key, also called the *server key* , that you received from Google to communicate with Google services.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-apikey
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2423be58cadb8b490fd75fff2ab6aed90e157053acb52709aa287c504b3e3361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value)

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3323a9d99664b4c17ae38b4f46b013e78f1183cebedb2245d4ec4c34e19018fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the GCM channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0745ca382b80b855b20463aaa8d3b618395a7da2852f6c1acdba6a6facb1f32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnGCMChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_id": "applicationId",
        "enabled": "enabled",
    },
)
class CfnGCMChannelProps:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGCMChannel``.

        :param api_key: The Web API key, also called the *server key* , that you received from Google to communicate with Google services.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.
        :param enabled: Specifies whether to enable the GCM channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_gCMChannel_props = pinpoint.CfnGCMChannelProps(
                api_key="apiKey",
                application_id="applicationId",
            
                # the properties below are optional
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1031f7a1856e06e99539ebcb64e2d7e5756b023dd5322f57b70aa72acf6958d6)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def api_key(self) -> builtins.str:
        '''The Web API key, also called the *server key* , that you received from Google to communicate with Google services.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-apikey
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the GCM channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the GCM channel for the Amazon Pinpoint application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGCMChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnInAppTemplate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnInAppTemplate",
):
    '''A CloudFormation ``AWS::Pinpoint::InAppTemplate``.

    Creates a message template that you can use to send in-app messages. A message template is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :cloudformationResource: AWS::Pinpoint::InAppTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        # custom_config: Any
        # tags: Any
        
        cfn_in_app_template = pinpoint.CfnInAppTemplate(self, "MyCfnInAppTemplate",
            template_name="templateName",
        
            # the properties below are optional
            content=[pinpoint.CfnInAppTemplate.InAppMessageContentProperty(
                background_color="backgroundColor",
                body_config=pinpoint.CfnInAppTemplate.BodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                ),
                header_config=pinpoint.CfnInAppTemplate.HeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                ),
                image_url="imageUrl",
                primary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                    android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                ),
                secondary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                    android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            )],
            custom_config=custom_config,
            layout="layout",
            tags=tags,
            template_description="templateDescription"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        template_name: builtins.str,
        content: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnInAppTemplate.InAppMessageContentProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        custom_config: typing.Any = None,
        layout: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::InAppTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_name: The name of the in-app message template.
        :param content: An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.
        :param custom_config: Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.
        :param layout: A string that determines the appearance of the in-app message. You can specify one of the following:. - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page. - ``TOP_BANNER`` – a message that appears as a banner at the top of the page. - ``OVERLAYS`` – a message that covers entire screen. - ``MOBILE_FEED`` – a message that appears in a window in front of the page. - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page. - ``CAROUSEL`` – a scrollable layout of up to five unique messages.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: An optional description of the in-app template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a920c894d191e02e5dbfb96fef5aceb7fc0b44faf901fe7224614c812a5237f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInAppTemplateProps(
            template_name=template_name,
            content=content,
            custom_config=custom_config,
            layout=layout,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188c65c214df80c884d7de0c03e080871f7f9814658f7c6445d6b9ae34fab752)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa9787c15a6189b4832bb83585fc36036f0191bf30f841deb4775b1eee1a1bd)
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
        '''The Amazon Resource Name (ARN) of the message template.

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
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="customConfig")
    def custom_config(self) -> typing.Any:
        '''Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-customconfig
        '''
        return typing.cast(typing.Any, jsii.get(self, "customConfig"))

    @custom_config.setter
    def custom_config(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072aa5b550311ef0e00a3bafd715ee886a59a16f7b8ef83e810e9649896a5a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customConfig", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the in-app message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatename
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e679e50a42ecdec445e3393378fb8199561711f9a2c4828ea1146175d06287f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnInAppTemplate.InAppMessageContentProperty", _IResolvable_a771d0ef]]]]:
        '''An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-content
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnInAppTemplate.InAppMessageContentProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "content"))

    @content.setter
    def content(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnInAppTemplate.InAppMessageContentProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d15b7e3672ad138c5100f8711b1158cc44e008f2ceeb569ebc34e8965fa3da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="layout")
    def layout(self) -> typing.Optional[builtins.str]:
        '''A string that determines the appearance of the in-app message. You can specify one of the following:.

        - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page.
        - ``TOP_BANNER`` – a message that appears as a banner at the top of the page.
        - ``OVERLAYS`` – a message that covers entire screen.
        - ``MOBILE_FEED`` – a message that appears in a window in front of the page.
        - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page.
        - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-layout
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "layout"))

    @layout.setter
    def layout(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2ce72c0400838c6bfbb696083318ab88583d2e9bb71ebc83d47976e484406e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layout", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the in-app template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatedescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d70456dbb54a5b6e1e36e5b18e12862b3cce4a648d1021cd9fafa31bf8a86f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnInAppTemplate.BodyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "body": "body",
            "text_color": "textColor",
        },
    )
    class BodyConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of the main body text of the in-app message.

            :param alignment: The text alignment of the main body text of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param body: The main body text of the message.
            :param text_color: The color of the body text, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                body_config_property = pinpoint.CfnInAppTemplate.BodyConfigProperty(
                    alignment="alignment",
                    body="body",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7340e172398f0bfb0ed5754be3932e665788618b3211f5f93a3a33783ac11b0)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if body is not None:
                self._values["body"] = body
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the main body text of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The main body text of the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-bodyconfig.html#cfn-pinpoint-inapptemplate-bodyconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BodyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnInAppTemplate.ButtonConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "android": "android",
            "default_config": "defaultConfig",
            "ios": "ios",
            "web": "web",
        },
    )
    class ButtonConfigProperty:
        def __init__(
            self,
            *,
            android: typing.Optional[typing.Union[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            default_config: typing.Optional[typing.Union[typing.Union["CfnInAppTemplate.DefaultButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ios: typing.Optional[typing.Union[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            web: typing.Optional[typing.Union[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the behavior of buttons that appear in an in-app message template.

            :param android: Optional button configuration to use for in-app messages sent to Android devices. This button configuration overrides the default button configuration.
            :param default_config: Specifies the default behavior of a button that appears in an in-app message. You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.
            :param ios: Optional button configuration to use for in-app messages sent to iOS devices. This button configuration overrides the default button configuration.
            :param web: Optional button configuration to use for in-app messages sent to web applications. This button configuration overrides the default button configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                button_config_property = pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                    android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                        background_color="backgroundColor",
                        border_radius=123,
                        button_action="buttonAction",
                        link="link",
                        text="text",
                        text_color="textColor"
                    ),
                    ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    ),
                    web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                        button_action="buttonAction",
                        link="link"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba62f583644620b8f31cf9dd62bbac8dfd6c43a77b596cfaa430d97e242c74fe)
                check_type(argname="argument android", value=android, expected_type=type_hints["android"])
                check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
                check_type(argname="argument ios", value=ios, expected_type=type_hints["ios"])
                check_type(argname="argument web", value=web, expected_type=type_hints["web"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if android is not None:
                self._values["android"] = android
            if default_config is not None:
                self._values["default_config"] = default_config
            if ios is not None:
                self._values["ios"] = ios
            if web is not None:
                self._values["web"] = web

        @builtins.property
        def android(
            self,
        ) -> typing.Optional[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Optional button configuration to use for in-app messages sent to Android devices.

            This button configuration overrides the default button configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-android
            '''
            result = self._values.get("android")
            return typing.cast(typing.Optional[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def default_config(
            self,
        ) -> typing.Optional[typing.Union["CfnInAppTemplate.DefaultButtonConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Specifies the default behavior of a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-defaultconfig
            '''
            result = self._values.get("default_config")
            return typing.cast(typing.Optional[typing.Union["CfnInAppTemplate.DefaultButtonConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ios(
            self,
        ) -> typing.Optional[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Optional button configuration to use for in-app messages sent to iOS devices.

            This button configuration overrides the default button configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-ios
            '''
            result = self._values.get("ios")
            return typing.cast(typing.Optional[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def web(
            self,
        ) -> typing.Optional[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Optional button configuration to use for in-app messages sent to web applications.

            This button configuration overrides the default button configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-buttonconfig.html#cfn-pinpoint-inapptemplate-buttonconfig-web
            '''
            result = self._values.get("web")
            return typing.cast(typing.Optional[typing.Union["CfnInAppTemplate.OverrideButtonConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ButtonConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "border_radius": "borderRadius",
            "button_action": "buttonAction",
            "link": "link",
            "text": "text",
            "text_color": "textColor",
        },
    )
    class DefaultButtonConfigurationProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            border_radius: typing.Optional[jsii.Number] = None,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
            text: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default behavior of a button that appears in an in-app message.

            You can optionally add button configurations that specifically apply to iOS, Android, or web browser users.

            :param background_color: The background color of a button, expressed as a hex color code (such as #000000 for black).
            :param border_radius: The border radius of a button.
            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.
            :param text: The text that appears on a button in an in-app message.
            :param text_color: The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                default_button_configuration_property = pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                    background_color="backgroundColor",
                    border_radius=123,
                    button_action="buttonAction",
                    link="link",
                    text="text",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e197e02d977cff08bef51725c29a1625036b679c304f6b142e7bc6b71b6afe19)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument border_radius", value=border_radius, expected_type=type_hints["border_radius"])
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if border_radius is not None:
                self._values["border_radius"] = border_radius
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link
            if text is not None:
                self._values["text"] = text
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color of a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def border_radius(self) -> typing.Optional[jsii.Number]:
            '''The border radius of a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-borderradius
            '''
            result = self._values.get("border_radius")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text that appears on a button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the body text in a button, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-defaultbuttonconfiguration.html#cfn-pinpoint-inapptemplate-defaultbuttonconfiguration-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnInAppTemplate.HeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alignment": "alignment",
            "header": "header",
            "text_color": "textColor",
        },
    )
    class HeaderConfigProperty:
        def __init__(
            self,
            *,
            alignment: typing.Optional[builtins.str] = None,
            header: typing.Optional[builtins.str] = None,
            text_color: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration and content of the header or title text of the in-app message.

            :param alignment: The text alignment of the title of the message. Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .
            :param header: The title text of the in-app message.
            :param text_color: The color of the title text, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                header_config_property = pinpoint.CfnInAppTemplate.HeaderConfigProperty(
                    alignment="alignment",
                    header="header",
                    text_color="textColor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60db439dea2fc8b4cf4e48ecbc220760d009c0b31f494ff6538f6651c6e4d67d)
                check_type(argname="argument alignment", value=alignment, expected_type=type_hints["alignment"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alignment is not None:
                self._values["alignment"] = alignment
            if header is not None:
                self._values["header"] = header
            if text_color is not None:
                self._values["text_color"] = text_color

        @builtins.property
        def alignment(self) -> typing.Optional[builtins.str]:
            '''The text alignment of the title of the message.

            Acceptable values: ``LEFT`` , ``CENTER`` , ``RIGHT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-alignment
            '''
            result = self._values.get("alignment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header(self) -> typing.Optional[builtins.str]:
            '''The title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-header
            '''
            result = self._values.get("header")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_color(self) -> typing.Optional[builtins.str]:
            '''The color of the title text, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-headerconfig.html#cfn-pinpoint-inapptemplate-headerconfig-textcolor
            '''
            result = self._values.get("text_color")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnInAppTemplate.InAppMessageContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "background_color": "backgroundColor",
            "body_config": "bodyConfig",
            "header_config": "headerConfig",
            "image_url": "imageUrl",
            "primary_btn": "primaryBtn",
            "secondary_btn": "secondaryBtn",
        },
    )
    class InAppMessageContentProperty:
        def __init__(
            self,
            *,
            background_color: typing.Optional[builtins.str] = None,
            body_config: typing.Optional[typing.Union[typing.Union["CfnInAppTemplate.BodyConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            header_config: typing.Optional[typing.Union[typing.Union["CfnInAppTemplate.HeaderConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            image_url: typing.Optional[builtins.str] = None,
            primary_btn: typing.Optional[typing.Union[typing.Union["CfnInAppTemplate.ButtonConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            secondary_btn: typing.Optional[typing.Union[typing.Union["CfnInAppTemplate.ButtonConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the configuration of an in-app message, including its header, body, buttons, colors, and images.

            :param background_color: The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).
            :param body_config: An object that contains configuration information about the header or title text of the in-app message.
            :param header_config: An object that contains configuration information about the header or title text of the in-app message.
            :param image_url: The URL of the image that appears on an in-app message banner.
            :param primary_btn: An object that contains configuration information about the primary button in an in-app message.
            :param secondary_btn: An object that contains configuration information about the secondary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                in_app_message_content_property = pinpoint.CfnInAppTemplate.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint.CfnInAppTemplate.BodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint.CfnInAppTemplate.HeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                        android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                        android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e3d5a8decc0c9889af580ba5c7146b1e57c16c619b75b684a45409c79e9acea)
                check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
                check_type(argname="argument body_config", value=body_config, expected_type=type_hints["body_config"])
                check_type(argname="argument header_config", value=header_config, expected_type=type_hints["header_config"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument primary_btn", value=primary_btn, expected_type=type_hints["primary_btn"])
                check_type(argname="argument secondary_btn", value=secondary_btn, expected_type=type_hints["secondary_btn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if background_color is not None:
                self._values["background_color"] = background_color
            if body_config is not None:
                self._values["body_config"] = body_config
            if header_config is not None:
                self._values["header_config"] = header_config
            if image_url is not None:
                self._values["image_url"] = image_url
            if primary_btn is not None:
                self._values["primary_btn"] = primary_btn
            if secondary_btn is not None:
                self._values["secondary_btn"] = secondary_btn

        @builtins.property
        def background_color(self) -> typing.Optional[builtins.str]:
            '''The background color for an in-app message banner, expressed as a hex color code (such as #000000 for black).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-backgroundcolor
            '''
            result = self._values.get("background_color")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body_config(
            self,
        ) -> typing.Optional[typing.Union["CfnInAppTemplate.BodyConfigProperty", _IResolvable_a771d0ef]]:
            '''An object that contains configuration information about the header or title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-bodyconfig
            '''
            result = self._values.get("body_config")
            return typing.cast(typing.Optional[typing.Union["CfnInAppTemplate.BodyConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def header_config(
            self,
        ) -> typing.Optional[typing.Union["CfnInAppTemplate.HeaderConfigProperty", _IResolvable_a771d0ef]]:
            '''An object that contains configuration information about the header or title text of the in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-headerconfig
            '''
            result = self._values.get("header_config")
            return typing.cast(typing.Optional[typing.Union["CfnInAppTemplate.HeaderConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the image that appears on an in-app message banner.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_btn(
            self,
        ) -> typing.Optional[typing.Union["CfnInAppTemplate.ButtonConfigProperty", _IResolvable_a771d0ef]]:
            '''An object that contains configuration information about the primary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-primarybtn
            '''
            result = self._values.get("primary_btn")
            return typing.cast(typing.Optional[typing.Union["CfnInAppTemplate.ButtonConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def secondary_btn(
            self,
        ) -> typing.Optional[typing.Union["CfnInAppTemplate.ButtonConfigProperty", _IResolvable_a771d0ef]]:
            '''An object that contains configuration information about the secondary button in an in-app message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-inappmessagecontent.html#cfn-pinpoint-inapptemplate-inappmessagecontent-secondarybtn
            '''
            result = self._values.get("secondary_btn")
            return typing.cast(typing.Optional[typing.Union["CfnInAppTemplate.ButtonConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InAppMessageContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"button_action": "buttonAction", "link": "link"},
    )
    class OverrideButtonConfigurationProperty:
        def __init__(
            self,
            *,
            button_action: typing.Optional[builtins.str] = None,
            link: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of a button with settings that are specific to a certain device type.

            :param button_action: The action that occurs when a recipient chooses a button in an in-app message. You can specify one of the following: - ``LINK`` – A link to a web destination. - ``DEEP_LINK`` – A link to a specific page in an application. - ``CLOSE`` – Dismisses the message.
            :param link: The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                override_button_configuration_property = pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                    button_action="buttonAction",
                    link="link"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdb7a7517f1dba9324cf8e28b7c4b59d8084c34ccc2b0a98d13701b827168745)
                check_type(argname="argument button_action", value=button_action, expected_type=type_hints["button_action"])
                check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if button_action is not None:
                self._values["button_action"] = button_action
            if link is not None:
                self._values["link"] = link

        @builtins.property
        def button_action(self) -> typing.Optional[builtins.str]:
            '''The action that occurs when a recipient chooses a button in an in-app message.

            You can specify one of the following:

            - ``LINK`` – A link to a web destination.
            - ``DEEP_LINK`` – A link to a specific page in an application.
            - ``CLOSE`` – Dismisses the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html#cfn-pinpoint-inapptemplate-overridebuttonconfiguration-buttonaction
            '''
            result = self._values.get("button_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def link(self) -> typing.Optional[builtins.str]:
            '''The destination (such as a URL) for a button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-inapptemplate-overridebuttonconfiguration.html#cfn-pinpoint-inapptemplate-overridebuttonconfiguration-link
            '''
            result = self._values.get("link")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideButtonConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnInAppTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_name": "templateName",
        "content": "content",
        "custom_config": "customConfig",
        "layout": "layout",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnInAppTemplateProps:
    def __init__(
        self,
        *,
        template_name: builtins.str,
        content: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnInAppTemplate.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        custom_config: typing.Any = None,
        layout: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnInAppTemplate``.

        :param template_name: The name of the in-app message template.
        :param content: An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.
        :param custom_config: Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.
        :param layout: A string that determines the appearance of the in-app message. You can specify one of the following:. - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page. - ``TOP_BANNER`` – a message that appears as a banner at the top of the page. - ``OVERLAYS`` – a message that covers entire screen. - ``MOBILE_FEED`` – a message that appears in a window in front of the page. - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page. - ``CAROUSEL`` – a scrollable layout of up to five unique messages.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: An optional description of the in-app template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            # custom_config: Any
            # tags: Any
            
            cfn_in_app_template_props = pinpoint.CfnInAppTemplateProps(
                template_name="templateName",
            
                # the properties below are optional
                content=[pinpoint.CfnInAppTemplate.InAppMessageContentProperty(
                    background_color="backgroundColor",
                    body_config=pinpoint.CfnInAppTemplate.BodyConfigProperty(
                        alignment="alignment",
                        body="body",
                        text_color="textColor"
                    ),
                    header_config=pinpoint.CfnInAppTemplate.HeaderConfigProperty(
                        alignment="alignment",
                        header="header",
                        text_color="textColor"
                    ),
                    image_url="imageUrl",
                    primary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                        android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    ),
                    secondary_btn=pinpoint.CfnInAppTemplate.ButtonConfigProperty(
                        android=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        default_config=pinpoint.CfnInAppTemplate.DefaultButtonConfigurationProperty(
                            background_color="backgroundColor",
                            border_radius=123,
                            button_action="buttonAction",
                            link="link",
                            text="text",
                            text_color="textColor"
                        ),
                        ios=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        ),
                        web=pinpoint.CfnInAppTemplate.OverrideButtonConfigurationProperty(
                            button_action="buttonAction",
                            link="link"
                        )
                    )
                )],
                custom_config=custom_config,
                layout="layout",
                tags=tags,
                template_description="templateDescription"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c009849a19465c26fafbcfc4baf6a9150b53545d9aaf0326df66c6acbf5e0107)
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
            check_type(argname="argument layout", value=layout, expected_type=type_hints["layout"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_name": template_name,
        }
        if content is not None:
            self._values["content"] = content
        if custom_config is not None:
            self._values["custom_config"] = custom_config
        if layout is not None:
            self._values["layout"] = layout
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the in-app message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnInAppTemplate.InAppMessageContentProperty, _IResolvable_a771d0ef]]]]:
        '''An object that contains information about the content of an in-app message, including its title and body text, text colors, background colors, images, buttons, and behaviors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnInAppTemplate.InAppMessageContentProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def custom_config(self) -> typing.Any:
        '''Custom data, in the form of key-value pairs, that is included in an in-app messaging payload.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-customconfig
        '''
        result = self._values.get("custom_config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def layout(self) -> typing.Optional[builtins.str]:
        '''A string that determines the appearance of the in-app message. You can specify one of the following:.

        - ``BOTTOM_BANNER`` – a message that appears as a banner at the bottom of the page.
        - ``TOP_BANNER`` – a message that appears as a banner at the top of the page.
        - ``OVERLAYS`` – a message that covers entire screen.
        - ``MOBILE_FEED`` – a message that appears in a window in front of the page.
        - ``MIDDLE_BANNER`` – a message that appears as a banner in the middle of the page.
        - ``CAROUSEL`` – a scrollable layout of up to five unique messages.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-layout
        '''
        result = self._values.get("layout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the in-app template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-inapptemplate.html#cfn-pinpoint-inapptemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInAppTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPushTemplate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnPushTemplate",
):
    '''A CloudFormation ``AWS::Pinpoint::PushTemplate``.

    Creates a message template that you can use in messages that are sent through a push notification channel. A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :cloudformationResource: AWS::Pinpoint::PushTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        # tags: Any
        
        cfn_push_template = pinpoint.CfnPushTemplate(self, "MyCfnPushTemplate",
            template_name="templateName",
        
            # the properties below are optional
            adm=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            apns=pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty(
                action="action",
                body="body",
                media_url="mediaUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            baidu=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            default=pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty(
                action="action",
                body="body",
                sound="sound",
                title="title",
                url="url"
            ),
            default_substitutions="defaultSubstitutions",
            gcm=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                action="action",
                body="body",
                image_icon_url="imageIconUrl",
                image_url="imageUrl",
                small_image_icon_url="smallImageIconUrl",
                sound="sound",
                title="title",
                url="url"
            ),
            tags=tags,
            template_description="templateDescription"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        template_name: builtins.str,
        adm: typing.Optional[typing.Union[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        apns: typing.Optional[typing.Union[typing.Union["CfnPushTemplate.APNSPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        baidu: typing.Optional[typing.Union[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        default: typing.Optional[typing.Union[typing.Union["CfnPushTemplate.DefaultPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        default_substitutions: typing.Optional[builtins.str] = None,
        gcm: typing.Optional[typing.Union[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::PushTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_name: The name of the message template.
        :param adm: The message template to use for the ADM (Amazon Device Messaging) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param apns: The message template to use for the APNs (Apple Push Notification service) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param baidu: The message template to use for the Baidu (Baidu Cloud Push) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param default: The default message template to use for push notification channels.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param gcm: The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd4fef242126a42b9fe6c869157300b9e2aa1e4c199d61fd5e9474849d6a727)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPushTemplateProps(
            template_name=template_name,
            adm=adm,
            apns=apns,
            baidu=baidu,
            default=default,
            default_substitutions=default_substitutions,
            gcm=gcm,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633ce22ae7e21b165aa3419db7a690755fa372bf2600e85b1052122b8a5ce2aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a030cc85a82ee4031e9a9219f81a37a4c656a52fe494015f6b94c7a6f3ecf337)
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
        '''The Amazon Resource Name (ARN) of the message template.

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
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatename
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0258b3e52265b23cc0c89ead15c3b6b674ee420767dcf757cac43ed753f79fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="adm")
    def adm(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]]:
        '''The message template to use for the ADM (Amazon Device Messaging) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-adm
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]], jsii.get(self, "adm"))

    @adm.setter
    def adm(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de826fd231f9bef42aaa84602f1b74be960dfb4c435bd41737184374bc7644d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adm", value)

    @builtins.property
    @jsii.member(jsii_name="apns")
    def apns(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.APNSPushNotificationTemplateProperty", _IResolvable_a771d0ef]]:
        '''The message template to use for the APNs (Apple Push Notification service) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-apns
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPushTemplate.APNSPushNotificationTemplateProperty", _IResolvable_a771d0ef]], jsii.get(self, "apns"))

    @apns.setter
    def apns(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.APNSPushNotificationTemplateProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68e746276a6cc1cf4e10b2534cdb1607053d2f28df8c963bdf960ad1c1a6b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apns", value)

    @builtins.property
    @jsii.member(jsii_name="baidu")
    def baidu(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]]:
        '''The message template to use for the Baidu (Baidu Cloud Push) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-baidu
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]], jsii.get(self, "baidu"))

    @baidu.setter
    def baidu(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f38bfc8d3ade04d0d866138a38b1dbb97f92dbf65cd14926366ec30efdec46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baidu", value)

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.DefaultPushNotificationTemplateProperty", _IResolvable_a771d0ef]]:
        '''The default message template to use for push notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-default
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPushTemplate.DefaultPushNotificationTemplateProperty", _IResolvable_a771d0ef]], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.DefaultPushNotificationTemplateProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4ae0e88118d6077b8353b256fe5ef9c7e291d9d66b7e88796f8953ab5698c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-defaultsubstitutions
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSubstitutions"))

    @default_substitutions.setter
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ad9e9436cb6d6de0604e08725dd1902af6cb032f8eab8bc2bfd549feb9efa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property
    @jsii.member(jsii_name="gcm")
    def gcm(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]]:
        '''The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-gcm
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]], jsii.get(self, "gcm"))

    @gcm.setter
    def gcm(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1642a056562aa094bcfb1b07e7f1627a432465dc3df6658d77c332f8bb30d617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcm", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatedescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe94b1bb9a3a97e0163b917f62ad062fb0d71460d0ab66e4fe06165106cd87ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "media_url": "mediaUrl",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class APNSPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            media_url: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies channel-specific content and settings for a message template that can be used in push notifications that are sent through the APNs (Apple Push Notification service) channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS platform. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in push notifications that are based on the message template.
            :param media_url: The URL of an image or video to display in push notifications that are based on the message template.
            :param sound: The key for the sound to play when the recipient receives a push notification that's based on the message template. The value for this key is the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.
            :param title: The title to use in push notifications that are based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in the recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                a_pNSPush_notification_template_property = pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    media_url="mediaUrl",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3e7da002b17d97eb8987d5d955593a0c645394bdbd9fe68855c640f9fff787c)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument media_url", value=media_url, expected_type=type_hints["media_url"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if media_url is not None:
                self._values["media_url"] = media_url
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS platform.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in push notifications that are based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def media_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image or video to display in push notifications that are based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-mediaurl
            '''
            result = self._values.get("media_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The key for the sound to play when the recipient receives a push notification that's based on the message template.

            The value for this key is the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in push notifications that are based on the message template.

            This title appears above the notification message on a recipient's device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in the recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "APNSPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "image_icon_url": "imageIconUrl",
            "image_url": "imageUrl",
            "small_image_icon_url": "smallImageIconUrl",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class AndroidPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            image_icon_url: typing.Optional[builtins.str] = None,
            image_url: typing.Optional[builtins.str] = None,
            small_image_icon_url: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies channel-specific content and settings for a message template that can be used in push notifications that are sent through the ADM (Amazon Device Messaging), Baidu (Baidu Cloud Push), or GCM (Firebase Cloud Messaging, formerly Google Cloud Messaging) channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This action uses the deep-linking features of the Android platform. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in a push notification that's based on the message template.
            :param image_icon_url: The URL of the large icon image to display in the content view of a push notification that's based on the message template.
            :param image_url: The URL of an image to display in a push notification that's based on the message template.
            :param small_image_icon_url: The URL of the small icon image to display in the status bar and the content view of a push notification that's based on the message template.
            :param sound: The sound to play when a recipient receives a push notification that's based on the message template. You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .
            :param title: The title to use in a push notification that's based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                android_push_notification_template_property = pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b3830fe4192f1362ed1cf072350261e04659ed0f688f5f92a5421a332486283)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument image_icon_url", value=image_icon_url, expected_type=type_hints["image_icon_url"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument small_image_icon_url", value=small_image_icon_url, expected_type=type_hints["small_image_icon_url"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if image_icon_url is not None:
                self._values["image_icon_url"] = image_icon_url
            if image_url is not None:
                self._values["image_url"] = image_url
            if small_image_icon_url is not None:
                self._values["small_image_icon_url"] = small_image_icon_url
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This action uses the deep-linking features of the Android platform.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in a push notification that's based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the large icon image to display in the content view of a push notification that's based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-imageiconurl
            '''
            result = self._values.get("image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image to display in a push notification that's based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def small_image_icon_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the small icon image to display in the status bar and the content view of a push notification that's based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-smallimageiconurl
            '''
            result = self._values.get("small_image_icon_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The sound to play when a recipient receives a push notification that's based on the message template.

            You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in a push notification that's based on the message template.

            This title appears above the notification message on a recipient's device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndroidPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class DefaultPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the default settings and content for a message template that can be used in messages that are sent through a push notification channel.

            :param action: The action to occur if a recipient taps a push notification that's based on the message template. Valid values are: - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action. - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS and Android platforms. - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.
            :param body: The message body to use in push notifications that are based on the message template.
            :param sound: The sound to play when a recipient receives a push notification that's based on the message template. You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` . For an iOS platform, this value is the key for the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.
            :param title: The title to use in push notifications that are based on the message template. This title appears above the notification message on a recipient's device.
            :param url: The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                default_push_notification_template_property = pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    sound="sound",
                    title="title",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afe3af211338f4c0d577e4bce165c38643746ba33f83e83068c7d344b9cc2646)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument sound", value=sound, expected_type=type_hints["sound"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to occur if a recipient taps a push notification that's based on the message template.

            Valid values are:

            - ``OPEN_APP`` – Your app opens or it becomes the foreground app if it was sent to the background. This is the default action.
            - ``DEEP_LINK`` – Your app opens and displays a designated user interface in the app. This setting uses the deep-linking features of the iOS and Android platforms.
            - ``URL`` – The default mobile browser on the recipient's device opens and loads the web page at a URL that you specify.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            '''The message body to use in push notifications that are based on the message template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            '''The sound to play when a recipient receives a push notification that's based on the message template.

            You can use the default stream or specify the file name of a sound resource that's bundled in your app. On an Android platform, the sound file must reside in ``/res/raw/`` .

            For an iOS platform, this value is the key for the name of a sound file in your app's main bundle or the ``Library/Sounds`` folder in your app's data container. If the sound file can't be found or you specify ``default`` for the value, the system plays the default alert sound.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-sound
            '''
            result = self._values.get("sound")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title to use in push notifications that are based on the message template.

            This title appears above the notification message on a recipient's device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to open in a recipient's default mobile browser, if a recipient taps a push notification that's based on the message template and the value of the ``Action`` property is ``URL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnPushTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_name": "templateName",
        "adm": "adm",
        "apns": "apns",
        "baidu": "baidu",
        "default": "default",
        "default_substitutions": "defaultSubstitutions",
        "gcm": "gcm",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnPushTemplateProps:
    def __init__(
        self,
        *,
        template_name: builtins.str,
        adm: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        apns: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        baidu: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        default: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        default_substitutions: typing.Optional[builtins.str] = None,
        gcm: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPushTemplate``.

        :param template_name: The name of the message template.
        :param adm: The message template to use for the ADM (Amazon Device Messaging) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param apns: The message template to use for the APNs (Apple Push Notification service) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param baidu: The message template to use for the Baidu (Baidu Cloud Push) channel. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param default: The default message template to use for push notification channels.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param gcm: The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service. This message template overrides the default template for push notification channels ( ``Default`` ).
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            # tags: Any
            
            cfn_push_template_props = pinpoint.CfnPushTemplateProps(
                template_name="templateName",
            
                # the properties below are optional
                adm=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                apns=pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    media_url="mediaUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                baidu=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                default=pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                default_substitutions="defaultSubstitutions",
                gcm=pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty(
                    action="action",
                    body="body",
                    image_icon_url="imageIconUrl",
                    image_url="imageUrl",
                    small_image_icon_url="smallImageIconUrl",
                    sound="sound",
                    title="title",
                    url="url"
                ),
                tags=tags,
                template_description="templateDescription"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db889fa25c129c979bd7e8e7dac80f6a38444b1d7956aff339f58dc6ad5452e0)
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument adm", value=adm, expected_type=type_hints["adm"])
            check_type(argname="argument apns", value=apns, expected_type=type_hints["apns"])
            check_type(argname="argument baidu", value=baidu, expected_type=type_hints["baidu"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument gcm", value=gcm, expected_type=type_hints["gcm"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_name": template_name,
        }
        if adm is not None:
            self._values["adm"] = adm
        if apns is not None:
            self._values["apns"] = apns
        if baidu is not None:
            self._values["baidu"] = baidu
        if default is not None:
            self._values["default"] = default
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if gcm is not None:
            self._values["gcm"] = gcm
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def adm(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]]:
        '''The message template to use for the ADM (Amazon Device Messaging) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-adm
        '''
        result = self._values.get("adm")
        return typing.cast(typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def apns(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, _IResolvable_a771d0ef]]:
        '''The message template to use for the APNs (Apple Push Notification service) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-apns
        '''
        result = self._values.get("apns")
        return typing.cast(typing.Optional[typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def baidu(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]]:
        '''The message template to use for the Baidu (Baidu Cloud Push) channel.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-baidu
        '''
        result = self._values.get("baidu")
        return typing.cast(typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, _IResolvable_a771d0ef]]:
        '''The default message template to use for push notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-default
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcm(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]]:
        '''The message template to use for the GCM channel, which is used to send notifications through the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging (GCM), service.

        This message template overrides the default template for push notification channels ( ``Default`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-gcm
        '''
        result = self._values.get("gcm")
        return typing.cast(typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPushTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSMSChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnSMSChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::SMSChannel``.

    A *channel* is a type of platform that you can deliver messages to. To send an SMS text message, you send the message through the SMS channel. Before you can use Amazon Pinpoint to send text messages, you have to enable the SMS channel for an Amazon Pinpoint application.

    The SMSChannel resource represents the status, sender ID, and other settings for the SMS channel for an application.

    :cloudformationResource: AWS::Pinpoint::SMSChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_sMSChannel = pinpoint.CfnSMSChannel(self, "MyCfnSMSChannel",
            application_id="applicationId",
        
            # the properties below are optional
            enabled=False,
            sender_id="senderId",
            short_code="shortCode"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        sender_id: typing.Optional[builtins.str] = None,
        short_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::SMSChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.
        :param enabled: Specifies whether to enable the SMS channel for the application.
        :param sender_id: The identity that you want to display on recipients' devices when they receive messages from the SMS channel. .. epigraph:: SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .
        :param short_code: The registered short code that you want to use when you send messages through the SMS channel. .. epigraph:: For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d487251e1ac55a04cb5ea65d246f0edcd320071cf0f1bdcf5a9a1cf7c31f1ff1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSMSChannelProps(
            application_id=application_id,
            enabled=enabled,
            sender_id=sender_id,
            short_code=short_code,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88e2e378d97b0f4681f5be0430bf0688db3f900d70056f784d9ee832493b08d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1c7e0ff3cae011bb73273d1b2cc93439a54501324279adf021647ae35b80424)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f188f164ae430b507be299859ed37a2defbf6bab722910ccd954d0f55ffc796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the SMS channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5df304b553f9e99fa74368a6eb241e0ad2b9b069031873c024f557f742900d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="senderId")
    def sender_id(self) -> typing.Optional[builtins.str]:
        '''The identity that you want to display on recipients' devices when they receive messages from the SMS channel.

        .. epigraph::

           SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-senderid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "senderId"))

    @sender_id.setter
    def sender_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5adab4b33ebc72e33ee3155131a373ec7fbb90f2e837aa335a164e2dfd0662c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "senderId", value)

    @builtins.property
    @jsii.member(jsii_name="shortCode")
    def short_code(self) -> typing.Optional[builtins.str]:
        '''The registered short code that you want to use when you send messages through the SMS channel.

        .. epigraph::

           For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-shortcode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shortCode"))

    @short_code.setter
    def short_code(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ba9b036e8129c3f9e9126505af325277f05113b9f0654b2d10db691ca84cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shortCode", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnSMSChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "enabled": "enabled",
        "sender_id": "senderId",
        "short_code": "shortCode",
    },
)
class CfnSMSChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        sender_id: typing.Optional[builtins.str] = None,
        short_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSMSChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.
        :param enabled: Specifies whether to enable the SMS channel for the application.
        :param sender_id: The identity that you want to display on recipients' devices when they receive messages from the SMS channel. .. epigraph:: SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .
        :param short_code: The registered short code that you want to use when you send messages through the SMS channel. .. epigraph:: For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_sMSChannel_props = pinpoint.CfnSMSChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                enabled=False,
                sender_id="senderId",
                short_code="shortCode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4329592acdcf99ca422d7135ad225b92b873191bc12c1fb25e7b4a89d6d55938)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument sender_id", value=sender_id, expected_type=type_hints["sender_id"])
            check_type(argname="argument short_code", value=short_code, expected_type=type_hints["short_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if sender_id is not None:
            self._values["sender_id"] = sender_id
        if short_code is not None:
            self._values["short_code"] = short_code

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the SMS channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the SMS channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def sender_id(self) -> typing.Optional[builtins.str]:
        '''The identity that you want to display on recipients' devices when they receive messages from the SMS channel.

        .. epigraph::

           SenderIDs are only supported in certain countries and regions. For more information, see `Supported Countries and Regions <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-senderid
        '''
        result = self._values.get("sender_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def short_code(self) -> typing.Optional[builtins.str]:
        '''The registered short code that you want to use when you send messages through the SMS channel.

        .. epigraph::

           For information about obtaining a dedicated short code for sending SMS messages, see `Requesting Dedicated Short Codes for SMS Messaging with Amazon Pinpoint <https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-awssupport-short-code.html>`_ in the *Amazon Pinpoint User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-shortcode
        '''
        result = self._values.get("short_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSMSChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSegment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnSegment",
):
    '''A CloudFormation ``AWS::Pinpoint::Segment``.

    Updates the configuration, dimension, and other settings for an existing segment.

    :cloudformationResource: AWS::Pinpoint::Segment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        # attributes: Any
        # metrics: Any
        # tags: Any
        # user_attributes: Any
        
        cfn_segment = pinpoint.CfnSegment(self, "MyCfnSegment",
            application_id="applicationId",
            name="name",
        
            # the properties below are optional
            dimensions=pinpoint.CfnSegment.SegmentDimensionsProperty(
                attributes=attributes,
                behavior=pinpoint.CfnSegment.BehaviorProperty(
                    recency=pinpoint.CfnSegment.RecencyProperty(
                        duration="duration",
                        recency_type="recencyType"
                    )
                ),
                demographic=pinpoint.CfnSegment.DemographicProperty(
                    app_version=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    channel=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    device_type=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    make=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    model=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    platform=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    )
                ),
                location=pinpoint.CfnSegment.LocationProperty(
                    country=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    gps_point=pinpoint.CfnSegment.GPSPointProperty(
                        coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                            latitude=123,
                            longitude=123
                        ),
                        range_in_kilometers=123
                    )
                ),
                metrics=metrics,
                user_attributes=user_attributes
            ),
            segment_groups=pinpoint.CfnSegment.SegmentGroupsProperty(
                groups=[pinpoint.CfnSegment.GroupsProperty(
                    dimensions=[pinpoint.CfnSegment.SegmentDimensionsProperty(
                        attributes=attributes,
                        behavior=pinpoint.CfnSegment.BehaviorProperty(
                            recency=pinpoint.CfnSegment.RecencyProperty(
                                duration="duration",
                                recency_type="recencyType"
                            )
                        ),
                        demographic=pinpoint.CfnSegment.DemographicProperty(
                            app_version=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            channel=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            device_type=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            make=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            model=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            platform=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        location=pinpoint.CfnSegment.LocationProperty(
                            country=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            gps_point=pinpoint.CfnSegment.GPSPointProperty(
                                coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                    latitude=123,
                                    longitude=123
                                ),
                                range_in_kilometers=123
                            )
                        ),
                        metrics=metrics,
                        user_attributes=user_attributes
                    )],
                    source_segments=[pinpoint.CfnSegment.SourceSegmentsProperty(
                        id="id",
        
                        # the properties below are optional
                        version=123
                    )],
                    source_type="sourceType",
                    type="type"
                )],
                include="include"
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        name: builtins.str,
        dimensions: typing.Optional[typing.Union[typing.Union["CfnSegment.SegmentDimensionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        segment_groups: typing.Optional[typing.Union[typing.Union["CfnSegment.SegmentGroupsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::Segment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the segment is associated with.
        :param name: The name of the segment. .. epigraph:: A segment must have a name otherwise it will not appear in the Amazon Pinpoint console.
        :param dimensions: The criteria that define the dimensions for the segment.
        :param segment_groups: The segment group to use and the dimensions to apply to the group's base segments in order to build the segment. A segment group can consist of zero or more base segments. Your request can include only one segment group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383e1befb95a42f70c11e76294d8d1a3d180c2cde8a017d9cd4dbafb48b5abc4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSegmentProps(
            application_id=application_id,
            name=name,
            dimensions=dimensions,
            segment_groups=segment_groups,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8ac3b6e0dd7a7be7fa4875b5d4094820364149511c8ec52e6dfb56003119d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f755029b91d754ffe1b8c98799e09e07ef9e5b31f7bc7917754513a0a731c96)
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
        '''The Amazon Resource Name (ARN) of the segment.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSegmentId")
    def attr_segment_id(self) -> builtins.str:
        '''The unique identifier for the segment.

        :cloudformationAttribute: SegmentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSegmentId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the segment is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea51ffe33eb489a2ac8d2e53a2832b7ef24b454b71d17a04b7f202f53ea12760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the segment.

        .. epigraph::

           A segment must have a name otherwise it will not appear in the Amazon Pinpoint console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecc64de0b23f28c35e823b36a05afa257d42ece094e55d2fe2699ab5a5de4e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_a771d0ef]]:
        '''The criteria that define the dimensions for the segment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-dimensions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "dimensions"))

    @dimensions.setter
    def dimensions(
        self,
        value: typing.Optional[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd538cedf4413425234faff50415946e5e681a668329a9d3c19e4e14d70556fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensions", value)

    @builtins.property
    @jsii.member(jsii_name="segmentGroups")
    def segment_groups(
        self,
    ) -> typing.Optional[typing.Union["CfnSegment.SegmentGroupsProperty", _IResolvable_a771d0ef]]:
        '''The segment group to use and the dimensions to apply to the group's base segments in order to build the segment.

        A segment group can consist of zero or more base segments. Your request can include only one segment group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-segmentgroups
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSegment.SegmentGroupsProperty", _IResolvable_a771d0ef]], jsii.get(self, "segmentGroups"))

    @segment_groups.setter
    def segment_groups(
        self,
        value: typing.Optional[typing.Union["CfnSegment.SegmentGroupsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1244ecc8feea9b3ad63602f4b31fed1f3055167f33b5be026ce88e337601f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentGroups", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.AttributeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_type": "attributeType", "values": "values"},
    )
    class AttributeDimensionProperty:
        def __init__(
            self,
            *,
            attribute_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies attribute-based criteria for including or excluding endpoints from a segment.

            :param attribute_type: The type of segment dimension to use. Valid values are:. - ``INCLUSIVE`` – endpoints that have attributes matching the values are included in the segment. - ``EXCLUSIVE`` – endpoints that have attributes matching the values are excluded from the segment. - ``CONTAINS`` – endpoints that have attributes' substrings match the values are included in the segment. - ``BEFORE`` – endpoints with attributes read as ISO_INSTANT datetimes before the value are included in the segment. - ``AFTER`` – endpoints with attributes read as ISO_INSTANT datetimes after the value are included in the segment. - ``BETWEEN`` – endpoints with attributes read as ISO_INSTANT datetimes between the values are included in the segment. - ``ON`` – endpoints with attributes read as ISO_INSTANT dates on the value are included in the segment. Time is ignored in this comparison.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``AttributeType`` property, endpoints are included or excluded from the segment if their attribute values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                attribute_dimension_property = pinpoint.CfnSegment.AttributeDimensionProperty(
                    attribute_type="attributeType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__20c89a4a2983a94e9ecabf61b05791e025372aad054b18c5d95f665a17e893ac)
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use. Valid values are:.

            - ``INCLUSIVE`` – endpoints that have attributes matching the values are included in the segment.
            - ``EXCLUSIVE`` – endpoints that have attributes matching the values are excluded from the segment.
            - ``CONTAINS`` – endpoints that have attributes' substrings match the values are included in the segment.
            - ``BEFORE`` – endpoints with attributes read as ISO_INSTANT datetimes before the value are included in the segment.
            - ``AFTER`` – endpoints with attributes read as ISO_INSTANT datetimes after the value are included in the segment.
            - ``BETWEEN`` – endpoints with attributes read as ISO_INSTANT datetimes between the values are included in the segment.
            - ``ON`` – endpoints with attributes read as ISO_INSTANT dates on the value are included in the segment. Time is ignored in this comparison.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html#cfn-pinpoint-segment-attributedimension-attributetype
            '''
            result = self._values.get("attribute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``AttributeType`` property, endpoints are included or excluded from the segment if their attribute values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html#cfn-pinpoint-segment-attributedimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.BehaviorProperty",
        jsii_struct_bases=[],
        name_mapping={"recency": "recency"},
    )
    class BehaviorProperty:
        def __init__(
            self,
            *,
            recency: typing.Optional[typing.Union[typing.Union["CfnSegment.RecencyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies behavior-based criteria for the segment, such as how recently users have used your app.

            :param recency: Specifies how recently segment members were active.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                behavior_property = pinpoint.CfnSegment.BehaviorProperty(
                    recency=pinpoint.CfnSegment.RecencyProperty(
                        duration="duration",
                        recency_type="recencyType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8e810d7fdfa951d02e549f378952452bdf72ac02c30f858286e7a1e00c132e3)
                check_type(argname="argument recency", value=recency, expected_type=type_hints["recency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recency is not None:
                self._values["recency"] = recency

        @builtins.property
        def recency(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.RecencyProperty", _IResolvable_a771d0ef]]:
            '''Specifies how recently segment members were active.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency
            '''
            result = self._values.get("recency")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.RecencyProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BehaviorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.CoordinatesProperty",
        jsii_struct_bases=[],
        name_mapping={"latitude": "latitude", "longitude": "longitude"},
    )
    class CoordinatesProperty:
        def __init__(self, *, latitude: jsii.Number, longitude: jsii.Number) -> None:
            '''Specifies the GPS coordinates of a location.

            :param latitude: The latitude coordinate of the location.
            :param longitude: The longitude coordinate of the location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                coordinates_property = pinpoint.CfnSegment.CoordinatesProperty(
                    latitude=123,
                    longitude=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86b8710b3fa3d7a5040619113ca59b15061fec700ace9560cd475b96d775dfa0)
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "latitude": latitude,
                "longitude": longitude,
            }

        @builtins.property
        def latitude(self) -> jsii.Number:
            '''The latitude coordinate of the location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates-latitude
            '''
            result = self._values.get("latitude")
            assert result is not None, "Required property 'latitude' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def longitude(self) -> jsii.Number:
            '''The longitude coordinate of the location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates-longitude
            '''
            result = self._values.get("longitude")
            assert result is not None, "Required property 'longitude' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoordinatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.DemographicProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_version": "appVersion",
            "channel": "channel",
            "device_type": "deviceType",
            "make": "make",
            "model": "model",
            "platform": "platform",
        },
    )
    class DemographicProperty:
        def __init__(
            self,
            *,
            app_version: typing.Optional[typing.Union[typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            channel: typing.Optional[typing.Union[typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            device_type: typing.Optional[typing.Union[typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            make: typing.Optional[typing.Union[typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            model: typing.Optional[typing.Union[typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            platform: typing.Optional[typing.Union[typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies demographic-based criteria, such as device platform, for the segment.

            :param app_version: The app version criteria for the segment.
            :param channel: The channel criteria for the segment.
            :param device_type: The device type criteria for the segment.
            :param make: The device make criteria for the segment.
            :param model: The device model criteria for the segment.
            :param platform: The device platform criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                demographic_property = pinpoint.CfnSegment.DemographicProperty(
                    app_version=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    channel=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    device_type=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    make=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    model=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    platform=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3996b2c2cfdfb4574916456a600b06ecb259779c5bc94b0f65dea399cec83c05)
                check_type(argname="argument app_version", value=app_version, expected_type=type_hints["app_version"])
                check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
                check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
                check_type(argname="argument make", value=make, expected_type=type_hints["make"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_version is not None:
                self._values["app_version"] = app_version
            if channel is not None:
                self._values["channel"] = channel
            if device_type is not None:
                self._values["device_type"] = device_type
            if make is not None:
                self._values["make"] = make
            if model is not None:
                self._values["model"] = model
            if platform is not None:
                self._values["platform"] = platform

        @builtins.property
        def app_version(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]]:
            '''The app version criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-appversion
            '''
            result = self._values.get("app_version")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def channel(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]]:
            '''The channel criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-channel
            '''
            result = self._values.get("channel")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def device_type(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]]:
            '''The device type criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-devicetype
            '''
            result = self._values.get("device_type")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def make(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]]:
            '''The device make criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-make
            '''
            result = self._values.get("make")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def model(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]]:
            '''The device model criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def platform(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]]:
            '''The device platform criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-platform
            '''
            result = self._values.get("platform")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DemographicProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.GPSPointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "coordinates": "coordinates",
            "range_in_kilometers": "rangeInKilometers",
        },
    )
    class GPSPointProperty:
        def __init__(
            self,
            *,
            coordinates: typing.Union[typing.Union["CfnSegment.CoordinatesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            range_in_kilometers: jsii.Number,
        ) -> None:
            '''Specifies the GPS coordinates of the endpoint location.

            :param coordinates: The GPS coordinates to measure distance from.
            :param range_in_kilometers: The range, in kilometers, from the GPS coordinates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                g_pSPoint_property = pinpoint.CfnSegment.GPSPointProperty(
                    coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                        latitude=123,
                        longitude=123
                    ),
                    range_in_kilometers=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d24f99b0eee0b9552a9375e978107548ca2e7aee8b57f02447056b58d5526f50)
                check_type(argname="argument coordinates", value=coordinates, expected_type=type_hints["coordinates"])
                check_type(argname="argument range_in_kilometers", value=range_in_kilometers, expected_type=type_hints["range_in_kilometers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "coordinates": coordinates,
                "range_in_kilometers": range_in_kilometers,
            }

        @builtins.property
        def coordinates(
            self,
        ) -> typing.Union["CfnSegment.CoordinatesProperty", _IResolvable_a771d0ef]:
            '''The GPS coordinates to measure distance from.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates
            '''
            result = self._values.get("coordinates")
            assert result is not None, "Required property 'coordinates' is missing"
            return typing.cast(typing.Union["CfnSegment.CoordinatesProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def range_in_kilometers(self) -> jsii.Number:
            '''The range, in kilometers, from the GPS coordinates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-rangeinkilometers
            '''
            result = self._values.get("range_in_kilometers")
            assert result is not None, "Required property 'range_in_kilometers' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GPSPointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.GroupsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "source_segments": "sourceSegments",
            "source_type": "sourceType",
            "type": "type",
        },
    )
    class GroupsProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSegment.SegmentDimensionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            source_segments: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSegment.SourceSegmentsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            source_type: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An array that defines the set of segment criteria to evaluate when handling segment groups for the segment.

            :param dimensions: An array that defines the dimensions to include or exclude from the segment.
            :param source_segments: The base segment to build the segment on. A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify. You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.
            :param source_type: Specifies how to handle multiple base segments for the segment. For example, if you specify three base segments for the segment, whether the resulting segment is based on all, any, or none of the base segments.
            :param type: Specifies how to handle multiple dimensions for the segment. For example, if you specify three dimensions for the segment, whether the resulting segment includes endpoints that match all, any, or none of the dimensions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                groups_property = pinpoint.CfnSegment.GroupsProperty(
                    dimensions=[pinpoint.CfnSegment.SegmentDimensionsProperty(
                        attributes=attributes,
                        behavior=pinpoint.CfnSegment.BehaviorProperty(
                            recency=pinpoint.CfnSegment.RecencyProperty(
                                duration="duration",
                                recency_type="recencyType"
                            )
                        ),
                        demographic=pinpoint.CfnSegment.DemographicProperty(
                            app_version=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            channel=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            device_type=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            make=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            model=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            platform=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        location=pinpoint.CfnSegment.LocationProperty(
                            country=pinpoint.CfnSegment.SetDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            gps_point=pinpoint.CfnSegment.GPSPointProperty(
                                coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                    latitude=123,
                                    longitude=123
                                ),
                                range_in_kilometers=123
                            )
                        ),
                        metrics=metrics,
                        user_attributes=user_attributes
                    )],
                    source_segments=[pinpoint.CfnSegment.SourceSegmentsProperty(
                        id="id",
                
                        # the properties below are optional
                        version=123
                    )],
                    source_type="sourceType",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bfdc055a957bb3ee2df06b88288a0a9b4d26529ec28cfbf0bdbaae2933833c83)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument source_segments", value=source_segments, expected_type=type_hints["source_segments"])
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if source_segments is not None:
                self._values["source_segments"] = source_segments
            if source_type is not None:
                self._values["source_type"] = source_type
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_a771d0ef]]]]:
            '''An array that defines the dimensions to include or exclude from the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def source_segments(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSegment.SourceSegmentsProperty", _IResolvable_a771d0ef]]]]:
            '''The base segment to build the segment on.

            A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify.

            You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments
            '''
            result = self._values.get("source_segments")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSegment.SourceSegmentsProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple base segments for the segment.

            For example, if you specify three base segments for the segment, whether the resulting segment is based on all, any, or none of the base segments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple dimensions for the segment.

            For example, if you specify three dimensions for the segment, whether the resulting segment includes endpoints that match all, any, or none of the dimensions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"country": "country", "gps_point": "gpsPoint"},
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            country: typing.Optional[typing.Union[typing.Union["CfnSegment.SetDimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            gps_point: typing.Optional[typing.Union[typing.Union["CfnSegment.GPSPointProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies location-based criteria, such as region or GPS coordinates, for the segment.

            :param country: The country or region code, in ISO 3166-1 alpha-2 format, for the segment.
            :param gps_point: The GPS point dimension for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                location_property = pinpoint.CfnSegment.LocationProperty(
                    country=pinpoint.CfnSegment.SetDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    gps_point=pinpoint.CfnSegment.GPSPointProperty(
                        coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                            latitude=123,
                            longitude=123
                        ),
                        range_in_kilometers=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6b090515a156f90544dd3e3fdf2aedb1a11b7d27ed2b0e54ace1ffa9041594e)
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument gps_point", value=gps_point, expected_type=type_hints["gps_point"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if country is not None:
                self._values["country"] = country
            if gps_point is not None:
                self._values["gps_point"] = gps_point

        @builtins.property
        def country(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]]:
            '''The country or region code, in ISO 3166-1 alpha-2 format, for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html#cfn-pinpoint-segment-segmentdimensions-location-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def gps_point(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.GPSPointProperty", _IResolvable_a771d0ef]]:
            '''The GPS point dimension for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint
            '''
            result = self._values.get("gps_point")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.GPSPointProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.RecencyProperty",
        jsii_struct_bases=[],
        name_mapping={"duration": "duration", "recency_type": "recencyType"},
    )
    class RecencyProperty:
        def __init__(
            self,
            *,
            duration: builtins.str,
            recency_type: builtins.str,
        ) -> None:
            '''Specifies how recently segment members were active.

            :param duration: The duration to use when determining which users have been active or inactive with your app. Possible values: ``HR_24`` | ``DAY_7`` | ``DAY_14`` | ``DAY_30`` .
            :param recency_type: The type of recency dimension to use for the segment. Valid values are: ``ACTIVE`` and ``INACTIVE`` . If the value is ``ACTIVE`` , the segment includes users who have used your app within the specified duration are included in the segment. If the value is ``INACTIVE`` , the segment includes users who haven't used your app within the specified duration are included in the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                recency_property = pinpoint.CfnSegment.RecencyProperty(
                    duration="duration",
                    recency_type="recencyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e37ea1e48ec1022aa2d5bce8d02b5fb3eea84d98998ca96899a6a1a80911bb96)
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument recency_type", value=recency_type, expected_type=type_hints["recency_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "duration": duration,
                "recency_type": recency_type,
            }

        @builtins.property
        def duration(self) -> builtins.str:
            '''The duration to use when determining which users have been active or inactive with your app.

            Possible values: ``HR_24`` | ``DAY_7`` | ``DAY_14`` | ``DAY_30`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency-duration
            '''
            result = self._values.get("duration")
            assert result is not None, "Required property 'duration' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def recency_type(self) -> builtins.str:
            '''The type of recency dimension to use for the segment.

            Valid values are: ``ACTIVE`` and ``INACTIVE`` . If the value is ``ACTIVE`` , the segment includes users who have used your app within the specified duration are included in the segment. If the value is ``INACTIVE`` , the segment includes users who haven't used your app within the specified duration are included in the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency-recencytype
            '''
            result = self._values.get("recency_type")
            assert result is not None, "Required property 'recency_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.SegmentDimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "behavior": "behavior",
            "demographic": "demographic",
            "location": "location",
            "metrics": "metrics",
            "user_attributes": "userAttributes",
        },
    )
    class SegmentDimensionsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            behavior: typing.Optional[typing.Union[typing.Union["CfnSegment.BehaviorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            demographic: typing.Optional[typing.Union[typing.Union["CfnSegment.DemographicProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            location: typing.Optional[typing.Union[typing.Union["CfnSegment.LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            metrics: typing.Any = None,
            user_attributes: typing.Any = None,
        ) -> None:
            '''Specifies the dimension settings for a segment.

            :param attributes: One or more custom attributes to use as criteria for the segment.
            :param behavior: The behavior-based criteria, such as how recently users have used your app, for the segment.
            :param demographic: The demographic-based criteria, such as device platform, for the segment.
            :param location: The location-based criteria, such as region or GPS coordinates, for the segment.
            :param metrics: One or more custom metrics to use as criteria for the segment.
            :param user_attributes: One or more custom user attributes to use as criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                segment_dimensions_property = pinpoint.CfnSegment.SegmentDimensionsProperty(
                    attributes=attributes,
                    behavior=pinpoint.CfnSegment.BehaviorProperty(
                        recency=pinpoint.CfnSegment.RecencyProperty(
                            duration="duration",
                            recency_type="recencyType"
                        )
                    ),
                    demographic=pinpoint.CfnSegment.DemographicProperty(
                        app_version=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        channel=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        device_type=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        make=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        model=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        platform=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    location=pinpoint.CfnSegment.LocationProperty(
                        country=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        gps_point=pinpoint.CfnSegment.GPSPointProperty(
                            coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                latitude=123,
                                longitude=123
                            ),
                            range_in_kilometers=123
                        )
                    ),
                    metrics=metrics,
                    user_attributes=user_attributes
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c05d4e22f82460a550962cb437dda0e356eff057a2bbcf2a663df4cb496b51b0)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
                check_type(argname="argument demographic", value=demographic, expected_type=type_hints["demographic"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                check_type(argname="argument user_attributes", value=user_attributes, expected_type=type_hints["user_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if behavior is not None:
                self._values["behavior"] = behavior
            if demographic is not None:
                self._values["demographic"] = demographic
            if location is not None:
                self._values["location"] = location
            if metrics is not None:
                self._values["metrics"] = metrics
            if user_attributes is not None:
                self._values["user_attributes"] = user_attributes

        @builtins.property
        def attributes(self) -> typing.Any:
            '''One or more custom attributes to use as criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Any, result)

        @builtins.property
        def behavior(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.BehaviorProperty", _IResolvable_a771d0ef]]:
            '''The behavior-based criteria, such as how recently users have used your app, for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-behavior
            '''
            result = self._values.get("behavior")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.BehaviorProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def demographic(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.DemographicProperty", _IResolvable_a771d0ef]]:
            '''The demographic-based criteria, such as device platform, for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-demographic
            '''
            result = self._values.get("demographic")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.DemographicProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def location(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.LocationProperty", _IResolvable_a771d0ef]]:
            '''The location-based criteria, such as region or GPS coordinates, for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[typing.Union["CfnSegment.LocationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def metrics(self) -> typing.Any:
            '''One or more custom metrics to use as criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Any, result)

        @builtins.property
        def user_attributes(self) -> typing.Any:
            '''One or more custom user attributes to use as criteria for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-userattributes
            '''
            result = self._values.get("user_attributes")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentDimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.SegmentGroupsProperty",
        jsii_struct_bases=[],
        name_mapping={"groups": "groups", "include": "include"},
    )
    class SegmentGroupsProperty:
        def __init__(
            self,
            *,
            groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSegment.GroupsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            include: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the set of segment criteria to evaluate when handling segment groups for the segment.

            :param groups: Specifies the set of segment criteria to evaluate when handling segment groups for the segment.
            :param include: Specifies how to handle multiple segment groups for the segment. For example, if the segment includes three segment groups, whether the resulting segment includes endpoints that match all, any, or none of the segment groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                # attributes: Any
                # metrics: Any
                # user_attributes: Any
                
                segment_groups_property = pinpoint.CfnSegment.SegmentGroupsProperty(
                    groups=[pinpoint.CfnSegment.GroupsProperty(
                        dimensions=[pinpoint.CfnSegment.SegmentDimensionsProperty(
                            attributes=attributes,
                            behavior=pinpoint.CfnSegment.BehaviorProperty(
                                recency=pinpoint.CfnSegment.RecencyProperty(
                                    duration="duration",
                                    recency_type="recencyType"
                                )
                            ),
                            demographic=pinpoint.CfnSegment.DemographicProperty(
                                app_version=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                channel=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                device_type=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                make=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                model=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                platform=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            location=pinpoint.CfnSegment.LocationProperty(
                                country=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                gps_point=pinpoint.CfnSegment.GPSPointProperty(
                                    coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                        latitude=123,
                                        longitude=123
                                    ),
                                    range_in_kilometers=123
                                )
                            ),
                            metrics=metrics,
                            user_attributes=user_attributes
                        )],
                        source_segments=[pinpoint.CfnSegment.SourceSegmentsProperty(
                            id="id",
                
                            # the properties below are optional
                            version=123
                        )],
                        source_type="sourceType",
                        type="type"
                    )],
                    include="include"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7f9ae45391f7f5ea1282db2f3787597127ae40e876cd3598cb30c650a846f8a)
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if groups is not None:
                self._values["groups"] = groups
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def groups(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSegment.GroupsProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies the set of segment criteria to evaluate when handling segment groups for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html#cfn-pinpoint-segment-segmentgroups-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSegment.GroupsProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def include(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle multiple segment groups for the segment.

            For example, if the segment includes three segment groups, whether the resulting segment includes endpoints that match all, any, or none of the segment groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html#cfn-pinpoint-segment-segmentgroups-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentGroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.SetDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class SetDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the dimension type and values for a segment dimension.

            :param dimension_type: The type of segment dimension to use. Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.
            :param values: The criteria values to use for the segment dimension. Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                set_dimension_property = pinpoint.CfnSegment.SetDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a4a0dd2cac4c28e291dcbc00ee7cf8b1bb693f2c96906cc95076fb93c2493b8)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The type of segment dimension to use.

            Valid values are: ``INCLUSIVE`` , endpoints that match the criteria are included in the segment; and, ``EXCLUSIVE`` , endpoints that match the criteria are excluded from the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html#cfn-pinpoint-segment-setdimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The criteria values to use for the segment dimension.

            Depending on the value of the ``DimensionType`` property, endpoints are included or excluded from the segment if their values match the criteria values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html#cfn-pinpoint-segment-setdimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_pinpoint.CfnSegment.SourceSegmentsProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "version": "version"},
    )
    class SourceSegmentsProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the base segment to build the segment on.

            A base segment, also called a *source segment* , defines the initial population of endpoints for a segment. When you add dimensions to the segment, Amazon Pinpoint filters the base segment by using the dimensions that you specify.

            You can specify more than one dimensional segment or only one imported segment. If you specify an imported segment, the segment size estimate that displays on the Amazon Pinpoint console indicates the size of the imported segment without any filters applied to it.

            :param id: The unique identifier for the source segment.
            :param version: The version number of the source segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_pinpoint as pinpoint
                
                source_segments_property = pinpoint.CfnSegment.SourceSegmentsProperty(
                    id="id",
                
                    # the properties below are optional
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8bce58a66e7af3565b2809716c830bce2e4c181cb7d2a579374561a39382dcb5)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def id(self) -> builtins.str:
            '''The unique identifier for the source segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''The version number of the source segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceSegmentsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnSegmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "name": "name",
        "dimensions": "dimensions",
        "segment_groups": "segmentGroups",
        "tags": "tags",
    },
)
class CfnSegmentProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        name: builtins.str,
        dimensions: typing.Optional[typing.Union[typing.Union[CfnSegment.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        segment_groups: typing.Optional[typing.Union[typing.Union[CfnSegment.SegmentGroupsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnSegment``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the segment is associated with.
        :param name: The name of the segment. .. epigraph:: A segment must have a name otherwise it will not appear in the Amazon Pinpoint console.
        :param dimensions: The criteria that define the dimensions for the segment.
        :param segment_groups: The segment group to use and the dimensions to apply to the group's base segments in order to build the segment. A segment group can consist of zero or more base segments. Your request can include only one segment group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            # attributes: Any
            # metrics: Any
            # tags: Any
            # user_attributes: Any
            
            cfn_segment_props = pinpoint.CfnSegmentProps(
                application_id="applicationId",
                name="name",
            
                # the properties below are optional
                dimensions=pinpoint.CfnSegment.SegmentDimensionsProperty(
                    attributes=attributes,
                    behavior=pinpoint.CfnSegment.BehaviorProperty(
                        recency=pinpoint.CfnSegment.RecencyProperty(
                            duration="duration",
                            recency_type="recencyType"
                        )
                    ),
                    demographic=pinpoint.CfnSegment.DemographicProperty(
                        app_version=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        channel=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        device_type=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        make=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        model=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        platform=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    location=pinpoint.CfnSegment.LocationProperty(
                        country=pinpoint.CfnSegment.SetDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        gps_point=pinpoint.CfnSegment.GPSPointProperty(
                            coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                latitude=123,
                                longitude=123
                            ),
                            range_in_kilometers=123
                        )
                    ),
                    metrics=metrics,
                    user_attributes=user_attributes
                ),
                segment_groups=pinpoint.CfnSegment.SegmentGroupsProperty(
                    groups=[pinpoint.CfnSegment.GroupsProperty(
                        dimensions=[pinpoint.CfnSegment.SegmentDimensionsProperty(
                            attributes=attributes,
                            behavior=pinpoint.CfnSegment.BehaviorProperty(
                                recency=pinpoint.CfnSegment.RecencyProperty(
                                    duration="duration",
                                    recency_type="recencyType"
                                )
                            ),
                            demographic=pinpoint.CfnSegment.DemographicProperty(
                                app_version=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                channel=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                device_type=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                make=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                model=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                platform=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            location=pinpoint.CfnSegment.LocationProperty(
                                country=pinpoint.CfnSegment.SetDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                gps_point=pinpoint.CfnSegment.GPSPointProperty(
                                    coordinates=pinpoint.CfnSegment.CoordinatesProperty(
                                        latitude=123,
                                        longitude=123
                                    ),
                                    range_in_kilometers=123
                                )
                            ),
                            metrics=metrics,
                            user_attributes=user_attributes
                        )],
                        source_segments=[pinpoint.CfnSegment.SourceSegmentsProperty(
                            id="id",
            
                            # the properties below are optional
                            version=123
                        )],
                        source_type="sourceType",
                        type="type"
                    )],
                    include="include"
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93aebaf2bf510915cad424f950ffd26342db1c3ff84143a706570d72c4b9d26)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument segment_groups", value=segment_groups, expected_type=type_hints["segment_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "name": name,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if segment_groups is not None:
            self._values["segment_groups"] = segment_groups
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the segment is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the segment.

        .. epigraph::

           A segment must have a name otherwise it will not appear in the Amazon Pinpoint console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[CfnSegment.SegmentDimensionsProperty, _IResolvable_a771d0ef]]:
        '''The criteria that define the dimensions for the segment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-dimensions
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[CfnSegment.SegmentDimensionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def segment_groups(
        self,
    ) -> typing.Optional[typing.Union[CfnSegment.SegmentGroupsProperty, _IResolvable_a771d0ef]]:
        '''The segment group to use and the dimensions to apply to the group's base segments in order to build the segment.

        A segment group can consist of zero or more base segments. Your request can include only one segment group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-segmentgroups
        '''
        result = self._values.get("segment_groups")
        return typing.cast(typing.Optional[typing.Union[CfnSegment.SegmentGroupsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSegmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSmsTemplate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnSmsTemplate",
):
    '''A CloudFormation ``AWS::Pinpoint::SmsTemplate``.

    Creates a message template that you can use in messages that are sent through the SMS channel. A *message template* is a set of content and settings that you can define, save, and reuse in messages for any of your Amazon Pinpoint applications.

    :cloudformationResource: AWS::Pinpoint::SmsTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        # tags: Any
        
        cfn_sms_template = pinpoint.CfnSmsTemplate(self, "MyCfnSmsTemplate",
            body="body",
            template_name="templateName",
        
            # the properties below are optional
            default_substitutions="defaultSubstitutions",
            tags=tags,
            template_description="templateDescription"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        body: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::SmsTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param body: The message body to use in text messages that are based on the message template.
        :param template_name: The name of the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89e836fe0fb857ba3235b41a6a85321e08225673b9989cda11aa96355c241e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSmsTemplateProps(
            body=body,
            template_name=template_name,
            default_substitutions=default_substitutions,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e74490a81844e84ef580b9246e9da1b4b3970fca5503120d02b2dac7ba9ca5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b84bc9d8d9fd76b24918c0cdab249438795d23d52acbca5257037c7f4aabf3e)
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
        '''The Amazon Resource Name (ARN) of the message template.

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
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        '''The message body to use in text messages that are based on the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-body
        '''
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07e500d8aa1d9d62ec7d4474936f0c12b8fc7732d39f5b578a9fc3ad81a36f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatename
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19956df446b7594962957c826084bdb1d3d7e015ad07f54d494833086c868aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-defaultsubstitutions
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSubstitutions"))

    @default_substitutions.setter
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e03c5b8de46747dca38ba4df7a0e6078af6374c615acaa03ef82cb2e05fb754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatedescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c0c28bd641128409e0ad9a36019f45abe63168283a067204a14e58f3dd35c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnSmsTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "body": "body",
        "template_name": "templateName",
        "default_substitutions": "defaultSubstitutions",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnSmsTemplateProps:
    def __init__(
        self,
        *,
        body: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSmsTemplate``.

        :param body: The message body to use in text messages that are based on the message template.
        :param template_name: The name of the message template.
        :param default_substitutions: A JSON object that specifies the default values to use for message variables in the message template. This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param template_description: A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            # tags: Any
            
            cfn_sms_template_props = pinpoint.CfnSmsTemplateProps(
                body="body",
                template_name="templateName",
            
                # the properties below are optional
                default_substitutions="defaultSubstitutions",
                tags=tags,
                template_description="templateDescription"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a23a3da1416b77f3e9db463a7fbe629d2098a431f3688c28b41c5394b1a44e)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument default_substitutions", value=default_substitutions, expected_type=type_hints["default_substitutions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "body": body,
            "template_name": template_name,
        }
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def body(self) -> builtins.str:
        '''The message body to use in text messages that are based on the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-body
        '''
        result = self._values.get("body")
        assert result is not None, "Required property 'body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        '''A JSON object that specifies the default values to use for message variables in the message template.

        This object is a set of key-value pairs. Each key defines a message variable in the template. The corresponding value defines the default value for that variable. When you create a message that's based on the template, you can override these defaults with message-specific and address-specific variables and values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-defaultsubstitutions
        '''
        result = self._values.get("default_substitutions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the message template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSmsTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnVoiceChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_pinpoint.CfnVoiceChannel",
):
    '''A CloudFormation ``AWS::Pinpoint::VoiceChannel``.

    A *channel* is a type of platform that you can deliver messages to. To send a voice message, you send the message through the voice channel. Before you can use Amazon Pinpoint to send voice messages, you have to enable the voice channel for an Amazon Pinpoint application.

    The VoiceChannel resource represents the status and other information about the voice channel for an application.

    :cloudformationResource: AWS::Pinpoint::VoiceChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_pinpoint as pinpoint
        
        cfn_voice_channel = pinpoint.CfnVoiceChannel(self, "MyCfnVoiceChannel",
            application_id="applicationId",
        
            # the properties below are optional
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Pinpoint::VoiceChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The unique identifier for the Amazon Pinpoint application that the voice channel applies to.
        :param enabled: Specifies whether to enable the voice channel for the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd7804715ea2b8b75ce9f22789fb309cb220fb4a24b514f47ac1f0411363501)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVoiceChannelProps(application_id=application_id, enabled=enabled)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4af74d553cd9592854cbe49793a58251694a59f1981f8bd4c614a9334e1e601)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5732a24e0fd1dbf4347af5d05f0a5399322c04cb34c182182dc461858db44505)
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the voice channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bc36cecc1939daac62f67d51b9a54450baac4287691a17704621a5bce98995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the voice channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__858ab471d2ae1aa1fb72f6f3afc19f155da10958021576be88474aaca9377a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="monocdk.aws_pinpoint.CfnVoiceChannelProps",
    jsii_struct_bases=[],
    name_mapping={"application_id": "applicationId", "enabled": "enabled"},
)
class CfnVoiceChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVoiceChannel``.

        :param application_id: The unique identifier for the Amazon Pinpoint application that the voice channel applies to.
        :param enabled: Specifies whether to enable the voice channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_pinpoint as pinpoint
            
            cfn_voice_channel_props = pinpoint.CfnVoiceChannelProps(
                application_id="applicationId",
            
                # the properties below are optional
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d3d192a5736c5f4d820de6c17ff2c5b58cf4ea9b655648908cd8f107dcaedb)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The unique identifier for the Amazon Pinpoint application that the voice channel applies to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether to enable the voice channel for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVoiceChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnADMChannel",
    "CfnADMChannelProps",
    "CfnAPNSChannel",
    "CfnAPNSChannelProps",
    "CfnAPNSSandboxChannel",
    "CfnAPNSSandboxChannelProps",
    "CfnAPNSVoipChannel",
    "CfnAPNSVoipChannelProps",
    "CfnAPNSVoipSandboxChannel",
    "CfnAPNSVoipSandboxChannelProps",
    "CfnApp",
    "CfnAppProps",
    "CfnApplicationSettings",
    "CfnApplicationSettingsProps",
    "CfnBaiduChannel",
    "CfnBaiduChannelProps",
    "CfnCampaign",
    "CfnCampaignProps",
    "CfnEmailChannel",
    "CfnEmailChannelProps",
    "CfnEmailTemplate",
    "CfnEmailTemplateProps",
    "CfnEventStream",
    "CfnEventStreamProps",
    "CfnGCMChannel",
    "CfnGCMChannelProps",
    "CfnInAppTemplate",
    "CfnInAppTemplateProps",
    "CfnPushTemplate",
    "CfnPushTemplateProps",
    "CfnSMSChannel",
    "CfnSMSChannelProps",
    "CfnSegment",
    "CfnSegmentProps",
    "CfnSmsTemplate",
    "CfnSmsTemplateProps",
    "CfnVoiceChannel",
    "CfnVoiceChannelProps",
]

publication.publish()

def _typecheckingstub__6f08ea26f317f5c538495ea0d7494bdd8ac7b3c8c2aeddc570532d2ae7204b56(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575bbba65644ea9f3f5e16a98dc810e1a54e42cff16434c1d78d937c8233d616(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be87d1beaaf3cc5bbe59b1effb7fef86a7c4124e1137c7b36056659b098810b4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7170e880d4caaac7e88c3f885e52b861a7fc5f4e97d8e145520b8c102752e3e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6389dbbe5fec78e7da51c5ae11295c44f1027e0c850e3623bd8bbfe76e4ae8e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460edc798ddf4bc7148c8195a0d30068525a114c2bfad899d52da753823ebcd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1b2a5c3a9428c2354a95bb0f8f5523812fca0d00fe601a0820ed88a21dfa95(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab29ace345c1bc763addd0ef24129475660792ee9790e2bccb3a67db999ae704(
    *,
    application_id: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebaa63b7127a31f6e03bdd047e0bf11ce9802532ce3813d7672a23c66689ecd(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db77dcf665327ca220280e80f37e93a7790625be1f2d6c6987cc5461d309825(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac8ec59dba336e509df5e8ab2c88397c1b9411a1d3cb281d91b2bad342c6572(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68db3be042adf3ca0e6450202e9bdc16520a72fdf3e1b118ad1de8c65f467c4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4510303941b3afed742a91cbc53b3fc8a50acdc697ccdc7b6e93b8116138d340(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802cb1b5a39327c7a490458c49b8341d2524a7a8b35a5215ffa3d0f01910064e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65ee12a28bf1149de653598cb771755e1d77c92f10260bd30c2e232d764e9d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6808f7fcad0e6964a15fe969da5f81b7c9fc820e301c813b6d37012caf3f7c78(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bad353341ab31a5932a8f4411e5514087d6fbe165f59178d7f94b7da84ffd89(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ebfc296fdee694ade57710d766c35e3abbf19c83bd824dad3c5a5ca4949402(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d0fb9736cc3069225623721ad2a50288d05812005f25c2e9520c30ebfe0a1f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ab52fd5f8ceeb6df54ea75d265fb59954b2d40c8d2c92c20cb386d7fe0c08c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db76aa8db8a67a5190cb7616bdb65778a6ba1599a4a212f2b0ea5a22d6020a1(
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a4bb7874d53a993e09ceb2eaa5b6a0b08f977ac716e229741fc96befbddf1b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb98732e17bf5babad2a6a571cf0aea4152818c7b740708f05a63c4d97e723b1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0a2a4cd2a41fb8fd03f8f89e95e70fb40466ccb195adb6d7a5bd9d6205c7ce(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96fd58145978490eca0bcc2cec5c57076937a4c75a1accb9db6caf0d501f624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee77226a87e6dbbae33e212be5ecb211cd69ed88beedcceb3a57581f167cf249(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c44c7d932eae06e32d7b1bae7896501d6576c547cc4c79fe9eee4a66b51803(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2da7a6b04526de603b21eb7e028ee4ff9995576fce69a0de80fd944b87e31a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a0609830eb8550ebd9b04b7ef24a9b95346f35732ce3c06014ce47d160b311(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392ac333731be67812fe8bc70ec6da2bf70634599e760996b2410f58bbf31536(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013dc4adc1b1223b178fd2015ebe77b8b959521d080c472ac67e627059fa6c9a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb7bcce604e851f493b3ddc3fd09ff4ece60f5714f47a8f11aa9c92d9fe33ea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad79920fe5da8de3b9ad171c5b14ed43dde94e707a671d84423a76e8209e711f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79476d9be557ee88417e9eff066b492d77bd04d7028228320626991975f387a9(
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e07b56d81ac05cf51196c2880bd2c35dea391d56cda8eb3216729843b3d725b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e546229b07b6e8b44cab5a99e0e40cab45d18855ae0e649864ea7cdb535e1b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2a766d747975e8948f040319e6fb13bc06c85fa135e9b563d3c7d2a01d6ba4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d2442635f63552380f5691b4f2f5e344a6fad8955e9e206810165986399ef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1831a835b34e97543fe3b9157a1b3630456957f26f33a5b25b507858298de88f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038b2adfac5a995ff3837e62842990e3fee635b0d670bd232358c8a5ca101e9f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9819a284e81f1a911bc16420bac69bb5903eba3dfc985142a28bb95abc86b548(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63fee5ffd3f00f9f2e7f64f1a643c366c65fcf3aa423809f049fe0951bf7947(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3e4965799fb51b3bcc16f143bd95d098db055b2f476fb02833d56c2421a2f8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08db0ae93c70e78a761c2dfbb5fa270e31be8308cbbc76537e046c6d7a5adaf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be5b165157762e262c2137b8b4695dda3e6499be18a96e396a2f4a366ef49ee(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5444f4be86adaf5bf170720b1388b1456bd90bb9235a1670199a3638b5d10ad(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134537b920b31565c0f7ec9cd6ba57697dab1a130a1bb3a74fda9fa1399d2bfa(
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f179fbcf21a1f0bd086b007f6b3edfd1faa7db6677fabfd7d067f0ee747021cb(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe2a21ef757b8e163b647d6b1d70a4c2345d9f5315ca4e0815a15ffc5b0f580(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d65c28cd0326ea6e65fb5868e735ea34c636cdfc688bb0f913e80a26427be9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50b6a55c5531fe21ad78c887cef888aa704c421cd650221646998d78dbafd7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9881543928cce337163f0f450692e4fd7326cf3f0b8252bf5b168929bee3b5fb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcf424773c2af13b79834dd52f424060a5c697d129ae8faeffe149aa3c90896(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58080bed9756bc4a99898d77018138745b9b0a26022499f2af15249f9d83d700(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61006cf9d0526af7bb68eb1471d0e66d6212ca7ac755853a51a0e1a7247f5c99(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2342d333e8522b11fbc5632207031d0fe6534c61052091aa91f2f47a829cae5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf635ab764d8fa26e3f387d2be0732d000f40ccb22056928f67e712a879feb9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f692f7e650c09f565a3c4a8fbe55591eb9f1c688a2a5c2db9aa6dafae628eb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ff9330b5f2085a236382d5839b13b3ba54fb14222590b737bac3b599ac9094(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164ac1be5ac1acc295bbf91bd3a9cbb438574c1f2ffc2b6c66256f52b3cfebae(
    *,
    application_id: builtins.str,
    bundle_id: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    default_authentication_method: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    private_key: typing.Optional[builtins.str] = None,
    team_id: typing.Optional[builtins.str] = None,
    token_key: typing.Optional[builtins.str] = None,
    token_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4791d7f10900a0dd87af81d7d79fe9cc68511c7ca55baede5018fb42bcd441(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874c740239b175c3fc973b48bbd36af37de2636672d22473d6b6465e98ba012f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d21055c937b6040cc9efebf7057788e8e4b04f1ab17059daccd3edd1d9c218(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e28be3f71054300a87dc2762b21dea3474a3f7dd5bd1374138d89cad2fb1981(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b841a739e748aadf8d0f90e76b7b6e27464c35a344204d56e26247ab9ce7e1(
    *,
    name: builtins.str,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf25db5a2f39b69aca8a33454894fd1766efd2f43a0cd55cdaa9251dc9fdb87(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    campaign_hook: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    limits: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.LimitsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    quiet_time: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c641cd4454890886c658d8c1e8a76d47c548fe8e0e8bfb71bb9c6a91ad63db2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9c7eb41d98d0764c8ac28670fd74b732246b97ed0b71b838c46069d42f9ccf(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015ae3c07c563e6ba464406bf9ac01e8a1657aa88bb062c959dd08db07da3939(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6a67df9c75da42632465499ead12facf7534e831ce801e5a400bff659b1dd8(
    value: typing.Optional[typing.Union[CfnApplicationSettings.CampaignHookProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5098168cb1b5c2cad35f1ccfd68fb61fe1b6f513e7b8ece1603972b36ad8b80c(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d34a8c378db2f5ff8ceb0ab049ca8c88506629509b003996f182269c306e4bc(
    value: typing.Optional[typing.Union[CfnApplicationSettings.LimitsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c88848954a038aba6196f0f54a67afa5930823a874680db5bf7209c98b0bb9(
    value: typing.Optional[typing.Union[CfnApplicationSettings.QuietTimeProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103885ff0e884277f249b55613135a29a3e4a2adcef62644b26f74831be6b410(
    *,
    lambda_function_name: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    web_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f9fe931904ce2a93dc77dafa29289eae10d3c15aa373b0bd5ab70765245543(
    *,
    daily: typing.Optional[jsii.Number] = None,
    maximum_duration: typing.Optional[jsii.Number] = None,
    messages_per_second: typing.Optional[jsii.Number] = None,
    total: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b22c680a7b9da065ed90da5bfd19b3c5a4d698e93abe2c2f6a123c37a14197(
    *,
    end: builtins.str,
    start: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fd7593767843fc4f35f1601dfafc1114297acdb348a8d18225e340f91a1d61(
    *,
    application_id: builtins.str,
    campaign_hook: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    limits: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.LimitsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    quiet_time: typing.Optional[typing.Union[typing.Union[CfnApplicationSettings.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f961110d7709f1c61c69f6ac0c6b9f921b4aae71b4bb27e98289ef3a2139ab77(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_key: builtins.str,
    application_id: builtins.str,
    secret_key: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3462693540d17552e574646088d3ce486e384d711274971451db8f8ca432e8e8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d50d36649e060d572c159366f5637f53752b3bb34e852f95cd895568b12d25(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c88f9b34391f99adc6c07c7335015361cb903cfc103c459396b53aee1ef814(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0defa188185f6baa5aefa85dd6e30ece25d260dae6c76f3e83949b8848f778f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fa330dd617578faaa68678a9263894bd2179eadb43b78759b4dfd14d764b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3374dd9a64c3da8f251c9e59cd630c71be0077de39ee64bb3c54c6c0ac70f9c0(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275b83d64f2fe22f6e2406c0bbe52e8e31106a87e9a916666c52a01df0f6e4b2(
    *,
    api_key: builtins.str,
    application_id: builtins.str,
    secret_key: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4541773d796cd7bd1e9fdd1f6954c7a8d9e17c8cda7251d42b134f503799027b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    name: builtins.str,
    schedule: typing.Union[typing.Union[CfnCampaign.ScheduleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    segment_id: builtins.str,
    additional_treatments: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCampaign.WriteTreatmentResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    campaign_hook: typing.Optional[typing.Union[typing.Union[CfnCampaign.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    custom_delivery_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    holdout_percent: typing.Optional[jsii.Number] = None,
    is_paused: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    limits: typing.Optional[typing.Union[typing.Union[CfnCampaign.LimitsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    message_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    priority: typing.Optional[jsii.Number] = None,
    segment_version: typing.Optional[jsii.Number] = None,
    tags: typing.Any = None,
    template_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    treatment_description: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f210abf917deba3041a8482b86e650ccd1b1f07ddf7070ea8629ed48f6d22ab8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17cfee3021ccbd47251a0edb2583ee52835b5216c92bddc4f9f1017472f5921c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b5499cc86281e48eae8e0c5014fca230153dba487c974ee9ef2c0ea55fcfd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40b6cda7b00aa16047609a8f929fc6de794647c87c16760e311329450c8d80c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21ed579b6432231d83d6d12d71c59b699e46c3c96cb385dbd819dd6c833309f(
    value: typing.Union[CfnCampaign.ScheduleProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9c90984d99d4aaf7c4e41fd9cb559df394ac074b4f8dc3e783a38248f9abb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c89f6e9524ba088b21d464f3efdd773c66ae19ba8ad98cb7a99b8c216ac8ec(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCampaign.WriteTreatmentResourceProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e7cb85d8c4b219975f6688174dfe88308fd0d38da3b0446b28fc78dbfd230d(
    value: typing.Optional[typing.Union[CfnCampaign.CampaignHookProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f5dfd8720435a9ce21c9a4f0a5bec8ab2146fd0d570bf23bbd1820828851ba(
    value: typing.Optional[typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d45fcab699ece8198987f3f9add8c9514454744c755380f96679d2ed5d446b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c91861545140f23d40fd6874edf2bec082e7dc2de4cca50c9720af02f837d0d(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eab9380b78222bd724427e8d35207323ba2ea74d8181f0500b030fcd46c538e(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07ddf54c74d6b24a96c24baa21fe9db78e1afe191fd98c8968b47ead90a5f4b(
    value: typing.Optional[typing.Union[CfnCampaign.LimitsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f39a9cdc96948eef8b79f16b10b629af2c69def79d27da4424d904be2c0fdf2(
    value: typing.Optional[typing.Union[CfnCampaign.MessageConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59984b4ef6210c445c94031b8a23fa7d2ca6dea33eb2fe80ada9efdf83e4e030(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69decea91b1db2db0c9e7a6177cd9ad407a99573af706b7a8c7be74719426398(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d125de3376c65c4042b017d6790f2d2e9de8743b494ca3aa66650320b8e03683(
    value: typing.Optional[typing.Union[CfnCampaign.TemplateConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8eda1a6bb530d88122f882e6d3548d0e40858795e49c079934fb92fe621af5a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e07911e6911fe8240669e042679c32b24f4c78de54a29f946184770fa824b19(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5596bbd839989137298ae6c67b14ecd834c8241dca10424e932ed6dcaa2f96fe(
    *,
    attribute_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b88fe61f00e69c95ac6b075367b95aff4ccb51711a2f7ed1e21b513184ec0a2(
    *,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cad9fd05af7ff052dc96c7041a287b6124f54cb7e95dc06682fe0eb4dfa9e78(
    *,
    body: typing.Optional[builtins.str] = None,
    from_address: typing.Optional[builtins.str] = None,
    html_body: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419b0f2785f3cdb6cd28dda11583fd7808e2ac5ef4dde6993f922a8619d70ba7(
    *,
    dimensions: typing.Optional[typing.Union[typing.Union[CfnCampaign.EventDimensionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04c20564ffd54414ab3a3a0a1fabff2e898032bd3f88f3a49ed921ff7aa80d8(
    *,
    lambda_function_name: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    web_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b922b87e0ba762479c27b5931d14e4a1b0cd53149a192e4d0a1aeca132496424(
    *,
    content: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCampaign.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    custom_config: typing.Any = None,
    layout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf74bae8597ffb16a4a8163894d2fa81ae2bd4802ead658243b34f656002ac24(
    *,
    body: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    message_type: typing.Optional[builtins.str] = None,
    origination_number: typing.Optional[builtins.str] = None,
    sender_id: typing.Optional[builtins.str] = None,
    template_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457128f545655310f7a89d972abb8697e0e15d643d6824bbdebf6b7cb1a6fad7(
    *,
    delivery_uri: typing.Optional[builtins.str] = None,
    endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1f98760b3d524ab9a096f012a64082defee479e8c8b565543c76199314ffad(
    *,
    background_color: typing.Optional[builtins.str] = None,
    border_radius: typing.Optional[jsii.Number] = None,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d0bc16432023257772621c71b46b5e384599a7acb4be254ee5726e3da00788(
    *,
    attributes: typing.Any = None,
    event_type: typing.Optional[typing.Union[typing.Union[CfnCampaign.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    metrics: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d97be6df17335dc55972a4299d970b8279e70fa18a8f123e3e54c28326b72a9(
    *,
    alignment: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f46dc3b29cc02420636386554d38e013b0cb0344ed7546c14f953589f35f6a(
    *,
    android: typing.Optional[typing.Union[typing.Union[CfnCampaign.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_config: typing.Optional[typing.Union[typing.Union[CfnCampaign.DefaultButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ios: typing.Optional[typing.Union[typing.Union[CfnCampaign.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    web: typing.Optional[typing.Union[typing.Union[CfnCampaign.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e540cc8d61a5c8a43891207bc6f002221365fb0f8a822d2f3c7ad5ff1a8c98(
    *,
    background_color: typing.Optional[builtins.str] = None,
    body_config: typing.Optional[typing.Union[typing.Union[CfnCampaign.InAppMessageBodyConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    header_config: typing.Optional[typing.Union[typing.Union[CfnCampaign.InAppMessageHeaderConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    image_url: typing.Optional[builtins.str] = None,
    primary_btn: typing.Optional[typing.Union[typing.Union[CfnCampaign.InAppMessageButtonProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    secondary_btn: typing.Optional[typing.Union[typing.Union[CfnCampaign.InAppMessageButtonProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07df763c8998b67257b3253b3f32a17df82b5b4e1d1d333bd08c41fb06749b5b(
    *,
    alignment: typing.Optional[builtins.str] = None,
    header: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950e7bce3ae6a11f6165ab433327d1873f0700c161184daa580c0540d079dc2b(
    *,
    daily: typing.Optional[jsii.Number] = None,
    maximum_duration: typing.Optional[jsii.Number] = None,
    messages_per_second: typing.Optional[jsii.Number] = None,
    session: typing.Optional[jsii.Number] = None,
    total: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f506a41a1fea37142d32aa60cd1ded4d78d34489b5d634fb8261fd7484ad2321(
    *,
    adm_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    apns_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    baidu_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    custom_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.CampaignCustomMessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    email_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.CampaignEmailMessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    gcm_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    in_app_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.CampaignInAppMessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sms_message: typing.Optional[typing.Union[typing.Union[CfnCampaign.CampaignSmsMessageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6703765b5d18a108e2935f8935f7d525f1aa48f210691dcb247e0fc2bf2e9ea4(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    image_icon_url: typing.Optional[builtins.str] = None,
    image_small_icon_url: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    json_body: typing.Optional[builtins.str] = None,
    media_url: typing.Optional[builtins.str] = None,
    raw_content: typing.Optional[builtins.str] = None,
    silent_push: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    time_to_live: typing.Optional[jsii.Number] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71dd3123da0599764a0023bdd6a9ae644343acb314a3274b2d7f55ddd775edc4(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5556ee2f86b9a70c0cb7d02d2c3ab85cb46316beb654288c4ea34242460e614b(
    *,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437d4e16c16916f75e859e32a3fa46726fbb88b1b9949eb8a443fb6aa28f192d(
    *,
    end: builtins.str,
    start: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a56fc7789bdbf066bcd444531c6bb3ed53397542d90500faa322a3936d6ebd(
    *,
    end_time: typing.Optional[builtins.str] = None,
    event_filter: typing.Optional[typing.Union[typing.Union[CfnCampaign.CampaignEventFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    frequency: typing.Optional[builtins.str] = None,
    is_local_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    quiet_time: typing.Optional[typing.Union[typing.Union[CfnCampaign.QuietTimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    start_time: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d86fbae36e2fe97df4c2a1aad64dc1ac67d24e71f102e9af687b319fa5b3fb6(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cbc60e3a9a24dad439717c2092e5c1de05f9f6a98cdf2275f08cc4fc10d03e2(
    *,
    email_template: typing.Optional[typing.Union[typing.Union[CfnCampaign.TemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    push_template: typing.Optional[typing.Union[typing.Union[CfnCampaign.TemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sms_template: typing.Optional[typing.Union[typing.Union[CfnCampaign.TemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    voice_template: typing.Optional[typing.Union[typing.Union[CfnCampaign.TemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66f7c9150a4441f8aeccc9ff31d527733cb6659c205e1a83167ec30bfd22207(
    *,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b80281097b61385e992001b7076f2ac2467552d16ccf164fa3ec27df87c225(
    *,
    custom_delivery_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    message_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    schedule: typing.Optional[typing.Union[typing.Union[CfnCampaign.ScheduleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    size_percent: typing.Optional[jsii.Number] = None,
    template_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    treatment_description: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a604c4cf0736947cde446186f88845d2d3fcd92bb46dcd583e0eabba82cc572f(
    *,
    application_id: builtins.str,
    name: builtins.str,
    schedule: typing.Union[typing.Union[CfnCampaign.ScheduleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    segment_id: builtins.str,
    additional_treatments: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCampaign.WriteTreatmentResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    campaign_hook: typing.Optional[typing.Union[typing.Union[CfnCampaign.CampaignHookProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    custom_delivery_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.CustomDeliveryConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    holdout_percent: typing.Optional[jsii.Number] = None,
    is_paused: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    limits: typing.Optional[typing.Union[typing.Union[CfnCampaign.LimitsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    message_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.MessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    priority: typing.Optional[jsii.Number] = None,
    segment_version: typing.Optional[jsii.Number] = None,
    tags: typing.Any = None,
    template_configuration: typing.Optional[typing.Union[typing.Union[CfnCampaign.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    treatment_description: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef0d86926d29015a7352241112aeead73ce2b022b237cc772dd7a2ae18bd38c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    from_address: builtins.str,
    identity: builtins.str,
    configuration_set: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb989a766331b66e6649d2c5124e542c30d53c7d32c747f107a92c6c595df12c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eee75605f28ff32d95ed0946b9c8ab06b43d7123af9f0b9bc88103600d0b800(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bfa930689b8dd7e328a261f2d7845bbbf81d1ae30595dc377c8e5e2108e3b7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3857e2bbccc6bcaad81662819e77a5c0b2c63899283edc24aa15f8aed4b4750c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24bee1c19e53d401f7004d2f7a5867920f5553f2d9302b389b81543279a5289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df420ecb7c550bd85c8508e299a1b5758f18ec30993f0d6e58526e200b4c81ed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5bcdbcb464e9ab4c3ff080558d18ff517746d6be746bad3896d6809d5a8640(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728b583166e75452c0eebebe8ef11628608faa63bbfcf156a28127681fe703d7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67dbc1410fcea3a0e159db5d3881724a5d570289c48acdb4850cc9f2481bd82(
    *,
    application_id: builtins.str,
    from_address: builtins.str,
    identity: builtins.str,
    configuration_set: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d927c3809ecb0286cc5e6d528d3f64570343d6ba9b73b738355aee0b45f5e3c4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    subject: builtins.str,
    template_name: builtins.str,
    default_substitutions: typing.Optional[builtins.str] = None,
    html_part: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
    text_part: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be23f59f6986c71eae8932e912916f3c2f9dca01b11cc5e836b4984703ed8ff3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c6d2fa656fb31e6645d928fd15cbbc90bd8c288de17c7e5e13a78e8f1cbffc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2b2dd810de41c517f3ec909a7b138adcaf76ba40d16b5dd29c93d1aa35f9a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a450a65be3406036009229b94484eace8f3c068b5d1099d6a23c23e3e12b2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9107d5e87077d7c3257764776931b738c66021e83269ba203f9eef3fecc4d74c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e06ca8dee809f3b6754574694dc4ac6d2cc2cb6e2317bc5f0132b14bff6b8e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5675fdd1bc484c321236765d8bae32ea24df6875286ea9a4d6f14400c9922f78(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051427f2b32ea625ef33877b4c5000034f8455c9271656bc095b184968ee6759(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865d643fd6c8b54e2c1caf3d92331d297d025bc33c2efc1b80da3e82fb9f527c(
    *,
    subject: builtins.str,
    template_name: builtins.str,
    default_substitutions: typing.Optional[builtins.str] = None,
    html_part: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
    text_part: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8debffb2d6bd1384c9a45a30fd5a7e265dd2718027b92936eddf91051b1305(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    destination_stream_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48bc8429903b60b948086e4ffbca6adfd48d93adcbc68b03a5bbe1acd1f0299(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfa16da52f3264a612af98b2a6bb15334278362a34a26441f3fd1e576ed5513(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef12f4b9591b522df320c027f65471f2452eccb0704bd2711f512042548b8b37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35eeab46bba4556c1ea4dd98df7745d70d13c2a0e898ab2b22ab120ca105d00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64661d3ed931a57188f870a3f3fce4b8ac6891342d012e56ab211d84974064f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cef0e4cdeda75a978529882134ae584c4ec71dfbf32a41923b239742ae4fb2(
    *,
    application_id: builtins.str,
    destination_stream_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05f6d6de0d6c0a814a6340975dec01c58d9950fa4b9e49790fa8f55af42e6c2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_key: builtins.str,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f6492f1ea7c853403286924b2c9104fd48d2df3a11055e583acb7ddc044487(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76fa7ef6049936b484d0327ebcfe29e954e3421d02879361597ada73c91517c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2423be58cadb8b490fd75fff2ab6aed90e157053acb52709aa287c504b3e3361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3323a9d99664b4c17ae38b4f46b013e78f1183cebedb2245d4ec4c34e19018fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0745ca382b80b855b20463aaa8d3b618395a7da2852f6c1acdba6a6facb1f32b(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1031f7a1856e06e99539ebcb64e2d7e5756b023dd5322f57b70aa72acf6958d6(
    *,
    api_key: builtins.str,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a920c894d191e02e5dbfb96fef5aceb7fc0b44faf901fe7224614c812a5237f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    template_name: builtins.str,
    content: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnInAppTemplate.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    custom_config: typing.Any = None,
    layout: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188c65c214df80c884d7de0c03e080871f7f9814658f7c6445d6b9ae34fab752(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa9787c15a6189b4832bb83585fc36036f0191bf30f841deb4775b1eee1a1bd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072aa5b550311ef0e00a3bafd715ee886a59a16f7b8ef83e810e9649896a5a7d(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e679e50a42ecdec445e3393378fb8199561711f9a2c4828ea1146175d06287f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d15b7e3672ad138c5100f8711b1158cc44e008f2ceeb569ebc34e8965fa3da3(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnInAppTemplate.InAppMessageContentProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2ce72c0400838c6bfbb696083318ab88583d2e9bb71ebc83d47976e484406e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d70456dbb54a5b6e1e36e5b18e12862b3cce4a648d1021cd9fafa31bf8a86f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7340e172398f0bfb0ed5754be3932e665788618b3211f5f93a3a33783ac11b0(
    *,
    alignment: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba62f583644620b8f31cf9dd62bbac8dfd6c43a77b596cfaa430d97e242c74fe(
    *,
    android: typing.Optional[typing.Union[typing.Union[CfnInAppTemplate.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_config: typing.Optional[typing.Union[typing.Union[CfnInAppTemplate.DefaultButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ios: typing.Optional[typing.Union[typing.Union[CfnInAppTemplate.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    web: typing.Optional[typing.Union[typing.Union[CfnInAppTemplate.OverrideButtonConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e197e02d977cff08bef51725c29a1625036b679c304f6b142e7bc6b71b6afe19(
    *,
    background_color: typing.Optional[builtins.str] = None,
    border_radius: typing.Optional[jsii.Number] = None,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60db439dea2fc8b4cf4e48ecbc220760d009c0b31f494ff6538f6651c6e4d67d(
    *,
    alignment: typing.Optional[builtins.str] = None,
    header: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3d5a8decc0c9889af580ba5c7146b1e57c16c619b75b684a45409c79e9acea(
    *,
    background_color: typing.Optional[builtins.str] = None,
    body_config: typing.Optional[typing.Union[typing.Union[CfnInAppTemplate.BodyConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    header_config: typing.Optional[typing.Union[typing.Union[CfnInAppTemplate.HeaderConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    image_url: typing.Optional[builtins.str] = None,
    primary_btn: typing.Optional[typing.Union[typing.Union[CfnInAppTemplate.ButtonConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    secondary_btn: typing.Optional[typing.Union[typing.Union[CfnInAppTemplate.ButtonConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb7a7517f1dba9324cf8e28b7c4b59d8084c34ccc2b0a98d13701b827168745(
    *,
    button_action: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c009849a19465c26fafbcfc4baf6a9150b53545d9aaf0326df66c6acbf5e0107(
    *,
    template_name: builtins.str,
    content: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnInAppTemplate.InAppMessageContentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    custom_config: typing.Any = None,
    layout: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd4fef242126a42b9fe6c869157300b9e2aa1e4c199d61fd5e9474849d6a727(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    template_name: builtins.str,
    adm: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    apns: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    baidu: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_substitutions: typing.Optional[builtins.str] = None,
    gcm: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633ce22ae7e21b165aa3419db7a690755fa372bf2600e85b1052122b8a5ce2aa(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a030cc85a82ee4031e9a9219f81a37a4c656a52fe494015f6b94c7a6f3ecf337(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0258b3e52265b23cc0c89ead15c3b6b674ee420767dcf757cac43ed753f79fc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de826fd231f9bef42aaa84602f1b74be960dfb4c435bd41737184374bc7644d(
    value: typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68e746276a6cc1cf4e10b2534cdb1607053d2f28df8c963bdf960ad1c1a6b4b(
    value: typing.Optional[typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f38bfc8d3ade04d0d866138a38b1dbb97f92dbf65cd14926366ec30efdec46(
    value: typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4ae0e88118d6077b8353b256fe5ef9c7e291d9d66b7e88796f8953ab5698c1(
    value: typing.Optional[typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ad9e9436cb6d6de0604e08725dd1902af6cb032f8eab8bc2bfd549feb9efa4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1642a056562aa094bcfb1b07e7f1627a432465dc3df6658d77c332f8bb30d617(
    value: typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe94b1bb9a3a97e0163b917f62ad062fb0d71460d0ab66e4fe06165106cd87ea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e7da002b17d97eb8987d5d955593a0c645394bdbd9fe68855c640f9fff787c(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    media_url: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3830fe4192f1362ed1cf072350261e04659ed0f688f5f92a5421a332486283(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    image_icon_url: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    small_image_icon_url: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe3af211338f4c0d577e4bce165c38643746ba33f83e83068c7d344b9cc2646(
    *,
    action: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
    sound: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db889fa25c129c979bd7e8e7dac80f6a38444b1d7956aff339f58dc6ad5452e0(
    *,
    template_name: builtins.str,
    adm: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    apns: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    baidu: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_substitutions: typing.Optional[builtins.str] = None,
    gcm: typing.Optional[typing.Union[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d487251e1ac55a04cb5ea65d246f0edcd320071cf0f1bdcf5a9a1cf7c31f1ff1(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    sender_id: typing.Optional[builtins.str] = None,
    short_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88e2e378d97b0f4681f5be0430bf0688db3f900d70056f784d9ee832493b08d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c7e0ff3cae011bb73273d1b2cc93439a54501324279adf021647ae35b80424(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f188f164ae430b507be299859ed37a2defbf6bab722910ccd954d0f55ffc796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5df304b553f9e99fa74368a6eb241e0ad2b9b069031873c024f557f742900d(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adab4b33ebc72e33ee3155131a373ec7fbb90f2e837aa335a164e2dfd0662c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ba9b036e8129c3f9e9126505af325277f05113b9f0654b2d10db691ca84cd7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4329592acdcf99ca422d7135ad225b92b873191bc12c1fb25e7b4a89d6d55938(
    *,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    sender_id: typing.Optional[builtins.str] = None,
    short_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383e1befb95a42f70c11e76294d8d1a3d180c2cde8a017d9cd4dbafb48b5abc4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    name: builtins.str,
    dimensions: typing.Optional[typing.Union[typing.Union[CfnSegment.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    segment_groups: typing.Optional[typing.Union[typing.Union[CfnSegment.SegmentGroupsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8ac3b6e0dd7a7be7fa4875b5d4094820364149511c8ec52e6dfb56003119d3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f755029b91d754ffe1b8c98799e09e07ef9e5b31f7bc7917754513a0a731c96(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea51ffe33eb489a2ac8d2e53a2832b7ef24b454b71d17a04b7f202f53ea12760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecc64de0b23f28c35e823b36a05afa257d42ece094e55d2fe2699ab5a5de4e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd538cedf4413425234faff50415946e5e681a668329a9d3c19e4e14d70556fb(
    value: typing.Optional[typing.Union[CfnSegment.SegmentDimensionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1244ecc8feea9b3ad63602f4b31fed1f3055167f33b5be026ce88e337601f63(
    value: typing.Optional[typing.Union[CfnSegment.SegmentGroupsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c89a4a2983a94e9ecabf61b05791e025372aad054b18c5d95f665a17e893ac(
    *,
    attribute_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e810d7fdfa951d02e549f378952452bdf72ac02c30f858286e7a1e00c132e3(
    *,
    recency: typing.Optional[typing.Union[typing.Union[CfnSegment.RecencyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b8710b3fa3d7a5040619113ca59b15061fec700ace9560cd475b96d775dfa0(
    *,
    latitude: jsii.Number,
    longitude: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3996b2c2cfdfb4574916456a600b06ecb259779c5bc94b0f65dea399cec83c05(
    *,
    app_version: typing.Optional[typing.Union[typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    channel: typing.Optional[typing.Union[typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    device_type: typing.Optional[typing.Union[typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    make: typing.Optional[typing.Union[typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    model: typing.Optional[typing.Union[typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    platform: typing.Optional[typing.Union[typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24f99b0eee0b9552a9375e978107548ca2e7aee8b57f02447056b58d5526f50(
    *,
    coordinates: typing.Union[typing.Union[CfnSegment.CoordinatesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    range_in_kilometers: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfdc055a957bb3ee2df06b88288a0a9b4d26529ec28cfbf0bdbaae2933833c83(
    *,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSegment.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    source_segments: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSegment.SourceSegmentsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    source_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b090515a156f90544dd3e3fdf2aedb1a11b7d27ed2b0e54ace1ffa9041594e(
    *,
    country: typing.Optional[typing.Union[typing.Union[CfnSegment.SetDimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    gps_point: typing.Optional[typing.Union[typing.Union[CfnSegment.GPSPointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37ea1e48ec1022aa2d5bce8d02b5fb3eea84d98998ca96899a6a1a80911bb96(
    *,
    duration: builtins.str,
    recency_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05d4e22f82460a550962cb437dda0e356eff057a2bbcf2a663df4cb496b51b0(
    *,
    attributes: typing.Any = None,
    behavior: typing.Optional[typing.Union[typing.Union[CfnSegment.BehaviorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    demographic: typing.Optional[typing.Union[typing.Union[CfnSegment.DemographicProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    location: typing.Optional[typing.Union[typing.Union[CfnSegment.LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    metrics: typing.Any = None,
    user_attributes: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f9ae45391f7f5ea1282db2f3787597127ae40e876cd3598cb30c650a846f8a(
    *,
    groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSegment.GroupsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    include: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4a0dd2cac4c28e291dcbc00ee7cf8b1bb693f2c96906cc95076fb93c2493b8(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bce58a66e7af3565b2809716c830bce2e4c181cb7d2a579374561a39382dcb5(
    *,
    id: builtins.str,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93aebaf2bf510915cad424f950ffd26342db1c3ff84143a706570d72c4b9d26(
    *,
    application_id: builtins.str,
    name: builtins.str,
    dimensions: typing.Optional[typing.Union[typing.Union[CfnSegment.SegmentDimensionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    segment_groups: typing.Optional[typing.Union[typing.Union[CfnSegment.SegmentGroupsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89e836fe0fb857ba3235b41a6a85321e08225673b9989cda11aa96355c241e1(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    body: builtins.str,
    template_name: builtins.str,
    default_substitutions: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e74490a81844e84ef580b9246e9da1b4b3970fca5503120d02b2dac7ba9ca5f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b84bc9d8d9fd76b24918c0cdab249438795d23d52acbca5257037c7f4aabf3e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07e500d8aa1d9d62ec7d4474936f0c12b8fc7732d39f5b578a9fc3ad81a36f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19956df446b7594962957c826084bdb1d3d7e015ad07f54d494833086c868aab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e03c5b8de46747dca38ba4df7a0e6078af6374c615acaa03ef82cb2e05fb754(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c0c28bd641128409e0ad9a36019f45abe63168283a067204a14e58f3dd35c2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a23a3da1416b77f3e9db463a7fbe629d2098a431f3688c28b41c5394b1a44e(
    *,
    body: builtins.str,
    template_name: builtins.str,
    default_substitutions: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd7804715ea2b8b75ce9f22789fb309cb220fb4a24b514f47ac1f0411363501(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4af74d553cd9592854cbe49793a58251694a59f1981f8bd4c614a9334e1e601(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5732a24e0fd1dbf4347af5d05f0a5399322c04cb34c182182dc461858db44505(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bc36cecc1939daac62f67d51b9a54450baac4287691a17704621a5bce98995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858ab471d2ae1aa1fb72f6f3afc19f155da10958021576be88474aaca9377a31(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d3d192a5736c5f4d820de6c17ff2c5b58cf4ea9b655648908cd8f107dcaedb(
    *,
    application_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass
