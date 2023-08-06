'''
# AWS::Cassandra Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as cassandra
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Cassandra construct libraries](https://constructs.dev/search?q=cassandra)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Cassandra resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Cassandra.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Cassandra](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Cassandra.html).

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
class CfnKeyspace(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cassandra.CfnKeyspace",
):
    '''A CloudFormation ``AWS::Cassandra::Keyspace``.

    You can use the ``AWS::Cassandra::Keyspace`` resource to create a new keyspace in Amazon Keyspaces (for Apache Cassandra). For more information, see `Create a keyspace and a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/getting-started.ddl.html>`_ in the *Amazon Keyspaces Developer Guide* .

    :cloudformationResource: AWS::Cassandra::Keyspace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cassandra as cassandra
        
        cfn_keyspace = cassandra.CfnKeyspace(self, "MyCfnKeyspace",
            keyspace_name="keyspaceName",
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
        keyspace_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Cassandra::Keyspace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param keyspace_name: The name of the keyspace to be created. The keyspace name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the keyspace name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . *Length constraints:* Minimum length of 3. Maximum length of 255. *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``
        :param tags: A list of key-value pair tags to be attached to the resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a1a98608699ed02b9062f13a83adfa4559b547a0e24a2574abfcdb7cc1800a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnKeyspaceProps(keyspace_name=keyspace_name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc651f3c5f8250887a68b637332f7ad7606a2c501da3a4723a331e0645d35b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76982159ed22e801f7c4fc629446e81e8424aafded99397fc8fefaff3dda68ab)
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
        '''A list of key-value pair tags to be attached to the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="keyspaceName")
    def keyspace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the keyspace to be created.

        The keyspace name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the keyspace name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        *Length constraints:* Minimum length of 3. Maximum length of 255.

        *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-keyspacename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyspaceName"))

    @keyspace_name.setter
    def keyspace_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ecea7e46babf2bf4a46c73a22a204ddb933d8b6a9842933ff7eddd10fdab83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyspaceName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_cassandra.CfnKeyspaceProps",
    jsii_struct_bases=[],
    name_mapping={"keyspace_name": "keyspaceName", "tags": "tags"},
)
class CfnKeyspaceProps:
    def __init__(
        self,
        *,
        keyspace_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnKeyspace``.

        :param keyspace_name: The name of the keyspace to be created. The keyspace name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the keyspace name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . *Length constraints:* Minimum length of 3. Maximum length of 255. *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``
        :param tags: A list of key-value pair tags to be attached to the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cassandra as cassandra
            
            cfn_keyspace_props = cassandra.CfnKeyspaceProps(
                keyspace_name="keyspaceName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041196832e428f6be1576fe987332f99f622555fa16aafc2e2562967d158531f)
            check_type(argname="argument keyspace_name", value=keyspace_name, expected_type=type_hints["keyspace_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if keyspace_name is not None:
            self._values["keyspace_name"] = keyspace_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def keyspace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the keyspace to be created.

        The keyspace name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the keyspace name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        *Length constraints:* Minimum length of 3. Maximum length of 255.

        *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-keyspacename
        '''
        result = self._values.get("keyspace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pair tags to be attached to the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKeyspaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTable(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cassandra.CfnTable",
):
    '''A CloudFormation ``AWS::Cassandra::Table``.

    You can use the ``AWS::Cassandra::Table`` resource to create a new table in Amazon Keyspaces (for Apache Cassandra). For more information, see `Create a keyspace and a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/getting-started.ddl.html>`_ in the *Amazon Keyspaces Developer Guide* .

    :cloudformationResource: AWS::Cassandra::Table
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cassandra as cassandra
        
        cfn_table = cassandra.CfnTable(self, "MyCfnTable",
            keyspace_name="keyspaceName",
            partition_key_columns=[cassandra.CfnTable.ColumnProperty(
                column_name="columnName",
                column_type="columnType"
            )],
        
            # the properties below are optional
            billing_mode=cassandra.CfnTable.BillingModeProperty(
                mode="mode",
        
                # the properties below are optional
                provisioned_throughput=cassandra.CfnTable.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                )
            ),
            client_side_timestamps_enabled=False,
            clustering_key_columns=[cassandra.CfnTable.ClusteringKeyColumnProperty(
                column=cassandra.CfnTable.ColumnProperty(
                    column_name="columnName",
                    column_type="columnType"
                ),
        
                # the properties below are optional
                order_by="orderBy"
            )],
            default_time_to_live=123,
            encryption_specification=cassandra.CfnTable.EncryptionSpecificationProperty(
                encryption_type="encryptionType",
        
                # the properties below are optional
                kms_key_identifier="kmsKeyIdentifier"
            ),
            point_in_time_recovery_enabled=False,
            regular_columns=[cassandra.CfnTable.ColumnProperty(
                column_name="columnName",
                column_type="columnType"
            )],
            table_name="tableName",
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
        keyspace_name: builtins.str,
        partition_key_columns: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.ColumnProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        billing_mode: typing.Optional[typing.Union[typing.Union["CfnTable.BillingModeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        client_side_timestamps_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        clustering_key_columns: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.ClusteringKeyColumnProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        default_time_to_live: typing.Optional[jsii.Number] = None,
        encryption_specification: typing.Optional[typing.Union[typing.Union["CfnTable.EncryptionSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        regular_columns: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.ColumnProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Cassandra::Table``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param keyspace_name: The name of the keyspace to create the table in. The keyspace must already exist.
        :param partition_key_columns: One or more columns that uniquely identify every row in the table. Every table must have a partition key.
        :param billing_mode: The billing mode for the table, which determines how you'll be charged for reads and writes:. - *On-demand mode* (default) - You pay based on the actual reads and writes your application performs. - *Provisioned mode* - Lets you specify the number of reads and writes per second that you need for your application. If you don't specify a value for this property, then the table will use on-demand mode.
        :param client_side_timestamps_enabled: Enables client-side timestamps for the table. By default, the setting is disabled. You can enable client-side timestamps with the following option: - ``status: "enabled"`` After client-side timestamps are enabled for a table, you can't disable this setting.
        :param clustering_key_columns: One or more columns that determine how the table data is sorted.
        :param default_time_to_live: The default Time To Live (TTL) value for all rows in a table in seconds. The maximum configurable value is 630,720,000 seconds, which is the equivalent of 20 years. By default, the TTL value for a table is 0, which means data does not expire. For more information, see `Setting the default TTL value for a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl>`_ in the *Amazon Keyspaces Developer Guide* .
        :param encryption_specification: The encryption at rest options for the table. - *AWS owned key* (default) - The key is owned by Amazon Keyspaces. - *Customer managed key* - The key is stored in your account and is created, owned, and managed by you. .. epigraph:: If you choose encryption with a customer managed key, you must specify a valid customer managed KMS key with permissions granted to Amazon Keyspaces. For more information, see `Encryption at rest in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html>`_ in the *Amazon Keyspaces Developer Guide* .
        :param point_in_time_recovery_enabled: Specifies if point-in-time recovery is enabled or disabled for the table. The options are ``PointInTimeRecoveryEnabled=true`` and ``PointInTimeRecoveryEnabled=false`` . If not specified, the default is ``PointInTimeRecoveryEnabled=false`` .
        :param regular_columns: One or more columns that are not part of the primary key - that is, columns that are *not* defined as partition key columns or clustering key columns. You can add regular columns to existing tables by adding them to the template.
        :param table_name: The name of the table to be created. The table name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacing this resource. You can perform updates that require no interruption or some interruption. If you must replace the resource, specify a new name. *Length constraints:* Minimum length of 3. Maximum length of 255. *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``
        :param tags: A list of key-value pair tags to be attached to the resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f502982ed1212ce0ef90b43cc55de90c351b7fa301c27ca7e15578b48aa698)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTableProps(
            keyspace_name=keyspace_name,
            partition_key_columns=partition_key_columns,
            billing_mode=billing_mode,
            client_side_timestamps_enabled=client_side_timestamps_enabled,
            clustering_key_columns=clustering_key_columns,
            default_time_to_live=default_time_to_live,
            encryption_specification=encryption_specification,
            point_in_time_recovery_enabled=point_in_time_recovery_enabled,
            regular_columns=regular_columns,
            table_name=table_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b59905126987e3729fb08ab70f1b555c185b39e0f5e57c5bba98e6ece2d9a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6c0d446a8d16094354a3fe1f31c4285732eb51dc3570b2d23edce3c9b21542f)
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
        '''A list of key-value pair tags to be attached to the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="keyspaceName")
    def keyspace_name(self) -> builtins.str:
        '''The name of the keyspace to create the table in.

        The keyspace must already exist.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-keyspacename
        '''
        return typing.cast(builtins.str, jsii.get(self, "keyspaceName"))

    @keyspace_name.setter
    def keyspace_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd9527e29412b6b7572d3b3cccfd27c2218e0bcb472c97932dcb24330d42e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyspaceName", value)

    @builtins.property
    @jsii.member(jsii_name="partitionKeyColumns")
    def partition_key_columns(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ColumnProperty", _IResolvable_a771d0ef]]]:
        '''One or more columns that uniquely identify every row in the table.

        Every table must have a partition key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-partitionkeycolumns
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ColumnProperty", _IResolvable_a771d0ef]]], jsii.get(self, "partitionKeyColumns"))

    @partition_key_columns.setter
    def partition_key_columns(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ColumnProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e64f0d40770bbe3ef7eebca06b7b2dfe769c3ef14432e3f14429dd74e2de76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKeyColumns", value)

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.BillingModeProperty", _IResolvable_a771d0ef]]:
        '''The billing mode for the table, which determines how you'll be charged for reads and writes:.

        - *On-demand mode* (default) - You pay based on the actual reads and writes your application performs.
        - *Provisioned mode* - Lets you specify the number of reads and writes per second that you need for your application.

        If you don't specify a value for this property, then the table will use on-demand mode.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-billingmode
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.BillingModeProperty", _IResolvable_a771d0ef]], jsii.get(self, "billingMode"))

    @billing_mode.setter
    def billing_mode(
        self,
        value: typing.Optional[typing.Union["CfnTable.BillingModeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c2ea9b2d4a6c74b8b039e2a7512a1a1ad0514be7e8417b292f998201312c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingMode", value)

    @builtins.property
    @jsii.member(jsii_name="clientSideTimestampsEnabled")
    def client_side_timestamps_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables client-side timestamps for the table.

        By default, the setting is disabled. You can enable client-side timestamps with the following option:

        - ``status: "enabled"``

        After client-side timestamps are enabled for a table, you can't disable this setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-clientsidetimestampsenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "clientSideTimestampsEnabled"))

    @client_side_timestamps_enabled.setter
    def client_side_timestamps_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35df6a7b4c87a63c4653d240ee2ae5d922a3f4976cd6b9377be1adf62445efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSideTimestampsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="clusteringKeyColumns")
    def clustering_key_columns(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ClusteringKeyColumnProperty", _IResolvable_a771d0ef]]]]:
        '''One or more columns that determine how the table data is sorted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-clusteringkeycolumns
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ClusteringKeyColumnProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "clusteringKeyColumns"))

    @clustering_key_columns.setter
    def clustering_key_columns(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ClusteringKeyColumnProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1b77e1442410b069a131b0f3665000806bb5d674d0f1efe02562a0f6a24f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusteringKeyColumns", value)

    @builtins.property
    @jsii.member(jsii_name="defaultTimeToLive")
    def default_time_to_live(self) -> typing.Optional[jsii.Number]:
        '''The default Time To Live (TTL) value for all rows in a table in seconds.

        The maximum configurable value is 630,720,000 seconds, which is the equivalent of 20 years. By default, the TTL value for a table is 0, which means data does not expire.

        For more information, see `Setting the default TTL value for a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl>`_ in the *Amazon Keyspaces Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-defaulttimetolive
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTimeToLive"))

    @default_time_to_live.setter
    def default_time_to_live(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21eeccee5c2a42c8c42a543545f505591011c844f29c93c7ead513f964db2c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTimeToLive", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionSpecification")
    def encryption_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.EncryptionSpecificationProperty", _IResolvable_a771d0ef]]:
        '''The encryption at rest options for the table.

        - *AWS owned key* (default) - The key is owned by Amazon Keyspaces.
        - *Customer managed key* - The key is stored in your account and is created, owned, and managed by you.

        .. epigraph::

           If you choose encryption with a customer managed key, you must specify a valid customer managed KMS key with permissions granted to Amazon Keyspaces.

        For more information, see `Encryption at rest in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html>`_ in the *Amazon Keyspaces Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-encryptionspecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.EncryptionSpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "encryptionSpecification"))

    @encryption_specification.setter
    def encryption_specification(
        self,
        value: typing.Optional[typing.Union["CfnTable.EncryptionSpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238d1e2e093591fecafe0fb7f9cc4b4ad0a15d833080aca09536ab67da65f9cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecoveryEnabled")
    def point_in_time_recovery_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies if point-in-time recovery is enabled or disabled for the table.

        The options are ``PointInTimeRecoveryEnabled=true`` and ``PointInTimeRecoveryEnabled=false`` . If not specified, the default is ``PointInTimeRecoveryEnabled=false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-pointintimerecoveryenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "pointInTimeRecoveryEnabled"))

    @point_in_time_recovery_enabled.setter
    def point_in_time_recovery_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269f14d1aeac1d9900cbc946262fe05bfdb573da085db0db64be1679ed367aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeRecoveryEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="regularColumns")
    def regular_columns(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ColumnProperty", _IResolvable_a771d0ef]]]]:
        '''One or more columns that are not part of the primary key - that is, columns that are *not* defined as partition key columns or clustering key columns.

        You can add regular columns to existing tables by adding them to the template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-regularcolumns
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ColumnProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "regularColumns"))

    @regular_columns.setter
    def regular_columns(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.ColumnProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f7ee948e09cae2575851620e3c4806e6dc9603f2286d630083c57ea427d26f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regularColumns", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name of the table to be created.

        The table name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacing this resource. You can perform updates that require no interruption or some interruption. If you must replace the resource, specify a new name.

        *Length constraints:* Minimum length of 3. Maximum length of 255.

        *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-tablename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893f404aee3cb7524033c2f9e1821d94455542b18f4cf7df19b809f9215193e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_cassandra.CfnTable.BillingModeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mode": "mode",
            "provisioned_throughput": "provisionedThroughput",
        },
    )
    class BillingModeProperty:
        def __init__(
            self,
            *,
            mode: builtins.str,
            provisioned_throughput: typing.Optional[typing.Union[typing.Union["CfnTable.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Determines the billing mode for the table - on-demand or provisioned.

            :param mode: The billing mode for the table:. - On-demand mode - ``ON_DEMAND`` - Provisioned mode - ``PROVISIONED`` .. epigraph:: If you choose ``PROVISIONED`` mode, then you also need to specify provisioned throughput (read and write capacity) for the table. Valid values: ``ON_DEMAND`` | ``PROVISIONED``
            :param provisioned_throughput: The provisioned read capacity and write capacity for the table. For more information, see `Provisioned throughput capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html#ReadWriteCapacityMode.Provisioned>`_ in the *Amazon Keyspaces Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cassandra as cassandra
                
                billing_mode_property = cassandra.CfnTable.BillingModeProperty(
                    mode="mode",
                
                    # the properties below are optional
                    provisioned_throughput=cassandra.CfnTable.ProvisionedThroughputProperty(
                        read_capacity_units=123,
                        write_capacity_units=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d393497717d7eb080bd2a8fb1373cc93f8b80720ed35a26ec40945c776aafab5)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mode": mode,
            }
            if provisioned_throughput is not None:
                self._values["provisioned_throughput"] = provisioned_throughput

        @builtins.property
        def mode(self) -> builtins.str:
            '''The billing mode for the table:.

            - On-demand mode - ``ON_DEMAND``
            - Provisioned mode - ``PROVISIONED``

            .. epigraph::

               If you choose ``PROVISIONED`` mode, then you also need to specify provisioned throughput (read and write capacity) for the table.

            Valid values: ``ON_DEMAND`` | ``PROVISIONED``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html#cfn-cassandra-table-billingmode-mode
            '''
            result = self._values.get("mode")
            assert result is not None, "Required property 'mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def provisioned_throughput(
            self,
        ) -> typing.Optional[typing.Union["CfnTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]]:
            '''The provisioned read capacity and write capacity for the table.

            For more information, see `Provisioned throughput capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html#ReadWriteCapacityMode.Provisioned>`_ in the *Amazon Keyspaces Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html#cfn-cassandra-table-billingmode-provisionedthroughput
            '''
            result = self._values.get("provisioned_throughput")
            return typing.cast(typing.Optional[typing.Union["CfnTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BillingModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cassandra.CfnTable.ClusteringKeyColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"column": "column", "order_by": "orderBy"},
    )
    class ClusteringKeyColumnProperty:
        def __init__(
            self,
            *,
            column: typing.Union[typing.Union["CfnTable.ColumnProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            order_by: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an individual column within the clustering key.

            :param column: The name and data type of this clustering key column.
            :param order_by: The order in which this column's data is stored:. - ``ASC`` (default) - The column's data is stored in ascending order. - ``DESC`` - The column's data is stored in descending order.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cassandra as cassandra
                
                clustering_key_column_property = cassandra.CfnTable.ClusteringKeyColumnProperty(
                    column=cassandra.CfnTable.ColumnProperty(
                        column_name="columnName",
                        column_type="columnType"
                    ),
                
                    # the properties below are optional
                    order_by="orderBy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e018cdbe40a2f9c173fe6b11ed6cf1050aedf61cc54775de7497297b1c86807)
                check_type(argname="argument column", value=column, expected_type=type_hints["column"])
                check_type(argname="argument order_by", value=order_by, expected_type=type_hints["order_by"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "column": column,
            }
            if order_by is not None:
                self._values["order_by"] = order_by

        @builtins.property
        def column(
            self,
        ) -> typing.Union["CfnTable.ColumnProperty", _IResolvable_a771d0ef]:
            '''The name and data type of this clustering key column.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html#cfn-cassandra-table-clusteringkeycolumn-column
            '''
            result = self._values.get("column")
            assert result is not None, "Required property 'column' is missing"
            return typing.cast(typing.Union["CfnTable.ColumnProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def order_by(self) -> typing.Optional[builtins.str]:
            '''The order in which this column's data is stored:.

            - ``ASC`` (default) - The column's data is stored in ascending order.
            - ``DESC`` - The column's data is stored in descending order.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html#cfn-cassandra-table-clusteringkeycolumn-orderby
            '''
            result = self._values.get("order_by")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClusteringKeyColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cassandra.CfnTable.ColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"column_name": "columnName", "column_type": "columnType"},
    )
    class ColumnProperty:
        def __init__(
            self,
            *,
            column_name: builtins.str,
            column_type: builtins.str,
        ) -> None:
            '''The name and data type of an individual column in a table.

            :param column_name: The name of the column. For more information, see `Identifiers <https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.elements.identifier>`_ in the *Amazon Keyspaces Developer Guide* .
            :param column_type: The data type of the column. For more information, see `Data types <https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.data-types>`_ in the *Amazon Keyspaces Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cassandra as cassandra
                
                column_property = cassandra.CfnTable.ColumnProperty(
                    column_name="columnName",
                    column_type="columnType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6da92151314285111b85dd2b91aa8477b2e1baac720c402707591183b94bcaa7)
                check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
                check_type(argname="argument column_type", value=column_type, expected_type=type_hints["column_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "column_name": column_name,
                "column_type": column_type,
            }

        @builtins.property
        def column_name(self) -> builtins.str:
            '''The name of the column.

            For more information, see `Identifiers <https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.elements.identifier>`_ in the *Amazon Keyspaces Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html#cfn-cassandra-table-column-columnname
            '''
            result = self._values.get("column_name")
            assert result is not None, "Required property 'column_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def column_type(self) -> builtins.str:
            '''The data type of the column.

            For more information, see `Data types <https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.data-types>`_ in the *Amazon Keyspaces Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html#cfn-cassandra-table-column-columntype
            '''
            result = self._values.get("column_type")
            assert result is not None, "Required property 'column_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cassandra.CfnTable.EncryptionSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_type": "encryptionType",
            "kms_key_identifier": "kmsKeyIdentifier",
        },
    )
    class EncryptionSpecificationProperty:
        def __init__(
            self,
            *,
            encryption_type: builtins.str,
            kms_key_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the encryption at rest option selected for the table.

            :param encryption_type: The encryption at rest options for the table. - *AWS owned key* (default) - ``AWS_OWNED_KMS_KEY`` - *Customer managed key* - ``CUSTOMER_MANAGED_KMS_KEY`` .. epigraph:: If you choose ``CUSTOMER_MANAGED_KMS_KEY`` , a ``kms_key_identifier`` in the format of a key ARN is required. Valid values: ``CUSTOMER_MANAGED_KMS_KEY`` | ``AWS_OWNED_KMS_KEY`` .
            :param kms_key_identifier: Requires a ``kms_key_identifier`` in the format of a key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-encryptionspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cassandra as cassandra
                
                encryption_specification_property = cassandra.CfnTable.EncryptionSpecificationProperty(
                    encryption_type="encryptionType",
                
                    # the properties below are optional
                    kms_key_identifier="kmsKeyIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38a8742b4ccdcac77dc7f1f16a3064e1e2db7c5a58ace697ac00af430803a392)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument kms_key_identifier", value=kms_key_identifier, expected_type=type_hints["kms_key_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encryption_type": encryption_type,
            }
            if kms_key_identifier is not None:
                self._values["kms_key_identifier"] = kms_key_identifier

        @builtins.property
        def encryption_type(self) -> builtins.str:
            '''The encryption at rest options for the table.

            - *AWS owned key* (default) - ``AWS_OWNED_KMS_KEY``
            - *Customer managed key* - ``CUSTOMER_MANAGED_KMS_KEY``

            .. epigraph::

               If you choose ``CUSTOMER_MANAGED_KMS_KEY`` , a ``kms_key_identifier`` in the format of a key ARN is required.

            Valid values: ``CUSTOMER_MANAGED_KMS_KEY`` | ``AWS_OWNED_KMS_KEY`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-encryptionspecification.html#cfn-cassandra-table-encryptionspecification-encryptiontype
            '''
            result = self._values.get("encryption_type")
            assert result is not None, "Required property 'encryption_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key_identifier(self) -> typing.Optional[builtins.str]:
            '''Requires a ``kms_key_identifier`` in the format of a key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-encryptionspecification.html#cfn-cassandra-table-encryptionspecification-kmskeyidentifier
            '''
            result = self._values.get("kms_key_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cassandra.CfnTable.ProvisionedThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_capacity_units": "readCapacityUnits",
            "write_capacity_units": "writeCapacityUnits",
        },
    )
    class ProvisionedThroughputProperty:
        def __init__(
            self,
            *,
            read_capacity_units: jsii.Number,
            write_capacity_units: jsii.Number,
        ) -> None:
            '''The provisioned throughput for the table, which consists of ``ReadCapacityUnits`` and ``WriteCapacityUnits`` .

            :param read_capacity_units: The amount of read capacity that's provisioned for the table. For more information, see `Read/write capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html>`_ in the *Amazon Keyspaces Developer Guide* .
            :param write_capacity_units: The amount of write capacity that's provisioned for the table. For more information, see `Read/write capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cassandra as cassandra
                
                provisioned_throughput_property = cassandra.CfnTable.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4820b25f1e19688ece01bbba4bc7accd4e5e6faa3adef0e1027cd364b6610357)
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
                check_type(argname="argument write_capacity_units", value=write_capacity_units, expected_type=type_hints["write_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "read_capacity_units": read_capacity_units,
                "write_capacity_units": write_capacity_units,
            }

        @builtins.property
        def read_capacity_units(self) -> jsii.Number:
            '''The amount of read capacity that's provisioned for the table.

            For more information, see `Read/write capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html#cfn-cassandra-table-provisionedthroughput-readcapacityunits
            '''
            result = self._values.get("read_capacity_units")
            assert result is not None, "Required property 'read_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def write_capacity_units(self) -> jsii.Number:
            '''The amount of write capacity that's provisioned for the table.

            For more information, see `Read/write capacity mode <https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html>`_ in the *Amazon Keyspaces Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html#cfn-cassandra-table-provisionedthroughput-writecapacityunits
            '''
            result = self._values.get("write_capacity_units")
            assert result is not None, "Required property 'write_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_cassandra.CfnTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "keyspace_name": "keyspaceName",
        "partition_key_columns": "partitionKeyColumns",
        "billing_mode": "billingMode",
        "client_side_timestamps_enabled": "clientSideTimestampsEnabled",
        "clustering_key_columns": "clusteringKeyColumns",
        "default_time_to_live": "defaultTimeToLive",
        "encryption_specification": "encryptionSpecification",
        "point_in_time_recovery_enabled": "pointInTimeRecoveryEnabled",
        "regular_columns": "regularColumns",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnTableProps:
    def __init__(
        self,
        *,
        keyspace_name: builtins.str,
        partition_key_columns: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        billing_mode: typing.Optional[typing.Union[typing.Union[CfnTable.BillingModeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        client_side_timestamps_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        clustering_key_columns: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ClusteringKeyColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        default_time_to_live: typing.Optional[jsii.Number] = None,
        encryption_specification: typing.Optional[typing.Union[typing.Union[CfnTable.EncryptionSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        regular_columns: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTable``.

        :param keyspace_name: The name of the keyspace to create the table in. The keyspace must already exist.
        :param partition_key_columns: One or more columns that uniquely identify every row in the table. Every table must have a partition key.
        :param billing_mode: The billing mode for the table, which determines how you'll be charged for reads and writes:. - *On-demand mode* (default) - You pay based on the actual reads and writes your application performs. - *Provisioned mode* - Lets you specify the number of reads and writes per second that you need for your application. If you don't specify a value for this property, then the table will use on-demand mode.
        :param client_side_timestamps_enabled: Enables client-side timestamps for the table. By default, the setting is disabled. You can enable client-side timestamps with the following option: - ``status: "enabled"`` After client-side timestamps are enabled for a table, you can't disable this setting.
        :param clustering_key_columns: One or more columns that determine how the table data is sorted.
        :param default_time_to_live: The default Time To Live (TTL) value for all rows in a table in seconds. The maximum configurable value is 630,720,000 seconds, which is the equivalent of 20 years. By default, the TTL value for a table is 0, which means data does not expire. For more information, see `Setting the default TTL value for a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl>`_ in the *Amazon Keyspaces Developer Guide* .
        :param encryption_specification: The encryption at rest options for the table. - *AWS owned key* (default) - The key is owned by Amazon Keyspaces. - *Customer managed key* - The key is stored in your account and is created, owned, and managed by you. .. epigraph:: If you choose encryption with a customer managed key, you must specify a valid customer managed KMS key with permissions granted to Amazon Keyspaces. For more information, see `Encryption at rest in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html>`_ in the *Amazon Keyspaces Developer Guide* .
        :param point_in_time_recovery_enabled: Specifies if point-in-time recovery is enabled or disabled for the table. The options are ``PointInTimeRecoveryEnabled=true`` and ``PointInTimeRecoveryEnabled=false`` . If not specified, the default is ``PointInTimeRecoveryEnabled=false`` .
        :param regular_columns: One or more columns that are not part of the primary key - that is, columns that are *not* defined as partition key columns or clustering key columns. You can add regular columns to existing tables by adding them to the template.
        :param table_name: The name of the table to be created. The table name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacing this resource. You can perform updates that require no interruption or some interruption. If you must replace the resource, specify a new name. *Length constraints:* Minimum length of 3. Maximum length of 255. *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``
        :param tags: A list of key-value pair tags to be attached to the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cassandra as cassandra
            
            cfn_table_props = cassandra.CfnTableProps(
                keyspace_name="keyspaceName",
                partition_key_columns=[cassandra.CfnTable.ColumnProperty(
                    column_name="columnName",
                    column_type="columnType"
                )],
            
                # the properties below are optional
                billing_mode=cassandra.CfnTable.BillingModeProperty(
                    mode="mode",
            
                    # the properties below are optional
                    provisioned_throughput=cassandra.CfnTable.ProvisionedThroughputProperty(
                        read_capacity_units=123,
                        write_capacity_units=123
                    )
                ),
                client_side_timestamps_enabled=False,
                clustering_key_columns=[cassandra.CfnTable.ClusteringKeyColumnProperty(
                    column=cassandra.CfnTable.ColumnProperty(
                        column_name="columnName",
                        column_type="columnType"
                    ),
            
                    # the properties below are optional
                    order_by="orderBy"
                )],
                default_time_to_live=123,
                encryption_specification=cassandra.CfnTable.EncryptionSpecificationProperty(
                    encryption_type="encryptionType",
            
                    # the properties below are optional
                    kms_key_identifier="kmsKeyIdentifier"
                ),
                point_in_time_recovery_enabled=False,
                regular_columns=[cassandra.CfnTable.ColumnProperty(
                    column_name="columnName",
                    column_type="columnType"
                )],
                table_name="tableName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd92bc8d89d5d112f0ff77ad31ed2134088e8bcb0ef5c9dabedc3e2b2eb3027)
            check_type(argname="argument keyspace_name", value=keyspace_name, expected_type=type_hints["keyspace_name"])
            check_type(argname="argument partition_key_columns", value=partition_key_columns, expected_type=type_hints["partition_key_columns"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument client_side_timestamps_enabled", value=client_side_timestamps_enabled, expected_type=type_hints["client_side_timestamps_enabled"])
            check_type(argname="argument clustering_key_columns", value=clustering_key_columns, expected_type=type_hints["clustering_key_columns"])
            check_type(argname="argument default_time_to_live", value=default_time_to_live, expected_type=type_hints["default_time_to_live"])
            check_type(argname="argument encryption_specification", value=encryption_specification, expected_type=type_hints["encryption_specification"])
            check_type(argname="argument point_in_time_recovery_enabled", value=point_in_time_recovery_enabled, expected_type=type_hints["point_in_time_recovery_enabled"])
            check_type(argname="argument regular_columns", value=regular_columns, expected_type=type_hints["regular_columns"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keyspace_name": keyspace_name,
            "partition_key_columns": partition_key_columns,
        }
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if client_side_timestamps_enabled is not None:
            self._values["client_side_timestamps_enabled"] = client_side_timestamps_enabled
        if clustering_key_columns is not None:
            self._values["clustering_key_columns"] = clustering_key_columns
        if default_time_to_live is not None:
            self._values["default_time_to_live"] = default_time_to_live
        if encryption_specification is not None:
            self._values["encryption_specification"] = encryption_specification
        if point_in_time_recovery_enabled is not None:
            self._values["point_in_time_recovery_enabled"] = point_in_time_recovery_enabled
        if regular_columns is not None:
            self._values["regular_columns"] = regular_columns
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def keyspace_name(self) -> builtins.str:
        '''The name of the keyspace to create the table in.

        The keyspace must already exist.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-keyspacename
        '''
        result = self._values.get("keyspace_name")
        assert result is not None, "Required property 'keyspace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition_key_columns(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ColumnProperty, _IResolvable_a771d0ef]]]:
        '''One or more columns that uniquely identify every row in the table.

        Every table must have a partition key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-partitionkeycolumns
        '''
        result = self._values.get("partition_key_columns")
        assert result is not None, "Required property 'partition_key_columns' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ColumnProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def billing_mode(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.BillingModeProperty, _IResolvable_a771d0ef]]:
        '''The billing mode for the table, which determines how you'll be charged for reads and writes:.

        - *On-demand mode* (default) - You pay based on the actual reads and writes your application performs.
        - *Provisioned mode* - Lets you specify the number of reads and writes per second that you need for your application.

        If you don't specify a value for this property, then the table will use on-demand mode.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-billingmode
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[typing.Union[CfnTable.BillingModeProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def client_side_timestamps_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables client-side timestamps for the table.

        By default, the setting is disabled. You can enable client-side timestamps with the following option:

        - ``status: "enabled"``

        After client-side timestamps are enabled for a table, you can't disable this setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-clientsidetimestampsenabled
        '''
        result = self._values.get("client_side_timestamps_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def clustering_key_columns(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ClusteringKeyColumnProperty, _IResolvable_a771d0ef]]]]:
        '''One or more columns that determine how the table data is sorted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-clusteringkeycolumns
        '''
        result = self._values.get("clustering_key_columns")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ClusteringKeyColumnProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def default_time_to_live(self) -> typing.Optional[jsii.Number]:
        '''The default Time To Live (TTL) value for all rows in a table in seconds.

        The maximum configurable value is 630,720,000 seconds, which is the equivalent of 20 years. By default, the TTL value for a table is 0, which means data does not expire.

        For more information, see `Setting the default TTL value for a table <https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl>`_ in the *Amazon Keyspaces Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-defaulttimetolive
        '''
        result = self._values.get("default_time_to_live")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def encryption_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.EncryptionSpecificationProperty, _IResolvable_a771d0ef]]:
        '''The encryption at rest options for the table.

        - *AWS owned key* (default) - The key is owned by Amazon Keyspaces.
        - *Customer managed key* - The key is stored in your account and is created, owned, and managed by you.

        .. epigraph::

           If you choose encryption with a customer managed key, you must specify a valid customer managed KMS key with permissions granted to Amazon Keyspaces.

        For more information, see `Encryption at rest in Amazon Keyspaces <https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html>`_ in the *Amazon Keyspaces Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-encryptionspecification
        '''
        result = self._values.get("encryption_specification")
        return typing.cast(typing.Optional[typing.Union[CfnTable.EncryptionSpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def point_in_time_recovery_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies if point-in-time recovery is enabled or disabled for the table.

        The options are ``PointInTimeRecoveryEnabled=true`` and ``PointInTimeRecoveryEnabled=false`` . If not specified, the default is ``PointInTimeRecoveryEnabled=false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-pointintimerecoveryenabled
        '''
        result = self._values.get("point_in_time_recovery_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def regular_columns(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ColumnProperty, _IResolvable_a771d0ef]]]]:
        '''One or more columns that are not part of the primary key - that is, columns that are *not* defined as partition key columns or clustering key columns.

        You can add regular columns to existing tables by adding them to the template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-regularcolumns
        '''
        result = self._values.get("regular_columns")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ColumnProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name of the table to be created.

        The table name is case sensitive. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacing this resource. You can perform updates that require no interruption or some interruption. If you must replace the resource, specify a new name.

        *Length constraints:* Minimum length of 3. Maximum length of 255.

        *Pattern:* ``^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pair tags to be attached to the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnKeyspace",
    "CfnKeyspaceProps",
    "CfnTable",
    "CfnTableProps",
]

publication.publish()

def _typecheckingstub__f6a1a98608699ed02b9062f13a83adfa4559b547a0e24a2574abfcdb7cc1800a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    keyspace_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc651f3c5f8250887a68b637332f7ad7606a2c501da3a4723a331e0645d35b2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76982159ed22e801f7c4fc629446e81e8424aafded99397fc8fefaff3dda68ab(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ecea7e46babf2bf4a46c73a22a204ddb933d8b6a9842933ff7eddd10fdab83(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041196832e428f6be1576fe987332f99f622555fa16aafc2e2562967d158531f(
    *,
    keyspace_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f502982ed1212ce0ef90b43cc55de90c351b7fa301c27ca7e15578b48aa698(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    keyspace_name: builtins.str,
    partition_key_columns: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    billing_mode: typing.Optional[typing.Union[typing.Union[CfnTable.BillingModeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    client_side_timestamps_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    clustering_key_columns: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ClusteringKeyColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    default_time_to_live: typing.Optional[jsii.Number] = None,
    encryption_specification: typing.Optional[typing.Union[typing.Union[CfnTable.EncryptionSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    regular_columns: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b59905126987e3729fb08ab70f1b555c185b39e0f5e57c5bba98e6ece2d9a3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c0d446a8d16094354a3fe1f31c4285732eb51dc3570b2d23edce3c9b21542f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd9527e29412b6b7572d3b3cccfd27c2218e0bcb472c97932dcb24330d42e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e64f0d40770bbe3ef7eebca06b7b2dfe769c3ef14432e3f14429dd74e2de76(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ColumnProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c2ea9b2d4a6c74b8b039e2a7512a1a1ad0514be7e8417b292f998201312c0e(
    value: typing.Optional[typing.Union[CfnTable.BillingModeProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35df6a7b4c87a63c4653d240ee2ae5d922a3f4976cd6b9377be1adf62445efe(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1b77e1442410b069a131b0f3665000806bb5d674d0f1efe02562a0f6a24f7d(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ClusteringKeyColumnProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21eeccee5c2a42c8c42a543545f505591011c844f29c93c7ead513f964db2c6b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238d1e2e093591fecafe0fb7f9cc4b4ad0a15d833080aca09536ab67da65f9cc(
    value: typing.Optional[typing.Union[CfnTable.EncryptionSpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269f14d1aeac1d9900cbc946262fe05bfdb573da085db0db64be1679ed367aff(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f7ee948e09cae2575851620e3c4806e6dc9603f2286d630083c57ea427d26f(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.ColumnProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893f404aee3cb7524033c2f9e1821d94455542b18f4cf7df19b809f9215193e8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d393497717d7eb080bd2a8fb1373cc93f8b80720ed35a26ec40945c776aafab5(
    *,
    mode: builtins.str,
    provisioned_throughput: typing.Optional[typing.Union[typing.Union[CfnTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e018cdbe40a2f9c173fe6b11ed6cf1050aedf61cc54775de7497297b1c86807(
    *,
    column: typing.Union[typing.Union[CfnTable.ColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    order_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da92151314285111b85dd2b91aa8477b2e1baac720c402707591183b94bcaa7(
    *,
    column_name: builtins.str,
    column_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a8742b4ccdcac77dc7f1f16a3064e1e2db7c5a58ace697ac00af430803a392(
    *,
    encryption_type: builtins.str,
    kms_key_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4820b25f1e19688ece01bbba4bc7accd4e5e6faa3adef0e1027cd364b6610357(
    *,
    read_capacity_units: jsii.Number,
    write_capacity_units: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd92bc8d89d5d112f0ff77ad31ed2134088e8bcb0ef5c9dabedc3e2b2eb3027(
    *,
    keyspace_name: builtins.str,
    partition_key_columns: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    billing_mode: typing.Optional[typing.Union[typing.Union[CfnTable.BillingModeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    client_side_timestamps_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    clustering_key_columns: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ClusteringKeyColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    default_time_to_live: typing.Optional[jsii.Number] = None,
    encryption_specification: typing.Optional[typing.Union[typing.Union[CfnTable.EncryptionSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    regular_columns: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.ColumnProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
