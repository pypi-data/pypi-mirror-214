'''
# Amazon EventBridge Construct Library

Amazon EventBridge delivers a near real-time stream of system events that
describe changes in AWS resources. For example, an AWS CodePipeline emits the
[State
Change](https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html#codepipeline-event-type)
event when the pipeline changes its state.

* **Events**: An event indicates a change in your AWS environment. AWS resources
  can generate events when their state changes. For example, Amazon EC2
  generates an event when the state of an EC2 instance changes from pending to
  running, and Amazon EC2 Auto Scaling generates events when it launches or
  terminates instances. AWS CloudTrail publishes events when you make API calls.
  You can generate custom application-level events and publish them to
  EventBridge. You can also set up scheduled events that are generated on
  a periodic basis. For a list of services that generate events, and sample
  events from each service, see [EventBridge Event Examples From Each
  Supported
  Service](https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html).
* **Targets**: A target processes events. Targets can include Amazon EC2
  instances, AWS Lambda functions, Kinesis streams, Amazon ECS tasks, Step
  Functions state machines, Amazon SNS topics, Amazon SQS queues, Amazon CloudWatch LogGroups, and built-in
  targets. A target receives events in JSON format.
* **Rules**: A rule matches incoming events and routes them to targets for
  processing. A single rule can route to multiple targets, all of which are
  processed in parallel. Rules are not processed in a particular order. This
  enables different parts of an organization to look for and process the events
  that are of interest to them. A rule can customize the JSON sent to the
  target, by passing only certain parts or by overwriting it with a constant.
* **EventBuses**: An event bus can receive events from your own custom applications
  or it can receive events from applications and services created by AWS SaaS partners.
  See [Creating an Event Bus](https://docs.aws.amazon.com/eventbridge/latest/userguide/create-event-bus.html).

## Rule

The `Rule` construct defines an EventBridge rule which monitors an
event based on an [event
pattern](https://docs.aws.amazon.com/eventbridge/latest/userguide/filtering-examples-structure.html)
and invoke **event targets** when the pattern is matched against a triggered
event. Event targets are objects that implement the `IRuleTarget` interface.

Normally, you will use one of the `source.onXxx(name[, target[, options]]) -> Rule` methods on the event source to define an event rule associated with
the specific activity. You can targets either via props, or add targets using
`rule.addTarget`.

For example, to define an rule that triggers a CodeBuild project build when a
commit is pushed to the "master" branch of a CodeCommit repository:

```python
# repo: codecommit.Repository
# project: codebuild.Project


on_commit_rule = repo.on_commit("OnCommit",
    target=targets.CodeBuildProject(project),
    branches=["master"]
)
```

You can add additional targets, with optional [input
transformer](https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_InputTransformer.html)
using `eventRule.addTarget(target[, input])`. For example, we can add a SNS
topic target which formats a human-readable message for the commit.

For example, this adds an SNS topic as a target:

```python
# on_commit_rule: events.Rule
# topic: sns.Topic


on_commit_rule.add_target(targets.SnsTopic(topic,
    message=events.RuleTargetInput.from_text(f"A commit was pushed to the repository {codecommit.ReferenceEvent.repositoryName} on branch {codecommit.ReferenceEvent.referenceName}")
))
```

Or using an Object:

```python
# on_commit_rule: events.Rule
# topic: sns.Topic


on_commit_rule.add_target(targets.SnsTopic(topic,
    message=events.RuleTargetInput.from_object({
        "DataType": f"custom_{events.EventField.fromPath('$.detail-type')}"
    })
))
```

## Scheduling

You can configure a Rule to run on a schedule (cron or rate).
Rate must be specified in minutes, hours or days.

The following example runs a task every day at 4am:

```python
from monocdk.aws_events import Rule, Schedule
from monocdk.aws_events_targets import EcsTask
from monocdk.aws_ecs import Cluster, TaskDefinition
from monocdk.aws_iam import Role

# cluster: Cluster
# task_definition: TaskDefinition
# role: Role


ecs_task_target = EcsTask(cluster=cluster, task_definition=task_definition, role=role)

Rule(self, "ScheduleRule",
    schedule=Schedule.cron(minute="0", hour="4"),
    targets=[ecs_task_target]
)
```

If you want to specify Fargate platform version, set `platformVersion` in EcsTask's props like the following example:

```python
# cluster: ecs.Cluster
# task_definition: ecs.TaskDefinition
# role: iam.Role


platform_version = ecs.FargatePlatformVersion.VERSION1_4
ecs_task_target = targets.EcsTask(cluster=cluster, task_definition=task_definition, role=role, platform_version=platform_version)
```

## Event Targets

The `@aws-cdk/aws-events-targets` module includes classes that implement the `IRuleTarget`
interface for various AWS services.

The following targets are supported:

* `targets.CodeBuildProject`: Start an AWS CodeBuild build
* `targets.CodePipeline`: Start an AWS CodePipeline pipeline execution
* `targets.EcsTask`: Start a task on an Amazon ECS cluster
* `targets.LambdaFunction`: Invoke an AWS Lambda function
* `targets.SnsTopic`: Publish into an SNS topic
* `targets.SqsQueue`: Send a message to an Amazon SQS Queue
* `targets.SfnStateMachine`: Trigger an AWS Step Functions state machine
* `targets.BatchJob`: Queue an AWS Batch Job
* `targets.AwsApi`: Make an AWS API call
* `targets.ApiGateway`: Invoke an AWS API Gateway
* `targets.ApiDestination`: Make an call to an external destination

### Cross-account and cross-region targets

It's possible to have the source of the event and a target in separate AWS accounts and regions:

```python
from monocdk import App, Stack
import monocdk as codebuild
import monocdk as codecommit
import monocdk as targets

app = App()

account1 = "11111111111"
account2 = "22222222222"

stack1 = Stack(app, "Stack1", env=codebuild.Environment(account=account1, region="us-west-1"))
repo = codecommit.Repository(stack1, "Repository",
    repository_name="myrepository"
)

stack2 = Stack(app, "Stack2", env=codebuild.Environment(account=account2, region="us-east-1"))
project = codebuild.Project(stack2, "Project")

repo.on_commit("OnCommit",
    target=targets.CodeBuildProject(project)
)
```

In this situation, the CDK will wire the 2 accounts together:

* It will generate a rule in the source stack with the event bus of the target account as the target
* It will generate a rule in the target stack, with the provided target
* It will generate a separate stack that gives the source account permissions to publish events
  to the event bus of the target account in the given region,
  and make sure its deployed before the source stack

For more information, see the
[AWS documentation on cross-account events](https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html).

## Archiving

It is possible to archive all or some events sent to an event bus. It is then possible to [replay these events](https://aws.amazon.com/blogs/aws/new-archive-and-replay-events-with-amazon-eventbridge/).

```python
bus = events.EventBus(self, "bus",
    event_bus_name="MyCustomEventBus"
)

bus.archive("MyArchive",
    archive_name="MyCustomEventBusArchive",
    description="MyCustomerEventBus Archive",
    event_pattern=events.aws_events.EventPattern(
        account=[Stack.of(self).account]
    ),
    retention=Duration.days(365)
)
```

## Granting PutEvents to an existing EventBus

To import an existing EventBus into your CDK application, use `EventBus.fromEventBusArn`, `EventBus.fromEventBusAttributes`
or `EventBus.fromEventBusName` factory method.

Then, you can use the `grantPutEventsTo` method to grant `event:PutEvents` to the eventBus.

```python
# lambda_function: lambda.Function


event_bus = events.EventBus.from_event_bus_arn(self, "ImportedEventBus", "arn:aws:events:us-east-1:111111111:event-bus/my-event-bus")

# now you can just call methods on the eventbus
event_bus.grant_put_events_to(lambda_function)
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
    IConstruct as _IConstruct_5a0f9c5e,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResolveContext as _IResolveContext_e363e2cb,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IRole as _IRole_59af6f50,
)


@jsii.data_type(
    jsii_type="monocdk.aws_events.ApiDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection": "connection",
        "endpoint": "endpoint",
        "api_destination_name": "apiDestinationName",
        "description": "description",
        "http_method": "httpMethod",
        "rate_limit_per_second": "rateLimitPerSecond",
    },
)
class ApiDestinationProps:
    def __init__(
        self,
        *,
        connection: "IConnection",
        endpoint: builtins.str,
        api_destination_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http_method: typing.Optional["HttpMethod"] = None,
        rate_limit_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The event API Destination properties.

        :param connection: (experimental) The ARN of the connection to use for the API destination.
        :param endpoint: (experimental) The URL to the HTTP invocation endpoint for the API destination..
        :param api_destination_name: (experimental) The name for the API destination. Default: - A unique name will be generated
        :param description: (experimental) A description for the API destination. Default: - none
        :param http_method: (experimental) The method to use for the request to the HTTP invocation endpoint. Default: HttpMethod.POST
        :param rate_limit_per_second: (experimental) The maximum number of requests per second to send to the HTTP invocation endpoint. Default: - Not rate limited

        :stability: experimental
        :exampleMetadata: infused

        Example::

            connection = events.Connection(self, "Connection",
                authorization=events.Authorization.api_key("x-api-key", SecretValue.secrets_manager("ApiSecretName")),
                description="Connection with API Key x-api-key"
            )
            
            destination = events.ApiDestination(self, "Destination",
                connection=connection,
                endpoint="https://example.com",
                description="Calling example.com with API key x-api-key"
            )
            
            rule = events.Rule(self, "Rule",
                schedule=events.Schedule.rate(cdk.Duration.minutes(1)),
                targets=[targets.ApiDestination(destination)]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056de4d4dfc5405f77afc31457d0430571baab1c1e5506a651947bae0b08cbec)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument api_destination_name", value=api_destination_name, expected_type=type_hints["api_destination_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument rate_limit_per_second", value=rate_limit_per_second, expected_type=type_hints["rate_limit_per_second"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection": connection,
            "endpoint": endpoint,
        }
        if api_destination_name is not None:
            self._values["api_destination_name"] = api_destination_name
        if description is not None:
            self._values["description"] = description
        if http_method is not None:
            self._values["http_method"] = http_method
        if rate_limit_per_second is not None:
            self._values["rate_limit_per_second"] = rate_limit_per_second

    @builtins.property
    def connection(self) -> "IConnection":
        '''(experimental) The ARN of the connection to use for the API destination.

        :stability: experimental
        '''
        result = self._values.get("connection")
        assert result is not None, "Required property 'connection' is missing"
        return typing.cast("IConnection", result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The URL to the HTTP invocation endpoint for the API destination..

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_destination_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the API destination.

        :default: - A unique name will be generated

        :stability: experimental
        '''
        result = self._values.get("api_destination_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the API destination.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_method(self) -> typing.Optional["HttpMethod"]:
        '''(experimental) The method to use for the request to the HTTP invocation endpoint.

        :default: HttpMethod.POST

        :stability: experimental
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional["HttpMethod"], result)

    @builtins.property
    def rate_limit_per_second(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of requests per second to send to the HTTP invocation endpoint.

        :default: - Not rate limited

        :stability: experimental
        '''
        result = self._values.get("rate_limit_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Archive(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.Archive",
):
    '''(experimental) Define an EventBridge Archive.

    :stability: experimental
    :resource: AWS::Events::Archive
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_events as events
        
        # detail: Any
        # duration: monocdk.Duration
        # event_bus: events.EventBus
        
        archive = events.Archive(self, "MyArchive",
            event_pattern=events.EventPattern(
                account=["account"],
                detail={
                    "detail_key": detail
                },
                detail_type=["detailType"],
                id=["id"],
                region=["region"],
                resources=["resources"],
                source=["source"],
                time=["time"],
                version=["version"]
            ),
            source_event_bus=event_bus,
        
            # the properties below are optional
            archive_name="archiveName",
            description="description",
            retention=duration
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source_event_bus: "IEventBus",
        event_pattern: typing.Union["EventPattern", typing.Dict[builtins.str, typing.Any]],
        archive_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source_event_bus: (experimental) The event source associated with the archive.
        :param event_pattern: (experimental) An event pattern to use to filter events sent to the archive.
        :param archive_name: (experimental) The name of the archive. Default: - Automatically generated
        :param description: (experimental) A description for the archive. Default: - none
        :param retention: (experimental) The number of days to retain events for. Default value is 0. If set to 0, events are retained indefinitely. Default: - Infinite

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bc4d139726aade8cf7cceeb4a81bd5339dcd2e866f97c5a7e51db1e6b064a5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ArchiveProps(
            source_event_bus=source_event_bus,
            event_pattern=event_pattern,
            archive_name=archive_name,
            description=description,
            retention=retention,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="archiveArn")
    def archive_arn(self) -> builtins.str:
        '''(experimental) The ARN of the archive created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "archiveArn"))

    @builtins.property
    @jsii.member(jsii_name="archiveName")
    def archive_name(self) -> builtins.str:
        '''(experimental) The archive name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "archiveName"))


class Authorization(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_events.Authorization",
):
    '''(experimental) Authorization type for an API Destination Connection.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        connection = events.Connection(self, "Connection",
            authorization=events.Authorization.api_key("x-api-key", SecretValue.secrets_manager("ApiSecretName")),
            description="Connection with API Key x-api-key"
        )
        
        destination = events.ApiDestination(self, "Destination",
            connection=connection,
            endpoint="https://example.com",
            description="Calling example.com with API key x-api-key"
        )
        
        rule = events.Rule(self, "Rule",
            schedule=events.Schedule.rate(cdk.Duration.minutes(1)),
            targets=[targets.ApiDestination(destination)]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="apiKey")
    @builtins.classmethod
    def api_key(
        cls,
        api_key_name: builtins.str,
        api_key_value: _SecretValue_c18506ef,
    ) -> "Authorization":
        '''(experimental) Use API key authorization.

        API key authorization has two components: an API key name and an API key value.
        What these are depends on the target of your connection.

        :param api_key_name: -
        :param api_key_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71b43935c8733a32c1408371563303b3fd842428bd5fc38091ada9f036a54f0)
            check_type(argname="argument api_key_name", value=api_key_name, expected_type=type_hints["api_key_name"])
            check_type(argname="argument api_key_value", value=api_key_value, expected_type=type_hints["api_key_value"])
        return typing.cast("Authorization", jsii.sinvoke(cls, "apiKey", [api_key_name, api_key_value]))

    @jsii.member(jsii_name="basic")
    @builtins.classmethod
    def basic(
        cls,
        username: builtins.str,
        password: _SecretValue_c18506ef,
    ) -> "Authorization":
        '''(experimental) Use username and password authorization.

        :param username: -
        :param password: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f1b0ec700d9ce94251d72a9bda95b32b2a70bf56ab8a2befcc4adb79a5aab0)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        return typing.cast("Authorization", jsii.sinvoke(cls, "basic", [username, password]))

    @jsii.member(jsii_name="oauth")
    @builtins.classmethod
    def oauth(
        cls,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: _SecretValue_c18506ef,
        http_method: "HttpMethod",
        body_parameters: typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]] = None,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]] = None,
    ) -> "Authorization":
        '''(experimental) Use OAuth authorization.

        :param authorization_endpoint: (experimental) The URL to the authorization endpoint.
        :param client_id: (experimental) The client ID to use for OAuth authorization for the connection.
        :param client_secret: (experimental) The client secret associated with the client ID to use for OAuth authorization for the connection.
        :param http_method: (experimental) The method to use for the authorization request. (Can only choose POST, GET or PUT).
        :param body_parameters: (experimental) Additional string parameters to add to the OAuth request body. Default: - No additional parameters
        :param header_parameters: (experimental) Additional string parameters to add to the OAuth request header. Default: - No additional parameters
        :param query_string_parameters: (experimental) Additional string parameters to add to the OAuth request query string. Default: - No additional parameters

        :stability: experimental
        '''
        props = OAuthAuthorizationProps(
            authorization_endpoint=authorization_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            http_method=http_method,
            body_parameters=body_parameters,
            header_parameters=header_parameters,
            query_string_parameters=query_string_parameters,
        )

        return typing.cast("Authorization", jsii.sinvoke(cls, "oauth", [props]))


class _AuthorizationProxy(Authorization):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Authorization).__jsii_proxy_class__ = lambda : _AuthorizationProxy


@jsii.data_type(
    jsii_type="monocdk.aws_events.BaseArchiveProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_pattern": "eventPattern",
        "archive_name": "archiveName",
        "description": "description",
        "retention": "retention",
    },
)
class BaseArchiveProps:
    def __init__(
        self,
        *,
        event_pattern: typing.Union["EventPattern", typing.Dict[builtins.str, typing.Any]],
        archive_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) The event archive base properties.

        :param event_pattern: (experimental) An event pattern to use to filter events sent to the archive.
        :param archive_name: (experimental) The name of the archive. Default: - Automatically generated
        :param description: (experimental) A description for the archive. Default: - none
        :param retention: (experimental) The number of days to retain events for. Default value is 0. If set to 0, events are retained indefinitely. Default: - Infinite

        :stability: experimental
        :exampleMetadata: infused

        Example::

            bus = events.EventBus(self, "bus",
                event_bus_name="MyCustomEventBus"
            )
            
            bus.archive("MyArchive",
                archive_name="MyCustomEventBusArchive",
                description="MyCustomerEventBus Archive",
                event_pattern=events.aws_events.EventPattern(
                    account=[Stack.of(self).account]
                ),
                retention=Duration.days(365)
            )
        '''
        if isinstance(event_pattern, dict):
            event_pattern = EventPattern(**event_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c427c50bf93d6b7ac5b531f350c35d3b4723158f4b79129729743df72791d10)
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument archive_name", value=archive_name, expected_type=type_hints["archive_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_pattern": event_pattern,
        }
        if archive_name is not None:
            self._values["archive_name"] = archive_name
        if description is not None:
            self._values["description"] = description
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def event_pattern(self) -> "EventPattern":
        '''(experimental) An event pattern to use to filter events sent to the archive.

        :stability: experimental
        '''
        result = self._values.get("event_pattern")
        assert result is not None, "Required property 'event_pattern' is missing"
        return typing.cast("EventPattern", result)

    @builtins.property
    def archive_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the archive.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("archive_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the archive.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The number of days to retain events for.

        Default value is 0. If set to 0, events are retained indefinitely.

        :default: - Infinite

        :stability: experimental
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseArchiveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApiDestination(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.CfnApiDestination",
):
    '''A CloudFormation ``AWS::Events::ApiDestination``.

    Creates an API destination, which is an HTTP invocation endpoint configured as a target for events.

    When using ApiDesinations with OAuth authentication we recommend these best practices:

    - Create a secret in Secrets Manager with your OAuth credentials.
    - Reference that secret in your CloudFormation template for ``AWS::Events::Connection`` using CloudFormation dynamic reference syntax. For more information, see `Secrets Manager secrets <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ .

    When the Connection resource is created the secret will be passed to EventBridge and stored in the customer account using “Service Linked Secrets,” effectively creating two secrets. This will minimize the cost because the original secret is only accessed when a CloudFormation template is created or updated, not every time an event is sent to the ApiDestination. The secret stored in the customer account by EventBridge is the one used for each event sent to the ApiDestination and AWS is responsible for the fees.
    .. epigraph::

       The secret stored in the customer account by EventBridge can’t be updated directly, only when a CloudFormation template is updated.

    For examples of CloudFormation templates that use secrets, see `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#aws-resource-events-connection--examples>`_ .

    :cloudformationResource: AWS::Events::ApiDestination
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_events as events
        
        cfn_api_destination = events.CfnApiDestination(self, "MyCfnApiDestination",
            connection_arn="connectionArn",
            http_method="httpMethod",
            invocation_endpoint="invocationEndpoint",
        
            # the properties below are optional
            description="description",
            invocation_rate_limit_per_second=123,
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        connection_arn: builtins.str,
        http_method: builtins.str,
        invocation_endpoint: builtins.str,
        description: typing.Optional[builtins.str] = None,
        invocation_rate_limit_per_second: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Events::ApiDestination``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param connection_arn: The ARN of the connection to use for the API destination. The destination endpoint must support the authorization type specified for the connection.
        :param http_method: The method to use for the request to the HTTP invocation endpoint.
        :param invocation_endpoint: The URL to the HTTP invocation endpoint for the API destination.
        :param description: A description for the API destination to create.
        :param invocation_rate_limit_per_second: The maximum number of requests per second to send to the HTTP invocation endpoint.
        :param name: The name for the API destination to create.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414e043e35e7ff34985ad10d0117c16197dee28a3dc677edf475cacd45c2525e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApiDestinationProps(
            connection_arn=connection_arn,
            http_method=http_method,
            invocation_endpoint=invocation_endpoint,
            description=description,
            invocation_rate_limit_per_second=invocation_rate_limit_per_second,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c283e206d7b7192c36ff64efe32f7e0528f57aa3feb3cb3cf57a6e493fed1555)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b6f21401e9ff19a502dde156acd474973ef1bf49ab1462c7bb1249f5b24a6a9)
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
        '''The ARN of the API destination that was created by the request.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''The ARN of the connection to use for the API destination.

        The destination endpoint must support the authorization type specified for the connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-connectionarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @connection_arn.setter
    def connection_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09fbe49e021c773790347138d6558ab8a4a9f84aab1e903aace14addb11937ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionArn", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        '''The method to use for the request to the HTTP invocation endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-httpmethod
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb155200f85150bbead5876ba5d1a0310028ff41d2b9d203f4d2e7d8f445731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="invocationEndpoint")
    def invocation_endpoint(self) -> builtins.str:
        '''The URL to the HTTP invocation endpoint for the API destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-invocationendpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "invocationEndpoint"))

    @invocation_endpoint.setter
    def invocation_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935406b0fc6c8042d6d7a0455bd2082e25fa24ee2beef12f5998e225f04a105e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the API destination to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a5a5d8d9a9ff34753b2732974cd0d0d6aed14ab50b6a39e73fbe3472c8ef14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="invocationRateLimitPerSecond")
    def invocation_rate_limit_per_second(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of requests per second to send to the HTTP invocation endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-invocationratelimitpersecond
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "invocationRateLimitPerSecond"))

    @invocation_rate_limit_per_second.setter
    def invocation_rate_limit_per_second(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce9144ed475cbef1abc3d42592613905e4104f401044f1df9af068fee11184e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationRateLimitPerSecond", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the API destination to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b8ed3846d787fdb89dd21cf23218a8d8da30ffc66f1928a73d0485ada5a073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_events.CfnApiDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_arn": "connectionArn",
        "http_method": "httpMethod",
        "invocation_endpoint": "invocationEndpoint",
        "description": "description",
        "invocation_rate_limit_per_second": "invocationRateLimitPerSecond",
        "name": "name",
    },
)
class CfnApiDestinationProps:
    def __init__(
        self,
        *,
        connection_arn: builtins.str,
        http_method: builtins.str,
        invocation_endpoint: builtins.str,
        description: typing.Optional[builtins.str] = None,
        invocation_rate_limit_per_second: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnApiDestination``.

        :param connection_arn: The ARN of the connection to use for the API destination. The destination endpoint must support the authorization type specified for the connection.
        :param http_method: The method to use for the request to the HTTP invocation endpoint.
        :param invocation_endpoint: The URL to the HTTP invocation endpoint for the API destination.
        :param description: A description for the API destination to create.
        :param invocation_rate_limit_per_second: The maximum number of requests per second to send to the HTTP invocation endpoint.
        :param name: The name for the API destination to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            cfn_api_destination_props = events.CfnApiDestinationProps(
                connection_arn="connectionArn",
                http_method="httpMethod",
                invocation_endpoint="invocationEndpoint",
            
                # the properties below are optional
                description="description",
                invocation_rate_limit_per_second=123,
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217318526b0830df863f9674be412e00b4c13393794f9009fc6d70c2dc810e56)
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument invocation_endpoint", value=invocation_endpoint, expected_type=type_hints["invocation_endpoint"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument invocation_rate_limit_per_second", value=invocation_rate_limit_per_second, expected_type=type_hints["invocation_rate_limit_per_second"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_arn": connection_arn,
            "http_method": http_method,
            "invocation_endpoint": invocation_endpoint,
        }
        if description is not None:
            self._values["description"] = description
        if invocation_rate_limit_per_second is not None:
            self._values["invocation_rate_limit_per_second"] = invocation_rate_limit_per_second
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def connection_arn(self) -> builtins.str:
        '''The ARN of the connection to use for the API destination.

        The destination endpoint must support the authorization type specified for the connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-connectionarn
        '''
        result = self._values.get("connection_arn")
        assert result is not None, "Required property 'connection_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_method(self) -> builtins.str:
        '''The method to use for the request to the HTTP invocation endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-httpmethod
        '''
        result = self._values.get("http_method")
        assert result is not None, "Required property 'http_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invocation_endpoint(self) -> builtins.str:
        '''The URL to the HTTP invocation endpoint for the API destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-invocationendpoint
        '''
        result = self._values.get("invocation_endpoint")
        assert result is not None, "Required property 'invocation_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the API destination to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invocation_rate_limit_per_second(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of requests per second to send to the HTTP invocation endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-invocationratelimitpersecond
        '''
        result = self._values.get("invocation_rate_limit_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the API destination to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-apidestination.html#cfn-events-apidestination-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnArchive(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.CfnArchive",
):
    '''A CloudFormation ``AWS::Events::Archive``.

    Creates an archive of events with the specified settings. When you create an archive, incoming events might not immediately start being sent to the archive. Allow a short period of time for changes to take effect. If you do not specify a pattern to filter events sent to the archive, all events are sent to the archive except replayed events. Replayed events are not sent to an archive.

    :cloudformationResource: AWS::Events::Archive
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_events as events
        
        # event_pattern: Any
        
        cfn_archive = events.CfnArchive(self, "MyCfnArchive",
            source_arn="sourceArn",
        
            # the properties below are optional
            archive_name="archiveName",
            description="description",
            event_pattern=event_pattern,
            retention_days=123
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        source_arn: builtins.str,
        archive_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Any = None,
        retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::Events::Archive``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param source_arn: The ARN of the event bus that sends events to the archive.
        :param archive_name: The name for the archive to create.
        :param description: A description for the archive.
        :param event_pattern: An event pattern to use to filter events sent to the archive.
        :param retention_days: The number of days to retain events for. Default value is 0. If set to 0, events are retained indefinitely
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899d2177eec6babc60e1a9746198a30b954eb998f5946da59a261cfe2d4ec3be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnArchiveProps(
            source_arn=source_arn,
            archive_name=archive_name,
            description=description,
            event_pattern=event_pattern,
            retention_days=retention_days,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ab1d304fee7af002fa70b35d461e4a6469efe75289a7d39185dee073549900)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1eb69c1b8f93a1f4997e93578de99b8c43db1f100fe5a88bddb22a164ccb540)
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
        '''The ARN of the archive created.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="eventPattern")
    def event_pattern(self) -> typing.Any:
        '''An event pattern to use to filter events sent to the archive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-eventpattern
        '''
        return typing.cast(typing.Any, jsii.get(self, "eventPattern"))

    @event_pattern.setter
    def event_pattern(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e08cf07e3933c4c27f841ea5420e2cddb9ab5a2b2b2343930c9a056448e155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventPattern", value)

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''The ARN of the event bus that sends events to the archive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-sourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @source_arn.setter
    def source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b812646ea7214910843bd9d365e0f413340f8ce942a81c40413e1a06d4787dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="archiveName")
    def archive_name(self) -> typing.Optional[builtins.str]:
        '''The name for the archive to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-archivename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "archiveName"))

    @archive_name.setter
    def archive_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c76082608f39f368f3a964d0dc223157177db6749767bc328c1f3e63d71a7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the archive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c16ab568e2a59f5edb1e4f667a8436aafa061c3431850431bf4064b2316837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain events for.

        Default value is 0. If set to 0, events are retained indefinitely

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-retentiondays
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b095110a80ad767e3d670cbd4c1e9142d975daaf8555b83c6ed203472748d3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value)


@jsii.data_type(
    jsii_type="monocdk.aws_events.CfnArchiveProps",
    jsii_struct_bases=[],
    name_mapping={
        "source_arn": "sourceArn",
        "archive_name": "archiveName",
        "description": "description",
        "event_pattern": "eventPattern",
        "retention_days": "retentionDays",
    },
)
class CfnArchiveProps:
    def __init__(
        self,
        *,
        source_arn: builtins.str,
        archive_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Any = None,
        retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnArchive``.

        :param source_arn: The ARN of the event bus that sends events to the archive.
        :param archive_name: The name for the archive to create.
        :param description: A description for the archive.
        :param event_pattern: An event pattern to use to filter events sent to the archive.
        :param retention_days: The number of days to retain events for. Default value is 0. If set to 0, events are retained indefinitely

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            # event_pattern: Any
            
            cfn_archive_props = events.CfnArchiveProps(
                source_arn="sourceArn",
            
                # the properties below are optional
                archive_name="archiveName",
                description="description",
                event_pattern=event_pattern,
                retention_days=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ace036bf5ad1ebe4e0fc424dc1df99e530ca0048462bdcbc8973a331c37aaf)
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument archive_name", value=archive_name, expected_type=type_hints["archive_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_arn": source_arn,
        }
        if archive_name is not None:
            self._values["archive_name"] = archive_name
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if retention_days is not None:
            self._values["retention_days"] = retention_days

    @builtins.property
    def source_arn(self) -> builtins.str:
        '''The ARN of the event bus that sends events to the archive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-sourcearn
        '''
        result = self._values.get("source_arn")
        assert result is not None, "Required property 'source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_name(self) -> typing.Optional[builtins.str]:
        '''The name for the archive to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-archivename
        '''
        result = self._values.get("archive_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the archive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_pattern(self) -> typing.Any:
        '''An event pattern to use to filter events sent to the archive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-eventpattern
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Any, result)

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain events for.

        Default value is 0. If set to 0, events are retained indefinitely

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-retentiondays
        '''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnArchiveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnConnection(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.CfnConnection",
):
    '''A CloudFormation ``AWS::Events::Connection``.

    Creates a connection. A connection defines the authorization type and credentials to use for authorization with an API destination HTTP endpoint.

    :cloudformationResource: AWS::Events::Connection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_events as events
        
        cfn_connection = events.CfnConnection(self, "MyCfnConnection",
            authorization_type="authorizationType",
            auth_parameters=events.CfnConnection.AuthParametersProperty(
                api_key_auth_parameters=events.CfnConnection.ApiKeyAuthParametersProperty(
                    api_key_name="apiKeyName",
                    api_key_value="apiKeyValue"
                ),
                basic_auth_parameters=events.CfnConnection.BasicAuthParametersProperty(
                    password="password",
                    username="username"
                ),
                invocation_http_parameters=events.CfnConnection.ConnectionHttpParametersProperty(
                    body_parameters=[events.CfnConnection.ParameterProperty(
                        key="key",
                        value="value",
        
                        # the properties below are optional
                        is_value_secret=False
                    )],
                    header_parameters=[events.CfnConnection.ParameterProperty(
                        key="key",
                        value="value",
        
                        # the properties below are optional
                        is_value_secret=False
                    )],
                    query_string_parameters=[events.CfnConnection.ParameterProperty(
                        key="key",
                        value="value",
        
                        # the properties below are optional
                        is_value_secret=False
                    )]
                ),
                o_auth_parameters=events.CfnConnection.OAuthParametersProperty(
                    authorization_endpoint="authorizationEndpoint",
                    client_parameters=events.CfnConnection.ClientParametersProperty(
                        client_id="clientId",
                        client_secret="clientSecret"
                    ),
                    http_method="httpMethod",
        
                    # the properties below are optional
                    o_auth_http_parameters=events.CfnConnection.ConnectionHttpParametersProperty(
                        body_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
        
                            # the properties below are optional
                            is_value_secret=False
                        )],
                        header_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
        
                            # the properties below are optional
                            is_value_secret=False
                        )],
                        query_string_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
        
                            # the properties below are optional
                            is_value_secret=False
                        )]
                    )
                )
            ),
        
            # the properties below are optional
            description="description",
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        authorization_type: builtins.str,
        auth_parameters: typing.Union[typing.Union["CfnConnection.AuthParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Events::Connection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authorization_type: The type of authorization to use for the connection. .. epigraph:: OAUTH tokens are refreshed when a 401 or 407 response is returned.
        :param auth_parameters: A ``CreateConnectionAuthRequestParameters`` object that contains the authorization parameters to use to authorize with the endpoint.
        :param description: A description for the connection to create.
        :param name: The name for the connection to create.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a7ca17db9837a39fffe498a415aeb3d2140262e6633705e0844a10ba8191b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectionProps(
            authorization_type=authorization_type,
            auth_parameters=auth_parameters,
            description=description,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961a11744a95d058912609c5ab6f17ff64af8bcdc99dc31210c673aa9aed75ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b641eb8a7d7c7ff37b4a32e378821a789c5cd0c0445f6bf48e5abf5741fef7d1)
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
        '''The ARN of the connection that was created by the request.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSecretArn")
    def attr_secret_arn(self) -> builtins.str:
        '''The ARN for the secret created for the connection.

        :cloudformationAttribute: SecretArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSecretArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> builtins.str:
        '''The type of authorization to use for the connection.

        .. epigraph::

           OAUTH tokens are refreshed when a 401 or 407 response is returned.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#cfn-events-connection-authorizationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "authorizationType"))

    @authorization_type.setter
    def authorization_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e656176a4db421f7835ed57a5ef1bced96c1c3066e8a5f271eb1ae4007fc9462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationType", value)

    @builtins.property
    @jsii.member(jsii_name="authParameters")
    def auth_parameters(
        self,
    ) -> typing.Union["CfnConnection.AuthParametersProperty", _IResolvable_a771d0ef]:
        '''A ``CreateConnectionAuthRequestParameters`` object that contains the authorization parameters to use to authorize with the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#cfn-events-connection-authparameters
        '''
        return typing.cast(typing.Union["CfnConnection.AuthParametersProperty", _IResolvable_a771d0ef], jsii.get(self, "authParameters"))

    @auth_parameters.setter
    def auth_parameters(
        self,
        value: typing.Union["CfnConnection.AuthParametersProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ccddce0a389219095b5b82a1c681c7fdb0160f7dbd8bd7b5f45422beb47b32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authParameters", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the connection to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#cfn-events-connection-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab54ed9b79591eded96ea1065fa935ddf91988a5cf89d07940e4f1d789697a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the connection to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#cfn-events-connection-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1d4ed239ba0505cc9ca7dee1585681b3302afb26f21677c79c936238c81011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnConnection.ApiKeyAuthParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key_name": "apiKeyName", "api_key_value": "apiKeyValue"},
    )
    class ApiKeyAuthParametersProperty:
        def __init__(
            self,
            *,
            api_key_name: builtins.str,
            api_key_value: builtins.str,
        ) -> None:
            '''Contains the API key authorization parameters for the connection.

            :param api_key_name: The name of the API key to use for authorization.
            :param api_key_value: The value for the API key to use for authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-apikeyauthparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                api_key_auth_parameters_property = events.CfnConnection.ApiKeyAuthParametersProperty(
                    api_key_name="apiKeyName",
                    api_key_value="apiKeyValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8a4472ae22623c757fc2a301322104c8c3a143767b80c16ab3ecbcdf80a8377)
                check_type(argname="argument api_key_name", value=api_key_name, expected_type=type_hints["api_key_name"])
                check_type(argname="argument api_key_value", value=api_key_value, expected_type=type_hints["api_key_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "api_key_name": api_key_name,
                "api_key_value": api_key_value,
            }

        @builtins.property
        def api_key_name(self) -> builtins.str:
            '''The name of the API key to use for authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-apikeyauthparameters.html#cfn-events-connection-apikeyauthparameters-apikeyname
            '''
            result = self._values.get("api_key_name")
            assert result is not None, "Required property 'api_key_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def api_key_value(self) -> builtins.str:
            '''The value for the API key to use for authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-apikeyauthparameters.html#cfn-events-connection-apikeyauthparameters-apikeyvalue
            '''
            result = self._values.get("api_key_value")
            assert result is not None, "Required property 'api_key_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiKeyAuthParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnConnection.AuthParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_key_auth_parameters": "apiKeyAuthParameters",
            "basic_auth_parameters": "basicAuthParameters",
            "invocation_http_parameters": "invocationHttpParameters",
            "o_auth_parameters": "oAuthParameters",
        },
    )
    class AuthParametersProperty:
        def __init__(
            self,
            *,
            api_key_auth_parameters: typing.Optional[typing.Union[typing.Union["CfnConnection.ApiKeyAuthParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            basic_auth_parameters: typing.Optional[typing.Union[typing.Union["CfnConnection.BasicAuthParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            invocation_http_parameters: typing.Optional[typing.Union[typing.Union["CfnConnection.ConnectionHttpParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            o_auth_parameters: typing.Optional[typing.Union[typing.Union["CfnConnection.OAuthParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains the authorization parameters to use for the connection.

            :param api_key_auth_parameters: The API Key parameters to use for authorization.
            :param basic_auth_parameters: The authorization parameters for Basic authorization.
            :param invocation_http_parameters: Additional parameters for the connection that are passed through with every invocation to the HTTP endpoint.
            :param o_auth_parameters: The OAuth parameters to use for authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-authparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                auth_parameters_property = events.CfnConnection.AuthParametersProperty(
                    api_key_auth_parameters=events.CfnConnection.ApiKeyAuthParametersProperty(
                        api_key_name="apiKeyName",
                        api_key_value="apiKeyValue"
                    ),
                    basic_auth_parameters=events.CfnConnection.BasicAuthParametersProperty(
                        password="password",
                        username="username"
                    ),
                    invocation_http_parameters=events.CfnConnection.ConnectionHttpParametersProperty(
                        body_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
                
                            # the properties below are optional
                            is_value_secret=False
                        )],
                        header_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
                
                            # the properties below are optional
                            is_value_secret=False
                        )],
                        query_string_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
                
                            # the properties below are optional
                            is_value_secret=False
                        )]
                    ),
                    o_auth_parameters=events.CfnConnection.OAuthParametersProperty(
                        authorization_endpoint="authorizationEndpoint",
                        client_parameters=events.CfnConnection.ClientParametersProperty(
                            client_id="clientId",
                            client_secret="clientSecret"
                        ),
                        http_method="httpMethod",
                
                        # the properties below are optional
                        o_auth_http_parameters=events.CfnConnection.ConnectionHttpParametersProperty(
                            body_parameters=[events.CfnConnection.ParameterProperty(
                                key="key",
                                value="value",
                
                                # the properties below are optional
                                is_value_secret=False
                            )],
                            header_parameters=[events.CfnConnection.ParameterProperty(
                                key="key",
                                value="value",
                
                                # the properties below are optional
                                is_value_secret=False
                            )],
                            query_string_parameters=[events.CfnConnection.ParameterProperty(
                                key="key",
                                value="value",
                
                                # the properties below are optional
                                is_value_secret=False
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93027c4d4e7c1e705f4997047909ba2ea831fdd236ba9e855a7513999f1443fa)
                check_type(argname="argument api_key_auth_parameters", value=api_key_auth_parameters, expected_type=type_hints["api_key_auth_parameters"])
                check_type(argname="argument basic_auth_parameters", value=basic_auth_parameters, expected_type=type_hints["basic_auth_parameters"])
                check_type(argname="argument invocation_http_parameters", value=invocation_http_parameters, expected_type=type_hints["invocation_http_parameters"])
                check_type(argname="argument o_auth_parameters", value=o_auth_parameters, expected_type=type_hints["o_auth_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key_auth_parameters is not None:
                self._values["api_key_auth_parameters"] = api_key_auth_parameters
            if basic_auth_parameters is not None:
                self._values["basic_auth_parameters"] = basic_auth_parameters
            if invocation_http_parameters is not None:
                self._values["invocation_http_parameters"] = invocation_http_parameters
            if o_auth_parameters is not None:
                self._values["o_auth_parameters"] = o_auth_parameters

        @builtins.property
        def api_key_auth_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnConnection.ApiKeyAuthParametersProperty", _IResolvable_a771d0ef]]:
            '''The API Key parameters to use for authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-authparameters.html#cfn-events-connection-authparameters-apikeyauthparameters
            '''
            result = self._values.get("api_key_auth_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnConnection.ApiKeyAuthParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def basic_auth_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnConnection.BasicAuthParametersProperty", _IResolvable_a771d0ef]]:
            '''The authorization parameters for Basic authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-authparameters.html#cfn-events-connection-authparameters-basicauthparameters
            '''
            result = self._values.get("basic_auth_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnConnection.BasicAuthParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def invocation_http_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnConnection.ConnectionHttpParametersProperty", _IResolvable_a771d0ef]]:
            '''Additional parameters for the connection that are passed through with every invocation to the HTTP endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-authparameters.html#cfn-events-connection-authparameters-invocationhttpparameters
            '''
            result = self._values.get("invocation_http_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnConnection.ConnectionHttpParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def o_auth_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnConnection.OAuthParametersProperty", _IResolvable_a771d0ef]]:
            '''The OAuth parameters to use for authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-authparameters.html#cfn-events-connection-authparameters-oauthparameters
            '''
            result = self._values.get("o_auth_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnConnection.OAuthParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnConnection.BasicAuthParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class BasicAuthParametersProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''Contains the Basic authorization parameters for the connection.

            :param password: The password associated with the user name to use for Basic authorization.
            :param username: The user name to use for Basic authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-basicauthparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                basic_auth_parameters_property = events.CfnConnection.BasicAuthParametersProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8cb02396d3f38aafa22abc29452a43619507ce54869d398b3d4d162185ce467)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''The password associated with the user name to use for Basic authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-basicauthparameters.html#cfn-events-connection-basicauthparameters-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''The user name to use for Basic authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-basicauthparameters.html#cfn-events-connection-basicauthparameters-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnConnection.ClientParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
    )
    class ClientParametersProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
        ) -> None:
            '''Contains the OAuth authorization parameters to use for the connection.

            :param client_id: The client ID to use for OAuth authorization.
            :param client_secret: The client secret assciated with the client ID to use for OAuth authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-clientparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                client_parameters_property = events.CfnConnection.ClientParametersProperty(
                    client_id="clientId",
                    client_secret="clientSecret"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d8f6d995e325c0cbcb0ead49053359ed637432382566ac0c4e7c402db90ceee)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }

        @builtins.property
        def client_id(self) -> builtins.str:
            '''The client ID to use for OAuth authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-clientparameters.html#cfn-events-connection-clientparameters-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''The client secret assciated with the client ID to use for OAuth authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-clientparameters.html#cfn-events-connection-clientparameters-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnConnection.ConnectionHttpParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body_parameters": "bodyParameters",
            "header_parameters": "headerParameters",
            "query_string_parameters": "queryStringParameters",
        },
    )
    class ConnectionHttpParametersProperty:
        def __init__(
            self,
            *,
            body_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnConnection.ParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            header_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnConnection.ParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            query_string_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnConnection.ParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Contains additional parameters for the connection.

            :param body_parameters: Contains additional body string parameters for the connection.
            :param header_parameters: Contains additional header parameters for the connection.
            :param query_string_parameters: Contains additional query string parameters for the connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-connectionhttpparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                connection_http_parameters_property = events.CfnConnection.ConnectionHttpParametersProperty(
                    body_parameters=[events.CfnConnection.ParameterProperty(
                        key="key",
                        value="value",
                
                        # the properties below are optional
                        is_value_secret=False
                    )],
                    header_parameters=[events.CfnConnection.ParameterProperty(
                        key="key",
                        value="value",
                
                        # the properties below are optional
                        is_value_secret=False
                    )],
                    query_string_parameters=[events.CfnConnection.ParameterProperty(
                        key="key",
                        value="value",
                
                        # the properties below are optional
                        is_value_secret=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f946f08a60b24a2b7a590df62875c873425d3333f6f3a81c7f651381def9a98a)
                check_type(argname="argument body_parameters", value=body_parameters, expected_type=type_hints["body_parameters"])
                check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
                check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body_parameters is not None:
                self._values["body_parameters"] = body_parameters
            if header_parameters is not None:
                self._values["header_parameters"] = header_parameters
            if query_string_parameters is not None:
                self._values["query_string_parameters"] = query_string_parameters

        @builtins.property
        def body_parameters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConnection.ParameterProperty", _IResolvable_a771d0ef]]]]:
            '''Contains additional body string parameters for the connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-connectionhttpparameters.html#cfn-events-connection-connectionhttpparameters-bodyparameters
            '''
            result = self._values.get("body_parameters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConnection.ParameterProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def header_parameters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConnection.ParameterProperty", _IResolvable_a771d0ef]]]]:
            '''Contains additional header parameters for the connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-connectionhttpparameters.html#cfn-events-connection-connectionhttpparameters-headerparameters
            '''
            result = self._values.get("header_parameters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConnection.ParameterProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def query_string_parameters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConnection.ParameterProperty", _IResolvable_a771d0ef]]]]:
            '''Contains additional query string parameters for the connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-connectionhttpparameters.html#cfn-events-connection-connectionhttpparameters-querystringparameters
            '''
            result = self._values.get("query_string_parameters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConnection.ParameterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionHttpParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnConnection.OAuthParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_endpoint": "authorizationEndpoint",
            "client_parameters": "clientParameters",
            "http_method": "httpMethod",
            "o_auth_http_parameters": "oAuthHttpParameters",
        },
    )
    class OAuthParametersProperty:
        def __init__(
            self,
            *,
            authorization_endpoint: builtins.str,
            client_parameters: typing.Union[typing.Union["CfnConnection.ClientParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            http_method: builtins.str,
            o_auth_http_parameters: typing.Optional[typing.Union[typing.Union["CfnConnection.ConnectionHttpParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains the OAuth authorization parameters to use for the connection.

            :param authorization_endpoint: The URL to the authorization endpoint when OAuth is specified as the authorization type.
            :param client_parameters: A ``CreateConnectionOAuthClientRequestParameters`` object that contains the client parameters for OAuth authorization.
            :param http_method: The method to use for the authorization request.
            :param o_auth_http_parameters: A ``ConnectionHttpParameters`` object that contains details about the additional parameters to use for the connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-oauthparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                o_auth_parameters_property = events.CfnConnection.OAuthParametersProperty(
                    authorization_endpoint="authorizationEndpoint",
                    client_parameters=events.CfnConnection.ClientParametersProperty(
                        client_id="clientId",
                        client_secret="clientSecret"
                    ),
                    http_method="httpMethod",
                
                    # the properties below are optional
                    o_auth_http_parameters=events.CfnConnection.ConnectionHttpParametersProperty(
                        body_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
                
                            # the properties below are optional
                            is_value_secret=False
                        )],
                        header_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
                
                            # the properties below are optional
                            is_value_secret=False
                        )],
                        query_string_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
                
                            # the properties below are optional
                            is_value_secret=False
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ea33a9104133a379688ce59075f05e62f0a4a5a265ff17c9ecbfb538924ed04)
                check_type(argname="argument authorization_endpoint", value=authorization_endpoint, expected_type=type_hints["authorization_endpoint"])
                check_type(argname="argument client_parameters", value=client_parameters, expected_type=type_hints["client_parameters"])
                check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
                check_type(argname="argument o_auth_http_parameters", value=o_auth_http_parameters, expected_type=type_hints["o_auth_http_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "authorization_endpoint": authorization_endpoint,
                "client_parameters": client_parameters,
                "http_method": http_method,
            }
            if o_auth_http_parameters is not None:
                self._values["o_auth_http_parameters"] = o_auth_http_parameters

        @builtins.property
        def authorization_endpoint(self) -> builtins.str:
            '''The URL to the authorization endpoint when OAuth is specified as the authorization type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-oauthparameters.html#cfn-events-connection-oauthparameters-authorizationendpoint
            '''
            result = self._values.get("authorization_endpoint")
            assert result is not None, "Required property 'authorization_endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_parameters(
            self,
        ) -> typing.Union["CfnConnection.ClientParametersProperty", _IResolvable_a771d0ef]:
            '''A ``CreateConnectionOAuthClientRequestParameters`` object that contains the client parameters for OAuth authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-oauthparameters.html#cfn-events-connection-oauthparameters-clientparameters
            '''
            result = self._values.get("client_parameters")
            assert result is not None, "Required property 'client_parameters' is missing"
            return typing.cast(typing.Union["CfnConnection.ClientParametersProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def http_method(self) -> builtins.str:
            '''The method to use for the authorization request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-oauthparameters.html#cfn-events-connection-oauthparameters-httpmethod
            '''
            result = self._values.get("http_method")
            assert result is not None, "Required property 'http_method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def o_auth_http_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnConnection.ConnectionHttpParametersProperty", _IResolvable_a771d0ef]]:
            '''A ``ConnectionHttpParameters`` object that contains details about the additional parameters to use for the connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-oauthparameters.html#cfn-events-connection-oauthparameters-oauthhttpparameters
            '''
            result = self._values.get("o_auth_http_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnConnection.ConnectionHttpParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuthParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnConnection.ParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "value": "value",
            "is_value_secret": "isValueSecret",
        },
    )
    class ParameterProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            value: builtins.str,
            is_value_secret: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Additional query string parameter for the connection.

            You can include up to 100 additional query string parameters per request. Each additional parameter counts towards the event payload size, which cannot exceed 64 KB.

            :param key: The key for a query string parameter.
            :param value: The value associated with the key for the query string parameter.
            :param is_value_secret: Specifies whether the value is secret.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-parameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                parameter_property = events.CfnConnection.ParameterProperty(
                    key="key",
                    value="value",
                
                    # the properties below are optional
                    is_value_secret=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1111de1449175e78941c91b4aa0ab29ebff934586c1a49b0e5a47ddac1582c06)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument is_value_secret", value=is_value_secret, expected_type=type_hints["is_value_secret"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }
            if is_value_secret is not None:
                self._values["is_value_secret"] = is_value_secret

        @builtins.property
        def key(self) -> builtins.str:
            '''The key for a query string parameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-parameter.html#cfn-events-connection-parameter-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value associated with the key for the query string parameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-parameter.html#cfn-events-connection-parameter-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def is_value_secret(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether the value is secret.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-connection-parameter.html#cfn-events-connection-parameter-isvaluesecret
            '''
            result = self._values.get("is_value_secret")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_events.CfnConnectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_type": "authorizationType",
        "auth_parameters": "authParameters",
        "description": "description",
        "name": "name",
    },
)
class CfnConnectionProps:
    def __init__(
        self,
        *,
        authorization_type: builtins.str,
        auth_parameters: typing.Union[typing.Union[CfnConnection.AuthParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnection``.

        :param authorization_type: The type of authorization to use for the connection. .. epigraph:: OAUTH tokens are refreshed when a 401 or 407 response is returned.
        :param auth_parameters: A ``CreateConnectionAuthRequestParameters`` object that contains the authorization parameters to use to authorize with the endpoint.
        :param description: A description for the connection to create.
        :param name: The name for the connection to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            cfn_connection_props = events.CfnConnectionProps(
                authorization_type="authorizationType",
                auth_parameters=events.CfnConnection.AuthParametersProperty(
                    api_key_auth_parameters=events.CfnConnection.ApiKeyAuthParametersProperty(
                        api_key_name="apiKeyName",
                        api_key_value="apiKeyValue"
                    ),
                    basic_auth_parameters=events.CfnConnection.BasicAuthParametersProperty(
                        password="password",
                        username="username"
                    ),
                    invocation_http_parameters=events.CfnConnection.ConnectionHttpParametersProperty(
                        body_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
            
                            # the properties below are optional
                            is_value_secret=False
                        )],
                        header_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
            
                            # the properties below are optional
                            is_value_secret=False
                        )],
                        query_string_parameters=[events.CfnConnection.ParameterProperty(
                            key="key",
                            value="value",
            
                            # the properties below are optional
                            is_value_secret=False
                        )]
                    ),
                    o_auth_parameters=events.CfnConnection.OAuthParametersProperty(
                        authorization_endpoint="authorizationEndpoint",
                        client_parameters=events.CfnConnection.ClientParametersProperty(
                            client_id="clientId",
                            client_secret="clientSecret"
                        ),
                        http_method="httpMethod",
            
                        # the properties below are optional
                        o_auth_http_parameters=events.CfnConnection.ConnectionHttpParametersProperty(
                            body_parameters=[events.CfnConnection.ParameterProperty(
                                key="key",
                                value="value",
            
                                # the properties below are optional
                                is_value_secret=False
                            )],
                            header_parameters=[events.CfnConnection.ParameterProperty(
                                key="key",
                                value="value",
            
                                # the properties below are optional
                                is_value_secret=False
                            )],
                            query_string_parameters=[events.CfnConnection.ParameterProperty(
                                key="key",
                                value="value",
            
                                # the properties below are optional
                                is_value_secret=False
                            )]
                        )
                    )
                ),
            
                # the properties below are optional
                description="description",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59ef04d1a0b2e2173f9eea534a6f5dc49ca1a590c337c6d6386c3d42f282861)
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument auth_parameters", value=auth_parameters, expected_type=type_hints["auth_parameters"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_type": authorization_type,
            "auth_parameters": auth_parameters,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def authorization_type(self) -> builtins.str:
        '''The type of authorization to use for the connection.

        .. epigraph::

           OAUTH tokens are refreshed when a 401 or 407 response is returned.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#cfn-events-connection-authorizationtype
        '''
        result = self._values.get("authorization_type")
        assert result is not None, "Required property 'authorization_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_parameters(
        self,
    ) -> typing.Union[CfnConnection.AuthParametersProperty, _IResolvable_a771d0ef]:
        '''A ``CreateConnectionAuthRequestParameters`` object that contains the authorization parameters to use to authorize with the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#cfn-events-connection-authparameters
        '''
        result = self._values.get("auth_parameters")
        assert result is not None, "Required property 'auth_parameters' is missing"
        return typing.cast(typing.Union[CfnConnection.AuthParametersProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the connection to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#cfn-events-connection-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the connection to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-connection.html#cfn-events-connection-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEndpoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.CfnEndpoint",
):
    '''A CloudFormation ``AWS::Events::Endpoint``.

    A global endpoint used to improve your application's availability by making it regional-fault tolerant. For more information about global endpoints, see `Making applications Regional-fault tolerant with global endpoints and event replication <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-global-endpoints.html>`_ in the *Amazon EventBridge User Guide* .

    :cloudformationResource: AWS::Events::Endpoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_events as events
        
        cfn_endpoint = events.CfnEndpoint(self, "MyCfnEndpoint",
            event_buses=[events.CfnEndpoint.EndpointEventBusProperty(
                event_bus_arn="eventBusArn"
            )],
            routing_config=events.CfnEndpoint.RoutingConfigProperty(
                failover_config=events.CfnEndpoint.FailoverConfigProperty(
                    primary=events.CfnEndpoint.PrimaryProperty(
                        health_check="healthCheck"
                    ),
                    secondary=events.CfnEndpoint.SecondaryProperty(
                        route="route"
                    )
                )
            ),
        
            # the properties below are optional
            description="description",
            name="name",
            replication_config=events.CfnEndpoint.ReplicationConfigProperty(
                state="state"
            ),
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        event_buses: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnEndpoint.EndpointEventBusProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        routing_config: typing.Union[typing.Union["CfnEndpoint.RoutingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        replication_config: typing.Optional[typing.Union[typing.Union["CfnEndpoint.ReplicationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Events::Endpoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param event_buses: The event buses being used by the endpoint. *Exactly* : ``2``
        :param routing_config: The routing configuration of the endpoint.
        :param description: A description for the endpoint.
        :param name: The name of the endpoint.
        :param replication_config: Whether event replication was enabled or disabled for this endpoint. The default state is ``ENABLED`` which means you must supply a ``RoleArn`` . If you don't have a ``RoleArn`` or you don't want event replication enabled, set the state to ``DISABLED`` .
        :param role_arn: The ARN of the role used by event replication for the endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25247b5b0c34991a5d15bf41a4b14ea46886300efd86cfac1b5b1484dfcd73bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEndpointProps(
            event_buses=event_buses,
            routing_config=routing_config,
            description=description,
            name=name,
            replication_config=replication_config,
            role_arn=role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c834be4845536a2a12e350d679a34a5386e192b1a5c4527184d0249411f229cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__984c0847c0d3080832af8164cfa5dd69efabb765ca14307ed69ef403c5c4b8c3)
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
        '''The ARN of the endpoint.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpointId")
    def attr_endpoint_id(self) -> builtins.str:
        '''The ID of the endpoint.

        :cloudformationAttribute: EndpointId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpointId"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpointUrl")
    def attr_endpoint_url(self) -> builtins.str:
        '''The URL of the endpoint.

        :cloudformationAttribute: EndpointUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The current state of the endpoint.

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrStateReason")
    def attr_state_reason(self) -> builtins.str:
        '''The reason the endpoint is in its current state.

        :cloudformationAttribute: StateReason
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStateReason"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="eventBuses")
    def event_buses(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEndpoint.EndpointEventBusProperty", _IResolvable_a771d0ef]]]:
        '''The event buses being used by the endpoint.

        *Exactly* : ``2``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-eventbuses
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEndpoint.EndpointEventBusProperty", _IResolvable_a771d0ef]]], jsii.get(self, "eventBuses"))

    @event_buses.setter
    def event_buses(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEndpoint.EndpointEventBusProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6758a5f9fd8d1dea211c67372558b9931e859df2e353d0af692cbc4cfd296644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBuses", value)

    @builtins.property
    @jsii.member(jsii_name="routingConfig")
    def routing_config(
        self,
    ) -> typing.Union["CfnEndpoint.RoutingConfigProperty", _IResolvable_a771d0ef]:
        '''The routing configuration of the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-routingconfig
        '''
        return typing.cast(typing.Union["CfnEndpoint.RoutingConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "routingConfig"))

    @routing_config.setter
    def routing_config(
        self,
        value: typing.Union["CfnEndpoint.RoutingConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9318307bcdd20c75c9e20de0eede533eec20f3a200d6895e78ef9a0916224f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingConfig", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b5180bcfa50607cc3258c9d9c01013f5d0cd419b749d147813d33405862e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e729931ec8ac2a40868b50093c046d47d4c33abd71aee7dd600e3f24983885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="replicationConfig")
    def replication_config(
        self,
    ) -> typing.Optional[typing.Union["CfnEndpoint.ReplicationConfigProperty", _IResolvable_a771d0ef]]:
        '''Whether event replication was enabled or disabled for this endpoint.

        The default state is ``ENABLED`` which means you must supply a ``RoleArn`` . If you don't have a ``RoleArn`` or you don't want event replication enabled, set the state to ``DISABLED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-replicationconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnEndpoint.ReplicationConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "replicationConfig"))

    @replication_config.setter
    def replication_config(
        self,
        value: typing.Optional[typing.Union["CfnEndpoint.ReplicationConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a79a4a5d4d1126e8bd137fc4c2be238a3743d490ec5be5d1e5c17dc67fdf4a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationConfig", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role used by event replication for the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa376f1e441f556b37db888437bebd8b3b93a96cd0ea85264a90989b31f34ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnEndpoint.EndpointEventBusProperty",
        jsii_struct_bases=[],
        name_mapping={"event_bus_arn": "eventBusArn"},
    )
    class EndpointEventBusProperty:
        def __init__(self, *, event_bus_arn: builtins.str) -> None:
            '''The event buses the endpoint is associated with.

            :param event_bus_arn: The ARN of the event bus the endpoint is associated with.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-endpointeventbus.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                endpoint_event_bus_property = events.CfnEndpoint.EndpointEventBusProperty(
                    event_bus_arn="eventBusArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f6133a78f467e67457dc52b31c7e035d5f4c333c85517656704e9ba0c2fec1b)
                check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "event_bus_arn": event_bus_arn,
            }

        @builtins.property
        def event_bus_arn(self) -> builtins.str:
            '''The ARN of the event bus the endpoint is associated with.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-endpointeventbus.html#cfn-events-endpoint-endpointeventbus-eventbusarn
            '''
            result = self._values.get("event_bus_arn")
            assert result is not None, "Required property 'event_bus_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointEventBusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnEndpoint.FailoverConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"primary": "primary", "secondary": "secondary"},
    )
    class FailoverConfigProperty:
        def __init__(
            self,
            *,
            primary: typing.Union[typing.Union["CfnEndpoint.PrimaryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            secondary: typing.Union[typing.Union["CfnEndpoint.SecondaryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''The failover configuration for an endpoint.

            This includes what triggers failover and what happens when it's triggered.

            :param primary: The main Region of the endpoint.
            :param secondary: The Region that events are routed to when failover is triggered or event replication is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-failoverconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                failover_config_property = events.CfnEndpoint.FailoverConfigProperty(
                    primary=events.CfnEndpoint.PrimaryProperty(
                        health_check="healthCheck"
                    ),
                    secondary=events.CfnEndpoint.SecondaryProperty(
                        route="route"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__860d62f1ccc30c6ee3e6d8611b864c1d3b67e403814bd89617c03d4a1a24dd54)
                check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
                check_type(argname="argument secondary", value=secondary, expected_type=type_hints["secondary"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "primary": primary,
                "secondary": secondary,
            }

        @builtins.property
        def primary(
            self,
        ) -> typing.Union["CfnEndpoint.PrimaryProperty", _IResolvable_a771d0ef]:
            '''The main Region of the endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-failoverconfig.html#cfn-events-endpoint-failoverconfig-primary
            '''
            result = self._values.get("primary")
            assert result is not None, "Required property 'primary' is missing"
            return typing.cast(typing.Union["CfnEndpoint.PrimaryProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def secondary(
            self,
        ) -> typing.Union["CfnEndpoint.SecondaryProperty", _IResolvable_a771d0ef]:
            '''The Region that events are routed to when failover is triggered or event replication is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-failoverconfig.html#cfn-events-endpoint-failoverconfig-secondary
            '''
            result = self._values.get("secondary")
            assert result is not None, "Required property 'secondary' is missing"
            return typing.cast(typing.Union["CfnEndpoint.SecondaryProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailoverConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnEndpoint.PrimaryProperty",
        jsii_struct_bases=[],
        name_mapping={"health_check": "healthCheck"},
    )
    class PrimaryProperty:
        def __init__(self, *, health_check: builtins.str) -> None:
            '''The primary Region of the endpoint.

            :param health_check: The ARN of the health check used by the endpoint to determine whether failover is triggered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-primary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                primary_property = events.CfnEndpoint.PrimaryProperty(
                    health_check="healthCheck"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6e1a13885d0575e65f6499dc625173a338e3f5de8df05d7377160ac71c9398b)
                check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "health_check": health_check,
            }

        @builtins.property
        def health_check(self) -> builtins.str:
            '''The ARN of the health check used by the endpoint to determine whether failover is triggered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-primary.html#cfn-events-endpoint-primary-healthcheck
            '''
            result = self._values.get("health_check")
            assert result is not None, "Required property 'health_check' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrimaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnEndpoint.ReplicationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"state": "state"},
    )
    class ReplicationConfigProperty:
        def __init__(self, *, state: builtins.str) -> None:
            '''Endpoints can replicate all events to the secondary Region.

            :param state: The state of event replication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-replicationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                replication_config_property = events.CfnEndpoint.ReplicationConfigProperty(
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__501d73f33c980dd89449674123020419efa8415e02f641b1011474405e2eb97f)
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "state": state,
            }

        @builtins.property
        def state(self) -> builtins.str:
            '''The state of event replication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-replicationconfig.html#cfn-events-endpoint-replicationconfig-state
            '''
            result = self._values.get("state")
            assert result is not None, "Required property 'state' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnEndpoint.RoutingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"failover_config": "failoverConfig"},
    )
    class RoutingConfigProperty:
        def __init__(
            self,
            *,
            failover_config: typing.Union[typing.Union["CfnEndpoint.FailoverConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''The routing configuration of the endpoint.

            :param failover_config: The failover configuration for an endpoint. This includes what triggers failover and what happens when it's triggered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-routingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                routing_config_property = events.CfnEndpoint.RoutingConfigProperty(
                    failover_config=events.CfnEndpoint.FailoverConfigProperty(
                        primary=events.CfnEndpoint.PrimaryProperty(
                            health_check="healthCheck"
                        ),
                        secondary=events.CfnEndpoint.SecondaryProperty(
                            route="route"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2063734ade08c209edda87381dd4d7142af24b8f15f93f2477fbc680a438d42e)
                check_type(argname="argument failover_config", value=failover_config, expected_type=type_hints["failover_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "failover_config": failover_config,
            }

        @builtins.property
        def failover_config(
            self,
        ) -> typing.Union["CfnEndpoint.FailoverConfigProperty", _IResolvable_a771d0ef]:
            '''The failover configuration for an endpoint.

            This includes what triggers failover and what happens when it's triggered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-routingconfig.html#cfn-events-endpoint-routingconfig-failoverconfig
            '''
            result = self._values.get("failover_config")
            assert result is not None, "Required property 'failover_config' is missing"
            return typing.cast(typing.Union["CfnEndpoint.FailoverConfigProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnEndpoint.SecondaryProperty",
        jsii_struct_bases=[],
        name_mapping={"route": "route"},
    )
    class SecondaryProperty:
        def __init__(self, *, route: builtins.str) -> None:
            '''The secondary Region that processes events when failover is triggered or replication is enabled.

            :param route: Defines the secondary Region.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-secondary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                secondary_property = events.CfnEndpoint.SecondaryProperty(
                    route="route"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3901c0a08df034770c93e503d11de451464eb6589892ff8a5d4ae500c502b0dd)
                check_type(argname="argument route", value=route, expected_type=type_hints["route"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "route": route,
            }

        @builtins.property
        def route(self) -> builtins.str:
            '''Defines the secondary Region.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-endpoint-secondary.html#cfn-events-endpoint-secondary-route
            '''
            result = self._values.get("route")
            assert result is not None, "Required property 'route' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecondaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_events.CfnEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_buses": "eventBuses",
        "routing_config": "routingConfig",
        "description": "description",
        "name": "name",
        "replication_config": "replicationConfig",
        "role_arn": "roleArn",
    },
)
class CfnEndpointProps:
    def __init__(
        self,
        *,
        event_buses: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEndpoint.EndpointEventBusProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        routing_config: typing.Union[typing.Union[CfnEndpoint.RoutingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        replication_config: typing.Optional[typing.Union[typing.Union[CfnEndpoint.ReplicationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEndpoint``.

        :param event_buses: The event buses being used by the endpoint. *Exactly* : ``2``
        :param routing_config: The routing configuration of the endpoint.
        :param description: A description for the endpoint.
        :param name: The name of the endpoint.
        :param replication_config: Whether event replication was enabled or disabled for this endpoint. The default state is ``ENABLED`` which means you must supply a ``RoleArn`` . If you don't have a ``RoleArn`` or you don't want event replication enabled, set the state to ``DISABLED`` .
        :param role_arn: The ARN of the role used by event replication for the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            cfn_endpoint_props = events.CfnEndpointProps(
                event_buses=[events.CfnEndpoint.EndpointEventBusProperty(
                    event_bus_arn="eventBusArn"
                )],
                routing_config=events.CfnEndpoint.RoutingConfigProperty(
                    failover_config=events.CfnEndpoint.FailoverConfigProperty(
                        primary=events.CfnEndpoint.PrimaryProperty(
                            health_check="healthCheck"
                        ),
                        secondary=events.CfnEndpoint.SecondaryProperty(
                            route="route"
                        )
                    )
                ),
            
                # the properties below are optional
                description="description",
                name="name",
                replication_config=events.CfnEndpoint.ReplicationConfigProperty(
                    state="state"
                ),
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0128f18d30a5ced22e4f832ac07b4d4f18fa36123d78a573689b7cff85a72b)
            check_type(argname="argument event_buses", value=event_buses, expected_type=type_hints["event_buses"])
            check_type(argname="argument routing_config", value=routing_config, expected_type=type_hints["routing_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replication_config", value=replication_config, expected_type=type_hints["replication_config"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_buses": event_buses,
            "routing_config": routing_config,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if replication_config is not None:
            self._values["replication_config"] = replication_config
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def event_buses(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEndpoint.EndpointEventBusProperty, _IResolvable_a771d0ef]]]:
        '''The event buses being used by the endpoint.

        *Exactly* : ``2``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-eventbuses
        '''
        result = self._values.get("event_buses")
        assert result is not None, "Required property 'event_buses' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEndpoint.EndpointEventBusProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def routing_config(
        self,
    ) -> typing.Union[CfnEndpoint.RoutingConfigProperty, _IResolvable_a771d0ef]:
        '''The routing configuration of the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-routingconfig
        '''
        result = self._values.get("routing_config")
        assert result is not None, "Required property 'routing_config' is missing"
        return typing.cast(typing.Union[CfnEndpoint.RoutingConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_config(
        self,
    ) -> typing.Optional[typing.Union[CfnEndpoint.ReplicationConfigProperty, _IResolvable_a771d0ef]]:
        '''Whether event replication was enabled or disabled for this endpoint.

        The default state is ``ENABLED`` which means you must supply a ``RoleArn`` . If you don't have a ``RoleArn`` or you don't want event replication enabled, set the state to ``DISABLED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-replicationconfig
        '''
        result = self._values.get("replication_config")
        return typing.cast(typing.Optional[typing.Union[CfnEndpoint.ReplicationConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role used by event replication for the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-endpoint.html#cfn-events-endpoint-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEventBus(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.CfnEventBus",
):
    '''A CloudFormation ``AWS::Events::EventBus``.

    Creates a new event bus within your account. This can be a custom event bus which you can use to receive events from your custom applications and services, or it can be a partner event bus which can be matched to a partner event source.

    :cloudformationResource: AWS::Events::EventBus
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_events as events
        
        cfn_event_bus = events.CfnEventBus(self, "MyCfnEventBus",
            name="name",
        
            # the properties below are optional
            event_source_name="eventSourceName",
            tags=[events.CfnEventBus.TagEntryProperty(
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
        event_source_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnEventBus.TagEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Events::EventBus``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the new event bus. Custom event bus names can't contain the ``/`` character, but you can use the ``/`` character in partner event bus names. In addition, for partner event buses, the name must exactly match the name of the partner event source that this event bus is matched to. You can't use the name ``default`` for a custom event bus, as this name is already used for your account's default event bus.
        :param event_source_name: If you are creating a partner event bus, this specifies the partner event source that the new event bus will be matched with.
        :param tags: Tags to associate with the event bus.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fcd473986abb3e1db7f382f367394b7ddc4f324470e9d739272a74f15ed688)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEventBusProps(
            name=name, event_source_name=event_source_name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a3557758ce7341a09ec455488601eb7c0175a4bc154af281fd0c3674444046)
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
            type_hints = typing.get_type_hints(_typecheckingstub__632606d4ca47e2e5c7a386510dfe7102321a1bb90b7151392fb3ebf6e58a654f)
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
        '''The ARN of the event bus, such as ``arn:aws:events:us-east-2:123456789012:event-bus/aws.partner/PartnerName/acct1/repo1`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the event bus, such as ``PartnerName/acct1/repo1`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrPolicy")
    def attr_policy(self) -> builtins.str:
        '''The policy for the event bus in JSON form.

        :cloudformationAttribute: Policy
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPolicy"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the new event bus.

        Custom event bus names can't contain the ``/`` character, but you can use the ``/`` character in partner event bus names. In addition, for partner event buses, the name must exactly match the name of the partner event source that this event bus is matched to.

        You can't use the name ``default`` for a custom event bus, as this name is already used for your account's default event bus.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a1f407f7fcca880863e3f642a7b27d94832bf8bad92709506ab0388836e64e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[builtins.str]:
        '''If you are creating a partner event bus, this specifies the partner event source that the new event bus will be matched with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceName"))

    @event_source_name.setter
    def event_source_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e823a500a06ee374ae9cf4c8cadf5386ab78ae2db71e902c77f4c9fd09fda3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSourceName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnEventBus.TagEntryProperty"]]:
        '''Tags to associate with the event bus.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-tags
        '''
        return typing.cast(typing.Optional[typing.List["CfnEventBus.TagEntryProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnEventBus.TagEntryProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df0d2dfb02c86e5f3a75616a9edc9eabe1afc148e5515a44007239397837196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnEventBus.TagEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''A key-value pair associated with an AWS resource.

            In EventBridge, rules and event buses support tagging.

            :param key: A string you can use to assign a value. The combination of tag keys and values can help you organize and categorize your resources.
            :param value: The value for the specified tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbus-tagentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                tag_entry_property = events.CfnEventBus.TagEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea1baf8cf81bde9b9a61d4c8be792b9c47ad9d8aacb6d58299e24f15b36a859e)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''A string you can use to assign a value.

            The combination of tag keys and values can help you organize and categorize your resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbus-tagentry.html#cfn-events-eventbus-tagentry-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value for the specified tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbus-tagentry.html#cfn-events-eventbus-tagentry-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnEventBusPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.CfnEventBusPolicy",
):
    '''A CloudFormation ``AWS::Events::EventBusPolicy``.

    Running ``PutPermission`` permits the specified AWS account or AWS organization to put events to the specified *event bus* . Amazon EventBridge (CloudWatch Events) rules in your account are triggered by these events arriving to an event bus in your account.

    For another account to send events to your account, that external account must have an EventBridge rule with your account's event bus as a target.

    To enable multiple AWS accounts to put events to your event bus, run ``PutPermission`` once for each of these accounts. Or, if all the accounts are members of the same AWS organization, you can run ``PutPermission`` once specifying ``Principal`` as "*" and specifying the AWS organization ID in ``Condition`` , to grant permissions to all accounts in that organization.

    If you grant permissions using an organization, then accounts in that organization must specify a ``RoleArn`` with proper permissions when they use ``PutTarget`` to add your account's event bus as a target. For more information, see `Sending and Receiving Events Between AWS Accounts <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html>`_ in the *Amazon EventBridge User Guide* .

    The permission policy on the event bus cannot exceed 10 KB in size.

    :cloudformationResource: AWS::Events::EventBusPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_events as events
        
        # statement: Any
        
        cfn_event_bus_policy = events.CfnEventBusPolicy(self, "MyCfnEventBusPolicy",
            statement_id="statementId",
        
            # the properties below are optional
            action="action",
            condition=events.CfnEventBusPolicy.ConditionProperty(
                key="key",
                type="type",
                value="value"
            ),
            event_bus_name="eventBusName",
            principal="principal",
            statement=statement
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        statement_id: builtins.str,
        action: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union[typing.Union["CfnEventBusPolicy.ConditionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
        principal: typing.Optional[builtins.str] = None,
        statement: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Events::EventBusPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param statement_id: An identifier string for the external account that you are granting permissions to. If you later want to revoke the permission for this external account, specify this ``StatementId`` when you run `RemovePermission <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_RemovePermission.html>`_ . .. epigraph:: Each ``StatementId`` must be unique.
        :param action: The action that you are enabling the other account to perform.
        :param condition: This parameter enables you to limit the permission to accounts that fulfill a certain condition, such as being a member of a certain AWS organization. For more information about AWS Organizations, see `What Is AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html>`_ in the *AWS Organizations User Guide* . If you specify ``Condition`` with an AWS organization ID, and specify "*" as the value for ``Principal`` , you grant permission to all the accounts in the named organization. The ``Condition`` is a JSON string which must contain ``Type`` , ``Key`` , and ``Value`` fields.
        :param event_bus_name: The name of the event bus associated with the rule. If you omit this, the default event bus is used.
        :param principal: The 12-digit AWS account ID that you are permitting to put events to your default event bus. Specify "*" to permit any account to put events to your default event bus. If you specify "*" without specifying ``Condition`` , avoid creating rules that may match undesirable events. To create more secure rules, make sure that the event pattern for each rule contains an ``account`` field with a specific account ID from which to receive events. Rules with an account field do not match any events sent from other accounts.
        :param statement: A JSON string that describes the permission policy statement. You can include a ``Policy`` parameter in the request instead of using the ``StatementId`` , ``Action`` , ``Principal`` , or ``Condition`` parameters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d864fff0969fce2aa0f79099ed45f692ae632ae6a7897dbc850a5d200ffddc90)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEventBusPolicyProps(
            statement_id=statement_id,
            action=action,
            condition=condition,
            event_bus_name=event_bus_name,
            principal=principal,
            statement=statement,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe8a5a2f8210b1622713ca2e5980f3df4adfb201a8e0633cbb32df59637c69e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d98cf37eaac5b0a4a4291f47ba01f5559df2c89e4aa3389e105da5667f215f6)
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
    @jsii.member(jsii_name="statement")
    def statement(self) -> typing.Any:
        '''A JSON string that describes the permission policy statement.

        You can include a ``Policy`` parameter in the request instead of using the ``StatementId`` , ``Action`` , ``Principal`` , or ``Condition`` parameters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statement
        '''
        return typing.cast(typing.Any, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ff5a1c5f4d4a725e2af72d9c2e70ad404502db8cfa94f58f4190d938b8ac86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value)

    @builtins.property
    @jsii.member(jsii_name="statementId")
    def statement_id(self) -> builtins.str:
        '''An identifier string for the external account that you are granting permissions to.

        If you later want to revoke the permission for this external account, specify this ``StatementId`` when you run `RemovePermission <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_RemovePermission.html>`_ .
        .. epigraph::

           Each ``StatementId`` must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statementid
        '''
        return typing.cast(builtins.str, jsii.get(self, "statementId"))

    @statement_id.setter
    def statement_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71dd1e50b6c396dcfe0cbf19fa3a5ee1ce02671f91cbd354a87a1f607f1de4dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementId", value)

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> typing.Optional[builtins.str]:
        '''The action that you are enabling the other account to perform.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-action
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "action"))

    @action.setter
    def action(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ffde2a1d53991016631d644ebf2613901d3122723d4cd6c6610ec0a47a17353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> typing.Optional[typing.Union["CfnEventBusPolicy.ConditionProperty", _IResolvable_a771d0ef]]:
        '''This parameter enables you to limit the permission to accounts that fulfill a certain condition, such as being a member of a certain AWS organization.

        For more information about AWS Organizations, see `What Is AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html>`_ in the *AWS Organizations User Guide* .

        If you specify ``Condition`` with an AWS organization ID, and specify "*" as the value for ``Principal`` , you grant permission to all the accounts in the named organization.

        The ``Condition`` is a JSON string which must contain ``Type`` , ``Key`` , and ``Value`` fields.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-condition
        '''
        return typing.cast(typing.Optional[typing.Union["CfnEventBusPolicy.ConditionProperty", _IResolvable_a771d0ef]], jsii.get(self, "condition"))

    @condition.setter
    def condition(
        self,
        value: typing.Optional[typing.Union["CfnEventBusPolicy.ConditionProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ebea21cce261aca4cce13c9a0d391553da4f94be0436893bf41a65fcaa6f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value)

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        '''The name of the event bus associated with the rule.

        If you omit this, the default event bus is used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-eventbusname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventBusName"))

    @event_bus_name.setter
    def event_bus_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acddce35f648a5abeca4154a153a66c0f11f9973b57b792a8352fff0e40d474e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBusName", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> typing.Optional[builtins.str]:
        '''The 12-digit AWS account ID that you are permitting to put events to your default event bus.

        Specify "*" to permit any account to put events to your default event bus.

        If you specify "*" without specifying ``Condition`` , avoid creating rules that may match undesirable events. To create more secure rules, make sure that the event pattern for each rule contains an ``account`` field with a specific account ID from which to receive events. Rules with an account field do not match any events sent from other accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-principal
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d71d46e4c7070d6c93fe58a40562ab1359f0b903e8512e1723908467697a6588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnEventBusPolicy.ConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type", "value": "value"},
    )
    class ConditionProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A JSON string which you can use to limit the event bus permissions you are granting to only accounts that fulfill the condition.

            Currently, the only supported condition is membership in a certain AWS organization. The string must contain ``Type`` , ``Key`` , and ``Value`` fields. The ``Value`` field specifies the ID of the AWS organization. Following is an example value for ``Condition`` :

            ``'{"Type" : "StringEquals", "Key": "aws:PrincipalOrgID", "Value": "o-1234567890"}'``

            :param key: Specifies the key for the condition. Currently the only supported key is ``aws:PrincipalOrgID`` .
            :param type: Specifies the type of condition. Currently the only supported value is ``StringEquals`` .
            :param value: Specifies the value for the key. Currently, this must be the ID of the organization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                condition_property = events.CfnEventBusPolicy.ConditionProperty(
                    key="key",
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6178299fd7a930cb3e908627d7403297c4383491cc37bb8ec4137508df573f73)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''Specifies the key for the condition.

            Currently the only supported key is ``aws:PrincipalOrgID`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of condition.

            Currently the only supported value is ``StringEquals`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Specifies the value for the key.

            Currently, this must be the ID of the organization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_events.CfnEventBusPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "statement_id": "statementId",
        "action": "action",
        "condition": "condition",
        "event_bus_name": "eventBusName",
        "principal": "principal",
        "statement": "statement",
    },
)
class CfnEventBusPolicyProps:
    def __init__(
        self,
        *,
        statement_id: builtins.str,
        action: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union[typing.Union[CfnEventBusPolicy.ConditionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
        principal: typing.Optional[builtins.str] = None,
        statement: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnEventBusPolicy``.

        :param statement_id: An identifier string for the external account that you are granting permissions to. If you later want to revoke the permission for this external account, specify this ``StatementId`` when you run `RemovePermission <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_RemovePermission.html>`_ . .. epigraph:: Each ``StatementId`` must be unique.
        :param action: The action that you are enabling the other account to perform.
        :param condition: This parameter enables you to limit the permission to accounts that fulfill a certain condition, such as being a member of a certain AWS organization. For more information about AWS Organizations, see `What Is AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html>`_ in the *AWS Organizations User Guide* . If you specify ``Condition`` with an AWS organization ID, and specify "*" as the value for ``Principal`` , you grant permission to all the accounts in the named organization. The ``Condition`` is a JSON string which must contain ``Type`` , ``Key`` , and ``Value`` fields.
        :param event_bus_name: The name of the event bus associated with the rule. If you omit this, the default event bus is used.
        :param principal: The 12-digit AWS account ID that you are permitting to put events to your default event bus. Specify "*" to permit any account to put events to your default event bus. If you specify "*" without specifying ``Condition`` , avoid creating rules that may match undesirable events. To create more secure rules, make sure that the event pattern for each rule contains an ``account`` field with a specific account ID from which to receive events. Rules with an account field do not match any events sent from other accounts.
        :param statement: A JSON string that describes the permission policy statement. You can include a ``Policy`` parameter in the request instead of using the ``StatementId`` , ``Action`` , ``Principal`` , or ``Condition`` parameters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            # statement: Any
            
            cfn_event_bus_policy_props = events.CfnEventBusPolicyProps(
                statement_id="statementId",
            
                # the properties below are optional
                action="action",
                condition=events.CfnEventBusPolicy.ConditionProperty(
                    key="key",
                    type="type",
                    value="value"
                ),
                event_bus_name="eventBusName",
                principal="principal",
                statement=statement
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca36960c34281fb096d25b28e623361e11cf6d6d268b022c613089919587b24)
            check_type(argname="argument statement_id", value=statement_id, expected_type=type_hints["statement_id"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "statement_id": statement_id,
        }
        if action is not None:
            self._values["action"] = action
        if condition is not None:
            self._values["condition"] = condition
        if event_bus_name is not None:
            self._values["event_bus_name"] = event_bus_name
        if principal is not None:
            self._values["principal"] = principal
        if statement is not None:
            self._values["statement"] = statement

    @builtins.property
    def statement_id(self) -> builtins.str:
        '''An identifier string for the external account that you are granting permissions to.

        If you later want to revoke the permission for this external account, specify this ``StatementId`` when you run `RemovePermission <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_RemovePermission.html>`_ .
        .. epigraph::

           Each ``StatementId`` must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statementid
        '''
        result = self._values.get("statement_id")
        assert result is not None, "Required property 'statement_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action that you are enabling the other account to perform.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[typing.Union[CfnEventBusPolicy.ConditionProperty, _IResolvable_a771d0ef]]:
        '''This parameter enables you to limit the permission to accounts that fulfill a certain condition, such as being a member of a certain AWS organization.

        For more information about AWS Organizations, see `What Is AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html>`_ in the *AWS Organizations User Guide* .

        If you specify ``Condition`` with an AWS organization ID, and specify "*" as the value for ``Principal`` , you grant permission to all the accounts in the named organization.

        The ``Condition`` is a JSON string which must contain ``Type`` , ``Key`` , and ``Value`` fields.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-condition
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[typing.Union[CfnEventBusPolicy.ConditionProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        '''The name of the event bus associated with the rule.

        If you omit this, the default event bus is used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-eventbusname
        '''
        result = self._values.get("event_bus_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal(self) -> typing.Optional[builtins.str]:
        '''The 12-digit AWS account ID that you are permitting to put events to your default event bus.

        Specify "*" to permit any account to put events to your default event bus.

        If you specify "*" without specifying ``Condition`` , avoid creating rules that may match undesirable events. To create more secure rules, make sure that the event pattern for each rule contains an ``account`` field with a specific account ID from which to receive events. Rules with an account field do not match any events sent from other accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement(self) -> typing.Any:
        '''A JSON string that describes the permission policy statement.

        You can include a ``Policy`` parameter in the request instead of using the ``StatementId`` , ``Action`` , ``Principal`` , or ``Condition`` parameters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statement
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventBusPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events.CfnEventBusProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "event_source_name": "eventSourceName",
        "tags": "tags",
    },
)
class CfnEventBusProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        event_source_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnEventBus.TagEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEventBus``.

        :param name: The name of the new event bus. Custom event bus names can't contain the ``/`` character, but you can use the ``/`` character in partner event bus names. In addition, for partner event buses, the name must exactly match the name of the partner event source that this event bus is matched to. You can't use the name ``default`` for a custom event bus, as this name is already used for your account's default event bus.
        :param event_source_name: If you are creating a partner event bus, this specifies the partner event source that the new event bus will be matched with.
        :param tags: Tags to associate with the event bus.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            cfn_event_bus_props = events.CfnEventBusProps(
                name="name",
            
                # the properties below are optional
                event_source_name="eventSourceName",
                tags=[events.CfnEventBus.TagEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd4e2bd712e858d7d5045dddfc2997d7ab569ad18e349aeea1200c2a1b26f06)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument event_source_name", value=event_source_name, expected_type=type_hints["event_source_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if event_source_name is not None:
            self._values["event_source_name"] = event_source_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the new event bus.

        Custom event bus names can't contain the ``/`` character, but you can use the ``/`` character in partner event bus names. In addition, for partner event buses, the name must exactly match the name of the partner event source that this event bus is matched to.

        You can't use the name ``default`` for a custom event bus, as this name is already used for your account's default event bus.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_source_name(self) -> typing.Optional[builtins.str]:
        '''If you are creating a partner event bus, this specifies the partner event source that the new event bus will be matched with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        '''
        result = self._values.get("event_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnEventBus.TagEntryProperty]]:
        '''Tags to associate with the event bus.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnEventBus.TagEntryProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventBusProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.CfnRule",
):
    '''A CloudFormation ``AWS::Events::Rule``.

    Creates or updates the specified rule. Rules are enabled by default, or based on value of the state. You can disable a rule using `DisableRule <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_DisableRule.html>`_ .

    A single rule watches for events from a single event bus. Events generated by AWS services go to your account's default event bus. Events generated by SaaS partner services or applications go to the matching partner event bus. If you have custom applications or services, you can specify whether their events go to your default event bus or a custom event bus that you have created. For more information, see `CreateEventBus <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_CreateEventBus.html>`_ .

    If you are updating an existing rule, the rule is replaced with what you specify in this ``PutRule`` command. If you omit arguments in ``PutRule`` , the old values for those arguments are not kept. Instead, they are replaced with null values.

    When you create or update a rule, incoming events might not immediately start matching to new or updated rules. Allow a short period of time for changes to take effect.

    A rule must contain at least an EventPattern or ScheduleExpression. Rules with EventPatterns are triggered when a matching event is observed. Rules with ScheduleExpressions self-trigger based on the given schedule. A rule can have both an EventPattern and a ScheduleExpression, in which case the rule triggers on matching events as well as on a schedule.

    Most services in AWS treat : or / as the same character in Amazon Resource Names (ARNs). However, EventBridge uses an exact match in event patterns and rules. Be sure to use the correct ARN characters when creating event patterns so that they match the ARN syntax in the event you want to match.

    In EventBridge, it is possible to create rules that lead to infinite loops, where a rule is fired repeatedly. For example, a rule might detect that ACLs have changed on an S3 bucket, and trigger software to change them to the desired state. If the rule is not written carefully, the subsequent change to the ACLs fires the rule again, creating an infinite loop.

    To prevent this, write the rules so that the triggered actions do not re-fire the same rule. For example, your rule could fire only if ACLs are found to be in a bad state, instead of after any change.

    An infinite loop can quickly cause higher than expected charges. We recommend that you use budgeting, which alerts you when charges exceed your specified limit. For more information, see `Managing Your Costs with Budgets <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/budgets-managing-costs.html>`_ .

    :cloudformationResource: AWS::Events::Rule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_events as events
        
        # event_pattern: Any
        
        cfn_rule = events.CfnRule(self, "MyCfnRule",
            description="description",
            event_bus_name="eventBusName",
            event_pattern=event_pattern,
            name="name",
            role_arn="roleArn",
            schedule_expression="scheduleExpression",
            state="state",
            targets=[events.CfnRule.TargetProperty(
                arn="arn",
                id="id",
        
                # the properties below are optional
                batch_parameters=events.CfnRule.BatchParametersProperty(
                    job_definition="jobDefinition",
                    job_name="jobName",
        
                    # the properties below are optional
                    array_properties=events.CfnRule.BatchArrayPropertiesProperty(
                        size=123
                    ),
                    retry_strategy=events.CfnRule.BatchRetryStrategyProperty(
                        attempts=123
                    )
                ),
                dead_letter_config=events.CfnRule.DeadLetterConfigProperty(
                    arn="arn"
                ),
                ecs_parameters=events.CfnRule.EcsParametersProperty(
                    task_definition_arn="taskDefinitionArn",
        
                    # the properties below are optional
                    capacity_provider_strategy=[events.CfnRule.CapacityProviderStrategyItemProperty(
                        capacity_provider="capacityProvider",
        
                        # the properties below are optional
                        base=123,
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=events.CfnRule.NetworkConfigurationProperty(
                        aws_vpc_configuration=events.CfnRule.AwsVpcConfigurationProperty(
                            subnets=["subnets"],
        
                            # the properties below are optional
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"]
                        )
                    ),
                    placement_constraints=[events.CfnRule.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategies=[events.CfnRule.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tag_list=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    task_count=123
                ),
                http_parameters=events.CfnRule.HttpParametersProperty(
                    header_parameters={
                        "header_parameters_key": "headerParameters"
                    },
                    path_parameter_values=["pathParameterValues"],
                    query_string_parameters={
                        "query_string_parameters_key": "queryStringParameters"
                    }
                ),
                input="input",
                input_path="inputPath",
                input_transformer=events.CfnRule.InputTransformerProperty(
                    input_template="inputTemplate",
        
                    # the properties below are optional
                    input_paths_map={
                        "input_paths_map_key": "inputPathsMap"
                    }
                ),
                kinesis_parameters=events.CfnRule.KinesisParametersProperty(
                    partition_key_path="partitionKeyPath"
                ),
                redshift_data_parameters=events.CfnRule.RedshiftDataParametersProperty(
                    database="database",
                    sql="sql",
        
                    # the properties below are optional
                    db_user="dbUser",
                    secret_manager_arn="secretManagerArn",
                    statement_name="statementName",
                    with_event=False
                ),
                retry_policy=events.CfnRule.RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                role_arn="roleArn",
                run_command_parameters=events.CfnRule.RunCommandParametersProperty(
                    run_command_targets=[events.CfnRule.RunCommandTargetProperty(
                        key="key",
                        values=["values"]
                    )]
                ),
                sage_maker_pipeline_parameters=events.CfnRule.SageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[events.CfnRule.SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                ),
                sqs_parameters=events.CfnRule.SqsParametersProperty(
                    message_group_id="messageGroupId"
                )
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
        event_pattern: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.TargetProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Events::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: The description of the rule.
        :param event_bus_name: The name or ARN of the event bus associated with the rule. If you omit this, the default event bus is used.
        :param event_pattern: The event pattern of the rule. For more information, see `Events and Event Patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html>`_ in the *Amazon EventBridge User Guide* .
        :param name: The name of the rule.
        :param role_arn: The Amazon Resource Name (ARN) of the role that is used for target invocation. If you're setting an event bus in another account as the target and that account granted permission to your account through an organization instead of directly by the account ID, you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure, instead of here in this parameter.
        :param schedule_expression: The scheduling expression. For example, "cron(0 20 * * ? *)", "rate(5 minutes)". For more information, see `Creating an Amazon EventBridge rule that runs on a schedule <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html>`_ .
        :param state: The state of the rule.
        :param targets: Adds the specified targets to the specified rule, or updates the targets if they are already associated with the rule. Targets are the resources that are invoked when a rule is triggered. The maximum number of entries per request is 10. .. epigraph:: Each rule can have up to five (5) targets associated with it at one time. For a list of services you can configure as targets for events, see `EventBridge targets <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html>`_ in the *Amazon EventBridge User Guide* . Creating rules with built-in targets is supported only in the AWS Management Console . The built-in targets are: - ``Amazon EBS CreateSnapshot API call`` - ``Amazon EC2 RebootInstances API call`` - ``Amazon EC2 StopInstances API call`` - ``Amazon EC2 TerminateInstances API call`` For some target types, ``PutTargets`` provides target-specific parameters. If the target is a Kinesis data stream, you can optionally specify which shard the event goes to by using the ``KinesisParameters`` argument. To invoke a command on multiple EC2 instances with one rule, you can use the ``RunCommandParameters`` field. To be able to make API calls against the resources that you own, Amazon EventBridge needs the appropriate permissions: - For AWS Lambda and Amazon SNS resources, EventBridge relies on resource-based policies. - For EC2 instances, Kinesis Data Streams, AWS Step Functions state machines and API Gateway APIs, EventBridge relies on IAM roles that you specify in the ``RoleARN`` argument in ``PutTargets`` . For more information, see `Authentication and Access Control <https://docs.aws.amazon.com/eventbridge/latest/userguide/auth-and-access-control-eventbridge.html>`_ in the *Amazon EventBridge User Guide* . If another AWS account is in the same region and has granted you permission (using ``PutPermission`` ), you can send events to that account. Set that account's event bus as a target of the rules in your account. To send the matched events to the other account, specify that account's event bus as the ``Arn`` value when you run ``PutTargets`` . If your account sends events to another account, your account is charged for each sent event. Each event sent to another account is charged as a custom event. The account receiving the event is not charged. For more information, see `Amazon EventBridge Pricing <https://docs.aws.amazon.com/eventbridge/pricing/>`_ . .. epigraph:: ``Input`` , ``InputPath`` , and ``InputTransformer`` are not available with ``PutTarget`` if the target is an event bus of a different AWS account. If you are setting the event bus of another account as the target, and that account granted permission to your account through an organization instead of directly by the account ID, then you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure. For more information, see `Sending and Receiving Events Between AWS Accounts <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html>`_ in the *Amazon EventBridge User Guide* . .. epigraph:: If you have an IAM role on a cross-account event bus target, a ``PutTargets`` call without a role on the same target (same ``Id`` and ``Arn`` ) will not remove the role. For more information about enabling cross-account events, see `PutPermission <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutPermission.html>`_ . *Input* , *InputPath* , and *InputTransformer* are mutually exclusive and optional parameters of a target. When a rule is triggered due to a matched event: - If none of the following arguments are specified for a target, then the entire event is passed to the target in JSON format (unless the target is Amazon EC2 Run Command or Amazon ECS task, in which case nothing from the event is passed to the target). - If *Input* is specified in the form of valid JSON, then the matched event is overridden with this constant. - If *InputPath* is specified in the form of JSONPath (for example, ``$.detail`` ), then only the part of the event specified in the path is passed to the target (for example, only the detail part of the event is passed). - If *InputTransformer* is specified, then one or more specified JSONPaths are extracted from the event and used as values in a template that you specify as the input to the target. When you specify ``InputPath`` or ``InputTransformer`` , you must use JSON dot notation, not bracket notation. When you add targets to a rule and the associated rule triggers soon after, new or updated targets might not be immediately invoked. Allow a short period of time for changes to take effect. This action can partially fail if too many requests are made at the same time. If that happens, ``FailedEntryCount`` is non-zero in the response and each entry in ``FailedEntries`` provides the ID of the failed target and the error code.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804ff16a8c2e9d52959f74e98242c891bca4d19b95d5a9b4fa4c684cce53c4bf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleProps(
            description=description,
            event_bus_name=event_bus_name,
            event_pattern=event_pattern,
            name=name,
            role_arn=role_arn,
            schedule_expression=schedule_expression,
            state=state,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f32e3d8bbf036b0c7c420013747c578efd226071acedc6d1f8a7d448bb76d58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c4c931c99ee79da0f5e1c2fe839cb1d1fb38dc2504287a989d713dc1bc1c41d)
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
        '''The ARN of the rule, such as ``arn:aws:events:us-east-2:123456789012:rule/example`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="eventPattern")
    def event_pattern(self) -> typing.Any:
        '''The event pattern of the rule.

        For more information, see `Events and Event Patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html>`_ in the *Amazon EventBridge User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventpattern
        '''
        return typing.cast(typing.Any, jsii.get(self, "eventPattern"))

    @event_pattern.setter
    def event_pattern(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4794fafa8a1aa77d92edcb41a01a0899dd2423c6a18ffbe9581fdcfe744e324b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventPattern", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a947957a93a0951d6597ed29b749eb37cee8d4894acf1065f33f2f933b312eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        '''The name or ARN of the event bus associated with the rule.

        If you omit this, the default event bus is used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventbusname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventBusName"))

    @event_bus_name.setter
    def event_bus_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f427759e09dd4e00ef1e08a727ecec4333af424ca7b33966972581e650b2f4f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBusName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320d06d1bfe5224905da51d5af3610c49dff87aad0ebc334d350370ae3692929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the role that is used for target invocation.

        If you're setting an event bus in another account as the target and that account granted permission to your account through an organization instead of directly by the account ID, you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure, instead of here in this parameter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0215d2db665069944dc033f0acf5fa49beda705d5d2f0a8e4835e7fd0b92bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="scheduleExpression")
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        '''The scheduling expression.

        For example, "cron(0 20 * * ? *)", "rate(5 minutes)". For more information, see `Creating an Amazon EventBridge rule that runs on a schedule <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-scheduleexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleExpression"))

    @schedule_expression.setter
    def schedule_expression(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91af7c731fa4589c5f5e3142db9e6c98ed9d3dab523c6a714fed5c8a0e567e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleExpression", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03c4050b40187f3e685cbc69a7e06ffc5e2aa537ecf8a7cde22fb6e7fdf05e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.TargetProperty", _IResolvable_a771d0ef]]]]:
        '''Adds the specified targets to the specified rule, or updates the targets if they are already associated with the rule.

        Targets are the resources that are invoked when a rule is triggered.

        The maximum number of entries per request is 10.
        .. epigraph::

           Each rule can have up to five (5) targets associated with it at one time.

        For a list of services you can configure as targets for events, see `EventBridge targets <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html>`_ in the *Amazon EventBridge User Guide* .

        Creating rules with built-in targets is supported only in the AWS Management Console . The built-in targets are:

        - ``Amazon EBS CreateSnapshot API call``
        - ``Amazon EC2 RebootInstances API call``
        - ``Amazon EC2 StopInstances API call``
        - ``Amazon EC2 TerminateInstances API call``

        For some target types, ``PutTargets`` provides target-specific parameters. If the target is a Kinesis data stream, you can optionally specify which shard the event goes to by using the ``KinesisParameters`` argument. To invoke a command on multiple EC2 instances with one rule, you can use the ``RunCommandParameters`` field.

        To be able to make API calls against the resources that you own, Amazon EventBridge needs the appropriate permissions:

        - For AWS Lambda and Amazon SNS resources, EventBridge relies on resource-based policies.
        - For EC2 instances, Kinesis Data Streams, AWS Step Functions state machines and API Gateway APIs, EventBridge relies on IAM roles that you specify in the ``RoleARN`` argument in ``PutTargets`` .

        For more information, see `Authentication and Access Control <https://docs.aws.amazon.com/eventbridge/latest/userguide/auth-and-access-control-eventbridge.html>`_ in the *Amazon EventBridge User Guide* .

        If another AWS account is in the same region and has granted you permission (using ``PutPermission`` ), you can send events to that account. Set that account's event bus as a target of the rules in your account. To send the matched events to the other account, specify that account's event bus as the ``Arn`` value when you run ``PutTargets`` . If your account sends events to another account, your account is charged for each sent event. Each event sent to another account is charged as a custom event. The account receiving the event is not charged. For more information, see `Amazon EventBridge Pricing <https://docs.aws.amazon.com/eventbridge/pricing/>`_ .
        .. epigraph::

           ``Input`` , ``InputPath`` , and ``InputTransformer`` are not available with ``PutTarget`` if the target is an event bus of a different AWS account.

        If you are setting the event bus of another account as the target, and that account granted permission to your account through an organization instead of directly by the account ID, then you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure. For more information, see `Sending and Receiving Events Between AWS Accounts <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html>`_ in the *Amazon EventBridge User Guide* .
        .. epigraph::

           If you have an IAM role on a cross-account event bus target, a ``PutTargets`` call without a role on the same target (same ``Id`` and ``Arn`` ) will not remove the role.

        For more information about enabling cross-account events, see `PutPermission <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutPermission.html>`_ .

        *Input* , *InputPath* , and *InputTransformer* are mutually exclusive and optional parameters of a target. When a rule is triggered due to a matched event:

        - If none of the following arguments are specified for a target, then the entire event is passed to the target in JSON format (unless the target is Amazon EC2 Run Command or Amazon ECS task, in which case nothing from the event is passed to the target).
        - If *Input* is specified in the form of valid JSON, then the matched event is overridden with this constant.
        - If *InputPath* is specified in the form of JSONPath (for example, ``$.detail`` ), then only the part of the event specified in the path is passed to the target (for example, only the detail part of the event is passed).
        - If *InputTransformer* is specified, then one or more specified JSONPaths are extracted from the event and used as values in a template that you specify as the input to the target.

        When you specify ``InputPath`` or ``InputTransformer`` , you must use JSON dot notation, not bracket notation.

        When you add targets to a rule and the associated rule triggers soon after, new or updated targets might not be immediately invoked. Allow a short period of time for changes to take effect.

        This action can partially fail if too many requests are made at the same time. If that happens, ``FailedEntryCount`` is non-zero in the response and each entry in ``FailedEntries`` provides the ID of the failed target and the error code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-targets
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.TargetProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "targets"))

    @targets.setter
    def targets(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.TargetProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dded918ff607b4b070ccc5e912f7dce582132f50b25c2259507834523826d2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targets", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.AwsVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subnets": "subnets",
            "assign_public_ip": "assignPublicIp",
            "security_groups": "securityGroups",
        },
    )
    class AwsVpcConfigurationProperty:
        def __init__(
            self,
            *,
            subnets: typing.Sequence[builtins.str],
            assign_public_ip: typing.Optional[builtins.str] = None,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure specifies the VPC subnets and security groups for the task, and whether a public IP address is to be used.

            This structure is relevant only for ECS tasks that use the ``awsvpc`` network mode.

            :param subnets: Specifies the subnets associated with the task. These subnets must all be in the same VPC. You can specify as many as 16 subnets.
            :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. You can specify ``ENABLED`` only when ``LaunchType`` in ``EcsParameters`` is set to ``FARGATE`` .
            :param security_groups: Specifies the security groups associated with the task. These security groups must all be in the same VPC. You can specify as many as five security groups. If you do not specify a security group, the default security group for the VPC is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                aws_vpc_configuration_property = events.CfnRule.AwsVpcConfigurationProperty(
                    subnets=["subnets"],
                
                    # the properties below are optional
                    assign_public_ip="assignPublicIp",
                    security_groups=["securityGroups"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa01ed22d9d20c5a73b73f89b398a70d1e187324fd9cced5856efc83a908528c)
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
                check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "subnets": subnets,
            }
            if assign_public_ip is not None:
                self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None:
                self._values["security_groups"] = security_groups

        @builtins.property
        def subnets(self) -> typing.List[builtins.str]:
            '''Specifies the subnets associated with the task.

            These subnets must all be in the same VPC. You can specify as many as 16 subnets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-subnets
            '''
            result = self._values.get("subnets")
            assert result is not None, "Required property 'subnets' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the task's elastic network interface receives a public IP address.

            You can specify ``ENABLED`` only when ``LaunchType`` in ``EcsParameters`` is set to ``FARGATE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-assignpublicip
            '''
            result = self._values.get("assign_public_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the security groups associated with the task.

            These security groups must all be in the same VPC. You can specify as many as five security groups. If you do not specify a security group, the default security group for the VPC is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.BatchArrayPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"size": "size"},
    )
    class BatchArrayPropertiesProperty:
        def __init__(self, *, size: typing.Optional[jsii.Number] = None) -> None:
            '''The array properties for the submitted job, such as the size of the array.

            The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. This parameter is used only if the target is an AWS Batch job.

            :param size: The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batcharrayproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                batch_array_properties_property = events.CfnRule.BatchArrayPropertiesProperty(
                    size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__091d4abe35c7b94428ed52b265691515c9a75fa46d71796ef3f885692a6ff6b2)
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size is not None:
                self._values["size"] = size

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The size of the array, if this is an array batch job.

            Valid values are integers between 2 and 10,000.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batcharrayproperties.html#cfn-events-rule-batcharrayproperties-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchArrayPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.BatchParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "job_definition": "jobDefinition",
            "job_name": "jobName",
            "array_properties": "arrayProperties",
            "retry_strategy": "retryStrategy",
        },
    )
    class BatchParametersProperty:
        def __init__(
            self,
            *,
            job_definition: builtins.str,
            job_name: builtins.str,
            array_properties: typing.Optional[typing.Union[typing.Union["CfnRule.BatchArrayPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            retry_strategy: typing.Optional[typing.Union[typing.Union["CfnRule.BatchRetryStrategyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The custom parameters to be used when the target is an AWS Batch job.

            :param job_definition: The ARN or name of the job definition to use if the event target is an AWS Batch job. This job definition must already exist.
            :param job_name: The name to use for this execution of the job, if the target is an AWS Batch job.
            :param array_properties: The array properties for the submitted job, such as the size of the array. The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. This parameter is used only if the target is an AWS Batch job.
            :param retry_strategy: The retry strategy to use for failed jobs, if the target is an AWS Batch job. The retry strategy is the number of times to retry the failed job execution. Valid values are 1–10. When you specify a retry strategy here, it overrides the retry strategy defined in the job definition.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                batch_parameters_property = events.CfnRule.BatchParametersProperty(
                    job_definition="jobDefinition",
                    job_name="jobName",
                
                    # the properties below are optional
                    array_properties=events.CfnRule.BatchArrayPropertiesProperty(
                        size=123
                    ),
                    retry_strategy=events.CfnRule.BatchRetryStrategyProperty(
                        attempts=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e7018bf93b8179d50a84ff19b2943d7bbed031466cf4ba9d4ab2d89bf414d4b)
                check_type(argname="argument job_definition", value=job_definition, expected_type=type_hints["job_definition"])
                check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                check_type(argname="argument array_properties", value=array_properties, expected_type=type_hints["array_properties"])
                check_type(argname="argument retry_strategy", value=retry_strategy, expected_type=type_hints["retry_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "job_definition": job_definition,
                "job_name": job_name,
            }
            if array_properties is not None:
                self._values["array_properties"] = array_properties
            if retry_strategy is not None:
                self._values["retry_strategy"] = retry_strategy

        @builtins.property
        def job_definition(self) -> builtins.str:
            '''The ARN or name of the job definition to use if the event target is an AWS Batch job.

            This job definition must already exist.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-jobdefinition
            '''
            result = self._values.get("job_definition")
            assert result is not None, "Required property 'job_definition' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def job_name(self) -> builtins.str:
            '''The name to use for this execution of the job, if the target is an AWS Batch job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-jobname
            '''
            result = self._values.get("job_name")
            assert result is not None, "Required property 'job_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def array_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.BatchArrayPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The array properties for the submitted job, such as the size of the array.

            The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. This parameter is used only if the target is an AWS Batch job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-arrayproperties
            '''
            result = self._values.get("array_properties")
            return typing.cast(typing.Optional[typing.Union["CfnRule.BatchArrayPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def retry_strategy(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.BatchRetryStrategyProperty", _IResolvable_a771d0ef]]:
            '''The retry strategy to use for failed jobs, if the target is an AWS Batch job.

            The retry strategy is the number of times to retry the failed job execution. Valid values are 1–10. When you specify a retry strategy here, it overrides the retry strategy defined in the job definition.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-retrystrategy
            '''
            result = self._values.get("retry_strategy")
            return typing.cast(typing.Optional[typing.Union["CfnRule.BatchRetryStrategyProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.BatchRetryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"attempts": "attempts"},
    )
    class BatchRetryStrategyProperty:
        def __init__(self, *, attempts: typing.Optional[jsii.Number] = None) -> None:
            '''The retry strategy to use for failed jobs, if the target is an AWS Batch job.

            If you specify a retry strategy here, it overrides the retry strategy defined in the job definition.

            :param attempts: The number of times to attempt to retry, if the job fails. Valid values are 1–10.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchretrystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                batch_retry_strategy_property = events.CfnRule.BatchRetryStrategyProperty(
                    attempts=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07a2eb860a6e3d4a1d81e83b7aef3bbf8dc36dc08084f22675dd40c4348167c5)
                check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attempts is not None:
                self._values["attempts"] = attempts

        @builtins.property
        def attempts(self) -> typing.Optional[jsii.Number]:
            '''The number of times to attempt to retry, if the job fails.

            Valid values are 1–10.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchretrystrategy.html#cfn-events-rule-batchretrystrategy-attempts
            '''
            result = self._values.get("attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchRetryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.CapacityProviderStrategyItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_provider": "capacityProvider",
            "base": "base",
            "weight": "weight",
        },
    )
    class CapacityProviderStrategyItemProperty:
        def __init__(
            self,
            *,
            capacity_provider: builtins.str,
            base: typing.Optional[jsii.Number] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The details of a capacity provider strategy.

            To learn more, see `CapacityProviderStrategyItem <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CapacityProviderStrategyItem.html>`_ in the Amazon ECS API Reference.

            :param capacity_provider: The short name of the capacity provider.
            :param base: The base value designates how many tasks, at a minimum, to run on the specified capacity provider. Only one capacity provider in a capacity provider strategy can have a base defined. If no value is specified, the default value of 0 is used.
            :param weight: The weight value designates the relative percentage of the total number of tasks launched that should use the specified capacity provider. The weight value is taken into consideration after the base value, if defined, is satisfied.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-capacityproviderstrategyitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                capacity_provider_strategy_item_property = events.CfnRule.CapacityProviderStrategyItemProperty(
                    capacity_provider="capacityProvider",
                
                    # the properties below are optional
                    base=123,
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1287bc79b1604ba267b9e845cf9a5b9fde4142070e47f06ef36c1e0af8e30d29)
                check_type(argname="argument capacity_provider", value=capacity_provider, expected_type=type_hints["capacity_provider"])
                check_type(argname="argument base", value=base, expected_type=type_hints["base"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "capacity_provider": capacity_provider,
            }
            if base is not None:
                self._values["base"] = base
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def capacity_provider(self) -> builtins.str:
            '''The short name of the capacity provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-capacityproviderstrategyitem.html#cfn-events-rule-capacityproviderstrategyitem-capacityprovider
            '''
            result = self._values.get("capacity_provider")
            assert result is not None, "Required property 'capacity_provider' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def base(self) -> typing.Optional[jsii.Number]:
            '''The base value designates how many tasks, at a minimum, to run on the specified capacity provider.

            Only one capacity provider in a capacity provider strategy can have a base defined. If no value is specified, the default value of 0 is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-capacityproviderstrategyitem.html#cfn-events-rule-capacityproviderstrategyitem-base
            '''
            result = self._values.get("base")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The weight value designates the relative percentage of the total number of tasks launched that should use the specified capacity provider.

            The weight value is taken into consideration after the base value, if defined, is satisfied.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-capacityproviderstrategyitem.html#cfn-events-rule-capacityproviderstrategyitem-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProviderStrategyItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.DeadLetterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class DeadLetterConfigProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''A ``DeadLetterConfig`` object that contains information about a dead-letter queue configuration.

            :param arn: The ARN of the SQS queue specified as the target for the dead-letter queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-deadletterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                dead_letter_config_property = events.CfnRule.DeadLetterConfigProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dbd7e6a3242956a5cbaf1d58b39b42483f55575378a1aa578652bd194b9ab7c1)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the SQS queue specified as the target for the dead-letter queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-deadletterconfig.html#cfn-events-rule-deadletterconfig-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.EcsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "task_definition_arn": "taskDefinitionArn",
            "capacity_provider_strategy": "capacityProviderStrategy",
            "enable_ecs_managed_tags": "enableEcsManagedTags",
            "enable_execute_command": "enableExecuteCommand",
            "group": "group",
            "launch_type": "launchType",
            "network_configuration": "networkConfiguration",
            "placement_constraints": "placementConstraints",
            "placement_strategies": "placementStrategies",
            "platform_version": "platformVersion",
            "propagate_tags": "propagateTags",
            "reference_id": "referenceId",
            "tag_list": "tagList",
            "task_count": "taskCount",
        },
    )
    class EcsParametersProperty:
        def __init__(
            self,
            *,
            task_definition_arn: builtins.str,
            capacity_provider_strategy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.CapacityProviderStrategyItemProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            enable_execute_command: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            group: typing.Optional[builtins.str] = None,
            launch_type: typing.Optional[builtins.str] = None,
            network_configuration: typing.Optional[typing.Union[typing.Union["CfnRule.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            placement_constraints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.PlacementConstraintProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            placement_strategies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.PlacementStrategyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            platform_version: typing.Optional[builtins.str] = None,
            propagate_tags: typing.Optional[builtins.str] = None,
            reference_id: typing.Optional[builtins.str] = None,
            tag_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            task_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The custom parameters to be used when the target is an Amazon ECS task.

            :param task_definition_arn: The ARN of the task definition to use if the event target is an Amazon ECS task.
            :param capacity_provider_strategy: The capacity provider strategy to use for the task. If a ``capacityProviderStrategy`` is specified, the ``launchType`` parameter must be omitted. If no ``capacityProviderStrategy`` or launchType is specified, the ``defaultCapacityProviderStrategy`` for the cluster is used.
            :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the task. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ in the Amazon Elastic Container Service Developer Guide.
            :param enable_execute_command: Whether or not to enable the execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task.
            :param group: Specifies an ECS task group for the task. The maximum length is 255 characters.
            :param launch_type: Specifies the launch type on which your task is running. The launch type that you specify here must match one of the launch type (compatibilities) of the target task. The ``FARGATE`` value is supported only in the Regions where AWS Fargate with Amazon ECS is supported. For more information, see `AWS Fargate on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS-Fargate.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param network_configuration: Use this structure if the Amazon ECS task uses the ``awsvpc`` network mode. This structure specifies the VPC subnets and security groups associated with the task, and whether a public IP address is to be used. This structure is required if ``LaunchType`` is ``FARGATE`` because the ``awsvpc`` mode is required for Fargate tasks. If you specify ``NetworkConfiguration`` when the target ECS task does not use the ``awsvpc`` network mode, the task fails.
            :param placement_constraints: An array of placement constraint objects to use for the task. You can specify up to 10 constraints per task (including constraints in the task definition and those specified at runtime).
            :param placement_strategies: The placement strategy objects to use for the task. You can specify a maximum of five strategy rules per task.
            :param platform_version: Specifies the platform version for the task. Specify only the numeric portion of the platform version, such as ``1.1.0`` . This structure is used only if ``LaunchType`` is ``FARGATE`` . For more information about valid platform versions, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param propagate_tags: Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Tags can only be propagated to the task during task creation. To add tags to a task after task creation, use the TagResource API action.
            :param reference_id: The reference ID to use for the task.
            :param tag_list: The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. To learn more, see `RunTask <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html#ECS-RunTask-request-tags>`_ in the Amazon ECS API Reference.
            :param task_count: The number of tasks to create based on ``TaskDefinition`` . The default is 1.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                ecs_parameters_property = events.CfnRule.EcsParametersProperty(
                    task_definition_arn="taskDefinitionArn",
                
                    # the properties below are optional
                    capacity_provider_strategy=[events.CfnRule.CapacityProviderStrategyItemProperty(
                        capacity_provider="capacityProvider",
                
                        # the properties below are optional
                        base=123,
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=events.CfnRule.NetworkConfigurationProperty(
                        aws_vpc_configuration=events.CfnRule.AwsVpcConfigurationProperty(
                            subnets=["subnets"],
                
                            # the properties below are optional
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"]
                        )
                    ),
                    placement_constraints=[events.CfnRule.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategies=[events.CfnRule.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tag_list=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    task_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__623d781f9bf9998c35e5b8102f4f7e34e7d4379e3b922acdaa2d61aead792717)
                check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
                check_type(argname="argument capacity_provider_strategy", value=capacity_provider_strategy, expected_type=type_hints["capacity_provider_strategy"])
                check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
                check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
                check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
                check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
                check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
                check_type(argname="argument placement_strategies", value=placement_strategies, expected_type=type_hints["placement_strategies"])
                check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
                check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
                check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
                check_type(argname="argument tag_list", value=tag_list, expected_type=type_hints["tag_list"])
                check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "task_definition_arn": task_definition_arn,
            }
            if capacity_provider_strategy is not None:
                self._values["capacity_provider_strategy"] = capacity_provider_strategy
            if enable_ecs_managed_tags is not None:
                self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
            if enable_execute_command is not None:
                self._values["enable_execute_command"] = enable_execute_command
            if group is not None:
                self._values["group"] = group
            if launch_type is not None:
                self._values["launch_type"] = launch_type
            if network_configuration is not None:
                self._values["network_configuration"] = network_configuration
            if placement_constraints is not None:
                self._values["placement_constraints"] = placement_constraints
            if placement_strategies is not None:
                self._values["placement_strategies"] = placement_strategies
            if platform_version is not None:
                self._values["platform_version"] = platform_version
            if propagate_tags is not None:
                self._values["propagate_tags"] = propagate_tags
            if reference_id is not None:
                self._values["reference_id"] = reference_id
            if tag_list is not None:
                self._values["tag_list"] = tag_list
            if task_count is not None:
                self._values["task_count"] = task_count

        @builtins.property
        def task_definition_arn(self) -> builtins.str:
            '''The ARN of the task definition to use if the event target is an Amazon ECS task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taskdefinitionarn
            '''
            result = self._values.get("task_definition_arn")
            assert result is not None, "Required property 'task_definition_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def capacity_provider_strategy(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.CapacityProviderStrategyItemProperty", _IResolvable_a771d0ef]]]]:
            '''The capacity provider strategy to use for the task.

            If a ``capacityProviderStrategy`` is specified, the ``launchType`` parameter must be omitted. If no ``capacityProviderStrategy`` or launchType is specified, the ``defaultCapacityProviderStrategy`` for the cluster is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-capacityproviderstrategy
            '''
            result = self._values.get("capacity_provider_strategy")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.CapacityProviderStrategyItemProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def enable_ecs_managed_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to enable Amazon ECS managed tags for the task.

            For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ in the Amazon Elastic Container Service Developer Guide.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-enableecsmanagedtags
            '''
            result = self._values.get("enable_ecs_managed_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def enable_execute_command(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether or not to enable the execute command functionality for the containers in this task.

            If true, this enables execute command functionality on all containers in the task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-enableexecutecommand
            '''
            result = self._values.get("enable_execute_command")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def group(self) -> typing.Optional[builtins.str]:
            '''Specifies an ECS task group for the task.

            The maximum length is 255 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-group
            '''
            result = self._values.get("group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the launch type on which your task is running.

            The launch type that you specify here must match one of the launch type (compatibilities) of the target task. The ``FARGATE`` value is supported only in the Regions where AWS Fargate with Amazon ECS is supported. For more information, see `AWS Fargate on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS-Fargate.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-launchtype
            '''
            result = self._values.get("launch_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.NetworkConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Use this structure if the Amazon ECS task uses the ``awsvpc`` network mode.

            This structure specifies the VPC subnets and security groups associated with the task, and whether a public IP address is to be used. This structure is required if ``LaunchType`` is ``FARGATE`` because the ``awsvpc`` mode is required for Fargate tasks.

            If you specify ``NetworkConfiguration`` when the target ECS task does not use the ``awsvpc`` network mode, the task fails.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-networkconfiguration
            '''
            result = self._values.get("network_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnRule.NetworkConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def placement_constraints(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.PlacementConstraintProperty", _IResolvable_a771d0ef]]]]:
            '''An array of placement constraint objects to use for the task.

            You can specify up to 10 constraints per task (including constraints in the task definition and those specified at runtime).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-placementconstraints
            '''
            result = self._values.get("placement_constraints")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.PlacementConstraintProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def placement_strategies(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.PlacementStrategyProperty", _IResolvable_a771d0ef]]]]:
            '''The placement strategy objects to use for the task.

            You can specify a maximum of five strategy rules per task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-placementstrategies
            '''
            result = self._values.get("placement_strategies")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.PlacementStrategyProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def platform_version(self) -> typing.Optional[builtins.str]:
            '''Specifies the platform version for the task.

            Specify only the numeric portion of the platform version, such as ``1.1.0`` .

            This structure is used only if ``LaunchType`` is ``FARGATE`` . For more information about valid platform versions, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-platformversion
            '''
            result = self._values.get("platform_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def propagate_tags(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to propagate the tags from the task definition to the task.

            If no value is specified, the tags are not propagated. Tags can only be propagated to the task during task creation. To add tags to a task after task creation, use the TagResource API action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-propagatetags
            '''
            result = self._values.get("propagate_tags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reference_id(self) -> typing.Optional[builtins.str]:
            '''The reference ID to use for the task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-referenceid
            '''
            result = self._values.get("reference_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_list(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
            '''The metadata that you apply to the task to help you categorize and organize them.

            Each tag consists of a key and an optional value, both of which you define. To learn more, see `RunTask <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html#ECS-RunTask-request-tags>`_ in the Amazon ECS API Reference.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taglist
            '''
            result = self._values.get("tag_list")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

        @builtins.property
        def task_count(self) -> typing.Optional[jsii.Number]:
            '''The number of tasks to create based on ``TaskDefinition`` .

            The default is 1.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taskcount
            '''
            result = self._values.get("task_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.HttpParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_parameters": "headerParameters",
            "path_parameter_values": "pathParameterValues",
            "query_string_parameters": "queryStringParameters",
        },
    )
    class HttpParametersProperty:
        def __init__(
            self,
            *,
            header_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            query_string_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''These are custom parameter to be used when the target is an API Gateway APIs or EventBridge ApiDestinations.

            In the latter case, these are merged with any InvocationParameters specified on the Connection, with any values from the Connection taking precedence.

            :param header_parameters: The headers that need to be sent as part of request invoking the API Gateway API or EventBridge ApiDestination.
            :param path_parameter_values: The path parameter values to be used to populate API Gateway API or EventBridge ApiDestination path wildcards ("*").
            :param query_string_parameters: The query string keys/values that need to be sent as part of request invoking the API Gateway API or EventBridge ApiDestination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-httpparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                http_parameters_property = events.CfnRule.HttpParametersProperty(
                    header_parameters={
                        "header_parameters_key": "headerParameters"
                    },
                    path_parameter_values=["pathParameterValues"],
                    query_string_parameters={
                        "query_string_parameters_key": "queryStringParameters"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e920a0b375bd58df77bb2269990dbb1f1212dd9945aea19847b196816d3db656)
                check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
                check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
                check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_parameters is not None:
                self._values["header_parameters"] = header_parameters
            if path_parameter_values is not None:
                self._values["path_parameter_values"] = path_parameter_values
            if query_string_parameters is not None:
                self._values["query_string_parameters"] = query_string_parameters

        @builtins.property
        def header_parameters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''The headers that need to be sent as part of request invoking the API Gateway API or EventBridge ApiDestination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-httpparameters.html#cfn-events-rule-httpparameters-headerparameters
            '''
            result = self._values.get("header_parameters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The path parameter values to be used to populate API Gateway API or EventBridge ApiDestination path wildcards ("*").

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-httpparameters.html#cfn-events-rule-httpparameters-pathparametervalues
            '''
            result = self._values.get("path_parameter_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def query_string_parameters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''The query string keys/values that need to be sent as part of request invoking the API Gateway API or EventBridge ApiDestination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-httpparameters.html#cfn-events-rule-httpparameters-querystringparameters
            '''
            result = self._values.get("query_string_parameters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.InputTransformerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_template": "inputTemplate",
            "input_paths_map": "inputPathsMap",
        },
    )
    class InputTransformerProperty:
        def __init__(
            self,
            *,
            input_template: builtins.str,
            input_paths_map: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''Contains the parameters needed for you to provide custom input to a target based on one or more pieces of data extracted from the event.

            :param input_template: Input template where you specify placeholders that will be filled with the values of the keys from ``InputPathsMap`` to customize the data sent to the target. Enclose each ``InputPathsMaps`` value in brackets: < *value* > If ``InputTemplate`` is a JSON object (surrounded by curly braces), the following restrictions apply: - The placeholder cannot be used as an object key. The following example shows the syntax for using ``InputPathsMap`` and ``InputTemplate`` . ``"InputTransformer":`` ``{`` ``"InputPathsMap": {"instance": "$.detail.instance","status": "$.detail.status"},`` ``"InputTemplate": "<instance> is in state <status>"`` ``}`` To have the ``InputTemplate`` include quote marks within a JSON string, escape each quote marks with a slash, as in the following example: ``"InputTransformer":`` ``{`` ``"InputPathsMap": {"instance": "$.detail.instance","status": "$.detail.status"},`` ``"InputTemplate": "<instance> is in state \\"<status>\\""`` ``}`` The ``InputTemplate`` can also be valid JSON with varibles in quotes or out, as in the following example: ``"InputTransformer":`` ``{`` ``"InputPathsMap": {"instance": "$.detail.instance","status": "$.detail.status"},`` ``"InputTemplate": '{"myInstance": <instance>,"myStatus": "<instance> is in state \\"<status>\\""}'`` ``}``
            :param input_paths_map: Map of JSON paths to be extracted from the event. You can then insert these in the template in ``InputTemplate`` to produce the output you want to be sent to the target. ``InputPathsMap`` is an array key-value pairs, where each value is a valid JSON path. You can have as many as 100 key-value pairs. You must use JSON dot notation, not bracket notation. The keys cannot start with " AWS ."

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                input_transformer_property = events.CfnRule.InputTransformerProperty(
                    input_template="inputTemplate",
                
                    # the properties below are optional
                    input_paths_map={
                        "input_paths_map_key": "inputPathsMap"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7bff3e9b7041e7cf3c0f2ac43ee4ea0370b51280bbe5ce24d385375fc1429c6)
                check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
                check_type(argname="argument input_paths_map", value=input_paths_map, expected_type=type_hints["input_paths_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "input_template": input_template,
            }
            if input_paths_map is not None:
                self._values["input_paths_map"] = input_paths_map

        @builtins.property
        def input_template(self) -> builtins.str:
            '''Input template where you specify placeholders that will be filled with the values of the keys from ``InputPathsMap`` to customize the data sent to the target.

            Enclose each ``InputPathsMaps`` value in brackets: < *value* >

            If ``InputTemplate`` is a JSON object (surrounded by curly braces), the following restrictions apply:

            - The placeholder cannot be used as an object key.

            The following example shows the syntax for using ``InputPathsMap`` and ``InputTemplate`` .

            ``"InputTransformer":``

            ``{``

            ``"InputPathsMap": {"instance": "$.detail.instance","status": "$.detail.status"},``

            ``"InputTemplate": "<instance> is in state <status>"``

            ``}``

            To have the ``InputTemplate`` include quote marks within a JSON string, escape each quote marks with a slash, as in the following example:

            ``"InputTransformer":``

            ``{``

            ``"InputPathsMap": {"instance": "$.detail.instance","status": "$.detail.status"},``

            ``"InputTemplate": "<instance> is in state \\"<status>\\""``

            ``}``

            The ``InputTemplate`` can also be valid JSON with varibles in quotes or out, as in the following example:

            ``"InputTransformer":``

            ``{``

            ``"InputPathsMap": {"instance": "$.detail.instance","status": "$.detail.status"},``

            ``"InputTemplate": '{"myInstance": <instance>,"myStatus": "<instance> is in state \\"<status>\\""}'``

            ``}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html#cfn-events-rule-inputtransformer-inputtemplate
            '''
            result = self._values.get("input_template")
            assert result is not None, "Required property 'input_template' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def input_paths_map(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''Map of JSON paths to be extracted from the event.

            You can then insert these in the template in ``InputTemplate`` to produce the output you want to be sent to the target.

            ``InputPathsMap`` is an array key-value pairs, where each value is a valid JSON path. You can have as many as 100 key-value pairs. You must use JSON dot notation, not bracket notation.

            The keys cannot start with " AWS ."

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html#cfn-events-rule-inputtransformer-inputpathsmap
            '''
            result = self._values.get("input_paths_map")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputTransformerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.KinesisParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"partition_key_path": "partitionKeyPath"},
    )
    class KinesisParametersProperty:
        def __init__(self, *, partition_key_path: builtins.str) -> None:
            '''This object enables you to specify a JSON path to extract from the event and use as the partition key for the Amazon Kinesis data stream, so that you can control the shard to which the event goes.

            If you do not include this parameter, the default is to use the ``eventId`` as the partition key.

            :param partition_key_path: The JSON path to be extracted from the event and used as the partition key. For more information, see `Amazon Kinesis Streams Key Concepts <https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html#partition-key>`_ in the *Amazon Kinesis Streams Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-kinesisparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                kinesis_parameters_property = events.CfnRule.KinesisParametersProperty(
                    partition_key_path="partitionKeyPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__897acde325fc7d287ed36876fbcfe9b778bd20f506bca930103ed1bd5765290f)
                check_type(argname="argument partition_key_path", value=partition_key_path, expected_type=type_hints["partition_key_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "partition_key_path": partition_key_path,
            }

        @builtins.property
        def partition_key_path(self) -> builtins.str:
            '''The JSON path to be extracted from the event and used as the partition key.

            For more information, see `Amazon Kinesis Streams Key Concepts <https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html#partition-key>`_ in the *Amazon Kinesis Streams Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-kinesisparameters.html#cfn-events-rule-kinesisparameters-partitionkeypath
            '''
            result = self._values.get("partition_key_path")
            assert result is not None, "Required property 'partition_key_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_vpc_configuration": "awsVpcConfiguration"},
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            aws_vpc_configuration: typing.Optional[typing.Union[typing.Union["CfnRule.AwsVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''This structure specifies the network configuration for an ECS task.

            :param aws_vpc_configuration: Use this structure to specify the VPC subnets and security groups for the task, and whether a public IP address is to be used. This structure is relevant only for ECS tasks that use the ``awsvpc`` network mode.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                network_configuration_property = events.CfnRule.NetworkConfigurationProperty(
                    aws_vpc_configuration=events.CfnRule.AwsVpcConfigurationProperty(
                        subnets=["subnets"],
                
                        # the properties below are optional
                        assign_public_ip="assignPublicIp",
                        security_groups=["securityGroups"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2ff95c58b8fc55bd66393b857f64135abbb8c7ad11f677b319d906c4145e8a9)
                check_type(argname="argument aws_vpc_configuration", value=aws_vpc_configuration, expected_type=type_hints["aws_vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_vpc_configuration is not None:
                self._values["aws_vpc_configuration"] = aws_vpc_configuration

        @builtins.property
        def aws_vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.AwsVpcConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Use this structure to specify the VPC subnets and security groups for the task, and whether a public IP address is to be used.

            This structure is relevant only for ECS tasks that use the ``awsvpc`` network mode.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-networkconfiguration.html#cfn-events-rule-networkconfiguration-awsvpcconfiguration
            '''
            result = self._values.get("aws_vpc_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnRule.AwsVpcConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.PlacementConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "type": "type"},
    )
    class PlacementConstraintProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing a constraint on task placement.

            To learn more, see `Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_ in the Amazon Elastic Container Service Developer Guide.

            :param expression: A cluster query language expression to apply to the constraint. You cannot specify an expression if the constraint type is ``distinctInstance`` . To learn more, see `Cluster Query Language <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html>`_ in the Amazon Elastic Container Service Developer Guide.
            :param type: The type of constraint. Use distinctInstance to ensure that each task in a particular group is running on a different container instance. Use memberOf to restrict the selection to a group of valid candidates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-placementconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                placement_constraint_property = events.CfnRule.PlacementConstraintProperty(
                    expression="expression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1427aee94ae7328fb67561e3c879c2b872c2ed5f5118762c52e6dd038bd47d27)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''A cluster query language expression to apply to the constraint.

            You cannot specify an expression if the constraint type is ``distinctInstance`` . To learn more, see `Cluster Query Language <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html>`_ in the Amazon Elastic Container Service Developer Guide.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-placementconstraint.html#cfn-events-rule-placementconstraint-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of constraint.

            Use distinctInstance to ensure that each task in a particular group is running on a different container instance. Use memberOf to restrict the selection to a group of valid candidates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-placementconstraint.html#cfn-events-rule-placementconstraint-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.PlacementStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"field": "field", "type": "type"},
    )
    class PlacementStrategyProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The task placement strategy for a task or service.

            To learn more, see `Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_ in the Amazon Elastic Container Service Service Developer Guide.

            :param field: The field to apply the placement strategy against. For the spread placement strategy, valid values are instanceId (or host, which has the same effect), or any platform or custom attribute that is applied to a container instance, such as attribute:ecs.availability-zone. For the binpack placement strategy, valid values are cpu and memory. For the random placement strategy, this field is not used.
            :param type: The type of placement strategy. The random placement strategy randomly places tasks on available candidates. The spread placement strategy spreads placement across available candidates evenly based on the field parameter. The binpack strategy places tasks on available candidates that have the least available amount of the resource that is specified with the field parameter. For example, if you binpack on memory, a task is placed on the instance with the least amount of remaining memory (but still enough to run the task).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-placementstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                placement_strategy_property = events.CfnRule.PlacementStrategyProperty(
                    field="field",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__849aae0a476285f4f092aa5d1bb465b73004437e362e00295987935eb20593ae)
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to apply the placement strategy against.

            For the spread placement strategy, valid values are instanceId (or host, which has the same effect), or any platform or custom attribute that is applied to a container instance, such as attribute:ecs.availability-zone. For the binpack placement strategy, valid values are cpu and memory. For the random placement strategy, this field is not used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-placementstrategy.html#cfn-events-rule-placementstrategy-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of placement strategy.

            The random placement strategy randomly places tasks on available candidates. The spread placement strategy spreads placement across available candidates evenly based on the field parameter. The binpack strategy places tasks on available candidates that have the least available amount of the resource that is specified with the field parameter. For example, if you binpack on memory, a task is placed on the instance with the least amount of remaining memory (but still enough to run the task).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-placementstrategy.html#cfn-events-rule-placementstrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.RedshiftDataParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database": "database",
            "sql": "sql",
            "db_user": "dbUser",
            "secret_manager_arn": "secretManagerArn",
            "statement_name": "statementName",
            "with_event": "withEvent",
        },
    )
    class RedshiftDataParametersProperty:
        def __init__(
            self,
            *,
            database: builtins.str,
            sql: builtins.str,
            db_user: typing.Optional[builtins.str] = None,
            secret_manager_arn: typing.Optional[builtins.str] = None,
            statement_name: typing.Optional[builtins.str] = None,
            with_event: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''These are custom parameters to be used when the target is a Amazon Redshift cluster to invoke the Amazon Redshift Data API ExecuteStatement based on EventBridge events.

            :param database: The name of the database. Required when authenticating using temporary credentials.
            :param sql: The SQL statement text to run.
            :param db_user: The database user name. Required when authenticating using temporary credentials.
            :param secret_manager_arn: The name or ARN of the secret that enables access to the database. Required when authenticating using AWS Secrets Manager.
            :param statement_name: The name of the SQL statement. You can name the SQL statement when you create it to identify the query.
            :param with_event: Indicates whether to send an event back to EventBridge after the SQL statement runs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                redshift_data_parameters_property = events.CfnRule.RedshiftDataParametersProperty(
                    database="database",
                    sql="sql",
                
                    # the properties below are optional
                    db_user="dbUser",
                    secret_manager_arn="secretManagerArn",
                    statement_name="statementName",
                    with_event=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b1155ceb4ab0be750ebc8765fef132799d68adb5dd647fe4926b6f3a789c2b4)
                check_type(argname="argument database", value=database, expected_type=type_hints["database"])
                check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
                check_type(argname="argument db_user", value=db_user, expected_type=type_hints["db_user"])
                check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
                check_type(argname="argument statement_name", value=statement_name, expected_type=type_hints["statement_name"])
                check_type(argname="argument with_event", value=with_event, expected_type=type_hints["with_event"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "database": database,
                "sql": sql,
            }
            if db_user is not None:
                self._values["db_user"] = db_user
            if secret_manager_arn is not None:
                self._values["secret_manager_arn"] = secret_manager_arn
            if statement_name is not None:
                self._values["statement_name"] = statement_name
            if with_event is not None:
                self._values["with_event"] = with_event

        @builtins.property
        def database(self) -> builtins.str:
            '''The name of the database.

            Required when authenticating using temporary credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-database
            '''
            result = self._values.get("database")
            assert result is not None, "Required property 'database' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sql(self) -> builtins.str:
            '''The SQL statement text to run.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-sql
            '''
            result = self._values.get("sql")
            assert result is not None, "Required property 'sql' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def db_user(self) -> typing.Optional[builtins.str]:
            '''The database user name.

            Required when authenticating using temporary credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-dbuser
            '''
            result = self._values.get("db_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_manager_arn(self) -> typing.Optional[builtins.str]:
            '''The name or ARN of the secret that enables access to the database.

            Required when authenticating using AWS Secrets Manager.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-secretmanagerarn
            '''
            result = self._values.get("secret_manager_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def statement_name(self) -> typing.Optional[builtins.str]:
            '''The name of the SQL statement.

            You can name the SQL statement when you create it to identify the query.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-statementname
            '''
            result = self._values.get("statement_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def with_event(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether to send an event back to EventBridge after the SQL statement runs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-withevent
            '''
            result = self._values.get("with_event")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftDataParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.RetryPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_event_age_in_seconds": "maximumEventAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
        },
    )
    class RetryPolicyProperty:
        def __init__(
            self,
            *,
            maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A ``RetryPolicy`` object that includes information about the retry policy settings.

            :param maximum_event_age_in_seconds: The maximum amount of time, in seconds, to continue to make retry attempts.
            :param maximum_retry_attempts: The maximum number of retry attempts to make before the request fails. Retry attempts continue until either the maximum number of attempts is made or until the duration of the ``MaximumEventAgeInSeconds`` is met.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-retrypolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                retry_policy_property = events.CfnRule.RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c372d2c538d0503741123e1b047163e868b9592299e22e2a32f9bc936361a8aa)
                check_type(argname="argument maximum_event_age_in_seconds", value=maximum_event_age_in_seconds, expected_type=type_hints["maximum_event_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_event_age_in_seconds is not None:
                self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts

        @builtins.property
        def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, to continue to make retry attempts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-retrypolicy.html#cfn-events-rule-retrypolicy-maximumeventageinseconds
            '''
            result = self._values.get("maximum_event_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of retry attempts to make before the request fails.

            Retry attempts continue until either the maximum number of attempts is made or until the duration of the ``MaximumEventAgeInSeconds`` is met.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-retrypolicy.html#cfn-events-rule-retrypolicy-maximumretryattempts
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.RunCommandParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"run_command_targets": "runCommandTargets"},
    )
    class RunCommandParametersProperty:
        def __init__(
            self,
            *,
            run_command_targets: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.RunCommandTargetProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''This parameter contains the criteria (either InstanceIds or a tag) used to specify which EC2 instances are to be sent the command.

            :param run_command_targets: Currently, we support including only one RunCommandTarget block, which specifies either an array of InstanceIds or a tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                run_command_parameters_property = events.CfnRule.RunCommandParametersProperty(
                    run_command_targets=[events.CfnRule.RunCommandTargetProperty(
                        key="key",
                        values=["values"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cfc5fa3ac67d9f802292f1e5e7533ab584dbaa58c111af64678681c5dc77446)
                check_type(argname="argument run_command_targets", value=run_command_targets, expected_type=type_hints["run_command_targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "run_command_targets": run_command_targets,
            }

        @builtins.property
        def run_command_targets(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.RunCommandTargetProperty", _IResolvable_a771d0ef]]]:
            '''Currently, we support including only one RunCommandTarget block, which specifies either an array of InstanceIds or a tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandparameters.html#cfn-events-rule-runcommandparameters-runcommandtargets
            '''
            result = self._values.get("run_command_targets")
            assert result is not None, "Required property 'run_command_targets' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.RunCommandTargetProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunCommandParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.RunCommandTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class RunCommandTargetProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            values: typing.Sequence[builtins.str],
        ) -> None:
            '''Information about the EC2 instances that are to be sent the command, specified as key-value pairs.

            Each ``RunCommandTarget`` block can include only one key, but this key may specify multiple values.

            :param key: Can be either ``tag:`` *tag-key* or ``InstanceIds`` .
            :param values: If ``Key`` is ``tag:`` *tag-key* , ``Values`` is a list of tag values. If ``Key`` is ``InstanceIds`` , ``Values`` is a list of Amazon EC2 instance IDs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                run_command_target_property = events.CfnRule.RunCommandTargetProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54a15cb254deee2eb1f84bf9132ad60d8297905d7ccbb36b720e57e663cdd51b)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "values": values,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''Can be either ``tag:`` *tag-key* or ``InstanceIds`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html#cfn-events-rule-runcommandtarget-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def values(self) -> typing.List[builtins.str]:
            '''If ``Key`` is ``tag:`` *tag-key* , ``Values`` is a list of tag values.

            If ``Key`` is ``InstanceIds`` , ``Values`` is a list of Amazon EC2 instance IDs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html#cfn-events-rule-runcommandtarget-values
            '''
            result = self._values.get("values")
            assert result is not None, "Required property 'values' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunCommandTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.SageMakerPipelineParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class SageMakerPipelineParameterProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''Name/Value pair of a parameter to start execution of a SageMaker Model Building Pipeline.

            :param name: Name of parameter to start execution of a SageMaker Model Building Pipeline.
            :param value: Value of parameter to start execution of a SageMaker Model Building Pipeline.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sagemakerpipelineparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                sage_maker_pipeline_parameter_property = events.CfnRule.SageMakerPipelineParameterProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38d8d7d828e2d3e272c5ff59f66b4366f592dafd41b8240702b48097658643ff)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''Name of parameter to start execution of a SageMaker Model Building Pipeline.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sagemakerpipelineparameter.html#cfn-events-rule-sagemakerpipelineparameter-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Value of parameter to start execution of a SageMaker Model Building Pipeline.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sagemakerpipelineparameter.html#cfn-events-rule-sagemakerpipelineparameter-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerPipelineParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.SageMakerPipelineParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"pipeline_parameter_list": "pipelineParameterList"},
    )
    class SageMakerPipelineParametersProperty:
        def __init__(
            self,
            *,
            pipeline_parameter_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.SageMakerPipelineParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''These are custom parameters to use when the target is a SageMaker Model Building Pipeline that starts based on EventBridge events.

            :param pipeline_parameter_list: List of Parameter names and values for SageMaker Model Building Pipeline execution.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sagemakerpipelineparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                sage_maker_pipeline_parameters_property = events.CfnRule.SageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[events.CfnRule.SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f090ccc1fe727c016df390010b828a998ad7131bef2472f65864e89e611b06a2)
                check_type(argname="argument pipeline_parameter_list", value=pipeline_parameter_list, expected_type=type_hints["pipeline_parameter_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pipeline_parameter_list is not None:
                self._values["pipeline_parameter_list"] = pipeline_parameter_list

        @builtins.property
        def pipeline_parameter_list(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.SageMakerPipelineParameterProperty", _IResolvable_a771d0ef]]]]:
            '''List of Parameter names and values for SageMaker Model Building Pipeline execution.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sagemakerpipelineparameters.html#cfn-events-rule-sagemakerpipelineparameters-pipelineparameterlist
            '''
            result = self._values.get("pipeline_parameter_list")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.SageMakerPipelineParameterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerPipelineParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.SqsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"message_group_id": "messageGroupId"},
    )
    class SqsParametersProperty:
        def __init__(self, *, message_group_id: builtins.str) -> None:
            '''This structure includes the custom parameter to be used when the target is an SQS FIFO queue.

            :param message_group_id: The FIFO message group ID to use as the target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sqsparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                sqs_parameters_property = events.CfnRule.SqsParametersProperty(
                    message_group_id="messageGroupId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__565a2dd7cd60fb9b67b2e2575515d7bf6fedf7d71f1055e523a8278fd99cf961)
                check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "message_group_id": message_group_id,
            }

        @builtins.property
        def message_group_id(self) -> builtins.str:
            '''The FIFO message group ID to use as the target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sqsparameters.html#cfn-events-rule-sqsparameters-messagegroupid
            '''
            result = self._values.get("message_group_id")
            assert result is not None, "Required property 'message_group_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.TagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key-value pair associated with an ECS Target of an EventBridge rule.

            The tag will be propagated to ECS by EventBridge when starting an ECS task based on a matched event.
            .. epigraph::

               Currently, tags are only available when using ECS with EventBridge .

            :param key: A string you can use to assign a value. The combination of tag keys and values can help you organize and categorize your resources.
            :param value: The value for the specified tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-tag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                tag_property = events.CfnRule.TagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c60b35cdfde0ea3e8670cd6598e824ffb005c7778b95d95cd69a3a3aca6f8812)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''A string you can use to assign a value.

            The combination of tag keys and values can help you organize and categorize your resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-tag.html#cfn-events-rule-tag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the specified tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-tag.html#cfn-events-rule-tag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_events.CfnRule.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "id": "id",
            "batch_parameters": "batchParameters",
            "dead_letter_config": "deadLetterConfig",
            "ecs_parameters": "ecsParameters",
            "http_parameters": "httpParameters",
            "input": "input",
            "input_path": "inputPath",
            "input_transformer": "inputTransformer",
            "kinesis_parameters": "kinesisParameters",
            "redshift_data_parameters": "redshiftDataParameters",
            "retry_policy": "retryPolicy",
            "role_arn": "roleArn",
            "run_command_parameters": "runCommandParameters",
            "sage_maker_pipeline_parameters": "sageMakerPipelineParameters",
            "sqs_parameters": "sqsParameters",
        },
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            arn: builtins.str,
            id: builtins.str,
            batch_parameters: typing.Optional[typing.Union[typing.Union["CfnRule.BatchParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dead_letter_config: typing.Optional[typing.Union[typing.Union["CfnRule.DeadLetterConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ecs_parameters: typing.Optional[typing.Union[typing.Union["CfnRule.EcsParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            http_parameters: typing.Optional[typing.Union[typing.Union["CfnRule.HttpParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
            input_transformer: typing.Optional[typing.Union[typing.Union["CfnRule.InputTransformerProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            kinesis_parameters: typing.Optional[typing.Union[typing.Union["CfnRule.KinesisParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            redshift_data_parameters: typing.Optional[typing.Union[typing.Union["CfnRule.RedshiftDataParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            retry_policy: typing.Optional[typing.Union[typing.Union["CfnRule.RetryPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            run_command_parameters: typing.Optional[typing.Union[typing.Union["CfnRule.RunCommandParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sage_maker_pipeline_parameters: typing.Optional[typing.Union[typing.Union["CfnRule.SageMakerPipelineParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sqs_parameters: typing.Optional[typing.Union[typing.Union["CfnRule.SqsParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Targets are the resources to be invoked when a rule is triggered.

            For a complete list of services and resources that can be set as a target, see `PutTargets <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutTargets.html>`_ .

            If you are setting the event bus of another account as the target, and that account granted permission to your account through an organization instead of directly by the account ID, then you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure. For more information, see `Sending and Receiving Events Between AWS Accounts <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html>`_ in the *Amazon EventBridge User Guide* .

            :param arn: The Amazon Resource Name (ARN) of the target.
            :param id: The ID of the target within the specified rule. Use this ID to reference the target when updating the rule. We recommend using a memorable and unique string.
            :param batch_parameters: If the event target is an AWS Batch job, this contains the job definition, job name, and other parameters. For more information, see `Jobs <https://docs.aws.amazon.com/batch/latest/userguide/jobs.html>`_ in the *AWS Batch User Guide* .
            :param dead_letter_config: The ``DeadLetterConfig`` that defines the target queue to send dead-letter queue events to.
            :param ecs_parameters: Contains the Amazon ECS task definition and task count to be used, if the event target is an Amazon ECS task. For more information about Amazon ECS tasks, see `Task Definitions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_defintions.html>`_ in the *Amazon EC2 Container Service Developer Guide* .
            :param http_parameters: Contains the HTTP parameters to use when the target is a API Gateway endpoint or EventBridge ApiDestination. If you specify an API Gateway API or EventBridge ApiDestination as a target, you can use this parameter to specify headers, path parameters, and query string keys/values as part of your target invoking request. If you're using ApiDestinations, the corresponding Connection can also have these values configured. In case of any conflicting keys, values from the Connection take precedence.
            :param input: Valid JSON text passed to the target. In this case, nothing from the event itself is passed to the target. For more information, see `The JavaScript Object Notation (JSON) Data Interchange Format <https://docs.aws.amazon.com/http://www.rfc-editor.org/rfc/rfc7159.txt>`_ .
            :param input_path: The value of the JSONPath that is used for extracting part of the matched event when passing it to the target. You may use JSON dot notation or bracket notation. For more information about JSON paths, see `JSONPath <https://docs.aws.amazon.com/http://goessner.net/articles/JsonPath/>`_ .
            :param input_transformer: Settings to enable you to provide custom input to a target based on certain event data. You can extract one or more key-value pairs from the event and then use that data to send customized input to the target.
            :param kinesis_parameters: The custom parameter you can use to control the shard assignment, when the target is a Kinesis data stream. If you do not include this parameter, the default is to use the ``eventId`` as the partition key.
            :param redshift_data_parameters: Contains the Amazon Redshift Data API parameters to use when the target is a Amazon Redshift cluster. If you specify a Amazon Redshift Cluster as a Target, you can use this to specify parameters to invoke the Amazon Redshift Data API ExecuteStatement based on EventBridge events.
            :param retry_policy: The ``RetryPolicy`` object that contains the retry policy configuration to use for the dead-letter queue.
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role to be used for this target when the rule is triggered. If one rule triggers multiple targets, you can use a different IAM role for each target.
            :param run_command_parameters: Parameters used when you are using the rule to invoke Amazon EC2 Run Command.
            :param sage_maker_pipeline_parameters: Contains the SageMaker Model Building Pipeline parameters to start execution of a SageMaker Model Building Pipeline. If you specify a SageMaker Model Building Pipeline as a target, you can use this to specify parameters to start a pipeline execution based on EventBridge events.
            :param sqs_parameters: Contains the message group ID to use when the target is a FIFO queue. If you specify an SQS FIFO queue as a target, the queue must have content-based deduplication enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_events as events
                
                target_property = events.CfnRule.TargetProperty(
                    arn="arn",
                    id="id",
                
                    # the properties below are optional
                    batch_parameters=events.CfnRule.BatchParametersProperty(
                        job_definition="jobDefinition",
                        job_name="jobName",
                
                        # the properties below are optional
                        array_properties=events.CfnRule.BatchArrayPropertiesProperty(
                            size=123
                        ),
                        retry_strategy=events.CfnRule.BatchRetryStrategyProperty(
                            attempts=123
                        )
                    ),
                    dead_letter_config=events.CfnRule.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    ecs_parameters=events.CfnRule.EcsParametersProperty(
                        task_definition_arn="taskDefinitionArn",
                
                        # the properties below are optional
                        capacity_provider_strategy=[events.CfnRule.CapacityProviderStrategyItemProperty(
                            capacity_provider="capacityProvider",
                
                            # the properties below are optional
                            base=123,
                            weight=123
                        )],
                        enable_ecs_managed_tags=False,
                        enable_execute_command=False,
                        group="group",
                        launch_type="launchType",
                        network_configuration=events.CfnRule.NetworkConfigurationProperty(
                            aws_vpc_configuration=events.CfnRule.AwsVpcConfigurationProperty(
                                subnets=["subnets"],
                
                                # the properties below are optional
                                assign_public_ip="assignPublicIp",
                                security_groups=["securityGroups"]
                            )
                        ),
                        placement_constraints=[events.CfnRule.PlacementConstraintProperty(
                            expression="expression",
                            type="type"
                        )],
                        placement_strategies=[events.CfnRule.PlacementStrategyProperty(
                            field="field",
                            type="type"
                        )],
                        platform_version="platformVersion",
                        propagate_tags="propagateTags",
                        reference_id="referenceId",
                        tag_list=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        task_count=123
                    ),
                    http_parameters=events.CfnRule.HttpParametersProperty(
                        header_parameters={
                            "header_parameters_key": "headerParameters"
                        },
                        path_parameter_values=["pathParameterValues"],
                        query_string_parameters={
                            "query_string_parameters_key": "queryStringParameters"
                        }
                    ),
                    input="input",
                    input_path="inputPath",
                    input_transformer=events.CfnRule.InputTransformerProperty(
                        input_template="inputTemplate",
                
                        # the properties below are optional
                        input_paths_map={
                            "input_paths_map_key": "inputPathsMap"
                        }
                    ),
                    kinesis_parameters=events.CfnRule.KinesisParametersProperty(
                        partition_key_path="partitionKeyPath"
                    ),
                    redshift_data_parameters=events.CfnRule.RedshiftDataParametersProperty(
                        database="database",
                        sql="sql",
                
                        # the properties below are optional
                        db_user="dbUser",
                        secret_manager_arn="secretManagerArn",
                        statement_name="statementName",
                        with_event=False
                    ),
                    retry_policy=events.CfnRule.RetryPolicyProperty(
                        maximum_event_age_in_seconds=123,
                        maximum_retry_attempts=123
                    ),
                    role_arn="roleArn",
                    run_command_parameters=events.CfnRule.RunCommandParametersProperty(
                        run_command_targets=[events.CfnRule.RunCommandTargetProperty(
                            key="key",
                            values=["values"]
                        )]
                    ),
                    sage_maker_pipeline_parameters=events.CfnRule.SageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[events.CfnRule.SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_parameters=events.CfnRule.SqsParametersProperty(
                        message_group_id="messageGroupId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e892f6930c9de3bae44a45977f41013f05f0c5c20431e9e0317f940d18a73a43)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument batch_parameters", value=batch_parameters, expected_type=type_hints["batch_parameters"])
                check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
                check_type(argname="argument ecs_parameters", value=ecs_parameters, expected_type=type_hints["ecs_parameters"])
                check_type(argname="argument http_parameters", value=http_parameters, expected_type=type_hints["http_parameters"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
                check_type(argname="argument input_transformer", value=input_transformer, expected_type=type_hints["input_transformer"])
                check_type(argname="argument kinesis_parameters", value=kinesis_parameters, expected_type=type_hints["kinesis_parameters"])
                check_type(argname="argument redshift_data_parameters", value=redshift_data_parameters, expected_type=type_hints["redshift_data_parameters"])
                check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument run_command_parameters", value=run_command_parameters, expected_type=type_hints["run_command_parameters"])
                check_type(argname="argument sage_maker_pipeline_parameters", value=sage_maker_pipeline_parameters, expected_type=type_hints["sage_maker_pipeline_parameters"])
                check_type(argname="argument sqs_parameters", value=sqs_parameters, expected_type=type_hints["sqs_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
                "id": id,
            }
            if batch_parameters is not None:
                self._values["batch_parameters"] = batch_parameters
            if dead_letter_config is not None:
                self._values["dead_letter_config"] = dead_letter_config
            if ecs_parameters is not None:
                self._values["ecs_parameters"] = ecs_parameters
            if http_parameters is not None:
                self._values["http_parameters"] = http_parameters
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path
            if input_transformer is not None:
                self._values["input_transformer"] = input_transformer
            if kinesis_parameters is not None:
                self._values["kinesis_parameters"] = kinesis_parameters
            if redshift_data_parameters is not None:
                self._values["redshift_data_parameters"] = redshift_data_parameters
            if retry_policy is not None:
                self._values["retry_policy"] = retry_policy
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if run_command_parameters is not None:
                self._values["run_command_parameters"] = run_command_parameters
            if sage_maker_pipeline_parameters is not None:
                self._values["sage_maker_pipeline_parameters"] = sage_maker_pipeline_parameters
            if sqs_parameters is not None:
                self._values["sqs_parameters"] = sqs_parameters

        @builtins.property
        def arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''The ID of the target within the specified rule.

            Use this ID to reference the target when updating the rule. We recommend using a memorable and unique string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.BatchParametersProperty", _IResolvable_a771d0ef]]:
            '''If the event target is an AWS Batch job, this contains the job definition, job name, and other parameters.

            For more information, see `Jobs <https://docs.aws.amazon.com/batch/latest/userguide/jobs.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-batchparameters
            '''
            result = self._values.get("batch_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnRule.BatchParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dead_letter_config(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.DeadLetterConfigProperty", _IResolvable_a771d0ef]]:
            '''The ``DeadLetterConfig`` that defines the target queue to send dead-letter queue events to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-deadletterconfig
            '''
            result = self._values.get("dead_letter_config")
            return typing.cast(typing.Optional[typing.Union["CfnRule.DeadLetterConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ecs_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.EcsParametersProperty", _IResolvable_a771d0ef]]:
            '''Contains the Amazon ECS task definition and task count to be used, if the event target is an Amazon ECS task.

            For more information about Amazon ECS tasks, see `Task Definitions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_defintions.html>`_ in the *Amazon EC2 Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-ecsparameters
            '''
            result = self._values.get("ecs_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnRule.EcsParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def http_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.HttpParametersProperty", _IResolvable_a771d0ef]]:
            '''Contains the HTTP parameters to use when the target is a API Gateway endpoint or EventBridge ApiDestination.

            If you specify an API Gateway API or EventBridge ApiDestination as a target, you can use this parameter to specify headers, path parameters, and query string keys/values as part of your target invoking request. If you're using ApiDestinations, the corresponding Connection can also have these values configured. In case of any conflicting keys, values from the Connection take precedence.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-httpparameters
            '''
            result = self._values.get("http_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnRule.HttpParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''Valid JSON text passed to the target.

            In this case, nothing from the event itself is passed to the target. For more information, see `The JavaScript Object Notation (JSON) Data Interchange Format <https://docs.aws.amazon.com/http://www.rfc-editor.org/rfc/rfc7159.txt>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''The value of the JSONPath that is used for extracting part of the matched event when passing it to the target.

            You may use JSON dot notation or bracket notation. For more information about JSON paths, see `JSONPath <https://docs.aws.amazon.com/http://goessner.net/articles/JsonPath/>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-inputpath
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_transformer(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.InputTransformerProperty", _IResolvable_a771d0ef]]:
            '''Settings to enable you to provide custom input to a target based on certain event data.

            You can extract one or more key-value pairs from the event and then use that data to send customized input to the target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-inputtransformer
            '''
            result = self._values.get("input_transformer")
            return typing.cast(typing.Optional[typing.Union["CfnRule.InputTransformerProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.KinesisParametersProperty", _IResolvable_a771d0ef]]:
            '''The custom parameter you can use to control the shard assignment, when the target is a Kinesis data stream.

            If you do not include this parameter, the default is to use the ``eventId`` as the partition key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-kinesisparameters
            '''
            result = self._values.get("kinesis_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnRule.KinesisParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def redshift_data_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.RedshiftDataParametersProperty", _IResolvable_a771d0ef]]:
            '''Contains the Amazon Redshift Data API parameters to use when the target is a Amazon Redshift cluster.

            If you specify a Amazon Redshift Cluster as a Target, you can use this to specify parameters to invoke the Amazon Redshift Data API ExecuteStatement based on EventBridge events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-redshiftdataparameters
            '''
            result = self._values.get("redshift_data_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnRule.RedshiftDataParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def retry_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.RetryPolicyProperty", _IResolvable_a771d0ef]]:
            '''The ``RetryPolicy`` object that contains the retry policy configuration to use for the dead-letter queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-retrypolicy
            '''
            result = self._values.get("retry_policy")
            return typing.cast(typing.Optional[typing.Union["CfnRule.RetryPolicyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role to be used for this target when the rule is triggered.

            If one rule triggers multiple targets, you can use a different IAM role for each target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def run_command_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.RunCommandParametersProperty", _IResolvable_a771d0ef]]:
            '''Parameters used when you are using the rule to invoke Amazon EC2 Run Command.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-runcommandparameters
            '''
            result = self._values.get("run_command_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnRule.RunCommandParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sage_maker_pipeline_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.SageMakerPipelineParametersProperty", _IResolvable_a771d0ef]]:
            '''Contains the SageMaker Model Building Pipeline parameters to start execution of a SageMaker Model Building Pipeline.

            If you specify a SageMaker Model Building Pipeline as a target, you can use this to specify parameters to start a pipeline execution based on EventBridge events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-sagemakerpipelineparameters
            '''
            result = self._values.get("sage_maker_pipeline_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnRule.SageMakerPipelineParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqs_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.SqsParametersProperty", _IResolvable_a771d0ef]]:
            '''Contains the message group ID to use when the target is a FIFO queue.

            If you specify an SQS FIFO queue as a target, the queue must have content-based deduplication enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-sqsparameters
            '''
            result = self._values.get("sqs_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnRule.SqsParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_events.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "event_bus_name": "eventBusName",
        "event_pattern": "eventPattern",
        "name": "name",
        "role_arn": "roleArn",
        "schedule_expression": "scheduleExpression",
        "state": "state",
        "targets": "targets",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
        event_pattern: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRule``.

        :param description: The description of the rule.
        :param event_bus_name: The name or ARN of the event bus associated with the rule. If you omit this, the default event bus is used.
        :param event_pattern: The event pattern of the rule. For more information, see `Events and Event Patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html>`_ in the *Amazon EventBridge User Guide* .
        :param name: The name of the rule.
        :param role_arn: The Amazon Resource Name (ARN) of the role that is used for target invocation. If you're setting an event bus in another account as the target and that account granted permission to your account through an organization instead of directly by the account ID, you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure, instead of here in this parameter.
        :param schedule_expression: The scheduling expression. For example, "cron(0 20 * * ? *)", "rate(5 minutes)". For more information, see `Creating an Amazon EventBridge rule that runs on a schedule <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html>`_ .
        :param state: The state of the rule.
        :param targets: Adds the specified targets to the specified rule, or updates the targets if they are already associated with the rule. Targets are the resources that are invoked when a rule is triggered. The maximum number of entries per request is 10. .. epigraph:: Each rule can have up to five (5) targets associated with it at one time. For a list of services you can configure as targets for events, see `EventBridge targets <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html>`_ in the *Amazon EventBridge User Guide* . Creating rules with built-in targets is supported only in the AWS Management Console . The built-in targets are: - ``Amazon EBS CreateSnapshot API call`` - ``Amazon EC2 RebootInstances API call`` - ``Amazon EC2 StopInstances API call`` - ``Amazon EC2 TerminateInstances API call`` For some target types, ``PutTargets`` provides target-specific parameters. If the target is a Kinesis data stream, you can optionally specify which shard the event goes to by using the ``KinesisParameters`` argument. To invoke a command on multiple EC2 instances with one rule, you can use the ``RunCommandParameters`` field. To be able to make API calls against the resources that you own, Amazon EventBridge needs the appropriate permissions: - For AWS Lambda and Amazon SNS resources, EventBridge relies on resource-based policies. - For EC2 instances, Kinesis Data Streams, AWS Step Functions state machines and API Gateway APIs, EventBridge relies on IAM roles that you specify in the ``RoleARN`` argument in ``PutTargets`` . For more information, see `Authentication and Access Control <https://docs.aws.amazon.com/eventbridge/latest/userguide/auth-and-access-control-eventbridge.html>`_ in the *Amazon EventBridge User Guide* . If another AWS account is in the same region and has granted you permission (using ``PutPermission`` ), you can send events to that account. Set that account's event bus as a target of the rules in your account. To send the matched events to the other account, specify that account's event bus as the ``Arn`` value when you run ``PutTargets`` . If your account sends events to another account, your account is charged for each sent event. Each event sent to another account is charged as a custom event. The account receiving the event is not charged. For more information, see `Amazon EventBridge Pricing <https://docs.aws.amazon.com/eventbridge/pricing/>`_ . .. epigraph:: ``Input`` , ``InputPath`` , and ``InputTransformer`` are not available with ``PutTarget`` if the target is an event bus of a different AWS account. If you are setting the event bus of another account as the target, and that account granted permission to your account through an organization instead of directly by the account ID, then you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure. For more information, see `Sending and Receiving Events Between AWS Accounts <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html>`_ in the *Amazon EventBridge User Guide* . .. epigraph:: If you have an IAM role on a cross-account event bus target, a ``PutTargets`` call without a role on the same target (same ``Id`` and ``Arn`` ) will not remove the role. For more information about enabling cross-account events, see `PutPermission <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutPermission.html>`_ . *Input* , *InputPath* , and *InputTransformer* are mutually exclusive and optional parameters of a target. When a rule is triggered due to a matched event: - If none of the following arguments are specified for a target, then the entire event is passed to the target in JSON format (unless the target is Amazon EC2 Run Command or Amazon ECS task, in which case nothing from the event is passed to the target). - If *Input* is specified in the form of valid JSON, then the matched event is overridden with this constant. - If *InputPath* is specified in the form of JSONPath (for example, ``$.detail`` ), then only the part of the event specified in the path is passed to the target (for example, only the detail part of the event is passed). - If *InputTransformer* is specified, then one or more specified JSONPaths are extracted from the event and used as values in a template that you specify as the input to the target. When you specify ``InputPath`` or ``InputTransformer`` , you must use JSON dot notation, not bracket notation. When you add targets to a rule and the associated rule triggers soon after, new or updated targets might not be immediately invoked. Allow a short period of time for changes to take effect. This action can partially fail if too many requests are made at the same time. If that happens, ``FailedEntryCount`` is non-zero in the response and each entry in ``FailedEntries`` provides the ID of the failed target and the error code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            # event_pattern: Any
            
            cfn_rule_props = events.CfnRuleProps(
                description="description",
                event_bus_name="eventBusName",
                event_pattern=event_pattern,
                name="name",
                role_arn="roleArn",
                schedule_expression="scheduleExpression",
                state="state",
                targets=[events.CfnRule.TargetProperty(
                    arn="arn",
                    id="id",
            
                    # the properties below are optional
                    batch_parameters=events.CfnRule.BatchParametersProperty(
                        job_definition="jobDefinition",
                        job_name="jobName",
            
                        # the properties below are optional
                        array_properties=events.CfnRule.BatchArrayPropertiesProperty(
                            size=123
                        ),
                        retry_strategy=events.CfnRule.BatchRetryStrategyProperty(
                            attempts=123
                        )
                    ),
                    dead_letter_config=events.CfnRule.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    ecs_parameters=events.CfnRule.EcsParametersProperty(
                        task_definition_arn="taskDefinitionArn",
            
                        # the properties below are optional
                        capacity_provider_strategy=[events.CfnRule.CapacityProviderStrategyItemProperty(
                            capacity_provider="capacityProvider",
            
                            # the properties below are optional
                            base=123,
                            weight=123
                        )],
                        enable_ecs_managed_tags=False,
                        enable_execute_command=False,
                        group="group",
                        launch_type="launchType",
                        network_configuration=events.CfnRule.NetworkConfigurationProperty(
                            aws_vpc_configuration=events.CfnRule.AwsVpcConfigurationProperty(
                                subnets=["subnets"],
            
                                # the properties below are optional
                                assign_public_ip="assignPublicIp",
                                security_groups=["securityGroups"]
                            )
                        ),
                        placement_constraints=[events.CfnRule.PlacementConstraintProperty(
                            expression="expression",
                            type="type"
                        )],
                        placement_strategies=[events.CfnRule.PlacementStrategyProperty(
                            field="field",
                            type="type"
                        )],
                        platform_version="platformVersion",
                        propagate_tags="propagateTags",
                        reference_id="referenceId",
                        tag_list=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        task_count=123
                    ),
                    http_parameters=events.CfnRule.HttpParametersProperty(
                        header_parameters={
                            "header_parameters_key": "headerParameters"
                        },
                        path_parameter_values=["pathParameterValues"],
                        query_string_parameters={
                            "query_string_parameters_key": "queryStringParameters"
                        }
                    ),
                    input="input",
                    input_path="inputPath",
                    input_transformer=events.CfnRule.InputTransformerProperty(
                        input_template="inputTemplate",
            
                        # the properties below are optional
                        input_paths_map={
                            "input_paths_map_key": "inputPathsMap"
                        }
                    ),
                    kinesis_parameters=events.CfnRule.KinesisParametersProperty(
                        partition_key_path="partitionKeyPath"
                    ),
                    redshift_data_parameters=events.CfnRule.RedshiftDataParametersProperty(
                        database="database",
                        sql="sql",
            
                        # the properties below are optional
                        db_user="dbUser",
                        secret_manager_arn="secretManagerArn",
                        statement_name="statementName",
                        with_event=False
                    ),
                    retry_policy=events.CfnRule.RetryPolicyProperty(
                        maximum_event_age_in_seconds=123,
                        maximum_retry_attempts=123
                    ),
                    role_arn="roleArn",
                    run_command_parameters=events.CfnRule.RunCommandParametersProperty(
                        run_command_targets=[events.CfnRule.RunCommandTargetProperty(
                            key="key",
                            values=["values"]
                        )]
                    ),
                    sage_maker_pipeline_parameters=events.CfnRule.SageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[events.CfnRule.SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_parameters=events.CfnRule.SqsParametersProperty(
                        message_group_id="messageGroupId"
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9254c5dad1f8ed99106a5103b289e4d6c9303ae06fe351234b5033b066abe806)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_bus_name is not None:
            self._values["event_bus_name"] = event_bus_name
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression
        if state is not None:
            self._values["state"] = state
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        '''The name or ARN of the event bus associated with the rule.

        If you omit this, the default event bus is used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventbusname
        '''
        result = self._values.get("event_bus_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_pattern(self) -> typing.Any:
        '''The event pattern of the rule.

        For more information, see `Events and Event Patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html>`_ in the *Amazon EventBridge User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventpattern
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Any, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the role that is used for target invocation.

        If you're setting an event bus in another account as the target and that account granted permission to your account through an organization instead of directly by the account ID, you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure, instead of here in this parameter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        '''The scheduling expression.

        For example, "cron(0 20 * * ? *)", "rate(5 minutes)". For more information, see `Creating an Amazon EventBridge rule that runs on a schedule <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-scheduleexpression
        '''
        result = self._values.get("schedule_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRule.TargetProperty, _IResolvable_a771d0ef]]]]:
        '''Adds the specified targets to the specified rule, or updates the targets if they are already associated with the rule.

        Targets are the resources that are invoked when a rule is triggered.

        The maximum number of entries per request is 10.
        .. epigraph::

           Each rule can have up to five (5) targets associated with it at one time.

        For a list of services you can configure as targets for events, see `EventBridge targets <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html>`_ in the *Amazon EventBridge User Guide* .

        Creating rules with built-in targets is supported only in the AWS Management Console . The built-in targets are:

        - ``Amazon EBS CreateSnapshot API call``
        - ``Amazon EC2 RebootInstances API call``
        - ``Amazon EC2 StopInstances API call``
        - ``Amazon EC2 TerminateInstances API call``

        For some target types, ``PutTargets`` provides target-specific parameters. If the target is a Kinesis data stream, you can optionally specify which shard the event goes to by using the ``KinesisParameters`` argument. To invoke a command on multiple EC2 instances with one rule, you can use the ``RunCommandParameters`` field.

        To be able to make API calls against the resources that you own, Amazon EventBridge needs the appropriate permissions:

        - For AWS Lambda and Amazon SNS resources, EventBridge relies on resource-based policies.
        - For EC2 instances, Kinesis Data Streams, AWS Step Functions state machines and API Gateway APIs, EventBridge relies on IAM roles that you specify in the ``RoleARN`` argument in ``PutTargets`` .

        For more information, see `Authentication and Access Control <https://docs.aws.amazon.com/eventbridge/latest/userguide/auth-and-access-control-eventbridge.html>`_ in the *Amazon EventBridge User Guide* .

        If another AWS account is in the same region and has granted you permission (using ``PutPermission`` ), you can send events to that account. Set that account's event bus as a target of the rules in your account. To send the matched events to the other account, specify that account's event bus as the ``Arn`` value when you run ``PutTargets`` . If your account sends events to another account, your account is charged for each sent event. Each event sent to another account is charged as a custom event. The account receiving the event is not charged. For more information, see `Amazon EventBridge Pricing <https://docs.aws.amazon.com/eventbridge/pricing/>`_ .
        .. epigraph::

           ``Input`` , ``InputPath`` , and ``InputTransformer`` are not available with ``PutTarget`` if the target is an event bus of a different AWS account.

        If you are setting the event bus of another account as the target, and that account granted permission to your account through an organization instead of directly by the account ID, then you must specify a ``RoleArn`` with proper permissions in the ``Target`` structure. For more information, see `Sending and Receiving Events Between AWS Accounts <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html>`_ in the *Amazon EventBridge User Guide* .
        .. epigraph::

           If you have an IAM role on a cross-account event bus target, a ``PutTargets`` call without a role on the same target (same ``Id`` and ``Arn`` ) will not remove the role.

        For more information about enabling cross-account events, see `PutPermission <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutPermission.html>`_ .

        *Input* , *InputPath* , and *InputTransformer* are mutually exclusive and optional parameters of a target. When a rule is triggered due to a matched event:

        - If none of the following arguments are specified for a target, then the entire event is passed to the target in JSON format (unless the target is Amazon EC2 Run Command or Amazon ECS task, in which case nothing from the event is passed to the target).
        - If *Input* is specified in the form of valid JSON, then the matched event is overridden with this constant.
        - If *InputPath* is specified in the form of JSONPath (for example, ``$.detail`` ), then only the part of the event specified in the path is passed to the target (for example, only the detail part of the event is passed).
        - If *InputTransformer* is specified, then one or more specified JSONPaths are extracted from the event and used as values in a template that you specify as the input to the target.

        When you specify ``InputPath`` or ``InputTransformer`` , you must use JSON dot notation, not bracket notation.

        When you add targets to a rule and the associated rule triggers soon after, new or updated targets might not be immediately invoked. Allow a short period of time for changes to take effect.

        This action can partially fail if too many requests are made at the same time. If that happens, ``FailedEntryCount`` is non-zero in the response and each entry in ``FailedEntries`` provides the ID of the failed target and the error code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRule.TargetProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events.ConnectionAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "connection_arn": "connectionArn",
        "connection_name": "connectionName",
        "connection_secret_arn": "connectionSecretArn",
    },
)
class ConnectionAttributes:
    def __init__(
        self,
        *,
        connection_arn: builtins.str,
        connection_name: builtins.str,
        connection_secret_arn: builtins.str,
    ) -> None:
        '''(experimental) Interface with properties necessary to import a reusable Connection.

        :param connection_arn: (experimental) The ARN of the connection created.
        :param connection_name: (experimental) The Name for the connection.
        :param connection_secret_arn: (experimental) The ARN for the secret created for the connection.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            connection_attributes = events.ConnectionAttributes(
                connection_arn="connectionArn",
                connection_name="connectionName",
                connection_secret_arn="connectionSecretArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392692c5c67d06bbb12b1b4a548ee5efb057535260ed889b2a8c6814622f30c7)
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument connection_secret_arn", value=connection_secret_arn, expected_type=type_hints["connection_secret_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_arn": connection_arn,
            "connection_name": connection_name,
            "connection_secret_arn": connection_secret_arn,
        }

    @builtins.property
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the connection created.

        :stability: experimental
        '''
        result = self._values.get("connection_arn")
        assert result is not None, "Required property 'connection_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_name(self) -> builtins.str:
        '''(experimental) The Name for the connection.

        :stability: experimental
        '''
        result = self._values.get("connection_name")
        assert result is not None, "Required property 'connection_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_secret_arn(self) -> builtins.str:
        '''(experimental) The ARN for the secret created for the connection.

        :stability: experimental
        '''
        result = self._values.get("connection_secret_arn")
        assert result is not None, "Required property 'connection_secret_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectionAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events.ConnectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorization": "authorization",
        "body_parameters": "bodyParameters",
        "connection_name": "connectionName",
        "description": "description",
        "header_parameters": "headerParameters",
        "query_string_parameters": "queryStringParameters",
    },
)
class ConnectionProps:
    def __init__(
        self,
        *,
        authorization: Authorization,
        body_parameters: typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]] = None,
        connection_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]] = None,
    ) -> None:
        '''(experimental) An API Destination Connection.

        A connection defines the authorization type and credentials to use for authorization with an API destination HTTP endpoint.

        :param authorization: (experimental) The authorization type for the connection.
        :param body_parameters: (experimental) Additional string parameters to add to the invocation bodies. Default: - No additional parameters
        :param connection_name: (experimental) The name of the connection. Default: - A name is automatically generated
        :param description: (experimental) The name of the connection. Default: - none
        :param header_parameters: (experimental) Additional string parameters to add to the invocation headers. Default: - No additional parameters
        :param query_string_parameters: (experimental) Additional string parameters to add to the invocation query strings. Default: - No additional parameters

        :stability: experimental
        :exampleMetadata: infused

        Example::

            connection = events.Connection(self, "Connection",
                authorization=events.Authorization.api_key("x-api-key", SecretValue.secrets_manager("ApiSecretName")),
                description="Connection with API Key x-api-key"
            )
            
            destination = events.ApiDestination(self, "Destination",
                connection=connection,
                endpoint="https://example.com",
                description="Calling example.com with API key x-api-key"
            )
            
            rule = events.Rule(self, "Rule",
                schedule=events.Schedule.rate(cdk.Duration.minutes(1)),
                targets=[targets.ApiDestination(destination)]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302aff7122d3d8d2d199aeeef52ca29a669d063bc0af6bfc6ef0c0dd3e00cbfb)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument body_parameters", value=body_parameters, expected_type=type_hints["body_parameters"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization": authorization,
        }
        if body_parameters is not None:
            self._values["body_parameters"] = body_parameters
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if description is not None:
            self._values["description"] = description
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters

    @builtins.property
    def authorization(self) -> Authorization:
        '''(experimental) The authorization type for the connection.

        :stability: experimental
        '''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(Authorization, result)

    @builtins.property
    def body_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]]:
        '''(experimental) Additional string parameters to add to the invocation bodies.

        :default: - No additional parameters

        :stability: experimental
        '''
        result = self._values.get("body_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the connection.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the connection.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]]:
        '''(experimental) Additional string parameters to add to the invocation headers.

        :default: - No additional parameters

        :stability: experimental
        '''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]]:
        '''(experimental) Additional string parameters to add to the invocation query strings.

        :default: - No additional parameters

        :stability: experimental
        '''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "HttpParameter"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events.CronOptions",
    jsii_struct_bases=[],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "week_day": "weekDay",
        "year": "year",
    },
)
class CronOptions:
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to configure a cron expression.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate.

        :param day: (experimental) The day of the month to run this rule at. Default: - Every day of the month
        :param hour: (experimental) The hour to run this rule at. Default: - Every hour
        :param minute: (experimental) The minute to run this rule at. Default: - Every minute
        :param month: (experimental) The month to run this rule at. Default: - Every month
        :param week_day: (experimental) The day of the week to run this rule at. Default: - Any day of the week
        :param year: (experimental) The year to run this rule at. Default: - Every year

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions
        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as events
            import monocdk as targets
            
            # fn: lambda.Function
            
            rule = events.Rule(self, "Schedule Rule",
                schedule=events.Schedule.cron(minute="0", hour="4")
            )
            rule.add_target(targets.LambdaFunction(fn))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd68a9be40601e8aa102c5153d55a2756229b53ab96b6b4e409fd05c400cd80f)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument week_day", value=week_day, expected_type=type_hints["week_day"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if month is not None:
            self._values["month"] = month
        if week_day is not None:
            self._values["week_day"] = week_day
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''(experimental) The day of the month to run this rule at.

        :default: - Every day of the month

        :stability: experimental
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hour to run this rule at.

        :default: - Every hour

        :stability: experimental
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        '''(experimental) The minute to run this rule at.

        :default: - Every minute

        :stability: experimental
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def month(self) -> typing.Optional[builtins.str]:
        '''(experimental) The month to run this rule at.

        :default: - Every month

        :stability: experimental
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_day(self) -> typing.Optional[builtins.str]:
        '''(experimental) The day of the week to run this rule at.

        :default: - Any day of the week

        :stability: experimental
        '''
        result = self._values.get("week_day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def year(self) -> typing.Optional[builtins.str]:
        '''(experimental) The year to run this rule at.

        :default: - Every year

        :stability: experimental
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events.EventBusAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus_arn": "eventBusArn",
        "event_bus_name": "eventBusName",
        "event_bus_policy": "eventBusPolicy",
        "event_source_name": "eventSourceName",
    },
)
class EventBusAttributes:
    def __init__(
        self,
        *,
        event_bus_arn: builtins.str,
        event_bus_name: builtins.str,
        event_bus_policy: builtins.str,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Interface with properties necessary to import a reusable EventBus.

        :param event_bus_arn: (experimental) The ARN of this event bus resource.
        :param event_bus_name: (experimental) The physical ID of this event bus resource.
        :param event_bus_policy: (experimental) The JSON policy of this event bus resource.
        :param event_source_name: (experimental) The partner event source to associate with this event bus resource. Default: - no partner event source

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            event_bus_attributes = events.EventBusAttributes(
                event_bus_arn="eventBusArn",
                event_bus_name="eventBusName",
                event_bus_policy="eventBusPolicy",
            
                # the properties below are optional
                event_source_name="eventSourceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933d9a0a685cc982575bbdc9a4eae209d357ef36f66ff735622b60c9355d443c)
            check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
            check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
            check_type(argname="argument event_bus_policy", value=event_bus_policy, expected_type=type_hints["event_bus_policy"])
            check_type(argname="argument event_source_name", value=event_source_name, expected_type=type_hints["event_source_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_bus_arn": event_bus_arn,
            "event_bus_name": event_bus_name,
            "event_bus_policy": event_bus_policy,
        }
        if event_source_name is not None:
            self._values["event_source_name"] = event_source_name

    @builtins.property
    def event_bus_arn(self) -> builtins.str:
        '''(experimental) The ARN of this event bus resource.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        '''
        result = self._values.get("event_bus_arn")
        assert result is not None, "Required property 'event_bus_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_bus_name(self) -> builtins.str:
        '''(experimental) The physical ID of this event bus resource.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        '''
        result = self._values.get("event_bus_name")
        assert result is not None, "Required property 'event_bus_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_bus_policy(self) -> builtins.str:
        '''(experimental) The JSON policy of this event bus resource.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        '''
        result = self._values.get("event_bus_policy")
        assert result is not None, "Required property 'event_bus_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The partner event source to associate with this event bus resource.

        :default: - no partner event source

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        '''
        result = self._values.get("event_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBusAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events.EventBusProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus_name": "eventBusName",
        "event_source_name": "eventSourceName",
    },
)
class EventBusProps:
    def __init__(
        self,
        *,
        event_bus_name: typing.Optional[builtins.str] = None,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define an event bus.

        :param event_bus_name: (experimental) The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this. Default: - automatically generated name
        :param event_source_name: (experimental) The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this. Default: - no partner event source

        :stability: experimental
        :exampleMetadata: infused

        Example::

            bus = events.EventBus(self, "bus",
                event_bus_name="MyCustomEventBus"
            )
            
            bus.archive("MyArchive",
                archive_name="MyCustomEventBusArchive",
                description="MyCustomerEventBus Archive",
                event_pattern=events.aws_events.EventPattern(
                    account=[Stack.of(self).account]
                ),
                retention=Duration.days(365)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4bdec86dcafc59cb0aff7abecdcede1060c17aa537eee7da923b7564e6b7032)
            check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
            check_type(argname="argument event_source_name", value=event_source_name, expected_type=type_hints["event_source_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event_bus_name is not None:
            self._values["event_bus_name"] = event_bus_name
        if event_source_name is not None:
            self._values["event_source_name"] = event_source_name

    @builtins.property
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this.

        :default: - automatically generated name

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        '''
        result = self._values.get("event_bus_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this.

        :default: - no partner event source

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        '''
        result = self._values.get("event_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBusProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IResolvable_a771d0ef)
class EventField(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_events.EventField"):
    '''(experimental) Represents a field in the event pattern.

    :stability: experimental
    '''

    @jsii.member(jsii_name="fromPath")
    @builtins.classmethod
    def from_path(cls, path: builtins.str) -> builtins.str:
        '''(experimental) Extract a custom JSON path from the event.

        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa5ca9039f534a59a6c9a309f530c554622a039d09995a5c8e10f076bac4fd6)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fromPath", [path]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _ctx: _IResolveContext_e363e2cb) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _ctx: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4422c5309bb5f7115ed19ba3ccbc80a2670e56e151a8a60d23f8f7916ea8728c)
            check_type(argname="argument _ctx", value=_ctx, expected_type=type_hints["_ctx"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_ctx]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        '''(experimental) Convert the path to the field in the event pattern to JSON.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="account")
    def account(cls) -> builtins.str:
        '''(experimental) Extract the account from the event.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "account"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="detailType")
    def detail_type(cls) -> builtins.str:
        '''(experimental) Extract the detail type from the event.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "detailType"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="eventId")
    def event_id(cls) -> builtins.str:
        '''(experimental) Extract the event ID from the event.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "eventId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="region")
    def region(cls) -> builtins.str:
        '''(experimental) Extract the region from the event.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "region"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="source")
    def source(cls) -> builtins.str:
        '''(experimental) Extract the source from the event.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "source"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="time")
    def time(cls) -> builtins.str:
        '''(experimental) Extract the time from the event.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "time"))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        This may return an array with a single informational element indicating how
        to get this property populated, if it was skipped for performance reasons.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="displayHint")
    def display_hint(self) -> builtins.str:
        '''(experimental) Human readable display hint about the event pattern.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "displayHint"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) the path to a field in the event pattern.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))


@jsii.data_type(
    jsii_type="monocdk.aws_events.EventPattern",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "detail": "detail",
        "detail_type": "detailType",
        "id": "id",
        "region": "region",
        "resources": "resources",
        "source": "source",
        "time": "time",
        "version": "version",
    },
)
class EventPattern:
    def __init__(
        self,
        *,
        account: typing.Optional[typing.Sequence[builtins.str]] = None,
        detail: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        detail_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[typing.Sequence[builtins.str]] = None,
        time: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Events in Amazon CloudWatch Events are represented as JSON objects. For more information about JSON objects, see RFC 7159.

        **Important**: this class can only be used with a ``Rule`` class. In particular,
        do not use it with ``CfnRule`` class: your pattern will not be rendered
        correctly. In a ``CfnRule`` class, write the pattern as you normally would when
        directly writing CloudFormation.

        Rules use event patterns to select events and route them to targets. A
        pattern either matches an event or it doesn't. Event patterns are represented
        as JSON objects with a structure that is similar to that of events.

        It is important to remember the following about event pattern matching:

        - For a pattern to match an event, the event must contain all the field names
          listed in the pattern. The field names must appear in the event with the
          same nesting structure.
        - Other fields of the event not mentioned in the pattern are ignored;
          effectively, there is a ``"*": "*"`` wildcard for fields not mentioned.
        - The matching is exact (character-by-character), without case-folding or any
          other string normalization.
        - The values being matched follow JSON rules: Strings enclosed in quotes,
          numbers, and the unquoted keywords true, false, and null.
        - Number matching is at the string representation level. For example, 300,
          300.0, and 3.0e2 are not considered equal.

        :param account: (experimental) The 12-digit number identifying an AWS account. Default: - No filtering on account
        :param detail: (experimental) A JSON object, whose content is at the discretion of the service originating the event. Default: - No filtering on detail
        :param detail_type: (experimental) Identifies, in combination with the source field, the fields and values that appear in the detail field. Represents the "detail-type" event field. Default: - No filtering on detail type
        :param id: (experimental) A unique value is generated for every event. This can be helpful in tracing events as they move through rules to targets, and are processed. Default: - No filtering on id
        :param region: (experimental) Identifies the AWS region where the event originated. Default: - No filtering on region
        :param resources: (experimental) This JSON array contains ARNs that identify resources that are involved in the event. Inclusion of these ARNs is at the discretion of the service. For example, Amazon EC2 instance state-changes include Amazon EC2 instance ARNs, Auto Scaling events include ARNs for both instances and Auto Scaling groups, but API calls with AWS CloudTrail do not include resource ARNs. Default: - No filtering on resource
        :param source: (experimental) Identifies the service that sourced the event. All events sourced from within AWS begin with "aws." Customer-generated events can have any value here, as long as it doesn't begin with "aws." We recommend the use of Java package-name style reverse domain-name strings. To find the correct value for source for an AWS service, see the table in AWS Service Namespaces. For example, the source value for Amazon CloudFront is aws.cloudfront. Default: - No filtering on source
        :param time: (experimental) The event timestamp, which can be specified by the service originating the event. If the event spans a time interval, the service might choose to report the start time, so this value can be noticeably before the time the event is actually received. Default: - No filtering on time
        :param version: (experimental) By default, this is set to 0 (zero) in all events. Default: - No filtering on version

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as lambda_
            
            
            fn = lambda_.Function(self, "MyFunc",
                runtime=lambda_.Runtime.NODEJS_14_X,
                handler="index.handler",
                code=lambda_.Code.from_inline("exports.handler = handler.toString()")
            )
            
            rule = events.Rule(self, "rule",
                event_pattern=lambda.aws_events.EventPattern(
                    source=["aws.ec2"]
                )
            )
            
            queue = sqs.Queue(self, "Queue")
            
            rule.add_target(targets.LambdaFunction(fn,
                dead_letter_queue=queue,  # Optional: add a dead letter queue
                max_event_age=cdk.Duration.hours(2),  # Optional: set the maxEventAge retry policy
                retry_attempts=2
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf02b1f62a417ff0f9a156328fb4b9bb940c4c65146d6ec6393d991f55c8bef)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument detail", value=detail, expected_type=type_hints["detail"])
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if detail is not None:
            self._values["detail"] = detail
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if resources is not None:
            self._values["resources"] = resources
        if source is not None:
            self._values["source"] = source
        if time is not None:
            self._values["time"] = time
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def account(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The 12-digit number identifying an AWS account.

        :default: - No filtering on account

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def detail(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) A JSON object, whose content is at the discretion of the service originating the event.

        :default: - No filtering on detail

        :stability: experimental
        '''
        result = self._values.get("detail")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def detail_type(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Identifies, in combination with the source field, the fields and values that appear in the detail field.

        Represents the "detail-type" event field.

        :default: - No filtering on detail type

        :stability: experimental
        '''
        result = self._values.get("detail_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A unique value is generated for every event.

        This can be helpful in
        tracing events as they move through rules to targets, and are processed.

        :default: - No filtering on id

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Identifies the AWS region where the event originated.

        :default: - No filtering on region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) This JSON array contains ARNs that identify resources that are involved in the event.

        Inclusion of these ARNs is at the discretion of the
        service.

        For example, Amazon EC2 instance state-changes include Amazon EC2
        instance ARNs, Auto Scaling events include ARNs for both instances and
        Auto Scaling groups, but API calls with AWS CloudTrail do not include
        resource ARNs.

        :default: - No filtering on resource

        :stability: experimental
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Identifies the service that sourced the event.

        All events sourced from
        within AWS begin with "aws." Customer-generated events can have any value
        here, as long as it doesn't begin with "aws." We recommend the use of
        Java package-name style reverse domain-name strings.

        To find the correct value for source for an AWS service, see the table in
        AWS Service Namespaces. For example, the source value for Amazon
        CloudFront is aws.cloudfront.

        :default: - No filtering on source

        :see: http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces
        :stability: experimental
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def time(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The event timestamp, which can be specified by the service originating the event.

        If the event spans a time interval, the service might choose
        to report the start time, so this value can be noticeably before the time
        the event is actually received.

        :default: - No filtering on time

        :stability: experimental
        '''
        result = self._values.get("time")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) By default, this is set to 0 (zero) in all events.

        :default: - No filtering on version

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_events.HttpMethod")
class HttpMethod(enum.Enum):
    '''(experimental) Supported HTTP operations.

    :stability: experimental
    '''

    POST = "POST"
    '''(experimental) POST.

    :stability: experimental
    '''
    GET = "GET"
    '''(experimental) GET.

    :stability: experimental
    '''
    HEAD = "HEAD"
    '''(experimental) HEAD.

    :stability: experimental
    '''
    OPTIONS = "OPTIONS"
    '''(experimental) OPTIONS.

    :stability: experimental
    '''
    PUT = "PUT"
    '''(experimental) PUT.

    :stability: experimental
    '''
    PATCH = "PATCH"
    '''(experimental) PATCH.

    :stability: experimental
    '''
    DELETE = "DELETE"
    '''(experimental) DELETE.

    :stability: experimental
    '''


class HttpParameter(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_events.HttpParameter",
):
    '''(experimental) An additional HTTP parameter to send along with the OAuth request.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_events as events
        
        # secret_value: monocdk.SecretValue
        
        http_parameter = events.HttpParameter.from_secret(secret_value)
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromSecret")
    @builtins.classmethod
    def from_secret(cls, value: _SecretValue_c18506ef) -> "HttpParameter":
        '''(experimental) Make an OAuthParameter from a secret.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e9551605e727974abec1cbbade4089ca2c80a8a65e2d370681c10a17e111ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("HttpParameter", jsii.sinvoke(cls, "fromSecret", [value]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, value: builtins.str) -> "HttpParameter":
        '''(experimental) Make an OAuthParameter from a string value.

        The value is not treated as a secret.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1b55e9a0d6c7af0f0ac3704e2d4b1f9d0ba437cccb334f12fd6533ed60672a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("HttpParameter", jsii.sinvoke(cls, "fromString", [value]))


class _HttpParameterProxy(HttpParameter):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, HttpParameter).__jsii_proxy_class__ = lambda : _HttpParameterProxy


@jsii.interface(jsii_type="monocdk.aws_events.IApiDestination")
class IApiDestination(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Interface for API Destinations.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="apiDestinationArn")
    def api_destination_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Api Destination created.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="apiDestinationName")
    def api_destination_name(self) -> builtins.str:
        '''(experimental) The Name of the Api Destination created.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IApiDestinationProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Interface for API Destinations.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_events.IApiDestination"

    @builtins.property
    @jsii.member(jsii_name="apiDestinationArn")
    def api_destination_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Api Destination created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiDestinationArn"))

    @builtins.property
    @jsii.member(jsii_name="apiDestinationName")
    def api_destination_name(self) -> builtins.str:
        '''(experimental) The Name of the Api Destination created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiDestinationName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApiDestination).__jsii_proxy_class__ = lambda : _IApiDestinationProxy


@jsii.interface(jsii_type="monocdk.aws_events.IConnection")
class IConnection(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Interface for EventBus Connections.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the connection created.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''(experimental) The Name for the connection.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="connectionSecretArn")
    def connection_secret_arn(self) -> builtins.str:
        '''(experimental) The ARN for the secret created for the connection.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IConnectionProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Interface for EventBus Connections.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_events.IConnection"

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the connection created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''(experimental) The Name for the connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @builtins.property
    @jsii.member(jsii_name="connectionSecretArn")
    def connection_secret_arn(self) -> builtins.str:
        '''(experimental) The ARN for the secret created for the connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionSecretArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConnection).__jsii_proxy_class__ = lambda : _IConnectionProxy


@jsii.interface(jsii_type="monocdk.aws_events.IEventBus")
class IEventBus(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Interface which all EventBus based classes MUST implement.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        '''(experimental) The ARN of this event bus resource.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> builtins.str:
        '''(experimental) The physical ID of this event bus resource.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> builtins.str:
        '''(experimental) The JSON policy of this event bus resource.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The partner event source to associate with this event bus resource.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        '''
        ...

    @jsii.member(jsii_name="archive")
    def archive(
        self,
        id: builtins.str,
        *,
        event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
        archive_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_Duration_070aa057] = None,
    ) -> Archive:
        '''(experimental) Create an EventBridge archive to send events to.

        When you create an archive, incoming events might not immediately start being sent to the archive.
        Allow a short period of time for changes to take effect.

        :param id: -
        :param event_pattern: (experimental) An event pattern to use to filter events sent to the archive.
        :param archive_name: (experimental) The name of the archive. Default: - Automatically generated
        :param description: (experimental) A description for the archive. Default: - none
        :param retention: (experimental) The number of days to retain events for. Default value is 0. If set to 0, events are retained indefinitely. Default: - Infinite

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPutEventsTo")
    def grant_put_events_to(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants an IAM Principal to send custom events to the eventBus so that they can be matched to rules.

        :param grantee: The principal (no-op if undefined).

        :stability: experimental
        '''
        ...


class _IEventBusProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Interface which all EventBus based classes MUST implement.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_events.IEventBus"

    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        '''(experimental) The ARN of this event bus resource.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventBusArn"))

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> builtins.str:
        '''(experimental) The physical ID of this event bus resource.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventBusName"))

    @builtins.property
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> builtins.str:
        '''(experimental) The JSON policy of this event bus resource.

        :stability: experimental
        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventBusPolicy"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The partner event source to associate with this event bus resource.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceName"))

    @jsii.member(jsii_name="archive")
    def archive(
        self,
        id: builtins.str,
        *,
        event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
        archive_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_Duration_070aa057] = None,
    ) -> Archive:
        '''(experimental) Create an EventBridge archive to send events to.

        When you create an archive, incoming events might not immediately start being sent to the archive.
        Allow a short period of time for changes to take effect.

        :param id: -
        :param event_pattern: (experimental) An event pattern to use to filter events sent to the archive.
        :param archive_name: (experimental) The name of the archive. Default: - Automatically generated
        :param description: (experimental) A description for the archive. Default: - none
        :param retention: (experimental) The number of days to retain events for. Default value is 0. If set to 0, events are retained indefinitely. Default: - Infinite

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67ec6534e3ef66d2ce6296408336b7b6862719fb4932d1602938eb7f185ad7a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BaseArchiveProps(
            event_pattern=event_pattern,
            archive_name=archive_name,
            description=description,
            retention=retention,
        )

        return typing.cast(Archive, jsii.invoke(self, "archive", [id, props]))

    @jsii.member(jsii_name="grantPutEventsTo")
    def grant_put_events_to(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants an IAM Principal to send custom events to the eventBus so that they can be matched to rules.

        :param grantee: The principal (no-op if undefined).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093b98c54db790fa516ec33b0f0d9984feb2d857f67a21e9da225f584b043c9a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPutEventsTo", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEventBus).__jsii_proxy_class__ = lambda : _IEventBusProxy


@jsii.interface(jsii_type="monocdk.aws_events.IRule")
class IRule(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an EventBridge Rule.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> builtins.str:
        '''(experimental) The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        '''(experimental) The name event rule.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IRuleProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an EventBridge Rule.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_events.IRule"

    @builtins.property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> builtins.str:
        '''(experimental) The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleArn"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        '''(experimental) The name event rule.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRule).__jsii_proxy_class__ = lambda : _IRuleProxy


@jsii.interface(jsii_type="monocdk.aws_events.IRuleTarget")
class IRuleTarget(typing_extensions.Protocol):
    '''(experimental) An abstract target for EventRules.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: IRule,
        id: typing.Optional[builtins.str] = None,
    ) -> "RuleTargetConfig":
        '''(experimental) Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param rule: The EventBridge Rule that would trigger this target.
        :param id: The id of the target that will be attached to the rule.

        :stability: experimental
        '''
        ...


class _IRuleTargetProxy:
    '''(experimental) An abstract target for EventRules.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_events.IRuleTarget"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: IRule,
        id: typing.Optional[builtins.str] = None,
    ) -> "RuleTargetConfig":
        '''(experimental) Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param rule: The EventBridge Rule that would trigger this target.
        :param id: The id of the target that will be attached to the rule.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e817ed6db9b626eeb6742677ca8c727bde17c76635c3381c46457bd94245337)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("RuleTargetConfig", jsii.invoke(self, "bind", [rule, id]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleTarget).__jsii_proxy_class__ = lambda : _IRuleTargetProxy


@jsii.data_type(
    jsii_type="monocdk.aws_events.OAuthAuthorizationProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_endpoint": "authorizationEndpoint",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "http_method": "httpMethod",
        "body_parameters": "bodyParameters",
        "header_parameters": "headerParameters",
        "query_string_parameters": "queryStringParameters",
    },
)
class OAuthAuthorizationProps:
    def __init__(
        self,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: _SecretValue_c18506ef,
        http_method: HttpMethod,
        body_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
    ) -> None:
        '''(experimental) Properties for ``Authorization.oauth()``.

        :param authorization_endpoint: (experimental) The URL to the authorization endpoint.
        :param client_id: (experimental) The client ID to use for OAuth authorization for the connection.
        :param client_secret: (experimental) The client secret associated with the client ID to use for OAuth authorization for the connection.
        :param http_method: (experimental) The method to use for the authorization request. (Can only choose POST, GET or PUT).
        :param body_parameters: (experimental) Additional string parameters to add to the OAuth request body. Default: - No additional parameters
        :param header_parameters: (experimental) Additional string parameters to add to the OAuth request header. Default: - No additional parameters
        :param query_string_parameters: (experimental) Additional string parameters to add to the OAuth request query string. Default: - No additional parameters

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_events as events
            
            # http_parameter: events.HttpParameter
            # secret_value: monocdk.SecretValue
            
            o_auth_authorization_props = events.OAuthAuthorizationProps(
                authorization_endpoint="authorizationEndpoint",
                client_id="clientId",
                client_secret=secret_value,
                http_method=events.HttpMethod.POST,
            
                # the properties below are optional
                body_parameters={
                    "body_parameters_key": http_parameter
                },
                header_parameters={
                    "header_parameters_key": http_parameter
                },
                query_string_parameters={
                    "query_string_parameters_key": http_parameter
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8613f5fd4f20ff9d3b36b847eac1c4db9dbf0bf3bec89429838823afc6f8b6)
            check_type(argname="argument authorization_endpoint", value=authorization_endpoint, expected_type=type_hints["authorization_endpoint"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument body_parameters", value=body_parameters, expected_type=type_hints["body_parameters"])
            check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_endpoint": authorization_endpoint,
            "client_id": client_id,
            "client_secret": client_secret,
            "http_method": http_method,
        }
        if body_parameters is not None:
            self._values["body_parameters"] = body_parameters
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters

    @builtins.property
    def authorization_endpoint(self) -> builtins.str:
        '''(experimental) The URL to the authorization endpoint.

        :stability: experimental
        '''
        result = self._values.get("authorization_endpoint")
        assert result is not None, "Required property 'authorization_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''(experimental) The client ID to use for OAuth authorization for the connection.

        :stability: experimental
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> _SecretValue_c18506ef:
        '''(experimental) The client secret associated with the client ID to use for OAuth authorization for the connection.

        :stability: experimental
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(_SecretValue_c18506ef, result)

    @builtins.property
    def http_method(self) -> HttpMethod:
        '''(experimental) The method to use for the authorization request.

        (Can only choose POST, GET or PUT).

        :stability: experimental
        '''
        result = self._values.get("http_method")
        assert result is not None, "Required property 'http_method' is missing"
        return typing.cast(HttpMethod, result)

    @builtins.property
    def body_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, HttpParameter]]:
        '''(experimental) Additional string parameters to add to the OAuth request body.

        :default: - No additional parameters

        :stability: experimental
        '''
        result = self._values.get("body_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, HttpParameter]], result)

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, HttpParameter]]:
        '''(experimental) Additional string parameters to add to the OAuth request header.

        :default: - No additional parameters

        :stability: experimental
        '''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, HttpParameter]], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, HttpParameter]]:
        '''(experimental) Additional string parameters to add to the OAuth request query string.

        :default: - No additional parameters

        :stability: experimental
        '''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, HttpParameter]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OAuthAuthorizationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events.OnEventOptions",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
    },
)
class OnEventOptions:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[IRuleTarget] = None,
    ) -> None:
        '''(experimental) Standard set of options for ``onXxx`` event handlers on construct.

        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Lambda function containing logic that evaluates compliance with the rule.
            eval_compliance_fn = lambda_.Function(self, "CustomFunction",
                code=lambda_.AssetCode.from_inline("exports.handler = (event) => console.log(event);"),
                handler="index.handler",
                runtime=lambda_.Runtime.NODEJS_14_X
            )
            
            # A custom rule that runs on configuration changes of EC2 instances
            custom_rule = config.CustomRule(self, "Custom",
                configuration_changes=True,
                lambda_function=eval_compliance_fn,
                rule_scope=config.RuleScope.from_resource(config.ResourceType.EC2_INSTANCE)
            )
            
            # A rule to detect stack drifts
            drift_rule = config.CloudFormationStackDriftDetectionCheck(self, "Drift")
            
            # Topic to which compliance notification events will be published
            compliance_topic = sns.Topic(self, "ComplianceTopic")
            
            # Send notification on compliance change events
            drift_rule.on_compliance_change("ComplianceChange",
                target=targets.SnsTopic(compliance_topic)
            )
        '''
        if isinstance(event_pattern, dict):
            event_pattern = EventPattern(**event_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45038ec4ed73b5a17cac37882dc3c6abb56f16d3199ae527c09a7e7cdc9bc49f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the rule's purpose.

        :default: - No description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_pattern(self) -> typing.Optional[EventPattern]:
        '''(experimental) Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        :stability: experimental
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[EventPattern], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[IRuleTarget]:
        '''(experimental) The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[IRuleTarget], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnEventOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRule)
class Rule(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.Rule",
):
    '''(experimental) Defines an EventBridge Rule in this stack.

    :stability: experimental
    :resource: AWS::Events::Rule
    :exampleMetadata: infused

    Example::

        import monocdk as lambda_
        
        
        fn = lambda_.Function(self, "MyFunc",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("exports.handler = handler.toString()")
        )
        
        rule = events.Rule(self, "rule",
            event_pattern=lambda.aws_events.EventPattern(
                source=["aws.ec2"]
            )
        )
        
        queue = sqs.Queue(self, "Queue")
        
        rule.add_target(targets.LambdaFunction(fn,
            dead_letter_queue=queue,  # Optional: add a dead letter queue
            max_event_age=cdk.Duration.hours(2),  # Optional: set the maxEventAge retry policy
            retry_attempts=2
        ))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[IEventBus] = None,
        event_pattern: typing.Optional[typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional["Schedule"] = None,
        targets: typing.Optional[typing.Sequence[IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description.
        :param enabled: (experimental) Indicates whether the rule is enabled. Default: true
        :param event_bus: (experimental) The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: (experimental) Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: (experimental) A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: (experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: (experimental) Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0c863d4c9662a1fa6adb04f01906949483865ecd6cb0d47709e96bb78332c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromEventRuleArn")
    @builtins.classmethod
    def from_event_rule_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        event_rule_arn: builtins.str,
    ) -> IRule:
        '''(experimental) Import an existing EventBridge Rule provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param event_rule_arn: Event Rule ARN (i.e. arn:aws:events:::rule/MyScheduledRule).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4730b0ffddce4d0a6478d2797a2842156c5c0721fc653e775b14f1fb0a79c8d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument event_rule_arn", value=event_rule_arn, expected_type=type_hints["event_rule_arn"])
        return typing.cast(IRule, jsii.sinvoke(cls, "fromEventRuleArn", [scope, id, event_rule_arn]))

    @jsii.member(jsii_name="addEventPattern")
    def add_event_pattern(
        self,
        *,
        account: typing.Optional[typing.Sequence[builtins.str]] = None,
        detail: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        detail_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[typing.Sequence[builtins.str]] = None,
        time: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Adds an event pattern filter to this rule.

        If a pattern was already specified,
        these values are merged into the existing pattern.

        For example, if the rule already contains the pattern::

           {
             "resources": [ "r1" ],
             "detail": {
               "hello": [ 1 ]
             }
           }

        And ``addEventPattern`` is called with the pattern::

           {
             "resources": [ "r2" ],
             "detail": {
               "foo": [ "bar" ]
             }
           }

        The resulting event pattern will be::

           {
             "resources": [ "r1", "r2" ],
             "detail": {
               "hello": [ 1 ],
               "foo": [ "bar" ]
             }
           }

        :param account: (experimental) The 12-digit number identifying an AWS account. Default: - No filtering on account
        :param detail: (experimental) A JSON object, whose content is at the discretion of the service originating the event. Default: - No filtering on detail
        :param detail_type: (experimental) Identifies, in combination with the source field, the fields and values that appear in the detail field. Represents the "detail-type" event field. Default: - No filtering on detail type
        :param id: (experimental) A unique value is generated for every event. This can be helpful in tracing events as they move through rules to targets, and are processed. Default: - No filtering on id
        :param region: (experimental) Identifies the AWS region where the event originated. Default: - No filtering on region
        :param resources: (experimental) This JSON array contains ARNs that identify resources that are involved in the event. Inclusion of these ARNs is at the discretion of the service. For example, Amazon EC2 instance state-changes include Amazon EC2 instance ARNs, Auto Scaling events include ARNs for both instances and Auto Scaling groups, but API calls with AWS CloudTrail do not include resource ARNs. Default: - No filtering on resource
        :param source: (experimental) Identifies the service that sourced the event. All events sourced from within AWS begin with "aws." Customer-generated events can have any value here, as long as it doesn't begin with "aws." We recommend the use of Java package-name style reverse domain-name strings. To find the correct value for source for an AWS service, see the table in AWS Service Namespaces. For example, the source value for Amazon CloudFront is aws.cloudfront. Default: - No filtering on source
        :param time: (experimental) The event timestamp, which can be specified by the service originating the event. If the event spans a time interval, the service might choose to report the start time, so this value can be noticeably before the time the event is actually received. Default: - No filtering on time
        :param version: (experimental) By default, this is set to 0 (zero) in all events. Default: - No filtering on version

        :stability: experimental
        '''
        event_pattern = EventPattern(
            account=account,
            detail=detail,
            detail_type=detail_type,
            id=id,
            region=region,
            resources=resources,
            source=source,
            time=time,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "addEventPattern", [event_pattern]))

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: typing.Optional[IRuleTarget] = None) -> None:
        '''(experimental) Adds a target to the rule. The abstract class RuleTarget can be extended to define new targets.

        No-op if target is undefined.

        :param target: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f592f3b3258f462c872d6cfdc232976ccc4b88742b3590c692104ef098f2f4e)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "addTarget", [target]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> builtins.str:
        '''(experimental) The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleArn"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        '''(experimental) The name event rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))


@jsii.data_type(
    jsii_type="monocdk.aws_events.RuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "enabled": "enabled",
        "event_bus": "eventBus",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "schedule": "schedule",
        "targets": "targets",
    },
)
class RuleProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[IEventBus] = None,
        event_pattern: typing.Optional[typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional["Schedule"] = None,
        targets: typing.Optional[typing.Sequence[IRuleTarget]] = None,
    ) -> None:
        '''(experimental) Properties for defining an EventBridge Rule.

        :param description: (experimental) A description of the rule's purpose. Default: - No description.
        :param enabled: (experimental) Indicates whether the rule is enabled. Default: true
        :param event_bus: (experimental) The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: (experimental) Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: (experimental) A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: (experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: (experimental) Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            connection = events.Connection(self, "Connection",
                authorization=events.Authorization.api_key("x-api-key", SecretValue.secrets_manager("ApiSecretName")),
                description="Connection with API Key x-api-key"
            )
            
            destination = events.ApiDestination(self, "Destination",
                connection=connection,
                endpoint="https://example.com",
                description="Calling example.com with API key x-api-key"
            )
            
            rule = events.Rule(self, "Rule",
                schedule=events.Schedule.rate(cdk.Duration.minutes(1)),
                targets=[targets.ApiDestination(destination)]
            )
        '''
        if isinstance(event_pattern, dict):
            event_pattern = EventPattern(**event_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66dc7a7b1e4cbfc50080088c2afebf17916b53ce19f2587c9dc8e68451b2b705)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if schedule is not None:
            self._values["schedule"] = schedule
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the rule's purpose.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the rule is enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_bus(self) -> typing.Optional[IEventBus]:
        '''(experimental) The event bus to associate with this rule.

        :default: - The default event bus.

        :stability: experimental
        '''
        result = self._values.get("event_bus")
        return typing.cast(typing.Optional[IEventBus], result)

    @builtins.property
    def event_pattern(self) -> typing.Optional[EventPattern]:
        '''(experimental) Describes which events EventBridge routes to the specified target.

        These routed events are matched events. For more information, see Events
        and Event Patterns in the Amazon EventBridge User Guide.

        :default: - None.

        :see:

        https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html

        You must specify this property (either via props or via
        ``addEventPattern``), the ``scheduleExpression`` property, or both. The
        method ``addEventPattern`` can be used to add filter values to the event
        pattern.
        :stability: experimental
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[EventPattern], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see Name Type.

        :stability: experimental
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        '''(experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule.

        For more information, see Schedule Expression Syntax for
        Rules in the Amazon EventBridge User Guide.

        :default: - None.

        :see:

        https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html

        You must specify this property, the ``eventPattern`` property, or both.
        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["Schedule"], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[IRuleTarget]]:
        '''(experimental) Targets to invoke when this rule matches an event.

        Input will be the full matched event. If you wish to specify custom
        target input, use ``addTarget(target[, inputOptions])``.

        :default: - No targets.

        :stability: experimental
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[IRuleTarget]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events.RuleTargetConfig",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "batch_parameters": "batchParameters",
        "dead_letter_config": "deadLetterConfig",
        "ecs_parameters": "ecsParameters",
        "http_parameters": "httpParameters",
        "id": "id",
        "input": "input",
        "kinesis_parameters": "kinesisParameters",
        "retry_policy": "retryPolicy",
        "role": "role",
        "run_command_parameters": "runCommandParameters",
        "sqs_parameters": "sqsParameters",
        "target_resource": "targetResource",
    },
)
class RuleTargetConfig:
    def __init__(
        self,
        *,
        arn: builtins.str,
        batch_parameters: typing.Optional[typing.Union[CfnRule.BatchParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_config: typing.Optional[typing.Union[CfnRule.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        ecs_parameters: typing.Optional[typing.Union[CfnRule.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        http_parameters: typing.Optional[typing.Union[CfnRule.HttpParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        input: typing.Optional["RuleTargetInput"] = None,
        kinesis_parameters: typing.Optional[typing.Union[CfnRule.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union[CfnRule.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        run_command_parameters: typing.Optional[typing.Union[CfnRule.RunCommandParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_parameters: typing.Optional[typing.Union[CfnRule.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource: typing.Optional[_IConstruct_5a0f9c5e] = None,
    ) -> None:
        '''(experimental) Properties for an event rule target.

        :param arn: (experimental) The Amazon Resource Name (ARN) of the target.
        :param batch_parameters: (experimental) Parameters used when the rule invokes Amazon AWS Batch Job/Queue. Default: no parameters set
        :param dead_letter_config: (experimental) Contains information about a dead-letter queue configuration. Default: no dead-letter queue set
        :param ecs_parameters: (experimental) The Amazon ECS task definition and task count to use, if the event target is an Amazon ECS task.
        :param http_parameters: (experimental) Contains the HTTP parameters to use when the target is a API Gateway REST endpoint or EventBridge API destination. Default: - None
        :param id: (deprecated) A unique, user-defined identifier for the target. Acceptable values include alphanumeric characters, periods (.), hyphens (-), and underscores (_). Default: - an auto-generated id
        :param input: (experimental) What input to send to the event target. Default: the entire event
        :param kinesis_parameters: (experimental) Settings that control shard assignment, when the target is a Kinesis stream. If you don't include this parameter, eventId is used as the partition key.
        :param retry_policy: (experimental) A RetryPolicy object that includes information about the retry policy settings. Default: EventBridge default retry policy
        :param role: (experimental) Role to use to invoke this event target.
        :param run_command_parameters: (experimental) Parameters used when the rule invokes Amazon EC2 Systems Manager Run Command.
        :param sqs_parameters: (experimental) Parameters used when the FIFO sqs queue is used an event target by the rule.
        :param target_resource: (experimental) The resource that is backing this target. This is the resource that will actually have some action performed on it when used as a target (for example, start a build for a CodeBuild project). We need it to determine whether the rule belongs to a different account than the target - if so, we generate a more complex setup, including an additional stack containing the EventBusPolicy. Default: the target is not backed by any resource

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_events as events
            from monocdk import aws_iam as iam
            
            # construct: monocdk.Construct
            # role: iam.Role
            # rule_target_input: events.RuleTargetInput
            
            rule_target_config = events.RuleTargetConfig(
                arn="arn",
            
                # the properties below are optional
                batch_parameters=events.CfnRule.BatchParametersProperty(
                    job_definition="jobDefinition",
                    job_name="jobName",
            
                    # the properties below are optional
                    array_properties=events.CfnRule.BatchArrayPropertiesProperty(
                        size=123
                    ),
                    retry_strategy=events.CfnRule.BatchRetryStrategyProperty(
                        attempts=123
                    )
                ),
                dead_letter_config=events.CfnRule.DeadLetterConfigProperty(
                    arn="arn"
                ),
                ecs_parameters=events.CfnRule.EcsParametersProperty(
                    task_definition_arn="taskDefinitionArn",
            
                    # the properties below are optional
                    capacity_provider_strategy=[events.CfnRule.CapacityProviderStrategyItemProperty(
                        capacity_provider="capacityProvider",
            
                        # the properties below are optional
                        base=123,
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=events.CfnRule.NetworkConfigurationProperty(
                        aws_vpc_configuration=events.CfnRule.AwsVpcConfigurationProperty(
                            subnets=["subnets"],
            
                            # the properties below are optional
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"]
                        )
                    ),
                    placement_constraints=[events.CfnRule.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategies=[events.CfnRule.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tag_list=[monocdk.CfnTag(
                        key="key",
                        value="value"
                    )],
                    task_count=123
                ),
                http_parameters=events.CfnRule.HttpParametersProperty(
                    header_parameters={
                        "header_parameters_key": "headerParameters"
                    },
                    path_parameter_values=["pathParameterValues"],
                    query_string_parameters={
                        "query_string_parameters_key": "queryStringParameters"
                    }
                ),
                id="id",
                input=rule_target_input,
                kinesis_parameters=events.CfnRule.KinesisParametersProperty(
                    partition_key_path="partitionKeyPath"
                ),
                retry_policy=events.CfnRule.RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                role=role,
                run_command_parameters=events.CfnRule.RunCommandParametersProperty(
                    run_command_targets=[events.CfnRule.RunCommandTargetProperty(
                        key="key",
                        values=["values"]
                    )]
                ),
                sqs_parameters=events.CfnRule.SqsParametersProperty(
                    message_group_id="messageGroupId"
                ),
                target_resource=construct
            )
        '''
        if isinstance(batch_parameters, dict):
            batch_parameters = CfnRule.BatchParametersProperty(**batch_parameters)
        if isinstance(dead_letter_config, dict):
            dead_letter_config = CfnRule.DeadLetterConfigProperty(**dead_letter_config)
        if isinstance(ecs_parameters, dict):
            ecs_parameters = CfnRule.EcsParametersProperty(**ecs_parameters)
        if isinstance(http_parameters, dict):
            http_parameters = CfnRule.HttpParametersProperty(**http_parameters)
        if isinstance(kinesis_parameters, dict):
            kinesis_parameters = CfnRule.KinesisParametersProperty(**kinesis_parameters)
        if isinstance(retry_policy, dict):
            retry_policy = CfnRule.RetryPolicyProperty(**retry_policy)
        if isinstance(run_command_parameters, dict):
            run_command_parameters = CfnRule.RunCommandParametersProperty(**run_command_parameters)
        if isinstance(sqs_parameters, dict):
            sqs_parameters = CfnRule.SqsParametersProperty(**sqs_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0eb8e0896a0c047dacb29b1ab5575c2b6a194f4184a3b16dc33716d0d5a0db)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument batch_parameters", value=batch_parameters, expected_type=type_hints["batch_parameters"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument ecs_parameters", value=ecs_parameters, expected_type=type_hints["ecs_parameters"])
            check_type(argname="argument http_parameters", value=http_parameters, expected_type=type_hints["http_parameters"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument kinesis_parameters", value=kinesis_parameters, expected_type=type_hints["kinesis_parameters"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument run_command_parameters", value=run_command_parameters, expected_type=type_hints["run_command_parameters"])
            check_type(argname="argument sqs_parameters", value=sqs_parameters, expected_type=type_hints["sqs_parameters"])
            check_type(argname="argument target_resource", value=target_resource, expected_type=type_hints["target_resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
        }
        if batch_parameters is not None:
            self._values["batch_parameters"] = batch_parameters
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if ecs_parameters is not None:
            self._values["ecs_parameters"] = ecs_parameters
        if http_parameters is not None:
            self._values["http_parameters"] = http_parameters
        if id is not None:
            self._values["id"] = id
        if input is not None:
            self._values["input"] = input
        if kinesis_parameters is not None:
            self._values["kinesis_parameters"] = kinesis_parameters
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if role is not None:
            self._values["role"] = role
        if run_command_parameters is not None:
            self._values["run_command_parameters"] = run_command_parameters
        if sqs_parameters is not None:
            self._values["sqs_parameters"] = sqs_parameters
        if target_resource is not None:
            self._values["target_resource"] = target_resource

    @builtins.property
    def arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the target.

        :stability: experimental
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_parameters(self) -> typing.Optional[CfnRule.BatchParametersProperty]:
        '''(experimental) Parameters used when the rule invokes Amazon AWS Batch Job/Queue.

        :default: no parameters set

        :stability: experimental
        '''
        result = self._values.get("batch_parameters")
        return typing.cast(typing.Optional[CfnRule.BatchParametersProperty], result)

    @builtins.property
    def dead_letter_config(self) -> typing.Optional[CfnRule.DeadLetterConfigProperty]:
        '''(experimental) Contains information about a dead-letter queue configuration.

        :default: no dead-letter queue set

        :stability: experimental
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional[CfnRule.DeadLetterConfigProperty], result)

    @builtins.property
    def ecs_parameters(self) -> typing.Optional[CfnRule.EcsParametersProperty]:
        '''(experimental) The Amazon ECS task definition and task count to use, if the event target is an Amazon ECS task.

        :stability: experimental
        '''
        result = self._values.get("ecs_parameters")
        return typing.cast(typing.Optional[CfnRule.EcsParametersProperty], result)

    @builtins.property
    def http_parameters(self) -> typing.Optional[CfnRule.HttpParametersProperty]:
        '''(experimental) Contains the HTTP parameters to use when the target is a API Gateway REST endpoint or EventBridge API destination.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("http_parameters")
        return typing.cast(typing.Optional[CfnRule.HttpParametersProperty], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) A unique, user-defined identifier for the target.

        Acceptable values
        include alphanumeric characters, periods (.), hyphens (-), and
        underscores (_).

        :default: - an auto-generated id

        :deprecated: no replacement. we will always use an autogenerated id.

        :stability: deprecated
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input(self) -> typing.Optional["RuleTargetInput"]:
        '''(experimental) What input to send to the event target.

        :default: the entire event

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional["RuleTargetInput"], result)

    @builtins.property
    def kinesis_parameters(self) -> typing.Optional[CfnRule.KinesisParametersProperty]:
        '''(experimental) Settings that control shard assignment, when the target is a Kinesis stream.

        If you don't include this parameter, eventId is used as the
        partition key.

        :stability: experimental
        '''
        result = self._values.get("kinesis_parameters")
        return typing.cast(typing.Optional[CfnRule.KinesisParametersProperty], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional[CfnRule.RetryPolicyProperty]:
        '''(experimental) A RetryPolicy object that includes information about the retry policy settings.

        :default: EventBridge default retry policy

        :stability: experimental
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional[CfnRule.RetryPolicyProperty], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Role to use to invoke this event target.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def run_command_parameters(
        self,
    ) -> typing.Optional[CfnRule.RunCommandParametersProperty]:
        '''(experimental) Parameters used when the rule invokes Amazon EC2 Systems Manager Run Command.

        :stability: experimental
        '''
        result = self._values.get("run_command_parameters")
        return typing.cast(typing.Optional[CfnRule.RunCommandParametersProperty], result)

    @builtins.property
    def sqs_parameters(self) -> typing.Optional[CfnRule.SqsParametersProperty]:
        '''(experimental) Parameters used when the FIFO sqs queue is used an event target by the rule.

        :stability: experimental
        '''
        result = self._values.get("sqs_parameters")
        return typing.cast(typing.Optional[CfnRule.SqsParametersProperty], result)

    @builtins.property
    def target_resource(self) -> typing.Optional[_IConstruct_5a0f9c5e]:
        '''(experimental) The resource that is backing this target.

        This is the resource that will actually have some action performed on it when used as a target
        (for example, start a build for a CodeBuild project).
        We need it to determine whether the rule belongs to a different account than the target -
        if so, we generate a more complex setup,
        including an additional stack containing the EventBusPolicy.

        :default: the target is not backed by any resource

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html
        :stability: experimental
        '''
        result = self._values.get("target_resource")
        return typing.cast(typing.Optional[_IConstruct_5a0f9c5e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RuleTargetInput(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_events.RuleTargetInput",
):
    '''(experimental) The input to send to the event target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as iam
        import monocdk as sfn
        
        
        rule = events.Rule(self, "Rule",
            schedule=events.Schedule.rate(cdk.Duration.minutes(1))
        )
        
        dlq = sqs.Queue(self, "DeadLetterQueue")
        
        role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("events.amazonaws.com")
        )
        state_machine = sfn.StateMachine(self, "SM",
            definition=sfn.Wait(self, "Hello", time=sfn.WaitTime.duration(cdk.Duration.seconds(10)))
        )
        
        rule.add_target(targets.SfnStateMachine(state_machine,
            input=events.RuleTargetInput.from_object({"SomeParam": "SomeValue"}),
            dead_letter_queue=dlq,
            role=role
        ))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromEventPath")
    @builtins.classmethod
    def from_event_path(cls, path: builtins.str) -> "RuleTargetInput":
        '''(experimental) Take the event target input from a path in the event JSON.

        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a24c7b828e6e33d038289fe7ecebaa41dc425e9293c13700a03186115e0036a)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("RuleTargetInput", jsii.sinvoke(cls, "fromEventPath", [path]))

    @jsii.member(jsii_name="fromMultilineText")
    @builtins.classmethod
    def from_multiline_text(cls, text: builtins.str) -> "RuleTargetInput":
        '''(experimental) Pass text to the event target, splitting on newlines.

        This is only useful when passing to a target that does not
        take a single argument.

        May contain strings returned by ``EventField.from()`` to substitute in parts
        of the matched event.

        :param text: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6283a42e540075b8fd3ad0fa5b988a2bba75dedecdfbdb687bf13e30b945bd77)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        return typing.cast("RuleTargetInput", jsii.sinvoke(cls, "fromMultilineText", [text]))

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, obj: typing.Any) -> "RuleTargetInput":
        '''(experimental) Pass a JSON object to the event target.

        May contain strings returned by ``EventField.from()`` to substitute in parts of the
        matched event.

        :param obj: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d708333f0009ee86d8befeb8aea855512ab3209b568fb28bb350331a91dbdc)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast("RuleTargetInput", jsii.sinvoke(cls, "fromObject", [obj]))

    @jsii.member(jsii_name="fromText")
    @builtins.classmethod
    def from_text(cls, text: builtins.str) -> "RuleTargetInput":
        '''(experimental) Pass text to the event target.

        May contain strings returned by ``EventField.from()`` to substitute in parts of the
        matched event.

        The Rule Target input value will be a single string: the string you pass
        here.  Do not use this method to pass a complex value like a JSON object to
        a Rule Target.  Use ``RuleTargetInput.fromObject()`` instead.

        :param text: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78802f8bb6490efe24606e4f1c05c5833de9437b78626567d3ad4c0c02ad144)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        return typing.cast("RuleTargetInput", jsii.sinvoke(cls, "fromText", [text]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, rule: IRule) -> "RuleTargetInputProperties":
        '''(experimental) Return the input properties for this input object.

        :param rule: -

        :stability: experimental
        '''
        ...


class _RuleTargetInputProxy(RuleTargetInput):
    @jsii.member(jsii_name="bind")
    def bind(self, rule: IRule) -> "RuleTargetInputProperties":
        '''(experimental) Return the input properties for this input object.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4e6f72acf9bdb866c8952421df65acde43dc73b07173b5181f00aa9dad0340)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast("RuleTargetInputProperties", jsii.invoke(self, "bind", [rule]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, RuleTargetInput).__jsii_proxy_class__ = lambda : _RuleTargetInputProxy


@jsii.data_type(
    jsii_type="monocdk.aws_events.RuleTargetInputProperties",
    jsii_struct_bases=[],
    name_mapping={
        "input": "input",
        "input_path": "inputPath",
        "input_paths_map": "inputPathsMap",
        "input_template": "inputTemplate",
    },
)
class RuleTargetInputProperties:
    def __init__(
        self,
        *,
        input: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        input_paths_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        input_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The input properties for an event target.

        :param input: (experimental) Literal input to the target service (must be valid JSON). Default: - input for the event target. If the input contains a paths map values wil be extracted from event and inserted into the ``inputTemplate``.
        :param input_path: (experimental) JsonPath to take input from the input event. Default: - None. The entire matched event is passed as input
        :param input_paths_map: (experimental) Paths map to extract values from event and insert into ``inputTemplate``. Default: - No values extracted from event.
        :param input_template: (experimental) Input template to insert paths map into. Default: - None.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_events as events
            
            rule_target_input_properties = events.RuleTargetInputProperties(
                input="input",
                input_path="inputPath",
                input_paths_map={
                    "input_paths_map_key": "inputPathsMap"
                },
                input_template="inputTemplate"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f092b95903ab0d3411285075977809ad67d062406a2b6ea2576eac014917fa54)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            check_type(argname="argument input_paths_map", value=input_paths_map, expected_type=type_hints["input_paths_map"])
            check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input is not None:
            self._values["input"] = input
        if input_path is not None:
            self._values["input_path"] = input_path
        if input_paths_map is not None:
            self._values["input_paths_map"] = input_paths_map
        if input_template is not None:
            self._values["input_template"] = input_template

    @builtins.property
    def input(self) -> typing.Optional[builtins.str]:
        '''(experimental) Literal input to the target service (must be valid JSON).

        :default:

        - input for the event target. If the input contains a paths map
        values wil be extracted from event and inserted into the ``inputTemplate``.

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JsonPath to take input from the input event.

        :default: - None. The entire matched event is passed as input

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_paths_map(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Paths map to extract values from event and insert into ``inputTemplate``.

        :default: - No values extracted from event.

        :stability: experimental
        '''
        result = self._values.get("input_paths_map")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def input_template(self) -> typing.Optional[builtins.str]:
        '''(experimental) Input template to insert paths map into.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("input_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleTargetInputProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Schedule(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_events.Schedule",
):
    '''(experimental) Schedule for scheduled event rules.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        connection = events.Connection(self, "Connection",
            authorization=events.Authorization.api_key("x-api-key", SecretValue.secrets_manager("ApiSecretName")),
            description="Connection with API Key x-api-key"
        )
        
        destination = events.ApiDestination(self, "Destination",
            connection=connection,
            endpoint="https://example.com",
            description="Calling example.com with API key x-api-key"
        )
        
        rule = events.Rule(self, "Rule",
            schedule=events.Schedule.rate(cdk.Duration.minutes(1)),
            targets=[targets.ApiDestination(destination)]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="cron")
    @builtins.classmethod
    def cron(
        cls,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
    ) -> "Schedule":
        '''(experimental) Create a schedule from a set of cron fields.

        :param day: (experimental) The day of the month to run this rule at. Default: - Every day of the month
        :param hour: (experimental) The hour to run this rule at. Default: - Every hour
        :param minute: (experimental) The minute to run this rule at. Default: - Every minute
        :param month: (experimental) The month to run this rule at. Default: - Every month
        :param week_day: (experimental) The day of the week to run this rule at. Default: - Any day of the week
        :param year: (experimental) The year to run this rule at. Default: - Every year

        :stability: experimental
        '''
        options = CronOptions(
            day=day,
            hour=hour,
            minute=minute,
            month=month,
            week_day=week_day,
            year=year,
        )

        return typing.cast("Schedule", jsii.sinvoke(cls, "cron", [options]))

    @jsii.member(jsii_name="expression")
    @builtins.classmethod
    def expression(cls, expression: builtins.str) -> "Schedule":
        '''(experimental) Construct a schedule from a literal schedule expression.

        :param expression: The expression to use. Must be in a format that EventBridge will recognize

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9f7434070b5a4e83eb4db15d8140b7eaf4e6832751c3d8aeea5cd480960a0c)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast("Schedule", jsii.sinvoke(cls, "expression", [expression]))

    @jsii.member(jsii_name="rate")
    @builtins.classmethod
    def rate(cls, duration: _Duration_070aa057) -> "Schedule":
        '''(experimental) Construct a schedule from an interval and a time unit.

        :param duration: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532ad9a3854a0c92e99c3af5abe3fc28a0e17c869350a3c948d24ddcb34081fc)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        return typing.cast("Schedule", jsii.sinvoke(cls, "rate", [duration]))

    @builtins.property
    @jsii.member(jsii_name="expressionString")
    @abc.abstractmethod
    def expression_string(self) -> builtins.str:
        '''(experimental) Retrieve the expression for this schedule.

        :stability: experimental
        '''
        ...


class _ScheduleProxy(Schedule):
    @builtins.property
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> builtins.str:
        '''(experimental) Retrieve the expression for this schedule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "expressionString"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Schedule).__jsii_proxy_class__ = lambda : _ScheduleProxy


@jsii.implements(IApiDestination)
class ApiDestination(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.ApiDestination",
):
    '''(experimental) Define an EventBridge Api Destination.

    :stability: experimental
    :resource: AWS::Events::ApiDestination
    :exampleMetadata: infused

    Example::

        connection = events.Connection(self, "Connection",
            authorization=events.Authorization.api_key("x-api-key", SecretValue.secrets_manager("ApiSecretName")),
            description="Connection with API Key x-api-key"
        )
        
        destination = events.ApiDestination(self, "Destination",
            connection=connection,
            endpoint="https://example.com",
            description="Calling example.com with API key x-api-key"
        )
        
        rule = events.Rule(self, "Rule",
            schedule=events.Schedule.rate(cdk.Duration.minutes(1)),
            targets=[targets.ApiDestination(destination)]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        connection: IConnection,
        endpoint: builtins.str,
        api_destination_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http_method: typing.Optional[HttpMethod] = None,
        rate_limit_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param connection: (experimental) The ARN of the connection to use for the API destination.
        :param endpoint: (experimental) The URL to the HTTP invocation endpoint for the API destination..
        :param api_destination_name: (experimental) The name for the API destination. Default: - A unique name will be generated
        :param description: (experimental) A description for the API destination. Default: - none
        :param http_method: (experimental) The method to use for the request to the HTTP invocation endpoint. Default: HttpMethod.POST
        :param rate_limit_per_second: (experimental) The maximum number of requests per second to send to the HTTP invocation endpoint. Default: - Not rate limited

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e679c791fbbeec5b5bb5a29795609846d029634819cca97f937e006724a68a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApiDestinationProps(
            connection=connection,
            endpoint=endpoint,
            api_destination_name=api_destination_name,
            description=description,
            http_method=http_method,
            rate_limit_per_second=rate_limit_per_second,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiDestinationArn")
    def api_destination_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Api Destination created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiDestinationArn"))

    @builtins.property
    @jsii.member(jsii_name="apiDestinationName")
    def api_destination_name(self) -> builtins.str:
        '''(experimental) The Name of the Api Destination created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiDestinationName"))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> IConnection:
        '''(experimental) The Connection to associate with Api Destination.

        :stability: experimental
        '''
        return typing.cast(IConnection, jsii.get(self, "connection"))


@jsii.data_type(
    jsii_type="monocdk.aws_events.ArchiveProps",
    jsii_struct_bases=[BaseArchiveProps],
    name_mapping={
        "event_pattern": "eventPattern",
        "archive_name": "archiveName",
        "description": "description",
        "retention": "retention",
        "source_event_bus": "sourceEventBus",
    },
)
class ArchiveProps(BaseArchiveProps):
    def __init__(
        self,
        *,
        event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
        archive_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_Duration_070aa057] = None,
        source_event_bus: IEventBus,
    ) -> None:
        '''(experimental) The event archive properties.

        :param event_pattern: (experimental) An event pattern to use to filter events sent to the archive.
        :param archive_name: (experimental) The name of the archive. Default: - Automatically generated
        :param description: (experimental) A description for the archive. Default: - none
        :param retention: (experimental) The number of days to retain events for. Default value is 0. If set to 0, events are retained indefinitely. Default: - Infinite
        :param source_event_bus: (experimental) The event source associated with the archive.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_events as events
            
            # detail: Any
            # duration: monocdk.Duration
            # event_bus: events.EventBus
            
            archive_props = events.ArchiveProps(
                event_pattern=events.EventPattern(
                    account=["account"],
                    detail={
                        "detail_key": detail
                    },
                    detail_type=["detailType"],
                    id=["id"],
                    region=["region"],
                    resources=["resources"],
                    source=["source"],
                    time=["time"],
                    version=["version"]
                ),
                source_event_bus=event_bus,
            
                # the properties below are optional
                archive_name="archiveName",
                description="description",
                retention=duration
            )
        '''
        if isinstance(event_pattern, dict):
            event_pattern = EventPattern(**event_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c89dcb9963618dd87fa18f1f55963a9f5156f5aaa3a0be401c29a2c9a7247c)
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument archive_name", value=archive_name, expected_type=type_hints["archive_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
            check_type(argname="argument source_event_bus", value=source_event_bus, expected_type=type_hints["source_event_bus"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_pattern": event_pattern,
            "source_event_bus": source_event_bus,
        }
        if archive_name is not None:
            self._values["archive_name"] = archive_name
        if description is not None:
            self._values["description"] = description
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def event_pattern(self) -> EventPattern:
        '''(experimental) An event pattern to use to filter events sent to the archive.

        :stability: experimental
        '''
        result = self._values.get("event_pattern")
        assert result is not None, "Required property 'event_pattern' is missing"
        return typing.cast(EventPattern, result)

    @builtins.property
    def archive_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the archive.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("archive_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the archive.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The number of days to retain events for.

        Default value is 0. If set to 0, events are retained indefinitely.

        :default: - Infinite

        :stability: experimental
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def source_event_bus(self) -> IEventBus:
        '''(experimental) The event source associated with the archive.

        :stability: experimental
        '''
        result = self._values.get("source_event_bus")
        assert result is not None, "Required property 'source_event_bus' is missing"
        return typing.cast(IEventBus, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArchiveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IConnection)
class Connection(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.Connection",
):
    '''(experimental) Define an EventBridge Connection.

    :stability: experimental
    :resource: AWS::Events::Connection
    :exampleMetadata: infused

    Example::

        connection = events.Connection(self, "Connection",
            authorization=events.Authorization.api_key("x-api-key", SecretValue.secrets_manager("ApiSecretName")),
            description="Connection with API Key x-api-key"
        )
        
        destination = events.ApiDestination(self, "Destination",
            connection=connection,
            endpoint="https://example.com",
            description="Calling example.com with API key x-api-key"
        )
        
        rule = events.Rule(self, "Rule",
            schedule=events.Schedule.rate(cdk.Duration.minutes(1)),
            targets=[targets.ApiDestination(destination)]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        authorization: Authorization,
        body_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
        connection_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param authorization: (experimental) The authorization type for the connection.
        :param body_parameters: (experimental) Additional string parameters to add to the invocation bodies. Default: - No additional parameters
        :param connection_name: (experimental) The name of the connection. Default: - A name is automatically generated
        :param description: (experimental) The name of the connection. Default: - none
        :param header_parameters: (experimental) Additional string parameters to add to the invocation headers. Default: - No additional parameters
        :param query_string_parameters: (experimental) Additional string parameters to add to the invocation query strings. Default: - No additional parameters

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c94be1129f5581b6aa562689ece88b1f1fe2607d57c7a779b1a8e2fd7a78d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConnectionProps(
            authorization=authorization,
            body_parameters=body_parameters,
            connection_name=connection_name,
            description=description,
            header_parameters=header_parameters,
            query_string_parameters=query_string_parameters,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromConnectionAttributes")
    @builtins.classmethod
    def from_connection_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        connection_arn: builtins.str,
        connection_name: builtins.str,
        connection_secret_arn: builtins.str,
    ) -> IConnection:
        '''(experimental) Import an existing connection resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param connection_arn: (experimental) The ARN of the connection created.
        :param connection_name: (experimental) The Name for the connection.
        :param connection_secret_arn: (experimental) The ARN for the secret created for the connection.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__695ebc40806ebfa7c2d39b4b4e2234c35f0e6e49a17120744a9311af38972b71)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ConnectionAttributes(
            connection_arn=connection_arn,
            connection_name=connection_name,
            connection_secret_arn=connection_secret_arn,
        )

        return typing.cast(IConnection, jsii.sinvoke(cls, "fromConnectionAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromEventBusArn")
    @builtins.classmethod
    def from_event_bus_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        connection_arn: builtins.str,
        connection_secret_arn: builtins.str,
    ) -> IConnection:
        '''(experimental) Import an existing connection resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param connection_arn: ARN of imported connection.
        :param connection_secret_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176d301421b76d67cf99a7984f12c6ba9baaf608ab20fb159283f7fa724e6886)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument connection_secret_arn", value=connection_secret_arn, expected_type=type_hints["connection_secret_arn"])
        return typing.cast(IConnection, jsii.sinvoke(cls, "fromEventBusArn", [scope, id, connection_arn, connection_secret_arn]))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the connection created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''(experimental) The Name for the connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @builtins.property
    @jsii.member(jsii_name="connectionSecretArn")
    def connection_secret_arn(self) -> builtins.str:
        '''(experimental) The ARN for the secret created for the connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionSecretArn"))


@jsii.implements(IEventBus)
class EventBus(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events.EventBus",
):
    '''(experimental) Define an EventBridge EventBus.

    :stability: experimental
    :resource: AWS::Events::EventBus
    :exampleMetadata: infused

    Example::

        bus = events.EventBus(self, "bus",
            event_bus_name="MyCustomEventBus"
        )
        
        bus.archive("MyArchive",
            archive_name="MyCustomEventBusArchive",
            description="MyCustomerEventBus Archive",
            event_pattern=events.aws_events.EventPattern(
                account=[Stack.of(self).account]
            ),
            retention=Duration.days(365)
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_bus_name: typing.Optional[builtins.str] = None,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_bus_name: (experimental) The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this. Default: - automatically generated name
        :param event_source_name: (experimental) The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this. Default: - no partner event source

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f55dc1baa6b4677affcb319248d25e0ba47c0c79489afdb5fccd4fa9473fbb9b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EventBusProps(
            event_bus_name=event_bus_name, event_source_name=event_source_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromEventBusArn")
    @builtins.classmethod
    def from_event_bus_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        event_bus_arn: builtins.str,
    ) -> IEventBus:
        '''(experimental) Import an existing event bus resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param event_bus_arn: ARN of imported event bus.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ecb929d47a0baaa7cfb09927ed586ccdc2300d217fa8f92c209fe7b09378617)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
        return typing.cast(IEventBus, jsii.sinvoke(cls, "fromEventBusArn", [scope, id, event_bus_arn]))

    @jsii.member(jsii_name="fromEventBusAttributes")
    @builtins.classmethod
    def from_event_bus_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_bus_arn: builtins.str,
        event_bus_name: builtins.str,
        event_bus_policy: builtins.str,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> IEventBus:
        '''(experimental) Import an existing event bus resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param event_bus_arn: (experimental) The ARN of this event bus resource.
        :param event_bus_name: (experimental) The physical ID of this event bus resource.
        :param event_bus_policy: (experimental) The JSON policy of this event bus resource.
        :param event_source_name: (experimental) The partner event source to associate with this event bus resource. Default: - no partner event source

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f99345032a6780f742a5878c4a2d8886898143a3487275ba683764cc53bad4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = EventBusAttributes(
            event_bus_arn=event_bus_arn,
            event_bus_name=event_bus_name,
            event_bus_policy=event_bus_policy,
            event_source_name=event_source_name,
        )

        return typing.cast(IEventBus, jsii.sinvoke(cls, "fromEventBusAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromEventBusName")
    @builtins.classmethod
    def from_event_bus_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        event_bus_name: builtins.str,
    ) -> IEventBus:
        '''(experimental) Import an existing event bus resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param event_bus_name: Name of imported event bus.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7dec58f42653205062f422efa5f1eeac3dac02eec49684d79718fbca475bc1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
        return typing.cast(IEventBus, jsii.sinvoke(cls, "fromEventBusName", [scope, id, event_bus_name]))

    @jsii.member(jsii_name="grantAllPutEvents")
    @builtins.classmethod
    def grant_all_put_events(cls, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Permits an IAM Principal to send custom events to EventBridge so that they can be matched to rules.

        :param grantee: The principal (no-op if undefined).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab5ee2eae8c53c790cc6a8503dda41da4714358cb06846afda19ae79beeaf68)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.sinvoke(cls, "grantAllPutEvents", [grantee]))

    @jsii.member(jsii_name="grantPutEvents")
    @builtins.classmethod
    def grant_put_events(cls, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(deprecated) Permits an IAM Principal to send custom events to EventBridge so that they can be matched to rules.

        :param grantee: The principal (no-op if undefined).

        :deprecated: use grantAllPutEvents instead

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f88ba34ea52c9d9e8151f408d56b1be8708cb3786187f0987f5d628aad2034)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.sinvoke(cls, "grantPutEvents", [grantee]))

    @jsii.member(jsii_name="archive")
    def archive(
        self,
        id: builtins.str,
        *,
        event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
        archive_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        retention: typing.Optional[_Duration_070aa057] = None,
    ) -> Archive:
        '''(experimental) Create an EventBridge archive to send events to.

        When you create an archive, incoming events might not immediately start being sent to the archive.
        Allow a short period of time for changes to take effect.

        :param id: -
        :param event_pattern: (experimental) An event pattern to use to filter events sent to the archive.
        :param archive_name: (experimental) The name of the archive. Default: - Automatically generated
        :param description: (experimental) A description for the archive. Default: - none
        :param retention: (experimental) The number of days to retain events for. Default value is 0. If set to 0, events are retained indefinitely. Default: - Infinite

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0834ad12f8e993486755de0fa9590f8cb3e2a2852942c308d2513d904e5ad35)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BaseArchiveProps(
            event_pattern=event_pattern,
            archive_name=archive_name,
            description=description,
            retention=retention,
        )

        return typing.cast(Archive, jsii.invoke(self, "archive", [id, props]))

    @jsii.member(jsii_name="grantPutEventsTo")
    def grant_put_events_to(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants an IAM Principal to send custom events to the eventBus so that they can be matched to rules.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8eed5e08283f724bbac20a2ed7be494e0961aa621c653cad7896b1e8339238)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPutEventsTo", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        '''(experimental) The ARN of the event bus, such as: arn:aws:events:us-east-2:123456789012:event-bus/aws.partner/PartnerName/acct1/repo1.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventBusArn"))

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> builtins.str:
        '''(experimental) The physical ID of this event bus resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventBusName"))

    @builtins.property
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> builtins.str:
        '''(experimental) The policy for the event bus in JSON form.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventBusPolicy"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the partner event source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceName"))


__all__ = [
    "ApiDestination",
    "ApiDestinationProps",
    "Archive",
    "ArchiveProps",
    "Authorization",
    "BaseArchiveProps",
    "CfnApiDestination",
    "CfnApiDestinationProps",
    "CfnArchive",
    "CfnArchiveProps",
    "CfnConnection",
    "CfnConnectionProps",
    "CfnEndpoint",
    "CfnEndpointProps",
    "CfnEventBus",
    "CfnEventBusPolicy",
    "CfnEventBusPolicyProps",
    "CfnEventBusProps",
    "CfnRule",
    "CfnRuleProps",
    "Connection",
    "ConnectionAttributes",
    "ConnectionProps",
    "CronOptions",
    "EventBus",
    "EventBusAttributes",
    "EventBusProps",
    "EventField",
    "EventPattern",
    "HttpMethod",
    "HttpParameter",
    "IApiDestination",
    "IConnection",
    "IEventBus",
    "IRule",
    "IRuleTarget",
    "OAuthAuthorizationProps",
    "OnEventOptions",
    "Rule",
    "RuleProps",
    "RuleTargetConfig",
    "RuleTargetInput",
    "RuleTargetInputProperties",
    "Schedule",
]

publication.publish()

def _typecheckingstub__056de4d4dfc5405f77afc31457d0430571baab1c1e5506a651947bae0b08cbec(
    *,
    connection: IConnection,
    endpoint: builtins.str,
    api_destination_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[HttpMethod] = None,
    rate_limit_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc4d139726aade8cf7cceeb4a81bd5339dcd2e866f97c5a7e51db1e6b064a5e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source_event_bus: IEventBus,
    event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
    archive_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    retention: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71b43935c8733a32c1408371563303b3fd842428bd5fc38091ada9f036a54f0(
    api_key_name: builtins.str,
    api_key_value: _SecretValue_c18506ef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f1b0ec700d9ce94251d72a9bda95b32b2a70bf56ab8a2befcc4adb79a5aab0(
    username: builtins.str,
    password: _SecretValue_c18506ef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c427c50bf93d6b7ac5b531f350c35d3b4723158f4b79129729743df72791d10(
    *,
    event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
    archive_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    retention: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414e043e35e7ff34985ad10d0117c16197dee28a3dc677edf475cacd45c2525e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    connection_arn: builtins.str,
    http_method: builtins.str,
    invocation_endpoint: builtins.str,
    description: typing.Optional[builtins.str] = None,
    invocation_rate_limit_per_second: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c283e206d7b7192c36ff64efe32f7e0528f57aa3feb3cb3cf57a6e493fed1555(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6f21401e9ff19a502dde156acd474973ef1bf49ab1462c7bb1249f5b24a6a9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09fbe49e021c773790347138d6558ab8a4a9f84aab1e903aace14addb11937ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb155200f85150bbead5876ba5d1a0310028ff41d2b9d203f4d2e7d8f445731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935406b0fc6c8042d6d7a0455bd2082e25fa24ee2beef12f5998e225f04a105e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a5a5d8d9a9ff34753b2732974cd0d0d6aed14ab50b6a39e73fbe3472c8ef14(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce9144ed475cbef1abc3d42592613905e4104f401044f1df9af068fee11184e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b8ed3846d787fdb89dd21cf23218a8d8da30ffc66f1928a73d0485ada5a073(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217318526b0830df863f9674be412e00b4c13393794f9009fc6d70c2dc810e56(
    *,
    connection_arn: builtins.str,
    http_method: builtins.str,
    invocation_endpoint: builtins.str,
    description: typing.Optional[builtins.str] = None,
    invocation_rate_limit_per_second: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899d2177eec6babc60e1a9746198a30b954eb998f5946da59a261cfe2d4ec3be(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    source_arn: builtins.str,
    archive_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Any = None,
    retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ab1d304fee7af002fa70b35d461e4a6469efe75289a7d39185dee073549900(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1eb69c1b8f93a1f4997e93578de99b8c43db1f100fe5a88bddb22a164ccb540(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e08cf07e3933c4c27f841ea5420e2cddb9ab5a2b2b2343930c9a056448e155(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b812646ea7214910843bd9d365e0f413340f8ce942a81c40413e1a06d4787dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c76082608f39f368f3a964d0dc223157177db6749767bc328c1f3e63d71a7f1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c16ab568e2a59f5edb1e4f667a8436aafa061c3431850431bf4064b2316837(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b095110a80ad767e3d670cbd4c1e9142d975daaf8555b83c6ed203472748d3a2(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ace036bf5ad1ebe4e0fc424dc1df99e530ca0048462bdcbc8973a331c37aaf(
    *,
    source_arn: builtins.str,
    archive_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Any = None,
    retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a7ca17db9837a39fffe498a415aeb3d2140262e6633705e0844a10ba8191b5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    authorization_type: builtins.str,
    auth_parameters: typing.Union[typing.Union[CfnConnection.AuthParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961a11744a95d058912609c5ab6f17ff64af8bcdc99dc31210c673aa9aed75ed(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b641eb8a7d7c7ff37b4a32e378821a789c5cd0c0445f6bf48e5abf5741fef7d1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e656176a4db421f7835ed57a5ef1bced96c1c3066e8a5f271eb1ae4007fc9462(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccddce0a389219095b5b82a1c681c7fdb0160f7dbd8bd7b5f45422beb47b32b(
    value: typing.Union[CfnConnection.AuthParametersProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab54ed9b79591eded96ea1065fa935ddf91988a5cf89d07940e4f1d789697a6f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1d4ed239ba0505cc9ca7dee1585681b3302afb26f21677c79c936238c81011(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a4472ae22623c757fc2a301322104c8c3a143767b80c16ab3ecbcdf80a8377(
    *,
    api_key_name: builtins.str,
    api_key_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93027c4d4e7c1e705f4997047909ba2ea831fdd236ba9e855a7513999f1443fa(
    *,
    api_key_auth_parameters: typing.Optional[typing.Union[typing.Union[CfnConnection.ApiKeyAuthParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    basic_auth_parameters: typing.Optional[typing.Union[typing.Union[CfnConnection.BasicAuthParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    invocation_http_parameters: typing.Optional[typing.Union[typing.Union[CfnConnection.ConnectionHttpParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    o_auth_parameters: typing.Optional[typing.Union[typing.Union[CfnConnection.OAuthParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cb02396d3f38aafa22abc29452a43619507ce54869d398b3d4d162185ce467(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8f6d995e325c0cbcb0ead49053359ed637432382566ac0c4e7c402db90ceee(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f946f08a60b24a2b7a590df62875c873425d3333f6f3a81c7f651381def9a98a(
    *,
    body_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnConnection.ParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    header_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnConnection.ParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    query_string_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnConnection.ParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea33a9104133a379688ce59075f05e62f0a4a5a265ff17c9ecbfb538924ed04(
    *,
    authorization_endpoint: builtins.str,
    client_parameters: typing.Union[typing.Union[CfnConnection.ClientParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    http_method: builtins.str,
    o_auth_http_parameters: typing.Optional[typing.Union[typing.Union[CfnConnection.ConnectionHttpParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1111de1449175e78941c91b4aa0ab29ebff934586c1a49b0e5a47ddac1582c06(
    *,
    key: builtins.str,
    value: builtins.str,
    is_value_secret: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59ef04d1a0b2e2173f9eea534a6f5dc49ca1a590c337c6d6386c3d42f282861(
    *,
    authorization_type: builtins.str,
    auth_parameters: typing.Union[typing.Union[CfnConnection.AuthParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25247b5b0c34991a5d15bf41a4b14ea46886300efd86cfac1b5b1484dfcd73bd(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    event_buses: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEndpoint.EndpointEventBusProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    routing_config: typing.Union[typing.Union[CfnEndpoint.RoutingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    replication_config: typing.Optional[typing.Union[typing.Union[CfnEndpoint.ReplicationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c834be4845536a2a12e350d679a34a5386e192b1a5c4527184d0249411f229cd(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984c0847c0d3080832af8164cfa5dd69efabb765ca14307ed69ef403c5c4b8c3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6758a5f9fd8d1dea211c67372558b9931e859df2e353d0af692cbc4cfd296644(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEndpoint.EndpointEventBusProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9318307bcdd20c75c9e20de0eede533eec20f3a200d6895e78ef9a0916224f4c(
    value: typing.Union[CfnEndpoint.RoutingConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b5180bcfa50607cc3258c9d9c01013f5d0cd419b749d147813d33405862e68(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e729931ec8ac2a40868b50093c046d47d4c33abd71aee7dd600e3f24983885(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a79a4a5d4d1126e8bd137fc4c2be238a3743d490ec5be5d1e5c17dc67fdf4a0(
    value: typing.Optional[typing.Union[CfnEndpoint.ReplicationConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa376f1e441f556b37db888437bebd8b3b93a96cd0ea85264a90989b31f34ac(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6133a78f467e67457dc52b31c7e035d5f4c333c85517656704e9ba0c2fec1b(
    *,
    event_bus_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860d62f1ccc30c6ee3e6d8611b864c1d3b67e403814bd89617c03d4a1a24dd54(
    *,
    primary: typing.Union[typing.Union[CfnEndpoint.PrimaryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    secondary: typing.Union[typing.Union[CfnEndpoint.SecondaryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e1a13885d0575e65f6499dc625173a338e3f5de8df05d7377160ac71c9398b(
    *,
    health_check: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501d73f33c980dd89449674123020419efa8415e02f641b1011474405e2eb97f(
    *,
    state: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2063734ade08c209edda87381dd4d7142af24b8f15f93f2477fbc680a438d42e(
    *,
    failover_config: typing.Union[typing.Union[CfnEndpoint.FailoverConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3901c0a08df034770c93e503d11de451464eb6589892ff8a5d4ae500c502b0dd(
    *,
    route: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0128f18d30a5ced22e4f832ac07b4d4f18fa36123d78a573689b7cff85a72b(
    *,
    event_buses: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEndpoint.EndpointEventBusProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    routing_config: typing.Union[typing.Union[CfnEndpoint.RoutingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    replication_config: typing.Optional[typing.Union[typing.Union[CfnEndpoint.ReplicationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fcd473986abb3e1db7f382f367394b7ddc4f324470e9d739272a74f15ed688(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    event_source_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnEventBus.TagEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a3557758ce7341a09ec455488601eb7c0175a4bc154af281fd0c3674444046(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632606d4ca47e2e5c7a386510dfe7102321a1bb90b7151392fb3ebf6e58a654f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a1f407f7fcca880863e3f642a7b27d94832bf8bad92709506ab0388836e64e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e823a500a06ee374ae9cf4c8cadf5386ab78ae2db71e902c77f4c9fd09fda3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df0d2dfb02c86e5f3a75616a9edc9eabe1afc148e5515a44007239397837196(
    value: typing.Optional[typing.List[CfnEventBus.TagEntryProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1baf8cf81bde9b9a61d4c8be792b9c47ad9d8aacb6d58299e24f15b36a859e(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d864fff0969fce2aa0f79099ed45f692ae632ae6a7897dbc850a5d200ffddc90(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    statement_id: builtins.str,
    action: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[typing.Union[CfnEventBusPolicy.ConditionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    event_bus_name: typing.Optional[builtins.str] = None,
    principal: typing.Optional[builtins.str] = None,
    statement: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe8a5a2f8210b1622713ca2e5980f3df4adfb201a8e0633cbb32df59637c69e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d98cf37eaac5b0a4a4291f47ba01f5559df2c89e4aa3389e105da5667f215f6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ff5a1c5f4d4a725e2af72d9c2e70ad404502db8cfa94f58f4190d938b8ac86(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71dd1e50b6c396dcfe0cbf19fa3a5ee1ce02671f91cbd354a87a1f607f1de4dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffde2a1d53991016631d644ebf2613901d3122723d4cd6c6610ec0a47a17353(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ebea21cce261aca4cce13c9a0d391553da4f94be0436893bf41a65fcaa6f04(
    value: typing.Optional[typing.Union[CfnEventBusPolicy.ConditionProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acddce35f648a5abeca4154a153a66c0f11f9973b57b792a8352fff0e40d474e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71d46e4c7070d6c93fe58a40562ab1359f0b903e8512e1723908467697a6588(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6178299fd7a930cb3e908627d7403297c4383491cc37bb8ec4137508df573f73(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca36960c34281fb096d25b28e623361e11cf6d6d268b022c613089919587b24(
    *,
    statement_id: builtins.str,
    action: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[typing.Union[CfnEventBusPolicy.ConditionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    event_bus_name: typing.Optional[builtins.str] = None,
    principal: typing.Optional[builtins.str] = None,
    statement: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd4e2bd712e858d7d5045dddfc2997d7ab569ad18e349aeea1200c2a1b26f06(
    *,
    name: builtins.str,
    event_source_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnEventBus.TagEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804ff16a8c2e9d52959f74e98242c891bca4d19b95d5a9b4fa4c684cce53c4bf(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_bus_name: typing.Optional[builtins.str] = None,
    event_pattern: typing.Any = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f32e3d8bbf036b0c7c420013747c578efd226071acedc6d1f8a7d448bb76d58(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4c931c99ee79da0f5e1c2fe839cb1d1fb38dc2504287a989d713dc1bc1c41d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4794fafa8a1aa77d92edcb41a01a0899dd2423c6a18ffbe9581fdcfe744e324b(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a947957a93a0951d6597ed29b749eb37cee8d4894acf1065f33f2f933b312eb5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f427759e09dd4e00ef1e08a727ecec4333af424ca7b33966972581e650b2f4f1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320d06d1bfe5224905da51d5af3610c49dff87aad0ebc334d350370ae3692929(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0215d2db665069944dc033f0acf5fa49beda705d5d2f0a8e4835e7fd0b92bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91af7c731fa4589c5f5e3142db9e6c98ed9d3dab523c6a714fed5c8a0e567e39(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03c4050b40187f3e685cbc69a7e06ffc5e2aa537ecf8a7cde22fb6e7fdf05e9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dded918ff607b4b070ccc5e912f7dce582132f50b25c2259507834523826d2b1(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRule.TargetProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa01ed22d9d20c5a73b73f89b398a70d1e187324fd9cced5856efc83a908528c(
    *,
    subnets: typing.Sequence[builtins.str],
    assign_public_ip: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091d4abe35c7b94428ed52b265691515c9a75fa46d71796ef3f885692a6ff6b2(
    *,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7018bf93b8179d50a84ff19b2943d7bbed031466cf4ba9d4ab2d89bf414d4b(
    *,
    job_definition: builtins.str,
    job_name: builtins.str,
    array_properties: typing.Optional[typing.Union[typing.Union[CfnRule.BatchArrayPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    retry_strategy: typing.Optional[typing.Union[typing.Union[CfnRule.BatchRetryStrategyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a2eb860a6e3d4a1d81e83b7aef3bbf8dc36dc08084f22675dd40c4348167c5(
    *,
    attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1287bc79b1604ba267b9e845cf9a5b9fde4142070e47f06ef36c1e0af8e30d29(
    *,
    capacity_provider: builtins.str,
    base: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd7e6a3242956a5cbaf1d58b39b42483f55575378a1aa578652bd194b9ab7c1(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623d781f9bf9998c35e5b8102f4f7e34e7d4379e3b922acdaa2d61aead792717(
    *,
    task_definition_arn: builtins.str,
    capacity_provider_strategy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.CapacityProviderStrategyItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    group: typing.Optional[builtins.str] = None,
    launch_type: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[typing.Union[CfnRule.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    placement_constraints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.PlacementConstraintProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    placement_strategies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.PlacementStrategyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    platform_version: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.str] = None,
    reference_id: typing.Optional[builtins.str] = None,
    tag_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    task_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e920a0b375bd58df77bb2269990dbb1f1212dd9945aea19847b196816d3db656(
    *,
    header_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bff3e9b7041e7cf3c0f2ac43ee4ea0370b51280bbe5ce24d385375fc1429c6(
    *,
    input_template: builtins.str,
    input_paths_map: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897acde325fc7d287ed36876fbcfe9b778bd20f506bca930103ed1bd5765290f(
    *,
    partition_key_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ff95c58b8fc55bd66393b857f64135abbb8c7ad11f677b319d906c4145e8a9(
    *,
    aws_vpc_configuration: typing.Optional[typing.Union[typing.Union[CfnRule.AwsVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1427aee94ae7328fb67561e3c879c2b872c2ed5f5118762c52e6dd038bd47d27(
    *,
    expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849aae0a476285f4f092aa5d1bb465b73004437e362e00295987935eb20593ae(
    *,
    field: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1155ceb4ab0be750ebc8765fef132799d68adb5dd647fe4926b6f3a789c2b4(
    *,
    database: builtins.str,
    sql: builtins.str,
    db_user: typing.Optional[builtins.str] = None,
    secret_manager_arn: typing.Optional[builtins.str] = None,
    statement_name: typing.Optional[builtins.str] = None,
    with_event: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c372d2c538d0503741123e1b047163e868b9592299e22e2a32f9bc936361a8aa(
    *,
    maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfc5fa3ac67d9f802292f1e5e7533ab584dbaa58c111af64678681c5dc77446(
    *,
    run_command_targets: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.RunCommandTargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a15cb254deee2eb1f84bf9132ad60d8297905d7ccbb36b720e57e663cdd51b(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d8d7d828e2d3e272c5ff59f66b4366f592dafd41b8240702b48097658643ff(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f090ccc1fe727c016df390010b828a998ad7131bef2472f65864e89e611b06a2(
    *,
    pipeline_parameter_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.SageMakerPipelineParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565a2dd7cd60fb9b67b2e2575515d7bf6fedf7d71f1055e523a8278fd99cf961(
    *,
    message_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60b35cdfde0ea3e8670cd6598e824ffb005c7778b95d95cd69a3a3aca6f8812(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e892f6930c9de3bae44a45977f41013f05f0c5c20431e9e0317f940d18a73a43(
    *,
    arn: builtins.str,
    id: builtins.str,
    batch_parameters: typing.Optional[typing.Union[typing.Union[CfnRule.BatchParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dead_letter_config: typing.Optional[typing.Union[typing.Union[CfnRule.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ecs_parameters: typing.Optional[typing.Union[typing.Union[CfnRule.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    http_parameters: typing.Optional[typing.Union[typing.Union[CfnRule.HttpParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
    input_transformer: typing.Optional[typing.Union[typing.Union[CfnRule.InputTransformerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_parameters: typing.Optional[typing.Union[typing.Union[CfnRule.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    redshift_data_parameters: typing.Optional[typing.Union[typing.Union[CfnRule.RedshiftDataParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    retry_policy: typing.Optional[typing.Union[typing.Union[CfnRule.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    run_command_parameters: typing.Optional[typing.Union[typing.Union[CfnRule.RunCommandParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sage_maker_pipeline_parameters: typing.Optional[typing.Union[typing.Union[CfnRule.SageMakerPipelineParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sqs_parameters: typing.Optional[typing.Union[typing.Union[CfnRule.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9254c5dad1f8ed99106a5103b289e4d6c9303ae06fe351234b5033b066abe806(
    *,
    description: typing.Optional[builtins.str] = None,
    event_bus_name: typing.Optional[builtins.str] = None,
    event_pattern: typing.Any = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392692c5c67d06bbb12b1b4a548ee5efb057535260ed889b2a8c6814622f30c7(
    *,
    connection_arn: builtins.str,
    connection_name: builtins.str,
    connection_secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302aff7122d3d8d2d199aeeef52ca29a669d063bc0af6bfc6ef0c0dd3e00cbfb(
    *,
    authorization: Authorization,
    body_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
    connection_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd68a9be40601e8aa102c5153d55a2756229b53ab96b6b4e409fd05c400cd80f(
    *,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    month: typing.Optional[builtins.str] = None,
    week_day: typing.Optional[builtins.str] = None,
    year: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933d9a0a685cc982575bbdc9a4eae209d357ef36f66ff735622b60c9355d443c(
    *,
    event_bus_arn: builtins.str,
    event_bus_name: builtins.str,
    event_bus_policy: builtins.str,
    event_source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4bdec86dcafc59cb0aff7abecdcede1060c17aa537eee7da923b7564e6b7032(
    *,
    event_bus_name: typing.Optional[builtins.str] = None,
    event_source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa5ca9039f534a59a6c9a309f530c554622a039d09995a5c8e10f076bac4fd6(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4422c5309bb5f7115ed19ba3ccbc80a2670e56e151a8a60d23f8f7916ea8728c(
    _ctx: _IResolveContext_e363e2cb,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf02b1f62a417ff0f9a156328fb4b9bb940c4c65146d6ec6393d991f55c8bef(
    *,
    account: typing.Optional[typing.Sequence[builtins.str]] = None,
    detail: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    detail_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[typing.Sequence[builtins.str]] = None,
    time: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e9551605e727974abec1cbbade4089ca2c80a8a65e2d370681c10a17e111ae(
    value: _SecretValue_c18506ef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1b55e9a0d6c7af0f0ac3704e2d4b1f9d0ba437cccb334f12fd6533ed60672a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67ec6534e3ef66d2ce6296408336b7b6862719fb4932d1602938eb7f185ad7a(
    id: builtins.str,
    *,
    event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
    archive_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    retention: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093b98c54db790fa516ec33b0f0d9984feb2d857f67a21e9da225f584b043c9a(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e817ed6db9b626eeb6742677ca8c727bde17c76635c3381c46457bd94245337(
    rule: IRule,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8613f5fd4f20ff9d3b36b847eac1c4db9dbf0bf3bec89429838823afc6f8b6(
    *,
    authorization_endpoint: builtins.str,
    client_id: builtins.str,
    client_secret: _SecretValue_c18506ef,
    http_method: HttpMethod,
    body_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45038ec4ed73b5a17cac37882dc3c6abb56f16d3199ae527c09a7e7cdc9bc49f(
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[IRuleTarget] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0c863d4c9662a1fa6adb04f01906949483865ecd6cb0d47709e96bb78332c0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[IEventBus] = None,
    event_pattern: typing.Optional[typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[Schedule] = None,
    targets: typing.Optional[typing.Sequence[IRuleTarget]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4730b0ffddce4d0a6478d2797a2842156c5c0721fc653e775b14f1fb0a79c8d9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    event_rule_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f592f3b3258f462c872d6cfdc232976ccc4b88742b3590c692104ef098f2f4e(
    target: typing.Optional[IRuleTarget] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66dc7a7b1e4cbfc50080088c2afebf17916b53ce19f2587c9dc8e68451b2b705(
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[IEventBus] = None,
    event_pattern: typing.Optional[typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[Schedule] = None,
    targets: typing.Optional[typing.Sequence[IRuleTarget]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0eb8e0896a0c047dacb29b1ab5575c2b6a194f4184a3b16dc33716d0d5a0db(
    *,
    arn: builtins.str,
    batch_parameters: typing.Optional[typing.Union[CfnRule.BatchParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_config: typing.Optional[typing.Union[CfnRule.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs_parameters: typing.Optional[typing.Union[CfnRule.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    http_parameters: typing.Optional[typing.Union[CfnRule.HttpParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    input: typing.Optional[RuleTargetInput] = None,
    kinesis_parameters: typing.Optional[typing.Union[CfnRule.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_policy: typing.Optional[typing.Union[CfnRule.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    run_command_parameters: typing.Optional[typing.Union[CfnRule.RunCommandParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_parameters: typing.Optional[typing.Union[CfnRule.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource: typing.Optional[_IConstruct_5a0f9c5e] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a24c7b828e6e33d038289fe7ecebaa41dc425e9293c13700a03186115e0036a(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6283a42e540075b8fd3ad0fa5b988a2bba75dedecdfbdb687bf13e30b945bd77(
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d708333f0009ee86d8befeb8aea855512ab3209b568fb28bb350331a91dbdc(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78802f8bb6490efe24606e4f1c05c5833de9437b78626567d3ad4c0c02ad144(
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4e6f72acf9bdb866c8952421df65acde43dc73b07173b5181f00aa9dad0340(
    rule: IRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f092b95903ab0d3411285075977809ad67d062406a2b6ea2576eac014917fa54(
    *,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
    input_paths_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    input_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9f7434070b5a4e83eb4db15d8140b7eaf4e6832751c3d8aeea5cd480960a0c(
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532ad9a3854a0c92e99c3af5abe3fc28a0e17c869350a3c948d24ddcb34081fc(
    duration: _Duration_070aa057,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e679c791fbbeec5b5bb5a29795609846d029634819cca97f937e006724a68a9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    connection: IConnection,
    endpoint: builtins.str,
    api_destination_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[HttpMethod] = None,
    rate_limit_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c89dcb9963618dd87fa18f1f55963a9f5156f5aaa3a0be401c29a2c9a7247c(
    *,
    event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
    archive_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    retention: typing.Optional[_Duration_070aa057] = None,
    source_event_bus: IEventBus,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c94be1129f5581b6aa562689ece88b1f1fe2607d57c7a779b1a8e2fd7a78d5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    authorization: Authorization,
    body_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
    connection_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, HttpParameter]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695ebc40806ebfa7c2d39b4b4e2234c35f0e6e49a17120744a9311af38972b71(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    connection_arn: builtins.str,
    connection_name: builtins.str,
    connection_secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176d301421b76d67cf99a7984f12c6ba9baaf608ab20fb159283f7fa724e6886(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    connection_arn: builtins.str,
    connection_secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55dc1baa6b4677affcb319248d25e0ba47c0c79489afdb5fccd4fa9473fbb9b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_bus_name: typing.Optional[builtins.str] = None,
    event_source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecb929d47a0baaa7cfb09927ed586ccdc2300d217fa8f92c209fe7b09378617(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    event_bus_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f99345032a6780f742a5878c4a2d8886898143a3487275ba683764cc53bad4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_bus_arn: builtins.str,
    event_bus_name: builtins.str,
    event_bus_policy: builtins.str,
    event_source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7dec58f42653205062f422efa5f1eeac3dac02eec49684d79718fbca475bc1f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    event_bus_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab5ee2eae8c53c790cc6a8503dda41da4714358cb06846afda19ae79beeaf68(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f88ba34ea52c9d9e8151f408d56b1be8708cb3786187f0987f5d628aad2034(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0834ad12f8e993486755de0fa9590f8cb3e2a2852942c308d2513d904e5ad35(
    id: builtins.str,
    *,
    event_pattern: typing.Union[EventPattern, typing.Dict[builtins.str, typing.Any]],
    archive_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    retention: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8eed5e08283f724bbac20a2ed7be494e0961aa621c653cad7896b1e8339238(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass
