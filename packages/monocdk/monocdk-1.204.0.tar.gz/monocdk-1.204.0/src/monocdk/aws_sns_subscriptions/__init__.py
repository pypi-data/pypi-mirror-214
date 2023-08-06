'''
# CDK Construct Library for Amazon Simple Notification Service Subscriptions

This library provides constructs for adding subscriptions to an Amazon SNS topic.
Subscriptions can be added by calling the `.addSubscription(...)` method on the topic.

## Subscriptions

Subscriptions can be added to the following endpoints:

* HTTPS
* Amazon SQS
* AWS Lambda
* Email
* SMS

Subscriptions to Amazon SQS and AWS Lambda can be added on topics across regions.

Create an Amazon SNS Topic to add subscriptions.

```python
my_topic = sns.Topic(self, "MyTopic")
```

### HTTPS

Add an HTTP or HTTPS Subscription to your topic:

```python
my_topic = sns.Topic(self, "MyTopic")

my_topic.add_subscription(subscriptions.UrlSubscription("https://foobar.com/"))
```

The URL being subscribed can also be [tokens](https://docs.aws.amazon.com/cdk/latest/guide/tokens.html), that resolve
to a URL during deployment. A typical use case is when the URL is passed in as a [CloudFormation
parameter](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html). The
following code defines a CloudFormation parameter and uses it in a URL subscription.

```python
my_topic = sns.Topic(self, "MyTopic")
url = CfnParameter(self, "url-param")

my_topic.add_subscription(subscriptions.UrlSubscription(url.value_as_string))
```

### Amazon SQS

Subscribe a queue to your topic:

```python
my_queue = sqs.Queue(self, "MyQueue")
my_topic = sns.Topic(self, "MyTopic")

my_topic.add_subscription(subscriptions.SqsSubscription(my_queue))
```

KMS key permissions will automatically be granted to SNS when a subscription is made to
an encrypted queue.

Note that subscriptions of queues in different accounts need to be manually confirmed by
reading the initial message from the queue and visiting the link found in it.

### AWS Lambda

Subscribe an AWS Lambda function to your topic:

```python
import monocdk as lambda_
# my_function: lambda.Function


my_topic = sns.Topic(self, "myTopic")
my_topic.add_subscription(subscriptions.LambdaSubscription(my_function))
```

### Email

Subscribe an email address to your topic:

```python
my_topic = sns.Topic(self, "MyTopic")
my_topic.add_subscription(subscriptions.EmailSubscription("foo@bar.com"))
```

The email being subscribed can also be [tokens](https://docs.aws.amazon.com/cdk/latest/guide/tokens.html), that resolve
to an email address during deployment. A typical use case is when the email address is passed in as a [CloudFormation
parameter](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html). The
following code defines a CloudFormation parameter and uses it in an email subscription.

```python
my_topic = sns.Topic(self, "Topic")
email_address = CfnParameter(self, "email-param")

my_topic.add_subscription(subscriptions.EmailSubscription(email_address.value_as_string))
```

Note that email subscriptions require confirmation by visiting the link sent to the
email address.

### SMS

Subscribe an sms number to your topic:

```python
my_topic = sns.Topic(self, "Topic")

my_topic.add_subscription(subscriptions.SmsSubscription("+15551231234"))
```

The number being subscribed can also be [tokens](https://docs.aws.amazon.com/cdk/latest/guide/tokens.html), that resolve
to a number during deployment. A typical use case is when the number is passed in as a [CloudFormation
parameter](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html). The
following code defines a CloudFormation parameter and uses it in an sms subscription.

```python
my_topic = sns.Topic(self, "Topic")
sms_number = CfnParameter(self, "sms-param")

my_topic.add_subscription(subscriptions.SmsSubscription(sms_number.value_as_string))
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

from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_sns import (
    ITopic as _ITopic_465e36b9,
    ITopicSubscription as _ITopicSubscription_2a04646f,
    SubscriptionFilter as _SubscriptionFilter_1f5c48ae,
    SubscriptionProtocol as _SubscriptionProtocol_2074d6f2,
    TopicSubscriptionConfig as _TopicSubscriptionConfig_74c52451,
)
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_ITopicSubscription_2a04646f)
class EmailSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.EmailSubscription",
):
    '''(experimental) Use an email address as a subscription target.

    Email subscriptions require confirmation.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        my_topic = sns.Topic(self, "Topic")
        email_address = CfnParameter(self, "email-param")
        
        my_topic.add_subscription(subscriptions.EmailSubscription(email_address.value_as_string))
    '''

    def __init__(
        self,
        email_address: builtins.str,
        *,
        json: typing.Optional[builtins.bool] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param email_address: -
        :param json: (experimental) Indicates if the full notification JSON should be sent to the email address or just the message text. Default: false (Message text)
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f17a1e6ae9afadd02fdde9ee572a8ff495947bfeef721683becaf17e14efec)
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
        props = EmailSubscriptionProps(
            json=json, dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(self.__class__, self, [email_address, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration for an email address to subscribe to an SNS topic.

        :param _topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c007436af2f5aa0cd396159acab7fa0a83892bc31a57cc7eecb45a54885f9d)
            check_type(argname="argument _topic", value=_topic, expected_type=type_hints["_topic"])
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [_topic]))


@jsii.implements(_ITopicSubscription_2a04646f)
class LambdaSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.LambdaSubscription",
):
    '''(experimental) Use a Lambda function as a subscription target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as lambda_
        # fn: lambda.Function
        
        
        my_topic = sns.Topic(self, "MyTopic")
        
        # Lambda should receive only message matching the following conditions on attributes:
        # color: 'red' or 'orange' or begins with 'bl'
        # size: anything but 'small' or 'medium'
        # price: between 100 and 200 or greater than 300
        # store: attribute must be present
        my_topic.add_subscription(subscriptions.LambdaSubscription(fn,
            filter_policy={
                "color": sns.SubscriptionFilter.string_filter(
                    allowlist=["red", "orange"],
                    match_prefixes=["bl"]
                ),
                "size": sns.SubscriptionFilter.string_filter(
                    denylist=["small", "medium"]
                ),
                "price": sns.SubscriptionFilter.numeric_filter(
                    between=lambda.aws_sns.BetweenCondition(start=100, stop=200),
                    greater_than=300
                ),
                "store": sns.SubscriptionFilter.exists_filter()
            }
        ))
    '''

    def __init__(
        self,
        fn: _IFunction_6e14f09e,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param fn: -
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a81bc02051a7732100f1a574e67c91dee7fbbd56ed49d3dd2bc5b709d4455d)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        props = LambdaSubscriptionProps(
            dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(self.__class__, self, [fn, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration for a Lambda function to subscribe to an SNS topic.

        :param topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0494d582c4d1514d16c7693cb8849370ee1dabe7a6312621d1a9afac3ccdf806)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [topic]))


@jsii.implements(_ITopicSubscription_2a04646f)
class SmsSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.SmsSubscription",
):
    '''(experimental) Use an sms address as a subscription target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        my_topic = sns.Topic(self, "Topic")
        
        my_topic.add_subscription(subscriptions.SmsSubscription("+15551231234"))
    '''

    def __init__(
        self,
        phone_number: builtins.str,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param phone_number: -
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67926cf05fce163ff42163cdc9bd58f87950404ab70c568a864991643af8f42b)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        props = SmsSubscriptionProps(
            dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(self.__class__, self, [phone_number, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration used to subscribe to an SNS topic.

        :param _topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939208b64522874a38a337210bd9b477710054f7542bb7a8e5277fe52df14d87)
            check_type(argname="argument _topic", value=_topic, expected_type=type_hints["_topic"])
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [_topic]))


@jsii.implements(_ITopicSubscription_2a04646f)
class SqsSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.SqsSubscription",
):
    '''(experimental) Use an SQS queue as a subscription target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # queue: sqs.Queue
        
        my_topic = sns.Topic(self, "MyTopic")
        
        my_topic.add_subscription(subscriptions.SqsSubscription(queue))
    '''

    def __init__(
        self,
        queue: _IQueue_45a01ab4,
        *,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param queue: -
        :param raw_message_delivery: (experimental) The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e4e5696f42e4e3b52079e4d46c462671195f5ebdd3b5c45da987db957eb5ba)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        props = SqsSubscriptionProps(
            raw_message_delivery=raw_message_delivery,
            dead_letter_queue=dead_letter_queue,
            filter_policy=filter_policy,
        )

        jsii.create(self.__class__, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration for an SQS queue to subscribe to an SNS topic.

        :param topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f8d63c7b8d469fc65b612f5e28cd576a4f478d96b299b4c530b82e5d16c130)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [topic]))


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.SubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class SubscriptionProps:
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''(experimental) Options to subscribing to an SNS topic.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            from monocdk import aws_sns_subscriptions as sns_subscriptions
            from monocdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            # subscription_filter: sns.SubscriptionFilter
            
            subscription_props = sns_subscriptions.SubscriptionProps(
                dead_letter_queue=queue,
                filter_policy={
                    "filter_policy_key": subscription_filter
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b604b4a989197f799d817f1c10d71e88e7fbd960e859b8c601c5d9967a80ee)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_ITopicSubscription_2a04646f)
class UrlSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.UrlSubscription",
):
    '''(experimental) Use a URL as a subscription target.

    The message will be POSTed to the given URL.

    :see: https://docs.aws.amazon.com/sns/latest/dg/sns-http-https-endpoint-as-subscriber.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        my_topic = sns.Topic(self, "MyTopic")
        
        my_topic.add_subscription(subscriptions.UrlSubscription("https://foobar.com/"))
    '''

    def __init__(
        self,
        url: builtins.str,
        *,
        protocol: typing.Optional[_SubscriptionProtocol_2074d6f2] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param url: -
        :param protocol: (experimental) The subscription's protocol. Default: - Protocol is derived from url
        :param raw_message_delivery: (experimental) The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77a522790aa2810be31ced7a8d667aa707b646272069d6c20f87f2c66956ce7)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        props = UrlSubscriptionProps(
            protocol=protocol,
            raw_message_delivery=raw_message_delivery,
            dead_letter_queue=dead_letter_queue,
            filter_policy=filter_policy,
        )

        jsii.create(self.__class__, self, [url, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration for a URL to subscribe to an SNS topic.

        :param _topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338c73ac40742be4530f43c0da88e08f520e138e8cb93d49aa24500262c56c50)
            check_type(argname="argument _topic", value=_topic, expected_type=type_hints["_topic"])
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [_topic]))


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.UrlSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "protocol": "protocol",
        "raw_message_delivery": "rawMessageDelivery",
    },
)
class UrlSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
        protocol: typing.Optional[_SubscriptionProtocol_2074d6f2] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for URL subscriptions.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param protocol: (experimental) The subscription's protocol. Default: - Protocol is derived from url
        :param raw_message_delivery: (experimental) The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            from monocdk import aws_sns_subscriptions as sns_subscriptions
            from monocdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            # subscription_filter: sns.SubscriptionFilter
            
            url_subscription_props = sns_subscriptions.UrlSubscriptionProps(
                dead_letter_queue=queue,
                filter_policy={
                    "filter_policy_key": subscription_filter
                },
                protocol=sns.SubscriptionProtocol.HTTP,
                raw_message_delivery=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b8a412c529b6399a06a393d2901ba209aa2898f2f6c4b29e55558417d5886a)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument raw_message_delivery", value=raw_message_delivery, expected_type=type_hints["raw_message_delivery"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if protocol is not None:
            self._values["protocol"] = protocol
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    @builtins.property
    def protocol(self) -> typing.Optional[_SubscriptionProtocol_2074d6f2]:
        '''(experimental) The subscription's protocol.

        :default: - Protocol is derived from url

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_SubscriptionProtocol_2074d6f2], result)

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The message to the queue is the same as it was sent to the topic.

        If false, the message will be wrapped in an SNS envelope.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UrlSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.EmailSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "json": "json",
    },
)
class EmailSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
        json: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for email subscriptions.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param json: (experimental) Indicates if the full notification JSON should be sent to the email address or just the message text. Default: false (Message text)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            from monocdk import aws_sns_subscriptions as sns_subscriptions
            from monocdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            # subscription_filter: sns.SubscriptionFilter
            
            email_subscription_props = sns_subscriptions.EmailSubscriptionProps(
                dead_letter_queue=queue,
                filter_policy={
                    "filter_policy_key": subscription_filter
                },
                json=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa6b39355e7e590216441dceddc3dde7841aeaefda5e1490cce80e41b666c67)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if json is not None:
            self._values["json"] = json

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    @builtins.property
    def json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if the full notification JSON should be sent to the email address or just the message text.

        :default: false (Message text)

        :stability: experimental
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.LambdaSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class LambdaSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''(experimental) Properties for a Lambda subscription.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as lambda_
            # fn: lambda.Function
            
            
            my_topic = sns.Topic(self, "MyTopic")
            
            # Lambda should receive only message matching the following conditions on attributes:
            # color: 'red' or 'orange' or begins with 'bl'
            # size: anything but 'small' or 'medium'
            # price: between 100 and 200 or greater than 300
            # store: attribute must be present
            my_topic.add_subscription(subscriptions.LambdaSubscription(fn,
                filter_policy={
                    "color": sns.SubscriptionFilter.string_filter(
                        allowlist=["red", "orange"],
                        match_prefixes=["bl"]
                    ),
                    "size": sns.SubscriptionFilter.string_filter(
                        denylist=["small", "medium"]
                    ),
                    "price": sns.SubscriptionFilter.numeric_filter(
                        between=lambda.aws_sns.BetweenCondition(start=100, stop=200),
                        greater_than=300
                    ),
                    "store": sns.SubscriptionFilter.exists_filter()
                }
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05a075e69aa66ee2236a1247a62bb2eb943ebef1a25b835693552c0222c1a99)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.SmsSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class SmsSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''(experimental) Options for SMS subscriptions.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            from monocdk import aws_sns_subscriptions as sns_subscriptions
            from monocdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            # subscription_filter: sns.SubscriptionFilter
            
            sms_subscription_props = sns_subscriptions.SmsSubscriptionProps(
                dead_letter_queue=queue,
                filter_policy={
                    "filter_policy_key": subscription_filter
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1be5319a0b676b29f39bd71324a3a5f9784fdc8355662d4af29f0477f4b389)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SmsSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.SqsSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
    },
)
class SqsSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for an SQS subscription.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: (experimental) The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            from monocdk import aws_sns_subscriptions as sns_subscriptions
            from monocdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            # subscription_filter: sns.SubscriptionFilter
            
            sqs_subscription_props = sns_subscriptions.SqsSubscriptionProps(
                dead_letter_queue=queue,
                filter_policy={
                    "filter_policy_key": subscription_filter
                },
                raw_message_delivery=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ad09d28198a270fde8ba717cb073ca698985478ab4504af98d71b625f83158)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
            check_type(argname="argument raw_message_delivery", value=raw_message_delivery, expected_type=type_hints["raw_message_delivery"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The message to the queue is the same as it was sent to the topic.

        If false, the message will be wrapped in an SNS envelope.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EmailSubscription",
    "EmailSubscriptionProps",
    "LambdaSubscription",
    "LambdaSubscriptionProps",
    "SmsSubscription",
    "SmsSubscriptionProps",
    "SqsSubscription",
    "SqsSubscriptionProps",
    "SubscriptionProps",
    "UrlSubscription",
    "UrlSubscriptionProps",
]

publication.publish()

def _typecheckingstub__89f17a1e6ae9afadd02fdde9ee572a8ff495947bfeef721683becaf17e14efec(
    email_address: builtins.str,
    *,
    json: typing.Optional[builtins.bool] = None,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c007436af2f5aa0cd396159acab7fa0a83892bc31a57cc7eecb45a54885f9d(
    _topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a81bc02051a7732100f1a574e67c91dee7fbbd56ed49d3dd2bc5b709d4455d(
    fn: _IFunction_6e14f09e,
    *,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0494d582c4d1514d16c7693cb8849370ee1dabe7a6312621d1a9afac3ccdf806(
    topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67926cf05fce163ff42163cdc9bd58f87950404ab70c568a864991643af8f42b(
    phone_number: builtins.str,
    *,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939208b64522874a38a337210bd9b477710054f7542bb7a8e5277fe52df14d87(
    _topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e4e5696f42e4e3b52079e4d46c462671195f5ebdd3b5c45da987db957eb5ba(
    queue: _IQueue_45a01ab4,
    *,
    raw_message_delivery: typing.Optional[builtins.bool] = None,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f8d63c7b8d469fc65b612f5e28cd576a4f478d96b299b4c530b82e5d16c130(
    topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b604b4a989197f799d817f1c10d71e88e7fbd960e859b8c601c5d9967a80ee(
    *,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77a522790aa2810be31ced7a8d667aa707b646272069d6c20f87f2c66956ce7(
    url: builtins.str,
    *,
    protocol: typing.Optional[_SubscriptionProtocol_2074d6f2] = None,
    raw_message_delivery: typing.Optional[builtins.bool] = None,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338c73ac40742be4530f43c0da88e08f520e138e8cb93d49aa24500262c56c50(
    _topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b8a412c529b6399a06a393d2901ba209aa2898f2f6c4b29e55558417d5886a(
    *,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    protocol: typing.Optional[_SubscriptionProtocol_2074d6f2] = None,
    raw_message_delivery: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa6b39355e7e590216441dceddc3dde7841aeaefda5e1490cce80e41b666c67(
    *,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    json: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05a075e69aa66ee2236a1247a62bb2eb943ebef1a25b835693552c0222c1a99(
    *,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1be5319a0b676b29f39bd71324a3a5f9784fdc8355662d4af29f0477f4b389(
    *,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ad09d28198a270fde8ba717cb073ca698985478ab4504af98d71b625f83158(
    *,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    raw_message_delivery: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
