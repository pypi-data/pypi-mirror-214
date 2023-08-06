'''
# Amazon Lambda Destinations Library

This library provides constructs for adding destinations to a Lambda function.
Destinations can be added by specifying the `onFailure` or `onSuccess` props when creating a function or alias.

## Destinations

The following destinations are supported

* Lambda function
* SQS queue - Only standard SQS queues are supported for failure destinations, FIFO queues are not supported.
* SNS topic
* EventBridge event bus

Example with a SNS topic for successful invocations:

```python
# An sns topic for successful invocations of a lambda function
import monocdk as sns


my_topic = sns.Topic(self, "Topic")

my_fn = lambda_.Function(self, "Fn",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
    # sns topic for successful invocations
    on_success=destinations.SnsDestination(my_topic)
)
```

Example with a SQS queue for unsuccessful invocations:

```python
# An sqs queue for unsuccessful invocations of a lambda function
import monocdk as sqs


dead_letter_queue = sqs.Queue(self, "DeadLetterQueue")

my_fn = lambda_.Function(self, "Fn",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_inline("// your code"),
    # sqs queue for unsuccessful invocations
    on_failure=destinations.SqsDestination(dead_letter_queue)
)
```

See also [Configuring Destinations for Asynchronous Invocation](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-async-destinations).

### Invocation record

When a lambda function is configured with a destination, an invocation record is created by the Lambda service
when the lambda function completes. The invocation record contains the details of the function, its context, and
the request and response payloads.

The following example shows the format of the invocation record for a successful invocation:

```json
{
	"version": "1.0",
	"timestamp": "2019-11-24T23:08:25.651Z",
	"requestContext": {
		"requestId": "c2a6f2ae-7dbb-4d22-8782-d0485c9877e2",
		"functionArn": "arn:aws:lambda:sa-east-1:123456789123:function:event-destinations:$LATEST",
		"condition": "Success",
		"approximateInvokeCount": 1
	},
	"requestPayload": {
		"Success": true
	},
	"responseContext": {
		"statusCode": 200,
		"executedVersion": "$LATEST"
	},
	"responsePayload": "<data returned by the function here>"
}
```

In case of failure, the record contains the reason and error object:

```json
{
  "version": "1.0",
  "timestamp": "2019-11-24T21:52:47.333Z",
  "requestContext": {
    "requestId": "8ea123e4-1db7-4aca-ad10-d9ca1234c1fd",
    "functionArn": "arn:aws:lambda:sa-east-1:123456678912:function:event-destinations:$LATEST",
    "condition": "RetriesExhausted",
    "approximateInvokeCount": 3
  },
  "requestPayload": {
    "Success": false
  },
  "responseContext": {
    "statusCode": 200,
    "executedVersion": "$LATEST",
    "functionError": "Handled"
  },
  "responsePayload": {
    "errorMessage": "Failure from event, Success = false, I am failing!",
    "errorType": "Error",
    "stackTrace": [ "exports.handler (/var/task/index.js:18:18)" ]
  }
}
```

#### Destination-specific JSON format

* For SNS/SQS (`SnsDestionation`/`SqsDestination`), the invocation record JSON is passed as the `Message` to the destination.
* For Lambda (`LambdaDestination`), the invocation record JSON is passed as the payload to the function.
* For EventBridge (`EventBridgeDestination`), the invocation record JSON is passed as the `detail` in the PutEvents call.
  The value for the event field `source` is `lambda`, and the value for the event field `detail-type`
  is either 'Lambda Function Invocation Result - Success' or 'Lambda Function Invocation Result – Failure',
  depending on whether the lambda function invocation succeeded or failed. The event field `resource`
  contains the function and destination ARNs. See [AWS Events](https://docs.aws.amazon.com/eventbridge/latest/userguide/aws-events.html)
  for the different event fields.

### Auto-extract response payload with lambda destination

The `responseOnly` option of `LambdaDestination` allows to auto-extract the response payload from the
invocation record:

```python
# Auto-extract response payload with a lambda destination
# destination_fn: lambda.Function


source_fn = lambda_.Function(self, "Source",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
    # auto-extract on success
    on_success=destinations.LambdaDestination(destination_fn,
        response_only=True
    )
)
```

In the above example, `destinationFn` will be invoked with the payload returned by `sourceFn`
(`responsePayload` in the invocation record, not the full record).

When used with `onFailure`, the destination function is invoked with the error object returned
by the source function.

Using the `responseOnly` option allows to easily chain asynchronous Lambda functions without
having to deal with data extraction in the runtime code.
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

from .. import Construct as _Construct_e78e779f
from ..aws_events import IEventBus as _IEventBus_2ca38c95
from ..aws_lambda import (
    DestinationConfig as _DestinationConfig_40b85fbc,
    DestinationOptions as _DestinationOptions_31232a3a,
    DestinationType as _DestinationType_0222745b,
    IDestination as _IDestination_7f253ff1,
    IFunction as _IFunction_6e14f09e,
)
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_IDestination_7f253ff1)
class EventBridgeDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_destinations.EventBridgeDestination",
):
    '''(experimental) Use an Event Bridge event bus as a Lambda destination.

    If no event bus is specified, the default event bus is used.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_events as events
        from monocdk import aws_lambda_destinations as lambda_destinations
        
        # event_bus: events.EventBus
        
        event_bridge_destination = lambda_destinations.EventBridgeDestination(event_bus)
    '''

    def __init__(self, event_bus: typing.Optional[_IEventBus_2ca38c95] = None) -> None:
        '''
        :param event_bus: -

        :default: - use the default event bus

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20879ee448b4fcfb1c511383c22ba67bab996ddaa2b289e6532314ed90c9000)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
        jsii.create(self.__class__, self, [event_bus])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        fn: _IFunction_6e14f09e,
        *,
        type: _DestinationType_0222745b,
    ) -> _DestinationConfig_40b85fbc:
        '''(experimental) Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: (experimental) The destination type.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1fbbe8e658d8e44f5d8518b98a5ea7f1f09d96258533283feff599d60068a7)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        _options = _DestinationOptions_31232a3a(type=type)

        return typing.cast(_DestinationConfig_40b85fbc, jsii.invoke(self, "bind", [_scope, fn, _options]))


@jsii.implements(_IDestination_7f253ff1)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_destinations.LambdaDestination",
):
    '''(experimental) Use a Lambda function as a Lambda destination.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Auto-extract response payload with a lambda destination
        # destination_fn: lambda.Function
        
        
        source_fn = lambda_.Function(self, "Source",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            # auto-extract on success
            on_success=destinations.LambdaDestination(destination_fn,
                response_only=True
            )
        )
    '''

    def __init__(
        self,
        fn: _IFunction_6e14f09e,
        *,
        response_only: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param fn: -
        :param response_only: (experimental) Whether the destination function receives only the ``responsePayload`` of the source function. When set to ``true`` and used as ``onSuccess`` destination, the destination function will be invoked with the payload returned by the source function. When set to ``true`` and used as ``onFailure`` destination, the destination function will be invoked with the error object returned by source function. See the README of this module to see a full explanation of this option. Default: false The destination function receives the full invocation record.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb014cf603941918527a35d4a7ea24127f7f95504638832941557040c3f46b1)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        options = LambdaDestinationOptions(response_only=response_only)

        jsii.create(self.__class__, self, [fn, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        fn: _IFunction_6e14f09e,
        *,
        type: _DestinationType_0222745b,
    ) -> _DestinationConfig_40b85fbc:
        '''(experimental) Returns a destination configuration.

        :param scope: -
        :param fn: -
        :param type: (experimental) The destination type.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855f841c1a99e6c40adf4d0af8c4b9051c1f73d98c248d91e01d0e976568dcd5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        options = _DestinationOptions_31232a3a(type=type)

        return typing.cast(_DestinationConfig_40b85fbc, jsii.invoke(self, "bind", [scope, fn, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_destinations.LambdaDestinationOptions",
    jsii_struct_bases=[],
    name_mapping={"response_only": "responseOnly"},
)
class LambdaDestinationOptions:
    def __init__(self, *, response_only: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options for a Lambda destination.

        :param response_only: (experimental) Whether the destination function receives only the ``responsePayload`` of the source function. When set to ``true`` and used as ``onSuccess`` destination, the destination function will be invoked with the payload returned by the source function. When set to ``true`` and used as ``onFailure`` destination, the destination function will be invoked with the error object returned by source function. See the README of this module to see a full explanation of this option. Default: false The destination function receives the full invocation record.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Auto-extract response payload with a lambda destination
            # destination_fn: lambda.Function
            
            
            source_fn = lambda_.Function(self, "Source",
                runtime=lambda_.Runtime.NODEJS_14_X,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                # auto-extract on success
                on_success=destinations.LambdaDestination(destination_fn,
                    response_only=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0737390e44bdb9d83b38dbe6609e14142ae9886ccdc4989f0a6357c4f2b5f4e6)
            check_type(argname="argument response_only", value=response_only, expected_type=type_hints["response_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if response_only is not None:
            self._values["response_only"] = response_only

    @builtins.property
    def response_only(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the destination function receives only the ``responsePayload`` of the source function.

        When set to ``true`` and used as ``onSuccess`` destination, the destination
        function will be invoked with the payload returned by the source function.

        When set to ``true`` and used as ``onFailure`` destination, the destination
        function will be invoked with the error object returned by source function.

        See the README of this module to see a full explanation of this option.

        :default: false The destination function receives the full invocation record.

        :stability: experimental
        '''
        result = self._values.get("response_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IDestination_7f253ff1)
class SnsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_destinations.SnsDestination",
):
    '''(experimental) Use a SNS topic as a Lambda destination.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # An sns topic for successful invocations of a lambda function
        import monocdk as sns
        
        
        my_topic = sns.Topic(self, "Topic")
        
        my_fn = lambda_.Function(self, "Fn",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            # sns topic for successful invocations
            on_success=destinations.SnsDestination(my_topic)
        )
    '''

    def __init__(self, topic: _ITopic_465e36b9) -> None:
        '''
        :param topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1051e7f902016253dae554e26b5ef065c453caaa0f9ddcaeaeb12060b8f38f3d)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        jsii.create(self.__class__, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        fn: _IFunction_6e14f09e,
        *,
        type: _DestinationType_0222745b,
    ) -> _DestinationConfig_40b85fbc:
        '''(experimental) Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: (experimental) The destination type.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b77622353747723549aaee5da248da3a87b3ffc8299879227cc0b7aa1c32d3)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        _options = _DestinationOptions_31232a3a(type=type)

        return typing.cast(_DestinationConfig_40b85fbc, jsii.invoke(self, "bind", [_scope, fn, _options]))


@jsii.implements(_IDestination_7f253ff1)
class SqsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_destinations.SqsDestination",
):
    '''(experimental) Use a SQS queue as a Lambda destination.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # An sqs queue for unsuccessful invocations of a lambda function
        import monocdk as sqs
        
        
        dead_letter_queue = sqs.Queue(self, "DeadLetterQueue")
        
        my_fn = lambda_.Function(self, "Fn",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("// your code"),
            # sqs queue for unsuccessful invocations
            on_failure=destinations.SqsDestination(dead_letter_queue)
        )
    '''

    def __init__(self, queue: _IQueue_45a01ab4) -> None:
        '''
        :param queue: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e103769a0934ede1d19c36ebc8e848d0f8c83f32139d9c54105e852b00f2ba)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        jsii.create(self.__class__, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        fn: _IFunction_6e14f09e,
        *,
        type: _DestinationType_0222745b,
    ) -> _DestinationConfig_40b85fbc:
        '''(experimental) Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: (experimental) The destination type.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd907c610c1ec345becd6e1804886151260cd9d7f8a21672d264557d21d3846)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        _options = _DestinationOptions_31232a3a(type=type)

        return typing.cast(_DestinationConfig_40b85fbc, jsii.invoke(self, "bind", [_scope, fn, _options]))


__all__ = [
    "EventBridgeDestination",
    "LambdaDestination",
    "LambdaDestinationOptions",
    "SnsDestination",
    "SqsDestination",
]

publication.publish()

def _typecheckingstub__f20879ee448b4fcfb1c511383c22ba67bab996ddaa2b289e6532314ed90c9000(
    event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1fbbe8e658d8e44f5d8518b98a5ea7f1f09d96258533283feff599d60068a7(
    _scope: _Construct_e78e779f,
    fn: _IFunction_6e14f09e,
    *,
    type: _DestinationType_0222745b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb014cf603941918527a35d4a7ea24127f7f95504638832941557040c3f46b1(
    fn: _IFunction_6e14f09e,
    *,
    response_only: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855f841c1a99e6c40adf4d0af8c4b9051c1f73d98c248d91e01d0e976568dcd5(
    scope: _Construct_e78e779f,
    fn: _IFunction_6e14f09e,
    *,
    type: _DestinationType_0222745b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0737390e44bdb9d83b38dbe6609e14142ae9886ccdc4989f0a6357c4f2b5f4e6(
    *,
    response_only: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1051e7f902016253dae554e26b5ef065c453caaa0f9ddcaeaeb12060b8f38f3d(
    topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b77622353747723549aaee5da248da3a87b3ffc8299879227cc0b7aa1c32d3(
    _scope: _Construct_e78e779f,
    fn: _IFunction_6e14f09e,
    *,
    type: _DestinationType_0222745b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e103769a0934ede1d19c36ebc8e848d0f8c83f32139d9c54105e852b00f2ba(
    queue: _IQueue_45a01ab4,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd907c610c1ec345becd6e1804886151260cd9d7f8a21672d264557d21d3846(
    _scope: _Construct_e78e779f,
    fn: _IFunction_6e14f09e,
    *,
    type: _DestinationType_0222745b,
) -> None:
    """Type checking stubs"""
    pass
