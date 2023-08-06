'''
# Amazon Data Lifecycle Manager Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as dlm
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DLM construct libraries](https://constructs.dev/search?q=dlm)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DLM resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DLM.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DLM](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DLM.html).

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
class CfnLifecyclePolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy",
):
    '''A CloudFormation ``AWS::DLM::LifecyclePolicy``.

    Specifies a lifecycle policy, which is used to automate operations on Amazon EBS resources.

    The properties are required when you add a lifecycle policy and optional when you update a lifecycle policy.

    :cloudformationResource: AWS::DLM::LifecyclePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_dlm as dlm
        
        cfn_lifecycle_policy = dlm.CfnLifecyclePolicy(self, "MyCfnLifecyclePolicy",
            description="description",
            execution_role_arn="executionRoleArn",
            policy_details=dlm.CfnLifecyclePolicy.PolicyDetailsProperty(
                actions=[dlm.CfnLifecyclePolicy.ActionProperty(
                    cross_region_copy=[dlm.CfnLifecyclePolicy.CrossRegionCopyActionProperty(
                        encryption_configuration=dlm.CfnLifecyclePolicy.EncryptionConfigurationProperty(
                            encrypted=False,
        
                            # the properties below are optional
                            cmk_arn="cmkArn"
                        ),
                        target="target",
        
                        # the properties below are optional
                        retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        )
                    )],
                    name="name"
                )],
                event_source=dlm.CfnLifecyclePolicy.EventSourceProperty(
                    type="type",
        
                    # the properties below are optional
                    parameters=dlm.CfnLifecyclePolicy.EventParametersProperty(
                        event_type="eventType",
                        snapshot_owner=["snapshotOwner"],
        
                        # the properties below are optional
                        description_regex="descriptionRegex"
                    )
                ),
                parameters=dlm.CfnLifecyclePolicy.ParametersProperty(
                    exclude_boot_volume=False,
                    exclude_data_volume_tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    no_reboot=False
                ),
                policy_type="policyType",
                resource_locations=["resourceLocations"],
                resource_types=["resourceTypes"],
                schedules=[dlm.CfnLifecyclePolicy.ScheduleProperty(
                    archive_rule=dlm.CfnLifecyclePolicy.ArchiveRuleProperty(
                        retain_rule=dlm.CfnLifecyclePolicy.ArchiveRetainRuleProperty(
                            retention_archive_tier=dlm.CfnLifecyclePolicy.RetentionArchiveTierProperty(
                                count=123,
                                interval=123,
                                interval_unit="intervalUnit"
                            )
                        )
                    ),
                    copy_tags=False,
                    create_rule=dlm.CfnLifecyclePolicy.CreateRuleProperty(
                        cron_expression="cronExpression",
                        interval=123,
                        interval_unit="intervalUnit",
                        location="location",
                        times=["times"]
                    ),
                    cross_region_copy_rules=[dlm.CfnLifecyclePolicy.CrossRegionCopyRuleProperty(
                        encrypted=False,
        
                        # the properties below are optional
                        cmk_arn="cmkArn",
                        copy_tags=False,
                        deprecate_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        target="target",
                        target_region="targetRegion"
                    )],
                    deprecate_rule=dlm.CfnLifecyclePolicy.DeprecateRuleProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    fast_restore_rule=dlm.CfnLifecyclePolicy.FastRestoreRuleProperty(
                        availability_zones=["availabilityZones"],
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    name="name",
                    retain_rule=dlm.CfnLifecyclePolicy.RetainRuleProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    share_rules=[dlm.CfnLifecyclePolicy.ShareRuleProperty(
                        target_accounts=["targetAccounts"],
                        unshare_interval=123,
                        unshare_interval_unit="unshareIntervalUnit"
                    )],
                    tags_to_add=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                target_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            state="state",
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
        description: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        policy_details: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DLM::LifecyclePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the lifecycle policy. The characters ^[0-9A-Za-z _-]+$ are supported.
        :param execution_role_arn: The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.
        :param policy_details: The configuration details of the lifecycle policy.
        :param state: The activation state of the lifecycle policy.
        :param tags: The tags to apply to the lifecycle policy during creation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77301b6dfe6ba608f1b3f2f352c7a49b8d2178faed5a27bdd9320566ac942072)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLifecyclePolicyProps(
            description=description,
            execution_role_arn=execution_role_arn,
            policy_details=policy_details,
            state=state,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f19528d58dbbceb9cf36cbd8dc734b2c4eef8450da7c415995ca30ab277607)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e11c21ead08f7e2d913cb434dc8159f393fae758d684ed03a8f9b2219f87f66b)
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
        '''The Amazon Resource Name (ARN) of the lifecycle policy.

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
        '''The tags to apply to the lifecycle policy during creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the lifecycle policy.

        The characters ^[0-9A-Za-z _-]+$ are supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7405efdae5591a408eeecd8432f4d9f08c4e127a660f3030de44203c3c0922eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-executionrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8905e7a5ebe291c4c37350ab768de403894589a231780c1bd57dc8f745f8e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="policyDetails")
    def policy_details(
        self,
    ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", _IResolvable_a771d0ef]]:
        '''The configuration details of the lifecycle policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-policydetails
        '''
        return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", _IResolvable_a771d0ef]], jsii.get(self, "policyDetails"))

    @policy_details.setter
    def policy_details(
        self,
        value: typing.Optional[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760917f8a84d9a86f51a29e4372964602e0d24abd07422406073fb0c4c68dae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDetails", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The activation state of the lifecycle policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f69033f85aa6e93437b96753874c8e34f5c4ffe06abdf4c788a6dbaa5635280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"cross_region_copy": "crossRegionCopy", "name": "name"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            cross_region_copy: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLifecyclePolicy.CrossRegionCopyActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            name: builtins.str,
        ) -> None:
            '''*[Event-based policies only]* Specifies an action for an event-based policy.

            :param cross_region_copy: The rule for copying shared snapshots across Regions.
            :param name: A descriptive name for the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                action_property = dlm.CfnLifecyclePolicy.ActionProperty(
                    cross_region_copy=[dlm.CfnLifecyclePolicy.CrossRegionCopyActionProperty(
                        encryption_configuration=dlm.CfnLifecyclePolicy.EncryptionConfigurationProperty(
                            encrypted=False,
                
                            # the properties below are optional
                            cmk_arn="cmkArn"
                        ),
                        target="target",
                
                        # the properties below are optional
                        retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        )
                    )],
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eef44f019348f0f733d7925ac1fa007c5c5c3527ee9afa5ae866fae88297a400)
                check_type(argname="argument cross_region_copy", value=cross_region_copy, expected_type=type_hints["cross_region_copy"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cross_region_copy": cross_region_copy,
                "name": name,
            }

        @builtins.property
        def cross_region_copy(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.CrossRegionCopyActionProperty", _IResolvable_a771d0ef]]]:
            '''The rule for copying shared snapshots across Regions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-action.html#cfn-dlm-lifecyclepolicy-action-crossregioncopy
            '''
            result = self._values.get("cross_region_copy")
            assert result is not None, "Required property 'cross_region_copy' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.CrossRegionCopyActionProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def name(self) -> builtins.str:
            '''A descriptive name for the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-action.html#cfn-dlm-lifecyclepolicy-action-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.ArchiveRetainRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"retention_archive_tier": "retentionArchiveTier"},
    )
    class ArchiveRetainRuleProperty:
        def __init__(
            self,
            *,
            retention_archive_tier: typing.Union[typing.Union["CfnLifecyclePolicy.RetentionArchiveTierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param retention_archive_tier: ``CfnLifecyclePolicy.ArchiveRetainRuleProperty.RetentionArchiveTier``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-archiveretainrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                archive_retain_rule_property = dlm.CfnLifecyclePolicy.ArchiveRetainRuleProperty(
                    retention_archive_tier=dlm.CfnLifecyclePolicy.RetentionArchiveTierProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5ab41ea31149bce42181e0f814679204be90120b23772030bc7078305493879)
                check_type(argname="argument retention_archive_tier", value=retention_archive_tier, expected_type=type_hints["retention_archive_tier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "retention_archive_tier": retention_archive_tier,
            }

        @builtins.property
        def retention_archive_tier(
            self,
        ) -> typing.Union["CfnLifecyclePolicy.RetentionArchiveTierProperty", _IResolvable_a771d0ef]:
            '''``CfnLifecyclePolicy.ArchiveRetainRuleProperty.RetentionArchiveTier``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-archiveretainrule.html#cfn-dlm-lifecyclepolicy-archiveretainrule-retentionarchivetier
            '''
            result = self._values.get("retention_archive_tier")
            assert result is not None, "Required property 'retention_archive_tier' is missing"
            return typing.cast(typing.Union["CfnLifecyclePolicy.RetentionArchiveTierProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArchiveRetainRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.ArchiveRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"retain_rule": "retainRule"},
    )
    class ArchiveRuleProperty:
        def __init__(
            self,
            *,
            retain_rule: typing.Union[typing.Union["CfnLifecyclePolicy.ArchiveRetainRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param retain_rule: ``CfnLifecyclePolicy.ArchiveRuleProperty.RetainRule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-archiverule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                archive_rule_property = dlm.CfnLifecyclePolicy.ArchiveRuleProperty(
                    retain_rule=dlm.CfnLifecyclePolicy.ArchiveRetainRuleProperty(
                        retention_archive_tier=dlm.CfnLifecyclePolicy.RetentionArchiveTierProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba5aec62a64a79d285afc0a7116dee0eddb18ebf21c9fa48eb03bf35f88e6fd3)
                check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "retain_rule": retain_rule,
            }

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Union["CfnLifecyclePolicy.ArchiveRetainRuleProperty", _IResolvable_a771d0ef]:
            '''``CfnLifecyclePolicy.ArchiveRuleProperty.RetainRule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-archiverule.html#cfn-dlm-lifecyclepolicy-archiverule-retainrule
            '''
            result = self._values.get("retain_rule")
            assert result is not None, "Required property 'retain_rule' is missing"
            return typing.cast(typing.Union["CfnLifecyclePolicy.ArchiveRetainRuleProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArchiveRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.CreateRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cron_expression": "cronExpression",
            "interval": "interval",
            "interval_unit": "intervalUnit",
            "location": "location",
            "times": "times",
        },
    )
    class CreateRuleProperty:
        def __init__(
            self,
            *,
            cron_expression: typing.Optional[builtins.str] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
            location: typing.Optional[builtins.str] = None,
            times: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''*[Snapshot and AMI policies only]* Specifies when the policy should create snapshots or AMIs.

            .. epigraph::

               - You must specify either *CronExpression* , or *Interval* , *IntervalUnit* , and *Times* .
               - If you need to specify an ``ArchiveRule`` for the schedule, then you must specify a creation frequency of at least 28 days.

            :param cron_expression: The schedule, as a Cron expression. The schedule interval must be between 1 hour and 1 year. For more information, see `Cron expressions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions>`_ in the *Amazon CloudWatch User Guide* .
            :param interval: The interval between snapshots. The supported values are 1, 2, 3, 4, 6, 8, 12, and 24.
            :param interval_unit: The interval unit.
            :param location: *[Snapshot policies only]* Specifies the destination for snapshots created by the policy. To create snapshots in the same Region as the source resource, specify ``CLOUD`` . To create snapshots on the same Outpost as the source resource, specify ``OUTPOST_LOCAL`` . If you omit this parameter, ``CLOUD`` is used by default. If the policy targets resources in an AWS Region , then you must create snapshots in the same Region as the source resource. If the policy targets resources on an Outpost, then you can create snapshots on the same Outpost as the source resource, or in the Region of that Outpost.
            :param times: The time, in UTC, to start the operation. The supported format is hh:mm. The operation occurs within a one-hour window following the specified time. If you do not specify a time, Amazon Data Lifecycle Manager selects a time within the next 24 hours.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                create_rule_property = dlm.CfnLifecyclePolicy.CreateRuleProperty(
                    cron_expression="cronExpression",
                    interval=123,
                    interval_unit="intervalUnit",
                    location="location",
                    times=["times"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab3bd86211bb978a74c5c16dc6b900331d304b5410ac087ea495abdd86c2453b)
                check_type(argname="argument cron_expression", value=cron_expression, expected_type=type_hints["cron_expression"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument times", value=times, expected_type=type_hints["times"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cron_expression is not None:
                self._values["cron_expression"] = cron_expression
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit
            if location is not None:
                self._values["location"] = location
            if times is not None:
                self._values["times"] = times

        @builtins.property
        def cron_expression(self) -> typing.Optional[builtins.str]:
            '''The schedule, as a Cron expression.

            The schedule interval must be between 1 hour and 1 year. For more information, see `Cron expressions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions>`_ in the *Amazon CloudWatch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-cronexpression
            '''
            result = self._values.get("cron_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The interval between snapshots.

            The supported values are 1, 2, 3, 4, 6, 8, 12, and 24.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The interval unit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''*[Snapshot policies only]* Specifies the destination for snapshots created by the policy.

            To create snapshots in the same Region as the source resource, specify ``CLOUD`` . To create snapshots on the same Outpost as the source resource, specify ``OUTPOST_LOCAL`` . If you omit this parameter, ``CLOUD`` is used by default.

            If the policy targets resources in an AWS Region , then you must create snapshots in the same Region as the source resource. If the policy targets resources on an Outpost, then you can create snapshots on the same Outpost as the source resource, or in the Region of that Outpost.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def times(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The time, in UTC, to start the operation. The supported format is hh:mm.

            The operation occurs within a one-hour window following the specified time. If you do not specify a time, Amazon Data Lifecycle Manager selects a time within the next 24 hours.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-times
            '''
            result = self._values.get("times")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.CrossRegionCopyActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_configuration": "encryptionConfiguration",
            "target": "target",
            "retain_rule": "retainRule",
        },
    )
    class CrossRegionCopyActionProperty:
        def __init__(
            self,
            *,
            encryption_configuration: typing.Union[typing.Union["CfnLifecyclePolicy.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            target: builtins.str,
            retain_rule: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies a cross-Region copy action for event-based policies.

            .. epigraph::

               To specify a cross-Region copy rule for snapshot and AMI policies, use ``CrossRegionCopyRule`` .

            :param encryption_configuration: The encryption settings for the copied snapshot.
            :param target: The target Region.
            :param retain_rule: Specifies a retention rule for cross-Region snapshot copies created by snapshot or event-based policies, or cross-Region AMI copies created by AMI policies. After the retention period expires, the cross-Region copy is deleted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                cross_region_copy_action_property = dlm.CfnLifecyclePolicy.CrossRegionCopyActionProperty(
                    encryption_configuration=dlm.CfnLifecyclePolicy.EncryptionConfigurationProperty(
                        encrypted=False,
                
                        # the properties below are optional
                        cmk_arn="cmkArn"
                    ),
                    target="target",
                
                    # the properties below are optional
                    retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                        interval=123,
                        interval_unit="intervalUnit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5239dc01669527fe9d69bcf001cbe05b2fb18145f3b2a2326d26b4188997167)
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encryption_configuration": encryption_configuration,
                "target": target,
            }
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Union["CfnLifecyclePolicy.EncryptionConfigurationProperty", _IResolvable_a771d0ef]:
            '''The encryption settings for the copied snapshot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyaction.html#cfn-dlm-lifecyclepolicy-crossregioncopyaction-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            assert result is not None, "Required property 'encryption_configuration' is missing"
            return typing.cast(typing.Union["CfnLifecyclePolicy.EncryptionConfigurationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def target(self) -> builtins.str:
            '''The target Region.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyaction.html#cfn-dlm-lifecyclepolicy-crossregioncopyaction-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", _IResolvable_a771d0ef]]:
            '''Specifies a retention rule for cross-Region snapshot copies created by snapshot or event-based policies, or cross-Region AMI copies created by AMI policies.

            After the retention period expires, the cross-Region copy is deleted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyaction.html#cfn-dlm-lifecyclepolicy-crossregioncopyaction-retainrule
            '''
            result = self._values.get("retain_rule")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
    )
    class CrossRegionCopyDeprecateRuleProperty:
        def __init__(
            self,
            *,
            interval: jsii.Number,
            interval_unit: builtins.str,
        ) -> None:
            '''
            :param interval: ``CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty.IntervalUnit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopydeprecaterule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                cross_region_copy_deprecate_rule_property = dlm.CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty(
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2f70ff3e76c651f5d2027b29a4cb6e1f8b49c37de4242fa30d7c1258f1fdcfe)
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "interval": interval,
                "interval_unit": interval_unit,
            }

        @builtins.property
        def interval(self) -> jsii.Number:
            '''``CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty.Interval``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopydeprecaterule.html#cfn-dlm-lifecyclepolicy-crossregioncopydeprecaterule-interval
            '''
            result = self._values.get("interval")
            assert result is not None, "Required property 'interval' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def interval_unit(self) -> builtins.str:
            '''``CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty.IntervalUnit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopydeprecaterule.html#cfn-dlm-lifecyclepolicy-crossregioncopydeprecaterule-intervalunit
            '''
            result = self._values.get("interval_unit")
            assert result is not None, "Required property 'interval_unit' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyDeprecateRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
    )
    class CrossRegionCopyRetainRuleProperty:
        def __init__(
            self,
            *,
            interval: jsii.Number,
            interval_unit: builtins.str,
        ) -> None:
            '''Specifies a retention rule for cross-Region snapshot copies created by snapshot or event-based policies, or cross-Region AMI copies created by AMI policies.

            After the retention period expires, the cross-Region copy is deleted.

            :param interval: The amount of time to retain a cross-Region snapshot or AMI copy. The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.
            :param interval_unit: The unit of time for time-based retention. For example, to retain a cross-Region copy for 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                cross_region_copy_retain_rule_property = dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e6042a86efa61f0e2417eede12b9e7cc8a8cfa411b45483aad6458458e18bbf)
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "interval": interval,
                "interval_unit": interval_unit,
            }

        @builtins.property
        def interval(self) -> jsii.Number:
            '''The amount of time to retain a cross-Region snapshot or AMI copy.

            The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyretainrule-interval
            '''
            result = self._values.get("interval")
            assert result is not None, "Required property 'interval' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def interval_unit(self) -> builtins.str:
            '''The unit of time for time-based retention.

            For example, to retain a cross-Region copy for 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyretainrule-intervalunit
            '''
            result = self._values.get("interval_unit")
            assert result is not None, "Required property 'interval_unit' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyRetainRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.CrossRegionCopyRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encrypted": "encrypted",
            "cmk_arn": "cmkArn",
            "copy_tags": "copyTags",
            "deprecate_rule": "deprecateRule",
            "retain_rule": "retainRule",
            "target": "target",
            "target_region": "targetRegion",
        },
    )
    class CrossRegionCopyRuleProperty:
        def __init__(
            self,
            *,
            encrypted: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            cmk_arn: typing.Optional[builtins.str] = None,
            copy_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            deprecate_rule: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            retain_rule: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            target: typing.Optional[builtins.str] = None,
            target_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Snapshot and AMI policies only]* Specifies a cross-Region copy rule for snapshot and AMI policies.

            .. epigraph::

               To specify a cross-Region copy action for event-based polices, use ``CrossRegionCopyAction`` .

            :param encrypted: To encrypt a copy of an unencrypted snapshot if encryption by default is not enabled, enable encryption using this parameter. Copies of encrypted snapshots are encrypted, even if this parameter is false or if encryption by default is not enabled.
            :param cmk_arn: The Amazon Resource Name (ARN) of the AWS KMS key to use for EBS encryption. If this parameter is not specified, the default KMS key for the account is used.
            :param copy_tags: Indicates whether to copy all user-defined tags from the source snapshot or AMI to the cross-Region copy.
            :param deprecate_rule: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.DeprecateRule``.
            :param retain_rule: The retention rule that indicates how long the cross-Region snapshot or AMI copies are to be retained in the destination Region.
            :param target: The target Region or the Amazon Resource Name (ARN) of the target Outpost for the snapshot copies. Use this parameter instead of *TargetRegion* . Do not specify both.
            :param target_region: .. epigraph:: Avoid using this parameter when creating new policies. Instead, use *Target* to specify a target Region or a target Outpost for snapshot copies. .. epigraph:: For policies created before the *Target* parameter was introduced, this parameter indicates the target Region for snapshot copies.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                cross_region_copy_rule_property = dlm.CfnLifecyclePolicy.CrossRegionCopyRuleProperty(
                    encrypted=False,
                
                    # the properties below are optional
                    cmk_arn="cmkArn",
                    copy_tags=False,
                    deprecate_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty(
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    target="target",
                    target_region="targetRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f52724520e4663413779515ac0a81f4e1699e35be8d9a6e2da264867e0e38020)
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
                check_type(argname="argument cmk_arn", value=cmk_arn, expected_type=type_hints["cmk_arn"])
                check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
                check_type(argname="argument deprecate_rule", value=deprecate_rule, expected_type=type_hints["deprecate_rule"])
                check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument target_region", value=target_region, expected_type=type_hints["target_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encrypted": encrypted,
            }
            if cmk_arn is not None:
                self._values["cmk_arn"] = cmk_arn
            if copy_tags is not None:
                self._values["copy_tags"] = copy_tags
            if deprecate_rule is not None:
                self._values["deprecate_rule"] = deprecate_rule
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule
            if target is not None:
                self._values["target"] = target
            if target_region is not None:
                self._values["target_region"] = target_region

        @builtins.property
        def encrypted(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''To encrypt a copy of an unencrypted snapshot if encryption by default is not enabled, enable encryption using this parameter.

            Copies of encrypted snapshots are encrypted, even if this parameter is false or if encryption by default is not enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-encrypted
            '''
            result = self._values.get("encrypted")
            assert result is not None, "Required property 'encrypted' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def cmk_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS KMS key to use for EBS encryption.

            If this parameter is not specified, the default KMS key for the account is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-cmkarn
            '''
            result = self._values.get("cmk_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def copy_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether to copy all user-defined tags from the source snapshot or AMI to the cross-Region copy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-copytags
            '''
            result = self._values.get("copy_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def deprecate_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty", _IResolvable_a771d0ef]]:
            '''``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.DeprecateRule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-deprecaterule
            '''
            result = self._values.get("deprecate_rule")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", _IResolvable_a771d0ef]]:
            '''The retention rule that indicates how long the cross-Region snapshot or AMI copies are to be retained in the destination Region.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-retainrule
            '''
            result = self._values.get("retain_rule")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The target Region or the Amazon Resource Name (ARN) of the target Outpost for the snapshot copies.

            Use this parameter instead of *TargetRegion* . Do not specify both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_region(self) -> typing.Optional[builtins.str]:
            '''.. epigraph::

   Avoid using this parameter when creating new policies.

            Instead, use *Target* to specify a target Region or a target Outpost for snapshot copies.
            .. epigraph::

               For policies created before the *Target* parameter was introduced, this parameter indicates the target Region for snapshot copies.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-targetregion
            '''
            result = self._values.get("target_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.DeprecateRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class DeprecateRuleProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param count: ``CfnLifecyclePolicy.DeprecateRuleProperty.Count``.
            :param interval: ``CfnLifecyclePolicy.DeprecateRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.DeprecateRuleProperty.IntervalUnit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-deprecaterule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                deprecate_rule_property = dlm.CfnLifecyclePolicy.DeprecateRuleProperty(
                    count=123,
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3df14d4bb615620f32764eca51a53a15b4d82601702149b76a666dcb946231c8)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''``CfnLifecyclePolicy.DeprecateRuleProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-deprecaterule.html#cfn-dlm-lifecyclepolicy-deprecaterule-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''``CfnLifecyclePolicy.DeprecateRuleProperty.Interval``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-deprecaterule.html#cfn-dlm-lifecyclepolicy-deprecaterule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''``CfnLifecyclePolicy.DeprecateRuleProperty.IntervalUnit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-deprecaterule.html#cfn-dlm-lifecyclepolicy-deprecaterule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeprecateRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encrypted": "encrypted", "cmk_arn": "cmkArn"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encrypted: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            cmk_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies the encryption settings for cross-Region snapshot copies created by event-based policies.

            :param encrypted: To encrypt a copy of an unencrypted snapshot when encryption by default is not enabled, enable encryption using this parameter. Copies of encrypted snapshots are encrypted, even if this parameter is false or when encryption by default is not enabled.
            :param cmk_arn: The Amazon Resource Name (ARN) of the AWS KMS key to use for EBS encryption. If this parameter is not specified, the default KMS key for the account is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                encryption_configuration_property = dlm.CfnLifecyclePolicy.EncryptionConfigurationProperty(
                    encrypted=False,
                
                    # the properties below are optional
                    cmk_arn="cmkArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__352778721ec9c4131a3d5743a1771db46ff29f75ac21a1a7e6fdb7b15af2f9c4)
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
                check_type(argname="argument cmk_arn", value=cmk_arn, expected_type=type_hints["cmk_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encrypted": encrypted,
            }
            if cmk_arn is not None:
                self._values["cmk_arn"] = cmk_arn

        @builtins.property
        def encrypted(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''To encrypt a copy of an unencrypted snapshot when encryption by default is not enabled, enable encryption using this parameter.

            Copies of encrypted snapshots are encrypted, even if this parameter is false or when encryption by default is not enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-encryptionconfiguration.html#cfn-dlm-lifecyclepolicy-encryptionconfiguration-encrypted
            '''
            result = self._values.get("encrypted")
            assert result is not None, "Required property 'encrypted' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def cmk_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS KMS key to use for EBS encryption.

            If this parameter is not specified, the default KMS key for the account is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-encryptionconfiguration.html#cfn-dlm-lifecyclepolicy-encryptionconfiguration-cmkarn
            '''
            result = self._values.get("cmk_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.EventParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_type": "eventType",
            "snapshot_owner": "snapshotOwner",
            "description_regex": "descriptionRegex",
        },
    )
    class EventParametersProperty:
        def __init__(
            self,
            *,
            event_type: builtins.str,
            snapshot_owner: typing.Sequence[builtins.str],
            description_regex: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies an event that activates an event-based policy.

            :param event_type: The type of event. Currently, only snapshot sharing events are supported.
            :param snapshot_owner: The IDs of the AWS accounts that can trigger policy by sharing snapshots with your account. The policy only runs if one of the specified AWS accounts shares a snapshot with your account.
            :param description_regex: The snapshot description that can trigger the policy. The description pattern is specified using a regular expression. The policy runs only if a snapshot with a description that matches the specified pattern is shared with your account. For example, specifying ``^.*Created for policy: policy-1234567890abcdef0.*$`` configures the policy to run only if snapshots created by policy ``policy-1234567890abcdef0`` are shared with your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                event_parameters_property = dlm.CfnLifecyclePolicy.EventParametersProperty(
                    event_type="eventType",
                    snapshot_owner=["snapshotOwner"],
                
                    # the properties below are optional
                    description_regex="descriptionRegex"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f908840a2529a0a266439f1220891ee20f80445a7fa86acb16b138db840b73eb)
                check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                check_type(argname="argument snapshot_owner", value=snapshot_owner, expected_type=type_hints["snapshot_owner"])
                check_type(argname="argument description_regex", value=description_regex, expected_type=type_hints["description_regex"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "event_type": event_type,
                "snapshot_owner": snapshot_owner,
            }
            if description_regex is not None:
                self._values["description_regex"] = description_regex

        @builtins.property
        def event_type(self) -> builtins.str:
            '''The type of event.

            Currently, only snapshot sharing events are supported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventparameters.html#cfn-dlm-lifecyclepolicy-eventparameters-eventtype
            '''
            result = self._values.get("event_type")
            assert result is not None, "Required property 'event_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def snapshot_owner(self) -> typing.List[builtins.str]:
            '''The IDs of the AWS accounts that can trigger policy by sharing snapshots with your account.

            The policy only runs if one of the specified AWS accounts shares a snapshot with your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventparameters.html#cfn-dlm-lifecyclepolicy-eventparameters-snapshotowner
            '''
            result = self._values.get("snapshot_owner")
            assert result is not None, "Required property 'snapshot_owner' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def description_regex(self) -> typing.Optional[builtins.str]:
            '''The snapshot description that can trigger the policy.

            The description pattern is specified using a regular expression. The policy runs only if a snapshot with a description that matches the specified pattern is shared with your account.

            For example, specifying ``^.*Created for policy: policy-1234567890abcdef0.*$`` configures the policy to run only if snapshots created by policy ``policy-1234567890abcdef0`` are shared with your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventparameters.html#cfn-dlm-lifecyclepolicy-eventparameters-descriptionregex
            '''
            result = self._values.get("description_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "parameters": "parameters"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            parameters: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.EventParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''*[Event-based policies only]* Specifies an event that activates an event-based policy.

            :param type: The source of the event. Currently only managed CloudWatch Events rules are supported.
            :param parameters: Information about the event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                event_source_property = dlm.CfnLifecyclePolicy.EventSourceProperty(
                    type="type",
                
                    # the properties below are optional
                    parameters=dlm.CfnLifecyclePolicy.EventParametersProperty(
                        event_type="eventType",
                        snapshot_owner=["snapshotOwner"],
                
                        # the properties below are optional
                        description_regex="descriptionRegex"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30b43aebdfc2a5c8f6e152c717ca2852d3dede90be3dddf82df2f7b44bd00b4d)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def type(self) -> builtins.str:
            '''The source of the event.

            Currently only managed CloudWatch Events rules are supported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventsource.html#cfn-dlm-lifecyclepolicy-eventsource-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.EventParametersProperty", _IResolvable_a771d0ef]]:
            '''Information about the event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-eventsource.html#cfn-dlm-lifecyclepolicy-eventsource-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.EventParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.FastRestoreRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zones": "availabilityZones",
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class FastRestoreRuleProperty:
        def __init__(
            self,
            *,
            availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Snapshot policies only]* Specifies a rule for enabling fast snapshot restore for snapshots created by snapshot policies.

            You can enable fast snapshot restore based on either a count or a time interval.

            :param availability_zones: The Availability Zones in which to enable fast snapshot restore.
            :param count: The number of snapshots to be enabled with fast snapshot restore.
            :param interval: The amount of time to enable fast snapshot restore. The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.
            :param interval_unit: The unit of time for enabling fast snapshot restore.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                fast_restore_rule_property = dlm.CfnLifecyclePolicy.FastRestoreRuleProperty(
                    availability_zones=["availabilityZones"],
                    count=123,
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc5198fcd4df82372f6ba436315f8c32af3bf8b1254dd23dd21d075c8224ff65)
                check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zones is not None:
                self._values["availability_zones"] = availability_zones
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Availability Zones in which to enable fast snapshot restore.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-availabilityzones
            '''
            result = self._values.get("availability_zones")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''The number of snapshots to be enabled with fast snapshot restore.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The amount of time to enable fast snapshot restore.

            The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time for enabling fast snapshot restore.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FastRestoreRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.ParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_boot_volume": "excludeBootVolume",
            "exclude_data_volume_tags": "excludeDataVolumeTags",
            "no_reboot": "noReboot",
        },
    )
    class ParametersProperty:
        def __init__(
            self,
            *,
            exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            exclude_data_volume_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            no_reboot: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''*[Snapshot and AMI policies only]* Specifies optional parameters for snapshot and AMI policies.

            The set of valid parameters depends on the combination of policy type and target resource type.

            If you choose to exclude boot volumes and you specify tags that consequently exclude all of the additional data volumes attached to an instance, then Amazon Data Lifecycle Manager will not create any snapshots for the affected instance, and it will emit a ``SnapshotsCreateFailed`` Amazon CloudWatch metric. For more information, see `Monitor your policies using Amazon CloudWatch <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitor-dlm-cw-metrics.html>`_ .

            :param exclude_boot_volume: *[Snapshot policies that target instances only]* Indicates whether to exclude the root volume from multi-volume snapshot sets. The default is ``false`` . If you specify ``true`` , then the root volumes attached to targeted instances will be excluded from the multi-volume snapshot sets created by the policy.
            :param exclude_data_volume_tags: ``CfnLifecyclePolicy.ParametersProperty.ExcludeDataVolumeTags``.
            :param no_reboot: *[AMI policies only]* Indicates whether targeted instances are rebooted when the lifecycle policy runs. ``true`` indicates that targeted instances are not rebooted when the policy runs. ``false`` indicates that target instances are rebooted when the policy runs. The default is ``true`` (instances are not rebooted).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                parameters_property = dlm.CfnLifecyclePolicy.ParametersProperty(
                    exclude_boot_volume=False,
                    exclude_data_volume_tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    no_reboot=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa8a03b9d445f7c6856ba1086d442ce3fcbcd4c518272cd3455cc4f4d2e460a4)
                check_type(argname="argument exclude_boot_volume", value=exclude_boot_volume, expected_type=type_hints["exclude_boot_volume"])
                check_type(argname="argument exclude_data_volume_tags", value=exclude_data_volume_tags, expected_type=type_hints["exclude_data_volume_tags"])
                check_type(argname="argument no_reboot", value=no_reboot, expected_type=type_hints["no_reboot"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_boot_volume is not None:
                self._values["exclude_boot_volume"] = exclude_boot_volume
            if exclude_data_volume_tags is not None:
                self._values["exclude_data_volume_tags"] = exclude_data_volume_tags
            if no_reboot is not None:
                self._values["no_reboot"] = no_reboot

        @builtins.property
        def exclude_boot_volume(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''*[Snapshot policies that target instances only]* Indicates whether to exclude the root volume from multi-volume snapshot sets.

            The default is ``false`` . If you specify ``true`` , then the root volumes attached to targeted instances will be excluded from the multi-volume snapshot sets created by the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-excludebootvolume
            '''
            result = self._values.get("exclude_boot_volume")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def exclude_data_volume_tags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
            '''``CfnLifecyclePolicy.ParametersProperty.ExcludeDataVolumeTags``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-excludedatavolumetags
            '''
            result = self._values.get("exclude_data_volume_tags")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

        @builtins.property
        def no_reboot(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''*[AMI policies only]* Indicates whether targeted instances are rebooted when the lifecycle policy runs.

            ``true`` indicates that targeted instances are not rebooted when the policy runs. ``false`` indicates that target instances are rebooted when the policy runs. The default is ``true`` (instances are not rebooted).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-noreboot
            '''
            result = self._values.get("no_reboot")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.PolicyDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "event_source": "eventSource",
            "parameters": "parameters",
            "policy_type": "policyType",
            "resource_locations": "resourceLocations",
            "resource_types": "resourceTypes",
            "schedules": "schedules",
            "target_tags": "targetTags",
        },
    )
    class PolicyDetailsProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLifecyclePolicy.ActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            event_source: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.EventSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            parameters: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.ParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            policy_type: typing.Optional[builtins.str] = None,
            resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            schedules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLifecyclePolicy.ScheduleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            target_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''*[All policy types]* Specifies the configuration of a lifecycle policy.

            :param actions: *[Event-based policies only]* The actions to be performed when the event-based policy is activated. You can specify only one action per policy.
            :param event_source: *[Event-based policies only]* The event that activates the event-based policy.
            :param parameters: *[Snapshot and AMI policies only]* A set of optional parameters for snapshot and AMI lifecycle policies. .. epigraph:: If you are modifying a policy that was created or previously modified using the Amazon Data Lifecycle Manager console, then you must include this parameter and specify either the default values or the new values that you require. You can't omit this parameter or set its values to null.
            :param policy_type: *[All policy types]* The valid target resource types and actions a policy can manage. Specify ``EBS_SNAPSHOT_MANAGEMENT`` to create a lifecycle policy that manages the lifecycle of Amazon EBS snapshots. Specify ``IMAGE_MANAGEMENT`` to create a lifecycle policy that manages the lifecycle of EBS-backed AMIs. Specify ``EVENT_BASED_POLICY`` to create an event-based policy that performs specific actions when a defined event occurs in your AWS account . The default is ``EBS_SNAPSHOT_MANAGEMENT`` .
            :param resource_locations: *[Snapshot and AMI policies only]* The location of the resources to backup. If the source resources are located in an AWS Region , specify ``CLOUD`` . If the source resources are located on an Outpost in your account, specify ``OUTPOST`` . If you specify ``OUTPOST`` , Amazon Data Lifecycle Manager backs up all resources of the specified type with matching target tags across all of the Outposts in your account.
            :param resource_types: *[Snapshot policies only]* The target resource type for snapshot and AMI lifecycle policies. Use ``VOLUME`` to create snapshots of individual volumes or use ``INSTANCE`` to create multi-volume snapshots from the volumes for an instance.
            :param schedules: *[Snapshot and AMI policies only]* The schedules of policy-defined actions for snapshot and AMI lifecycle policies. A policy can have up to four schedules—one mandatory schedule and up to three optional schedules.
            :param target_tags: *[Snapshot and AMI policies only]* The single tag that identifies targeted resources for this policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                policy_details_property = dlm.CfnLifecyclePolicy.PolicyDetailsProperty(
                    actions=[dlm.CfnLifecyclePolicy.ActionProperty(
                        cross_region_copy=[dlm.CfnLifecyclePolicy.CrossRegionCopyActionProperty(
                            encryption_configuration=dlm.CfnLifecyclePolicy.EncryptionConfigurationProperty(
                                encrypted=False,
                
                                # the properties below are optional
                                cmk_arn="cmkArn"
                            ),
                            target="target",
                
                            # the properties below are optional
                            retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            )
                        )],
                        name="name"
                    )],
                    event_source=dlm.CfnLifecyclePolicy.EventSourceProperty(
                        type="type",
                
                        # the properties below are optional
                        parameters=dlm.CfnLifecyclePolicy.EventParametersProperty(
                            event_type="eventType",
                            snapshot_owner=["snapshotOwner"],
                
                            # the properties below are optional
                            description_regex="descriptionRegex"
                        )
                    ),
                    parameters=dlm.CfnLifecyclePolicy.ParametersProperty(
                        exclude_boot_volume=False,
                        exclude_data_volume_tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        no_reboot=False
                    ),
                    policy_type="policyType",
                    resource_locations=["resourceLocations"],
                    resource_types=["resourceTypes"],
                    schedules=[dlm.CfnLifecyclePolicy.ScheduleProperty(
                        archive_rule=dlm.CfnLifecyclePolicy.ArchiveRuleProperty(
                            retain_rule=dlm.CfnLifecyclePolicy.ArchiveRetainRuleProperty(
                                retention_archive_tier=dlm.CfnLifecyclePolicy.RetentionArchiveTierProperty(
                                    count=123,
                                    interval=123,
                                    interval_unit="intervalUnit"
                                )
                            )
                        ),
                        copy_tags=False,
                        create_rule=dlm.CfnLifecyclePolicy.CreateRuleProperty(
                            cron_expression="cronExpression",
                            interval=123,
                            interval_unit="intervalUnit",
                            location="location",
                            times=["times"]
                        ),
                        cross_region_copy_rules=[dlm.CfnLifecyclePolicy.CrossRegionCopyRuleProperty(
                            encrypted=False,
                
                            # the properties below are optional
                            cmk_arn="cmkArn",
                            copy_tags=False,
                            deprecate_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            target="target",
                            target_region="targetRegion"
                        )],
                        deprecate_rule=dlm.CfnLifecyclePolicy.DeprecateRuleProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        fast_restore_rule=dlm.CfnLifecyclePolicy.FastRestoreRuleProperty(
                            availability_zones=["availabilityZones"],
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        name="name",
                        retain_rule=dlm.CfnLifecyclePolicy.RetainRuleProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        share_rules=[dlm.CfnLifecyclePolicy.ShareRuleProperty(
                            target_accounts=["targetAccounts"],
                            unshare_interval=123,
                            unshare_interval_unit="unshareIntervalUnit"
                        )],
                        tags_to_add=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        variable_tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    target_tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fc225292eba74253b17b8544d6fe2b3bbfc6bf64194a57d8183dddce529b249)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
                check_type(argname="argument resource_locations", value=resource_locations, expected_type=type_hints["resource_locations"])
                check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
                check_type(argname="argument schedules", value=schedules, expected_type=type_hints["schedules"])
                check_type(argname="argument target_tags", value=target_tags, expected_type=type_hints["target_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if event_source is not None:
                self._values["event_source"] = event_source
            if parameters is not None:
                self._values["parameters"] = parameters
            if policy_type is not None:
                self._values["policy_type"] = policy_type
            if resource_locations is not None:
                self._values["resource_locations"] = resource_locations
            if resource_types is not None:
                self._values["resource_types"] = resource_types
            if schedules is not None:
                self._values["schedules"] = schedules
            if target_tags is not None:
                self._values["target_tags"] = target_tags

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.ActionProperty", _IResolvable_a771d0ef]]]]:
            '''*[Event-based policies only]* The actions to be performed when the event-based policy is activated.

            You can specify only one action per policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.ActionProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def event_source(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.EventSourceProperty", _IResolvable_a771d0ef]]:
            '''*[Event-based policies only]* The event that activates the event-based policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-eventsource
            '''
            result = self._values.get("event_source")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.EventSourceProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.ParametersProperty", _IResolvable_a771d0ef]]:
            '''*[Snapshot and AMI policies only]* A set of optional parameters for snapshot and AMI lifecycle policies.

            .. epigraph::

               If you are modifying a policy that was created or previously modified using the Amazon Data Lifecycle Manager console, then you must include this parameter and specify either the default values or the new values that you require. You can't omit this parameter or set its values to null.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.ParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def policy_type(self) -> typing.Optional[builtins.str]:
            '''*[All policy types]* The valid target resource types and actions a policy can manage.

            Specify ``EBS_SNAPSHOT_MANAGEMENT`` to create a lifecycle policy that manages the lifecycle of Amazon EBS snapshots. Specify ``IMAGE_MANAGEMENT`` to create a lifecycle policy that manages the lifecycle of EBS-backed AMIs. Specify ``EVENT_BASED_POLICY`` to create an event-based policy that performs specific actions when a defined event occurs in your AWS account .

            The default is ``EBS_SNAPSHOT_MANAGEMENT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-policytype
            '''
            result = self._values.get("policy_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_locations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''*[Snapshot and AMI policies only]* The location of the resources to backup.

            If the source resources are located in an AWS Region , specify ``CLOUD`` . If the source resources are located on an Outpost in your account, specify ``OUTPOST`` .

            If you specify ``OUTPOST`` , Amazon Data Lifecycle Manager backs up all resources of the specified type with matching target tags across all of the Outposts in your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-resourcelocations
            '''
            result = self._values.get("resource_locations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''*[Snapshot policies only]* The target resource type for snapshot and AMI lifecycle policies.

            Use ``VOLUME`` to create snapshots of individual volumes or use ``INSTANCE`` to create multi-volume snapshots from the volumes for an instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-resourcetypes
            '''
            result = self._values.get("resource_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def schedules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.ScheduleProperty", _IResolvable_a771d0ef]]]]:
            '''*[Snapshot and AMI policies only]* The schedules of policy-defined actions for snapshot and AMI lifecycle policies.

            A policy can have up to four schedules—one mandatory schedule and up to three optional schedules.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-schedules
            '''
            result = self._values.get("schedules")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.ScheduleProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def target_tags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
            '''*[Snapshot and AMI policies only]* The single tag that identifies targeted resources for this policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-targettags
            '''
            result = self._values.get("target_tags")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.RetainRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class RetainRuleProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Snapshot and AMI policies only]* Specifies a retention rule for snapshots created by snapshot policies, or for AMIs created by AMI policies.

            .. epigraph::

               For snapshot policies that have an ``ArchiveRule`` , this retention rule applies to standard tier retention. When the retention threshold is met, snapshots are moved from the standard to the archive tier.

               For snapshot policies that do not have an *ArchiveRule* , snapshots are permanently deleted when this retention threshold is met.

            You can retain snapshots based on either a count or a time interval.

            - *Count-based retention*

            You must specify *Count* . If you specify an ``ArchiveRule`` for the schedule, then you can specify a retention count of ``0`` to archive snapshots immediately after creation. If you specify a ``FastRestoreRule`` , ``ShareRule`` , or a ``CrossRegionCopyRule`` , then you must specify a retention count of ``1`` or more.

            - *Age-based retention*

            You must specify *Interval* and *IntervalUnit* . If you specify an ``ArchiveRule`` for the schedule, then you can specify a retention interval of ``0`` days to archive snapshots immediately after creation. If you specify a ``FastRestoreRule`` , ``ShareRule`` , or a ``CrossRegionCopyRule`` , then you must specify a retention interval of ``1`` day or more.

            :param count: The number of snapshots to retain for each volume, up to a maximum of 1000. For example if you want to retain a maximum of three snapshots, specify ``3`` . When the fourth snapshot is created, the oldest retained snapshot is deleted, or it is moved to the archive tier if you have specified an ``ArchiveRule`` .
            :param interval: The amount of time to retain each snapshot. The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.
            :param interval_unit: The unit of time for time-based retention. For example, to retain snapshots for 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` . Once the snapshot has been retained for 3 months, it is deleted, or it is moved to the archive tier if you have specified an ``ArchiveRule`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                retain_rule_property = dlm.CfnLifecyclePolicy.RetainRuleProperty(
                    count=123,
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__972486b102e1bf60dc205682fb6d23f4bcf390f88b0c62e3d48456befe08407a)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''The number of snapshots to retain for each volume, up to a maximum of 1000.

            For example if you want to retain a maximum of three snapshots, specify ``3`` . When the fourth snapshot is created, the oldest retained snapshot is deleted, or it is moved to the archive tier if you have specified an ``ArchiveRule`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The amount of time to retain each snapshot.

            The maximum is 100 years. This is equivalent to 1200 months, 5200 weeks, or 36500 days.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time for time-based retention.

            For example, to retain snapshots for 3 months, specify ``Interval=3`` and ``IntervalUnit=MONTHS`` . Once the snapshot has been retained for 3 months, it is deleted, or it is moved to the archive tier if you have specified an ``ArchiveRule`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetainRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.RetentionArchiveTierProperty",
        jsii_struct_bases=[],
        name_mapping={
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class RetentionArchiveTierProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param count: ``CfnLifecyclePolicy.RetentionArchiveTierProperty.Count``.
            :param interval: ``CfnLifecyclePolicy.RetentionArchiveTierProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.RetentionArchiveTierProperty.IntervalUnit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retentionarchivetier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                retention_archive_tier_property = dlm.CfnLifecyclePolicy.RetentionArchiveTierProperty(
                    count=123,
                    interval=123,
                    interval_unit="intervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d7371a1ba72418ff82e67c0e8e6dd226ddb6779df3e3558d7c6c394624d5dca)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''``CfnLifecyclePolicy.RetentionArchiveTierProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retentionarchivetier.html#cfn-dlm-lifecyclepolicy-retentionarchivetier-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''``CfnLifecyclePolicy.RetentionArchiveTierProperty.Interval``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retentionarchivetier.html#cfn-dlm-lifecyclepolicy-retentionarchivetier-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            '''``CfnLifecyclePolicy.RetentionArchiveTierProperty.IntervalUnit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retentionarchivetier.html#cfn-dlm-lifecyclepolicy-retentionarchivetier-intervalunit
            '''
            result = self._values.get("interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionArchiveTierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "archive_rule": "archiveRule",
            "copy_tags": "copyTags",
            "create_rule": "createRule",
            "cross_region_copy_rules": "crossRegionCopyRules",
            "deprecate_rule": "deprecateRule",
            "fast_restore_rule": "fastRestoreRule",
            "name": "name",
            "retain_rule": "retainRule",
            "share_rules": "shareRules",
            "tags_to_add": "tagsToAdd",
            "variable_tags": "variableTags",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            archive_rule: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.ArchiveRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            copy_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            create_rule: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.CreateRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            cross_region_copy_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            deprecate_rule: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.DeprecateRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            fast_restore_rule: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.FastRestoreRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            name: typing.Optional[builtins.str] = None,
            retain_rule: typing.Optional[typing.Union[typing.Union["CfnLifecyclePolicy.RetainRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            share_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLifecyclePolicy.ShareRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            tags_to_add: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            variable_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''*[Snapshot and AMI policies only]* Specifies a schedule for a snapshot or AMI lifecycle policy.

            :param archive_rule: ``CfnLifecyclePolicy.ScheduleProperty.ArchiveRule``.
            :param copy_tags: Copy all user-defined tags on a source volume to snapshots of the volume created by this policy.
            :param create_rule: The creation rule.
            :param cross_region_copy_rules: Specifies a rule for copying snapshots or AMIs across regions. .. epigraph:: You can't specify cross-Region copy rules for policies that create snapshots on an Outpost. If the policy creates snapshots in a Region, then snapshots can be copied to up to three Regions or Outposts.
            :param deprecate_rule: ``CfnLifecyclePolicy.ScheduleProperty.DeprecateRule``.
            :param fast_restore_rule: *[Snapshot policies only]* The rule for enabling fast snapshot restore.
            :param name: The name of the schedule.
            :param retain_rule: The retention rule for snapshots or AMIs created by the policy.
            :param share_rules: *[Snapshot policies only]* The rule for sharing snapshots with other AWS accounts .
            :param tags_to_add: The tags to apply to policy-created resources. These user-defined tags are in addition to the AWS -added lifecycle tags.
            :param variable_tags: *[AMI policies and snapshot policies that target instances only]* A collection of key/value pairs with values determined dynamically when the policy is executed. Keys may be any valid Amazon EC2 tag key. Values must be in one of the two following formats: ``$(instance-id)`` or ``$(timestamp)`` . Variable tags are only valid for EBS Snapshot Management – Instance policies.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                schedule_property = dlm.CfnLifecyclePolicy.ScheduleProperty(
                    archive_rule=dlm.CfnLifecyclePolicy.ArchiveRuleProperty(
                        retain_rule=dlm.CfnLifecyclePolicy.ArchiveRetainRuleProperty(
                            retention_archive_tier=dlm.CfnLifecyclePolicy.RetentionArchiveTierProperty(
                                count=123,
                                interval=123,
                                interval_unit="intervalUnit"
                            )
                        )
                    ),
                    copy_tags=False,
                    create_rule=dlm.CfnLifecyclePolicy.CreateRuleProperty(
                        cron_expression="cronExpression",
                        interval=123,
                        interval_unit="intervalUnit",
                        location="location",
                        times=["times"]
                    ),
                    cross_region_copy_rules=[dlm.CfnLifecyclePolicy.CrossRegionCopyRuleProperty(
                        encrypted=False,
                
                        # the properties below are optional
                        cmk_arn="cmkArn",
                        copy_tags=False,
                        deprecate_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        target="target",
                        target_region="targetRegion"
                    )],
                    deprecate_rule=dlm.CfnLifecyclePolicy.DeprecateRuleProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    fast_restore_rule=dlm.CfnLifecyclePolicy.FastRestoreRuleProperty(
                        availability_zones=["availabilityZones"],
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    name="name",
                    retain_rule=dlm.CfnLifecyclePolicy.RetainRuleProperty(
                        count=123,
                        interval=123,
                        interval_unit="intervalUnit"
                    ),
                    share_rules=[dlm.CfnLifecyclePolicy.ShareRuleProperty(
                        target_accounts=["targetAccounts"],
                        unshare_interval=123,
                        unshare_interval_unit="unshareIntervalUnit"
                    )],
                    tags_to_add=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf126a38043d201643fed4f4b3c71c9b3fb21e3b3b0321ab8647555a35617ec0)
                check_type(argname="argument archive_rule", value=archive_rule, expected_type=type_hints["archive_rule"])
                check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
                check_type(argname="argument create_rule", value=create_rule, expected_type=type_hints["create_rule"])
                check_type(argname="argument cross_region_copy_rules", value=cross_region_copy_rules, expected_type=type_hints["cross_region_copy_rules"])
                check_type(argname="argument deprecate_rule", value=deprecate_rule, expected_type=type_hints["deprecate_rule"])
                check_type(argname="argument fast_restore_rule", value=fast_restore_rule, expected_type=type_hints["fast_restore_rule"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
                check_type(argname="argument share_rules", value=share_rules, expected_type=type_hints["share_rules"])
                check_type(argname="argument tags_to_add", value=tags_to_add, expected_type=type_hints["tags_to_add"])
                check_type(argname="argument variable_tags", value=variable_tags, expected_type=type_hints["variable_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if archive_rule is not None:
                self._values["archive_rule"] = archive_rule
            if copy_tags is not None:
                self._values["copy_tags"] = copy_tags
            if create_rule is not None:
                self._values["create_rule"] = create_rule
            if cross_region_copy_rules is not None:
                self._values["cross_region_copy_rules"] = cross_region_copy_rules
            if deprecate_rule is not None:
                self._values["deprecate_rule"] = deprecate_rule
            if fast_restore_rule is not None:
                self._values["fast_restore_rule"] = fast_restore_rule
            if name is not None:
                self._values["name"] = name
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule
            if share_rules is not None:
                self._values["share_rules"] = share_rules
            if tags_to_add is not None:
                self._values["tags_to_add"] = tags_to_add
            if variable_tags is not None:
                self._values["variable_tags"] = variable_tags

        @builtins.property
        def archive_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.ArchiveRuleProperty", _IResolvable_a771d0ef]]:
            '''``CfnLifecyclePolicy.ScheduleProperty.ArchiveRule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-archiverule
            '''
            result = self._values.get("archive_rule")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.ArchiveRuleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def copy_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Copy all user-defined tags on a source volume to snapshots of the volume created by this policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-copytags
            '''
            result = self._values.get("copy_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def create_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.CreateRuleProperty", _IResolvable_a771d0ef]]:
            '''The creation rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-createrule
            '''
            result = self._values.get("create_rule")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.CreateRuleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def cross_region_copy_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRuleProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies a rule for copying snapshots or AMIs across regions.

            .. epigraph::

               You can't specify cross-Region copy rules for policies that create snapshots on an Outpost. If the policy creates snapshots in a Region, then snapshots can be copied to up to three Regions or Outposts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-crossregioncopyrules
            '''
            result = self._values.get("cross_region_copy_rules")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRuleProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def deprecate_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.DeprecateRuleProperty", _IResolvable_a771d0ef]]:
            '''``CfnLifecyclePolicy.ScheduleProperty.DeprecateRule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-deprecaterule
            '''
            result = self._values.get("deprecate_rule")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.DeprecateRuleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def fast_restore_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.FastRestoreRuleProperty", _IResolvable_a771d0ef]]:
            '''*[Snapshot policies only]* The rule for enabling fast snapshot restore.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-fastrestorerule
            '''
            result = self._values.get("fast_restore_rule")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.FastRestoreRuleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the schedule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.RetainRuleProperty", _IResolvable_a771d0ef]]:
            '''The retention rule for snapshots or AMIs created by the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-retainrule
            '''
            result = self._values.get("retain_rule")
            return typing.cast(typing.Optional[typing.Union["CfnLifecyclePolicy.RetainRuleProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def share_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.ShareRuleProperty", _IResolvable_a771d0ef]]]]:
            '''*[Snapshot policies only]* The rule for sharing snapshots with other AWS accounts .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-sharerules
            '''
            result = self._values.get("share_rules")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.ShareRuleProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def tags_to_add(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
            '''The tags to apply to policy-created resources.

            These user-defined tags are in addition to the AWS -added lifecycle tags.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-tagstoadd
            '''
            result = self._values.get("tags_to_add")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

        @builtins.property
        def variable_tags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
            '''*[AMI policies and snapshot policies that target instances only]* A collection of key/value pairs with values determined dynamically when the policy is executed.

            Keys may be any valid Amazon EC2 tag key. Values must be in one of the two following formats: ``$(instance-id)`` or ``$(timestamp)`` . Variable tags are only valid for EBS Snapshot Management – Instance policies.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-variabletags
            '''
            result = self._values.get("variable_tags")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.ShareRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_accounts": "targetAccounts",
            "unshare_interval": "unshareInterval",
            "unshare_interval_unit": "unshareIntervalUnit",
        },
    )
    class ShareRuleProperty:
        def __init__(
            self,
            *,
            target_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            unshare_interval: typing.Optional[jsii.Number] = None,
            unshare_interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*[Snapshot policies only]* Specifies a rule for sharing snapshots across AWS accounts .

            :param target_accounts: The IDs of the AWS accounts with which to share the snapshots.
            :param unshare_interval: The period after which snapshots that are shared with other AWS accounts are automatically unshared.
            :param unshare_interval_unit: The unit of time for the automatic unsharing interval.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-sharerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dlm as dlm
                
                share_rule_property = dlm.CfnLifecyclePolicy.ShareRuleProperty(
                    target_accounts=["targetAccounts"],
                    unshare_interval=123,
                    unshare_interval_unit="unshareIntervalUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54316211badc49f9081340f52d5c10940ac84450ece4923729aac060213055fc)
                check_type(argname="argument target_accounts", value=target_accounts, expected_type=type_hints["target_accounts"])
                check_type(argname="argument unshare_interval", value=unshare_interval, expected_type=type_hints["unshare_interval"])
                check_type(argname="argument unshare_interval_unit", value=unshare_interval_unit, expected_type=type_hints["unshare_interval_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_accounts is not None:
                self._values["target_accounts"] = target_accounts
            if unshare_interval is not None:
                self._values["unshare_interval"] = unshare_interval
            if unshare_interval_unit is not None:
                self._values["unshare_interval_unit"] = unshare_interval_unit

        @builtins.property
        def target_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the AWS accounts with which to share the snapshots.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-sharerule.html#cfn-dlm-lifecyclepolicy-sharerule-targetaccounts
            '''
            result = self._values.get("target_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def unshare_interval(self) -> typing.Optional[jsii.Number]:
            '''The period after which snapshots that are shared with other AWS accounts are automatically unshared.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-sharerule.html#cfn-dlm-lifecyclepolicy-sharerule-unshareinterval
            '''
            result = self._values.get("unshare_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unshare_interval_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time for the automatic unsharing interval.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-sharerule.html#cfn-dlm-lifecyclepolicy-sharerule-unshareintervalunit
            '''
            result = self._values.get("unshare_interval_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShareRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_dlm.CfnLifecyclePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "execution_role_arn": "executionRoleArn",
        "policy_details": "policyDetails",
        "state": "state",
        "tags": "tags",
    },
)
class CfnLifecyclePolicyProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        policy_details: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.PolicyDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLifecyclePolicy``.

        :param description: A description of the lifecycle policy. The characters ^[0-9A-Za-z _-]+$ are supported.
        :param execution_role_arn: The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.
        :param policy_details: The configuration details of the lifecycle policy.
        :param state: The activation state of the lifecycle policy.
        :param tags: The tags to apply to the lifecycle policy during creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dlm as dlm
            
            cfn_lifecycle_policy_props = dlm.CfnLifecyclePolicyProps(
                description="description",
                execution_role_arn="executionRoleArn",
                policy_details=dlm.CfnLifecyclePolicy.PolicyDetailsProperty(
                    actions=[dlm.CfnLifecyclePolicy.ActionProperty(
                        cross_region_copy=[dlm.CfnLifecyclePolicy.CrossRegionCopyActionProperty(
                            encryption_configuration=dlm.CfnLifecyclePolicy.EncryptionConfigurationProperty(
                                encrypted=False,
            
                                # the properties below are optional
                                cmk_arn="cmkArn"
                            ),
                            target="target",
            
                            # the properties below are optional
                            retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            )
                        )],
                        name="name"
                    )],
                    event_source=dlm.CfnLifecyclePolicy.EventSourceProperty(
                        type="type",
            
                        # the properties below are optional
                        parameters=dlm.CfnLifecyclePolicy.EventParametersProperty(
                            event_type="eventType",
                            snapshot_owner=["snapshotOwner"],
            
                            # the properties below are optional
                            description_regex="descriptionRegex"
                        )
                    ),
                    parameters=dlm.CfnLifecyclePolicy.ParametersProperty(
                        exclude_boot_volume=False,
                        exclude_data_volume_tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        no_reboot=False
                    ),
                    policy_type="policyType",
                    resource_locations=["resourceLocations"],
                    resource_types=["resourceTypes"],
                    schedules=[dlm.CfnLifecyclePolicy.ScheduleProperty(
                        archive_rule=dlm.CfnLifecyclePolicy.ArchiveRuleProperty(
                            retain_rule=dlm.CfnLifecyclePolicy.ArchiveRetainRuleProperty(
                                retention_archive_tier=dlm.CfnLifecyclePolicy.RetentionArchiveTierProperty(
                                    count=123,
                                    interval=123,
                                    interval_unit="intervalUnit"
                                )
                            )
                        ),
                        copy_tags=False,
                        create_rule=dlm.CfnLifecyclePolicy.CreateRuleProperty(
                            cron_expression="cronExpression",
                            interval=123,
                            interval_unit="intervalUnit",
                            location="location",
                            times=["times"]
                        ),
                        cross_region_copy_rules=[dlm.CfnLifecyclePolicy.CrossRegionCopyRuleProperty(
                            encrypted=False,
            
                            # the properties below are optional
                            cmk_arn="cmkArn",
                            copy_tags=False,
                            deprecate_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            retain_rule=dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty(
                                interval=123,
                                interval_unit="intervalUnit"
                            ),
                            target="target",
                            target_region="targetRegion"
                        )],
                        deprecate_rule=dlm.CfnLifecyclePolicy.DeprecateRuleProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        fast_restore_rule=dlm.CfnLifecyclePolicy.FastRestoreRuleProperty(
                            availability_zones=["availabilityZones"],
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        name="name",
                        retain_rule=dlm.CfnLifecyclePolicy.RetainRuleProperty(
                            count=123,
                            interval=123,
                            interval_unit="intervalUnit"
                        ),
                        share_rules=[dlm.CfnLifecyclePolicy.ShareRuleProperty(
                            target_accounts=["targetAccounts"],
                            unshare_interval=123,
                            unshare_interval_unit="unshareIntervalUnit"
                        )],
                        tags_to_add=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        variable_tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    target_tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764a317923b196bfc4390c0815a72b55d4943581f5bc973c741656da964f633c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument policy_details", value=policy_details, expected_type=type_hints["policy_details"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if policy_details is not None:
            self._values["policy_details"] = policy_details
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the lifecycle policy.

        The characters ^[0-9A-Za-z _-]+$ are supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_details(
        self,
    ) -> typing.Optional[typing.Union[CfnLifecyclePolicy.PolicyDetailsProperty, _IResolvable_a771d0ef]]:
        '''The configuration details of the lifecycle policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-policydetails
        '''
        result = self._values.get("policy_details")
        return typing.cast(typing.Optional[typing.Union[CfnLifecyclePolicy.PolicyDetailsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The activation state of the lifecycle policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to apply to the lifecycle policy during creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLifecyclePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLifecyclePolicy",
    "CfnLifecyclePolicyProps",
]

publication.publish()

def _typecheckingstub__77301b6dfe6ba608f1b3f2f352c7a49b8d2178faed5a27bdd9320566ac942072(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    policy_details: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.PolicyDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f19528d58dbbceb9cf36cbd8dc734b2c4eef8450da7c415995ca30ab277607(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11c21ead08f7e2d913cb434dc8159f393fae758d684ed03a8f9b2219f87f66b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7405efdae5591a408eeecd8432f4d9f08c4e127a660f3030de44203c3c0922eb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8905e7a5ebe291c4c37350ab768de403894589a231780c1bd57dc8f745f8e50(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760917f8a84d9a86f51a29e4372964602e0d24abd07422406073fb0c4c68dae6(
    value: typing.Optional[typing.Union[CfnLifecyclePolicy.PolicyDetailsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f69033f85aa6e93437b96753874c8e34f5c4ffe06abdf4c788a6dbaa5635280(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef44f019348f0f733d7925ac1fa007c5c5c3527ee9afa5ae866fae88297a400(
    *,
    cross_region_copy: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLifecyclePolicy.CrossRegionCopyActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ab41ea31149bce42181e0f814679204be90120b23772030bc7078305493879(
    *,
    retention_archive_tier: typing.Union[typing.Union[CfnLifecyclePolicy.RetentionArchiveTierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5aec62a64a79d285afc0a7116dee0eddb18ebf21c9fa48eb03bf35f88e6fd3(
    *,
    retain_rule: typing.Union[typing.Union[CfnLifecyclePolicy.ArchiveRetainRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3bd86211bb978a74c5c16dc6b900331d304b5410ac087ea495abdd86c2453b(
    *,
    cron_expression: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    times: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5239dc01669527fe9d69bcf001cbe05b2fb18145f3b2a2326d26b4188997167(
    *,
    encryption_configuration: typing.Union[typing.Union[CfnLifecyclePolicy.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    target: builtins.str,
    retain_rule: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f70ff3e76c651f5d2027b29a4cb6e1f8b49c37de4242fa30d7c1258f1fdcfe(
    *,
    interval: jsii.Number,
    interval_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6042a86efa61f0e2417eede12b9e7cc8a8cfa411b45483aad6458458e18bbf(
    *,
    interval: jsii.Number,
    interval_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52724520e4663413779515ac0a81f4e1699e35be8d9a6e2da264867e0e38020(
    *,
    encrypted: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    cmk_arn: typing.Optional[builtins.str] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    deprecate_rule: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.CrossRegionCopyDeprecateRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    retain_rule: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    target: typing.Optional[builtins.str] = None,
    target_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df14d4bb615620f32764eca51a53a15b4d82601702149b76a666dcb946231c8(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352778721ec9c4131a3d5743a1771db46ff29f75ac21a1a7e6fdb7b15af2f9c4(
    *,
    encrypted: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    cmk_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f908840a2529a0a266439f1220891ee20f80445a7fa86acb16b138db840b73eb(
    *,
    event_type: builtins.str,
    snapshot_owner: typing.Sequence[builtins.str],
    description_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b43aebdfc2a5c8f6e152c717ca2852d3dede90be3dddf82df2f7b44bd00b4d(
    *,
    type: builtins.str,
    parameters: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.EventParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5198fcd4df82372f6ba436315f8c32af3bf8b1254dd23dd21d075c8224ff65(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8a03b9d445f7c6856ba1086d442ce3fcbcd4c518272cd3455cc4f4d2e460a4(
    *,
    exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    exclude_data_volume_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    no_reboot: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc225292eba74253b17b8544d6fe2b3bbfc6bf64194a57d8183dddce529b249(
    *,
    actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLifecyclePolicy.ActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    event_source: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.EventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    parameters: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.ParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    policy_type: typing.Optional[builtins.str] = None,
    resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    schedules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLifecyclePolicy.ScheduleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    target_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972486b102e1bf60dc205682fb6d23f4bcf390f88b0c62e3d48456befe08407a(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7371a1ba72418ff82e67c0e8e6dd226ddb6779df3e3558d7c6c394624d5dca(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf126a38043d201643fed4f4b3c71c9b3fb21e3b3b0321ab8647555a35617ec0(
    *,
    archive_rule: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.ArchiveRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    create_rule: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.CreateRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cross_region_copy_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLifecyclePolicy.CrossRegionCopyRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    deprecate_rule: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.DeprecateRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    fast_restore_rule: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.FastRestoreRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    retain_rule: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.RetainRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    share_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLifecyclePolicy.ShareRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags_to_add: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    variable_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54316211badc49f9081340f52d5c10940ac84450ece4923729aac060213055fc(
    *,
    target_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    unshare_interval: typing.Optional[jsii.Number] = None,
    unshare_interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764a317923b196bfc4390c0815a72b55d4943581f5bc973c741656da964f633c(
    *,
    description: typing.Optional[builtins.str] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    policy_details: typing.Optional[typing.Union[typing.Union[CfnLifecyclePolicy.PolicyDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
