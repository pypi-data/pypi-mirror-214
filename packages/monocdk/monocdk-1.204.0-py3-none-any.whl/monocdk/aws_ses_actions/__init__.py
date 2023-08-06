'''
# Amazon Simple Email Service Actions Library

This module contains integration classes to add action to SES email receiving rules.
Instances of these classes should be passed to the `rule.addAction()` method.

Currently supported are:

* [Add header](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-add-header.html)
* [Bounce](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-bounce.html)
* [Lambda](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-lambda.html)
* [S3](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-s3.html)
* [SNS](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-sns.html)
* [Stop](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-stop.html)

See the README of `@aws-cdk/aws-ses` for more information.
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

from ..aws_kms import IKey as _IKey_36930160
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_s3 import IBucket as _IBucket_73486e29
from ..aws_ses import (
    IReceiptRule as _IReceiptRule_77e30645,
    IReceiptRuleAction as _IReceiptRuleAction_4e833cf2,
    ReceiptRuleActionConfig as _ReceiptRuleActionConfig_c996e325,
)
from ..aws_sns import ITopic as _ITopic_465e36b9


@jsii.implements(_IReceiptRuleAction_4e833cf2)
class AddHeader(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_ses_actions.AddHeader"):
    '''(experimental) Adds a header to the received email.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as s3
        import monocdk as actions
        
        
        bucket = s3.Bucket(self, "Bucket")
        topic = sns.Topic(self, "Topic")
        
        ses.ReceiptRuleSet(self, "RuleSet",
            rules=[s3.aws_ses.ReceiptRuleOptions(
                recipients=["hello@aws.com"],
                actions=[
                    actions.AddHeader(
                        name="X-Special-Header",
                        value="aws"
                    ),
                    actions.S3(
                        bucket=bucket,
                        object_key_prefix="emails/",
                        topic=topic
                    )
                ]
            ), s3.aws_ses.ReceiptRuleOptions(
                recipients=["aws.com"],
                actions=[
                    actions.Sns(
                        topic=topic
                    )
                ]
            )
            ]
        )
    '''

    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: (experimental) The name of the header to add. Must be between 1 and 50 characters, inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters and dashes only.
        :param value: (experimental) The value of the header to add. Must be less than 2048 characters, and must not contain newline characters ("\\r" or "\\n").

        :stability: experimental
        '''
        props = AddHeaderProps(name=name, value=value)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IReceiptRule_77e30645) -> _ReceiptRuleActionConfig_c996e325:
        '''(experimental) Returns the receipt rule action specification.

        :param _rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0316d9aec8e1be8ef153705c92deef7054a2038013165f0ecb1f78e462e0f40)
            check_type(argname="argument _rule", value=_rule, expected_type=type_hints["_rule"])
        return typing.cast(_ReceiptRuleActionConfig_c996e325, jsii.invoke(self, "bind", [_rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_ses_actions.AddHeaderProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class AddHeaderProps:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Construction properties for a add header action.

        :param name: (experimental) The name of the header to add. Must be between 1 and 50 characters, inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters and dashes only.
        :param value: (experimental) The value of the header to add. Must be less than 2048 characters, and must not contain newline characters ("\\r" or "\\n").

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as s3
            import monocdk as actions
            
            
            bucket = s3.Bucket(self, "Bucket")
            topic = sns.Topic(self, "Topic")
            
            ses.ReceiptRuleSet(self, "RuleSet",
                rules=[s3.aws_ses.ReceiptRuleOptions(
                    recipients=["hello@aws.com"],
                    actions=[
                        actions.AddHeader(
                            name="X-Special-Header",
                            value="aws"
                        ),
                        actions.S3(
                            bucket=bucket,
                            object_key_prefix="emails/",
                            topic=topic
                        )
                    ]
                ), s3.aws_ses.ReceiptRuleOptions(
                    recipients=["aws.com"],
                    actions=[
                        actions.Sns(
                            topic=topic
                        )
                    ]
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312b3bc1a8b5a5742c3ab66700aab60215ff3c6216fff28554139d317950549e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the header to add.

        Must be between 1 and 50 characters,
        inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters
        and dashes only.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) The value of the header to add.

        Must be less than 2048 characters,
        and must not contain newline characters ("\\r" or "\\n").

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddHeaderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IReceiptRuleAction_4e833cf2)
class Bounce(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_ses_actions.Bounce"):
    '''(experimental) Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon SNS.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_ses_actions as ses_actions
        from monocdk import aws_sns as sns
        
        # bounce_template: ses_actions.BounceTemplate
        # topic: sns.Topic
        
        bounce = ses_actions.Bounce(
            sender="sender",
            template=bounce_template,
        
            # the properties below are optional
            topic=topic
        )
    '''

    def __init__(
        self,
        *,
        sender: builtins.str,
        template: "BounceTemplate",
        topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''
        :param sender: (experimental) The email address of the sender of the bounced email. This is the address from which the bounce message will be sent.
        :param template: (experimental) The template containing the message, reply code and status code.
        :param topic: (experimental) The SNS topic to notify when the bounce action is taken. Default: no notification

        :stability: experimental
        '''
        props = BounceProps(sender=sender, template=template, topic=topic)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IReceiptRule_77e30645) -> _ReceiptRuleActionConfig_c996e325:
        '''(experimental) Returns the receipt rule action specification.

        :param _rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5314c8a8d47493a81baa553a3c140237eb9558dd9e285a10fd3003ab6fea3a56)
            check_type(argname="argument _rule", value=_rule, expected_type=type_hints["_rule"])
        return typing.cast(_ReceiptRuleActionConfig_c996e325, jsii.invoke(self, "bind", [_rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_ses_actions.BounceProps",
    jsii_struct_bases=[],
    name_mapping={"sender": "sender", "template": "template", "topic": "topic"},
)
class BounceProps:
    def __init__(
        self,
        *,
        sender: builtins.str,
        template: "BounceTemplate",
        topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''(experimental) Construction properties for a bounce action.

        :param sender: (experimental) The email address of the sender of the bounced email. This is the address from which the bounce message will be sent.
        :param template: (experimental) The template containing the message, reply code and status code.
        :param topic: (experimental) The SNS topic to notify when the bounce action is taken. Default: no notification

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_ses_actions as ses_actions
            from monocdk import aws_sns as sns
            
            # bounce_template: ses_actions.BounceTemplate
            # topic: sns.Topic
            
            bounce_props = ses_actions.BounceProps(
                sender="sender",
                template=bounce_template,
            
                # the properties below are optional
                topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd2e339732b4a70272c4ec018a8d29d916aa2b3e25cb1708975c11e8dec6b0f)
            check_type(argname="argument sender", value=sender, expected_type=type_hints["sender"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sender": sender,
            "template": template,
        }
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def sender(self) -> builtins.str:
        '''(experimental) The email address of the sender of the bounced email.

        This is the address
        from which the bounce message will be sent.

        :stability: experimental
        '''
        result = self._values.get("sender")
        assert result is not None, "Required property 'sender' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> "BounceTemplate":
        '''(experimental) The template containing the message, reply code and status code.

        :stability: experimental
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("BounceTemplate", result)

    @builtins.property
    def topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) The SNS topic to notify when the bounce action is taken.

        :default: no notification

        :stability: experimental
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BounceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BounceTemplate(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ses_actions.BounceTemplate",
):
    '''(experimental) A bounce template.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_ses_actions as ses_actions
        
        bounce_template = ses_actions.BounceTemplate.MAILBOX_DOES_NOT_EXIST
    '''

    def __init__(
        self,
        *,
        message: builtins.str,
        smtp_reply_code: builtins.str,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: (experimental) Human-readable text to include in the bounce message.
        :param smtp_reply_code: (experimental) The SMTP reply code, as defined by RFC 5321.
        :param status_code: (experimental) The SMTP enhanced status code, as defined by RFC 3463.

        :stability: experimental
        '''
        props = BounceTemplateProps(
            message=message, smtp_reply_code=smtp_reply_code, status_code=status_code
        )

        jsii.create(self.__class__, self, [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAILBOX_DOES_NOT_EXIST")
    def MAILBOX_DOES_NOT_EXIST(cls) -> "BounceTemplate":
        '''
        :stability: experimental
        '''
        return typing.cast("BounceTemplate", jsii.sget(cls, "MAILBOX_DOES_NOT_EXIST"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAILBOX_FULL")
    def MAILBOX_FULL(cls) -> "BounceTemplate":
        '''
        :stability: experimental
        '''
        return typing.cast("BounceTemplate", jsii.sget(cls, "MAILBOX_FULL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MESSAGE_CONTENT_REJECTED")
    def MESSAGE_CONTENT_REJECTED(cls) -> "BounceTemplate":
        '''
        :stability: experimental
        '''
        return typing.cast("BounceTemplate", jsii.sget(cls, "MESSAGE_CONTENT_REJECTED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MESSAGE_TOO_LARGE")
    def MESSAGE_TOO_LARGE(cls) -> "BounceTemplate":
        '''
        :stability: experimental
        '''
        return typing.cast("BounceTemplate", jsii.sget(cls, "MESSAGE_TOO_LARGE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TEMPORARY_FAILURE")
    def TEMPORARY_FAILURE(cls) -> "BounceTemplate":
        '''
        :stability: experimental
        '''
        return typing.cast("BounceTemplate", jsii.sget(cls, "TEMPORARY_FAILURE"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "BounceTemplateProps":
        '''
        :stability: experimental
        '''
        return typing.cast("BounceTemplateProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="monocdk.aws_ses_actions.BounceTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "message": "message",
        "smtp_reply_code": "smtpReplyCode",
        "status_code": "statusCode",
    },
)
class BounceTemplateProps:
    def __init__(
        self,
        *,
        message: builtins.str,
        smtp_reply_code: builtins.str,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties for a BounceTemplate.

        :param message: (experimental) Human-readable text to include in the bounce message.
        :param smtp_reply_code: (experimental) The SMTP reply code, as defined by RFC 5321.
        :param status_code: (experimental) The SMTP enhanced status code, as defined by RFC 3463.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_ses_actions as ses_actions
            
            bounce_template_props = ses_actions.BounceTemplateProps(
                message="message",
                smtp_reply_code="smtpReplyCode",
            
                # the properties below are optional
                status_code="statusCode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5129053407ae2ad320f3c264501c5c3bc0f1dbc7d651e502e787c323021577)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument smtp_reply_code", value=smtp_reply_code, expected_type=type_hints["smtp_reply_code"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
            "smtp_reply_code": smtp_reply_code,
        }
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def message(self) -> builtins.str:
        '''(experimental) Human-readable text to include in the bounce message.

        :stability: experimental
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def smtp_reply_code(self) -> builtins.str:
        '''(experimental) The SMTP reply code, as defined by RFC 5321.

        :see: https://tools.ietf.org/html/rfc5321
        :stability: experimental
        '''
        result = self._values.get("smtp_reply_code")
        assert result is not None, "Required property 'smtp_reply_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        '''(experimental) The SMTP enhanced status code, as defined by RFC 3463.

        :see: https://tools.ietf.org/html/rfc3463
        :stability: experimental
        '''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BounceTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_ses_actions.EmailEncoding")
class EmailEncoding(enum.Enum):
    '''(experimental) The type of email encoding to use for a SNS action.

    :stability: experimental
    '''

    BASE64 = "BASE64"
    '''(experimental) Base 64.

    :stability: experimental
    '''
    UTF8 = "UTF8"
    '''(experimental) UTF-8.

    :stability: experimental
    '''


@jsii.implements(_IReceiptRuleAction_4e833cf2)
class Lambda(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_ses_actions.Lambda"):
    '''(experimental) Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_lambda as lambda_
        from monocdk import aws_ses_actions as ses_actions
        from monocdk import aws_sns as sns
        
        # function_: lambda.Function
        # topic: sns.Topic
        
        lambda_ = ses_actions.Lambda(
            function=function_,
        
            # the properties below are optional
            invocation_type=ses_actions.LambdaInvocationType.EVENT,
            topic=topic
        )
    '''

    def __init__(
        self,
        *,
        function: _IFunction_6e14f09e,
        invocation_type: typing.Optional["LambdaInvocationType"] = None,
        topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''
        :param function: (experimental) The Lambda function to invoke.
        :param invocation_type: (experimental) The invocation type of the Lambda function. Default: Event
        :param topic: (experimental) The SNS topic to notify when the Lambda action is taken. Default: no notification

        :stability: experimental
        '''
        props = LambdaProps(
            function=function, invocation_type=invocation_type, topic=topic
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _IReceiptRule_77e30645) -> _ReceiptRuleActionConfig_c996e325:
        '''(experimental) Returns the receipt rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b97a459d45318152320949ac0b34a7ef1e43e7ad364c022ed1c004aa69fa61)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ReceiptRuleActionConfig_c996e325, jsii.invoke(self, "bind", [rule]))


@jsii.enum(jsii_type="monocdk.aws_ses_actions.LambdaInvocationType")
class LambdaInvocationType(enum.Enum):
    '''(experimental) The type of invocation to use for a Lambda Action.

    :stability: experimental
    '''

    EVENT = "EVENT"
    '''(experimental) The function will be invoked asynchronously.

    :stability: experimental
    '''
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    '''(experimental) The function will be invoked sychronously.

    Use RequestResponse only when
    you want to make a mail flow decision, such as whether to stop the receipt
    rule or the receipt rule set.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_ses_actions.LambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "function": "function",
        "invocation_type": "invocationType",
        "topic": "topic",
    },
)
class LambdaProps:
    def __init__(
        self,
        *,
        function: _IFunction_6e14f09e,
        invocation_type: typing.Optional[LambdaInvocationType] = None,
        topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''(experimental) Construction properties for a Lambda action.

        :param function: (experimental) The Lambda function to invoke.
        :param invocation_type: (experimental) The invocation type of the Lambda function. Default: Event
        :param topic: (experimental) The SNS topic to notify when the Lambda action is taken. Default: no notification

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_lambda as lambda_
            from monocdk import aws_ses_actions as ses_actions
            from monocdk import aws_sns as sns
            
            # function_: lambda.Function
            # topic: sns.Topic
            
            lambda_props = ses_actions.LambdaProps(
                function=function_,
            
                # the properties below are optional
                invocation_type=ses_actions.LambdaInvocationType.EVENT,
                topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6e17e8c7c5449e52886ce44d00b3e5e352413449e6fa2550f465919e973611)
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function": function,
        }
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def function(self) -> _IFunction_6e14f09e:
        '''(experimental) The Lambda function to invoke.

        :stability: experimental
        '''
        result = self._values.get("function")
        assert result is not None, "Required property 'function' is missing"
        return typing.cast(_IFunction_6e14f09e, result)

    @builtins.property
    def invocation_type(self) -> typing.Optional[LambdaInvocationType]:
        '''(experimental) The invocation type of the Lambda function.

        :default: Event

        :stability: experimental
        '''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[LambdaInvocationType], result)

    @builtins.property
    def topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) The SNS topic to notify when the Lambda action is taken.

        :default: no notification

        :stability: experimental
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IReceiptRuleAction_4e833cf2)
class S3(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_ses_actions.S3"):
    '''(experimental) Saves the received message to an Amazon S3 bucket and, optionally, publishes a notification to Amazon SNS.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as s3
        import monocdk as actions
        
        
        bucket = s3.Bucket(self, "Bucket")
        topic = sns.Topic(self, "Topic")
        
        ses.ReceiptRuleSet(self, "RuleSet",
            rules=[s3.aws_ses.ReceiptRuleOptions(
                recipients=["hello@aws.com"],
                actions=[
                    actions.AddHeader(
                        name="X-Special-Header",
                        value="aws"
                    ),
                    actions.S3(
                        bucket=bucket,
                        object_key_prefix="emails/",
                        topic=topic
                    )
                ]
            ), s3.aws_ses.ReceiptRuleOptions(
                recipients=["aws.com"],
                actions=[
                    actions.Sns(
                        topic=topic
                    )
                ]
            )
            ]
        )
    '''

    def __init__(
        self,
        *,
        bucket: _IBucket_73486e29,
        kms_key: typing.Optional[_IKey_36930160] = None,
        object_key_prefix: typing.Optional[builtins.str] = None,
        topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''
        :param bucket: (experimental) The S3 bucket that incoming email will be saved to.
        :param kms_key: (experimental) The master key that SES should use to encrypt your emails before saving them to the S3 bucket. Default: no encryption
        :param object_key_prefix: (experimental) The key prefix of the S3 bucket. Default: no prefix
        :param topic: (experimental) The SNS topic to notify when the S3 action is taken. Default: no notification

        :stability: experimental
        '''
        props = S3Props(
            bucket=bucket,
            kms_key=kms_key,
            object_key_prefix=object_key_prefix,
            topic=topic,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _IReceiptRule_77e30645) -> _ReceiptRuleActionConfig_c996e325:
        '''(experimental) Returns the receipt rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c8a363709fdac45ee1ad6cbef1f9d09848b22fc498e9e49169397beb7d3802)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ReceiptRuleActionConfig_c996e325, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_ses_actions.S3Props",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "kms_key": "kmsKey",
        "object_key_prefix": "objectKeyPrefix",
        "topic": "topic",
    },
)
class S3Props:
    def __init__(
        self,
        *,
        bucket: _IBucket_73486e29,
        kms_key: typing.Optional[_IKey_36930160] = None,
        object_key_prefix: typing.Optional[builtins.str] = None,
        topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''(experimental) Construction properties for a S3 action.

        :param bucket: (experimental) The S3 bucket that incoming email will be saved to.
        :param kms_key: (experimental) The master key that SES should use to encrypt your emails before saving them to the S3 bucket. Default: no encryption
        :param object_key_prefix: (experimental) The key prefix of the S3 bucket. Default: no prefix
        :param topic: (experimental) The SNS topic to notify when the S3 action is taken. Default: no notification

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as s3
            import monocdk as actions
            
            
            bucket = s3.Bucket(self, "Bucket")
            topic = sns.Topic(self, "Topic")
            
            ses.ReceiptRuleSet(self, "RuleSet",
                rules=[s3.aws_ses.ReceiptRuleOptions(
                    recipients=["hello@aws.com"],
                    actions=[
                        actions.AddHeader(
                            name="X-Special-Header",
                            value="aws"
                        ),
                        actions.S3(
                            bucket=bucket,
                            object_key_prefix="emails/",
                            topic=topic
                        )
                    ]
                ), s3.aws_ses.ReceiptRuleOptions(
                    recipients=["aws.com"],
                    actions=[
                        actions.Sns(
                            topic=topic
                        )
                    ]
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d109e5731b38200538c496ccce9edbf2f1f1540548369d9f86afb409796a5918)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if object_key_prefix is not None:
            self._values["object_key_prefix"] = object_key_prefix
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def bucket(self) -> _IBucket_73486e29:
        '''(experimental) The S3 bucket that incoming email will be saved to.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_IBucket_73486e29, result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The master key that SES should use to encrypt your emails before saving them to the S3 bucket.

        :default: no encryption

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def object_key_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key prefix of the S3 bucket.

        :default: no prefix

        :stability: experimental
        '''
        result = self._values.get("object_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) The SNS topic to notify when the S3 action is taken.

        :default: no notification

        :stability: experimental
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IReceiptRuleAction_4e833cf2)
class Sns(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_ses_actions.Sns"):
    '''(experimental) Publishes the email content within a notification to Amazon SNS.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as s3
        import monocdk as actions
        
        
        bucket = s3.Bucket(self, "Bucket")
        topic = sns.Topic(self, "Topic")
        
        ses.ReceiptRuleSet(self, "RuleSet",
            rules=[s3.aws_ses.ReceiptRuleOptions(
                recipients=["hello@aws.com"],
                actions=[
                    actions.AddHeader(
                        name="X-Special-Header",
                        value="aws"
                    ),
                    actions.S3(
                        bucket=bucket,
                        object_key_prefix="emails/",
                        topic=topic
                    )
                ]
            ), s3.aws_ses.ReceiptRuleOptions(
                recipients=["aws.com"],
                actions=[
                    actions.Sns(
                        topic=topic
                    )
                ]
            )
            ]
        )
    '''

    def __init__(
        self,
        *,
        topic: _ITopic_465e36b9,
        encoding: typing.Optional[EmailEncoding] = None,
    ) -> None:
        '''
        :param topic: (experimental) The SNS topic to notify.
        :param encoding: (experimental) The encoding to use for the email within the Amazon SNS notification. Default: UTF-8

        :stability: experimental
        '''
        props = SnsProps(topic=topic, encoding=encoding)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IReceiptRule_77e30645) -> _ReceiptRuleActionConfig_c996e325:
        '''(experimental) Returns the receipt rule action specification.

        :param _rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abc01b7b48d7658b8cbee6816bcadf1affebc01c82d1eccba4bc2cd916a1499)
            check_type(argname="argument _rule", value=_rule, expected_type=type_hints["_rule"])
        return typing.cast(_ReceiptRuleActionConfig_c996e325, jsii.invoke(self, "bind", [_rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_ses_actions.SnsProps",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic", "encoding": "encoding"},
)
class SnsProps:
    def __init__(
        self,
        *,
        topic: _ITopic_465e36b9,
        encoding: typing.Optional[EmailEncoding] = None,
    ) -> None:
        '''(experimental) Construction properties for a SNS action.

        :param topic: (experimental) The SNS topic to notify.
        :param encoding: (experimental) The encoding to use for the email within the Amazon SNS notification. Default: UTF-8

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as s3
            import monocdk as actions
            
            
            bucket = s3.Bucket(self, "Bucket")
            topic = sns.Topic(self, "Topic")
            
            ses.ReceiptRuleSet(self, "RuleSet",
                rules=[s3.aws_ses.ReceiptRuleOptions(
                    recipients=["hello@aws.com"],
                    actions=[
                        actions.AddHeader(
                            name="X-Special-Header",
                            value="aws"
                        ),
                        actions.S3(
                            bucket=bucket,
                            object_key_prefix="emails/",
                            topic=topic
                        )
                    ]
                ), s3.aws_ses.ReceiptRuleOptions(
                    recipients=["aws.com"],
                    actions=[
                        actions.Sns(
                            topic=topic
                        )
                    ]
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b25d4677a1c84cfae2acc372763bcc95560fd06787dbfc79dc4e34f7e61fd99)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if encoding is not None:
            self._values["encoding"] = encoding

    @builtins.property
    def topic(self) -> _ITopic_465e36b9:
        '''(experimental) The SNS topic to notify.

        :stability: experimental
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_ITopic_465e36b9, result)

    @builtins.property
    def encoding(self) -> typing.Optional[EmailEncoding]:
        '''(experimental) The encoding to use for the email within the Amazon SNS notification.

        :default: UTF-8

        :stability: experimental
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[EmailEncoding], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IReceiptRuleAction_4e833cf2)
class Stop(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_ses_actions.Stop"):
    '''(experimental) Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_ses_actions as ses_actions
        from monocdk import aws_sns as sns
        
        # topic: sns.Topic
        
        stop = ses_actions.Stop(
            topic=topic
        )
    '''

    def __init__(self, *, topic: typing.Optional[_ITopic_465e36b9] = None) -> None:
        '''
        :param topic: (experimental) The SNS topic to notify when the stop action is taken.

        :stability: experimental
        '''
        props = StopProps(topic=topic)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: _IReceiptRule_77e30645) -> _ReceiptRuleActionConfig_c996e325:
        '''(experimental) Returns the receipt rule action specification.

        :param _rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4080961c200e0efdbb77d4167613abdf23a064c5349dd1c92369cc78eac73611)
            check_type(argname="argument _rule", value=_rule, expected_type=type_hints["_rule"])
        return typing.cast(_ReceiptRuleActionConfig_c996e325, jsii.invoke(self, "bind", [_rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_ses_actions.StopProps",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class StopProps:
    def __init__(self, *, topic: typing.Optional[_ITopic_465e36b9] = None) -> None:
        '''(experimental) Construction properties for a stop action.

        :param topic: (experimental) The SNS topic to notify when the stop action is taken.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_ses_actions as ses_actions
            from monocdk import aws_sns as sns
            
            # topic: sns.Topic
            
            stop_props = ses_actions.StopProps(
                topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f5fd9dc4c569270a4b7a4714927de0bb9323e62fb0f6fb7789625a02f9f1a3)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) The SNS topic to notify when the stop action is taken.

        :stability: experimental
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StopProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddHeader",
    "AddHeaderProps",
    "Bounce",
    "BounceProps",
    "BounceTemplate",
    "BounceTemplateProps",
    "EmailEncoding",
    "Lambda",
    "LambdaInvocationType",
    "LambdaProps",
    "S3",
    "S3Props",
    "Sns",
    "SnsProps",
    "Stop",
    "StopProps",
]

publication.publish()

def _typecheckingstub__c0316d9aec8e1be8ef153705c92deef7054a2038013165f0ecb1f78e462e0f40(
    _rule: _IReceiptRule_77e30645,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312b3bc1a8b5a5742c3ab66700aab60215ff3c6216fff28554139d317950549e(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5314c8a8d47493a81baa553a3c140237eb9558dd9e285a10fd3003ab6fea3a56(
    _rule: _IReceiptRule_77e30645,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd2e339732b4a70272c4ec018a8d29d916aa2b3e25cb1708975c11e8dec6b0f(
    *,
    sender: builtins.str,
    template: BounceTemplate,
    topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5129053407ae2ad320f3c264501c5c3bc0f1dbc7d651e502e787c323021577(
    *,
    message: builtins.str,
    smtp_reply_code: builtins.str,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b97a459d45318152320949ac0b34a7ef1e43e7ad364c022ed1c004aa69fa61(
    rule: _IReceiptRule_77e30645,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6e17e8c7c5449e52886ce44d00b3e5e352413449e6fa2550f465919e973611(
    *,
    function: _IFunction_6e14f09e,
    invocation_type: typing.Optional[LambdaInvocationType] = None,
    topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c8a363709fdac45ee1ad6cbef1f9d09848b22fc498e9e49169397beb7d3802(
    rule: _IReceiptRule_77e30645,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d109e5731b38200538c496ccce9edbf2f1f1540548369d9f86afb409796a5918(
    *,
    bucket: _IBucket_73486e29,
    kms_key: typing.Optional[_IKey_36930160] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
    topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abc01b7b48d7658b8cbee6816bcadf1affebc01c82d1eccba4bc2cd916a1499(
    _rule: _IReceiptRule_77e30645,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b25d4677a1c84cfae2acc372763bcc95560fd06787dbfc79dc4e34f7e61fd99(
    *,
    topic: _ITopic_465e36b9,
    encoding: typing.Optional[EmailEncoding] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4080961c200e0efdbb77d4167613abdf23a064c5349dd1c92369cc78eac73611(
    _rule: _IReceiptRule_77e30645,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f5fd9dc4c569270a4b7a4714927de0bb9323e62fb0f6fb7789625a02f9f1a3(
    *,
    topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass
