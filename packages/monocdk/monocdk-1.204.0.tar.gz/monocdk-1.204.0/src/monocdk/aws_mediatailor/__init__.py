'''
# AWS::MediaTailor Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as mediatailor
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for MediaTailor construct libraries](https://constructs.dev/search?q=mediatailor)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::MediaTailor resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaTailor.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::MediaTailor](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaTailor.html).

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
class CfnPlaybackConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration",
):
    '''A CloudFormation ``AWS::MediaTailor::PlaybackConfiguration``.

    Adds a new playback configuration to AWS Elemental MediaTailor .

    :cloudformationResource: AWS::MediaTailor::PlaybackConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediatailor as mediatailor
        
        # configuration_aliases: Any
        
        cfn_playback_configuration = mediatailor.CfnPlaybackConfiguration(self, "MyCfnPlaybackConfiguration",
            ad_decision_server_url="adDecisionServerUrl",
            name="name",
            video_content_source_url="videoContentSourceUrl",
        
            # the properties below are optional
            avail_suppression=mediatailor.CfnPlaybackConfiguration.AvailSuppressionProperty(
                mode="mode",
                value="value"
            ),
            bumper=mediatailor.CfnPlaybackConfiguration.BumperProperty(
                end_url="endUrl",
                start_url="startUrl"
            ),
            cdn_configuration=mediatailor.CfnPlaybackConfiguration.CdnConfigurationProperty(
                ad_segment_url_prefix="adSegmentUrlPrefix",
                content_segment_url_prefix="contentSegmentUrlPrefix"
            ),
            configuration_aliases={
                "configuration_aliases_key": configuration_aliases
            },
            dash_configuration=mediatailor.CfnPlaybackConfiguration.DashConfigurationProperty(
                manifest_endpoint_prefix="manifestEndpointPrefix",
                mpd_location="mpdLocation",
                origin_manifest_type="originManifestType"
            ),
            hls_configuration=mediatailor.CfnPlaybackConfiguration.HlsConfigurationProperty(
                manifest_endpoint_prefix="manifestEndpointPrefix"
            ),
            live_pre_roll_configuration=mediatailor.CfnPlaybackConfiguration.LivePreRollConfigurationProperty(
                ad_decision_server_url="adDecisionServerUrl",
                max_duration_seconds=123
            ),
            manifest_processing_rules=mediatailor.CfnPlaybackConfiguration.ManifestProcessingRulesProperty(
                ad_marker_passthrough=mediatailor.CfnPlaybackConfiguration.AdMarkerPassthroughProperty(
                    enabled=False
                )
            ),
            personalization_threshold_seconds=123,
            slate_ad_url="slateAdUrl",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transcode_profile_name="transcodeProfileName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        ad_decision_server_url: builtins.str,
        name: builtins.str,
        video_content_source_url: builtins.str,
        avail_suppression: typing.Optional[typing.Union[typing.Union["CfnPlaybackConfiguration.AvailSuppressionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        bumper: typing.Optional[typing.Union[typing.Union["CfnPlaybackConfiguration.BumperProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cdn_configuration: typing.Optional[typing.Union[typing.Union["CfnPlaybackConfiguration.CdnConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        configuration_aliases: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]] = None,
        dash_configuration: typing.Optional[typing.Union[typing.Union["CfnPlaybackConfiguration.DashConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        hls_configuration: typing.Optional[typing.Union[typing.Union["CfnPlaybackConfiguration.HlsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        live_pre_roll_configuration: typing.Optional[typing.Union[typing.Union["CfnPlaybackConfiguration.LivePreRollConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        manifest_processing_rules: typing.Optional[typing.Union[typing.Union["CfnPlaybackConfiguration.ManifestProcessingRulesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        personalization_threshold_seconds: typing.Optional[jsii.Number] = None,
        slate_ad_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        transcode_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::MediaTailor::PlaybackConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ad_decision_server_url: ``AWS::MediaTailor::PlaybackConfiguration.AdDecisionServerUrl``.
        :param name: ``AWS::MediaTailor::PlaybackConfiguration.Name``.
        :param video_content_source_url: ``AWS::MediaTailor::PlaybackConfiguration.VideoContentSourceUrl``.
        :param avail_suppression: ``AWS::MediaTailor::PlaybackConfiguration.AvailSuppression``.
        :param bumper: ``AWS::MediaTailor::PlaybackConfiguration.Bumper``.
        :param cdn_configuration: ``AWS::MediaTailor::PlaybackConfiguration.CdnConfiguration``.
        :param configuration_aliases: The player parameters and aliases used as dynamic variables during session initialization. For more information, see `Domain Variables <https://docs.aws.amazon.com/mediatailor/latest/ug/variables-domain.html>`_ .
        :param dash_configuration: ``AWS::MediaTailor::PlaybackConfiguration.DashConfiguration``.
        :param hls_configuration: The configuration for HLS content.
        :param live_pre_roll_configuration: ``AWS::MediaTailor::PlaybackConfiguration.LivePreRollConfiguration``.
        :param manifest_processing_rules: ``AWS::MediaTailor::PlaybackConfiguration.ManifestProcessingRules``.
        :param personalization_threshold_seconds: ``AWS::MediaTailor::PlaybackConfiguration.PersonalizationThresholdSeconds``.
        :param slate_ad_url: ``AWS::MediaTailor::PlaybackConfiguration.SlateAdUrl``.
        :param tags: ``AWS::MediaTailor::PlaybackConfiguration.Tags``.
        :param transcode_profile_name: ``AWS::MediaTailor::PlaybackConfiguration.TranscodeProfileName``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457460c2c5b29c71ca582ce4ceb9b0dff73319fc192ea729f3190c3df2d2f802)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPlaybackConfigurationProps(
            ad_decision_server_url=ad_decision_server_url,
            name=name,
            video_content_source_url=video_content_source_url,
            avail_suppression=avail_suppression,
            bumper=bumper,
            cdn_configuration=cdn_configuration,
            configuration_aliases=configuration_aliases,
            dash_configuration=dash_configuration,
            hls_configuration=hls_configuration,
            live_pre_roll_configuration=live_pre_roll_configuration,
            manifest_processing_rules=manifest_processing_rules,
            personalization_threshold_seconds=personalization_threshold_seconds,
            slate_ad_url=slate_ad_url,
            tags=tags,
            transcode_profile_name=transcode_profile_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7bd7810d57d6aa391ea820da68cd68cf5d6ec7420a76d5ad1aaa8936224473)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c23debe2e7354cecb12019bb98abb5c3db662509a1556964fd0e26582e090273)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDashConfigurationManifestEndpointPrefix")
    def attr_dash_configuration_manifest_endpoint_prefix(self) -> builtins.str:
        '''The URL generated by MediaTailor to initiate a playback session.

        The session uses server-side reporting. This setting is ignored in PUT operations.

        :cloudformationAttribute: DashConfiguration.ManifestEndpointPrefix
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDashConfigurationManifestEndpointPrefix"))

    @builtins.property
    @jsii.member(jsii_name="attrHlsConfigurationManifestEndpointPrefix")
    def attr_hls_configuration_manifest_endpoint_prefix(self) -> builtins.str:
        '''The URL that is used to initiate a playback session for devices that support Apple HLS.

        The session uses server-side reporting.

        :cloudformationAttribute: HlsConfiguration.ManifestEndpointPrefix
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHlsConfigurationManifestEndpointPrefix"))

    @builtins.property
    @jsii.member(jsii_name="attrPlaybackConfigurationArn")
    def attr_playback_configuration_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the playback configuration.

        :cloudformationAttribute: PlaybackConfigurationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPlaybackConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPlaybackEndpointPrefix")
    def attr_playback_endpoint_prefix(self) -> builtins.str:
        '''The URL that the player accesses to get a manifest from MediaTailor .

        This session will use server-side reporting.

        :cloudformationAttribute: PlaybackEndpointPrefix
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPlaybackEndpointPrefix"))

    @builtins.property
    @jsii.member(jsii_name="attrSessionInitializationEndpointPrefix")
    def attr_session_initialization_endpoint_prefix(self) -> builtins.str:
        '''The URL that the player uses to initialize a session that uses client-side reporting.

        :cloudformationAttribute: SessionInitializationEndpointPrefix
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSessionInitializationEndpointPrefix"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::MediaTailor::PlaybackConfiguration.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="adDecisionServerUrl")
    def ad_decision_server_url(self) -> builtins.str:
        '''``AWS::MediaTailor::PlaybackConfiguration.AdDecisionServerUrl``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-addecisionserverurl
        '''
        return typing.cast(builtins.str, jsii.get(self, "adDecisionServerUrl"))

    @ad_decision_server_url.setter
    def ad_decision_server_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd1d466ce0ffd4daef6139ace24b68a6294e0f70a285a728eeefe23f45dee85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adDecisionServerUrl", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::MediaTailor::PlaybackConfiguration.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88b41276138b2aacdca2ee650f2879688cbd935c291ea7cc1d7b527deca2849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="videoContentSourceUrl")
    def video_content_source_url(self) -> builtins.str:
        '''``AWS::MediaTailor::PlaybackConfiguration.VideoContentSourceUrl``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-videocontentsourceurl
        '''
        return typing.cast(builtins.str, jsii.get(self, "videoContentSourceUrl"))

    @video_content_source_url.setter
    def video_content_source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b9a77af5a51d9dcd700cb69388c32f6c76e2c41230b08f769858dc6cfc3662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "videoContentSourceUrl", value)

    @builtins.property
    @jsii.member(jsii_name="availSuppression")
    def avail_suppression(
        self,
    ) -> typing.Optional[typing.Union["CfnPlaybackConfiguration.AvailSuppressionProperty", _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.AvailSuppression``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-availsuppression
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPlaybackConfiguration.AvailSuppressionProperty", _IResolvable_a771d0ef]], jsii.get(self, "availSuppression"))

    @avail_suppression.setter
    def avail_suppression(
        self,
        value: typing.Optional[typing.Union["CfnPlaybackConfiguration.AvailSuppressionProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3c6c59d7f18cf1773f45d773c98a47761277c2bcafe1419c3dce0c3fa9e314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availSuppression", value)

    @builtins.property
    @jsii.member(jsii_name="bumper")
    def bumper(
        self,
    ) -> typing.Optional[typing.Union["CfnPlaybackConfiguration.BumperProperty", _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.Bumper``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-bumper
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPlaybackConfiguration.BumperProperty", _IResolvable_a771d0ef]], jsii.get(self, "bumper"))

    @bumper.setter
    def bumper(
        self,
        value: typing.Optional[typing.Union["CfnPlaybackConfiguration.BumperProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0641b25ed4f76d60db48c3623779a871e32ef859cfb4334827e332abe2d86bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bumper", value)

    @builtins.property
    @jsii.member(jsii_name="cdnConfiguration")
    def cdn_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnPlaybackConfiguration.CdnConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.CdnConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-cdnconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPlaybackConfiguration.CdnConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "cdnConfiguration"))

    @cdn_configuration.setter
    def cdn_configuration(
        self,
        value: typing.Optional[typing.Union["CfnPlaybackConfiguration.CdnConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3390509fc59bce563b12ade2b9e08967c6bcf15c6126dd6d70ee6d41e1370a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="configurationAliases")
    def configuration_aliases(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]]:
        '''The player parameters and aliases used as dynamic variables during session initialization.

        For more information, see `Domain Variables <https://docs.aws.amazon.com/mediatailor/latest/ug/variables-domain.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-configurationaliases
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]], jsii.get(self, "configurationAliases"))

    @configuration_aliases.setter
    def configuration_aliases(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f1d9aa5d53d760560a700a95cf5039456e543a26a2991f57bd6e53a5645f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationAliases", value)

    @builtins.property
    @jsii.member(jsii_name="dashConfiguration")
    def dash_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnPlaybackConfiguration.DashConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.DashConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPlaybackConfiguration.DashConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "dashConfiguration"))

    @dash_configuration.setter
    def dash_configuration(
        self,
        value: typing.Optional[typing.Union["CfnPlaybackConfiguration.DashConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f61a69a4096cd3f6733bccb3652bb55a842649b272e6fce528eb03e3904c44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="hlsConfiguration")
    def hls_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnPlaybackConfiguration.HlsConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The configuration for HLS content.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-hlsconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPlaybackConfiguration.HlsConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "hlsConfiguration"))

    @hls_configuration.setter
    def hls_configuration(
        self,
        value: typing.Optional[typing.Union["CfnPlaybackConfiguration.HlsConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a777de677890a8ff958ce0fac28f9de7b466555f670e90861fdf2839c03853d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hlsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="livePreRollConfiguration")
    def live_pre_roll_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnPlaybackConfiguration.LivePreRollConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.LivePreRollConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-liveprerollconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPlaybackConfiguration.LivePreRollConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "livePreRollConfiguration"))

    @live_pre_roll_configuration.setter
    def live_pre_roll_configuration(
        self,
        value: typing.Optional[typing.Union["CfnPlaybackConfiguration.LivePreRollConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1b84da61bc0027c1142f55aa97be4998b9d111e69b2fadb8115d1a2a674848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "livePreRollConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="manifestProcessingRules")
    def manifest_processing_rules(
        self,
    ) -> typing.Optional[typing.Union["CfnPlaybackConfiguration.ManifestProcessingRulesProperty", _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.ManifestProcessingRules``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-manifestprocessingrules
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPlaybackConfiguration.ManifestProcessingRulesProperty", _IResolvable_a771d0ef]], jsii.get(self, "manifestProcessingRules"))

    @manifest_processing_rules.setter
    def manifest_processing_rules(
        self,
        value: typing.Optional[typing.Union["CfnPlaybackConfiguration.ManifestProcessingRulesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac497ae9814611add9e723f13efd422dcc562d585f487f5a5d5e9e15c8135a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifestProcessingRules", value)

    @builtins.property
    @jsii.member(jsii_name="personalizationThresholdSeconds")
    def personalization_threshold_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::MediaTailor::PlaybackConfiguration.PersonalizationThresholdSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-personalizationthresholdseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "personalizationThresholdSeconds"))

    @personalization_threshold_seconds.setter
    def personalization_threshold_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005ddb6cc27c743bf57c38e726e8170e8aa5e8e4dd2c1b1e6de87949e37e00b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "personalizationThresholdSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="slateAdUrl")
    def slate_ad_url(self) -> typing.Optional[builtins.str]:
        '''``AWS::MediaTailor::PlaybackConfiguration.SlateAdUrl``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-slateadurl
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slateAdUrl"))

    @slate_ad_url.setter
    def slate_ad_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f649f95ce7e1f8ac60e2016c7b260fe410d78bda897f77394a53c646ea2c4b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slateAdUrl", value)

    @builtins.property
    @jsii.member(jsii_name="transcodeProfileName")
    def transcode_profile_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::MediaTailor::PlaybackConfiguration.TranscodeProfileName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-transcodeprofilename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transcodeProfileName"))

    @transcode_profile_name.setter
    def transcode_profile_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7abc09a21f868f0d966471f2ed4e9c2a4b7ccd3182199bc0c5ebb1829ee0168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transcodeProfileName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration.AdMarkerPassthroughProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class AdMarkerPassthroughProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnPlaybackConfiguration.AdMarkerPassthroughProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-admarkerpassthrough.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediatailor as mediatailor
                
                ad_marker_passthrough_property = mediatailor.CfnPlaybackConfiguration.AdMarkerPassthroughProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f674bccf97e23f109f4400c41a299fde389d46f98dbd6e8300996cc0a054e89)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnPlaybackConfiguration.AdMarkerPassthroughProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-admarkerpassthrough.html#cfn-mediatailor-playbackconfiguration-admarkerpassthrough-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdMarkerPassthroughProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration.AvailSuppressionProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode", "value": "value"},
    )
    class AvailSuppressionProperty:
        def __init__(
            self,
            *,
            mode: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param mode: ``CfnPlaybackConfiguration.AvailSuppressionProperty.Mode``.
            :param value: ``CfnPlaybackConfiguration.AvailSuppressionProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-availsuppression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediatailor as mediatailor
                
                avail_suppression_property = mediatailor.CfnPlaybackConfiguration.AvailSuppressionProperty(
                    mode="mode",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af29250e2c226e2e17cfb5a52f9b05c99cf839d4eae77edad57b729341b1258d)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''``CfnPlaybackConfiguration.AvailSuppressionProperty.Mode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-availsuppression.html#cfn-mediatailor-playbackconfiguration-availsuppression-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnPlaybackConfiguration.AvailSuppressionProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-availsuppression.html#cfn-mediatailor-playbackconfiguration-availsuppression-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AvailSuppressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration.BumperProperty",
        jsii_struct_bases=[],
        name_mapping={"end_url": "endUrl", "start_url": "startUrl"},
    )
    class BumperProperty:
        def __init__(
            self,
            *,
            end_url: typing.Optional[builtins.str] = None,
            start_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param end_url: ``CfnPlaybackConfiguration.BumperProperty.EndUrl``.
            :param start_url: ``CfnPlaybackConfiguration.BumperProperty.StartUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-bumper.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediatailor as mediatailor
                
                bumper_property = mediatailor.CfnPlaybackConfiguration.BumperProperty(
                    end_url="endUrl",
                    start_url="startUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__028f3dbe0550799aaff864d75131930f3b49aa11baef846d9f7331ada6de3ccb)
                check_type(argname="argument end_url", value=end_url, expected_type=type_hints["end_url"])
                check_type(argname="argument start_url", value=start_url, expected_type=type_hints["start_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_url is not None:
                self._values["end_url"] = end_url
            if start_url is not None:
                self._values["start_url"] = start_url

        @builtins.property
        def end_url(self) -> typing.Optional[builtins.str]:
            '''``CfnPlaybackConfiguration.BumperProperty.EndUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-bumper.html#cfn-mediatailor-playbackconfiguration-bumper-endurl
            '''
            result = self._values.get("end_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_url(self) -> typing.Optional[builtins.str]:
            '''``CfnPlaybackConfiguration.BumperProperty.StartUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-bumper.html#cfn-mediatailor-playbackconfiguration-bumper-starturl
            '''
            result = self._values.get("start_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BumperProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration.CdnConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_segment_url_prefix": "adSegmentUrlPrefix",
            "content_segment_url_prefix": "contentSegmentUrlPrefix",
        },
    )
    class CdnConfigurationProperty:
        def __init__(
            self,
            *,
            ad_segment_url_prefix: typing.Optional[builtins.str] = None,
            content_segment_url_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param ad_segment_url_prefix: ``CfnPlaybackConfiguration.CdnConfigurationProperty.AdSegmentUrlPrefix``.
            :param content_segment_url_prefix: ``CfnPlaybackConfiguration.CdnConfigurationProperty.ContentSegmentUrlPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-cdnconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediatailor as mediatailor
                
                cdn_configuration_property = mediatailor.CfnPlaybackConfiguration.CdnConfigurationProperty(
                    ad_segment_url_prefix="adSegmentUrlPrefix",
                    content_segment_url_prefix="contentSegmentUrlPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__931902ba833f0d67da23a5eb2a4e7d3de3cdb9404b3dc528f3bd2d513b1161ab)
                check_type(argname="argument ad_segment_url_prefix", value=ad_segment_url_prefix, expected_type=type_hints["ad_segment_url_prefix"])
                check_type(argname="argument content_segment_url_prefix", value=content_segment_url_prefix, expected_type=type_hints["content_segment_url_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_segment_url_prefix is not None:
                self._values["ad_segment_url_prefix"] = ad_segment_url_prefix
            if content_segment_url_prefix is not None:
                self._values["content_segment_url_prefix"] = content_segment_url_prefix

        @builtins.property
        def ad_segment_url_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnPlaybackConfiguration.CdnConfigurationProperty.AdSegmentUrlPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-cdnconfiguration.html#cfn-mediatailor-playbackconfiguration-cdnconfiguration-adsegmenturlprefix
            '''
            result = self._values.get("ad_segment_url_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def content_segment_url_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnPlaybackConfiguration.CdnConfigurationProperty.ContentSegmentUrlPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-cdnconfiguration.html#cfn-mediatailor-playbackconfiguration-cdnconfiguration-contentsegmenturlprefix
            '''
            result = self._values.get("content_segment_url_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CdnConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration.DashConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "manifest_endpoint_prefix": "manifestEndpointPrefix",
            "mpd_location": "mpdLocation",
            "origin_manifest_type": "originManifestType",
        },
    )
    class DashConfigurationProperty:
        def __init__(
            self,
            *,
            manifest_endpoint_prefix: typing.Optional[builtins.str] = None,
            mpd_location: typing.Optional[builtins.str] = None,
            origin_manifest_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for DASH content.

            :param manifest_endpoint_prefix: The URL generated by MediaTailor to initiate a playback session. The session uses server-side reporting. This setting is ignored in PUT operations.
            :param mpd_location: The setting that controls whether MediaTailor includes the Location tag in DASH manifests. MediaTailor populates the Location tag with the URL for manifest update requests, to be used by players that don't support sticky redirects. Disable this if you have CDN routing rules set up for accessing MediaTailor manifests, and you are either using client-side reporting or your players support sticky HTTP redirects. Valid values are ``DISABLED`` and ``EMT_DEFAULT`` . The ``EMT_DEFAULT`` setting enables the inclusion of the tag and is the default value.
            :param origin_manifest_type: The setting that controls whether MediaTailor handles manifests from the origin server as multi-period manifests or single-period manifests. If your origin server produces single-period manifests, set this to ``SINGLE_PERIOD`` . The default setting is ``MULTI_PERIOD`` . For multi-period manifests, omit this setting or set it to ``MULTI_PERIOD`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-dashconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediatailor as mediatailor
                
                dash_configuration_property = mediatailor.CfnPlaybackConfiguration.DashConfigurationProperty(
                    manifest_endpoint_prefix="manifestEndpointPrefix",
                    mpd_location="mpdLocation",
                    origin_manifest_type="originManifestType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5df6187e4a2caac05a0f64d7f95c2990dd6a9164c164b9d48c8c18b75b1aae60)
                check_type(argname="argument manifest_endpoint_prefix", value=manifest_endpoint_prefix, expected_type=type_hints["manifest_endpoint_prefix"])
                check_type(argname="argument mpd_location", value=mpd_location, expected_type=type_hints["mpd_location"])
                check_type(argname="argument origin_manifest_type", value=origin_manifest_type, expected_type=type_hints["origin_manifest_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_endpoint_prefix is not None:
                self._values["manifest_endpoint_prefix"] = manifest_endpoint_prefix
            if mpd_location is not None:
                self._values["mpd_location"] = mpd_location
            if origin_manifest_type is not None:
                self._values["origin_manifest_type"] = origin_manifest_type

        @builtins.property
        def manifest_endpoint_prefix(self) -> typing.Optional[builtins.str]:
            '''The URL generated by MediaTailor to initiate a playback session.

            The session uses server-side reporting. This setting is ignored in PUT operations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-dashconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration-manifestendpointprefix
            '''
            result = self._values.get("manifest_endpoint_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mpd_location(self) -> typing.Optional[builtins.str]:
            '''The setting that controls whether MediaTailor includes the Location tag in DASH manifests.

            MediaTailor populates the Location tag with the URL for manifest update requests, to be used by players that don't support sticky redirects. Disable this if you have CDN routing rules set up for accessing MediaTailor manifests, and you are either using client-side reporting or your players support sticky HTTP redirects. Valid values are ``DISABLED`` and ``EMT_DEFAULT`` . The ``EMT_DEFAULT`` setting enables the inclusion of the tag and is the default value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-dashconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration-mpdlocation
            '''
            result = self._values.get("mpd_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def origin_manifest_type(self) -> typing.Optional[builtins.str]:
            '''The setting that controls whether MediaTailor handles manifests from the origin server as multi-period manifests or single-period manifests.

            If your origin server produces single-period manifests, set this to ``SINGLE_PERIOD`` . The default setting is ``MULTI_PERIOD`` . For multi-period manifests, omit this setting or set it to ``MULTI_PERIOD`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-dashconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration-originmanifesttype
            '''
            result = self._values.get("origin_manifest_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration.HlsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"manifest_endpoint_prefix": "manifestEndpointPrefix"},
    )
    class HlsConfigurationProperty:
        def __init__(
            self,
            *,
            manifest_endpoint_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for HLS content.

            :param manifest_endpoint_prefix: The URL that is used to initiate a playback session for devices that support Apple HLS. The session uses server-side reporting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-hlsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediatailor as mediatailor
                
                hls_configuration_property = mediatailor.CfnPlaybackConfiguration.HlsConfigurationProperty(
                    manifest_endpoint_prefix="manifestEndpointPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4a198608d11ef9ba008b3e5678f6acd19537dd8af5bbe688609f99d388d3626)
                check_type(argname="argument manifest_endpoint_prefix", value=manifest_endpoint_prefix, expected_type=type_hints["manifest_endpoint_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_endpoint_prefix is not None:
                self._values["manifest_endpoint_prefix"] = manifest_endpoint_prefix

        @builtins.property
        def manifest_endpoint_prefix(self) -> typing.Optional[builtins.str]:
            '''The URL that is used to initiate a playback session for devices that support Apple HLS.

            The session uses server-side reporting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-hlsconfiguration.html#cfn-mediatailor-playbackconfiguration-hlsconfiguration-manifestendpointprefix
            '''
            result = self._values.get("manifest_endpoint_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration.LivePreRollConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_decision_server_url": "adDecisionServerUrl",
            "max_duration_seconds": "maxDurationSeconds",
        },
    )
    class LivePreRollConfigurationProperty:
        def __init__(
            self,
            *,
            ad_decision_server_url: typing.Optional[builtins.str] = None,
            max_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param ad_decision_server_url: ``CfnPlaybackConfiguration.LivePreRollConfigurationProperty.AdDecisionServerUrl``.
            :param max_duration_seconds: ``CfnPlaybackConfiguration.LivePreRollConfigurationProperty.MaxDurationSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-liveprerollconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediatailor as mediatailor
                
                live_pre_roll_configuration_property = mediatailor.CfnPlaybackConfiguration.LivePreRollConfigurationProperty(
                    ad_decision_server_url="adDecisionServerUrl",
                    max_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8353984a1b3ad9b67c31a40c018bf9d71bd6cca3bcd0277318fc8b7ca3217356)
                check_type(argname="argument ad_decision_server_url", value=ad_decision_server_url, expected_type=type_hints["ad_decision_server_url"])
                check_type(argname="argument max_duration_seconds", value=max_duration_seconds, expected_type=type_hints["max_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_decision_server_url is not None:
                self._values["ad_decision_server_url"] = ad_decision_server_url
            if max_duration_seconds is not None:
                self._values["max_duration_seconds"] = max_duration_seconds

        @builtins.property
        def ad_decision_server_url(self) -> typing.Optional[builtins.str]:
            '''``CfnPlaybackConfiguration.LivePreRollConfigurationProperty.AdDecisionServerUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-liveprerollconfiguration.html#cfn-mediatailor-playbackconfiguration-liveprerollconfiguration-addecisionserverurl
            '''
            result = self._values.get("ad_decision_server_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnPlaybackConfiguration.LivePreRollConfigurationProperty.MaxDurationSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-liveprerollconfiguration.html#cfn-mediatailor-playbackconfiguration-liveprerollconfiguration-maxdurationseconds
            '''
            result = self._values.get("max_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LivePreRollConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfiguration.ManifestProcessingRulesProperty",
        jsii_struct_bases=[],
        name_mapping={"ad_marker_passthrough": "adMarkerPassthrough"},
    )
    class ManifestProcessingRulesProperty:
        def __init__(
            self,
            *,
            ad_marker_passthrough: typing.Optional[typing.Union[typing.Union["CfnPlaybackConfiguration.AdMarkerPassthroughProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param ad_marker_passthrough: ``CfnPlaybackConfiguration.ManifestProcessingRulesProperty.AdMarkerPassthrough``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-manifestprocessingrules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediatailor as mediatailor
                
                manifest_processing_rules_property = mediatailor.CfnPlaybackConfiguration.ManifestProcessingRulesProperty(
                    ad_marker_passthrough=mediatailor.CfnPlaybackConfiguration.AdMarkerPassthroughProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18d3f1a918a8e299ff09cf38cc52dc366fb34d92f79c7b8280a0a663a6d6ca33)
                check_type(argname="argument ad_marker_passthrough", value=ad_marker_passthrough, expected_type=type_hints["ad_marker_passthrough"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_marker_passthrough is not None:
                self._values["ad_marker_passthrough"] = ad_marker_passthrough

        @builtins.property
        def ad_marker_passthrough(
            self,
        ) -> typing.Optional[typing.Union["CfnPlaybackConfiguration.AdMarkerPassthroughProperty", _IResolvable_a771d0ef]]:
            '''``CfnPlaybackConfiguration.ManifestProcessingRulesProperty.AdMarkerPassthrough``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediatailor-playbackconfiguration-manifestprocessingrules.html#cfn-mediatailor-playbackconfiguration-manifestprocessingrules-admarkerpassthrough
            '''
            result = self._values.get("ad_marker_passthrough")
            return typing.cast(typing.Optional[typing.Union["CfnPlaybackConfiguration.AdMarkerPassthroughProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestProcessingRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediatailor.CfnPlaybackConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "ad_decision_server_url": "adDecisionServerUrl",
        "name": "name",
        "video_content_source_url": "videoContentSourceUrl",
        "avail_suppression": "availSuppression",
        "bumper": "bumper",
        "cdn_configuration": "cdnConfiguration",
        "configuration_aliases": "configurationAliases",
        "dash_configuration": "dashConfiguration",
        "hls_configuration": "hlsConfiguration",
        "live_pre_roll_configuration": "livePreRollConfiguration",
        "manifest_processing_rules": "manifestProcessingRules",
        "personalization_threshold_seconds": "personalizationThresholdSeconds",
        "slate_ad_url": "slateAdUrl",
        "tags": "tags",
        "transcode_profile_name": "transcodeProfileName",
    },
)
class CfnPlaybackConfigurationProps:
    def __init__(
        self,
        *,
        ad_decision_server_url: builtins.str,
        name: builtins.str,
        video_content_source_url: builtins.str,
        avail_suppression: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.AvailSuppressionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        bumper: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.BumperProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cdn_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.CdnConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        configuration_aliases: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]] = None,
        dash_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.DashConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        hls_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.HlsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        live_pre_roll_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.LivePreRollConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        manifest_processing_rules: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.ManifestProcessingRulesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        personalization_threshold_seconds: typing.Optional[jsii.Number] = None,
        slate_ad_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        transcode_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPlaybackConfiguration``.

        :param ad_decision_server_url: ``AWS::MediaTailor::PlaybackConfiguration.AdDecisionServerUrl``.
        :param name: ``AWS::MediaTailor::PlaybackConfiguration.Name``.
        :param video_content_source_url: ``AWS::MediaTailor::PlaybackConfiguration.VideoContentSourceUrl``.
        :param avail_suppression: ``AWS::MediaTailor::PlaybackConfiguration.AvailSuppression``.
        :param bumper: ``AWS::MediaTailor::PlaybackConfiguration.Bumper``.
        :param cdn_configuration: ``AWS::MediaTailor::PlaybackConfiguration.CdnConfiguration``.
        :param configuration_aliases: The player parameters and aliases used as dynamic variables during session initialization. For more information, see `Domain Variables <https://docs.aws.amazon.com/mediatailor/latest/ug/variables-domain.html>`_ .
        :param dash_configuration: ``AWS::MediaTailor::PlaybackConfiguration.DashConfiguration``.
        :param hls_configuration: The configuration for HLS content.
        :param live_pre_roll_configuration: ``AWS::MediaTailor::PlaybackConfiguration.LivePreRollConfiguration``.
        :param manifest_processing_rules: ``AWS::MediaTailor::PlaybackConfiguration.ManifestProcessingRules``.
        :param personalization_threshold_seconds: ``AWS::MediaTailor::PlaybackConfiguration.PersonalizationThresholdSeconds``.
        :param slate_ad_url: ``AWS::MediaTailor::PlaybackConfiguration.SlateAdUrl``.
        :param tags: ``AWS::MediaTailor::PlaybackConfiguration.Tags``.
        :param transcode_profile_name: ``AWS::MediaTailor::PlaybackConfiguration.TranscodeProfileName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediatailor as mediatailor
            
            # configuration_aliases: Any
            
            cfn_playback_configuration_props = mediatailor.CfnPlaybackConfigurationProps(
                ad_decision_server_url="adDecisionServerUrl",
                name="name",
                video_content_source_url="videoContentSourceUrl",
            
                # the properties below are optional
                avail_suppression=mediatailor.CfnPlaybackConfiguration.AvailSuppressionProperty(
                    mode="mode",
                    value="value"
                ),
                bumper=mediatailor.CfnPlaybackConfiguration.BumperProperty(
                    end_url="endUrl",
                    start_url="startUrl"
                ),
                cdn_configuration=mediatailor.CfnPlaybackConfiguration.CdnConfigurationProperty(
                    ad_segment_url_prefix="adSegmentUrlPrefix",
                    content_segment_url_prefix="contentSegmentUrlPrefix"
                ),
                configuration_aliases={
                    "configuration_aliases_key": configuration_aliases
                },
                dash_configuration=mediatailor.CfnPlaybackConfiguration.DashConfigurationProperty(
                    manifest_endpoint_prefix="manifestEndpointPrefix",
                    mpd_location="mpdLocation",
                    origin_manifest_type="originManifestType"
                ),
                hls_configuration=mediatailor.CfnPlaybackConfiguration.HlsConfigurationProperty(
                    manifest_endpoint_prefix="manifestEndpointPrefix"
                ),
                live_pre_roll_configuration=mediatailor.CfnPlaybackConfiguration.LivePreRollConfigurationProperty(
                    ad_decision_server_url="adDecisionServerUrl",
                    max_duration_seconds=123
                ),
                manifest_processing_rules=mediatailor.CfnPlaybackConfiguration.ManifestProcessingRulesProperty(
                    ad_marker_passthrough=mediatailor.CfnPlaybackConfiguration.AdMarkerPassthroughProperty(
                        enabled=False
                    )
                ),
                personalization_threshold_seconds=123,
                slate_ad_url="slateAdUrl",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transcode_profile_name="transcodeProfileName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308981c0e11cc4d9ff1ca288fd3e497fc4ccf13208b61497881d664d4a71a561)
            check_type(argname="argument ad_decision_server_url", value=ad_decision_server_url, expected_type=type_hints["ad_decision_server_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument video_content_source_url", value=video_content_source_url, expected_type=type_hints["video_content_source_url"])
            check_type(argname="argument avail_suppression", value=avail_suppression, expected_type=type_hints["avail_suppression"])
            check_type(argname="argument bumper", value=bumper, expected_type=type_hints["bumper"])
            check_type(argname="argument cdn_configuration", value=cdn_configuration, expected_type=type_hints["cdn_configuration"])
            check_type(argname="argument configuration_aliases", value=configuration_aliases, expected_type=type_hints["configuration_aliases"])
            check_type(argname="argument dash_configuration", value=dash_configuration, expected_type=type_hints["dash_configuration"])
            check_type(argname="argument hls_configuration", value=hls_configuration, expected_type=type_hints["hls_configuration"])
            check_type(argname="argument live_pre_roll_configuration", value=live_pre_roll_configuration, expected_type=type_hints["live_pre_roll_configuration"])
            check_type(argname="argument manifest_processing_rules", value=manifest_processing_rules, expected_type=type_hints["manifest_processing_rules"])
            check_type(argname="argument personalization_threshold_seconds", value=personalization_threshold_seconds, expected_type=type_hints["personalization_threshold_seconds"])
            check_type(argname="argument slate_ad_url", value=slate_ad_url, expected_type=type_hints["slate_ad_url"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transcode_profile_name", value=transcode_profile_name, expected_type=type_hints["transcode_profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ad_decision_server_url": ad_decision_server_url,
            "name": name,
            "video_content_source_url": video_content_source_url,
        }
        if avail_suppression is not None:
            self._values["avail_suppression"] = avail_suppression
        if bumper is not None:
            self._values["bumper"] = bumper
        if cdn_configuration is not None:
            self._values["cdn_configuration"] = cdn_configuration
        if configuration_aliases is not None:
            self._values["configuration_aliases"] = configuration_aliases
        if dash_configuration is not None:
            self._values["dash_configuration"] = dash_configuration
        if hls_configuration is not None:
            self._values["hls_configuration"] = hls_configuration
        if live_pre_roll_configuration is not None:
            self._values["live_pre_roll_configuration"] = live_pre_roll_configuration
        if manifest_processing_rules is not None:
            self._values["manifest_processing_rules"] = manifest_processing_rules
        if personalization_threshold_seconds is not None:
            self._values["personalization_threshold_seconds"] = personalization_threshold_seconds
        if slate_ad_url is not None:
            self._values["slate_ad_url"] = slate_ad_url
        if tags is not None:
            self._values["tags"] = tags
        if transcode_profile_name is not None:
            self._values["transcode_profile_name"] = transcode_profile_name

    @builtins.property
    def ad_decision_server_url(self) -> builtins.str:
        '''``AWS::MediaTailor::PlaybackConfiguration.AdDecisionServerUrl``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-addecisionserverurl
        '''
        result = self._values.get("ad_decision_server_url")
        assert result is not None, "Required property 'ad_decision_server_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::MediaTailor::PlaybackConfiguration.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def video_content_source_url(self) -> builtins.str:
        '''``AWS::MediaTailor::PlaybackConfiguration.VideoContentSourceUrl``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-videocontentsourceurl
        '''
        result = self._values.get("video_content_source_url")
        assert result is not None, "Required property 'video_content_source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avail_suppression(
        self,
    ) -> typing.Optional[typing.Union[CfnPlaybackConfiguration.AvailSuppressionProperty, _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.AvailSuppression``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-availsuppression
        '''
        result = self._values.get("avail_suppression")
        return typing.cast(typing.Optional[typing.Union[CfnPlaybackConfiguration.AvailSuppressionProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def bumper(
        self,
    ) -> typing.Optional[typing.Union[CfnPlaybackConfiguration.BumperProperty, _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.Bumper``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-bumper
        '''
        result = self._values.get("bumper")
        return typing.cast(typing.Optional[typing.Union[CfnPlaybackConfiguration.BumperProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cdn_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnPlaybackConfiguration.CdnConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.CdnConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-cdnconfiguration
        '''
        result = self._values.get("cdn_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnPlaybackConfiguration.CdnConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def configuration_aliases(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]]:
        '''The player parameters and aliases used as dynamic variables during session initialization.

        For more information, see `Domain Variables <https://docs.aws.amazon.com/mediatailor/latest/ug/variables-domain.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-configurationaliases
        '''
        result = self._values.get("configuration_aliases")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]], result)

    @builtins.property
    def dash_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnPlaybackConfiguration.DashConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.DashConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-dashconfiguration
        '''
        result = self._values.get("dash_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnPlaybackConfiguration.DashConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def hls_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnPlaybackConfiguration.HlsConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The configuration for HLS content.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-hlsconfiguration
        '''
        result = self._values.get("hls_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnPlaybackConfiguration.HlsConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def live_pre_roll_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnPlaybackConfiguration.LivePreRollConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.LivePreRollConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-liveprerollconfiguration
        '''
        result = self._values.get("live_pre_roll_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnPlaybackConfiguration.LivePreRollConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def manifest_processing_rules(
        self,
    ) -> typing.Optional[typing.Union[CfnPlaybackConfiguration.ManifestProcessingRulesProperty, _IResolvable_a771d0ef]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.ManifestProcessingRules``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-manifestprocessingrules
        '''
        result = self._values.get("manifest_processing_rules")
        return typing.cast(typing.Optional[typing.Union[CfnPlaybackConfiguration.ManifestProcessingRulesProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def personalization_threshold_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::MediaTailor::PlaybackConfiguration.PersonalizationThresholdSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-personalizationthresholdseconds
        '''
        result = self._values.get("personalization_threshold_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def slate_ad_url(self) -> typing.Optional[builtins.str]:
        '''``AWS::MediaTailor::PlaybackConfiguration.SlateAdUrl``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-slateadurl
        '''
        result = self._values.get("slate_ad_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::MediaTailor::PlaybackConfiguration.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def transcode_profile_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::MediaTailor::PlaybackConfiguration.TranscodeProfileName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediatailor-playbackconfiguration.html#cfn-mediatailor-playbackconfiguration-transcodeprofilename
        '''
        result = self._values.get("transcode_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlaybackConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnPlaybackConfiguration",
    "CfnPlaybackConfigurationProps",
]

publication.publish()

def _typecheckingstub__457460c2c5b29c71ca582ce4ceb9b0dff73319fc192ea729f3190c3df2d2f802(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    ad_decision_server_url: builtins.str,
    name: builtins.str,
    video_content_source_url: builtins.str,
    avail_suppression: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.AvailSuppressionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    bumper: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.BumperProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cdn_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.CdnConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    configuration_aliases: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]] = None,
    dash_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.DashConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    hls_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.HlsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    live_pre_roll_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.LivePreRollConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    manifest_processing_rules: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.ManifestProcessingRulesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    personalization_threshold_seconds: typing.Optional[jsii.Number] = None,
    slate_ad_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    transcode_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7bd7810d57d6aa391ea820da68cd68cf5d6ec7420a76d5ad1aaa8936224473(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23debe2e7354cecb12019bb98abb5c3db662509a1556964fd0e26582e090273(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd1d466ce0ffd4daef6139ace24b68a6294e0f70a285a728eeefe23f45dee85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88b41276138b2aacdca2ee650f2879688cbd935c291ea7cc1d7b527deca2849(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b9a77af5a51d9dcd700cb69388c32f6c76e2c41230b08f769858dc6cfc3662(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3c6c59d7f18cf1773f45d773c98a47761277c2bcafe1419c3dce0c3fa9e314(
    value: typing.Optional[typing.Union[CfnPlaybackConfiguration.AvailSuppressionProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0641b25ed4f76d60db48c3623779a871e32ef859cfb4334827e332abe2d86bc3(
    value: typing.Optional[typing.Union[CfnPlaybackConfiguration.BumperProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3390509fc59bce563b12ade2b9e08967c6bcf15c6126dd6d70ee6d41e1370a8(
    value: typing.Optional[typing.Union[CfnPlaybackConfiguration.CdnConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f1d9aa5d53d760560a700a95cf5039456e543a26a2991f57bd6e53a5645f7e(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f61a69a4096cd3f6733bccb3652bb55a842649b272e6fce528eb03e3904c44a(
    value: typing.Optional[typing.Union[CfnPlaybackConfiguration.DashConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a777de677890a8ff958ce0fac28f9de7b466555f670e90861fdf2839c03853d(
    value: typing.Optional[typing.Union[CfnPlaybackConfiguration.HlsConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1b84da61bc0027c1142f55aa97be4998b9d111e69b2fadb8115d1a2a674848(
    value: typing.Optional[typing.Union[CfnPlaybackConfiguration.LivePreRollConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac497ae9814611add9e723f13efd422dcc562d585f487f5a5d5e9e15c8135a28(
    value: typing.Optional[typing.Union[CfnPlaybackConfiguration.ManifestProcessingRulesProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005ddb6cc27c743bf57c38e726e8170e8aa5e8e4dd2c1b1e6de87949e37e00b8(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f649f95ce7e1f8ac60e2016c7b260fe410d78bda897f77394a53c646ea2c4b9d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7abc09a21f868f0d966471f2ed4e9c2a4b7ccd3182199bc0c5ebb1829ee0168(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f674bccf97e23f109f4400c41a299fde389d46f98dbd6e8300996cc0a054e89(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af29250e2c226e2e17cfb5a52f9b05c99cf839d4eae77edad57b729341b1258d(
    *,
    mode: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028f3dbe0550799aaff864d75131930f3b49aa11baef846d9f7331ada6de3ccb(
    *,
    end_url: typing.Optional[builtins.str] = None,
    start_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931902ba833f0d67da23a5eb2a4e7d3de3cdb9404b3dc528f3bd2d513b1161ab(
    *,
    ad_segment_url_prefix: typing.Optional[builtins.str] = None,
    content_segment_url_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df6187e4a2caac05a0f64d7f95c2990dd6a9164c164b9d48c8c18b75b1aae60(
    *,
    manifest_endpoint_prefix: typing.Optional[builtins.str] = None,
    mpd_location: typing.Optional[builtins.str] = None,
    origin_manifest_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a198608d11ef9ba008b3e5678f6acd19537dd8af5bbe688609f99d388d3626(
    *,
    manifest_endpoint_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8353984a1b3ad9b67c31a40c018bf9d71bd6cca3bcd0277318fc8b7ca3217356(
    *,
    ad_decision_server_url: typing.Optional[builtins.str] = None,
    max_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d3f1a918a8e299ff09cf38cc52dc366fb34d92f79c7b8280a0a663a6d6ca33(
    *,
    ad_marker_passthrough: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.AdMarkerPassthroughProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308981c0e11cc4d9ff1ca288fd3e497fc4ccf13208b61497881d664d4a71a561(
    *,
    ad_decision_server_url: builtins.str,
    name: builtins.str,
    video_content_source_url: builtins.str,
    avail_suppression: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.AvailSuppressionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    bumper: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.BumperProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cdn_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.CdnConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    configuration_aliases: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Any]]] = None,
    dash_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.DashConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    hls_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.HlsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    live_pre_roll_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.LivePreRollConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    manifest_processing_rules: typing.Optional[typing.Union[typing.Union[CfnPlaybackConfiguration.ManifestProcessingRulesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    personalization_threshold_seconds: typing.Optional[jsii.Number] = None,
    slate_ad_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    transcode_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
