'''
# Amazon DynamoDB Construct Library

Here is a minimal deployable DynamoDB table definition:

```python
table = dynamodb.Table(self, "Table",
    partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
)
```

## Importing existing tables

To import an existing table into your CDK application, use the `Table.fromTableName`, `Table.fromTableArn` or `Table.fromTableAttributes`
factory method. This method accepts table name or table ARN which describes the properties of an already
existing table:

```python
# user: iam.User

table = dynamodb.Table.from_table_arn(self, "ImportedTable", "arn:aws:dynamodb:us-east-1:111111111:table/my-table")
# now you can just call methods on the table
table.grant_read_write_data(user)
```

If you intend to use the `tableStreamArn` (including indirectly, for example by creating an
`@aws-cdk/aws-lambda-event-source.DynamoEventSource` on the imported table), you *must* use the
`Table.fromTableAttributes` method and the `tableStreamArn` property *must* be populated.

## Keys

When a table is defined, you must define it's schema using the `partitionKey`
(required) and `sortKey` (optional) properties.

## Billing Mode

DynamoDB supports two billing modes:

* PROVISIONED - the default mode where the table and global secondary indexes have configured read and write capacity.
* PAY_PER_REQUEST - on-demand pricing and scaling. You only pay for what you use and there is no read and write capacity for the table or its global secondary indexes.

```python
table = dynamodb.Table(self, "Table",
    partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
)
```

Further reading:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.

## Table Class

DynamoDB supports two table classes:

* STANDARD - the default mode, and is recommended for the vast majority of workloads.
* STANDARD_INFREQUENT_ACCESS - optimized for tables where storage is the dominant cost.

```python
table = dynamodb.Table(self, "Table",
    partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    table_class=dynamodb.TableClass.STANDARD_INFREQUENT_ACCESS
)
```

Further reading:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.TableClasses.html

## Configure AutoScaling for your table

You can have DynamoDB automatically raise and lower the read and write capacities
of your table by setting up autoscaling. You can use this to either keep your
tables at a desired utilization level, or by scaling up and down at pre-configured
times of the day:

Auto-scaling is only relevant for tables with the billing mode, PROVISIONED.

```python
read_scaling = table.auto_scale_read_capacity(min_capacity=1, max_capacity=50)

read_scaling.scale_on_utilization(
    target_utilization_percent=50
)

read_scaling.scale_on_schedule("ScaleUpInTheMorning",
    schedule=appscaling.Schedule.cron(hour="8", minute="0"),
    min_capacity=20
)

read_scaling.scale_on_schedule("ScaleDownAtNight",
    schedule=appscaling.Schedule.cron(hour="20", minute="0"),
    max_capacity=20
)
```

Further reading:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html
https://aws.amazon.com/blogs/database/how-to-use-aws-cloudformation-to-configure-auto-scaling-for-amazon-dynamodb-tables-and-indexes/

## Amazon DynamoDB Global Tables

You can create DynamoDB Global Tables by setting the `replicationRegions` property on a `Table`:

```python
global_table = dynamodb.Table(self, "Table",
    partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    replication_regions=["us-east-1", "us-east-2", "us-west-2"]
)
```

When doing so, a CloudFormation Custom Resource will be added to the stack in order to create the replica tables in the
selected regions.

The default billing mode for Global Tables is `PAY_PER_REQUEST`.
If you want to use `PROVISIONED`,
you have to make sure write auto-scaling is enabled for that Table:

```python
global_table = dynamodb.Table(self, "Table",
    partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    replication_regions=["us-east-1", "us-east-2", "us-west-2"],
    billing_mode=dynamodb.BillingMode.PROVISIONED
)

global_table.auto_scale_write_capacity(
    min_capacity=1,
    max_capacity=10
).scale_on_utilization(target_utilization_percent=75)
```

When adding a replica region for a large table, you might want to increase the
timeout for the replication operation:

```python
global_table = dynamodb.Table(self, "Table",
    partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    replication_regions=["us-east-1", "us-east-2", "us-west-2"],
    replication_timeout=Duration.hours(2)
)
```

## Encryption

All user data stored in Amazon DynamoDB is fully encrypted at rest. When creating a new table, you can choose to encrypt using the following customer master keys (CMK) to encrypt your table:

* AWS owned CMK - By default, all tables are encrypted under an AWS owned customer master key (CMK) in the DynamoDB service account (no additional charges apply).
* AWS managed CMK - AWS KMS keys (one per region) are created in your account, managed, and used on your behalf by AWS DynamoDB (AWS KMS charges apply).
* Customer managed CMK - You have full control over the KMS key used to encrypt the DynamoDB Table (AWS KMS charges apply).

Creating a Table encrypted with a customer managed CMK:

```python
table = dynamodb.Table(self, "MyTable",
    partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED
)

# You can access the CMK that was added to the stack on your behalf by the Table construct via:
table_encryption_key = table.encryption_key
```

You can also supply your own key:

```python
import monocdk as kms


encryption_key = kms.Key(self, "Key",
    enable_key_rotation=True
)
table = dynamodb.Table(self, "MyTable",
    partition_key=kms.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED,
    encryption_key=encryption_key
)
```

In order to use the AWS managed CMK instead, change the code to:

```python
table = dynamodb.Table(self, "MyTable",
    partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    encryption=dynamodb.TableEncryption.AWS_MANAGED
)
```

## Get schema of table or secondary indexes

To get the partition key and sort key of the table or indexes you have configured:

```python
# table: dynamodb.Table

schema = table.schema()
partition_key = schema.partition_key
sort_key = schema.sort_key
```

## Kinesis Stream

A Kinesis Data Stream can be configured on the DynamoDB table to capture item-level changes.

```python
import monocdk as kinesis


stream = kinesis.Stream(self, "Stream")

table = dynamodb.Table(self, "Table",
    partition_key=kinesis.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
    kinesis_stream=stream
)
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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_applicationautoscaling import (
    BaseTargetTrackingProps as _BaseTargetTrackingProps_e4402570,
    ScalingSchedule as _ScalingSchedule_6c3fc38f,
    Schedule as _Schedule_c2a5a45d,
)
from ..aws_cloudwatch import (
    IMetric as _IMetric_5db43d61,
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_iam import Grant as _Grant_bcb5eae7, IGrantable as _IGrantable_4c5a91d1
from ..aws_kinesis import IStream as _IStream_14c6ec7f
from ..aws_kms import IKey as _IKey_36930160


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.Attribute",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class Attribute:
    def __init__(self, *, name: builtins.str, type: "AttributeType") -> None:
        '''(experimental) Represents an attribute for describing the key schema for the table and indexes.

        :param name: (experimental) The name of an attribute.
        :param type: (experimental) The data type of an attribute.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            global_table = dynamodb.Table(self, "Table",
                partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
                replication_regions=["us-east-1", "us-east-2", "us-west-2"],
                billing_mode=dynamodb.BillingMode.PROVISIONED
            )
            
            global_table.auto_scale_write_capacity(
                min_capacity=1,
                max_capacity=10
            ).scale_on_utilization(target_utilization_percent=75)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816674236dee7a82734c355c923a191a5221dc625a7c6e2d61515e1e623731fd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of an attribute.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "AttributeType":
        '''(experimental) The data type of an attribute.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("AttributeType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Attribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_dynamodb.AttributeType")
class AttributeType(enum.Enum):
    '''(experimental) Data types for attributes within a table.

    :see: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html#HowItWorks.DataTypes
    :stability: experimental
    :exampleMetadata: infused

    Example::

        global_table = dynamodb.Table(self, "Table",
            partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            replication_regions=["us-east-1", "us-east-2", "us-west-2"],
            billing_mode=dynamodb.BillingMode.PROVISIONED
        )
        
        global_table.auto_scale_write_capacity(
            min_capacity=1,
            max_capacity=10
        ).scale_on_utilization(target_utilization_percent=75)
    '''

    BINARY = "BINARY"
    '''(experimental) Up to 400KiB of binary data (which must be encoded as base64 before sending to DynamoDB).

    :stability: experimental
    '''
    NUMBER = "NUMBER"
    '''(experimental) Numeric values made of up to 38 digits (positive, negative or zero).

    :stability: experimental
    '''
    STRING = "STRING"
    '''(experimental) Up to 400KiB of UTF-8 encoded text.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_dynamodb.BillingMode")
class BillingMode(enum.Enum):
    '''(experimental) DynamoDB's Read/Write capacity modes.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        table = dynamodb.Table(self, "Table",
            partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
    '''

    PAY_PER_REQUEST = "PAY_PER_REQUEST"
    '''(experimental) Pay only for what you use.

    You don't configure Read/Write capacity units.

    :stability: experimental
    '''
    PROVISIONED = "PROVISIONED"
    '''(experimental) Explicitly specified Read/Write capacity units.

    :stability: experimental
    '''


@jsii.implements(_IInspectable_82c04a63)
class CfnGlobalTable(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dynamodb.CfnGlobalTable",
):
    '''A CloudFormation ``AWS::DynamoDB::GlobalTable``.

    The ``AWS::DynamoDB::GlobalTable`` resource enables you to create and manage a Version 2019.11.21 global table. This resource cannot be used to create or manage a Version 2017.11.29 global table. For more information, see `Global tables <https://docs.aws.amazon.com//amazondynamodb/latest/developerguide/GlobalTables.html>`_ .
    .. epigraph::

       You cannot convert a resource of type ``AWS::DynamoDB::Table`` into a resource of type ``AWS::DynamoDB::GlobalTable`` by changing its type in your template. *Doing so might result in the deletion of your DynamoDB table.*

       You can instead use the GlobalTable resource to create a new table in a single Region. This will be billed the same as a single Region table. If you later update the stack to add other Regions then Global Tables pricing will apply.

    You should be aware of the following behaviors when working with DynamoDB global tables.

    - The IAM Principal executing the stack operation must have the permissions listed below in all regions where you plan to have a global table replica. The IAM Principal's permissions should not have restrictions based on IP source address. Some global tables operations (for example, adding a replica) are asynchronous, and require that the IAM Principal is valid until they complete. You should not delete the Principal (user or IAM role) until CloudFormation has finished updating your stack.
    - ``dynamodb:CreateTable``
    - ``dynamodb:UpdateTable``
    - ``dynamodb:DeleteTable``
    - ``dynamodb:DescribeContinuousBackups``
    - ``dynamodb:DescribeContributorInsights``
    - ``dynamodb:DescribeTable``
    - ``dynamodb:DescribeTableReplicaAutoScaling``
    - ``dynamodb:DescribeTimeToLive``
    - ``dynamodb:ListTables``
    - ``dynamodb:UpdateTimeToLive``
    - ``dynamodb:UpdateContributorInsights``
    - ``dynamodb:UpdateContinuousBackups``
    - ``dynamodb:ListTagsOfResource``
    - ``dynamodb:TableClass``
    - ``dynamodb:TagResource``
    - ``dynamodb:UntagResource``
    - ``dynamodb:BatchWriteItem``
    - ``dynamodb:CreateTableReplica``
    - ``dynamodb:DeleteItem``
    - ``dynamodb:DeleteTableReplica``
    - ``dynamodb:DisableKinesisStreamingDestination``
    - ``dynamodb:EnableKinesisStreamingDestination``
    - ``dynamodb:GetItem``
    - ``dynamodb:PutItem``
    - ``dynamodb:Query``
    - ``dynamodb:Scan``
    - ``dynamodb:UpdateItem``
    - ``dynamodb:DescribeTableReplicaAutoScaling``
    - ``dynamodb:UpdateTableReplicaAutoScaling``
    - ``iam:CreateServiceLinkedRole``
    - ``kms:CreateGrant``
    - ``kms:DescribeKey``
    - ``application-autoscaling:DeleteScalingPolicy``
    - ``application-autoscaling:DeleteScheduledAction``
    - ``application-autoscaling:DeregisterScalableTarget``
    - ``application-autoscaling:DescribeScalingPolicies``
    - ``application-autoscaling:DescribeScalableTargets``
    - ``application-autoscaling:PutScalingPolicy``
    - ``application-autoscaling:PutScheduledAction``
    - ``application-autoscaling:RegisterScalableTarget``
    - When using provisioned billing mode, CloudFormation will create an auto scaling policy on each of your replicas to control their write capacities. You must configure this policy using the ``WriteProvisionedThroughputSettings`` property. CloudFormation will ensure that all replicas have the same write capacity auto scaling property. You cannot directly specify a value for write capacity for a global table.
    - If your table uses provisioned capacity, you must configure auto scaling directly in the ``AWS::DynamoDB::GlobalTable`` resource. You should not configure additional auto scaling policies on any of the table replicas or global secondary indexes, either via API or via ``AWS::ApplicationAutoScaling::ScalableTarget`` or ``AWS::ApplicationAutoScaling::ScalingPolicy`` . Doing so might result in unexpected behavior and is unsupported.
    - In AWS CloudFormation , each global table is controlled by a single stack, in a single region, regardless of the number of replicas. When you deploy your template, CloudFormation will create/update all replicas as part of a single stack operation. You should not deploy the same ``AWS::DynamoDB::GlobalTable`` resource in multiple regions. Doing so will result in errors, and is unsupported. If you deploy your application template in multiple regions, you can use conditions to only create the resource in a single region. Alternatively, you can choose to define your ``AWS::DynamoDB::GlobalTable`` resources in a stack separate from your application stack, and make sure it is only deployed to a single region.

    :cloudformationResource: AWS::DynamoDB::GlobalTable
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_dynamodb as dynamodb
        
        cfn_global_table = dynamodb.CfnGlobalTable(self, "MyCfnGlobalTable",
            attribute_definitions=[dynamodb.CfnGlobalTable.AttributeDefinitionProperty(
                attribute_name="attributeName",
                attribute_type="attributeType"
            )],
            key_schema=[dynamodb.CfnGlobalTable.KeySchemaProperty(
                attribute_name="attributeName",
                key_type="keyType"
            )],
            replicas=[dynamodb.CfnGlobalTable.ReplicaSpecificationProperty(
                region="region",
        
                # the properties below are optional
                contributor_insights_specification=dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty(
                    enabled=False
                ),
                deletion_protection_enabled=False,
                global_secondary_indexes=[dynamodb.CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty(
                    index_name="indexName",
        
                    # the properties below are optional
                    contributor_insights_specification=dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty(
                        enabled=False
                    ),
                    read_provisioned_throughput_settings=dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty(
                        read_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                                target_value=123,
        
                                # the properties below are optional
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123
                            ),
        
                            # the properties below are optional
                            seed_capacity=123
                        ),
                        read_capacity_units=123
                    )
                )],
                kinesis_stream_specification=dynamodb.CfnGlobalTable.KinesisStreamSpecificationProperty(
                    stream_arn="streamArn"
                ),
                point_in_time_recovery_specification=dynamodb.CfnGlobalTable.PointInTimeRecoverySpecificationProperty(
                    point_in_time_recovery_enabled=False
                ),
                read_provisioned_throughput_settings=dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty(
                    read_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                            target_value=123,
        
                            # the properties below are optional
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123
                        ),
        
                        # the properties below are optional
                        seed_capacity=123
                    ),
                    read_capacity_units=123
                ),
                sse_specification=dynamodb.CfnGlobalTable.ReplicaSSESpecificationProperty(
                    kms_master_key_id="kmsMasterKeyId"
                ),
                table_class="tableClass",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )],
        
            # the properties below are optional
            billing_mode="billingMode",
            global_secondary_indexes=[dynamodb.CfnGlobalTable.GlobalSecondaryIndexProperty(
                index_name="indexName",
                key_schema=[dynamodb.CfnGlobalTable.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                projection=dynamodb.CfnGlobalTable.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                ),
        
                # the properties below are optional
                write_provisioned_throughput_settings=dynamodb.CfnGlobalTable.WriteProvisionedThroughputSettingsProperty(
                    write_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                            target_value=123,
        
                            # the properties below are optional
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123
                        ),
        
                        # the properties below are optional
                        seed_capacity=123
                    )
                )
            )],
            local_secondary_indexes=[dynamodb.CfnGlobalTable.LocalSecondaryIndexProperty(
                index_name="indexName",
                key_schema=[dynamodb.CfnGlobalTable.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                projection=dynamodb.CfnGlobalTable.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                )
            )],
            sse_specification=dynamodb.CfnGlobalTable.SSESpecificationProperty(
                sse_enabled=False,
        
                # the properties below are optional
                sse_type="sseType"
            ),
            stream_specification=dynamodb.CfnGlobalTable.StreamSpecificationProperty(
                stream_view_type="streamViewType"
            ),
            table_name="tableName",
            time_to_live_specification=dynamodb.CfnGlobalTable.TimeToLiveSpecificationProperty(
                enabled=False,
        
                # the properties below are optional
                attribute_name="attributeName"
            ),
            write_provisioned_throughput_settings=dynamodb.CfnGlobalTable.WriteProvisionedThroughputSettingsProperty(
                write_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                    max_capacity=123,
                    min_capacity=123,
                    target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                        target_value=123,
        
                        # the properties below are optional
                        disable_scale_in=False,
                        scale_in_cooldown=123,
                        scale_out_cooldown=123
                    ),
        
                    # the properties below are optional
                    seed_capacity=123
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        attribute_definitions: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalTable.AttributeDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalTable.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        replicas: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalTable.ReplicaSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        billing_mode: typing.Optional[builtins.str] = None,
        global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalTable.GlobalSecondaryIndexProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        local_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalTable.LocalSecondaryIndexProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        sse_specification: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stream_specification: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.StreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        table_name: typing.Optional[builtins.str] = None,
        time_to_live_specification: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.TimeToLiveSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        write_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.WriteProvisionedThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::DynamoDB::GlobalTable``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attribute_definitions: A list of attributes that describe the key schema for the global table and indexes.
        :param key_schema: Specifies the attributes that make up the primary key for the table. The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.
        :param replicas: Specifies the list of replicas for your global table. The list must contain at least one element, the region where the stack defining the global table is deployed. For example, if you define your table in a stack deployed to us-east-1, you must have an entry in ``Replicas`` with the region us-east-1. You cannot remove the replica in the stack region. .. epigraph:: Adding a replica might take a few minutes for an empty table, or up to several hours for large tables. If you want to add or remove a replica, we recommend submitting an ``UpdateStack`` operation containing only that change. If you add or delete a replica during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new replica, you might need to manually delete the replica. You can create a new global table with as many replicas as needed. You can add or remove replicas after table creation, but you can only add or remove a single replica in each update.
        :param billing_mode: Specifies how you are charged for read and write throughput and how you manage capacity. Valid values are:. - ``PAY_PER_REQUEST`` - ``PROVISIONED`` All replicas in your global table will have the same billing mode. If you use ``PROVISIONED`` billing mode, you must provide an auto scaling configuration via the ``WriteProvisionedThroughputSettings`` property. The default value of this property is ``PROVISIONED`` .
        :param global_secondary_indexes: Global secondary indexes to be created on the global table. You can create up to 20 global secondary indexes. Each replica in your global table will have the same global secondary index settings. You can only create or delete one global secondary index in a single stack operation. Since the backfilling of an index could take a long time, CloudFormation does not wait for the index to become active. If a stack operation rolls back, CloudFormation might not delete an index that has been added. In that case, you will need to delete the index manually.
        :param local_secondary_indexes: Local secondary indexes to be created on the table. You can create up to five local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes. Each replica in your global table will have the same local secondary index settings.
        :param sse_specification: Specifies the settings to enable server-side encryption. These settings will be applied to all replicas. If you plan to use customer-managed KMS keys, you must provide a key for each replica using the ``ReplicaSpecification.ReplicaSSESpecification`` property.
        :param stream_specification: Specifies the streams settings on your global table. You must provide a value for this property if your global table contains more than one replica. You can only change the streams settings if your global table has only one replica.
        :param table_name: A name for the global table. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID as the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param time_to_live_specification: Specifies the time to live (TTL) settings for the table. This setting will be applied to all replicas.
        :param write_provisioned_throughput_settings: Specifies an auto scaling policy for write capacity. This policy will be applied to all replicas. This setting must be specified if ``BillingMode`` is set to ``PROVISIONED`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbe5d7f749468118280141c91598ee529c3cb7b9b24c48a1f398f27e21546d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGlobalTableProps(
            attribute_definitions=attribute_definitions,
            key_schema=key_schema,
            replicas=replicas,
            billing_mode=billing_mode,
            global_secondary_indexes=global_secondary_indexes,
            local_secondary_indexes=local_secondary_indexes,
            sse_specification=sse_specification,
            stream_specification=stream_specification,
            table_name=table_name,
            time_to_live_specification=time_to_live_specification,
            write_provisioned_throughput_settings=write_provisioned_throughput_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4010b24590498478c2356fb3c7bc894f03bb87a29e9f3902f199bce5ef3e7653)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24d17caa3295d0c79582f79aab3278e501df1324875ac0f7877e8804642af5aa)
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
        '''The Amazon Resource Name (ARN) of the DynamoDB table, such as ``arn:aws:dynamodb:us-east-2:123456789012:table/myDynamoDBTable`` .

        The ARN returned is that of the replica in the region the stack is deployed to.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStreamArn")
    def attr_stream_arn(self) -> builtins.str:
        '''The ARN of the DynamoDB stream, such as ``arn:aws:dynamodb:us-east-1:123456789012:table/testddbstack-myDynamoDBTable-012A1SL7SMP5Q/stream/2015-11-30T20:10:00.000`` . The ``StreamArn`` returned is that of the replica in the region the stack is deployed to.

        .. epigraph::

           You must specify the ``StreamSpecification`` property to use this attribute.

        :cloudformationAttribute: StreamArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStreamArn"))

    @builtins.property
    @jsii.member(jsii_name="attrTableId")
    def attr_table_id(self) -> builtins.str:
        '''Unique identifier for the table, such as ``a123b456-01ab-23cd-123a-111222aaabbb`` .

        The ``TableId`` returned is that of the replica in the region the stack is deployed to.

        :cloudformationAttribute: TableId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTableId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="attributeDefinitions")
    def attribute_definitions(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.AttributeDefinitionProperty", _IResolvable_a771d0ef]]]:
        '''A list of attributes that describe the key schema for the global table and indexes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-attributedefinitions
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.AttributeDefinitionProperty", _IResolvable_a771d0ef]]], jsii.get(self, "attributeDefinitions"))

    @attribute_definitions.setter
    def attribute_definitions(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.AttributeDefinitionProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd425fc8274826e47420227bf64b306fbf22a1fdb2c224363c3ad74ae666f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeDefinitions", value)

    @builtins.property
    @jsii.member(jsii_name="keySchema")
    def key_schema(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.KeySchemaProperty", _IResolvable_a771d0ef]]]:
        '''Specifies the attributes that make up the primary key for the table.

        The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-keyschema
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.KeySchemaProperty", _IResolvable_a771d0ef]]], jsii.get(self, "keySchema"))

    @key_schema.setter
    def key_schema(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.KeySchemaProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c62749d0a6bacb4d43b8361e2fd5837ab2168b09083ec3b536f0e25540cbf52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keySchema", value)

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.ReplicaSpecificationProperty", _IResolvable_a771d0ef]]]:
        '''Specifies the list of replicas for your global table.

        The list must contain at least one element, the region where the stack defining the global table is deployed. For example, if you define your table in a stack deployed to us-east-1, you must have an entry in ``Replicas`` with the region us-east-1. You cannot remove the replica in the stack region.
        .. epigraph::

           Adding a replica might take a few minutes for an empty table, or up to several hours for large tables. If you want to add or remove a replica, we recommend submitting an ``UpdateStack`` operation containing only that change.

           If you add or delete a replica during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new replica, you might need to manually delete the replica.

        You can create a new global table with as many replicas as needed. You can add or remove replicas after table creation, but you can only add or remove a single replica in each update.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-replicas
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.ReplicaSpecificationProperty", _IResolvable_a771d0ef]]], jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.ReplicaSpecificationProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fbb4cc25efb389ad0b9d976819ea6231f7bfb2ff258a7a46116a0e53ef3820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value)

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies how you are charged for read and write throughput and how you manage capacity. Valid values are:.

        - ``PAY_PER_REQUEST``
        - ``PROVISIONED``

        All replicas in your global table will have the same billing mode. If you use ``PROVISIONED`` billing mode, you must provide an auto scaling configuration via the ``WriteProvisionedThroughputSettings`` property. The default value of this property is ``PROVISIONED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-billingmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingMode"))

    @billing_mode.setter
    def billing_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6efc0baee2aa5341df4c9b7745e9054fe0a917625a9356223c71078d3b5be83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingMode", value)

    @builtins.property
    @jsii.member(jsii_name="globalSecondaryIndexes")
    def global_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.GlobalSecondaryIndexProperty", _IResolvable_a771d0ef]]]]:
        '''Global secondary indexes to be created on the global table.

        You can create up to 20 global secondary indexes. Each replica in your global table will have the same global secondary index settings. You can only create or delete one global secondary index in a single stack operation.

        Since the backfilling of an index could take a long time, CloudFormation does not wait for the index to become active. If a stack operation rolls back, CloudFormation might not delete an index that has been added. In that case, you will need to delete the index manually.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-globalsecondaryindexes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.GlobalSecondaryIndexProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "globalSecondaryIndexes"))

    @global_secondary_indexes.setter
    def global_secondary_indexes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.GlobalSecondaryIndexProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2478f9274ce4a7ab14835c6d24750a8c17a0b4d3ff2347cd333c0ee405eac56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalSecondaryIndexes", value)

    @builtins.property
    @jsii.member(jsii_name="localSecondaryIndexes")
    def local_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.LocalSecondaryIndexProperty", _IResolvable_a771d0ef]]]]:
        '''Local secondary indexes to be created on the table.

        You can create up to five local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes. Each replica in your global table will have the same local secondary index settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-localsecondaryindexes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.LocalSecondaryIndexProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "localSecondaryIndexes"))

    @local_secondary_indexes.setter
    def local_secondary_indexes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.LocalSecondaryIndexProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae009ce121eebd8aed0117f82d85b3e8de211d3020bf61526a556af2b252b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSecondaryIndexes", value)

    @builtins.property
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnGlobalTable.SSESpecificationProperty", _IResolvable_a771d0ef]]:
        '''Specifies the settings to enable server-side encryption.

        These settings will be applied to all replicas. If you plan to use customer-managed KMS keys, you must provide a key for each replica using the ``ReplicaSpecification.ReplicaSSESpecification`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-ssespecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.SSESpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseSpecification"))

    @sse_specification.setter
    def sse_specification(
        self,
        value: typing.Optional[typing.Union["CfnGlobalTable.SSESpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a2f40fd9b2aa40e87c338172d2e2fa8f55fc371ddaa51a12e30dc0292e6e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="streamSpecification")
    def stream_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnGlobalTable.StreamSpecificationProperty", _IResolvable_a771d0ef]]:
        '''Specifies the streams settings on your global table.

        You must provide a value for this property if your global table contains more than one replica. You can only change the streams settings if your global table has only one replica.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-streamspecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.StreamSpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "streamSpecification"))

    @stream_specification.setter
    def stream_specification(
        self,
        value: typing.Optional[typing.Union["CfnGlobalTable.StreamSpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed23fa6d569a437212b6bb12e9558cbbae2573d5f2b032c1d165e23bb940b7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        '''A name for the global table.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID as the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-tablename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b580c90602b438aaf5a3087527fbb06a308696ca83bb13a1850e7d5e5b9fe637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @builtins.property
    @jsii.member(jsii_name="timeToLiveSpecification")
    def time_to_live_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnGlobalTable.TimeToLiveSpecificationProperty", _IResolvable_a771d0ef]]:
        '''Specifies the time to live (TTL) settings for the table.

        This setting will be applied to all replicas.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-timetolivespecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.TimeToLiveSpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "timeToLiveSpecification"))

    @time_to_live_specification.setter
    def time_to_live_specification(
        self,
        value: typing.Optional[typing.Union["CfnGlobalTable.TimeToLiveSpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e496d8e393afef1b7683d9c8e8dc2504964d4a146d6fa117ea49b070180f20b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeToLiveSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="writeProvisionedThroughputSettings")
    def write_provisioned_throughput_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnGlobalTable.WriteProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]]:
        '''Specifies an auto scaling policy for write capacity.

        This policy will be applied to all replicas. This setting must be specified if ``BillingMode`` is set to ``PROVISIONED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-writeprovisionedthroughputsettings
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.WriteProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "writeProvisionedThroughputSettings"))

    @write_provisioned_throughput_settings.setter
    def write_provisioned_throughput_settings(
        self,
        value: typing.Optional[typing.Union["CfnGlobalTable.WriteProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dcfa7424cde69e61c8ddf4b4594568319da156ae7b2a0982224cb8dde4c1130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeProvisionedThroughputSettings", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.AttributeDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_type": "attributeType",
        },
    )
    class AttributeDefinitionProperty:
        def __init__(
            self,
            *,
            attribute_name: builtins.str,
            attribute_type: builtins.str,
        ) -> None:
            '''Represents an attribute for describing the key schema for the table and indexes.

            :param attribute_name: A name for the attribute.
            :param attribute_type: The data type for the attribute, where:. - ``S`` - the attribute is of type String - ``N`` - the attribute is of type Number - ``B`` - the attribute is of type Binary

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-attributedefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                attribute_definition_property = dynamodb.CfnGlobalTable.AttributeDefinitionProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8a37ead1c9c6ba599121eeebd25cbfc0d8cf9bb9a2e268c50b45516015ec676)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attribute_name": attribute_name,
                "attribute_type": attribute_type,
            }

        @builtins.property
        def attribute_name(self) -> builtins.str:
            '''A name for the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-attributedefinition.html#cfn-dynamodb-globaltable-attributedefinition-attributename
            '''
            result = self._values.get("attribute_name")
            assert result is not None, "Required property 'attribute_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def attribute_type(self) -> builtins.str:
            '''The data type for the attribute, where:.

            - ``S`` - the attribute is of type String
            - ``N`` - the attribute is of type Number
            - ``B`` - the attribute is of type Binary

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-attributedefinition.html#cfn-dynamodb-globaltable-attributedefinition-attributetype
            '''
            result = self._values.get("attribute_type")
            assert result is not None, "Required property 'attribute_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_capacity": "maxCapacity",
            "min_capacity": "minCapacity",
            "target_tracking_scaling_policy_configuration": "targetTrackingScalingPolicyConfiguration",
            "seed_capacity": "seedCapacity",
        },
    )
    class CapacityAutoScalingSettingsProperty:
        def __init__(
            self,
            *,
            max_capacity: jsii.Number,
            min_capacity: jsii.Number,
            target_tracking_scaling_policy_configuration: typing.Union[typing.Union["CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            seed_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configures a scalable target and an autoscaling policy for a table or global secondary index's read or write capacity.

            :param max_capacity: The maximum provisioned capacity units for the global table.
            :param min_capacity: The minimum provisioned capacity units for the global table.
            :param target_tracking_scaling_policy_configuration: Defines a target tracking scaling policy.
            :param seed_capacity: When switching billing mode from ``PAY_PER_REQUEST`` to ``PROVISIONED`` , DynamoDB requires you to specify read and write capacity unit values for the table and for each global secondary index. These values will be applied to all replicas. The table will use these provisioned values until CloudFormation creates the autoscaling policies you configured in your template. CloudFormation cannot determine what capacity the table and its global secondary indexes will require in this time period, since they are application-dependent. If you want to switch a table's billing mode from ``PAY_PER_REQUEST`` to ``PROVISIONED`` , you must specify a value for this property for each autoscaled resource. If you specify different values for the same resource in different regions, CloudFormation will use the highest value found in either the ``SeedCapacity`` or ``ReadCapacityUnits`` properties. For example, if your global secondary index ``myGSI`` has a ``SeedCapacity`` of 10 in us-east-1 and a fixed ``ReadCapacityUnits`` of 20 in eu-west-1, CloudFormation will initially set the read capacity for ``myGSI`` to 20. Note that if you disable ``ScaleIn`` for ``myGSI`` in us-east-1, its read capacity units might not be set back to 10. You must also specify a value for ``SeedCapacity`` when you plan to switch a table's billing mode from ``PROVISIONED`` to ``PAY_PER_REQUEST`` , because CloudFormation might need to roll back the operation (reverting the billing mode to ``PROVISIONED`` ) and this cannot succeed without specifying a value for ``SeedCapacity`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                capacity_auto_scaling_settings_property = dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                    max_capacity=123,
                    min_capacity=123,
                    target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                        target_value=123,
                
                        # the properties below are optional
                        disable_scale_in=False,
                        scale_in_cooldown=123,
                        scale_out_cooldown=123
                    ),
                
                    # the properties below are optional
                    seed_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fcf57773cc4fd4d20db865a5ec5577bc5536def8ccbc720f4de0851d10aece6)
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
                check_type(argname="argument target_tracking_scaling_policy_configuration", value=target_tracking_scaling_policy_configuration, expected_type=type_hints["target_tracking_scaling_policy_configuration"])
                check_type(argname="argument seed_capacity", value=seed_capacity, expected_type=type_hints["seed_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "max_capacity": max_capacity,
                "min_capacity": min_capacity,
                "target_tracking_scaling_policy_configuration": target_tracking_scaling_policy_configuration,
            }
            if seed_capacity is not None:
                self._values["seed_capacity"] = seed_capacity

        @builtins.property
        def max_capacity(self) -> jsii.Number:
            '''The maximum provisioned capacity units for the global table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html#cfn-dynamodb-globaltable-capacityautoscalingsettings-maxcapacity
            '''
            result = self._values.get("max_capacity")
            assert result is not None, "Required property 'max_capacity' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def min_capacity(self) -> jsii.Number:
            '''The minimum provisioned capacity units for the global table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html#cfn-dynamodb-globaltable-capacityautoscalingsettings-mincapacity
            '''
            result = self._values.get("min_capacity")
            assert result is not None, "Required property 'min_capacity' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def target_tracking_scaling_policy_configuration(
            self,
        ) -> typing.Union["CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty", _IResolvable_a771d0ef]:
            '''Defines a target tracking scaling policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html#cfn-dynamodb-globaltable-capacityautoscalingsettings-targettrackingscalingpolicyconfiguration
            '''
            result = self._values.get("target_tracking_scaling_policy_configuration")
            assert result is not None, "Required property 'target_tracking_scaling_policy_configuration' is missing"
            return typing.cast(typing.Union["CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def seed_capacity(self) -> typing.Optional[jsii.Number]:
            '''When switching billing mode from ``PAY_PER_REQUEST`` to ``PROVISIONED`` , DynamoDB requires you to specify read and write capacity unit values for the table and for each global secondary index.

            These values will be applied to all replicas. The table will use these provisioned values until CloudFormation creates the autoscaling policies you configured in your template. CloudFormation cannot determine what capacity the table and its global secondary indexes will require in this time period, since they are application-dependent.

            If you want to switch a table's billing mode from ``PAY_PER_REQUEST`` to ``PROVISIONED`` , you must specify a value for this property for each autoscaled resource. If you specify different values for the same resource in different regions, CloudFormation will use the highest value found in either the ``SeedCapacity`` or ``ReadCapacityUnits`` properties. For example, if your global secondary index ``myGSI`` has a ``SeedCapacity`` of 10 in us-east-1 and a fixed ``ReadCapacityUnits`` of 20 in eu-west-1, CloudFormation will initially set the read capacity for ``myGSI`` to 20. Note that if you disable ``ScaleIn`` for ``myGSI`` in us-east-1, its read capacity units might not be set back to 10.

            You must also specify a value for ``SeedCapacity`` when you plan to switch a table's billing mode from ``PROVISIONED`` to ``PAY_PER_REQUEST`` , because CloudFormation might need to roll back the operation (reverting the billing mode to ``PROVISIONED`` ) and this cannot succeed without specifying a value for ``SeedCapacity`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-capacityautoscalingsettings.html#cfn-dynamodb-globaltable-capacityautoscalingsettings-seedcapacity
            '''
            result = self._values.get("seed_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityAutoScalingSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class ContributorInsightsSpecificationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''Configures contributor insights settings for a replica or one of its indexes.

            :param enabled: Indicates whether CloudWatch Contributor Insights are to be enabled (true) or disabled (false).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-contributorinsightsspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                contributor_insights_specification_property = dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__909baaf0655c8cd7d7c9db8c52aac90d9a2fb28008905cbce16f74e8a536d32f)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Indicates whether CloudWatch Contributor Insights are to be enabled (true) or disabled (false).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-contributorinsightsspecification.html#cfn-dynamodb-globaltable-contributorinsightsspecification-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContributorInsightsSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.GlobalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
            "write_provisioned_throughput_settings": "writeProvisionedThroughputSettings",
        },
    )
    class GlobalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: builtins.str,
            key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalTable.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            projection: typing.Union[typing.Union["CfnGlobalTable.ProjectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            write_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.WriteProvisionedThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Allows you to specify a global secondary index for the global table.

            The index will be defined on all replicas.

            :param index_name: The name of the global secondary index. The name must be unique among all other indexes on this table.
            :param key_schema: The complete key schema for a global secondary index, which consists of one or more pairs of attribute names and key types: - ``HASH`` - partition key - ``RANGE`` - sort key > The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. .. epigraph:: The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.
            :param projection: Represents attributes that are copied (projected) from the table into the global secondary index. These are in addition to the primary key attributes and index key attributes, which are automatically projected.
            :param write_provisioned_throughput_settings: Defines write capacity settings for the global secondary index. You must specify a value for this property if the table's ``BillingMode`` is ``PROVISIONED`` . All replicas will have the same write capacity settings for this global secondary index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                global_secondary_index_property = dynamodb.CfnGlobalTable.GlobalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb.CfnGlobalTable.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb.CfnGlobalTable.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    ),
                
                    # the properties below are optional
                    write_provisioned_throughput_settings=dynamodb.CfnGlobalTable.WriteProvisionedThroughputSettingsProperty(
                        write_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                                target_value=123,
                
                                # the properties below are optional
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123
                            ),
                
                            # the properties below are optional
                            seed_capacity=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6d2a1270d054d7667312c4fb83f1e4e6a39a3be162ed778dff5febe59661860)
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
                check_type(argname="argument projection", value=projection, expected_type=type_hints["projection"])
                check_type(argname="argument write_provisioned_throughput_settings", value=write_provisioned_throughput_settings, expected_type=type_hints["write_provisioned_throughput_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "index_name": index_name,
                "key_schema": key_schema,
                "projection": projection,
            }
            if write_provisioned_throughput_settings is not None:
                self._values["write_provisioned_throughput_settings"] = write_provisioned_throughput_settings

        @builtins.property
        def index_name(self) -> builtins.str:
            '''The name of the global secondary index.

            The name must be unique among all other indexes on this table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-indexname
            '''
            result = self._values.get("index_name")
            assert result is not None, "Required property 'index_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.KeySchemaProperty", _IResolvable_a771d0ef]]]:
            '''The complete key schema for a global secondary index, which consists of one or more pairs of attribute names and key types:  - ``HASH`` - partition key - ``RANGE`` - sort key  > The partition key of an item is also known as its *hash attribute* .

            The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.
            .. epigraph::

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-keyschema
            '''
            result = self._values.get("key_schema")
            assert result is not None, "Required property 'key_schema' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.KeySchemaProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def projection(
            self,
        ) -> typing.Union["CfnGlobalTable.ProjectionProperty", _IResolvable_a771d0ef]:
            '''Represents attributes that are copied (projected) from the table into the global secondary index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-projection
            '''
            result = self._values.get("projection")
            assert result is not None, "Required property 'projection' is missing"
            return typing.cast(typing.Union["CfnGlobalTable.ProjectionProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def write_provisioned_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.WriteProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]]:
            '''Defines write capacity settings for the global secondary index.

            You must specify a value for this property if the table's ``BillingMode`` is ``PROVISIONED`` . All replicas will have the same write capacity settings for this global secondary index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-globalsecondaryindex.html#cfn-dynamodb-globaltable-globalsecondaryindex-writeprovisionedthroughputsettings
            '''
            result = self._values.get("write_provisioned_throughput_settings")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.WriteProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.KeySchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "key_type": "keyType"},
    )
    class KeySchemaProperty:
        def __init__(
            self,
            *,
            attribute_name: builtins.str,
            key_type: builtins.str,
        ) -> None:
            '''Represents *a single element* of a key schema.

            A key schema specifies the attributes that make up the primary key of a table, or the key attributes of an index.

            A ``KeySchemaElement`` represents exactly one attribute of the primary key. For example, a simple primary key would be represented by one ``KeySchemaElement`` (for the partition key). A composite primary key would require one ``KeySchemaElement`` for the partition key, and another ``KeySchemaElement`` for the sort key.

            A ``KeySchemaElement`` must be a scalar, top-level attribute (not a nested attribute). The data type must be one of String, Number, or Binary. The attribute cannot be nested within a List or a Map.

            :param attribute_name: The name of a key attribute.
            :param key_type: The role that this key attribute will assume:. - ``HASH`` - partition key - ``RANGE`` - sort key .. epigraph:: The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-keyschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                key_schema_property = dynamodb.CfnGlobalTable.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c91f0abf47628c0b91309cddfa931146d5b3cddd46f7e0157c0801e0824b155f)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attribute_name": attribute_name,
                "key_type": key_type,
            }

        @builtins.property
        def attribute_name(self) -> builtins.str:
            '''The name of a key attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-keyschema.html#cfn-dynamodb-globaltable-keyschema-attributename
            '''
            result = self._values.get("attribute_name")
            assert result is not None, "Required property 'attribute_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_type(self) -> builtins.str:
            '''The role that this key attribute will assume:.

            - ``HASH`` - partition key
            - ``RANGE`` - sort key

            .. epigraph::

               The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-keyschema.html#cfn-dynamodb-globaltable-keyschema-keytype
            '''
            result = self._values.get("key_type")
            assert result is not None, "Required property 'key_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.KinesisStreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_arn": "streamArn"},
    )
    class KinesisStreamSpecificationProperty:
        def __init__(self, *, stream_arn: builtins.str) -> None:
            '''The Kinesis Data Streams configuration for the specified global table replica.

            :param stream_arn: The ARN for a specific Kinesis data stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-kinesisstreamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                kinesis_stream_specification_property = dynamodb.CfnGlobalTable.KinesisStreamSpecificationProperty(
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d84ce952ed9b4a9e80736b02634bbbacf3d01b042614641e0cea68781cd1348)
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_arn": stream_arn,
            }

        @builtins.property
        def stream_arn(self) -> builtins.str:
            '''The ARN for a specific Kinesis data stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-kinesisstreamspecification.html#cfn-dynamodb-globaltable-kinesisstreamspecification-streamarn
            '''
            result = self._values.get("stream_arn")
            assert result is not None, "Required property 'stream_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.LocalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
        },
    )
    class LocalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: builtins.str,
            key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalTable.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            projection: typing.Union[typing.Union["CfnGlobalTable.ProjectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Represents the properties of a local secondary index.

            A local secondary index can only be created when its parent table is created.

            :param index_name: The name of the local secondary index. The name must be unique among all other indexes on this table.
            :param key_schema: The complete key schema for the local secondary index, consisting of one or more pairs of attribute names and key types: - ``HASH`` - partition key - ``RANGE`` - sort key > The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. .. epigraph:: The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.
            :param projection: Represents attributes that are copied (projected) from the table into the local secondary index. These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-localsecondaryindex.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                local_secondary_index_property = dynamodb.CfnGlobalTable.LocalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb.CfnGlobalTable.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb.CfnGlobalTable.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d85b8871429ee864b365f5e68edb2be0686e51a559e0487e54183a7d022936ad)
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
                check_type(argname="argument projection", value=projection, expected_type=type_hints["projection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "index_name": index_name,
                "key_schema": key_schema,
                "projection": projection,
            }

        @builtins.property
        def index_name(self) -> builtins.str:
            '''The name of the local secondary index.

            The name must be unique among all other indexes on this table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-localsecondaryindex.html#cfn-dynamodb-globaltable-localsecondaryindex-indexname
            '''
            result = self._values.get("index_name")
            assert result is not None, "Required property 'index_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.KeySchemaProperty", _IResolvable_a771d0ef]]]:
            '''The complete key schema for the local secondary index, consisting of one or more pairs of attribute names and key types:  - ``HASH`` - partition key - ``RANGE`` - sort key  > The partition key of an item is also known as its *hash attribute* .

            The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.
            .. epigraph::

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-localsecondaryindex.html#cfn-dynamodb-globaltable-localsecondaryindex-keyschema
            '''
            result = self._values.get("key_schema")
            assert result is not None, "Required property 'key_schema' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.KeySchemaProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def projection(
            self,
        ) -> typing.Union["CfnGlobalTable.ProjectionProperty", _IResolvable_a771d0ef]:
            '''Represents attributes that are copied (projected) from the table into the local secondary index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-localsecondaryindex.html#cfn-dynamodb-globaltable-localsecondaryindex-projection
            '''
            result = self._values.get("projection")
            assert result is not None, "Required property 'projection' is missing"
            return typing.cast(typing.Union["CfnGlobalTable.ProjectionProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.PointInTimeRecoverySpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"point_in_time_recovery_enabled": "pointInTimeRecoveryEnabled"},
    )
    class PointInTimeRecoverySpecificationProperty:
        def __init__(
            self,
            *,
            point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Represents the settings used to enable point in time recovery.

            :param point_in_time_recovery_enabled: Indicates whether point in time recovery is enabled (true) or disabled (false) on the table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-pointintimerecoveryspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                point_in_time_recovery_specification_property = dynamodb.CfnGlobalTable.PointInTimeRecoverySpecificationProperty(
                    point_in_time_recovery_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__165c6e0baaaa0dcbd41e473e6033d59fa7e20b2e28af25301745498b70e20e99)
                check_type(argname="argument point_in_time_recovery_enabled", value=point_in_time_recovery_enabled, expected_type=type_hints["point_in_time_recovery_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if point_in_time_recovery_enabled is not None:
                self._values["point_in_time_recovery_enabled"] = point_in_time_recovery_enabled

        @builtins.property
        def point_in_time_recovery_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether point in time recovery is enabled (true) or disabled (false) on the table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-pointintimerecoveryspecification.html#cfn-dynamodb-globaltable-pointintimerecoveryspecification-pointintimerecoveryenabled
            '''
            result = self._values.get("point_in_time_recovery_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PointInTimeRecoverySpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.ProjectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "non_key_attributes": "nonKeyAttributes",
            "projection_type": "projectionType",
        },
    )
    class ProjectionProperty:
        def __init__(
            self,
            *,
            non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
            projection_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents attributes that are copied (projected) from the table into an index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :param non_key_attributes: Represents the non-key attribute names which will be projected into the index. For local secondary indexes, the total count of ``NonKeyAttributes`` summed across all of the local secondary indexes, must not exceed 100. If you project the same attribute into two different indexes, this counts as two distinct attributes when determining the total.
            :param projection_type: The set of attributes that are projected into the index:. - ``KEYS_ONLY`` - Only the index and primary keys are projected into the index. - ``INCLUDE`` - In addition to the attributes described in ``KEYS_ONLY`` , the secondary index will include other non-key attributes that you specify. - ``ALL`` - All of the table attributes are projected into the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-projection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                projection_property = dynamodb.CfnGlobalTable.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9f57925ff29b6ddd938306497d6eff6be463e8490a416c19943e761a4b3490d)
                check_type(argname="argument non_key_attributes", value=non_key_attributes, expected_type=type_hints["non_key_attributes"])
                check_type(argname="argument projection_type", value=projection_type, expected_type=type_hints["projection_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if non_key_attributes is not None:
                self._values["non_key_attributes"] = non_key_attributes
            if projection_type is not None:
                self._values["projection_type"] = projection_type

        @builtins.property
        def non_key_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents the non-key attribute names which will be projected into the index.

            For local secondary indexes, the total count of ``NonKeyAttributes`` summed across all of the local secondary indexes, must not exceed 100. If you project the same attribute into two different indexes, this counts as two distinct attributes when determining the total.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-projection.html#cfn-dynamodb-globaltable-projection-nonkeyattributes
            '''
            result = self._values.get("non_key_attributes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def projection_type(self) -> typing.Optional[builtins.str]:
            '''The set of attributes that are projected into the index:.

            - ``KEYS_ONLY`` - Only the index and primary keys are projected into the index.
            - ``INCLUDE`` - In addition to the attributes described in ``KEYS_ONLY`` , the secondary index will include other non-key attributes that you specify.
            - ``ALL`` - All of the table attributes are projected into the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-projection.html#cfn-dynamodb-globaltable-projection-projectiontype
            '''
            result = self._values.get("projection_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_capacity_auto_scaling_settings": "readCapacityAutoScalingSettings",
            "read_capacity_units": "readCapacityUnits",
        },
    )
    class ReadProvisionedThroughputSettingsProperty:
        def __init__(
            self,
            *,
            read_capacity_auto_scaling_settings: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.CapacityAutoScalingSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            read_capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Allows you to specify the read capacity settings for a replica table or a replica global secondary index when the ``BillingMode`` is set to ``PROVISIONED`` .

            You must specify a value for either ``ReadCapacityUnits`` or ``ReadCapacityAutoScalingSettings`` , but not both. You can switch between fixed capacity and auto scaling.

            :param read_capacity_auto_scaling_settings: Specifies auto scaling settings for the replica table or global secondary index.
            :param read_capacity_units: Specifies a fixed read capacity for the replica table or global secondary index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-readprovisionedthroughputsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                read_provisioned_throughput_settings_property = dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty(
                    read_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                            target_value=123,
                
                            # the properties below are optional
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123
                        ),
                
                        # the properties below are optional
                        seed_capacity=123
                    ),
                    read_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7d158d665c80e66da0c4967725ab33811ac7669debf35586c66c3de7f96cb17)
                check_type(argname="argument read_capacity_auto_scaling_settings", value=read_capacity_auto_scaling_settings, expected_type=type_hints["read_capacity_auto_scaling_settings"])
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_capacity_auto_scaling_settings is not None:
                self._values["read_capacity_auto_scaling_settings"] = read_capacity_auto_scaling_settings
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units

        @builtins.property
        def read_capacity_auto_scaling_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.CapacityAutoScalingSettingsProperty", _IResolvable_a771d0ef]]:
            '''Specifies auto scaling settings for the replica table or global secondary index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-readprovisionedthroughputsettings.html#cfn-dynamodb-globaltable-readprovisionedthroughputsettings-readcapacityautoscalingsettings
            '''
            result = self._values.get("read_capacity_auto_scaling_settings")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.CapacityAutoScalingSettingsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''Specifies a fixed read capacity for the replica table or global secondary index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-readprovisionedthroughputsettings.html#cfn-dynamodb-globaltable-readprovisionedthroughputsettings-readcapacityunits
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadProvisionedThroughputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "contributor_insights_specification": "contributorInsightsSpecification",
            "read_provisioned_throughput_settings": "readProvisionedThroughputSettings",
        },
    )
    class ReplicaGlobalSecondaryIndexSpecificationProperty:
        def __init__(
            self,
            *,
            index_name: builtins.str,
            contributor_insights_specification: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.ContributorInsightsSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            read_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.ReadProvisionedThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Represents the properties of a global secondary index that can be set on a per-replica basis.

            :param index_name: The name of the global secondary index. The name must be unique among all other indexes on this table.
            :param contributor_insights_specification: Updates the status for contributor insights for a specific table or index. CloudWatch Contributor Insights for DynamoDB graphs display the partition key and (if applicable) sort key of frequently accessed items and frequently throttled items in plaintext. If you require the use of AWS Key Management Service (KMS) to encrypt this table’s partition key and sort key data with an AWS managed key or customer managed key, you should not enable CloudWatch Contributor Insights for DynamoDB for this table.
            :param read_provisioned_throughput_settings: Allows you to specify the read capacity settings for a replica global secondary index when the ``BillingMode`` is set to ``PROVISIONED`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                replica_global_secondary_index_specification_property = dynamodb.CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty(
                    index_name="indexName",
                
                    # the properties below are optional
                    contributor_insights_specification=dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty(
                        enabled=False
                    ),
                    read_provisioned_throughput_settings=dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty(
                        read_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                                target_value=123,
                
                                # the properties below are optional
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123
                            ),
                
                            # the properties below are optional
                            seed_capacity=123
                        ),
                        read_capacity_units=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6946430e1f985786a9ea4a350a72a2bd07244ea6ff1b64649aaf834cca6d65d)
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument contributor_insights_specification", value=contributor_insights_specification, expected_type=type_hints["contributor_insights_specification"])
                check_type(argname="argument read_provisioned_throughput_settings", value=read_provisioned_throughput_settings, expected_type=type_hints["read_provisioned_throughput_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "index_name": index_name,
            }
            if contributor_insights_specification is not None:
                self._values["contributor_insights_specification"] = contributor_insights_specification
            if read_provisioned_throughput_settings is not None:
                self._values["read_provisioned_throughput_settings"] = read_provisioned_throughput_settings

        @builtins.property
        def index_name(self) -> builtins.str:
            '''The name of the global secondary index.

            The name must be unique among all other indexes on this table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html#cfn-dynamodb-globaltable-replicaglobalsecondaryindexspecification-indexname
            '''
            result = self._values.get("index_name")
            assert result is not None, "Required property 'index_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def contributor_insights_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]]:
            '''Updates the status for contributor insights for a specific table or index.

            CloudWatch Contributor Insights for DynamoDB graphs display the partition key and (if applicable) sort key of frequently accessed items and frequently throttled items in plaintext. If you require the use of AWS Key Management Service (KMS) to encrypt this table’s partition key and sort key data with an AWS managed key or customer managed key, you should not enable CloudWatch Contributor Insights for DynamoDB for this table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html#cfn-dynamodb-globaltable-replicaglobalsecondaryindexspecification-contributorinsightsspecification
            '''
            result = self._values.get("contributor_insights_specification")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def read_provisioned_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.ReadProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]]:
            '''Allows you to specify the read capacity settings for a replica global secondary index when the ``BillingMode`` is set to ``PROVISIONED`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaglobalsecondaryindexspecification.html#cfn-dynamodb-globaltable-replicaglobalsecondaryindexspecification-readprovisionedthroughputsettings
            '''
            result = self._values.get("read_provisioned_throughput_settings")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.ReadProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaGlobalSecondaryIndexSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.ReplicaSSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_master_key_id": "kmsMasterKeyId"},
    )
    class ReplicaSSESpecificationProperty:
        def __init__(self, *, kms_master_key_id: builtins.str) -> None:
            '''Allows you to specify a KMS key identifier to be used for server-side encryption.

            The key can be specified via ARN, key ID, or alias. The key must be created in the same region as the replica.

            :param kms_master_key_id: The AWS KMS key that should be used for the AWS KMS encryption. To specify a key, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter if the key is different from the default DynamoDB key ``alias/aws/dynamodb`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicassespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                replica_sSESpecification_property = dynamodb.CfnGlobalTable.ReplicaSSESpecificationProperty(
                    kms_master_key_id="kmsMasterKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9bf1ebc7fc9f32960697b047a7757a342a5befe96061784aeef4097dcae41d7)
                check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "kms_master_key_id": kms_master_key_id,
            }

        @builtins.property
        def kms_master_key_id(self) -> builtins.str:
            '''The AWS KMS key that should be used for the AWS KMS encryption.

            To specify a key, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter if the key is different from the default DynamoDB key ``alias/aws/dynamodb`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicassespecification.html#cfn-dynamodb-globaltable-replicassespecification-kmsmasterkeyid
            '''
            result = self._values.get("kms_master_key_id")
            assert result is not None, "Required property 'kms_master_key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaSSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.ReplicaSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "region": "region",
            "contributor_insights_specification": "contributorInsightsSpecification",
            "deletion_protection_enabled": "deletionProtectionEnabled",
            "global_secondary_indexes": "globalSecondaryIndexes",
            "kinesis_stream_specification": "kinesisStreamSpecification",
            "point_in_time_recovery_specification": "pointInTimeRecoverySpecification",
            "read_provisioned_throughput_settings": "readProvisionedThroughputSettings",
            "sse_specification": "sseSpecification",
            "table_class": "tableClass",
            "tags": "tags",
        },
    )
    class ReplicaSpecificationProperty:
        def __init__(
            self,
            *,
            region: builtins.str,
            contributor_insights_specification: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.ContributorInsightsSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            kinesis_stream_specification: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.KinesisStreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            point_in_time_recovery_specification: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.PointInTimeRecoverySpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            read_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.ReadProvisionedThroughputSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sse_specification: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.ReplicaSSESpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            table_class: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines settings specific to a single replica of a global table.

            :param region: The region in which this replica exists.
            :param contributor_insights_specification: The settings used to enable or disable CloudWatch Contributor Insights for the specified replica. When not specified, defaults to contributor insights disabled for the replica.
            :param deletion_protection_enabled: Determines if a replica is protected from deletion. When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .
            :param global_secondary_indexes: Defines additional settings for the global secondary indexes of this replica.
            :param kinesis_stream_specification: Defines the Kinesis Data Streams configuration for the specified replica.
            :param point_in_time_recovery_specification: The settings used to enable point in time recovery. When not specified, defaults to point in time recovery disabled for the replica.
            :param read_provisioned_throughput_settings: Defines read capacity settings for the replica table.
            :param sse_specification: Allows you to specify a customer-managed key for the replica. When using customer-managed keys for server-side encryption, this property must have a value in all replicas.
            :param table_class: The table class of the specified table. Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .
            :param tags: An array of key-value pairs to apply to this replica. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                replica_specification_property = dynamodb.CfnGlobalTable.ReplicaSpecificationProperty(
                    region="region",
                
                    # the properties below are optional
                    contributor_insights_specification=dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty(
                        enabled=False
                    ),
                    deletion_protection_enabled=False,
                    global_secondary_indexes=[dynamodb.CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty(
                        index_name="indexName",
                
                        # the properties below are optional
                        contributor_insights_specification=dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty(
                            enabled=False
                        ),
                        read_provisioned_throughput_settings=dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty(
                            read_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                                max_capacity=123,
                                min_capacity=123,
                                target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                                    target_value=123,
                
                                    # the properties below are optional
                                    disable_scale_in=False,
                                    scale_in_cooldown=123,
                                    scale_out_cooldown=123
                                ),
                
                                # the properties below are optional
                                seed_capacity=123
                            ),
                            read_capacity_units=123
                        )
                    )],
                    kinesis_stream_specification=dynamodb.CfnGlobalTable.KinesisStreamSpecificationProperty(
                        stream_arn="streamArn"
                    ),
                    point_in_time_recovery_specification=dynamodb.CfnGlobalTable.PointInTimeRecoverySpecificationProperty(
                        point_in_time_recovery_enabled=False
                    ),
                    read_provisioned_throughput_settings=dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty(
                        read_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                                target_value=123,
                
                                # the properties below are optional
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123
                            ),
                
                            # the properties below are optional
                            seed_capacity=123
                        ),
                        read_capacity_units=123
                    ),
                    sse_specification=dynamodb.CfnGlobalTable.ReplicaSSESpecificationProperty(
                        kms_master_key_id="kmsMasterKeyId"
                    ),
                    table_class="tableClass",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67a5869029b02679d4f1087f08eaedbb43dd60d8a3fef4ca87fdf9b38d052195)
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument contributor_insights_specification", value=contributor_insights_specification, expected_type=type_hints["contributor_insights_specification"])
                check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
                check_type(argname="argument global_secondary_indexes", value=global_secondary_indexes, expected_type=type_hints["global_secondary_indexes"])
                check_type(argname="argument kinesis_stream_specification", value=kinesis_stream_specification, expected_type=type_hints["kinesis_stream_specification"])
                check_type(argname="argument point_in_time_recovery_specification", value=point_in_time_recovery_specification, expected_type=type_hints["point_in_time_recovery_specification"])
                check_type(argname="argument read_provisioned_throughput_settings", value=read_provisioned_throughput_settings, expected_type=type_hints["read_provisioned_throughput_settings"])
                check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
                check_type(argname="argument table_class", value=table_class, expected_type=type_hints["table_class"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "region": region,
            }
            if contributor_insights_specification is not None:
                self._values["contributor_insights_specification"] = contributor_insights_specification
            if deletion_protection_enabled is not None:
                self._values["deletion_protection_enabled"] = deletion_protection_enabled
            if global_secondary_indexes is not None:
                self._values["global_secondary_indexes"] = global_secondary_indexes
            if kinesis_stream_specification is not None:
                self._values["kinesis_stream_specification"] = kinesis_stream_specification
            if point_in_time_recovery_specification is not None:
                self._values["point_in_time_recovery_specification"] = point_in_time_recovery_specification
            if read_provisioned_throughput_settings is not None:
                self._values["read_provisioned_throughput_settings"] = read_provisioned_throughput_settings
            if sse_specification is not None:
                self._values["sse_specification"] = sse_specification
            if table_class is not None:
                self._values["table_class"] = table_class
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def region(self) -> builtins.str:
            '''The region in which this replica exists.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-region
            '''
            result = self._values.get("region")
            assert result is not None, "Required property 'region' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def contributor_insights_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]]:
            '''The settings used to enable or disable CloudWatch Contributor Insights for the specified replica.

            When not specified, defaults to contributor insights disabled for the replica.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-contributorinsightsspecification
            '''
            result = self._values.get("contributor_insights_specification")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def deletion_protection_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Determines if a replica is protected from deletion.

            When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-deletionprotectionenabled
            '''
            result = self._values.get("deletion_protection_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def global_secondary_indexes(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty", _IResolvable_a771d0ef]]]]:
            '''Defines additional settings for the global secondary indexes of this replica.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-globalsecondaryindexes
            '''
            result = self._values.get("global_secondary_indexes")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def kinesis_stream_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.KinesisStreamSpecificationProperty", _IResolvable_a771d0ef]]:
            '''Defines the Kinesis Data Streams configuration for the specified replica.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-kinesisstreamspecification
            '''
            result = self._values.get("kinesis_stream_specification")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.KinesisStreamSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def point_in_time_recovery_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.PointInTimeRecoverySpecificationProperty", _IResolvable_a771d0ef]]:
            '''The settings used to enable point in time recovery.

            When not specified, defaults to point in time recovery disabled for the replica.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-pointintimerecoveryspecification
            '''
            result = self._values.get("point_in_time_recovery_specification")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.PointInTimeRecoverySpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def read_provisioned_throughput_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.ReadProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]]:
            '''Defines read capacity settings for the replica table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-readprovisionedthroughputsettings
            '''
            result = self._values.get("read_provisioned_throughput_settings")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.ReadProvisionedThroughputSettingsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sse_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.ReplicaSSESpecificationProperty", _IResolvable_a771d0ef]]:
            '''Allows you to specify a customer-managed key for the replica.

            When using customer-managed keys for server-side encryption, this property must have a value in all replicas.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-ssespecification
            '''
            result = self._values.get("sse_specification")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.ReplicaSSESpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def table_class(self) -> typing.Optional[builtins.str]:
            '''The table class of the specified table.

            Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-tableclass
            '''
            result = self._values.get("table_class")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
            '''An array of key-value pairs to apply to this replica.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled", "sse_type": "sseType"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            sse_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the settings used to enable server-side encryption.

            :param sse_enabled: Indicates whether server-side encryption is performed using an AWS managed key or an AWS owned key. If enabled (true), server-side encryption type is set to KMS and an AWS managed key is used ( AWS KMS charges apply). If disabled (false) or not specified,server-side encryption is set to an AWS owned key. If you choose to use KMS encryption, you can also use customer managed KMS keys by specifying them in the ``ReplicaSpecification.SSESpecification`` object. You cannot mix AWS managed and customer managed KMS keys.
            :param sse_type: Server-side encryption type. The only supported value is:. - ``KMS`` - Server-side encryption that uses AWS Key Management Service . The key is stored in your account and is managed by AWS KMS ( AWS KMS charges apply).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                s_sESpecification_property = dynamodb.CfnGlobalTable.SSESpecificationProperty(
                    sse_enabled=False,
                
                    # the properties below are optional
                    sse_type="sseType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6e716e476896f0940a9b5354c21cc0dee07d5ec08f3fec8d08ff4725c80743d)
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
                check_type(argname="argument sse_type", value=sse_type, expected_type=type_hints["sse_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "sse_enabled": sse_enabled,
            }
            if sse_type is not None:
                self._values["sse_type"] = sse_type

        @builtins.property
        def sse_enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Indicates whether server-side encryption is performed using an AWS managed key or an AWS owned key.

            If enabled (true), server-side encryption type is set to KMS and an AWS managed key is used ( AWS KMS charges apply). If disabled (false) or not specified,server-side encryption is set to an AWS owned key. If you choose to use KMS encryption, you can also use customer managed KMS keys by specifying them in the ``ReplicaSpecification.SSESpecification`` object. You cannot mix AWS managed and customer managed KMS keys.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-ssespecification.html#cfn-dynamodb-globaltable-ssespecification-sseenabled
            '''
            result = self._values.get("sse_enabled")
            assert result is not None, "Required property 'sse_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def sse_type(self) -> typing.Optional[builtins.str]:
            '''Server-side encryption type. The only supported value is:.

            - ``KMS`` - Server-side encryption that uses AWS Key Management Service . The key is stored in your account and is managed by AWS KMS ( AWS KMS charges apply).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-ssespecification.html#cfn-dynamodb-globaltable-ssespecification-ssetype
            '''
            result = self._values.get("sse_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.StreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_view_type": "streamViewType"},
    )
    class StreamSpecificationProperty:
        def __init__(self, *, stream_view_type: builtins.str) -> None:
            '''Represents the DynamoDB Streams configuration for a table in DynamoDB.

            You can only modify this value if your ``AWS::DynamoDB::GlobalTable`` contains only one entry in ``Replicas`` . You must specify a value for this property if your ``AWS::DynamoDB::GlobalTable`` contains more than one replica.

            :param stream_view_type: When an item in the table is modified, ``StreamViewType`` determines what information is written to the stream for this table. Valid values for ``StreamViewType`` are: - ``KEYS_ONLY`` - Only the key attributes of the modified item are written to the stream. - ``NEW_IMAGE`` - The entire item, as it appears after it was modified, is written to the stream. - ``OLD_IMAGE`` - The entire item, as it appeared before it was modified, is written to the stream. - ``NEW_AND_OLD_IMAGES`` - Both the new and the old item images of the item are written to the stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-streamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                stream_specification_property = dynamodb.CfnGlobalTable.StreamSpecificationProperty(
                    stream_view_type="streamViewType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c56c9f1d49878069057c8d58f23c9c7bda820a349951193c7046e4d1cb865551)
                check_type(argname="argument stream_view_type", value=stream_view_type, expected_type=type_hints["stream_view_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_view_type": stream_view_type,
            }

        @builtins.property
        def stream_view_type(self) -> builtins.str:
            '''When an item in the table is modified, ``StreamViewType`` determines what information is written to the stream for this table.

            Valid values for ``StreamViewType`` are:

            - ``KEYS_ONLY`` - Only the key attributes of the modified item are written to the stream.
            - ``NEW_IMAGE`` - The entire item, as it appears after it was modified, is written to the stream.
            - ``OLD_IMAGE`` - The entire item, as it appeared before it was modified, is written to the stream.
            - ``NEW_AND_OLD_IMAGES`` - Both the new and the old item images of the item are written to the stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-streamspecification.html#cfn-dynamodb-globaltable-streamspecification-streamviewtype
            '''
            result = self._values.get("stream_view_type")
            assert result is not None, "Required property 'stream_view_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_value": "targetValue",
            "disable_scale_in": "disableScaleIn",
            "scale_in_cooldown": "scaleInCooldown",
            "scale_out_cooldown": "scaleOutCooldown",
        },
    )
    class TargetTrackingScalingPolicyConfigurationProperty:
        def __init__(
            self,
            *,
            target_value: jsii.Number,
            disable_scale_in: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            scale_in_cooldown: typing.Optional[jsii.Number] = None,
            scale_out_cooldown: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines a target tracking scaling policy.

            :param target_value: Defines a target value for the scaling policy.
            :param disable_scale_in: Indicates whether scale in by the target tracking scaling policy is disabled. The default value is ``false`` .
            :param scale_in_cooldown: The amount of time, in seconds, after a scale-in activity completes before another scale-in activity can start.
            :param scale_out_cooldown: The amount of time, in seconds, after a scale-out activity completes before another scale-out activity can start.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                target_tracking_scaling_policy_configuration_property = dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                    target_value=123,
                
                    # the properties below are optional
                    disable_scale_in=False,
                    scale_in_cooldown=123,
                    scale_out_cooldown=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65047cc14f31b8f45c1f4e553ba54123080aa2bb64019097b878d33591b944db)
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
                check_type(argname="argument disable_scale_in", value=disable_scale_in, expected_type=type_hints["disable_scale_in"])
                check_type(argname="argument scale_in_cooldown", value=scale_in_cooldown, expected_type=type_hints["scale_in_cooldown"])
                check_type(argname="argument scale_out_cooldown", value=scale_out_cooldown, expected_type=type_hints["scale_out_cooldown"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_value": target_value,
            }
            if disable_scale_in is not None:
                self._values["disable_scale_in"] = disable_scale_in
            if scale_in_cooldown is not None:
                self._values["scale_in_cooldown"] = scale_in_cooldown
            if scale_out_cooldown is not None:
                self._values["scale_out_cooldown"] = scale_out_cooldown

        @builtins.property
        def target_value(self) -> jsii.Number:
            '''Defines a target value for the scaling policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html#cfn-dynamodb-globaltable-targettrackingscalingpolicyconfiguration-targetvalue
            '''
            result = self._values.get("target_value")
            assert result is not None, "Required property 'target_value' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def disable_scale_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether scale in by the target tracking scaling policy is disabled.

            The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html#cfn-dynamodb-globaltable-targettrackingscalingpolicyconfiguration-disablescalein
            '''
            result = self._values.get("disable_scale_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def scale_in_cooldown(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, after a scale-in activity completes before another scale-in activity can start.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html#cfn-dynamodb-globaltable-targettrackingscalingpolicyconfiguration-scaleincooldown
            '''
            result = self._values.get("scale_in_cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scale_out_cooldown(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, after a scale-out activity completes before another scale-out activity can start.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-targettrackingscalingpolicyconfiguration.html#cfn-dynamodb-globaltable-targettrackingscalingpolicyconfiguration-scaleoutcooldown
            '''
            result = self._values.get("scale_out_cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingScalingPolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.TimeToLiveSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "attribute_name": "attributeName"},
    )
    class TimeToLiveSpecificationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            attribute_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the settings used to enable or disable Time to Live (TTL) for the specified table.

            All replicas will have the same time to live configuration.

            :param enabled: Indicates whether TTL is to be enabled (true) or disabled (false) on the table.
            :param attribute_name: The name of the attribute used to store the expiration time for items in the table. Currently, you cannot directly change the attribute name used to evaluate time to live. In order to do so, you must first disable time to live, and then re-enable it with the new attribute name. It can take up to one hour for changes to time to live to take effect. If you attempt to modify time to live within that time window, your stack operation might be delayed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-timetolivespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                time_to_live_specification_property = dynamodb.CfnGlobalTable.TimeToLiveSpecificationProperty(
                    enabled=False,
                
                    # the properties below are optional
                    attribute_name="attributeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a2e1b5f2abd745f82312e8a8f9f569cfc3761627512ddc9f780b57c2cd26619)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Indicates whether TTL is to be enabled (true) or disabled (false) on the table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-timetolivespecification.html#cfn-dynamodb-globaltable-timetolivespecification-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute used to store the expiration time for items in the table.

            Currently, you cannot directly change the attribute name used to evaluate time to live. In order to do so, you must first disable time to live, and then re-enable it with the new attribute name. It can take up to one hour for changes to time to live to take effect. If you attempt to modify time to live within that time window, your stack operation might be delayed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-timetolivespecification.html#cfn-dynamodb-globaltable-timetolivespecification-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeToLiveSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnGlobalTable.WriteProvisionedThroughputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "write_capacity_auto_scaling_settings": "writeCapacityAutoScalingSettings",
        },
    )
    class WriteProvisionedThroughputSettingsProperty:
        def __init__(
            self,
            *,
            write_capacity_auto_scaling_settings: typing.Optional[typing.Union[typing.Union["CfnGlobalTable.CapacityAutoScalingSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies an auto scaling policy for write capacity.

            This policy will be applied to all replicas. This setting must be specified if ``BillingMode`` is set to ``PROVISIONED`` .

            :param write_capacity_auto_scaling_settings: Specifies auto scaling settings for the replica table or global secondary index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-writeprovisionedthroughputsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                write_provisioned_throughput_settings_property = dynamodb.CfnGlobalTable.WriteProvisionedThroughputSettingsProperty(
                    write_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                            target_value=123,
                
                            # the properties below are optional
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123
                        ),
                
                        # the properties below are optional
                        seed_capacity=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c20781366ff4d453194f93634df4a8b4d241003b5410ab28f33db210f2b3366)
                check_type(argname="argument write_capacity_auto_scaling_settings", value=write_capacity_auto_scaling_settings, expected_type=type_hints["write_capacity_auto_scaling_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if write_capacity_auto_scaling_settings is not None:
                self._values["write_capacity_auto_scaling_settings"] = write_capacity_auto_scaling_settings

        @builtins.property
        def write_capacity_auto_scaling_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnGlobalTable.CapacityAutoScalingSettingsProperty", _IResolvable_a771d0ef]]:
            '''Specifies auto scaling settings for the replica table or global secondary index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-writeprovisionedthroughputsettings.html#cfn-dynamodb-globaltable-writeprovisionedthroughputsettings-writecapacityautoscalingsettings
            '''
            result = self._values.get("write_capacity_auto_scaling_settings")
            return typing.cast(typing.Optional[typing.Union["CfnGlobalTable.CapacityAutoScalingSettingsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WriteProvisionedThroughputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.CfnGlobalTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_definitions": "attributeDefinitions",
        "key_schema": "keySchema",
        "replicas": "replicas",
        "billing_mode": "billingMode",
        "global_secondary_indexes": "globalSecondaryIndexes",
        "local_secondary_indexes": "localSecondaryIndexes",
        "sse_specification": "sseSpecification",
        "stream_specification": "streamSpecification",
        "table_name": "tableName",
        "time_to_live_specification": "timeToLiveSpecification",
        "write_provisioned_throughput_settings": "writeProvisionedThroughputSettings",
    },
)
class CfnGlobalTableProps:
    def __init__(
        self,
        *,
        attribute_definitions: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.AttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        replicas: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.ReplicaSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        billing_mode: typing.Optional[builtins.str] = None,
        global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.GlobalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        local_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.LocalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        sse_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stream_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.StreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        table_name: typing.Optional[builtins.str] = None,
        time_to_live_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.TimeToLiveSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        write_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.WriteProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGlobalTable``.

        :param attribute_definitions: A list of attributes that describe the key schema for the global table and indexes.
        :param key_schema: Specifies the attributes that make up the primary key for the table. The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.
        :param replicas: Specifies the list of replicas for your global table. The list must contain at least one element, the region where the stack defining the global table is deployed. For example, if you define your table in a stack deployed to us-east-1, you must have an entry in ``Replicas`` with the region us-east-1. You cannot remove the replica in the stack region. .. epigraph:: Adding a replica might take a few minutes for an empty table, or up to several hours for large tables. If you want to add or remove a replica, we recommend submitting an ``UpdateStack`` operation containing only that change. If you add or delete a replica during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new replica, you might need to manually delete the replica. You can create a new global table with as many replicas as needed. You can add or remove replicas after table creation, but you can only add or remove a single replica in each update.
        :param billing_mode: Specifies how you are charged for read and write throughput and how you manage capacity. Valid values are:. - ``PAY_PER_REQUEST`` - ``PROVISIONED`` All replicas in your global table will have the same billing mode. If you use ``PROVISIONED`` billing mode, you must provide an auto scaling configuration via the ``WriteProvisionedThroughputSettings`` property. The default value of this property is ``PROVISIONED`` .
        :param global_secondary_indexes: Global secondary indexes to be created on the global table. You can create up to 20 global secondary indexes. Each replica in your global table will have the same global secondary index settings. You can only create or delete one global secondary index in a single stack operation. Since the backfilling of an index could take a long time, CloudFormation does not wait for the index to become active. If a stack operation rolls back, CloudFormation might not delete an index that has been added. In that case, you will need to delete the index manually.
        :param local_secondary_indexes: Local secondary indexes to be created on the table. You can create up to five local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes. Each replica in your global table will have the same local secondary index settings.
        :param sse_specification: Specifies the settings to enable server-side encryption. These settings will be applied to all replicas. If you plan to use customer-managed KMS keys, you must provide a key for each replica using the ``ReplicaSpecification.ReplicaSSESpecification`` property.
        :param stream_specification: Specifies the streams settings on your global table. You must provide a value for this property if your global table contains more than one replica. You can only change the streams settings if your global table has only one replica.
        :param table_name: A name for the global table. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID as the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param time_to_live_specification: Specifies the time to live (TTL) settings for the table. This setting will be applied to all replicas.
        :param write_provisioned_throughput_settings: Specifies an auto scaling policy for write capacity. This policy will be applied to all replicas. This setting must be specified if ``BillingMode`` is set to ``PROVISIONED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dynamodb as dynamodb
            
            cfn_global_table_props = dynamodb.CfnGlobalTableProps(
                attribute_definitions=[dynamodb.CfnGlobalTable.AttributeDefinitionProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )],
                key_schema=[dynamodb.CfnGlobalTable.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                replicas=[dynamodb.CfnGlobalTable.ReplicaSpecificationProperty(
                    region="region",
            
                    # the properties below are optional
                    contributor_insights_specification=dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty(
                        enabled=False
                    ),
                    deletion_protection_enabled=False,
                    global_secondary_indexes=[dynamodb.CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty(
                        index_name="indexName",
            
                        # the properties below are optional
                        contributor_insights_specification=dynamodb.CfnGlobalTable.ContributorInsightsSpecificationProperty(
                            enabled=False
                        ),
                        read_provisioned_throughput_settings=dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty(
                            read_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                                max_capacity=123,
                                min_capacity=123,
                                target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                                    target_value=123,
            
                                    # the properties below are optional
                                    disable_scale_in=False,
                                    scale_in_cooldown=123,
                                    scale_out_cooldown=123
                                ),
            
                                # the properties below are optional
                                seed_capacity=123
                            ),
                            read_capacity_units=123
                        )
                    )],
                    kinesis_stream_specification=dynamodb.CfnGlobalTable.KinesisStreamSpecificationProperty(
                        stream_arn="streamArn"
                    ),
                    point_in_time_recovery_specification=dynamodb.CfnGlobalTable.PointInTimeRecoverySpecificationProperty(
                        point_in_time_recovery_enabled=False
                    ),
                    read_provisioned_throughput_settings=dynamodb.CfnGlobalTable.ReadProvisionedThroughputSettingsProperty(
                        read_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                                target_value=123,
            
                                # the properties below are optional
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123
                            ),
            
                            # the properties below are optional
                            seed_capacity=123
                        ),
                        read_capacity_units=123
                    ),
                    sse_specification=dynamodb.CfnGlobalTable.ReplicaSSESpecificationProperty(
                        kms_master_key_id="kmsMasterKeyId"
                    ),
                    table_class="tableClass",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
            
                # the properties below are optional
                billing_mode="billingMode",
                global_secondary_indexes=[dynamodb.CfnGlobalTable.GlobalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb.CfnGlobalTable.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb.CfnGlobalTable.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    ),
            
                    # the properties below are optional
                    write_provisioned_throughput_settings=dynamodb.CfnGlobalTable.WriteProvisionedThroughputSettingsProperty(
                        write_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                            max_capacity=123,
                            min_capacity=123,
                            target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                                target_value=123,
            
                                # the properties below are optional
                                disable_scale_in=False,
                                scale_in_cooldown=123,
                                scale_out_cooldown=123
                            ),
            
                            # the properties below are optional
                            seed_capacity=123
                        )
                    )
                )],
                local_secondary_indexes=[dynamodb.CfnGlobalTable.LocalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb.CfnGlobalTable.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb.CfnGlobalTable.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    )
                )],
                sse_specification=dynamodb.CfnGlobalTable.SSESpecificationProperty(
                    sse_enabled=False,
            
                    # the properties below are optional
                    sse_type="sseType"
                ),
                stream_specification=dynamodb.CfnGlobalTable.StreamSpecificationProperty(
                    stream_view_type="streamViewType"
                ),
                table_name="tableName",
                time_to_live_specification=dynamodb.CfnGlobalTable.TimeToLiveSpecificationProperty(
                    enabled=False,
            
                    # the properties below are optional
                    attribute_name="attributeName"
                ),
                write_provisioned_throughput_settings=dynamodb.CfnGlobalTable.WriteProvisionedThroughputSettingsProperty(
                    write_capacity_auto_scaling_settings=dynamodb.CfnGlobalTable.CapacityAutoScalingSettingsProperty(
                        max_capacity=123,
                        min_capacity=123,
                        target_tracking_scaling_policy_configuration=dynamodb.CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty(
                            target_value=123,
            
                            # the properties below are optional
                            disable_scale_in=False,
                            scale_in_cooldown=123,
                            scale_out_cooldown=123
                        ),
            
                        # the properties below are optional
                        seed_capacity=123
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab4bb4e6ae2dc28ed812176f22c08f7e8c6272c5a6b3baa5bfdfea00845d1b9)
            check_type(argname="argument attribute_definitions", value=attribute_definitions, expected_type=type_hints["attribute_definitions"])
            check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument global_secondary_indexes", value=global_secondary_indexes, expected_type=type_hints["global_secondary_indexes"])
            check_type(argname="argument local_secondary_indexes", value=local_secondary_indexes, expected_type=type_hints["local_secondary_indexes"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument stream_specification", value=stream_specification, expected_type=type_hints["stream_specification"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument time_to_live_specification", value=time_to_live_specification, expected_type=type_hints["time_to_live_specification"])
            check_type(argname="argument write_provisioned_throughput_settings", value=write_provisioned_throughput_settings, expected_type=type_hints["write_provisioned_throughput_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute_definitions": attribute_definitions,
            "key_schema": key_schema,
            "replicas": replicas,
        }
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if global_secondary_indexes is not None:
            self._values["global_secondary_indexes"] = global_secondary_indexes
        if local_secondary_indexes is not None:
            self._values["local_secondary_indexes"] = local_secondary_indexes
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if stream_specification is not None:
            self._values["stream_specification"] = stream_specification
        if table_name is not None:
            self._values["table_name"] = table_name
        if time_to_live_specification is not None:
            self._values["time_to_live_specification"] = time_to_live_specification
        if write_provisioned_throughput_settings is not None:
            self._values["write_provisioned_throughput_settings"] = write_provisioned_throughput_settings

    @builtins.property
    def attribute_definitions(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.AttributeDefinitionProperty, _IResolvable_a771d0ef]]]:
        '''A list of attributes that describe the key schema for the global table and indexes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-attributedefinitions
        '''
        result = self._values.get("attribute_definitions")
        assert result is not None, "Required property 'attribute_definitions' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.AttributeDefinitionProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def key_schema(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.KeySchemaProperty, _IResolvable_a771d0ef]]]:
        '''Specifies the attributes that make up the primary key for the table.

        The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-keyschema
        '''
        result = self._values.get("key_schema")
        assert result is not None, "Required property 'key_schema' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.KeySchemaProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def replicas(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.ReplicaSpecificationProperty, _IResolvable_a771d0ef]]]:
        '''Specifies the list of replicas for your global table.

        The list must contain at least one element, the region where the stack defining the global table is deployed. For example, if you define your table in a stack deployed to us-east-1, you must have an entry in ``Replicas`` with the region us-east-1. You cannot remove the replica in the stack region.
        .. epigraph::

           Adding a replica might take a few minutes for an empty table, or up to several hours for large tables. If you want to add or remove a replica, we recommend submitting an ``UpdateStack`` operation containing only that change.

           If you add or delete a replica during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new replica, you might need to manually delete the replica.

        You can create a new global table with as many replicas as needed. You can add or remove replicas after table creation, but you can only add or remove a single replica in each update.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-replicas
        '''
        result = self._values.get("replicas")
        assert result is not None, "Required property 'replicas' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.ReplicaSpecificationProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies how you are charged for read and write throughput and how you manage capacity. Valid values are:.

        - ``PAY_PER_REQUEST``
        - ``PROVISIONED``

        All replicas in your global table will have the same billing mode. If you use ``PROVISIONED`` billing mode, you must provide an auto scaling configuration via the ``WriteProvisionedThroughputSettings`` property. The default value of this property is ``PROVISIONED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-billingmode
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.GlobalSecondaryIndexProperty, _IResolvable_a771d0ef]]]]:
        '''Global secondary indexes to be created on the global table.

        You can create up to 20 global secondary indexes. Each replica in your global table will have the same global secondary index settings. You can only create or delete one global secondary index in a single stack operation.

        Since the backfilling of an index could take a long time, CloudFormation does not wait for the index to become active. If a stack operation rolls back, CloudFormation might not delete an index that has been added. In that case, you will need to delete the index manually.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-globalsecondaryindexes
        '''
        result = self._values.get("global_secondary_indexes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.GlobalSecondaryIndexProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def local_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.LocalSecondaryIndexProperty, _IResolvable_a771d0ef]]]]:
        '''Local secondary indexes to be created on the table.

        You can create up to five local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes. Each replica in your global table will have the same local secondary index settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-localsecondaryindexes
        '''
        result = self._values.get("local_secondary_indexes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.LocalSecondaryIndexProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnGlobalTable.SSESpecificationProperty, _IResolvable_a771d0ef]]:
        '''Specifies the settings to enable server-side encryption.

        These settings will be applied to all replicas. If you plan to use customer-managed KMS keys, you must provide a key for each replica using the ``ReplicaSpecification.ReplicaSSESpecification`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-ssespecification
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[CfnGlobalTable.SSESpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def stream_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnGlobalTable.StreamSpecificationProperty, _IResolvable_a771d0ef]]:
        '''Specifies the streams settings on your global table.

        You must provide a value for this property if your global table contains more than one replica. You can only change the streams settings if your global table has only one replica.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-streamspecification
        '''
        result = self._values.get("stream_specification")
        return typing.cast(typing.Optional[typing.Union[CfnGlobalTable.StreamSpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''A name for the global table.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID as the table name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_to_live_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnGlobalTable.TimeToLiveSpecificationProperty, _IResolvable_a771d0ef]]:
        '''Specifies the time to live (TTL) settings for the table.

        This setting will be applied to all replicas.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-timetolivespecification
        '''
        result = self._values.get("time_to_live_specification")
        return typing.cast(typing.Optional[typing.Union[CfnGlobalTable.TimeToLiveSpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def write_provisioned_throughput_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnGlobalTable.WriteProvisionedThroughputSettingsProperty, _IResolvable_a771d0ef]]:
        '''Specifies an auto scaling policy for write capacity.

        This policy will be applied to all replicas. This setting must be specified if ``BillingMode`` is set to ``PROVISIONED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-writeprovisionedthroughputsettings
        '''
        result = self._values.get("write_provisioned_throughput_settings")
        return typing.cast(typing.Optional[typing.Union[CfnGlobalTable.WriteProvisionedThroughputSettingsProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGlobalTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTable(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dynamodb.CfnTable",
):
    '''A CloudFormation ``AWS::DynamoDB::Table``.

    The ``AWS::DynamoDB::Table`` resource creates a DynamoDB table. For more information, see `CreateTable <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_CreateTable.html>`_ in the *Amazon DynamoDB API Reference* .

    You should be aware of the following behaviors when working with DynamoDB tables:

    - AWS CloudFormation typically creates DynamoDB tables in parallel. However, if your template includes multiple DynamoDB tables with indexes, you must declare dependencies so that the tables are created sequentially. Amazon DynamoDB limits the number of tables with secondary indexes that are in the creating state. If you create multiple tables with indexes at the same time, DynamoDB returns an error and the stack operation fails. For an example, see `DynamoDB Table with a DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#aws-resource-dynamodb-table--examples--DynamoDB_Table_with_a_DependsOn_Attribute>`_ .

    .. epigraph::

       Our guidance is to use the latest schema documented here for your AWS CloudFormation templates. This schema supports the provisioning of all table settings below. When using this schema in your AWS CloudFormation templates, please ensure that your Identity and Access Management ( IAM ) policies are updated with appropriate permissions to allow for the authorization of these setting changes.

    :cloudformationResource: AWS::DynamoDB::Table
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_dynamodb as dynamodb
        
        cfn_table = dynamodb.CfnTable(self, "MyCfnTable",
            key_schema=[dynamodb.CfnTable.KeySchemaProperty(
                attribute_name="attributeName",
                key_type="keyType"
            )],
        
            # the properties below are optional
            attribute_definitions=[dynamodb.CfnTable.AttributeDefinitionProperty(
                attribute_name="attributeName",
                attribute_type="attributeType"
            )],
            billing_mode="billingMode",
            contributor_insights_specification=dynamodb.CfnTable.ContributorInsightsSpecificationProperty(
                enabled=False
            ),
            deletion_protection_enabled=False,
            global_secondary_indexes=[dynamodb.CfnTable.GlobalSecondaryIndexProperty(
                index_name="indexName",
                key_schema=[dynamodb.CfnTable.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                projection=dynamodb.CfnTable.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                ),
        
                # the properties below are optional
                contributor_insights_specification=dynamodb.CfnTable.ContributorInsightsSpecificationProperty(
                    enabled=False
                ),
                provisioned_throughput=dynamodb.CfnTable.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                )
            )],
            import_source_specification=dynamodb.CfnTable.ImportSourceSpecificationProperty(
                input_format="inputFormat",
                s3_bucket_source=dynamodb.CfnTable.S3BucketSourceProperty(
                    s3_bucket="s3Bucket",
        
                    # the properties below are optional
                    s3_bucket_owner="s3BucketOwner",
                    s3_key_prefix="s3KeyPrefix"
                ),
        
                # the properties below are optional
                input_compression_type="inputCompressionType",
                input_format_options=dynamodb.CfnTable.InputFormatOptionsProperty(
                    csv=dynamodb.CfnTable.CsvProperty(
                        delimiter="delimiter",
                        header_list=["headerList"]
                    )
                )
            ),
            kinesis_stream_specification=dynamodb.CfnTable.KinesisStreamSpecificationProperty(
                stream_arn="streamArn"
            ),
            local_secondary_indexes=[dynamodb.CfnTable.LocalSecondaryIndexProperty(
                index_name="indexName",
                key_schema=[dynamodb.CfnTable.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
                projection=dynamodb.CfnTable.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                )
            )],
            point_in_time_recovery_specification=dynamodb.CfnTable.PointInTimeRecoverySpecificationProperty(
                point_in_time_recovery_enabled=False
            ),
            provisioned_throughput=dynamodb.CfnTable.ProvisionedThroughputProperty(
                read_capacity_units=123,
                write_capacity_units=123
            ),
            sse_specification=dynamodb.CfnTable.SSESpecificationProperty(
                sse_enabled=False,
        
                # the properties below are optional
                kms_master_key_id="kmsMasterKeyId",
                sse_type="sseType"
            ),
            stream_specification=dynamodb.CfnTable.StreamSpecificationProperty(
                stream_view_type="streamViewType"
            ),
            table_class="tableClass",
            table_name="tableName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_to_live_specification=dynamodb.CfnTable.TimeToLiveSpecificationProperty(
                attribute_name="attributeName",
                enabled=False
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        attribute_definitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.AttributeDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        billing_mode: typing.Optional[builtins.str] = None,
        contributor_insights_specification: typing.Optional[typing.Union[typing.Union["CfnTable.ContributorInsightsSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.GlobalSecondaryIndexProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        import_source_specification: typing.Optional[typing.Union[typing.Union["CfnTable.ImportSourceSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kinesis_stream_specification: typing.Optional[typing.Union[typing.Union["CfnTable.KinesisStreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        local_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.LocalSecondaryIndexProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        point_in_time_recovery_specification: typing.Optional[typing.Union[typing.Union["CfnTable.PointInTimeRecoverySpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        provisioned_throughput: typing.Optional[typing.Union[typing.Union["CfnTable.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sse_specification: typing.Optional[typing.Union[typing.Union["CfnTable.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stream_specification: typing.Optional[typing.Union[typing.Union["CfnTable.StreamSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        table_class: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_to_live_specification: typing.Optional[typing.Union[typing.Union["CfnTable.TimeToLiveSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::DynamoDB::Table``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_schema: Specifies the attributes that make up the primary key for the table. The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.
        :param attribute_definitions: A list of attributes that describe the key schema for the table and indexes. This property is required to create a DynamoDB table. Update requires: `Some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ . Replacement if you edit an existing AttributeDefinition.
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Valid values include: - ``PROVISIONED`` - We recommend using ``PROVISIONED`` for predictable workloads. ``PROVISIONED`` sets the billing mode to `Provisioned Mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.ProvisionedThroughput.Manual>`_ . - ``PAY_PER_REQUEST`` - We recommend using ``PAY_PER_REQUEST`` for unpredictable workloads. ``PAY_PER_REQUEST`` sets the billing mode to `On-Demand Mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.OnDemand>`_ . If not specified, the default is ``PROVISIONED`` .
        :param contributor_insights_specification: The settings used to enable or disable CloudWatch Contributor Insights for the specified table.
        :param deletion_protection_enabled: Determines if a table is protected from deletion. When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .
        :param global_secondary_indexes: Global secondary indexes to be created on the table. You can create up to 20 global secondary indexes. .. epigraph:: If you update a table to include a new global secondary index, AWS CloudFormation initiates the index creation and then proceeds with the stack update. AWS CloudFormation doesn't wait for the index to complete creation because the backfilling phase can take a long time, depending on the size of the table. You can't use the index or update the table until the index's status is ``ACTIVE`` . You can track its status by using the DynamoDB `DescribeTable <https://docs.aws.amazon.com/cli/latest/reference/dynamodb/describe-table.html>`_ command. If you add or delete an index during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new index, you must manually delete the index. Updates are not supported. The following are exceptions: - If you update either the contributor insights specification or the provisioned throughput values of global secondary indexes, you can update the table without interruption. - You can delete or add one global secondary index without interruption. If you do both in the same update (for example, by changing the index's logical ID), the update fails.
        :param import_source_specification: Specifies the properties of data being imported from the S3 bucket source to the table. .. epigraph:: If you specify the ``ImportSourceSpecification`` property, and also specify either the ``StreamSpecification`` , the ``TableClass`` property, or the ``DeletionProtectionEnabled`` property, the IAM entity creating/updating stack must have ``UpdateTable`` permission.
        :param kinesis_stream_specification: The Kinesis Data Streams configuration for the specified table.
        :param local_secondary_indexes: Local secondary indexes to be created on the table. You can create up to 5 local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes.
        :param point_in_time_recovery_specification: The settings used to enable point in time recovery.
        :param provisioned_throughput: Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits`` . For more information about the contents of a provisioned throughput structure, see `Amazon DynamoDB Table ProvisionedThroughput <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ProvisionedThroughput.html>`_ . If you set ``BillingMode`` as ``PROVISIONED`` , you must specify this property. If you set ``BillingMode`` as ``PAY_PER_REQUEST`` , you cannot specify this property.
        :param sse_specification: Specifies the settings to enable server-side encryption.
        :param stream_specification: The settings for the DynamoDB table stream, which capture changes to items stored in the table.
        :param table_class: The table class of the new table. Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .
        :param table_name: A name for the table. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the table name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param time_to_live_specification: Specifies the Time to Live (TTL) settings for the table. .. epigraph:: For detailed information about the limits in DynamoDB, see `Limits in Amazon DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the Amazon DynamoDB Developer Guide.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85be0711ab7591b6225f503e4224d9c87c962430d54cd36372e3eeb918c268b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTableProps(
            key_schema=key_schema,
            attribute_definitions=attribute_definitions,
            billing_mode=billing_mode,
            contributor_insights_specification=contributor_insights_specification,
            deletion_protection_enabled=deletion_protection_enabled,
            global_secondary_indexes=global_secondary_indexes,
            import_source_specification=import_source_specification,
            kinesis_stream_specification=kinesis_stream_specification,
            local_secondary_indexes=local_secondary_indexes,
            point_in_time_recovery_specification=point_in_time_recovery_specification,
            provisioned_throughput=provisioned_throughput,
            sse_specification=sse_specification,
            stream_specification=stream_specification,
            table_class=table_class,
            table_name=table_name,
            tags=tags,
            time_to_live_specification=time_to_live_specification,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b830bfc4553247aa6445b466a617246c5e7857bfcb84af7bad3ef80f68a69f76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd466d9021dacc515e9198f0d83843ebcf5506ba3489672a6c5c697c2811e06)
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
        '''The Amazon Resource Name (ARN) of the DynamoDB table, such as ``arn:aws:dynamodb:us-east-2:123456789012:table/myDynamoDBTable`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStreamArn")
    def attr_stream_arn(self) -> builtins.str:
        '''The ARN of the DynamoDB stream, such as ``arn:aws:dynamodb:us-east-1:123456789012:table/testddbstack-myDynamoDBTable-012A1SL7SMP5Q/stream/2015-11-30T20:10:00.000`` .

        .. epigraph::

           You must specify the ``StreamSpecification`` property to use this attribute.

        :cloudformationAttribute: StreamArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStreamArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="keySchema")
    def key_schema(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.KeySchemaProperty", _IResolvable_a771d0ef]]]:
        '''Specifies the attributes that make up the primary key for the table.

        The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-keyschema
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.KeySchemaProperty", _IResolvable_a771d0ef]]], jsii.get(self, "keySchema"))

    @key_schema.setter
    def key_schema(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.KeySchemaProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e99008ec9e92d4e21806472950ebaf6488e258740d69a726ec75569f36b968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keySchema", value)

    @builtins.property
    @jsii.member(jsii_name="attributeDefinitions")
    def attribute_definitions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.AttributeDefinitionProperty", _IResolvable_a771d0ef]]]]:
        '''A list of attributes that describe the key schema for the table and indexes.

        This property is required to create a DynamoDB table.

        Update requires: `Some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ . Replacement if you edit an existing AttributeDefinition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-attributedefinitions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.AttributeDefinitionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "attributeDefinitions"))

    @attribute_definitions.setter
    def attribute_definitions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.AttributeDefinitionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0608b5b9696face2f4b4b73951b15835d8cd87978d9965214b421babc187d5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeDefinitions", value)

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(self) -> typing.Optional[builtins.str]:
        '''Specify how you are charged for read and write throughput and how you manage capacity.

        Valid values include:

        - ``PROVISIONED`` - We recommend using ``PROVISIONED`` for predictable workloads. ``PROVISIONED`` sets the billing mode to `Provisioned Mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.ProvisionedThroughput.Manual>`_ .
        - ``PAY_PER_REQUEST`` - We recommend using ``PAY_PER_REQUEST`` for unpredictable workloads. ``PAY_PER_REQUEST`` sets the billing mode to `On-Demand Mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.OnDemand>`_ .

        If not specified, the default is ``PROVISIONED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-billingmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingMode"))

    @billing_mode.setter
    def billing_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11cf6355f9c07e3e9ede53c9f91af4b3c9f708a5be58c17173a1ae09a3817604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingMode", value)

    @builtins.property
    @jsii.member(jsii_name="contributorInsightsSpecification")
    def contributor_insights_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]]:
        '''The settings used to enable or disable CloudWatch Contributor Insights for the specified table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-contributorinsightsspecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "contributorInsightsSpecification"))

    @contributor_insights_specification.setter
    def contributor_insights_specification(
        self,
        value: typing.Optional[typing.Union["CfnTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db3dc901d145b97fdba90f4dfc4846152b0061e14aeb02eb22e6a69cf5ae767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contributorInsightsSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabled")
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Determines if a table is protected from deletion.

        When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-deletionprotectionenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "deletionProtectionEnabled"))

    @deletion_protection_enabled.setter
    def deletion_protection_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc0546f894efe114db4cf43c84f79365c64bbdd94130b1216cc0a33443477f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="globalSecondaryIndexes")
    def global_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.GlobalSecondaryIndexProperty", _IResolvable_a771d0ef]]]]:
        '''Global secondary indexes to be created on the table. You can create up to 20 global secondary indexes.

        .. epigraph::

           If you update a table to include a new global secondary index, AWS CloudFormation initiates the index creation and then proceeds with the stack update. AWS CloudFormation doesn't wait for the index to complete creation because the backfilling phase can take a long time, depending on the size of the table. You can't use the index or update the table until the index's status is ``ACTIVE`` . You can track its status by using the DynamoDB `DescribeTable <https://docs.aws.amazon.com/cli/latest/reference/dynamodb/describe-table.html>`_ command.

           If you add or delete an index during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new index, you must manually delete the index.

           Updates are not supported. The following are exceptions:

           - If you update either the contributor insights specification or the provisioned throughput values of global secondary indexes, you can update the table without interruption.
           - You can delete or add one global secondary index without interruption. If you do both in the same update (for example, by changing the index's logical ID), the update fails.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-globalsecondaryindexes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.GlobalSecondaryIndexProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "globalSecondaryIndexes"))

    @global_secondary_indexes.setter
    def global_secondary_indexes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.GlobalSecondaryIndexProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cbc8eaf2d0227a95669789102bfb304881905ee60d1e8c0feb3f4376de4c5e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalSecondaryIndexes", value)

    @builtins.property
    @jsii.member(jsii_name="importSourceSpecification")
    def import_source_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.ImportSourceSpecificationProperty", _IResolvable_a771d0ef]]:
        '''Specifies the properties of data being imported from the S3 bucket source to the table.

        .. epigraph::

           If you specify the ``ImportSourceSpecification`` property, and also specify either the ``StreamSpecification`` , the ``TableClass`` property, or the ``DeletionProtectionEnabled`` property, the IAM entity creating/updating stack must have ``UpdateTable`` permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-importsourcespecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.ImportSourceSpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "importSourceSpecification"))

    @import_source_specification.setter
    def import_source_specification(
        self,
        value: typing.Optional[typing.Union["CfnTable.ImportSourceSpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d840c1a7c8764b2abb0138c53971a02b5f3d6350627273aa3018824886c747b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importSourceSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamSpecification")
    def kinesis_stream_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.KinesisStreamSpecificationProperty", _IResolvable_a771d0ef]]:
        '''The Kinesis Data Streams configuration for the specified table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-kinesisstreamspecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.KinesisStreamSpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "kinesisStreamSpecification"))

    @kinesis_stream_specification.setter
    def kinesis_stream_specification(
        self,
        value: typing.Optional[typing.Union["CfnTable.KinesisStreamSpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399da2757acdc128203f1943512bfb1c670403f78b17ab28b12cfad414cb97df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisStreamSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="localSecondaryIndexes")
    def local_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.LocalSecondaryIndexProperty", _IResolvable_a771d0ef]]]]:
        '''Local secondary indexes to be created on the table.

        You can create up to 5 local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-localsecondaryindexes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.LocalSecondaryIndexProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "localSecondaryIndexes"))

    @local_secondary_indexes.setter
    def local_secondary_indexes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.LocalSecondaryIndexProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d255b8331c53f30d7967508a99acb1be108798cecf531faaa65a940b8b008c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSecondaryIndexes", value)

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecoverySpecification")
    def point_in_time_recovery_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.PointInTimeRecoverySpecificationProperty", _IResolvable_a771d0ef]]:
        '''The settings used to enable point in time recovery.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-pointintimerecoveryspecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.PointInTimeRecoverySpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "pointInTimeRecoverySpecification"))

    @point_in_time_recovery_specification.setter
    def point_in_time_recovery_specification(
        self,
        value: typing.Optional[typing.Union["CfnTable.PointInTimeRecoverySpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e06be30678f747fe104eab6112203c576778a06fcea872a10ddd45a47f27ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeRecoverySpecification", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]]:
        '''Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits`` .

        For more information about the contents of a provisioned throughput structure, see `Amazon DynamoDB Table ProvisionedThroughput <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ProvisionedThroughput.html>`_ .

        If you set ``BillingMode`` as ``PROVISIONED`` , you must specify this property. If you set ``BillingMode`` as ``PAY_PER_REQUEST`` , you cannot specify this property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-provisionedthroughput
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]], jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(
        self,
        value: typing.Optional[typing.Union["CfnTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8789bec6f5b5369126eb8a594fb26f3b9ad0a27625c9a022ed5c155a73c43efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedThroughput", value)

    @builtins.property
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.SSESpecificationProperty", _IResolvable_a771d0ef]]:
        '''Specifies the settings to enable server-side encryption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-ssespecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.SSESpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseSpecification"))

    @sse_specification.setter
    def sse_specification(
        self,
        value: typing.Optional[typing.Union["CfnTable.SSESpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da5df6980650a3a8d72c24023d2f2e1c04b69510c34b9e3be1443590f151d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="streamSpecification")
    def stream_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.StreamSpecificationProperty", _IResolvable_a771d0ef]]:
        '''The settings for the DynamoDB table stream, which capture changes to items stored in the table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-streamspecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.StreamSpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "streamSpecification"))

    @stream_specification.setter
    def stream_specification(
        self,
        value: typing.Optional[typing.Union["CfnTable.StreamSpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e434617353b6b44480450b63c362760aed242f6a24692f1db95e4a6d619bb31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="tableClass")
    def table_class(self) -> typing.Optional[builtins.str]:
        '''The table class of the new table.

        Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tableclass
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableClass"))

    @table_class.setter
    def table_class(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2330969407eb951c8226fb1ab2e942e17b39f7e62f09215ccbc8665e1dc8ecc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableClass", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        '''A name for the table.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the table name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tablename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e592cbce269b5585c738fd2e58a360f88d109c439412177701f6fd689407d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @builtins.property
    @jsii.member(jsii_name="timeToLiveSpecification")
    def time_to_live_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.TimeToLiveSpecificationProperty", _IResolvable_a771d0ef]]:
        '''Specifies the Time to Live (TTL) settings for the table.

        .. epigraph::

           For detailed information about the limits in DynamoDB, see `Limits in Amazon DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the Amazon DynamoDB Developer Guide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-timetolivespecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.TimeToLiveSpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "timeToLiveSpecification"))

    @time_to_live_specification.setter
    def time_to_live_specification(
        self,
        value: typing.Optional[typing.Union["CfnTable.TimeToLiveSpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0a1d22b9eaf17d6b0150306a0a773ac0b9eb75eef39c0c051de885a3f0c7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeToLiveSpecification", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.AttributeDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_type": "attributeType",
        },
    )
    class AttributeDefinitionProperty:
        def __init__(
            self,
            *,
            attribute_name: builtins.str,
            attribute_type: builtins.str,
        ) -> None:
            '''Represents an attribute for describing the key schema for the table and indexes.

            :param attribute_name: A name for the attribute.
            :param attribute_type: The data type for the attribute, where:. - ``S`` - the attribute is of type String - ``N`` - the attribute is of type Number - ``B`` - the attribute is of type Binary

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-attributedefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                attribute_definition_property = dynamodb.CfnTable.AttributeDefinitionProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76ca9f552dc7e6d78fd9e5e449d1234067ceb642887cee714f485cdc46b9a5e3)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attribute_name": attribute_name,
                "attribute_type": attribute_type,
            }

        @builtins.property
        def attribute_name(self) -> builtins.str:
            '''A name for the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-attributedefinition.html#cfn-dynamodb-table-attributedefinition-attributename
            '''
            result = self._values.get("attribute_name")
            assert result is not None, "Required property 'attribute_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def attribute_type(self) -> builtins.str:
            '''The data type for the attribute, where:.

            - ``S`` - the attribute is of type String
            - ``N`` - the attribute is of type Number
            - ``B`` - the attribute is of type Binary

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-attributedefinition.html#cfn-dynamodb-table-attributedefinition-attributetype
            '''
            result = self._values.get("attribute_type")
            assert result is not None, "Required property 'attribute_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.ContributorInsightsSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class ContributorInsightsSpecificationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''The settings used to enable or disable CloudWatch Contributor Insights.

            :param enabled: Indicates whether CloudWatch Contributor Insights are to be enabled (true) or disabled (false).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-contributorinsightsspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                contributor_insights_specification_property = dynamodb.CfnTable.ContributorInsightsSpecificationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f89d3b21c0ad477e959fc26d96ef5c63878c18a54eade1680959e2741e47af0d)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Indicates whether CloudWatch Contributor Insights are to be enabled (true) or disabled (false).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-contributorinsightsspecification.html#cfn-dynamodb-table-contributorinsightsspecification-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContributorInsightsSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.CsvProperty",
        jsii_struct_bases=[],
        name_mapping={"delimiter": "delimiter", "header_list": "headerList"},
    )
    class CsvProperty:
        def __init__(
            self,
            *,
            delimiter: typing.Optional[builtins.str] = None,
            header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The options for imported source files in CSV format.

            The values are Delimiter and HeaderList.

            :param delimiter: The delimiter used for separating items in the CSV file being imported.
            :param header_list: List of the headers used to specify a common header for all source CSV files being imported. If this field is specified then the first line of each CSV file is treated as data instead of the header. If this field is not specified the the first line of each CSV file is treated as the header.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-csv.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                csv_property = dynamodb.CfnTable.CsvProperty(
                    delimiter="delimiter",
                    header_list=["headerList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1910e1560f86fe9d3c766dad4d35c72c71e8629ca3d7d25442a8ee599e9dcae)
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
                check_type(argname="argument header_list", value=header_list, expected_type=type_hints["header_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if header_list is not None:
                self._values["header_list"] = header_list

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''The delimiter used for separating items in the CSV file being imported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-csv.html#cfn-dynamodb-table-csv-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of the headers used to specify a common header for all source CSV files being imported.

            If this field is specified then the first line of each CSV file is treated as data instead of the header. If this field is not specified the the first line of each CSV file is treated as the header.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-csv.html#cfn-dynamodb-table-csv-headerlist
            '''
            result = self._values.get("header_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsvProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.GlobalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
            "contributor_insights_specification": "contributorInsightsSpecification",
            "provisioned_throughput": "provisionedThroughput",
        },
    )
    class GlobalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: builtins.str,
            key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            projection: typing.Union[typing.Union["CfnTable.ProjectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            contributor_insights_specification: typing.Optional[typing.Union[typing.Union["CfnTable.ContributorInsightsSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            provisioned_throughput: typing.Optional[typing.Union[typing.Union["CfnTable.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Represents the properties of a global secondary index.

            :param index_name: The name of the global secondary index. The name must be unique among all other indexes on this table.
            :param key_schema: The complete key schema for a global secondary index, which consists of one or more pairs of attribute names and key types: - ``HASH`` - partition key - ``RANGE`` - sort key > The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. .. epigraph:: The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.
            :param projection: Represents attributes that are copied (projected) from the table into the global secondary index. These are in addition to the primary key attributes and index key attributes, which are automatically projected.
            :param contributor_insights_specification: The settings used to enable or disable CloudWatch Contributor Insights for the specified global secondary index.
            :param provisioned_throughput: Represents the provisioned throughput settings for the specified global secondary index. For current minimum and maximum provisioned throughput values, see `Service, Account, and Table Quotas <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the *Amazon DynamoDB Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                global_secondary_index_property = dynamodb.CfnTable.GlobalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb.CfnTable.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb.CfnTable.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    ),
                
                    # the properties below are optional
                    contributor_insights_specification=dynamodb.CfnTable.ContributorInsightsSpecificationProperty(
                        enabled=False
                    ),
                    provisioned_throughput=dynamodb.CfnTable.ProvisionedThroughputProperty(
                        read_capacity_units=123,
                        write_capacity_units=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__43c1b671d74eccaecc71ca0eb7290c862f8a15f213c2d9db856d7711f73ae318)
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
                check_type(argname="argument projection", value=projection, expected_type=type_hints["projection"])
                check_type(argname="argument contributor_insights_specification", value=contributor_insights_specification, expected_type=type_hints["contributor_insights_specification"])
                check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "index_name": index_name,
                "key_schema": key_schema,
                "projection": projection,
            }
            if contributor_insights_specification is not None:
                self._values["contributor_insights_specification"] = contributor_insights_specification
            if provisioned_throughput is not None:
                self._values["provisioned_throughput"] = provisioned_throughput

        @builtins.property
        def index_name(self) -> builtins.str:
            '''The name of the global secondary index.

            The name must be unique among all other indexes on this table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-indexname
            '''
            result = self._values.get("index_name")
            assert result is not None, "Required property 'index_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.KeySchemaProperty", _IResolvable_a771d0ef]]]:
            '''The complete key schema for a global secondary index, which consists of one or more pairs of attribute names and key types:  - ``HASH`` - partition key - ``RANGE`` - sort key  > The partition key of an item is also known as its *hash attribute* .

            The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.
            .. epigraph::

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-keyschema
            '''
            result = self._values.get("key_schema")
            assert result is not None, "Required property 'key_schema' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.KeySchemaProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def projection(
            self,
        ) -> typing.Union["CfnTable.ProjectionProperty", _IResolvable_a771d0ef]:
            '''Represents attributes that are copied (projected) from the table into the global secondary index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-projection
            '''
            result = self._values.get("projection")
            assert result is not None, "Required property 'projection' is missing"
            return typing.cast(typing.Union["CfnTable.ProjectionProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def contributor_insights_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]]:
            '''The settings used to enable or disable CloudWatch Contributor Insights for the specified global secondary index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-contributorinsightsspecification
            '''
            result = self._values.get("contributor_insights_specification")
            return typing.cast(typing.Optional[typing.Union["CfnTable.ContributorInsightsSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def provisioned_throughput(
            self,
        ) -> typing.Optional[typing.Union["CfnTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]]:
            '''Represents the provisioned throughput settings for the specified global secondary index.

            For current minimum and maximum provisioned throughput values, see `Service, Account, and Table Quotas <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the *Amazon DynamoDB Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-globalsecondaryindex.html#cfn-dynamodb-table-globalsecondaryindex-provisionedthroughput
            '''
            result = self._values.get("provisioned_throughput")
            return typing.cast(typing.Optional[typing.Union["CfnTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.ImportSourceSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_format": "inputFormat",
            "s3_bucket_source": "s3BucketSource",
            "input_compression_type": "inputCompressionType",
            "input_format_options": "inputFormatOptions",
        },
    )
    class ImportSourceSpecificationProperty:
        def __init__(
            self,
            *,
            input_format: builtins.str,
            s3_bucket_source: typing.Union[typing.Union["CfnTable.S3BucketSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            input_compression_type: typing.Optional[builtins.str] = None,
            input_format_options: typing.Optional[typing.Union[typing.Union["CfnTable.InputFormatOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the properties of data being imported from the S3 bucket source to the table.

            :param input_format: The format of the source data. Valid values for ``ImportFormat`` are ``CSV`` , ``DYNAMODB_JSON`` or ``ION`` .
            :param s3_bucket_source: The S3 bucket that provides the source for the import.
            :param input_compression_type: Type of compression to be used on the input coming from the imported table.
            :param input_format_options: Additional properties that specify how the input is formatted,.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                import_source_specification_property = dynamodb.CfnTable.ImportSourceSpecificationProperty(
                    input_format="inputFormat",
                    s3_bucket_source=dynamodb.CfnTable.S3BucketSourceProperty(
                        s3_bucket="s3Bucket",
                
                        # the properties below are optional
                        s3_bucket_owner="s3BucketOwner",
                        s3_key_prefix="s3KeyPrefix"
                    ),
                
                    # the properties below are optional
                    input_compression_type="inputCompressionType",
                    input_format_options=dynamodb.CfnTable.InputFormatOptionsProperty(
                        csv=dynamodb.CfnTable.CsvProperty(
                            delimiter="delimiter",
                            header_list=["headerList"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__718bfb735c53c4df753bfe5a9a73388b72b6b7a5c9cb396f0300ef4406672f85)
                check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
                check_type(argname="argument s3_bucket_source", value=s3_bucket_source, expected_type=type_hints["s3_bucket_source"])
                check_type(argname="argument input_compression_type", value=input_compression_type, expected_type=type_hints["input_compression_type"])
                check_type(argname="argument input_format_options", value=input_format_options, expected_type=type_hints["input_format_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "input_format": input_format,
                "s3_bucket_source": s3_bucket_source,
            }
            if input_compression_type is not None:
                self._values["input_compression_type"] = input_compression_type
            if input_format_options is not None:
                self._values["input_format_options"] = input_format_options

        @builtins.property
        def input_format(self) -> builtins.str:
            '''The format of the source data.

            Valid values for ``ImportFormat`` are ``CSV`` , ``DYNAMODB_JSON`` or ``ION`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html#cfn-dynamodb-table-importsourcespecification-inputformat
            '''
            result = self._values.get("input_format")
            assert result is not None, "Required property 'input_format' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket_source(
            self,
        ) -> typing.Union["CfnTable.S3BucketSourceProperty", _IResolvable_a771d0ef]:
            '''The S3 bucket that provides the source for the import.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html#cfn-dynamodb-table-importsourcespecification-s3bucketsource
            '''
            result = self._values.get("s3_bucket_source")
            assert result is not None, "Required property 's3_bucket_source' is missing"
            return typing.cast(typing.Union["CfnTable.S3BucketSourceProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def input_compression_type(self) -> typing.Optional[builtins.str]:
            '''Type of compression to be used on the input coming from the imported table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html#cfn-dynamodb-table-importsourcespecification-inputcompressiontype
            '''
            result = self._values.get("input_compression_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_format_options(
            self,
        ) -> typing.Optional[typing.Union["CfnTable.InputFormatOptionsProperty", _IResolvable_a771d0ef]]:
            '''Additional properties that specify how the input is formatted,.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-importsourcespecification.html#cfn-dynamodb-table-importsourcespecification-inputformatoptions
            '''
            result = self._values.get("input_format_options")
            return typing.cast(typing.Optional[typing.Union["CfnTable.InputFormatOptionsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImportSourceSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.InputFormatOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"csv": "csv"},
    )
    class InputFormatOptionsProperty:
        def __init__(
            self,
            *,
            csv: typing.Optional[typing.Union[typing.Union["CfnTable.CsvProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The format options for the data that was imported into the target table.

            There is one value, CsvOption.

            :param csv: The options for imported source files in CSV format. The values are Delimiter and HeaderList.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-inputformatoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                input_format_options_property = dynamodb.CfnTable.InputFormatOptionsProperty(
                    csv=dynamodb.CfnTable.CsvProperty(
                        delimiter="delimiter",
                        header_list=["headerList"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2618be9553d593cda68c324154302ce946c332678e3950d7030c32a7cdba181c)
                check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if csv is not None:
                self._values["csv"] = csv

        @builtins.property
        def csv(
            self,
        ) -> typing.Optional[typing.Union["CfnTable.CsvProperty", _IResolvable_a771d0ef]]:
            '''The options for imported source files in CSV format.

            The values are Delimiter and HeaderList.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-inputformatoptions.html#cfn-dynamodb-table-inputformatoptions-csv
            '''
            result = self._values.get("csv")
            return typing.cast(typing.Optional[typing.Union["CfnTable.CsvProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputFormatOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.KeySchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "key_type": "keyType"},
    )
    class KeySchemaProperty:
        def __init__(
            self,
            *,
            attribute_name: builtins.str,
            key_type: builtins.str,
        ) -> None:
            '''Represents *a single element* of a key schema.

            A key schema specifies the attributes that make up the primary key of a table, or the key attributes of an index.

            A ``KeySchemaElement`` represents exactly one attribute of the primary key. For example, a simple primary key would be represented by one ``KeySchemaElement`` (for the partition key). A composite primary key would require one ``KeySchemaElement`` for the partition key, and another ``KeySchemaElement`` for the sort key.

            A ``KeySchemaElement`` must be a scalar, top-level attribute (not a nested attribute). The data type must be one of String, Number, or Binary. The attribute cannot be nested within a List or a Map.

            :param attribute_name: The name of a key attribute.
            :param key_type: The role that this key attribute will assume:. - ``HASH`` - partition key - ``RANGE`` - sort key .. epigraph:: The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-keyschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                key_schema_property = dynamodb.CfnTable.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a06cc940eab42d67b773ff8157af3c42e5806b2241741015a3b943c58fc5ba23)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attribute_name": attribute_name,
                "key_type": key_type,
            }

        @builtins.property
        def attribute_name(self) -> builtins.str:
            '''The name of a key attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-keyschema.html#cfn-dynamodb-table-keyschema-attributename
            '''
            result = self._values.get("attribute_name")
            assert result is not None, "Required property 'attribute_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_type(self) -> builtins.str:
            '''The role that this key attribute will assume:.

            - ``HASH`` - partition key
            - ``RANGE`` - sort key

            .. epigraph::

               The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-keyschema.html#cfn-dynamodb-table-keyschema-keytype
            '''
            result = self._values.get("key_type")
            assert result is not None, "Required property 'key_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.KinesisStreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_arn": "streamArn"},
    )
    class KinesisStreamSpecificationProperty:
        def __init__(self, *, stream_arn: builtins.str) -> None:
            '''The Kinesis Data Streams configuration for the specified table.

            :param stream_arn: The ARN for a specific Kinesis data stream. Length Constraints: Minimum length of 37. Maximum length of 1024.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-kinesisstreamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                kinesis_stream_specification_property = dynamodb.CfnTable.KinesisStreamSpecificationProperty(
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4173e3e9b222adbdd1234ca9ddd8353adbf7b1e710512b85d185024f3c02211)
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_arn": stream_arn,
            }

        @builtins.property
        def stream_arn(self) -> builtins.str:
            '''The ARN for a specific Kinesis data stream.

            Length Constraints: Minimum length of 37. Maximum length of 1024.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-kinesisstreamspecification.html#cfn-dynamodb-table-kinesisstreamspecification-streamarn
            '''
            result = self._values.get("stream_arn")
            assert result is not None, "Required property 'stream_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.LocalSecondaryIndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "key_schema": "keySchema",
            "projection": "projection",
        },
    )
    class LocalSecondaryIndexProperty:
        def __init__(
            self,
            *,
            index_name: builtins.str,
            key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTable.KeySchemaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            projection: typing.Union[typing.Union["CfnTable.ProjectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Represents the properties of a local secondary index.

            A local secondary index can only be created when its parent table is created.

            :param index_name: The name of the local secondary index. The name must be unique among all other indexes on this table.
            :param key_schema: The complete key schema for the local secondary index, consisting of one or more pairs of attribute names and key types: - ``HASH`` - partition key - ``RANGE`` - sort key > The partition key of an item is also known as its *hash attribute* . The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values. .. epigraph:: The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.
            :param projection: Represents attributes that are copied (projected) from the table into the local secondary index. These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-localsecondaryindex.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                local_secondary_index_property = dynamodb.CfnTable.LocalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb.CfnTable.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb.CfnTable.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcac9a98632b25795eb0d094c0eb7ce020ae04d36273703d276feff371bc06af)
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
                check_type(argname="argument projection", value=projection, expected_type=type_hints["projection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "index_name": index_name,
                "key_schema": key_schema,
                "projection": projection,
            }

        @builtins.property
        def index_name(self) -> builtins.str:
            '''The name of the local secondary index.

            The name must be unique among all other indexes on this table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-localsecondaryindex.html#cfn-dynamodb-table-localsecondaryindex-indexname
            '''
            result = self._values.get("index_name")
            assert result is not None, "Required property 'index_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_schema(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.KeySchemaProperty", _IResolvable_a771d0ef]]]:
            '''The complete key schema for the local secondary index, consisting of one or more pairs of attribute names and key types:  - ``HASH`` - partition key - ``RANGE`` - sort key  > The partition key of an item is also known as its *hash attribute* .

            The term "hash attribute" derives from DynamoDB's usage of an internal hash function to evenly distribute data items across partitions, based on their partition key values.
            .. epigraph::

               The sort key of an item is also known as its *range attribute* . The term "range attribute" derives from the way DynamoDB stores items with the same partition key physically close together, in sorted order by the sort key value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-localsecondaryindex.html#cfn-dynamodb-table-localsecondaryindex-keyschema
            '''
            result = self._values.get("key_schema")
            assert result is not None, "Required property 'key_schema' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTable.KeySchemaProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def projection(
            self,
        ) -> typing.Union["CfnTable.ProjectionProperty", _IResolvable_a771d0ef]:
            '''Represents attributes that are copied (projected) from the table into the local secondary index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-localsecondaryindex.html#cfn-dynamodb-table-localsecondaryindex-projection
            '''
            result = self._values.get("projection")
            assert result is not None, "Required property 'projection' is missing"
            return typing.cast(typing.Union["CfnTable.ProjectionProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalSecondaryIndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.PointInTimeRecoverySpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"point_in_time_recovery_enabled": "pointInTimeRecoveryEnabled"},
    )
    class PointInTimeRecoverySpecificationProperty:
        def __init__(
            self,
            *,
            point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The settings used to enable point in time recovery.

            :param point_in_time_recovery_enabled: Indicates whether point in time recovery is enabled (true) or disabled (false) on the table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-pointintimerecoveryspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                point_in_time_recovery_specification_property = dynamodb.CfnTable.PointInTimeRecoverySpecificationProperty(
                    point_in_time_recovery_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0baa9db43cfc972ee5bf1b5ba9521012a5128be92bb92dec1b8563be496a9b65)
                check_type(argname="argument point_in_time_recovery_enabled", value=point_in_time_recovery_enabled, expected_type=type_hints["point_in_time_recovery_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if point_in_time_recovery_enabled is not None:
                self._values["point_in_time_recovery_enabled"] = point_in_time_recovery_enabled

        @builtins.property
        def point_in_time_recovery_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether point in time recovery is enabled (true) or disabled (false) on the table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-pointintimerecoveryspecification.html#cfn-dynamodb-table-pointintimerecoveryspecification-pointintimerecoveryenabled
            '''
            result = self._values.get("point_in_time_recovery_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PointInTimeRecoverySpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.ProjectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "non_key_attributes": "nonKeyAttributes",
            "projection_type": "projectionType",
        },
    )
    class ProjectionProperty:
        def __init__(
            self,
            *,
            non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
            projection_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents attributes that are copied (projected) from the table into an index.

            These are in addition to the primary key attributes and index key attributes, which are automatically projected.

            :param non_key_attributes: Represents the non-key attribute names which will be projected into the index. For local secondary indexes, the total count of ``NonKeyAttributes`` summed across all of the local secondary indexes, must not exceed 100. If you project the same attribute into two different indexes, this counts as two distinct attributes when determining the total.
            :param projection_type: The set of attributes that are projected into the index:. - ``KEYS_ONLY`` - Only the index and primary keys are projected into the index. - ``INCLUDE`` - In addition to the attributes described in ``KEYS_ONLY`` , the secondary index will include other non-key attributes that you specify. - ``ALL`` - All of the table attributes are projected into the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-projection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                projection_property = dynamodb.CfnTable.ProjectionProperty(
                    non_key_attributes=["nonKeyAttributes"],
                    projection_type="projectionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0897b4b9796dea226f35dea63debe91e6e511f41df2ac5e7a14cdf9913e142f4)
                check_type(argname="argument non_key_attributes", value=non_key_attributes, expected_type=type_hints["non_key_attributes"])
                check_type(argname="argument projection_type", value=projection_type, expected_type=type_hints["projection_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if non_key_attributes is not None:
                self._values["non_key_attributes"] = non_key_attributes
            if projection_type is not None:
                self._values["projection_type"] = projection_type

        @builtins.property
        def non_key_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Represents the non-key attribute names which will be projected into the index.

            For local secondary indexes, the total count of ``NonKeyAttributes`` summed across all of the local secondary indexes, must not exceed 100. If you project the same attribute into two different indexes, this counts as two distinct attributes when determining the total.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-projection.html#cfn-dynamodb-table-projection-nonkeyattributes
            '''
            result = self._values.get("non_key_attributes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def projection_type(self) -> typing.Optional[builtins.str]:
            '''The set of attributes that are projected into the index:.

            - ``KEYS_ONLY`` - Only the index and primary keys are projected into the index.
            - ``INCLUDE`` - In addition to the attributes described in ``KEYS_ONLY`` , the secondary index will include other non-key attributes that you specify.
            - ``ALL`` - All of the table attributes are projected into the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-projection.html#cfn-dynamodb-table-projection-projectiontype
            '''
            result = self._values.get("projection_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.ProvisionedThroughputProperty",
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
            '''Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits`` .

            For more information about the contents of a provisioned throughput structure, see `Amazon DynamoDB Table ProvisionedThroughput <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ProvisionedThroughput.html>`_ .

            :param read_capacity_units: The maximum number of strongly consistent reads consumed per second before DynamoDB returns a ``ThrottlingException`` . For more information, see `Specifying Read and Write Requirements <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html>`_ in the *Amazon DynamoDB Developer Guide* . If read/write capacity mode is ``PAY_PER_REQUEST`` the value is set to 0.
            :param write_capacity_units: The maximum number of writes consumed per second before DynamoDB returns a ``ThrottlingException`` . For more information, see `Specifying Read and Write Requirements <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html>`_ in the *Amazon DynamoDB Developer Guide* . If read/write capacity mode is ``PAY_PER_REQUEST`` the value is set to 0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-provisionedthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                provisioned_throughput_property = dynamodb.CfnTable.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eff28a83c2c1f4fb7bee6cdf58953313cd5159fe058faf732680062688fca3a1)
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
                check_type(argname="argument write_capacity_units", value=write_capacity_units, expected_type=type_hints["write_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "read_capacity_units": read_capacity_units,
                "write_capacity_units": write_capacity_units,
            }

        @builtins.property
        def read_capacity_units(self) -> jsii.Number:
            '''The maximum number of strongly consistent reads consumed per second before DynamoDB returns a ``ThrottlingException`` .

            For more information, see `Specifying Read and Write Requirements <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html>`_ in the *Amazon DynamoDB Developer Guide* .

            If read/write capacity mode is ``PAY_PER_REQUEST`` the value is set to 0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-provisionedthroughput.html#cfn-dynamodb-table-provisionedthroughput-readcapacityunits
            '''
            result = self._values.get("read_capacity_units")
            assert result is not None, "Required property 'read_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def write_capacity_units(self) -> jsii.Number:
            '''The maximum number of writes consumed per second before DynamoDB returns a ``ThrottlingException`` .

            For more information, see `Specifying Read and Write Requirements <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html>`_ in the *Amazon DynamoDB Developer Guide* .

            If read/write capacity mode is ``PAY_PER_REQUEST`` the value is set to 0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-provisionedthroughput.html#cfn-dynamodb-table-provisionedthroughput-writecapacityunits
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
        jsii_type="monocdk.aws_dynamodb.CfnTable.S3BucketSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket": "s3Bucket",
            "s3_bucket_owner": "s3BucketOwner",
            "s3_key_prefix": "s3KeyPrefix",
        },
    )
    class S3BucketSourceProperty:
        def __init__(
            self,
            *,
            s3_bucket: builtins.str,
            s3_bucket_owner: typing.Optional[builtins.str] = None,
            s3_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 bucket that is being imported from.

            :param s3_bucket: The S3 bucket that is being imported from.
            :param s3_bucket_owner: The account number of the S3 bucket that is being imported from. If the bucket is owned by the requester this is optional.
            :param s3_key_prefix: The key prefix shared by all S3 Objects that are being imported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-s3bucketsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                s3_bucket_source_property = dynamodb.CfnTable.S3BucketSourceProperty(
                    s3_bucket="s3Bucket",
                
                    # the properties below are optional
                    s3_bucket_owner="s3BucketOwner",
                    s3_key_prefix="s3KeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78c029c869a0c1f5ab867a2830ad96fd8ffdd6ffcbaacdccbe58cfdaaae34dd0)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_bucket_owner", value=s3_bucket_owner, expected_type=type_hints["s3_bucket_owner"])
                check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
            }
            if s3_bucket_owner is not None:
                self._values["s3_bucket_owner"] = s3_bucket_owner
            if s3_key_prefix is not None:
                self._values["s3_key_prefix"] = s3_key_prefix

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The S3 bucket that is being imported from.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-s3bucketsource.html#cfn-dynamodb-table-s3bucketsource-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The account number of the S3 bucket that is being imported from.

            If the bucket is owned by the requester this is optional.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-s3bucketsource.html#cfn-dynamodb-table-s3bucketsource-s3bucketowner
            '''
            result = self._values.get("s3_bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The key prefix shared by all S3 Objects that are being imported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-s3bucketsource.html#cfn-dynamodb-table-s3bucketsource-s3keyprefix
            '''
            result = self._values.get("s3_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "sse_enabled": "sseEnabled",
            "kms_master_key_id": "kmsMasterKeyId",
            "sse_type": "sseType",
        },
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            kms_master_key_id: typing.Optional[builtins.str] = None,
            sse_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the settings used to enable server-side encryption.

            :param sse_enabled: Indicates whether server-side encryption is done using an AWS managed key or an AWS owned key. If enabled (true), server-side encryption type is set to ``KMS`` and an AWS managed key is used ( AWS KMS charges apply). If disabled (false) or not specified, server-side encryption is set to AWS owned key.
            :param kms_master_key_id: The AWS KMS key that should be used for the AWS KMS encryption. To specify a key, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter if the key is different from the default DynamoDB key ``alias/aws/dynamodb`` .
            :param sse_type: Server-side encryption type. The only supported value is:. - ``KMS`` - Server-side encryption that uses AWS Key Management Service . The key is stored in your account and is managed by AWS KMS ( AWS KMS charges apply).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                s_sESpecification_property = dynamodb.CfnTable.SSESpecificationProperty(
                    sse_enabled=False,
                
                    # the properties below are optional
                    kms_master_key_id="kmsMasterKeyId",
                    sse_type="sseType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7fcd0cd914dfaaa760893f87c53f947c543a10d21b25d7f32f53b8b6da1defcb)
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
                check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
                check_type(argname="argument sse_type", value=sse_type, expected_type=type_hints["sse_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "sse_enabled": sse_enabled,
            }
            if kms_master_key_id is not None:
                self._values["kms_master_key_id"] = kms_master_key_id
            if sse_type is not None:
                self._values["sse_type"] = sse_type

        @builtins.property
        def sse_enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Indicates whether server-side encryption is done using an AWS managed key or an AWS owned key.

            If enabled (true), server-side encryption type is set to ``KMS`` and an AWS managed key is used ( AWS KMS charges apply). If disabled (false) or not specified, server-side encryption is set to AWS owned key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-sseenabled
            '''
            result = self._values.get("sse_enabled")
            assert result is not None, "Required property 'sse_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def kms_master_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS KMS key that should be used for the AWS KMS encryption.

            To specify a key, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter if the key is different from the default DynamoDB key ``alias/aws/dynamodb`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-kmsmasterkeyid
            '''
            result = self._values.get("kms_master_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_type(self) -> typing.Optional[builtins.str]:
            '''Server-side encryption type. The only supported value is:.

            - ``KMS`` - Server-side encryption that uses AWS Key Management Service . The key is stored in your account and is managed by AWS KMS ( AWS KMS charges apply).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html#cfn-dynamodb-table-ssespecification-ssetype
            '''
            result = self._values.get("sse_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.StreamSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_view_type": "streamViewType"},
    )
    class StreamSpecificationProperty:
        def __init__(self, *, stream_view_type: builtins.str) -> None:
            '''Represents the DynamoDB Streams configuration for a table in DynamoDB.

            :param stream_view_type: When an item in the table is modified, ``StreamViewType`` determines what information is written to the stream for this table. Valid values for ``StreamViewType`` are: - ``KEYS_ONLY`` - Only the key attributes of the modified item are written to the stream. - ``NEW_IMAGE`` - The entire item, as it appears after it was modified, is written to the stream. - ``OLD_IMAGE`` - The entire item, as it appeared before it was modified, is written to the stream. - ``NEW_AND_OLD_IMAGES`` - Both the new and the old item images of the item are written to the stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-streamspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                stream_specification_property = dynamodb.CfnTable.StreamSpecificationProperty(
                    stream_view_type="streamViewType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b6e167540d028aef1e290eaa63099f021d65666c2dbddb909a00aa19179c373)
                check_type(argname="argument stream_view_type", value=stream_view_type, expected_type=type_hints["stream_view_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_view_type": stream_view_type,
            }

        @builtins.property
        def stream_view_type(self) -> builtins.str:
            '''When an item in the table is modified, ``StreamViewType`` determines what information is written to the stream for this table.

            Valid values for ``StreamViewType`` are:

            - ``KEYS_ONLY`` - Only the key attributes of the modified item are written to the stream.
            - ``NEW_IMAGE`` - The entire item, as it appears after it was modified, is written to the stream.
            - ``OLD_IMAGE`` - The entire item, as it appeared before it was modified, is written to the stream.
            - ``NEW_AND_OLD_IMAGES`` - Both the new and the old item images of the item are written to the stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-streamspecification.html#cfn-dynamodb-table-streamspecification-streamviewtype
            '''
            result = self._values.get("stream_view_type")
            assert result is not None, "Required property 'stream_view_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dynamodb.CfnTable.TimeToLiveSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_name": "attributeName", "enabled": "enabled"},
    )
    class TimeToLiveSpecificationProperty:
        def __init__(
            self,
            *,
            attribute_name: builtins.str,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''Represents the settings used to enable or disable Time to Live (TTL) for the specified table.

            :param attribute_name: The name of the TTL attribute used to store the expiration time for items in the table. .. epigraph:: - To update this property, you must first disable TTL and then enable TTL with the new attribute name.
            :param enabled: Indicates whether TTL is to be enabled (true) or disabled (false) on the table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-timetolivespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dynamodb as dynamodb
                
                time_to_live_specification_property = dynamodb.CfnTable.TimeToLiveSpecificationProperty(
                    attribute_name="attributeName",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__69bfeaa5ee709146cf4c4e2578c645eb4e66e88a97e8f377b8fc8be03aaac182)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attribute_name": attribute_name,
                "enabled": enabled,
            }

        @builtins.property
        def attribute_name(self) -> builtins.str:
            '''The name of the TTL attribute used to store the expiration time for items in the table.

            .. epigraph::

               - To update this property, you must first disable TTL and then enable TTL with the new attribute name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-timetolivespecification.html#cfn-dynamodb-table-timetolivespecification-attributename
            '''
            result = self._values.get("attribute_name")
            assert result is not None, "Required property 'attribute_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Indicates whether TTL is to be enabled (true) or disabled (false) on the table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-timetolivespecification.html#cfn-dynamodb-table-timetolivespecification-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeToLiveSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.CfnTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_schema": "keySchema",
        "attribute_definitions": "attributeDefinitions",
        "billing_mode": "billingMode",
        "contributor_insights_specification": "contributorInsightsSpecification",
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "global_secondary_indexes": "globalSecondaryIndexes",
        "import_source_specification": "importSourceSpecification",
        "kinesis_stream_specification": "kinesisStreamSpecification",
        "local_secondary_indexes": "localSecondaryIndexes",
        "point_in_time_recovery_specification": "pointInTimeRecoverySpecification",
        "provisioned_throughput": "provisionedThroughput",
        "sse_specification": "sseSpecification",
        "stream_specification": "streamSpecification",
        "table_class": "tableClass",
        "table_name": "tableName",
        "tags": "tags",
        "time_to_live_specification": "timeToLiveSpecification",
    },
)
class CfnTableProps:
    def __init__(
        self,
        *,
        key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        attribute_definitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.AttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        billing_mode: typing.Optional[builtins.str] = None,
        contributor_insights_specification: typing.Optional[typing.Union[typing.Union[CfnTable.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.GlobalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        import_source_specification: typing.Optional[typing.Union[typing.Union[CfnTable.ImportSourceSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kinesis_stream_specification: typing.Optional[typing.Union[typing.Union[CfnTable.KinesisStreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        local_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.LocalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        point_in_time_recovery_specification: typing.Optional[typing.Union[typing.Union[CfnTable.PointInTimeRecoverySpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        provisioned_throughput: typing.Optional[typing.Union[typing.Union[CfnTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sse_specification: typing.Optional[typing.Union[typing.Union[CfnTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stream_specification: typing.Optional[typing.Union[typing.Union[CfnTable.StreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        table_class: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_to_live_specification: typing.Optional[typing.Union[typing.Union[CfnTable.TimeToLiveSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTable``.

        :param key_schema: Specifies the attributes that make up the primary key for the table. The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.
        :param attribute_definitions: A list of attributes that describe the key schema for the table and indexes. This property is required to create a DynamoDB table. Update requires: `Some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ . Replacement if you edit an existing AttributeDefinition.
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Valid values include: - ``PROVISIONED`` - We recommend using ``PROVISIONED`` for predictable workloads. ``PROVISIONED`` sets the billing mode to `Provisioned Mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.ProvisionedThroughput.Manual>`_ . - ``PAY_PER_REQUEST`` - We recommend using ``PAY_PER_REQUEST`` for unpredictable workloads. ``PAY_PER_REQUEST`` sets the billing mode to `On-Demand Mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.OnDemand>`_ . If not specified, the default is ``PROVISIONED`` .
        :param contributor_insights_specification: The settings used to enable or disable CloudWatch Contributor Insights for the specified table.
        :param deletion_protection_enabled: Determines if a table is protected from deletion. When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .
        :param global_secondary_indexes: Global secondary indexes to be created on the table. You can create up to 20 global secondary indexes. .. epigraph:: If you update a table to include a new global secondary index, AWS CloudFormation initiates the index creation and then proceeds with the stack update. AWS CloudFormation doesn't wait for the index to complete creation because the backfilling phase can take a long time, depending on the size of the table. You can't use the index or update the table until the index's status is ``ACTIVE`` . You can track its status by using the DynamoDB `DescribeTable <https://docs.aws.amazon.com/cli/latest/reference/dynamodb/describe-table.html>`_ command. If you add or delete an index during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new index, you must manually delete the index. Updates are not supported. The following are exceptions: - If you update either the contributor insights specification or the provisioned throughput values of global secondary indexes, you can update the table without interruption. - You can delete or add one global secondary index without interruption. If you do both in the same update (for example, by changing the index's logical ID), the update fails.
        :param import_source_specification: Specifies the properties of data being imported from the S3 bucket source to the table. .. epigraph:: If you specify the ``ImportSourceSpecification`` property, and also specify either the ``StreamSpecification`` , the ``TableClass`` property, or the ``DeletionProtectionEnabled`` property, the IAM entity creating/updating stack must have ``UpdateTable`` permission.
        :param kinesis_stream_specification: The Kinesis Data Streams configuration for the specified table.
        :param local_secondary_indexes: Local secondary indexes to be created on the table. You can create up to 5 local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes.
        :param point_in_time_recovery_specification: The settings used to enable point in time recovery.
        :param provisioned_throughput: Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits`` . For more information about the contents of a provisioned throughput structure, see `Amazon DynamoDB Table ProvisionedThroughput <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ProvisionedThroughput.html>`_ . If you set ``BillingMode`` as ``PROVISIONED`` , you must specify this property. If you set ``BillingMode`` as ``PAY_PER_REQUEST`` , you cannot specify this property.
        :param sse_specification: Specifies the settings to enable server-side encryption.
        :param stream_specification: The settings for the DynamoDB table stream, which capture changes to items stored in the table.
        :param table_class: The table class of the new table. Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .
        :param table_name: A name for the table. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the table name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param time_to_live_specification: Specifies the Time to Live (TTL) settings for the table. .. epigraph:: For detailed information about the limits in DynamoDB, see `Limits in Amazon DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the Amazon DynamoDB Developer Guide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dynamodb as dynamodb
            
            cfn_table_props = dynamodb.CfnTableProps(
                key_schema=[dynamodb.CfnTable.KeySchemaProperty(
                    attribute_name="attributeName",
                    key_type="keyType"
                )],
            
                # the properties below are optional
                attribute_definitions=[dynamodb.CfnTable.AttributeDefinitionProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )],
                billing_mode="billingMode",
                contributor_insights_specification=dynamodb.CfnTable.ContributorInsightsSpecificationProperty(
                    enabled=False
                ),
                deletion_protection_enabled=False,
                global_secondary_indexes=[dynamodb.CfnTable.GlobalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb.CfnTable.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb.CfnTable.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    ),
            
                    # the properties below are optional
                    contributor_insights_specification=dynamodb.CfnTable.ContributorInsightsSpecificationProperty(
                        enabled=False
                    ),
                    provisioned_throughput=dynamodb.CfnTable.ProvisionedThroughputProperty(
                        read_capacity_units=123,
                        write_capacity_units=123
                    )
                )],
                import_source_specification=dynamodb.CfnTable.ImportSourceSpecificationProperty(
                    input_format="inputFormat",
                    s3_bucket_source=dynamodb.CfnTable.S3BucketSourceProperty(
                        s3_bucket="s3Bucket",
            
                        # the properties below are optional
                        s3_bucket_owner="s3BucketOwner",
                        s3_key_prefix="s3KeyPrefix"
                    ),
            
                    # the properties below are optional
                    input_compression_type="inputCompressionType",
                    input_format_options=dynamodb.CfnTable.InputFormatOptionsProperty(
                        csv=dynamodb.CfnTable.CsvProperty(
                            delimiter="delimiter",
                            header_list=["headerList"]
                        )
                    )
                ),
                kinesis_stream_specification=dynamodb.CfnTable.KinesisStreamSpecificationProperty(
                    stream_arn="streamArn"
                ),
                local_secondary_indexes=[dynamodb.CfnTable.LocalSecondaryIndexProperty(
                    index_name="indexName",
                    key_schema=[dynamodb.CfnTable.KeySchemaProperty(
                        attribute_name="attributeName",
                        key_type="keyType"
                    )],
                    projection=dynamodb.CfnTable.ProjectionProperty(
                        non_key_attributes=["nonKeyAttributes"],
                        projection_type="projectionType"
                    )
                )],
                point_in_time_recovery_specification=dynamodb.CfnTable.PointInTimeRecoverySpecificationProperty(
                    point_in_time_recovery_enabled=False
                ),
                provisioned_throughput=dynamodb.CfnTable.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                ),
                sse_specification=dynamodb.CfnTable.SSESpecificationProperty(
                    sse_enabled=False,
            
                    # the properties below are optional
                    kms_master_key_id="kmsMasterKeyId",
                    sse_type="sseType"
                ),
                stream_specification=dynamodb.CfnTable.StreamSpecificationProperty(
                    stream_view_type="streamViewType"
                ),
                table_class="tableClass",
                table_name="tableName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_to_live_specification=dynamodb.CfnTable.TimeToLiveSpecificationProperty(
                    attribute_name="attributeName",
                    enabled=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc78bc34bb106a907f40bdbe677d639ee2b61288936dd19cc79b6874f6db2742)
            check_type(argname="argument key_schema", value=key_schema, expected_type=type_hints["key_schema"])
            check_type(argname="argument attribute_definitions", value=attribute_definitions, expected_type=type_hints["attribute_definitions"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument contributor_insights_specification", value=contributor_insights_specification, expected_type=type_hints["contributor_insights_specification"])
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument global_secondary_indexes", value=global_secondary_indexes, expected_type=type_hints["global_secondary_indexes"])
            check_type(argname="argument import_source_specification", value=import_source_specification, expected_type=type_hints["import_source_specification"])
            check_type(argname="argument kinesis_stream_specification", value=kinesis_stream_specification, expected_type=type_hints["kinesis_stream_specification"])
            check_type(argname="argument local_secondary_indexes", value=local_secondary_indexes, expected_type=type_hints["local_secondary_indexes"])
            check_type(argname="argument point_in_time_recovery_specification", value=point_in_time_recovery_specification, expected_type=type_hints["point_in_time_recovery_specification"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument stream_specification", value=stream_specification, expected_type=type_hints["stream_specification"])
            check_type(argname="argument table_class", value=table_class, expected_type=type_hints["table_class"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_to_live_specification", value=time_to_live_specification, expected_type=type_hints["time_to_live_specification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_schema": key_schema,
        }
        if attribute_definitions is not None:
            self._values["attribute_definitions"] = attribute_definitions
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if contributor_insights_specification is not None:
            self._values["contributor_insights_specification"] = contributor_insights_specification
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if global_secondary_indexes is not None:
            self._values["global_secondary_indexes"] = global_secondary_indexes
        if import_source_specification is not None:
            self._values["import_source_specification"] = import_source_specification
        if kinesis_stream_specification is not None:
            self._values["kinesis_stream_specification"] = kinesis_stream_specification
        if local_secondary_indexes is not None:
            self._values["local_secondary_indexes"] = local_secondary_indexes
        if point_in_time_recovery_specification is not None:
            self._values["point_in_time_recovery_specification"] = point_in_time_recovery_specification
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if stream_specification is not None:
            self._values["stream_specification"] = stream_specification
        if table_class is not None:
            self._values["table_class"] = table_class
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags
        if time_to_live_specification is not None:
            self._values["time_to_live_specification"] = time_to_live_specification

    @builtins.property
    def key_schema(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.KeySchemaProperty, _IResolvable_a771d0ef]]]:
        '''Specifies the attributes that make up the primary key for the table.

        The attributes in the ``KeySchema`` property must also be defined in the ``AttributeDefinitions`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-keyschema
        '''
        result = self._values.get("key_schema")
        assert result is not None, "Required property 'key_schema' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.KeySchemaProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def attribute_definitions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.AttributeDefinitionProperty, _IResolvable_a771d0ef]]]]:
        '''A list of attributes that describe the key schema for the table and indexes.

        This property is required to create a DynamoDB table.

        Update requires: `Some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ . Replacement if you edit an existing AttributeDefinition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-attributedefinitions
        '''
        result = self._values.get("attribute_definitions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.AttributeDefinitionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[builtins.str]:
        '''Specify how you are charged for read and write throughput and how you manage capacity.

        Valid values include:

        - ``PROVISIONED`` - We recommend using ``PROVISIONED`` for predictable workloads. ``PROVISIONED`` sets the billing mode to `Provisioned Mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.ProvisionedThroughput.Manual>`_ .
        - ``PAY_PER_REQUEST`` - We recommend using ``PAY_PER_REQUEST`` for unpredictable workloads. ``PAY_PER_REQUEST`` sets the billing mode to `On-Demand Mode <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.OnDemand>`_ .

        If not specified, the default is ``PROVISIONED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-billingmode
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contributor_insights_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.ContributorInsightsSpecificationProperty, _IResolvable_a771d0ef]]:
        '''The settings used to enable or disable CloudWatch Contributor Insights for the specified table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-contributorinsightsspecification
        '''
        result = self._values.get("contributor_insights_specification")
        return typing.cast(typing.Optional[typing.Union[CfnTable.ContributorInsightsSpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Determines if a table is protected from deletion.

        When enabled, the table cannot be deleted by any user or process. This setting is disabled by default. For more information, see `Using deletion protection <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.Basics.html#WorkingWithTables.Basics.DeletionProtection>`_ in the *Amazon DynamoDB Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-deletionprotectionenabled
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def global_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.GlobalSecondaryIndexProperty, _IResolvable_a771d0ef]]]]:
        '''Global secondary indexes to be created on the table. You can create up to 20 global secondary indexes.

        .. epigraph::

           If you update a table to include a new global secondary index, AWS CloudFormation initiates the index creation and then proceeds with the stack update. AWS CloudFormation doesn't wait for the index to complete creation because the backfilling phase can take a long time, depending on the size of the table. You can't use the index or update the table until the index's status is ``ACTIVE`` . You can track its status by using the DynamoDB `DescribeTable <https://docs.aws.amazon.com/cli/latest/reference/dynamodb/describe-table.html>`_ command.

           If you add or delete an index during an update, we recommend that you don't update any other resources. If your stack fails to update and is rolled back while adding a new index, you must manually delete the index.

           Updates are not supported. The following are exceptions:

           - If you update either the contributor insights specification or the provisioned throughput values of global secondary indexes, you can update the table without interruption.
           - You can delete or add one global secondary index without interruption. If you do both in the same update (for example, by changing the index's logical ID), the update fails.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-globalsecondaryindexes
        '''
        result = self._values.get("global_secondary_indexes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.GlobalSecondaryIndexProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def import_source_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.ImportSourceSpecificationProperty, _IResolvable_a771d0ef]]:
        '''Specifies the properties of data being imported from the S3 bucket source to the table.

        .. epigraph::

           If you specify the ``ImportSourceSpecification`` property, and also specify either the ``StreamSpecification`` , the ``TableClass`` property, or the ``DeletionProtectionEnabled`` property, the IAM entity creating/updating stack must have ``UpdateTable`` permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-importsourcespecification
        '''
        result = self._values.get("import_source_specification")
        return typing.cast(typing.Optional[typing.Union[CfnTable.ImportSourceSpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kinesis_stream_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.KinesisStreamSpecificationProperty, _IResolvable_a771d0ef]]:
        '''The Kinesis Data Streams configuration for the specified table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-kinesisstreamspecification
        '''
        result = self._values.get("kinesis_stream_specification")
        return typing.cast(typing.Optional[typing.Union[CfnTable.KinesisStreamSpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def local_secondary_indexes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.LocalSecondaryIndexProperty, _IResolvable_a771d0ef]]]]:
        '''Local secondary indexes to be created on the table.

        You can create up to 5 local secondary indexes. Each index is scoped to a given hash key value. The size of each hash key can be up to 10 gigabytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-localsecondaryindexes
        '''
        result = self._values.get("local_secondary_indexes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.LocalSecondaryIndexProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def point_in_time_recovery_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.PointInTimeRecoverySpecificationProperty, _IResolvable_a771d0ef]]:
        '''The settings used to enable point in time recovery.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-pointintimerecoveryspecification
        '''
        result = self._values.get("point_in_time_recovery_specification")
        return typing.cast(typing.Optional[typing.Union[CfnTable.PointInTimeRecoverySpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.ProvisionedThroughputProperty, _IResolvable_a771d0ef]]:
        '''Throughput for the specified table, which consists of values for ``ReadCapacityUnits`` and ``WriteCapacityUnits`` .

        For more information about the contents of a provisioned throughput structure, see `Amazon DynamoDB Table ProvisionedThroughput <https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ProvisionedThroughput.html>`_ .

        If you set ``BillingMode`` as ``PROVISIONED`` , you must specify this property. If you set ``BillingMode`` as ``PAY_PER_REQUEST`` , you cannot specify this property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-provisionedthroughput
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[typing.Union[CfnTable.ProvisionedThroughputProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.SSESpecificationProperty, _IResolvable_a771d0ef]]:
        '''Specifies the settings to enable server-side encryption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-ssespecification
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[CfnTable.SSESpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def stream_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.StreamSpecificationProperty, _IResolvable_a771d0ef]]:
        '''The settings for the DynamoDB table stream, which capture changes to items stored in the table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-streamspecification
        '''
        result = self._values.get("stream_specification")
        return typing.cast(typing.Optional[typing.Union[CfnTable.StreamSpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def table_class(self) -> typing.Optional[builtins.str]:
        '''The table class of the new table.

        Valid values are ``STANDARD`` and ``STANDARD_INFREQUENT_ACCESS`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tableclass
        '''
        result = self._values.get("table_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''A name for the table.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the table name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def time_to_live_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.TimeToLiveSpecificationProperty, _IResolvable_a771d0ef]]:
        '''Specifies the Time to Live (TTL) settings for the table.

        .. epigraph::

           For detailed information about the limits in DynamoDB, see `Limits in Amazon DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html>`_ in the Amazon DynamoDB Developer Guide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#cfn-dynamodb-table-timetolivespecification
        '''
        result = self._values.get("time_to_live_specification")
        return typing.cast(typing.Optional[typing.Union[CfnTable.TimeToLiveSpecificationProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.EnableScalingProps",
    jsii_struct_bases=[],
    name_mapping={"max_capacity": "maxCapacity", "min_capacity": "minCapacity"},
)
class EnableScalingProps:
    def __init__(self, *, max_capacity: jsii.Number, min_capacity: jsii.Number) -> None:
        '''(experimental) Properties for enabling DynamoDB capacity scaling.

        :param max_capacity: (experimental) Maximum capacity to scale to.
        :param min_capacity: (experimental) Minimum capacity to scale to.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            global_table = dynamodb.Table(self, "Table",
                partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
                replication_regions=["us-east-1", "us-east-2", "us-west-2"],
                billing_mode=dynamodb.BillingMode.PROVISIONED
            )
            
            global_table.auto_scale_write_capacity(
                min_capacity=1,
                max_capacity=10
            ).scale_on_utilization(target_utilization_percent=75)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8fd7d90add35438221014ce0249949bfa9061175978a5cc128f0ff78de8b63)
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_capacity": max_capacity,
            "min_capacity": min_capacity,
        }

    @builtins.property
    def max_capacity(self) -> jsii.Number:
        '''(experimental) Maximum capacity to scale to.

        :stability: experimental
        '''
        result = self._values.get("max_capacity")
        assert result is not None, "Required property 'max_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_capacity(self) -> jsii.Number:
        '''(experimental) Minimum capacity to scale to.

        :stability: experimental
        '''
        result = self._values.get("min_capacity")
        assert result is not None, "Required property 'min_capacity' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnableScalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_dynamodb.IScalableTableAttribute")
class IScalableTableAttribute(typing_extensions.Protocol):
    '''(experimental) Interface for scalable attributes.

    :stability: experimental
    '''

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(
        self,
        id: builtins.str,
        *,
        schedule: _Schedule_c2a5a45d,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''(experimental) Add scheduled scaling for this scaling attribute.

        :param id: -
        :param schedule: (experimental) When to perform this action.
        :param end_time: (experimental) When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: (experimental) The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: (experimental) The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: (experimental) When this scheduled action becomes active. Default: The rule is activate immediately

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="scaleOnUtilization")
    def scale_on_utilization(
        self,
        *,
        target_utilization_percent: jsii.Number,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        policy_name: typing.Optional[builtins.str] = None,
        scale_in_cooldown: typing.Optional[_Duration_070aa057] = None,
        scale_out_cooldown: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) Scale out or in to keep utilization at a given level.

        :param target_utilization_percent: (experimental) Target utilization percentage for the attribute.
        :param disable_scale_in: (experimental) Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: (experimental) A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: (experimental) Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: (experimental) Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency

        :stability: experimental
        '''
        ...


class _IScalableTableAttributeProxy:
    '''(experimental) Interface for scalable attributes.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_dynamodb.IScalableTableAttribute"

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(
        self,
        id: builtins.str,
        *,
        schedule: _Schedule_c2a5a45d,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''(experimental) Add scheduled scaling for this scaling attribute.

        :param id: -
        :param schedule: (experimental) When to perform this action.
        :param end_time: (experimental) When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: (experimental) The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: (experimental) The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: (experimental) When this scheduled action becomes active. Default: The rule is activate immediately

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e8d8fe8957c47430011940e40c90ff53f8590450724e598342eab9a75a9cf0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        actions = _ScalingSchedule_6c3fc38f(
            schedule=schedule,
            end_time=end_time,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            start_time=start_time,
        )

        return typing.cast(None, jsii.invoke(self, "scaleOnSchedule", [id, actions]))

    @jsii.member(jsii_name="scaleOnUtilization")
    def scale_on_utilization(
        self,
        *,
        target_utilization_percent: jsii.Number,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        policy_name: typing.Optional[builtins.str] = None,
        scale_in_cooldown: typing.Optional[_Duration_070aa057] = None,
        scale_out_cooldown: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) Scale out or in to keep utilization at a given level.

        :param target_utilization_percent: (experimental) Target utilization percentage for the attribute.
        :param disable_scale_in: (experimental) Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: (experimental) A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: (experimental) Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: (experimental) Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency

        :stability: experimental
        '''
        props = UtilizationScalingProps(
            target_utilization_percent=target_utilization_percent,
            disable_scale_in=disable_scale_in,
            policy_name=policy_name,
            scale_in_cooldown=scale_in_cooldown,
            scale_out_cooldown=scale_out_cooldown,
        )

        return typing.cast(None, jsii.invoke(self, "scaleOnUtilization", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IScalableTableAttribute).__jsii_proxy_class__ = lambda : _IScalableTableAttributeProxy


@jsii.interface(jsii_type="monocdk.aws_dynamodb.ITable")
class ITable(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) An interface that represents a DynamoDB Table - either created with the CDK, or an existing one.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''(experimental) Arn of the dynamodb table.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) Table name of the dynamodb table.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Optional KMS encryption key associated with this table.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tableStreamArn")
    def table_stream_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN of the table's stream, if there is one.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement associated with this table to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:PutItem", "dynamodb:GetItem", ...).

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantFullAccess")
    def grant_full_access(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits all DynamoDB operations ("dynamodb:*") to an IAM principal.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadData")
    def grant_read_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all data read operations from this table: BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWriteData")
    def grant_read_write_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal to all data read/write operations to this table.

        BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan,
        BatchWriteItem, PutItem, UpdateItem, DeleteItem

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantStream")
    def grant_stream(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement associated with this table's stream to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:DescribeStream", "dynamodb:GetRecords", ...).

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantStreamRead")
    def grant_stream_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all stream data read operations for this table's stream: DescribeStream, GetRecords, GetShardIterator, ListStreams.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantTableListStreams")
    def grant_table_list_streams(
        self,
        grantee: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM Principal to list streams attached to current dynamodb table.

        :param grantee: The principal (no-op if undefined).

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWriteData")
    def grant_write_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all data write operations to this table: BatchWriteItem, PutItem, UpdateItem, DeleteItem.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of Errors executing all Lambdas.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricConditionalCheckFailedRequests")
    def metric_conditional_check_failed_requests(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the conditional check failed requests.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricConsumedReadCapacityUnits")
    def metric_consumed_read_capacity_units(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the consumed read capacity units.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricConsumedWriteCapacityUnits")
    def metric_consumed_write_capacity_units(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the consumed write capacity units.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSuccessfulRequestLatency")
    def metric_successful_request_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the successful request latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSystemErrors")
    def metric_system_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the system errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :deprecated: use ``metricSystemErrorsForOperations``

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricSystemErrorsForOperations")
    def metric_system_errors_for_operations(
        self,
        *,
        operations: typing.Optional[typing.Sequence["Operation"]] = None,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _IMetric_5db43d61:
        '''(experimental) Metric for the system errors this table.

        :param operations: (experimental) The operations to apply the metric to. Default: - All operations available by DynamoDB tables will be considered.
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricThrottledRequests")
    def metric_throttled_requests(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for throttled requests.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricUserErrors")
    def metric_user_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the user errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...


class _ITableProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) An interface that represents a DynamoDB Table - either created with the CDK, or an existing one.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_dynamodb.ITable"

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''(experimental) Arn of the dynamodb table.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) Table name of the dynamodb table.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Optional KMS encryption key associated with this table.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="tableStreamArn")
    def table_stream_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN of the table's stream, if there is one.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableStreamArn"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement associated with this table to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:PutItem", "dynamodb:GetItem", ...).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7b2607f481000408ca0428572818f5c6bdbb9fed6e81115c2dd3f9116bb103)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantFullAccess")
    def grant_full_access(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits all DynamoDB operations ("dynamodb:*") to an IAM principal.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60032d7de59b0cce743f6a33489466642fdf7a4772fe05afc645346a4bb8f797)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantFullAccess", [grantee]))

    @jsii.member(jsii_name="grantReadData")
    def grant_read_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all data read operations from this table: BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a72c99aa6908ffa8e732697a82fbc672394ef9d167d85955e3405245eccc2f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadData", [grantee]))

    @jsii.member(jsii_name="grantReadWriteData")
    def grant_read_write_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal to all data read/write operations to this table.

        BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan,
        BatchWriteItem, PutItem, UpdateItem, DeleteItem

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1c8330ec43f14a6c708e78e5242df9d7c07c7427e915166e6fcc6256e558bb)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWriteData", [grantee]))

    @jsii.member(jsii_name="grantStream")
    def grant_stream(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement associated with this table's stream to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:DescribeStream", "dynamodb:GetRecords", ...).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3409f2a3618c344be6d9f7f4ff98169acc4e590904d7a92dc30259055dafc6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantStream", [grantee, *actions]))

    @jsii.member(jsii_name="grantStreamRead")
    def grant_stream_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all stream data read operations for this table's stream: DescribeStream, GetRecords, GetShardIterator, ListStreams.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682e1b23ead29876f6b964aa061261d32858b9192b31d8ad490d9393bbaa6e33)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantStreamRead", [grantee]))

    @jsii.member(jsii_name="grantTableListStreams")
    def grant_table_list_streams(
        self,
        grantee: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM Principal to list streams attached to current dynamodb table.

        :param grantee: The principal (no-op if undefined).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b83ef0843e15bfa856c87b3b928d384e2f42b7910f18022dfe2e355dd8f849)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantTableListStreams", [grantee]))

    @jsii.member(jsii_name="grantWriteData")
    def grant_write_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all data write operations to this table: BatchWriteItem, PutItem, UpdateItem, DeleteItem.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45419850d951c8e2c92a4ef018d4b41da248670ab1c95483faed69c9df2f4c5)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWriteData", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of Errors executing all Lambdas.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703cb9c708e6170cfc4fc98cc092f234f243919de301984bbacbd47b23dfb7ef)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricConditionalCheckFailedRequests")
    def metric_conditional_check_failed_requests(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the conditional check failed requests.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricConditionalCheckFailedRequests", [props]))

    @jsii.member(jsii_name="metricConsumedReadCapacityUnits")
    def metric_consumed_read_capacity_units(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the consumed read capacity units.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricConsumedReadCapacityUnits", [props]))

    @jsii.member(jsii_name="metricConsumedWriteCapacityUnits")
    def metric_consumed_write_capacity_units(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the consumed write capacity units.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricConsumedWriteCapacityUnits", [props]))

    @jsii.member(jsii_name="metricSuccessfulRequestLatency")
    def metric_successful_request_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the successful request latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSuccessfulRequestLatency", [props]))

    @jsii.member(jsii_name="metricSystemErrors")
    def metric_system_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the system errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :deprecated: use ``metricSystemErrorsForOperations``

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSystemErrors", [props]))

    @jsii.member(jsii_name="metricSystemErrorsForOperations")
    def metric_system_errors_for_operations(
        self,
        *,
        operations: typing.Optional[typing.Sequence["Operation"]] = None,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _IMetric_5db43d61:
        '''(experimental) Metric for the system errors this table.

        :param operations: (experimental) The operations to apply the metric to. Default: - All operations available by DynamoDB tables will be considered.
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = SystemErrorsForOperationsMetricOptions(
            operations=operations,
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_IMetric_5db43d61, jsii.invoke(self, "metricSystemErrorsForOperations", [props]))

    @jsii.member(jsii_name="metricThrottledRequests")
    def metric_throttled_requests(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for throttled requests.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricThrottledRequests", [props]))

    @jsii.member(jsii_name="metricUserErrors")
    def metric_user_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the user errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricUserErrors", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITable).__jsii_proxy_class__ = lambda : _ITableProxy


@jsii.enum(jsii_type="monocdk.aws_dynamodb.Operation")
class Operation(enum.Enum):
    '''(experimental) Supported DynamoDB table operations.

    :stability: experimental
    '''

    GET_ITEM = "GET_ITEM"
    '''(experimental) GetItem.

    :stability: experimental
    '''
    BATCH_GET_ITEM = "BATCH_GET_ITEM"
    '''(experimental) BatchGetItem.

    :stability: experimental
    '''
    SCAN = "SCAN"
    '''(experimental) Scan.

    :stability: experimental
    '''
    QUERY = "QUERY"
    '''(experimental) Query.

    :stability: experimental
    '''
    GET_RECORDS = "GET_RECORDS"
    '''(experimental) GetRecords.

    :stability: experimental
    '''
    PUT_ITEM = "PUT_ITEM"
    '''(experimental) PutItem.

    :stability: experimental
    '''
    DELETE_ITEM = "DELETE_ITEM"
    '''(experimental) DeleteItem.

    :stability: experimental
    '''
    UPDATE_ITEM = "UPDATE_ITEM"
    '''(experimental) UpdateItem.

    :stability: experimental
    '''
    BATCH_WRITE_ITEM = "BATCH_WRITE_ITEM"
    '''(experimental) BatchWriteItem.

    :stability: experimental
    '''
    TRANSACT_WRITE_ITEMS = "TRANSACT_WRITE_ITEMS"
    '''(experimental) TransactWriteItems.

    :stability: experimental
    '''
    TRANSACT_GET_ITEMS = "TRANSACT_GET_ITEMS"
    '''(experimental) TransactGetItems.

    :stability: experimental
    '''
    EXECUTE_TRANSACTION = "EXECUTE_TRANSACTION"
    '''(experimental) ExecuteTransaction.

    :stability: experimental
    '''
    BATCH_EXECUTE_STATEMENT = "BATCH_EXECUTE_STATEMENT"
    '''(experimental) BatchExecuteStatement.

    :stability: experimental
    '''
    EXECUTE_STATEMENT = "EXECUTE_STATEMENT"
    '''(experimental) ExecuteStatement.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_dynamodb.ProjectionType")
class ProjectionType(enum.Enum):
    '''(experimental) The set of attributes that are projected into the index.

    :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Projection.html
    :stability: experimental
    '''

    KEYS_ONLY = "KEYS_ONLY"
    '''(experimental) Only the index and primary keys are projected into the index.

    :stability: experimental
    '''
    INCLUDE = "INCLUDE"
    '''(experimental) Only the specified table attributes are projected into the index.

    The list of projected attributes is in ``nonKeyAttributes``.

    :stability: experimental
    '''
    ALL = "ALL"
    '''(experimental) All of the table attributes are projected into the index.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.SchemaOptions",
    jsii_struct_bases=[],
    name_mapping={"partition_key": "partitionKey", "sort_key": "sortKey"},
)
class SchemaOptions:
    def __init__(
        self,
        *,
        partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
        sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Represents the table schema attributes.

        :param partition_key: (experimental) Partition key attribute definition.
        :param sort_key: (experimental) Sort key attribute definition. Default: no sort key

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # table: dynamodb.Table
            
            schema = table.schema()
            partition_key = schema.partition_key
            sort_key = schema.sort_key
        '''
        if isinstance(partition_key, dict):
            partition_key = Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4af3894bd36cd682954530649231759a53e3e5a7a272a17a3b1608b8e8187d8)
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            check_type(argname="argument sort_key", value=sort_key, expected_type=type_hints["sort_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }
        if sort_key is not None:
            self._values["sort_key"] = sort_key

    @builtins.property
    def partition_key(self) -> Attribute:
        '''(experimental) Partition key attribute definition.

        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(Attribute, result)

    @builtins.property
    def sort_key(self) -> typing.Optional[Attribute]:
        '''(experimental) Sort key attribute definition.

        :default: no sort key

        :stability: experimental
        '''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional[Attribute], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.SecondaryIndexProps",
    jsii_struct_bases=[],
    name_mapping={
        "index_name": "indexName",
        "non_key_attributes": "nonKeyAttributes",
        "projection_type": "projectionType",
    },
)
class SecondaryIndexProps:
    def __init__(
        self,
        *,
        index_name: builtins.str,
        non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        projection_type: typing.Optional[ProjectionType] = None,
    ) -> None:
        '''(experimental) Properties for a secondary index.

        :param index_name: (experimental) The name of the secondary index.
        :param non_key_attributes: (experimental) The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: (experimental) The set of attributes that are projected into the secondary index. Default: ALL

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dynamodb as dynamodb
            
            secondary_index_props = dynamodb.SecondaryIndexProps(
                index_name="indexName",
            
                # the properties below are optional
                non_key_attributes=["nonKeyAttributes"],
                projection_type=dynamodb.ProjectionType.KEYS_ONLY
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2398c4d8a8092a0501d854033bf87064409616a1a27eb43cb06380ec90be295)
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument non_key_attributes", value=non_key_attributes, expected_type=type_hints["non_key_attributes"])
            check_type(argname="argument projection_type", value=projection_type, expected_type=type_hints["projection_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_name": index_name,
        }
        if non_key_attributes is not None:
            self._values["non_key_attributes"] = non_key_attributes
        if projection_type is not None:
            self._values["projection_type"] = projection_type

    @builtins.property
    def index_name(self) -> builtins.str:
        '''(experimental) The name of the secondary index.

        :stability: experimental
        '''
        result = self._values.get("index_name")
        assert result is not None, "Required property 'index_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def non_key_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The non-key attributes that are projected into the secondary index.

        :default: - No additional attributes

        :stability: experimental
        '''
        result = self._values.get("non_key_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def projection_type(self) -> typing.Optional[ProjectionType]:
        '''(experimental) The set of attributes that are projected into the secondary index.

        :default: ALL

        :stability: experimental
        '''
        result = self._values.get("projection_type")
        return typing.cast(typing.Optional[ProjectionType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecondaryIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_dynamodb.StreamViewType")
class StreamViewType(enum.Enum):
    '''(experimental) When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

    :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_StreamSpecification.html
    :stability: experimental
    '''

    NEW_IMAGE = "NEW_IMAGE"
    '''(experimental) The entire item, as it appears after it was modified, is written to the stream.

    :stability: experimental
    '''
    OLD_IMAGE = "OLD_IMAGE"
    '''(experimental) The entire item, as it appeared before it was modified, is written to the stream.

    :stability: experimental
    '''
    NEW_AND_OLD_IMAGES = "NEW_AND_OLD_IMAGES"
    '''(experimental) Both the new and the old item images of the item are written to the stream.

    :stability: experimental
    '''
    KEYS_ONLY = "KEYS_ONLY"
    '''(experimental) Only the key attributes of the modified item are written to the stream.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.SystemErrorsForOperationsMetricOptions",
    jsii_struct_bases=[_MetricOptions_1c185ae8],
    name_mapping={
        "account": "account",
        "color": "color",
        "dimensions": "dimensions",
        "dimensions_map": "dimensionsMap",
        "label": "label",
        "period": "period",
        "region": "region",
        "statistic": "statistic",
        "unit": "unit",
        "operations": "operations",
    },
)
class SystemErrorsForOperationsMetricOptions(_MetricOptions_1c185ae8):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
        operations: typing.Optional[typing.Sequence[Operation]] = None,
    ) -> None:
        '''(experimental) Options for configuring a system errors metric that considers multiple operations.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param operations: (experimental) The operations to apply the metric to. Default: - All operations available by DynamoDB tables will be considered.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_cloudwatch as cloudwatch
            from monocdk import aws_dynamodb as dynamodb
            
            # dimensions: Any
            # duration: monocdk.Duration
            
            system_errors_for_operations_metric_options = dynamodb.SystemErrorsForOperationsMetricOptions(
                account="account",
                color="color",
                dimensions={
                    "dimensions_key": dimensions
                },
                dimensions_map={
                    "dimensions_map_key": "dimensionsMap"
                },
                label="label",
                operations=[dynamodb.Operation.GET_ITEM],
                period=duration,
                region="region",
                statistic="statistic",
                unit=cloudwatch.Unit.SECONDS
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2df1695ef53ce52e27e8b9d8d6a5fbbfc4c80ad0017f1e3183882aae3219a7c)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument dimensions_map", value=dimensions_map, expected_type=type_hints["dimensions_map"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if color is not None:
            self._values["color"] = color
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if dimensions_map is not None:
            self._values["dimensions_map"] = dimensions_map
        if label is not None:
            self._values["label"] = label
        if period is not None:
            self._values["period"] = period
        if region is not None:
            self._values["region"] = region
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit
        if operations is not None:
            self._values["operations"] = operations

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account which this metric comes from.

        :default: - Deployment account.

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.

        :default: - Automatic color

        :stability: experimental
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(deprecated) Dimensions of the metric.

        :default: - No dimensions.

        :deprecated: Use 'dimensionsMap' instead.

        :stability: deprecated
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def dimensions_map(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Dimensions of the metric.

        :default: - No dimensions.

        :stability: experimental
        '''
        result = self._values.get("dimensions_map")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(experimental) Label for this metric when added to a Graph in a Dashboard.

        You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_
        to show summary information about the entire displayed time series
        in the legend. For example, if you use::

           [max: ${MAX}] MyMetric

        As the metric label, the maximum value in the visible range will
        be shown next to the time series name in the graph's legend.

        :default: - No label

        :stability: experimental
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The period over which the specified statistic is applied.

        :default: Duration.minutes(5)

        :stability: experimental
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region which this metric comes from.

        :default: - Deployment region.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''(experimental) What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        :default: Average

        :stability: experimental
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unit(self) -> typing.Optional[_Unit_113c79f9]:
        '''(experimental) Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        The default is to use all matric datums in the stream, regardless of unit,
        which is recommended in nearly all cases.

        CloudWatch does not honor this property for graphs.

        :default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[_Unit_113c79f9], result)

    @builtins.property
    def operations(self) -> typing.Optional[typing.List[Operation]]:
        '''(experimental) The operations to apply the metric to.

        :default: - All operations available by DynamoDB tables will be considered.

        :stability: experimental
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.List[Operation]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemErrorsForOperationsMetricOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITable)
class Table(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dynamodb.Table",
):
    '''(experimental) Provides a DynamoDB table.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        global_table = dynamodb.Table(self, "Table",
            partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            replication_regions=["us-east-1", "us-east-2", "us-west-2"],
            billing_mode=dynamodb.BillingMode.PROVISIONED
        )
        
        global_table.auto_scale_write_capacity(
            min_capacity=1,
            max_capacity=10
        ).scale_on_utilization(target_utilization_percent=75)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        kinesis_stream: typing.Optional[_IStream_14c6ec7f] = None,
        table_name: typing.Optional[builtins.str] = None,
        billing_mode: typing.Optional[BillingMode] = None,
        contributor_insights_enabled: typing.Optional[builtins.bool] = None,
        encryption: typing.Optional["TableEncryption"] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        point_in_time_recovery: typing.Optional[builtins.bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_timeout: typing.Optional[_Duration_070aa057] = None,
        server_side_encryption: typing.Optional[builtins.bool] = None,
        stream: typing.Optional[StreamViewType] = None,
        table_class: typing.Optional["TableClass"] = None,
        time_to_live_attribute: typing.Optional[builtins.str] = None,
        wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
        sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param kinesis_stream: (experimental) Kinesis Data Stream to capture item-level changes for the table. Default: - no Kinesis Data Stream
        :param table_name: (experimental) Enforces a particular physical table name. Default: 
        :param billing_mode: (experimental) Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param contributor_insights_enabled: (experimental) Whether CloudWatch contributor insights is enabled. Default: false
        :param encryption: (experimental) Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. .. epigraph:: **NOTE**: if you set this to ``CUSTOMER_MANAGED`` and ``encryptionKey`` is not specified, the key that the Tablet generates for you will be created with default permissions. If you are using CDKv2, these permissions will be sufficient to enable the key for use with DynamoDB tables. If you are using CDKv1, make sure the feature flag ``@aws-cdk/aws-kms:defaultKeyPolicies`` is set to ``true`` in your ``cdk.json``. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: (experimental) External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: (experimental) Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: (experimental) The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: (experimental) The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: (experimental) Regions where replica tables will be created. Default: - no replica tables are created
        :param replication_timeout: (experimental) The timeout for a table replication operation in a single region. Default: Duration.minutes(30)
        :param server_side_encryption: (deprecated) Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param stream: (experimental) When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param table_class: (experimental) Specify the table class. Default: STANDARD
        :param time_to_live_attribute: (experimental) The name of TTL attribute. Default: - TTL is disabled
        :param wait_for_replication_to_finish: (experimental) Indicates whether CloudFormation stack waits for replication to finish. If set to false, the CloudFormation resource will mark the resource as created and replication will be completed asynchronously. This property is ignored if replicationRegions property is not set. DO NOT UNSET this property if adding/removing multiple replicationRegions in one deployment, as CloudFormation only supports one region replication at a time. CDK overcomes this limitation by waiting for replication to finish before starting new replicationRegion. Default: true
        :param write_capacity: (experimental) The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param partition_key: (experimental) Partition key attribute definition.
        :param sort_key: (experimental) Sort key attribute definition. Default: no sort key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea29923c4ccaf6679ececf63cf2b8daf28911ddb13fd632abced46270cafdfc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TableProps(
            kinesis_stream=kinesis_stream,
            table_name=table_name,
            billing_mode=billing_mode,
            contributor_insights_enabled=contributor_insights_enabled,
            encryption=encryption,
            encryption_key=encryption_key,
            point_in_time_recovery=point_in_time_recovery,
            read_capacity=read_capacity,
            removal_policy=removal_policy,
            replication_regions=replication_regions,
            replication_timeout=replication_timeout,
            server_side_encryption=server_side_encryption,
            stream=stream,
            table_class=table_class,
            time_to_live_attribute=time_to_live_attribute,
            wait_for_replication_to_finish=wait_for_replication_to_finish,
            write_capacity=write_capacity,
            partition_key=partition_key,
            sort_key=sort_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTableArn")
    @builtins.classmethod
    def from_table_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        table_arn: builtins.str,
    ) -> ITable:
        '''(experimental) Creates a Table construct that represents an external table via table arn.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param table_arn: The table's ARN.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5c07d63555371d61b654b59d911d534e33095941a709ab5cb43dfba9a97c77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
        return typing.cast(ITable, jsii.sinvoke(cls, "fromTableArn", [scope, id, table_arn]))

    @jsii.member(jsii_name="fromTableAttributes")
    @builtins.classmethod
    def from_table_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        global_indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
        table_arn: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
        table_stream_arn: typing.Optional[builtins.str] = None,
    ) -> ITable:
        '''(experimental) Creates a Table construct that represents an external table.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param encryption_key: (experimental) KMS encryption key, if this table uses a customer-managed encryption key. Default: - no key
        :param global_indexes: (experimental) The name of the global indexes set for this Table. Note that you need to set either this property, or {@link localIndexes}, if you want methods like grantReadData() to grant permissions for indexes as well as the table itself. Default: - no global indexes
        :param local_indexes: (experimental) The name of the local indexes set for this Table. Note that you need to set either this property, or {@link globalIndexes}, if you want methods like grantReadData() to grant permissions for indexes as well as the table itself. Default: - no local indexes
        :param table_arn: (experimental) The ARN of the dynamodb table. One of this, or {@link tableName}, is required. Default: - no table arn
        :param table_name: (experimental) The table name of the dynamodb table. One of this, or {@link tableArn}, is required. Default: - no table name
        :param table_stream_arn: (experimental) The ARN of the table's stream. Default: - no table stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980d657cde0582520a272daa50682b09c00dd359f25116d406e948c41a2c8b03)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = TableAttributes(
            encryption_key=encryption_key,
            global_indexes=global_indexes,
            local_indexes=local_indexes,
            table_arn=table_arn,
            table_name=table_name,
            table_stream_arn=table_stream_arn,
        )

        return typing.cast(ITable, jsii.sinvoke(cls, "fromTableAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromTableName")
    @builtins.classmethod
    def from_table_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        table_name: builtins.str,
    ) -> ITable:
        '''(experimental) Creates a Table construct that represents an external table via table name.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param table_name: The table's name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595569c990aa2292a7db1b0d5695312a6ab81ffeb3c61aaef4913998f0883c35)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        return typing.cast(ITable, jsii.sinvoke(cls, "fromTableName", [scope, id, table_name]))

    @jsii.member(jsii_name="grantListStreams")
    @builtins.classmethod
    def grant_list_streams(cls, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(deprecated) Permits an IAM Principal to list all DynamoDB Streams.

        :param grantee: The principal (no-op if undefined).

        :deprecated: Use {@link #grantTableListStreams} for more granular permission

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c61194dced99002b7e63d7e65319a2de58e95d7bdbc3ea6255294218d9b572)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.sinvoke(cls, "grantListStreams", [grantee]))

    @jsii.member(jsii_name="addGlobalSecondaryIndex")
    def add_global_secondary_index(
        self,
        *,
        read_capacity: typing.Optional[jsii.Number] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        index_name: builtins.str,
        non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        projection_type: typing.Optional[ProjectionType] = None,
        partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
        sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Add a global secondary index of table.

        :param read_capacity: (experimental) The read capacity for the global secondary index. Can only be provided if table billingMode is Provisioned or undefined. Default: 5
        :param write_capacity: (experimental) The write capacity for the global secondary index. Can only be provided if table billingMode is Provisioned or undefined. Default: 5
        :param index_name: (experimental) The name of the secondary index.
        :param non_key_attributes: (experimental) The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: (experimental) The set of attributes that are projected into the secondary index. Default: ALL
        :param partition_key: (experimental) Partition key attribute definition.
        :param sort_key: (experimental) Sort key attribute definition. Default: no sort key

        :stability: experimental
        '''
        props = GlobalSecondaryIndexProps(
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            index_name=index_name,
            non_key_attributes=non_key_attributes,
            projection_type=projection_type,
            partition_key=partition_key,
            sort_key=sort_key,
        )

        return typing.cast(None, jsii.invoke(self, "addGlobalSecondaryIndex", [props]))

    @jsii.member(jsii_name="addLocalSecondaryIndex")
    def add_local_secondary_index(
        self,
        *,
        sort_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
        index_name: builtins.str,
        non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        projection_type: typing.Optional[ProjectionType] = None,
    ) -> None:
        '''(experimental) Add a local secondary index of table.

        :param sort_key: (experimental) The attribute of a sort key for the local secondary index.
        :param index_name: (experimental) The name of the secondary index.
        :param non_key_attributes: (experimental) The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: (experimental) The set of attributes that are projected into the secondary index. Default: ALL

        :stability: experimental
        '''
        props = LocalSecondaryIndexProps(
            sort_key=sort_key,
            index_name=index_name,
            non_key_attributes=non_key_attributes,
            projection_type=projection_type,
        )

        return typing.cast(None, jsii.invoke(self, "addLocalSecondaryIndex", [props]))

    @jsii.member(jsii_name="autoScaleGlobalSecondaryIndexReadCapacity")
    def auto_scale_global_secondary_index_read_capacity(
        self,
        index_name: builtins.str,
        *,
        max_capacity: jsii.Number,
        min_capacity: jsii.Number,
    ) -> IScalableTableAttribute:
        '''(experimental) Enable read capacity scaling for the given GSI.

        :param index_name: -
        :param max_capacity: (experimental) Maximum capacity to scale to.
        :param min_capacity: (experimental) Minimum capacity to scale to.

        :return: An object to configure additional AutoScaling settings for this attribute

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a095b69d37faa53bb5a73051c54ab695bd05b8545a5e440aa72ebfb28a38e3)
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
        props = EnableScalingProps(
            max_capacity=max_capacity, min_capacity=min_capacity
        )

        return typing.cast(IScalableTableAttribute, jsii.invoke(self, "autoScaleGlobalSecondaryIndexReadCapacity", [index_name, props]))

    @jsii.member(jsii_name="autoScaleGlobalSecondaryIndexWriteCapacity")
    def auto_scale_global_secondary_index_write_capacity(
        self,
        index_name: builtins.str,
        *,
        max_capacity: jsii.Number,
        min_capacity: jsii.Number,
    ) -> IScalableTableAttribute:
        '''(experimental) Enable write capacity scaling for the given GSI.

        :param index_name: -
        :param max_capacity: (experimental) Maximum capacity to scale to.
        :param min_capacity: (experimental) Minimum capacity to scale to.

        :return: An object to configure additional AutoScaling settings for this attribute

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c0f431c663f1118d9bffa12428df7bdcfb3cdd5cdf5c0ebe3361b16ae988d1)
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
        props = EnableScalingProps(
            max_capacity=max_capacity, min_capacity=min_capacity
        )

        return typing.cast(IScalableTableAttribute, jsii.invoke(self, "autoScaleGlobalSecondaryIndexWriteCapacity", [index_name, props]))

    @jsii.member(jsii_name="autoScaleReadCapacity")
    def auto_scale_read_capacity(
        self,
        *,
        max_capacity: jsii.Number,
        min_capacity: jsii.Number,
    ) -> IScalableTableAttribute:
        '''(experimental) Enable read capacity scaling for this table.

        :param max_capacity: (experimental) Maximum capacity to scale to.
        :param min_capacity: (experimental) Minimum capacity to scale to.

        :return: An object to configure additional AutoScaling settings

        :stability: experimental
        '''
        props = EnableScalingProps(
            max_capacity=max_capacity, min_capacity=min_capacity
        )

        return typing.cast(IScalableTableAttribute, jsii.invoke(self, "autoScaleReadCapacity", [props]))

    @jsii.member(jsii_name="autoScaleWriteCapacity")
    def auto_scale_write_capacity(
        self,
        *,
        max_capacity: jsii.Number,
        min_capacity: jsii.Number,
    ) -> IScalableTableAttribute:
        '''(experimental) Enable write capacity scaling for this table.

        :param max_capacity: (experimental) Maximum capacity to scale to.
        :param min_capacity: (experimental) Minimum capacity to scale to.

        :return: An object to configure additional AutoScaling settings for this attribute

        :stability: experimental
        '''
        props = EnableScalingProps(
            max_capacity=max_capacity, min_capacity=min_capacity
        )

        return typing.cast(IScalableTableAttribute, jsii.invoke(self, "autoScaleWriteCapacity", [props]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement associated with this table to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:PutItem", "dynamodb:GetItem", ...).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b0b2130c10ca06ef0313012d738fe5cb717fac1ab57b35f09cf285bd38339d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantFullAccess")
    def grant_full_access(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits all DynamoDB operations ("dynamodb:*") to an IAM principal.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e57f6316eeaa5af8316fcc3679968ea578aa2c98f59bc3f8fdbdd9b23ded5f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantFullAccess", [grantee]))

    @jsii.member(jsii_name="grantReadData")
    def grant_read_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all data read operations from this table: BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan, DescribeTable.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f98f6a698f48f5de9f786d3e782d94e03f19b475e1aa341df7a660933d88503)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadData", [grantee]))

    @jsii.member(jsii_name="grantReadWriteData")
    def grant_read_write_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal to all data read/write operations to this table.

        BatchGetItem, GetRecords, GetShardIterator, Query, GetItem, Scan,
        BatchWriteItem, PutItem, UpdateItem, DeleteItem, DescribeTable

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f294325b8a881305f7a7764ec025316493b813eed9536133957dadcdb51c02)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWriteData", [grantee]))

    @jsii.member(jsii_name="grantStream")
    def grant_stream(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement associated with this table's stream to an IAM principal's policy.

        If ``encryptionKey`` is present, appropriate grants to the key needs to be added
        separately using the ``table.encryptionKey.grant*`` methods.

        :param grantee: The principal (no-op if undefined).
        :param actions: The set of actions to allow (i.e. "dynamodb:DescribeStream", "dynamodb:GetRecords", ...).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d07ff8771a4839c2221a01140f69e39241e25ac7deb1a681054334419bdc378)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantStream", [grantee, *actions]))

    @jsii.member(jsii_name="grantStreamRead")
    def grant_stream_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all stream data read operations for this table's stream: DescribeStream, GetRecords, GetShardIterator, ListStreams.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ace47aecbb9f1270afb7345eb951fc887108e79a5e918af72c627d5eecf6499)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantStreamRead", [grantee]))

    @jsii.member(jsii_name="grantTableListStreams")
    def grant_table_list_streams(
        self,
        grantee: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM Principal to list streams attached to current dynamodb table.

        :param grantee: The principal (no-op if undefined).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75e0142b4bb76502b18a0bff91e4ebff82c6783fecae351b4cb9061db6cd523)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantTableListStreams", [grantee]))

    @jsii.member(jsii_name="grantWriteData")
    def grant_write_data(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM principal all data write operations to this table: BatchWriteItem, PutItem, UpdateItem, DeleteItem, DescribeTable.

        Appropriate grants will also be added to the customer-managed KMS key
        if one was configured.

        :param grantee: The principal to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a40174682421a0a672d3c91e86c55d631fc79e37f4cfb58812e3199f392ee1)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWriteData", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this Table.

        By default, the metric will be calculated as a sum over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5add888be5b7ec8e0343bb052fb0e9560b78e32215fa8a7bdcb6d58abbe486)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricConditionalCheckFailedRequests")
    def metric_conditional_check_failed_requests(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the conditional check failed requests this table.

        By default, the metric will be calculated as a sum over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricConditionalCheckFailedRequests", [props]))

    @jsii.member(jsii_name="metricConsumedReadCapacityUnits")
    def metric_consumed_read_capacity_units(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the consumed read capacity units this table.

        By default, the metric will be calculated as a sum over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricConsumedReadCapacityUnits", [props]))

    @jsii.member(jsii_name="metricConsumedWriteCapacityUnits")
    def metric_consumed_write_capacity_units(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the consumed write capacity units this table.

        By default, the metric will be calculated as a sum over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricConsumedWriteCapacityUnits", [props]))

    @jsii.member(jsii_name="metricSuccessfulRequestLatency")
    def metric_successful_request_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the successful request latency this table.

        By default, the metric will be calculated as an average over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSuccessfulRequestLatency", [props]))

    @jsii.member(jsii_name="metricSystemErrors")
    def metric_system_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the system errors this table.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :deprecated: use ``metricSystemErrorsForOperations``.

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSystemErrors", [props]))

    @jsii.member(jsii_name="metricSystemErrorsForOperations")
    def metric_system_errors_for_operations(
        self,
        *,
        operations: typing.Optional[typing.Sequence[Operation]] = None,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _IMetric_5db43d61:
        '''(experimental) Metric for the system errors this table.

        This will sum errors across all possible operations.
        Note that by default, each individual metric will be calculated as a sum over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param operations: (experimental) The operations to apply the metric to. Default: - All operations available by DynamoDB tables will be considered.
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = SystemErrorsForOperationsMetricOptions(
            operations=operations,
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_IMetric_5db43d61, jsii.invoke(self, "metricSystemErrorsForOperations", [props]))

    @jsii.member(jsii_name="metricThrottledRequests")
    def metric_throttled_requests(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) How many requests are throttled on this table.

        Default: sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :deprecated: Do not use this function. It returns an invalid metric. Use ``metricThrottledRequestsForOperation`` instead.

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricThrottledRequests", [props]))

    @jsii.member(jsii_name="metricThrottledRequestsForOperation")
    def metric_throttled_requests_for_operation(
        self,
        operation: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) How many requests are throttled on this table, for the given operation.

        Default: sum over 5 minutes

        :param operation: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a6d02c1dd045f47b1691ceb9e29ed5d882d80600ea8f0f04347c1a53eb28e0)
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricThrottledRequestsForOperation", [operation, props]))

    @jsii.member(jsii_name="metricUserErrors")
    def metric_user_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the user errors.

        Note that this metric reports user errors across all
        the tables in the account and region the table resides in.

        By default, the metric will be calculated as a sum over a period of 5 minutes.
        You can customize this by using the ``statistic`` and ``period`` properties.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricUserErrors", [props]))

    @jsii.member(jsii_name="schema")
    def schema(self, index_name: typing.Optional[builtins.str] = None) -> SchemaOptions:
        '''(experimental) Get schema attributes of table or index.

        :param index_name: -

        :return: Schema of table or index.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be525c1780cb31b87140c8aa5629003cb7b6c8b45b931822540d6b8c8bdc6917)
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
        return typing.cast(SchemaOptions, jsii.invoke(self, "schema", [index_name]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the table construct.

        :return: an array of validation error message

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="hasIndex")
    def _has_index(self) -> builtins.bool:
        '''(experimental) Whether this table has indexes.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "hasIndex"))

    @builtins.property
    @jsii.member(jsii_name="regionalArns")
    def _regional_arns(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regionalArns"))

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''(experimental) Arn of the dynamodb table.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) Table name of the dynamodb table.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) KMS encryption key, if this table uses a customer-managed encryption key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="tableStreamArn")
    def table_stream_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN of the table's stream, if there is one.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableStreamArn"))


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.TableAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_key": "encryptionKey",
        "global_indexes": "globalIndexes",
        "local_indexes": "localIndexes",
        "table_arn": "tableArn",
        "table_name": "tableName",
        "table_stream_arn": "tableStreamArn",
    },
)
class TableAttributes:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        global_indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
        table_arn: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
        table_stream_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Reference to a dynamodb table.

        :param encryption_key: (experimental) KMS encryption key, if this table uses a customer-managed encryption key. Default: - no key
        :param global_indexes: (experimental) The name of the global indexes set for this Table. Note that you need to set either this property, or {@link localIndexes}, if you want methods like grantReadData() to grant permissions for indexes as well as the table itself. Default: - no global indexes
        :param local_indexes: (experimental) The name of the local indexes set for this Table. Note that you need to set either this property, or {@link globalIndexes}, if you want methods like grantReadData() to grant permissions for indexes as well as the table itself. Default: - no local indexes
        :param table_arn: (experimental) The ARN of the dynamodb table. One of this, or {@link tableName}, is required. Default: - no table arn
        :param table_name: (experimental) The table name of the dynamodb table. One of this, or {@link tableArn}, is required. Default: - no table name
        :param table_stream_arn: (experimental) The ARN of the table's stream. Default: - no table stream

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dynamodb as dynamodb
            from monocdk import aws_kms as kms
            
            # key: kms.Key
            
            table_attributes = dynamodb.TableAttributes(
                encryption_key=key,
                global_indexes=["globalIndexes"],
                local_indexes=["localIndexes"],
                table_arn="tableArn",
                table_name="tableName",
                table_stream_arn="tableStreamArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f301cf436b0ac904f16e15b35a8792bb72d2edab625d7ab85e78883b8692340)
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument global_indexes", value=global_indexes, expected_type=type_hints["global_indexes"])
            check_type(argname="argument local_indexes", value=local_indexes, expected_type=type_hints["local_indexes"])
            check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument table_stream_arn", value=table_stream_arn, expected_type=type_hints["table_stream_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if global_indexes is not None:
            self._values["global_indexes"] = global_indexes
        if local_indexes is not None:
            self._values["local_indexes"] = local_indexes
        if table_arn is not None:
            self._values["table_arn"] = table_arn
        if table_name is not None:
            self._values["table_name"] = table_name
        if table_stream_arn is not None:
            self._values["table_stream_arn"] = table_stream_arn

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) KMS encryption key, if this table uses a customer-managed encryption key.

        :default: - no key

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def global_indexes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The name of the global indexes set for this Table.

        Note that you need to set either this property,
        or {@link localIndexes},
        if you want methods like grantReadData()
        to grant permissions for indexes as well as the table itself.

        :default: - no global indexes

        :stability: experimental
        '''
        result = self._values.get("global_indexes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def local_indexes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The name of the local indexes set for this Table.

        Note that you need to set either this property,
        or {@link globalIndexes},
        if you want methods like grantReadData()
        to grant permissions for indexes as well as the table itself.

        :default: - no local indexes

        :stability: experimental
        '''
        result = self._values.get("local_indexes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def table_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the dynamodb table.

        One of this, or {@link tableName}, is required.

        :default: - no table arn

        :stability: experimental
        '''
        result = self._values.get("table_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The table name of the dynamodb table.

        One of this, or {@link tableArn}, is required.

        :default: - no table name

        :stability: experimental
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_stream_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the table's stream.

        :default: - no table stream

        :stability: experimental
        '''
        result = self._values.get("table_stream_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_dynamodb.TableClass")
class TableClass(enum.Enum):
    '''(experimental) DynamoDB's table class.

    :see: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.TableClasses.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        table = dynamodb.Table(self, "Table",
            partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            table_class=dynamodb.TableClass.STANDARD_INFREQUENT_ACCESS
        )
    '''

    STANDARD = "STANDARD"
    '''(experimental) Default table class for DynamoDB.

    :stability: experimental
    '''
    STANDARD_INFREQUENT_ACCESS = "STANDARD_INFREQUENT_ACCESS"
    '''(experimental) Table class for DynamoDB that reduces storage costs compared to existing DynamoDB Standard tables.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_dynamodb.TableEncryption")
class TableEncryption(enum.Enum):
    '''(experimental) What kind of server-side encryption to apply to this table.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        table = dynamodb.Table(self, "MyTable",
            partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED
        )
        
        # You can access the CMK that was added to the stack on your behalf by the Table construct via:
        table_encryption_key = table.encryption_key
    '''

    DEFAULT = "DEFAULT"
    '''(experimental) Server-side KMS encryption with a master key owned by AWS.

    :stability: experimental
    '''
    CUSTOMER_MANAGED = "CUSTOMER_MANAGED"
    '''(experimental) Server-side KMS encryption with a customer master key managed by customer.

    If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.
    .. epigraph::

       **NOTE**: if ``encryptionKey`` is not specified and the ``Table`` construct creates
       a KMS key for you, the key will be created with default permissions. If you are using
       CDKv2, these permissions will be sufficient to enable the key for use with DynamoDB tables.
       If you are using CDKv1, make sure the feature flag ``@aws-cdk/aws-kms:defaultKeyPolicies``
       is set to ``true`` in your ``cdk.json``.

    :stability: experimental
    '''
    AWS_MANAGED = "AWS_MANAGED"
    '''(experimental) Server-side KMS encryption with a master key managed by AWS.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.TableOptions",
    jsii_struct_bases=[SchemaOptions],
    name_mapping={
        "partition_key": "partitionKey",
        "sort_key": "sortKey",
        "billing_mode": "billingMode",
        "contributor_insights_enabled": "contributorInsightsEnabled",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "point_in_time_recovery": "pointInTimeRecovery",
        "read_capacity": "readCapacity",
        "removal_policy": "removalPolicy",
        "replication_regions": "replicationRegions",
        "replication_timeout": "replicationTimeout",
        "server_side_encryption": "serverSideEncryption",
        "stream": "stream",
        "table_class": "tableClass",
        "time_to_live_attribute": "timeToLiveAttribute",
        "wait_for_replication_to_finish": "waitForReplicationToFinish",
        "write_capacity": "writeCapacity",
    },
)
class TableOptions(SchemaOptions):
    def __init__(
        self,
        *,
        partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
        sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
        billing_mode: typing.Optional[BillingMode] = None,
        contributor_insights_enabled: typing.Optional[builtins.bool] = None,
        encryption: typing.Optional[TableEncryption] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        point_in_time_recovery: typing.Optional[builtins.bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_timeout: typing.Optional[_Duration_070aa057] = None,
        server_side_encryption: typing.Optional[builtins.bool] = None,
        stream: typing.Optional[StreamViewType] = None,
        table_class: typing.Optional[TableClass] = None,
        time_to_live_attribute: typing.Optional[builtins.str] = None,
        wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties of a DynamoDB Table.

        Use {@link TableProps} for all table properties

        :param partition_key: (experimental) Partition key attribute definition.
        :param sort_key: (experimental) Sort key attribute definition. Default: no sort key
        :param billing_mode: (experimental) Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param contributor_insights_enabled: (experimental) Whether CloudWatch contributor insights is enabled. Default: false
        :param encryption: (experimental) Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. .. epigraph:: **NOTE**: if you set this to ``CUSTOMER_MANAGED`` and ``encryptionKey`` is not specified, the key that the Tablet generates for you will be created with default permissions. If you are using CDKv2, these permissions will be sufficient to enable the key for use with DynamoDB tables. If you are using CDKv1, make sure the feature flag ``@aws-cdk/aws-kms:defaultKeyPolicies`` is set to ``true`` in your ``cdk.json``. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: (experimental) External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: (experimental) Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: (experimental) The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: (experimental) The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: (experimental) Regions where replica tables will be created. Default: - no replica tables are created
        :param replication_timeout: (experimental) The timeout for a table replication operation in a single region. Default: Duration.minutes(30)
        :param server_side_encryption: (deprecated) Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param stream: (experimental) When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param table_class: (experimental) Specify the table class. Default: STANDARD
        :param time_to_live_attribute: (experimental) The name of TTL attribute. Default: - TTL is disabled
        :param wait_for_replication_to_finish: (experimental) Indicates whether CloudFormation stack waits for replication to finish. If set to false, the CloudFormation resource will mark the resource as created and replication will be completed asynchronously. This property is ignored if replicationRegions property is not set. DO NOT UNSET this property if adding/removing multiple replicationRegions in one deployment, as CloudFormation only supports one region replication at a time. CDK overcomes this limitation by waiting for replication to finish before starting new replicationRegion. Default: true
        :param write_capacity: (experimental) The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_dynamodb as dynamodb
            from monocdk import aws_kms as kms
            
            # duration: monocdk.Duration
            # key: kms.Key
            
            table_options = dynamodb.TableOptions(
                partition_key=dynamodb.Attribute(
                    name="name",
                    type=dynamodb.AttributeType.BINARY
                ),
            
                # the properties below are optional
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                contributor_insights_enabled=False,
                encryption=dynamodb.TableEncryption.DEFAULT,
                encryption_key=key,
                point_in_time_recovery=False,
                read_capacity=123,
                removal_policy=monocdk.RemovalPolicy.DESTROY,
                replication_regions=["replicationRegions"],
                replication_timeout=duration,
                server_side_encryption=False,
                sort_key=dynamodb.Attribute(
                    name="name",
                    type=dynamodb.AttributeType.BINARY
                ),
                stream=dynamodb.StreamViewType.NEW_IMAGE,
                table_class=dynamodb.TableClass.STANDARD,
                time_to_live_attribute="timeToLiveAttribute",
                wait_for_replication_to_finish=False,
                write_capacity=123
            )
        '''
        if isinstance(partition_key, dict):
            partition_key = Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3462a9f3e3a4e301259511b7b046e264ce4eed8bc1263f48f972dcc4018849)
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            check_type(argname="argument sort_key", value=sort_key, expected_type=type_hints["sort_key"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument contributor_insights_enabled", value=contributor_insights_enabled, expected_type=type_hints["contributor_insights_enabled"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument point_in_time_recovery", value=point_in_time_recovery, expected_type=type_hints["point_in_time_recovery"])
            check_type(argname="argument read_capacity", value=read_capacity, expected_type=type_hints["read_capacity"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument replication_regions", value=replication_regions, expected_type=type_hints["replication_regions"])
            check_type(argname="argument replication_timeout", value=replication_timeout, expected_type=type_hints["replication_timeout"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            check_type(argname="argument table_class", value=table_class, expected_type=type_hints["table_class"])
            check_type(argname="argument time_to_live_attribute", value=time_to_live_attribute, expected_type=type_hints["time_to_live_attribute"])
            check_type(argname="argument wait_for_replication_to_finish", value=wait_for_replication_to_finish, expected_type=type_hints["wait_for_replication_to_finish"])
            check_type(argname="argument write_capacity", value=write_capacity, expected_type=type_hints["write_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if contributor_insights_enabled is not None:
            self._values["contributor_insights_enabled"] = contributor_insights_enabled
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if point_in_time_recovery is not None:
            self._values["point_in_time_recovery"] = point_in_time_recovery
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replication_regions is not None:
            self._values["replication_regions"] = replication_regions
        if replication_timeout is not None:
            self._values["replication_timeout"] = replication_timeout
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if stream is not None:
            self._values["stream"] = stream
        if table_class is not None:
            self._values["table_class"] = table_class
        if time_to_live_attribute is not None:
            self._values["time_to_live_attribute"] = time_to_live_attribute
        if wait_for_replication_to_finish is not None:
            self._values["wait_for_replication_to_finish"] = wait_for_replication_to_finish
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity

    @builtins.property
    def partition_key(self) -> Attribute:
        '''(experimental) Partition key attribute definition.

        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(Attribute, result)

    @builtins.property
    def sort_key(self) -> typing.Optional[Attribute]:
        '''(experimental) Sort key attribute definition.

        :default: no sort key

        :stability: experimental
        '''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional[Attribute], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[BillingMode]:
        '''(experimental) Specify how you are charged for read and write throughput and how you manage capacity.

        :default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise

        :stability: experimental
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[BillingMode], result)

    @builtins.property
    def contributor_insights_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether CloudWatch contributor insights is enabled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("contributor_insights_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption(self) -> typing.Optional[TableEncryption]:
        '''(experimental) Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``serverSideEncryption`` is set.
        .. epigraph::

           **NOTE**: if you set this to ``CUSTOMER_MANAGED`` and ``encryptionKey`` is not
           specified, the key that the Tablet generates for you will be created with
           default permissions. If you are using CDKv2, these permissions will be
           sufficient to enable the key for use with DynamoDB tables.  If you are
           using CDKv1, make sure the feature flag
           ``@aws-cdk/aws-kms:defaultKeyPolicies`` is set to ``true`` in your ``cdk.json``.

        :default: - server-side encryption is enabled with an AWS owned customer master key

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[TableEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) External KMS key to use for table encryption.

        This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``.

        :default:

        - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this
        property is undefined, a new KMS key will be created and associated with this table.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def point_in_time_recovery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether point-in-time recovery is enabled.

        :default: - point-in-time recovery is disabled

        :stability: experimental
        '''
        result = self._values.get("point_in_time_recovery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The read capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("read_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The removal policy to apply to the DynamoDB Table.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def replication_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regions where replica tables will be created.

        :default: - no replica tables are created

        :stability: experimental
        '''
        result = self._values.get("replication_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replication_timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The timeout for a table replication operation in a single region.

        :default: Duration.minutes(30)

        :stability: experimental
        '''
        result = self._values.get("replication_timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set.

        :default: - server-side encryption is enabled with an AWS owned customer master key

        :deprecated:

        This property is deprecated. In order to obtain the same behavior as
        enabling this, set the ``encryption`` property to ``TableEncryption.AWS_MANAGED`` instead.

        :stability: deprecated
        '''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stream(self) -> typing.Optional[StreamViewType]:
        '''(experimental) When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

        :default: - streams are disabled unless ``replicationRegions`` is specified

        :stability: experimental
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[StreamViewType], result)

    @builtins.property
    def table_class(self) -> typing.Optional[TableClass]:
        '''(experimental) Specify the table class.

        :default: STANDARD

        :stability: experimental
        '''
        result = self._values.get("table_class")
        return typing.cast(typing.Optional[TableClass], result)

    @builtins.property
    def time_to_live_attribute(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of TTL attribute.

        :default: - TTL is disabled

        :stability: experimental
        '''
        result = self._values.get("time_to_live_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_replication_to_finish(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether CloudFormation stack waits for replication to finish.

        If set to false, the CloudFormation resource will mark the resource as
        created and replication will be completed asynchronously. This property is
        ignored if replicationRegions property is not set.

        DO NOT UNSET this property if adding/removing multiple replicationRegions
        in one deployment, as CloudFormation only supports one region replication
        at a time. CDK overcomes this limitation by waiting for replication to
        finish before starting new replicationRegion.

        :default: true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-replicas
        :stability: experimental
        '''
        result = self._values.get("wait_for_replication_to_finish")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The write capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("write_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.TableProps",
    jsii_struct_bases=[TableOptions],
    name_mapping={
        "partition_key": "partitionKey",
        "sort_key": "sortKey",
        "billing_mode": "billingMode",
        "contributor_insights_enabled": "contributorInsightsEnabled",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "point_in_time_recovery": "pointInTimeRecovery",
        "read_capacity": "readCapacity",
        "removal_policy": "removalPolicy",
        "replication_regions": "replicationRegions",
        "replication_timeout": "replicationTimeout",
        "server_side_encryption": "serverSideEncryption",
        "stream": "stream",
        "table_class": "tableClass",
        "time_to_live_attribute": "timeToLiveAttribute",
        "wait_for_replication_to_finish": "waitForReplicationToFinish",
        "write_capacity": "writeCapacity",
        "kinesis_stream": "kinesisStream",
        "table_name": "tableName",
    },
)
class TableProps(TableOptions):
    def __init__(
        self,
        *,
        partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
        sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
        billing_mode: typing.Optional[BillingMode] = None,
        contributor_insights_enabled: typing.Optional[builtins.bool] = None,
        encryption: typing.Optional[TableEncryption] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        point_in_time_recovery: typing.Optional[builtins.bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_timeout: typing.Optional[_Duration_070aa057] = None,
        server_side_encryption: typing.Optional[builtins.bool] = None,
        stream: typing.Optional[StreamViewType] = None,
        table_class: typing.Optional[TableClass] = None,
        time_to_live_attribute: typing.Optional[builtins.str] = None,
        wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        kinesis_stream: typing.Optional[_IStream_14c6ec7f] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a DynamoDB Table.

        :param partition_key: (experimental) Partition key attribute definition.
        :param sort_key: (experimental) Sort key attribute definition. Default: no sort key
        :param billing_mode: (experimental) Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param contributor_insights_enabled: (experimental) Whether CloudWatch contributor insights is enabled. Default: false
        :param encryption: (experimental) Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. .. epigraph:: **NOTE**: if you set this to ``CUSTOMER_MANAGED`` and ``encryptionKey`` is not specified, the key that the Tablet generates for you will be created with default permissions. If you are using CDKv2, these permissions will be sufficient to enable the key for use with DynamoDB tables. If you are using CDKv1, make sure the feature flag ``@aws-cdk/aws-kms:defaultKeyPolicies`` is set to ``true`` in your ``cdk.json``. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: (experimental) External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: (experimental) Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: (experimental) The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: (experimental) The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: (experimental) Regions where replica tables will be created. Default: - no replica tables are created
        :param replication_timeout: (experimental) The timeout for a table replication operation in a single region. Default: Duration.minutes(30)
        :param server_side_encryption: (deprecated) Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param stream: (experimental) When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param table_class: (experimental) Specify the table class. Default: STANDARD
        :param time_to_live_attribute: (experimental) The name of TTL attribute. Default: - TTL is disabled
        :param wait_for_replication_to_finish: (experimental) Indicates whether CloudFormation stack waits for replication to finish. If set to false, the CloudFormation resource will mark the resource as created and replication will be completed asynchronously. This property is ignored if replicationRegions property is not set. DO NOT UNSET this property if adding/removing multiple replicationRegions in one deployment, as CloudFormation only supports one region replication at a time. CDK overcomes this limitation by waiting for replication to finish before starting new replicationRegion. Default: true
        :param write_capacity: (experimental) The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param kinesis_stream: (experimental) Kinesis Data Stream to capture item-level changes for the table. Default: - no Kinesis Data Stream
        :param table_name: (experimental) Enforces a particular physical table name. Default: 

        :stability: experimental
        :exampleMetadata: infused

        Example::

            global_table = dynamodb.Table(self, "Table",
                partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
                replication_regions=["us-east-1", "us-east-2", "us-west-2"],
                billing_mode=dynamodb.BillingMode.PROVISIONED
            )
            
            global_table.auto_scale_write_capacity(
                min_capacity=1,
                max_capacity=10
            ).scale_on_utilization(target_utilization_percent=75)
        '''
        if isinstance(partition_key, dict):
            partition_key = Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c6aa67c2622b786574c5df48e5ca3d844b5fb21317d9704e6225b88bae9fc9)
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            check_type(argname="argument sort_key", value=sort_key, expected_type=type_hints["sort_key"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument contributor_insights_enabled", value=contributor_insights_enabled, expected_type=type_hints["contributor_insights_enabled"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument point_in_time_recovery", value=point_in_time_recovery, expected_type=type_hints["point_in_time_recovery"])
            check_type(argname="argument read_capacity", value=read_capacity, expected_type=type_hints["read_capacity"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument replication_regions", value=replication_regions, expected_type=type_hints["replication_regions"])
            check_type(argname="argument replication_timeout", value=replication_timeout, expected_type=type_hints["replication_timeout"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            check_type(argname="argument table_class", value=table_class, expected_type=type_hints["table_class"])
            check_type(argname="argument time_to_live_attribute", value=time_to_live_attribute, expected_type=type_hints["time_to_live_attribute"])
            check_type(argname="argument wait_for_replication_to_finish", value=wait_for_replication_to_finish, expected_type=type_hints["wait_for_replication_to_finish"])
            check_type(argname="argument write_capacity", value=write_capacity, expected_type=type_hints["write_capacity"])
            check_type(argname="argument kinesis_stream", value=kinesis_stream, expected_type=type_hints["kinesis_stream"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if contributor_insights_enabled is not None:
            self._values["contributor_insights_enabled"] = contributor_insights_enabled
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if point_in_time_recovery is not None:
            self._values["point_in_time_recovery"] = point_in_time_recovery
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replication_regions is not None:
            self._values["replication_regions"] = replication_regions
        if replication_timeout is not None:
            self._values["replication_timeout"] = replication_timeout
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if stream is not None:
            self._values["stream"] = stream
        if table_class is not None:
            self._values["table_class"] = table_class
        if time_to_live_attribute is not None:
            self._values["time_to_live_attribute"] = time_to_live_attribute
        if wait_for_replication_to_finish is not None:
            self._values["wait_for_replication_to_finish"] = wait_for_replication_to_finish
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity
        if kinesis_stream is not None:
            self._values["kinesis_stream"] = kinesis_stream
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def partition_key(self) -> Attribute:
        '''(experimental) Partition key attribute definition.

        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(Attribute, result)

    @builtins.property
    def sort_key(self) -> typing.Optional[Attribute]:
        '''(experimental) Sort key attribute definition.

        :default: no sort key

        :stability: experimental
        '''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional[Attribute], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[BillingMode]:
        '''(experimental) Specify how you are charged for read and write throughput and how you manage capacity.

        :default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise

        :stability: experimental
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[BillingMode], result)

    @builtins.property
    def contributor_insights_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether CloudWatch contributor insights is enabled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("contributor_insights_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption(self) -> typing.Optional[TableEncryption]:
        '''(experimental) Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``serverSideEncryption`` is set.
        .. epigraph::

           **NOTE**: if you set this to ``CUSTOMER_MANAGED`` and ``encryptionKey`` is not
           specified, the key that the Tablet generates for you will be created with
           default permissions. If you are using CDKv2, these permissions will be
           sufficient to enable the key for use with DynamoDB tables.  If you are
           using CDKv1, make sure the feature flag
           ``@aws-cdk/aws-kms:defaultKeyPolicies`` is set to ``true`` in your ``cdk.json``.

        :default: - server-side encryption is enabled with an AWS owned customer master key

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[TableEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) External KMS key to use for table encryption.

        This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``.

        :default:

        - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this
        property is undefined, a new KMS key will be created and associated with this table.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def point_in_time_recovery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether point-in-time recovery is enabled.

        :default: - point-in-time recovery is disabled

        :stability: experimental
        '''
        result = self._values.get("point_in_time_recovery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The read capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("read_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The removal policy to apply to the DynamoDB Table.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def replication_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Regions where replica tables will be created.

        :default: - no replica tables are created

        :stability: experimental
        '''
        result = self._values.get("replication_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replication_timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The timeout for a table replication operation in a single region.

        :default: Duration.minutes(30)

        :stability: experimental
        '''
        result = self._values.get("replication_timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``encryption`` and/or ``encryptionKey`` is set.

        :default: - server-side encryption is enabled with an AWS owned customer master key

        :deprecated:

        This property is deprecated. In order to obtain the same behavior as
        enabling this, set the ``encryption`` property to ``TableEncryption.AWS_MANAGED`` instead.

        :stability: deprecated
        '''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stream(self) -> typing.Optional[StreamViewType]:
        '''(experimental) When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

        :default: - streams are disabled unless ``replicationRegions`` is specified

        :stability: experimental
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[StreamViewType], result)

    @builtins.property
    def table_class(self) -> typing.Optional[TableClass]:
        '''(experimental) Specify the table class.

        :default: STANDARD

        :stability: experimental
        '''
        result = self._values.get("table_class")
        return typing.cast(typing.Optional[TableClass], result)

    @builtins.property
    def time_to_live_attribute(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of TTL attribute.

        :default: - TTL is disabled

        :stability: experimental
        '''
        result = self._values.get("time_to_live_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_replication_to_finish(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether CloudFormation stack waits for replication to finish.

        If set to false, the CloudFormation resource will mark the resource as
        created and replication will be completed asynchronously. This property is
        ignored if replicationRegions property is not set.

        DO NOT UNSET this property if adding/removing multiple replicationRegions
        in one deployment, as CloudFormation only supports one region replication
        at a time. CDK overcomes this limitation by waiting for replication to
        finish before starting new replicationRegion.

        :default: true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-replicas
        :stability: experimental
        '''
        result = self._values.get("wait_for_replication_to_finish")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The write capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("write_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kinesis_stream(self) -> typing.Optional[_IStream_14c6ec7f]:
        '''(experimental) Kinesis Data Stream to capture item-level changes for the table.

        :default: - no Kinesis Data Stream

        :stability: experimental
        '''
        result = self._values.get("kinesis_stream")
        return typing.cast(typing.Optional[_IStream_14c6ec7f], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Enforces a particular physical table name.

        :default:

        :stability: experimental
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.UtilizationScalingProps",
    jsii_struct_bases=[_BaseTargetTrackingProps_e4402570],
    name_mapping={
        "disable_scale_in": "disableScaleIn",
        "policy_name": "policyName",
        "scale_in_cooldown": "scaleInCooldown",
        "scale_out_cooldown": "scaleOutCooldown",
        "target_utilization_percent": "targetUtilizationPercent",
    },
)
class UtilizationScalingProps(_BaseTargetTrackingProps_e4402570):
    def __init__(
        self,
        *,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        policy_name: typing.Optional[builtins.str] = None,
        scale_in_cooldown: typing.Optional[_Duration_070aa057] = None,
        scale_out_cooldown: typing.Optional[_Duration_070aa057] = None,
        target_utilization_percent: jsii.Number,
    ) -> None:
        '''(experimental) Properties for enabling DynamoDB utilization tracking.

        :param disable_scale_in: (experimental) Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: (experimental) A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: (experimental) Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: (experimental) Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param target_utilization_percent: (experimental) Target utilization percentage for the attribute.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            global_table = dynamodb.Table(self, "Table",
                partition_key=dynamodb.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
                replication_regions=["us-east-1", "us-east-2", "us-west-2"],
                billing_mode=dynamodb.BillingMode.PROVISIONED
            )
            
            global_table.auto_scale_write_capacity(
                min_capacity=1,
                max_capacity=10
            ).scale_on_utilization(target_utilization_percent=75)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610af3e0a1310b39ee25edafe838dc3766987bc96bd9e2e955be17ba57765faf)
            check_type(argname="argument disable_scale_in", value=disable_scale_in, expected_type=type_hints["disable_scale_in"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument scale_in_cooldown", value=scale_in_cooldown, expected_type=type_hints["scale_in_cooldown"])
            check_type(argname="argument scale_out_cooldown", value=scale_out_cooldown, expected_type=type_hints["scale_out_cooldown"])
            check_type(argname="argument target_utilization_percent", value=target_utilization_percent, expected_type=type_hints["target_utilization_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_utilization_percent": target_utilization_percent,
        }
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None:
            self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None:
            self._values["scale_out_cooldown"] = scale_out_cooldown

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable_scale_in")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the scaling policy.

        :default: - Automatically generated name.

        :stability: experimental
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Period after a scale in activity completes before another scale in activity can start.

        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        :stability: experimental
        '''
        result = self._values.get("scale_in_cooldown")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Period after a scale out activity completes before another scale out activity can start.

        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        :stability: experimental
        '''
        result = self._values.get("scale_out_cooldown")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def target_utilization_percent(self) -> jsii.Number:
        '''(experimental) Target utilization percentage for the attribute.

        :stability: experimental
        '''
        result = self._values.get("target_utilization_percent")
        assert result is not None, "Required property 'target_utilization_percent' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UtilizationScalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.GlobalSecondaryIndexProps",
    jsii_struct_bases=[SecondaryIndexProps, SchemaOptions],
    name_mapping={
        "index_name": "indexName",
        "non_key_attributes": "nonKeyAttributes",
        "projection_type": "projectionType",
        "partition_key": "partitionKey",
        "sort_key": "sortKey",
        "read_capacity": "readCapacity",
        "write_capacity": "writeCapacity",
    },
)
class GlobalSecondaryIndexProps(SecondaryIndexProps, SchemaOptions):
    def __init__(
        self,
        *,
        index_name: builtins.str,
        non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        projection_type: typing.Optional[ProjectionType] = None,
        partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
        sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for a global secondary index.

        :param index_name: (experimental) The name of the secondary index.
        :param non_key_attributes: (experimental) The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: (experimental) The set of attributes that are projected into the secondary index. Default: ALL
        :param partition_key: (experimental) Partition key attribute definition.
        :param sort_key: (experimental) Sort key attribute definition. Default: no sort key
        :param read_capacity: (experimental) The read capacity for the global secondary index. Can only be provided if table billingMode is Provisioned or undefined. Default: 5
        :param write_capacity: (experimental) The write capacity for the global secondary index. Can only be provided if table billingMode is Provisioned or undefined. Default: 5

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dynamodb as dynamodb
            
            global_secondary_index_props = dynamodb.GlobalSecondaryIndexProps(
                index_name="indexName",
                partition_key=dynamodb.Attribute(
                    name="name",
                    type=dynamodb.AttributeType.BINARY
                ),
            
                # the properties below are optional
                non_key_attributes=["nonKeyAttributes"],
                projection_type=dynamodb.ProjectionType.KEYS_ONLY,
                read_capacity=123,
                sort_key=dynamodb.Attribute(
                    name="name",
                    type=dynamodb.AttributeType.BINARY
                ),
                write_capacity=123
            )
        '''
        if isinstance(partition_key, dict):
            partition_key = Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2c307fbcb4f8ca783da6df7736a73d017d606d99f6363a3559377475f17d48)
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument non_key_attributes", value=non_key_attributes, expected_type=type_hints["non_key_attributes"])
            check_type(argname="argument projection_type", value=projection_type, expected_type=type_hints["projection_type"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            check_type(argname="argument sort_key", value=sort_key, expected_type=type_hints["sort_key"])
            check_type(argname="argument read_capacity", value=read_capacity, expected_type=type_hints["read_capacity"])
            check_type(argname="argument write_capacity", value=write_capacity, expected_type=type_hints["write_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_name": index_name,
            "partition_key": partition_key,
        }
        if non_key_attributes is not None:
            self._values["non_key_attributes"] = non_key_attributes
        if projection_type is not None:
            self._values["projection_type"] = projection_type
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity

    @builtins.property
    def index_name(self) -> builtins.str:
        '''(experimental) The name of the secondary index.

        :stability: experimental
        '''
        result = self._values.get("index_name")
        assert result is not None, "Required property 'index_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def non_key_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The non-key attributes that are projected into the secondary index.

        :default: - No additional attributes

        :stability: experimental
        '''
        result = self._values.get("non_key_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def projection_type(self) -> typing.Optional[ProjectionType]:
        '''(experimental) The set of attributes that are projected into the secondary index.

        :default: ALL

        :stability: experimental
        '''
        result = self._values.get("projection_type")
        return typing.cast(typing.Optional[ProjectionType], result)

    @builtins.property
    def partition_key(self) -> Attribute:
        '''(experimental) Partition key attribute definition.

        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(Attribute, result)

    @builtins.property
    def sort_key(self) -> typing.Optional[Attribute]:
        '''(experimental) Sort key attribute definition.

        :default: no sort key

        :stability: experimental
        '''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional[Attribute], result)

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The read capacity for the global secondary index.

        Can only be provided if table billingMode is Provisioned or undefined.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("read_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The write capacity for the global secondary index.

        Can only be provided if table billingMode is Provisioned or undefined.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("write_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlobalSecondaryIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_dynamodb.LocalSecondaryIndexProps",
    jsii_struct_bases=[SecondaryIndexProps],
    name_mapping={
        "index_name": "indexName",
        "non_key_attributes": "nonKeyAttributes",
        "projection_type": "projectionType",
        "sort_key": "sortKey",
    },
)
class LocalSecondaryIndexProps(SecondaryIndexProps):
    def __init__(
        self,
        *,
        index_name: builtins.str,
        non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        projection_type: typing.Optional[ProjectionType] = None,
        sort_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties for a local secondary index.

        :param index_name: (experimental) The name of the secondary index.
        :param non_key_attributes: (experimental) The non-key attributes that are projected into the secondary index. Default: - No additional attributes
        :param projection_type: (experimental) The set of attributes that are projected into the secondary index. Default: ALL
        :param sort_key: (experimental) The attribute of a sort key for the local secondary index.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dynamodb as dynamodb
            
            local_secondary_index_props = dynamodb.LocalSecondaryIndexProps(
                index_name="indexName",
                sort_key=dynamodb.Attribute(
                    name="name",
                    type=dynamodb.AttributeType.BINARY
                ),
            
                # the properties below are optional
                non_key_attributes=["nonKeyAttributes"],
                projection_type=dynamodb.ProjectionType.KEYS_ONLY
            )
        '''
        if isinstance(sort_key, dict):
            sort_key = Attribute(**sort_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea3816a7fd77b7dbc148beefca3fd2034bdb880c8eb1d61bbdfd2f52e64b7ae)
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument non_key_attributes", value=non_key_attributes, expected_type=type_hints["non_key_attributes"])
            check_type(argname="argument projection_type", value=projection_type, expected_type=type_hints["projection_type"])
            check_type(argname="argument sort_key", value=sort_key, expected_type=type_hints["sort_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_name": index_name,
            "sort_key": sort_key,
        }
        if non_key_attributes is not None:
            self._values["non_key_attributes"] = non_key_attributes
        if projection_type is not None:
            self._values["projection_type"] = projection_type

    @builtins.property
    def index_name(self) -> builtins.str:
        '''(experimental) The name of the secondary index.

        :stability: experimental
        '''
        result = self._values.get("index_name")
        assert result is not None, "Required property 'index_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def non_key_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The non-key attributes that are projected into the secondary index.

        :default: - No additional attributes

        :stability: experimental
        '''
        result = self._values.get("non_key_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def projection_type(self) -> typing.Optional[ProjectionType]:
        '''(experimental) The set of attributes that are projected into the secondary index.

        :default: ALL

        :stability: experimental
        '''
        result = self._values.get("projection_type")
        return typing.cast(typing.Optional[ProjectionType], result)

    @builtins.property
    def sort_key(self) -> Attribute:
        '''(experimental) The attribute of a sort key for the local secondary index.

        :stability: experimental
        '''
        result = self._values.get("sort_key")
        assert result is not None, "Required property 'sort_key' is missing"
        return typing.cast(Attribute, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalSecondaryIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Attribute",
    "AttributeType",
    "BillingMode",
    "CfnGlobalTable",
    "CfnGlobalTableProps",
    "CfnTable",
    "CfnTableProps",
    "EnableScalingProps",
    "GlobalSecondaryIndexProps",
    "IScalableTableAttribute",
    "ITable",
    "LocalSecondaryIndexProps",
    "Operation",
    "ProjectionType",
    "SchemaOptions",
    "SecondaryIndexProps",
    "StreamViewType",
    "SystemErrorsForOperationsMetricOptions",
    "Table",
    "TableAttributes",
    "TableClass",
    "TableEncryption",
    "TableOptions",
    "TableProps",
    "UtilizationScalingProps",
]

publication.publish()

def _typecheckingstub__816674236dee7a82734c355c923a191a5221dc625a7c6e2d61515e1e623731fd(
    *,
    name: builtins.str,
    type: AttributeType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbe5d7f749468118280141c91598ee529c3cb7b9b24c48a1f398f27e21546d9(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    attribute_definitions: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.AttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    replicas: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.ReplicaSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    billing_mode: typing.Optional[builtins.str] = None,
    global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.GlobalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    local_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.LocalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stream_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.StreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_name: typing.Optional[builtins.str] = None,
    time_to_live_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.TimeToLiveSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    write_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.WriteProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4010b24590498478c2356fb3c7bc894f03bb87a29e9f3902f199bce5ef3e7653(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d17caa3295d0c79582f79aab3278e501df1324875ac0f7877e8804642af5aa(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd425fc8274826e47420227bf64b306fbf22a1fdb2c224363c3ad74ae666f8d(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.AttributeDefinitionProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c62749d0a6bacb4d43b8361e2fd5837ab2168b09083ec3b536f0e25540cbf52(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.KeySchemaProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fbb4cc25efb389ad0b9d976819ea6231f7bfb2ff258a7a46116a0e53ef3820(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.ReplicaSpecificationProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6efc0baee2aa5341df4c9b7745e9054fe0a917625a9356223c71078d3b5be83(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2478f9274ce4a7ab14835c6d24750a8c17a0b4d3ff2347cd333c0ee405eac56d(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.GlobalSecondaryIndexProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae009ce121eebd8aed0117f82d85b3e8de211d3020bf61526a556af2b252b95(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalTable.LocalSecondaryIndexProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a2f40fd9b2aa40e87c338172d2e2fa8f55fc371ddaa51a12e30dc0292e6e61(
    value: typing.Optional[typing.Union[CfnGlobalTable.SSESpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed23fa6d569a437212b6bb12e9558cbbae2573d5f2b032c1d165e23bb940b7cf(
    value: typing.Optional[typing.Union[CfnGlobalTable.StreamSpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b580c90602b438aaf5a3087527fbb06a308696ca83bb13a1850e7d5e5b9fe637(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e496d8e393afef1b7683d9c8e8dc2504964d4a146d6fa117ea49b070180f20b6(
    value: typing.Optional[typing.Union[CfnGlobalTable.TimeToLiveSpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcfa7424cde69e61c8ddf4b4594568319da156ae7b2a0982224cb8dde4c1130(
    value: typing.Optional[typing.Union[CfnGlobalTable.WriteProvisionedThroughputSettingsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a37ead1c9c6ba599121eeebd25cbfc0d8cf9bb9a2e268c50b45516015ec676(
    *,
    attribute_name: builtins.str,
    attribute_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcf57773cc4fd4d20db865a5ec5577bc5536def8ccbc720f4de0851d10aece6(
    *,
    max_capacity: jsii.Number,
    min_capacity: jsii.Number,
    target_tracking_scaling_policy_configuration: typing.Union[typing.Union[CfnGlobalTable.TargetTrackingScalingPolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    seed_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909baaf0655c8cd7d7c9db8c52aac90d9a2fb28008905cbce16f74e8a536d32f(
    *,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d2a1270d054d7667312c4fb83f1e4e6a39a3be162ed778dff5febe59661860(
    *,
    index_name: builtins.str,
    key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    projection: typing.Union[typing.Union[CfnGlobalTable.ProjectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    write_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.WriteProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91f0abf47628c0b91309cddfa931146d5b3cddd46f7e0157c0801e0824b155f(
    *,
    attribute_name: builtins.str,
    key_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d84ce952ed9b4a9e80736b02634bbbacf3d01b042614641e0cea68781cd1348(
    *,
    stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85b8871429ee864b365f5e68edb2be0686e51a559e0487e54183a7d022936ad(
    *,
    index_name: builtins.str,
    key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    projection: typing.Union[typing.Union[CfnGlobalTable.ProjectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165c6e0baaaa0dcbd41e473e6033d59fa7e20b2e28af25301745498b70e20e99(
    *,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f57925ff29b6ddd938306497d6eff6be463e8490a416c19943e761a4b3490d(
    *,
    non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    projection_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d158d665c80e66da0c4967725ab33811ac7669debf35586c66c3de7f96cb17(
    *,
    read_capacity_auto_scaling_settings: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.CapacityAutoScalingSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    read_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6946430e1f985786a9ea4a350a72a2bd07244ea6ff1b64649aaf834cca6d65d(
    *,
    index_name: builtins.str,
    contributor_insights_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    read_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.ReadProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bf1ebc7fc9f32960697b047a7757a342a5befe96061784aeef4097dcae41d7(
    *,
    kms_master_key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a5869029b02679d4f1087f08eaedbb43dd60d8a3fef4ca87fdf9b38d052195(
    *,
    region: builtins.str,
    contributor_insights_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.ReplicaGlobalSecondaryIndexSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    kinesis_stream_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.KinesisStreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    point_in_time_recovery_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.PointInTimeRecoverySpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    read_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.ReadProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.ReplicaSSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_class: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e716e476896f0940a9b5354c21cc0dee07d5ec08f3fec8d08ff4725c80743d(
    *,
    sse_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    sse_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56c9f1d49878069057c8d58f23c9c7bda820a349951193c7046e4d1cb865551(
    *,
    stream_view_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65047cc14f31b8f45c1f4e553ba54123080aa2bb64019097b878d33591b944db(
    *,
    target_value: jsii.Number,
    disable_scale_in: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    scale_in_cooldown: typing.Optional[jsii.Number] = None,
    scale_out_cooldown: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2e1b5f2abd745f82312e8a8f9f569cfc3761627512ddc9f780b57c2cd26619(
    *,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    attribute_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c20781366ff4d453194f93634df4a8b4d241003b5410ab28f33db210f2b3366(
    *,
    write_capacity_auto_scaling_settings: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.CapacityAutoScalingSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab4bb4e6ae2dc28ed812176f22c08f7e8c6272c5a6b3baa5bfdfea00845d1b9(
    *,
    attribute_definitions: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.AttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    replicas: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.ReplicaSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    billing_mode: typing.Optional[builtins.str] = None,
    global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.GlobalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    local_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalTable.LocalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stream_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.StreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_name: typing.Optional[builtins.str] = None,
    time_to_live_specification: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.TimeToLiveSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    write_provisioned_throughput_settings: typing.Optional[typing.Union[typing.Union[CfnGlobalTable.WriteProvisionedThroughputSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85be0711ab7591b6225f503e4224d9c87c962430d54cd36372e3eeb918c268b5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    attribute_definitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.AttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    billing_mode: typing.Optional[builtins.str] = None,
    contributor_insights_specification: typing.Optional[typing.Union[typing.Union[CfnTable.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.GlobalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    import_source_specification: typing.Optional[typing.Union[typing.Union[CfnTable.ImportSourceSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_stream_specification: typing.Optional[typing.Union[typing.Union[CfnTable.KinesisStreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    local_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.LocalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    point_in_time_recovery_specification: typing.Optional[typing.Union[typing.Union[CfnTable.PointInTimeRecoverySpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    provisioned_throughput: typing.Optional[typing.Union[typing.Union[CfnTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stream_specification: typing.Optional[typing.Union[typing.Union[CfnTable.StreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_class: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_to_live_specification: typing.Optional[typing.Union[typing.Union[CfnTable.TimeToLiveSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b830bfc4553247aa6445b466a617246c5e7857bfcb84af7bad3ef80f68a69f76(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd466d9021dacc515e9198f0d83843ebcf5506ba3489672a6c5c697c2811e06(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e99008ec9e92d4e21806472950ebaf6488e258740d69a726ec75569f36b968(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.KeySchemaProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0608b5b9696face2f4b4b73951b15835d8cd87978d9965214b421babc187d5b2(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.AttributeDefinitionProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11cf6355f9c07e3e9ede53c9f91af4b3c9f708a5be58c17173a1ae09a3817604(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db3dc901d145b97fdba90f4dfc4846152b0061e14aeb02eb22e6a69cf5ae767(
    value: typing.Optional[typing.Union[CfnTable.ContributorInsightsSpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc0546f894efe114db4cf43c84f79365c64bbdd94130b1216cc0a33443477f9(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cbc8eaf2d0227a95669789102bfb304881905ee60d1e8c0feb3f4376de4c5e3(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.GlobalSecondaryIndexProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d840c1a7c8764b2abb0138c53971a02b5f3d6350627273aa3018824886c747b(
    value: typing.Optional[typing.Union[CfnTable.ImportSourceSpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399da2757acdc128203f1943512bfb1c670403f78b17ab28b12cfad414cb97df(
    value: typing.Optional[typing.Union[CfnTable.KinesisStreamSpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d255b8331c53f30d7967508a99acb1be108798cecf531faaa65a940b8b008c3(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTable.LocalSecondaryIndexProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e06be30678f747fe104eab6112203c576778a06fcea872a10ddd45a47f27ab(
    value: typing.Optional[typing.Union[CfnTable.PointInTimeRecoverySpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8789bec6f5b5369126eb8a594fb26f3b9ad0a27625c9a022ed5c155a73c43efd(
    value: typing.Optional[typing.Union[CfnTable.ProvisionedThroughputProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da5df6980650a3a8d72c24023d2f2e1c04b69510c34b9e3be1443590f151d50(
    value: typing.Optional[typing.Union[CfnTable.SSESpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e434617353b6b44480450b63c362760aed242f6a24692f1db95e4a6d619bb31(
    value: typing.Optional[typing.Union[CfnTable.StreamSpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2330969407eb951c8226fb1ab2e942e17b39f7e62f09215ccbc8665e1dc8ecc5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e592cbce269b5585c738fd2e58a360f88d109c439412177701f6fd689407d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0a1d22b9eaf17d6b0150306a0a773ac0b9eb75eef39c0c051de885a3f0c7b7(
    value: typing.Optional[typing.Union[CfnTable.TimeToLiveSpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ca9f552dc7e6d78fd9e5e449d1234067ceb642887cee714f485cdc46b9a5e3(
    *,
    attribute_name: builtins.str,
    attribute_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89d3b21c0ad477e959fc26d96ef5c63878c18a54eade1680959e2741e47af0d(
    *,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1910e1560f86fe9d3c766dad4d35c72c71e8629ca3d7d25442a8ee599e9dcae(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c1b671d74eccaecc71ca0eb7290c862f8a15f213c2d9db856d7711f73ae318(
    *,
    index_name: builtins.str,
    key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    projection: typing.Union[typing.Union[CfnTable.ProjectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    contributor_insights_specification: typing.Optional[typing.Union[typing.Union[CfnTable.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    provisioned_throughput: typing.Optional[typing.Union[typing.Union[CfnTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718bfb735c53c4df753bfe5a9a73388b72b6b7a5c9cb396f0300ef4406672f85(
    *,
    input_format: builtins.str,
    s3_bucket_source: typing.Union[typing.Union[CfnTable.S3BucketSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    input_compression_type: typing.Optional[builtins.str] = None,
    input_format_options: typing.Optional[typing.Union[typing.Union[CfnTable.InputFormatOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2618be9553d593cda68c324154302ce946c332678e3950d7030c32a7cdba181c(
    *,
    csv: typing.Optional[typing.Union[typing.Union[CfnTable.CsvProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06cc940eab42d67b773ff8157af3c42e5806b2241741015a3b943c58fc5ba23(
    *,
    attribute_name: builtins.str,
    key_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4173e3e9b222adbdd1234ca9ddd8353adbf7b1e710512b85d185024f3c02211(
    *,
    stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcac9a98632b25795eb0d094c0eb7ce020ae04d36273703d276feff371bc06af(
    *,
    index_name: builtins.str,
    key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    projection: typing.Union[typing.Union[CfnTable.ProjectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baa9db43cfc972ee5bf1b5ba9521012a5128be92bb92dec1b8563be496a9b65(
    *,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0897b4b9796dea226f35dea63debe91e6e511f41df2ac5e7a14cdf9913e142f4(
    *,
    non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    projection_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff28a83c2c1f4fb7bee6cdf58953313cd5159fe058faf732680062688fca3a1(
    *,
    read_capacity_units: jsii.Number,
    write_capacity_units: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c029c869a0c1f5ab867a2830ad96fd8ffdd6ffcbaacdccbe58cfdaaae34dd0(
    *,
    s3_bucket: builtins.str,
    s3_bucket_owner: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcd0cd914dfaaa760893f87c53f947c543a10d21b25d7f32f53b8b6da1defcb(
    *,
    sse_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    kms_master_key_id: typing.Optional[builtins.str] = None,
    sse_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6e167540d028aef1e290eaa63099f021d65666c2dbddb909a00aa19179c373(
    *,
    stream_view_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bfeaa5ee709146cf4c4e2578c645eb4e66e88a97e8f377b8fc8be03aaac182(
    *,
    attribute_name: builtins.str,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc78bc34bb106a907f40bdbe677d639ee2b61288936dd19cc79b6874f6db2742(
    *,
    key_schema: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.KeySchemaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    attribute_definitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.AttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    billing_mode: typing.Optional[builtins.str] = None,
    contributor_insights_specification: typing.Optional[typing.Union[typing.Union[CfnTable.ContributorInsightsSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    global_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.GlobalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    import_source_specification: typing.Optional[typing.Union[typing.Union[CfnTable.ImportSourceSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_stream_specification: typing.Optional[typing.Union[typing.Union[CfnTable.KinesisStreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    local_secondary_indexes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTable.LocalSecondaryIndexProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    point_in_time_recovery_specification: typing.Optional[typing.Union[typing.Union[CfnTable.PointInTimeRecoverySpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    provisioned_throughput: typing.Optional[typing.Union[typing.Union[CfnTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stream_specification: typing.Optional[typing.Union[typing.Union[CfnTable.StreamSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_class: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_to_live_specification: typing.Optional[typing.Union[typing.Union[CfnTable.TimeToLiveSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8fd7d90add35438221014ce0249949bfa9061175978a5cc128f0ff78de8b63(
    *,
    max_capacity: jsii.Number,
    min_capacity: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e8d8fe8957c47430011940e40c90ff53f8590450724e598342eab9a75a9cf0(
    id: builtins.str,
    *,
    schedule: _Schedule_c2a5a45d,
    end_time: typing.Optional[datetime.datetime] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7b2607f481000408ca0428572818f5c6bdbb9fed6e81115c2dd3f9116bb103(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60032d7de59b0cce743f6a33489466642fdf7a4772fe05afc645346a4bb8f797(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a72c99aa6908ffa8e732697a82fbc672394ef9d167d85955e3405245eccc2f(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1c8330ec43f14a6c708e78e5242df9d7c07c7427e915166e6fcc6256e558bb(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3409f2a3618c344be6d9f7f4ff98169acc4e590904d7a92dc30259055dafc6(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682e1b23ead29876f6b964aa061261d32858b9192b31d8ad490d9393bbaa6e33(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b83ef0843e15bfa856c87b3b928d384e2f42b7910f18022dfe2e355dd8f849(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45419850d951c8e2c92a4ef018d4b41da248670ab1c95483faed69c9df2f4c5(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703cb9c708e6170cfc4fc98cc092f234f243919de301984bbacbd47b23dfb7ef(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4af3894bd36cd682954530649231759a53e3e5a7a272a17a3b1608b8e8187d8(
    *,
    partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
    sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2398c4d8a8092a0501d854033bf87064409616a1a27eb43cb06380ec90be295(
    *,
    index_name: builtins.str,
    non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    projection_type: typing.Optional[ProjectionType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2df1695ef53ce52e27e8b9d8d6a5fbbfc4c80ad0017f1e3183882aae3219a7c(
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
    operations: typing.Optional[typing.Sequence[Operation]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea29923c4ccaf6679ececf63cf2b8daf28911ddb13fd632abced46270cafdfc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    kinesis_stream: typing.Optional[_IStream_14c6ec7f] = None,
    table_name: typing.Optional[builtins.str] = None,
    billing_mode: typing.Optional[BillingMode] = None,
    contributor_insights_enabled: typing.Optional[builtins.bool] = None,
    encryption: typing.Optional[TableEncryption] = None,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    point_in_time_recovery: typing.Optional[builtins.bool] = None,
    read_capacity: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_timeout: typing.Optional[_Duration_070aa057] = None,
    server_side_encryption: typing.Optional[builtins.bool] = None,
    stream: typing.Optional[StreamViewType] = None,
    table_class: typing.Optional[TableClass] = None,
    time_to_live_attribute: typing.Optional[builtins.str] = None,
    wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
    write_capacity: typing.Optional[jsii.Number] = None,
    partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
    sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5c07d63555371d61b654b59d911d534e33095941a709ab5cb43dfba9a97c77(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    table_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980d657cde0582520a272daa50682b09c00dd359f25116d406e948c41a2c8b03(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    global_indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
    table_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    table_stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595569c990aa2292a7db1b0d5695312a6ab81ffeb3c61aaef4913998f0883c35(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c61194dced99002b7e63d7e65319a2de58e95d7bdbc3ea6255294218d9b572(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a095b69d37faa53bb5a73051c54ab695bd05b8545a5e440aa72ebfb28a38e3(
    index_name: builtins.str,
    *,
    max_capacity: jsii.Number,
    min_capacity: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c0f431c663f1118d9bffa12428df7bdcfb3cdd5cdf5c0ebe3361b16ae988d1(
    index_name: builtins.str,
    *,
    max_capacity: jsii.Number,
    min_capacity: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b0b2130c10ca06ef0313012d738fe5cb717fac1ab57b35f09cf285bd38339d(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e57f6316eeaa5af8316fcc3679968ea578aa2c98f59bc3f8fdbdd9b23ded5f(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f98f6a698f48f5de9f786d3e782d94e03f19b475e1aa341df7a660933d88503(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f294325b8a881305f7a7764ec025316493b813eed9536133957dadcdb51c02(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d07ff8771a4839c2221a01140f69e39241e25ac7deb1a681054334419bdc378(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ace47aecbb9f1270afb7345eb951fc887108e79a5e918af72c627d5eecf6499(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75e0142b4bb76502b18a0bff91e4ebff82c6783fecae351b4cb9061db6cd523(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a40174682421a0a672d3c91e86c55d631fc79e37f4cfb58812e3199f392ee1(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5add888be5b7ec8e0343bb052fb0e9560b78e32215fa8a7bdcb6d58abbe486(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a6d02c1dd045f47b1691ceb9e29ed5d882d80600ea8f0f04347c1a53eb28e0(
    operation: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be525c1780cb31b87140c8aa5629003cb7b6c8b45b931822540d6b8c8bdc6917(
    index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f301cf436b0ac904f16e15b35a8792bb72d2edab625d7ab85e78883b8692340(
    *,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    global_indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_indexes: typing.Optional[typing.Sequence[builtins.str]] = None,
    table_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    table_stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3462a9f3e3a4e301259511b7b046e264ce4eed8bc1263f48f972dcc4018849(
    *,
    partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
    sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
    billing_mode: typing.Optional[BillingMode] = None,
    contributor_insights_enabled: typing.Optional[builtins.bool] = None,
    encryption: typing.Optional[TableEncryption] = None,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    point_in_time_recovery: typing.Optional[builtins.bool] = None,
    read_capacity: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_timeout: typing.Optional[_Duration_070aa057] = None,
    server_side_encryption: typing.Optional[builtins.bool] = None,
    stream: typing.Optional[StreamViewType] = None,
    table_class: typing.Optional[TableClass] = None,
    time_to_live_attribute: typing.Optional[builtins.str] = None,
    wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
    write_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c6aa67c2622b786574c5df48e5ca3d844b5fb21317d9704e6225b88bae9fc9(
    *,
    partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
    sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
    billing_mode: typing.Optional[BillingMode] = None,
    contributor_insights_enabled: typing.Optional[builtins.bool] = None,
    encryption: typing.Optional[TableEncryption] = None,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    point_in_time_recovery: typing.Optional[builtins.bool] = None,
    read_capacity: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_timeout: typing.Optional[_Duration_070aa057] = None,
    server_side_encryption: typing.Optional[builtins.bool] = None,
    stream: typing.Optional[StreamViewType] = None,
    table_class: typing.Optional[TableClass] = None,
    time_to_live_attribute: typing.Optional[builtins.str] = None,
    wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
    write_capacity: typing.Optional[jsii.Number] = None,
    kinesis_stream: typing.Optional[_IStream_14c6ec7f] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610af3e0a1310b39ee25edafe838dc3766987bc96bd9e2e955be17ba57765faf(
    *,
    disable_scale_in: typing.Optional[builtins.bool] = None,
    policy_name: typing.Optional[builtins.str] = None,
    scale_in_cooldown: typing.Optional[_Duration_070aa057] = None,
    scale_out_cooldown: typing.Optional[_Duration_070aa057] = None,
    target_utilization_percent: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2c307fbcb4f8ca783da6df7736a73d017d606d99f6363a3559377475f17d48(
    *,
    index_name: builtins.str,
    non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    projection_type: typing.Optional[ProjectionType] = None,
    partition_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
    sort_key: typing.Optional[typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]]] = None,
    read_capacity: typing.Optional[jsii.Number] = None,
    write_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea3816a7fd77b7dbc148beefca3fd2034bdb880c8eb1d61bbdfd2f52e64b7ae(
    *,
    index_name: builtins.str,
    non_key_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    projection_type: typing.Optional[ProjectionType] = None,
    sort_key: typing.Union[Attribute, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass
