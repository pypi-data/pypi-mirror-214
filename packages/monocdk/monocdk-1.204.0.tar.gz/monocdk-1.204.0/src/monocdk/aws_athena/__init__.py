'''
# Amazon Athena Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as athena
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Athena construct libraries](https://constructs.dev/search?q=athena)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Athena resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Athena.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Athena](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Athena.html).

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
class CfnDataCatalog(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_athena.CfnDataCatalog",
):
    '''A CloudFormation ``AWS::Athena::DataCatalog``.

    The AWS::Athena::DataCatalog resource specifies an Amazon Athena data catalog, which contains a name, description, type, parameters, and tags. For more information, see `DataCatalog <https://docs.aws.amazon.com/athena/latest/APIReference/API_DataCatalog.html>`_ in the *Amazon Athena API Reference* .

    :cloudformationResource: AWS::Athena::DataCatalog
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_athena as athena
        
        cfn_data_catalog = athena.CfnDataCatalog(self, "MyCfnDataCatalog",
            name="name",
            type="type",
        
            # the properties below are optional
            description="description",
            parameters={
                "parameters_key": "parameters"
            },
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
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Athena::DataCatalog``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the data catalog. The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.
        :param type: The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.
        :param description: A description of the data catalog.
        :param parameters: Specifies the Lambda function or functions to use for the data catalog. The mapping used depends on the catalog type. - The ``HIVE`` data catalog type uses the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version. ``metadata-function= *lambda_arn* , sdk-version= *version_number*`` - The ``LAMBDA`` data catalog type uses one of the following sets of required parameters, but not both. - When one Lambda function processes metadata and another Lambda function reads data, the following syntax is used. Both parameters are required. ``metadata-function= *lambda_arn* , record-function= *lambda_arn*`` - A composite Lambda function that processes both metadata and data uses the following syntax. ``function= *lambda_arn*`` - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the Glue catalog belongs. ``catalog-id= *catalog_id*`` - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify. - Queries that specify a GLUE data catalog other than the default ``AwsDataCatalog`` must be run on Athena engine version 2. - In Regions where Athena engine version 2 is not available, creating new GLUE data catalogs results in an ``INVALID_INPUT`` error.
        :param tags: The tags (key-value pairs) to associate with this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e778036132a28ba53c2761bc41c8664829b3975fbb9bd462237ff7988847c8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDataCatalogProps(
            name=name,
            type=type,
            description=description,
            parameters=parameters,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623c0ddaefa992801c97232bd24ec08bd540ddcba1d326b8a2dd765111fed0b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dc0756c9dda825a86e51d436121b8c2f7aee994ed87f506f9672c829a33b42d)
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
        '''The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the data catalog.

        The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59bf1b05dc3bde3b33046cf6cf9474d1f971ca0ec8f972d1ad9370f1d7fbfdaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddea67e3e5e92b65efefcc1f16dcd95746251f8e30289d3f61bb667343d25567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data catalog.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a2627302d674bb8859b7e7eb8c403fdb1d36efd5283fe9f8a9bc801c216496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''Specifies the Lambda function or functions to use for the data catalog.

        The mapping used depends on the catalog type.

        - The ``HIVE`` data catalog type uses the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version.

        ``metadata-function= *lambda_arn* , sdk-version= *version_number*``

        - The ``LAMBDA`` data catalog type uses one of the following sets of required parameters, but not both.
        - When one Lambda function processes metadata and another Lambda function reads data, the following syntax is used. Both parameters are required.

        ``metadata-function= *lambda_arn* , record-function= *lambda_arn*``

        - A composite Lambda function that processes both metadata and data uses the following syntax.

        ``function= *lambda_arn*``

        - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the Glue catalog belongs.

        ``catalog-id= *catalog_id*``

        - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify.
        - Queries that specify a GLUE data catalog other than the default ``AwsDataCatalog`` must be run on Athena engine version 2.
        - In Regions where Athena engine version 2 is not available, creating new GLUE data catalogs results in an ``INVALID_INPUT`` error.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-parameters
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9584a124e83265c9f256c529d0f8d5667c75b3ed304fd0ea183e14a03a074ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)


@jsii.data_type(
    jsii_type="monocdk.aws_athena.CfnDataCatalogProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "description": "description",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnDataCatalogProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataCatalog``.

        :param name: The name of the data catalog. The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.
        :param type: The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.
        :param description: A description of the data catalog.
        :param parameters: Specifies the Lambda function or functions to use for the data catalog. The mapping used depends on the catalog type. - The ``HIVE`` data catalog type uses the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version. ``metadata-function= *lambda_arn* , sdk-version= *version_number*`` - The ``LAMBDA`` data catalog type uses one of the following sets of required parameters, but not both. - When one Lambda function processes metadata and another Lambda function reads data, the following syntax is used. Both parameters are required. ``metadata-function= *lambda_arn* , record-function= *lambda_arn*`` - A composite Lambda function that processes both metadata and data uses the following syntax. ``function= *lambda_arn*`` - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the Glue catalog belongs. ``catalog-id= *catalog_id*`` - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify. - Queries that specify a GLUE data catalog other than the default ``AwsDataCatalog`` must be run on Athena engine version 2. - In Regions where Athena engine version 2 is not available, creating new GLUE data catalogs results in an ``INVALID_INPUT`` error.
        :param tags: The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_athena as athena
            
            cfn_data_catalog_props = athena.CfnDataCatalogProps(
                name="name",
                type="type",
            
                # the properties below are optional
                description="description",
                parameters={
                    "parameters_key": "parameters"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93644181c193cacde74fb34a9d64691fc796b769ca68a955b420c1e3c9bf03b3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the data catalog.

        The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data catalog.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''Specifies the Lambda function or functions to use for the data catalog.

        The mapping used depends on the catalog type.

        - The ``HIVE`` data catalog type uses the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version.

        ``metadata-function= *lambda_arn* , sdk-version= *version_number*``

        - The ``LAMBDA`` data catalog type uses one of the following sets of required parameters, but not both.
        - When one Lambda function processes metadata and another Lambda function reads data, the following syntax is used. Both parameters are required.

        ``metadata-function= *lambda_arn* , record-function= *lambda_arn*``

        - A composite Lambda function that processes both metadata and data uses the following syntax.

        ``function= *lambda_arn*``

        - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the Glue catalog belongs.

        ``catalog-id= *catalog_id*``

        - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify.
        - Queries that specify a GLUE data catalog other than the default ``AwsDataCatalog`` must be run on Athena engine version 2.
        - In Regions where Athena engine version 2 is not available, creating new GLUE data catalogs results in an ``INVALID_INPUT`` error.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataCatalogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnNamedQuery(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_athena.CfnNamedQuery",
):
    '''A CloudFormation ``AWS::Athena::NamedQuery``.

    The ``AWS::Athena::NamedQuery`` resource specifies an Amazon Athena saved query, where ``QueryString`` contains the SQL query statements that make up the query.

    :cloudformationResource: AWS::Athena::NamedQuery
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_athena as athena
        
        cfn_named_query = athena.CfnNamedQuery(self, "MyCfnNamedQuery",
            database="database",
            query_string="queryString",
        
            # the properties below are optional
            description="description",
            name="name",
            work_group="workGroup"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        database: builtins.str,
        query_string: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        work_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Athena::NamedQuery``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database: The database to which the query belongs.
        :param query_string: The SQL statements that make up the query.
        :param description: The query description.
        :param name: The query name.
        :param work_group: The name of the workgroup that contains the named query.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5868b76e84664daa2f4fa0755c2c1d8fee8d10193f6329ef606dd67627dbab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNamedQueryProps(
            database=database,
            query_string=query_string,
            description=description,
            name=name,
            work_group=work_group,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762369ff56ee5797d14a909f8f486247a83d36abeef983c30baac084e48c329a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e59b8b66869691fe80e9b6c2d35bf2ac94e5209cff845e1a63017675d253a74)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrNamedQueryId")
    def attr_named_query_id(self) -> builtins.str:
        '''The unique ID of the query.

        :cloudformationAttribute: NamedQueryId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNamedQueryId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        '''The database to which the query belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        '''
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae4090d261b65e8c773c16cff11db0ab88dece33852c6acb34ff7f5e226e89f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        '''The SQL statements that make up the query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9162781a631ecbf5e8e352347a800d3f4e40b954993cd38c070009f6df37784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The query description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc8a648e2a52820eaf168ab38bf09066d7a9482187de4ab63950268efd9b264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The query name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6278c66ab57522a47ef60a226b5a0719eee722244bfa121f8b91a4799de54e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="workGroup")
    def work_group(self) -> typing.Optional[builtins.str]:
        '''The name of the workgroup that contains the named query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-workgroup
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workGroup"))

    @work_group.setter
    def work_group(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ff53ebd66e8f949c207d93d29b7eded7e0b28dd0ad66c361b45723f91416de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workGroup", value)


@jsii.data_type(
    jsii_type="monocdk.aws_athena.CfnNamedQueryProps",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "query_string": "queryString",
        "description": "description",
        "name": "name",
        "work_group": "workGroup",
    },
)
class CfnNamedQueryProps:
    def __init__(
        self,
        *,
        database: builtins.str,
        query_string: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        work_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnNamedQuery``.

        :param database: The database to which the query belongs.
        :param query_string: The SQL statements that make up the query.
        :param description: The query description.
        :param name: The query name.
        :param work_group: The name of the workgroup that contains the named query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_athena as athena
            
            cfn_named_query_props = athena.CfnNamedQueryProps(
                database="database",
                query_string="queryString",
            
                # the properties below are optional
                description="description",
                name="name",
                work_group="workGroup"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec988326e0e2b0fff4116e1018ea8159751f91e0c2de7b80c01aee67712ca9d)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "query_string": query_string,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if work_group is not None:
            self._values["work_group"] = work_group

    @builtins.property
    def database(self) -> builtins.str:
        '''The database to which the query belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_string(self) -> builtins.str:
        '''The SQL statements that make up the query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        '''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The query description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The query name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def work_group(self) -> typing.Optional[builtins.str]:
        '''The name of the workgroup that contains the named query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-workgroup
        '''
        result = self._values.get("work_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNamedQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPreparedStatement(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_athena.CfnPreparedStatement",
):
    '''A CloudFormation ``AWS::Athena::PreparedStatement``.

    Specifies a prepared statement for use with SQL queries in Athena.

    :cloudformationResource: AWS::Athena::PreparedStatement
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_athena as athena
        
        cfn_prepared_statement = athena.CfnPreparedStatement(self, "MyCfnPreparedStatement",
            query_statement="queryStatement",
            statement_name="statementName",
            work_group="workGroup",
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        query_statement: builtins.str,
        statement_name: builtins.str,
        work_group: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Athena::PreparedStatement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param query_statement: The query string for the prepared statement.
        :param statement_name: The name of the prepared statement.
        :param work_group: The workgroup to which the prepared statement belongs.
        :param description: The description of the prepared statement.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3c2ba02eb6d39b4f5bc166d5336f28fae12779abb14e01cbf992c5e7e1f713)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPreparedStatementProps(
            query_statement=query_statement,
            statement_name=statement_name,
            work_group=work_group,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1843656e5295b31a6cff6fb82fa107336abdaabe12066b45b91b0630881911)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7610fe8f5cee5605081b5385e7a4034cd1c7c740e1d58e54d41ab8d74a6571f5)
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
    @jsii.member(jsii_name="queryStatement")
    def query_statement(self) -> builtins.str:
        '''The query string for the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-querystatement
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryStatement"))

    @query_statement.setter
    def query_statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9cb45d56841b4d94ac73342791c32599c5398265a4d226b16f08e33d21b8ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStatement", value)

    @builtins.property
    @jsii.member(jsii_name="statementName")
    def statement_name(self) -> builtins.str:
        '''The name of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-statementname
        '''
        return typing.cast(builtins.str, jsii.get(self, "statementName"))

    @statement_name.setter
    def statement_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff01499702a5d6cdb3cbd4ca2f205d27e7c36b70935160f8fc567c23e65c396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementName", value)

    @builtins.property
    @jsii.member(jsii_name="workGroup")
    def work_group(self) -> builtins.str:
        '''The workgroup to which the prepared statement belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-workgroup
        '''
        return typing.cast(builtins.str, jsii.get(self, "workGroup"))

    @work_group.setter
    def work_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67320217f6bf9ae689da110dcef43980db7c8e21ae3fec66f75b5a77ed347d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workGroup", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6b19b6aeb432b5d2b85002b7f2757504935f8075d3b9924553bb3f58602b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_athena.CfnPreparedStatementProps",
    jsii_struct_bases=[],
    name_mapping={
        "query_statement": "queryStatement",
        "statement_name": "statementName",
        "work_group": "workGroup",
        "description": "description",
    },
)
class CfnPreparedStatementProps:
    def __init__(
        self,
        *,
        query_statement: builtins.str,
        statement_name: builtins.str,
        work_group: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPreparedStatement``.

        :param query_statement: The query string for the prepared statement.
        :param statement_name: The name of the prepared statement.
        :param work_group: The workgroup to which the prepared statement belongs.
        :param description: The description of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_athena as athena
            
            cfn_prepared_statement_props = athena.CfnPreparedStatementProps(
                query_statement="queryStatement",
                statement_name="statementName",
                work_group="workGroup",
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2ea406d49f4b8450c827512a4a81c1a53e378e1ff4ec7ac57f282e33c09def)
            check_type(argname="argument query_statement", value=query_statement, expected_type=type_hints["query_statement"])
            check_type(argname="argument statement_name", value=statement_name, expected_type=type_hints["statement_name"])
            check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query_statement": query_statement,
            "statement_name": statement_name,
            "work_group": work_group,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def query_statement(self) -> builtins.str:
        '''The query string for the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-querystatement
        '''
        result = self._values.get("query_statement")
        assert result is not None, "Required property 'query_statement' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statement_name(self) -> builtins.str:
        '''The name of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-statementname
        '''
        result = self._values.get("statement_name")
        assert result is not None, "Required property 'statement_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def work_group(self) -> builtins.str:
        '''The workgroup to which the prepared statement belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-workgroup
        '''
        result = self._values.get("work_group")
        assert result is not None, "Required property 'work_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPreparedStatementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnWorkGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_athena.CfnWorkGroup",
):
    '''A CloudFormation ``AWS::Athena::WorkGroup``.

    The AWS::Athena::WorkGroup resource specifies an Amazon Athena workgroup, which contains a name, description, creation time, state, and other configuration, listed under ``WorkGroupConfiguration`` . Each workgroup enables you to isolate queries for you or your group from other queries in the same account. For more information, see `CreateWorkGroup <https://docs.aws.amazon.com/athena/latest/APIReference/API_CreateWorkGroup.html>`_ in the *Amazon Athena API Reference* .

    :cloudformationResource: AWS::Athena::WorkGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_athena as athena
        
        cfn_work_group = athena.CfnWorkGroup(self, "MyCfnWorkGroup",
            name="name",
        
            # the properties below are optional
            description="description",
            recursive_delete_option=False,
            state="state",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                additional_configuration="additionalConfiguration",
                bytes_scanned_cutoff_per_query=123,
                customer_content_encryption_configuration=athena.CfnWorkGroup.CustomerContentEncryptionConfigurationProperty(
                    kms_key="kmsKey"
                ),
                enforce_work_group_configuration=False,
                engine_version=athena.CfnWorkGroup.EngineVersionProperty(
                    effective_engine_version="effectiveEngineVersion",
                    selected_engine_version="selectedEngineVersion"
                ),
                execution_role="executionRole",
                publish_cloud_watch_metrics_enabled=False,
                requester_pays_enabled=False,
                result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                    acl_configuration=athena.CfnWorkGroup.AclConfigurationProperty(
                        s3_acl_option="s3AclOption"
                    ),
                    encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                        encryption_option="encryptionOption",
        
                        # the properties below are optional
                        kms_key="kmsKey"
                    ),
                    expected_bucket_owner="expectedBucketOwner",
                    output_location="outputLocation"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        work_group_configuration: typing.Optional[typing.Union[typing.Union["CfnWorkGroup.WorkGroupConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Athena::WorkGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The workgroup name.
        :param description: The workgroup description.
        :param recursive_delete_option: The option to delete a workgroup and its contents even if the workgroup contains any named queries. The default is false.
        :param state: The state of the workgroup: ENABLED or DISABLED.
        :param tags: The tags (key-value pairs) to associate with this resource.
        :param work_group_configuration: The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified. The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9fb82712577ce374298ec4efb512f5f2863cfccfd4db99d5b65aac752e9189)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkGroupProps(
            name=name,
            description=description,
            recursive_delete_option=recursive_delete_option,
            state=state,
            tags=tags,
            work_group_configuration=work_group_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f9d58b59ea00c7a64e346b6e003a8bf66387a1c233ec0421ccbf1db254a1b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c09ddfd7431fb1762310c00a3bb551614ee2cdb386010fb6494c93fce21102ad)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time the workgroup was created, as a UNIX timestamp in seconds.

        For example: ``1582761016`` .

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrWorkGroupConfigurationEngineVersionEffectiveEngineVersion")
    def attr_work_group_configuration_engine_version_effective_engine_version(
        self,
    ) -> builtins.str:
        '''
        :cloudformationAttribute: WorkGroupConfiguration.EngineVersion.EffectiveEngineVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrWorkGroupConfigurationEngineVersionEffectiveEngineVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The workgroup name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61033d36d0a40f0949e4eaff014845a7e73915c950f37a75697546334c1ca94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The workgroup description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33288ce48ecb174722c12aa7cdf34d2581999a1aa49647e4986937b50634519f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="recursiveDeleteOption")
    def recursive_delete_option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''The option to delete a workgroup and its contents even if the workgroup contains any named queries.

        The default is false.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-recursivedeleteoption
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "recursiveDeleteOption"))

    @recursive_delete_option.setter
    def recursive_delete_option(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d2e46d61f30d0fb00680579358b3984f54fbe934dfe21d843aa8c57fd191825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recursiveDeleteOption", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the workgroup: ENABLED or DISABLED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecefe30ef12ef65b8d4f89620033dee21748b8d2a547a362de6ef40a114e11d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="workGroupConfiguration")
    def work_group_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnWorkGroup.WorkGroupConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified.

        The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnWorkGroup.WorkGroupConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "workGroupConfiguration"))

    @work_group_configuration.setter
    def work_group_configuration(
        self,
        value: typing.Optional[typing.Union["CfnWorkGroup.WorkGroupConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e620a2c249804dab7f5f0a5bcb273bc7f116a21242c4e140ed06c3920f3e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workGroupConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_athena.CfnWorkGroup.AclConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_acl_option": "s3AclOption"},
    )
    class AclConfigurationProperty:
        def __init__(self, *, s3_acl_option: builtins.str) -> None:
            '''Indicates that an Amazon S3 canned ACL should be set to control ownership of stored query results.

            When Athena stores query results in Amazon S3, the canned ACL is set with the ``x-amz-acl`` request header. For more information about S3 Object Ownership, see `Object Ownership settings <https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html#object-ownership-overview>`_ in the *Amazon S3 User Guide* .

            :param s3_acl_option: The Amazon S3 canned ACL that Athena should specify when storing query results. Currently the only supported canned ACL is ``BUCKET_OWNER_FULL_CONTROL`` . If a query runs in a workgroup and the workgroup overrides client-side settings, then the Amazon S3 canned ACL specified in the workgroup's settings is used for all queries that run in the workgroup. For more information about Amazon S3 canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-aclconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_athena as athena
                
                acl_configuration_property = athena.CfnWorkGroup.AclConfigurationProperty(
                    s3_acl_option="s3AclOption"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73d89b88502202fadb4b4f5c62c9e133051037e60aee7fbcb30b0316864d200a)
                check_type(argname="argument s3_acl_option", value=s3_acl_option, expected_type=type_hints["s3_acl_option"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_acl_option": s3_acl_option,
            }

        @builtins.property
        def s3_acl_option(self) -> builtins.str:
            '''The Amazon S3 canned ACL that Athena should specify when storing query results.

            Currently the only supported canned ACL is ``BUCKET_OWNER_FULL_CONTROL`` . If a query runs in a workgroup and the workgroup overrides client-side settings, then the Amazon S3 canned ACL specified in the workgroup's settings is used for all queries that run in the workgroup. For more information about Amazon S3 canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-aclconfiguration.html#cfn-athena-workgroup-aclconfiguration-s3acloption
            '''
            result = self._values.get("s3_acl_option")
            assert result is not None, "Required property 's3_acl_option' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AclConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_athena.CfnWorkGroup.CustomerContentEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key": "kmsKey"},
    )
    class CustomerContentEncryptionConfigurationProperty:
        def __init__(self, *, kms_key: builtins.str) -> None:
            '''Specifies the KMS key that is used to encrypt the user's data stores in Athena.

            This setting does not apply to Athena SQL workgroups.

            :param kms_key: The KMS key that is used to encrypt the user's data stores in Athena.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-customercontentencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_athena as athena
                
                customer_content_encryption_configuration_property = athena.CfnWorkGroup.CustomerContentEncryptionConfigurationProperty(
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17aeff2a519d826d532643c3cac2a7a67c318a1a7362ea9c3e6a30d0502c732f)
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "kms_key": kms_key,
            }

        @builtins.property
        def kms_key(self) -> builtins.str:
            '''The KMS key that is used to encrypt the user's data stores in Athena.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-customercontentencryptionconfiguration.html#cfn-athena-workgroup-customercontentencryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            assert result is not None, "Required property 'kms_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerContentEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_athena.CfnWorkGroup.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_option": "encryptionOption", "kms_key": "kmsKey"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_option: builtins.str,
            kms_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information.

            :param encryption_option: Indicates whether Amazon S3 server-side encryption with Amazon S3-managed keys ( ``SSE_S3`` ), server-side encryption with KMS-managed keys ( ``SSE_KMS`` ), or client-side encryption with KMS-managed keys ( ``CSE_KMS`` ) is used. If a query runs in a workgroup and the workgroup overrides client-side settings, then the workgroup's setting for encryption is used. It specifies whether query results must be encrypted, for all queries that run in this workgroup.
            :param kms_key: For ``SSE_KMS`` and ``CSE_KMS`` , this is the KMS key ARN or ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_athena as athena
                
                encryption_configuration_property = athena.CfnWorkGroup.EncryptionConfigurationProperty(
                    encryption_option="encryptionOption",
                
                    # the properties below are optional
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__caa73a07ec83d53098934adf62448447af84e0c2c6cc90838faf27e12978c0e9)
                check_type(argname="argument encryption_option", value=encryption_option, expected_type=type_hints["encryption_option"])
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encryption_option": encryption_option,
            }
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def encryption_option(self) -> builtins.str:
            '''Indicates whether Amazon S3 server-side encryption with Amazon S3-managed keys ( ``SSE_S3`` ), server-side encryption with KMS-managed keys ( ``SSE_KMS`` ), or client-side encryption with KMS-managed keys ( ``CSE_KMS`` ) is used.

            If a query runs in a workgroup and the workgroup overrides client-side settings, then the workgroup's setting for encryption is used. It specifies whether query results must be encrypted, for all queries that run in this workgroup.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html#cfn-athena-workgroup-encryptionconfiguration-encryptionoption
            '''
            result = self._values.get("encryption_option")
            assert result is not None, "Required property 'encryption_option' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''For ``SSE_KMS`` and ``CSE_KMS`` , this is the KMS key ARN or ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html#cfn-athena-workgroup-encryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
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
        jsii_type="monocdk.aws_athena.CfnWorkGroup.EngineVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "effective_engine_version": "effectiveEngineVersion",
            "selected_engine_version": "selectedEngineVersion",
        },
    )
    class EngineVersionProperty:
        def __init__(
            self,
            *,
            effective_engine_version: typing.Optional[builtins.str] = None,
            selected_engine_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Athena engine version for running queries, or the PySpark engine version for running sessions.

            :param effective_engine_version: Read only. The engine version on which the query runs. If the user requests a valid engine version other than Auto, the effective engine version is the same as the engine version that the user requested. If the user requests Auto, the effective engine version is chosen by Athena. When a request to update the engine version is made by a ``CreateWorkGroup`` or ``UpdateWorkGroup`` operation, the ``EffectiveEngineVersion`` field is ignored.
            :param selected_engine_version: The engine version requested by the user. Possible values are determined by the output of ``ListEngineVersions`` , including AUTO. The default is AUTO.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_athena as athena
                
                engine_version_property = athena.CfnWorkGroup.EngineVersionProperty(
                    effective_engine_version="effectiveEngineVersion",
                    selected_engine_version="selectedEngineVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__08752fe8bd643a2bc0e8be04800c5035c187009740dab904e8c4a12a4fb9f100)
                check_type(argname="argument effective_engine_version", value=effective_engine_version, expected_type=type_hints["effective_engine_version"])
                check_type(argname="argument selected_engine_version", value=selected_engine_version, expected_type=type_hints["selected_engine_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if effective_engine_version is not None:
                self._values["effective_engine_version"] = effective_engine_version
            if selected_engine_version is not None:
                self._values["selected_engine_version"] = selected_engine_version

        @builtins.property
        def effective_engine_version(self) -> typing.Optional[builtins.str]:
            '''Read only.

            The engine version on which the query runs. If the user requests a valid engine version other than Auto, the effective engine version is the same as the engine version that the user requested. If the user requests Auto, the effective engine version is chosen by Athena. When a request to update the engine version is made by a ``CreateWorkGroup`` or ``UpdateWorkGroup`` operation, the ``EffectiveEngineVersion`` field is ignored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html#cfn-athena-workgroup-engineversion-effectiveengineversion
            '''
            result = self._values.get("effective_engine_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def selected_engine_version(self) -> typing.Optional[builtins.str]:
            '''The engine version requested by the user.

            Possible values are determined by the output of ``ListEngineVersions`` , including AUTO. The default is AUTO.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html#cfn-athena-workgroup-engineversion-selectedengineversion
            '''
            result = self._values.get("selected_engine_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EngineVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_athena.CfnWorkGroup.ResultConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acl_configuration": "aclConfiguration",
            "encryption_configuration": "encryptionConfiguration",
            "expected_bucket_owner": "expectedBucketOwner",
            "output_location": "outputLocation",
        },
    )
    class ResultConfigurationProperty:
        def __init__(
            self,
            *,
            acl_configuration: typing.Optional[typing.Union[typing.Union["CfnWorkGroup.AclConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            encryption_configuration: typing.Optional[typing.Union[typing.Union["CfnWorkGroup.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            expected_bucket_owner: typing.Optional[builtins.str] = None,
            output_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location in Amazon S3 where query and calculation results are stored and the encryption option, if any, used for query and calculation results.

            These are known as "client-side settings". If workgroup settings override client-side settings, then the query uses the workgroup settings.

            :param acl_configuration: Indicates that an Amazon S3 canned ACL should be set to control ownership of stored query results. Currently the only supported canned ACL is ``BUCKET_OWNER_FULL_CONTROL`` . This is a client-side setting. If workgroup settings override client-side settings, then the query uses the ACL configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` .
            :param encryption_configuration: If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information. This is a client-side setting. If workgroup settings override client-side settings, then the query uses the encryption configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` and `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param expected_bucket_owner: The account ID that you expect to be the owner of the Amazon S3 bucket specified by ``ResultConfiguration:OutputLocation`` . If set, Athena uses the value for ``ExpectedBucketOwner`` when it makes Amazon S3 calls to your specified output location. If the ``ExpectedBucketOwner`` account ID does not match the actual owner of the Amazon S3 bucket, the call fails with a permissions error. This is a client-side setting. If workgroup settings override client-side settings, then the query uses the ``ExpectedBucketOwner`` setting that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` .
            :param output_location: The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/`` . To run a query, you must specify the query results location using either a client-side setting for individual queries or a location specified by the workgroup. If workgroup settings override client-side settings, then the query uses the location specified for the workgroup. If no query location is set, Athena issues an error. For more information, see `Working with Query Results, Output Files, and Query History <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ and ``EnforceWorkGroupConfiguration`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_athena as athena
                
                result_configuration_property = athena.CfnWorkGroup.ResultConfigurationProperty(
                    acl_configuration=athena.CfnWorkGroup.AclConfigurationProperty(
                        s3_acl_option="s3AclOption"
                    ),
                    encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                        encryption_option="encryptionOption",
                
                        # the properties below are optional
                        kms_key="kmsKey"
                    ),
                    expected_bucket_owner="expectedBucketOwner",
                    output_location="outputLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b8806fe1222a772491a722490c4de6c85ce69dbe96aac090522718664605a0a)
                check_type(argname="argument acl_configuration", value=acl_configuration, expected_type=type_hints["acl_configuration"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
                check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acl_configuration is not None:
                self._values["acl_configuration"] = acl_configuration
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if expected_bucket_owner is not None:
                self._values["expected_bucket_owner"] = expected_bucket_owner
            if output_location is not None:
                self._values["output_location"] = output_location

        @builtins.property
        def acl_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkGroup.AclConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Indicates that an Amazon S3 canned ACL should be set to control ownership of stored query results.

            Currently the only supported canned ACL is ``BUCKET_OWNER_FULL_CONTROL`` . This is a client-side setting. If workgroup settings override client-side settings, then the query uses the ACL configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-aclconfiguration
            '''
            result = self._values.get("acl_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnWorkGroup.AclConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkGroup.EncryptionConfigurationProperty", _IResolvable_a771d0ef]]:
            '''If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information.

            This is a client-side setting. If workgroup settings override client-side settings, then the query uses the encryption configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` and `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnWorkGroup.EncryptionConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The account ID that you expect to be the owner of the Amazon S3 bucket specified by ``ResultConfiguration:OutputLocation`` .

            If set, Athena uses the value for ``ExpectedBucketOwner`` when it makes Amazon S3 calls to your specified output location. If the ``ExpectedBucketOwner`` account ID does not match the actual owner of the Amazon S3 bucket, the call fails with a permissions error.

            This is a client-side setting. If workgroup settings override client-side settings, then the query uses the ``ExpectedBucketOwner`` setting that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-expectedbucketowner
            '''
            result = self._values.get("expected_bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_location(self) -> typing.Optional[builtins.str]:
            '''The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/`` .

            To run a query, you must specify the query results location using either a client-side setting for individual queries or a location specified by the workgroup. If workgroup settings override client-side settings, then the query uses the location specified for the workgroup. If no query location is set, Athena issues an error. For more information, see `Working with Query Results, Output Files, and Query History <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ and ``EnforceWorkGroupConfiguration`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-outputlocation
            '''
            result = self._values.get("output_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResultConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_athena.CfnWorkGroup.WorkGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_configuration": "additionalConfiguration",
            "bytes_scanned_cutoff_per_query": "bytesScannedCutoffPerQuery",
            "customer_content_encryption_configuration": "customerContentEncryptionConfiguration",
            "enforce_work_group_configuration": "enforceWorkGroupConfiguration",
            "engine_version": "engineVersion",
            "execution_role": "executionRole",
            "publish_cloud_watch_metrics_enabled": "publishCloudWatchMetricsEnabled",
            "requester_pays_enabled": "requesterPaysEnabled",
            "result_configuration": "resultConfiguration",
        },
    )
    class WorkGroupConfigurationProperty:
        def __init__(
            self,
            *,
            additional_configuration: typing.Optional[builtins.str] = None,
            bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
            customer_content_encryption_configuration: typing.Optional[typing.Union[typing.Union["CfnWorkGroup.CustomerContentEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            enforce_work_group_configuration: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            engine_version: typing.Optional[typing.Union[typing.Union["CfnWorkGroup.EngineVersionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            execution_role: typing.Optional[builtins.str] = None,
            publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            result_configuration: typing.Optional[typing.Union[typing.Union["CfnWorkGroup.ResultConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified.

            The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

            :param additional_configuration: Specifies a user defined JSON string that is passed to the session engine.
            :param bytes_scanned_cutoff_per_query: The upper limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan. No default is defined. .. epigraph:: This property currently supports integer types. Support for long values is planned.
            :param customer_content_encryption_configuration: Specifies the KMS key that is used to encrypt the user's data stores in Athena. This setting does not apply to Athena SQL workgroups.
            :param enforce_work_group_configuration: If set to "true", the settings for the workgroup override client-side settings. If set to "false", client-side settings are used. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param engine_version: The engine version that all queries running on the workgroup use.
            :param execution_role: Role used to access user resources in an Athena for Apache Spark session. This property applies only to Spark-enabled workgroups in Athena.
            :param publish_cloud_watch_metrics_enabled: Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.
            :param requester_pays_enabled: If set to ``true`` , allows members assigned to a workgroup to reference Amazon S3 Requester Pays buckets in queries. If set to ``false`` , workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false`` . For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide* .
            :param result_configuration: Specifies the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results. For more information, see `Working with Query Results, Output Files, and Query History <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_athena as athena
                
                work_group_configuration_property = athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                    additional_configuration="additionalConfiguration",
                    bytes_scanned_cutoff_per_query=123,
                    customer_content_encryption_configuration=athena.CfnWorkGroup.CustomerContentEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    ),
                    enforce_work_group_configuration=False,
                    engine_version=athena.CfnWorkGroup.EngineVersionProperty(
                        effective_engine_version="effectiveEngineVersion",
                        selected_engine_version="selectedEngineVersion"
                    ),
                    execution_role="executionRole",
                    publish_cloud_watch_metrics_enabled=False,
                    requester_pays_enabled=False,
                    result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                        acl_configuration=athena.CfnWorkGroup.AclConfigurationProperty(
                            s3_acl_option="s3AclOption"
                        ),
                        encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                            encryption_option="encryptionOption",
                
                            # the properties below are optional
                            kms_key="kmsKey"
                        ),
                        expected_bucket_owner="expectedBucketOwner",
                        output_location="outputLocation"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5ec8c8085eddf90c3f02c7e144adbdeb0af959225ac8bf6af81e5653b2f3a44)
                check_type(argname="argument additional_configuration", value=additional_configuration, expected_type=type_hints["additional_configuration"])
                check_type(argname="argument bytes_scanned_cutoff_per_query", value=bytes_scanned_cutoff_per_query, expected_type=type_hints["bytes_scanned_cutoff_per_query"])
                check_type(argname="argument customer_content_encryption_configuration", value=customer_content_encryption_configuration, expected_type=type_hints["customer_content_encryption_configuration"])
                check_type(argname="argument enforce_work_group_configuration", value=enforce_work_group_configuration, expected_type=type_hints["enforce_work_group_configuration"])
                check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
                check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
                check_type(argname="argument publish_cloud_watch_metrics_enabled", value=publish_cloud_watch_metrics_enabled, expected_type=type_hints["publish_cloud_watch_metrics_enabled"])
                check_type(argname="argument requester_pays_enabled", value=requester_pays_enabled, expected_type=type_hints["requester_pays_enabled"])
                check_type(argname="argument result_configuration", value=result_configuration, expected_type=type_hints["result_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_configuration is not None:
                self._values["additional_configuration"] = additional_configuration
            if bytes_scanned_cutoff_per_query is not None:
                self._values["bytes_scanned_cutoff_per_query"] = bytes_scanned_cutoff_per_query
            if customer_content_encryption_configuration is not None:
                self._values["customer_content_encryption_configuration"] = customer_content_encryption_configuration
            if enforce_work_group_configuration is not None:
                self._values["enforce_work_group_configuration"] = enforce_work_group_configuration
            if engine_version is not None:
                self._values["engine_version"] = engine_version
            if execution_role is not None:
                self._values["execution_role"] = execution_role
            if publish_cloud_watch_metrics_enabled is not None:
                self._values["publish_cloud_watch_metrics_enabled"] = publish_cloud_watch_metrics_enabled
            if requester_pays_enabled is not None:
                self._values["requester_pays_enabled"] = requester_pays_enabled
            if result_configuration is not None:
                self._values["result_configuration"] = result_configuration

        @builtins.property
        def additional_configuration(self) -> typing.Optional[builtins.str]:
            '''Specifies a user defined JSON string that is passed to the session engine.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-additionalconfiguration
            '''
            result = self._values.get("additional_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bytes_scanned_cutoff_per_query(self) -> typing.Optional[jsii.Number]:
            '''The upper limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan.

            No default is defined.
            .. epigraph::

               This property currently supports integer types. Support for long values is planned.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-bytesscannedcutoffperquery
            '''
            result = self._values.get("bytes_scanned_cutoff_per_query")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def customer_content_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkGroup.CustomerContentEncryptionConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Specifies the KMS key that is used to encrypt the user's data stores in Athena.

            This setting does not apply to Athena SQL workgroups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-customercontentencryptionconfiguration
            '''
            result = self._values.get("customer_content_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnWorkGroup.CustomerContentEncryptionConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def enforce_work_group_configuration(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''If set to "true", the settings for the workgroup override client-side settings.

            If set to "false", client-side settings are used. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-enforceworkgroupconfiguration
            '''
            result = self._values.get("enforce_work_group_configuration")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def engine_version(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkGroup.EngineVersionProperty", _IResolvable_a771d0ef]]:
            '''The engine version that all queries running on the workgroup use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-engineversion
            '''
            result = self._values.get("engine_version")
            return typing.cast(typing.Optional[typing.Union["CfnWorkGroup.EngineVersionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def execution_role(self) -> typing.Optional[builtins.str]:
            '''Role used to access user resources in an Athena for Apache Spark session.

            This property applies only to Spark-enabled workgroups in Athena.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-executionrole
            '''
            result = self._values.get("execution_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def publish_cloud_watch_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-publishcloudwatchmetricsenabled
            '''
            result = self._values.get("publish_cloud_watch_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def requester_pays_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''If set to ``true`` , allows members assigned to a workgroup to reference Amazon S3 Requester Pays buckets in queries.

            If set to ``false`` , workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false`` . For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-requesterpaysenabled
            '''
            result = self._values.get("requester_pays_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def result_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkGroup.ResultConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Specifies the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results.

            For more information, see `Working with Query Results, Output Files, and Query History <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-resultconfiguration
            '''
            result = self._values.get("result_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnWorkGroup.ResultConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_athena.CfnWorkGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "recursive_delete_option": "recursiveDeleteOption",
        "state": "state",
        "tags": "tags",
        "work_group_configuration": "workGroupConfiguration",
    },
)
class CfnWorkGroupProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        work_group_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkGroup``.

        :param name: The workgroup name.
        :param description: The workgroup description.
        :param recursive_delete_option: The option to delete a workgroup and its contents even if the workgroup contains any named queries. The default is false.
        :param state: The state of the workgroup: ENABLED or DISABLED.
        :param tags: The tags (key-value pairs) to associate with this resource.
        :param work_group_configuration: The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified. The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_athena as athena
            
            cfn_work_group_props = athena.CfnWorkGroupProps(
                name="name",
            
                # the properties below are optional
                description="description",
                recursive_delete_option=False,
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                    additional_configuration="additionalConfiguration",
                    bytes_scanned_cutoff_per_query=123,
                    customer_content_encryption_configuration=athena.CfnWorkGroup.CustomerContentEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    ),
                    enforce_work_group_configuration=False,
                    engine_version=athena.CfnWorkGroup.EngineVersionProperty(
                        effective_engine_version="effectiveEngineVersion",
                        selected_engine_version="selectedEngineVersion"
                    ),
                    execution_role="executionRole",
                    publish_cloud_watch_metrics_enabled=False,
                    requester_pays_enabled=False,
                    result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                        acl_configuration=athena.CfnWorkGroup.AclConfigurationProperty(
                            s3_acl_option="s3AclOption"
                        ),
                        encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                            encryption_option="encryptionOption",
            
                            # the properties below are optional
                            kms_key="kmsKey"
                        ),
                        expected_bucket_owner="expectedBucketOwner",
                        output_location="outputLocation"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc86e44e8d5721f2ee5ab7b90522e4629fc80461ea08e816109bd72c8e7a14ad)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument recursive_delete_option", value=recursive_delete_option, expected_type=type_hints["recursive_delete_option"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument work_group_configuration", value=work_group_configuration, expected_type=type_hints["work_group_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if recursive_delete_option is not None:
            self._values["recursive_delete_option"] = recursive_delete_option
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if work_group_configuration is not None:
            self._values["work_group_configuration"] = work_group_configuration

    @builtins.property
    def name(self) -> builtins.str:
        '''The workgroup name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The workgroup description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recursive_delete_option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''The option to delete a workgroup and its contents even if the workgroup contains any named queries.

        The default is false.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-recursivedeleteoption
        '''
        result = self._values.get("recursive_delete_option")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the workgroup: ENABLED or DISABLED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def work_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified.

        The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfiguration
        '''
        result = self._values.get("work_group_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDataCatalog",
    "CfnDataCatalogProps",
    "CfnNamedQuery",
    "CfnNamedQueryProps",
    "CfnPreparedStatement",
    "CfnPreparedStatementProps",
    "CfnWorkGroup",
    "CfnWorkGroupProps",
]

publication.publish()

def _typecheckingstub__9e778036132a28ba53c2761bc41c8664829b3975fbb9bd462237ff7988847c8c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623c0ddaefa992801c97232bd24ec08bd540ddcba1d326b8a2dd765111fed0b8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc0756c9dda825a86e51d436121b8c2f7aee994ed87f506f9672c829a33b42d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bf1b05dc3bde3b33046cf6cf9474d1f971ca0ec8f972d1ad9370f1d7fbfdaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddea67e3e5e92b65efefcc1f16dcd95746251f8e30289d3f61bb667343d25567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a2627302d674bb8859b7e7eb8c403fdb1d36efd5283fe9f8a9bc801c216496(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9584a124e83265c9f256c529d0f8d5667c75b3ed304fd0ea183e14a03a074ae(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93644181c193cacde74fb34a9d64691fc796b769ca68a955b420c1e3c9bf03b3(
    *,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5868b76e84664daa2f4fa0755c2c1d8fee8d10193f6329ef606dd67627dbab(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    database: builtins.str,
    query_string: builtins.str,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762369ff56ee5797d14a909f8f486247a83d36abeef983c30baac084e48c329a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e59b8b66869691fe80e9b6c2d35bf2ac94e5209cff845e1a63017675d253a74(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae4090d261b65e8c773c16cff11db0ab88dece33852c6acb34ff7f5e226e89f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9162781a631ecbf5e8e352347a800d3f4e40b954993cd38c070009f6df37784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc8a648e2a52820eaf168ab38bf09066d7a9482187de4ab63950268efd9b264(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6278c66ab57522a47ef60a226b5a0719eee722244bfa121f8b91a4799de54e5a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ff53ebd66e8f949c207d93d29b7eded7e0b28dd0ad66c361b45723f91416de(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec988326e0e2b0fff4116e1018ea8159751f91e0c2de7b80c01aee67712ca9d(
    *,
    database: builtins.str,
    query_string: builtins.str,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3c2ba02eb6d39b4f5bc166d5336f28fae12779abb14e01cbf992c5e7e1f713(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    query_statement: builtins.str,
    statement_name: builtins.str,
    work_group: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1843656e5295b31a6cff6fb82fa107336abdaabe12066b45b91b0630881911(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7610fe8f5cee5605081b5385e7a4034cd1c7c740e1d58e54d41ab8d74a6571f5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9cb45d56841b4d94ac73342791c32599c5398265a4d226b16f08e33d21b8ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff01499702a5d6cdb3cbd4ca2f205d27e7c36b70935160f8fc567c23e65c396(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67320217f6bf9ae689da110dcef43980db7c8e21ae3fec66f75b5a77ed347d8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6b19b6aeb432b5d2b85002b7f2757504935f8075d3b9924553bb3f58602b1d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2ea406d49f4b8450c827512a4a81c1a53e378e1ff4ec7ac57f282e33c09def(
    *,
    query_statement: builtins.str,
    statement_name: builtins.str,
    work_group: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9fb82712577ce374298ec4efb512f5f2863cfccfd4db99d5b65aac752e9189(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    work_group_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f9d58b59ea00c7a64e346b6e003a8bf66387a1c233ec0421ccbf1db254a1b4(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09ddfd7431fb1762310c00a3bb551614ee2cdb386010fb6494c93fce21102ad(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61033d36d0a40f0949e4eaff014845a7e73915c950f37a75697546334c1ca94d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33288ce48ecb174722c12aa7cdf34d2581999a1aa49647e4986937b50634519f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2e46d61f30d0fb00680579358b3984f54fbe934dfe21d843aa8c57fd191825(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecefe30ef12ef65b8d4f89620033dee21748b8d2a547a362de6ef40a114e11d8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e620a2c249804dab7f5f0a5bcb273bc7f116a21242c4e140ed06c3920f3e89(
    value: typing.Optional[typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d89b88502202fadb4b4f5c62c9e133051037e60aee7fbcb30b0316864d200a(
    *,
    s3_acl_option: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aeff2a519d826d532643c3cac2a7a67c318a1a7362ea9c3e6a30d0502c732f(
    *,
    kms_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa73a07ec83d53098934adf62448447af84e0c2c6cc90838faf27e12978c0e9(
    *,
    encryption_option: builtins.str,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08752fe8bd643a2bc0e8be04800c5035c187009740dab904e8c4a12a4fb9f100(
    *,
    effective_engine_version: typing.Optional[builtins.str] = None,
    selected_engine_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8806fe1222a772491a722490c4de6c85ce69dbe96aac090522718664605a0a(
    *,
    acl_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkGroup.AclConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    encryption_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkGroup.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    output_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ec8c8085eddf90c3f02c7e144adbdeb0af959225ac8bf6af81e5653b2f3a44(
    *,
    additional_configuration: typing.Optional[builtins.str] = None,
    bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
    customer_content_encryption_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkGroup.CustomerContentEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    enforce_work_group_configuration: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    engine_version: typing.Optional[typing.Union[typing.Union[CfnWorkGroup.EngineVersionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    execution_role: typing.Optional[builtins.str] = None,
    publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    result_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkGroup.ResultConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc86e44e8d5721f2ee5ab7b90522e4629fc80461ea08e816109bd72c8e7a14ad(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    work_group_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass
