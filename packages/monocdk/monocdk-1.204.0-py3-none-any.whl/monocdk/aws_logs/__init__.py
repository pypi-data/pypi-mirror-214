'''
# Amazon CloudWatch Logs Construct Library

This library supplies constructs for working with CloudWatch Logs.

## Log Groups/Streams

The basic unit of CloudWatch is a *Log Group*. Every log group typically has the
same kind of data logged to it, in the same format. If there are multiple
applications or services logging into the Log Group, each of them creates a new
*Log Stream*.

Every log operation creates a "log event", which can consist of a simple string
or a single-line JSON object. JSON objects have the advantage that they afford
more filtering abilities (see below).

The only configurable attribute for log streams is the retention period, which
configures after how much time the events in the log stream expire and are
deleted.

The default retention period if not supplied is 2 years, but it can be set to
one of the values in the `RetentionDays` enum to configure a different
retention period (including infinite retention).

```python
# Configure log group for short retention
log_group = LogGroup(stack, "LogGroup",
    retention=RetentionDays.ONE_WEEK
)# Configure log group for infinite retention
log_group = LogGroup(stack, "LogGroup",
    retention=Infinity
)
```

## LogRetention

The `LogRetention` construct is a way to control the retention period of log groups that are created outside of the CDK. The construct is usually
used on log groups that are auto created by AWS services, such as [AWS
lambda](https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html).

This is implemented using a [CloudFormation custom
resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html)
which pre-creates the log group if it doesn't exist, and sets the specified log retention period (never expire, by default).

By default, the log group will be created in the same region as the stack. The `logGroupRegion` property can be used to configure
log groups in other regions. This is typically useful when controlling retention for log groups auto-created by global services that
publish their log group to a specific region, such as AWS Chatbot creating a log group in `us-east-1`.

## Resource Policy

CloudWatch Resource Policies allow other AWS services or IAM Principals to put log events into the log groups.
A resource policy is automatically created when `addToResourcePolicy` is called on the LogGroup for the first time:

```python
log_group = logs.LogGroup(self, "LogGroup")
log_group.add_to_resource_policy(iam.PolicyStatement(
    actions=["logs:CreateLogStream", "logs:PutLogEvents"],
    principals=[iam.ServicePrincipal("es.amazonaws.com")],
    resources=[log_group.log_group_arn]
))
```

Or more conveniently, write permissions to the log group can be granted as follows which gives same result as in the above example.

```python
log_group = logs.LogGroup(self, "LogGroup")
log_group.grant_write(iam.ServicePrincipal("es.amazonaws.com"))
```

Be aware that any ARNs or tokenized values passed to the resource policy will be converted into AWS Account IDs.
This is because CloudWatch Logs Resource Policies do not accept ARNs as principals, but they do accept
Account ID strings. Non-ARN principals, like Service principals or Any princpals, are accepted by CloudWatch.

## Encrypting Log Groups

By default, log group data is always encrypted in CloudWatch Logs. You have the
option to encrypt log group data using a AWS KMS customer master key (CMK) should
you not wish to use the default AWS encryption. Keep in mind that if you decide to
encrypt a log group, any service or IAM identity that needs to read the encrypted
log streams in the future will require the same CMK to decrypt the data.

Here's a simple example of creating an encrypted Log Group using a KMS CMK.

```python
import monocdk as kms


logs.LogGroup(self, "LogGroup",
    encryption_key=kms.Key(self, "Key")
)
```

See the AWS documentation for more detailed information about [encrypting CloudWatch
Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html).

## Subscriptions and Destinations

Log events matching a particular filter can be sent to either a Lambda function
or a Kinesis stream.

If the Kinesis stream lives in a different account, a `CrossAccountDestination`
object needs to be added in the destination account which will act as a proxy
for the remote Kinesis stream. This object is automatically created for you
if you use the CDK Kinesis library.

Create a `SubscriptionFilter`, initialize it with an appropriate `Pattern` (see
below) and supply the intended destination:

```python
import monocdk as destinations
# fn: lambda.Function
# log_group: logs.LogGroup


logs.SubscriptionFilter(self, "Subscription",
    log_group=log_group,
    destination=destinations.LambdaDestination(fn),
    filter_pattern=logs.FilterPattern.all_terms("ERROR", "MainThread")
)
```

## Metric Filters

CloudWatch Logs can extract and emit metrics based on a textual log stream.
Depending on your needs, this may be a more convenient way of generating metrics
for you application than making calls to CloudWatch Metrics yourself.

A `MetricFilter` either emits a fixed number every time it sees a log event
matching a particular pattern (see below), or extracts a number from the log
event and uses that as the metric value.

Example:

```python
MetricFilter(self, "MetricFilter",
    log_group=log_group,
    metric_namespace="MyApp",
    metric_name="Latency",
    filter_pattern=FilterPattern.exists("$.latency"),
    metric_value="$.latency"
)
```

Remember that if you want to use a value from the log event as the metric value,
you must mention it in your pattern somewhere.

A very simple MetricFilter can be created by using the `logGroup.extractMetric()`
helper function:

```python
# log_group: logs.LogGroup

log_group.extract_metric("$.jsonField", "Namespace", "MetricName")
```

Will extract the value of `jsonField` wherever it occurs in JSON-structed
log records in the LogGroup, and emit them to CloudWatch Metrics under
the name `Namespace/MetricName`.

### Exposing Metric on a Metric Filter

You can expose a metric on a metric filter by calling the `MetricFilter.metric()` API.
This has a default of `statistic = 'avg'` if the statistic is not set in the `props`.

```python
# log_group: logs.LogGroup

mf = logs.MetricFilter(self, "MetricFilter",
    log_group=log_group,
    metric_namespace="MyApp",
    metric_name="Latency",
    filter_pattern=logs.FilterPattern.exists("$.latency"),
    metric_value="$.latency"
)

# expose a metric from the metric filter
metric = mf.metric()

# you can use the metric to create a new alarm
cloudwatch.Alarm(self, "alarm from metric filter",
    metric=metric,
    threshold=100,
    evaluation_periods=2
)
```

## Patterns

Patterns describe which log events match a subscription or metric filter. There
are three types of patterns:

* Text patterns
* JSON patterns
* Space-delimited table patterns

All patterns are constructed by using static functions on the `FilterPattern`
class.

In addition to the patterns above, the following special patterns exist:

* `FilterPattern.allEvents()`: matches all log events.
* `FilterPattern.literal(string)`: if you already know what pattern expression to
  use, this function takes a string and will use that as the log pattern. For
  more information, see the [Filter and Pattern
  Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html).

### Text Patterns

Text patterns match if the literal strings appear in the text form of the log
line.

* `FilterPattern.allTerms(term, term, ...)`: matches if all of the given terms
  (substrings) appear in the log event.
* `FilterPattern.anyTerm(term, term, ...)`: matches if all of the given terms
  (substrings) appear in the log event.
* `FilterPattern.anyTermGroup([term, term, ...], [term, term, ...], ...)`: matches if
  all of the terms in any of the groups (specified as arrays) matches. This is
  an OR match.

Examples:

```python
# Search for lines that contain both "ERROR" and "MainThread"
pattern1 = logs.FilterPattern.all_terms("ERROR", "MainThread")

# Search for lines that either contain both "ERROR" and "MainThread", or
# both "WARN" and "Deadlock".
pattern2 = logs.FilterPattern.any_term_group(["ERROR", "MainThread"], ["WARN", "Deadlock"])
```

## JSON Patterns

JSON patterns apply if the log event is the JSON representation of an object
(without any other characters, so it cannot include a prefix such as timestamp
or log level). JSON patterns can make comparisons on the values inside the
fields.

* **Strings**: the comparison operators allowed for strings are `=` and `!=`.
  String values can start or end with a `*` wildcard.
* **Numbers**: the comparison operators allowed for numbers are `=`, `!=`,
  `<`, `<=`, `>`, `>=`.

Fields in the JSON structure are identified by identifier the complete object as `$`
and then descending into it, such as `$.field` or `$.list[0].field`.

* `FilterPattern.stringValue(field, comparison, string)`: matches if the given
  field compares as indicated with the given string value.
* `FilterPattern.numberValue(field, comparison, number)`: matches if the given
  field compares as indicated with the given numerical value.
* `FilterPattern.isNull(field)`: matches if the given field exists and has the
  value `null`.
* `FilterPattern.notExists(field)`: matches if the given field is not in the JSON
  structure.
* `FilterPattern.exists(field)`: matches if the given field is in the JSON
  structure.
* `FilterPattern.booleanValue(field, boolean)`: matches if the given field
  is exactly the given boolean value.
* `FilterPattern.all(jsonPattern, jsonPattern, ...)`: matches if all of the
  given JSON patterns match. This makes an AND combination of the given
  patterns.
* `FilterPattern.any(jsonPattern, jsonPattern, ...)`: matches if any of the
  given JSON patterns match. This makes an OR combination of the given
  patterns.

Example:

```python
# Search for all events where the component field is equal to
# "HttpServer" and either error is true or the latency is higher
# than 1000.
pattern = logs.FilterPattern.all(
    logs.FilterPattern.string_value("$.component", "=", "HttpServer"),
    logs.FilterPattern.any(
        logs.FilterPattern.boolean_value("$.error", True),
        logs.FilterPattern.number_value("$.latency", ">", 1000)))
```

## Space-delimited table patterns

If the log events are rows of a space-delimited table, this pattern can be used
to identify the columns in that structure and add conditions on any of them. The
canonical example where you would apply this type of pattern is Apache server
logs.

Text that is surrounded by `"..."` quotes or `[...]` square brackets will
be treated as one column.

* `FilterPattern.spaceDelimited(column, column, ...)`: construct a
  `SpaceDelimitedTextPattern` object with the indicated columns. The columns
  map one-by-one the columns found in the log event. The string `"..."` may
  be used to specify an arbitrary number of unnamed columns anywhere in the
  name list (but may only be specified once).

After constructing a `SpaceDelimitedTextPattern`, you can use the following
two members to add restrictions:

* `pattern.whereString(field, comparison, string)`: add a string condition.
  The rules are the same as for JSON patterns.
* `pattern.whereNumber(field, comparison, number)`: add a numerical condition.
  The rules are the same as for JSON patterns.

Multiple restrictions can be added on the same column; they must all apply.

Example:

```python
# Search for all events where the component is "HttpServer" and the
# result code is not equal to 200.
pattern = logs.FilterPattern.space_delimited("time", "component", "...", "result_code", "latency").where_string("component", "=", "HttpServer").where_number("result_code", "!=", 200)
```

## Logs Insights Query Definition

Creates a query definition for CloudWatch Logs Insights.

Example:

```python
logs.QueryDefinition(self, "QueryDefinition",
    query_definition_name="MyQuery",
    query_string=logs.QueryString(
        fields=["@timestamp", "@message"],
        sort="@timestamp desc",
        limit=20
    )
)
```

## Notes

Be aware that Log Group ARNs will always have the string `:*` appended to
them, to match the behavior of [the CloudFormation `AWS::Logs::LogGroup`
resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#aws-resource-logs-loggroup-return-values).
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
from ..aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_iam import (
    AddToResourcePolicyResult as _AddToResourcePolicyResult_0fd9d2a9,
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IResourceWithPolicy as _IResourceWithPolicy_b83339b0,
    IRole as _IRole_59af6f50,
    PolicyDocument as _PolicyDocument_b5de5177,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_kms import IKey as _IKey_36930160


@jsii.implements(_IInspectable_82c04a63)
class CfnDestination(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnDestination",
):
    '''A CloudFormation ``AWS::Logs::Destination``.

    The AWS::Logs::Destination resource specifies a CloudWatch Logs destination. A destination encapsulates a physical resource (such as an Amazon Kinesis data stream) and enables you to subscribe that resource to a stream of log events.

    :cloudformationResource: AWS::Logs::Destination
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_logs as logs
        
        cfn_destination = logs.CfnDestination(self, "MyCfnDestination",
            destination_name="destinationName",
            role_arn="roleArn",
            target_arn="targetArn",
        
            # the properties below are optional
            destination_policy="destinationPolicy"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        destination_name: builtins.str,
        role_arn: builtins.str,
        target_arn: builtins.str,
        destination_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::Destination``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_name: The name of the destination.
        :param role_arn: The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.
        :param target_arn: The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).
        :param destination_policy: An IAM policy document that governs which AWS accounts can create subscription filters against this destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd366b11808e27e134ad0197dec51f8dfe7485d17307a2dfdd2a29c5da54219)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDestinationProps(
            destination_name=destination_name,
            role_arn=role_arn,
            target_arn=target_arn,
            destination_policy=destination_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4eb1d4e64853911a9612b45bdc1f28d1343b85025183b4bd894df329899f56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fccee2a62a5f07a27f8c76396414a95d3fef2278e7e62cf4eb8da2a6980f8a0a)
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
        '''The ARN of the CloudWatch Logs destination, such as ``arn:aws:logs:us-west-1:123456789012:destination:MyDestination`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> builtins.str:
        '''The name of the destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationName"))

    @destination_name.setter
    def destination_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32acc85d0429c0fe249d91678db9f28392c12be0b4735928bd8db5b5715bd7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be8d8d60bff686aec5167eeec4b1d33f5a199acf29369cbb8581f68edc7abfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db4fe7ae950d68e999870d97794febac8633356fe2fb04e9d8cf718214bed39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value)

    @builtins.property
    @jsii.member(jsii_name="destinationPolicy")
    def destination_policy(self) -> typing.Optional[builtins.str]:
        '''An IAM policy document that governs which AWS accounts can create subscription filters against this destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPolicy"))

    @destination_policy.setter
    def destination_policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9447363130e595be514f1c565b5fbb02e200cfd137a03c6b1c0592a5ec7360b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPolicy", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_name": "destinationName",
        "role_arn": "roleArn",
        "target_arn": "targetArn",
        "destination_policy": "destinationPolicy",
    },
)
class CfnDestinationProps:
    def __init__(
        self,
        *,
        destination_name: builtins.str,
        role_arn: builtins.str,
        target_arn: builtins.str,
        destination_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDestination``.

        :param destination_name: The name of the destination.
        :param role_arn: The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.
        :param target_arn: The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).
        :param destination_policy: An IAM policy document that governs which AWS accounts can create subscription filters against this destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            cfn_destination_props = logs.CfnDestinationProps(
                destination_name="destinationName",
                role_arn="roleArn",
                target_arn="targetArn",
            
                # the properties below are optional
                destination_policy="destinationPolicy"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc86692bf80e03d5976c96e595483f7ba735691cced9ab50d2260d7209a476b)
            check_type(argname="argument destination_name", value=destination_name, expected_type=type_hints["destination_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument destination_policy", value=destination_policy, expected_type=type_hints["destination_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_name": destination_name,
            "role_arn": role_arn,
            "target_arn": target_arn,
        }
        if destination_policy is not None:
            self._values["destination_policy"] = destination_policy

    @builtins.property
    def destination_name(self) -> builtins.str:
        '''The name of the destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        '''
        result = self._values.get("destination_name")
        assert result is not None, "Required property 'destination_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_policy(self) -> typing.Optional[builtins.str]:
        '''An IAM policy document that governs which AWS accounts can create subscription filters against this destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        '''
        result = self._values.get("destination_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLogGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnLogGroup",
):
    '''A CloudFormation ``AWS::Logs::LogGroup``.

    The ``AWS::Logs::LogGroup`` resource specifies a log group. A log group defines common properties for log streams, such as their retention and access control rules. Each log stream must belong to one log group.

    You can create up to 1,000,000 log groups per Region per account. You must use the following guidelines when naming a log group:

    - Log group names must be unique within a Region for an AWS account.
    - Log group names can be between 1 and 512 characters long.
    - Log group names consist of the following characters: a-z, A-Z, 0-9, '_' (underscore), '-' (hyphen), '/' (forward slash), and '.' (period).

    :cloudformationResource: AWS::Logs::LogGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_logs as logs
        
        # data_protection_policy: Any
        
        cfn_log_group = logs.CfnLogGroup(self, "MyCfnLogGroup",
            data_protection_policy=data_protection_policy,
            kms_key_id="kmsKeyId",
            log_group_name="logGroupName",
            retention_in_days=123,
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
        data_protection_policy: typing.Any = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::LogGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_protection_policy: Creates a data protection policy and assigns it to the log group. A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks. For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .
        :param kms_key_id: The Amazon Resource Name (ARN) of the AWS KMS key to use when encrypting log data. To associate an AWS KMS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested. If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error. Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS KMS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_
        :param log_group_name: The name of the log group. If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.
        :param retention_in_days: The number of days to retain the log events in the specified log group. Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653. To set a log group so that its log events do not expire, use `DeleteRetentionPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteRetentionPolicy.html>`_ .
        :param tags: An array of key-value pairs to apply to the log group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36bc84863cf3c073756e31b583685df56c11046f4104f2f6cbdca1d7578ba83)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLogGroupProps(
            data_protection_policy=data_protection_policy,
            kms_key_id=kms_key_id,
            log_group_name=log_group_name,
            retention_in_days=retention_in_days,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f953123a3452c9b24f8de2ee1c531834b7a64b513052dbe9ade88e5f14c9bf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d96abd0e04d68a03fa0f154bd2755c69d3590cdb2e6bc7202c352eb4a68e48ec)
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
        '''The ARN of the log group, such as ``arn:aws:logs:us-west-1:123456789012:log-group:/mystack-testgroup-12ABC1AB12A1:*``.

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
        '''An array of key-value pairs to apply to the log group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionPolicy")
    def data_protection_policy(self) -> typing.Any:
        '''Creates a data protection policy and assigns it to the log group.

        A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks.

        For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-dataprotectionpolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "dataProtectionPolicy"))

    @data_protection_policy.setter
    def data_protection_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5290dcda35696cf43b5727908fa2d558fe21447b24ca80c2f4202274a904051a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataProtectionPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS KMS key to use when encrypting log data.

        To associate an AWS KMS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested.

        If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error.

        Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS KMS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdad71d01c1afd05263e1259d8ad95b9f622acb1a63dbeb6374bd2397bde83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log group.

        If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-loggroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cafe04c904bc5232bdde564693af5841b02728bffb99e1ce501078ae22c71d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="retentionInDays")
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain the log events in the specified log group.

        Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653.

        To set a log group so that its log events do not expire, use `DeleteRetentionPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteRetentionPolicy.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-retentionindays
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionInDays"))

    @retention_in_days.setter
    def retention_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac3993ff0f47a088df1fb3993244523d26bb7831a1d897a228020ad081e02d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionInDays", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnLogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_protection_policy": "dataProtectionPolicy",
        "kms_key_id": "kmsKeyId",
        "log_group_name": "logGroupName",
        "retention_in_days": "retentionInDays",
        "tags": "tags",
    },
)
class CfnLogGroupProps:
    def __init__(
        self,
        *,
        data_protection_policy: typing.Any = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLogGroup``.

        :param data_protection_policy: Creates a data protection policy and assigns it to the log group. A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks. For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .
        :param kms_key_id: The Amazon Resource Name (ARN) of the AWS KMS key to use when encrypting log data. To associate an AWS KMS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested. If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error. Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS KMS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_
        :param log_group_name: The name of the log group. If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.
        :param retention_in_days: The number of days to retain the log events in the specified log group. Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653. To set a log group so that its log events do not expire, use `DeleteRetentionPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteRetentionPolicy.html>`_ .
        :param tags: An array of key-value pairs to apply to the log group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            # data_protection_policy: Any
            
            cfn_log_group_props = logs.CfnLogGroupProps(
                data_protection_policy=data_protection_policy,
                kms_key_id="kmsKeyId",
                log_group_name="logGroupName",
                retention_in_days=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a625215d9327f9864a73debe7c9e0c517923916936e53690238516db9f79da78)
            check_type(argname="argument data_protection_policy", value=data_protection_policy, expected_type=type_hints["data_protection_policy"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument retention_in_days", value=retention_in_days, expected_type=type_hints["retention_in_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_protection_policy is not None:
            self._values["data_protection_policy"] = data_protection_policy
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if retention_in_days is not None:
            self._values["retention_in_days"] = retention_in_days
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_protection_policy(self) -> typing.Any:
        '''Creates a data protection policy and assigns it to the log group.

        A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks.

        For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-dataprotectionpolicy
        '''
        result = self._values.get("data_protection_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS KMS key to use when encrypting log data.

        To associate an AWS KMS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested.

        If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error.

        Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS KMS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log group.

        If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain the log events in the specified log group.

        Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653.

        To set a log group so that its log events do not expire, use `DeleteRetentionPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteRetentionPolicy.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-retentionindays
        '''
        result = self._values.get("retention_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to the log group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLogStream(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnLogStream",
):
    '''A CloudFormation ``AWS::Logs::LogStream``.

    The ``AWS::Logs::LogStream`` resource specifies an Amazon CloudWatch Logs log stream in a specific log group. A log stream represents the sequence of events coming from an application instance or resource that you are monitoring.

    There is no limit on the number of log streams that you can create for a log group.

    You must use the following guidelines when naming a log stream:

    - Log stream names must be unique within the log group.
    - Log stream names can be between 1 and 512 characters long.
    - The ':' (colon) and '*' (asterisk) characters are not allowed.

    :cloudformationResource: AWS::Logs::LogStream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_logs as logs
        
        cfn_log_stream = logs.CfnLogStream(self, "MyCfnLogStream",
            log_group_name="logGroupName",
        
            # the properties below are optional
            log_stream_name="logStreamName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        log_group_name: builtins.str,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::LogStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param log_group_name: The name of the log group where the log stream is created.
        :param log_stream_name: The name of the log stream. The name must be unique within the log group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60c8c8a73232433901aff1d23c0083d11607db169b3d20774309640c4dbf1d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLogStreamProps(
            log_group_name=log_group_name, log_stream_name=log_stream_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed8bc226d18d8600f85181d259003888fe69db70006a3fc3a94ca6d510b77eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f1af18e5d46ba48a5e15d1d7d39d7bfa484712f31e8f7957fc7bd471651f191)
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
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The name of the log group where the log stream is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d203cc5c6d04d07178aaf4a1b0619d42be968d68cb9d0bbcf0281928650320e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log stream.

        The name must be unique within the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100b1127258df06af75a75f8484fbd6617f0a43429de3163c2a0baae15d5e8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnLogStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class CfnLogStreamProps:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLogStream``.

        :param log_group_name: The name of the log group where the log stream is created.
        :param log_stream_name: The name of the log stream. The name must be unique within the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            cfn_log_stream_props = logs.CfnLogStreamProps(
                log_group_name="logGroupName",
            
                # the properties below are optional
                log_stream_name="logStreamName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38dc3079ece170f6873cfbbadd6f87785ab37fad9a1c4cb895d13cfdd89783ef)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
        }
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''The name of the log group where the log stream is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log stream.

        The name must be unique within the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnMetricFilter(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnMetricFilter",
):
    '''A CloudFormation ``AWS::Logs::MetricFilter``.

    The ``AWS::Logs::MetricFilter`` resource specifies a metric filter that describes how CloudWatch Logs extracts information from logs and transforms it into Amazon CloudWatch metrics. If you have multiple metric filters that are associated with a log group, all the filters are applied to the log streams in that group.

    The maximum number of metric filters that can be associated with a log group is 100.

    :cloudformationResource: AWS::Logs::MetricFilter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_logs as logs
        
        cfn_metric_filter = logs.CfnMetricFilter(self, "MyCfnMetricFilter",
            filter_pattern="filterPattern",
            log_group_name="logGroupName",
            metric_transformations=[logs.CfnMetricFilter.MetricTransformationProperty(
                metric_name="metricName",
                metric_namespace="metricNamespace",
                metric_value="metricValue",
        
                # the properties below are optional
                default_value=123,
                dimensions=[logs.CfnMetricFilter.DimensionProperty(
                    key="key",
                    value="value"
                )],
                unit="unit"
            )],
        
            # the properties below are optional
            filter_name="filterName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        metric_transformations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnMetricFilter.MetricTransformationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        filter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::MetricFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param filter_pattern: A filter pattern for extracting metric data out of ingested log events. For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The name of an existing log group that you want to associate with this metric filter.
        :param metric_transformations: The metric transformations.
        :param filter_name: The name of the metric filter.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e20b6b1a449989796d745885365a86b5926e6683cc8c7c3df4d2b681fd4107)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMetricFilterProps(
            filter_pattern=filter_pattern,
            log_group_name=log_group_name,
            metric_transformations=metric_transformations,
            filter_name=filter_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bc5001111212e97d57d09d9c297faf5cb9108218300c23ad5167f3312e20ace)
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
            type_hints = typing.get_type_hints(_typecheckingstub__903d42219c1d8ec2ac4b00b49f411a8c48f8a223c3865d8390137d5944c68960)
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
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> builtins.str:
        '''A filter pattern for extracting metric data out of ingested log events.

        For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filterpattern
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterPattern"))

    @filter_pattern.setter
    def filter_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1249d76ed1279862a5802042d67bdcb33c9ee1f82ad6dff0f72df6d8ac6c3aea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPattern", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The name of an existing log group that you want to associate with this metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7c4b13dc093ea849aa48200bd454cc05b1e905649876386c377c401cbedf0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="metricTransformations")
    def metric_transformations(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_a771d0ef]]]:
        '''The metric transformations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-metrictransformations
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_a771d0ef]]], jsii.get(self, "metricTransformations"))

    @metric_transformations.setter
    def metric_transformations(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c3c686f0d59b99cb9a9068c5b6900f196068faa8d566af526c6f23ed78b17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricTransformations", value)

    @builtins.property
    @jsii.member(jsii_name="filterName")
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filtername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterName"))

    @filter_name.setter
    def filter_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9822c1819ab526b1dcf91859e0f7b45194deea4250b31f4d0f3b543a474201b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_logs.CfnMetricFilter.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''Specifies the CloudWatch metric dimensions to publish with this metric.

            Because dimensions are part of the unique identifier for a metric, whenever a unique dimension name/value pair is extracted from your logs, you are creating a new variation of that metric.

            For more information about publishing dimensions with metrics created by metric filters, see `Publishing dimensions with metrics from values in JSON or space-delimited log events <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html#logs-metric-filters-dimensions>`_ .
            .. epigraph::

               Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric.

               To help prevent accidental high charges, Amazon disables a metric filter if it generates 1000 different name/value pairs for the dimensions that you have specified within a certain amount of time.

               You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .

            :param key: The name for the CloudWatch metric dimension that the metric filter creates. Dimension names must contain only ASCII characters, must include at least one non-whitespace character, and cannot start with a colon (:).
            :param value: The log event field that will contain the value for this dimension. This dimension will only be published for a metric if the value is found in the log event. For example, ``$.eventType`` for JSON log events, or ``$server`` for space-delimited log events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_logs as logs
                
                dimension_property = logs.CfnMetricFilter.DimensionProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e31aba6414afd737e80dd81a17d0fc3908210ff53250534fbc338f86d00d5c1b)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The name for the CloudWatch metric dimension that the metric filter creates.

            Dimension names must contain only ASCII characters, must include at least one non-whitespace character, and cannot start with a colon (:).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html#cfn-logs-metricfilter-dimension-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The log event field that will contain the value for this dimension.

            This dimension will only be published for a metric if the value is found in the log event. For example, ``$.eventType`` for JSON log events, or ``$server`` for space-delimited log events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html#cfn-logs-metricfilter-dimension-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_logs.CfnMetricFilter.MetricTransformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric_name": "metricName",
            "metric_namespace": "metricNamespace",
            "metric_value": "metricValue",
            "default_value": "defaultValue",
            "dimensions": "dimensions",
            "unit": "unit",
        },
    )
    class MetricTransformationProperty:
        def __init__(
            self,
            *,
            metric_name: builtins.str,
            metric_namespace: builtins.str,
            metric_value: builtins.str,
            default_value: typing.Optional[jsii.Number] = None,
            dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnMetricFilter.DimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetricTransformation`` is a property of the ``AWS::Logs::MetricFilter`` resource that describes how to transform log streams into a CloudWatch metric.

            :param metric_name: The name of the CloudWatch metric.
            :param metric_namespace: A custom namespace to contain your metric in CloudWatch. Use namespaces to group together metrics that are similar. For more information, see `Namespaces <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace>`_ .
            :param metric_value: The value that is published to the CloudWatch metric. For example, if you're counting the occurrences of a particular term like ``Error`` , specify 1 for the metric value. If you're counting the number of bytes transferred, reference the value that is in the log event by using $. followed by the name of the field that you specified in the filter pattern, such as ``$.size`` .
            :param default_value: (Optional) The value to emit when a filter pattern does not match a log event. This value can be null.
            :param dimensions: The fields to use as dimensions for the metric. One metric filter can include as many as three dimensions. .. epigraph:: Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric. CloudWatch Logs disables a metric filter if it generates 1000 different name/value pairs for your specified dimensions within a certain amount of time. This helps to prevent accidental high charges. You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .
            :param unit: The unit to assign to the metric. If you omit this, the unit is set as ``None`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_logs as logs
                
                metric_transformation_property = logs.CfnMetricFilter.MetricTransformationProperty(
                    metric_name="metricName",
                    metric_namespace="metricNamespace",
                    metric_value="metricValue",
                
                    # the properties below are optional
                    default_value=123,
                    dimensions=[logs.CfnMetricFilter.DimensionProperty(
                        key="key",
                        value="value"
                    )],
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de36e210a18a9ef57b44ae06fa0064253b0670f44ceb4de0bf26e80a9587e4b5)
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
                check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "metric_name": metric_name,
                "metric_namespace": metric_namespace,
                "metric_value": metric_value,
            }
            if default_value is not None:
                self._values["default_value"] = default_value
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''The name of the CloudWatch metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_namespace(self) -> builtins.str:
            '''A custom namespace to contain your metric in CloudWatch.

            Use namespaces to group together metrics that are similar. For more information, see `Namespaces <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricnamespace
            '''
            result = self._values.get("metric_namespace")
            assert result is not None, "Required property 'metric_namespace' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_value(self) -> builtins.str:
            '''The value that is published to the CloudWatch metric.

            For example, if you're counting the occurrences of a particular term like ``Error`` , specify 1 for the metric value. If you're counting the number of bytes transferred, reference the value that is in the log event by using $. followed by the name of the field that you specified in the filter pattern, such as ``$.size`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricvalue
            '''
            result = self._values.get("metric_value")
            assert result is not None, "Required property 'metric_value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def default_value(self) -> typing.Optional[jsii.Number]:
            '''(Optional) The value to emit when a filter pattern does not match a log event.

            This value can be null.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.DimensionProperty", _IResolvable_a771d0ef]]]]:
            '''The fields to use as dimensions for the metric. One metric filter can include as many as three dimensions.

            .. epigraph::

               Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric.

               CloudWatch Logs disables a metric filter if it generates 1000 different name/value pairs for your specified dimensions within a certain amount of time. This helps to prevent accidental high charges.

               You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.DimensionProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to assign to the metric.

            If you omit this, the unit is set as ``None`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricTransformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnMetricFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "filter_pattern": "filterPattern",
        "log_group_name": "logGroupName",
        "metric_transformations": "metricTransformations",
        "filter_name": "filterName",
    },
)
class CfnMetricFilterProps:
    def __init__(
        self,
        *,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        metric_transformations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricFilter.MetricTransformationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        filter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMetricFilter``.

        :param filter_pattern: A filter pattern for extracting metric data out of ingested log events. For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The name of an existing log group that you want to associate with this metric filter.
        :param metric_transformations: The metric transformations.
        :param filter_name: The name of the metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            cfn_metric_filter_props = logs.CfnMetricFilterProps(
                filter_pattern="filterPattern",
                log_group_name="logGroupName",
                metric_transformations=[logs.CfnMetricFilter.MetricTransformationProperty(
                    metric_name="metricName",
                    metric_namespace="metricNamespace",
                    metric_value="metricValue",
            
                    # the properties below are optional
                    default_value=123,
                    dimensions=[logs.CfnMetricFilter.DimensionProperty(
                        key="key",
                        value="value"
                    )],
                    unit="unit"
                )],
            
                # the properties below are optional
                filter_name="filterName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75abbbbaad23c2e2fa6e36cdde1ae09e1ae1fce2b702d94b90bb872b38ad0d6)
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument metric_transformations", value=metric_transformations, expected_type=type_hints["metric_transformations"])
            check_type(argname="argument filter_name", value=filter_name, expected_type=type_hints["filter_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "log_group_name": log_group_name,
            "metric_transformations": metric_transformations,
        }
        if filter_name is not None:
            self._values["filter_name"] = filter_name

    @builtins.property
    def filter_pattern(self) -> builtins.str:
        '''A filter pattern for extracting metric data out of ingested log events.

        For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filterpattern
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''The name of an existing log group that you want to associate with this metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_transformations(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricFilter.MetricTransformationProperty, _IResolvable_a771d0ef]]]:
        '''The metric transformations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-metrictransformations
        '''
        result = self._values.get("metric_transformations")
        assert result is not None, "Required property 'metric_transformations' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricFilter.MetricTransformationProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filtername
        '''
        result = self._values.get("filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnQueryDefinition(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnQueryDefinition",
):
    '''A CloudFormation ``AWS::Logs::QueryDefinition``.

    Creates a query definition for CloudWatch Logs Insights. For more information, see `Analyzing Log Data with CloudWatch Logs Insights <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html>`_ .

    :cloudformationResource: AWS::Logs::QueryDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_logs as logs
        
        cfn_query_definition = logs.CfnQueryDefinition(self, "MyCfnQueryDefinition",
            name="name",
            query_string="queryString",
        
            # the properties below are optional
            log_group_names=["logGroupNames"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        query_string: builtins.str,
        log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::QueryDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the query definition.
        :param query_string: The query string to use for this query definition. For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .
        :param log_group_names: Use this parameter if you want the query to query only certain log groups.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12de71f864ff4f28fdb606d12311c3f3ab47c4b59c6b4457f5a5df86d3bd00a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnQueryDefinitionProps(
            name=name, query_string=query_string, log_group_names=log_group_names
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387cfb50c0f81082b33fffefdf678ab79c9f7fe2133de048c09f33d021113560)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c58130be6056c2d0862cb96eb421c902ffd2f9bae92f78d9c3e9be9f05b04b5b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrQueryDefinitionId")
    def attr_query_definition_id(self) -> builtins.str:
        '''The ID of the query definition.

        :cloudformationAttribute: QueryDefinitionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrQueryDefinitionId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the query definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d003ded7fc1d367b7418a4517d01fb5dc3b60fd5f7b41f6c93179dbee83134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        '''The query string to use for this query definition.

        For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-querystring
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ffa30cbf015263d1d84ce4d4b1eea1565cd50715028a6f199d0b4279077c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupNames")
    def log_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Use this parameter if you want the query to query only certain log groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-loggroupnames
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logGroupNames"))

    @log_group_names.setter
    def log_group_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c9c4e12ade3bf456674ee4e7ec16eb9f60d8b1c0dbb1668f4394126ebdd6ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupNames", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnQueryDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "query_string": "queryString",
        "log_group_names": "logGroupNames",
    },
)
class CfnQueryDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        query_string: builtins.str,
        log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnQueryDefinition``.

        :param name: A name for the query definition.
        :param query_string: The query string to use for this query definition. For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .
        :param log_group_names: Use this parameter if you want the query to query only certain log groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            cfn_query_definition_props = logs.CfnQueryDefinitionProps(
                name="name",
                query_string="queryString",
            
                # the properties below are optional
                log_group_names=["logGroupNames"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adbe31585afcf4e6add21afa574e718a8fe45d4fc92fc641aa7391829f9879cd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument log_group_names", value=log_group_names, expected_type=type_hints["log_group_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "query_string": query_string,
        }
        if log_group_names is not None:
            self._values["log_group_names"] = log_group_names

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the query definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_string(self) -> builtins.str:
        '''The query string to use for this query definition.

        For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-querystring
        '''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Use this parameter if you want the query to query only certain log groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-loggroupnames
        '''
        result = self._values.get("log_group_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueryDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourcePolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnResourcePolicy",
):
    '''A CloudFormation ``AWS::Logs::ResourcePolicy``.

    Creates or updates a resource policy that allows other AWS services to put log events to this account. An account can have up to 10 resource policies per AWS Region.

    :cloudformationResource: AWS::Logs::ResourcePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_logs as logs
        
        cfn_resource_policy = logs.CfnResourcePolicy(self, "MyCfnResourcePolicy",
            policy_document="policyDocument",
            policy_name="policyName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy_document: builtins.str,
        policy_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Logs::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: The details of the policy. It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.
        :param policy_name: The name of the resource policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f34ec1b38e2709581b8dd8629bc9e66c57b4105d678fbb77a72198d51c19421)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourcePolicyProps(
            policy_document=policy_document, policy_name=policy_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a6b303b44a78cddb325fa6be90918ecb31674a23ac52fbb90b30b828a20794)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31ef83d419ffb657634634acc2e80d781d60b1471d6aa7a9573e0fea05dddff8)
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
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> builtins.str:
        '''The details of the policy.

        It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policydocument
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879667565155e3b7005f419cf3b33788b923c5b4ca884176a95d6cdb22a09cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of the resource policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff27ba0351e552e63eefce3310604dea6ed840a8d83a849663061d640461444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "policy_name": "policyName"},
)
class CfnResourcePolicyProps:
    def __init__(
        self,
        *,
        policy_document: builtins.str,
        policy_name: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnResourcePolicy``.

        :param policy_document: The details of the policy. It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.
        :param policy_name: The name of the resource policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            cfn_resource_policy_props = logs.CfnResourcePolicyProps(
                policy_document="policyDocument",
                policy_name="policyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32110d43d0c3e43bbb6a64417ae2c9a409afda8518cdc42c5f4770a101af18d)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
            "policy_name": policy_name,
        }

    @builtins.property
    def policy_document(self) -> builtins.str:
        '''The details of the policy.

        It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''The name of the resource policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSubscriptionFilter(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnSubscriptionFilter",
):
    '''A CloudFormation ``AWS::Logs::SubscriptionFilter``.

    The ``AWS::Logs::SubscriptionFilter`` resource specifies a subscription filter and associates it with the specified log group. Subscription filters allow you to subscribe to a real-time stream of log events and have them delivered to a specific destination. Currently, the supported destinations are:

    - An Amazon Kinesis data stream belonging to the same account as the subscription filter, for same-account delivery.
    - A logical destination that belongs to a different account, for cross-account delivery.
    - An Amazon Kinesis Firehose delivery stream that belongs to the same account as the subscription filter, for same-account delivery.
    - An AWS Lambda function that belongs to the same account as the subscription filter, for same-account delivery.

    There can be as many as two subscription filters associated with a log group.

    :cloudformationResource: AWS::Logs::SubscriptionFilter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_logs as logs
        
        cfn_subscription_filter = logs.CfnSubscriptionFilter(self, "MyCfnSubscriptionFilter",
            destination_arn="destinationArn",
            filter_pattern="filterPattern",
            log_group_name="logGroupName",
        
            # the properties below are optional
            distribution="distribution",
            filter_name="filterName",
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        destination_arn: builtins.str,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        distribution: typing.Optional[builtins.str] = None,
        filter_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::SubscriptionFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: The Amazon Resource Name (ARN) of the destination.
        :param filter_pattern: The filtering expressions that restrict what gets delivered to the destination AWS resource. For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The log group to associate with the subscription filter. All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.
        :param distribution: The method used to distribute log data to the destination, which can be either random or grouped by log stream.
        :param filter_name: The name of the subscription filter.
        :param role_arn: The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream. You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee9a645833f43d0a04fee9c772313ec1ab680df2484655439f98f53353db57d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubscriptionFilterProps(
            destination_arn=destination_arn,
            filter_pattern=filter_pattern,
            log_group_name=log_group_name,
            distribution=distribution,
            filter_name=filter_name,
            role_arn=role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ea202432fdd0a962dd7c8e24767d96e9f1af10446cd0ccba0010c8d451eed6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0e5a1163432d9cbb665c40a602c46a2f2ad5cb31a694672c513b29761655541)
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
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-destinationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e78ec1fdd9df6b46c36352cd7678970fe992477c577f2e65b4c1a12fcb0e11f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> builtins.str:
        '''The filtering expressions that restrict what gets delivered to the destination AWS resource.

        For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filterpattern
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterPattern"))

    @filter_pattern.setter
    def filter_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c021269504f0d229b7d2ed5f7657b66c79c9fe5e838bda7528536c068d717da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPattern", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The log group to associate with the subscription filter.

        All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b2983ed823c8490457ca526fb49482cd42cbd139079267276051e99e400bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> typing.Optional[builtins.str]:
        '''The method used to distribute log data to the destination, which can be either random or grouped by log stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-distribution
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878242b2dbbaed6c351db7a26ac60ea43528b9096f3b8c8da9eaaaf7d50bedc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value)

    @builtins.property
    @jsii.member(jsii_name="filterName")
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subscription filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filtername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterName"))

    @filter_name.setter
    def filter_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69b798efa1019758b576d1d23b64a19f8cbd180e78e77121051e1587bb94be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream.

        You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a3ba882b4a507547915968b1b8c62b34402bdc684a3232d5f1e19d68afee94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnSubscriptionFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_arn": "destinationArn",
        "filter_pattern": "filterPattern",
        "log_group_name": "logGroupName",
        "distribution": "distribution",
        "filter_name": "filterName",
        "role_arn": "roleArn",
    },
)
class CfnSubscriptionFilterProps:
    def __init__(
        self,
        *,
        destination_arn: builtins.str,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        distribution: typing.Optional[builtins.str] = None,
        filter_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSubscriptionFilter``.

        :param destination_arn: The Amazon Resource Name (ARN) of the destination.
        :param filter_pattern: The filtering expressions that restrict what gets delivered to the destination AWS resource. For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The log group to associate with the subscription filter. All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.
        :param distribution: The method used to distribute log data to the destination, which can be either random or grouped by log stream.
        :param filter_name: The name of the subscription filter.
        :param role_arn: The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream. You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            cfn_subscription_filter_props = logs.CfnSubscriptionFilterProps(
                destination_arn="destinationArn",
                filter_pattern="filterPattern",
                log_group_name="logGroupName",
            
                # the properties below are optional
                distribution="distribution",
                filter_name="filterName",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6730b3f8bc4f84870cd8d9e39da45dbb681b1e5b357ac49bb44479fd4d645f2c)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument filter_name", value=filter_name, expected_type=type_hints["filter_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_arn": destination_arn,
            "filter_pattern": filter_pattern,
            "log_group_name": log_group_name,
        }
        if distribution is not None:
            self._values["distribution"] = distribution
        if filter_name is not None:
            self._values["filter_name"] = filter_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-destinationarn
        '''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_pattern(self) -> builtins.str:
        '''The filtering expressions that restrict what gets delivered to the destination AWS resource.

        For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filterpattern
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''The log group to associate with the subscription filter.

        All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def distribution(self) -> typing.Optional[builtins.str]:
        '''The method used to distribute log data to the destination, which can be either random or grouped by log stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-distribution
        '''
        result = self._values.get("distribution")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subscription filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filtername
        '''
        result = self._values.get("filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream.

        You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.ColumnRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "comparison": "comparison",
        "number_value": "numberValue",
        "string_value": "stringValue",
    },
)
class ColumnRestriction:
    def __init__(
        self,
        *,
        comparison: builtins.str,
        number_value: typing.Optional[jsii.Number] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparison: (experimental) Comparison operator to use.
        :param number_value: (experimental) Number value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.
        :param string_value: (experimental) String value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            column_restriction = logs.ColumnRestriction(
                comparison="comparison",
            
                # the properties below are optional
                number_value=123,
                string_value="stringValue"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9947df8ee021d7894d2097aa0c5f857bd8530cfcf8e88a639914f9df12fded27)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument number_value", value=number_value, expected_type=type_hints["number_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
        }
        if number_value is not None:
            self._values["number_value"] = number_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def comparison(self) -> builtins.str:
        '''(experimental) Comparison operator to use.

        :stability: experimental
        '''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def number_value(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.

        :stability: experimental
        '''
        result = self._values.get("number_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''(experimental) String value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.

        :stability: experimental
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColumnRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CrossAccountDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "role": "role",
        "target_arn": "targetArn",
        "destination_name": "destinationName",
    },
)
class CrossAccountDestinationProps:
    def __init__(
        self,
        *,
        role: _IRole_59af6f50,
        target_arn: builtins.str,
        destination_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a CrossAccountDestination.

        :param role: (experimental) The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: (experimental) The log destination target's ARN.
        :param destination_name: (experimental) The name of the log destination. Default: Automatically generated

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_logs as logs
            
            # role: iam.Role
            
            cross_account_destination_props = logs.CrossAccountDestinationProps(
                role=role,
                target_arn="targetArn",
            
                # the properties below are optional
                destination_name="destinationName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae339298fb3e6b4389a9d339a8b0d02f109ec0ab09fcf369851d9502eddd3d0d)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument destination_name", value=destination_name, expected_type=type_hints["destination_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
            "target_arn": target_arn,
        }
        if destination_name is not None:
            self._values["destination_name"] = destination_name

    @builtins.property
    def role(self) -> _IRole_59af6f50:
        '''(experimental) The role to assume that grants permissions to write to 'target'.

        The role must be assumable by 'logs.{REGION}.amazonaws.com'.

        :stability: experimental
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_IRole_59af6f50, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''(experimental) The log destination target's ARN.

        :stability: experimental
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the log destination.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("destination_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossAccountDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilterPattern(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.FilterPattern",
):
    '''(experimental) A collection of static methods to generate appropriate ILogPatterns.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Search for lines that contain both "ERROR" and "MainThread"
        pattern1 = logs.FilterPattern.all_terms("ERROR", "MainThread")
        
        # Search for lines that either contain both "ERROR" and "MainThread", or
        # both "WARN" and "Deadlock".
        pattern2 = logs.FilterPattern.any_term_group(["ERROR", "MainThread"], ["WARN", "Deadlock"])
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls, *patterns: "JsonPattern") -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if all given JSON log patterns match.

        :param patterns: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65a662074f54f22f5f274cd5f9007523337d0e3b921a2553727d82cf32f4a30)
            check_type(argname="argument patterns", value=patterns, expected_type=typing.Tuple[type_hints["patterns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "all", [*patterns]))

    @jsii.member(jsii_name="allEvents")
    @builtins.classmethod
    def all_events(cls) -> "IFilterPattern":
        '''(experimental) A log pattern that matches all events.

        :stability: experimental
        '''
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "allEvents", []))

    @jsii.member(jsii_name="allTerms")
    @builtins.classmethod
    def all_terms(cls, *terms: builtins.str) -> "IFilterPattern":
        '''(experimental) A log pattern that matches if all the strings given appear in the event.

        :param terms: The words to search for. All terms must match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1deebfacc8519ccab47e84866d6c4724d1cef35038b3a1308e81d912d2b1d7)
            check_type(argname="argument terms", value=terms, expected_type=typing.Tuple[type_hints["terms"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "allTerms", [*terms]))

    @jsii.member(jsii_name="any")
    @builtins.classmethod
    def any(cls, *patterns: "JsonPattern") -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if any of the given JSON log patterns match.

        :param patterns: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96e486d1116041c9c048a9d0714d86dba302db0873405292c18e05ea16268b4)
            check_type(argname="argument patterns", value=patterns, expected_type=typing.Tuple[type_hints["patterns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "any", [*patterns]))

    @jsii.member(jsii_name="anyTerm")
    @builtins.classmethod
    def any_term(cls, *terms: builtins.str) -> "IFilterPattern":
        '''(experimental) A log pattern that matches if any of the strings given appear in the event.

        :param terms: The words to search for. Any terms must match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5da0d4912abd0a331e810bb4e8df383569d67fe2fa4f8055d0f700e44db8fd)
            check_type(argname="argument terms", value=terms, expected_type=typing.Tuple[type_hints["terms"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "anyTerm", [*terms]))

    @jsii.member(jsii_name="anyTermGroup")
    @builtins.classmethod
    def any_term_group(
        cls,
        *term_groups: typing.List[builtins.str],
    ) -> "IFilterPattern":
        '''(experimental) A log pattern that matches if any of the given term groups matches the event.

        A term group matches an event if all the terms in it appear in the event string.

        :param term_groups: A list of term groups to search for. Any one of the clauses must match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22190981306e6053ccb8c2c91c021b0c52d32caae5793359720e74306444b0e)
            check_type(argname="argument term_groups", value=term_groups, expected_type=typing.Tuple[type_hints["term_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "anyTermGroup", [*term_groups]))

    @jsii.member(jsii_name="booleanValue")
    @builtins.classmethod
    def boolean_value(
        cls,
        json_field: builtins.str,
        value: builtins.bool,
    ) -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if the field exists and equals the boolean value.

        :param json_field: Field inside JSON. Example: "$.myField"
        :param value: The value to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02208a8bab988c48d31c935d15f26e2ea3b74e3feccfb0fb0534b622574de52c)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "booleanValue", [json_field, value]))

    @jsii.member(jsii_name="exists")
    @builtins.classmethod
    def exists(cls, json_field: builtins.str) -> "JsonPattern":
        '''(experimental) A JSON log patter that matches if the field exists.

        This is a readable convenience wrapper over 'field = *'

        :param json_field: Field inside JSON. Example: "$.myField"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a578913674f850accd056344b0b65bb61bff6f217d24d3f8b56060e9f6b0eb3)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "exists", [json_field]))

    @jsii.member(jsii_name="isNull")
    @builtins.classmethod
    def is_null(cls, json_field: builtins.str) -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if the field exists and has the special value 'null'.

        :param json_field: Field inside JSON. Example: "$.myField"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5be2a35598b612ff4d99c189a546f04f4fba79cbe082e1960d8b396020b6b5)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "isNull", [json_field]))

    @jsii.member(jsii_name="literal")
    @builtins.classmethod
    def literal(cls, log_pattern_string: builtins.str) -> "IFilterPattern":
        '''(experimental) Use the given string as log pattern.

        See https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html
        for information on writing log patterns.

        :param log_pattern_string: The pattern string to use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8751dc825b705474dcb23ede94a83786aea6a0c153e66d6f80ba733941f1cd)
            check_type(argname="argument log_pattern_string", value=log_pattern_string, expected_type=type_hints["log_pattern_string"])
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "literal", [log_pattern_string]))

    @jsii.member(jsii_name="notExists")
    @builtins.classmethod
    def not_exists(cls, json_field: builtins.str) -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if the field does not exist.

        :param json_field: Field inside JSON. Example: "$.myField"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca18acfe1048b18e94b7daaebd7cc29c27421261db705d0aa7340b775d22975)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "notExists", [json_field]))

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(
        cls,
        json_field: builtins.str,
        comparison: builtins.str,
        value: jsii.Number,
    ) -> "JsonPattern":
        '''(experimental) A JSON log pattern that compares numerical values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the value in the indicated way.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. One of =, !=, <, <=, >, >=.
        :param value: The numerical value to compare to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da19a504bf12f110ed72281c189d1570317ad303e767cb4527b3fe1d3eb2529c)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "numberValue", [json_field, comparison, value]))

    @jsii.member(jsii_name="spaceDelimited")
    @builtins.classmethod
    def space_delimited(cls, *columns: builtins.str) -> "SpaceDelimitedTextPattern":
        '''(experimental) A space delimited log pattern matcher.

        The log event is divided into space-delimited columns (optionally
        enclosed by "" or [] to capture spaces into column values), and names
        are given to each column.

        '...' may be specified once to match any number of columns.

        Afterwards, conditions may be added to individual columns.

        :param columns: The columns in the space-delimited log stream.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d14aa6cbc0206a6c3cb21344a83024e2e3db69254b90aab8e152bbeadb9370)
            check_type(argname="argument columns", value=columns, expected_type=typing.Tuple[type_hints["columns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("SpaceDelimitedTextPattern", jsii.sinvoke(cls, "spaceDelimited", [*columns]))

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(
        cls,
        json_field: builtins.str,
        comparison: builtins.str,
        value: builtins.str,
    ) -> "JsonPattern":
        '''(experimental) A JSON log pattern that compares string values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the string value.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. Either = or !=.
        :param value: The string value to compare to. May use '*' as wildcard at start or end of string.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31dba100a6bd877bfcb39353b09edcec71c09e8bf0a1cc4d0093f7b0d6c1a742)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "stringValue", [json_field, comparison, value]))


@jsii.interface(jsii_type="monocdk.aws_logs.IFilterPattern")
class IFilterPattern(typing_extensions.Protocol):
    '''(experimental) Interface for objects that can render themselves to log patterns.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _IFilterPatternProxy:
    '''(experimental) Interface for objects that can render themselves to log patterns.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_logs.IFilterPattern"

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilterPattern).__jsii_proxy_class__ = lambda : _IFilterPatternProxy


@jsii.interface(jsii_type="monocdk.aws_logs.ILogGroup")
class ILogGroup(_IResourceWithPolicy_b83339b0, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this log group, with ':*' appended.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''(experimental) The name of this log group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''(experimental) Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''(experimental) Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: "ILogSubscriptionDestination",
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''(experimental) Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Give permissions to write to create and write to streams in this log group.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="logGroupPhysicalName")
    def log_group_physical_name(self) -> builtins.str:
        '''(experimental) Public method to get the physical name of this log group.

        :stability: experimental
        '''
        ...


class _ILogGroupProxy(
    jsii.proxy_for(_IResourceWithPolicy_b83339b0), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_logs.ILogGroup"

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this log group, with ':*' appended.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''(experimental) The name of this log group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''(experimental) Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2314a9a733245ba376f6f30e2bf3d2e9d12a0183ee739746b2733fc32b9f4b90)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MetricFilterOptions(
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        return typing.cast("MetricFilter", jsii.invoke(self, "addMetricFilter", [id, props]))

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''(experimental) Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32bc2fd33655163579e46872c4bfbba5d7e069196d20fc46ab9cb829a00f9a9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StreamOptions(log_stream_name=log_stream_name)

        return typing.cast("LogStream", jsii.invoke(self, "addStream", [id, props]))

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: "ILogSubscriptionDestination",
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''(experimental) Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd7768fb08aacf8ff72f4b3e2981029716b38af005520fb3c5d768597c9ae2d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubscriptionFilterOptions(
            destination=destination, filter_pattern=filter_pattern
        )

        return typing.cast("SubscriptionFilter", jsii.invoke(self, "addSubscriptionFilter", [id, props]))

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb35ac5929b205a3252e85a2d53b39d58fae896a5e708d7b4a8a377edcab1248)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05591ed0a8a91a9d10d8cc768229623cd87e654f7bd9a679e675085f842260c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Give permissions to write to create and write to streams in this log group.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547b3fd69c8247416c130defa03ea61831cce3116787ae44a3e619bb2bd8c04f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.member(jsii_name="logGroupPhysicalName")
    def log_group_physical_name(self) -> builtins.str:
        '''(experimental) Public method to get the physical name of this log group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "logGroupPhysicalName", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogGroup).__jsii_proxy_class__ = lambda : _ILogGroupProxy


@jsii.interface(jsii_type="monocdk.aws_logs.ILogStream")
class ILogStream(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''(experimental) The name of this log stream.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ILogStreamProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_logs.ILogStream"

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''(experimental) The name of this log stream.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogStream).__jsii_proxy_class__ = lambda : _ILogStreamProxy


@jsii.interface(jsii_type="monocdk.aws_logs.ILogSubscriptionDestination")
class ILogSubscriptionDestination(typing_extensions.Protocol):
    '''(experimental) Interface for classes that can be the destination of a log Subscription.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        source_log_group: ILogGroup,
    ) -> "LogSubscriptionDestinationConfig":
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -

        :stability: experimental
        '''
        ...


class _ILogSubscriptionDestinationProxy:
    '''(experimental) Interface for classes that can be the destination of a log Subscription.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_logs.ILogSubscriptionDestination"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        source_log_group: ILogGroup,
    ) -> "LogSubscriptionDestinationConfig":
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cd3e878164e854ce5da4f63912eac05504d52191e64374d4570dbfcb6f7376)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument source_log_group", value=source_log_group, expected_type=type_hints["source_log_group"])
        return typing.cast("LogSubscriptionDestinationConfig", jsii.invoke(self, "bind", [scope, source_log_group]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogSubscriptionDestination).__jsii_proxy_class__ = lambda : _ILogSubscriptionDestinationProxy


@jsii.implements(IFilterPattern)
class JsonPattern(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_logs.JsonPattern",
):
    '''(experimental) Base class for patterns that only match JSON log events.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Search for all events where the component field is equal to
        # "HttpServer" and either error is true or the latency is higher
        # than 1000.
        pattern = logs.FilterPattern.all(
            logs.FilterPattern.string_value("$.component", "=", "HttpServer"),
            logs.FilterPattern.any(
                logs.FilterPattern.boolean_value("$.error", True),
                logs.FilterPattern.number_value("$.latency", ">", 1000)))
    '''

    def __init__(self, json_pattern_string: builtins.str) -> None:
        '''
        :param json_pattern_string: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a8c8d4b6c2d91b3287dda04dd66785bab48cf76e5bbac208d748ec43254bb2)
            check_type(argname="argument json_pattern_string", value=json_pattern_string, expected_type=type_hints["json_pattern_string"])
        jsii.create(self.__class__, self, [json_pattern_string])

    @builtins.property
    @jsii.member(jsii_name="jsonPatternString")
    def json_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jsonPatternString"))

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))


class _JsonPatternProxy(JsonPattern):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, JsonPattern).__jsii_proxy_class__ = lambda : _JsonPatternProxy


@jsii.implements(ILogGroup)
class LogGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.LogGroup",
):
    '''(experimental) Define a CloudWatch Log Group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as logs
        
        
        log_group = logs.LogGroup(self, "Log Group")
        log_bucket = s3.Bucket(self, "S3 Bucket")
        
        tasks.EmrContainersStartJobRun(self, "EMR Containers Start Job Run",
            virtual_cluster=tasks.VirtualClusterInput.from_virtual_cluster_id("de92jdei2910fwedz"),
            release_label=tasks.ReleaseLabel.EMR_6_2_0,
            job_driver=logs.aws_stepfunctions_tasks.JobDriver(
                spark_submit_job_driver=logs.aws_stepfunctions_tasks.SparkSubmitJobDriver(
                    entry_point=sfn.TaskInput.from_text("local:///usr/lib/spark/examples/src/main/python/pi.py"),
                    spark_submit_parameters="--conf spark.executor.instances=2 --conf spark.executor.memory=2G --conf spark.executor.cores=2 --conf spark.driver.cores=1"
                )
            ),
            monitoring=logs.aws_stepfunctions_tasks.Monitoring(
                log_group=log_group,
                log_bucket=log_bucket
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        retention: typing.Optional["RetentionDays"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption_key: (experimental) The KMS Key to encrypt the log group with. Default: - log group is encrypted with the default master key
        :param log_group_name: (experimental) Name of the log group. Default: Automatically generated
        :param removal_policy: (experimental) Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: (experimental) How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b35113a0248bb9274d0b60e9cf452f8b6632c2581c664f69284a0220137005)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LogGroupProps(
            encryption_key=encryption_key,
            log_group_name=log_group_name,
            removal_policy=removal_policy,
            retention=retention,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogGroupArn")
    @builtins.classmethod
    def from_log_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        log_group_arn: builtins.str,
    ) -> ILogGroup:
        '''(experimental) Import an existing LogGroup given its ARN.

        :param scope: -
        :param id: -
        :param log_group_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d918df03ba3e0c25f25263c78d775444b5d8bb951e57aff911af8151f4f761db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
        return typing.cast(ILogGroup, jsii.sinvoke(cls, "fromLogGroupArn", [scope, id, log_group_arn]))

    @jsii.member(jsii_name="fromLogGroupName")
    @builtins.classmethod
    def from_log_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        log_group_name: builtins.str,
    ) -> ILogGroup:
        '''(experimental) Import an existing LogGroup given its name.

        :param scope: -
        :param id: -
        :param log_group_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fa1e81e918057d45c664d0ffc38eb7f23dd483a6f6ac9c8f880193cd4e6c93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
        return typing.cast(ILogGroup, jsii.sinvoke(cls, "fromLogGroupName", [scope, id, log_group_name]))

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''(experimental) Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7b287458a4e5b044d52e7be08be5844416409a970b0e1a86eccc7dfadc3a76)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MetricFilterOptions(
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        return typing.cast("MetricFilter", jsii.invoke(self, "addMetricFilter", [id, props]))

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''(experimental) Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249b81330e6d660c4e132250cebf95714a3bee4df979e7946d14a456551c890a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StreamOptions(log_stream_name=log_stream_name)

        return typing.cast("LogStream", jsii.invoke(self, "addStream", [id, props]))

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''(experimental) Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee956bbfc346c3b832b379ae5be6515710d700a76c5754a1407a634a9e091210)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubscriptionFilterOptions(
            destination=destination, filter_pattern=filter_pattern
        )

        return typing.cast("SubscriptionFilter", jsii.invoke(self, "addSubscriptionFilter", [id, props]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the resource policy associated with this log group.

        A resource policy will be automatically created upon the first call to ``addToResourcePolicy``.

        Any ARN Principals inside of the statement will be converted into AWS Account ID strings
        because CloudWatch Logs Resource Policies do not accept ARN principals.

        :param statement: The policy statement to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f5e2b603889964cefad95d82bc7348cbb5369e8649307a0e3e309c9e67a45c)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34bb5f8009a0cd10355fbf268e0505307fbe779f10513431e2052fdb119d0d6)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7aab6be603941fa788682a966b5f4fe2b2197bf49ba025a62c9dad2637489b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Give permissions to create and write to streams in this log group.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cfe6da84fe450bab8f4badb5bc36894c613015cd130676e9266287966d47a6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.member(jsii_name="logGroupPhysicalName")
    def log_group_physical_name(self) -> builtins.str:
        '''(experimental) Public method to get the physical name of this log group.

        :return: Physical name of log group

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "logGroupPhysicalName", []))

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this log group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''(experimental) The name of this log group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_key": "encryptionKey",
        "log_group_name": "logGroupName",
        "removal_policy": "removalPolicy",
        "retention": "retention",
    },
)
class LogGroupProps:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        retention: typing.Optional["RetentionDays"] = None,
    ) -> None:
        '''(experimental) Properties for a LogGroup.

        :param encryption_key: (experimental) The KMS Key to encrypt the log group with. Default: - log group is encrypted with the default master key
        :param log_group_name: (experimental) Name of the log group. Default: Automatically generated
        :param removal_policy: (experimental) Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: (experimental) How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            kms_key = kms.Key(self, "KmsKey")
            
            # Pass the KMS key in the `encryptionKey` field to associate the key to the log group
            log_group = logs.LogGroup(self, "LogGroup",
                encryption_key=kms_key
            )
            
            # Pass the KMS key in the `encryptionKey` field to associate the key to the S3 bucket
            exec_bucket = s3.Bucket(self, "EcsExecBucket",
                encryption_key=kms_key
            )
            
            cluster = ecs.Cluster(self, "Cluster",
                vpc=vpc,
                execute_command_configuration=autoscaling.aws_ecs.ExecuteCommandConfiguration(
                    kms_key=kms_key,
                    log_configuration=autoscaling.aws_ecs.ExecuteCommandLogConfiguration(
                        cloud_watch_log_group=log_group,
                        cloud_watch_encryption_enabled=True,
                        s3_bucket=exec_bucket,
                        s3_encryption_enabled=True,
                        s3_key_prefix="exec-command-output"
                    ),
                    logging=ecs.ExecuteCommandLogging.OVERRIDE
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3ec525f067623433f5d3608870632a6d87a3b3fdd28f0e0304f0b4eb54bdc6)
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The KMS Key to encrypt the log group with.

        :default: - log group is encrypted with the default master key

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the log group.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Determine the removal policy of this log group.

        Normally you want to retain the log group so you can diagnose issues
        from logs even after a deployment that no longer includes the log group.
        In that case, use the normal date-based retention policy to age out your
        logs.

        :default: RemovalPolicy.Retain

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def retention(self) -> typing.Optional["RetentionDays"]:
        '''(experimental) How long, in days, the log contents will be retained.

        To retain all logs, set this value to RetentionDays.INFINITE.

        :default: RetentionDays.TWO_YEARS

        :stability: experimental
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional["RetentionDays"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogRetention(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.LogRetention",
):
    '''(experimental) Creates a custom resource to control the retention policy of a CloudWatch Logs log group.

    The log group is created if it doesn't already exist. The policy
    is removed when ``retentionDays`` is ``undefined`` or equal to ``Infinity``.
    Log group can be created in the region that is different from stack region by
    specifying ``logGroupRegion``

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_iam as iam
        from monocdk import aws_logs as logs
        
        # duration: monocdk.Duration
        # role: iam.Role
        
        log_retention = logs.LogRetention(self, "MyLogRetention",
            log_group_name="logGroupName",
            retention=logs.RetentionDays.ONE_DAY,
        
            # the properties below are optional
            log_group_region="logGroupRegion",
            log_retention_retry_options=logs.LogRetentionRetryOptions(
                base=duration,
                max_retries=123
            ),
            role=role
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group_name: builtins.str,
        retention: "RetentionDays",
        log_group_region: typing.Optional[builtins.str] = None,
        log_retention_retry_options: typing.Optional[typing.Union["LogRetentionRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group_name: (experimental) The log group name.
        :param retention: (experimental) The number of days log events are kept in CloudWatch Logs.
        :param log_group_region: (experimental) The region where the log group should be created. Default: - same region as the stack
        :param log_retention_retry_options: (experimental) Retry options for all AWS API calls. Default: - AWS SDK default retry options
        :param role: (experimental) The IAM role for the Lambda function associated with the custom resource. Default: - A new role is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2056666925a7ae370ce23c0c80fecaef238e9541f689173a5b2914beff9c3742)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LogRetentionProps(
            log_group_name=log_group_name,
            retention=retention,
            log_group_region=log_group_region,
            log_retention_retry_options=log_retention_retry_options,
            role=role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the LogGroup.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogRetentionProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "retention": "retention",
        "log_group_region": "logGroupRegion",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "role": "role",
    },
)
class LogRetentionProps:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        retention: "RetentionDays",
        log_group_region: typing.Optional[builtins.str] = None,
        log_retention_retry_options: typing.Optional[typing.Union["LogRetentionRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Construction properties for a LogRetention.

        :param log_group_name: (experimental) The log group name.
        :param retention: (experimental) The number of days log events are kept in CloudWatch Logs.
        :param log_group_region: (experimental) The region where the log group should be created. Default: - same region as the stack
        :param log_retention_retry_options: (experimental) Retry options for all AWS API calls. Default: - AWS SDK default retry options
        :param role: (experimental) The IAM role for the Lambda function associated with the custom resource. Default: - A new role is created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_iam as iam
            from monocdk import aws_logs as logs
            
            # duration: monocdk.Duration
            # role: iam.Role
            
            log_retention_props = logs.LogRetentionProps(
                log_group_name="logGroupName",
                retention=logs.RetentionDays.ONE_DAY,
            
                # the properties below are optional
                log_group_region="logGroupRegion",
                log_retention_retry_options=logs.LogRetentionRetryOptions(
                    base=duration,
                    max_retries=123
                ),
                role=role
            )
        '''
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = LogRetentionRetryOptions(**log_retention_retry_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ad180609ca86d06e8e1cab1c60b1817923869c2691b02bbd1f4385b52725e5)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
            check_type(argname="argument log_group_region", value=log_group_region, expected_type=type_hints["log_group_region"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
            "retention": retention,
        }
        if log_group_region is not None:
            self._values["log_group_region"] = log_group_region
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''(experimental) The log group name.

        :stability: experimental
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention(self) -> "RetentionDays":
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        :stability: experimental
        '''
        result = self._values.get("retention")
        assert result is not None, "Required property 'retention' is missing"
        return typing.cast("RetentionDays", result)

    @builtins.property
    def log_group_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the log group should be created.

        :default: - same region as the stack

        :stability: experimental
        '''
        result = self._values.get("log_group_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional["LogRetentionRetryOptions"]:
        '''(experimental) Retry options for all AWS API calls.

        :default: - AWS SDK default retry options

        :stability: experimental
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional["LogRetentionRetryOptions"], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role for the Lambda function associated with the custom resource.

        :default: - A new role is created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogRetentionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogRetentionRetryOptions",
    jsii_struct_bases=[],
    name_mapping={"base": "base", "max_retries": "maxRetries"},
)
class LogRetentionRetryOptions:
    def __init__(
        self,
        *,
        base: typing.Optional[_Duration_070aa057] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Retry options for all AWS API calls.

        :param base: (experimental) The base duration to use in the exponential backoff for operation retries. Default: Duration.millis(100) (AWS SDK default)
        :param max_retries: (experimental) The maximum amount of retries. Default: 3 (AWS SDK default)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_logs as logs
            
            # duration: monocdk.Duration
            
            log_retention_retry_options = logs.LogRetentionRetryOptions(
                base=duration,
                max_retries=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78fee926002f7f3516e399cbdc05386761049865e684a426009126f7a4ccbbd)
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base is not None:
            self._values["base"] = base
        if max_retries is not None:
            self._values["max_retries"] = max_retries

    @builtins.property
    def base(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The base duration to use in the exponential backoff for operation retries.

        :default: Duration.millis(100) (AWS SDK default)

        :stability: experimental
        '''
        result = self._values.get("base")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum amount of retries.

        :default: 3 (AWS SDK default)

        :stability: experimental
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogRetentionRetryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILogStream)
class LogStream(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.LogStream",
):
    '''(experimental) Define a Log Stream in a Log Group.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_logs as logs
        
        # log_group: logs.LogGroup
        
        log_stream = logs.LogStream(self, "MyLogStream",
            log_group=log_group,
        
            # the properties below are optional
            log_stream_name="logStreamName",
            removal_policy=monocdk.RemovalPolicy.DESTROY
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        log_stream_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: (experimental) The log group to create a log stream for.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: (experimental) Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eeac18022a002ccfdefb3b01a3fd8cf3109803b5a7b056b9e49443d637b09bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LogStreamProps(
            log_group=log_group,
            log_stream_name=log_stream_name,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogStreamName")
    @builtins.classmethod
    def from_log_stream_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        log_stream_name: builtins.str,
    ) -> ILogStream:
        '''(experimental) Import an existing LogGroup.

        :param scope: -
        :param id: -
        :param log_stream_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacf0e838d63538a2799e0c1d1e2ced394a4abe43f838b92f30c761a8dd62f74)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        return typing.cast(ILogStream, jsii.sinvoke(cls, "fromLogStreamName", [scope, id, log_stream_name]))

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''(experimental) The name of this log stream.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group": "logGroup",
        "log_stream_name": "logStreamName",
        "removal_policy": "removalPolicy",
    },
)
class LogStreamProps:
    def __init__(
        self,
        *,
        log_group: ILogGroup,
        log_stream_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''(experimental) Properties for a LogStream.

        :param log_group: (experimental) The log group to create a log stream for.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: (experimental) Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_logs as logs
            
            # log_group: logs.LogGroup
            
            log_stream_props = logs.LogStreamProps(
                log_group=log_group,
            
                # the properties below are optional
                log_stream_name="logStreamName",
                removal_policy=monocdk.RemovalPolicy.DESTROY
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5709347cc47fadaad33a7f4239f7e8b5fe4d18082057801758242a615aa7ec28)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group": log_group,
        }
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''(experimental) The log group to create a log stream for.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the log stream to create.

        The name must be unique within the log group.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Determine what happens when the log stream resource is removed from the app.

        Normally you want to retain the log stream so you can diagnose issues from
        logs even after a deployment that no longer includes the log stream.

        The date-based retention policy of your log group will age out the logs
        after a certain time.

        :default: RemovalPolicy.Retain

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogSubscriptionDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "role": "role"},
)
class LogSubscriptionDestinationConfig:
    def __init__(
        self,
        *,
        arn: builtins.str,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Properties returned by a Subscription destination.

        :param arn: (experimental) The ARN of the subscription's destination.
        :param role: (experimental) The role to assume to write log events to the destination. Default: No role assumed

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_logs as logs
            
            # role: iam.Role
            
            log_subscription_destination_config = logs.LogSubscriptionDestinationConfig(
                arn="arn",
            
                # the properties below are optional
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e708f819c4286cfb8b2ca3a208b616f946ba803f0c484c7d3876a418791d13)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
        }
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the subscription's destination.

        :stability: experimental
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The role to assume to write log events to the destination.

        :default: No role assumed

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogSubscriptionDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetricFilter(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.MetricFilter",
):
    '''(experimental) A filter that extracts information from CloudWatch Logs and emits to CloudWatch Metrics.

    :stability: experimental
    :exampleMetadata: lit=lib/aws-logs/test/integ.metricfilter.lit.ts infused

    Example::

        MetricFilter(self, "MetricFilter",
            log_group=log_group,
            metric_namespace="MyApp",
            metric_name="Latency",
            filter_pattern=FilterPattern.exists("$.latency"),
            metric_value="$.latency"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: (experimental) The log group to create the filter on.
        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da25335796fefba8050510fd40210d3972d40537f7988fa138a104d4414a465)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MetricFilterProps(
            log_group=log_group,
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="metric")
    def metric(
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
        '''(experimental) Return the given named metric for this Metric Filter.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: avg over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [props]))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.MetricFilterOptions",
    jsii_struct_bases=[],
    name_mapping={
        "filter_pattern": "filterPattern",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "default_value": "defaultValue",
        "metric_value": "metricValue",
    },
)
class MetricFilterOptions:
    def __init__(
        self,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a MetricFilter created from a LogGroup.

        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            # filter_pattern: logs.IFilterPattern
            
            metric_filter_options = logs.MetricFilterOptions(
                filter_pattern=filter_pattern,
                metric_name="metricName",
                metric_namespace="metricNamespace",
            
                # the properties below are optional
                default_value=123,
                metric_value="metricValue"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59bcddc6a371b0b385413a2dece9edc02cfd586071249abedecd0e8bc66e584)
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if metric_value is not None:
            self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''(experimental) Pattern to search for log events.

        :stability: experimental
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(experimental) The name of the metric to emit.

        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''(experimental) The namespace of the metric to emit.

        :stability: experimental
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The value to emit if the pattern does not match a particular event.

        :default: No metric emitted.

        :stability: experimental
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_value(self) -> typing.Optional[builtins.str]:
        '''(experimental) The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        :default: "1"

        :stability: experimental
        '''
        result = self._values.get("metric_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.MetricFilterProps",
    jsii_struct_bases=[MetricFilterOptions],
    name_mapping={
        "filter_pattern": "filterPattern",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "default_value": "defaultValue",
        "metric_value": "metricValue",
        "log_group": "logGroup",
    },
)
class MetricFilterProps(MetricFilterOptions):
    def __init__(
        self,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
        log_group: ILogGroup,
    ) -> None:
        '''(experimental) Properties for a MetricFilter.

        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        :param log_group: (experimental) The log group to create the filter on.

        :stability: experimental
        :exampleMetadata: lit=lib/aws-logs/test/integ.metricfilter.lit.ts infused

        Example::

            MetricFilter(self, "MetricFilter",
                log_group=log_group,
                metric_namespace="MyApp",
                metric_name="Latency",
                filter_pattern=FilterPattern.exists("$.latency"),
                metric_value="$.latency"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4270b7d9bbdb52d731c4469a914b0fa3e3940a4b19adb66a9bd25d719519917b)
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "log_group": log_group,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if metric_value is not None:
            self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''(experimental) Pattern to search for log events.

        :stability: experimental
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(experimental) The name of the metric to emit.

        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''(experimental) The namespace of the metric to emit.

        :stability: experimental
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The value to emit if the pattern does not match a particular event.

        :default: No metric emitted.

        :stability: experimental
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_value(self) -> typing.Optional[builtins.str]:
        '''(experimental) The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        :default: "1"

        :stability: experimental
        '''
        result = self._values.get("metric_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''(experimental) The log group to create the filter on.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QueryDefinition(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.QueryDefinition",
):
    '''(experimental) Define a query definition for CloudWatch Logs Insights.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        logs.QueryDefinition(self, "QueryDefinition",
            query_definition_name="MyQuery",
            query_string=logs.QueryString(
                fields=["@timestamp", "@message"],
                sort="@timestamp desc",
                limit=20
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        query_definition_name: builtins.str,
        query_string: "QueryString",
        log_groups: typing.Optional[typing.Sequence[ILogGroup]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param query_definition_name: (experimental) Name of the query definition.
        :param query_string: (experimental) The query string to use for this query definition.
        :param log_groups: (experimental) Specify certain log groups for the query definition. Default: - no specified log groups

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3494b258801c6f0f90f53c9f3e82248946b6a09eaa8d5b6c9921cba9d4ee2d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = QueryDefinitionProps(
            query_definition_name=query_definition_name,
            query_string=query_string,
            log_groups=log_groups,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="queryDefinitionId")
    def query_definition_id(self) -> builtins.str:
        '''(experimental) The ID of the query definition.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryDefinitionId"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.QueryDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "query_definition_name": "queryDefinitionName",
        "query_string": "queryString",
        "log_groups": "logGroups",
    },
)
class QueryDefinitionProps:
    def __init__(
        self,
        *,
        query_definition_name: builtins.str,
        query_string: "QueryString",
        log_groups: typing.Optional[typing.Sequence[ILogGroup]] = None,
    ) -> None:
        '''(experimental) Properties for a QueryDefinition.

        :param query_definition_name: (experimental) Name of the query definition.
        :param query_string: (experimental) The query string to use for this query definition.
        :param log_groups: (experimental) Specify certain log groups for the query definition. Default: - no specified log groups

        :stability: experimental
        :exampleMetadata: infused

        Example::

            logs.QueryDefinition(self, "QueryDefinition",
                query_definition_name="MyQuery",
                query_string=logs.QueryString(
                    fields=["@timestamp", "@message"],
                    sort="@timestamp desc",
                    limit=20
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a413f3493dd443f75478c8ab40b530523017fb90d0d9a36aa24e7b7d3ca51306)
            check_type(argname="argument query_definition_name", value=query_definition_name, expected_type=type_hints["query_definition_name"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument log_groups", value=log_groups, expected_type=type_hints["log_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query_definition_name": query_definition_name,
            "query_string": query_string,
        }
        if log_groups is not None:
            self._values["log_groups"] = log_groups

    @builtins.property
    def query_definition_name(self) -> builtins.str:
        '''(experimental) Name of the query definition.

        :stability: experimental
        '''
        result = self._values.get("query_definition_name")
        assert result is not None, "Required property 'query_definition_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_string(self) -> "QueryString":
        '''(experimental) The query string to use for this query definition.

        :stability: experimental
        '''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast("QueryString", result)

    @builtins.property
    def log_groups(self) -> typing.Optional[typing.List[ILogGroup]]:
        '''(experimental) Specify certain log groups for the query definition.

        :default: - no specified log groups

        :stability: experimental
        '''
        result = self._values.get("log_groups")
        return typing.cast(typing.Optional[typing.List[ILogGroup]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueryDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QueryString(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_logs.QueryString"):
    '''(experimental) Define a QueryString.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        logs.QueryDefinition(self, "QueryDefinition",
            query_definition_name="MyQuery",
            query_string=logs.QueryString(
                fields=["@timestamp", "@message"],
                sort="@timestamp desc",
                limit=20
            )
        )
    '''

    def __init__(
        self,
        *,
        display: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        filter: typing.Optional[builtins.str] = None,
        limit: typing.Optional[jsii.Number] = None,
        parse: typing.Optional[builtins.str] = None,
        sort: typing.Optional[builtins.str] = None,
        stats: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display: (experimental) Specifies which fields to display in the query results. Default: - no display in QueryString
        :param fields: (experimental) Retrieves the specified fields from log events for display. Default: - no fields in QueryString
        :param filter: (experimental) Filters the results of a query that's based on one or more conditions. Default: - no filter in QueryString
        :param limit: (experimental) Specifies the number of log events returned by the query. Default: - no limit in QueryString
        :param parse: (experimental) Extracts data from a log field and creates one or more ephemeral fields that you can process further in the query. Default: - no parse in QueryString
        :param sort: (experimental) Sorts the retrieved log events. Default: - no sort in QueryString
        :param stats: (experimental) Uses log field values to calculate aggregate statistics. Default: - no stats in QueryString

        :stability: experimental
        '''
        props = QueryStringProps(
            display=display,
            fields=fields,
            filter=filter,
            limit=limit,
            parse=parse,
            sort=sort,
            stats=stats,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) String representation of this QueryString.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.QueryStringProps",
    jsii_struct_bases=[],
    name_mapping={
        "display": "display",
        "fields": "fields",
        "filter": "filter",
        "limit": "limit",
        "parse": "parse",
        "sort": "sort",
        "stats": "stats",
    },
)
class QueryStringProps:
    def __init__(
        self,
        *,
        display: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        filter: typing.Optional[builtins.str] = None,
        limit: typing.Optional[jsii.Number] = None,
        parse: typing.Optional[builtins.str] = None,
        sort: typing.Optional[builtins.str] = None,
        stats: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a QueryString.

        :param display: (experimental) Specifies which fields to display in the query results. Default: - no display in QueryString
        :param fields: (experimental) Retrieves the specified fields from log events for display. Default: - no fields in QueryString
        :param filter: (experimental) Filters the results of a query that's based on one or more conditions. Default: - no filter in QueryString
        :param limit: (experimental) Specifies the number of log events returned by the query. Default: - no limit in QueryString
        :param parse: (experimental) Extracts data from a log field and creates one or more ephemeral fields that you can process further in the query. Default: - no parse in QueryString
        :param sort: (experimental) Sorts the retrieved log events. Default: - no sort in QueryString
        :param stats: (experimental) Uses log field values to calculate aggregate statistics. Default: - no stats in QueryString

        :stability: experimental
        :exampleMetadata: infused

        Example::

            logs.QueryDefinition(self, "QueryDefinition",
                query_definition_name="MyQuery",
                query_string=logs.QueryString(
                    fields=["@timestamp", "@message"],
                    sort="@timestamp desc",
                    limit=20
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4aea6f0385fde5f7a674c2872c0d9df6bbbe6b8fe16956792d6343f303c019)
            check_type(argname="argument display", value=display, expected_type=type_hints["display"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument parse", value=parse, expected_type=type_hints["parse"])
            check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
            check_type(argname="argument stats", value=stats, expected_type=type_hints["stats"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if display is not None:
            self._values["display"] = display
        if fields is not None:
            self._values["fields"] = fields
        if filter is not None:
            self._values["filter"] = filter
        if limit is not None:
            self._values["limit"] = limit
        if parse is not None:
            self._values["parse"] = parse
        if sort is not None:
            self._values["sort"] = sort
        if stats is not None:
            self._values["stats"] = stats

    @builtins.property
    def display(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies which fields to display in the query results.

        :default: - no display in QueryString

        :stability: experimental
        '''
        result = self._values.get("display")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Retrieves the specified fields from log events for display.

        :default: - no fields in QueryString

        :stability: experimental
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filters the results of a query that's based on one or more conditions.

        :default: - no filter in QueryString

        :stability: experimental
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Specifies the number of log events returned by the query.

        :default: - no limit in QueryString

        :stability: experimental
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parse(self) -> typing.Optional[builtins.str]:
        '''(experimental) Extracts data from a log field and creates one or more ephemeral fields that you can process further in the query.

        :default: - no parse in QueryString

        :stability: experimental
        '''
        result = self._values.get("parse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sorts the retrieved log events.

        :default: - no sort in QueryString

        :stability: experimental
        '''
        result = self._values.get("sort")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stats(self) -> typing.Optional[builtins.str]:
        '''(experimental) Uses log field values to calculate aggregate statistics.

        :default: - no stats in QueryString

        :stability: experimental
        '''
        result = self._values.get("stats")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueryStringProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourcePolicy(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.ResourcePolicy",
):
    '''(experimental) Resource Policy for CloudWatch Log Groups.

    Policies define the operations that are allowed on this resource.

    You almost never need to define this construct directly.

    All AWS resources that support resource policies have a method called
    ``addToResourcePolicy()``, which will automatically create a new resource
    policy if one doesn't exist yet, otherwise it will add to the existing
    policy.

    Prefer to use ``addToResourcePolicy()`` instead.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        from monocdk import aws_logs as logs
        
        # policy_statement: iam.PolicyStatement
        
        resource_policy = logs.ResourcePolicy(self, "MyResourcePolicy",
            policy_statements=[policy_statement],
            resource_policy_name="resourcePolicyName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        resource_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param policy_statements: (experimental) Initial statements to add to the resource policy. Default: - No statements
        :param resource_policy_name: (experimental) Name of the log group resource policy. Default: - Uses a unique id based on the construct path

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce7ed2bbd7b86bb1435856be4b40ff98aaea72df5bc6cd6cc5b0be5e163a7fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ResourcePolicyProps(
            policy_statements=policy_statements,
            resource_policy_name=resource_policy_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> _PolicyDocument_b5de5177:
        '''(experimental) The IAM policy document for this resource policy.

        :stability: experimental
        '''
        return typing.cast(_PolicyDocument_b5de5177, jsii.get(self, "document"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.ResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_statements": "policyStatements",
        "resource_policy_name": "resourcePolicyName",
    },
)
class ResourcePolicyProps:
    def __init__(
        self,
        *,
        policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        resource_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define Cloudwatch log group resource policy.

        :param policy_statements: (experimental) Initial statements to add to the resource policy. Default: - No statements
        :param resource_policy_name: (experimental) Name of the log group resource policy. Default: - Uses a unique id based on the construct path

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_logs as logs
            
            # policy_statement: iam.PolicyStatement
            
            resource_policy_props = logs.ResourcePolicyProps(
                policy_statements=[policy_statement],
                resource_policy_name="resourcePolicyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034de1d72f2257e2aad72fbdbd1acdfdf6052134ae135d2b1bc80caf899cc47f)
            check_type(argname="argument policy_statements", value=policy_statements, expected_type=type_hints["policy_statements"])
            check_type(argname="argument resource_policy_name", value=resource_policy_name, expected_type=type_hints["resource_policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_statements is not None:
            self._values["policy_statements"] = policy_statements
        if resource_policy_name is not None:
            self._values["resource_policy_name"] = resource_policy_name

    @builtins.property
    def policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Initial statements to add to the resource policy.

        :default: - No statements

        :stability: experimental
        '''
        result = self._values.get("policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def resource_policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the log group resource policy.

        :default: - Uses a unique id based on the construct path

        :stability: experimental
        '''
        result = self._values.get("resource_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_logs.RetentionDays")
class RetentionDays(enum.Enum):
    '''(experimental) How long, in days, the log contents will be retained.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as logs
        # my_logs_publishing_role: iam.Role
        # vpc: ec2.Vpc
        
        
        # Exporting logs from a cluster
        cluster = rds.DatabaseCluster(self, "Database",
            engine=rds.DatabaseClusterEngine.aurora(
                version=rds.AuroraEngineVersion.VER_1_17_9
            ),
            instance_props=logs.aws_rds.InstanceProps(
                vpc=vpc
            ),
            cloudwatch_logs_exports=["error", "general", "slowquery", "audit"],  # Export all available MySQL-based logs
            cloudwatch_logs_retention=logs.RetentionDays.THREE_MONTHS,  # Optional - default is to never expire logs
            cloudwatch_logs_retention_role=my_logs_publishing_role
        )
        
        # Exporting logs from an instance
        instance = rds.DatabaseInstance(self, "Instance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_3
            ),
            vpc=vpc,
            cloudwatch_logs_exports=["postgresql"]
        )
    '''

    ONE_DAY = "ONE_DAY"
    '''(experimental) 1 day.

    :stability: experimental
    '''
    THREE_DAYS = "THREE_DAYS"
    '''(experimental) 3 days.

    :stability: experimental
    '''
    FIVE_DAYS = "FIVE_DAYS"
    '''(experimental) 5 days.

    :stability: experimental
    '''
    ONE_WEEK = "ONE_WEEK"
    '''(experimental) 1 week.

    :stability: experimental
    '''
    TWO_WEEKS = "TWO_WEEKS"
    '''(experimental) 2 weeks.

    :stability: experimental
    '''
    ONE_MONTH = "ONE_MONTH"
    '''(experimental) 1 month.

    :stability: experimental
    '''
    TWO_MONTHS = "TWO_MONTHS"
    '''(experimental) 2 months.

    :stability: experimental
    '''
    THREE_MONTHS = "THREE_MONTHS"
    '''(experimental) 3 months.

    :stability: experimental
    '''
    FOUR_MONTHS = "FOUR_MONTHS"
    '''(experimental) 4 months.

    :stability: experimental
    '''
    FIVE_MONTHS = "FIVE_MONTHS"
    '''(experimental) 5 months.

    :stability: experimental
    '''
    SIX_MONTHS = "SIX_MONTHS"
    '''(experimental) 6 months.

    :stability: experimental
    '''
    ONE_YEAR = "ONE_YEAR"
    '''(experimental) 1 year.

    :stability: experimental
    '''
    THIRTEEN_MONTHS = "THIRTEEN_MONTHS"
    '''(experimental) 13 months.

    :stability: experimental
    '''
    EIGHTEEN_MONTHS = "EIGHTEEN_MONTHS"
    '''(experimental) 18 months.

    :stability: experimental
    '''
    TWO_YEARS = "TWO_YEARS"
    '''(experimental) 2 years.

    :stability: experimental
    '''
    FIVE_YEARS = "FIVE_YEARS"
    '''(experimental) 5 years.

    :stability: experimental
    '''
    SIX_YEARS = "SIX_YEARS"
    '''(experimental) 6 years.

    :stability: experimental
    '''
    SEVEN_YEARS = "SEVEN_YEARS"
    '''(experimental) 7 years.

    :stability: experimental
    '''
    EIGHT_YEARS = "EIGHT_YEARS"
    '''(experimental) 8 years.

    :stability: experimental
    '''
    NINE_YEARS = "NINE_YEARS"
    '''(experimental) 9 years.

    :stability: experimental
    '''
    TEN_YEARS = "TEN_YEARS"
    '''(experimental) 10 years.

    :stability: experimental
    '''
    INFINITE = "INFINITE"
    '''(experimental) Retain logs forever.

    :stability: experimental
    '''


@jsii.implements(IFilterPattern)
class SpaceDelimitedTextPattern(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.SpaceDelimitedTextPattern",
):
    '''(experimental) Space delimited text pattern.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Search for all events where the component is "HttpServer" and the
        # result code is not equal to 200.
        pattern = logs.FilterPattern.space_delimited("time", "component", "...", "result_code", "latency").where_string("component", "=", "HttpServer").where_number("result_code", "!=", 200)
    '''

    def __init__(
        self,
        columns: typing.Sequence[builtins.str],
        restrictions: typing.Mapping[builtins.str, typing.Sequence[typing.Union[ColumnRestriction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param columns: -
        :param restrictions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201dfea95d4608037ea86c671ee9e2e47d53eee2fae8e62c511b7242aae364ee)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
        jsii.create(self.__class__, self, [columns, restrictions])

    @jsii.member(jsii_name="construct")
    @builtins.classmethod
    def construct(
        cls,
        columns: typing.Sequence[builtins.str],
    ) -> "SpaceDelimitedTextPattern":
        '''(experimental) Construct a new instance of a space delimited text pattern.

        Since this class must be public, we can't rely on the user only creating it through
        the ``LogPattern.spaceDelimited()`` factory function. We must therefore validate the
        argument in the constructor. Since we're returning a copy on every mutation, and we
        don't want to re-validate the same things on every construction, we provide a limited
        set of mutator functions and only validate the new data every time.

        :param columns: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29aea15442e5dae204d31348b0d3100f070fe625e4ff02b6be44928f55cf948f)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
        return typing.cast("SpaceDelimitedTextPattern", jsii.sinvoke(cls, "construct", [columns]))

    @jsii.member(jsii_name="whereNumber")
    def where_number(
        self,
        column_name: builtins.str,
        comparison: builtins.str,
        value: jsii.Number,
    ) -> "SpaceDelimitedTextPattern":
        '''(experimental) Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c8e701ae3efdc5a1c8d3494734382a00000795439466dd075cf83909b3e3e2)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("SpaceDelimitedTextPattern", jsii.invoke(self, "whereNumber", [column_name, comparison, value]))

    @jsii.member(jsii_name="whereString")
    def where_string(
        self,
        column_name: builtins.str,
        comparison: builtins.str,
        value: builtins.str,
    ) -> "SpaceDelimitedTextPattern":
        '''(experimental) Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97843ea52d2c5501746f6dc4b46073f50b5c90ec953d87f9aa2ad9ef2898ef62)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("SpaceDelimitedTextPattern", jsii.invoke(self, "whereString", [column_name, comparison, value]))

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.StreamOptions",
    jsii_struct_bases=[],
    name_mapping={"log_stream_name": "logStreamName"},
)
class StreamOptions:
    def __init__(
        self,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a new LogStream created from a LogGroup.

        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            stream_options = logs.StreamOptions(
                log_stream_name="logStreamName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6811f4c15328aa7ae283b0c0a596227eaf88de84fdd4946de7556e1eecc9dd73)
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the log stream to create.

        The name must be unique within the log group.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubscriptionFilter(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.SubscriptionFilter",
):
    '''(experimental) A new Subscription on a CloudWatch log group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as destinations
        # fn: lambda.Function
        # log_group: logs.LogGroup
        
        
        logs.SubscriptionFilter(self, "Subscription",
            log_group=log_group,
            destination=destinations.LambdaDestination(fn),
            filter_pattern=logs.FilterPattern.all_terms("ERROR", "MainThread")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: (experimental) The log group to create the subscription on.
        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0168ffffe070a301bfc4483a950daf4cae7c18eade13de303aeaa986e90109bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubscriptionFilterProps(
            log_group=log_group, destination=destination, filter_pattern=filter_pattern
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_logs.SubscriptionFilterOptions",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "filter_pattern": "filterPattern"},
)
class SubscriptionFilterOptions:
    def __init__(
        self,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> None:
        '''(experimental) Properties for a new SubscriptionFilter created from a LogGroup.

        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_logs as logs
            
            # filter_pattern: logs.IFilterPattern
            # log_subscription_destination: logs.ILogSubscriptionDestination
            
            subscription_filter_options = logs.SubscriptionFilterOptions(
                destination=log_subscription_destination,
                filter_pattern=filter_pattern
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784581c59f7691426dc6def33084aa510201472914fbd2d9004dcd3e3a64dad7)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "filter_pattern": filter_pattern,
        }

    @builtins.property
    def destination(self) -> ILogSubscriptionDestination:
        '''(experimental) The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(ILogSubscriptionDestination, result)

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''(experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.SubscriptionFilterProps",
    jsii_struct_bases=[SubscriptionFilterOptions],
    name_mapping={
        "destination": "destination",
        "filter_pattern": "filterPattern",
        "log_group": "logGroup",
    },
)
class SubscriptionFilterProps(SubscriptionFilterOptions):
    def __init__(
        self,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
        log_group: ILogGroup,
    ) -> None:
        '''(experimental) Properties for a SubscriptionFilter.

        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.
        :param log_group: (experimental) The log group to create the subscription on.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as destinations
            # fn: lambda.Function
            # log_group: logs.LogGroup
            
            
            logs.SubscriptionFilter(self, "Subscription",
                log_group=log_group,
                destination=destinations.LambdaDestination(fn),
                filter_pattern=logs.FilterPattern.all_terms("ERROR", "MainThread")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c873e24975576e2cf985e4057d4821bbcdef1b8c33548cad85a9d9af1c3bbf)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "filter_pattern": filter_pattern,
            "log_group": log_group,
        }

    @builtins.property
    def destination(self) -> ILogSubscriptionDestination:
        '''(experimental) The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(ILogSubscriptionDestination, result)

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''(experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''(experimental) The log group to create the subscription on.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILogSubscriptionDestination)
class CrossAccountDestination(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CrossAccountDestination",
):
    '''(experimental) A new CloudWatch Logs Destination for use in cross-account scenarios.

    CrossAccountDestinations are used to subscribe a Kinesis stream in a
    different account to a CloudWatch Subscription.

    Consumers will hardly ever need to use this class. Instead, directly
    subscribe a Kinesis stream using the integration class in the
    ``@aws-cdk/aws-logs-destinations`` package; if necessary, a
    ``CrossAccountDestination`` will be created automatically.

    :stability: experimental
    :resource: AWS::Logs::Destination
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        from monocdk import aws_logs as logs
        
        # role: iam.Role
        
        cross_account_destination = logs.CrossAccountDestination(self, "MyCrossAccountDestination",
            role=role,
            target_arn="targetArn",
        
            # the properties below are optional
            destination_name="destinationName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        role: _IRole_59af6f50,
        target_arn: builtins.str,
        destination_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param role: (experimental) The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: (experimental) The log destination target's ARN.
        :param destination_name: (experimental) The name of the log destination. Default: Automatically generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864ab89cd5b2c71964dceae91572c99415a804b28da1e887fcbce2ab448fea01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CrossAccountDestinationProps(
            role=role, target_arn=target_arn, destination_name=destination_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: _PolicyStatement_296fe8a3) -> None:
        '''
        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4d8b545461929090a250ab5e7be4a2ff9fbff1b9e297f5c41be7d117797e49)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        _source_log_group: ILogGroup,
    ) -> LogSubscriptionDestinationConfig:
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param _scope: -
        :param _source_log_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0312d2390e235dc277da3e3b8b49ae2c66d53e7c1223bdd7783f3fbad2f2bdc7)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _source_log_group", value=_source_log_group, expected_type=type_hints["_source_log_group"])
        return typing.cast(LogSubscriptionDestinationConfig, jsii.invoke(self, "bind", [_scope, _source_log_group]))

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        '''(experimental) The ARN of this CrossAccountDestination object.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @builtins.property
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> builtins.str:
        '''(experimental) The name of this CrossAccountDestination object.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationName"))

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> _PolicyDocument_b5de5177:
        '''(experimental) Policy object of this CrossAccountDestination object.

        :stability: experimental
        '''
        return typing.cast(_PolicyDocument_b5de5177, jsii.get(self, "policyDocument"))


__all__ = [
    "CfnDestination",
    "CfnDestinationProps",
    "CfnLogGroup",
    "CfnLogGroupProps",
    "CfnLogStream",
    "CfnLogStreamProps",
    "CfnMetricFilter",
    "CfnMetricFilterProps",
    "CfnQueryDefinition",
    "CfnQueryDefinitionProps",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
    "CfnSubscriptionFilter",
    "CfnSubscriptionFilterProps",
    "ColumnRestriction",
    "CrossAccountDestination",
    "CrossAccountDestinationProps",
    "FilterPattern",
    "IFilterPattern",
    "ILogGroup",
    "ILogStream",
    "ILogSubscriptionDestination",
    "JsonPattern",
    "LogGroup",
    "LogGroupProps",
    "LogRetention",
    "LogRetentionProps",
    "LogRetentionRetryOptions",
    "LogStream",
    "LogStreamProps",
    "LogSubscriptionDestinationConfig",
    "MetricFilter",
    "MetricFilterOptions",
    "MetricFilterProps",
    "QueryDefinition",
    "QueryDefinitionProps",
    "QueryString",
    "QueryStringProps",
    "ResourcePolicy",
    "ResourcePolicyProps",
    "RetentionDays",
    "SpaceDelimitedTextPattern",
    "StreamOptions",
    "SubscriptionFilter",
    "SubscriptionFilterOptions",
    "SubscriptionFilterProps",
]

publication.publish()

def _typecheckingstub__6bd366b11808e27e134ad0197dec51f8dfe7485d17307a2dfdd2a29c5da54219(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    destination_name: builtins.str,
    role_arn: builtins.str,
    target_arn: builtins.str,
    destination_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4eb1d4e64853911a9612b45bdc1f28d1343b85025183b4bd894df329899f56(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccee2a62a5f07a27f8c76396414a95d3fef2278e7e62cf4eb8da2a6980f8a0a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32acc85d0429c0fe249d91678db9f28392c12be0b4735928bd8db5b5715bd7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be8d8d60bff686aec5167eeec4b1d33f5a199acf29369cbb8581f68edc7abfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db4fe7ae950d68e999870d97794febac8633356fe2fb04e9d8cf718214bed39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9447363130e595be514f1c565b5fbb02e200cfd137a03c6b1c0592a5ec7360b4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc86692bf80e03d5976c96e595483f7ba735691cced9ab50d2260d7209a476b(
    *,
    destination_name: builtins.str,
    role_arn: builtins.str,
    target_arn: builtins.str,
    destination_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36bc84863cf3c073756e31b583685df56c11046f4104f2f6cbdca1d7578ba83(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    data_protection_policy: typing.Any = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f953123a3452c9b24f8de2ee1c531834b7a64b513052dbe9ade88e5f14c9bf8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96abd0e04d68a03fa0f154bd2755c69d3590cdb2e6bc7202c352eb4a68e48ec(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5290dcda35696cf43b5727908fa2d558fe21447b24ca80c2f4202274a904051a(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdad71d01c1afd05263e1259d8ad95b9f622acb1a63dbeb6374bd2397bde83e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cafe04c904bc5232bdde564693af5841b02728bffb99e1ce501078ae22c71d9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac3993ff0f47a088df1fb3993244523d26bb7831a1d897a228020ad081e02d5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a625215d9327f9864a73debe7c9e0c517923916936e53690238516db9f79da78(
    *,
    data_protection_policy: typing.Any = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60c8c8a73232433901aff1d23c0083d11607db169b3d20774309640c4dbf1d6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    log_group_name: builtins.str,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed8bc226d18d8600f85181d259003888fe69db70006a3fc3a94ca6d510b77eb(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1af18e5d46ba48a5e15d1d7d39d7bfa484712f31e8f7957fc7bd471651f191(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d203cc5c6d04d07178aaf4a1b0619d42be968d68cb9d0bbcf0281928650320e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100b1127258df06af75a75f8484fbd6617f0a43429de3163c2a0baae15d5e8f0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dc3079ece170f6873cfbbadd6f87785ab37fad9a1c4cb895d13cfdd89783ef(
    *,
    log_group_name: builtins.str,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e20b6b1a449989796d745885365a86b5926e6683cc8c7c3df4d2b681fd4107(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
    metric_transformations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricFilter.MetricTransformationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    filter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc5001111212e97d57d09d9c297faf5cb9108218300c23ad5167f3312e20ace(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903d42219c1d8ec2ac4b00b49f411a8c48f8a223c3865d8390137d5944c68960(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1249d76ed1279862a5802042d67bdcb33c9ee1f82ad6dff0f72df6d8ac6c3aea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7c4b13dc093ea849aa48200bd454cc05b1e905649876386c377c401cbedf0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c3c686f0d59b99cb9a9068c5b6900f196068faa8d566af526c6f23ed78b17c(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricFilter.MetricTransformationProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9822c1819ab526b1dcf91859e0f7b45194deea4250b31f4d0f3b543a474201b6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31aba6414afd737e80dd81a17d0fc3908210ff53250534fbc338f86d00d5c1b(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de36e210a18a9ef57b44ae06fa0064253b0670f44ceb4de0bf26e80a9587e4b5(
    *,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    metric_value: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricFilter.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75abbbbaad23c2e2fa6e36cdde1ae09e1ae1fce2b702d94b90bb872b38ad0d6(
    *,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
    metric_transformations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricFilter.MetricTransformationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    filter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12de71f864ff4f28fdb606d12311c3f3ab47c4b59c6b4457f5a5df86d3bd00a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    query_string: builtins.str,
    log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387cfb50c0f81082b33fffefdf678ab79c9f7fe2133de048c09f33d021113560(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58130be6056c2d0862cb96eb421c902ffd2f9bae92f78d9c3e9be9f05b04b5b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d003ded7fc1d367b7418a4517d01fb5dc3b60fd5f7b41f6c93179dbee83134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ffa30cbf015263d1d84ce4d4b1eea1565cd50715028a6f199d0b4279077c86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c9c4e12ade3bf456674ee4e7ec16eb9f60d8b1c0dbb1668f4394126ebdd6ea(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbe31585afcf4e6add21afa574e718a8fe45d4fc92fc641aa7391829f9879cd(
    *,
    name: builtins.str,
    query_string: builtins.str,
    log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f34ec1b38e2709581b8dd8629bc9e66c57b4105d678fbb77a72198d51c19421(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy_document: builtins.str,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a6b303b44a78cddb325fa6be90918ecb31674a23ac52fbb90b30b828a20794(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ef83d419ffb657634634acc2e80d781d60b1471d6aa7a9573e0fea05dddff8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879667565155e3b7005f419cf3b33788b923c5b4ca884176a95d6cdb22a09cf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff27ba0351e552e63eefce3310604dea6ed840a8d83a849663061d640461444(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32110d43d0c3e43bbb6a64417ae2c9a409afda8518cdc42c5f4770a101af18d(
    *,
    policy_document: builtins.str,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee9a645833f43d0a04fee9c772313ec1ab680df2484655439f98f53353db57d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    destination_arn: builtins.str,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
    distribution: typing.Optional[builtins.str] = None,
    filter_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ea202432fdd0a962dd7c8e24767d96e9f1af10446cd0ccba0010c8d451eed6(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e5a1163432d9cbb665c40a602c46a2f2ad5cb31a694672c513b29761655541(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e78ec1fdd9df6b46c36352cd7678970fe992477c577f2e65b4c1a12fcb0e11f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c021269504f0d229b7d2ed5f7657b66c79c9fe5e838bda7528536c068d717da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b2983ed823c8490457ca526fb49482cd42cbd139079267276051e99e400bfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878242b2dbbaed6c351db7a26ac60ea43528b9096f3b8c8da9eaaaf7d50bedc2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69b798efa1019758b576d1d23b64a19f8cbd180e78e77121051e1587bb94be6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a3ba882b4a507547915968b1b8c62b34402bdc684a3232d5f1e19d68afee94(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6730b3f8bc4f84870cd8d9e39da45dbb681b1e5b357ac49bb44479fd4d645f2c(
    *,
    destination_arn: builtins.str,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
    distribution: typing.Optional[builtins.str] = None,
    filter_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9947df8ee021d7894d2097aa0c5f857bd8530cfcf8e88a639914f9df12fded27(
    *,
    comparison: builtins.str,
    number_value: typing.Optional[jsii.Number] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae339298fb3e6b4389a9d339a8b0d02f109ec0ab09fcf369851d9502eddd3d0d(
    *,
    role: _IRole_59af6f50,
    target_arn: builtins.str,
    destination_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65a662074f54f22f5f274cd5f9007523337d0e3b921a2553727d82cf32f4a30(
    *patterns: JsonPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1deebfacc8519ccab47e84866d6c4724d1cef35038b3a1308e81d912d2b1d7(
    *terms: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96e486d1116041c9c048a9d0714d86dba302db0873405292c18e05ea16268b4(
    *patterns: JsonPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5da0d4912abd0a331e810bb4e8df383569d67fe2fa4f8055d0f700e44db8fd(
    *terms: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22190981306e6053ccb8c2c91c021b0c52d32caae5793359720e74306444b0e(
    *term_groups: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02208a8bab988c48d31c935d15f26e2ea3b74e3feccfb0fb0534b622574de52c(
    json_field: builtins.str,
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a578913674f850accd056344b0b65bb61bff6f217d24d3f8b56060e9f6b0eb3(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5be2a35598b612ff4d99c189a546f04f4fba79cbe082e1960d8b396020b6b5(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8751dc825b705474dcb23ede94a83786aea6a0c153e66d6f80ba733941f1cd(
    log_pattern_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca18acfe1048b18e94b7daaebd7cc29c27421261db705d0aa7340b775d22975(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da19a504bf12f110ed72281c189d1570317ad303e767cb4527b3fe1d3eb2529c(
    json_field: builtins.str,
    comparison: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d14aa6cbc0206a6c3cb21344a83024e2e3db69254b90aab8e152bbeadb9370(
    *columns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31dba100a6bd877bfcb39353b09edcec71c09e8bf0a1cc4d0093f7b0d6c1a742(
    json_field: builtins.str,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2314a9a733245ba376f6f30e2bf3d2e9d12a0183ee739746b2733fc32b9f4b90(
    id: builtins.str,
    *,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32bc2fd33655163579e46872c4bfbba5d7e069196d20fc46ab9cb829a00f9a9(
    id: builtins.str,
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd7768fb08aacf8ff72f4b3e2981029716b38af005520fb3c5d768597c9ae2d(
    id: builtins.str,
    *,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb35ac5929b205a3252e85a2d53b39d58fae896a5e708d7b4a8a377edcab1248(
    json_field: builtins.str,
    metric_namespace: builtins.str,
    metric_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05591ed0a8a91a9d10d8cc768229623cd87e654f7bd9a679e675085f842260c(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547b3fd69c8247416c130defa03ea61831cce3116787ae44a3e619bb2bd8c04f(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cd3e878164e854ce5da4f63912eac05504d52191e64374d4570dbfcb6f7376(
    scope: _Construct_e78e779f,
    source_log_group: ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a8c8d4b6c2d91b3287dda04dd66785bab48cf76e5bbac208d748ec43254bb2(
    json_pattern_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b35113a0248bb9274d0b60e9cf452f8b6632c2581c664f69284a0220137005(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    retention: typing.Optional[RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d918df03ba3e0c25f25263c78d775444b5d8bb951e57aff911af8151f4f761db(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    log_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fa1e81e918057d45c664d0ffc38eb7f23dd483a6f6ac9c8f880193cd4e6c93(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7b287458a4e5b044d52e7be08be5844416409a970b0e1a86eccc7dfadc3a76(
    id: builtins.str,
    *,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249b81330e6d660c4e132250cebf95714a3bee4df979e7946d14a456551c890a(
    id: builtins.str,
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee956bbfc346c3b832b379ae5be6515710d700a76c5754a1407a634a9e091210(
    id: builtins.str,
    *,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f5e2b603889964cefad95d82bc7348cbb5369e8649307a0e3e309c9e67a45c(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34bb5f8009a0cd10355fbf268e0505307fbe779f10513431e2052fdb119d0d6(
    json_field: builtins.str,
    metric_namespace: builtins.str,
    metric_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7aab6be603941fa788682a966b5f4fe2b2197bf49ba025a62c9dad2637489b(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cfe6da84fe450bab8f4badb5bc36894c613015cd130676e9266287966d47a6(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3ec525f067623433f5d3608870632a6d87a3b3fdd28f0e0304f0b4eb54bdc6(
    *,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    retention: typing.Optional[RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2056666925a7ae370ce23c0c80fecaef238e9541f689173a5b2914beff9c3742(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group_name: builtins.str,
    retention: RetentionDays,
    log_group_region: typing.Optional[builtins.str] = None,
    log_retention_retry_options: typing.Optional[typing.Union[LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ad180609ca86d06e8e1cab1c60b1817923869c2691b02bbd1f4385b52725e5(
    *,
    log_group_name: builtins.str,
    retention: RetentionDays,
    log_group_region: typing.Optional[builtins.str] = None,
    log_retention_retry_options: typing.Optional[typing.Union[LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78fee926002f7f3516e399cbdc05386761049865e684a426009126f7a4ccbbd(
    *,
    base: typing.Optional[_Duration_070aa057] = None,
    max_retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eeac18022a002ccfdefb3b01a3fd8cf3109803b5a7b056b9e49443d637b09bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group: ILogGroup,
    log_stream_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacf0e838d63538a2799e0c1d1e2ced394a4abe43f838b92f30c761a8dd62f74(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    log_stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5709347cc47fadaad33a7f4239f7e8b5fe4d18082057801758242a615aa7ec28(
    *,
    log_group: ILogGroup,
    log_stream_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e708f819c4286cfb8b2ca3a208b616f946ba803f0c484c7d3876a418791d13(
    *,
    arn: builtins.str,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da25335796fefba8050510fd40210d3972d40537f7988fa138a104d4414a465(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group: ILogGroup,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59bcddc6a371b0b385413a2dece9edc02cfd586071249abedecd0e8bc66e584(
    *,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4270b7d9bbdb52d731c4469a914b0fa3e3940a4b19adb66a9bd25d719519917b(
    *,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
    log_group: ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3494b258801c6f0f90f53c9f3e82248946b6a09eaa8d5b6c9921cba9d4ee2d0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    query_definition_name: builtins.str,
    query_string: QueryString,
    log_groups: typing.Optional[typing.Sequence[ILogGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a413f3493dd443f75478c8ab40b530523017fb90d0d9a36aa24e7b7d3ca51306(
    *,
    query_definition_name: builtins.str,
    query_string: QueryString,
    log_groups: typing.Optional[typing.Sequence[ILogGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4aea6f0385fde5f7a674c2872c0d9df6bbbe6b8fe16956792d6343f303c019(
    *,
    display: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    filter: typing.Optional[builtins.str] = None,
    limit: typing.Optional[jsii.Number] = None,
    parse: typing.Optional[builtins.str] = None,
    sort: typing.Optional[builtins.str] = None,
    stats: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce7ed2bbd7b86bb1435856be4b40ff98aaea72df5bc6cd6cc5b0be5e163a7fe(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    resource_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034de1d72f2257e2aad72fbdbd1acdfdf6052134ae135d2b1bc80caf899cc47f(
    *,
    policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    resource_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201dfea95d4608037ea86c671ee9e2e47d53eee2fae8e62c511b7242aae364ee(
    columns: typing.Sequence[builtins.str],
    restrictions: typing.Mapping[builtins.str, typing.Sequence[typing.Union[ColumnRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29aea15442e5dae204d31348b0d3100f070fe625e4ff02b6be44928f55cf948f(
    columns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c8e701ae3efdc5a1c8d3494734382a00000795439466dd075cf83909b3e3e2(
    column_name: builtins.str,
    comparison: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97843ea52d2c5501746f6dc4b46073f50b5c90ec953d87f9aa2ad9ef2898ef62(
    column_name: builtins.str,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6811f4c15328aa7ae283b0c0a596227eaf88de84fdd4946de7556e1eecc9dd73(
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0168ffffe070a301bfc4483a950daf4cae7c18eade13de303aeaa986e90109bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group: ILogGroup,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784581c59f7691426dc6def33084aa510201472914fbd2d9004dcd3e3a64dad7(
    *,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c873e24975576e2cf985e4057d4821bbcdef1b8c33548cad85a9d9af1c3bbf(
    *,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
    log_group: ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864ab89cd5b2c71964dceae91572c99415a804b28da1e887fcbce2ab448fea01(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    role: _IRole_59af6f50,
    target_arn: builtins.str,
    destination_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4d8b545461929090a250ab5e7be4a2ff9fbff1b9e297f5c41be7d117797e49(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0312d2390e235dc277da3e3b8b49ae2c66d53e7c1223bdd7783f3fbad2f2bdc7(
    _scope: _Construct_e78e779f,
    _source_log_group: ILogGroup,
) -> None:
    """Type checking stubs"""
    pass
