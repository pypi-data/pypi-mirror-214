'''
# Amazon Simple Queue Service Construct Library

Amazon Simple Queue Service (SQS) is a fully managed message queuing service that
enables you to decouple and scale microservices, distributed systems, and serverless
applications. SQS eliminates the complexity and overhead associated with managing and
operating message oriented middleware, and empowers developers to focus on differentiating work.
Using SQS, you can send, store, and receive messages between software components at any volume,
without losing messages or requiring other services to be available.

## Installation

Import to your project:

```python
import monocdk as sqs
```

## Basic usage

Here's how to add a basic queue to your application:

```python
sqs.Queue(self, "Queue")
```

## Encryption

If you want to encrypt the queue contents, set the `encryption` property. You can have
the messages encrypted with a key that SQS manages for you, or a key that you
can manage yourself.

```python
# Use managed key
sqs.Queue(self, "Queue",
    encryption=sqs.QueueEncryption.KMS_MANAGED
)

# Use custom key
my_key = kms.Key(self, "Key")

sqs.Queue(self, "Queue",
    encryption=sqs.QueueEncryption.KMS,
    encryption_master_key=my_key
)
```

## First-In-First-Out (FIFO) queues

FIFO queues give guarantees on the order in which messages are dequeued, and have additional
features in order to help guarantee exactly-once processing. For more information, see
the SQS manual. Note that FIFO queues are not available in all AWS regions.

A queue can be made a FIFO queue by either setting `fifo: true`, giving it a name which ends
in `".fifo"`, or by enabling a FIFO specific feature such as: content-based deduplication,
deduplication scope or fifo throughput limit.
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
    ResourceProps as _ResourceProps_9b554c0f,
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
    PolicyDocument as _PolicyDocument_b5de5177,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_kms import IKey as _IKey_36930160


@jsii.implements(_IInspectable_82c04a63)
class CfnQueue(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sqs.CfnQueue",
):
    '''A CloudFormation ``AWS::SQS::Queue``.

    The ``AWS::SQS::Queue`` resource creates an Amazon SQS standard or FIFO queue.

    Keep the following caveats in mind:

    - If you don't specify the ``FifoQueue`` property, Amazon SQS creates a standard queue.

    .. epigraph::

       You can't change the queue type after you create it and you can't convert an existing standard queue into a FIFO queue. You must either create a new FIFO queue for your application or delete your existing standard queue and recreate it as a FIFO queue. For more information, see `Moving from a standard queue to a FIFO queue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-moving.html>`_ in the *Amazon SQS Developer Guide* .

    - If you don't provide a value for a property, the queue is created with the default value for the property.
    - If you delete a queue, you must wait at least 60 seconds before creating a queue with the same name.
    - To successfully create a new queue, you must provide a queue name that adheres to the `limits related to queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/limits-queues.html>`_ and is unique within the scope of your queues.

    For more information about creating FIFO (first-in-first-out) queues, see `Creating an Amazon SQS queue ( AWS CloudFormation ) <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/screate-queue-cloudformation.html>`_ in the *Amazon SQS Developer Guide* .

    :cloudformationResource: AWS::SQS::Queue
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sqs as sqs
        
        # redrive_allow_policy: Any
        # redrive_policy: Any
        
        cfn_queue = sqs.CfnQueue(self, "MyCfnQueue",
            content_based_deduplication=False,
            deduplication_scope="deduplicationScope",
            delay_seconds=123,
            fifo_queue=False,
            fifo_throughput_limit="fifoThroughputLimit",
            kms_data_key_reuse_period_seconds=123,
            kms_master_key_id="kmsMasterKeyId",
            maximum_message_size=123,
            message_retention_period=123,
            queue_name="queueName",
            receive_message_wait_time_seconds=123,
            redrive_allow_policy=redrive_allow_policy,
            redrive_policy=redrive_policy,
            sqs_managed_sse_enabled=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            visibility_timeout=123
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        deduplication_scope: typing.Optional[builtins.str] = None,
        delay_seconds: typing.Optional[jsii.Number] = None,
        fifo_queue: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        fifo_throughput_limit: typing.Optional[builtins.str] = None,
        kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        maximum_message_size: typing.Optional[jsii.Number] = None,
        message_retention_period: typing.Optional[jsii.Number] = None,
        queue_name: typing.Optional[builtins.str] = None,
        receive_message_wait_time_seconds: typing.Optional[jsii.Number] = None,
        redrive_allow_policy: typing.Any = None,
        redrive_policy: typing.Any = None,
        sqs_managed_sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        visibility_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::SQS::Queue``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content_based_deduplication: For first-in-first-out (FIFO) queues, specifies whether to enable content-based deduplication. During the deduplication interval, Amazon SQS treats messages that are sent with identical content as duplicates and delivers only one copy of the message. For more information, see the ``ContentBasedDeduplication`` attribute for the ``[CreateQueue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html)`` action in the *Amazon SQS API Reference* .
        :param deduplication_scope: For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level. Valid values are ``messageGroup`` and ``queue`` . To enable high throughput for a FIFO queue, set this attribute to ``messageGroup`` *and* set the ``FifoThroughputLimit`` attribute to ``perMessageGroupId`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .
        :param delay_seconds: The time in seconds for which the delivery of all messages in the queue is delayed. You can specify an integer value of ``0`` to ``900`` (15 minutes). The default value is ``0`` .
        :param fifo_queue: If set to true, creates a FIFO queue. If you don't specify this property, Amazon SQS creates a standard queue. For more information, see `FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html>`_ in the *Amazon SQS Developer Guide* .
        :param fifo_throughput_limit: For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group. Valid values are ``perQueue`` and ``perMessageGroupId`` . To enable high throughput for a FIFO queue, set this attribute to ``perMessageGroupId`` *and* set the ``DeduplicationScope`` attribute to ``messageGroup`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .
        :param kms_data_key_reuse_period_seconds: The length of time in seconds for which Amazon SQS can reuse a data key to encrypt or decrypt messages before calling AWS KMS again. The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes). .. epigraph:: A shorter time period provides better security, but results in more calls to AWS KMS , which might incur charges after Free Tier. For more information, see `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html#sqs-how-does-the-data-key-reuse-period-work>`_ in the *Amazon SQS Developer Guide* .
        :param kms_master_key_id: The ID of an AWS Key Management Service (KMS) for Amazon SQS , or a custom KMS. To use the AWS managed KMS for Amazon SQS , specify a (default) alias ARN, alias name (e.g. ``alias/aws/sqs`` ), key ARN, or key ID. For more information, see the following: - `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html>`_ in the *Amazon SQS Developer Guide* - `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ in the *Amazon SQS API Reference* - `Request Parameters <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters>`_ in the *AWS Key Management Service API Reference* - The Key Management Service (KMS) section of the `AWS Key Management Service Best Practices <https://docs.aws.amazon.com/https://d0.awsstatic.com/whitepapers/aws-kms-best-practices.pdf>`_ whitepaper
        :param maximum_message_size: The limit of how many bytes that a message can contain before Amazon SQS rejects it. You can specify an integer value from ``1,024`` bytes (1 KiB) to ``262,144`` bytes (256 KiB). The default value is ``262,144`` (256 KiB).
        :param message_retention_period: The number of seconds that Amazon SQS retains a message. You can specify an integer value from ``60`` seconds (1 minute) to ``1,209,600`` seconds (14 days). The default value is ``345,600`` seconds (4 days).
        :param queue_name: A name for the queue. To create a FIFO queue, the name of your FIFO queue must end with the ``.fifo`` suffix. For more information, see `FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html>`_ in the *Amazon SQS Developer Guide* . If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the queue name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param receive_message_wait_time_seconds: Specifies the duration, in seconds, that the ReceiveMessage action call waits until a message is in the queue in order to include it in the response, rather than returning an empty response if a message isn't yet available. You can specify an integer from 1 to 20. Short polling is used as the default or when you specify 0 for this property. For more information, see `Consuming messages using long polling <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html#sqs-long-polling>`_ in the *Amazon SQS Developer Guide* .
        :param redrive_allow_policy: The string that includes the parameters for the permissions for the dead-letter queue redrive permission and which source queues can specify dead-letter queues as a JSON object. The parameters are as follows: - ``redrivePermission`` : The permission type that defines which source queues can specify the current queue as the dead-letter queue. Valid values are: - ``allowAll`` : (Default) Any source queues in this AWS account in the same Region can specify this queue as the dead-letter queue. - ``denyAll`` : No source queues can specify this queue as the dead-letter queue. - ``byQueue`` : Only queues specified by the ``sourceQueueArns`` parameter can specify this queue as the dead-letter queue. - ``sourceQueueArns`` : The Amazon Resource Names (ARN)s of the source queues that can specify this queue as the dead-letter queue and redrive messages. You can specify this parameter only when the ``redrivePermission`` parameter is set to ``byQueue`` . You can specify up to 10 source queue ARNs. To allow more than 10 source queues to specify dead-letter queues, set the ``redrivePermission`` parameter to ``allowAll`` .
        :param redrive_policy: The string that includes the parameters for the dead-letter queue functionality of the source queue as a JSON object. The parameters are as follows: - ``deadLetterTargetArn`` : The Amazon Resource Name (ARN) of the dead-letter queue to which Amazon SQS moves messages after the value of ``maxReceiveCount`` is exceeded. - ``maxReceiveCount`` : The number of times a message is delivered to the source queue before being moved to the dead-letter queue. When the ``ReceiveCount`` for a message exceeds the ``maxReceiveCount`` for a queue, Amazon SQS moves the message to the dead-letter-queue. .. epigraph:: The dead-letter queue of a FIFO queue must also be a FIFO queue. Similarly, the dead-letter queue of a standard queue must also be a standard queue. *JSON* ``{ "deadLetterTargetArn" : *String* , "maxReceiveCount" : *Integer* }`` *YAML* ``deadLetterTargetArn : *String*`` ``maxReceiveCount : *Integer*``
        :param sqs_managed_sse_enabled: Enables server-side queue encryption using SQS owned encryption keys. Only one server-side encryption option is supported per queue (for example, `SSE-KMS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sse-existing-queue.html>`_ or `SSE-SQS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sqs-sse-queue.html>`_ ).
        :param tags: The tags that you attach to this queue. For more information, see `Resource tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        :param visibility_timeout: The length of time during which a message will be unavailable after a message is delivered from the queue. This blocks other components from receiving the same message and gives the initial component time to process and delete the message from the queue. Values must be from 0 to 43,200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds. For more information about Amazon SQS queue visibility timeouts, see `Visibility timeout <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>`_ in the *Amazon SQS Developer Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b966f857467dc3eca3b20bcf8645d8fdbf83c8f0e6d6f487caec321b15e4fa2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnQueueProps(
            content_based_deduplication=content_based_deduplication,
            deduplication_scope=deduplication_scope,
            delay_seconds=delay_seconds,
            fifo_queue=fifo_queue,
            fifo_throughput_limit=fifo_throughput_limit,
            kms_data_key_reuse_period_seconds=kms_data_key_reuse_period_seconds,
            kms_master_key_id=kms_master_key_id,
            maximum_message_size=maximum_message_size,
            message_retention_period=message_retention_period,
            queue_name=queue_name,
            receive_message_wait_time_seconds=receive_message_wait_time_seconds,
            redrive_allow_policy=redrive_allow_policy,
            redrive_policy=redrive_policy,
            sqs_managed_sse_enabled=sqs_managed_sse_enabled,
            tags=tags,
            visibility_timeout=visibility_timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc24cb6372f95fb7aba43666df8950478848424c62f84060708e9f1766788d40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ce696eb25b3637569ee84e933254bbe73df611506638e4e9ccab1a856c97e0)
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
        '''Returns the Amazon Resource Name (ARN) of the queue.

        For example: ``arn:aws:sqs:us-east-2:123456789012:mystack-myqueue-15PG5C2FC1CW8`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrQueueName")
    def attr_queue_name(self) -> builtins.str:
        '''Returns the queue name.

        For example: ``mystack-myqueue-1VF9BKQH5BJVI`` .

        :cloudformationAttribute: QueueName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrQueueName"))

    @builtins.property
    @jsii.member(jsii_name="attrQueueUrl")
    def attr_queue_url(self) -> builtins.str:
        '''Returns the URLs of the queues from the policy.

        :cloudformationAttribute: QueueUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrQueueUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags that you attach to this queue.

        For more information, see `Resource tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="redriveAllowPolicy")
    def redrive_allow_policy(self) -> typing.Any:
        '''The string that includes the parameters for the permissions for the dead-letter queue redrive permission and which source queues can specify dead-letter queues as a JSON object.

        The parameters are as follows:

        - ``redrivePermission`` : The permission type that defines which source queues can specify the current queue as the dead-letter queue. Valid values are:
        - ``allowAll`` : (Default) Any source queues in this AWS account in the same Region can specify this queue as the dead-letter queue.
        - ``denyAll`` : No source queues can specify this queue as the dead-letter queue.
        - ``byQueue`` : Only queues specified by the ``sourceQueueArns`` parameter can specify this queue as the dead-letter queue.
        - ``sourceQueueArns`` : The Amazon Resource Names (ARN)s of the source queues that can specify this queue as the dead-letter queue and redrive messages. You can specify this parameter only when the ``redrivePermission`` parameter is set to ``byQueue`` . You can specify up to 10 source queue ARNs. To allow more than 10 source queues to specify dead-letter queues, set the ``redrivePermission`` parameter to ``allowAll`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-redriveallowpolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "redriveAllowPolicy"))

    @redrive_allow_policy.setter
    def redrive_allow_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6c34eae64fadbfb7b7b53d8cca14ad0b48ee2042a3ef365873bb429eb43dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redriveAllowPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="redrivePolicy")
    def redrive_policy(self) -> typing.Any:
        '''The string that includes the parameters for the dead-letter queue functionality of the source queue as a JSON object.

        The parameters are as follows:

        - ``deadLetterTargetArn`` : The Amazon Resource Name (ARN) of the dead-letter queue to which Amazon SQS moves messages after the value of ``maxReceiveCount`` is exceeded.
        - ``maxReceiveCount`` : The number of times a message is delivered to the source queue before being moved to the dead-letter queue. When the ``ReceiveCount`` for a message exceeds the ``maxReceiveCount`` for a queue, Amazon SQS moves the message to the dead-letter-queue.

        .. epigraph::

           The dead-letter queue of a FIFO queue must also be a FIFO queue. Similarly, the dead-letter queue of a standard queue must also be a standard queue.

        *JSON*

        ``{ "deadLetterTargetArn" : *String* , "maxReceiveCount" : *Integer* }``

        *YAML*

        ``deadLetterTargetArn : *String*``

        ``maxReceiveCount : *Integer*``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-redrivepolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "redrivePolicy"))

    @redrive_policy.setter
    def redrive_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800c15898da5aad1a8be95ea7df7bd5d7ee559bed7dc47af9e55af895a546b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redrivePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="contentBasedDeduplication")
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''For first-in-first-out (FIFO) queues, specifies whether to enable content-based deduplication.

        During the deduplication interval, Amazon SQS treats messages that are sent with identical content as duplicates and delivers only one copy of the message. For more information, see the ``ContentBasedDeduplication`` attribute for the ``[CreateQueue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html)`` action in the *Amazon SQS API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-contentbaseddeduplication
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "contentBasedDeduplication"))

    @content_based_deduplication.setter
    def content_based_deduplication(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb5063294bcf65631c98d9c690b176401dd1bf332d6ddfc38666d135b740662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentBasedDeduplication", value)

    @builtins.property
    @jsii.member(jsii_name="deduplicationScope")
    def deduplication_scope(self) -> typing.Optional[builtins.str]:
        '''For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level.

        Valid values are ``messageGroup`` and ``queue`` .

        To enable high throughput for a FIFO queue, set this attribute to ``messageGroup`` *and* set the ``FifoThroughputLimit`` attribute to ``perMessageGroupId`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-deduplicationscope
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deduplicationScope"))

    @deduplication_scope.setter
    def deduplication_scope(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0234687b26c1ab1e4eadf9e8b7e7b1656611c8a2fcd00ffd67ece7125f0c35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deduplicationScope", value)

    @builtins.property
    @jsii.member(jsii_name="delaySeconds")
    def delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time in seconds for which the delivery of all messages in the queue is delayed.

        You can specify an integer value of ``0`` to ``900`` (15 minutes). The default value is ``0`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-delayseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "delaySeconds"))

    @delay_seconds.setter
    def delay_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9905c8e33d3b624e01c457c7ca954ba52b2fdabaff2c55155c0e5b55bcba6f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delaySeconds", value)

    @builtins.property
    @jsii.member(jsii_name="fifoQueue")
    def fifo_queue(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If set to true, creates a FIFO queue.

        If you don't specify this property, Amazon SQS creates a standard queue. For more information, see `FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-fifoqueue
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "fifoQueue"))

    @fifo_queue.setter
    def fifo_queue(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f019054afaa98471bda07a4bc80a39b073bb151d319e7dd90c7c05d621c81b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fifoQueue", value)

    @builtins.property
    @jsii.member(jsii_name="fifoThroughputLimit")
    def fifo_throughput_limit(self) -> typing.Optional[builtins.str]:
        '''For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group.

        Valid values are ``perQueue`` and ``perMessageGroupId`` .

        To enable high throughput for a FIFO queue, set this attribute to ``perMessageGroupId`` *and* set the ``DeduplicationScope`` attribute to ``messageGroup`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-fifothroughputlimit
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fifoThroughputLimit"))

    @fifo_throughput_limit.setter
    def fifo_throughput_limit(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b44e254a10a43eb2b9ffddae3f0bbde0b25f1b4d685a268d1446378688388e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fifoThroughputLimit", value)

    @builtins.property
    @jsii.member(jsii_name="kmsDataKeyReusePeriodSeconds")
    def kms_data_key_reuse_period_seconds(self) -> typing.Optional[jsii.Number]:
        '''The length of time in seconds for which Amazon SQS can reuse a data key to encrypt or decrypt messages before calling AWS KMS again.

        The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes).
        .. epigraph::

           A shorter time period provides better security, but results in more calls to AWS KMS , which might incur charges after Free Tier. For more information, see `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html#sqs-how-does-the-data-key-reuse-period-work>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-kmsdatakeyreuseperiodseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "kmsDataKeyReusePeriodSeconds"))

    @kms_data_key_reuse_period_seconds.setter
    def kms_data_key_reuse_period_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1766a21beef2e41883d097e9c658a0fada533df42b2c38a4ed7500afdedc32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsDataKeyReusePeriodSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="kmsMasterKeyId")
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an AWS Key Management Service (KMS) for Amazon SQS , or a custom KMS.

        To use the AWS managed KMS for Amazon SQS , specify a (default) alias ARN, alias name (e.g. ``alias/aws/sqs`` ), key ARN, or key ID. For more information, see the following:

        - `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html>`_ in the *Amazon SQS Developer Guide*
        - `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ in the *Amazon SQS API Reference*
        - `Request Parameters <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters>`_ in the *AWS Key Management Service API Reference*
        - The Key Management Service (KMS) section of the `AWS Key Management Service Best Practices <https://docs.aws.amazon.com/https://d0.awsstatic.com/whitepapers/aws-kms-best-practices.pdf>`_ whitepaper

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-kmsmasterkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsMasterKeyId"))

    @kms_master_key_id.setter
    def kms_master_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e58b673a1d0996e8a656c4a6d9f52d867e74330dd7d4c4035d195eabe3789a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsMasterKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="maximumMessageSize")
    def maximum_message_size(self) -> typing.Optional[jsii.Number]:
        '''The limit of how many bytes that a message can contain before Amazon SQS rejects it.

        You can specify an integer value from ``1,024`` bytes (1 KiB) to ``262,144`` bytes (256 KiB). The default value is ``262,144`` (256 KiB).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-maximummessagesize
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumMessageSize"))

    @maximum_message_size.setter
    def maximum_message_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bec0d8792d725f4ecf22854700fcf319d30f21820c499d5f5dd86026473370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumMessageSize", value)

    @builtins.property
    @jsii.member(jsii_name="messageRetentionPeriod")
    def message_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds that Amazon SQS retains a message.

        You can specify an integer value from ``60`` seconds (1 minute) to ``1,209,600`` seconds (14 days). The default value is ``345,600`` seconds (4 days).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-messageretentionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "messageRetentionPeriod"))

    @message_retention_period.setter
    def message_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5504e9f1b99db86e259b4b2cb2637ff5066727ee9fa42a8e88b6c1d92173cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> typing.Optional[builtins.str]:
        '''A name for the queue.

        To create a FIFO queue, the name of your FIFO queue must end with the ``.fifo`` suffix. For more information, see `FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html>`_ in the *Amazon SQS Developer Guide* .

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the queue name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-queuename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600ceee83b6c1f48825d04a8085b478b08e0ac31eb58ee92379d809f0b8e708a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value)

    @builtins.property
    @jsii.member(jsii_name="receiveMessageWaitTimeSeconds")
    def receive_message_wait_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''Specifies the duration, in seconds, that the ReceiveMessage action call waits until a message is in the queue in order to include it in the response, rather than returning an empty response if a message isn't yet available.

        You can specify an integer from 1 to 20. Short polling is used as the default or when you specify 0 for this property. For more information, see `Consuming messages using long polling <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html#sqs-long-polling>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-receivemessagewaittimeseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "receiveMessageWaitTimeSeconds"))

    @receive_message_wait_time_seconds.setter
    def receive_message_wait_time_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9d8c5fc62afa3a6855e545e3169408779aca8791233fb963d369a9b7bac55e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "receiveMessageWaitTimeSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="sqsManagedSseEnabled")
    def sqs_managed_sse_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables server-side queue encryption using SQS owned encryption keys.

        Only one server-side encryption option is supported per queue (for example, `SSE-KMS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sse-existing-queue.html>`_ or `SSE-SQS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sqs-sse-queue.html>`_ ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-sqsmanagedsseenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "sqsManagedSseEnabled"))

    @sqs_managed_sse_enabled.setter
    def sqs_managed_sse_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5dbe47074fc3fab420b5c12f3b58350e4bb589f23a40e5fe439587219d97e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqsManagedSseEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="visibilityTimeout")
    def visibility_timeout(self) -> typing.Optional[jsii.Number]:
        '''The length of time during which a message will be unavailable after a message is delivered from the queue.

        This blocks other components from receiving the same message and gives the initial component time to process and delete the message from the queue.

        Values must be from 0 to 43,200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds.

        For more information about Amazon SQS queue visibility timeouts, see `Visibility timeout <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-visibilitytimeout
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "visibilityTimeout"))

    @visibility_timeout.setter
    def visibility_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9bfde971d36d9221effffd6812896622398d206473bb12f36e53dd33d397b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibilityTimeout", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnQueuePolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sqs.CfnQueuePolicy",
):
    '''A CloudFormation ``AWS::SQS::QueuePolicy``.

    The ``AWS::SQS::QueuePolicy`` type applies a policy to Amazon SQS queues. For an example snippet, see `Declaring an Amazon SQS policy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-sqs-policy>`_ in the *AWS CloudFormation User Guide* .

    :cloudformationResource: AWS::SQS::QueuePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sqs as sqs
        
        # policy_document: Any
        
        cfn_queue_policy = sqs.CfnQueuePolicy(self, "MyCfnQueuePolicy",
            policy_document=policy_document,
            queues=["queues"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy_document: typing.Any,
        queues: typing.Sequence[builtins.str],
    ) -> None:
        '''Create a new ``AWS::SQS::QueuePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: A policy document that contains the permissions for the specified Amazon SQS queues. For more information about Amazon SQS policies, see `Using custom policies with the Amazon SQS access policy language <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html>`_ in the *Amazon SQS Developer Guide* .
        :param queues: The URLs of the queues to which you want to add the policy. You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html)`` resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b460b4585e0e26fbf1e9482f8d0a2489e127775e1a336c204f216cdb3941cea4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnQueuePolicyProps(policy_document=policy_document, queues=queues)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c7bb97d9f6eeb6907f34bd1ff7902637a1be3bf26ad959c3ae41cd12e9c942)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec6a2d478a4ae539266b3c01207d2ab8b02228df3e5deca4976796ce8e9415e)
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
    def policy_document(self) -> typing.Any:
        '''A policy document that contains the permissions for the specified Amazon SQS queues.

        For more information about Amazon SQS policies, see `Using custom policies with the Amazon SQS access policy language <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html#cfn-sqs-queuepolicy-policydoc
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a0d40235a94be1804049d5624b932ad77e2a347be58c35ee13d52a9f891764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="queues")
    def queues(self) -> typing.List[builtins.str]:
        '''The URLs of the queues to which you want to add the policy.

        You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html)`` resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html#cfn-sqs-queuepolicy-queues
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queues"))

    @queues.setter
    def queues(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c313624f0694c7a6ab32b9209b29a517d9c889e2e3f782e2bfdff8ead3c81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queues", value)


@jsii.data_type(
    jsii_type="monocdk.aws_sqs.CfnQueuePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "queues": "queues"},
)
class CfnQueuePolicyProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any,
        queues: typing.Sequence[builtins.str],
    ) -> None:
        '''Properties for defining a ``CfnQueuePolicy``.

        :param policy_document: A policy document that contains the permissions for the specified Amazon SQS queues. For more information about Amazon SQS policies, see `Using custom policies with the Amazon SQS access policy language <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html>`_ in the *Amazon SQS Developer Guide* .
        :param queues: The URLs of the queues to which you want to add the policy. You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html)`` resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sqs as sqs
            
            # policy_document: Any
            
            cfn_queue_policy_props = sqs.CfnQueuePolicyProps(
                policy_document=policy_document,
                queues=["queues"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d3686cbe3a3ab1fbd6b544bda75f42994de52e7608a442feb49881506cf4127)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument queues", value=queues, expected_type=type_hints["queues"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
            "queues": queues,
        }

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document that contains the permissions for the specified Amazon SQS queues.

        For more information about Amazon SQS policies, see `Using custom policies with the Amazon SQS access policy language <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html#cfn-sqs-queuepolicy-policydoc
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def queues(self) -> typing.List[builtins.str]:
        '''The URLs of the queues to which you want to add the policy.

        You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html)`` resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html#cfn-sqs-queuepolicy-queues
        '''
        result = self._values.get("queues")
        assert result is not None, "Required property 'queues' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueuePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sqs.CfnQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_based_deduplication": "contentBasedDeduplication",
        "deduplication_scope": "deduplicationScope",
        "delay_seconds": "delaySeconds",
        "fifo_queue": "fifoQueue",
        "fifo_throughput_limit": "fifoThroughputLimit",
        "kms_data_key_reuse_period_seconds": "kmsDataKeyReusePeriodSeconds",
        "kms_master_key_id": "kmsMasterKeyId",
        "maximum_message_size": "maximumMessageSize",
        "message_retention_period": "messageRetentionPeriod",
        "queue_name": "queueName",
        "receive_message_wait_time_seconds": "receiveMessageWaitTimeSeconds",
        "redrive_allow_policy": "redriveAllowPolicy",
        "redrive_policy": "redrivePolicy",
        "sqs_managed_sse_enabled": "sqsManagedSseEnabled",
        "tags": "tags",
        "visibility_timeout": "visibilityTimeout",
    },
)
class CfnQueueProps:
    def __init__(
        self,
        *,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        deduplication_scope: typing.Optional[builtins.str] = None,
        delay_seconds: typing.Optional[jsii.Number] = None,
        fifo_queue: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        fifo_throughput_limit: typing.Optional[builtins.str] = None,
        kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        maximum_message_size: typing.Optional[jsii.Number] = None,
        message_retention_period: typing.Optional[jsii.Number] = None,
        queue_name: typing.Optional[builtins.str] = None,
        receive_message_wait_time_seconds: typing.Optional[jsii.Number] = None,
        redrive_allow_policy: typing.Any = None,
        redrive_policy: typing.Any = None,
        sqs_managed_sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        visibility_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnQueue``.

        :param content_based_deduplication: For first-in-first-out (FIFO) queues, specifies whether to enable content-based deduplication. During the deduplication interval, Amazon SQS treats messages that are sent with identical content as duplicates and delivers only one copy of the message. For more information, see the ``ContentBasedDeduplication`` attribute for the ``[CreateQueue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html)`` action in the *Amazon SQS API Reference* .
        :param deduplication_scope: For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level. Valid values are ``messageGroup`` and ``queue`` . To enable high throughput for a FIFO queue, set this attribute to ``messageGroup`` *and* set the ``FifoThroughputLimit`` attribute to ``perMessageGroupId`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .
        :param delay_seconds: The time in seconds for which the delivery of all messages in the queue is delayed. You can specify an integer value of ``0`` to ``900`` (15 minutes). The default value is ``0`` .
        :param fifo_queue: If set to true, creates a FIFO queue. If you don't specify this property, Amazon SQS creates a standard queue. For more information, see `FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html>`_ in the *Amazon SQS Developer Guide* .
        :param fifo_throughput_limit: For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group. Valid values are ``perQueue`` and ``perMessageGroupId`` . To enable high throughput for a FIFO queue, set this attribute to ``perMessageGroupId`` *and* set the ``DeduplicationScope`` attribute to ``messageGroup`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .
        :param kms_data_key_reuse_period_seconds: The length of time in seconds for which Amazon SQS can reuse a data key to encrypt or decrypt messages before calling AWS KMS again. The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes). .. epigraph:: A shorter time period provides better security, but results in more calls to AWS KMS , which might incur charges after Free Tier. For more information, see `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html#sqs-how-does-the-data-key-reuse-period-work>`_ in the *Amazon SQS Developer Guide* .
        :param kms_master_key_id: The ID of an AWS Key Management Service (KMS) for Amazon SQS , or a custom KMS. To use the AWS managed KMS for Amazon SQS , specify a (default) alias ARN, alias name (e.g. ``alias/aws/sqs`` ), key ARN, or key ID. For more information, see the following: - `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html>`_ in the *Amazon SQS Developer Guide* - `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ in the *Amazon SQS API Reference* - `Request Parameters <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters>`_ in the *AWS Key Management Service API Reference* - The Key Management Service (KMS) section of the `AWS Key Management Service Best Practices <https://docs.aws.amazon.com/https://d0.awsstatic.com/whitepapers/aws-kms-best-practices.pdf>`_ whitepaper
        :param maximum_message_size: The limit of how many bytes that a message can contain before Amazon SQS rejects it. You can specify an integer value from ``1,024`` bytes (1 KiB) to ``262,144`` bytes (256 KiB). The default value is ``262,144`` (256 KiB).
        :param message_retention_period: The number of seconds that Amazon SQS retains a message. You can specify an integer value from ``60`` seconds (1 minute) to ``1,209,600`` seconds (14 days). The default value is ``345,600`` seconds (4 days).
        :param queue_name: A name for the queue. To create a FIFO queue, the name of your FIFO queue must end with the ``.fifo`` suffix. For more information, see `FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html>`_ in the *Amazon SQS Developer Guide* . If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the queue name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param receive_message_wait_time_seconds: Specifies the duration, in seconds, that the ReceiveMessage action call waits until a message is in the queue in order to include it in the response, rather than returning an empty response if a message isn't yet available. You can specify an integer from 1 to 20. Short polling is used as the default or when you specify 0 for this property. For more information, see `Consuming messages using long polling <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html#sqs-long-polling>`_ in the *Amazon SQS Developer Guide* .
        :param redrive_allow_policy: The string that includes the parameters for the permissions for the dead-letter queue redrive permission and which source queues can specify dead-letter queues as a JSON object. The parameters are as follows: - ``redrivePermission`` : The permission type that defines which source queues can specify the current queue as the dead-letter queue. Valid values are: - ``allowAll`` : (Default) Any source queues in this AWS account in the same Region can specify this queue as the dead-letter queue. - ``denyAll`` : No source queues can specify this queue as the dead-letter queue. - ``byQueue`` : Only queues specified by the ``sourceQueueArns`` parameter can specify this queue as the dead-letter queue. - ``sourceQueueArns`` : The Amazon Resource Names (ARN)s of the source queues that can specify this queue as the dead-letter queue and redrive messages. You can specify this parameter only when the ``redrivePermission`` parameter is set to ``byQueue`` . You can specify up to 10 source queue ARNs. To allow more than 10 source queues to specify dead-letter queues, set the ``redrivePermission`` parameter to ``allowAll`` .
        :param redrive_policy: The string that includes the parameters for the dead-letter queue functionality of the source queue as a JSON object. The parameters are as follows: - ``deadLetterTargetArn`` : The Amazon Resource Name (ARN) of the dead-letter queue to which Amazon SQS moves messages after the value of ``maxReceiveCount`` is exceeded. - ``maxReceiveCount`` : The number of times a message is delivered to the source queue before being moved to the dead-letter queue. When the ``ReceiveCount`` for a message exceeds the ``maxReceiveCount`` for a queue, Amazon SQS moves the message to the dead-letter-queue. .. epigraph:: The dead-letter queue of a FIFO queue must also be a FIFO queue. Similarly, the dead-letter queue of a standard queue must also be a standard queue. *JSON* ``{ "deadLetterTargetArn" : *String* , "maxReceiveCount" : *Integer* }`` *YAML* ``deadLetterTargetArn : *String*`` ``maxReceiveCount : *Integer*``
        :param sqs_managed_sse_enabled: Enables server-side queue encryption using SQS owned encryption keys. Only one server-side encryption option is supported per queue (for example, `SSE-KMS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sse-existing-queue.html>`_ or `SSE-SQS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sqs-sse-queue.html>`_ ).
        :param tags: The tags that you attach to this queue. For more information, see `Resource tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        :param visibility_timeout: The length of time during which a message will be unavailable after a message is delivered from the queue. This blocks other components from receiving the same message and gives the initial component time to process and delete the message from the queue. Values must be from 0 to 43,200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds. For more information about Amazon SQS queue visibility timeouts, see `Visibility timeout <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sqs as sqs
            
            # redrive_allow_policy: Any
            # redrive_policy: Any
            
            cfn_queue_props = sqs.CfnQueueProps(
                content_based_deduplication=False,
                deduplication_scope="deduplicationScope",
                delay_seconds=123,
                fifo_queue=False,
                fifo_throughput_limit="fifoThroughputLimit",
                kms_data_key_reuse_period_seconds=123,
                kms_master_key_id="kmsMasterKeyId",
                maximum_message_size=123,
                message_retention_period=123,
                queue_name="queueName",
                receive_message_wait_time_seconds=123,
                redrive_allow_policy=redrive_allow_policy,
                redrive_policy=redrive_policy,
                sqs_managed_sse_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                visibility_timeout=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644c014f03c653a9a83c75b626e118e690808f6a652c15a6c86cd474baa63480)
            check_type(argname="argument content_based_deduplication", value=content_based_deduplication, expected_type=type_hints["content_based_deduplication"])
            check_type(argname="argument deduplication_scope", value=deduplication_scope, expected_type=type_hints["deduplication_scope"])
            check_type(argname="argument delay_seconds", value=delay_seconds, expected_type=type_hints["delay_seconds"])
            check_type(argname="argument fifo_queue", value=fifo_queue, expected_type=type_hints["fifo_queue"])
            check_type(argname="argument fifo_throughput_limit", value=fifo_throughput_limit, expected_type=type_hints["fifo_throughput_limit"])
            check_type(argname="argument kms_data_key_reuse_period_seconds", value=kms_data_key_reuse_period_seconds, expected_type=type_hints["kms_data_key_reuse_period_seconds"])
            check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
            check_type(argname="argument maximum_message_size", value=maximum_message_size, expected_type=type_hints["maximum_message_size"])
            check_type(argname="argument message_retention_period", value=message_retention_period, expected_type=type_hints["message_retention_period"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument receive_message_wait_time_seconds", value=receive_message_wait_time_seconds, expected_type=type_hints["receive_message_wait_time_seconds"])
            check_type(argname="argument redrive_allow_policy", value=redrive_allow_policy, expected_type=type_hints["redrive_allow_policy"])
            check_type(argname="argument redrive_policy", value=redrive_policy, expected_type=type_hints["redrive_policy"])
            check_type(argname="argument sqs_managed_sse_enabled", value=sqs_managed_sse_enabled, expected_type=type_hints["sqs_managed_sse_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument visibility_timeout", value=visibility_timeout, expected_type=type_hints["visibility_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_based_deduplication is not None:
            self._values["content_based_deduplication"] = content_based_deduplication
        if deduplication_scope is not None:
            self._values["deduplication_scope"] = deduplication_scope
        if delay_seconds is not None:
            self._values["delay_seconds"] = delay_seconds
        if fifo_queue is not None:
            self._values["fifo_queue"] = fifo_queue
        if fifo_throughput_limit is not None:
            self._values["fifo_throughput_limit"] = fifo_throughput_limit
        if kms_data_key_reuse_period_seconds is not None:
            self._values["kms_data_key_reuse_period_seconds"] = kms_data_key_reuse_period_seconds
        if kms_master_key_id is not None:
            self._values["kms_master_key_id"] = kms_master_key_id
        if maximum_message_size is not None:
            self._values["maximum_message_size"] = maximum_message_size
        if message_retention_period is not None:
            self._values["message_retention_period"] = message_retention_period
        if queue_name is not None:
            self._values["queue_name"] = queue_name
        if receive_message_wait_time_seconds is not None:
            self._values["receive_message_wait_time_seconds"] = receive_message_wait_time_seconds
        if redrive_allow_policy is not None:
            self._values["redrive_allow_policy"] = redrive_allow_policy
        if redrive_policy is not None:
            self._values["redrive_policy"] = redrive_policy
        if sqs_managed_sse_enabled is not None:
            self._values["sqs_managed_sse_enabled"] = sqs_managed_sse_enabled
        if tags is not None:
            self._values["tags"] = tags
        if visibility_timeout is not None:
            self._values["visibility_timeout"] = visibility_timeout

    @builtins.property
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''For first-in-first-out (FIFO) queues, specifies whether to enable content-based deduplication.

        During the deduplication interval, Amazon SQS treats messages that are sent with identical content as duplicates and delivers only one copy of the message. For more information, see the ``ContentBasedDeduplication`` attribute for the ``[CreateQueue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html)`` action in the *Amazon SQS API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-contentbaseddeduplication
        '''
        result = self._values.get("content_based_deduplication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def deduplication_scope(self) -> typing.Optional[builtins.str]:
        '''For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level.

        Valid values are ``messageGroup`` and ``queue`` .

        To enable high throughput for a FIFO queue, set this attribute to ``messageGroup`` *and* set the ``FifoThroughputLimit`` attribute to ``perMessageGroupId`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-deduplicationscope
        '''
        result = self._values.get("deduplication_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time in seconds for which the delivery of all messages in the queue is delayed.

        You can specify an integer value of ``0`` to ``900`` (15 minutes). The default value is ``0`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-delayseconds
        '''
        result = self._values.get("delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fifo_queue(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If set to true, creates a FIFO queue.

        If you don't specify this property, Amazon SQS creates a standard queue. For more information, see `FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-fifoqueue
        '''
        result = self._values.get("fifo_queue")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def fifo_throughput_limit(self) -> typing.Optional[builtins.str]:
        '''For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group.

        Valid values are ``perQueue`` and ``perMessageGroupId`` .

        To enable high throughput for a FIFO queue, set this attribute to ``perMessageGroupId`` *and* set the ``DeduplicationScope`` attribute to ``messageGroup`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-fifothroughputlimit
        '''
        result = self._values.get("fifo_throughput_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_data_key_reuse_period_seconds(self) -> typing.Optional[jsii.Number]:
        '''The length of time in seconds for which Amazon SQS can reuse a data key to encrypt or decrypt messages before calling AWS KMS again.

        The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes).
        .. epigraph::

           A shorter time period provides better security, but results in more calls to AWS KMS , which might incur charges after Free Tier. For more information, see `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html#sqs-how-does-the-data-key-reuse-period-work>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-kmsdatakeyreuseperiodseconds
        '''
        result = self._values.get("kms_data_key_reuse_period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an AWS Key Management Service (KMS) for Amazon SQS , or a custom KMS.

        To use the AWS managed KMS for Amazon SQS , specify a (default) alias ARN, alias name (e.g. ``alias/aws/sqs`` ), key ARN, or key ID. For more information, see the following:

        - `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html>`_ in the *Amazon SQS Developer Guide*
        - `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ in the *Amazon SQS API Reference*
        - `Request Parameters <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters>`_ in the *AWS Key Management Service API Reference*
        - The Key Management Service (KMS) section of the `AWS Key Management Service Best Practices <https://docs.aws.amazon.com/https://d0.awsstatic.com/whitepapers/aws-kms-best-practices.pdf>`_ whitepaper

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-kmsmasterkeyid
        '''
        result = self._values.get("kms_master_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_message_size(self) -> typing.Optional[jsii.Number]:
        '''The limit of how many bytes that a message can contain before Amazon SQS rejects it.

        You can specify an integer value from ``1,024`` bytes (1 KiB) to ``262,144`` bytes (256 KiB). The default value is ``262,144`` (256 KiB).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-maximummessagesize
        '''
        result = self._values.get("maximum_message_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def message_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds that Amazon SQS retains a message.

        You can specify an integer value from ``60`` seconds (1 minute) to ``1,209,600`` seconds (14 days). The default value is ``345,600`` seconds (4 days).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-messageretentionperiod
        '''
        result = self._values.get("message_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_name(self) -> typing.Optional[builtins.str]:
        '''A name for the queue.

        To create a FIFO queue, the name of your FIFO queue must end with the ``.fifo`` suffix. For more information, see `FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html>`_ in the *Amazon SQS Developer Guide* .

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the queue name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-queuename
        '''
        result = self._values.get("queue_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def receive_message_wait_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''Specifies the duration, in seconds, that the ReceiveMessage action call waits until a message is in the queue in order to include it in the response, rather than returning an empty response if a message isn't yet available.

        You can specify an integer from 1 to 20. Short polling is used as the default or when you specify 0 for this property. For more information, see `Consuming messages using long polling <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html#sqs-long-polling>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-receivemessagewaittimeseconds
        '''
        result = self._values.get("receive_message_wait_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redrive_allow_policy(self) -> typing.Any:
        '''The string that includes the parameters for the permissions for the dead-letter queue redrive permission and which source queues can specify dead-letter queues as a JSON object.

        The parameters are as follows:

        - ``redrivePermission`` : The permission type that defines which source queues can specify the current queue as the dead-letter queue. Valid values are:
        - ``allowAll`` : (Default) Any source queues in this AWS account in the same Region can specify this queue as the dead-letter queue.
        - ``denyAll`` : No source queues can specify this queue as the dead-letter queue.
        - ``byQueue`` : Only queues specified by the ``sourceQueueArns`` parameter can specify this queue as the dead-letter queue.
        - ``sourceQueueArns`` : The Amazon Resource Names (ARN)s of the source queues that can specify this queue as the dead-letter queue and redrive messages. You can specify this parameter only when the ``redrivePermission`` parameter is set to ``byQueue`` . You can specify up to 10 source queue ARNs. To allow more than 10 source queues to specify dead-letter queues, set the ``redrivePermission`` parameter to ``allowAll`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-redriveallowpolicy
        '''
        result = self._values.get("redrive_allow_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def redrive_policy(self) -> typing.Any:
        '''The string that includes the parameters for the dead-letter queue functionality of the source queue as a JSON object.

        The parameters are as follows:

        - ``deadLetterTargetArn`` : The Amazon Resource Name (ARN) of the dead-letter queue to which Amazon SQS moves messages after the value of ``maxReceiveCount`` is exceeded.
        - ``maxReceiveCount`` : The number of times a message is delivered to the source queue before being moved to the dead-letter queue. When the ``ReceiveCount`` for a message exceeds the ``maxReceiveCount`` for a queue, Amazon SQS moves the message to the dead-letter-queue.

        .. epigraph::

           The dead-letter queue of a FIFO queue must also be a FIFO queue. Similarly, the dead-letter queue of a standard queue must also be a standard queue.

        *JSON*

        ``{ "deadLetterTargetArn" : *String* , "maxReceiveCount" : *Integer* }``

        *YAML*

        ``deadLetterTargetArn : *String*``

        ``maxReceiveCount : *Integer*``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-redrivepolicy
        '''
        result = self._values.get("redrive_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def sqs_managed_sse_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables server-side queue encryption using SQS owned encryption keys.

        Only one server-side encryption option is supported per queue (for example, `SSE-KMS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sse-existing-queue.html>`_ or `SSE-SQS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sqs-sse-queue.html>`_ ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-sqsmanagedsseenabled
        '''
        result = self._values.get("sqs_managed_sse_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags that you attach to this queue.

        For more information, see `Resource tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def visibility_timeout(self) -> typing.Optional[jsii.Number]:
        '''The length of time during which a message will be unavailable after a message is delivered from the queue.

        This blocks other components from receiving the same message and gives the initial component time to process and delete the message from the queue.

        Values must be from 0 to 43,200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds.

        For more information about Amazon SQS queue visibility timeouts, see `Visibility timeout <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-visibilitytimeout
        '''
        result = self._values.get("visibility_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sqs.DeadLetterQueue",
    jsii_struct_bases=[],
    name_mapping={"max_receive_count": "maxReceiveCount", "queue": "queue"},
)
class DeadLetterQueue:
    def __init__(self, *, max_receive_count: jsii.Number, queue: "IQueue") -> None:
        '''(experimental) Dead letter queue settings.

        :param max_receive_count: (experimental) The number of times a message can be unsuccesfully dequeued before being moved to the dead-letter queue.
        :param queue: (experimental) The dead-letter queue to which Amazon SQS moves messages after the value of maxReceiveCount is exceeded.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            
            dead_letter_queue = sqs.DeadLetterQueue(
                max_receive_count=123,
                queue=queue
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b2dcab57acc441eaa63ee634c2c8e5ac9295c94eb9266418ad3a5520b8848d)
            check_type(argname="argument max_receive_count", value=max_receive_count, expected_type=type_hints["max_receive_count"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_receive_count": max_receive_count,
            "queue": queue,
        }

    @builtins.property
    def max_receive_count(self) -> jsii.Number:
        '''(experimental) The number of times a message can be unsuccesfully dequeued before being moved to the dead-letter queue.

        :stability: experimental
        '''
        result = self._values.get("max_receive_count")
        assert result is not None, "Required property 'max_receive_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def queue(self) -> "IQueue":
        '''(experimental) The dead-letter queue to which Amazon SQS moves messages after the value of maxReceiveCount is exceeded.

        :stability: experimental
        '''
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return typing.cast("IQueue", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeadLetterQueue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_sqs.DeduplicationScope")
class DeduplicationScope(enum.Enum):
    '''(experimental) What kind of deduplication scope to apply.

    :stability: experimental
    '''

    MESSAGE_GROUP = "MESSAGE_GROUP"
    '''(experimental) Deduplication occurs at the message group level.

    :stability: experimental
    '''
    QUEUE = "QUEUE"
    '''(experimental) Deduplication occurs at the message queue level.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_sqs.FifoThroughputLimit")
class FifoThroughputLimit(enum.Enum):
    '''(experimental) Whether the FIFO queue throughput quota applies to the entire queue or per message group.

    :stability: experimental
    '''

    PER_QUEUE = "PER_QUEUE"
    '''(experimental) Throughput quota applies per queue.

    :stability: experimental
    '''
    PER_MESSAGE_GROUP_ID = "PER_MESSAGE_GROUP_ID"
    '''(experimental) Throughput quota applies per message group id.

    :stability: experimental
    '''


@jsii.interface(jsii_type="monocdk.aws_sqs.IQueue")
class IQueue(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an SQS queue.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this queue.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        '''(experimental) The name of this queue.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> builtins.str:
        '''(experimental) The URL of this queue.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) If this queue is server-side encrypted, this is the KMS encryption key.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this queue.

        If this queue was created in this stack (``new Queue``), a queue policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the queue is imported (``Queue.import``), then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *queue_actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the actions defined in queueActions to the identity Principal given on this SQS queue resource.

        :param grantee: Principal to grant right to.
        :param queue_actions: The actions to grant.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant permissions to consume messages from a queue.

        This will grant the following permissions:

        - sqs:ChangeMessageVisibility
        - sqs:DeleteMessage
        - sqs:ReceiveMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant consume rights to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant an IAM principal permissions to purge all messages from the queue.

        This will grant the following permissions:

        - sqs:PurgeQueue
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to send messages to a queue to the given identity.

        This will grant the following permissions:

        - sqs:SendMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.

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
        '''(experimental) Return the given named metric for this Queue.

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

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(
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
        '''(experimental) The approximate age of the oldest non-deleted message in the queue.

        Maximum over 5 minutes

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

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(
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
        '''(experimental) The number of messages in the queue that are delayed and not available for reading immediately.

        Maximum over 5 minutes

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

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(
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
        '''(experimental) The number of messages that are in flight.

        Maximum over 5 minutes

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

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(
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
        '''(experimental) The number of messages available for retrieval from the queue.

        Maximum over 5 minutes

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

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(
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
        '''(experimental) The number of ReceiveMessage API calls that did not return a message.

        Sum over 5 minutes

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

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(
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
        '''(experimental) The number of messages deleted from the queue.

        Sum over 5 minutes

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

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(
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
        '''(experimental) The number of messages returned by calls to the ReceiveMessage action.

        Sum over 5 minutes

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

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(
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
        '''(experimental) The number of messages added to a queue.

        Sum over 5 minutes

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

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(
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
        '''(experimental) The size of messages added to a queue.

        Average over 5 minutes

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


class _IQueueProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an SQS queue.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_sqs.IQueue"

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "fifo"))

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this queue.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueArn"))

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        '''(experimental) The name of this queue.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> builtins.str:
        '''(experimental) The URL of this queue.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueUrl"))

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) If this queue is server-side encrypted, this is the KMS encryption key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionMasterKey"))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this queue.

        If this queue was created in this stack (``new Queue``), a queue policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the queue is imported (``Queue.import``), then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157cf7572c38088b4b87e878ba341ee41a4c992de389fedf35a6d633c45add1f)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *queue_actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the actions defined in queueActions to the identity Principal given on this SQS queue resource.

        :param grantee: Principal to grant right to.
        :param queue_actions: The actions to grant.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a7c5b38daa71e99641ce252abc9ccff3c3206cbd4abbfaec1b8a9201a29a5a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument queue_actions", value=queue_actions, expected_type=typing.Tuple[type_hints["queue_actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *queue_actions]))

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant permissions to consume messages from a queue.

        This will grant the following permissions:

        - sqs:ChangeMessageVisibility
        - sqs:DeleteMessage
        - sqs:ReceiveMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant consume rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd41af889216d3b9b20a10de3ae772f91cd70ebd2d4436f33eb5dd5ddb891b91)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantConsumeMessages", [grantee]))

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant an IAM principal permissions to purge all messages from the queue.

        This will grant the following permissions:

        - sqs:PurgeQueue
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e3d0525c7d13dc6521cf60ef8f5b4c94644764076e9700fef89019cb67c65c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPurge", [grantee]))

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to send messages to a queue to the given identity.

        This will grant the following permissions:

        - sqs:SendMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0675f749c5d860bfd6e2773128196db6eb2dc6d75173fe333973afdfbad172)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantSendMessages", [grantee]))

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
        '''(experimental) Return the given named metric for this Queue.

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
            type_hints = typing.get_type_hints(_typecheckingstub__536893be1eb70ff1e34fb6a822c3dca0bfc89bd38da1961145970a7fc53ef54f)
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

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(
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
        '''(experimental) The approximate age of the oldest non-deleted message in the queue.

        Maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricApproximateAgeOfOldestMessage", [props]))

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(
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
        '''(experimental) The number of messages in the queue that are delayed and not available for reading immediately.

        Maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricApproximateNumberOfMessagesDelayed", [props]))

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(
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
        '''(experimental) The number of messages that are in flight.

        Maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricApproximateNumberOfMessagesNotVisible", [props]))

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(
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
        '''(experimental) The number of messages available for retrieval from the queue.

        Maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricApproximateNumberOfMessagesVisible", [props]))

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(
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
        '''(experimental) The number of ReceiveMessage API calls that did not return a message.

        Sum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfEmptyReceives", [props]))

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(
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
        '''(experimental) The number of messages deleted from the queue.

        Sum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfMessagesDeleted", [props]))

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(
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
        '''(experimental) The number of messages returned by calls to the ReceiveMessage action.

        Sum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfMessagesReceived", [props]))

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(
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
        '''(experimental) The number of messages added to a queue.

        Sum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfMessagesSent", [props]))

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(
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
        '''(experimental) The size of messages added to a queue.

        Average over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSentMessageSize", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IQueue).__jsii_proxy_class__ = lambda : _IQueueProxy


@jsii.data_type(
    jsii_type="monocdk.aws_sqs.QueueAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "queue_arn": "queueArn",
        "fifo": "fifo",
        "key_arn": "keyArn",
        "queue_name": "queueName",
        "queue_url": "queueUrl",
    },
)
class QueueAttributes:
    def __init__(
        self,
        *,
        queue_arn: builtins.str,
        fifo: typing.Optional[builtins.bool] = None,
        key_arn: typing.Optional[builtins.str] = None,
        queue_name: typing.Optional[builtins.str] = None,
        queue_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Reference to a queue.

        :param queue_arn: (experimental) The ARN of the queue.
        :param fifo: (experimental) Whether this queue is an Amazon SQS FIFO queue. If false, this is a standard queue. In case of a FIFO queue which is imported from a token, this value has to be explicitly set to true. Default: - if fifo is not specified, the property will be determined based on the queue name (not possible for FIFO queues imported from a token)
        :param key_arn: (experimental) KMS encryption key, if this queue is server-side encrypted by a KMS key. Default: - None
        :param queue_name: (experimental) The name of the queue. Default: if queue name is not specified, the name will be derived from the queue ARN
        :param queue_url: (experimental) The URL of the queue. Default: - 'https://sqs.//'

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sqs as sqs
            
            queue_attributes = sqs.QueueAttributes(
                queue_arn="queueArn",
            
                # the properties below are optional
                fifo=False,
                key_arn="keyArn",
                queue_name="queueName",
                queue_url="queueUrl"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a86fd4023b1edf299c17bde75d13a32296ed01e50bb66c97075101b4d6f843)
            check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
            check_type(argname="argument fifo", value=fifo, expected_type=type_hints["fifo"])
            check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queue_arn": queue_arn,
        }
        if fifo is not None:
            self._values["fifo"] = fifo
        if key_arn is not None:
            self._values["key_arn"] = key_arn
        if queue_name is not None:
            self._values["queue_name"] = queue_name
        if queue_url is not None:
            self._values["queue_url"] = queue_url

    @builtins.property
    def queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of the queue.

        :stability: experimental
        '''
        result = self._values.get("queue_arn")
        assert result is not None, "Required property 'queue_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fifo(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this queue is an Amazon SQS FIFO queue. If false, this is a standard queue.

        In case of a FIFO queue which is imported from a token, this value has to be explicitly set to true.

        :default: - if fifo is not specified, the property will be determined based on the queue name (not possible for FIFO queues imported from a token)

        :stability: experimental
        '''
        result = self._values.get("fifo")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) KMS encryption key, if this queue is server-side encrypted by a KMS key.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the queue.

        :default: if queue name is not specified, the name will be derived from the queue ARN

        :stability: experimental
        '''
        result = self._values.get("queue_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL of the queue.

        :default: - 'https://sqs.//'

        :see: https://docs.aws.amazon.com/sdk-for-net/v2/developer-guide/QueueURL.html
        :stability: experimental
        '''
        result = self._values.get("queue_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueueAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IQueue)
class QueueBase(
    _Resource_abff4495,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_sqs.QueueBase",
):
    '''(experimental) Reference to a new or existing Amazon SQS queue.

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
            type_hints = typing.get_type_hints(_typecheckingstub__23ab7dfd92a78e52492f76393421676e56f3dffa0de06d24e32d0378288d3d83)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _ResourceProps_9b554c0f(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this queue.

        If this queue was created in this stack (``new Queue``), a queue policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the queue is imported (``Queue.import``), then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84509b6ab26dbe9c5c77f8f9fb80a26f267d6625b729ebbe2d817aebea702b22)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the actions defined in queueActions to the identity Principal given on this SQS queue resource.

        :param grantee: Principal to grant right to.
        :param actions: The actions to grant.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56559880b2a252730d737ba618e13691568dc1aa52c3da19d175f20e6b275b95)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant permissions to consume messages from a queue.

        This will grant the following permissions:

        - sqs:ChangeMessageVisibility
        - sqs:DeleteMessage
        - sqs:ReceiveMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant consume rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e9000e1bae36681297ba807ab97b9eedd71438d90b74b07b09f4809eef82f3)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantConsumeMessages", [grantee]))

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant an IAM principal permissions to purge all messages from the queue.

        This will grant the following permissions:

        - sqs:PurgeQueue
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b8dde73162cebe0cb64ed9abc4fa73027f046143aebe2b9e6f2b1c3b978bd9)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPurge", [grantee]))

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to send messages to a queue to the given identity.

        This will grant the following permissions:

        - sqs:SendMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba3115b73e0fff7fa3b33e421e2d2a3d7d1b25be8aa41e28a4111f77582d6b0)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantSendMessages", [grantee]))

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
        '''(experimental) Return the given named metric for this Queue.

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
            type_hints = typing.get_type_hints(_typecheckingstub__3bff84db8502e388e7bd7a01717dc870a8661019991a47ab3391cd8ff090fcaa)
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

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(
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
        '''(experimental) The approximate age of the oldest non-deleted message in the queue.

        Maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricApproximateAgeOfOldestMessage", [props]))

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(
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
        '''(experimental) The number of messages in the queue that are delayed and not available for reading immediately.

        Maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricApproximateNumberOfMessagesDelayed", [props]))

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(
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
        '''(experimental) The number of messages that are in flight.

        Maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricApproximateNumberOfMessagesNotVisible", [props]))

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(
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
        '''(experimental) The number of messages available for retrieval from the queue.

        Maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricApproximateNumberOfMessagesVisible", [props]))

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(
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
        '''(experimental) The number of ReceiveMessage API calls that did not return a message.

        Sum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfEmptyReceives", [props]))

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(
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
        '''(experimental) The number of messages deleted from the queue.

        Sum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfMessagesDeleted", [props]))

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(
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
        '''(experimental) The number of messages returned by calls to the ReceiveMessage action.

        Sum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfMessagesReceived", [props]))

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(
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
        '''(experimental) The number of messages added to a queue.

        Sum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfMessagesSent", [props]))

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(
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
        '''(experimental) The size of messages added to a queue.

        Average over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSentMessageSize", [props]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Controls automatic creation of policy objects.

        Set by subclasses.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="fifo")
    @abc.abstractmethod
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    @abc.abstractmethod
    def queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this queue.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="queueName")
    @abc.abstractmethod
    def queue_name(self) -> builtins.str:
        '''(experimental) The name of this queue.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    @abc.abstractmethod
    def queue_url(self) -> builtins.str:
        '''(experimental) The URL of this queue.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    @abc.abstractmethod
    def encryption_master_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) If this queue is server-side encrypted, this is the KMS encryption key.

        :stability: experimental
        '''
        ...


class _QueueBaseProxy(
    QueueBase,
    jsii.proxy_for(_Resource_abff4495), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Controls automatic creation of policy objects.

        Set by subclasses.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "fifo"))

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this queue.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueArn"))

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        '''(experimental) The name of this queue.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> builtins.str:
        '''(experimental) The URL of this queue.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueUrl"))

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) If this queue is server-side encrypted, this is the KMS encryption key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionMasterKey"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, QueueBase).__jsii_proxy_class__ = lambda : _QueueBaseProxy


@jsii.enum(jsii_type="monocdk.aws_sqs.QueueEncryption")
class QueueEncryption(enum.Enum):
    '''(experimental) What kind of encryption to apply to this queue.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Use managed key
        sqs.Queue(self, "Queue",
            encryption=sqs.QueueEncryption.KMS_MANAGED
        )
        
        # Use custom key
        my_key = kms.Key(self, "Key")
        
        sqs.Queue(self, "Queue",
            encryption=sqs.QueueEncryption.KMS,
            encryption_master_key=my_key
        )
    '''

    UNENCRYPTED = "UNENCRYPTED"
    '''(experimental) Messages in the queue are not encrypted.

    :stability: experimental
    '''
    KMS_MANAGED = "KMS_MANAGED"
    '''(experimental) Server-side KMS encryption with a master key managed by SQS.

    :stability: experimental
    '''
    KMS = "KMS"
    '''(experimental) Server-side encryption with a KMS key managed by the user.

    If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.

    :stability: experimental
    '''


class QueuePolicy(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sqs.QueuePolicy",
):
    '''(experimental) The policy for an SQS Queue.

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
        from monocdk import aws_sqs as sqs
        
        # queue: sqs.Queue
        
        queue_policy = sqs.QueuePolicy(self, "MyQueuePolicy",
            queues=[queue]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        queues: typing.Sequence[IQueue],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param queues: (experimental) The set of queues this policy applies to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3e9ec101c0b00df7a6922522e7d84d406b7d27d4c7bd829cbf35c958d911e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = QueuePolicyProps(queues=queues)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> _PolicyDocument_b5de5177:
        '''(experimental) The IAM policy document for this policy.

        :stability: experimental
        '''
        return typing.cast(_PolicyDocument_b5de5177, jsii.get(self, "document"))

    @builtins.property
    @jsii.member(jsii_name="queuePolicyId")
    def queue_policy_id(self) -> builtins.str:
        '''(experimental) Not currently supported by AWS CloudFormation.

        This attribute temporarily existed in CloudFormation, and then was removed again.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "queuePolicyId"))


@jsii.data_type(
    jsii_type="monocdk.aws_sqs.QueuePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"queues": "queues"},
)
class QueuePolicyProps:
    def __init__(self, *, queues: typing.Sequence[IQueue]) -> None:
        '''(experimental) Properties to associate SQS queues with a policy.

        :param queues: (experimental) The set of queues this policy applies to.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            
            queue_policy_props = sqs.QueuePolicyProps(
                queues=[queue]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9664aca6aa5631b3f8d4148ffa0a893fdee6ce81436ae211fd25081b6288126)
            check_type(argname="argument queues", value=queues, expected_type=type_hints["queues"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queues": queues,
        }

    @builtins.property
    def queues(self) -> typing.List[IQueue]:
        '''(experimental) The set of queues this policy applies to.

        :stability: experimental
        '''
        result = self._values.get("queues")
        assert result is not None, "Required property 'queues' is missing"
        return typing.cast(typing.List[IQueue], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueuePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sqs.QueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_based_deduplication": "contentBasedDeduplication",
        "data_key_reuse": "dataKeyReuse",
        "dead_letter_queue": "deadLetterQueue",
        "deduplication_scope": "deduplicationScope",
        "delivery_delay": "deliveryDelay",
        "encryption": "encryption",
        "encryption_master_key": "encryptionMasterKey",
        "fifo": "fifo",
        "fifo_throughput_limit": "fifoThroughputLimit",
        "max_message_size_bytes": "maxMessageSizeBytes",
        "queue_name": "queueName",
        "receive_message_wait_time": "receiveMessageWaitTime",
        "removal_policy": "removalPolicy",
        "retention_period": "retentionPeriod",
        "visibility_timeout": "visibilityTimeout",
    },
)
class QueueProps:
    def __init__(
        self,
        *,
        content_based_deduplication: typing.Optional[builtins.bool] = None,
        data_key_reuse: typing.Optional[_Duration_070aa057] = None,
        dead_letter_queue: typing.Optional[typing.Union[DeadLetterQueue, typing.Dict[builtins.str, typing.Any]]] = None,
        deduplication_scope: typing.Optional[DeduplicationScope] = None,
        delivery_delay: typing.Optional[_Duration_070aa057] = None,
        encryption: typing.Optional[QueueEncryption] = None,
        encryption_master_key: typing.Optional[_IKey_36930160] = None,
        fifo: typing.Optional[builtins.bool] = None,
        fifo_throughput_limit: typing.Optional[FifoThroughputLimit] = None,
        max_message_size_bytes: typing.Optional[jsii.Number] = None,
        queue_name: typing.Optional[builtins.str] = None,
        receive_message_wait_time: typing.Optional[_Duration_070aa057] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        retention_period: typing.Optional[_Duration_070aa057] = None,
        visibility_timeout: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) Properties for creating a new Queue.

        :param content_based_deduplication: (experimental) Specifies whether to enable content-based deduplication. During the deduplication interval (5 minutes), Amazon SQS treats messages that are sent with identical content (excluding attributes) as duplicates and delivers only one copy of the message. If you don't enable content-based deduplication and you want to deduplicate messages, provide an explicit deduplication ID in your SendMessage() call. (Only applies to FIFO queues.) Default: false
        :param data_key_reuse: (experimental) The length of time that Amazon SQS reuses a data key before calling KMS again. The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes). Default: Duration.minutes(5)
        :param dead_letter_queue: (experimental) Send messages to this queue if they were unsuccessfully dequeued a number of times. Default: no dead-letter queue
        :param deduplication_scope: (experimental) For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level. (Only applies to FIFO queues.) Default: DeduplicationScope.QUEUE
        :param delivery_delay: (experimental) The time in seconds that the delivery of all messages in the queue is delayed. You can specify an integer value of 0 to 900 (15 minutes). The default value is 0. Default: 0
        :param encryption: (experimental) Whether the contents of the queue are encrypted, and by what type of key. Be aware that encryption is not available in all regions, please see the docs for current availability details. Default: Unencrypted
        :param encryption_master_key: (experimental) External KMS master key to use for queue encryption. Individual messages will be encrypted using data keys. The data keys in turn will be encrypted using this key, and reused for a maximum of ``dataKeyReuseSecs`` seconds. If the 'encryptionMasterKey' property is set, 'encryption' type will be implicitly set to "KMS". Default: If encryption is set to KMS and not specified, a key will be created.
        :param fifo: (experimental) Whether this a first-in-first-out (FIFO) queue. Default: false, unless queueName ends in '.fifo' or 'contentBasedDeduplication' is true.
        :param fifo_throughput_limit: (experimental) For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group. (Only applies to FIFO queues.) Default: FifoThroughputLimit.PER_QUEUE
        :param max_message_size_bytes: (experimental) The limit of how many bytes that a message can contain before Amazon SQS rejects it. You can specify an integer value from 1024 bytes (1 KiB) to 262144 bytes (256 KiB). The default value is 262144 (256 KiB). Default: 256KiB
        :param queue_name: (experimental) A name for the queue. If specified and this is a FIFO queue, must end in the string '.fifo'. Default: CloudFormation-generated name
        :param receive_message_wait_time: (experimental) Default wait time for ReceiveMessage calls. Does not wait if set to 0, otherwise waits this amount of seconds by default for messages to arrive. For more information, see Amazon SQS Long Poll. Default: 0
        :param removal_policy: (experimental) Policy to apply when the queue is removed from the stack. Even though queues are technically stateful, their contents are transient and it is common to add and remove Queues while rearchitecting your application. The default is therefore ``DESTROY``. Change it to ``RETAIN`` if the messages are so valuable that accidentally losing them would be unacceptable. Default: RemovalPolicy.DESTROY
        :param retention_period: (experimental) The number of seconds that Amazon SQS retains a message. You can specify an integer value from 60 seconds (1 minute) to 1209600 seconds (14 days). The default value is 345600 seconds (4 days). Default: Duration.days(4)
        :param visibility_timeout: (experimental) Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be from 0 to 43200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds. Default: Duration.seconds(30)

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Use managed key
            sqs.Queue(self, "Queue",
                encryption=sqs.QueueEncryption.KMS_MANAGED
            )
            
            # Use custom key
            my_key = kms.Key(self, "Key")
            
            sqs.Queue(self, "Queue",
                encryption=sqs.QueueEncryption.KMS,
                encryption_master_key=my_key
            )
        '''
        if isinstance(dead_letter_queue, dict):
            dead_letter_queue = DeadLetterQueue(**dead_letter_queue)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df77686ddc181af44734d8cf09c96a903f68e09db85cc64f2697c872ce9d6297)
            check_type(argname="argument content_based_deduplication", value=content_based_deduplication, expected_type=type_hints["content_based_deduplication"])
            check_type(argname="argument data_key_reuse", value=data_key_reuse, expected_type=type_hints["data_key_reuse"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument deduplication_scope", value=deduplication_scope, expected_type=type_hints["deduplication_scope"])
            check_type(argname="argument delivery_delay", value=delivery_delay, expected_type=type_hints["delivery_delay"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_master_key", value=encryption_master_key, expected_type=type_hints["encryption_master_key"])
            check_type(argname="argument fifo", value=fifo, expected_type=type_hints["fifo"])
            check_type(argname="argument fifo_throughput_limit", value=fifo_throughput_limit, expected_type=type_hints["fifo_throughput_limit"])
            check_type(argname="argument max_message_size_bytes", value=max_message_size_bytes, expected_type=type_hints["max_message_size_bytes"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument receive_message_wait_time", value=receive_message_wait_time, expected_type=type_hints["receive_message_wait_time"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument visibility_timeout", value=visibility_timeout, expected_type=type_hints["visibility_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_based_deduplication is not None:
            self._values["content_based_deduplication"] = content_based_deduplication
        if data_key_reuse is not None:
            self._values["data_key_reuse"] = data_key_reuse
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if deduplication_scope is not None:
            self._values["deduplication_scope"] = deduplication_scope
        if delivery_delay is not None:
            self._values["delivery_delay"] = delivery_delay
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_master_key is not None:
            self._values["encryption_master_key"] = encryption_master_key
        if fifo is not None:
            self._values["fifo"] = fifo
        if fifo_throughput_limit is not None:
            self._values["fifo_throughput_limit"] = fifo_throughput_limit
        if max_message_size_bytes is not None:
            self._values["max_message_size_bytes"] = max_message_size_bytes
        if queue_name is not None:
            self._values["queue_name"] = queue_name
        if receive_message_wait_time is not None:
            self._values["receive_message_wait_time"] = receive_message_wait_time
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if visibility_timeout is not None:
            self._values["visibility_timeout"] = visibility_timeout

    @builtins.property
    def content_based_deduplication(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable content-based deduplication.

        During the deduplication interval (5 minutes), Amazon SQS treats
        messages that are sent with identical content (excluding attributes) as
        duplicates and delivers only one copy of the message.

        If you don't enable content-based deduplication and you want to deduplicate
        messages, provide an explicit deduplication ID in your SendMessage() call.

        (Only applies to FIFO queues.)

        :default: false

        :stability: experimental
        '''
        result = self._values.get("content_based_deduplication")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def data_key_reuse(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The length of time that Amazon SQS reuses a data key before calling KMS again.

        The value must be an integer between 60 (1 minute) and 86,400 (24
        hours). The default is 300 (5 minutes).

        :default: Duration.minutes(5)

        :stability: experimental
        '''
        result = self._values.get("data_key_reuse")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[DeadLetterQueue]:
        '''(experimental) Send messages to this queue if they were unsuccessfully dequeued a number of times.

        :default: no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[DeadLetterQueue], result)

    @builtins.property
    def deduplication_scope(self) -> typing.Optional[DeduplicationScope]:
        '''(experimental) For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level.

        (Only applies to FIFO queues.)

        :default: DeduplicationScope.QUEUE

        :stability: experimental
        '''
        result = self._values.get("deduplication_scope")
        return typing.cast(typing.Optional[DeduplicationScope], result)

    @builtins.property
    def delivery_delay(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The time in seconds that the delivery of all messages in the queue is delayed.

        You can specify an integer value of 0 to 900 (15 minutes). The default
        value is 0.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("delivery_delay")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def encryption(self) -> typing.Optional[QueueEncryption]:
        '''(experimental) Whether the contents of the queue are encrypted, and by what type of key.

        Be aware that encryption is not available in all regions, please see the docs
        for current availability details.

        :default: Unencrypted

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[QueueEncryption], result)

    @builtins.property
    def encryption_master_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) External KMS master key to use for queue encryption.

        Individual messages will be encrypted using data keys. The data keys in
        turn will be encrypted using this key, and reused for a maximum of
        ``dataKeyReuseSecs`` seconds.

        If the 'encryptionMasterKey' property is set, 'encryption' type will be
        implicitly set to "KMS".

        :default: If encryption is set to KMS and not specified, a key will be created.

        :stability: experimental
        '''
        result = self._values.get("encryption_master_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def fifo(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this a first-in-first-out (FIFO) queue.

        :default: false, unless queueName ends in '.fifo' or 'contentBasedDeduplication' is true.

        :stability: experimental
        '''
        result = self._values.get("fifo")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fifo_throughput_limit(self) -> typing.Optional[FifoThroughputLimit]:
        '''(experimental) For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group.

        (Only applies to FIFO queues.)

        :default: FifoThroughputLimit.PER_QUEUE

        :stability: experimental
        '''
        result = self._values.get("fifo_throughput_limit")
        return typing.cast(typing.Optional[FifoThroughputLimit], result)

    @builtins.property
    def max_message_size_bytes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The limit of how many bytes that a message can contain before Amazon SQS rejects it.

        You can specify an integer value from 1024 bytes (1 KiB) to 262144 bytes
        (256 KiB). The default value is 262144 (256 KiB).

        :default: 256KiB

        :stability: experimental
        '''
        result = self._values.get("max_message_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the queue.

        If specified and this is a FIFO queue, must end in the string '.fifo'.

        :default: CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("queue_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def receive_message_wait_time(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Default wait time for ReceiveMessage calls.

        Does not wait if set to 0, otherwise waits this amount of seconds
        by default for messages to arrive.

        For more information, see Amazon SQS Long Poll.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("receive_message_wait_time")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Policy to apply when the queue is removed from the stack.

        Even though queues are technically stateful, their contents are transient and it
        is common to add and remove Queues while rearchitecting your application. The
        default is therefore ``DESTROY``. Change it to ``RETAIN`` if the messages are so
        valuable that accidentally losing them would be unacceptable.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The number of seconds that Amazon SQS retains a message.

        You can specify an integer value from 60 seconds (1 minute) to 1209600
        seconds (14 days). The default value is 345600 seconds (4 days).

        :default: Duration.days(4)

        :stability: experimental
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def visibility_timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Timeout of processing a single message.

        After dequeuing, the processor has this much time to handle the message
        and delete it from the queue before it becomes visible again for dequeueing
        by another processor.

        Values must be from 0 to 43200 seconds (12 hours). If you don't specify
        a value, AWS CloudFormation uses the default value of 30 seconds.

        :default: Duration.seconds(30)

        :stability: experimental
        '''
        result = self._values.get("visibility_timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Queue(QueueBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_sqs.Queue"):
    '''(experimental) A new Amazon SQS queue.

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

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        content_based_deduplication: typing.Optional[builtins.bool] = None,
        data_key_reuse: typing.Optional[_Duration_070aa057] = None,
        dead_letter_queue: typing.Optional[typing.Union[DeadLetterQueue, typing.Dict[builtins.str, typing.Any]]] = None,
        deduplication_scope: typing.Optional[DeduplicationScope] = None,
        delivery_delay: typing.Optional[_Duration_070aa057] = None,
        encryption: typing.Optional[QueueEncryption] = None,
        encryption_master_key: typing.Optional[_IKey_36930160] = None,
        fifo: typing.Optional[builtins.bool] = None,
        fifo_throughput_limit: typing.Optional[FifoThroughputLimit] = None,
        max_message_size_bytes: typing.Optional[jsii.Number] = None,
        queue_name: typing.Optional[builtins.str] = None,
        receive_message_wait_time: typing.Optional[_Duration_070aa057] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        retention_period: typing.Optional[_Duration_070aa057] = None,
        visibility_timeout: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param content_based_deduplication: (experimental) Specifies whether to enable content-based deduplication. During the deduplication interval (5 minutes), Amazon SQS treats messages that are sent with identical content (excluding attributes) as duplicates and delivers only one copy of the message. If you don't enable content-based deduplication and you want to deduplicate messages, provide an explicit deduplication ID in your SendMessage() call. (Only applies to FIFO queues.) Default: false
        :param data_key_reuse: (experimental) The length of time that Amazon SQS reuses a data key before calling KMS again. The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes). Default: Duration.minutes(5)
        :param dead_letter_queue: (experimental) Send messages to this queue if they were unsuccessfully dequeued a number of times. Default: no dead-letter queue
        :param deduplication_scope: (experimental) For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level. (Only applies to FIFO queues.) Default: DeduplicationScope.QUEUE
        :param delivery_delay: (experimental) The time in seconds that the delivery of all messages in the queue is delayed. You can specify an integer value of 0 to 900 (15 minutes). The default value is 0. Default: 0
        :param encryption: (experimental) Whether the contents of the queue are encrypted, and by what type of key. Be aware that encryption is not available in all regions, please see the docs for current availability details. Default: Unencrypted
        :param encryption_master_key: (experimental) External KMS master key to use for queue encryption. Individual messages will be encrypted using data keys. The data keys in turn will be encrypted using this key, and reused for a maximum of ``dataKeyReuseSecs`` seconds. If the 'encryptionMasterKey' property is set, 'encryption' type will be implicitly set to "KMS". Default: If encryption is set to KMS and not specified, a key will be created.
        :param fifo: (experimental) Whether this a first-in-first-out (FIFO) queue. Default: false, unless queueName ends in '.fifo' or 'contentBasedDeduplication' is true.
        :param fifo_throughput_limit: (experimental) For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group. (Only applies to FIFO queues.) Default: FifoThroughputLimit.PER_QUEUE
        :param max_message_size_bytes: (experimental) The limit of how many bytes that a message can contain before Amazon SQS rejects it. You can specify an integer value from 1024 bytes (1 KiB) to 262144 bytes (256 KiB). The default value is 262144 (256 KiB). Default: 256KiB
        :param queue_name: (experimental) A name for the queue. If specified and this is a FIFO queue, must end in the string '.fifo'. Default: CloudFormation-generated name
        :param receive_message_wait_time: (experimental) Default wait time for ReceiveMessage calls. Does not wait if set to 0, otherwise waits this amount of seconds by default for messages to arrive. For more information, see Amazon SQS Long Poll. Default: 0
        :param removal_policy: (experimental) Policy to apply when the queue is removed from the stack. Even though queues are technically stateful, their contents are transient and it is common to add and remove Queues while rearchitecting your application. The default is therefore ``DESTROY``. Change it to ``RETAIN`` if the messages are so valuable that accidentally losing them would be unacceptable. Default: RemovalPolicy.DESTROY
        :param retention_period: (experimental) The number of seconds that Amazon SQS retains a message. You can specify an integer value from 60 seconds (1 minute) to 1209600 seconds (14 days). The default value is 345600 seconds (4 days). Default: Duration.days(4)
        :param visibility_timeout: (experimental) Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be from 0 to 43200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds. Default: Duration.seconds(30)

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e10214bb4ae1d2b659b1a832cb5e2f23d35aced4c4b220d5e093991fad80bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = QueueProps(
            content_based_deduplication=content_based_deduplication,
            data_key_reuse=data_key_reuse,
            dead_letter_queue=dead_letter_queue,
            deduplication_scope=deduplication_scope,
            delivery_delay=delivery_delay,
            encryption=encryption,
            encryption_master_key=encryption_master_key,
            fifo=fifo,
            fifo_throughput_limit=fifo_throughput_limit,
            max_message_size_bytes=max_message_size_bytes,
            queue_name=queue_name,
            receive_message_wait_time=receive_message_wait_time,
            removal_policy=removal_policy,
            retention_period=retention_period,
            visibility_timeout=visibility_timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromQueueArn")
    @builtins.classmethod
    def from_queue_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        queue_arn: builtins.str,
    ) -> IQueue:
        '''(experimental) Import an existing SQS queue provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param queue_arn: queue ARN (i.e. arn:aws:sqs:us-east-2:444455556666:queue1).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b97e93b39a794752ecfbec32d0ab270d2dbf6bcc2c2ce30d2c206421915150)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
        return typing.cast(IQueue, jsii.sinvoke(cls, "fromQueueArn", [scope, id, queue_arn]))

    @jsii.member(jsii_name="fromQueueAttributes")
    @builtins.classmethod
    def from_queue_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        queue_arn: builtins.str,
        fifo: typing.Optional[builtins.bool] = None,
        key_arn: typing.Optional[builtins.str] = None,
        queue_name: typing.Optional[builtins.str] = None,
        queue_url: typing.Optional[builtins.str] = None,
    ) -> IQueue:
        '''(experimental) Import an existing queue.

        :param scope: -
        :param id: -
        :param queue_arn: (experimental) The ARN of the queue.
        :param fifo: (experimental) Whether this queue is an Amazon SQS FIFO queue. If false, this is a standard queue. In case of a FIFO queue which is imported from a token, this value has to be explicitly set to true. Default: - if fifo is not specified, the property will be determined based on the queue name (not possible for FIFO queues imported from a token)
        :param key_arn: (experimental) KMS encryption key, if this queue is server-side encrypted by a KMS key. Default: - None
        :param queue_name: (experimental) The name of the queue. Default: if queue name is not specified, the name will be derived from the queue ARN
        :param queue_url: (experimental) The URL of the queue. Default: - 'https://sqs.//'

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799c0d2ecc369af14eac01004089459dc48317c55bbb906129f7de1fe8b47712)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = QueueAttributes(
            queue_arn=queue_arn,
            fifo=fifo,
            key_arn=key_arn,
            queue_name=queue_name,
            queue_url=queue_url,
        )

        return typing.cast(IQueue, jsii.sinvoke(cls, "fromQueueAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Controls automatic creation of policy objects.

        Set by subclasses.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "fifo"))

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this queue.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueArn"))

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        '''(experimental) The name of this queue.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> builtins.str:
        '''(experimental) The URL of this queue.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "queueUrl"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[DeadLetterQueue]:
        '''(experimental) If this queue is configured with a dead-letter queue, this is the dead-letter queue settings.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[DeadLetterQueue], jsii.get(self, "deadLetterQueue"))

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) If this queue is encrypted, this is the KMS key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionMasterKey"))


__all__ = [
    "CfnQueue",
    "CfnQueuePolicy",
    "CfnQueuePolicyProps",
    "CfnQueueProps",
    "DeadLetterQueue",
    "DeduplicationScope",
    "FifoThroughputLimit",
    "IQueue",
    "Queue",
    "QueueAttributes",
    "QueueBase",
    "QueueEncryption",
    "QueuePolicy",
    "QueuePolicyProps",
    "QueueProps",
]

publication.publish()

def _typecheckingstub__1b966f857467dc3eca3b20bcf8645d8fdbf83c8f0e6d6f487caec321b15e4fa2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    deduplication_scope: typing.Optional[builtins.str] = None,
    delay_seconds: typing.Optional[jsii.Number] = None,
    fifo_queue: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    fifo_throughput_limit: typing.Optional[builtins.str] = None,
    kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    maximum_message_size: typing.Optional[jsii.Number] = None,
    message_retention_period: typing.Optional[jsii.Number] = None,
    queue_name: typing.Optional[builtins.str] = None,
    receive_message_wait_time_seconds: typing.Optional[jsii.Number] = None,
    redrive_allow_policy: typing.Any = None,
    redrive_policy: typing.Any = None,
    sqs_managed_sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    visibility_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc24cb6372f95fb7aba43666df8950478848424c62f84060708e9f1766788d40(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ce696eb25b3637569ee84e933254bbe73df611506638e4e9ccab1a856c97e0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6c34eae64fadbfb7b7b53d8cca14ad0b48ee2042a3ef365873bb429eb43dae(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800c15898da5aad1a8be95ea7df7bd5d7ee559bed7dc47af9e55af895a546b6e(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb5063294bcf65631c98d9c690b176401dd1bf332d6ddfc38666d135b740662(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0234687b26c1ab1e4eadf9e8b7e7b1656611c8a2fcd00ffd67ece7125f0c35(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9905c8e33d3b624e01c457c7ca954ba52b2fdabaff2c55155c0e5b55bcba6f57(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f019054afaa98471bda07a4bc80a39b073bb151d319e7dd90c7c05d621c81b1(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b44e254a10a43eb2b9ffddae3f0bbde0b25f1b4d685a268d1446378688388e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1766a21beef2e41883d097e9c658a0fada533df42b2c38a4ed7500afdedc32(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e58b673a1d0996e8a656c4a6d9f52d867e74330dd7d4c4035d195eabe3789a3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bec0d8792d725f4ecf22854700fcf319d30f21820c499d5f5dd86026473370(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5504e9f1b99db86e259b4b2cb2637ff5066727ee9fa42a8e88b6c1d92173cc6(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600ceee83b6c1f48825d04a8085b478b08e0ac31eb58ee92379d809f0b8e708a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9d8c5fc62afa3a6855e545e3169408779aca8791233fb963d369a9b7bac55e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5dbe47074fc3fab420b5c12f3b58350e4bb589f23a40e5fe439587219d97e47(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bfde971d36d9221effffd6812896622398d206473bb12f36e53dd33d397b36(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b460b4585e0e26fbf1e9482f8d0a2489e127775e1a336c204f216cdb3941cea4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy_document: typing.Any,
    queues: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c7bb97d9f6eeb6907f34bd1ff7902637a1be3bf26ad959c3ae41cd12e9c942(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec6a2d478a4ae539266b3c01207d2ab8b02228df3e5deca4976796ce8e9415e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a0d40235a94be1804049d5624b932ad77e2a347be58c35ee13d52a9f891764(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c313624f0694c7a6ab32b9209b29a517d9c889e2e3f782e2bfdff8ead3c81c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3686cbe3a3ab1fbd6b544bda75f42994de52e7608a442feb49881506cf4127(
    *,
    policy_document: typing.Any,
    queues: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644c014f03c653a9a83c75b626e118e690808f6a652c15a6c86cd474baa63480(
    *,
    content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    deduplication_scope: typing.Optional[builtins.str] = None,
    delay_seconds: typing.Optional[jsii.Number] = None,
    fifo_queue: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    fifo_throughput_limit: typing.Optional[builtins.str] = None,
    kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    maximum_message_size: typing.Optional[jsii.Number] = None,
    message_retention_period: typing.Optional[jsii.Number] = None,
    queue_name: typing.Optional[builtins.str] = None,
    receive_message_wait_time_seconds: typing.Optional[jsii.Number] = None,
    redrive_allow_policy: typing.Any = None,
    redrive_policy: typing.Any = None,
    sqs_managed_sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    visibility_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b2dcab57acc441eaa63ee634c2c8e5ac9295c94eb9266418ad3a5520b8848d(
    *,
    max_receive_count: jsii.Number,
    queue: IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157cf7572c38088b4b87e878ba341ee41a4c992de389fedf35a6d633c45add1f(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a7c5b38daa71e99641ce252abc9ccff3c3206cbd4abbfaec1b8a9201a29a5a(
    grantee: _IGrantable_4c5a91d1,
    *queue_actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd41af889216d3b9b20a10de3ae772f91cd70ebd2d4436f33eb5dd5ddb891b91(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e3d0525c7d13dc6521cf60ef8f5b4c94644764076e9700fef89019cb67c65c(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0675f749c5d860bfd6e2773128196db6eb2dc6d75173fe333973afdfbad172(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536893be1eb70ff1e34fb6a822c3dca0bfc89bd38da1961145970a7fc53ef54f(
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

def _typecheckingstub__63a86fd4023b1edf299c17bde75d13a32296ed01e50bb66c97075101b4d6f843(
    *,
    queue_arn: builtins.str,
    fifo: typing.Optional[builtins.bool] = None,
    key_arn: typing.Optional[builtins.str] = None,
    queue_name: typing.Optional[builtins.str] = None,
    queue_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ab7dfd92a78e52492f76393421676e56f3dffa0de06d24e32d0378288d3d83(
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

def _typecheckingstub__84509b6ab26dbe9c5c77f8f9fb80a26f267d6625b729ebbe2d817aebea702b22(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56559880b2a252730d737ba618e13691568dc1aa52c3da19d175f20e6b275b95(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e9000e1bae36681297ba807ab97b9eedd71438d90b74b07b09f4809eef82f3(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b8dde73162cebe0cb64ed9abc4fa73027f046143aebe2b9e6f2b1c3b978bd9(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba3115b73e0fff7fa3b33e421e2d2a3d7d1b25be8aa41e28a4111f77582d6b0(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bff84db8502e388e7bd7a01717dc870a8661019991a47ab3391cd8ff090fcaa(
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

def _typecheckingstub__fc3e9ec101c0b00df7a6922522e7d84d406b7d27d4c7bd829cbf35c958d911e3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    queues: typing.Sequence[IQueue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9664aca6aa5631b3f8d4148ffa0a893fdee6ce81436ae211fd25081b6288126(
    *,
    queues: typing.Sequence[IQueue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df77686ddc181af44734d8cf09c96a903f68e09db85cc64f2697c872ce9d6297(
    *,
    content_based_deduplication: typing.Optional[builtins.bool] = None,
    data_key_reuse: typing.Optional[_Duration_070aa057] = None,
    dead_letter_queue: typing.Optional[typing.Union[DeadLetterQueue, typing.Dict[builtins.str, typing.Any]]] = None,
    deduplication_scope: typing.Optional[DeduplicationScope] = None,
    delivery_delay: typing.Optional[_Duration_070aa057] = None,
    encryption: typing.Optional[QueueEncryption] = None,
    encryption_master_key: typing.Optional[_IKey_36930160] = None,
    fifo: typing.Optional[builtins.bool] = None,
    fifo_throughput_limit: typing.Optional[FifoThroughputLimit] = None,
    max_message_size_bytes: typing.Optional[jsii.Number] = None,
    queue_name: typing.Optional[builtins.str] = None,
    receive_message_wait_time: typing.Optional[_Duration_070aa057] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    retention_period: typing.Optional[_Duration_070aa057] = None,
    visibility_timeout: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e10214bb4ae1d2b659b1a832cb5e2f23d35aced4c4b220d5e093991fad80bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content_based_deduplication: typing.Optional[builtins.bool] = None,
    data_key_reuse: typing.Optional[_Duration_070aa057] = None,
    dead_letter_queue: typing.Optional[typing.Union[DeadLetterQueue, typing.Dict[builtins.str, typing.Any]]] = None,
    deduplication_scope: typing.Optional[DeduplicationScope] = None,
    delivery_delay: typing.Optional[_Duration_070aa057] = None,
    encryption: typing.Optional[QueueEncryption] = None,
    encryption_master_key: typing.Optional[_IKey_36930160] = None,
    fifo: typing.Optional[builtins.bool] = None,
    fifo_throughput_limit: typing.Optional[FifoThroughputLimit] = None,
    max_message_size_bytes: typing.Optional[jsii.Number] = None,
    queue_name: typing.Optional[builtins.str] = None,
    receive_message_wait_time: typing.Optional[_Duration_070aa057] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    retention_period: typing.Optional[_Duration_070aa057] = None,
    visibility_timeout: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b97e93b39a794752ecfbec32d0ab270d2dbf6bcc2c2ce30d2c206421915150(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    queue_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799c0d2ecc369af14eac01004089459dc48317c55bbb906129f7de1fe8b47712(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    queue_arn: builtins.str,
    fifo: typing.Optional[builtins.bool] = None,
    key_arn: typing.Optional[builtins.str] = None,
    queue_name: typing.Optional[builtins.str] = None,
    queue_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
