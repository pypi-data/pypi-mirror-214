'''
# Amazon CloudWatch Construct Library

## Metric objects

Metric objects represent a metric that is emitted by AWS services or your own
application, such as `CPUUsage`, `FailureCount` or `Bandwidth`.

Metric objects can be constructed directly or are exposed by resources as
attributes. Resources that expose metrics will have functions that look
like `metricXxx()` which will return a Metric object, initialized with defaults
that make sense.

For example, `lambda.Function` objects have the `fn.metricErrors()` method, which
represents the amount of errors reported by that Lambda function:

```python
# fn: lambda.Function


errors = fn.metric_errors()
```

`Metric` objects can be account and region aware. You can specify `account` and `region` as properties of the metric, or use the `metric.attachTo(Construct)` method. `metric.attachTo()` will automatically copy the `region` and `account` fields of the `Construct`, which can come from anywhere in the Construct tree.

You can also instantiate `Metric` objects to reference any
[published metric](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html)
that's not exposed using a convenience method on the CDK construct.
For example:

```python
hosted_zone = route53.HostedZone(self, "MyHostedZone", zone_name="example.org")
metric = cloudwatch.Metric(
    namespace="AWS/Route53",
    metric_name="DNSQueries",
    dimensions_map={
        "HostedZoneId": hosted_zone.hosted_zone_id
    }
)
```

### Instantiating a new Metric object

If you want to reference a metric that is not yet exposed by an existing construct,
you can instantiate a `Metric` object to represent it. For example:

```python
metric = cloudwatch.Metric(
    namespace="MyNamespace",
    metric_name="MyMetric",
    dimensions_map={
        "ProcessingStep": "Download"
    }
)
```

### Metric Math

Math expressions are supported by instantiating the `MathExpression` class.
For example, a math expression that sums two other metrics looks like this:

```python
# fn: lambda.Function


all_problems = cloudwatch.MathExpression(
    expression="errors + throttles",
    using_metrics={
        "errors": fn.metric_errors(),
        "faults": fn.metric_throttles()
    }
)
```

You can use `MathExpression` objects like any other metric, including using
them in other math expressions:

```python
# fn: lambda.Function
# all_problems: cloudwatch.MathExpression


problem_percentage = cloudwatch.MathExpression(
    expression="(problems / invocations) * 100",
    using_metrics={
        "problems": all_problems,
        "invocations": fn.metric_invocations()
    }
)
```

### Search Expressions

Math expressions also support search expressions. For example, the following
search expression returns all CPUUtilization metrics that it finds, with the
graph showing the Average statistic with an aggregation period of 5 minutes:

```python
cpu_utilization = cloudwatch.MathExpression(
    expression="SEARCH('{AWS/EC2,InstanceId} MetricName=\"CPUUtilization\"', 'Average', 300)",

    # Specifying '' as the label suppresses the default behavior
    # of using the expression as metric label. This is especially appropriate
    # when using expressions that return multiple time series (like SEARCH()
    # or METRICS()), to show the labels of the retrieved metrics only.
    label=""
)
```

Cross-account and cross-region search expressions are also supported. Use
the `searchAccount` and `searchRegion` properties to specify the account
and/or region to evaluate the search expression against.

### Aggregation

To graph or alarm on metrics you must aggregate them first, using a function
like `Average` or a percentile function like `P99`. By default, most Metric objects
returned by CDK libraries will be configured as `Average` over `300 seconds` (5 minutes).
The exception is if the metric represents a count of discrete events, such as
failures. In that case, the Metric object will be configured as `Sum` over `300 seconds`, i.e. it represents the number of times that event occurred over the
time period.

If you want to change the default aggregation of the Metric object (for example,
the function or the period), you can do so by passing additional parameters
to the metric function call:

```python
# fn: lambda.Function


minute_error_rate = fn.metric_errors(
    statistic="avg",
    period=Duration.minutes(1),
    label="Lambda failure rate"
)
```

This function also allows changing the metric label or color (which will be
useful when embedding them in graphs, see below).

> Rates versus Sums
>
> The reason for using `Sum` to count discrete events is that *some* events are
> emitted as either `0` or `1` (for example `Errors` for a Lambda) and some are
> only emitted as `1` (for example `NumberOfMessagesPublished` for an SNS
> topic).
>
> In case `0`-metrics are emitted, it makes sense to take the `Average` of this
> metric: the result will be the fraction of errors over all executions.
>
> If `0`-metrics are not emitted, the `Average` will always be equal to `1`,
> and not be very useful.
>
> In order to simplify the mental model of `Metric` objects, we default to
> aggregating using `Sum`, which will be the same for both metrics types. If you
> happen to know the Metric you want to alarm on makes sense as a rate
> (`Average`) you can always choose to change the statistic.

### Labels

Metric labels are displayed in the legend of graphs that include the metrics.

You can use [dynamic labels](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html)
to show summary information about the displayed time series
in the legend. For example, if you use:

```python
# fn: lambda.Function


minute_error_rate = fn.metric_errors(
    statistic="sum",
    period=Duration.hours(1),

    # Show the maximum hourly error count in the legend
    label="[max: ${MAX}] Lambda failure rate"
)
```

As the metric label, the maximum value in the visible range will
be shown next to the time series name in the graph's legend.

If the metric is a math expression producing more than one time series, the
maximum will be individually calculated and shown for each time series produce
by the math expression.

## Alarms

Alarms can be created on metrics in one of two ways. Either create an `Alarm`
object, passing the `Metric` object to set the alarm on:

```python
# fn: lambda.Function


cloudwatch.Alarm(self, "Alarm",
    metric=fn.metric_errors(),
    threshold=100,
    evaluation_periods=2
)
```

Alternatively, you can call `metric.createAlarm()`:

```python
# fn: lambda.Function


fn.metric_errors().create_alarm(self, "Alarm",
    threshold=100,
    evaluation_periods=2
)
```

The most important properties to set while creating an Alarms are:

* `threshold`: the value to compare the metric against.
* `comparisonOperator`: the comparison operation to use, defaults to `metric >= threshold`.
* `evaluationPeriods`: how many consecutive periods the metric has to be
  breaching the the threshold for the alarm to trigger.

To create a cross-account alarm, make sure you have enabled [cross-account functionality](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Cross-Account-Cross-Region.html) in CloudWatch. Then, set the `account` property in the `Metric` object either manually or via the `metric.attachTo()` method.

### Alarm Actions

To add actions to an alarm, use the integration classes from the
`@aws-cdk/aws-cloudwatch-actions` package. For example, to post a message to
an SNS topic when an alarm breaches, do the following:

```python
import monocdk as cw_actions
# alarm: cloudwatch.Alarm


topic = sns.Topic(self, "Topic")
alarm.add_alarm_action(cw_actions.SnsAction(topic))
```

#### Notification formats

Alarms can be created in one of two "formats":

* With "top-level parameters" (these are the classic style of CloudWatch Alarms).
* With a list of metrics specifications (these are the modern style of CloudWatch Alarms).

For backwards compatibility, CDK will try to create classic, top-level CloudWatch alarms
as much as possible, unless you are using features that cannot be expressed in that format.
Features that require the new-style alarm format are:

* Metric math
* Cross-account metrics
* Labels

The difference between these two does not impact the functionality of the alarm
in any way, *except* that the format of the notifications the Alarm generates is
different between them. This affects both the notifications sent out over SNS,
as well as the EventBridge events generated by this Alarm. If you are writing
code to consume these notifications, be sure to handle both formats.

### Composite Alarms

[Composite Alarms](https://aws.amazon.com/about-aws/whats-new/2020/03/amazon-cloudwatch-now-allows-you-to-combine-multiple-alarms/)
can be created from existing Alarm resources.

```python
# alarm1: cloudwatch.Alarm
# alarm2: cloudwatch.Alarm
# alarm3: cloudwatch.Alarm
# alarm4: cloudwatch.Alarm


alarm_rule = cloudwatch.AlarmRule.any_of(
    cloudwatch.AlarmRule.all_of(
        cloudwatch.AlarmRule.any_of(alarm1,
            cloudwatch.AlarmRule.from_alarm(alarm2, cloudwatch.AlarmState.OK), alarm3),
        cloudwatch.AlarmRule.not(cloudwatch.AlarmRule.from_alarm(alarm4, cloudwatch.AlarmState.INSUFFICIENT_DATA))),
    cloudwatch.AlarmRule.from_boolean(False))

cloudwatch.CompositeAlarm(self, "MyAwesomeCompositeAlarm",
    alarm_rule=alarm_rule
)
```

### A note on units

In CloudWatch, Metrics datums are emitted with units, such as `seconds` or
`bytes`. When `Metric` objects are given a `unit` attribute, it will be used to
*filter* the stream of metric datums for datums emitted using the same `unit`
attribute.

In particular, the `unit` field is *not* used to rescale datums or alarm threshold
values (for example, it cannot be used to specify an alarm threshold in
*Megabytes* if the metric stream is being emitted as *bytes*).

You almost certainly don't want to specify the `unit` property when creating
`Metric` objects (which will retrieve all datums regardless of their unit),
unless you have very specific requirements. Note that in any case, CloudWatch
only supports filtering by `unit` for Alarms, not in Dashboard graphs.

Please see the following GitHub issue for a discussion on real unit
calculations in CDK: https://github.com/aws/aws-cdk/issues/5595

## Dashboards

Dashboards are set of Widgets stored server-side which can be accessed quickly
from the AWS console. Available widgets are graphs of a metric over time, the
current value of a metric, or a static piece of Markdown which explains what the
graphs mean.

The following widgets are available:

* `GraphWidget` -- shows any number of metrics on both the left and right
  vertical axes.
* `AlarmWidget` -- shows the graph and alarm line for a single alarm.
* `SingleValueWidget` -- shows the current value of a set of metrics.
* `TextWidget` -- shows some static Markdown.
* `AlarmStatusWidget` -- shows the status of your alarms in a grid view.

### Graph widget

A graph widget can display any number of metrics on either the `left` or
`right` vertical axis:

```python
# dashboard: cloudwatch.Dashboard
# execution_count_metric: cloudwatch.Metric
# error_count_metric: cloudwatch.Metric


dashboard.add_widgets(cloudwatch.GraphWidget(
    title="Executions vs error rate",

    left=[execution_count_metric],

    right=[error_count_metric.with(
        statistic="average",
        label="Error rate",
        color=cloudwatch.Color.GREEN
    )]
))
```

Using the methods `addLeftMetric()` and `addRightMetric()` you can add metrics to a graph widget later on.

Graph widgets can also display annotations attached to the left or the right y-axis.

```python
# dashboard: cloudwatch.Dashboard


dashboard.add_widgets(cloudwatch.GraphWidget(
    # ...

    left_annotations=[cloudwatch.aws_cloudwatch.HorizontalAnnotation(value=1800, label=Duration.minutes(30).to_human_string(), color=cloudwatch.Color.RED), cloudwatch.aws_cloudwatch.HorizontalAnnotation(value=3600, label="1 hour", color="#2ca02c")
    ]
))
```

The graph legend can be adjusted from the default position at bottom of the widget.

```python
# dashboard: cloudwatch.Dashboard


dashboard.add_widgets(cloudwatch.GraphWidget(
    # ...

    legend_position=cloudwatch.LegendPosition.RIGHT
))
```

The graph can publish live data within the last minute that has not been fully aggregated.

```python
# dashboard: cloudwatch.Dashboard


dashboard.add_widgets(cloudwatch.GraphWidget(
    # ...

    live_data=True
))
```

The graph view can be changed from default 'timeSeries' to 'bar' or 'pie'.

```python
# dashboard: cloudwatch.Dashboard


dashboard.add_widgets(cloudwatch.GraphWidget(
    # ...

    view=cloudwatch.GraphWidgetView.BAR
))
```

### Alarm widget

An alarm widget shows the graph and the alarm line of a single alarm:

```python
# dashboard: cloudwatch.Dashboard
# error_alarm: cloudwatch.Alarm


dashboard.add_widgets(cloudwatch.AlarmWidget(
    title="Errors",
    alarm=error_alarm
))
```

### Single value widget

A single-value widget shows the latest value of a set of metrics (as opposed
to a graph of the value over time):

```python
# dashboard: cloudwatch.Dashboard
# visitor_count: cloudwatch.Metric
# purchase_count: cloudwatch.Metric


dashboard.add_widgets(cloudwatch.SingleValueWidget(
    metrics=[visitor_count, purchase_count]
))
```

Show as many digits as can fit, before rounding.

```python
# dashboard: cloudwatch.Dashboard


dashboard.add_widgets(cloudwatch.SingleValueWidget(
    metrics=[],

    full_precision=True
))
```

### Text widget

A text widget shows an arbitrary piece of MarkDown. Use this to add explanations
to your dashboard:

```python
# dashboard: cloudwatch.Dashboard


dashboard.add_widgets(cloudwatch.TextWidget(
    markdown="# Key Performance Indicators"
))
```

### Alarm Status widget

An alarm status widget displays instantly the status of any type of alarms and gives the
ability to aggregate one or more alarms together in a small surface.

```python
# dashboard: cloudwatch.Dashboard
# error_alarm: cloudwatch.Alarm


dashboard.add_widgets(
    cloudwatch.AlarmStatusWidget(
        alarms=[error_alarm]
    ))
```

An alarm status widget only showing firing alarms, sorted by state and timestamp:

```python
# dashboard: cloudwatch.Dashboard
# error_alarm: cloudwatch.Alarm


dashboard.add_widgets(cloudwatch.AlarmStatusWidget(
    title="Errors",
    alarms=[error_alarm],
    sort_by=cloudwatch.AlarmStatusWidgetSortBy.STATE_UPDATED_TIMESTAMP,
    states=[cloudwatch.AlarmState.ALARM]
))
```

### Query results widget

A `LogQueryWidget` shows the results of a query from Logs Insights:

```python
# dashboard: cloudwatch.Dashboard


dashboard.add_widgets(cloudwatch.LogQueryWidget(
    log_group_names=["my-log-group"],
    view=cloudwatch.LogQueryVisualizationType.TABLE,
    # The lines will be automatically combined using '\n|'.
    query_lines=["fields @message", "filter @message like /Error/"
    ]
))
```

### Custom widget

A `CustomWidget` shows the result of an AWS Lambda function:

```python
# dashboard: cloudwatch.Dashboard


# Import or create a lambda function
fn = lambda_.Function.from_function_arn(dashboard, "Function", "arn:aws:lambda:us-east-1:123456789012:function:MyFn")

dashboard.add_widgets(cloudwatch.CustomWidget(
    function_arn=fn.function_arn,
    title="My lambda baked widget"
))
```

You can learn more about custom widgets in the [Amazon Cloudwatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/add_custom_widget_dashboard.html).

### Dashboard Layout

The widgets on a dashboard are visually laid out in a grid that is 24 columns
wide. Normally you specify X and Y coordinates for the widgets on a Dashboard,
but because this is inconvenient to do manually, the library contains a simple
layout system to help you lay out your dashboards the way you want them to.

Widgets have a `width` and `height` property, and they will be automatically
laid out either horizontally or vertically stacked to fill out the available
space.

Widgets are added to a Dashboard by calling `add(widget1, widget2, ...)`.
Widgets given in the same call will be laid out horizontally. Widgets given
in different calls will be laid out vertically. To make more complex layouts,
you can use the following widgets to pack widgets together in different ways:

* `Column`: stack two or more widgets vertically.
* `Row`: lay out two or more widgets horizontally.
* `Spacer`: take up empty space
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
    Resource as _Resource_abff4495,
    ResourceProps as _ResourceProps_9b554c0f,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_iam import Grant as _Grant_bcb5eae7, IGrantable as _IGrantable_4c5a91d1


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.AlarmActionConfig",
    jsii_struct_bases=[],
    name_mapping={"alarm_action_arn": "alarmActionArn"},
)
class AlarmActionConfig:
    def __init__(self, *, alarm_action_arn: builtins.str) -> None:
        '''(experimental) Properties for an alarm action.

        :param alarm_action_arn: (experimental) Return the ARN that should be used for a CloudWatch Alarm action.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            alarm_action_config = cloudwatch.AlarmActionConfig(
                alarm_action_arn="alarmActionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828b5e743f934eace92473166216cdba7942dba7759734258932c75f6d1b60fe)
            check_type(argname="argument alarm_action_arn", value=alarm_action_arn, expected_type=type_hints["alarm_action_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_action_arn": alarm_action_arn,
        }

    @builtins.property
    def alarm_action_arn(self) -> builtins.str:
        '''(experimental) Return the ARN that should be used for a CloudWatch Alarm action.

        :stability: experimental
        '''
        result = self._values.get("alarm_action_arn")
        assert result is not None, "Required property 'alarm_action_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlarmRule(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_cloudwatch.AlarmRule"):
    '''(experimental) Class with static functions to build AlarmRule for Composite Alarms.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # alarm1: cloudwatch.Alarm
        # alarm2: cloudwatch.Alarm
        # alarm3: cloudwatch.Alarm
        # alarm4: cloudwatch.Alarm
        
        
        alarm_rule = cloudwatch.AlarmRule.any_of(
            cloudwatch.AlarmRule.all_of(
                cloudwatch.AlarmRule.any_of(alarm1,
                    cloudwatch.AlarmRule.from_alarm(alarm2, cloudwatch.AlarmState.OK), alarm3),
                cloudwatch.AlarmRule.not(cloudwatch.AlarmRule.from_alarm(alarm4, cloudwatch.AlarmState.INSUFFICIENT_DATA))),
            cloudwatch.AlarmRule.from_boolean(False))
        
        cloudwatch.CompositeAlarm(self, "MyAwesomeCompositeAlarm",
            alarm_rule=alarm_rule
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="allOf")
    @builtins.classmethod
    def all_of(cls, *operands: "IAlarmRule") -> "IAlarmRule":
        '''(experimental) function to join all provided AlarmRules with AND operator.

        :param operands: IAlarmRules to be joined with AND operator.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ccc76ffbdaab58ab46dd890881bd2d51fda3ffaade34818c9d921c9aad17e2)
            check_type(argname="argument operands", value=operands, expected_type=typing.Tuple[type_hints["operands"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IAlarmRule", jsii.sinvoke(cls, "allOf", [*operands]))

    @jsii.member(jsii_name="anyOf")
    @builtins.classmethod
    def any_of(cls, *operands: "IAlarmRule") -> "IAlarmRule":
        '''(experimental) function to join all provided AlarmRules with OR operator.

        :param operands: IAlarmRules to be joined with OR operator.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e55dc9e374eb3ce18406aaa408fd4f91f84b4e98908ac8da0f8f3ebcb42f598)
            check_type(argname="argument operands", value=operands, expected_type=typing.Tuple[type_hints["operands"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IAlarmRule", jsii.sinvoke(cls, "anyOf", [*operands]))

    @jsii.member(jsii_name="fromAlarm")
    @builtins.classmethod
    def from_alarm(cls, alarm: "IAlarm", alarm_state: "AlarmState") -> "IAlarmRule":
        '''(experimental) function to build Rule Expression for given IAlarm and AlarmState.

        :param alarm: IAlarm to be used in Rule Expression.
        :param alarm_state: AlarmState to be used in Rule Expression.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45af71d930e95351339b010f5ab318692e68cdb6dee7a20949d9dbedc12f2d27)
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
            check_type(argname="argument alarm_state", value=alarm_state, expected_type=type_hints["alarm_state"])
        return typing.cast("IAlarmRule", jsii.sinvoke(cls, "fromAlarm", [alarm, alarm_state]))

    @jsii.member(jsii_name="fromBoolean")
    @builtins.classmethod
    def from_boolean(cls, value: builtins.bool) -> "IAlarmRule":
        '''(experimental) function to build TRUE/FALSE intent for Rule Expression.

        :param value: boolean value to be used in rule expression.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dcd555c870f9f21a529544f6b53e8389836573ef98bc7355cfebae9597e4b30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("IAlarmRule", jsii.sinvoke(cls, "fromBoolean", [value]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, alarm_rule: builtins.str) -> "IAlarmRule":
        '''(experimental) function to build Rule Expression for given Alarm Rule string.

        :param alarm_rule: string to be used in Rule Expression.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2455351c588454e76962f85dfda3a8ac9433bc75f318bbf33b65ce82550a5cc)
            check_type(argname="argument alarm_rule", value=alarm_rule, expected_type=type_hints["alarm_rule"])
        return typing.cast("IAlarmRule", jsii.sinvoke(cls, "fromString", [alarm_rule]))

    @jsii.member(jsii_name="not")
    @builtins.classmethod
    def not_(cls, operand: "IAlarmRule") -> "IAlarmRule":
        '''(experimental) function to wrap provided AlarmRule in NOT operator.

        :param operand: IAlarmRule to be wrapped in NOT operator.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d634202649774dde1ecfee34cdfa2e6f61245ee27de9ead3ab9cdca28d14953)
            check_type(argname="argument operand", value=operand, expected_type=type_hints["operand"])
        return typing.cast("IAlarmRule", jsii.sinvoke(cls, "not", [operand]))


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.AlarmState")
class AlarmState(enum.Enum):
    '''(experimental) Enumeration indicates state of Alarm used in building Alarm Rule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        # error_alarm: cloudwatch.Alarm
        
        
        dashboard.add_widgets(cloudwatch.AlarmStatusWidget(
            title="Errors",
            alarms=[error_alarm],
            sort_by=cloudwatch.AlarmStatusWidgetSortBy.STATE_UPDATED_TIMESTAMP,
            states=[cloudwatch.AlarmState.ALARM]
        ))
    '''

    ALARM = "ALARM"
    '''(experimental) State indicates resource is in ALARM.

    :stability: experimental
    '''
    OK = "OK"
    '''(experimental) State indicates resource is not in ALARM.

    :stability: experimental
    '''
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    '''(experimental) State indicates there is not enough data to determine is resource is in ALARM.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.AlarmStatusWidgetProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarms": "alarms",
        "height": "height",
        "sort_by": "sortBy",
        "states": "states",
        "title": "title",
        "width": "width",
    },
)
class AlarmStatusWidgetProps:
    def __init__(
        self,
        *,
        alarms: typing.Sequence["IAlarm"],
        height: typing.Optional[jsii.Number] = None,
        sort_by: typing.Optional["AlarmStatusWidgetSortBy"] = None,
        states: typing.Optional[typing.Sequence[AlarmState]] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for an Alarm Status Widget.

        :param alarms: (experimental) CloudWatch Alarms to show in widget.
        :param height: (experimental) Height of the widget. Default: 3
        :param sort_by: (experimental) Specifies how to sort the alarms in the widget. Default: - alphabetical order
        :param states: (experimental) Use this field to filter the list of alarms displayed in the widget to only those alarms currently in the specified states. You can specify one or more alarm states in the value for this field. The alarm states that you can specify are ALARM, INSUFFICIENT_DATA, and OK. If you omit this field or specify an empty array, all the alarms specifed in alarms are displayed. Default: - all the alarms specified in alarms are displayed.
        :param title: (experimental) The title of the widget. Default: 'Alarm Status'
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # dashboard: cloudwatch.Dashboard
            # error_alarm: cloudwatch.Alarm
            
            
            dashboard.add_widgets(
                cloudwatch.AlarmStatusWidget(
                    alarms=[error_alarm]
                ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c87adf30fb80727ccb2d1e6883ef8b04e7ce2e1792eb226d045b4c444093d5)
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument sort_by", value=sort_by, expected_type=type_hints["sort_by"])
            check_type(argname="argument states", value=states, expected_type=type_hints["states"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarms": alarms,
        }
        if height is not None:
            self._values["height"] = height
        if sort_by is not None:
            self._values["sort_by"] = sort_by
        if states is not None:
            self._values["states"] = states
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def alarms(self) -> typing.List["IAlarm"]:
        '''(experimental) CloudWatch Alarms to show in widget.

        :stability: experimental
        '''
        result = self._values.get("alarms")
        assert result is not None, "Required property 'alarms' is missing"
        return typing.cast(typing.List["IAlarm"], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the widget.

        :default: 3

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sort_by(self) -> typing.Optional["AlarmStatusWidgetSortBy"]:
        '''(experimental) Specifies how to sort the alarms in the widget.

        :default: - alphabetical order

        :stability: experimental
        '''
        result = self._values.get("sort_by")
        return typing.cast(typing.Optional["AlarmStatusWidgetSortBy"], result)

    @builtins.property
    def states(self) -> typing.Optional[typing.List[AlarmState]]:
        '''(experimental) Use this field to filter the list of alarms displayed in the widget to only those alarms currently in the specified states.

        You can specify one or more alarm states in the value for this field.
        The alarm states that you can specify are ALARM, INSUFFICIENT_DATA, and OK.

        If you omit this field or specify an empty array, all the alarms specifed in alarms are displayed.

        :default: - all the alarms specified in alarms are displayed.

        :stability: experimental
        '''
        result = self._values.get("states")
        return typing.cast(typing.Optional[typing.List[AlarmState]], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''(experimental) The title of the widget.

        :default: 'Alarm Status'

        :stability: experimental
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the widget, in a grid of 24 units wide.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmStatusWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.AlarmStatusWidgetSortBy")
class AlarmStatusWidgetSortBy(enum.Enum):
    '''(experimental) The sort possibilities for AlarmStatusWidgets.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        # error_alarm: cloudwatch.Alarm
        
        
        dashboard.add_widgets(cloudwatch.AlarmStatusWidget(
            title="Errors",
            alarms=[error_alarm],
            sort_by=cloudwatch.AlarmStatusWidgetSortBy.STATE_UPDATED_TIMESTAMP,
            states=[cloudwatch.AlarmState.ALARM]
        ))
    '''

    DEFAULT = "DEFAULT"
    '''(experimental) Choose DEFAULT to sort them in alphabetical order by alarm name.

    :stability: experimental
    '''
    STATE_UPDATED_TIMESTAMP = "STATE_UPDATED_TIMESTAMP"
    '''(experimental) Choose STATE_UPDATED_TIMESTAMP to sort them first by alarm state, with alarms in ALARM state first, INSUFFICIENT_DATA alarms next, and OK alarms last.

    Within each group, the alarms are sorted by when they last changed state, with more recent state changes listed first.

    :stability: experimental
    '''
    TIMESTAMP = "TIMESTAMP"
    '''(experimental) Choose TIMESTAMP to sort them by the time when the alarms most recently changed state, no matter the current alarm state.

    The alarm that changed state most recently is listed first.

    :stability: experimental
    '''


@jsii.implements(_IInspectable_82c04a63)
class CfnAlarm(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.CfnAlarm",
):
    '''A CloudFormation ``AWS::CloudWatch::Alarm``.

    The ``AWS::CloudWatch::Alarm`` type specifies an alarm and associates it with the specified metric or metric math expression.

    When this operation creates an alarm, the alarm state is immediately set to ``INSUFFICIENT_DATA`` . The alarm is then evaluated and its state is set appropriately. Any actions associated with the new state are then executed.

    When you update an existing alarm, its state is left unchanged, but the update completely overwrites the previous configuration of the alarm.

    :cloudformationResource: AWS::CloudWatch::Alarm
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        cfn_alarm = cloudwatch.CfnAlarm(self, "MyCfnAlarm",
            comparison_operator="comparisonOperator",
            evaluation_periods=123,
        
            # the properties below are optional
            actions_enabled=False,
            alarm_actions=["alarmActions"],
            alarm_description="alarmDescription",
            alarm_name="alarmName",
            datapoints_to_alarm=123,
            dimensions=[cloudwatch.CfnAlarm.DimensionProperty(
                name="name",
                value="value"
            )],
            evaluate_low_sample_count_percentile="evaluateLowSampleCountPercentile",
            extended_statistic="extendedStatistic",
            insufficient_data_actions=["insufficientDataActions"],
            metric_name="metricName",
            metrics=[cloudwatch.CfnAlarm.MetricDataQueryProperty(
                id="id",
        
                # the properties below are optional
                account_id="accountId",
                expression="expression",
                label="label",
                metric_stat=cloudwatch.CfnAlarm.MetricStatProperty(
                    metric=cloudwatch.CfnAlarm.MetricProperty(
                        dimensions=[cloudwatch.CfnAlarm.DimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    period=123,
                    stat="stat",
        
                    # the properties below are optional
                    unit="unit"
                ),
                period=123,
                return_data=False
            )],
            namespace="namespace",
            ok_actions=["okActions"],
            period=123,
            statistic="statistic",
            threshold=123,
            threshold_metric_id="thresholdMetricId",
            treat_missing_data="treatMissingData",
            unit="unit"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        comparison_operator: builtins.str,
        evaluation_periods: jsii.Number,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAlarm.DimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        metrics: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAlarm.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        namespace: typing.Optional[builtins.str] = None,
        ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        period: typing.Optional[jsii.Number] = None,
        statistic: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        threshold_metric_id: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[builtins.str] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudWatch::Alarm``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param comparison_operator: The arithmetic operation to use when comparing the specified statistic and threshold. The specified statistic value is used as the first operand. You can specify the following values: ``GreaterThanThreshold`` , ``GreaterThanOrEqualToThreshold`` , ``LessThanThreshold`` , or ``LessThanOrEqualToThreshold`` .
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. If you are setting an alarm that requires that a number of consecutive data points be breaching to trigger the alarm, this value specifies that number. If you are setting an "M out of N" alarm, this value is the N, and ``DatapointsToAlarm`` is the M. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .
        :param actions_enabled: Indicates whether actions should be executed during any changes to the alarm state. The default is TRUE.
        :param alarm_actions: The list of actions to execute when this alarm transitions into an ALARM state from any other state. Specify each action as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutMetricAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param alarm_description: The description of the alarm.
        :param alarm_name: The name of the alarm. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the alarm name. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M, and the value that you set for ``EvaluationPeriods`` is the N value. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* . If you omit this parameter, CloudWatch uses the same value here that you set for ``EvaluationPeriods`` , and the alarm goes to alarm state if that many consecutive periods are breaching.
        :param dimensions: The dimensions for the metric associated with the alarm. For an alarm based on a math expression, you can't specify ``Dimensions`` . Instead, you use ``Metrics`` .
        :param evaluate_low_sample_count_percentile: Used only for alarms based on percentiles. If ``ignore`` , the alarm state does not change during periods with too few data points to be statistically significant. If ``evaluate`` or this parameter is not used, the alarm is always evaluated and possibly changes state no matter how many data points are available.
        :param extended_statistic: The percentile statistic for the metric associated with the alarm. Specify a value between p0.0 and p100. For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both. For an alarm based on a math expression, you can't specify ``ExtendedStatistic`` . Instead, you use ``Metrics`` .
        :param insufficient_data_actions: The actions to execute when this alarm transitions to the ``INSUFFICIENT_DATA`` state from any other state. Each action is specified as an Amazon Resource Name (ARN).
        :param metric_name: The name of the metric associated with the alarm. This is required for an alarm based on a metric. For an alarm based on a math expression, you use ``Metrics`` instead and you can't specify ``MetricName`` .
        :param metrics: An array that enables you to create an alarm based on the result of a metric math expression. Each item in the array either retrieves a metric or performs a math expression. If you specify the ``Metrics`` parameter, you cannot specify ``MetricName`` , ``Dimensions`` , ``Period`` , ``Namespace`` , ``Statistic`` , ``ExtendedStatistic`` , or ``Unit`` .
        :param namespace: The namespace of the metric associated with the alarm. This is required for an alarm based on a metric. For an alarm based on a math expression, you can't specify ``Namespace`` and you use ``Metrics`` instead. For a list of namespaces for metrics from AWS services, see `AWS Services That Publish CloudWatch Metrics. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_
        :param ok_actions: The actions to execute when this alarm transitions to the ``OK`` state from any other state. Each action is specified as an Amazon Resource Name (ARN).
        :param period: The period, in seconds, over which the statistic is applied. This is required for an alarm based on a metric. Valid values are 10, 30, 60, and any multiple of 60. For an alarm based on a math expression, you can't specify ``Period`` , and instead you use the ``Metrics`` parameter. *Minimum:* 10
        :param statistic: The statistic for the metric associated with the alarm, other than percentile. For percentile statistics, use ``ExtendedStatistic`` . For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both. For an alarm based on a math expression, you can't specify ``Statistic`` . Instead, you use ``Metrics`` .
        :param threshold: The value to compare with the specified statistic.
        :param threshold_metric_id: In an alarm based on an anomaly detection model, this is the ID of the ``ANOMALY_DETECTION_BAND`` function used as the threshold for the alarm.
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Valid values are ``breaching`` , ``notBreaching`` , ``ignore`` , and ``missing`` . For more information, see `Configuring How CloudWatch Alarms Treat Missing Data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-missing-data>`_ in the *Amazon CloudWatch User Guide* . If you omit this parameter, the default behavior of ``missing`` is used.
        :param unit: The unit of the metric associated with the alarm. Specify this only if you are creating an alarm based on a single metric. Do not specify this if you are specifying a ``Metrics`` array. You can specify the following values: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c24ca6383d248ea374ad81e7f13cdd4a072058b78dcf7bf2385aa98e1ad2133)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAlarmProps(
            comparison_operator=comparison_operator,
            evaluation_periods=evaluation_periods,
            actions_enabled=actions_enabled,
            alarm_actions=alarm_actions,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            dimensions=dimensions,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            extended_statistic=extended_statistic,
            insufficient_data_actions=insufficient_data_actions,
            metric_name=metric_name,
            metrics=metrics,
            namespace=namespace,
            ok_actions=ok_actions,
            period=period,
            statistic=statistic,
            threshold=threshold,
            threshold_metric_id=threshold_metric_id,
            treat_missing_data=treat_missing_data,
            unit=unit,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91d206bd113655b45d119993347bc9e78ca9b8fc3499119ef01759f71d6019c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab049447fe9220a41bfcac7f6d506f687a8a2bf503393a8eeb5ddcb592ae7e98)
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
        '''The ARN of the CloudWatch alarm, such as ``arn:aws:cloudwatch:us-west-2:123456789012:alarm:myCloudWatchAlarm-CPUAlarm-UXMMZK36R55Z`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> builtins.str:
        '''The arithmetic operation to use when comparing the specified statistic and threshold.

        The specified statistic value is used as the first operand.

        You can specify the following values: ``GreaterThanThreshold`` , ``GreaterThanOrEqualToThreshold`` , ``LessThanThreshold`` , or ``LessThanOrEqualToThreshold`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-comparisonoperator
        '''
        return typing.cast(builtins.str, jsii.get(self, "comparisonOperator"))

    @comparison_operator.setter
    def comparison_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60a4736d5ef7284ea710d91bef64e80f131e9eccd820b0feac514e3b5a7d8e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparisonOperator", value)

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        '''The number of periods over which data is compared to the specified threshold.

        If you are setting an alarm that requires that a number of consecutive data points be breaching to trigger the alarm, this value specifies that number. If you are setting an "M out of N" alarm, this value is the N, and ``DatapointsToAlarm`` is the M.

        For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-evaluationperiods
        '''
        return typing.cast(jsii.Number, jsii.get(self, "evaluationPeriods"))

    @evaluation_periods.setter
    def evaluation_periods(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33595f0ec9f507090942a0b67a10b8763d914bf0e95f880b79ff82c856e03c9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationPeriods", value)

    @builtins.property
    @jsii.member(jsii_name="actionsEnabled")
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether actions should be executed during any changes to the alarm state.

        The default is TRUE.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-actionsenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "actionsEnabled"))

    @actions_enabled.setter
    def actions_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62523cb7d3fa6fd5886a00ecbf98aa8e496669044f52d634d65e4854b42fbf05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="alarmActions")
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of actions to execute when this alarm transitions into an ALARM state from any other state.

        Specify each action as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutMetricAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-alarmactions
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "alarmActions"))

    @alarm_actions.setter
    def alarm_actions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e372146b0922980c86287415ac5e364ddfc1568817a733fdd53ced35c4dd8358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmActions", value)

    @builtins.property
    @jsii.member(jsii_name="alarmDescription")
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-alarmdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmDescription"))

    @alarm_description.setter
    def alarm_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c424852715a6156bea31c7a5765794861fc7f0c8b02fbd2ecb0109d72f08f147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmDescription", value)

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The name of the alarm.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the alarm name.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-alarmname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29724c0be9d5cee8832bbb0c491987cfa2d997d36adb9100fafa40dc43ba31cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value)

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M out of N" alarm. In that case, this value is the M, and the value that you set for ``EvaluationPeriods`` is the N value. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .

        If you omit this parameter, CloudWatch uses the same value here that you set for ``EvaluationPeriods`` , and the alarm goes to alarm state if that many consecutive periods are breaching.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-datapointstoalarm
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "datapointsToAlarm"))

    @datapoints_to_alarm.setter
    def datapoints_to_alarm(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d2ef1ef926d68bbeb61af51744c12b92bc26540305fa30af9fdfee8c9b5315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datapointsToAlarm", value)

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarm.DimensionProperty", _IResolvable_a771d0ef]]]]:
        '''The dimensions for the metric associated with the alarm.

        For an alarm based on a math expression, you can't specify ``Dimensions`` . Instead, you use ``Metrics`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-dimension
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarm.DimensionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "dimensions"))

    @dimensions.setter
    def dimensions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarm.DimensionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d133df1313d197b723790dcad4101ce29287628f175b37e4db21eb94dcfe27d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensions", value)

    @builtins.property
    @jsii.member(jsii_name="evaluateLowSampleCountPercentile")
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        '''Used only for alarms based on percentiles.

        If ``ignore`` , the alarm state does not change during periods with too few data points to be statistically significant. If ``evaluate`` or this parameter is not used, the alarm is always evaluated and possibly changes state no matter how many data points are available.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-evaluatelowsamplecountpercentile
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluateLowSampleCountPercentile"))

    @evaluate_low_sample_count_percentile.setter
    def evaluate_low_sample_count_percentile(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ae31754ab79be0b6f2568f893054fe16a36c23ca861c3525fccd87001a2538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluateLowSampleCountPercentile", value)

    @builtins.property
    @jsii.member(jsii_name="extendedStatistic")
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        '''The percentile statistic for the metric associated with the alarm. Specify a value between p0.0 and p100.

        For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both.

        For an alarm based on a math expression, you can't specify ``ExtendedStatistic`` . Instead, you use ``Metrics`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-extendedstatistic
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extendedStatistic"))

    @extended_statistic.setter
    def extended_statistic(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4553c43b30e89874ae83e6354b8d502ec595847884b34857dc1cad8a69b3550b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendedStatistic", value)

    @builtins.property
    @jsii.member(jsii_name="insufficientDataActions")
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ``INSUFFICIENT_DATA`` state from any other state.

        Each action is specified as an Amazon Resource Name (ARN).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-insufficientdataactions
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "insufficientDataActions"))

    @insufficient_data_actions.setter
    def insufficient_data_actions(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36105d7a1f9983b372591215bb9c09cc085c625b0cf9a439aa525d497424b4e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insufficientDataActions", value)

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric associated with the alarm.

        This is required for an alarm based on a metric. For an alarm based on a math expression, you use ``Metrics`` instead and you can't specify ``MetricName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-metricname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5356c5b82889bec14fbfc6f06e4e4b18e8782d782a0cd71530485a37949921fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarm.MetricDataQueryProperty", _IResolvable_a771d0ef]]]]:
        '''An array that enables you to create an alarm based on the result of a metric math expression.

        Each item in the array either retrieves a metric or performs a math expression.

        If you specify the ``Metrics`` parameter, you cannot specify ``MetricName`` , ``Dimensions`` , ``Period`` , ``Namespace`` , ``Statistic`` , ``ExtendedStatistic`` , or ``Unit`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-metrics
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarm.MetricDataQueryProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "metrics"))

    @metrics.setter
    def metrics(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarm.MetricDataQueryProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1f1038b6b29c749cbb7f277ef012c7726adf40bc5804b850ea0a38895c4428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metrics", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the metric associated with the alarm.

        This is required for an alarm based on a metric. For an alarm based on a math expression, you can't specify ``Namespace`` and you use ``Metrics`` instead.

        For a list of namespaces for metrics from AWS services, see `AWS Services That Publish CloudWatch Metrics. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-namespace
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7f180021c784875f3320d829202b9b517f804817d7930ff3cc5c727d0906db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="okActions")
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ``OK`` state from any other state.

        Each action is specified as an Amazon Resource Name (ARN).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-okactions
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "okActions"))

    @ok_actions.setter
    def ok_actions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b52c25ae87a46f62904cf534dda8f8daae553f306ec27cc90462a194bb51d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "okActions", value)

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> typing.Optional[jsii.Number]:
        '''The period, in seconds, over which the statistic is applied.

        This is required for an alarm based on a metric. Valid values are 10, 30, 60, and any multiple of 60.

        For an alarm based on a math expression, you can't specify ``Period`` , and instead you use the ``Metrics`` parameter.

        *Minimum:* 10

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-period
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "period"))

    @period.setter
    def period(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b5d4ef4fea06e25a9d6c64905a32a1f554c6ddf713660cae5523f926264c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> typing.Optional[builtins.str]:
        '''The statistic for the metric associated with the alarm, other than percentile. For percentile statistics, use ``ExtendedStatistic`` .

        For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both.

        For an alarm based on a math expression, you can't specify ``Statistic`` . Instead, you use ``Metrics`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-statistic
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statistic"))

    @statistic.setter
    def statistic(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde464d49ec310cbfcd21cfd9bb921930c2c69138fee6130181db71ec4b1e9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statistic", value)

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value to compare with the specified statistic.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-threshold
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0124f9ae85c4e9eb99be3196dbd924d8f830905e30f1ce4b7fc42d8fa807304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value)

    @builtins.property
    @jsii.member(jsii_name="thresholdMetricId")
    def threshold_metric_id(self) -> typing.Optional[builtins.str]:
        '''In an alarm based on an anomaly detection model, this is the ID of the ``ANOMALY_DETECTION_BAND`` function used as the threshold for the alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-dynamic-threshold
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdMetricId"))

    @threshold_metric_id.setter
    def threshold_metric_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e68c1e14e7e7d416e49a51141fef966c8b9c37439e87002c208ba84d5b4ddd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdMetricId", value)

    @builtins.property
    @jsii.member(jsii_name="treatMissingData")
    def treat_missing_data(self) -> typing.Optional[builtins.str]:
        '''Sets how this alarm is to handle missing data points.

        Valid values are ``breaching`` , ``notBreaching`` , ``ignore`` , and ``missing`` . For more information, see `Configuring How CloudWatch Alarms Treat Missing Data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-missing-data>`_ in the *Amazon CloudWatch User Guide* .

        If you omit this parameter, the default behavior of ``missing`` is used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-treatmissingdata
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "treatMissingData"))

    @treat_missing_data.setter
    def treat_missing_data(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf95b3bb442c2d369adc621180469300f23ebd3f858d8893412859068c9ede9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "treatMissingData", value)

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> typing.Optional[builtins.str]:
        '''The unit of the metric associated with the alarm.

        Specify this only if you are creating an alarm based on a single metric. Do not specify this if you are specifying a ``Metrics`` array.

        You can specify the following values: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-unit
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51907af862e25b54574dd482761a16eecda38676300ab082f32149a41025c334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAlarm.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''Dimension is an embedded property of the ``AWS::CloudWatch::Alarm`` type.

            Dimensions are name/value pairs that can be associated with a CloudWatch metric. You can specify a maximum of 10 dimensions for a given metric.

            :param name: The name of the dimension, from 1–255 characters in length. This dimension name must have been included when the metric was published.
            :param value: The value for the dimension, from 1–255 characters in length.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                dimension_property = cloudwatch.CfnAlarm.DimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77fd70bddd3c9b8df9e8a4a6052dc66f074ce0995925135b53a4ee698b32cb5b)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the dimension, from 1–255 characters in length.

            This dimension name must have been included when the metric was published.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html#cfn-cloudwatch-alarm-dimension-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value for the dimension, from 1–255 characters in length.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html#cfn-cloudwatch-alarm-dimension-value
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
        jsii_type="monocdk.aws_cloudwatch.CfnAlarm.MetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "account_id": "accountId",
            "expression": "expression",
            "label": "label",
            "metric_stat": "metricStat",
            "period": "period",
            "return_data": "returnData",
        },
    )
    class MetricDataQueryProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            account_id: typing.Optional[builtins.str] = None,
            expression: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[typing.Union["CfnAlarm.MetricStatProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            period: typing.Optional[jsii.Number] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The ``MetricDataQuery`` property type specifies the metric data to return, and whether this call is just retrieving a batch set of data for one metric, or is performing a math expression on metric data.

            Any expression used must return a single time series. For more information, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            :param id: A short name used to tie this object to the results in the response. This name must be unique within a single call to ``GetMetricData`` . If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.
            :param account_id: The ID of the account where the metrics are located, if this is a cross-account alarm.
            :param expression: The math expression to be performed on the returned data, if this object is performing a math expression. This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* . Within each MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param label: A human-readable label for this metric or expression. This is especially useful if this is an expression, so that you know what the value represents. If the metric or expression is shown in a CloudWatch dashboard widget, the label is shown. If ``Label`` is omitted, CloudWatch generates a default.
            :param metric_stat: The metric to be returned, along with statistics, period, and units. Use this parameter only if this object is retrieving a metric and not performing a math expression on returned data. Within one MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param period: The granularity, in seconds, of the returned data points. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` operation that includes a ``StorageResolution of 1 second`` .
            :param return_data: This option indicates whether to return the timestamps and raw data values of this metric. When you create an alarm based on a metric math expression, specify ``True`` for this value for only the one math expression that the alarm is based on. You must specify ``False`` for ``ReturnData`` for all the other metrics and expressions used in the alarm. This field is required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_data_query_property = cloudwatch.CfnAlarm.MetricDataQueryProperty(
                    id="id",
                
                    # the properties below are optional
                    account_id="accountId",
                    expression="expression",
                    label="label",
                    metric_stat=cloudwatch.CfnAlarm.MetricStatProperty(
                        metric=cloudwatch.CfnAlarm.MetricProperty(
                            dimensions=[cloudwatch.CfnAlarm.DimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        period=123,
                        stat="stat",
                
                        # the properties below are optional
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d1cb5a63970ca8765d2107090ed89107a38bf33148d51952b46452ea2fbbfe5)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }
            if account_id is not None:
                self._values["account_id"] = account_id
            if expression is not None:
                self._values["expression"] = expression
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if period is not None:
                self._values["period"] = period
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def id(self) -> builtins.str:
            '''A short name used to tie this object to the results in the response.

            This name must be unique within a single call to ``GetMetricData`` . If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the account where the metrics are located, if this is a cross-account alarm.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The math expression to be performed on the returned data, if this object is performing a math expression.

            This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            Within each MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''A human-readable label for this metric or expression.

            This is especially useful if this is an expression, so that you know what the value represents. If the metric or expression is shown in a CloudWatch dashboard widget, the label is shown. If ``Label`` is omitted, CloudWatch generates a default.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarm.MetricStatProperty", _IResolvable_a771d0ef]]:
            '''The metric to be returned, along with statistics, period, and units.

            Use this parameter only if this object is retrieving a metric and not performing a math expression on returned data.

            Within one MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union["CfnAlarm.MetricStatProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The granularity, in seconds, of the returned data points.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` operation that includes a ``StorageResolution of 1 second`` .
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''This option indicates whether to return the timestamps and raw data values of this metric.

            When you create an alarm based on a metric math expression, specify ``True`` for this value for only the one math expression that the alarm is based on. You must specify ``False`` for ``ReturnData`` for all the other metrics and expressions used in the alarm.

            This field is required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAlarm.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAlarm.DimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Metric`` property type represents a specific metric.

            ``Metric`` is a property of the `MetricStat <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html>`_ property type.

            :param dimensions: The metric dimensions that you want to be used for the metric that the alarm will watch.
            :param metric_name: The name of the metric that you want the alarm to watch. This is a required field.
            :param namespace: The namespace of the metric that the alarm will watch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_property = cloudwatch.CfnAlarm.MetricProperty(
                    dimensions=[cloudwatch.CfnAlarm.DimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ae49ce87a49f68673dfade799a579408e3dab374a0ce78a61aee42e76e06063)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarm.DimensionProperty", _IResolvable_a771d0ef]]]]:
            '''The metric dimensions that you want to be used for the metric that the alarm will watch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarm.DimensionProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric that you want the alarm to watch.

            This is a required field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric that the alarm will watch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAlarm.MetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric": "metric",
            "period": "period",
            "stat": "stat",
            "unit": "unit",
        },
    )
    class MetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Union[typing.Union["CfnAlarm.MetricProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            period: jsii.Number,
            stat: builtins.str,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the metric to be returned, along with the statistics, period, and units.

            ``MetricStat`` is a property of the `MetricDataQuery <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html>`_ property type.

            :param metric: The metric to return, including the metric name, namespace, and dimensions.
            :param period: The granularity, in seconds, of the returned data points. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second. If the ``StartTime`` parameter specifies a time stamp that is greater than 3 hours ago, you must specify the period as follows or no data points in that time range is returned: - Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute). - Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes). - Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).
            :param stat: The statistic to return. It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* .
            :param unit: The unit to use for the returned data points. Valid values are: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_stat_property = cloudwatch.CfnAlarm.MetricStatProperty(
                    metric=cloudwatch.CfnAlarm.MetricProperty(
                        dimensions=[cloudwatch.CfnAlarm.DimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    period=123,
                    stat="stat",
                
                    # the properties below are optional
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dad9e52cb051de75b765be5e717099b5f885390b0e3a27ccb8478123c5a967eb)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "metric": metric,
                "period": period,
                "stat": stat,
            }
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Union["CfnAlarm.MetricProperty", _IResolvable_a771d0ef]:
            '''The metric to return, including the metric name, namespace, and dimensions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-metric
            '''
            result = self._values.get("metric")
            assert result is not None, "Required property 'metric' is missing"
            return typing.cast(typing.Union["CfnAlarm.MetricProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def period(self) -> jsii.Number:
            '''The granularity, in seconds, of the returned data points.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second.

            If the ``StartTime`` parameter specifies a time stamp that is greater than 3 hours ago, you must specify the period as follows or no data points in that time range is returned:

            - Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute).
            - Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes).
            - Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-period
            '''
            result = self._values.get("period")
            assert result is not None, "Required property 'period' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def stat(self) -> builtins.str:
            '''The statistic to return.

            It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-stat
            '''
            result = self._values.get("stat")
            assert result is not None, "Required property 'stat' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to use for the returned data points.

            Valid values are: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CfnAlarmProps",
    jsii_struct_bases=[],
    name_mapping={
        "comparison_operator": "comparisonOperator",
        "evaluation_periods": "evaluationPeriods",
        "actions_enabled": "actionsEnabled",
        "alarm_actions": "alarmActions",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "dimensions": "dimensions",
        "evaluate_low_sample_count_percentile": "evaluateLowSampleCountPercentile",
        "extended_statistic": "extendedStatistic",
        "insufficient_data_actions": "insufficientDataActions",
        "metric_name": "metricName",
        "metrics": "metrics",
        "namespace": "namespace",
        "ok_actions": "okActions",
        "period": "period",
        "statistic": "statistic",
        "threshold": "threshold",
        "threshold_metric_id": "thresholdMetricId",
        "treat_missing_data": "treatMissingData",
        "unit": "unit",
    },
)
class CfnAlarmProps:
    def __init__(
        self,
        *,
        comparison_operator: builtins.str,
        evaluation_periods: jsii.Number,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAlarm.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        metrics: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAlarm.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        namespace: typing.Optional[builtins.str] = None,
        ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        period: typing.Optional[jsii.Number] = None,
        statistic: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        threshold_metric_id: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[builtins.str] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAlarm``.

        :param comparison_operator: The arithmetic operation to use when comparing the specified statistic and threshold. The specified statistic value is used as the first operand. You can specify the following values: ``GreaterThanThreshold`` , ``GreaterThanOrEqualToThreshold`` , ``LessThanThreshold`` , or ``LessThanOrEqualToThreshold`` .
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. If you are setting an alarm that requires that a number of consecutive data points be breaching to trigger the alarm, this value specifies that number. If you are setting an "M out of N" alarm, this value is the N, and ``DatapointsToAlarm`` is the M. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .
        :param actions_enabled: Indicates whether actions should be executed during any changes to the alarm state. The default is TRUE.
        :param alarm_actions: The list of actions to execute when this alarm transitions into an ALARM state from any other state. Specify each action as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutMetricAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param alarm_description: The description of the alarm.
        :param alarm_name: The name of the alarm. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the alarm name. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M, and the value that you set for ``EvaluationPeriods`` is the N value. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* . If you omit this parameter, CloudWatch uses the same value here that you set for ``EvaluationPeriods`` , and the alarm goes to alarm state if that many consecutive periods are breaching.
        :param dimensions: The dimensions for the metric associated with the alarm. For an alarm based on a math expression, you can't specify ``Dimensions`` . Instead, you use ``Metrics`` .
        :param evaluate_low_sample_count_percentile: Used only for alarms based on percentiles. If ``ignore`` , the alarm state does not change during periods with too few data points to be statistically significant. If ``evaluate`` or this parameter is not used, the alarm is always evaluated and possibly changes state no matter how many data points are available.
        :param extended_statistic: The percentile statistic for the metric associated with the alarm. Specify a value between p0.0 and p100. For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both. For an alarm based on a math expression, you can't specify ``ExtendedStatistic`` . Instead, you use ``Metrics`` .
        :param insufficient_data_actions: The actions to execute when this alarm transitions to the ``INSUFFICIENT_DATA`` state from any other state. Each action is specified as an Amazon Resource Name (ARN).
        :param metric_name: The name of the metric associated with the alarm. This is required for an alarm based on a metric. For an alarm based on a math expression, you use ``Metrics`` instead and you can't specify ``MetricName`` .
        :param metrics: An array that enables you to create an alarm based on the result of a metric math expression. Each item in the array either retrieves a metric or performs a math expression. If you specify the ``Metrics`` parameter, you cannot specify ``MetricName`` , ``Dimensions`` , ``Period`` , ``Namespace`` , ``Statistic`` , ``ExtendedStatistic`` , or ``Unit`` .
        :param namespace: The namespace of the metric associated with the alarm. This is required for an alarm based on a metric. For an alarm based on a math expression, you can't specify ``Namespace`` and you use ``Metrics`` instead. For a list of namespaces for metrics from AWS services, see `AWS Services That Publish CloudWatch Metrics. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_
        :param ok_actions: The actions to execute when this alarm transitions to the ``OK`` state from any other state. Each action is specified as an Amazon Resource Name (ARN).
        :param period: The period, in seconds, over which the statistic is applied. This is required for an alarm based on a metric. Valid values are 10, 30, 60, and any multiple of 60. For an alarm based on a math expression, you can't specify ``Period`` , and instead you use the ``Metrics`` parameter. *Minimum:* 10
        :param statistic: The statistic for the metric associated with the alarm, other than percentile. For percentile statistics, use ``ExtendedStatistic`` . For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both. For an alarm based on a math expression, you can't specify ``Statistic`` . Instead, you use ``Metrics`` .
        :param threshold: The value to compare with the specified statistic.
        :param threshold_metric_id: In an alarm based on an anomaly detection model, this is the ID of the ``ANOMALY_DETECTION_BAND`` function used as the threshold for the alarm.
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Valid values are ``breaching`` , ``notBreaching`` , ``ignore`` , and ``missing`` . For more information, see `Configuring How CloudWatch Alarms Treat Missing Data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-missing-data>`_ in the *Amazon CloudWatch User Guide* . If you omit this parameter, the default behavior of ``missing`` is used.
        :param unit: The unit of the metric associated with the alarm. Specify this only if you are creating an alarm based on a single metric. Do not specify this if you are specifying a ``Metrics`` array. You can specify the following values: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            cfn_alarm_props = cloudwatch.CfnAlarmProps(
                comparison_operator="comparisonOperator",
                evaluation_periods=123,
            
                # the properties below are optional
                actions_enabled=False,
                alarm_actions=["alarmActions"],
                alarm_description="alarmDescription",
                alarm_name="alarmName",
                datapoints_to_alarm=123,
                dimensions=[cloudwatch.CfnAlarm.DimensionProperty(
                    name="name",
                    value="value"
                )],
                evaluate_low_sample_count_percentile="evaluateLowSampleCountPercentile",
                extended_statistic="extendedStatistic",
                insufficient_data_actions=["insufficientDataActions"],
                metric_name="metricName",
                metrics=[cloudwatch.CfnAlarm.MetricDataQueryProperty(
                    id="id",
            
                    # the properties below are optional
                    account_id="accountId",
                    expression="expression",
                    label="label",
                    metric_stat=cloudwatch.CfnAlarm.MetricStatProperty(
                        metric=cloudwatch.CfnAlarm.MetricProperty(
                            dimensions=[cloudwatch.CfnAlarm.DimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        period=123,
                        stat="stat",
            
                        # the properties below are optional
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )],
                namespace="namespace",
                ok_actions=["okActions"],
                period=123,
                statistic="statistic",
                threshold=123,
                threshold_metric_id="thresholdMetricId",
                treat_missing_data="treatMissingData",
                unit="unit"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e0e217c648a25dde1802881478c821b3e1daa736f624effab66d5b567bfff1)
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument actions_enabled", value=actions_enabled, expected_type=type_hints["actions_enabled"])
            check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument evaluate_low_sample_count_percentile", value=evaluate_low_sample_count_percentile, expected_type=type_hints["evaluate_low_sample_count_percentile"])
            check_type(argname="argument extended_statistic", value=extended_statistic, expected_type=type_hints["extended_statistic"])
            check_type(argname="argument insufficient_data_actions", value=insufficient_data_actions, expected_type=type_hints["insufficient_data_actions"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument ok_actions", value=ok_actions, expected_type=type_hints["ok_actions"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument threshold_metric_id", value=threshold_metric_id, expected_type=type_hints["threshold_metric_id"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison_operator": comparison_operator,
            "evaluation_periods": evaluation_periods,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_actions is not None:
            self._values["alarm_actions"] = alarm_actions
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if evaluate_low_sample_count_percentile is not None:
            self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if extended_statistic is not None:
            self._values["extended_statistic"] = extended_statistic
        if insufficient_data_actions is not None:
            self._values["insufficient_data_actions"] = insufficient_data_actions
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if metrics is not None:
            self._values["metrics"] = metrics
        if namespace is not None:
            self._values["namespace"] = namespace
        if ok_actions is not None:
            self._values["ok_actions"] = ok_actions
        if period is not None:
            self._values["period"] = period
        if statistic is not None:
            self._values["statistic"] = statistic
        if threshold is not None:
            self._values["threshold"] = threshold
        if threshold_metric_id is not None:
            self._values["threshold_metric_id"] = threshold_metric_id
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def comparison_operator(self) -> builtins.str:
        '''The arithmetic operation to use when comparing the specified statistic and threshold.

        The specified statistic value is used as the first operand.

        You can specify the following values: ``GreaterThanThreshold`` , ``GreaterThanOrEqualToThreshold`` , ``LessThanThreshold`` , or ``LessThanOrEqualToThreshold`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-comparisonoperator
        '''
        result = self._values.get("comparison_operator")
        assert result is not None, "Required property 'comparison_operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        '''The number of periods over which data is compared to the specified threshold.

        If you are setting an alarm that requires that a number of consecutive data points be breaching to trigger the alarm, this value specifies that number. If you are setting an "M out of N" alarm, this value is the N, and ``DatapointsToAlarm`` is the M.

        For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-evaluationperiods
        '''
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether actions should be executed during any changes to the alarm state.

        The default is TRUE.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-actionsenabled
        '''
        result = self._values.get("actions_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of actions to execute when this alarm transitions into an ALARM state from any other state.

        Specify each action as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutMetricAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-alarmactions
        '''
        result = self._values.get("alarm_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-alarmdescription
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The name of the alarm.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the alarm name.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-alarmname
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M out of N" alarm. In that case, this value is the M, and the value that you set for ``EvaluationPeriods`` is the N value. For more information, see `Evaluating an Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation>`_ in the *Amazon CloudWatch User Guide* .

        If you omit this parameter, CloudWatch uses the same value here that you set for ``EvaluationPeriods`` , and the alarm goes to alarm state if that many consecutive periods are breaching.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-datapointstoalarm
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAlarm.DimensionProperty, _IResolvable_a771d0ef]]]]:
        '''The dimensions for the metric associated with the alarm.

        For an alarm based on a math expression, you can't specify ``Dimensions`` . Instead, you use ``Metrics`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-dimension
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAlarm.DimensionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        '''Used only for alarms based on percentiles.

        If ``ignore`` , the alarm state does not change during periods with too few data points to be statistically significant. If ``evaluate`` or this parameter is not used, the alarm is always evaluated and possibly changes state no matter how many data points are available.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-evaluatelowsamplecountpercentile
        '''
        result = self._values.get("evaluate_low_sample_count_percentile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        '''The percentile statistic for the metric associated with the alarm. Specify a value between p0.0 and p100.

        For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both.

        For an alarm based on a math expression, you can't specify ``ExtendedStatistic`` . Instead, you use ``Metrics`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-extendedstatistic
        '''
        result = self._values.get("extended_statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ``INSUFFICIENT_DATA`` state from any other state.

        Each action is specified as an Amazon Resource Name (ARN).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-insufficientdataactions
        '''
        result = self._values.get("insufficient_data_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric associated with the alarm.

        This is required for an alarm based on a metric. For an alarm based on a math expression, you use ``Metrics`` instead and you can't specify ``MetricName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-metricname
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metrics(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAlarm.MetricDataQueryProperty, _IResolvable_a771d0ef]]]]:
        '''An array that enables you to create an alarm based on the result of a metric math expression.

        Each item in the array either retrieves a metric or performs a math expression.

        If you specify the ``Metrics`` parameter, you cannot specify ``MetricName`` , ``Dimensions`` , ``Period`` , ``Namespace`` , ``Statistic`` , ``ExtendedStatistic`` , or ``Unit`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarm-metrics
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAlarm.MetricDataQueryProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the metric associated with the alarm.

        This is required for an alarm based on a metric. For an alarm based on a math expression, you can't specify ``Namespace`` and you use ``Metrics`` instead.

        For a list of namespaces for metrics from AWS services, see `AWS Services That Publish CloudWatch Metrics. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ``OK`` state from any other state.

        Each action is specified as an Amazon Resource Name (ARN).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-okactions
        '''
        result = self._values.get("ok_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        '''The period, in seconds, over which the statistic is applied.

        This is required for an alarm based on a metric. Valid values are 10, 30, 60, and any multiple of 60.

        For an alarm based on a math expression, you can't specify ``Period`` , and instead you use the ``Metrics`` parameter.

        *Minimum:* 10

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-period
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''The statistic for the metric associated with the alarm, other than percentile. For percentile statistics, use ``ExtendedStatistic`` .

        For an alarm based on a metric, you must specify either ``Statistic`` or ``ExtendedStatistic`` but not both.

        For an alarm based on a math expression, you can't specify ``Statistic`` . Instead, you use ``Metrics`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-statistic
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value to compare with the specified statistic.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_metric_id(self) -> typing.Optional[builtins.str]:
        '''In an alarm based on an anomaly detection model, this is the ID of the ``ANOMALY_DETECTION_BAND`` function used as the threshold for the alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-dynamic-threshold
        '''
        result = self._values.get("threshold_metric_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def treat_missing_data(self) -> typing.Optional[builtins.str]:
        '''Sets how this alarm is to handle missing data points.

        Valid values are ``breaching`` , ``notBreaching`` , ``ignore`` , and ``missing`` . For more information, see `Configuring How CloudWatch Alarms Treat Missing Data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-missing-data>`_ in the *Amazon CloudWatch User Guide* .

        If you omit this parameter, the default behavior of ``missing`` is used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-treatmissingdata
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''The unit of the metric associated with the alarm.

        Specify this only if you are creating an alarm based on a single metric. Do not specify this if you are specifying a ``Metrics`` array.

        You can specify the following values: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits, Terabits, Percent, Count, Bytes/Second, Kilobytes/Second, Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second, Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second, Count/Second, or None.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-alarm.html#cfn-cloudwatch-alarms-unit
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAnomalyDetector(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector",
):
    '''A CloudFormation ``AWS::CloudWatch::AnomalyDetector``.

    The ``AWS::CloudWatch::AnomalyDetector`` type specifies an anomaly detection band for a certain metric and statistic. The band represents the expected "normal" range for the metric values. Anomaly detection bands can be used for visualization of a metric's expected values, and for alarms.

    :cloudformationResource: AWS::CloudWatch::AnomalyDetector
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        cfn_anomaly_detector = cloudwatch.CfnAnomalyDetector(self, "MyCfnAnomalyDetector",
            configuration=cloudwatch.CfnAnomalyDetector.ConfigurationProperty(
                excluded_time_ranges=[cloudwatch.CfnAnomalyDetector.RangeProperty(
                    end_time="endTime",
                    start_time="startTime"
                )],
                metric_time_zone="metricTimeZone"
            ),
            dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                name="name",
                value="value"
            )],
            metric_math_anomaly_detector=cloudwatch.CfnAnomalyDetector.MetricMathAnomalyDetectorProperty(
                metric_data_queries=[cloudwatch.CfnAnomalyDetector.MetricDataQueryProperty(
                    id="id",
        
                    # the properties below are optional
                    account_id="accountId",
                    expression="expression",
                    label="label",
                    metric_stat=cloudwatch.CfnAnomalyDetector.MetricStatProperty(
                        metric=cloudwatch.CfnAnomalyDetector.MetricProperty(
                            metric_name="metricName",
                            namespace="namespace",
        
                            # the properties below are optional
                            dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                                name="name",
                                value="value"
                            )]
                        ),
                        period=123,
                        stat="stat",
        
                        # the properties below are optional
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )]
            ),
            metric_name="metricName",
            namespace="namespace",
            single_metric_anomaly_detector=cloudwatch.CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty(
                dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                    name="name",
                    value="value"
                )],
                metric_name="metricName",
                namespace="namespace",
                stat="stat"
            ),
            stat="stat"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        configuration: typing.Optional[typing.Union[typing.Union["CfnAnomalyDetector.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAnomalyDetector.DimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        metric_math_anomaly_detector: typing.Optional[typing.Union[typing.Union["CfnAnomalyDetector.MetricMathAnomalyDetectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        single_metric_anomaly_detector: typing.Optional[typing.Union[typing.Union["CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stat: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudWatch::AnomalyDetector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration: Specifies details about how the anomaly detection model is to be trained, including time ranges to exclude when training and updating the model. The configuration can also include the time zone to use for the metric.
        :param dimensions: The dimensions of the metric associated with the anomaly detection band.
        :param metric_math_anomaly_detector: The CloudWatch metric math expression for this anomaly detector.
        :param metric_name: The name of the metric associated with the anomaly detection band.
        :param namespace: The namespace of the metric associated with the anomaly detection band.
        :param single_metric_anomaly_detector: The CloudWatch metric and statistic for this anomaly detector.
        :param stat: The statistic of the metric associated with the anomaly detection band.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f024cb919501d6256d3a9898edb1caea942ff694f6e986d25d0c28cf567a521e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAnomalyDetectorProps(
            configuration=configuration,
            dimensions=dimensions,
            metric_math_anomaly_detector=metric_math_anomaly_detector,
            metric_name=metric_name,
            namespace=namespace,
            single_metric_anomaly_detector=single_metric_anomaly_detector,
            stat=stat,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987d53e7d0f3eca9379a125bb8ac4789698bf4ffa82e6e82a44cac3a61373ae5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c23644ea90e6a967388476b9fcc0f38a5dd4e5dc169387cf389f70aa83b7d87)
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
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnAnomalyDetector.ConfigurationProperty", _IResolvable_a771d0ef]]:
        '''Specifies details about how the anomaly detection model is to be trained, including time ranges to exclude when training and updating the model.

        The configuration can also include the time zone to use for the metric.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-configuration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAnomalyDetector.ConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Optional[typing.Union["CfnAnomalyDetector.ConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b82836bf991c393dd6a785302ab87c1be4aeeac04c02fd721c4d8efe6267e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.DimensionProperty", _IResolvable_a771d0ef]]]]:
        '''The dimensions of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-dimensions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.DimensionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "dimensions"))

    @dimensions.setter
    def dimensions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.DimensionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff6c0b6eef7e662bfb15fcb659824d458e5d07caa9aeaaff38ace8dc88dedea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensions", value)

    @builtins.property
    @jsii.member(jsii_name="metricMathAnomalyDetector")
    def metric_math_anomaly_detector(
        self,
    ) -> typing.Optional[typing.Union["CfnAnomalyDetector.MetricMathAnomalyDetectorProperty", _IResolvable_a771d0ef]]:
        '''The CloudWatch metric math expression for this anomaly detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricmathanomalydetector
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAnomalyDetector.MetricMathAnomalyDetectorProperty", _IResolvable_a771d0ef]], jsii.get(self, "metricMathAnomalyDetector"))

    @metric_math_anomaly_detector.setter
    def metric_math_anomaly_detector(
        self,
        value: typing.Optional[typing.Union["CfnAnomalyDetector.MetricMathAnomalyDetectorProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66255c5cb5bc8b964fbf32e42c84dbdf66e4b6f60b2e93a3210de30770fe5a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricMathAnomalyDetector", value)

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93b2d935a49d98c94ae2c996f51a72f81b33807bfa6fa8589a38f96465fbca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-namespace
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d8cfa34753a015c76c75ab49ee06dd93a171bfa660f1a798cf6451961744cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="singleMetricAnomalyDetector")
    def single_metric_anomaly_detector(
        self,
    ) -> typing.Optional[typing.Union["CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty", _IResolvable_a771d0ef]]:
        '''The CloudWatch metric and statistic for this anomaly detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty", _IResolvable_a771d0ef]], jsii.get(self, "singleMetricAnomalyDetector"))

    @single_metric_anomaly_detector.setter
    def single_metric_anomaly_detector(
        self,
        value: typing.Optional[typing.Union["CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34244eb8e6ae656a33e3f6dc51bcd7ee170fa6a091cbcc827d3c0104c7fbb863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleMetricAnomalyDetector", value)

    @builtins.property
    @jsii.member(jsii_name="stat")
    def stat(self) -> typing.Optional[builtins.str]:
        '''The statistic of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-stat
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stat"))

    @stat.setter
    def stat(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ce6b19026996cad40bb729580f8361dd13e7ac354ab844da0904dda5695821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stat", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector.ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "excluded_time_ranges": "excludedTimeRanges",
            "metric_time_zone": "metricTimeZone",
        },
    )
    class ConfigurationProperty:
        def __init__(
            self,
            *,
            excluded_time_ranges: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAnomalyDetector.RangeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            metric_time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies details about how the anomaly detection model is to be trained, including time ranges to exclude when training and updating the model.

            The configuration can also include the time zone to use for the metric.

            :param excluded_time_ranges: Specifies an array of time ranges to exclude from use when the anomaly detection model is trained and updated. Use this to make sure that events that could cause unusual values for the metric, such as deployments, aren't used when CloudWatch creates or updates the model.
            :param metric_time_zone: The time zone to use for the metric. This is useful to enable the model to automatically account for daylight savings time changes if the metric is sensitive to such time changes. To specify a time zone, use the name of the time zone as specified in the standard tz database. For more information, see `tz database <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Tz_database>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                configuration_property = cloudwatch.CfnAnomalyDetector.ConfigurationProperty(
                    excluded_time_ranges=[cloudwatch.CfnAnomalyDetector.RangeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )],
                    metric_time_zone="metricTimeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4acfa60383b9d31293e0aeab081eb4abc3aed45c896d2145df5a328ab595b8e)
                check_type(argname="argument excluded_time_ranges", value=excluded_time_ranges, expected_type=type_hints["excluded_time_ranges"])
                check_type(argname="argument metric_time_zone", value=metric_time_zone, expected_type=type_hints["metric_time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excluded_time_ranges is not None:
                self._values["excluded_time_ranges"] = excluded_time_ranges
            if metric_time_zone is not None:
                self._values["metric_time_zone"] = metric_time_zone

        @builtins.property
        def excluded_time_ranges(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.RangeProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies an array of time ranges to exclude from use when the anomaly detection model is trained and updated.

            Use this to make sure that events that could cause unusual values for the metric, such as deployments, aren't used when CloudWatch creates or updates the model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html#cfn-cloudwatch-anomalydetector-configuration-excludedtimeranges
            '''
            result = self._values.get("excluded_time_ranges")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.RangeProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def metric_time_zone(self) -> typing.Optional[builtins.str]:
            '''The time zone to use for the metric.

            This is useful to enable the model to automatically account for daylight savings time changes if the metric is sensitive to such time changes.

            To specify a time zone, use the name of the time zone as specified in the standard tz database. For more information, see `tz database <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Tz_database>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html#cfn-cloudwatch-anomalydetector-configuration-metrictimezone
            '''
            result = self._values.get("metric_time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''A dimension is a name/value pair that is part of the identity of a metric.

            Because dimensions are part of the unique identifier for a metric, whenever you add a unique name/value pair to one of your metrics, you are creating a new variation of that metric. For example, many Amazon EC2 metrics publish ``InstanceId`` as a dimension name, and the actual instance ID as the value for that dimension.

            You can assign up to 30 dimensions to a metric.

            :param name: The name of the dimension.
            :param value: The value of the dimension. Dimension values must contain only ASCII characters and must include at least one non-whitespace character. ASCII control characters are not supported as part of dimension values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                dimension_property = cloudwatch.CfnAnomalyDetector.DimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa7841f336d62bbf0a2d6a9bffcf99f3cc531d6282d5e8a6b76624f87cc5ee1a)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the dimension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html#cfn-cloudwatch-anomalydetector-dimension-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value of the dimension.

            Dimension values must contain only ASCII characters and must include at least one non-whitespace character. ASCII control characters are not supported as part of dimension values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html#cfn-cloudwatch-anomalydetector-dimension-value
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
        jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector.MetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "account_id": "accountId",
            "expression": "expression",
            "label": "label",
            "metric_stat": "metricStat",
            "period": "period",
            "return_data": "returnData",
        },
    )
    class MetricDataQueryProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            account_id: typing.Optional[builtins.str] = None,
            expression: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[typing.Union["CfnAnomalyDetector.MetricStatProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            period: typing.Optional[jsii.Number] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''This structure is used in both ``GetMetricData`` and ``PutMetricAlarm`` .

            The supported use of this structure is different for those two operations.

            When used in ``GetMetricData`` , it indicates the metric data to return, and whether this call is just retrieving a batch set of data for one metric, or is performing a Metrics Insights query or a math expression. A single ``GetMetricData`` call can include up to 500 ``MetricDataQuery`` structures.

            When used in ``PutMetricAlarm`` , it enables you to create an alarm based on a metric math expression. Each ``MetricDataQuery`` in the array specifies either a metric to retrieve, or a math expression to be performed on retrieved metrics. A single ``PutMetricAlarm`` call can include up to 20 ``MetricDataQuery`` structures in the array. The 20 structures can include as many as 10 structures that contain a ``MetricStat`` parameter to retrieve a metric, and as many as 10 structures that contain the ``Expression`` parameter to perform a math expression. Of those ``Expression`` structures, one must have ``true`` as the value for ``ReturnData`` . The result of this expression is the value the alarm watches.

            Any expression used in a ``PutMetricAlarm`` operation must return a single time series. For more information, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            Some of the parameters of this structure also have different uses whether you are using this structure in a ``GetMetricData`` operation or a ``PutMetricAlarm`` operation. These differences are explained in the following parameter list.

            :param id: A short name used to tie this object to the results in the response. This name must be unique within a single call to ``GetMetricData`` . If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.
            :param account_id: The ID of the account where the metrics are located. If you are performing a ``GetMetricData`` operation in a monitoring account, use this to specify which account to retrieve this metric from. If you are performing a ``PutMetricAlarm`` operation, use this to specify which account contains the metric that the alarm is watching.
            :param expression: This field can contain either a Metrics Insights query, or a metric math expression to be performed on the returned data. For more information about Metrics Insights queries, see `Metrics Insights query components and syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-querylanguage>`_ in the *Amazon CloudWatch User Guide* . A math expression can use the ``Id`` of the other metrics or queries to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* . Within each MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param label: A human-readable label for this metric or expression. This is especially useful if this is an expression, so that you know what the value represents. If the metric or expression is shown in a CloudWatch dashboard widget, the label is shown. If Label is omitted, CloudWatch generates a default. You can put dynamic expressions into a label, so that it is more descriptive. For more information, see `Using Dynamic Labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ .
            :param metric_stat: The metric to be returned, along with statistics, period, and units. Use this parameter only if this object is retrieving a metric and not performing a math expression on returned data. Within one MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param period: The granularity, in seconds, of the returned data points. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` operation that includes a ``StorageResolution of 1 second`` .
            :param return_data: When used in ``GetMetricData`` , this option indicates whether to return the timestamps and raw data values of this metric. If you are performing this call just to do math expressions and do not also need the raw data returned, you can specify ``false`` . If you omit this, the default of ``true`` is used. When used in ``PutMetricAlarm`` , specify ``true`` for the one expression result to use as the alarm. For all other metrics and expressions in the same ``PutMetricAlarm`` operation, specify ``ReturnData`` as False.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_data_query_property = cloudwatch.CfnAnomalyDetector.MetricDataQueryProperty(
                    id="id",
                
                    # the properties below are optional
                    account_id="accountId",
                    expression="expression",
                    label="label",
                    metric_stat=cloudwatch.CfnAnomalyDetector.MetricStatProperty(
                        metric=cloudwatch.CfnAnomalyDetector.MetricProperty(
                            metric_name="metricName",
                            namespace="namespace",
                
                            # the properties below are optional
                            dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                                name="name",
                                value="value"
                            )]
                        ),
                        period=123,
                        stat="stat",
                
                        # the properties below are optional
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04a57c5029500d8afedb8814b1a32bf111b55f688a3e50e4d72a4a11eccb122c)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }
            if account_id is not None:
                self._values["account_id"] = account_id
            if expression is not None:
                self._values["expression"] = expression
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if period is not None:
                self._values["period"] = period
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def id(self) -> builtins.str:
            '''A short name used to tie this object to the results in the response.

            This name must be unique within a single call to ``GetMetricData`` . If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the account where the metrics are located.

            If you are performing a ``GetMetricData`` operation in a monitoring account, use this to specify which account to retrieve this metric from.

            If you are performing a ``PutMetricAlarm`` operation, use this to specify which account contains the metric that the alarm is watching.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''This field can contain either a Metrics Insights query, or a metric math expression to be performed on the returned data.

            For more information about Metrics Insights queries, see `Metrics Insights query components and syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-querylanguage>`_ in the *Amazon CloudWatch User Guide* .

            A math expression can use the ``Id`` of the other metrics or queries to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            Within each MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''A human-readable label for this metric or expression.

            This is especially useful if this is an expression, so that you know what the value represents. If the metric or expression is shown in a CloudWatch dashboard widget, the label is shown. If Label is omitted, CloudWatch generates a default.

            You can put dynamic expressions into a label, so that it is more descriptive. For more information, see `Using Dynamic Labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union["CfnAnomalyDetector.MetricStatProperty", _IResolvable_a771d0ef]]:
            '''The metric to be returned, along with statistics, period, and units.

            Use this parameter only if this object is retrieving a metric and not performing a math expression on returned data.

            Within one MetricDataQuery object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union["CfnAnomalyDetector.MetricStatProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The granularity, in seconds, of the returned data points.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` operation that includes a ``StorageResolution of 1 second`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''When used in ``GetMetricData`` , this option indicates whether to return the timestamps and raw data values of this metric.

            If you are performing this call just to do math expressions and do not also need the raw data returned, you can specify ``false`` . If you omit this, the default of ``true`` is used.

            When used in ``PutMetricAlarm`` , specify ``true`` for the one expression result to use as the alarm. For all other metrics and expressions in the same ``PutMetricAlarm`` operation, specify ``ReturnData`` as False.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricdataquery.html#cfn-cloudwatch-anomalydetector-metricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector.MetricMathAnomalyDetectorProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_data_queries": "metricDataQueries"},
    )
    class MetricMathAnomalyDetectorProperty:
        def __init__(
            self,
            *,
            metric_data_queries: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAnomalyDetector.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Indicates the CloudWatch math expression that provides the time series the anomaly detector uses as input.

            The designated math expression must return a single time series.

            :param metric_data_queries: An array of metric data query structures that enables you to create an anomaly detector based on the result of a metric math expression. Each item in ``MetricDataQueries`` gets a metric or performs a math expression. One item in ``MetricDataQueries`` is the expression that provides the time series that the anomaly detector uses as input. Designate the expression by setting ``ReturnData`` to ``true`` for this object in the array. For all other expressions and metrics, set ``ReturnData`` to ``false`` . The designated expression must return a single time series.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricmathanomalydetector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_math_anomaly_detector_property = cloudwatch.CfnAnomalyDetector.MetricMathAnomalyDetectorProperty(
                    metric_data_queries=[cloudwatch.CfnAnomalyDetector.MetricDataQueryProperty(
                        id="id",
                
                        # the properties below are optional
                        account_id="accountId",
                        expression="expression",
                        label="label",
                        metric_stat=cloudwatch.CfnAnomalyDetector.MetricStatProperty(
                            metric=cloudwatch.CfnAnomalyDetector.MetricProperty(
                                metric_name="metricName",
                                namespace="namespace",
                
                                # the properties below are optional
                                dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                                    name="name",
                                    value="value"
                                )]
                            ),
                            period=123,
                            stat="stat",
                
                            # the properties below are optional
                            unit="unit"
                        ),
                        period=123,
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c5ac0ada49a61d757fdd28f86ecd5ed2191b50ad82a1581b7f65004a8120236)
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.MetricDataQueryProperty", _IResolvable_a771d0ef]]]]:
            '''An array of metric data query structures that enables you to create an anomaly detector based on the result of a metric math expression.

            Each item in ``MetricDataQueries`` gets a metric or performs a math expression. One item in ``MetricDataQueries`` is the expression that provides the time series that the anomaly detector uses as input. Designate the expression by setting ``ReturnData`` to ``true`` for this object in the array. For all other expressions and metrics, set ``ReturnData`` to ``false`` . The designated expression must return a single time series.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricmathanomalydetector.html#cfn-cloudwatch-anomalydetector-metricmathanomalydetector-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.MetricDataQueryProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricMathAnomalyDetectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric_name": "metricName",
            "namespace": "namespace",
            "dimensions": "dimensions",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            metric_name: builtins.str,
            namespace: builtins.str,
            dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAnomalyDetector.DimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Represents a specific metric.

            :param metric_name: The name of the metric. This is a required field.
            :param namespace: The namespace of the metric.
            :param dimensions: The dimensions for the metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_property = cloudwatch.CfnAnomalyDetector.MetricProperty(
                    metric_name="metricName",
                    namespace="namespace",
                
                    # the properties below are optional
                    dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fed6436864d53ea88be2d61348a8d10ba1969f2f17f23cb912fd1f106c00dae6)
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "metric_name": metric_name,
                "namespace": namespace,
            }
            if dimensions is not None:
                self._values["dimensions"] = dimensions

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''The name of the metric.

            This is a required field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metric.html#cfn-cloudwatch-anomalydetector-metric-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def namespace(self) -> builtins.str:
            '''The namespace of the metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metric.html#cfn-cloudwatch-anomalydetector-metric-namespace
            '''
            result = self._values.get("namespace")
            assert result is not None, "Required property 'namespace' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.DimensionProperty", _IResolvable_a771d0ef]]]]:
            '''The dimensions for the metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metric.html#cfn-cloudwatch-anomalydetector-metric-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.DimensionProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector.MetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric": "metric",
            "period": "period",
            "stat": "stat",
            "unit": "unit",
        },
    )
    class MetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Union[typing.Union["CfnAnomalyDetector.MetricProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            period: jsii.Number,
            stat: builtins.str,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the metric to be returned, along with the statistics, period, and units.

            :param metric: The metric to return, including the metric name, namespace, and dimensions.
            :param period: The granularity, in seconds, of the returned data points. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second. If the ``StartTime`` parameter specifies a time stamp that is greater than 3 hours ago, you must specify the period as follows or no data points in that time range is returned: - Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute). - Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes). - Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).
            :param stat: The statistic to return. It can include any CloudWatch statistic or extended statistic.
            :param unit: When you are using a ``Put`` operation, this defines what unit you want to use when storing the metric. In a ``Get`` operation, if you omit ``Unit`` then all data that was collected with any unit is returned, along with the corresponding units that were specified when the data was reported to CloudWatch. If you specify a unit, the operation returns only data that was collected with that unit specified. If you specify a unit that does not match the data collected, the results of the operation are null. CloudWatch does not perform unit conversions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_stat_property = cloudwatch.CfnAnomalyDetector.MetricStatProperty(
                    metric=cloudwatch.CfnAnomalyDetector.MetricProperty(
                        metric_name="metricName",
                        namespace="namespace",
                
                        # the properties below are optional
                        dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    period=123,
                    stat="stat",
                
                    # the properties below are optional
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa5be944c8b2710063bbeef93199eef661b796af2de7b18252eb52a491af5601)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "metric": metric,
                "period": period,
                "stat": stat,
            }
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Union["CfnAnomalyDetector.MetricProperty", _IResolvable_a771d0ef]:
            '''The metric to return, including the metric name, namespace, and dimensions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html#cfn-cloudwatch-anomalydetector-metricstat-metric
            '''
            result = self._values.get("metric")
            assert result is not None, "Required property 'metric' is missing"
            return typing.cast(typing.Union["CfnAnomalyDetector.MetricProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def period(self) -> jsii.Number:
            '''The granularity, in seconds, of the returned data points.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second.

            If the ``StartTime`` parameter specifies a time stamp that is greater than 3 hours ago, you must specify the period as follows or no data points in that time range is returned:

            - Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute).
            - Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes).
            - Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html#cfn-cloudwatch-anomalydetector-metricstat-period
            '''
            result = self._values.get("period")
            assert result is not None, "Required property 'period' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def stat(self) -> builtins.str:
            '''The statistic to return.

            It can include any CloudWatch statistic or extended statistic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html#cfn-cloudwatch-anomalydetector-metricstat-stat
            '''
            result = self._values.get("stat")
            assert result is not None, "Required property 'stat' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''When you are using a ``Put`` operation, this defines what unit you want to use when storing the metric.

            In a ``Get`` operation, if you omit ``Unit`` then all data that was collected with any unit is returned, along with the corresponding units that were specified when the data was reported to CloudWatch. If you specify a unit, the operation returns only data that was collected with that unit specified. If you specify a unit that does not match the data collected, the results of the operation are null. CloudWatch does not perform unit conversions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-metricstat.html#cfn-cloudwatch-anomalydetector-metricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector.RangeProperty",
        jsii_struct_bases=[],
        name_mapping={"end_time": "endTime", "start_time": "startTime"},
    )
    class RangeProperty:
        def __init__(self, *, end_time: builtins.str, start_time: builtins.str) -> None:
            '''Each ``Range`` specifies one range of days or times to exclude from use for training or updating an anomaly detection model.

            :param end_time: The end time of the range to exclude. The format is ``yyyy-MM-dd'T'HH:mm:ss`` . For example, ``2019-07-01T23:59:59`` .
            :param start_time: The start time of the range to exclude. The format is ``yyyy-MM-dd'T'HH:mm:ss`` . For example, ``2019-07-01T23:59:59`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                range_property = cloudwatch.CfnAnomalyDetector.RangeProperty(
                    end_time="endTime",
                    start_time="startTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92d0fa74dbb859e57a41b981be21516fbdb5516aaf990beb72e166d885b64378)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "end_time": end_time,
                "start_time": start_time,
            }

        @builtins.property
        def end_time(self) -> builtins.str:
            '''The end time of the range to exclude.

            The format is ``yyyy-MM-dd'T'HH:mm:ss`` . For example, ``2019-07-01T23:59:59`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html#cfn-cloudwatch-anomalydetector-range-endtime
            '''
            result = self._values.get("end_time")
            assert result is not None, "Required property 'end_time' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def start_time(self) -> builtins.str:
            '''The start time of the range to exclude.

            The format is ``yyyy-MM-dd'T'HH:mm:ss`` . For example, ``2019-07-01T23:59:59`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html#cfn-cloudwatch-anomalydetector-range-starttime
            '''
            result = self._values.get("start_time")
            assert result is not None, "Required property 'start_time' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
            "stat": "stat",
        },
    )
    class SingleMetricAnomalyDetectorProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAnomalyDetector.DimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
            stat: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Designates the CloudWatch metric and statistic that provides the time series the anomaly detector uses as input.

            :param dimensions: The metric dimensions to create the anomaly detection model for.
            :param metric_name: The name of the metric to create the anomaly detection model for.
            :param namespace: The namespace of the metric to create the anomaly detection model for.
            :param stat: The statistic to use for the metric and anomaly detection model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                single_metric_anomaly_detector_property = cloudwatch.CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty(
                    dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace",
                    stat="stat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71d42d63a3c5e06c19361c11897efe4729859ac06e62c32a74e71ec521d25a83)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace
            if stat is not None:
                self._values["stat"] = stat

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.DimensionProperty", _IResolvable_a771d0ef]]]]:
            '''The metric dimensions to create the anomaly detection model for.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAnomalyDetector.DimensionProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric to create the anomaly detection model for.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric to create the anomaly detection model for.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to use for the metric and anomaly detection model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-singlemetricanomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingleMetricAnomalyDetectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CfnAnomalyDetectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "dimensions": "dimensions",
        "metric_math_anomaly_detector": "metricMathAnomalyDetector",
        "metric_name": "metricName",
        "namespace": "namespace",
        "single_metric_anomaly_detector": "singleMetricAnomalyDetector",
        "stat": "stat",
    },
)
class CfnAnomalyDetectorProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAnomalyDetector.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        metric_math_anomaly_detector: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.MetricMathAnomalyDetectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        single_metric_anomaly_detector: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stat: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAnomalyDetector``.

        :param configuration: Specifies details about how the anomaly detection model is to be trained, including time ranges to exclude when training and updating the model. The configuration can also include the time zone to use for the metric.
        :param dimensions: The dimensions of the metric associated with the anomaly detection band.
        :param metric_math_anomaly_detector: The CloudWatch metric math expression for this anomaly detector.
        :param metric_name: The name of the metric associated with the anomaly detection band.
        :param namespace: The namespace of the metric associated with the anomaly detection band.
        :param single_metric_anomaly_detector: The CloudWatch metric and statistic for this anomaly detector.
        :param stat: The statistic of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            cfn_anomaly_detector_props = cloudwatch.CfnAnomalyDetectorProps(
                configuration=cloudwatch.CfnAnomalyDetector.ConfigurationProperty(
                    excluded_time_ranges=[cloudwatch.CfnAnomalyDetector.RangeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )],
                    metric_time_zone="metricTimeZone"
                ),
                dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                    name="name",
                    value="value"
                )],
                metric_math_anomaly_detector=cloudwatch.CfnAnomalyDetector.MetricMathAnomalyDetectorProperty(
                    metric_data_queries=[cloudwatch.CfnAnomalyDetector.MetricDataQueryProperty(
                        id="id",
            
                        # the properties below are optional
                        account_id="accountId",
                        expression="expression",
                        label="label",
                        metric_stat=cloudwatch.CfnAnomalyDetector.MetricStatProperty(
                            metric=cloudwatch.CfnAnomalyDetector.MetricProperty(
                                metric_name="metricName",
                                namespace="namespace",
            
                                # the properties below are optional
                                dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                                    name="name",
                                    value="value"
                                )]
                            ),
                            period=123,
                            stat="stat",
            
                            # the properties below are optional
                            unit="unit"
                        ),
                        period=123,
                        return_data=False
                    )]
                ),
                metric_name="metricName",
                namespace="namespace",
                single_metric_anomaly_detector=cloudwatch.CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty(
                    dimensions=[cloudwatch.CfnAnomalyDetector.DimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace",
                    stat="stat"
                ),
                stat="stat"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f423aec7b474b2405381de97cce1ca5c2a8e1b7acfeac128a7890dbee3f7bbd)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument metric_math_anomaly_detector", value=metric_math_anomaly_detector, expected_type=type_hints["metric_math_anomaly_detector"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument single_metric_anomaly_detector", value=single_metric_anomaly_detector, expected_type=type_hints["single_metric_anomaly_detector"])
            check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if metric_math_anomaly_detector is not None:
            self._values["metric_math_anomaly_detector"] = metric_math_anomaly_detector
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if namespace is not None:
            self._values["namespace"] = namespace
        if single_metric_anomaly_detector is not None:
            self._values["single_metric_anomaly_detector"] = single_metric_anomaly_detector
        if stat is not None:
            self._values["stat"] = stat

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnAnomalyDetector.ConfigurationProperty, _IResolvable_a771d0ef]]:
        '''Specifies details about how the anomaly detection model is to be trained, including time ranges to exclude when training and updating the model.

        The configuration can also include the time zone to use for the metric.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[CfnAnomalyDetector.ConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAnomalyDetector.DimensionProperty, _IResolvable_a771d0ef]]]]:
        '''The dimensions of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-dimensions
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAnomalyDetector.DimensionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def metric_math_anomaly_detector(
        self,
    ) -> typing.Optional[typing.Union[CfnAnomalyDetector.MetricMathAnomalyDetectorProperty, _IResolvable_a771d0ef]]:
        '''The CloudWatch metric math expression for this anomaly detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricmathanomalydetector
        '''
        result = self._values.get("metric_math_anomaly_detector")
        return typing.cast(typing.Optional[typing.Union[CfnAnomalyDetector.MetricMathAnomalyDetectorProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricname
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_metric_anomaly_detector(
        self,
    ) -> typing.Optional[typing.Union[CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty, _IResolvable_a771d0ef]]:
        '''The CloudWatch metric and statistic for this anomaly detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-singlemetricanomalydetector
        '''
        result = self._values.get("single_metric_anomaly_detector")
        return typing.cast(typing.Optional[typing.Union[CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def stat(self) -> typing.Optional[builtins.str]:
        '''The statistic of the metric associated with the anomaly detection band.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-stat
        '''
        result = self._values.get("stat")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnomalyDetectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnCompositeAlarm(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.CfnCompositeAlarm",
):
    '''A CloudFormation ``AWS::CloudWatch::CompositeAlarm``.

    The ``AWS::CloudWatch::CompositeAlarm`` type creates or updates a composite alarm. When you create a composite alarm, you specify a rule expression for the alarm that takes into account the alarm states of other alarms that you have created. The composite alarm goes into ALARM state only if all conditions of the rule are met.

    The alarms specified in a composite alarm's rule expression can include metric alarms and other composite alarms.

    Using composite alarms can reduce alarm noise. You can create multiple metric alarms, and also create a composite alarm and set up alerts only for the composite alarm. For example, you could create a composite alarm that goes into ALARM state only when more than one of the underlying metric alarms are in ALARM state.

    Currently, the only alarm actions that can be taken by composite alarms are notifying SNS topics.

    When this operation creates an alarm, the alarm state is immediately set to INSUFFICIENT_DATA. The alarm is then evaluated and its state is set appropriately. Any actions associated with the new state are then executed. For a composite alarm, this initial time after creation is the only time that the alarm can be in INSUFFICIENT_DATA state.

    When you update an existing alarm, its state is left unchanged, but the update completely overwrites the previous configuration of the alarm.

    :cloudformationResource: AWS::CloudWatch::CompositeAlarm
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        cfn_composite_alarm = cloudwatch.CfnCompositeAlarm(self, "MyCfnCompositeAlarm",
            alarm_rule="alarmRule",
        
            # the properties below are optional
            actions_enabled=False,
            actions_suppressor="actionsSuppressor",
            actions_suppressor_extension_period=123,
            actions_suppressor_wait_period=123,
            alarm_actions=["alarmActions"],
            alarm_description="alarmDescription",
            alarm_name="alarmName",
            insufficient_data_actions=["insufficientDataActions"],
            ok_actions=["okActions"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        alarm_rule: builtins.str,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        actions_suppressor: typing.Optional[builtins.str] = None,
        actions_suppressor_extension_period: typing.Optional[jsii.Number] = None,
        actions_suppressor_wait_period: typing.Optional[jsii.Number] = None,
        alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::CloudWatch::CompositeAlarm``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param alarm_rule: An expression that specifies which other alarms are to be evaluated to determine this composite alarm's state. For each alarm that you reference, you designate a function that specifies whether that alarm needs to be in ALARM state, OK state, or INSUFFICIENT_DATA state. You can use operators (AND, OR and NOT) to combine multiple functions in a single expression. You can use parenthesis to logically group the functions in your expression. You can use either alarm names or ARNs to reference the other alarms that are to be evaluated. Functions can include the following: - ALARM("alarm-name or alarm-ARN") is TRUE if the named alarm is in ALARM state. - OK("alarm-name or alarm-ARN") is TRUE if the named alarm is in OK state. - INSUFFICIENT_DATA("alarm-name or alarm-ARN") is TRUE if the named alarm is in INSUFFICIENT_DATA state. - TRUE always evaluates to TRUE. - FALSE always evaluates to FALSE. TRUE and FALSE are useful for testing a complex AlarmRule structure, and for testing your alarm actions. For more information about ``AlarmRule`` syntax, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param actions_enabled: Indicates whether actions should be executed during any changes to the alarm state of the composite alarm. The default is TRUE.
        :param actions_suppressor: Actions will be suppressed if the suppressor alarm is in the ``ALARM`` state. ``ActionsSuppressor`` can be an AlarmName or an Amazon Resource Name (ARN) from an existing alarm.
        :param actions_suppressor_extension_period: The maximum time in seconds that the composite alarm waits after suppressor alarm goes out of the ``ALARM`` state. After this time, the composite alarm performs its actions. .. epigraph:: ``ExtensionPeriod`` is required only when ``ActionsSuppressor`` is specified.
        :param actions_suppressor_wait_period: The maximum time in seconds that the composite alarm waits for the suppressor alarm to go into the ``ALARM`` state. After this time, the composite alarm performs its actions. .. epigraph:: ``WaitPeriod`` is required only when ``ActionsSuppressor`` is specified.
        :param alarm_actions: The actions to execute when this alarm transitions to the ALARM state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param alarm_description: The description for the composite alarm.
        :param alarm_name: The name for the composite alarm. This name must be unique within your AWS account.
        :param insufficient_data_actions: The actions to execute when this alarm transitions to the INSUFFICIENT_DATA state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param ok_actions: The actions to execute when this alarm transitions to the OK state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9593e237fc8c8aea557e2ed8d0a67cdd3a400906a67897616b93db9d941e82bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCompositeAlarmProps(
            alarm_rule=alarm_rule,
            actions_enabled=actions_enabled,
            actions_suppressor=actions_suppressor,
            actions_suppressor_extension_period=actions_suppressor_extension_period,
            actions_suppressor_wait_period=actions_suppressor_wait_period,
            alarm_actions=alarm_actions,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            insufficient_data_actions=insufficient_data_actions,
            ok_actions=ok_actions,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df9cb16b9c43c51c658df2bb6416d1f00738d70d5237937ed3d5fc5c8b1104e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d46321bca7536499159d49ec75b970f11874ca9ac3bfe6a3ac2edece4a72c6e)
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
        '''The ARN of the composite alarm, such as ``arn:aws:cloudwatch:us-west-2:123456789012:alarm/CompositeAlarmName`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="alarmRule")
    def alarm_rule(self) -> builtins.str:
        '''An expression that specifies which other alarms are to be evaluated to determine this composite alarm's state.

        For each alarm that you reference, you designate a function that specifies whether that alarm needs to be in ALARM state, OK state, or INSUFFICIENT_DATA state. You can use operators (AND, OR and NOT) to combine multiple functions in a single expression. You can use parenthesis to logically group the functions in your expression.

        You can use either alarm names or ARNs to reference the other alarms that are to be evaluated.

        Functions can include the following:

        - ALARM("alarm-name or alarm-ARN") is TRUE if the named alarm is in ALARM state.
        - OK("alarm-name or alarm-ARN") is TRUE if the named alarm is in OK state.
        - INSUFFICIENT_DATA("alarm-name or alarm-ARN") is TRUE if the named alarm is in INSUFFICIENT_DATA state.
        - TRUE always evaluates to TRUE.
        - FALSE always evaluates to FALSE.

        TRUE and FALSE are useful for testing a complex AlarmRule structure, and for testing your alarm actions.

        For more information about ``AlarmRule`` syntax, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmrule
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmRule"))

    @alarm_rule.setter
    def alarm_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c488f3c4f855735f99b6f5828b0e1601bb238699c7caf144ea2c88f34bce129f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmRule", value)

    @builtins.property
    @jsii.member(jsii_name="actionsEnabled")
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether actions should be executed during any changes to the alarm state of the composite alarm.

        The default is TRUE.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionsenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "actionsEnabled"))

    @actions_enabled.setter
    def actions_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91abbd9fb2785e34daa08bbc507f1ae105cb931caf39a5c9e1510c57bdcd971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="actionsSuppressor")
    def actions_suppressor(self) -> typing.Optional[builtins.str]:
        '''Actions will be suppressed if the suppressor alarm is in the ``ALARM`` state.

        ``ActionsSuppressor`` can be an AlarmName or an Amazon Resource Name (ARN) from an existing alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressor
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionsSuppressor"))

    @actions_suppressor.setter
    def actions_suppressor(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c34c6e65a8749e64e7322e1658bbec579a139c397e83765a929eb635d00760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionsSuppressor", value)

    @builtins.property
    @jsii.member(jsii_name="actionsSuppressorExtensionPeriod")
    def actions_suppressor_extension_period(self) -> typing.Optional[jsii.Number]:
        '''The maximum time in seconds that the composite alarm waits after suppressor alarm goes out of the ``ALARM`` state.

        After this time, the composite alarm performs its actions.
        .. epigraph::

           ``ExtensionPeriod`` is required only when ``ActionsSuppressor`` is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressorextensionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "actionsSuppressorExtensionPeriod"))

    @actions_suppressor_extension_period.setter
    def actions_suppressor_extension_period(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb1d60d67f1f40d6f106b3cf899228574ad6c5317747cbd221bbf5aae1d62d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionsSuppressorExtensionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="actionsSuppressorWaitPeriod")
    def actions_suppressor_wait_period(self) -> typing.Optional[jsii.Number]:
        '''The maximum time in seconds that the composite alarm waits for the suppressor alarm to go into the ``ALARM`` state.

        After this time, the composite alarm performs its actions.
        .. epigraph::

           ``WaitPeriod`` is required only when ``ActionsSuppressor`` is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressorwaitperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "actionsSuppressorWaitPeriod"))

    @actions_suppressor_wait_period.setter
    def actions_suppressor_wait_period(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dfabf3a249e61172f0e642fb4f6acd9fd7b89deb648e6086a57fc7aa0144da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionsSuppressorWaitPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="alarmActions")
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ALARM state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmactions
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "alarmActions"))

    @alarm_actions.setter
    def alarm_actions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426a54d2120ab6779d268b159493239e90d38974834c5da45f273e8f547274df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmActions", value)

    @builtins.property
    @jsii.member(jsii_name="alarmDescription")
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description for the composite alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmDescription"))

    @alarm_description.setter
    def alarm_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe3c49a91ca15cc602dcb47256b2ed7b28b1b905f6d30e505b11f03a5044250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmDescription", value)

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The name for the composite alarm.

        This name must be unique within your AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d604bf958b97f677f4c77aaee0aa53c7f04ce854450a7024295430d6428ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value)

    @builtins.property
    @jsii.member(jsii_name="insufficientDataActions")
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the INSUFFICIENT_DATA state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-insufficientdataactions
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "insufficientDataActions"))

    @insufficient_data_actions.setter
    def insufficient_data_actions(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060864e2b0279f28410f46c4099d8cda6f219fbc42363143047bcb45b8b3d3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insufficientDataActions", value)

    @builtins.property
    @jsii.member(jsii_name="okActions")
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the OK state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-okactions
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "okActions"))

    @ok_actions.setter
    def ok_actions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe83217e9a362db90e0b6374888438a6b0fdcf1a12b0c142e00f8733ec2dfb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "okActions", value)


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CfnCompositeAlarmProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_rule": "alarmRule",
        "actions_enabled": "actionsEnabled",
        "actions_suppressor": "actionsSuppressor",
        "actions_suppressor_extension_period": "actionsSuppressorExtensionPeriod",
        "actions_suppressor_wait_period": "actionsSuppressorWaitPeriod",
        "alarm_actions": "alarmActions",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "insufficient_data_actions": "insufficientDataActions",
        "ok_actions": "okActions",
    },
)
class CfnCompositeAlarmProps:
    def __init__(
        self,
        *,
        alarm_rule: builtins.str,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        actions_suppressor: typing.Optional[builtins.str] = None,
        actions_suppressor_extension_period: typing.Optional[jsii.Number] = None,
        actions_suppressor_wait_period: typing.Optional[jsii.Number] = None,
        alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCompositeAlarm``.

        :param alarm_rule: An expression that specifies which other alarms are to be evaluated to determine this composite alarm's state. For each alarm that you reference, you designate a function that specifies whether that alarm needs to be in ALARM state, OK state, or INSUFFICIENT_DATA state. You can use operators (AND, OR and NOT) to combine multiple functions in a single expression. You can use parenthesis to logically group the functions in your expression. You can use either alarm names or ARNs to reference the other alarms that are to be evaluated. Functions can include the following: - ALARM("alarm-name or alarm-ARN") is TRUE if the named alarm is in ALARM state. - OK("alarm-name or alarm-ARN") is TRUE if the named alarm is in OK state. - INSUFFICIENT_DATA("alarm-name or alarm-ARN") is TRUE if the named alarm is in INSUFFICIENT_DATA state. - TRUE always evaluates to TRUE. - FALSE always evaluates to FALSE. TRUE and FALSE are useful for testing a complex AlarmRule structure, and for testing your alarm actions. For more information about ``AlarmRule`` syntax, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param actions_enabled: Indicates whether actions should be executed during any changes to the alarm state of the composite alarm. The default is TRUE.
        :param actions_suppressor: Actions will be suppressed if the suppressor alarm is in the ``ALARM`` state. ``ActionsSuppressor`` can be an AlarmName or an Amazon Resource Name (ARN) from an existing alarm.
        :param actions_suppressor_extension_period: The maximum time in seconds that the composite alarm waits after suppressor alarm goes out of the ``ALARM`` state. After this time, the composite alarm performs its actions. .. epigraph:: ``ExtensionPeriod`` is required only when ``ActionsSuppressor`` is specified.
        :param actions_suppressor_wait_period: The maximum time in seconds that the composite alarm waits for the suppressor alarm to go into the ``ALARM`` state. After this time, the composite alarm performs its actions. .. epigraph:: ``WaitPeriod`` is required only when ``ActionsSuppressor`` is specified.
        :param alarm_actions: The actions to execute when this alarm transitions to the ALARM state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param alarm_description: The description for the composite alarm.
        :param alarm_name: The name for the composite alarm. This name must be unique within your AWS account.
        :param insufficient_data_actions: The actions to execute when this alarm transitions to the INSUFFICIENT_DATA state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .
        :param ok_actions: The actions to execute when this alarm transitions to the OK state from any other state. Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            cfn_composite_alarm_props = cloudwatch.CfnCompositeAlarmProps(
                alarm_rule="alarmRule",
            
                # the properties below are optional
                actions_enabled=False,
                actions_suppressor="actionsSuppressor",
                actions_suppressor_extension_period=123,
                actions_suppressor_wait_period=123,
                alarm_actions=["alarmActions"],
                alarm_description="alarmDescription",
                alarm_name="alarmName",
                insufficient_data_actions=["insufficientDataActions"],
                ok_actions=["okActions"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bc2ae85019462d24df8e7586c59b5ed9ac963e291177c526f577f43c14a886)
            check_type(argname="argument alarm_rule", value=alarm_rule, expected_type=type_hints["alarm_rule"])
            check_type(argname="argument actions_enabled", value=actions_enabled, expected_type=type_hints["actions_enabled"])
            check_type(argname="argument actions_suppressor", value=actions_suppressor, expected_type=type_hints["actions_suppressor"])
            check_type(argname="argument actions_suppressor_extension_period", value=actions_suppressor_extension_period, expected_type=type_hints["actions_suppressor_extension_period"])
            check_type(argname="argument actions_suppressor_wait_period", value=actions_suppressor_wait_period, expected_type=type_hints["actions_suppressor_wait_period"])
            check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument insufficient_data_actions", value=insufficient_data_actions, expected_type=type_hints["insufficient_data_actions"])
            check_type(argname="argument ok_actions", value=ok_actions, expected_type=type_hints["ok_actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_rule": alarm_rule,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if actions_suppressor is not None:
            self._values["actions_suppressor"] = actions_suppressor
        if actions_suppressor_extension_period is not None:
            self._values["actions_suppressor_extension_period"] = actions_suppressor_extension_period
        if actions_suppressor_wait_period is not None:
            self._values["actions_suppressor_wait_period"] = actions_suppressor_wait_period
        if alarm_actions is not None:
            self._values["alarm_actions"] = alarm_actions
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if insufficient_data_actions is not None:
            self._values["insufficient_data_actions"] = insufficient_data_actions
        if ok_actions is not None:
            self._values["ok_actions"] = ok_actions

    @builtins.property
    def alarm_rule(self) -> builtins.str:
        '''An expression that specifies which other alarms are to be evaluated to determine this composite alarm's state.

        For each alarm that you reference, you designate a function that specifies whether that alarm needs to be in ALARM state, OK state, or INSUFFICIENT_DATA state. You can use operators (AND, OR and NOT) to combine multiple functions in a single expression. You can use parenthesis to logically group the functions in your expression.

        You can use either alarm names or ARNs to reference the other alarms that are to be evaluated.

        Functions can include the following:

        - ALARM("alarm-name or alarm-ARN") is TRUE if the named alarm is in ALARM state.
        - OK("alarm-name or alarm-ARN") is TRUE if the named alarm is in OK state.
        - INSUFFICIENT_DATA("alarm-name or alarm-ARN") is TRUE if the named alarm is in INSUFFICIENT_DATA state.
        - TRUE always evaluates to TRUE.
        - FALSE always evaluates to FALSE.

        TRUE and FALSE are useful for testing a complex AlarmRule structure, and for testing your alarm actions.

        For more information about ``AlarmRule`` syntax, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmrule
        '''
        result = self._values.get("alarm_rule")
        assert result is not None, "Required property 'alarm_rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether actions should be executed during any changes to the alarm state of the composite alarm.

        The default is TRUE.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionsenabled
        '''
        result = self._values.get("actions_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def actions_suppressor(self) -> typing.Optional[builtins.str]:
        '''Actions will be suppressed if the suppressor alarm is in the ``ALARM`` state.

        ``ActionsSuppressor`` can be an AlarmName or an Amazon Resource Name (ARN) from an existing alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressor
        '''
        result = self._values.get("actions_suppressor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def actions_suppressor_extension_period(self) -> typing.Optional[jsii.Number]:
        '''The maximum time in seconds that the composite alarm waits after suppressor alarm goes out of the ``ALARM`` state.

        After this time, the composite alarm performs its actions.
        .. epigraph::

           ``ExtensionPeriod`` is required only when ``ActionsSuppressor`` is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressorextensionperiod
        '''
        result = self._values.get("actions_suppressor_extension_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def actions_suppressor_wait_period(self) -> typing.Optional[jsii.Number]:
        '''The maximum time in seconds that the composite alarm waits for the suppressor alarm to go into the ``ALARM`` state.

        After this time, the composite alarm performs its actions.
        .. epigraph::

           ``WaitPeriod`` is required only when ``ActionsSuppressor`` is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionssuppressorwaitperiod
        '''
        result = self._values.get("actions_suppressor_wait_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the ALARM state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmactions
        '''
        result = self._values.get("alarm_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description for the composite alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmdescription
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The name for the composite alarm.

        This name must be unique within your AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmname
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the INSUFFICIENT_DATA state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-insufficientdataactions
        '''
        result = self._values.get("insufficient_data_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The actions to execute when this alarm transitions to the OK state from any other state.

        Each action is specified as an Amazon Resource Name (ARN). For more information about creating alarms and the actions that you can specify, see `PutCompositeAlarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html>`_ in the *Amazon CloudWatch API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-okactions
        '''
        result = self._values.get("ok_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCompositeAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDashboard(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.CfnDashboard",
):
    '''A CloudFormation ``AWS::CloudWatch::Dashboard``.

    The ``AWS::CloudWatch::Dashboard`` resource specifies an Amazon CloudWatch dashboard. A dashboard is a customizable home page in the CloudWatch console that you can use to monitor your AWS resources in a single view.

    All dashboards in your account are global, not region-specific.

    :cloudformationResource: AWS::CloudWatch::Dashboard
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        cfn_dashboard = cloudwatch.CfnDashboard(self, "MyCfnDashboard",
            dashboard_body="dashboardBody",
        
            # the properties below are optional
            dashboard_name="dashboardName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        dashboard_body: builtins.str,
        dashboard_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudWatch::Dashboard``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dashboard_body: The detailed information about the dashboard in JSON format, including the widgets to include and their location on the dashboard. This parameter is required. For more information about the syntax, see `Dashboard Body Structure and Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html>`_ .
        :param dashboard_name: The name of the dashboard. The name must be between 1 and 255 characters. If you do not specify a name, one will be generated automatically.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc4d480bcab6b22924ff9d4b2d8e53e79bca7d4ebd0be23a9f9fe88c9524ed1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDashboardProps(
            dashboard_body=dashboard_body, dashboard_name=dashboard_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdb1cce6bcd184a48fec81f6d63f4dbe7a303f77ef77adcdf293751fca34fa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05debdae58a97f84253e7df4b73dc5828234ca4a93ca04d832dc47d91a526df2)
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
    @jsii.member(jsii_name="dashboardBody")
    def dashboard_body(self) -> builtins.str:
        '''The detailed information about the dashboard in JSON format, including the widgets to include and their location on the dashboard.

        This parameter is required.

        For more information about the syntax, see `Dashboard Body Structure and Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardbody
        '''
        return typing.cast(builtins.str, jsii.get(self, "dashboardBody"))

    @dashboard_body.setter
    def dashboard_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34fcdaf86787ba9b030f60afaece32f761411bb3697b550ded89bd1ed5fb5cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardBody", value)

    @builtins.property
    @jsii.member(jsii_name="dashboardName")
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dashboard.

        The name must be between 1 and 255 characters. If you do not specify a name, one will be generated automatically.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dashboardName"))

    @dashboard_name.setter
    def dashboard_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88031f24013086d04bf22f7f72208ebbf9078466d64b6ca01f1ba923469f8fbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CfnDashboardProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_body": "dashboardBody",
        "dashboard_name": "dashboardName",
    },
)
class CfnDashboardProps:
    def __init__(
        self,
        *,
        dashboard_body: builtins.str,
        dashboard_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDashboard``.

        :param dashboard_body: The detailed information about the dashboard in JSON format, including the widgets to include and their location on the dashboard. This parameter is required. For more information about the syntax, see `Dashboard Body Structure and Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html>`_ .
        :param dashboard_name: The name of the dashboard. The name must be between 1 and 255 characters. If you do not specify a name, one will be generated automatically.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            cfn_dashboard_props = cloudwatch.CfnDashboardProps(
                dashboard_body="dashboardBody",
            
                # the properties below are optional
                dashboard_name="dashboardName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52a1aa45c6d954169fb9b99d30879c3a2b5c4e561c05f6a2c83ec6828da5349)
            check_type(argname="argument dashboard_body", value=dashboard_body, expected_type=type_hints["dashboard_body"])
            check_type(argname="argument dashboard_name", value=dashboard_name, expected_type=type_hints["dashboard_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dashboard_body": dashboard_body,
        }
        if dashboard_name is not None:
            self._values["dashboard_name"] = dashboard_name

    @builtins.property
    def dashboard_body(self) -> builtins.str:
        '''The detailed information about the dashboard in JSON format, including the widgets to include and their location on the dashboard.

        This parameter is required.

        For more information about the syntax, see `Dashboard Body Structure and Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardbody
        '''
        result = self._values.get("dashboard_body")
        assert result is not None, "Required property 'dashboard_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dashboard.

        The name must be between 1 and 255 characters. If you do not specify a name, one will be generated automatically.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardname
        '''
        result = self._values.get("dashboard_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDashboardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnInsightRule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.CfnInsightRule",
):
    '''A CloudFormation ``AWS::CloudWatch::InsightRule``.

    Creates or updates a Contributor Insights rule. Rules evaluate log events in a CloudWatch Logs log group, enabling you to find contributor data for the log events in that log group. For more information, see `Using Contributor Insights to Analyze High-Cardinality Data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights.html>`_ in the *Amazon CloudWatch User Guide* .

    :cloudformationResource: AWS::CloudWatch::InsightRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        cfn_insight_rule = cloudwatch.CfnInsightRule(self, "MyCfnInsightRule",
            rule_body="ruleBody",
            rule_name="ruleName",
            rule_state="ruleState",
        
            # the properties below are optional
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
        rule_body: builtins.str,
        rule_name: builtins.str,
        rule_state: builtins.str,
        tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CloudWatch::InsightRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rule_body: The definition of the rule, as a JSON object. For details about the syntax, see `Contributor Insights Rule Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-RuleSyntax.html>`_ in the *Amazon CloudWatch User Guide* .
        :param rule_name: The name of the rule.
        :param rule_state: The current state of the rule. Valid values are ``ENABLED`` and ``DISABLED`` .
        :param tags: A list of key-value pairs to associate with the Contributor Insights rule. You can associate as many as 50 tags with a rule. Tags can help you organize and categorize your resources. For more information, see `Tagging Your Amazon CloudWatch Resources <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Tagging.html>`_ . To be able to associate tags with a rule, you must have the ``cloudwatch:TagResource`` permission in addition to the ``cloudwatch:PutInsightRule`` permission.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8bcffc97c5a49aa76301f74824b77e2ca3f134e08695fd0ef54dfc637057e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInsightRuleProps(
            rule_body=rule_body, rule_name=rule_name, rule_state=rule_state, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734b7d1d39df442a0777926343f5dd49517d73b80aa92052efcd09b0fb278fe1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35996c89b98e7300859e8dd8866901f448446c1e97d53466d6a366c8bc0ea4e1)
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
        '''The ARN of the Contributor Insights rule, such as ``arn:aws:cloudwatch:us-west-2:123456789012:insight-rule/MyInsightRuleName`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleName")
    def attr_rule_name(self) -> builtins.str:
        '''The name of the Contributor Insights rule.

        :cloudformationAttribute: RuleName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs to associate with the Contributor Insights rule.

        You can associate as many as 50 tags with a rule.

        Tags can help you organize and categorize your resources. For more information, see `Tagging Your Amazon CloudWatch Resources <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Tagging.html>`_ .

        To be able to associate tags with a rule, you must have the ``cloudwatch:TagResource`` permission in addition to the ``cloudwatch:PutInsightRule`` permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="ruleBody")
    def rule_body(self) -> builtins.str:
        '''The definition of the rule, as a JSON object.

        For details about the syntax, see `Contributor Insights Rule Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-RuleSyntax.html>`_ in the *Amazon CloudWatch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulebody
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleBody"))

    @rule_body.setter
    def rule_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65921830dd71708f791d2baf286e6359d33d18c175d15967919249ca2d71c76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleBody", value)

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        '''The name of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulename
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007fc5499a09ea1aeb3cacc0893304e7babb25b9f81e26d48470ace948751f3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value)

    @builtins.property
    @jsii.member(jsii_name="ruleState")
    def rule_state(self) -> builtins.str:
        '''The current state of the rule.

        Valid values are ``ENABLED`` and ``DISABLED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulestate
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleState"))

    @rule_state.setter
    def rule_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4dbe03b10e790be682fe7c06dce4a803f172771047b706f0fbcab023c794626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleState", value)


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CfnInsightRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "rule_body": "ruleBody",
        "rule_name": "ruleName",
        "rule_state": "ruleState",
        "tags": "tags",
    },
)
class CfnInsightRuleProps:
    def __init__(
        self,
        *,
        rule_body: builtins.str,
        rule_name: builtins.str,
        rule_state: builtins.str,
        tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnInsightRule``.

        :param rule_body: The definition of the rule, as a JSON object. For details about the syntax, see `Contributor Insights Rule Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-RuleSyntax.html>`_ in the *Amazon CloudWatch User Guide* .
        :param rule_name: The name of the rule.
        :param rule_state: The current state of the rule. Valid values are ``ENABLED`` and ``DISABLED`` .
        :param tags: A list of key-value pairs to associate with the Contributor Insights rule. You can associate as many as 50 tags with a rule. Tags can help you organize and categorize your resources. For more information, see `Tagging Your Amazon CloudWatch Resources <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Tagging.html>`_ . To be able to associate tags with a rule, you must have the ``cloudwatch:TagResource`` permission in addition to the ``cloudwatch:PutInsightRule`` permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            cfn_insight_rule_props = cloudwatch.CfnInsightRuleProps(
                rule_body="ruleBody",
                rule_name="ruleName",
                rule_state="ruleState",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b811b83cfa7e4436a429d27651bebd9f33590f3935874b4d33427cf6e402b7)
            check_type(argname="argument rule_body", value=rule_body, expected_type=type_hints["rule_body"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument rule_state", value=rule_state, expected_type=type_hints["rule_state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_body": rule_body,
            "rule_name": rule_name,
            "rule_state": rule_state,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule_body(self) -> builtins.str:
        '''The definition of the rule, as a JSON object.

        For details about the syntax, see `Contributor Insights Rule Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-RuleSyntax.html>`_ in the *Amazon CloudWatch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulebody
        '''
        result = self._values.get("rule_body")
        assert result is not None, "Required property 'rule_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''The name of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulename
        '''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_state(self) -> builtins.str:
        '''The current state of the rule.

        Valid values are ``ENABLED`` and ``DISABLED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulestate
        '''
        result = self._values.get("rule_state")
        assert result is not None, "Required property 'rule_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''A list of key-value pairs to associate with the Contributor Insights rule.

        You can associate as many as 50 tags with a rule.

        Tags can help you organize and categorize your resources. For more information, see `Tagging Your Amazon CloudWatch Resources <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Tagging.html>`_ .

        To be able to associate tags with a rule, you must have the ``cloudwatch:TagResource`` permission in addition to the ``cloudwatch:PutInsightRule`` permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInsightRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnMetricStream(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.CfnMetricStream",
):
    '''A CloudFormation ``AWS::CloudWatch::MetricStream``.

    Creates or updates a metric stream. Metrics streams can automatically stream CloudWatch metrics to AWS destinations including Amazon S3 and to many third-party solutions. For more information, see `Metric streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Metric-Streams.html>`_ .

    To create a metric stream, you must be logged on to an account that has the ``iam:PassRole`` permission and either the *CloudWatchFullAccess* policy or the ``cloudwatch:PutMetricStream`` permission.

    When you create or update a metric stream, you choose one of the following:

    - Stream metrics from all metric namespaces in the account.
    - Stream metrics from all metric namespaces in the account, except for the namespaces that you list in ``ExcludeFilters`` .
    - Stream metrics from only the metric namespaces that you list in ``IncludeFilters`` .

    When you create a metric stream, the stream is created in the ``running`` state. If you update an existing metric stream, the state does not change.

    If you create a metric stream in an account that has been set up as a monitoring account in CloudWatch cross-account observability, you can choose whether to include metrics from linked source accounts in the metric stream.

    :cloudformationResource: AWS::CloudWatch::MetricStream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        cfn_metric_stream = cloudwatch.CfnMetricStream(self, "MyCfnMetricStream",
            firehose_arn="firehoseArn",
            output_format="outputFormat",
            role_arn="roleArn",
        
            # the properties below are optional
            exclude_filters=[cloudwatch.CfnMetricStream.MetricStreamFilterProperty(
                namespace="namespace",
        
                # the properties below are optional
                metric_names=["metricNames"]
            )],
            include_filters=[cloudwatch.CfnMetricStream.MetricStreamFilterProperty(
                namespace="namespace",
        
                # the properties below are optional
                metric_names=["metricNames"]
            )],
            include_linked_accounts_metrics=False,
            name="name",
            statistics_configurations=[cloudwatch.CfnMetricStream.MetricStreamStatisticsConfigurationProperty(
                additional_statistics=["additionalStatistics"],
                include_metrics=[cloudwatch.CfnMetricStream.MetricStreamStatisticsMetricProperty(
                    metric_name="metricName",
                    namespace="namespace"
                )]
            )],
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
        firehose_arn: builtins.str,
        output_format: builtins.str,
        role_arn: builtins.str,
        exclude_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnMetricStream.MetricStreamFilterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        include_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnMetricStream.MetricStreamFilterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        include_linked_accounts_metrics: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        statistics_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnMetricStream.MetricStreamStatisticsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CloudWatch::MetricStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firehose_arn: The ARN of the Amazon Kinesis Firehose delivery stream to use for this metric stream. This Amazon Kinesis Firehose delivery stream must already exist and must be in the same account as the metric stream.
        :param output_format: The output format for the stream. Valid values are ``json`` and ``opentelemetry0.7`` For more information about metric stream output formats, see `Metric streams output formats <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-metric-streams-formats.html>`_ . This parameter is required.
        :param role_arn: The ARN of an IAM role that this metric stream will use to access Amazon Kinesis Firehose resources. This IAM role must already exist and must be in the same account as the metric stream. This IAM role must include the ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` permissions.
        :param exclude_filters: If you specify this parameter, the stream sends metrics from all metric namespaces except for the namespaces that you specify here. You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream. When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.
        :param include_filters: If you specify this parameter, the stream sends only the metrics from the metric namespaces that you specify here. You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream. When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.
        :param include_linked_accounts_metrics: If you are creating a metric stream in a monitoring account, specify ``true`` to include metrics from source accounts that are linked to this monitoring account, in the metric stream. The default is ``false`` . For more information about linking accounts, see `CloudWatch cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html>`_
        :param name: If you are creating a new metric stream, this is the name for the new stream. The name must be different than the names of other metric streams in this account and Region. If you are updating a metric stream, specify the name of that stream here.
        :param statistics_configurations: By default, a metric stream always sends the MAX, MIN, SUM, and SAMPLECOUNT statistics for each metric that is streamed. You can use this parameter to have the metric stream also send additional statistics in the stream. This array can have up to 100 members. For each entry in this array, you specify one or more metrics and the list of additional statistics to stream for those metrics. The additional statistics that you can stream depend on the stream's ``OutputFormat`` . If the ``OutputFormat`` is ``json`` , you can stream any additional statistic that is supported by CloudWatch , listed in `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html.html>`_ . If the ``OutputFormat`` is ``opentelemetry0`` .7, you can stream percentile statistics *(p??)* .
        :param tags: An array of key-value pairs to apply to the metric stream. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6eb648d8ee9f1901d472d8639e6c94ea3e30c72d07bdbb72f595c9f49b8f741)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMetricStreamProps(
            firehose_arn=firehose_arn,
            output_format=output_format,
            role_arn=role_arn,
            exclude_filters=exclude_filters,
            include_filters=include_filters,
            include_linked_accounts_metrics=include_linked_accounts_metrics,
            name=name,
            statistics_configurations=statistics_configurations,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18fd6e24308ffdf8d29019bd5f818321742205776438f2c5042716b9a2d09a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff85e225c8d4aac4670e69459cc26d0796d7060711dadecca26881934449d521)
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
        '''The ARN of the metric stream.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDate")
    def attr_creation_date(self) -> builtins.str:
        '''The date that the metric stream was originally created.

        :cloudformationAttribute: CreationDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDate"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdateDate")
    def attr_last_update_date(self) -> builtins.str:
        '''The date that the metric stream was most recently updated.

        :cloudformationAttribute: LastUpdateDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdateDate"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the metric stream, either ``running`` or ``stopped`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to the metric stream.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="firehoseArn")
    def firehose_arn(self) -> builtins.str:
        '''The ARN of the Amazon Kinesis Firehose delivery stream to use for this metric stream.

        This Amazon Kinesis Firehose delivery stream must already exist and must be in the same account as the metric stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-firehosearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "firehoseArn"))

    @firehose_arn.setter
    def firehose_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5138db29db67eb4e16d0c3ab1a6b71f3a678a623b61ed96f573671fbdb84e494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firehoseArn", value)

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        '''The output format for the stream.

        Valid values are ``json`` and ``opentelemetry0.7`` For more information about metric stream output formats, see `Metric streams output formats <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-metric-streams-formats.html>`_ .

        This parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-outputformat
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89438dbd0ecf8eff56d6aac0f07a5d5ca7aae9489d1780ad3ce3810f6299ab77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of an IAM role that this metric stream will use to access Amazon Kinesis Firehose resources.

        This IAM role must already exist and must be in the same account as the metric stream. This IAM role must include the ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e76161dba4eed0b71fda6b8d7eda8d0b2258a063cb68c3068774a1f8a6093c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="excludeFilters")
    def exclude_filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamFilterProperty", _IResolvable_a771d0ef]]]]:
        '''If you specify this parameter, the stream sends metrics from all metric namespaces except for the namespaces that you specify here.

        You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream.

        When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-excludefilters
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamFilterProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "excludeFilters"))

    @exclude_filters.setter
    def exclude_filters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamFilterProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b3ce32049c481b13a4f597634d739f777ddbee6209b7addbb10f5eb1c3ff83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeFilters", value)

    @builtins.property
    @jsii.member(jsii_name="includeFilters")
    def include_filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamFilterProperty", _IResolvable_a771d0ef]]]]:
        '''If you specify this parameter, the stream sends only the metrics from the metric namespaces that you specify here.

        You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream.

        When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-includefilters
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamFilterProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "includeFilters"))

    @include_filters.setter
    def include_filters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamFilterProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d58f02b153747fa3026d5f0049a95a148d6fe8fcbb7883a65375d7a43393a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeFilters", value)

    @builtins.property
    @jsii.member(jsii_name="includeLinkedAccountsMetrics")
    def include_linked_accounts_metrics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If you are creating a metric stream in a monitoring account, specify ``true`` to include metrics from source accounts that are linked to this monitoring account, in the metric stream.

        The default is ``false`` .

        For more information about linking accounts, see `CloudWatch cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-includelinkedaccountsmetrics
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "includeLinkedAccountsMetrics"))

    @include_linked_accounts_metrics.setter
    def include_linked_accounts_metrics(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6def02a5c015f89c2e231d46514f8159962b76203b6c5247b4fb3fced33e6896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeLinkedAccountsMetrics", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''If you are creating a new metric stream, this is the name for the new stream.

        The name must be different than the names of other metric streams in this account and Region.

        If you are updating a metric stream, specify the name of that stream here.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb7928bcb3f6a7ac0ac41b5879ad0a5b04f83b7d60a02c6852ba565dbadecb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="statisticsConfigurations")
    def statistics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamStatisticsConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''By default, a metric stream always sends the MAX, MIN, SUM, and SAMPLECOUNT statistics for each metric that is streamed.

        You can use this parameter to have the metric stream also send additional statistics in the stream. This array can have up to 100 members.

        For each entry in this array, you specify one or more metrics and the list of additional statistics to stream for those metrics. The additional statistics that you can stream depend on the stream's ``OutputFormat`` . If the ``OutputFormat`` is ``json`` , you can stream any additional statistic that is supported by CloudWatch , listed in `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html.html>`_ . If the ``OutputFormat`` is ``opentelemetry0`` .7, you can stream percentile statistics *(p??)* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-statisticsconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamStatisticsConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "statisticsConfigurations"))

    @statistics_configurations.setter
    def statistics_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamStatisticsConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c7a4de6f9ec9e3f10b25e1f357075b2222c7136b4a7ced75cfce902b8cc720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statisticsConfigurations", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnMetricStream.MetricStreamFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"namespace": "namespace", "metric_names": "metricNames"},
    )
    class MetricStreamFilterProperty:
        def __init__(
            self,
            *,
            namespace: builtins.str,
            metric_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure contains a metric namespace and optionally, a list of metric names, to either include in a metric ' stream or exclude from a metric stream.

            A metric stream's filters can include up to 1000 total names. This limit applies to the sum of namespace names and metric names in the filters. For example, this could include 10 metric namespace filters with 99 metrics each, or 20 namespace filters with 49 metrics specified in each filter.

            :param namespace: The name of the metric namespace in the filter. The namespace can contain only ASCII printable characters (ASCII range 32 through 126). It must contain at least one non-whitespace character.
            :param metric_names: The names of the metrics to either include or exclude from the metric stream. If you omit this parameter, all metrics in the namespace are included or excluded, depending on whether this filter is specified as an exclude filter or an include filter. Each metric name can contain only ASCII printable characters (ASCII range 32 through 126). Each metric name must contain at least one non-whitespace character.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_stream_filter_property = cloudwatch.CfnMetricStream.MetricStreamFilterProperty(
                    namespace="namespace",
                
                    # the properties below are optional
                    metric_names=["metricNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94a12e26817c34cb058edd1e2ffe91c19fea8facd02af81b71bf97d8d10f6e8a)
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument metric_names", value=metric_names, expected_type=type_hints["metric_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "namespace": namespace,
            }
            if metric_names is not None:
                self._values["metric_names"] = metric_names

        @builtins.property
        def namespace(self) -> builtins.str:
            '''The name of the metric namespace in the filter.

            The namespace can contain only ASCII printable characters (ASCII range 32 through 126). It must contain at least one non-whitespace character.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamfilter.html#cfn-cloudwatch-metricstream-metricstreamfilter-namespace
            '''
            result = self._values.get("namespace")
            assert result is not None, "Required property 'namespace' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of the metrics to either include or exclude from the metric stream.

            If you omit this parameter, all metrics in the namespace are included or excluded, depending on whether this filter is specified as an exclude filter or an include filter.

            Each metric name can contain only ASCII printable characters (ASCII range 32 through 126). Each metric name must contain at least one non-whitespace character.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamfilter.html#cfn-cloudwatch-metricstream-metricstreamfilter-metricnames
            '''
            result = self._values.get("metric_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStreamFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnMetricStream.MetricStreamStatisticsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_statistics": "additionalStatistics",
            "include_metrics": "includeMetrics",
        },
    )
    class MetricStreamStatisticsConfigurationProperty:
        def __init__(
            self,
            *,
            additional_statistics: typing.Sequence[builtins.str],
            include_metrics: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnMetricStream.MetricStreamStatisticsMetricProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''This structure specifies a list of additional statistics to stream, and the metrics to stream those additional statistics for.

            All metrics that match the combination of metric name and namespace will be streamed with the additional statistics, no matter their dimensions.

            :param additional_statistics: The additional statistics to stream for the metrics listed in ``IncludeMetrics`` .
            :param include_metrics: An array that defines the metrics that are to have additional statistics streamed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_stream_statistics_configuration_property = cloudwatch.CfnMetricStream.MetricStreamStatisticsConfigurationProperty(
                    additional_statistics=["additionalStatistics"],
                    include_metrics=[cloudwatch.CfnMetricStream.MetricStreamStatisticsMetricProperty(
                        metric_name="metricName",
                        namespace="namespace"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0c72f24e1ad345ad4426d4db3eec0187fb91eff100ec57b906f60e61b2b05b9)
                check_type(argname="argument additional_statistics", value=additional_statistics, expected_type=type_hints["additional_statistics"])
                check_type(argname="argument include_metrics", value=include_metrics, expected_type=type_hints["include_metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "additional_statistics": additional_statistics,
                "include_metrics": include_metrics,
            }

        @builtins.property
        def additional_statistics(self) -> typing.List[builtins.str]:
            '''The additional statistics to stream for the metrics listed in ``IncludeMetrics`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsconfiguration.html#cfn-cloudwatch-metricstream-metricstreamstatisticsconfiguration-additionalstatistics
            '''
            result = self._values.get("additional_statistics")
            assert result is not None, "Required property 'additional_statistics' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def include_metrics(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamStatisticsMetricProperty", _IResolvable_a771d0ef]]]:
            '''An array that defines the metrics that are to have additional statistics streamed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsconfiguration.html#cfn-cloudwatch-metricstream-metricstreamstatisticsconfiguration-includemetrics
            '''
            result = self._values.get("include_metrics")
            assert result is not None, "Required property 'include_metrics' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricStream.MetricStreamStatisticsMetricProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStreamStatisticsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudwatch.CfnMetricStream.MetricStreamStatisticsMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_name": "metricName", "namespace": "namespace"},
    )
    class MetricStreamStatisticsMetricProperty:
        def __init__(
            self,
            *,
            metric_name: builtins.str,
            namespace: builtins.str,
        ) -> None:
            '''A structure that specifies the metric name and namespace for one metric that is going to have additional statistics included in the stream.

            :param metric_name: The name of the metric.
            :param namespace: The namespace of the metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudwatch as cloudwatch
                
                metric_stream_statistics_metric_property = cloudwatch.CfnMetricStream.MetricStreamStatisticsMetricProperty(
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4d525f834f62eace41e71b2ac53bdd15e18bbe8b221507a7ca6488213176f1e)
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "metric_name": metric_name,
                "namespace": namespace,
            }

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''The name of the metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsmetric.html#cfn-cloudwatch-metricstream-metricstreamstatisticsmetric-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def namespace(self) -> builtins.str:
            '''The namespace of the metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamstatisticsmetric.html#cfn-cloudwatch-metricstream-metricstreamstatisticsmetric-namespace
            '''
            result = self._values.get("namespace")
            assert result is not None, "Required property 'namespace' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStreamStatisticsMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CfnMetricStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "firehose_arn": "firehoseArn",
        "output_format": "outputFormat",
        "role_arn": "roleArn",
        "exclude_filters": "excludeFilters",
        "include_filters": "includeFilters",
        "include_linked_accounts_metrics": "includeLinkedAccountsMetrics",
        "name": "name",
        "statistics_configurations": "statisticsConfigurations",
        "tags": "tags",
    },
)
class CfnMetricStreamProps:
    def __init__(
        self,
        *,
        firehose_arn: builtins.str,
        output_format: builtins.str,
        role_arn: builtins.str,
        exclude_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        include_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        include_linked_accounts_metrics: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        statistics_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamStatisticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnMetricStream``.

        :param firehose_arn: The ARN of the Amazon Kinesis Firehose delivery stream to use for this metric stream. This Amazon Kinesis Firehose delivery stream must already exist and must be in the same account as the metric stream.
        :param output_format: The output format for the stream. Valid values are ``json`` and ``opentelemetry0.7`` For more information about metric stream output formats, see `Metric streams output formats <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-metric-streams-formats.html>`_ . This parameter is required.
        :param role_arn: The ARN of an IAM role that this metric stream will use to access Amazon Kinesis Firehose resources. This IAM role must already exist and must be in the same account as the metric stream. This IAM role must include the ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` permissions.
        :param exclude_filters: If you specify this parameter, the stream sends metrics from all metric namespaces except for the namespaces that you specify here. You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream. When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.
        :param include_filters: If you specify this parameter, the stream sends only the metrics from the metric namespaces that you specify here. You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream. When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.
        :param include_linked_accounts_metrics: If you are creating a metric stream in a monitoring account, specify ``true`` to include metrics from source accounts that are linked to this monitoring account, in the metric stream. The default is ``false`` . For more information about linking accounts, see `CloudWatch cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html>`_
        :param name: If you are creating a new metric stream, this is the name for the new stream. The name must be different than the names of other metric streams in this account and Region. If you are updating a metric stream, specify the name of that stream here.
        :param statistics_configurations: By default, a metric stream always sends the MAX, MIN, SUM, and SAMPLECOUNT statistics for each metric that is streamed. You can use this parameter to have the metric stream also send additional statistics in the stream. This array can have up to 100 members. For each entry in this array, you specify one or more metrics and the list of additional statistics to stream for those metrics. The additional statistics that you can stream depend on the stream's ``OutputFormat`` . If the ``OutputFormat`` is ``json`` , you can stream any additional statistic that is supported by CloudWatch , listed in `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html.html>`_ . If the ``OutputFormat`` is ``opentelemetry0`` .7, you can stream percentile statistics *(p??)* .
        :param tags: An array of key-value pairs to apply to the metric stream. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            cfn_metric_stream_props = cloudwatch.CfnMetricStreamProps(
                firehose_arn="firehoseArn",
                output_format="outputFormat",
                role_arn="roleArn",
            
                # the properties below are optional
                exclude_filters=[cloudwatch.CfnMetricStream.MetricStreamFilterProperty(
                    namespace="namespace",
            
                    # the properties below are optional
                    metric_names=["metricNames"]
                )],
                include_filters=[cloudwatch.CfnMetricStream.MetricStreamFilterProperty(
                    namespace="namespace",
            
                    # the properties below are optional
                    metric_names=["metricNames"]
                )],
                include_linked_accounts_metrics=False,
                name="name",
                statistics_configurations=[cloudwatch.CfnMetricStream.MetricStreamStatisticsConfigurationProperty(
                    additional_statistics=["additionalStatistics"],
                    include_metrics=[cloudwatch.CfnMetricStream.MetricStreamStatisticsMetricProperty(
                        metric_name="metricName",
                        namespace="namespace"
                    )]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01ae8278600fd5d054aecdc05a6df6e59a0b915ab186de415a85c8632b640df)
            check_type(argname="argument firehose_arn", value=firehose_arn, expected_type=type_hints["firehose_arn"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument exclude_filters", value=exclude_filters, expected_type=type_hints["exclude_filters"])
            check_type(argname="argument include_filters", value=include_filters, expected_type=type_hints["include_filters"])
            check_type(argname="argument include_linked_accounts_metrics", value=include_linked_accounts_metrics, expected_type=type_hints["include_linked_accounts_metrics"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument statistics_configurations", value=statistics_configurations, expected_type=type_hints["statistics_configurations"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firehose_arn": firehose_arn,
            "output_format": output_format,
            "role_arn": role_arn,
        }
        if exclude_filters is not None:
            self._values["exclude_filters"] = exclude_filters
        if include_filters is not None:
            self._values["include_filters"] = include_filters
        if include_linked_accounts_metrics is not None:
            self._values["include_linked_accounts_metrics"] = include_linked_accounts_metrics
        if name is not None:
            self._values["name"] = name
        if statistics_configurations is not None:
            self._values["statistics_configurations"] = statistics_configurations
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firehose_arn(self) -> builtins.str:
        '''The ARN of the Amazon Kinesis Firehose delivery stream to use for this metric stream.

        This Amazon Kinesis Firehose delivery stream must already exist and must be in the same account as the metric stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-firehosearn
        '''
        result = self._values.get("firehose_arn")
        assert result is not None, "Required property 'firehose_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_format(self) -> builtins.str:
        '''The output format for the stream.

        Valid values are ``json`` and ``opentelemetry0.7`` For more information about metric stream output formats, see `Metric streams output formats <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-metric-streams-formats.html>`_ .

        This parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-outputformat
        '''
        result = self._values.get("output_format")
        assert result is not None, "Required property 'output_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The ARN of an IAM role that this metric stream will use to access Amazon Kinesis Firehose resources.

        This IAM role must already exist and must be in the same account as the metric stream. This IAM role must include the ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamFilterProperty, _IResolvable_a771d0ef]]]]:
        '''If you specify this parameter, the stream sends metrics from all metric namespaces except for the namespaces that you specify here.

        You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream.

        When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-excludefilters
        '''
        result = self._values.get("exclude_filters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamFilterProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def include_filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamFilterProperty, _IResolvable_a771d0ef]]]]:
        '''If you specify this parameter, the stream sends only the metrics from the metric namespaces that you specify here.

        You cannot specify both ``IncludeFilters`` and ``ExcludeFilters`` in the same metric stream.

        When you modify the ``IncludeFilters`` or ``ExcludeFilters`` of an existing metric stream in any way, the metric stream is effectively restarted, so after such a change you will get only the datapoints that have a timestamp after the time of the update.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-includefilters
        '''
        result = self._values.get("include_filters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamFilterProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def include_linked_accounts_metrics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If you are creating a metric stream in a monitoring account, specify ``true`` to include metrics from source accounts that are linked to this monitoring account, in the metric stream.

        The default is ``false`` .

        For more information about linking accounts, see `CloudWatch cross-account observability <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-includelinkedaccountsmetrics
        '''
        result = self._values.get("include_linked_accounts_metrics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''If you are creating a new metric stream, this is the name for the new stream.

        The name must be different than the names of other metric streams in this account and Region.

        If you are updating a metric stream, specify the name of that stream here.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamStatisticsConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''By default, a metric stream always sends the MAX, MIN, SUM, and SAMPLECOUNT statistics for each metric that is streamed.

        You can use this parameter to have the metric stream also send additional statistics in the stream. This array can have up to 100 members.

        For each entry in this array, you specify one or more metrics and the list of additional statistics to stream for those metrics. The additional statistics that you can stream depend on the stream's ``OutputFormat`` . If the ``OutputFormat`` is ``json`` , you can stream any additional statistic that is supported by CloudWatch , listed in `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html.html>`_ . If the ``OutputFormat`` is ``opentelemetry0`` .7, you can stream percentile statistics *(p??)* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-statisticsconfigurations
        '''
        result = self._values.get("statistics_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamStatisticsConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to the metric stream.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Color(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_cloudwatch.Color"):
    '''(experimental) A set of standard colours that can be used in annotations in a GraphWidget.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        # execution_count_metric: cloudwatch.Metric
        # error_count_metric: cloudwatch.Metric
        
        
        dashboard.add_widgets(cloudwatch.GraphWidget(
            title="Executions vs error rate",
        
            left=[execution_count_metric],
        
            right=[error_count_metric.with(
                statistic="average",
                label="Error rate",
                color=cloudwatch.Color.GREEN
            )]
        ))
    '''

    @jsii.python.classproperty
    @jsii.member(jsii_name="BLUE")
    def BLUE(cls) -> builtins.str:
        '''(experimental) blue - hex #1f77b4.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "BLUE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BROWN")
    def BROWN(cls) -> builtins.str:
        '''(experimental) brown - hex #8c564b.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "BROWN"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GREEN")
    def GREEN(cls) -> builtins.str:
        '''(experimental) green - hex #2ca02c.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "GREEN"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GREY")
    def GREY(cls) -> builtins.str:
        '''(experimental) grey - hex #7f7f7f.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "GREY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORANGE")
    def ORANGE(cls) -> builtins.str:
        '''(experimental) orange - hex #ff7f0e.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ORANGE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PINK")
    def PINK(cls) -> builtins.str:
        '''(experimental) pink - hex #e377c2.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PINK"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PURPLE")
    def PURPLE(cls) -> builtins.str:
        '''(experimental) purple - hex #9467bd.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PURPLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RED")
    def RED(cls) -> builtins.str:
        '''(experimental) red - hex #d62728.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "RED"))


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CommonMetricOptions",
    jsii_struct_bases=[],
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
    },
)
class CommonMetricOptions:
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
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        '''(experimental) Options shared by most methods accepting metric options.

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
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_cloudwatch as cloudwatch
            
            # dimensions: Any
            # duration: monocdk.Duration
            
            common_metric_options = cloudwatch.CommonMetricOptions(
                account="account",
                color="color",
                dimensions={
                    "dimensions_key": dimensions
                },
                dimensions_map={
                    "dimensions_map_key": "dimensionsMap"
                },
                label="label",
                period=duration,
                region="region",
                statistic="statistic",
                unit=cloudwatch.Unit.SECONDS
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2836747294724a281bcf8aa8fcb1eadfd36d0e5667d3a3d69f3e91abf21cc568)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument dimensions_map", value=dimensions_map, expected_type=type_hints["dimensions_map"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
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
    def unit(self) -> typing.Optional["Unit"]:
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
        return typing.cast(typing.Optional["Unit"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonMetricOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.ComparisonOperator")
class ComparisonOperator(enum.Enum):
    '''(experimental) Comparison operator for evaluating alarms.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cloudwatch
        
        # my_hosted_zone: route53.HostedZone
        
        certificate = acm.Certificate(self, "Certificate",
            domain_name="hello.example.com",
            validation=acm.CertificateValidation.from_dns(my_hosted_zone)
        )
        certificate.metric_days_to_expiry().create_alarm(self, "Alarm",
            comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
            evaluation_periods=1,
            threshold=45
        )
    '''

    GREATER_THAN_OR_EQUAL_TO_THRESHOLD = "GREATER_THAN_OR_EQUAL_TO_THRESHOLD"
    '''(experimental) Specified statistic is greater than or equal to the threshold.

    :stability: experimental
    '''
    GREATER_THAN_THRESHOLD = "GREATER_THAN_THRESHOLD"
    '''(experimental) Specified statistic is strictly greater than the threshold.

    :stability: experimental
    '''
    LESS_THAN_THRESHOLD = "LESS_THAN_THRESHOLD"
    '''(experimental) Specified statistic is strictly less than the threshold.

    :stability: experimental
    '''
    LESS_THAN_OR_EQUAL_TO_THRESHOLD = "LESS_THAN_OR_EQUAL_TO_THRESHOLD"
    '''(experimental) Specified statistic is less than or equal to the threshold.

    :stability: experimental
    '''
    LESS_THAN_LOWER_OR_GREATER_THAN_UPPER_THRESHOLD = "LESS_THAN_LOWER_OR_GREATER_THAN_UPPER_THRESHOLD"
    '''(experimental) Specified statistic is lower than or greater than the anomaly model band.

    Used only for alarms based on anomaly detection models

    :stability: experimental
    '''
    GREATER_THAN_UPPER_THRESHOLD = "GREATER_THAN_UPPER_THRESHOLD"
    '''(experimental) Specified statistic is greater than the anomaly model band.

    Used only for alarms based on anomaly detection models

    :stability: experimental
    '''
    LESS_THAN_LOWER_THRESHOLD = "LESS_THAN_LOWER_THRESHOLD"
    '''(experimental) Specified statistic is lower than the anomaly model band.

    Used only for alarms based on anomaly detection models

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CompositeAlarmProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_rule": "alarmRule",
        "actions_enabled": "actionsEnabled",
        "alarm_description": "alarmDescription",
        "composite_alarm_name": "compositeAlarmName",
    },
)
class CompositeAlarmProps:
    def __init__(
        self,
        *,
        alarm_rule: "IAlarmRule",
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        composite_alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating a Composite Alarm.

        :param alarm_rule: (experimental) Expression that specifies which other alarms are to be evaluated to determine this composite alarm's state.
        :param actions_enabled: (experimental) Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: (experimental) Description for the alarm. Default: No description
        :param composite_alarm_name: (experimental) Name of the alarm. Default: Automatically generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # alarm1: cloudwatch.Alarm
            # alarm2: cloudwatch.Alarm
            # alarm3: cloudwatch.Alarm
            # alarm4: cloudwatch.Alarm
            
            
            alarm_rule = cloudwatch.AlarmRule.any_of(
                cloudwatch.AlarmRule.all_of(
                    cloudwatch.AlarmRule.any_of(alarm1,
                        cloudwatch.AlarmRule.from_alarm(alarm2, cloudwatch.AlarmState.OK), alarm3),
                    cloudwatch.AlarmRule.not(cloudwatch.AlarmRule.from_alarm(alarm4, cloudwatch.AlarmState.INSUFFICIENT_DATA))),
                cloudwatch.AlarmRule.from_boolean(False))
            
            cloudwatch.CompositeAlarm(self, "MyAwesomeCompositeAlarm",
                alarm_rule=alarm_rule
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca1d4eaea3c63ce37db39e18ed5413537df008a2a64ab30a457103428476e4a)
            check_type(argname="argument alarm_rule", value=alarm_rule, expected_type=type_hints["alarm_rule"])
            check_type(argname="argument actions_enabled", value=actions_enabled, expected_type=type_hints["actions_enabled"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument composite_alarm_name", value=composite_alarm_name, expected_type=type_hints["composite_alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_rule": alarm_rule,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if composite_alarm_name is not None:
            self._values["composite_alarm_name"] = composite_alarm_name

    @builtins.property
    def alarm_rule(self) -> "IAlarmRule":
        '''(experimental) Expression that specifies which other alarms are to be evaluated to determine this composite alarm's state.

        :stability: experimental
        '''
        result = self._values.get("alarm_rule")
        assert result is not None, "Required property 'alarm_rule' is missing"
        return typing.cast("IAlarmRule", result)

    @builtins.property
    def actions_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the actions for this alarm are enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("actions_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for the alarm.

        :default: No description

        :stability: experimental
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def composite_alarm_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the alarm.

        :default: Automatically generated name

        :stability: experimental
        '''
        result = self._values.get("composite_alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompositeAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CreateAlarmOptions",
    jsii_struct_bases=[],
    name_mapping={
        "evaluation_periods": "evaluationPeriods",
        "threshold": "threshold",
        "actions_enabled": "actionsEnabled",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "comparison_operator": "comparisonOperator",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluate_low_sample_count_percentile": "evaluateLowSampleCountPercentile",
        "period": "period",
        "statistic": "statistic",
        "treat_missing_data": "treatMissingData",
    },
)
class CreateAlarmOptions:
    def __init__(
        self,
        *,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional["TreatMissingData"] = None,
    ) -> None:
        '''(experimental) Properties needed to make an alarm from a metric.

        :param evaluation_periods: (experimental) The number of periods over which data is compared to the specified threshold.
        :param threshold: (experimental) The value against which the specified statistic is compared.
        :param actions_enabled: (experimental) Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: (experimental) Description for the alarm. Default: No description
        :param alarm_name: (experimental) Name of the alarm. Default: Automatically generated name
        :param comparison_operator: (experimental) Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: (experimental) The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: (experimental) Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: (experimental) Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as cloudwatch
            
            # my_hosted_zone: route53.HostedZone
            
            certificate = acm.Certificate(self, "Certificate",
                domain_name="hello.example.com",
                validation=acm.CertificateValidation.from_dns(my_hosted_zone)
            )
            certificate.metric_days_to_expiry().create_alarm(self, "Alarm",
                comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                evaluation_periods=1,
                threshold=45
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1f7778a5b877bb8eecb3cbba837c03054d139d31eede24c02c3d4bd9233e4b)
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument actions_enabled", value=actions_enabled, expected_type=type_hints["actions_enabled"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluate_low_sample_count_percentile", value=evaluate_low_sample_count_percentile, expected_type=type_hints["evaluate_low_sample_count_percentile"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "evaluation_periods": evaluation_periods,
            "threshold": threshold,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if comparison_operator is not None:
            self._values["comparison_operator"] = comparison_operator
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluate_low_sample_count_percentile is not None:
            self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if period is not None:
            self._values["period"] = period
        if statistic is not None:
            self._values["statistic"] = statistic
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        '''(experimental) The number of periods over which data is compared to the specified threshold.

        :stability: experimental
        '''
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''(experimental) The value against which the specified statistic is compared.

        :stability: experimental
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def actions_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the actions for this alarm are enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("actions_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for the alarm.

        :default: No description

        :stability: experimental
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the alarm.

        :default: Automatically generated name

        :stability: experimental
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comparison_operator(self) -> typing.Optional[ComparisonOperator]:
        '''(experimental) Comparison to use to check if metric is breaching.

        :default: GreaterThanOrEqualToThreshold

        :stability: experimental
        '''
        result = self._values.get("comparison_operator")
        return typing.cast(typing.Optional[ComparisonOperator], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M
        out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon
        CloudWatch User Guide.

        :default: ``evaluationPeriods``

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation
        :stability: experimental
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant.

        Used only for alarms that are based on percentiles.

        :default: - Not configured.

        :stability: experimental
        '''
        result = self._values.get("evaluate_low_sample_count_percentile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[_Duration_070aa057]:
        '''(deprecated) The period over which the specified statistic is applied.

        Cannot be used with ``MathExpression`` objects.

        :default: - The period from the metric

        :deprecated: Use ``metric.with({ period: ... })`` to encode the period into the Metric object

        :stability: deprecated
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''(deprecated) What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        Cannot be used with ``MathExpression`` objects.

        :default: - The statistic from the metric

        :deprecated: Use ``metric.with({ statistic: ... })`` to encode the period into the Metric object

        :stability: deprecated
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def treat_missing_data(self) -> typing.Optional["TreatMissingData"]:
        '''(experimental) Sets how this alarm is to handle missing data points.

        :default: TreatMissingData.Missing

        :stability: experimental
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional["TreatMissingData"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateAlarmOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.CustomWidgetProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_arn": "functionArn",
        "title": "title",
        "height": "height",
        "params": "params",
        "update_on_refresh": "updateOnRefresh",
        "update_on_resize": "updateOnResize",
        "update_on_time_range_change": "updateOnTimeRangeChange",
        "width": "width",
    },
)
class CustomWidgetProps:
    def __init__(
        self,
        *,
        function_arn: builtins.str,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        params: typing.Any = None,
        update_on_refresh: typing.Optional[builtins.bool] = None,
        update_on_resize: typing.Optional[builtins.bool] = None,
        update_on_time_range_change: typing.Optional[builtins.bool] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The properties for a CustomWidget.

        :param function_arn: (experimental) The Arn of the AWS Lambda function that returns HTML or JSON that will be displayed in the widget.
        :param title: (experimental) The title of the widget.
        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param params: (experimental) Parameters passed to the lambda function. Default: - no parameters are passed to the lambda function
        :param update_on_refresh: (experimental) Update the widget on refresh. Default: true
        :param update_on_resize: (experimental) Update the widget on resize. Default: true
        :param update_on_time_range_change: (experimental) Update the widget on time range change. Default: true
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # dashboard: cloudwatch.Dashboard
            
            
            # Import or create a lambda function
            fn = lambda_.Function.from_function_arn(dashboard, "Function", "arn:aws:lambda:us-east-1:123456789012:function:MyFn")
            
            dashboard.add_widgets(cloudwatch.CustomWidget(
                function_arn=fn.function_arn,
                title="My lambda baked widget"
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8a3786cd095ff0c21b02074192e7d7caae9f04b303a72aa79c8918bd02ef24)
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument update_on_refresh", value=update_on_refresh, expected_type=type_hints["update_on_refresh"])
            check_type(argname="argument update_on_resize", value=update_on_resize, expected_type=type_hints["update_on_resize"])
            check_type(argname="argument update_on_time_range_change", value=update_on_time_range_change, expected_type=type_hints["update_on_time_range_change"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_arn": function_arn,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if params is not None:
            self._values["params"] = params
        if update_on_refresh is not None:
            self._values["update_on_refresh"] = update_on_refresh
        if update_on_resize is not None:
            self._values["update_on_resize"] = update_on_resize
        if update_on_time_range_change is not None:
            self._values["update_on_time_range_change"] = update_on_time_range_change
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''(experimental) The Arn of the AWS Lambda function that returns HTML or JSON that will be displayed in the widget.

        :stability: experimental
        '''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''(experimental) The title of the widget.

        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def params(self) -> typing.Any:
        '''(experimental) Parameters passed to the lambda function.

        :default: - no parameters are passed to the lambda function

        :stability: experimental
        '''
        result = self._values.get("params")
        return typing.cast(typing.Any, result)

    @builtins.property
    def update_on_refresh(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the widget on refresh.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("update_on_refresh")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def update_on_resize(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the widget on resize.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("update_on_resize")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def update_on_time_range_change(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the widget on time range change.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("update_on_time_range_change")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the widget, in a grid of 24 units wide.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Dashboard(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.Dashboard",
):
    '''(experimental) A CloudWatch dashboard.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        # widget: cloudwatch.IWidget
        
        dashboard = cloudwatch.Dashboard(self, "MyDashboard",
            dashboard_name="dashboardName",
            end="end",
            period_override=cloudwatch.PeriodOverride.AUTO,
            start="start",
            widgets=[[widget]]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dashboard_name: typing.Optional[builtins.str] = None,
        end: typing.Optional[builtins.str] = None,
        period_override: typing.Optional["PeriodOverride"] = None,
        start: typing.Optional[builtins.str] = None,
        widgets: typing.Optional[typing.Sequence[typing.Sequence["IWidget"]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param dashboard_name: (experimental) Name of the dashboard. If set, must only contain alphanumerics, dash (-) and underscore (_) Default: - automatically generated name
        :param end: (experimental) The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
        :param period_override: (experimental) Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
        :param start: (experimental) The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        :param widgets: (experimental) Initial set of widgets on the dashboard. One array represents a row of widgets. Default: - No widgets

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc2441ca033c0fc7869f0bf6c90cf43070aec52a7a41e90a2ce70fcf7d7f8b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DashboardProps(
            dashboard_name=dashboard_name,
            end=end,
            period_override=period_override,
            start=start,
            widgets=widgets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: "IWidget") -> None:
        '''(experimental) Add a widget to the dashboard.

        Widgets given in multiple calls to add() will be laid out stacked on
        top of each other.

        Multiple widgets added in the same call to add() will be laid out next
        to each other.

        :param widgets: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d81df9283670f017e089e4c21e0cd472e165bfe2609bfa9251ef3fc003a04f)
            check_type(argname="argument widgets", value=widgets, expected_type=typing.Tuple[type_hints["widgets"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addWidgets", [*widgets]))

    @builtins.property
    @jsii.member(jsii_name="dashboardArn")
    def dashboard_arn(self) -> builtins.str:
        '''(experimental) ARN of this dashboard.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "dashboardArn"))

    @builtins.property
    @jsii.member(jsii_name="dashboardName")
    def dashboard_name(self) -> builtins.str:
        '''(experimental) The name of this dashboard.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "dashboardName"))


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.DashboardProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_name": "dashboardName",
        "end": "end",
        "period_override": "periodOverride",
        "start": "start",
        "widgets": "widgets",
    },
)
class DashboardProps:
    def __init__(
        self,
        *,
        dashboard_name: typing.Optional[builtins.str] = None,
        end: typing.Optional[builtins.str] = None,
        period_override: typing.Optional["PeriodOverride"] = None,
        start: typing.Optional[builtins.str] = None,
        widgets: typing.Optional[typing.Sequence[typing.Sequence["IWidget"]]] = None,
    ) -> None:
        '''(experimental) Properties for defining a CloudWatch Dashboard.

        :param dashboard_name: (experimental) Name of the dashboard. If set, must only contain alphanumerics, dash (-) and underscore (_) Default: - automatically generated name
        :param end: (experimental) The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
        :param period_override: (experimental) Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
        :param start: (experimental) The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        :param widgets: (experimental) Initial set of widgets on the dashboard. One array represents a row of widgets. Default: - No widgets

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            # widget: cloudwatch.IWidget
            
            dashboard_props = cloudwatch.DashboardProps(
                dashboard_name="dashboardName",
                end="end",
                period_override=cloudwatch.PeriodOverride.AUTO,
                start="start",
                widgets=[[widget]]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50643d8232c3a0f8ab2a83803a2e0c785903f22448cfc6b1799e783663978fa)
            check_type(argname="argument dashboard_name", value=dashboard_name, expected_type=type_hints["dashboard_name"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument period_override", value=period_override, expected_type=type_hints["period_override"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument widgets", value=widgets, expected_type=type_hints["widgets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dashboard_name is not None:
            self._values["dashboard_name"] = dashboard_name
        if end is not None:
            self._values["end"] = end
        if period_override is not None:
            self._values["period_override"] = period_override
        if start is not None:
            self._values["start"] = start
        if widgets is not None:
            self._values["widgets"] = widgets

    @builtins.property
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the dashboard.

        If set, must only contain alphanumerics, dash (-) and underscore (_)

        :default: - automatically generated name

        :stability: experimental
        '''
        result = self._values.get("dashboard_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''(experimental) The end of the time range to use for each widget on the dashboard when the dashboard loads.

        If you specify a value for end, you must also specify a value for start.
        Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

        :default: When the dashboard loads, the end date will be the current time.

        :stability: experimental
        '''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period_override(self) -> typing.Optional["PeriodOverride"]:
        '''(experimental) Use this field to specify the period for the graphs when the dashboard loads.

        Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard.
        Specifying ``Inherit`` ensures that the period set for each graph is always obeyed.

        :default: Auto

        :stability: experimental
        '''
        result = self._values.get("period_override")
        return typing.cast(typing.Optional["PeriodOverride"], result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''(experimental) The start of the time range to use for each widget on the dashboard.

        You can specify start without specifying end to specify a relative time range that ends with the current time.
        In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for
        minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months.
        You can also use start along with an end field, to specify an absolute time range.
        When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

        :default: When the dashboard loads, the start time will be the default time range.

        :stability: experimental
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def widgets(self) -> typing.Optional[typing.List[typing.List["IWidget"]]]:
        '''(experimental) Initial set of widgets on the dashboard.

        One array represents a row of widgets.

        :default: - No widgets

        :stability: experimental
        '''
        result = self._values.get("widgets")
        return typing.cast(typing.Optional[typing.List[typing.List["IWidget"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.Dimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Dimension:
    def __init__(self, *, name: builtins.str, value: typing.Any) -> None:
        '''(experimental) Metric dimension.

        :param name: (experimental) Name of the dimension.
        :param value: (experimental) Value of the dimension.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            # value: Any
            
            dimension = cloudwatch.Dimension(
                name="name",
                value=value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c8a78675a396e604694e7d4b4dbc5f9855bbb5891303b66cd0f7fe85002c00)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the dimension.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Any:
        '''(experimental) Value of the dimension.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Dimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.GraphWidgetView")
class GraphWidgetView(enum.Enum):
    '''(experimental) Types of view.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        
        
        dashboard.add_widgets(cloudwatch.GraphWidget(
            # ...
        
            view=cloudwatch.GraphWidgetView.BAR
        ))
    '''

    TIME_SERIES = "TIME_SERIES"
    '''(experimental) Display as a line graph.

    :stability: experimental
    '''
    BAR = "BAR"
    '''(experimental) Display as a bar graph.

    :stability: experimental
    '''
    PIE = "PIE"
    '''(experimental) Display as a pie graph.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.HorizontalAnnotation",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "color": "color",
        "fill": "fill",
        "label": "label",
        "visible": "visible",
    },
)
class HorizontalAnnotation:
    def __init__(
        self,
        *,
        value: jsii.Number,
        color: typing.Optional[builtins.str] = None,
        fill: typing.Optional["Shading"] = None,
        label: typing.Optional[builtins.str] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Horizontal annotation to be added to a graph.

        :param value: (experimental) The value of the annotation.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to be used for the annotation. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param fill: (experimental) Add shading above or below the annotation. Default: No shading
        :param label: (experimental) Label for the annotation. Default: - No label
        :param visible: (experimental) Whether the annotation is visible. Default: true

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            horizontal_annotation = cloudwatch.HorizontalAnnotation(
                value=123,
            
                # the properties below are optional
                color="color",
                fill=cloudwatch.Shading.NONE,
                label="label",
                visible=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b291fb2da233e4c299e325e23e406c4d2034081e37e85a1ae888188a4de7fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument fill", value=fill, expected_type=type_hints["fill"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument visible", value=visible, expected_type=type_hints["visible"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if color is not None:
            self._values["color"] = color
        if fill is not None:
            self._values["fill"] = fill
        if label is not None:
            self._values["label"] = label
        if visible is not None:
            self._values["visible"] = visible

    @builtins.property
    def value(self) -> jsii.Number:
        '''(experimental) The value of the annotation.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to be used for the annotation. The ``Color`` class has a set of standard colors that can be used here.

        :default: - Automatic color

        :stability: experimental
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill(self) -> typing.Optional["Shading"]:
        '''(experimental) Add shading above or below the annotation.

        :default: No shading

        :stability: experimental
        '''
        result = self._values.get("fill")
        return typing.cast(typing.Optional["Shading"], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(experimental) Label for the annotation.

        :default: - No label

        :stability: experimental
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visible(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the annotation is visible.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("visible")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalAnnotation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_cloudwatch.IAlarmAction")
class IAlarmAction(typing_extensions.Protocol):
    '''(experimental) Interface for objects that can be the targets of CloudWatch alarm actions.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_e78e779f, alarm: "IAlarm") -> AlarmActionConfig:
        '''(experimental) Return the properties required to send alarm actions to this CloudWatch alarm.

        :param scope: root Construct that allows creating new Constructs.
        :param alarm: CloudWatch alarm that the action will target.

        :stability: experimental
        '''
        ...


class _IAlarmActionProxy:
    '''(experimental) Interface for objects that can be the targets of CloudWatch alarm actions.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_cloudwatch.IAlarmAction"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_e78e779f, alarm: "IAlarm") -> AlarmActionConfig:
        '''(experimental) Return the properties required to send alarm actions to this CloudWatch alarm.

        :param scope: root Construct that allows creating new Constructs.
        :param alarm: CloudWatch alarm that the action will target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2785d3adb99b00446f2088de67423c9d3f630afaa0281f669057f00d74916785)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
        return typing.cast(AlarmActionConfig, jsii.invoke(self, "bind", [scope, alarm]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAlarmAction).__jsii_proxy_class__ = lambda : _IAlarmActionProxy


@jsii.interface(jsii_type="monocdk.aws_cloudwatch.IAlarmRule")
class IAlarmRule(typing_extensions.Protocol):
    '''(experimental) Interface for Alarm Rule.

    :stability: experimental
    '''

    @jsii.member(jsii_name="renderAlarmRule")
    def render_alarm_rule(self) -> builtins.str:
        '''(experimental) serialized representation of Alarm Rule to be used when building the Composite Alarm resource.

        :stability: experimental
        '''
        ...


class _IAlarmRuleProxy:
    '''(experimental) Interface for Alarm Rule.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_cloudwatch.IAlarmRule"

    @jsii.member(jsii_name="renderAlarmRule")
    def render_alarm_rule(self) -> builtins.str:
        '''(experimental) serialized representation of Alarm Rule to be used when building the Composite Alarm resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "renderAlarmRule", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAlarmRule).__jsii_proxy_class__ = lambda : _IAlarmRuleProxy


@jsii.interface(jsii_type="monocdk.aws_cloudwatch.IMetric")
class IMetric(typing_extensions.Protocol):
    '''(experimental) Interface for metrics.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Any warnings related to this metric.

        Should be attached to the consuming construct.

        :default: - None

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        '''(deprecated) Turn this metric object into an alarm configuration.

        :deprecated: Use ``toMetricConfig()`` instead.

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        '''(deprecated) Turn this metric object into a graph configuration.

        :deprecated: Use ``toMetricConfig()`` instead.

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        '''(experimental) Inspect the details of the metric object.

        :stability: experimental
        '''
        ...


class _IMetricProxy:
    '''(experimental) Interface for metrics.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_cloudwatch.IMetric"

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Any warnings related to this metric.

        Should be attached to the consuming construct.

        :default: - None

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "warnings"))

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        '''(deprecated) Turn this metric object into an alarm configuration.

        :deprecated: Use ``toMetricConfig()`` instead.

        :stability: deprecated
        '''
        return typing.cast("MetricAlarmConfig", jsii.invoke(self, "toAlarmConfig", []))

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        '''(deprecated) Turn this metric object into a graph configuration.

        :deprecated: Use ``toMetricConfig()`` instead.

        :stability: deprecated
        '''
        return typing.cast("MetricGraphConfig", jsii.invoke(self, "toGraphConfig", []))

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        '''(experimental) Inspect the details of the metric object.

        :stability: experimental
        '''
        return typing.cast("MetricConfig", jsii.invoke(self, "toMetricConfig", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMetric).__jsii_proxy_class__ = lambda : _IMetricProxy


@jsii.interface(jsii_type="monocdk.aws_cloudwatch.IWidget")
class IWidget(typing_extensions.Protocol):
    '''(experimental) A single dashboard widget.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        '''(experimental) The amount of vertical grid units the widget will take up.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        '''(experimental) The amount of horizontal grid units the widget will take up.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Any warnings that are produced as a result of putting together this widget.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        '''(experimental) Place the widget at a given position.

        :param x: -
        :param y: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        ...


class _IWidgetProxy:
    '''(experimental) A single dashboard widget.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_cloudwatch.IWidget"

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        '''(experimental) The amount of vertical grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        '''(experimental) The amount of horizontal grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Any warnings that are produced as a result of putting together this widget.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "warnings"))

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        '''(experimental) Place the widget at a given position.

        :param x: -
        :param y: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96d51d870dfc91a094333515161f8456605eebb6433779d18e6fdcac9ed3842)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        return typing.cast(None, jsii.invoke(self, "position", [x, y]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWidget).__jsii_proxy_class__ = lambda : _IWidgetProxy


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.LegendPosition")
class LegendPosition(enum.Enum):
    '''(experimental) The position of the legend on a GraphWidget.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        
        
        dashboard.add_widgets(cloudwatch.GraphWidget(
            # ...
        
            legend_position=cloudwatch.LegendPosition.RIGHT
        ))
    '''

    BOTTOM = "BOTTOM"
    '''(experimental) Legend appears below the graph (default).

    :stability: experimental
    '''
    RIGHT = "RIGHT"
    '''(experimental) Add shading above the annotation.

    :stability: experimental
    '''
    HIDDEN = "HIDDEN"
    '''(experimental) Add shading below the annotation.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.LogQueryVisualizationType")
class LogQueryVisualizationType(enum.Enum):
    '''(experimental) Types of view.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        
        
        dashboard.add_widgets(cloudwatch.LogQueryWidget(
            log_group_names=["my-log-group"],
            view=cloudwatch.LogQueryVisualizationType.TABLE,
            # The lines will be automatically combined using '\n|'.
            query_lines=["fields @message", "filter @message like /Error/"
            ]
        ))
    '''

    TABLE = "TABLE"
    '''(experimental) Table view.

    :stability: experimental
    '''
    LINE = "LINE"
    '''(experimental) Line view.

    :stability: experimental
    '''
    STACKEDAREA = "STACKEDAREA"
    '''(experimental) Stacked area view.

    :stability: experimental
    '''
    BAR = "BAR"
    '''(experimental) Bar view.

    :stability: experimental
    '''
    PIE = "PIE"
    '''(experimental) Pie view.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.LogQueryWidgetProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_names": "logGroupNames",
        "height": "height",
        "query_lines": "queryLines",
        "query_string": "queryString",
        "region": "region",
        "title": "title",
        "view": "view",
        "width": "width",
    },
)
class LogQueryWidgetProps:
    def __init__(
        self,
        *,
        log_group_names: typing.Sequence[builtins.str],
        height: typing.Optional[jsii.Number] = None,
        query_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        view: typing.Optional[LogQueryVisualizationType] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for a Query widget.

        :param log_group_names: (experimental) Names of log groups to query.
        :param height: (experimental) Height of the widget. Default: 6
        :param query_lines: (experimental) A sequence of lines to use to build the query. The query will be built by joining the lines together using ``\\n|``. Default: - Exactly one of ``queryString``, ``queryLines`` is required.
        :param query_string: (experimental) Full query string for log insights. Be sure to prepend every new line with a newline and pipe character (``\\n|``). Default: - Exactly one of ``queryString``, ``queryLines`` is required.
        :param region: (experimental) The region the metrics of this widget should be taken from. Default: Current region
        :param title: (experimental) Title for the widget. Default: No title
        :param view: (experimental) The type of view to use. Default: LogQueryVisualizationType.TABLE
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # dashboard: cloudwatch.Dashboard
            
            
            dashboard.add_widgets(cloudwatch.LogQueryWidget(
                log_group_names=["my-log-group"],
                view=cloudwatch.LogQueryVisualizationType.TABLE,
                # The lines will be automatically combined using '\n|'.
                query_lines=["fields @message", "filter @message like /Error/"
                ]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0cf610a40ba144394f70dee71dcc96a4d2df100bbd3a21536d890359a88dfe)
            check_type(argname="argument log_group_names", value=log_group_names, expected_type=type_hints["log_group_names"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument query_lines", value=query_lines, expected_type=type_hints["query_lines"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument view", value=view, expected_type=type_hints["view"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_names": log_group_names,
        }
        if height is not None:
            self._values["height"] = height
        if query_lines is not None:
            self._values["query_lines"] = query_lines
        if query_string is not None:
            self._values["query_string"] = query_string
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if view is not None:
            self._values["view"] = view
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def log_group_names(self) -> typing.List[builtins.str]:
        '''(experimental) Names of log groups to query.

        :stability: experimental
        '''
        result = self._values.get("log_group_names")
        assert result is not None, "Required property 'log_group_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the widget.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query_lines(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A sequence of lines to use to build the query.

        The query will be built by joining the lines together using ``\\n|``.

        :default: - Exactly one of ``queryString``, ``queryLines`` is required.

        :stability: experimental
        '''
        result = self._values.get("query_lines")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Full query string for log insights.

        Be sure to prepend every new line with a newline and pipe character
        (``\\n|``).

        :default: - Exactly one of ``queryString``, ``queryLines`` is required.

        :stability: experimental
        '''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region the metrics of this widget should be taken from.

        :default: Current region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''(experimental) Title for the widget.

        :default: No title

        :stability: experimental
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view(self) -> typing.Optional[LogQueryVisualizationType]:
        '''(experimental) The type of view to use.

        :default: LogQueryVisualizationType.TABLE

        :stability: experimental
        '''
        result = self._values.get("view")
        return typing.cast(typing.Optional[LogQueryVisualizationType], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the widget, in a grid of 24 units wide.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogQueryWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMetric)
class MathExpression(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.MathExpression",
):
    '''(experimental) A math expression built with metric(s) emitted by a service.

    The math expression is a combination of an expression (x+y) and metrics to apply expression on.
    It also contains metadata which is used only in graphs, such as color and label.
    It makes sense to embed this in here, so that compound constructs can attach
    that metadata to metrics they expose.

    MathExpression can also be used for search expressions. In this case,
    it also optionally accepts a searchRegion and searchAccount property for cross-environment
    search expressions.

    This class does not represent a resource, so hence is not a construct. Instead,
    MathExpression is an abstraction that makes it easy to specify metrics for use in both
    alarms and graphs.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # fn: lambda.Function
        
        
        all_problems = cloudwatch.MathExpression(
            expression="errors + throttles",
            using_metrics={
                "errors": fn.metric_errors(),
                "faults": fn.metric_throttles()
            }
        )
    '''

    def __init__(
        self,
        *,
        expression: builtins.str,
        using_metrics: typing.Optional[typing.Mapping[builtins.str, IMetric]] = None,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        search_account: typing.Optional[builtins.str] = None,
        search_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: (experimental) The expression defining the metric. When an expression contains a SEARCH function, it cannot be used within an Alarm.
        :param using_metrics: (experimental) The metrics used in the expression, in a map. The key is the identifier that represents the given metric in the expression, and the value is the actual Metric object. Default: - Empty map.
        :param color: (experimental) Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: (experimental) Label for this expression when added to a Graph in a Dashboard. If this expression evaluates to more than one time series (for example, through the use of ``METRICS()`` or ``SEARCH()`` expressions), each time series will appear in the graph using a combination of the expression label and the individual metric label. Specify the empty string (``''``) to suppress the expression label and only keep the metric label. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. If the math expression produces more than one time series, the maximum will be shown for each individual time series produce by this math expression. Default: - Expression value is used as label
        :param period: (experimental) The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        :param search_account: (experimental) Account to evaluate search expressions within. Specifying a searchAccount has no effect to the account used for metrics within the expression (passed via usingMetrics). Default: - Deployment account.
        :param search_region: (experimental) Region to evaluate search expressions within. Specifying a searchRegion has no effect to the region used for metrics within the expression (passed via usingMetrics). Default: - Deployment region.

        :stability: experimental
        '''
        props = MathExpressionProps(
            expression=expression,
            using_metrics=using_metrics,
            color=color,
            label=label,
            period=period,
            search_account=search_account,
            search_region=search_region,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="createAlarm")
    def create_alarm(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional["TreatMissingData"] = None,
    ) -> "Alarm":
        '''(experimental) Make a new Alarm for this metric.

        Combines both properties that may adjust the metric (aggregation) as well
        as alarm properties.

        :param scope: -
        :param id: -
        :param evaluation_periods: (experimental) The number of periods over which data is compared to the specified threshold.
        :param threshold: (experimental) The value against which the specified statistic is compared.
        :param actions_enabled: (experimental) Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: (experimental) Description for the alarm. Default: No description
        :param alarm_name: (experimental) Name of the alarm. Default: Automatically generated name
        :param comparison_operator: (experimental) Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: (experimental) The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: (experimental) Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: (experimental) Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18a7808c14a4c5292f94693fc9c01fe6e3ce432424a347ac2574133b7dff698)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CreateAlarmOptions(
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            actions_enabled=actions_enabled,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            comparison_operator=comparison_operator,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            period=period,
            statistic=statistic,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("Alarm", jsii.invoke(self, "createAlarm", [scope, id, props]))

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        '''(deprecated) Turn this metric object into an alarm configuration.

        :deprecated: use toMetricConfig()

        :stability: deprecated
        '''
        return typing.cast("MetricAlarmConfig", jsii.invoke(self, "toAlarmConfig", []))

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        '''(deprecated) Turn this metric object into a graph configuration.

        :deprecated: use toMetricConfig()

        :stability: deprecated
        '''
        return typing.cast("MetricGraphConfig", jsii.invoke(self, "toGraphConfig", []))

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        '''(experimental) Inspect the details of the metric object.

        :stability: experimental
        '''
        return typing.cast("MetricConfig", jsii.invoke(self, "toMetricConfig", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="with")
    def with_(
        self,
        *,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        search_account: typing.Optional[builtins.str] = None,
        search_region: typing.Optional[builtins.str] = None,
    ) -> "MathExpression":
        '''(experimental) Return a copy of Metric with properties changed.

        All properties except namespace and metricName can be changed.

        :param color: (experimental) Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: (experimental) Label for this expression when added to a Graph in a Dashboard. If this expression evaluates to more than one time series (for example, through the use of ``METRICS()`` or ``SEARCH()`` expressions), each time series will appear in the graph using a combination of the expression label and the individual metric label. Specify the empty string (``''``) to suppress the expression label and only keep the metric label. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. If the math expression produces more than one time series, the maximum will be shown for each individual time series produce by this math expression. Default: - Expression value is used as label
        :param period: (experimental) The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        :param search_account: (experimental) Account to evaluate search expressions within. Specifying a searchAccount has no effect to the account used for metrics within the expression (passed via usingMetrics). Default: - Deployment account.
        :param search_region: (experimental) Region to evaluate search expressions within. Specifying a searchRegion has no effect to the region used for metrics within the expression (passed via usingMetrics). Default: - Deployment region.

        :stability: experimental
        '''
        props = MathExpressionOptions(
            color=color,
            label=label,
            period=period,
            search_account=search_account,
            search_region=search_region,
        )

        return typing.cast("MathExpression", jsii.invoke(self, "with", [props]))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        '''(experimental) The expression defining the metric.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _Duration_070aa057:
        '''(experimental) Aggregation period of this metric.

        :stability: experimental
        '''
        return typing.cast(_Duration_070aa057, jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="usingMetrics")
    def using_metrics(self) -> typing.Mapping[builtins.str, IMetric]:
        '''(experimental) The metrics used in the expression as KeyValuePair <id, metric>.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, IMetric], jsii.get(self, "usingMetrics"))

    @builtins.property
    @jsii.member(jsii_name="color")
    def color(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "color"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Optional[builtins.str]:
        '''(experimental) Label for this metric when added to a Graph.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "label"))

    @builtins.property
    @jsii.member(jsii_name="searchAccount")
    def search_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account to evaluate search expressions within.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchAccount"))

    @builtins.property
    @jsii.member(jsii_name="searchRegion")
    def search_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region to evaluate search expressions within.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchRegion"))

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Warnings generated by this math expression.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "warnings"))


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MathExpressionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "color": "color",
        "label": "label",
        "period": "period",
        "search_account": "searchAccount",
        "search_region": "searchRegion",
    },
)
class MathExpressionOptions:
    def __init__(
        self,
        *,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        search_account: typing.Optional[builtins.str] = None,
        search_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configurable options for MathExpressions.

        :param color: (experimental) Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: (experimental) Label for this expression when added to a Graph in a Dashboard. If this expression evaluates to more than one time series (for example, through the use of ``METRICS()`` or ``SEARCH()`` expressions), each time series will appear in the graph using a combination of the expression label and the individual metric label. Specify the empty string (``''``) to suppress the expression label and only keep the metric label. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. If the math expression produces more than one time series, the maximum will be shown for each individual time series produce by this math expression. Default: - Expression value is used as label
        :param period: (experimental) The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        :param search_account: (experimental) Account to evaluate search expressions within. Specifying a searchAccount has no effect to the account used for metrics within the expression (passed via usingMetrics). Default: - Deployment account.
        :param search_region: (experimental) Region to evaluate search expressions within. Specifying a searchRegion has no effect to the region used for metrics within the expression (passed via usingMetrics). Default: - Deployment region.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_cloudwatch as cloudwatch
            
            # duration: monocdk.Duration
            
            math_expression_options = cloudwatch.MathExpressionOptions(
                color="color",
                label="label",
                period=duration,
                search_account="searchAccount",
                search_region="searchRegion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f693ea6b1f10e6962d3f83241a0088267d68a7f6cbb8c014cd9a93515ecb6842)
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument search_account", value=search_account, expected_type=type_hints["search_account"])
            check_type(argname="argument search_region", value=search_region, expected_type=type_hints["search_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if color is not None:
            self._values["color"] = color
        if label is not None:
            self._values["label"] = label
        if period is not None:
            self._values["period"] = period
        if search_account is not None:
            self._values["search_account"] = search_account
        if search_region is not None:
            self._values["search_region"] = search_region

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        '''(experimental) Color for this metric when added to a Graph in a Dashboard.

        :default: - Automatic color

        :stability: experimental
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(experimental) Label for this expression when added to a Graph in a Dashboard.

        If this expression evaluates to more than one time series (for
        example, through the use of ``METRICS()`` or ``SEARCH()`` expressions),
        each time series will appear in the graph using a combination of the
        expression label and the individual metric label. Specify the empty
        string (``''``) to suppress the expression label and only keep the
        metric label.

        You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_
        to show summary information about the displayed time series
        in the legend. For example, if you use::

           [max: ${MAX}] MyMetric

        As the metric label, the maximum value in the visible range will
        be shown next to the time series name in the graph's legend. If the
        math expression produces more than one time series, the maximum
        will be shown for each individual time series produce by this
        math expression.

        :default: - Expression value is used as label

        :stability: experimental
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The period over which the expression's statistics are applied.

        This period overrides all periods in the metrics used in this
        math expression.

        :default: Duration.minutes(5)

        :stability: experimental
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def search_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account to evaluate search expressions within.

        Specifying a searchAccount has no effect to the account used
        for metrics within the expression (passed via usingMetrics).

        :default: - Deployment account.

        :stability: experimental
        '''
        result = self._values.get("search_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region to evaluate search expressions within.

        Specifying a searchRegion has no effect to the region used
        for metrics within the expression (passed via usingMetrics).

        :default: - Deployment region.

        :stability: experimental
        '''
        result = self._values.get("search_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MathExpressionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MathExpressionProps",
    jsii_struct_bases=[MathExpressionOptions],
    name_mapping={
        "color": "color",
        "label": "label",
        "period": "period",
        "search_account": "searchAccount",
        "search_region": "searchRegion",
        "expression": "expression",
        "using_metrics": "usingMetrics",
    },
)
class MathExpressionProps(MathExpressionOptions):
    def __init__(
        self,
        *,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        search_account: typing.Optional[builtins.str] = None,
        search_region: typing.Optional[builtins.str] = None,
        expression: builtins.str,
        using_metrics: typing.Optional[typing.Mapping[builtins.str, IMetric]] = None,
    ) -> None:
        '''(experimental) Properties for a MathExpression.

        :param color: (experimental) Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: (experimental) Label for this expression when added to a Graph in a Dashboard. If this expression evaluates to more than one time series (for example, through the use of ``METRICS()`` or ``SEARCH()`` expressions), each time series will appear in the graph using a combination of the expression label and the individual metric label. Specify the empty string (``''``) to suppress the expression label and only keep the metric label. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. If the math expression produces more than one time series, the maximum will be shown for each individual time series produce by this math expression. Default: - Expression value is used as label
        :param period: (experimental) The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        :param search_account: (experimental) Account to evaluate search expressions within. Specifying a searchAccount has no effect to the account used for metrics within the expression (passed via usingMetrics). Default: - Deployment account.
        :param search_region: (experimental) Region to evaluate search expressions within. Specifying a searchRegion has no effect to the region used for metrics within the expression (passed via usingMetrics). Default: - Deployment region.
        :param expression: (experimental) The expression defining the metric. When an expression contains a SEARCH function, it cannot be used within an Alarm.
        :param using_metrics: (experimental) The metrics used in the expression, in a map. The key is the identifier that represents the given metric in the expression, and the value is the actual Metric object. Default: - Empty map.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # fn: lambda.Function
            
            
            all_problems = cloudwatch.MathExpression(
                expression="errors + throttles",
                using_metrics={
                    "errors": fn.metric_errors(),
                    "faults": fn.metric_throttles()
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9581302082381523367d1717dc5cb89dabad600a231634d5f4d7667973c22fd1)
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument search_account", value=search_account, expected_type=type_hints["search_account"])
            check_type(argname="argument search_region", value=search_region, expected_type=type_hints["search_region"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument using_metrics", value=using_metrics, expected_type=type_hints["using_metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if color is not None:
            self._values["color"] = color
        if label is not None:
            self._values["label"] = label
        if period is not None:
            self._values["period"] = period
        if search_account is not None:
            self._values["search_account"] = search_account
        if search_region is not None:
            self._values["search_region"] = search_region
        if using_metrics is not None:
            self._values["using_metrics"] = using_metrics

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        '''(experimental) Color for this metric when added to a Graph in a Dashboard.

        :default: - Automatic color

        :stability: experimental
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(experimental) Label for this expression when added to a Graph in a Dashboard.

        If this expression evaluates to more than one time series (for
        example, through the use of ``METRICS()`` or ``SEARCH()`` expressions),
        each time series will appear in the graph using a combination of the
        expression label and the individual metric label. Specify the empty
        string (``''``) to suppress the expression label and only keep the
        metric label.

        You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_
        to show summary information about the displayed time series
        in the legend. For example, if you use::

           [max: ${MAX}] MyMetric

        As the metric label, the maximum value in the visible range will
        be shown next to the time series name in the graph's legend. If the
        math expression produces more than one time series, the maximum
        will be shown for each individual time series produce by this
        math expression.

        :default: - Expression value is used as label

        :stability: experimental
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The period over which the expression's statistics are applied.

        This period overrides all periods in the metrics used in this
        math expression.

        :default: Duration.minutes(5)

        :stability: experimental
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def search_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account to evaluate search expressions within.

        Specifying a searchAccount has no effect to the account used
        for metrics within the expression (passed via usingMetrics).

        :default: - Deployment account.

        :stability: experimental
        '''
        result = self._values.get("search_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region to evaluate search expressions within.

        Specifying a searchRegion has no effect to the region used
        for metrics within the expression (passed via usingMetrics).

        :default: - Deployment region.

        :stability: experimental
        '''
        result = self._values.get("search_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> builtins.str:
        '''(experimental) The expression defining the metric.

        When an expression contains a SEARCH function, it cannot be used
        within an Alarm.

        :stability: experimental
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def using_metrics(self) -> typing.Optional[typing.Mapping[builtins.str, IMetric]]:
        '''(experimental) The metrics used in the expression, in a map.

        The key is the identifier that represents the given metric in the
        expression, and the value is the actual Metric object.

        :default: - Empty map.

        :stability: experimental
        '''
        result = self._values.get("using_metrics")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, IMetric]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MathExpressionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMetric)
class Metric(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_cloudwatch.Metric"):
    '''(experimental) A metric emitted by a service.

    The metric is a combination of a metric identifier (namespace, name and dimensions)
    and an aggregation function (statistic, period and unit).

    It also contains metadata which is used only in graphs, such as color and label.
    It makes sense to embed this in here, so that compound constructs can attach
    that metadata to metrics they expose.

    This class does not represent a resource, so hence is not a construct. Instead,
    Metric is an abstraction that makes it easy to specify metrics for use in both
    alarms and graphs.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # fn: lambda.Function
        
        
        minute_error_rate = fn.metric_errors(
            statistic="avg",
            period=Duration.minutes(1),
            label="Lambda failure rate"
        )
    '''

    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        '''
        :param metric_name: (experimental) Name of the metric.
        :param namespace: (experimental) Namespace of the metric.
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
        props = MetricProps(
            metric_name=metric_name,
            namespace=namespace,
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

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="grantPutMetricData")
    @builtins.classmethod
    def grant_put_metric_data(cls, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant permissions to the given identity to write metrics.

        :param grantee: The IAM identity to give permissions to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ca50267f75729e43c6dccb066af962ca5f0fbda4ef23f8a3e163216dd55c47)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.sinvoke(cls, "grantPutMetricData", [grantee]))

    @jsii.member(jsii_name="attachTo")
    def attach_to(self, scope: _constructs_77d1e7e8.IConstruct) -> "Metric":
        '''(experimental) Attach the metric object to the given construct scope.

        Returns a Metric object that uses the account and region from the Stack
        the given construct is defined in. If the metric is subsequently used
        in a Dashboard or Alarm in a different Stack defined in a different
        account or region, the appropriate 'region' and 'account' fields
        will be added to it.

        If the scope we attach to is in an environment-agnostic stack,
        nothing is done and the same Metric object is returned.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d6a191cecda4161675d78a063b4b5132574036535821f60f8c3ad1a12d4407)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("Metric", jsii.invoke(self, "attachTo", [scope]))

    @jsii.member(jsii_name="createAlarm")
    def create_alarm(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional["TreatMissingData"] = None,
    ) -> "Alarm":
        '''(experimental) Make a new Alarm for this metric.

        Combines both properties that may adjust the metric (aggregation) as well
        as alarm properties.

        :param scope: -
        :param id: -
        :param evaluation_periods: (experimental) The number of periods over which data is compared to the specified threshold.
        :param threshold: (experimental) The value against which the specified statistic is compared.
        :param actions_enabled: (experimental) Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: (experimental) Description for the alarm. Default: No description
        :param alarm_name: (experimental) Name of the alarm. Default: Automatically generated name
        :param comparison_operator: (experimental) Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: (experimental) The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: (experimental) Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: (experimental) Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a85163e9a6980b62870514e4bb90adfbb00f8bb4e9b627d88c8712935e9f008)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CreateAlarmOptions(
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            actions_enabled=actions_enabled,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            comparison_operator=comparison_operator,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            period=period,
            statistic=statistic,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("Alarm", jsii.invoke(self, "createAlarm", [scope, id, props]))

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        '''(deprecated) Turn this metric object into an alarm configuration.

        :deprecated: use toMetricConfig()

        :stability: deprecated
        '''
        return typing.cast("MetricAlarmConfig", jsii.invoke(self, "toAlarmConfig", []))

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        '''(deprecated) Turn this metric object into a graph configuration.

        :deprecated: use toMetricConfig()

        :stability: deprecated
        '''
        return typing.cast("MetricGraphConfig", jsii.invoke(self, "toGraphConfig", []))

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        '''(experimental) Inspect the details of the metric object.

        :stability: experimental
        '''
        return typing.cast("MetricConfig", jsii.invoke(self, "toMetricConfig", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="with")
    def with_(
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
        unit: typing.Optional["Unit"] = None,
    ) -> "Metric":
        '''(experimental) Return a copy of Metric ``with`` properties changed.

        All properties except namespace and metricName can be changed.

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
        props = MetricOptions(
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

        return typing.cast("Metric", jsii.invoke(self, "with", [props]))

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        '''(experimental) Name of this metric.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        '''(experimental) Namespace of this metric.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> _Duration_070aa057:
        '''(experimental) Period of this metric.

        :stability: experimental
        '''
        return typing.cast(_Duration_070aa057, jsii.get(self, "period"))

    @builtins.property
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> builtins.str:
        '''(experimental) Statistic of this metric.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "statistic"))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account which this metric comes from.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "account"))

    @builtins.property
    @jsii.member(jsii_name="color")
    def color(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hex color code used when this metric is rendered on a graph.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "color"))

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Dimensions of this metric.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "dimensions"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Optional[builtins.str]:
        '''(experimental) Label for this metric when added to a Graph in a Dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "label"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region which this metric comes from.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> typing.Optional["Unit"]:
        '''(experimental) Unit of the metric.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Unit"], jsii.get(self, "unit"))

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Warnings attached to this metric.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "warnings"))


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricAlarmConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "namespace": "namespace",
        "period": "period",
        "dimensions": "dimensions",
        "extended_statistic": "extendedStatistic",
        "statistic": "statistic",
        "unit": "unit",
    },
)
class MetricAlarmConfig:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        period: jsii.Number,
        dimensions: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        statistic: typing.Optional["Statistic"] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        '''(deprecated) Properties used to construct the Metric identifying part of an Alarm.

        :param metric_name: (deprecated) Name of the metric.
        :param namespace: (deprecated) Namespace of the metric.
        :param period: (deprecated) How many seconds to aggregate over.
        :param dimensions: (deprecated) The dimensions to apply to the alarm.
        :param extended_statistic: (deprecated) Percentile aggregation function to use.
        :param statistic: (deprecated) Simple aggregation function to use.
        :param unit: (deprecated) The unit of the alarm.

        :deprecated: Replaced by MetricConfig

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            # value: Any
            
            metric_alarm_config = cloudwatch.MetricAlarmConfig(
                metric_name="metricName",
                namespace="namespace",
                period=123,
            
                # the properties below are optional
                dimensions=[cloudwatch.Dimension(
                    name="name",
                    value=value
                )],
                extended_statistic="extendedStatistic",
                statistic=cloudwatch.Statistic.SAMPLE_COUNT,
                unit=cloudwatch.Unit.SECONDS
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6e2cc15f94cac6f392c9e83a6c877bd354a5f78230fc429d5235687f9f0b9b)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument extended_statistic", value=extended_statistic, expected_type=type_hints["extended_statistic"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
            "period": period,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if extended_statistic is not None:
            self._values["extended_statistic"] = extended_statistic
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(deprecated) Name of the metric.

        :stability: deprecated
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''(deprecated) Namespace of the metric.

        :stability: deprecated
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> jsii.Number:
        '''(deprecated) How many seconds to aggregate over.

        :stability: deprecated
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List[Dimension]]:
        '''(deprecated) The dimensions to apply to the alarm.

        :stability: deprecated
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.List[Dimension]], result)

    @builtins.property
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Percentile aggregation function to use.

        :stability: deprecated
        '''
        result = self._values.get("extended_statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistic(self) -> typing.Optional["Statistic"]:
        '''(deprecated) Simple aggregation function to use.

        :stability: deprecated
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional["Statistic"], result)

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        '''(deprecated) The unit of the alarm.

        :stability: deprecated
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional["Unit"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricConfig",
    jsii_struct_bases=[],
    name_mapping={
        "math_expression": "mathExpression",
        "metric_stat": "metricStat",
        "rendering_properties": "renderingProperties",
    },
)
class MetricConfig:
    def __init__(
        self,
        *,
        math_expression: typing.Optional[typing.Union["MetricExpressionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_stat: typing.Optional[typing.Union["MetricStatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        rendering_properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) Properties of a rendered metric.

        :param math_expression: (experimental) In case the metric is a math expression, the details of the math expression. Default: - None
        :param metric_stat: (experimental) In case the metric represents a query, the details of the query. Default: - None
        :param rendering_properties: (experimental) Additional properties which will be rendered if the metric is used in a dashboard. Examples are 'label' and 'color', but any key in here will be added to dashboard graphs. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_cloudwatch as cloudwatch
            
            # duration: monocdk.Duration
            # metric: cloudwatch.Metric
            # rendering_properties: Any
            # value: Any
            
            metric_config = cloudwatch.MetricConfig(
                math_expression=cloudwatch.MetricExpressionConfig(
                    expression="expression",
                    period=123,
                    using_metrics={
                        "using_metrics_key": metric
                    },
            
                    # the properties below are optional
                    search_account="searchAccount",
                    search_region="searchRegion"
                ),
                metric_stat=cloudwatch.MetricStatConfig(
                    metric_name="metricName",
                    namespace="namespace",
                    period=duration,
                    statistic="statistic",
            
                    # the properties below are optional
                    account="account",
                    dimensions=[cloudwatch.Dimension(
                        name="name",
                        value=value
                    )],
                    region="region",
                    unit_filter=cloudwatch.Unit.SECONDS
                ),
                rendering_properties={
                    "rendering_properties_key": rendering_properties
                }
            )
        '''
        if isinstance(math_expression, dict):
            math_expression = MetricExpressionConfig(**math_expression)
        if isinstance(metric_stat, dict):
            metric_stat = MetricStatConfig(**metric_stat)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4456db504977796f6c3432ae050aa6080896c10d5a4dc43ea7014fc6f4876de3)
            check_type(argname="argument math_expression", value=math_expression, expected_type=type_hints["math_expression"])
            check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
            check_type(argname="argument rendering_properties", value=rendering_properties, expected_type=type_hints["rendering_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if math_expression is not None:
            self._values["math_expression"] = math_expression
        if metric_stat is not None:
            self._values["metric_stat"] = metric_stat
        if rendering_properties is not None:
            self._values["rendering_properties"] = rendering_properties

    @builtins.property
    def math_expression(self) -> typing.Optional["MetricExpressionConfig"]:
        '''(experimental) In case the metric is a math expression, the details of the math expression.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("math_expression")
        return typing.cast(typing.Optional["MetricExpressionConfig"], result)

    @builtins.property
    def metric_stat(self) -> typing.Optional["MetricStatConfig"]:
        '''(experimental) In case the metric represents a query, the details of the query.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("metric_stat")
        return typing.cast(typing.Optional["MetricStatConfig"], result)

    @builtins.property
    def rendering_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional properties which will be rendered if the metric is used in a dashboard.

        Examples are 'label' and 'color', but any key in here will be
        added to dashboard graphs.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("rendering_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricExpressionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "period": "period",
        "using_metrics": "usingMetrics",
        "search_account": "searchAccount",
        "search_region": "searchRegion",
    },
)
class MetricExpressionConfig:
    def __init__(
        self,
        *,
        expression: builtins.str,
        period: jsii.Number,
        using_metrics: typing.Mapping[builtins.str, IMetric],
        search_account: typing.Optional[builtins.str] = None,
        search_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a concrete metric.

        :param expression: (experimental) Math expression for the metric.
        :param period: (experimental) How many seconds to aggregate over.
        :param using_metrics: (experimental) Metrics used in the math expression.
        :param search_account: (experimental) Account to evaluate search expressions within. Default: - Deployment account.
        :param search_region: (experimental) Region to evaluate search expressions within. Default: - Deployment region.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            # metric: cloudwatch.Metric
            
            metric_expression_config = cloudwatch.MetricExpressionConfig(
                expression="expression",
                period=123,
                using_metrics={
                    "using_metrics_key": metric
                },
            
                # the properties below are optional
                search_account="searchAccount",
                search_region="searchRegion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8157cb73d47f162e524f16ee12df7244a5f41d979eb72c167bb70b8d118eac)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument using_metrics", value=using_metrics, expected_type=type_hints["using_metrics"])
            check_type(argname="argument search_account", value=search_account, expected_type=type_hints["search_account"])
            check_type(argname="argument search_region", value=search_region, expected_type=type_hints["search_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
            "period": period,
            "using_metrics": using_metrics,
        }
        if search_account is not None:
            self._values["search_account"] = search_account
        if search_region is not None:
            self._values["search_region"] = search_region

    @builtins.property
    def expression(self) -> builtins.str:
        '''(experimental) Math expression for the metric.

        :stability: experimental
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> jsii.Number:
        '''(experimental) How many seconds to aggregate over.

        :stability: experimental
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def using_metrics(self) -> typing.Mapping[builtins.str, IMetric]:
        '''(experimental) Metrics used in the math expression.

        :stability: experimental
        '''
        result = self._values.get("using_metrics")
        assert result is not None, "Required property 'using_metrics' is missing"
        return typing.cast(typing.Mapping[builtins.str, IMetric], result)

    @builtins.property
    def search_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account to evaluate search expressions within.

        :default: - Deployment account.

        :stability: experimental
        '''
        result = self._values.get("search_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region to evaluate search expressions within.

        :default: - Deployment region.

        :stability: experimental
        '''
        result = self._values.get("search_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricExpressionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricGraphConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "namespace": "namespace",
        "period": "period",
        "rendering_properties": "renderingProperties",
        "color": "color",
        "dimensions": "dimensions",
        "label": "label",
        "statistic": "statistic",
        "unit": "unit",
    },
)
class MetricGraphConfig:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        period: jsii.Number,
        rendering_properties: typing.Union["MetricRenderingProperties", typing.Dict[builtins.str, typing.Any]],
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
        label: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        '''(deprecated) Properties used to construct the Metric identifying part of a Graph.

        :param metric_name: (deprecated) Name of the metric.
        :param namespace: (deprecated) Namespace of the metric.
        :param period: (deprecated) How many seconds to aggregate over.
        :param rendering_properties: (deprecated) Rendering properties override yAxis parameter of the widget object.
        :param color: (deprecated) Color for the graph line.
        :param dimensions: (deprecated) The dimensions to apply to the alarm.
        :param label: (deprecated) Label for the metric.
        :param statistic: (deprecated) Aggregation function to use (can be either simple or a percentile).
        :param unit: (deprecated) The unit of the alarm.

        :deprecated: Replaced by MetricConfig

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            # value: Any
            
            metric_graph_config = cloudwatch.MetricGraphConfig(
                metric_name="metricName",
                namespace="namespace",
                period=123,
                rendering_properties=cloudwatch.MetricRenderingProperties(
                    period=123,
            
                    # the properties below are optional
                    color="color",
                    label="label",
                    stat="stat"
                ),
            
                # the properties below are optional
                color="color",
                dimensions=[cloudwatch.Dimension(
                    name="name",
                    value=value
                )],
                label="label",
                statistic="statistic",
                unit=cloudwatch.Unit.SECONDS
            )
        '''
        if isinstance(rendering_properties, dict):
            rendering_properties = MetricRenderingProperties(**rendering_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4216a0e537c421715a3df848babe18bf684e87b4f1646df51ebc2f18ce38c70c)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument rendering_properties", value=rendering_properties, expected_type=type_hints["rendering_properties"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
            "period": period,
            "rendering_properties": rendering_properties,
        }
        if color is not None:
            self._values["color"] = color
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if label is not None:
            self._values["label"] = label
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(deprecated) Name of the metric.

        :stability: deprecated
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''(deprecated) Namespace of the metric.

        :stability: deprecated
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> jsii.Number:
        '''(deprecated) How many seconds to aggregate over.

        :deprecated: Use ``period`` in ``renderingProperties``

        :stability: deprecated
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rendering_properties(self) -> "MetricRenderingProperties":
        '''(deprecated) Rendering properties override yAxis parameter of the widget object.

        :stability: deprecated
        '''
        result = self._values.get("rendering_properties")
        assert result is not None, "Required property 'rendering_properties' is missing"
        return typing.cast("MetricRenderingProperties", result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Color for the graph line.

        :deprecated: Use ``color`` in ``renderingProperties``

        :stability: deprecated
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List[Dimension]]:
        '''(deprecated) The dimensions to apply to the alarm.

        :stability: deprecated
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.List[Dimension]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Label for the metric.

        :deprecated: Use ``label`` in ``renderingProperties``

        :stability: deprecated
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Aggregation function to use (can be either simple or a percentile).

        :deprecated: Use ``stat`` in ``renderingProperties``

        :stability: deprecated
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        '''(deprecated) The unit of the alarm.

        :deprecated: not used in dashboard widgets

        :stability: deprecated
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional["Unit"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricGraphConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricOptions",
    jsii_struct_bases=[CommonMetricOptions],
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
    },
)
class MetricOptions(CommonMetricOptions):
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
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        '''(experimental) Properties of a metric that can be changed.

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
        :exampleMetadata: infused

        Example::

            import monocdk as cloudwatch
            # delivery_stream: firehose.DeliveryStream
            
            
            # Alarm that triggers when the per-second average of incoming bytes exceeds 90% of the current service limit
            incoming_bytes_percent_of_limit = cloudwatch.MathExpression(
                expression="incomingBytes / 300 / bytePerSecLimit",
                using_metrics={
                    "incoming_bytes": delivery_stream.metric_incoming_bytes(statistic=cloudwatch.Statistic.SUM),
                    "byte_per_sec_limit": delivery_stream.metric("BytesPerSecondLimit")
                }
            )
            
            cloudwatch.Alarm(self, "Alarm",
                metric=incoming_bytes_percent_of_limit,
                threshold=0.9,
                evaluation_periods=3
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaddf80d4cf1272cabcfaa9b11044f2fcfe5e0313dcf2fe288425fdc3c0218d)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument dimensions_map", value=dimensions_map, expected_type=type_hints["dimensions_map"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
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
    def unit(self) -> typing.Optional["Unit"]:
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
        return typing.cast(typing.Optional["Unit"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricProps",
    jsii_struct_bases=[CommonMetricOptions],
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
        "metric_name": "metricName",
        "namespace": "namespace",
    },
)
class MetricProps(CommonMetricOptions):
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
        unit: typing.Optional["Unit"] = None,
        metric_name: builtins.str,
        namespace: builtins.str,
    ) -> None:
        '''(experimental) Properties for a metric.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param metric_name: (experimental) Name of the metric.
        :param namespace: (experimental) Namespace of the metric.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            hosted_zone = route53.HostedZone(self, "MyHostedZone", zone_name="example.org")
            metric = cloudwatch.Metric(
                namespace="AWS/Route53",
                metric_name="DNSQueries",
                dimensions_map={
                    "HostedZoneId": hosted_zone.hosted_zone_id
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b483b4310a80d19c72c15ad3ed43f149d986b65b4e8082b6752f479be1f2ab)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument dimensions_map", value=dimensions_map, expected_type=type_hints["dimensions_map"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
        }
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
    def unit(self) -> typing.Optional["Unit"]:
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
        return typing.cast(typing.Optional["Unit"], result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(experimental) Name of the metric.

        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''(experimental) Namespace of the metric.

        :stability: experimental
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricRenderingProperties",
    jsii_struct_bases=[],
    name_mapping={
        "period": "period",
        "color": "color",
        "label": "label",
        "stat": "stat",
    },
)
class MetricRenderingProperties:
    def __init__(
        self,
        *,
        period: jsii.Number,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        stat: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(deprecated) Custom rendering properties that override the default rendering properties specified in the yAxis parameter of the widget object.

        :param period: (deprecated) How many seconds to aggregate over.
        :param color: (deprecated) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.
        :param label: (deprecated) Label for the metric.
        :param stat: (deprecated) Aggregation function to use (can be either simple or a percentile).

        :deprecated: Replaced by MetricConfig.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            metric_rendering_properties = cloudwatch.MetricRenderingProperties(
                period=123,
            
                # the properties below are optional
                color="color",
                label="label",
                stat="stat"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5559662d3f9c667a0baa7f01117ec758df4bb96b61e3617ee49d424d050bbc2e)
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "period": period,
        }
        if color is not None:
            self._values["color"] = color
        if label is not None:
            self._values["label"] = label
        if stat is not None:
            self._values["stat"] = stat

    @builtins.property
    def period(self) -> jsii.Number:
        '''(deprecated) How many seconds to aggregate over.

        :stability: deprecated
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.

        :stability: deprecated
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Label for the metric.

        :stability: deprecated
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stat(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Aggregation function to use (can be either simple or a percentile).

        :stability: deprecated
        '''
        result = self._values.get("stat")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricRenderingProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricStatConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "namespace": "namespace",
        "period": "period",
        "statistic": "statistic",
        "account": "account",
        "dimensions": "dimensions",
        "region": "region",
        "unit_filter": "unitFilter",
    },
)
class MetricStatConfig:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        period: _Duration_070aa057,
        statistic: builtins.str,
        account: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
        region: typing.Optional[builtins.str] = None,
        unit_filter: typing.Optional["Unit"] = None,
    ) -> None:
        '''(experimental) Properties for a concrete metric.

        NOTE: ``unit`` is no longer on this object since it is only used for ``Alarms``, and doesn't mean what one
        would expect it to mean there anyway. It is most likely to be misused.

        :param metric_name: (experimental) Name of the metric.
        :param namespace: (experimental) Namespace of the metric.
        :param period: (experimental) How many seconds to aggregate over.
        :param statistic: (experimental) Aggregation function to use (can be either simple or a percentile).
        :param account: (experimental) Account which this metric comes from. Default: Deployment account.
        :param dimensions: (experimental) The dimensions to apply to the alarm. Default: []
        :param region: (experimental) Region which this metric comes from. Default: Deployment region.
        :param unit_filter: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. This field has been renamed from plain ``unit`` to clearly communicate its purpose. Default: - Refer to all metric datums

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_cloudwatch as cloudwatch
            
            # duration: monocdk.Duration
            # value: Any
            
            metric_stat_config = cloudwatch.MetricStatConfig(
                metric_name="metricName",
                namespace="namespace",
                period=duration,
                statistic="statistic",
            
                # the properties below are optional
                account="account",
                dimensions=[cloudwatch.Dimension(
                    name="name",
                    value=value
                )],
                region="region",
                unit_filter=cloudwatch.Unit.SECONDS
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb362e6c7d6246bb6929f8a40cd4d977bcd0756ded8b7ddcd5af8250555ef3d)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument unit_filter", value=unit_filter, expected_type=type_hints["unit_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
            "period": period,
            "statistic": statistic,
        }
        if account is not None:
            self._values["account"] = account
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if region is not None:
            self._values["region"] = region
        if unit_filter is not None:
            self._values["unit_filter"] = unit_filter

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(experimental) Name of the metric.

        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''(experimental) Namespace of the metric.

        :stability: experimental
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> _Duration_070aa057:
        '''(experimental) How many seconds to aggregate over.

        :stability: experimental
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(_Duration_070aa057, result)

    @builtins.property
    def statistic(self) -> builtins.str:
        '''(experimental) Aggregation function to use (can be either simple or a percentile).

        :stability: experimental
        '''
        result = self._values.get("statistic")
        assert result is not None, "Required property 'statistic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account which this metric comes from.

        :default: Deployment account.

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List[Dimension]]:
        '''(experimental) The dimensions to apply to the alarm.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.List[Dimension]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region which this metric comes from.

        :default: Deployment region.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unit_filter(self) -> typing.Optional["Unit"]:
        '''(experimental) Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        This field has been renamed from plain ``unit`` to clearly communicate
        its purpose.

        :default: - Refer to all metric datums

        :stability: experimental
        '''
        result = self._values.get("unit_filter")
        return typing.cast(typing.Optional["Unit"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricStatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.MetricWidgetProps",
    jsii_struct_bases=[],
    name_mapping={
        "height": "height",
        "region": "region",
        "title": "title",
        "width": "width",
    },
)
class MetricWidgetProps:
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Basic properties for widgets that display metrics.

        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: (experimental) The region the metrics of this graph should be taken from. Default: - Current region
        :param title: (experimental) Title for the graph. Default: - None
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            metric_widget_props = cloudwatch.MetricWidgetProps(
                height=123,
                region="region",
                title="title",
                width=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95974eb9f925ab06f8175ddb989bbbd09174cb4e49b5b5275245a99d1dad9d32)
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if height is not None:
            self._values["height"] = height
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region the metrics of this graph should be taken from.

        :default: - Current region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''(experimental) Title for the graph.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the widget, in a grid of 24 units wide.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.PeriodOverride")
class PeriodOverride(enum.Enum):
    '''(experimental) Specify the period for graphs when the CloudWatch dashboard loads.

    :stability: experimental
    '''

    AUTO = "AUTO"
    '''(experimental) Period of all graphs on the dashboard automatically adapt to the time range of the dashboard.

    :stability: experimental
    '''
    INHERIT = "INHERIT"
    '''(experimental) Period set for each graph will be used.

    :stability: experimental
    '''


@jsii.implements(IWidget)
class Row(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_cloudwatch.Row"):
    '''(experimental) A widget that contains other widgets in a horizontal row.

    Widgets will be laid out next to each other

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        # widget: cloudwatch.IWidget
        
        row = cloudwatch.Row(widget)
    '''

    def __init__(self, *widgets: IWidget) -> None:
        '''
        :param widgets: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142011a6d7a20eace51da73490abef3d99af35dc0ad07dc8d0e31e2a50790e63)
            check_type(argname="argument widgets", value=widgets, expected_type=typing.Tuple[type_hints["widgets"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        '''(experimental) Place the widget at a given position.

        :param x: -
        :param y: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6c8e4c956f00058a4800dcd7797588e2882f0b9812c3bfa638694239d14e06)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        return typing.cast(None, jsii.invoke(self, "position", [x, y]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        '''(experimental) The amount of vertical grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @builtins.property
    @jsii.member(jsii_name="widgets")
    def widgets(self) -> typing.List[IWidget]:
        '''(experimental) List of contained widgets.

        :stability: experimental
        '''
        return typing.cast(typing.List[IWidget], jsii.get(self, "widgets"))

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        '''(experimental) The amount of horizontal grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "width"))


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.Shading")
class Shading(enum.Enum):
    '''(experimental) Fill shading options that will be used with an annotation.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) Don't add shading.

    :stability: experimental
    '''
    ABOVE = "ABOVE"
    '''(experimental) Add shading above the annotation.

    :stability: experimental
    '''
    BELOW = "BELOW"
    '''(experimental) Add shading below the annotation.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.SingleValueWidgetProps",
    jsii_struct_bases=[MetricWidgetProps],
    name_mapping={
        "height": "height",
        "region": "region",
        "title": "title",
        "width": "width",
        "metrics": "metrics",
        "full_precision": "fullPrecision",
        "set_period_to_time_range": "setPeriodToTimeRange",
    },
)
class SingleValueWidgetProps(MetricWidgetProps):
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        metrics: typing.Sequence[IMetric],
        full_precision: typing.Optional[builtins.bool] = None,
        set_period_to_time_range: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for a SingleValueWidget.

        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: (experimental) The region the metrics of this graph should be taken from. Default: - Current region
        :param title: (experimental) Title for the graph. Default: - None
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6
        :param metrics: (experimental) Metrics to display.
        :param full_precision: (experimental) Whether to show as many digits as can fit, before rounding. Default: false
        :param set_period_to_time_range: (experimental) Whether to show the value from the entire time range. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # dashboard: cloudwatch.Dashboard
            # visitor_count: cloudwatch.Metric
            # purchase_count: cloudwatch.Metric
            
            
            dashboard.add_widgets(cloudwatch.SingleValueWidget(
                metrics=[visitor_count, purchase_count]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e86eb4a8643de80d4d70ec06fab477568088cb9144a8fab5da2c58452540a9)
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument full_precision", value=full_precision, expected_type=type_hints["full_precision"])
            check_type(argname="argument set_period_to_time_range", value=set_period_to_time_range, expected_type=type_hints["set_period_to_time_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metrics": metrics,
        }
        if height is not None:
            self._values["height"] = height
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width
        if full_precision is not None:
            self._values["full_precision"] = full_precision
        if set_period_to_time_range is not None:
            self._values["set_period_to_time_range"] = set_period_to_time_range

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region the metrics of this graph should be taken from.

        :default: - Current region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''(experimental) Title for the graph.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the widget, in a grid of 24 units wide.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metrics(self) -> typing.List[IMetric]:
        '''(experimental) Metrics to display.

        :stability: experimental
        '''
        result = self._values.get("metrics")
        assert result is not None, "Required property 'metrics' is missing"
        return typing.cast(typing.List[IMetric], result)

    @builtins.property
    def full_precision(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to show as many digits as can fit, before rounding.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("full_precision")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def set_period_to_time_range(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to show the value from the entire time range.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("set_period_to_time_range")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SingleValueWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWidget)
class Spacer(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_cloudwatch.Spacer"):
    '''(experimental) A widget that doesn't display anything but takes up space.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        spacer = cloudwatch.Spacer(
            height=123,
            width=123
        )
    '''

    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param height: (experimental) Height of the spacer. Default: : 1
        :param width: (experimental) Width of the spacer. Default: 1

        :stability: experimental
        '''
        props = SpacerProps(height=height, width=width)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, _x: jsii.Number, _y: jsii.Number) -> None:
        '''(experimental) Place the widget at a given position.

        :param _x: -
        :param _y: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017b8501dabf7f830fb059a6c1f3eb58b177dde1df4d76f72a7d7fc624c08bce)
            check_type(argname="argument _x", value=_x, expected_type=type_hints["_x"])
            check_type(argname="argument _y", value=_y, expected_type=type_hints["_y"])
        return typing.cast(None, jsii.invoke(self, "position", [_x, _y]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        '''(experimental) The amount of vertical grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        '''(experimental) The amount of horizontal grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "width"))


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.SpacerProps",
    jsii_struct_bases=[],
    name_mapping={"height": "height", "width": "width"},
)
class SpacerProps:
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Props of the spacer.

        :param height: (experimental) Height of the spacer. Default: : 1
        :param width: (experimental) Width of the spacer. Default: 1

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            spacer_props = cloudwatch.SpacerProps(
                height=123,
                width=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1507df7e5f90646ca07bde07f8874ca5c43d66f2186310556a4d7e1e067079c3)
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if height is not None:
            self._values["height"] = height
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the spacer.

        :default: : 1

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the spacer.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpacerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.Statistic")
class Statistic(enum.Enum):
    '''(experimental) Statistic to use over the aggregation period.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cloudwatch
        # delivery_stream: firehose.DeliveryStream
        
        
        # Alarm that triggers when the per-second average of incoming bytes exceeds 90% of the current service limit
        incoming_bytes_percent_of_limit = cloudwatch.MathExpression(
            expression="incomingBytes / 300 / bytePerSecLimit",
            using_metrics={
                "incoming_bytes": delivery_stream.metric_incoming_bytes(statistic=cloudwatch.Statistic.SUM),
                "byte_per_sec_limit": delivery_stream.metric("BytesPerSecondLimit")
            }
        )
        
        cloudwatch.Alarm(self, "Alarm",
            metric=incoming_bytes_percent_of_limit,
            threshold=0.9,
            evaluation_periods=3
        )
    '''

    SAMPLE_COUNT = "SAMPLE_COUNT"
    '''(experimental) The count (number) of data points used for the statistical calculation.

    :stability: experimental
    '''
    AVERAGE = "AVERAGE"
    '''(experimental) The value of Sum / SampleCount during the specified period.

    :stability: experimental
    '''
    SUM = "SUM"
    '''(experimental) All values submitted for the matching metric added together.

    This statistic can be useful for determining the total volume of a metric.

    :stability: experimental
    '''
    MINIMUM = "MINIMUM"
    '''(experimental) The lowest value observed during the specified period.

    You can use this value to determine low volumes of activity for your application.

    :stability: experimental
    '''
    MAXIMUM = "MAXIMUM"
    '''(experimental) The highest value observed during the specified period.

    You can use this value to determine high volumes of activity for your application.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.TextWidgetProps",
    jsii_struct_bases=[],
    name_mapping={"markdown": "markdown", "height": "height", "width": "width"},
)
class TextWidgetProps:
    def __init__(
        self,
        *,
        markdown: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for a Text widget.

        :param markdown: (experimental) The text to display, in MarkDown format.
        :param height: (experimental) Height of the widget. Default: 2
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # dashboard: cloudwatch.Dashboard
            
            
            dashboard.add_widgets(cloudwatch.TextWidget(
                markdown="# Key Performance Indicators"
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ff7e3019985b4f604cec265a08f66c64e8a61cf937357d3a593827b75ef386)
            check_type(argname="argument markdown", value=markdown, expected_type=type_hints["markdown"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "markdown": markdown,
        }
        if height is not None:
            self._values["height"] = height
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def markdown(self) -> builtins.str:
        '''(experimental) The text to display, in MarkDown format.

        :stability: experimental
        '''
        result = self._values.get("markdown")
        assert result is not None, "Required property 'markdown' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the widget.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the widget, in a grid of 24 units wide.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.TreatMissingData")
class TreatMissingData(enum.Enum):
    '''(experimental) Specify how missing data points are treated during alarm evaluation.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cdk
        import monocdk as cloudwatch
        
        
        fn = lambda_.Function(self, "MyFunction",
            runtime=lambda_.Runtime.NODEJS_16_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            timeout=cdk.Duration.minutes(5)
        )
        
        if fn.timeout:
            cloudwatch.Alarm(self, "MyAlarm",
                metric=fn.metric_duration().with(
                    statistic="Maximum"
                ),
                evaluation_periods=1,
                datapoints_to_alarm=1,
                threshold=fn.timeout.to_milliseconds(),
                treat_missing_data=cloudwatch.TreatMissingData.IGNORE,
                alarm_name="My Lambda Timeout"
            )
    '''

    BREACHING = "BREACHING"
    '''(experimental) Missing data points are treated as breaching the threshold.

    :stability: experimental
    '''
    NOT_BREACHING = "NOT_BREACHING"
    '''(experimental) Missing data points are treated as being within the threshold.

    :stability: experimental
    '''
    IGNORE = "IGNORE"
    '''(experimental) The current alarm state is maintained.

    :stability: experimental
    '''
    MISSING = "MISSING"
    '''(experimental) The alarm does not consider missing data points when evaluating whether to change state.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_cloudwatch.Unit")
class Unit(enum.Enum):
    '''(experimental) Unit for metric.

    :stability: experimental
    '''

    SECONDS = "SECONDS"
    '''(experimental) Seconds.

    :stability: experimental
    '''
    MICROSECONDS = "MICROSECONDS"
    '''(experimental) Microseconds.

    :stability: experimental
    '''
    MILLISECONDS = "MILLISECONDS"
    '''(experimental) Milliseconds.

    :stability: experimental
    '''
    BYTES = "BYTES"
    '''(experimental) Bytes.

    :stability: experimental
    '''
    KILOBYTES = "KILOBYTES"
    '''(experimental) Kilobytes.

    :stability: experimental
    '''
    MEGABYTES = "MEGABYTES"
    '''(experimental) Megabytes.

    :stability: experimental
    '''
    GIGABYTES = "GIGABYTES"
    '''(experimental) Gigabytes.

    :stability: experimental
    '''
    TERABYTES = "TERABYTES"
    '''(experimental) Terabytes.

    :stability: experimental
    '''
    BITS = "BITS"
    '''(experimental) Bits.

    :stability: experimental
    '''
    KILOBITS = "KILOBITS"
    '''(experimental) Kilobits.

    :stability: experimental
    '''
    MEGABITS = "MEGABITS"
    '''(experimental) Megabits.

    :stability: experimental
    '''
    GIGABITS = "GIGABITS"
    '''(experimental) Gigabits.

    :stability: experimental
    '''
    TERABITS = "TERABITS"
    '''(experimental) Terabits.

    :stability: experimental
    '''
    PERCENT = "PERCENT"
    '''(experimental) Percent.

    :stability: experimental
    '''
    COUNT = "COUNT"
    '''(experimental) Count.

    :stability: experimental
    '''
    BYTES_PER_SECOND = "BYTES_PER_SECOND"
    '''(experimental) Bytes/second (B/s).

    :stability: experimental
    '''
    KILOBYTES_PER_SECOND = "KILOBYTES_PER_SECOND"
    '''(experimental) Kilobytes/second (kB/s).

    :stability: experimental
    '''
    MEGABYTES_PER_SECOND = "MEGABYTES_PER_SECOND"
    '''(experimental) Megabytes/second (MB/s).

    :stability: experimental
    '''
    GIGABYTES_PER_SECOND = "GIGABYTES_PER_SECOND"
    '''(experimental) Gigabytes/second (GB/s).

    :stability: experimental
    '''
    TERABYTES_PER_SECOND = "TERABYTES_PER_SECOND"
    '''(experimental) Terabytes/second (TB/s).

    :stability: experimental
    '''
    BITS_PER_SECOND = "BITS_PER_SECOND"
    '''(experimental) Bits/second (b/s).

    :stability: experimental
    '''
    KILOBITS_PER_SECOND = "KILOBITS_PER_SECOND"
    '''(experimental) Kilobits/second (kb/s).

    :stability: experimental
    '''
    MEGABITS_PER_SECOND = "MEGABITS_PER_SECOND"
    '''(experimental) Megabits/second (Mb/s).

    :stability: experimental
    '''
    GIGABITS_PER_SECOND = "GIGABITS_PER_SECOND"
    '''(experimental) Gigabits/second (Gb/s).

    :stability: experimental
    '''
    TERABITS_PER_SECOND = "TERABITS_PER_SECOND"
    '''(experimental) Terabits/second (Tb/s).

    :stability: experimental
    '''
    COUNT_PER_SECOND = "COUNT_PER_SECOND"
    '''(experimental) Count/second.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) None.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.YAxisProps",
    jsii_struct_bases=[],
    name_mapping={
        "label": "label",
        "max": "max",
        "min": "min",
        "show_units": "showUnits",
    },
)
class YAxisProps:
    def __init__(
        self,
        *,
        label: typing.Optional[builtins.str] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        show_units: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for a Y-Axis.

        :param label: (experimental) The label. Default: - No label
        :param max: (experimental) The max value. Default: - No maximum value
        :param min: (experimental) The min value. Default: 0
        :param show_units: (experimental) Whether to show units. Default: true

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudwatch as cloudwatch
            
            y_axis_props = cloudwatch.YAxisProps(
                label="label",
                max=123,
                min=123,
                show_units=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f240bcbea86f9e713bc00f2859125c57a987ccf88c1b3681c2c600755ab120)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument show_units", value=show_units, expected_type=type_hints["show_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if label is not None:
            self._values["label"] = label
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min
        if show_units is not None:
            self._values["show_units"] = show_units

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(experimental) The label.

        :default: - No label

        :stability: experimental
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The max value.

        :default: - No maximum value

        :stability: experimental
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The min value.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def show_units(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to show units.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("show_units")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YAxisProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.AlarmProps",
    jsii_struct_bases=[CreateAlarmOptions],
    name_mapping={
        "evaluation_periods": "evaluationPeriods",
        "threshold": "threshold",
        "actions_enabled": "actionsEnabled",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "comparison_operator": "comparisonOperator",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluate_low_sample_count_percentile": "evaluateLowSampleCountPercentile",
        "period": "period",
        "statistic": "statistic",
        "treat_missing_data": "treatMissingData",
        "metric": "metric",
    },
)
class AlarmProps(CreateAlarmOptions):
    def __init__(
        self,
        *,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[TreatMissingData] = None,
        metric: IMetric,
    ) -> None:
        '''(experimental) Properties for Alarms.

        :param evaluation_periods: (experimental) The number of periods over which data is compared to the specified threshold.
        :param threshold: (experimental) The value against which the specified statistic is compared.
        :param actions_enabled: (experimental) Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: (experimental) Description for the alarm. Default: No description
        :param alarm_name: (experimental) Name of the alarm. Default: Automatically generated name
        :param comparison_operator: (experimental) Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: (experimental) The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: (experimental) Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: (experimental) Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        :param metric: (experimental) The metric to add the alarm on. Metric objects can be obtained from most resources, or you can construct custom Metric objects by instantiating one.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as cloudwatch
            
            # alias: lambda.Alias
            
            # or add alarms to an existing group
            # blue_green_alias: lambda.Alias
            
            alarm = cloudwatch.Alarm(self, "Errors",
                comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=1,
                evaluation_periods=1,
                metric=alias.metric_errors()
            )
            deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
                alias=alias,
                deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
                alarms=[alarm
                ]
            )
            deployment_group.add_alarm(cloudwatch.Alarm(self, "BlueGreenErrors",
                comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=1,
                evaluation_periods=1,
                metric=blue_green_alias.metric_errors()
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39c05d2740897b5c8c39250be68575247dbd4c00909bb417c760dd8beaf633f)
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument actions_enabled", value=actions_enabled, expected_type=type_hints["actions_enabled"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluate_low_sample_count_percentile", value=evaluate_low_sample_count_percentile, expected_type=type_hints["evaluate_low_sample_count_percentile"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "evaluation_periods": evaluation_periods,
            "threshold": threshold,
            "metric": metric,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if comparison_operator is not None:
            self._values["comparison_operator"] = comparison_operator
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluate_low_sample_count_percentile is not None:
            self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if period is not None:
            self._values["period"] = period
        if statistic is not None:
            self._values["statistic"] = statistic
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        '''(experimental) The number of periods over which data is compared to the specified threshold.

        :stability: experimental
        '''
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''(experimental) The value against which the specified statistic is compared.

        :stability: experimental
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def actions_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the actions for this alarm are enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("actions_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for the alarm.

        :default: No description

        :stability: experimental
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the alarm.

        :default: Automatically generated name

        :stability: experimental
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comparison_operator(self) -> typing.Optional[ComparisonOperator]:
        '''(experimental) Comparison to use to check if metric is breaching.

        :default: GreaterThanOrEqualToThreshold

        :stability: experimental
        '''
        result = self._values.get("comparison_operator")
        return typing.cast(typing.Optional[ComparisonOperator], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M
        out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon
        CloudWatch User Guide.

        :default: ``evaluationPeriods``

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation
        :stability: experimental
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant.

        Used only for alarms that are based on percentiles.

        :default: - Not configured.

        :stability: experimental
        '''
        result = self._values.get("evaluate_low_sample_count_percentile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period(self) -> typing.Optional[_Duration_070aa057]:
        '''(deprecated) The period over which the specified statistic is applied.

        Cannot be used with ``MathExpression`` objects.

        :default: - The period from the metric

        :deprecated: Use ``metric.with({ period: ... })`` to encode the period into the Metric object

        :stability: deprecated
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''(deprecated) What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        Cannot be used with ``MathExpression`` objects.

        :default: - The statistic from the metric

        :deprecated: Use ``metric.with({ statistic: ... })`` to encode the period into the Metric object

        :stability: deprecated
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def treat_missing_data(self) -> typing.Optional[TreatMissingData]:
        '''(experimental) Sets how this alarm is to handle missing data points.

        :default: TreatMissingData.Missing

        :stability: experimental
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[TreatMissingData], result)

    @builtins.property
    def metric(self) -> IMetric:
        '''(experimental) The metric to add the alarm on.

        Metric objects can be obtained from most resources, or you can construct
        custom Metric objects by instantiating one.

        :stability: experimental
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast(IMetric, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.AlarmWidgetProps",
    jsii_struct_bases=[MetricWidgetProps],
    name_mapping={
        "height": "height",
        "region": "region",
        "title": "title",
        "width": "width",
        "alarm": "alarm",
        "left_y_axis": "leftYAxis",
    },
)
class AlarmWidgetProps(MetricWidgetProps):
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        alarm: "IAlarm",
        left_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for an AlarmWidget.

        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: (experimental) The region the metrics of this graph should be taken from. Default: - Current region
        :param title: (experimental) Title for the graph. Default: - None
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6
        :param alarm: (experimental) The alarm to show.
        :param left_y_axis: (experimental) Left Y axis. Default: - No minimum or maximum values for the left Y-axis

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # dashboard: cloudwatch.Dashboard
            # error_alarm: cloudwatch.Alarm
            
            
            dashboard.add_widgets(cloudwatch.AlarmWidget(
                title="Errors",
                alarm=error_alarm
            ))
        '''
        if isinstance(left_y_axis, dict):
            left_y_axis = YAxisProps(**left_y_axis)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2bd39a483140a25a960dc7ecf83a4356cfd98780979b71f6c4422d5e9f72cb)
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
            check_type(argname="argument left_y_axis", value=left_y_axis, expected_type=type_hints["left_y_axis"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm": alarm,
        }
        if height is not None:
            self._values["height"] = height
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width
        if left_y_axis is not None:
            self._values["left_y_axis"] = left_y_axis

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region the metrics of this graph should be taken from.

        :default: - Current region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''(experimental) Title for the graph.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the widget, in a grid of 24 units wide.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alarm(self) -> "IAlarm":
        '''(experimental) The alarm to show.

        :stability: experimental
        '''
        result = self._values.get("alarm")
        assert result is not None, "Required property 'alarm' is missing"
        return typing.cast("IAlarm", result)

    @builtins.property
    def left_y_axis(self) -> typing.Optional[YAxisProps]:
        '''(experimental) Left Y axis.

        :default: - No minimum or maximum values for the left Y-axis

        :stability: experimental
        '''
        result = self._values.get("left_y_axis")
        return typing.cast(typing.Optional[YAxisProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWidget)
class Column(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_cloudwatch.Column"):
    '''(experimental) A widget that contains other widgets in a vertical column.

    Widgets will be laid out next to each other

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudwatch as cloudwatch
        
        # widget: cloudwatch.IWidget
        
        column = cloudwatch.Column(widget)
    '''

    def __init__(self, *widgets: IWidget) -> None:
        '''
        :param widgets: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3c393a65c4e2cf70d4f2c5f930039e13cce8a89d9eb12b109fba7d39b9f304)
            check_type(argname="argument widgets", value=widgets, expected_type=typing.Tuple[type_hints["widgets"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        '''(experimental) Place the widget at a given position.

        :param x: -
        :param y: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab7f8e7820f55a8cd5c0182608aa686a5e98839b19ebd713716d34364b0d31c)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        return typing.cast(None, jsii.invoke(self, "position", [x, y]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        '''(experimental) The amount of vertical grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @builtins.property
    @jsii.member(jsii_name="widgets")
    def widgets(self) -> typing.List[IWidget]:
        '''(experimental) List of contained widgets.

        :stability: experimental
        '''
        return typing.cast(typing.List[IWidget], jsii.get(self, "widgets"))

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        '''(experimental) The amount of horizontal grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "width"))


@jsii.implements(IWidget)
class ConcreteWidget(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_cloudwatch.ConcreteWidget",
):
    '''(experimental) A real CloudWatch widget that has its own fixed size and remembers its position.

    This is in contrast to other widgets which exist for layout purposes.

    :stability: experimental
    '''

    def __init__(self, width: jsii.Number, height: jsii.Number) -> None:
        '''
        :param width: -
        :param height: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c46b69ee54330b8ccf9902e9ebf08b2e5eccd53372f96bdbb75a384a4ae21d)
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
        jsii.create(self.__class__, self, [width, height])

    @jsii.member(jsii_name="copyMetricWarnings")
    def _copy_metric_warnings(self, *ms: IMetric) -> None:
        '''(experimental) Copy the warnings from the given metric.

        :param ms: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea1a37d58cd01cde16416cf22a3b75e3abf7cd702c146be2451137da54473ae)
            check_type(argname="argument ms", value=ms, expected_type=typing.Tuple[type_hints["ms"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "copyMetricWarnings", [*ms]))

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        '''(experimental) Place the widget at a given position.

        :param x: -
        :param y: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71446f487f91a003cac597c54103a2ca236ae040a7cd21570da4debb34a9e4e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        return typing.cast(None, jsii.invoke(self, "position", [x, y]))

    @jsii.member(jsii_name="toJson")
    @abc.abstractmethod
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        '''(experimental) The amount of vertical grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        '''(experimental) The amount of horizontal grid units the widget will take up.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Any warnings that are produced as a result of putting together this widget.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "warnings"))

    @builtins.property
    @jsii.member(jsii_name="x")
    def _x(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "x"))

    @_x.setter
    def _x(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0249aad8cb00d8d0a8264c7fbeb34d056c4b91c7ccaca87664369c10af84b48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x", value)

    @builtins.property
    @jsii.member(jsii_name="y")
    def _y(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "y"))

    @_y.setter
    def _y(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96f2e543cbdea06e53d57bf90e303d06ef7fbca0828060f297881d41d4a7728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "y", value)


class _ConcreteWidgetProxy(ConcreteWidget):
    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ConcreteWidget).__jsii_proxy_class__ = lambda : _ConcreteWidgetProxy


class CustomWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.CustomWidget",
):
    '''(experimental) A CustomWidget shows the result of a AWS lambda function.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        
        
        # Import or create a lambda function
        fn = lambda_.Function.from_function_arn(dashboard, "Function", "arn:aws:lambda:us-east-1:123456789012:function:MyFn")
        
        dashboard.add_widgets(cloudwatch.CustomWidget(
            function_arn=fn.function_arn,
            title="My lambda baked widget"
        ))
    '''

    def __init__(
        self,
        *,
        function_arn: builtins.str,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        params: typing.Any = None,
        update_on_refresh: typing.Optional[builtins.bool] = None,
        update_on_resize: typing.Optional[builtins.bool] = None,
        update_on_time_range_change: typing.Optional[builtins.bool] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function_arn: (experimental) The Arn of the AWS Lambda function that returns HTML or JSON that will be displayed in the widget.
        :param title: (experimental) The title of the widget.
        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param params: (experimental) Parameters passed to the lambda function. Default: - no parameters are passed to the lambda function
        :param update_on_refresh: (experimental) Update the widget on refresh. Default: true
        :param update_on_resize: (experimental) Update the widget on resize. Default: true
        :param update_on_time_range_change: (experimental) Update the widget on time range change. Default: true
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        '''
        props = CustomWidgetProps(
            function_arn=function_arn,
            title=title,
            height=height,
            params=params,
            update_on_refresh=update_on_refresh,
            update_on_resize=update_on_resize,
            update_on_time_range_change=update_on_time_range_change,
            width=width,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))


class GraphWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.GraphWidget",
):
    '''(experimental) A dashboard widget that displays metrics.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        
        
        dashboard.add_widgets(cloudwatch.GraphWidget(
            # ...
        
            legend_position=cloudwatch.LegendPosition.RIGHT
        ))
    '''

    def __init__(
        self,
        *,
        left: typing.Optional[typing.Sequence[IMetric]] = None,
        left_annotations: typing.Optional[typing.Sequence[typing.Union[HorizontalAnnotation, typing.Dict[builtins.str, typing.Any]]]] = None,
        left_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
        legend_position: typing.Optional[LegendPosition] = None,
        live_data: typing.Optional[builtins.bool] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        right: typing.Optional[typing.Sequence[IMetric]] = None,
        right_annotations: typing.Optional[typing.Sequence[typing.Union[HorizontalAnnotation, typing.Dict[builtins.str, typing.Any]]]] = None,
        right_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
        set_period_to_time_range: typing.Optional[builtins.bool] = None,
        stacked: typing.Optional[builtins.bool] = None,
        statistic: typing.Optional[builtins.str] = None,
        view: typing.Optional[GraphWidgetView] = None,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param left: (experimental) Metrics to display on left Y axis. Default: - No metrics
        :param left_annotations: (experimental) Annotations for the left Y axis. Default: - No annotations
        :param left_y_axis: (experimental) Left Y axis. Default: - None
        :param legend_position: (experimental) Position of the legend. Default: - bottom
        :param live_data: (experimental) Whether the graph should show live data. Default: false
        :param period: (experimental) The default period for all metrics in this widget. The period is the length of time represented by one data point on the graph. This default can be overridden within each metric definition. Default: cdk.Duration.seconds(300)
        :param right: (experimental) Metrics to display on right Y axis. Default: - No metrics
        :param right_annotations: (experimental) Annotations for the right Y axis. Default: - No annotations
        :param right_y_axis: (experimental) Right Y axis. Default: - None
        :param set_period_to_time_range: (experimental) Whether to show the value from the entire time range. Only applicable for Bar and Pie charts. If false, values will be from the most recent period of your chosen time range; if true, shows the value from the entire time range. Default: false
        :param stacked: (experimental) Whether the graph should be shown as stacked lines. Default: false
        :param statistic: (experimental) The default statistic to be displayed for each metric. This default can be overridden within the definition of each individual metric Default: - The statistic for each metric is used
        :param view: (experimental) Display this metric. Default: TimeSeries
        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: (experimental) The region the metrics of this graph should be taken from. Default: - Current region
        :param title: (experimental) Title for the graph. Default: - None
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        '''
        props = GraphWidgetProps(
            left=left,
            left_annotations=left_annotations,
            left_y_axis=left_y_axis,
            legend_position=legend_position,
            live_data=live_data,
            period=period,
            right=right,
            right_annotations=right_annotations,
            right_y_axis=right_y_axis,
            set_period_to_time_range=set_period_to_time_range,
            stacked=stacked,
            statistic=statistic,
            view=view,
            height=height,
            region=region,
            title=title,
            width=width,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addLeftMetric")
    def add_left_metric(self, metric: IMetric) -> None:
        '''(experimental) Add another metric to the left Y axis of the GraphWidget.

        :param metric: the metric to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7f1b224cb097001743e3068bfe3ca70594d0e6ece90e5112ec4d5e37dc3185)
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
        return typing.cast(None, jsii.invoke(self, "addLeftMetric", [metric]))

    @jsii.member(jsii_name="addRightMetric")
    def add_right_metric(self, metric: IMetric) -> None:
        '''(experimental) Add another metric to the right Y axis of the GraphWidget.

        :param metric: the metric to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a6490e8bcbec6dfc73bfc1f46ceff5267cabbec890c8913f5c95f7149db5c2)
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
        return typing.cast(None, jsii.invoke(self, "addRightMetric", [metric]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))


@jsii.data_type(
    jsii_type="monocdk.aws_cloudwatch.GraphWidgetProps",
    jsii_struct_bases=[MetricWidgetProps],
    name_mapping={
        "height": "height",
        "region": "region",
        "title": "title",
        "width": "width",
        "left": "left",
        "left_annotations": "leftAnnotations",
        "left_y_axis": "leftYAxis",
        "legend_position": "legendPosition",
        "live_data": "liveData",
        "period": "period",
        "right": "right",
        "right_annotations": "rightAnnotations",
        "right_y_axis": "rightYAxis",
        "set_period_to_time_range": "setPeriodToTimeRange",
        "stacked": "stacked",
        "statistic": "statistic",
        "view": "view",
    },
)
class GraphWidgetProps(MetricWidgetProps):
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        left: typing.Optional[typing.Sequence[IMetric]] = None,
        left_annotations: typing.Optional[typing.Sequence[typing.Union[HorizontalAnnotation, typing.Dict[builtins.str, typing.Any]]]] = None,
        left_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
        legend_position: typing.Optional[LegendPosition] = None,
        live_data: typing.Optional[builtins.bool] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        right: typing.Optional[typing.Sequence[IMetric]] = None,
        right_annotations: typing.Optional[typing.Sequence[typing.Union[HorizontalAnnotation, typing.Dict[builtins.str, typing.Any]]]] = None,
        right_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
        set_period_to_time_range: typing.Optional[builtins.bool] = None,
        stacked: typing.Optional[builtins.bool] = None,
        statistic: typing.Optional[builtins.str] = None,
        view: typing.Optional[GraphWidgetView] = None,
    ) -> None:
        '''(experimental) Properties for a GraphWidget.

        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: (experimental) The region the metrics of this graph should be taken from. Default: - Current region
        :param title: (experimental) Title for the graph. Default: - None
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6
        :param left: (experimental) Metrics to display on left Y axis. Default: - No metrics
        :param left_annotations: (experimental) Annotations for the left Y axis. Default: - No annotations
        :param left_y_axis: (experimental) Left Y axis. Default: - None
        :param legend_position: (experimental) Position of the legend. Default: - bottom
        :param live_data: (experimental) Whether the graph should show live data. Default: false
        :param period: (experimental) The default period for all metrics in this widget. The period is the length of time represented by one data point on the graph. This default can be overridden within each metric definition. Default: cdk.Duration.seconds(300)
        :param right: (experimental) Metrics to display on right Y axis. Default: - No metrics
        :param right_annotations: (experimental) Annotations for the right Y axis. Default: - No annotations
        :param right_y_axis: (experimental) Right Y axis. Default: - None
        :param set_period_to_time_range: (experimental) Whether to show the value from the entire time range. Only applicable for Bar and Pie charts. If false, values will be from the most recent period of your chosen time range; if true, shows the value from the entire time range. Default: false
        :param stacked: (experimental) Whether the graph should be shown as stacked lines. Default: false
        :param statistic: (experimental) The default statistic to be displayed for each metric. This default can be overridden within the definition of each individual metric Default: - The statistic for each metric is used
        :param view: (experimental) Display this metric. Default: TimeSeries

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # dashboard: cloudwatch.Dashboard
            
            
            dashboard.add_widgets(cloudwatch.GraphWidget(
                # ...
            
                legend_position=cloudwatch.LegendPosition.RIGHT
            ))
        '''
        if isinstance(left_y_axis, dict):
            left_y_axis = YAxisProps(**left_y_axis)
        if isinstance(right_y_axis, dict):
            right_y_axis = YAxisProps(**right_y_axis)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506fdf1caa630e70d2328750626c4e97e828dc9efbfd6a0848053551fde755c3)
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument left_annotations", value=left_annotations, expected_type=type_hints["left_annotations"])
            check_type(argname="argument left_y_axis", value=left_y_axis, expected_type=type_hints["left_y_axis"])
            check_type(argname="argument legend_position", value=legend_position, expected_type=type_hints["legend_position"])
            check_type(argname="argument live_data", value=live_data, expected_type=type_hints["live_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
            check_type(argname="argument right_annotations", value=right_annotations, expected_type=type_hints["right_annotations"])
            check_type(argname="argument right_y_axis", value=right_y_axis, expected_type=type_hints["right_y_axis"])
            check_type(argname="argument set_period_to_time_range", value=set_period_to_time_range, expected_type=type_hints["set_period_to_time_range"])
            check_type(argname="argument stacked", value=stacked, expected_type=type_hints["stacked"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument view", value=view, expected_type=type_hints["view"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if height is not None:
            self._values["height"] = height
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width
        if left is not None:
            self._values["left"] = left
        if left_annotations is not None:
            self._values["left_annotations"] = left_annotations
        if left_y_axis is not None:
            self._values["left_y_axis"] = left_y_axis
        if legend_position is not None:
            self._values["legend_position"] = legend_position
        if live_data is not None:
            self._values["live_data"] = live_data
        if period is not None:
            self._values["period"] = period
        if right is not None:
            self._values["right"] = right
        if right_annotations is not None:
            self._values["right_annotations"] = right_annotations
        if right_y_axis is not None:
            self._values["right_y_axis"] = right_y_axis
        if set_period_to_time_range is not None:
            self._values["set_period_to_time_range"] = set_period_to_time_range
        if stacked is not None:
            self._values["stacked"] = stacked
        if statistic is not None:
            self._values["statistic"] = statistic
        if view is not None:
            self._values["view"] = view

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.

        :stability: experimental
        '''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region the metrics of this graph should be taken from.

        :default: - Current region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''(experimental) Title for the graph.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Width of the widget, in a grid of 24 units wide.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def left(self) -> typing.Optional[typing.List[IMetric]]:
        '''(experimental) Metrics to display on left Y axis.

        :default: - No metrics

        :stability: experimental
        '''
        result = self._values.get("left")
        return typing.cast(typing.Optional[typing.List[IMetric]], result)

    @builtins.property
    def left_annotations(self) -> typing.Optional[typing.List[HorizontalAnnotation]]:
        '''(experimental) Annotations for the left Y axis.

        :default: - No annotations

        :stability: experimental
        '''
        result = self._values.get("left_annotations")
        return typing.cast(typing.Optional[typing.List[HorizontalAnnotation]], result)

    @builtins.property
    def left_y_axis(self) -> typing.Optional[YAxisProps]:
        '''(experimental) Left Y axis.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("left_y_axis")
        return typing.cast(typing.Optional[YAxisProps], result)

    @builtins.property
    def legend_position(self) -> typing.Optional[LegendPosition]:
        '''(experimental) Position of the legend.

        :default: - bottom

        :stability: experimental
        '''
        result = self._values.get("legend_position")
        return typing.cast(typing.Optional[LegendPosition], result)

    @builtins.property
    def live_data(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the graph should show live data.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("live_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def period(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The default period for all metrics in this widget.

        The period is the length of time represented by one data point on the graph.
        This default can be overridden within each metric definition.

        :default: cdk.Duration.seconds(300)

        :stability: experimental
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def right(self) -> typing.Optional[typing.List[IMetric]]:
        '''(experimental) Metrics to display on right Y axis.

        :default: - No metrics

        :stability: experimental
        '''
        result = self._values.get("right")
        return typing.cast(typing.Optional[typing.List[IMetric]], result)

    @builtins.property
    def right_annotations(self) -> typing.Optional[typing.List[HorizontalAnnotation]]:
        '''(experimental) Annotations for the right Y axis.

        :default: - No annotations

        :stability: experimental
        '''
        result = self._values.get("right_annotations")
        return typing.cast(typing.Optional[typing.List[HorizontalAnnotation]], result)

    @builtins.property
    def right_y_axis(self) -> typing.Optional[YAxisProps]:
        '''(experimental) Right Y axis.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("right_y_axis")
        return typing.cast(typing.Optional[YAxisProps], result)

    @builtins.property
    def set_period_to_time_range(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to show the value from the entire time range. Only applicable for Bar and Pie charts.

        If false, values will be from the most recent period of your chosen time range;
        if true, shows the value from the entire time range.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("set_period_to_time_range")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stacked(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the graph should be shown as stacked lines.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stacked")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''(experimental) The default statistic to be displayed for each metric.

        This default can be overridden within the definition of each individual metric

        :default: - The statistic for each metric is used

        :stability: experimental
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view(self) -> typing.Optional[GraphWidgetView]:
        '''(experimental) Display this metric.

        :default: TimeSeries

        :stability: experimental
        '''
        result = self._values.get("view")
        return typing.cast(typing.Optional[GraphWidgetView], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_cloudwatch.IAlarm")
class IAlarm(IAlarmRule, _IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents a CloudWatch Alarm.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        '''(experimental) Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        '''(experimental) Name of the alarm.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAlarmProxy(
    jsii.proxy_for(IAlarmRule), # type: ignore[misc]
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents a CloudWatch Alarm.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_cloudwatch.IAlarm"

    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        '''(experimental) Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmArn"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        '''(experimental) Name of the alarm.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAlarm).__jsii_proxy_class__ = lambda : _IAlarmProxy


class LogQueryWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.LogQueryWidget",
):
    '''(experimental) Display query results from Logs Insights.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        
        
        dashboard.add_widgets(cloudwatch.LogQueryWidget(
            log_group_names=["my-log-group"],
            view=cloudwatch.LogQueryVisualizationType.TABLE,
            # The lines will be automatically combined using '\n|'.
            query_lines=["fields @message", "filter @message like /Error/"
            ]
        ))
    '''

    def __init__(
        self,
        *,
        log_group_names: typing.Sequence[builtins.str],
        height: typing.Optional[jsii.Number] = None,
        query_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        view: typing.Optional[LogQueryVisualizationType] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param log_group_names: (experimental) Names of log groups to query.
        :param height: (experimental) Height of the widget. Default: 6
        :param query_lines: (experimental) A sequence of lines to use to build the query. The query will be built by joining the lines together using ``\\n|``. Default: - Exactly one of ``queryString``, ``queryLines`` is required.
        :param query_string: (experimental) Full query string for log insights. Be sure to prepend every new line with a newline and pipe character (``\\n|``). Default: - Exactly one of ``queryString``, ``queryLines`` is required.
        :param region: (experimental) The region the metrics of this widget should be taken from. Default: Current region
        :param title: (experimental) Title for the widget. Default: No title
        :param view: (experimental) The type of view to use. Default: LogQueryVisualizationType.TABLE
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        '''
        props = LogQueryWidgetProps(
            log_group_names=log_group_names,
            height=height,
            query_lines=query_lines,
            query_string=query_string,
            region=region,
            title=title,
            view=view,
            width=width,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))


class SingleValueWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.SingleValueWidget",
):
    '''(experimental) A dashboard widget that displays the most recent value for every metric.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        # visitor_count: cloudwatch.Metric
        # purchase_count: cloudwatch.Metric
        
        
        dashboard.add_widgets(cloudwatch.SingleValueWidget(
            metrics=[visitor_count, purchase_count]
        ))
    '''

    def __init__(
        self,
        *,
        metrics: typing.Sequence[IMetric],
        full_precision: typing.Optional[builtins.bool] = None,
        set_period_to_time_range: typing.Optional[builtins.bool] = None,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics: (experimental) Metrics to display.
        :param full_precision: (experimental) Whether to show as many digits as can fit, before rounding. Default: false
        :param set_period_to_time_range: (experimental) Whether to show the value from the entire time range. Default: false
        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: (experimental) The region the metrics of this graph should be taken from. Default: - Current region
        :param title: (experimental) Title for the graph. Default: - None
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        '''
        props = SingleValueWidgetProps(
            metrics=metrics,
            full_precision=full_precision,
            set_period_to_time_range=set_period_to_time_range,
            height=height,
            region=region,
            title=title,
            width=width,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))


class TextWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.TextWidget",
):
    '''(experimental) A dashboard widget that displays MarkDown.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        
        
        dashboard.add_widgets(cloudwatch.TextWidget(
            markdown="# Key Performance Indicators"
        ))
    '''

    def __init__(
        self,
        *,
        markdown: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param markdown: (experimental) The text to display, in MarkDown format.
        :param height: (experimental) Height of the widget. Default: 2
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        '''
        props = TextWidgetProps(markdown=markdown, height=height, width=width)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        '''(experimental) Place the widget at a given position.

        :param x: -
        :param y: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4c4de5a3e74718bcd627776135ff63ab9233ffbebe122215435d5a0b849cb5)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        return typing.cast(None, jsii.invoke(self, "position", [x, y]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))


@jsii.implements(IAlarm)
class AlarmBase(
    _Resource_abff4495,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_cloudwatch.AlarmBase",
):
    '''(experimental) The base class for Alarm and CompositeAlarm resources.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: (experimental) The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: (experimental) ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: (experimental) The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: (experimental) The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2938b982909b4e6af9fc71266467a13cfba3eb22bf5142413e3bf3a8cbf8ecd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _ResourceProps_9b554c0f(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAlarmAction")
    def add_alarm_action(self, *actions: IAlarmAction) -> None:
        '''(experimental) Trigger this action if the alarm fires.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4c23febb97794ad30a0a58b7e60e4a871a09431bf35515b01e8aba425ebed0)
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addAlarmAction", [*actions]))

    @jsii.member(jsii_name="addInsufficientDataAction")
    def add_insufficient_data_action(self, *actions: IAlarmAction) -> None:
        '''(experimental) Trigger this action if there is insufficient data to evaluate the alarm.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b373d564fffdc1454afbb63e72bde376bac3e6b3fa01c8c834a63011313e23ae)
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addInsufficientDataAction", [*actions]))

    @jsii.member(jsii_name="addOkAction")
    def add_ok_action(self, *actions: IAlarmAction) -> None:
        '''(experimental) Trigger this action if the alarm returns from breaching state into ok state.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68a38cc786405e0bd7e74e5db46cc6d420a882bd634e5bf7c92687366402c25)
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addOkAction", [*actions]))

    @jsii.member(jsii_name="renderAlarmRule")
    def render_alarm_rule(self) -> builtins.str:
        '''(experimental) AlarmRule indicating ALARM state for Alarm.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "renderAlarmRule", []))

    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    @abc.abstractmethod
    def alarm_arn(self) -> builtins.str:
        '''(experimental) Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    @abc.abstractmethod
    def alarm_name(self) -> builtins.str:
        '''(experimental) Name of the alarm.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="alarmActionArns")
    def _alarm_action_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "alarmActionArns"))

    @_alarm_action_arns.setter
    def _alarm_action_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3264323041148d02a0ffa665f5739ed1634de62662b309fcb3d8096fea99f7a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmActionArns", value)

    @builtins.property
    @jsii.member(jsii_name="insufficientDataActionArns")
    def _insufficient_data_action_arns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "insufficientDataActionArns"))

    @_insufficient_data_action_arns.setter
    def _insufficient_data_action_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c862645c58a62d2253d3608885de7c5104eefa4adf6b06ccc47088afc8bb2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insufficientDataActionArns", value)

    @builtins.property
    @jsii.member(jsii_name="okActionArns")
    def _ok_action_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "okActionArns"))

    @_ok_action_arns.setter
    def _ok_action_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e713d35ae99db7dd3669d8f63eb420bf2ebab7d1ea4a08d4de3d4146be253775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "okActionArns", value)


class _AlarmBaseProxy(
    AlarmBase,
    jsii.proxy_for(_Resource_abff4495), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        '''(experimental) Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmArn"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        '''(experimental) Name of the alarm.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AlarmBase).__jsii_proxy_class__ = lambda : _AlarmBaseProxy


class AlarmStatusWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.AlarmStatusWidget",
):
    '''(experimental) A dashboard widget that displays alarms in a grid view.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        # error_alarm: cloudwatch.Alarm
        
        
        dashboard.add_widgets(
            cloudwatch.AlarmStatusWidget(
                alarms=[error_alarm]
            ))
    '''

    def __init__(
        self,
        *,
        alarms: typing.Sequence[IAlarm],
        height: typing.Optional[jsii.Number] = None,
        sort_by: typing.Optional[AlarmStatusWidgetSortBy] = None,
        states: typing.Optional[typing.Sequence[AlarmState]] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param alarms: (experimental) CloudWatch Alarms to show in widget.
        :param height: (experimental) Height of the widget. Default: 3
        :param sort_by: (experimental) Specifies how to sort the alarms in the widget. Default: - alphabetical order
        :param states: (experimental) Use this field to filter the list of alarms displayed in the widget to only those alarms currently in the specified states. You can specify one or more alarm states in the value for this field. The alarm states that you can specify are ALARM, INSUFFICIENT_DATA, and OK. If you omit this field or specify an empty array, all the alarms specifed in alarms are displayed. Default: - all the alarms specified in alarms are displayed.
        :param title: (experimental) The title of the widget. Default: 'Alarm Status'
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        '''
        props = AlarmStatusWidgetProps(
            alarms=alarms,
            height=height,
            sort_by=sort_by,
            states=states,
            title=title,
            width=width,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        '''(experimental) Place the widget at a given position.

        :param x: -
        :param y: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f554edd1d2fa0ffb5a27ab15f8a336e1d656ed6ce5eb1a64117aaedcc0ab4e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        return typing.cast(None, jsii.invoke(self, "position", [x, y]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))


class AlarmWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.AlarmWidget",
):
    '''(experimental) Display the metric associated with an alarm, including the alarm line.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # dashboard: cloudwatch.Dashboard
        # error_alarm: cloudwatch.Alarm
        
        
        dashboard.add_widgets(cloudwatch.AlarmWidget(
            title="Errors",
            alarm=error_alarm
        ))
    '''

    def __init__(
        self,
        *,
        alarm: IAlarm,
        left_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param alarm: (experimental) The alarm to show.
        :param left_y_axis: (experimental) Left Y axis. Default: - No minimum or maximum values for the left Y-axis
        :param height: (experimental) Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: (experimental) The region the metrics of this graph should be taken from. Default: - Current region
        :param title: (experimental) Title for the graph. Default: - None
        :param width: (experimental) Width of the widget, in a grid of 24 units wide. Default: 6

        :stability: experimental
        '''
        props = AlarmWidgetProps(
            alarm=alarm,
            left_y_axis=left_y_axis,
            height=height,
            region=region,
            title=title,
            width=width,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''(experimental) Return the widget JSON for use in the dashboard.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))


class CompositeAlarm(
    AlarmBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.CompositeAlarm",
):
    '''(experimental) A Composite Alarm based on Alarm Rule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # alarm1: cloudwatch.Alarm
        # alarm2: cloudwatch.Alarm
        # alarm3: cloudwatch.Alarm
        # alarm4: cloudwatch.Alarm
        
        
        alarm_rule = cloudwatch.AlarmRule.any_of(
            cloudwatch.AlarmRule.all_of(
                cloudwatch.AlarmRule.any_of(alarm1,
                    cloudwatch.AlarmRule.from_alarm(alarm2, cloudwatch.AlarmState.OK), alarm3),
                cloudwatch.AlarmRule.not(cloudwatch.AlarmRule.from_alarm(alarm4, cloudwatch.AlarmState.INSUFFICIENT_DATA))),
            cloudwatch.AlarmRule.from_boolean(False))
        
        cloudwatch.CompositeAlarm(self, "MyAwesomeCompositeAlarm",
            alarm_rule=alarm_rule
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alarm_rule: IAlarmRule,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        composite_alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alarm_rule: (experimental) Expression that specifies which other alarms are to be evaluated to determine this composite alarm's state.
        :param actions_enabled: (experimental) Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: (experimental) Description for the alarm. Default: No description
        :param composite_alarm_name: (experimental) Name of the alarm. Default: Automatically generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4feae6f1cf2e38992ab5d3412459c4039410d72ee39c5e42b57149b67578cc86)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CompositeAlarmProps(
            alarm_rule=alarm_rule,
            actions_enabled=actions_enabled,
            alarm_description=alarm_description,
            composite_alarm_name=composite_alarm_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCompositeAlarmArn")
    @builtins.classmethod
    def from_composite_alarm_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        composite_alarm_arn: builtins.str,
    ) -> IAlarm:
        '''(experimental) Import an existing CloudWatch composite alarm provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param composite_alarm_arn: Composite Alarm ARN (i.e. arn:aws:cloudwatch:::alarm/CompositeAlarmName).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a26cead2fab0fe732df55f1dbd50e538241b26827f4a68fb3b7c39275760c0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument composite_alarm_arn", value=composite_alarm_arn, expected_type=type_hints["composite_alarm_arn"])
        return typing.cast(IAlarm, jsii.sinvoke(cls, "fromCompositeAlarmArn", [scope, id, composite_alarm_arn]))

    @jsii.member(jsii_name="fromCompositeAlarmName")
    @builtins.classmethod
    def from_composite_alarm_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        composite_alarm_name: builtins.str,
    ) -> IAlarm:
        '''(experimental) Import an existing CloudWatch composite alarm provided an Name.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param composite_alarm_name: Composite Alarm Name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4286af826b666008118f3cb4d3cf39c4b6d2e1187e6e05060d837fd109a8a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument composite_alarm_name", value=composite_alarm_name, expected_type=type_hints["composite_alarm_name"])
        return typing.cast(IAlarm, jsii.sinvoke(cls, "fromCompositeAlarmName", [scope, id, composite_alarm_name]))

    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        '''(experimental) ARN of this alarm.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmArn"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        '''(experimental) Name of this alarm.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))


class Alarm(
    AlarmBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch.Alarm",
):
    '''(experimental) An alarm on a CloudWatch metric.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cloudwatch
        
        # alias: lambda.Alias
        
        # or add alarms to an existing group
        # blue_green_alias: lambda.Alias
        
        alarm = cloudwatch.Alarm(self, "Errors",
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=1,
            evaluation_periods=1,
            metric=alias.metric_errors()
        )
        deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
            alarms=[alarm
            ]
        )
        deployment_group.add_alarm(cloudwatch.Alarm(self, "BlueGreenErrors",
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=1,
            evaluation_periods=1,
            metric=blue_green_alias.metric_errors()
        ))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        metric: IMetric,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param metric: (experimental) The metric to add the alarm on. Metric objects can be obtained from most resources, or you can construct custom Metric objects by instantiating one.
        :param evaluation_periods: (experimental) The number of periods over which data is compared to the specified threshold.
        :param threshold: (experimental) The value against which the specified statistic is compared.
        :param actions_enabled: (experimental) Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: (experimental) Description for the alarm. Default: No description
        :param alarm_name: (experimental) Name of the alarm. Default: Automatically generated name
        :param comparison_operator: (experimental) Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: (experimental) The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: (experimental) Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: (experimental) Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30aa707e600a4ca3ae8431871546bf606c0c23361ca12c26ec2b5c5cacf209c9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AlarmProps(
            metric=metric,
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            actions_enabled=actions_enabled,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            comparison_operator=comparison_operator,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            period=period,
            statistic=statistic,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAlarmArn")
    @builtins.classmethod
    def from_alarm_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        alarm_arn: builtins.str,
    ) -> IAlarm:
        '''(experimental) Import an existing CloudWatch alarm provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param alarm_arn: Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee5e8cb4f2da0888d874a831e0a0fec9e1bfd36350b17e2939d6e22ede7e3f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument alarm_arn", value=alarm_arn, expected_type=type_hints["alarm_arn"])
        return typing.cast(IAlarm, jsii.sinvoke(cls, "fromAlarmArn", [scope, id, alarm_arn]))

    @jsii.member(jsii_name="addAlarmAction")
    def add_alarm_action(self, *actions: IAlarmAction) -> None:
        '''(experimental) Trigger this action if the alarm fires.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7f1b904277bc52ea17b85ea1e2f2b65dcbb5e0db4414bc2c3110339bdae9b3)
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addAlarmAction", [*actions]))

    @jsii.member(jsii_name="toAnnotation")
    def to_annotation(self) -> HorizontalAnnotation:
        '''(experimental) Turn this alarm into a horizontal annotation.

        This is useful if you want to represent an Alarm in a non-AlarmWidget.
        An ``AlarmWidget`` can directly show an alarm, but it can only show a
        single alarm and no other metrics. Instead, you can convert the alarm to
        a HorizontalAnnotation and add it as an annotation to another graph.

        This might be useful if:

        - You want to show multiple alarms inside a single graph, for example if
          you have both a "small margin/long period" alarm as well as a
          "large margin/short period" alarm.
        - You want to show an Alarm line in a graph with multiple metrics in it.

        :stability: experimental
        '''
        return typing.cast(HorizontalAnnotation, jsii.invoke(self, "toAnnotation", []))

    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        '''(experimental) ARN of this alarm.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmArn"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        '''(experimental) Name of this alarm.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> IMetric:
        '''(experimental) The metric object this alarm was based on.

        :stability: experimental
        '''
        return typing.cast(IMetric, jsii.get(self, "metric"))


__all__ = [
    "Alarm",
    "AlarmActionConfig",
    "AlarmBase",
    "AlarmProps",
    "AlarmRule",
    "AlarmState",
    "AlarmStatusWidget",
    "AlarmStatusWidgetProps",
    "AlarmStatusWidgetSortBy",
    "AlarmWidget",
    "AlarmWidgetProps",
    "CfnAlarm",
    "CfnAlarmProps",
    "CfnAnomalyDetector",
    "CfnAnomalyDetectorProps",
    "CfnCompositeAlarm",
    "CfnCompositeAlarmProps",
    "CfnDashboard",
    "CfnDashboardProps",
    "CfnInsightRule",
    "CfnInsightRuleProps",
    "CfnMetricStream",
    "CfnMetricStreamProps",
    "Color",
    "Column",
    "CommonMetricOptions",
    "ComparisonOperator",
    "CompositeAlarm",
    "CompositeAlarmProps",
    "ConcreteWidget",
    "CreateAlarmOptions",
    "CustomWidget",
    "CustomWidgetProps",
    "Dashboard",
    "DashboardProps",
    "Dimension",
    "GraphWidget",
    "GraphWidgetProps",
    "GraphWidgetView",
    "HorizontalAnnotation",
    "IAlarm",
    "IAlarmAction",
    "IAlarmRule",
    "IMetric",
    "IWidget",
    "LegendPosition",
    "LogQueryVisualizationType",
    "LogQueryWidget",
    "LogQueryWidgetProps",
    "MathExpression",
    "MathExpressionOptions",
    "MathExpressionProps",
    "Metric",
    "MetricAlarmConfig",
    "MetricConfig",
    "MetricExpressionConfig",
    "MetricGraphConfig",
    "MetricOptions",
    "MetricProps",
    "MetricRenderingProperties",
    "MetricStatConfig",
    "MetricWidgetProps",
    "PeriodOverride",
    "Row",
    "Shading",
    "SingleValueWidget",
    "SingleValueWidgetProps",
    "Spacer",
    "SpacerProps",
    "Statistic",
    "TextWidget",
    "TextWidgetProps",
    "TreatMissingData",
    "Unit",
    "YAxisProps",
]

publication.publish()

def _typecheckingstub__828b5e743f934eace92473166216cdba7942dba7759734258932c75f6d1b60fe(
    *,
    alarm_action_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ccc76ffbdaab58ab46dd890881bd2d51fda3ffaade34818c9d921c9aad17e2(
    *operands: IAlarmRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e55dc9e374eb3ce18406aaa408fd4f91f84b4e98908ac8da0f8f3ebcb42f598(
    *operands: IAlarmRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45af71d930e95351339b010f5ab318692e68cdb6dee7a20949d9dbedc12f2d27(
    alarm: IAlarm,
    alarm_state: AlarmState,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dcd555c870f9f21a529544f6b53e8389836573ef98bc7355cfebae9597e4b30(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2455351c588454e76962f85dfda3a8ac9433bc75f318bbf33b65ce82550a5cc(
    alarm_rule: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d634202649774dde1ecfee34cdfa2e6f61245ee27de9ead3ab9cdca28d14953(
    operand: IAlarmRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c87adf30fb80727ccb2d1e6883ef8b04e7ce2e1792eb226d045b4c444093d5(
    *,
    alarms: typing.Sequence[IAlarm],
    height: typing.Optional[jsii.Number] = None,
    sort_by: typing.Optional[AlarmStatusWidgetSortBy] = None,
    states: typing.Optional[typing.Sequence[AlarmState]] = None,
    title: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c24ca6383d248ea374ad81e7f13cdd4a072058b78dcf7bf2385aa98e1ad2133(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    comparison_operator: builtins.str,
    evaluation_periods: jsii.Number,
    actions_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAlarm.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
    extended_statistic: typing.Optional[builtins.str] = None,
    insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    metrics: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAlarm.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    period: typing.Optional[jsii.Number] = None,
    statistic: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    threshold_metric_id: typing.Optional[builtins.str] = None,
    treat_missing_data: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91d206bd113655b45d119993347bc9e78ca9b8fc3499119ef01759f71d6019c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab049447fe9220a41bfcac7f6d506f687a8a2bf503393a8eeb5ddcb592ae7e98(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60a4736d5ef7284ea710d91bef64e80f131e9eccd820b0feac514e3b5a7d8e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33595f0ec9f507090942a0b67a10b8763d914bf0e95f880b79ff82c856e03c9b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62523cb7d3fa6fd5886a00ecbf98aa8e496669044f52d634d65e4854b42fbf05(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e372146b0922980c86287415ac5e364ddfc1568817a733fdd53ced35c4dd8358(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c424852715a6156bea31c7a5765794861fc7f0c8b02fbd2ecb0109d72f08f147(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29724c0be9d5cee8832bbb0c491987cfa2d997d36adb9100fafa40dc43ba31cf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d2ef1ef926d68bbeb61af51744c12b92bc26540305fa30af9fdfee8c9b5315(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d133df1313d197b723790dcad4101ce29287628f175b37e4db21eb94dcfe27d(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAlarm.DimensionProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ae31754ab79be0b6f2568f893054fe16a36c23ca861c3525fccd87001a2538(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4553c43b30e89874ae83e6354b8d502ec595847884b34857dc1cad8a69b3550b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36105d7a1f9983b372591215bb9c09cc085c625b0cf9a439aa525d497424b4e5(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5356c5b82889bec14fbfc6f06e4e4b18e8782d782a0cd71530485a37949921fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1f1038b6b29c749cbb7f277ef012c7726adf40bc5804b850ea0a38895c4428(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAlarm.MetricDataQueryProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7f180021c784875f3320d829202b9b517f804817d7930ff3cc5c727d0906db(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b52c25ae87a46f62904cf534dda8f8daae553f306ec27cc90462a194bb51d83(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b5d4ef4fea06e25a9d6c64905a32a1f554c6ddf713660cae5523f926264c3a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde464d49ec310cbfcd21cfd9bb921930c2c69138fee6130181db71ec4b1e9a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0124f9ae85c4e9eb99be3196dbd924d8f830905e30f1ce4b7fc42d8fa807304(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e68c1e14e7e7d416e49a51141fef966c8b9c37439e87002c208ba84d5b4ddd3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf95b3bb442c2d369adc621180469300f23ebd3f858d8893412859068c9ede9c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51907af862e25b54574dd482761a16eecda38676300ab082f32149a41025c334(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fd70bddd3c9b8df9e8a4a6052dc66f074ce0995925135b53a4ee698b32cb5b(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1cb5a63970ca8765d2107090ed89107a38bf33148d51952b46452ea2fbbfe5(
    *,
    id: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[typing.Union[CfnAlarm.MetricStatProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    period: typing.Optional[jsii.Number] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae49ce87a49f68673dfade799a579408e3dab374a0ce78a61aee42e76e06063(
    *,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAlarm.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad9e52cb051de75b765be5e717099b5f885390b0e3a27ccb8478123c5a967eb(
    *,
    metric: typing.Union[typing.Union[CfnAlarm.MetricProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    period: jsii.Number,
    stat: builtins.str,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e0e217c648a25dde1802881478c821b3e1daa736f624effab66d5b567bfff1(
    *,
    comparison_operator: builtins.str,
    evaluation_periods: jsii.Number,
    actions_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAlarm.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
    extended_statistic: typing.Optional[builtins.str] = None,
    insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    metrics: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAlarm.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    period: typing.Optional[jsii.Number] = None,
    statistic: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    threshold_metric_id: typing.Optional[builtins.str] = None,
    treat_missing_data: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f024cb919501d6256d3a9898edb1caea942ff694f6e986d25d0c28cf567a521e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    configuration: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAnomalyDetector.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    metric_math_anomaly_detector: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.MetricMathAnomalyDetectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    single_metric_anomaly_detector: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stat: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987d53e7d0f3eca9379a125bb8ac4789698bf4ffa82e6e82a44cac3a61373ae5(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c23644ea90e6a967388476b9fcc0f38a5dd4e5dc169387cf389f70aa83b7d87(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b82836bf991c393dd6a785302ab87c1be4aeeac04c02fd721c4d8efe6267e7d(
    value: typing.Optional[typing.Union[CfnAnomalyDetector.ConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff6c0b6eef7e662bfb15fcb659824d458e5d07caa9aeaaff38ace8dc88dedea(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAnomalyDetector.DimensionProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66255c5cb5bc8b964fbf32e42c84dbdf66e4b6f60b2e93a3210de30770fe5a35(
    value: typing.Optional[typing.Union[CfnAnomalyDetector.MetricMathAnomalyDetectorProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93b2d935a49d98c94ae2c996f51a72f81b33807bfa6fa8589a38f96465fbca2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d8cfa34753a015c76c75ab49ee06dd93a171bfa660f1a798cf6451961744cd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34244eb8e6ae656a33e3f6dc51bcd7ee170fa6a091cbcc827d3c0104c7fbb863(
    value: typing.Optional[typing.Union[CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ce6b19026996cad40bb729580f8361dd13e7ac354ab844da0904dda5695821(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4acfa60383b9d31293e0aeab081eb4abc3aed45c896d2145df5a328ab595b8e(
    *,
    excluded_time_ranges: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAnomalyDetector.RangeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    metric_time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7841f336d62bbf0a2d6a9bffcf99f3cc531d6282d5e8a6b76624f87cc5ee1a(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a57c5029500d8afedb8814b1a32bf111b55f688a3e50e4d72a4a11eccb122c(
    *,
    id: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.MetricStatProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    period: typing.Optional[jsii.Number] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5ac0ada49a61d757fdd28f86ecd5ed2191b50ad82a1581b7f65004a8120236(
    *,
    metric_data_queries: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAnomalyDetector.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed6436864d53ea88be2d61348a8d10ba1969f2f17f23cb912fd1f106c00dae6(
    *,
    metric_name: builtins.str,
    namespace: builtins.str,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAnomalyDetector.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5be944c8b2710063bbeef93199eef661b796af2de7b18252eb52a491af5601(
    *,
    metric: typing.Union[typing.Union[CfnAnomalyDetector.MetricProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    period: jsii.Number,
    stat: builtins.str,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d0fa74dbb859e57a41b981be21516fbdb5516aaf990beb72e166d885b64378(
    *,
    end_time: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d42d63a3c5e06c19361c11897efe4729859ac06e62c32a74e71ec521d25a83(
    *,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAnomalyDetector.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    stat: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f423aec7b474b2405381de97cce1ca5c2a8e1b7acfeac128a7890dbee3f7bbd(
    *,
    configuration: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAnomalyDetector.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    metric_math_anomaly_detector: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.MetricMathAnomalyDetectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    single_metric_anomaly_detector: typing.Optional[typing.Union[typing.Union[CfnAnomalyDetector.SingleMetricAnomalyDetectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stat: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9593e237fc8c8aea557e2ed8d0a67cdd3a400906a67897616b93db9d941e82bb(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    alarm_rule: builtins.str,
    actions_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    actions_suppressor: typing.Optional[builtins.str] = None,
    actions_suppressor_extension_period: typing.Optional[jsii.Number] = None,
    actions_suppressor_wait_period: typing.Optional[jsii.Number] = None,
    alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df9cb16b9c43c51c658df2bb6416d1f00738d70d5237937ed3d5fc5c8b1104e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d46321bca7536499159d49ec75b970f11874ca9ac3bfe6a3ac2edece4a72c6e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c488f3c4f855735f99b6f5828b0e1601bb238699c7caf144ea2c88f34bce129f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91abbd9fb2785e34daa08bbc507f1ae105cb931caf39a5c9e1510c57bdcd971(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c34c6e65a8749e64e7322e1658bbec579a139c397e83765a929eb635d00760(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb1d60d67f1f40d6f106b3cf899228574ad6c5317747cbd221bbf5aae1d62d9(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfabf3a249e61172f0e642fb4f6acd9fd7b89deb648e6086a57fc7aa0144da6(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426a54d2120ab6779d268b159493239e90d38974834c5da45f273e8f547274df(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe3c49a91ca15cc602dcb47256b2ed7b28b1b905f6d30e505b11f03a5044250(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d604bf958b97f677f4c77aaee0aa53c7f04ce854450a7024295430d6428ebb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060864e2b0279f28410f46c4099d8cda6f219fbc42363143047bcb45b8b3d3a2(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe83217e9a362db90e0b6374888438a6b0fdcf1a12b0c142e00f8733ec2dfb4(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bc2ae85019462d24df8e7586c59b5ed9ac963e291177c526f577f43c14a886(
    *,
    alarm_rule: builtins.str,
    actions_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    actions_suppressor: typing.Optional[builtins.str] = None,
    actions_suppressor_extension_period: typing.Optional[jsii.Number] = None,
    actions_suppressor_wait_period: typing.Optional[jsii.Number] = None,
    alarm_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    insufficient_data_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ok_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc4d480bcab6b22924ff9d4b2d8e53e79bca7d4ebd0be23a9f9fe88c9524ed1(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    dashboard_body: builtins.str,
    dashboard_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdb1cce6bcd184a48fec81f6d63f4dbe7a303f77ef77adcdf293751fca34fa9(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05debdae58a97f84253e7df4b73dc5828234ca4a93ca04d832dc47d91a526df2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34fcdaf86787ba9b030f60afaece32f761411bb3697b550ded89bd1ed5fb5cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88031f24013086d04bf22f7f72208ebbf9078466d64b6ca01f1ba923469f8fbf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52a1aa45c6d954169fb9b99d30879c3a2b5c4e561c05f6a2c83ec6828da5349(
    *,
    dashboard_body: builtins.str,
    dashboard_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8bcffc97c5a49aa76301f74824b77e2ca3f134e08695fd0ef54dfc637057e9(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    rule_body: builtins.str,
    rule_name: builtins.str,
    rule_state: builtins.str,
    tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734b7d1d39df442a0777926343f5dd49517d73b80aa92052efcd09b0fb278fe1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35996c89b98e7300859e8dd8866901f448446c1e97d53466d6a366c8bc0ea4e1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65921830dd71708f791d2baf286e6359d33d18c175d15967919249ca2d71c76d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007fc5499a09ea1aeb3cacc0893304e7babb25b9f81e26d48470ace948751f3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4dbe03b10e790be682fe7c06dce4a803f172771047b706f0fbcab023c794626(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b811b83cfa7e4436a429d27651bebd9f33590f3935874b4d33427cf6e402b7(
    *,
    rule_body: builtins.str,
    rule_name: builtins.str,
    rule_state: builtins.str,
    tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6eb648d8ee9f1901d472d8639e6c94ea3e30c72d07bdbb72f595c9f49b8f741(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    firehose_arn: builtins.str,
    output_format: builtins.str,
    role_arn: builtins.str,
    exclude_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    include_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    include_linked_accounts_metrics: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    statistics_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamStatisticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18fd6e24308ffdf8d29019bd5f818321742205776438f2c5042716b9a2d09a2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff85e225c8d4aac4670e69459cc26d0796d7060711dadecca26881934449d521(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5138db29db67eb4e16d0c3ab1a6b71f3a678a623b61ed96f573671fbdb84e494(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89438dbd0ecf8eff56d6aac0f07a5d5ca7aae9489d1780ad3ce3810f6299ab77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e76161dba4eed0b71fda6b8d7eda8d0b2258a063cb68c3068774a1f8a6093c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b3ce32049c481b13a4f597634d739f777ddbee6209b7addbb10f5eb1c3ff83(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamFilterProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d58f02b153747fa3026d5f0049a95a148d6fe8fcbb7883a65375d7a43393a46(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamFilterProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6def02a5c015f89c2e231d46514f8159962b76203b6c5247b4fb3fced33e6896(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb7928bcb3f6a7ac0ac41b5879ad0a5b04f83b7d60a02c6852ba565dbadecb1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c7a4de6f9ec9e3f10b25e1f357075b2222c7136b4a7ced75cfce902b8cc720(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricStream.MetricStreamStatisticsConfigurationProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a12e26817c34cb058edd1e2ffe91c19fea8facd02af81b71bf97d8d10f6e8a(
    *,
    namespace: builtins.str,
    metric_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c72f24e1ad345ad4426d4db3eec0187fb91eff100ec57b906f60e61b2b05b9(
    *,
    additional_statistics: typing.Sequence[builtins.str],
    include_metrics: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamStatisticsMetricProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d525f834f62eace41e71b2ac53bdd15e18bbe8b221507a7ca6488213176f1e(
    *,
    metric_name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01ae8278600fd5d054aecdc05a6df6e59a0b915ab186de415a85c8632b640df(
    *,
    firehose_arn: builtins.str,
    output_format: builtins.str,
    role_arn: builtins.str,
    exclude_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    include_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    include_linked_accounts_metrics: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    statistics_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnMetricStream.MetricStreamStatisticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2836747294724a281bcf8aa8fcb1eadfd36d0e5667d3a3d69f3e91abf21cc568(
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca1d4eaea3c63ce37db39e18ed5413537df008a2a64ab30a457103428476e4a(
    *,
    alarm_rule: IAlarmRule,
    actions_enabled: typing.Optional[builtins.bool] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    composite_alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1f7778a5b877bb8eecb3cbba837c03054d139d31eede24c02c3d4bd9233e4b(
    *,
    evaluation_periods: jsii.Number,
    threshold: jsii.Number,
    actions_enabled: typing.Optional[builtins.bool] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    comparison_operator: typing.Optional[ComparisonOperator] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    statistic: typing.Optional[builtins.str] = None,
    treat_missing_data: typing.Optional[TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8a3786cd095ff0c21b02074192e7d7caae9f04b303a72aa79c8918bd02ef24(
    *,
    function_arn: builtins.str,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    params: typing.Any = None,
    update_on_refresh: typing.Optional[builtins.bool] = None,
    update_on_resize: typing.Optional[builtins.bool] = None,
    update_on_time_range_change: typing.Optional[builtins.bool] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc2441ca033c0fc7869f0bf6c90cf43070aec52a7a41e90a2ce70fcf7d7f8b3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dashboard_name: typing.Optional[builtins.str] = None,
    end: typing.Optional[builtins.str] = None,
    period_override: typing.Optional[PeriodOverride] = None,
    start: typing.Optional[builtins.str] = None,
    widgets: typing.Optional[typing.Sequence[typing.Sequence[IWidget]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d81df9283670f017e089e4c21e0cd472e165bfe2609bfa9251ef3fc003a04f(
    *widgets: IWidget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50643d8232c3a0f8ab2a83803a2e0c785903f22448cfc6b1799e783663978fa(
    *,
    dashboard_name: typing.Optional[builtins.str] = None,
    end: typing.Optional[builtins.str] = None,
    period_override: typing.Optional[PeriodOverride] = None,
    start: typing.Optional[builtins.str] = None,
    widgets: typing.Optional[typing.Sequence[typing.Sequence[IWidget]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c8a78675a396e604694e7d4b4dbc5f9855bbb5891303b66cd0f7fe85002c00(
    *,
    name: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b291fb2da233e4c299e325e23e406c4d2034081e37e85a1ae888188a4de7fc(
    *,
    value: jsii.Number,
    color: typing.Optional[builtins.str] = None,
    fill: typing.Optional[Shading] = None,
    label: typing.Optional[builtins.str] = None,
    visible: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2785d3adb99b00446f2088de67423c9d3f630afaa0281f669057f00d74916785(
    scope: _Construct_e78e779f,
    alarm: IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96d51d870dfc91a094333515161f8456605eebb6433779d18e6fdcac9ed3842(
    x: jsii.Number,
    y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0cf610a40ba144394f70dee71dcc96a4d2df100bbd3a21536d890359a88dfe(
    *,
    log_group_names: typing.Sequence[builtins.str],
    height: typing.Optional[jsii.Number] = None,
    query_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    view: typing.Optional[LogQueryVisualizationType] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18a7808c14a4c5292f94693fc9c01fe6e3ce432424a347ac2574133b7dff698(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    evaluation_periods: jsii.Number,
    threshold: jsii.Number,
    actions_enabled: typing.Optional[builtins.bool] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    comparison_operator: typing.Optional[ComparisonOperator] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    statistic: typing.Optional[builtins.str] = None,
    treat_missing_data: typing.Optional[TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f693ea6b1f10e6962d3f83241a0088267d68a7f6cbb8c014cd9a93515ecb6842(
    *,
    color: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    search_account: typing.Optional[builtins.str] = None,
    search_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9581302082381523367d1717dc5cb89dabad600a231634d5f4d7667973c22fd1(
    *,
    color: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    search_account: typing.Optional[builtins.str] = None,
    search_region: typing.Optional[builtins.str] = None,
    expression: builtins.str,
    using_metrics: typing.Optional[typing.Mapping[builtins.str, IMetric]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ca50267f75729e43c6dccb066af962ca5f0fbda4ef23f8a3e163216dd55c47(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d6a191cecda4161675d78a063b4b5132574036535821f60f8c3ad1a12d4407(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a85163e9a6980b62870514e4bb90adfbb00f8bb4e9b627d88c8712935e9f008(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    evaluation_periods: jsii.Number,
    threshold: jsii.Number,
    actions_enabled: typing.Optional[builtins.bool] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    comparison_operator: typing.Optional[ComparisonOperator] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    statistic: typing.Optional[builtins.str] = None,
    treat_missing_data: typing.Optional[TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6e2cc15f94cac6f392c9e83a6c877bd354a5f78230fc429d5235687f9f0b9b(
    *,
    metric_name: builtins.str,
    namespace: builtins.str,
    period: jsii.Number,
    dimensions: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
    extended_statistic: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[Statistic] = None,
    unit: typing.Optional[Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4456db504977796f6c3432ae050aa6080896c10d5a4dc43ea7014fc6f4876de3(
    *,
    math_expression: typing.Optional[typing.Union[MetricExpressionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metric_stat: typing.Optional[typing.Union[MetricStatConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    rendering_properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8157cb73d47f162e524f16ee12df7244a5f41d979eb72c167bb70b8d118eac(
    *,
    expression: builtins.str,
    period: jsii.Number,
    using_metrics: typing.Mapping[builtins.str, IMetric],
    search_account: typing.Optional[builtins.str] = None,
    search_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4216a0e537c421715a3df848babe18bf684e87b4f1646df51ebc2f18ce38c70c(
    *,
    metric_name: builtins.str,
    namespace: builtins.str,
    period: jsii.Number,
    rendering_properties: typing.Union[MetricRenderingProperties, typing.Dict[builtins.str, typing.Any]],
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
    label: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaddf80d4cf1272cabcfaa9b11044f2fcfe5e0313dcf2fe288425fdc3c0218d(
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b483b4310a80d19c72c15ad3ed43f149d986b65b4e8082b6752f479be1f2ab(
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[Unit] = None,
    metric_name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5559662d3f9c667a0baa7f01117ec758df4bb96b61e3617ee49d424d050bbc2e(
    *,
    period: jsii.Number,
    color: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    stat: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb362e6c7d6246bb6929f8a40cd4d977bcd0756ded8b7ddcd5af8250555ef3d(
    *,
    metric_name: builtins.str,
    namespace: builtins.str,
    period: _Duration_070aa057,
    statistic: builtins.str,
    account: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Sequence[typing.Union[Dimension, typing.Dict[builtins.str, typing.Any]]]] = None,
    region: typing.Optional[builtins.str] = None,
    unit_filter: typing.Optional[Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95974eb9f925ab06f8175ddb989bbbd09174cb4e49b5b5275245a99d1dad9d32(
    *,
    height: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142011a6d7a20eace51da73490abef3d99af35dc0ad07dc8d0e31e2a50790e63(
    *widgets: IWidget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6c8e4c956f00058a4800dcd7797588e2882f0b9812c3bfa638694239d14e06(
    x: jsii.Number,
    y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e86eb4a8643de80d4d70ec06fab477568088cb9144a8fab5da2c58452540a9(
    *,
    height: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    metrics: typing.Sequence[IMetric],
    full_precision: typing.Optional[builtins.bool] = None,
    set_period_to_time_range: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017b8501dabf7f830fb059a6c1f3eb58b177dde1df4d76f72a7d7fc624c08bce(
    _x: jsii.Number,
    _y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1507df7e5f90646ca07bde07f8874ca5c43d66f2186310556a4d7e1e067079c3(
    *,
    height: typing.Optional[jsii.Number] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ff7e3019985b4f604cec265a08f66c64e8a61cf937357d3a593827b75ef386(
    *,
    markdown: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f240bcbea86f9e713bc00f2859125c57a987ccf88c1b3681c2c600755ab120(
    *,
    label: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    show_units: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39c05d2740897b5c8c39250be68575247dbd4c00909bb417c760dd8beaf633f(
    *,
    evaluation_periods: jsii.Number,
    threshold: jsii.Number,
    actions_enabled: typing.Optional[builtins.bool] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    comparison_operator: typing.Optional[ComparisonOperator] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    statistic: typing.Optional[builtins.str] = None,
    treat_missing_data: typing.Optional[TreatMissingData] = None,
    metric: IMetric,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2bd39a483140a25a960dc7ecf83a4356cfd98780979b71f6c4422d5e9f72cb(
    *,
    height: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    alarm: IAlarm,
    left_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3c393a65c4e2cf70d4f2c5f930039e13cce8a89d9eb12b109fba7d39b9f304(
    *widgets: IWidget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab7f8e7820f55a8cd5c0182608aa686a5e98839b19ebd713716d34364b0d31c(
    x: jsii.Number,
    y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c46b69ee54330b8ccf9902e9ebf08b2e5eccd53372f96bdbb75a384a4ae21d(
    width: jsii.Number,
    height: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea1a37d58cd01cde16416cf22a3b75e3abf7cd702c146be2451137da54473ae(
    *ms: IMetric,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71446f487f91a003cac597c54103a2ca236ae040a7cd21570da4debb34a9e4e(
    x: jsii.Number,
    y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0249aad8cb00d8d0a8264c7fbeb34d056c4b91c7ccaca87664369c10af84b48(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96f2e543cbdea06e53d57bf90e303d06ef7fbca0828060f297881d41d4a7728(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7f1b224cb097001743e3068bfe3ca70594d0e6ece90e5112ec4d5e37dc3185(
    metric: IMetric,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a6490e8bcbec6dfc73bfc1f46ceff5267cabbec890c8913f5c95f7149db5c2(
    metric: IMetric,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506fdf1caa630e70d2328750626c4e97e828dc9efbfd6a0848053551fde755c3(
    *,
    height: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    left: typing.Optional[typing.Sequence[IMetric]] = None,
    left_annotations: typing.Optional[typing.Sequence[typing.Union[HorizontalAnnotation, typing.Dict[builtins.str, typing.Any]]]] = None,
    left_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
    legend_position: typing.Optional[LegendPosition] = None,
    live_data: typing.Optional[builtins.bool] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    right: typing.Optional[typing.Sequence[IMetric]] = None,
    right_annotations: typing.Optional[typing.Sequence[typing.Union[HorizontalAnnotation, typing.Dict[builtins.str, typing.Any]]]] = None,
    right_y_axis: typing.Optional[typing.Union[YAxisProps, typing.Dict[builtins.str, typing.Any]]] = None,
    set_period_to_time_range: typing.Optional[builtins.bool] = None,
    stacked: typing.Optional[builtins.bool] = None,
    statistic: typing.Optional[builtins.str] = None,
    view: typing.Optional[GraphWidgetView] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4c4de5a3e74718bcd627776135ff63ab9233ffbebe122215435d5a0b849cb5(
    x: jsii.Number,
    y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2938b982909b4e6af9fc71266467a13cfba3eb22bf5142413e3bf3a8cbf8ecd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4c23febb97794ad30a0a58b7e60e4a871a09431bf35515b01e8aba425ebed0(
    *actions: IAlarmAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b373d564fffdc1454afbb63e72bde376bac3e6b3fa01c8c834a63011313e23ae(
    *actions: IAlarmAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68a38cc786405e0bd7e74e5db46cc6d420a882bd634e5bf7c92687366402c25(
    *actions: IAlarmAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3264323041148d02a0ffa665f5739ed1634de62662b309fcb3d8096fea99f7a8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c862645c58a62d2253d3608885de7c5104eefa4adf6b06ccc47088afc8bb2e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e713d35ae99db7dd3669d8f63eb420bf2ebab7d1ea4a08d4de3d4146be253775(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f554edd1d2fa0ffb5a27ab15f8a336e1d656ed6ce5eb1a64117aaedcc0ab4e(
    x: jsii.Number,
    y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feae6f1cf2e38992ab5d3412459c4039410d72ee39c5e42b57149b67578cc86(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alarm_rule: IAlarmRule,
    actions_enabled: typing.Optional[builtins.bool] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    composite_alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a26cead2fab0fe732df55f1dbd50e538241b26827f4a68fb3b7c39275760c0b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    composite_alarm_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4286af826b666008118f3cb4d3cf39c4b6d2e1187e6e05060d837fd109a8a9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    composite_alarm_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30aa707e600a4ca3ae8431871546bf606c0c23361ca12c26ec2b5c5cacf209c9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    metric: IMetric,
    evaluation_periods: jsii.Number,
    threshold: jsii.Number,
    actions_enabled: typing.Optional[builtins.bool] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    comparison_operator: typing.Optional[ComparisonOperator] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    statistic: typing.Optional[builtins.str] = None,
    treat_missing_data: typing.Optional[TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee5e8cb4f2da0888d874a831e0a0fec9e1bfd36350b17e2939d6e22ede7e3f4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    alarm_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7f1b904277bc52ea17b85ea1e2f2b65dcbb5e0db4414bc2c3110339bdae9b3(
    *actions: IAlarmAction,
) -> None:
    """Type checking stubs"""
    pass
