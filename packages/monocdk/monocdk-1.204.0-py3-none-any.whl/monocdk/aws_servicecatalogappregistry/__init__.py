'''
# AWS ServiceCatalogAppRegistry Construct Library

[AWS Service Catalog App Registry](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/appregistry.html)
enables organizations to create and manage repositores of applications and associated resources.

## Table Of Contents

* [Application](#application)
* [Attribute-Group](#attribute-group)
* [Associations](#associations)

  * [Associating application with an attribute group](#attribute-group-association)
  * [Associating application with a stack](#resource-association)

The `@aws-cdk/aws-servicecatalogappregistry` package contains resources that enable users to automate governance and management of their AWS resources at scale.

```python
import monocdk as appreg
```

## Application

An AppRegistry application enables you to define your applications and associated resources.
The application name must be unique at the account level, but is mutable.

```python
application = appreg.Application(self, "MyFirstApplication",
    application_name="MyFirstApplicationName",
    description="description for my application"
)
```

An application that has been created outside of the stack can be imported into your CDK app.
Applications can be imported by their ARN via the `Application.fromApplicationArn()` API:

```python
imported_application = appreg.Application.from_application_arn(self, "MyImportedApplication", "arn:aws:servicecatalog:us-east-1:012345678910:/applications/0aqmvxvgmry0ecc4mjhwypun6i")
```

## Attribute Group

An AppRegistry attribute group acts as a container for user-defined attributes for an application.
Metadata is attached in a machine-readble format to integrate with automated workflows and tools.

```python
attribute_group = appreg.AttributeGroup(self, "MyFirstAttributeGroup",
    attribute_group_name="MyFirstAttributeGroupName",
    description="description for my attribute group",  # the description is optional,
    attributes={
        "project": "foo",
        "team": ["member1", "member2", "member3"],
        "public": False,
        "stages": {
            "alpha": "complete",
            "beta": "incomplete",
            "release": "not started"
        }
    }
)
```

An attribute group that has been created outside of the stack can be imported into your CDK app.
Attribute groups can be imported by their ARN via the `AttributeGroup.fromAttributeGroupArn()` API:

```python
imported_attribute_group = appreg.AttributeGroup.from_attribute_group_arn(self, "MyImportedAttrGroup", "arn:aws:servicecatalog:us-east-1:012345678910:/attribute-groups/0aqmvxvgmry0ecc4mjhwypun6i")
```

## Associations

You can associate your appregistry application with attribute groups and resources.
Resources are CloudFormation stacks that you can associate with an application to group relevant
stacks together to enable metadata rich insights into your applications and resources.
A Cloudformation stack can only be associated with one appregistry application.
If a stack is associated with multiple applications in your app or is already associated with one,
CDK will fail at deploy time.

### Associating application with an attribute group

You can associate an attribute group with an application with the `associateAttributeGroup()` API:

```python
# application: appreg.Application
# attribute_group: appreg.AttributeGroup

application.associate_attribute_group(attribute_group)
```

### Associating application with a Stack

You can associate a stack with an application with the `associateStack()` API:

```python
# application: appreg.Application
app = App()
my_stack = Stack(app, "MyStack")
application.associate_stack(my_stack)
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
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    Stack as _Stack_9f43e4a3,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.ApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName", "description": "description"},
)
class ApplicationProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a Service Catalog AppRegistry Application.

        :param application_name: (experimental) Enforces a particular physical application name.
        :param description: (experimental) Description for application. Default: - No description provided

        :stability: experimental
        :exampleMetadata: infused

        Example::

            application = appreg.Application(self, "MyFirstApplication",
                application_name="MyFirstApplicationName",
                description="description for my application"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd697e58a8ebc0f11b44ab160600f3677cb68e30a649922754e06feb856f0e7c)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_name": application_name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def application_name(self) -> builtins.str:
        '''(experimental) Enforces a particular physical application name.

        :stability: experimental
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for application.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.AttributeGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_group_name": "attributeGroupName",
        "attributes": "attributes",
        "description": "description",
    },
)
class AttributeGroupProps:
    def __init__(
        self,
        *,
        attribute_group_name: builtins.str,
        attributes: typing.Mapping[builtins.str, typing.Any],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a Service Catalog AppRegistry Attribute Group.

        :param attribute_group_name: (experimental) Enforces a particular physical attribute group name.
        :param attributes: (experimental) A JSON of nested key-value pairs that represent the attributes in the group. Attributes maybe an empty JSON '{}', but must be explicitly stated.
        :param description: (experimental) Description for attribute group. Default: - No description provided

        :stability: experimental
        :exampleMetadata: infused

        Example::

            attribute_group = appreg.AttributeGroup(self, "MyFirstAttributeGroup",
                attribute_group_name="MyFirstAttributeGroupName",
                description="description for my attribute group",  # the description is optional,
                attributes={
                    "project": "foo",
                    "team": ["member1", "member2", "member3"],
                    "public": False,
                    "stages": {
                        "alpha": "complete",
                        "beta": "incomplete",
                        "release": "not started"
                    }
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc62dec6de3a3b0965f74419f1076daae5a13f0d85496ef982000afcd7c64ae)
            check_type(argname="argument attribute_group_name", value=attribute_group_name, expected_type=type_hints["attribute_group_name"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute_group_name": attribute_group_name,
            "attributes": attributes,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def attribute_group_name(self) -> builtins.str:
        '''(experimental) Enforces a particular physical attribute group name.

        :stability: experimental
        '''
        result = self._values.get("attribute_group_name")
        assert result is not None, "Required property 'attribute_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) A JSON of nested key-value pairs that represent the attributes in the group.

        Attributes maybe an empty JSON '{}', but must be explicitly stated.

        :stability: experimental
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for attribute group.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttributeGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnApplication",
):
    '''A CloudFormation ``AWS::ServiceCatalogAppRegistry::Application``.

    Represents a AWS Service Catalog AppRegistry application that is the top-level node in a hierarchy of related cloud resource abstractions.

    :cloudformationResource: AWS::ServiceCatalogAppRegistry::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalogappregistry as servicecatalogappregistry
        
        cfn_application = servicecatalogappregistry.CfnApplication(self, "MyCfnApplication",
            name="name",
        
            # the properties below are optional
            description="description",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalogAppRegistry::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the application. The name must be unique in the region in which you are creating the application.
        :param description: The description of the application.
        :param tags: Key-value pairs you can use to associate with the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc9f7ffb1722eb580263626543856be0b7a1a697054cab335964930db4997a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016e95f37dbfb5de1159d0563b94188f3b0ed42b93d07ee445028710c8f98d56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fba157846fd7cef56224c2406925177d4125df29bcea573795ce4c283a794ff)
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
        '''The Amazon resource name (ARN) that specifies the application across services.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier of the application.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs you can use to associate with the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the application.

        The name must be unique in the region in which you are creating the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103b687a09dc11773e7f3a819bc28af2e7a9c809b6e08e87a67a3ec4124f90a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c99ab990ea60a95b26e7a44b53742ecda6273696f54c58a743be3421c96423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param name: The name of the application. The name must be unique in the region in which you are creating the application.
        :param description: The description of the application.
        :param tags: Key-value pairs you can use to associate with the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalogappregistry as servicecatalogappregistry
            
            cfn_application_props = servicecatalogappregistry.CfnApplicationProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef1ddc254084a352873d53fc5e9a79aebba677e8b2ba04bac5b0e6cccb2a2a4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the application.

        The name must be unique in the region in which you are creating the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs you can use to associate with the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAttributeGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroup",
):
    '''A CloudFormation ``AWS::ServiceCatalogAppRegistry::AttributeGroup``.

    Creates a new attribute group as a container for user-defined attributes. This feature enables users to have full control over their cloud application's metadata in a rich machine-readable format to facilitate integration with automated workflows and third-party tools.

    :cloudformationResource: AWS::ServiceCatalogAppRegistry::AttributeGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalogappregistry as servicecatalogappregistry
        
        # attributes: Any
        
        cfn_attribute_group = servicecatalogappregistry.CfnAttributeGroup(self, "MyCfnAttributeGroup",
            attributes=attributes,
            name="name",
        
            # the properties below are optional
            description="description",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        attributes: typing.Any,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalogAppRegistry::AttributeGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attributes: A nested object in a JSON or YAML template that supports arbitrary definitions. Represents the attributes in an attribute group that describes an application and its components.
        :param name: The name of the attribute group.
        :param description: The description of the attribute group that the user provides.
        :param tags: Key-value pairs you can use to associate with the attribute group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e264f2d622241fc342a5bc848edde1ddc028c7a4c4db5d69408bd5371c94fb51)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAttributeGroupProps(
            attributes=attributes, name=name, description=description, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9264572f621c69a72b9fb8c3f81a99c455887fa2b2803614db81ccbdf84c4c62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb930ee7cdc83ef615f27582579801cf4a51c031b5c6f62df506a6ed8c98ff6f)
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
        '''The Amazon resource name (ARN) that specifies the attribute group across services.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The globally unique attribute group identifier of the attribute group.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key-value pairs you can use to associate with the attribute group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Any:
        '''A nested object in a JSON or YAML template that supports arbitrary definitions.

        Represents the attributes in an attribute group that describes an application and its components.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-attributes
        '''
        return typing.cast(typing.Any, jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142f9c71cc5729ae50b64ece0d3c85dee1d83cc1800ed9e63b99d84b990bb191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the attribute group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6253cc404dffceab80d11cfd538dae9827f627a4f832fa80d4ca6f0daf127c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the attribute group that the user provides.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d07be8bb1d691e26c4eadf398288256d0fcf1a53995c01d774cadd09a91087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnAttributeGroupAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroupAssociation",
):
    '''A CloudFormation ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation``.

    Associates an attribute group with an application to augment the application's metadata with the group's attributes. This feature enables applications to be described with user-defined details that are machine-readable, such as third-party integrations.

    :cloudformationResource: AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalogappregistry as servicecatalogappregistry
        
        cfn_attribute_group_association = servicecatalogappregistry.CfnAttributeGroupAssociation(self, "MyCfnAttributeGroupAssociation",
            application="application",
            attribute_group="attributeGroup"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application: builtins.str,
        attribute_group: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: The name or ID of the application.
        :param attribute_group: The name or ID of the attribute group that holds the attributes to describe the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f3c548b9c154bac7210aaac75a02b5b75b8519117e6d64e663447404defba5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAttributeGroupAssociationProps(
            application=application, attribute_group=attribute_group
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5c060c2f8fba52aaa3430ca63284bb8a5ae9fede93c8549e01c1482975fcec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d34f2825b36b1cdca148cdf477dc0ba8d95e1163f8c91c37cc68cbe5d133aec8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationArn")
    def attr_application_arn(self) -> builtins.str:
        '''The Amazon resource name (ARN) of the application that was augmented with attributes.

        :cloudformationAttribute: ApplicationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAttributeGroupArn")
    def attr_attribute_group_arn(self) -> builtins.str:
        '''The Amazon resource name (ARN) of the attribute group that contains the application's new attributes.

        :cloudformationAttribute: AttributeGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAttributeGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The Id of the Association.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        '''The name or ID of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-application
        '''
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @application.setter
    def application(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ba1fbe50b49713ff9a8c266913edcf75266b83d1b3c5c3e75b60e8ab6a13f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "application", value)

    @builtins.property
    @jsii.member(jsii_name="attributeGroup")
    def attribute_group(self) -> builtins.str:
        '''The name or ID of the attribute group that holds the attributes to describe the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-attributegroup
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroup"))

    @attribute_group.setter
    def attribute_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92b1efc999a9dcd2cfe8da98ae567d0cc7163986feb42faad2bfee8187d7ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeGroup", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroupAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"application": "application", "attribute_group": "attributeGroup"},
)
class CfnAttributeGroupAssociationProps:
    def __init__(
        self,
        *,
        application: builtins.str,
        attribute_group: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnAttributeGroupAssociation``.

        :param application: The name or ID of the application.
        :param attribute_group: The name or ID of the attribute group that holds the attributes to describe the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalogappregistry as servicecatalogappregistry
            
            cfn_attribute_group_association_props = servicecatalogappregistry.CfnAttributeGroupAssociationProps(
                application="application",
                attribute_group="attributeGroup"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a86750a936812d3f8ff61f904c8c2ad5cd7d78da1dcbddfc252fdf202c46e8f)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument attribute_group", value=attribute_group, expected_type=type_hints["attribute_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application": application,
            "attribute_group": attribute_group,
        }

    @builtins.property
    def application(self) -> builtins.str:
        '''The name or ID of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-application
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute_group(self) -> builtins.str:
        '''The name or ID of the attribute group that holds the attributes to describe the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-attributegroup
        '''
        result = self._values.get("attribute_group")
        assert result is not None, "Required property 'attribute_group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAttributeGroupAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "name": "name",
        "description": "description",
        "tags": "tags",
    },
)
class CfnAttributeGroupProps:
    def __init__(
        self,
        *,
        attributes: typing.Any,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAttributeGroup``.

        :param attributes: A nested object in a JSON or YAML template that supports arbitrary definitions. Represents the attributes in an attribute group that describes an application and its components.
        :param name: The name of the attribute group.
        :param description: The description of the attribute group that the user provides.
        :param tags: Key-value pairs you can use to associate with the attribute group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalogappregistry as servicecatalogappregistry
            
            # attributes: Any
            
            cfn_attribute_group_props = servicecatalogappregistry.CfnAttributeGroupProps(
                attributes=attributes,
                name="name",
            
                # the properties below are optional
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cfeb4beb644be807870e113dd0ea922361b889124e390f208946c9fe93fa1ef)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attributes": attributes,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def attributes(self) -> typing.Any:
        '''A nested object in a JSON or YAML template that supports arbitrary definitions.

        Represents the attributes in an attribute group that describes an application and its components.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-attributes
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the attribute group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the attribute group that the user provides.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs you can use to associate with the attribute group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAttributeGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourceAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnResourceAssociation",
):
    '''A CloudFormation ``AWS::ServiceCatalogAppRegistry::ResourceAssociation``.

    Associates a resource with an application. Both the resource and the application can be specified either by ID or name.

    :cloudformationResource: AWS::ServiceCatalogAppRegistry::ResourceAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalogappregistry as servicecatalogappregistry
        
        cfn_resource_association = servicecatalogappregistry.CfnResourceAssociation(self, "MyCfnResourceAssociation",
            application="application",
            resource="resource",
            resource_type="resourceType"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application: builtins.str,
        resource: builtins.str,
        resource_type: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalogAppRegistry::ResourceAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: The name or ID of the application.
        :param resource: The name or ID of the resource of which the application will be associated.
        :param resource_type: The type of resource of which the application will be associated.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b469ca6db7dfa9a9c82c19e911d0915f779db93d21681d0cd8b46ad10ecaaa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceAssociationProps(
            application=application, resource=resource, resource_type=resource_type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e93db56115e60e2a5e72381af5dcf3fda564a31457d97519f4a3a9d573b1700)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d692dc3f01e2790374184471df7a071c862b471de45214826cd444aacaa52604)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationArn")
    def attr_application_arn(self) -> builtins.str:
        '''The Amazon resource name (ARN) that specifies the application.

        :cloudformationAttribute: ApplicationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The Id of the Association.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceArn")
    def attr_resource_arn(self) -> builtins.str:
        '''The Amazon resource name (ARN) that specifies the resource.

        :cloudformationAttribute: ResourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        '''The name or ID of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-application
        '''
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @application.setter
    def application(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2a8a079d740c6f7067490c398b49bd89d184dd70926ec7299911a0abe50a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "application", value)

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        '''The name or ID of the resource of which the application will be associated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resource
        '''
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2579810868de368119e062c7e0dcaf191612ec2188b79b794b02df98af121499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        '''The type of resource of which the application will be associated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resourcetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a534234de5559a857834dd71fe01cfc12f061c9ec37df4d1f0bdb0a9bf9bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnResourceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "resource": "resource",
        "resource_type": "resourceType",
    },
)
class CfnResourceAssociationProps:
    def __init__(
        self,
        *,
        application: builtins.str,
        resource: builtins.str,
        resource_type: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnResourceAssociation``.

        :param application: The name or ID of the application.
        :param resource: The name or ID of the resource of which the application will be associated.
        :param resource_type: The type of resource of which the application will be associated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalogappregistry as servicecatalogappregistry
            
            cfn_resource_association_props = servicecatalogappregistry.CfnResourceAssociationProps(
                application="application",
                resource="resource",
                resource_type="resourceType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9ff12e974c8a35d13aa5852f953e7ccf7a06eeccbbd86bce61824ff71a6f98)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application": application,
            "resource": resource,
            "resource_type": resource_type,
        }

    @builtins.property
    def application(self) -> builtins.str:
        '''The name or ID of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-application
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(self) -> builtins.str:
        '''The name or ID of the resource of which the application will be associated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resource
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''The type of resource of which the application will be associated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resourcetype
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_servicecatalogappregistry.IApplication")
class IApplication(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A Service Catalog AppRegistry Application.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''(experimental) The ID of the application.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="associateAttributeGroup")
    def associate_attribute_group(self, attribute_group: "IAttributeGroup") -> None:
        '''(experimental) Associate thisapplication with an attribute group.

        :param attribute_group: AppRegistry attribute group.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="associateStack")
    def associate_stack(self, stack: _Stack_9f43e4a3) -> None:
        '''(experimental) Associate this application with a CloudFormation stack.

        :param stack: a CFN stack.

        :stability: experimental
        '''
        ...


class _IApplicationProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A Service Catalog AppRegistry Application.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_servicecatalogappregistry.IApplication"

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''(experimental) The ID of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @jsii.member(jsii_name="associateAttributeGroup")
    def associate_attribute_group(self, attribute_group: "IAttributeGroup") -> None:
        '''(experimental) Associate thisapplication with an attribute group.

        :param attribute_group: AppRegistry attribute group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74afdce272c1bbde5d9a6553ab36ed880d470a533abbd05a4633b680c79e191e)
            check_type(argname="argument attribute_group", value=attribute_group, expected_type=type_hints["attribute_group"])
        return typing.cast(None, jsii.invoke(self, "associateAttributeGroup", [attribute_group]))

    @jsii.member(jsii_name="associateStack")
    def associate_stack(self, stack: _Stack_9f43e4a3) -> None:
        '''(experimental) Associate this application with a CloudFormation stack.

        :param stack: a CFN stack.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501e11687bc2f5dc6182b2cd7eee4d4608fbe040fa66eceb21f0b4fafe84c1db)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "associateStack", [stack]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplication).__jsii_proxy_class__ = lambda : _IApplicationProxy


@jsii.interface(jsii_type="monocdk.aws_servicecatalogappregistry.IAttributeGroup")
class IAttributeGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A Service Catalog AppRegistry Attribute Group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="attributeGroupArn")
    def attribute_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the attribute group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="attributeGroupId")
    def attribute_group_id(self) -> builtins.str:
        '''(experimental) The ID of the attribute group.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAttributeGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A Service Catalog AppRegistry Attribute Group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_servicecatalogappregistry.IAttributeGroup"

    @builtins.property
    @jsii.member(jsii_name="attributeGroupArn")
    def attribute_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the attribute group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="attributeGroupId")
    def attribute_group_id(self) -> builtins.str:
        '''(experimental) The ID of the attribute group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAttributeGroup).__jsii_proxy_class__ = lambda : _IAttributeGroupProxy


@jsii.implements(IApplication)
class Application(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.Application",
):
    '''(experimental) A Service Catalog AppRegistry Application.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        application = appreg.Application(self, "MyFirstApplication",
            application_name="MyFirstApplicationName",
            description="description for my application"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_name: (experimental) Enforces a particular physical application name.
        :param description: (experimental) Description for application. Default: - No description provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0add5ca44cf4deef52cf4b8555f9e3ac5fa6c1a8db6adf0d1860d10b17c4dabc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationProps(
            application_name=application_name, description=description
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationArn")
    @builtins.classmethod
    def from_application_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        application_arn: builtins.str,
    ) -> IApplication:
        '''(experimental) Imports an Application construct that represents an external application.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param application_arn: the Amazon Resource Name of the existing AppRegistry Application.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595fd678aae6aaa4a5277eb0f8d50c1a4ee27f6b1db7b03a8fc9aeb7bdb91f41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
        return typing.cast(IApplication, jsii.sinvoke(cls, "fromApplicationArn", [scope, id, application_arn]))

    @jsii.member(jsii_name="associateAttributeGroup")
    def associate_attribute_group(self, attribute_group: IAttributeGroup) -> None:
        '''(experimental) Associate an attribute group with application If the attribute group is already associated, it will ignore duplicate request.

        :param attribute_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3110f10be133ed3c456a449357686baed7194447d5d7b64d6b8401b72a3689e5)
            check_type(argname="argument attribute_group", value=attribute_group, expected_type=type_hints["attribute_group"])
        return typing.cast(None, jsii.invoke(self, "associateAttributeGroup", [attribute_group]))

    @jsii.member(jsii_name="associateStack")
    def associate_stack(self, stack: _Stack_9f43e4a3) -> None:
        '''(experimental) Associate a stack with the application If the resource is already associated, it will ignore duplicate request.

        A stack can only be associated with one application.

        :param stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d096beb675797884cecb441d4828e6cf9a94e5536cf4c102e4e027badf817146)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "associateStack", [stack]))

    @jsii.member(jsii_name="generateUniqueHash")
    def _generate_unique_hash(self, resource_address: builtins.str) -> builtins.str:
        '''(experimental) Create a unique id.

        :param resource_address: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4489628b9b53aa3f2f20a58ebe947ca66d3294ed5a4b782f3e1d0506bd7653a)
            check_type(argname="argument resource_address", value=resource_address, expected_type=type_hints["resource_address"])
        return typing.cast(builtins.str, jsii.invoke(self, "generateUniqueHash", [resource_address]))

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''(experimental) The ID of the application.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))


@jsii.implements(IAttributeGroup)
class AttributeGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.AttributeGroup",
):
    '''(experimental) A Service Catalog AppRegistry Attribute Group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        attribute_group = appreg.AttributeGroup(self, "MyFirstAttributeGroup",
            attribute_group_name="MyFirstAttributeGroupName",
            description="description for my attribute group",  # the description is optional,
            attributes={
                "project": "foo",
                "team": ["member1", "member2", "member3"],
                "public": False,
                "stages": {
                    "alpha": "complete",
                    "beta": "incomplete",
                    "release": "not started"
                }
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        attribute_group_name: builtins.str,
        attributes: typing.Mapping[builtins.str, typing.Any],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param attribute_group_name: (experimental) Enforces a particular physical attribute group name.
        :param attributes: (experimental) A JSON of nested key-value pairs that represent the attributes in the group. Attributes maybe an empty JSON '{}', but must be explicitly stated.
        :param description: (experimental) Description for attribute group. Default: - No description provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99451f48e327240a947af0e681bf75ff3f1f6589ce7a5df0922c782ee2262f3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AttributeGroupProps(
            attribute_group_name=attribute_group_name,
            attributes=attributes,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAttributeGroupArn")
    @builtins.classmethod
    def from_attribute_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        attribute_group_arn: builtins.str,
    ) -> IAttributeGroup:
        '''(experimental) Imports an attribute group construct that represents an external attribute group.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param attribute_group_arn: the Amazon Resource Name of the existing AppRegistry attribute group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa1bd802ff3dc9301a5ed7faeae3e3d18311f832a2d1642aa289885daca7252)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument attribute_group_arn", value=attribute_group_arn, expected_type=type_hints["attribute_group_arn"])
        return typing.cast(IAttributeGroup, jsii.sinvoke(cls, "fromAttributeGroupArn", [scope, id, attribute_group_arn]))

    @builtins.property
    @jsii.member(jsii_name="attributeGroupArn")
    def attribute_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the attribute group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="attributeGroupId")
    def attribute_group_id(self) -> builtins.str:
        '''(experimental) The ID of the attribute group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroupId"))


__all__ = [
    "Application",
    "ApplicationProps",
    "AttributeGroup",
    "AttributeGroupProps",
    "CfnApplication",
    "CfnApplicationProps",
    "CfnAttributeGroup",
    "CfnAttributeGroupAssociation",
    "CfnAttributeGroupAssociationProps",
    "CfnAttributeGroupProps",
    "CfnResourceAssociation",
    "CfnResourceAssociationProps",
    "IApplication",
    "IAttributeGroup",
]

publication.publish()

def _typecheckingstub__fd697e58a8ebc0f11b44ab160600f3677cb68e30a649922754e06feb856f0e7c(
    *,
    application_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc62dec6de3a3b0965f74419f1076daae5a13f0d85496ef982000afcd7c64ae(
    *,
    attribute_group_name: builtins.str,
    attributes: typing.Mapping[builtins.str, typing.Any],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc9f7ffb1722eb580263626543856be0b7a1a697054cab335964930db4997a6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016e95f37dbfb5de1159d0563b94188f3b0ed42b93d07ee445028710c8f98d56(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fba157846fd7cef56224c2406925177d4125df29bcea573795ce4c283a794ff(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103b687a09dc11773e7f3a819bc28af2e7a9c809b6e08e87a67a3ec4124f90a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c99ab990ea60a95b26e7a44b53742ecda6273696f54c58a743be3421c96423(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef1ddc254084a352873d53fc5e9a79aebba677e8b2ba04bac5b0e6cccb2a2a4(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e264f2d622241fc342a5bc848edde1ddc028c7a4c4db5d69408bd5371c94fb51(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    attributes: typing.Any,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9264572f621c69a72b9fb8c3f81a99c455887fa2b2803614db81ccbdf84c4c62(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb930ee7cdc83ef615f27582579801cf4a51c031b5c6f62df506a6ed8c98ff6f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142f9c71cc5729ae50b64ece0d3c85dee1d83cc1800ed9e63b99d84b990bb191(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6253cc404dffceab80d11cfd538dae9827f627a4f832fa80d4ca6f0daf127c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d07be8bb1d691e26c4eadf398288256d0fcf1a53995c01d774cadd09a91087(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f3c548b9c154bac7210aaac75a02b5b75b8519117e6d64e663447404defba5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application: builtins.str,
    attribute_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5c060c2f8fba52aaa3430ca63284bb8a5ae9fede93c8549e01c1482975fcec(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34f2825b36b1cdca148cdf477dc0ba8d95e1163f8c91c37cc68cbe5d133aec8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ba1fbe50b49713ff9a8c266913edcf75266b83d1b3c5c3e75b60e8ab6a13f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92b1efc999a9dcd2cfe8da98ae567d0cc7163986feb42faad2bfee8187d7ee2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a86750a936812d3f8ff61f904c8c2ad5cd7d78da1dcbddfc252fdf202c46e8f(
    *,
    application: builtins.str,
    attribute_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cfeb4beb644be807870e113dd0ea922361b889124e390f208946c9fe93fa1ef(
    *,
    attributes: typing.Any,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b469ca6db7dfa9a9c82c19e911d0915f779db93d21681d0cd8b46ad10ecaaa(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application: builtins.str,
    resource: builtins.str,
    resource_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e93db56115e60e2a5e72381af5dcf3fda564a31457d97519f4a3a9d573b1700(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d692dc3f01e2790374184471df7a071c862b471de45214826cd444aacaa52604(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2a8a079d740c6f7067490c398b49bd89d184dd70926ec7299911a0abe50a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2579810868de368119e062c7e0dcaf191612ec2188b79b794b02df98af121499(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a534234de5559a857834dd71fe01cfc12f061c9ec37df4d1f0bdb0a9bf9bea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9ff12e974c8a35d13aa5852f953e7ccf7a06eeccbbd86bce61824ff71a6f98(
    *,
    application: builtins.str,
    resource: builtins.str,
    resource_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74afdce272c1bbde5d9a6553ab36ed880d470a533abbd05a4633b680c79e191e(
    attribute_group: IAttributeGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501e11687bc2f5dc6182b2cd7eee4d4608fbe040fa66eceb21f0b4fafe84c1db(
    stack: _Stack_9f43e4a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0add5ca44cf4deef52cf4b8555f9e3ac5fa6c1a8db6adf0d1860d10b17c4dabc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595fd678aae6aaa4a5277eb0f8d50c1a4ee27f6b1db7b03a8fc9aeb7bdb91f41(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    application_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3110f10be133ed3c456a449357686baed7194447d5d7b64d6b8401b72a3689e5(
    attribute_group: IAttributeGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d096beb675797884cecb441d4828e6cf9a94e5536cf4c102e4e027badf817146(
    stack: _Stack_9f43e4a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4489628b9b53aa3f2f20a58ebe947ca66d3294ed5a4b782f3e1d0506bd7653a(
    resource_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99451f48e327240a947af0e681bf75ff3f1f6589ce7a5df0922c782ee2262f3c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    attribute_group_name: builtins.str,
    attributes: typing.Mapping[builtins.str, typing.Any],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa1bd802ff3dc9301a5ed7faeae3e3d18311f832a2d1642aa289885daca7252(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    attribute_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
