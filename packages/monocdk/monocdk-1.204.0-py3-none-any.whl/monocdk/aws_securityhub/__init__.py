'''
# AWS Security Hub Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as securityhub
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for SecurityHub construct libraries](https://constructs.dev/search?q=securityhub)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::SecurityHub resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SecurityHub.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::SecurityHub](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SecurityHub.html).

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
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnHub(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_securityhub.CfnHub",
):
    '''A CloudFormation ``AWS::SecurityHub::Hub``.

    The ``AWS::SecurityHub::Hub`` resource represents the implementation of the AWS Security Hub service in your account. One hub resource is created for each Region in which you enable Security Hub .

    The CIS AWS Foundations Benchmark standard and the Foundational Security Best Practices standard are also enabled in each Region where you enable Security Hub .

    :cloudformationResource: AWS::SecurityHub::Hub
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_securityhub as securityhub
        
        # tags: Any
        
        cfn_hub = securityhub.CfnHub(self, "MyCfnHub",
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::SecurityHub::Hub``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param tags: The tags to add to the hub resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19560a3ab750ab426ff2fb32b87e7fc787bbe1dca90280b6cae12629409fb943)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHubProps(tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d0f700735899763db99721b646c52fc024d441916a18e5163170c9f245e45f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b7e0cc8221273625f97a3ac30739aa5bb19fe03938bf844fda597389af0496)
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to add to the hub resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html#cfn-securityhub-hub-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="monocdk.aws_securityhub.CfnHubProps",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class CfnHubProps:
    def __init__(self, *, tags: typing.Any = None) -> None:
        '''Properties for defining a ``CfnHub``.

        :param tags: The tags to add to the hub resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_securityhub as securityhub
            
            # tags: Any
            
            cfn_hub_props = securityhub.CfnHubProps(
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197da5aa5d51e8285630d563d64d493f05f3c87cc1a2d1c615a93681b4d8a578)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags to add to the hub resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html#cfn-securityhub-hub-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHubProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnHub",
    "CfnHubProps",
]

publication.publish()

def _typecheckingstub__19560a3ab750ab426ff2fb32b87e7fc787bbe1dca90280b6cae12629409fb943(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d0f700735899763db99721b646c52fc024d441916a18e5163170c9f245e45f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b7e0cc8221273625f97a3ac30739aa5bb19fe03938bf844fda597389af0496(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197da5aa5d51e8285630d563d64d493f05f3c87cc1a2d1c615a93681b4d8a578(
    *,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
