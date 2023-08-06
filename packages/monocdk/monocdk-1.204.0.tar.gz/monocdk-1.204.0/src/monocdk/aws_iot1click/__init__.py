'''
# AWS IoT 1-Click Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as iot1click
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for IoT1Click construct libraries](https://constructs.dev/search?q=iot1click)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::IoT1Click resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoT1Click.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::IoT1Click](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoT1Click.html).

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
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnDevice(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot1click.CfnDevice",
):
    '''A CloudFormation ``AWS::IoT1Click::Device``.

    The ``AWS::IoT1Click::Device`` resource controls the enabled state of an AWS IoT 1-Click compatible device. For more information, see `Device <https://docs.aws.amazon.com/iot-1-click/1.0/devices-apireference/devices-deviceid.html>`_ in the *AWS IoT 1-Click Devices API Reference* .

    :cloudformationResource: AWS::IoT1Click::Device
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iot1click as iot1click
        
        cfn_device = iot1click.CfnDevice(self, "MyCfnDevice",
            device_id="deviceId",
            enabled=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        device_id: builtins.str,
        enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::IoT1Click::Device``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param device_id: The ID of the device, such as ``G030PX0312744DWM`` .
        :param enabled: A Boolean value indicating whether the device is enabled ( ``true`` ) or not ( ``false`` ).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50fcaa6bf2619d89ac39763ea604e83e5ec6863fe1c7f70c9c100cb42d8e641)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeviceProps(device_id=device_id, enabled=enabled)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27567b3e1d332d2d1a3305f122f6b9176423f3756c214fd62f418a53214f123f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5780f29dd6bcf32cc4748b83fe77100840f0bd3f0d7b5471ad782bfb7f8ae0bc)
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
        '''The ARN of the device, such as ``arn:aws:iot1click:us-west-2:123456789012:devices/G030PX0312744DWM`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDeviceId")
    def attr_device_id(self) -> builtins.str:
        '''The unique identifier of the device.

        :cloudformationAttribute: DeviceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeviceId"))

    @builtins.property
    @jsii.member(jsii_name="attrEnabled")
    def attr_enabled(self) -> _IResolvable_a771d0ef:
        '''A Boolean value indicating whether the device is enabled ( ``true`` ) or not ( ``false`` ).

        :cloudformationAttribute: Enabled
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrEnabled"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        '''The ID of the device, such as ``G030PX0312744DWM`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html#cfn-iot1click-device-deviceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "deviceId"))

    @device_id.setter
    def device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340984acc855e0ffadf41003365998463cd9da665fae00331731bae5c9eb6fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceId", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        '''A Boolean value indicating whether the device is enabled ( ``true`` ) or not ( ``false`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html#cfn-iot1click-device-enabled
        '''
        return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8bf6085661fc98d97d2d8f61023b8923bb914e9b1c6555c3a83e7196c5017c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iot1click.CfnDeviceProps",
    jsii_struct_bases=[],
    name_mapping={"device_id": "deviceId", "enabled": "enabled"},
)
class CfnDeviceProps:
    def __init__(
        self,
        *,
        device_id: builtins.str,
        enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``CfnDevice``.

        :param device_id: The ID of the device, such as ``G030PX0312744DWM`` .
        :param enabled: A Boolean value indicating whether the device is enabled ( ``true`` ) or not ( ``false`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iot1click as iot1click
            
            cfn_device_props = iot1click.CfnDeviceProps(
                device_id="deviceId",
                enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bebd5127ff068a673bae6f346ba6d24c94934294da259d24b0058bc453af952)
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "device_id": device_id,
            "enabled": enabled,
        }

    @builtins.property
    def device_id(self) -> builtins.str:
        '''The ID of the device, such as ``G030PX0312744DWM`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html#cfn-iot1click-device-deviceid
        '''
        result = self._values.get("device_id")
        assert result is not None, "Required property 'device_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        '''A Boolean value indicating whether the device is enabled ( ``true`` ) or not ( ``false`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html#cfn-iot1click-device-enabled
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPlacement(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot1click.CfnPlacement",
):
    '''A CloudFormation ``AWS::IoT1Click::Placement``.

    The ``AWS::IoT1Click::Placement`` resource creates a placement to be associated with an AWS IoT 1-Click project. A placement is an instance of a device in a location. For more information, see `Projects, Templates, and Placements <https://docs.aws.amazon.com/iot-1-click/latest/developerguide/1click-PTP.html>`_ in the *AWS IoT 1-Click Developer Guide* .

    :cloudformationResource: AWS::IoT1Click::Placement
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iot1click as iot1click
        
        # associated_devices: Any
        # attributes: Any
        
        cfn_placement = iot1click.CfnPlacement(self, "MyCfnPlacement",
            project_name="projectName",
        
            # the properties below are optional
            associated_devices=associated_devices,
            attributes=attributes,
            placement_name="placementName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        project_name: builtins.str,
        associated_devices: typing.Any = None,
        attributes: typing.Any = None,
        placement_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IoT1Click::Placement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param project_name: The name of the project containing the placement.
        :param associated_devices: The devices to associate with the placement, as defined by a mapping of zero or more key-value pairs wherein the key is a template name and the value is a device ID.
        :param attributes: The user-defined attributes associated with the placement.
        :param placement_name: The name of the placement.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e301de0e97436376443f4bdfe5e86cc1543b5e606ac52850890e509b23da4d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPlacementProps(
            project_name=project_name,
            associated_devices=associated_devices,
            attributes=attributes,
            placement_name=placement_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c120957e1c58bc83fc35bd62879e9677fae11635392ccca231e3871c4428b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__629a8470569b83d344c6a37277d15cbfb736fd99b19b441cd3edb40930554614)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPlacementName")
    def attr_placement_name(self) -> builtins.str:
        '''The name of the placement, such as ``floor17`` .

        :cloudformationAttribute: PlacementName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPlacementName"))

    @builtins.property
    @jsii.member(jsii_name="attrProjectName")
    def attr_project_name(self) -> builtins.str:
        '''The name of the project containing the placement, such as ``conference-rooms`` .

        :cloudformationAttribute: ProjectName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProjectName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="associatedDevices")
    def associated_devices(self) -> typing.Any:
        '''The devices to associate with the placement, as defined by a mapping of zero or more key-value pairs wherein the key is a template name and the value is a device ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-associateddevices
        '''
        return typing.cast(typing.Any, jsii.get(self, "associatedDevices"))

    @associated_devices.setter
    def associated_devices(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26caa826477a586447fab611612cfeb87ed582572400178161256a3904e2b92b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedDevices", value)

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Any:
        '''The user-defined attributes associated with the placement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-attributes
        '''
        return typing.cast(typing.Any, jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16ef3b7f64438ae6e662cbf6b48a74ddfcaa235188721daf81ad0be74cb1fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value)

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        '''The name of the project containing the placement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-projectname
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectName"))

    @project_name.setter
    def project_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72be795107d572d5ba798b7f117a3517220c0ee9387d70b3459760672fb5b795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectName", value)

    @builtins.property
    @jsii.member(jsii_name="placementName")
    def placement_name(self) -> typing.Optional[builtins.str]:
        '''The name of the placement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-placementname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "placementName"))

    @placement_name.setter
    def placement_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf05b02207126907d0c358a8db0da28faafc1b4f8b62513737297b1a63ec489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iot1click.CfnPlacementProps",
    jsii_struct_bases=[],
    name_mapping={
        "project_name": "projectName",
        "associated_devices": "associatedDevices",
        "attributes": "attributes",
        "placement_name": "placementName",
    },
)
class CfnPlacementProps:
    def __init__(
        self,
        *,
        project_name: builtins.str,
        associated_devices: typing.Any = None,
        attributes: typing.Any = None,
        placement_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPlacement``.

        :param project_name: The name of the project containing the placement.
        :param associated_devices: The devices to associate with the placement, as defined by a mapping of zero or more key-value pairs wherein the key is a template name and the value is a device ID.
        :param attributes: The user-defined attributes associated with the placement.
        :param placement_name: The name of the placement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iot1click as iot1click
            
            # associated_devices: Any
            # attributes: Any
            
            cfn_placement_props = iot1click.CfnPlacementProps(
                project_name="projectName",
            
                # the properties below are optional
                associated_devices=associated_devices,
                attributes=attributes,
                placement_name="placementName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1c2f44a831f0a5790c1649f8284ad76c7918c91f0aaa0a8b93288a8c379ea2)
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument associated_devices", value=associated_devices, expected_type=type_hints["associated_devices"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument placement_name", value=placement_name, expected_type=type_hints["placement_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_name": project_name,
        }
        if associated_devices is not None:
            self._values["associated_devices"] = associated_devices
        if attributes is not None:
            self._values["attributes"] = attributes
        if placement_name is not None:
            self._values["placement_name"] = placement_name

    @builtins.property
    def project_name(self) -> builtins.str:
        '''The name of the project containing the placement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-projectname
        '''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def associated_devices(self) -> typing.Any:
        '''The devices to associate with the placement, as defined by a mapping of zero or more key-value pairs wherein the key is a template name and the value is a device ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-associateddevices
        '''
        result = self._values.get("associated_devices")
        return typing.cast(typing.Any, result)

    @builtins.property
    def attributes(self) -> typing.Any:
        '''The user-defined attributes associated with the placement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Any, result)

    @builtins.property
    def placement_name(self) -> typing.Optional[builtins.str]:
        '''The name of the placement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-placementname
        '''
        result = self._values.get("placement_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlacementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnProject(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot1click.CfnProject",
):
    '''A CloudFormation ``AWS::IoT1Click::Project``.

    The ``AWS::IoT1Click::Project`` resource creates an empty project with a placement template. A project contains zero or more placements that adhere to the placement template defined in the project. For more information, see `CreateProject <https://docs.aws.amazon.com/iot-1-click/latest/projects-apireference/API_CreateProject.html>`_ in the *AWS IoT 1-Click Projects API Reference* .

    :cloudformationResource: AWS::IoT1Click::Project
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iot1click as iot1click
        
        # callback_overrides: Any
        # default_attributes: Any
        
        cfn_project = iot1click.CfnProject(self, "MyCfnProject",
            placement_template=iot1click.CfnProject.PlacementTemplateProperty(
                default_attributes=default_attributes,
                device_templates={
                    "device_templates_key": iot1click.CfnProject.DeviceTemplateProperty(
                        callback_overrides=callback_overrides,
                        device_type="deviceType"
                    )
                }
            ),
        
            # the properties below are optional
            description="description",
            project_name="projectName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        placement_template: typing.Union[typing.Union["CfnProject.PlacementTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IoT1Click::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param placement_template: An object describing the project's placement specifications.
        :param description: The description of the project.
        :param project_name: The name of the project from which to obtain information.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b7cd485f6a1d2c0874086b210164acc5151dc129bba478d92bc12fd2b2c501)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProjectProps(
            placement_template=placement_template,
            description=description,
            project_name=project_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f8e0e79027b5dc4a25669066e1b47edc0ca5d7516573f180768f0f65b33a2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c86a9d0137d16db4b8c88b3dd1251450d143e272fd83da7f41865f805700d4)
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
        '''The Amazon Resource Name (ARN) of the project, such as ``arn:aws:iot1click:us-east-1:123456789012:projects/project-a1bzhi`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProjectName")
    def attr_project_name(self) -> builtins.str:
        '''The name of the project, such as ``project-a1bzhi`` .

        :cloudformationAttribute: ProjectName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProjectName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="placementTemplate")
    def placement_template(
        self,
    ) -> typing.Union["CfnProject.PlacementTemplateProperty", _IResolvable_a771d0ef]:
        '''An object describing the project's placement specifications.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-placementtemplate
        '''
        return typing.cast(typing.Union["CfnProject.PlacementTemplateProperty", _IResolvable_a771d0ef], jsii.get(self, "placementTemplate"))

    @placement_template.setter
    def placement_template(
        self,
        value: typing.Union["CfnProject.PlacementTemplateProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357cd81fd465e3224b567df28758f5e9b8e70f95c2e5232449dbd170c753bf0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ff4c8cdad8e7bb07492d86d6e8b95ee36e47335bba535c40a5ba98ee430778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> typing.Optional[builtins.str]:
        '''The name of the project from which to obtain information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-projectname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectName"))

    @project_name.setter
    def project_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ffd728f82e79afb313117c8fd2295478467de07c52e1e81ec8499adfd5aaf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iot1click.CfnProject.DeviceTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "callback_overrides": "callbackOverrides",
            "device_type": "deviceType",
        },
    )
    class DeviceTemplateProperty:
        def __init__(
            self,
            *,
            callback_overrides: typing.Any = None,
            device_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''In AWS CloudFormation , use the ``DeviceTemplate`` property type to define the template for an AWS IoT 1-Click project.

            ``DeviceTemplate`` is a property of the ``AWS::IoT1Click::Project`` resource.

            :param callback_overrides: An optional AWS Lambda function to invoke instead of the default AWS Lambda function provided by the placement template.
            :param device_type: The device type, which currently must be ``"button"`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-devicetemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iot1click as iot1click
                
                # callback_overrides: Any
                
                device_template_property = iot1click.CfnProject.DeviceTemplateProperty(
                    callback_overrides=callback_overrides,
                    device_type="deviceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__089bd9a2ed7efe7f00dce431c2fe511cb33e6a8caf7c8240b79025d846066d01)
                check_type(argname="argument callback_overrides", value=callback_overrides, expected_type=type_hints["callback_overrides"])
                check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if callback_overrides is not None:
                self._values["callback_overrides"] = callback_overrides
            if device_type is not None:
                self._values["device_type"] = device_type

        @builtins.property
        def callback_overrides(self) -> typing.Any:
            '''An optional AWS Lambda function to invoke instead of the default AWS Lambda function provided by the placement template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-devicetemplate.html#cfn-iot1click-project-devicetemplate-callbackoverrides
            '''
            result = self._values.get("callback_overrides")
            return typing.cast(typing.Any, result)

        @builtins.property
        def device_type(self) -> typing.Optional[builtins.str]:
            '''The device type, which currently must be ``"button"`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-devicetemplate.html#cfn-iot1click-project-devicetemplate-devicetype
            '''
            result = self._values.get("device_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iot1click.CfnProject.PlacementTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_attributes": "defaultAttributes",
            "device_templates": "deviceTemplates",
        },
    )
    class PlacementTemplateProperty:
        def __init__(
            self,
            *,
            default_attributes: typing.Any = None,
            device_templates: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnProject.DeviceTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''In AWS CloudFormation , use the ``PlacementTemplate`` property type to define the template for an AWS IoT 1-Click project.

            ``PlacementTemplate`` is a property of the ``AWS::IoT1Click::Project`` resource.

            :param default_attributes: The default attributes (key-value pairs) to be applied to all placements using this template.
            :param device_templates: An object specifying the `DeviceTemplate <https://docs.aws.amazon.com/iot-1-click/latest/projects-apireference/API_DeviceTemplate.html>`_ for all placements using this ( `PlacementTemplate <https://docs.aws.amazon.com/iot-1-click/latest/projects-apireference/API_PlacementTemplate.html>`_ ) template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-placementtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iot1click as iot1click
                
                # callback_overrides: Any
                # default_attributes: Any
                
                placement_template_property = iot1click.CfnProject.PlacementTemplateProperty(
                    default_attributes=default_attributes,
                    device_templates={
                        "device_templates_key": iot1click.CfnProject.DeviceTemplateProperty(
                            callback_overrides=callback_overrides,
                            device_type="deviceType"
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b3774bcb36dcd70416321f01998016b0b4a03b589e2b14cfb0780dcf35f44a0)
                check_type(argname="argument default_attributes", value=default_attributes, expected_type=type_hints["default_attributes"])
                check_type(argname="argument device_templates", value=device_templates, expected_type=type_hints["device_templates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_attributes is not None:
                self._values["default_attributes"] = default_attributes
            if device_templates is not None:
                self._values["device_templates"] = device_templates

        @builtins.property
        def default_attributes(self) -> typing.Any:
            '''The default attributes (key-value pairs) to be applied to all placements using this template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-placementtemplate.html#cfn-iot1click-project-placementtemplate-defaultattributes
            '''
            result = self._values.get("default_attributes")
            return typing.cast(typing.Any, result)

        @builtins.property
        def device_templates(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnProject.DeviceTemplateProperty", _IResolvable_a771d0ef]]]]:
            '''An object specifying the `DeviceTemplate <https://docs.aws.amazon.com/iot-1-click/latest/projects-apireference/API_DeviceTemplate.html>`_ for all placements using this ( `PlacementTemplate <https://docs.aws.amazon.com/iot-1-click/latest/projects-apireference/API_PlacementTemplate.html>`_ ) template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-placementtemplate.html#cfn-iot1click-project-placementtemplate-devicetemplates
            '''
            result = self._values.get("device_templates")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnProject.DeviceTemplateProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iot1click.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "placement_template": "placementTemplate",
        "description": "description",
        "project_name": "projectName",
    },
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        placement_template: typing.Union[typing.Union[CfnProject.PlacementTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnProject``.

        :param placement_template: An object describing the project's placement specifications.
        :param description: The description of the project.
        :param project_name: The name of the project from which to obtain information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iot1click as iot1click
            
            # callback_overrides: Any
            # default_attributes: Any
            
            cfn_project_props = iot1click.CfnProjectProps(
                placement_template=iot1click.CfnProject.PlacementTemplateProperty(
                    default_attributes=default_attributes,
                    device_templates={
                        "device_templates_key": iot1click.CfnProject.DeviceTemplateProperty(
                            callback_overrides=callback_overrides,
                            device_type="deviceType"
                        )
                    }
                ),
            
                # the properties below are optional
                description="description",
                project_name="projectName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f50328a90437e767303bc86c8f98688ca2eb29fd0b604b11e77b4d2529a3c80)
            check_type(argname="argument placement_template", value=placement_template, expected_type=type_hints["placement_template"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "placement_template": placement_template,
        }
        if description is not None:
            self._values["description"] = description
        if project_name is not None:
            self._values["project_name"] = project_name

    @builtins.property
    def placement_template(
        self,
    ) -> typing.Union[CfnProject.PlacementTemplateProperty, _IResolvable_a771d0ef]:
        '''An object describing the project's placement specifications.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-placementtemplate
        '''
        result = self._values.get("placement_template")
        assert result is not None, "Required property 'placement_template' is missing"
        return typing.cast(typing.Union[CfnProject.PlacementTemplateProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the project.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''The name of the project from which to obtain information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-projectname
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDevice",
    "CfnDeviceProps",
    "CfnPlacement",
    "CfnPlacementProps",
    "CfnProject",
    "CfnProjectProps",
]

publication.publish()

def _typecheckingstub__e50fcaa6bf2619d89ac39763ea604e83e5ec6863fe1c7f70c9c100cb42d8e641(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    device_id: builtins.str,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27567b3e1d332d2d1a3305f122f6b9176423f3756c214fd62f418a53214f123f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5780f29dd6bcf32cc4748b83fe77100840f0bd3f0d7b5471ad782bfb7f8ae0bc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340984acc855e0ffadf41003365998463cd9da665fae00331731bae5c9eb6fed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bf6085661fc98d97d2d8f61023b8923bb914e9b1c6555c3a83e7196c5017c9(
    value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bebd5127ff068a673bae6f346ba6d24c94934294da259d24b0058bc453af952(
    *,
    device_id: builtins.str,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e301de0e97436376443f4bdfe5e86cc1543b5e606ac52850890e509b23da4d6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    project_name: builtins.str,
    associated_devices: typing.Any = None,
    attributes: typing.Any = None,
    placement_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c120957e1c58bc83fc35bd62879e9677fae11635392ccca231e3871c4428b3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629a8470569b83d344c6a37277d15cbfb736fd99b19b441cd3edb40930554614(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26caa826477a586447fab611612cfeb87ed582572400178161256a3904e2b92b(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16ef3b7f64438ae6e662cbf6b48a74ddfcaa235188721daf81ad0be74cb1fec(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72be795107d572d5ba798b7f117a3517220c0ee9387d70b3459760672fb5b795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf05b02207126907d0c358a8db0da28faafc1b4f8b62513737297b1a63ec489(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1c2f44a831f0a5790c1649f8284ad76c7918c91f0aaa0a8b93288a8c379ea2(
    *,
    project_name: builtins.str,
    associated_devices: typing.Any = None,
    attributes: typing.Any = None,
    placement_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b7cd485f6a1d2c0874086b210164acc5151dc129bba478d92bc12fd2b2c501(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    placement_template: typing.Union[typing.Union[CfnProject.PlacementTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f8e0e79027b5dc4a25669066e1b47edc0ca5d7516573f180768f0f65b33a2b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c86a9d0137d16db4b8c88b3dd1251450d143e272fd83da7f41865f805700d4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357cd81fd465e3224b567df28758f5e9b8e70f95c2e5232449dbd170c753bf0f(
    value: typing.Union[CfnProject.PlacementTemplateProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ff4c8cdad8e7bb07492d86d6e8b95ee36e47335bba535c40a5ba98ee430778(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ffd728f82e79afb313117c8fd2295478467de07c52e1e81ec8499adfd5aaf9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089bd9a2ed7efe7f00dce431c2fe511cb33e6a8caf7c8240b79025d846066d01(
    *,
    callback_overrides: typing.Any = None,
    device_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3774bcb36dcd70416321f01998016b0b4a03b589e2b14cfb0780dcf35f44a0(
    *,
    default_attributes: typing.Any = None,
    device_templates: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnProject.DeviceTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f50328a90437e767303bc86c8f98688ca2eb29fd0b604b11e77b4d2529a3c80(
    *,
    placement_template: typing.Union[typing.Union[CfnProject.PlacementTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
