'''
# integ-tests

## Overview

This library is meant to be used in combination with the [integ-runner]() CLI
to enable users to write and execute integration tests for AWS CDK Constructs.

An integration test should be defined as a CDK application, and
there should be a 1:1 relationship between an integration test and a CDK application.

So for example, in order to create an integration test called `my-function`
we would need to create a file to contain our integration test application.

*test/integ.my-function.ts*

```python
app = App()
stack = Stack()
lambda_.Function(stack, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
)
```

This is a self contained CDK application which we could deploy by running

```bash
cdk deploy --app 'node test/integ.my-function.js'
```

In order to turn this into an integration test, all that is needed is to
use the `IntegTest` construct.

```python
# app: App
# stack: Stack

IntegTest(app, "Integ", test_cases=[stack])
```

You will notice that the `stack` is registered to the `IntegTest` as a test case.
Each integration test can contain multiple test cases, which are just instances
of a stack. See the [Usage](#usage) section for more details.

## Usage

### IntegTest

Suppose you have a simple stack, that only encapsulates a Lambda function with a
certain handler:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )
```

You may want to test this stack under different conditions. For example, we want
this stack to be deployed correctly, regardless of the architecture we choose
for the Lambda function. In particular, it should work for both `ARM_64` and
`X86_64`. So you can create an `IntegTestCase` that exercises both scenarios:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )

# Beginning of the test suite
app = App()

IntegTest(app, "DifferentArchitectures",
    test_cases=[
        StackUnderTest(app, "Stack1",
            architecture=lambda_.Architecture.ARM_64
        ),
        StackUnderTest(app, "Stack2",
            architecture=lambda_.Architecture.X86_64
        )
    ]
)
```

This is all the instruction you need for the integration test runner to know
which stacks to synthesize, deploy and destroy. But you may also need to
customize the behavior of the runner by changing its parameters. For example:

```python
app = App()

stack_under_test = Stack(app, "StackUnderTest")

stack = Stack(app, "stack")

test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
    test_cases=[stack_under_test],
    diff_assets=True,
    stack_update_workflow=True,
    cdk_command_options=lambda.cloud_assembly_schema.CdkCommands(
        deploy=lambda.cloud_assembly_schema.DeployCommand(
            args=lambda.cloud_assembly_schema.DeployOptions(
                require_approval=RequireApproval.NEVER,
                json=True
            )
        ),
        destroy=lambda.cloud_assembly_schema.DestroyCommand(
            args=lambda.cloud_assembly_schema.DestroyOptions(
                force=True
            )
        )
    )
)
```

### IntegTestCaseStack

In the majority of cases an integration test will contain a single `IntegTestCase`.
By default when you create an `IntegTest` an `IntegTestCase` is created for you
and all of your test cases are registered to this `IntegTestCase`. The `IntegTestCase`
and `IntegTestCaseStack` constructs are only needed when it is necessary to
defined different options for individual test cases.

For example, you might want to have one test case where `diffAssets` is enabled.

```python
# app: App
# stack_under_test: Stack

test_case_with_assets = IntegTestCaseStack(app, "TestCaseAssets",
    diff_assets=True
)

IntegTest(app, "Integ", test_cases=[stack_under_test, test_case_with_assets])
```

## Assertions

This library also provides a utility to make assertions against the infrastructure that the integration test deploys.

There are two main scenarios in which assertions are created.

* Part of an integration test using `integ-runner`

In this case you would create an integration test using the `IntegTest` construct and then make assertions using the `assert` property.
You should **not** utilize the assertion constructs directly, but should instead use the `methods` on `IntegTest.assert`.

```python
# app: App
# stack: Stack


integ = IntegTest(app, "Integ", test_cases=[stack])
integ.assertions.aws_api_call("S3", "getObject")
```

* Part of a  normal CDK deployment

In this case you may be using assertions as part of a normal CDK deployment in order to make an assertion on the infrastructure
before the deployment is considered successful. In this case you can utilize the assertions constructs directly.

```python
# my_app_stack: Stack


AwsApiCall(my_app_stack, "GetObject",
    service="S3",
    api="getObject"
)
```

### DeployAssert

Assertions are created by using the `DeployAssert` construct. This construct creates it's own `Stack` separate from
any stacks that you create as part of your integration tests. This `Stack` is treated differently from other stacks
by the `integ-runner` tool. For example, this stack will not be diffed by the `integ-runner`.

`DeployAssert` also provides utilities to register your own assertions.

```python
# my_custom_resource: CustomResource
# stack: Stack
# app: App


integ = IntegTest(app, "Integ", test_cases=[stack])
integ.assertions.expect("CustomAssertion",
    ExpectedResult.object_like({"foo": "bar"}),
    ActualResult.from_custom_resource(my_custom_resource, "data"))
```

In the above example an assertion is created that will trigger a user defined `CustomResource`
and assert that the `data` attribute is equal to `{ foo: 'bar' }`.

### AwsApiCall

A common method to retrieve the "actual" results to compare with what is expected is to make an
AWS API call to receive some data. This library does this by utilizing CloudFormation custom resources
which means that CloudFormation will call out to a Lambda Function which will
use the AWS JavaScript SDK to make the API call.

This can be done by using the class directory (in the case of a normal deployment):

```python
# stack: Stack


AwsApiCall(stack, "MyAssertion",
    service="SQS",
    api="receiveMessage",
    parameters={
        "QueueUrl": "url"
    }
)
```

Or by using the `awsApiCall` method on `DeployAssert` (when writing integration tests):

```python
# app: App
# stack: Stack

integ = IntegTest(app, "Integ",
    test_cases=[stack]
)
integ.assertions.aws_api_call("SQS", "receiveMessage", {
    "QueueUrl": "url"
})
```

### EqualsAssertion

This library currently provides the ability to assert that two values are equal
to one another by utilizing the `EqualsAssertion` class. This utilizes a Lambda
backed `CustomResource` which in tern uses the [Match](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions.Match.html) utility from the
[@aws-cdk/assertions](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions-readme.html) library.

```python
# app: App
# stack: Stack
# queue: sqs.Queue
# fn: lambda.IFunction


integ = IntegTest(app, "Integ",
    test_cases=[stack]
)

integ.assertions.invoke_function(
    function_name=fn.function_name,
    invocation_type=InvocationType.EVENT,
    payload=JSON.stringify({"status": "OK"})
)

message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
    "QueueUrl": queue.queue_url,
    "WaitTimeSeconds": 20
})

message.assert_at_path("Messages.0.Body", ExpectedResult.object_like({
    "request_context": {
        "condition": "Success"
    },
    "request_payload": {
        "status": "OK"
    },
    "response_context": {
        "status_code": 200
    },
    "response_payload": "success"
}))
```

#### Match

`integ-tests` also provides a `Match` utility similar to the `@aws-cdk/assertions` module. `Match`
can be used to construct the `ExpectedResult`.

```python
# message: AwsApiCall


message.expect(ExpectedResult.object_like({
    "Messages": Match.array_with([{
        "Body": {
            "Values": Match.array_with([{"Asdf": 3}]),
            "Message": Match.string_like_regexp("message")
        }
    }
    ])
}))
```

### Examples

#### Invoke a Lambda Function

In this example there is a Lambda Function that is invoked and
we assert that the payload that is returned is equal to '200'.

```python
# lambda_function: lambda.IFunction
# app: App


stack = Stack(app, "cdk-integ-lambda-bundling")

integ = IntegTest(app, "IntegTest",
    test_cases=[stack]
)

invoke = integ.assertions.invoke_function(
    function_name=lambda_function.function_name
)
invoke.expect(ExpectedResult.object_like({
    "Payload": "200"
}))
```

#### Make an AWS API Call

In this example there is a StepFunctions state machine that is executed
and then we assert that the result of the execution is successful.

```python
# app: App
# stack: Stack
# sm: IStateMachine


test_case = IntegTest(app, "IntegTest",
    test_cases=[stack]
)

# Start an execution
start = test_case.assertions.aws_api_call("StepFunctions", "startExecution", {
    "state_machine_arn": sm.state_machine_arn
})

# describe the results of the execution
describe = test_case.assertions.aws_api_call("StepFunctions", "describeExecution", {
    "execution_arn": start.get_att_string("executionArn")
})

# assert the results
describe.expect(ExpectedResult.object_like({
    "status": "SUCCEEDED"
}))
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
    Construct as _Construct_e78e779f,
    CustomResource as _CustomResource_9c5112da,
    Environment as _Environment_0cfdf5e4,
    IConstruct as _IConstruct_5a0f9c5e,
    IStackSynthesizer as _IStackSynthesizer_a39ceded,
    Reference as _Reference_a96c80b4,
    Stack as _Stack_9f43e4a3,
    StackProps as _StackProps_484a498c,
)
from ..cloud_assembly_schema import (
    CdkCommands as _CdkCommands_3043a8a5,
    Hooks as _Hooks_ffcd74d8,
    IntegManifest as _IntegManifest_8b169ea0,
    TestOptions as _TestOptions_4ebd1db7,
)


class ActualResult(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.integ_tests.ActualResult",
):
    '''(experimental) Represents the "actual" results to compare.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_custom_resource: CustomResource
        # stack: Stack
        # app: App
        
        
        integ = IntegTest(app, "Integ", test_cases=[stack])
        integ.assertions.expect("CustomAssertion",
            ExpectedResult.object_like({"foo": "bar"}),
            ActualResult.from_custom_resource(my_custom_resource, "data"))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAwsApiCall")
    @builtins.classmethod
    def from_aws_api_call(
        cls,
        query: "IAwsApiCall",
        attribute: builtins.str,
    ) -> "ActualResult":
        '''(experimental) Get the actual results from a AwsApiCall.

        :param query: -
        :param attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf0a35dc8b584618fd101445f6a16a7474d4538a5211ee2180b04c43f0f3a0c)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast("ActualResult", jsii.sinvoke(cls, "fromAwsApiCall", [query, attribute]))

    @jsii.member(jsii_name="fromCustomResource")
    @builtins.classmethod
    def from_custom_resource(
        cls,
        custom_resource: _CustomResource_9c5112da,
        attribute: builtins.str,
    ) -> "ActualResult":
        '''(experimental) Get the actual results from a CustomResource.

        :param custom_resource: -
        :param attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fecb853311b88e6c54c8b6fc004c806cfa6883449057df1309c3fc1947c2e47)
            check_type(argname="argument custom_resource", value=custom_resource, expected_type=type_hints["custom_resource"])
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast("ActualResult", jsii.sinvoke(cls, "fromCustomResource", [custom_resource, attribute]))

    @builtins.property
    @jsii.member(jsii_name="result")
    @abc.abstractmethod
    def result(self) -> builtins.str:
        '''(experimental) The actual results as a string.

        :stability: experimental
        '''
        ...

    @result.setter
    @abc.abstractmethod
    def result(self, value: builtins.str) -> None:
        ...


class _ActualResultProxy(ActualResult):
    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        '''(experimental) The actual results as a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "result"))

    @result.setter
    def result(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5aae03de3c56c51ea3d29c34abbb0ce8708ca59206bf81cc4edfcdbc889596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "result", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ActualResult).__jsii_proxy_class__ = lambda : _ActualResultProxy


@jsii.data_type(
    jsii_type="monocdk.integ_tests.AssertionRequest",
    jsii_struct_bases=[],
    name_mapping={
        "actual": "actual",
        "expected": "expected",
        "fail_deployment": "failDeployment",
    },
)
class AssertionRequest:
    def __init__(
        self,
        *,
        actual: typing.Any,
        expected: typing.Any,
        fail_deployment: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) A request to make an assertion that the actual value matches the expected.

        :param actual: (experimental) The actual value received.
        :param expected: (experimental) The expected value to assert.
        :param fail_deployment: (experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure. This is only necessary if assertions are being executed outside of ``integ-runner``. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import integ_tests
            
            # actual: Any
            # expected: Any
            
            assertion_request = integ_tests.AssertionRequest(
                actual=actual,
                expected=expected,
            
                # the properties below are optional
                fail_deployment=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4030e9d317d57ff13f4c6fcb1baeae719f184f98e633744958682a75855b1d9)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
            check_type(argname="argument fail_deployment", value=fail_deployment, expected_type=type_hints["fail_deployment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actual": actual,
            "expected": expected,
        }
        if fail_deployment is not None:
            self._values["fail_deployment"] = fail_deployment

    @builtins.property
    def actual(self) -> typing.Any:
        '''(experimental) The actual value received.

        :stability: experimental
        '''
        result = self._values.get("actual")
        assert result is not None, "Required property 'actual' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def expected(self) -> typing.Any:
        '''(experimental) The expected value to assert.

        :stability: experimental
        '''
        result = self._values.get("expected")
        assert result is not None, "Required property 'expected' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def fail_deployment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure.

        This is only necessary if assertions are being
        executed outside of ``integ-runner``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("fail_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssertionRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.integ_tests.AssertionResult",
    jsii_struct_bases=[],
    name_mapping={"data": "data", "failed": "failed"},
)
class AssertionResult:
    def __init__(
        self,
        *,
        data: builtins.str,
        failed: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The result of an Assertion wrapping the actual result data in another struct.

        Needed to access the whole message via getAtt() on the custom resource.

        :param data: (experimental) The result of an assertion.
        :param failed: (experimental) Whether or not the assertion failed. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import integ_tests
            
            assertion_result = integ_tests.AssertionResult(
                data="data",
            
                # the properties below are optional
                failed=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bc0f7c539b19de148ea78fa0171d311bfd2eb2527bfeaacc675f7f22ebaa56)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument failed", value=failed, expected_type=type_hints["failed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
        }
        if failed is not None:
            self._values["failed"] = failed

    @builtins.property
    def data(self) -> builtins.str:
        '''(experimental) The result of an assertion.

        :stability: experimental
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the assertion failed.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("failed")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssertionResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.integ_tests.AssertionResultData",
    jsii_struct_bases=[],
    name_mapping={"status": "status", "message": "message"},
)
class AssertionResultData:
    def __init__(
        self,
        *,
        status: "Status",
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The result of an assertion.

        :param status: (experimental) The status of the assertion, i.e. pass or fail.
        :param message: (experimental) Any message returned with the assertion result typically this will be the diff if there is any. Default: - none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import integ_tests
            
            assertion_result_data = integ_tests.AssertionResultData(
                status=integ_tests.Status.PASS,
            
                # the properties below are optional
                message="message"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e481d2fa04efe9b510e1a833547070cca1d6e3798a736f5b324373fd46fbed7)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def status(self) -> "Status":
        '''(experimental) The status of the assertion, i.e. pass or fail.

        :stability: experimental
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast("Status", result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''(experimental) Any message returned with the assertion result typically this will be the diff if there is any.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssertionResultData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.integ_tests.AssertionType")
class AssertionType(enum.Enum):
    '''(experimental) The type of assertion to perform.

    :stability: experimental
    '''

    EQUALS = "EQUALS"
    '''(experimental) Assert that two values are equal.

    :stability: experimental
    '''
    OBJECT_LIKE = "OBJECT_LIKE"
    '''(experimental) The keys and their values must be present in the target but the target can be a superset.

    :stability: experimental
    '''
    ARRAY_WITH = "ARRAY_WITH"
    '''(experimental) Matches the specified pattern with the array The set of elements must be in the same order as would be found.

    :stability: experimental
    '''


class AssertionsProvider(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.AssertionsProvider",
):
    '''(experimental) Represents an assertions provider.

    The creates a singletone
    Lambda Function that will create a single function per stack
    that serves as the custom resource provider for the various
    assertion providers

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import integ_tests
        
        assertions_provider = integ_tests.AssertionsProvider(self, "MyAssertionsProvider")
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9dde7b2d27b7d5a2254f873e27b33f47d3649a5d101bac96d5dad9074a8eb6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="addPolicyStatementFromSdkCall")
    def add_policy_statement_from_sdk_call(
        self,
        service: builtins.str,
        api: builtins.str,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Create a policy statement from a specific api call.

        :param service: -
        :param api: -
        :param resources: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1e8cda486b554525db3a6b7c902d3ea86b5c776dbc4e6b8bb8d7608f5863b0)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        return typing.cast(None, jsii.invoke(self, "addPolicyStatementFromSdkCall", [service, api, resources]))

    @jsii.member(jsii_name="encode")
    def encode(self, obj: typing.Any) -> typing.Any:
        '''(experimental) Encode an object so it can be passed as custom resource parameters.

        Custom resources will convert
        all input parameters to strings so we encode non-strings here
        so we can then decode them correctly in the provider function

        :param obj: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b975ea2041b07f5835d6704c3e01ed13682dc7728fc231a3dc537ce4e88b5e)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast(typing.Any, jsii.invoke(self, "encode", [obj]))

    @builtins.property
    @jsii.member(jsii_name="handlerRoleArn")
    def handler_role_arn(self) -> _Reference_a96c80b4:
        '''(experimental) A reference to the provider Lambda Function execution Role ARN.

        :stability: experimental
        '''
        return typing.cast(_Reference_a96c80b4, jsii.get(self, "handlerRoleArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''(experimental) The ARN of the lambda function which can be used as a serviceToken to a CustomResource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceToken"))


@jsii.data_type(
    jsii_type="monocdk.integ_tests.AwsApiCallOptions",
    jsii_struct_bases=[],
    name_mapping={"api": "api", "service": "service", "parameters": "parameters"},
)
class AwsApiCallOptions:
    def __init__(
        self,
        *,
        api: builtins.str,
        service: builtins.str,
        parameters: typing.Any = None,
    ) -> None:
        '''(experimental) Options to perform an AWS JavaScript V2 API call.

        :param api: (experimental) The api call to make, i.e. getBucketLifecycle.
        :param service: (experimental) The AWS service, i.e. S3.
        :param parameters: (experimental) Any parameters to pass to the api call. Default: - no parameters

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import integ_tests
            
            # parameters: Any
            
            aws_api_call_options = integ_tests.AwsApiCallOptions(
                api="api",
                service="service",
            
                # the properties below are optional
                parameters=parameters
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca91f6bbceeef568696be4828a2c693f09e7e58145083b9e286e17d7e8fb4fbe)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "service": service,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def api(self) -> builtins.str:
        '''(experimental) The api call to make, i.e. getBucketLifecycle.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The AWS service, i.e. S3.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) Any parameters to pass to the api call.

        :default: - no parameters

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiCallOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.integ_tests.AwsApiCallProps",
    jsii_struct_bases=[AwsApiCallOptions],
    name_mapping={"api": "api", "service": "service", "parameters": "parameters"},
)
class AwsApiCallProps(AwsApiCallOptions):
    def __init__(
        self,
        *,
        api: builtins.str,
        service: builtins.str,
        parameters: typing.Any = None,
    ) -> None:
        '''(experimental) Options for creating an SDKQuery provider.

        :param api: (experimental) The api call to make, i.e. getBucketLifecycle.
        :param service: (experimental) The AWS service, i.e. S3.
        :param parameters: (experimental) Any parameters to pass to the api call. Default: - no parameters

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_app_stack: Stack
            
            
            AwsApiCall(my_app_stack, "GetObject",
                service="S3",
                api="getObject"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf58de5f81726112fc71071644768b314ec33c41449e05321883ee28e3fa69f)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "service": service,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def api(self) -> builtins.str:
        '''(experimental) The api call to make, i.e. getBucketLifecycle.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The AWS service, i.e. S3.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) Any parameters to pass to the api call.

        :default: - no parameters

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiCallProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.integ_tests.AwsApiCallRequest",
    jsii_struct_bases=[],
    name_mapping={
        "api": "api",
        "service": "service",
        "flatten_response": "flattenResponse",
        "parameters": "parameters",
    },
)
class AwsApiCallRequest:
    def __init__(
        self,
        *,
        api: builtins.str,
        service: builtins.str,
        flatten_response: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''(experimental) A AWS JavaScript SDK V2 request.

        :param api: (experimental) The AWS api call to make i.e. getBucketLifecycle.
        :param service: (experimental) The AWS service i.e. S3.
        :param flatten_response: (experimental) Whether or not to flatten the response from the api call. Valid values are 'true' or 'false' as strings Typically when using an SdkRequest you will be passing it as the ``actual`` value to an assertion provider so this would be set to 'false' (you want the actual response). If you are using the SdkRequest to perform more of a query to return a single value to use, then this should be set to 'true'. For example, you could make a StepFunctions.startExecution api call and retreive the ``executionArn`` from the response. Default: 'false'
        :param parameters: (experimental) Any parameters to pass to the api call. Default: - no parameters

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import integ_tests
            
            # parameters: Any
            
            aws_api_call_request = integ_tests.AwsApiCallRequest(
                api="api",
                service="service",
            
                # the properties below are optional
                flatten_response="flattenResponse",
                parameters=parameters
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d303790b049091ffee968459a0e4f6e9553ac92c3ee4cb9478b7910978492de)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument flatten_response", value=flatten_response, expected_type=type_hints["flatten_response"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "service": service,
        }
        if flatten_response is not None:
            self._values["flatten_response"] = flatten_response
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def api(self) -> builtins.str:
        '''(experimental) The AWS api call to make i.e. getBucketLifecycle.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The AWS service i.e. S3.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flatten_response(self) -> typing.Optional[builtins.str]:
        '''(experimental) Whether or not to flatten the response from the api call.

        Valid values are 'true' or 'false' as strings

        Typically when using an SdkRequest you will be passing it as the
        ``actual`` value to an assertion provider so this would be set
        to 'false' (you want the actual response).

        If you are using the SdkRequest to perform more of a query to return
        a single value to use, then this should be set to 'true'. For example,
        you could make a StepFunctions.startExecution api call and retreive the
        ``executionArn`` from the response.

        :default: 'false'

        :stability: experimental
        '''
        result = self._values.get("flatten_response")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) Any parameters to pass to the api call.

        :default: - no parameters

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiCallRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.integ_tests.AwsApiCallResult",
    jsii_struct_bases=[],
    name_mapping={"api_call_response": "apiCallResponse"},
)
class AwsApiCallResult:
    def __init__(self, *, api_call_response: typing.Any) -> None:
        '''(experimental) The result from a SdkQuery.

        :param api_call_response: (experimental) The full api response.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import integ_tests
            
            # api_call_response: Any
            
            aws_api_call_result = integ_tests.AwsApiCallResult(
                api_call_response=api_call_response
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade32195848192ce06935a91a3e1612fc1f70d944975ea098ef990d2c1e7ab2d)
            check_type(argname="argument api_call_response", value=api_call_response, expected_type=type_hints["api_call_response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_call_response": api_call_response,
        }

    @builtins.property
    def api_call_response(self) -> typing.Any:
        '''(experimental) The full api response.

        :stability: experimental
        '''
        result = self._values.get("api_call_response")
        assert result is not None, "Required property 'api_call_response' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiCallResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EqualsAssertion(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.EqualsAssertion",
):
    '''(experimental) Construct that creates a CustomResource to assert that two values are equal.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import integ_tests
        
        # actual_result: integ_tests.ActualResult
        # expected_result: integ_tests.ExpectedResult
        
        equals_assertion = integ_tests.EqualsAssertion(self, "MyEqualsAssertion",
            actual=actual_result,
            expected=expected_result,
        
            # the properties below are optional
            fail_deployment=False
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        actual: ActualResult,
        expected: "ExpectedResult",
        fail_deployment: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param actual: (experimental) The actual results to compare.
        :param expected: (experimental) The expected result to assert.
        :param fail_deployment: (experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure. This is only necessary if assertions are being executed outside of ``integ-runner``. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d48c7e24b52e0f50040fba910fc7422057e6f3c1939daffece409faf74e1649)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EqualsAssertionProps(
            actual=actual, expected=expected, fail_deployment=fail_deployment
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        '''(experimental) The result of the assertion.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "result"))


@jsii.data_type(
    jsii_type="monocdk.integ_tests.EqualsAssertionProps",
    jsii_struct_bases=[],
    name_mapping={
        "actual": "actual",
        "expected": "expected",
        "fail_deployment": "failDeployment",
    },
)
class EqualsAssertionProps:
    def __init__(
        self,
        *,
        actual: ActualResult,
        expected: "ExpectedResult",
        fail_deployment: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for an EqualsAssertion.

        :param actual: (experimental) The actual results to compare.
        :param expected: (experimental) The expected result to assert.
        :param fail_deployment: (experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure. This is only necessary if assertions are being executed outside of ``integ-runner``. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import integ_tests
            
            # actual_result: integ_tests.ActualResult
            # expected_result: integ_tests.ExpectedResult
            
            equals_assertion_props = integ_tests.EqualsAssertionProps(
                actual=actual_result,
                expected=expected_result,
            
                # the properties below are optional
                fail_deployment=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a075d4dbe35ce6ab0999aac810f840f5c086acb98ceec83ed07e91a080cf763)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
            check_type(argname="argument fail_deployment", value=fail_deployment, expected_type=type_hints["fail_deployment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actual": actual,
            "expected": expected,
        }
        if fail_deployment is not None:
            self._values["fail_deployment"] = fail_deployment

    @builtins.property
    def actual(self) -> ActualResult:
        '''(experimental) The actual results to compare.

        :stability: experimental
        '''
        result = self._values.get("actual")
        assert result is not None, "Required property 'actual' is missing"
        return typing.cast(ActualResult, result)

    @builtins.property
    def expected(self) -> "ExpectedResult":
        '''(experimental) The expected result to assert.

        :stability: experimental
        '''
        result = self._values.get("expected")
        assert result is not None, "Required property 'expected' is missing"
        return typing.cast("ExpectedResult", result)

    @builtins.property
    def fail_deployment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set this to true if a failed assertion should result in a CloudFormation deployment failure.

        This is only necessary if assertions are being
        executed outside of ``integ-runner``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("fail_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EqualsAssertionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpectedResult(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.integ_tests.ExpectedResult",
):
    '''(experimental) Represents the "expected" results to compare.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # app: App
        # integ: IntegTest
        
        integ.assertions.aws_api_call("SQS", "sendMessage", {
            "QueueUrl": "url",
            "MessageBody": "hello"
        })
        message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
            "QueueUrl": "url"
        })
        message.expect(ExpectedResult.object_like({
            "Messages": [{"Body": "hello"}]
        }))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="arrayWith")
    @builtins.classmethod
    def array_with(cls, expected: typing.Sequence[typing.Any]) -> "ExpectedResult":
        '''(experimental) The actual results must be a list and must contain an item with the expected results.

        :param expected: -

        :stability: experimental

        Example::

            # actual results
            actual = [{
                "string_param": "hello"
            }, {
                "string_param": "world"
            }
            ]
            # pass
            ExpectedResult.array_with([{
                "string_param": "hello"
            }
            ])
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e186bf8a3f6df778944f09d8ba1ed5307c8fc16c75d2fabbf80574fb5665899)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast("ExpectedResult", jsii.sinvoke(cls, "arrayWith", [expected]))

    @jsii.member(jsii_name="exact")
    @builtins.classmethod
    def exact(cls, expected: typing.Any) -> "ExpectedResult":
        '''(experimental) The actual results must match exactly.

        Missing data
        will result in a failure

        :param expected: -

        :stability: experimental

        Example::

            # actual results
            actual = {
                "string_param": "hello",
                "number_param": 3,
                "boolean_param": True
            }
            # pass
            ExpectedResult.exact({
                "string_param": "hello",
                "number_param": 3,
                "boolean_param": True
            })
            
            # fail
            ExpectedResult.exact({
                "string_param": "hello"
            })
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e8f980394f80968ccd7c34ba31335c4dacd0dee22bd9002df14901fa1f4df2)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast("ExpectedResult", jsii.sinvoke(cls, "exact", [expected]))

    @jsii.member(jsii_name="objectLike")
    @builtins.classmethod
    def object_like(
        cls,
        expected: typing.Mapping[builtins.str, typing.Any],
    ) -> "ExpectedResult":
        '''(experimental) The expected results must be a subset of the actual results.

        :param expected: -

        :stability: experimental

        Example::

            # actual results
            actual = {
                "string_param": "hello",
                "number_param": 3,
                "boolean_param": True
            }
            # pass
            ExpectedResult.object_like({
                "string_param": "hello"
            })
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a635ed49719edf557718ceec9185b3632ad7cacf350195c8005460ea0bf205)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast("ExpectedResult", jsii.sinvoke(cls, "objectLike", [expected]))

    @jsii.member(jsii_name="stringLikeRegexp")
    @builtins.classmethod
    def string_like_regexp(cls, expected: builtins.str) -> "ExpectedResult":
        '''(experimental) Actual results is a string that matches the Expected result regex.

        :param expected: -

        :stability: experimental

        Example::

            # actual results
            actual = "some string value"
            
            # pass
            ExpectedResult.string_like_regexp("value")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6cc452cf2f0633e1fe92f19789f0df4093f0cc8e114c92ea02024ff107c0ce)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast("ExpectedResult", jsii.sinvoke(cls, "stringLikeRegexp", [expected]))

    @builtins.property
    @jsii.member(jsii_name="result")
    @abc.abstractmethod
    def result(self) -> builtins.str:
        '''(experimental) The expected results encoded as a string.

        :stability: experimental
        '''
        ...

    @result.setter
    @abc.abstractmethod
    def result(self, value: builtins.str) -> None:
        ...


class _ExpectedResultProxy(ExpectedResult):
    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        '''(experimental) The expected results encoded as a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "result"))

    @result.setter
    def result(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afc6ed0cb784ac0b9dca691bb58b664deacee4d0b57ab6ce6d8140719bf9760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "result", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ExpectedResult).__jsii_proxy_class__ = lambda : _ExpectedResultProxy


@jsii.interface(jsii_type="monocdk.integ_tests.IAwsApiCall")
class IAwsApiCall(_IConstruct_5a0f9c5e, typing_extensions.Protocol):
    '''(experimental) Interface for creating a custom resource that will perform an API call using the AWS SDK.

    :stability: experimental
    '''

    @jsii.member(jsii_name="assertAtPath")
    def assert_at_path(self, path: builtins.str, expected: ExpectedResult) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param path: -
        :param expected: -

        :stability: experimental

        Example::

            # integ: IntegTest
            actual = {
                "Messages": [{
                    "MessageId": "",
                    "ReceiptHandle": "",
                    "MD5OfBody": "",
                    "Body": "hello",
                    "Attributes": {},
                    "MD5OfMessageAttributes": {},
                    "MessageAttributes": {}
                }]
            }
            message = integ.assertions.aws_api_call("SQS", "receiveMessage")
            
            message.assert_at_path("Messages.0.Body", ExpectedResult.string_like_regexp("hello"))
        '''
        ...

    @jsii.member(jsii_name="expect")
    def expect(self, expected: ExpectedResult) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall.

        :param expected: -

        :stability: experimental

        Example::

            # integ: IntegTest
            
            invoke = integ.assertions.invoke_function(
                function_name="my-func"
            )
            invoke.expect(ExpectedResult.object_like({"Payload": "OK"}))
        '''
        ...

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: builtins.str) -> _Reference_a96c80b4:
        '''(experimental) Returns the value of an attribute of the custom resource of an arbitrary type.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return:

        a token for ``Fn::GetAtt``. Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getAttString`` for string attributes.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attribute_name: builtins.str) -> builtins.str:
        '''(experimental) Returns the value of an attribute of the custom resource of type string.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return: a token for ``Fn::GetAtt`` encoded as a string.

        :stability: experimental
        '''
        ...


class _IAwsApiCallProxy(
    jsii.proxy_for(_IConstruct_5a0f9c5e), # type: ignore[misc]
):
    '''(experimental) Interface for creating a custom resource that will perform an API call using the AWS SDK.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.integ_tests.IAwsApiCall"

    @jsii.member(jsii_name="assertAtPath")
    def assert_at_path(self, path: builtins.str, expected: ExpectedResult) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param path: -
        :param expected: -

        :stability: experimental

        Example::

            # integ: IntegTest
            actual = {
                "Messages": [{
                    "MessageId": "",
                    "ReceiptHandle": "",
                    "MD5OfBody": "",
                    "Body": "hello",
                    "Attributes": {},
                    "MD5OfMessageAttributes": {},
                    "MessageAttributes": {}
                }]
            }
            message = integ.assertions.aws_api_call("SQS", "receiveMessage")
            
            message.assert_at_path("Messages.0.Body", ExpectedResult.string_like_regexp("hello"))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c70c7539ab2dcec1d3ee533e8b251ff7b5c9fe7b37df11e7aa9e5f00bd33d01)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(None, jsii.invoke(self, "assertAtPath", [path, expected]))

    @jsii.member(jsii_name="expect")
    def expect(self, expected: ExpectedResult) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall.

        :param expected: -

        :stability: experimental

        Example::

            # integ: IntegTest
            
            invoke = integ.assertions.invoke_function(
                function_name="my-func"
            )
            invoke.expect(ExpectedResult.object_like({"Payload": "OK"}))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607ba2652f958b9a1caff27ef81475647ce95319b7dd98410086122ff8d5241f)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(None, jsii.invoke(self, "expect", [expected]))

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: builtins.str) -> _Reference_a96c80b4:
        '''(experimental) Returns the value of an attribute of the custom resource of an arbitrary type.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return:

        a token for ``Fn::GetAtt``. Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getAttString`` for string attributes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb5984af4e2f4d55dbf8453d59370029f37147e38d3c8d2b89c147f5212320a)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(_Reference_a96c80b4, jsii.invoke(self, "getAtt", [attribute_name]))

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attribute_name: builtins.str) -> builtins.str:
        '''(experimental) Returns the value of an attribute of the custom resource of type string.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return: a token for ``Fn::GetAtt`` encoded as a string.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f02ac6d85512dbc03ddfbac4cd7eedafda9bd7fc0259275fef0535d9f652f26)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "getAttString", [attribute_name]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAwsApiCall).__jsii_proxy_class__ = lambda : _IAwsApiCallProxy


@jsii.interface(jsii_type="monocdk.integ_tests.IDeployAssert")
class IDeployAssert(typing_extensions.Protocol):
    '''(experimental) Interface that allows for registering a list of assertions that should be performed on a construct.

    This is only necessary
    when writing integration tests.

    :stability: experimental
    '''

    @jsii.member(jsii_name="awsApiCall")
    def aws_api_call(
        self,
        service: builtins.str,
        api: builtins.str,
        parameters: typing.Any = None,
    ) -> IAwsApiCall:
        '''(experimental) Query AWS using JavaScript SDK V2 API calls.

        This can be used to either
        trigger an action or to return a result that can then be asserted against
        an expected value

        :param service: -
        :param api: -
        :param parameters: -

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            integ.assertions.aws_api_call("SQS", "sendMessage", {
                "QueueUrl": "url",
                "MessageBody": "hello"
            })
            message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
                "QueueUrl": "url"
            })
            message.expect(ExpectedResult.object_like({
                "Messages": [{"Body": "hello"}]
            }))
        '''
        ...

    @jsii.member(jsii_name="expect")
    def expect(
        self,
        id: builtins.str,
        expected: ExpectedResult,
        actual: ActualResult,
    ) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the ActualResult.

        :param id: -
        :param expected: -
        :param actual: -

        :stability: experimental

        Example::

            # integ: IntegTest
            # api_call: AwsApiCall
            
            integ.assertions.expect("invoke",
                ExpectedResult.object_like({"Payload": "OK"}),
                ActualResult.from_aws_api_call(api_call, "Body"))
        '''
        ...

    @jsii.member(jsii_name="invokeFunction")
    def invoke_function(
        self,
        *,
        function_name: builtins.str,
        invocation_type: typing.Optional["InvocationType"] = None,
        log_type: typing.Optional["LogType"] = None,
        payload: typing.Optional[builtins.str] = None,
    ) -> IAwsApiCall:
        '''(experimental) Invoke a lambda function and return the response which can be asserted.

        :param function_name: (experimental) The name of the function to invoke.
        :param invocation_type: (experimental) The type of invocation to use. Default: InvocationType.REQUEST_RESPONE
        :param log_type: (experimental) Whether to return the logs as part of the response. Default: LogType.NONE
        :param payload: (experimental) Payload to send as part of the invoke. Default: - no payload

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            invoke = integ.assertions.invoke_function(
                function_name="my-function"
            )
            invoke.expect(ExpectedResult.object_like({
                "Payload": "200"
            }))
        '''
        ...


class _IDeployAssertProxy:
    '''(experimental) Interface that allows for registering a list of assertions that should be performed on a construct.

    This is only necessary
    when writing integration tests.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.integ_tests.IDeployAssert"

    @jsii.member(jsii_name="awsApiCall")
    def aws_api_call(
        self,
        service: builtins.str,
        api: builtins.str,
        parameters: typing.Any = None,
    ) -> IAwsApiCall:
        '''(experimental) Query AWS using JavaScript SDK V2 API calls.

        This can be used to either
        trigger an action or to return a result that can then be asserted against
        an expected value

        :param service: -
        :param api: -
        :param parameters: -

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            integ.assertions.aws_api_call("SQS", "sendMessage", {
                "QueueUrl": "url",
                "MessageBody": "hello"
            })
            message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
                "QueueUrl": "url"
            })
            message.expect(ExpectedResult.object_like({
                "Messages": [{"Body": "hello"}]
            }))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723b226a328538d949b8e3fec802059e60948bfb52f3a682201c3255a06b2372)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        return typing.cast(IAwsApiCall, jsii.invoke(self, "awsApiCall", [service, api, parameters]))

    @jsii.member(jsii_name="expect")
    def expect(
        self,
        id: builtins.str,
        expected: ExpectedResult,
        actual: ActualResult,
    ) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the ActualResult.

        :param id: -
        :param expected: -
        :param actual: -

        :stability: experimental

        Example::

            # integ: IntegTest
            # api_call: AwsApiCall
            
            integ.assertions.expect("invoke",
                ExpectedResult.object_like({"Payload": "OK"}),
                ActualResult.from_aws_api_call(api_call, "Body"))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1f8f020ba86c5a9596bc0ad7767aa1720d49b99dd755bd1521487942e58a75)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
        return typing.cast(None, jsii.invoke(self, "expect", [id, expected, actual]))

    @jsii.member(jsii_name="invokeFunction")
    def invoke_function(
        self,
        *,
        function_name: builtins.str,
        invocation_type: typing.Optional["InvocationType"] = None,
        log_type: typing.Optional["LogType"] = None,
        payload: typing.Optional[builtins.str] = None,
    ) -> IAwsApiCall:
        '''(experimental) Invoke a lambda function and return the response which can be asserted.

        :param function_name: (experimental) The name of the function to invoke.
        :param invocation_type: (experimental) The type of invocation to use. Default: InvocationType.REQUEST_RESPONE
        :param log_type: (experimental) Whether to return the logs as part of the response. Default: LogType.NONE
        :param payload: (experimental) Payload to send as part of the invoke. Default: - no payload

        :stability: experimental

        Example::

            # app: App
            # integ: IntegTest
            
            invoke = integ.assertions.invoke_function(
                function_name="my-function"
            )
            invoke.expect(ExpectedResult.object_like({
                "Payload": "200"
            }))
        '''
        props = LambdaInvokeFunctionProps(
            function_name=function_name,
            invocation_type=invocation_type,
            log_type=log_type,
            payload=payload,
        )

        return typing.cast(IAwsApiCall, jsii.invoke(self, "invokeFunction", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeployAssert).__jsii_proxy_class__ = lambda : _IDeployAssertProxy


class IntegTest(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.IntegTest",
):
    '''(experimental) A collection of test cases.

    Each test case file should contain exactly one
    instance of this class.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # lambda_function: lambda.IFunction
        # app: App
        
        
        stack = Stack(app, "cdk-integ-lambda-bundling")
        
        integ = IntegTest(app, "IntegTest",
            test_cases=[stack]
        )
        
        invoke = integ.assertions.invoke_function(
            function_name=lambda_function.function_name
        )
        invoke.expect(ExpectedResult.object_like({
            "Payload": "200"
        }))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        test_cases: typing.Sequence[_Stack_9f43e4a3],
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param test_cases: (experimental) List of test cases that make up this test.
        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef48575e9a5fbcea489cfd7a16367b4e236b712020e1881809f842dab5aba39)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IntegTestProps(
            test_cases=test_cases,
            allow_destroy=allow_destroy,
            cdk_command_options=cdk_command_options,
            diff_assets=diff_assets,
            hooks=hooks,
            regions=regions,
            stack_update_workflow=stack_update_workflow,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="onPrepare")
    def _on_prepare(self) -> None:
        '''(experimental) Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "onPrepare", []))

    @builtins.property
    @jsii.member(jsii_name="assertions")
    def assertions(self) -> IDeployAssert:
        '''(experimental) Make assertions on resources in this test case.

        :stability: experimental
        '''
        return typing.cast(IDeployAssert, jsii.get(self, "assertions"))


class IntegTestCase(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.IntegTestCase",
):
    '''(experimental) An integration test case. Allows the definition of test properties that apply to all stacks under this case.

    It is recommended that you use the IntegTest construct since that will create
    a default IntegTestCase

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import cloud_assembly_schema
        from monocdk import integ_tests
        
        # stack: monocdk.Stack
        
        integ_test_case = integ_tests.IntegTestCase(self, "MyIntegTestCase",
            stacks=[stack],
        
            # the properties below are optional
            allow_destroy=["allowDestroy"],
            cdk_command_options=cloud_assembly_schema.CdkCommands(
                deploy=cloud_assembly_schema.DeployCommand(
                    args=cloud_assembly_schema.DeployOptions(
                        all=False,
                        app="app",
                        asset_metadata=False,
                        ca_bundle_path="caBundlePath",
                        change_set_name="changeSetName",
                        ci=False,
                        color=False,
                        context={
                            "context_key": "context"
                        },
                        debug=False,
                        ec2_creds=False,
                        exclusively=False,
                        execute=False,
                        force=False,
                        ignore_errors=False,
                        json=False,
                        lookups=False,
                        notices=False,
                        notification_arns=["notificationArns"],
                        output="output",
                        outputs_file="outputsFile",
                        parameters={
                            "parameters_key": "parameters"
                        },
                        path_metadata=False,
                        profile="profile",
                        proxy="proxy",
                        require_approval=cloud_assembly_schema.RequireApproval.NEVER,
                        reuse_assets=["reuseAssets"],
                        role_arn="roleArn",
                        rollback=False,
                        stacks=["stacks"],
                        staging=False,
                        strict=False,
                        toolkit_stack_name="toolkitStackName",
                        trace=False,
                        use_previous_parameters=False,
                        verbose=False,
                        version_reporting=False
                    ),
                    enabled=False,
                    expected_message="expectedMessage",
                    expect_error=False
                ),
                destroy=cloud_assembly_schema.DestroyCommand(
                    args=cloud_assembly_schema.DestroyOptions(
                        all=False,
                        app="app",
                        asset_metadata=False,
                        ca_bundle_path="caBundlePath",
                        color=False,
                        context={
                            "context_key": "context"
                        },
                        debug=False,
                        ec2_creds=False,
                        exclusively=False,
                        force=False,
                        ignore_errors=False,
                        json=False,
                        lookups=False,
                        notices=False,
                        output="output",
                        path_metadata=False,
                        profile="profile",
                        proxy="proxy",
                        role_arn="roleArn",
                        stacks=["stacks"],
                        staging=False,
                        strict=False,
                        trace=False,
                        verbose=False,
                        version_reporting=False
                    ),
                    enabled=False,
                    expected_message="expectedMessage",
                    expect_error=False
                )
            ),
            diff_assets=False,
            hooks=cloud_assembly_schema.Hooks(
                post_deploy=["postDeploy"],
                post_destroy=["postDestroy"],
                pre_deploy=["preDeploy"],
                pre_destroy=["preDestroy"]
            ),
            regions=["regions"],
            stack_update_workflow=False
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        stacks: typing.Sequence[_Stack_9f43e4a3],
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stacks: (experimental) Stacks to be deployed during the test.
        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e24ac92f5a33fa4bbc3132f824907485994e5f58e912d454c8650f83727523)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IntegTestCaseProps(
            stacks=stacks,
            allow_destroy=allow_destroy,
            cdk_command_options=cdk_command_options,
            diff_assets=diff_assets,
            hooks=hooks,
            regions=regions,
            stack_update_workflow=stack_update_workflow,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assertions")
    def assertions(self) -> IDeployAssert:
        '''(experimental) Make assertions on resources in this test case.

        :stability: experimental
        '''
        return typing.cast(IDeployAssert, jsii.get(self, "assertions"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> _IntegManifest_8b169ea0:
        '''(experimental) The integration test manifest for this test case.

        Manifests are used
        by the integration test runner.

        :stability: experimental
        '''
        return typing.cast(_IntegManifest_8b169ea0, jsii.get(self, "manifest"))


@jsii.data_type(
    jsii_type="monocdk.integ_tests.IntegTestCaseProps",
    jsii_struct_bases=[_TestOptions_4ebd1db7],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "stacks": "stacks",
    },
)
class IntegTestCaseProps(_TestOptions_4ebd1db7):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        stacks: typing.Sequence[_Stack_9f43e4a3],
    ) -> None:
        '''(experimental) Properties of an integration test case.

        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param stacks: (experimental) Stacks to be deployed during the test.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import cloud_assembly_schema
            from monocdk import integ_tests
            
            # stack: monocdk.Stack
            
            integ_test_case_props = integ_tests.IntegTestCaseProps(
                stacks=[stack],
            
                # the properties below are optional
                allow_destroy=["allowDestroy"],
                cdk_command_options=cloud_assembly_schema.CdkCommands(
                    deploy=cloud_assembly_schema.DeployCommand(
                        args=cloud_assembly_schema.DeployOptions(
                            all=False,
                            app="app",
                            asset_metadata=False,
                            ca_bundle_path="caBundlePath",
                            change_set_name="changeSetName",
                            ci=False,
                            color=False,
                            context={
                                "context_key": "context"
                            },
                            debug=False,
                            ec2_creds=False,
                            exclusively=False,
                            execute=False,
                            force=False,
                            ignore_errors=False,
                            json=False,
                            lookups=False,
                            notices=False,
                            notification_arns=["notificationArns"],
                            output="output",
                            outputs_file="outputsFile",
                            parameters={
                                "parameters_key": "parameters"
                            },
                            path_metadata=False,
                            profile="profile",
                            proxy="proxy",
                            require_approval=cloud_assembly_schema.RequireApproval.NEVER,
                            reuse_assets=["reuseAssets"],
                            role_arn="roleArn",
                            rollback=False,
                            stacks=["stacks"],
                            staging=False,
                            strict=False,
                            toolkit_stack_name="toolkitStackName",
                            trace=False,
                            use_previous_parameters=False,
                            verbose=False,
                            version_reporting=False
                        ),
                        enabled=False,
                        expected_message="expectedMessage",
                        expect_error=False
                    ),
                    destroy=cloud_assembly_schema.DestroyCommand(
                        args=cloud_assembly_schema.DestroyOptions(
                            all=False,
                            app="app",
                            asset_metadata=False,
                            ca_bundle_path="caBundlePath",
                            color=False,
                            context={
                                "context_key": "context"
                            },
                            debug=False,
                            ec2_creds=False,
                            exclusively=False,
                            force=False,
                            ignore_errors=False,
                            json=False,
                            lookups=False,
                            notices=False,
                            output="output",
                            path_metadata=False,
                            profile="profile",
                            proxy="proxy",
                            role_arn="roleArn",
                            stacks=["stacks"],
                            staging=False,
                            strict=False,
                            trace=False,
                            verbose=False,
                            version_reporting=False
                        ),
                        enabled=False,
                        expected_message="expectedMessage",
                        expect_error=False
                    )
                ),
                diff_assets=False,
                hooks=cloud_assembly_schema.Hooks(
                    post_deploy=["postDeploy"],
                    post_destroy=["postDestroy"],
                    pre_deploy=["preDeploy"],
                    pre_destroy=["preDestroy"]
                ),
                regions=["regions"],
                stack_update_workflow=False
            )
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = _CdkCommands_3043a8a5(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = _Hooks_ffcd74d8(**hooks)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4cba82fb7f23f1c541750324cdfbedc3be7b1528482c716f40cc1ba24abc2c)
            check_type(argname="argument allow_destroy", value=allow_destroy, expected_type=type_hints["allow_destroy"])
            check_type(argname="argument cdk_command_options", value=cdk_command_options, expected_type=type_hints["cdk_command_options"])
            check_type(argname="argument diff_assets", value=diff_assets, expected_type=type_hints["diff_assets"])
            check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument stack_update_workflow", value=stack_update_workflow, expected_type=type_hints["stack_update_workflow"])
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update

        :stability: experimental
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(self) -> typing.Optional[_CdkCommands_3043a8a5]:
        '''(experimental) Additional options to use for each CDK command.

        :default: - runner default options

        :stability: experimental
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[_CdkCommands_3043a8a5], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false

        :stability: experimental
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[_Hooks_ffcd74d8]:
        '''(experimental) Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks

        :stability: experimental
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[_Hooks_ffcd74d8], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Limit deployment to these regions.

        :default: - can run in any region

        :stability: experimental
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stacks(self) -> typing.List[_Stack_9f43e4a3]:
        '''(experimental) Stacks to be deployed during the test.

        :stability: experimental
        '''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[_Stack_9f43e4a3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestCaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegTestCaseStack(
    _Stack_9f43e4a3,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.IntegTestCaseStack",
):
    '''(experimental) An integration test case stack. Allows the definition of test properties that should apply to this stack.

    This should be used if there are multiple stacks in the integration test
    and it is necessary to specify different test case option for each. Otherwise
    normal stacks should be added to IntegTest

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # app: App
        # stack_under_test: Stack
        
        test_case_with_assets = IntegTestCaseStack(app, "TestCaseAssets",
            diff_assets=True
        )
        
        IntegTest(app, "Integ", test_cases=[stack_under_test, test_case_with_assets])
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_Environment_0cfdf5e4, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_IStackSynthesizer_a39ceded] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param analytics_reporting: (experimental) Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: (experimental) A description of the stack. Default: - No description.
        :param env: (experimental) The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: (experimental) Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: (experimental) Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: (experimental) Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: (experimental) Whether to enable termination protection for this stack. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4e80692903d66ffe93fc80560d03d27fbfa8a0f9f1dbe102bdae86963c49f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IntegTestCaseStackProps(
            allow_destroy=allow_destroy,
            cdk_command_options=cdk_command_options,
            diff_assets=diff_assets,
            hooks=hooks,
            regions=regions,
            stack_update_workflow=stack_update_workflow,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isIntegTestCaseStack")
    @builtins.classmethod
    def is_integ_test_case_stack(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Returns whether the construct is a IntegTestCaseStack.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659dc864459a4d09f967ae43942dd4f6e3b37b161e292e93302a810cba19bbee)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isIntegTestCaseStack", [x]))

    @builtins.property
    @jsii.member(jsii_name="assertions")
    def assertions(self) -> IDeployAssert:
        '''(experimental) Make assertions on resources in this test case.

        :stability: experimental
        '''
        return typing.cast(IDeployAssert, jsii.get(self, "assertions"))


@jsii.data_type(
    jsii_type="monocdk.integ_tests.IntegTestCaseStackProps",
    jsii_struct_bases=[_TestOptions_4ebd1db7, _StackProps_484a498c],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "analytics_reporting": "analyticsReporting",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
    },
)
class IntegTestCaseStackProps(_TestOptions_4ebd1db7, _StackProps_484a498c):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_Environment_0cfdf5e4, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_IStackSynthesizer_a39ceded] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties of an integration test case stack.

        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param analytics_reporting: (experimental) Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: (experimental) A description of the stack. Default: - No description.
        :param env: (experimental) The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: (experimental) Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: (experimental) Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: (experimental) Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: (experimental) Whether to enable termination protection for this stack. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # app: App
            # stack_under_test: Stack
            
            test_case_with_assets = IntegTestCaseStack(app, "TestCaseAssets",
                diff_assets=True
            )
            
            IntegTest(app, "Integ", test_cases=[stack_under_test, test_case_with_assets])
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = _CdkCommands_3043a8a5(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = _Hooks_ffcd74d8(**hooks)
        if isinstance(env, dict):
            env = _Environment_0cfdf5e4(**env)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f747cb770ef4deba2a35a52d44c50e29acbfe8bcad2e890a64cc4d5af14b7a9c)
            check_type(argname="argument allow_destroy", value=allow_destroy, expected_type=type_hints["allow_destroy"])
            check_type(argname="argument cdk_command_options", value=cdk_command_options, expected_type=type_hints["cdk_command_options"])
            check_type(argname="argument diff_assets", value=diff_assets, expected_type=type_hints["diff_assets"])
            check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument stack_update_workflow", value=stack_update_workflow, expected_type=type_hints["stack_update_workflow"])
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update

        :stability: experimental
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(self) -> typing.Optional[_CdkCommands_3043a8a5]:
        '''(experimental) Additional options to use for each CDK command.

        :default: - runner default options

        :stability: experimental
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[_CdkCommands_3043a8a5], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false

        :stability: experimental
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[_Hooks_ffcd74d8]:
        '''(experimental) Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks

        :stability: experimental
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[_Hooks_ffcd74d8], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Limit deployment to these regions.

        :default: - can run in any region

        :stability: experimental
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key

        :stability: experimental
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the stack.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_Environment_0cfdf5e4]:
        '''(experimental) The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        :stability: experimental

        Example::

            # Use a concrete account and region to deploy this stack to:
            # `.account` and `.region` will simply return these values.
            Stack(app, "Stack1",
                env=cfn.Environment(
                    account="123456789012",
                    region="us-east-1"
                )
            )
            
            # Use the CLI's current credentials to determine the target environment:
            # `.account` and `.region` will reflect the account+region the CLI
            # is configured to use (based on the user CLI credentials)
            Stack(app, "Stack2",
                env=cfn.Environment(
                    account=process.env.CDK_DEFAULT_ACCOUNT,
                    region=process.env.CDK_DEFAULT_REGION
                )
            )
            
            # Define multiple stacks stage associated with an environment
            my_stage = Stage(app, "MyStage",
                env=cfn.Environment(
                    account="123456789012",
                    region="us-east-1"
                )
            )
            
            # both of these stacks will use the stage's account/region:
            # `.account` and `.region` will resolve to the concrete values as above
            MyStack(my_stage, "Stack1")
            YourStack(my_stage, "Stack2")
            
            # Define an environment-agnostic stack:
            # `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            # which will only resolve to actual values by CloudFormation during deployment.
            MyStack(app, "Stack1")
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_Environment_0cfdf5e4], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name to deploy the stack with.

        :default: - Derived from construct path.

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_IStackSynthesizer_a39ceded]:
        '''(experimental) Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.

        :stability: experimental
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_IStackSynthesizer_a39ceded], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable termination protection for this stack.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestCaseStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.integ_tests.IntegTestProps",
    jsii_struct_bases=[_TestOptions_4ebd1db7],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "test_cases": "testCases",
    },
)
class IntegTestProps(_TestOptions_4ebd1db7):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        test_cases: typing.Sequence[_Stack_9f43e4a3],
    ) -> None:
        '''(experimental) Integration test properties.

        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param test_cases: (experimental) List of test cases that make up this test.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # lambda_function: lambda.IFunction
            # app: App
            
            
            stack = Stack(app, "cdk-integ-lambda-bundling")
            
            integ = IntegTest(app, "IntegTest",
                test_cases=[stack]
            )
            
            invoke = integ.assertions.invoke_function(
                function_name=lambda_function.function_name
            )
            invoke.expect(ExpectedResult.object_like({
                "Payload": "200"
            }))
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = _CdkCommands_3043a8a5(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = _Hooks_ffcd74d8(**hooks)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53dc1f725a10fe89a339913fbcf33afc97f634e0d58d8cf180a2cd21adcc0dd)
            check_type(argname="argument allow_destroy", value=allow_destroy, expected_type=type_hints["allow_destroy"])
            check_type(argname="argument cdk_command_options", value=cdk_command_options, expected_type=type_hints["cdk_command_options"])
            check_type(argname="argument diff_assets", value=diff_assets, expected_type=type_hints["diff_assets"])
            check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument stack_update_workflow", value=stack_update_workflow, expected_type=type_hints["stack_update_workflow"])
            check_type(argname="argument test_cases", value=test_cases, expected_type=type_hints["test_cases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "test_cases": test_cases,
        }
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update

        :stability: experimental
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(self) -> typing.Optional[_CdkCommands_3043a8a5]:
        '''(experimental) Additional options to use for each CDK command.

        :default: - runner default options

        :stability: experimental
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[_CdkCommands_3043a8a5], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false

        :stability: experimental
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[_Hooks_ffcd74d8]:
        '''(experimental) Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks

        :stability: experimental
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[_Hooks_ffcd74d8], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Limit deployment to these regions.

        :default: - can run in any region

        :stability: experimental
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def test_cases(self) -> typing.List[_Stack_9f43e4a3]:
        '''(experimental) List of test cases that make up this test.

        :stability: experimental
        '''
        result = self._values.get("test_cases")
        assert result is not None, "Required property 'test_cases' is missing"
        return typing.cast(typing.List[_Stack_9f43e4a3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.integ_tests.InvocationType")
class InvocationType(enum.Enum):
    '''(experimental) The type of invocation.

    Default is REQUEST_RESPONE

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # app: App
        # stack: Stack
        # queue: sqs.Queue
        # fn: lambda.IFunction
        
        
        integ = IntegTest(app, "Integ",
            test_cases=[stack]
        )
        
        integ.assertions.invoke_function(
            function_name=fn.function_name,
            invocation_type=InvocationType.EVENT,
            payload=JSON.stringify({"status": "OK"})
        )
        
        message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
            "QueueUrl": queue.queue_url,
            "WaitTimeSeconds": 20
        })
        
        message.assert_at_path("Messages.0.Body", ExpectedResult.object_like({
            "request_context": {
                "condition": "Success"
            },
            "request_payload": {
                "status": "OK"
            },
            "response_context": {
                "status_code": 200
            },
            "response_payload": "success"
        }))
    '''

    EVENT = "EVENT"
    '''(experimental) Invoke the function asynchronously.

    Send events that fail multiple times to the function's
    dead-letter queue (if it's configured).
    The API response only includes a status code.

    :stability: experimental
    '''
    REQUEST_RESPONE = "REQUEST_RESPONE"
    '''(experimental) Invoke the function synchronously.

    Keep the connection open until the function returns a response or times out.
    The API response includes the function response and additional data.

    :stability: experimental
    '''
    DRY_RUN = "DRY_RUN"
    '''(experimental) Validate parameter values and verify that the user or role has permission to invoke the function.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.integ_tests.LambdaInvokeFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "invocation_type": "invocationType",
        "log_type": "logType",
        "payload": "payload",
    },
)
class LambdaInvokeFunctionProps:
    def __init__(
        self,
        *,
        function_name: builtins.str,
        invocation_type: typing.Optional[InvocationType] = None,
        log_type: typing.Optional["LogType"] = None,
        payload: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to pass to the Lambda invokeFunction API call.

        :param function_name: (experimental) The name of the function to invoke.
        :param invocation_type: (experimental) The type of invocation to use. Default: InvocationType.REQUEST_RESPONE
        :param log_type: (experimental) Whether to return the logs as part of the response. Default: LogType.NONE
        :param payload: (experimental) Payload to send as part of the invoke. Default: - no payload

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # lambda_function: lambda.IFunction
            # app: App
            
            
            stack = Stack(app, "cdk-integ-lambda-bundling")
            
            integ = IntegTest(app, "IntegTest",
                test_cases=[stack]
            )
            
            invoke = integ.assertions.invoke_function(
                function_name=lambda_function.function_name
            )
            invoke.expect(ExpectedResult.object_like({
                "Payload": "200"
            }))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff2d3d5282c2f5bfee238fa2d4727d4ea3028d2b47caeac19d24f05c5fb89b3)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
        }
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if log_type is not None:
            self._values["log_type"] = log_type
        if payload is not None:
            self._values["payload"] = payload

    @builtins.property
    def function_name(self) -> builtins.str:
        '''(experimental) The name of the function to invoke.

        :stability: experimental
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invocation_type(self) -> typing.Optional[InvocationType]:
        '''(experimental) The type of invocation to use.

        :default: InvocationType.REQUEST_RESPONE

        :stability: experimental
        '''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[InvocationType], result)

    @builtins.property
    def log_type(self) -> typing.Optional["LogType"]:
        '''(experimental) Whether to return the logs as part of the response.

        :default: LogType.NONE

        :stability: experimental
        '''
        result = self._values.get("log_type")
        return typing.cast(typing.Optional["LogType"], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''(experimental) Payload to send as part of the invoke.

        :default: - no payload

        :stability: experimental
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaInvokeFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.integ_tests.LogType")
class LogType(enum.Enum):
    '''(experimental) Set to Tail to include the execution log in the response.

    Applies to synchronously invoked functions only.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) The log messages are not returned in the response.

    :stability: experimental
    '''
    TAIL = "TAIL"
    '''(experimental) The log messages are returned in the response.

    :stability: experimental
    '''


class Match(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk.integ_tests.Match"):
    '''(experimental) Partial and special matching during assertions.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="arrayWith")
    @builtins.classmethod
    def array_with(
        cls,
        pattern: typing.Sequence[typing.Any],
    ) -> typing.Mapping[builtins.str, typing.List[typing.Any]]:
        '''(experimental) Matches the specified pattern with the array found in the same relative path of the target.

        The set of elements (or matchers) must be in the same order as would be found.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64909b1dd15243aae75315ba4f1c7a823168d5cd238cb3827bfc5e716571f644)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(typing.Mapping[builtins.str, typing.List[typing.Any]], jsii.sinvoke(cls, "arrayWith", [pattern]))

    @jsii.member(jsii_name="objectLike")
    @builtins.classmethod
    def object_like(
        cls,
        pattern: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Matches the specified pattern to an object found in the same relative path of the target.

        The keys and their values (or matchers) must be present in the target but the target can be a superset.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f15d0f9d9bbe8f64ee41e6fe34b6b267e6dcbafa487e54ed1385e53bf76d7f)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.sinvoke(cls, "objectLike", [pattern]))

    @jsii.member(jsii_name="stringLikeRegexp")
    @builtins.classmethod
    def string_like_regexp(
        cls,
        pattern: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Matches targets according to a regular expression.

        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637b7839a1018cba09f01b605443e0aaa5cfbcaf67e32c6b46d87655e61c0728)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.sinvoke(cls, "stringLikeRegexp", [pattern]))


class _MatchProxy(Match):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Match).__jsii_proxy_class__ = lambda : _MatchProxy


@jsii.enum(jsii_type="monocdk.integ_tests.Status")
class Status(enum.Enum):
    '''(experimental) The status of the assertion.

    :stability: experimental
    '''

    PASS = "PASS"
    '''(experimental) The assertion passed.

    :stability: experimental
    '''
    FAIL = "FAIL"
    '''(experimental) The assertion failed.

    :stability: experimental
    '''


@jsii.implements(IAwsApiCall)
class AwsApiCall(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.AwsApiCall",
):
    '''(experimental) Construct that creates a custom resource that will perform a query using the AWS SDK.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_app_stack: Stack
        
        
        AwsApiCall(my_app_stack, "GetObject",
            service="S3",
            api="getObject"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api: builtins.str,
        service: builtins.str,
        parameters: typing.Any = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api: (experimental) The api call to make, i.e. getBucketLifecycle.
        :param service: (experimental) The AWS service, i.e. S3.
        :param parameters: (experimental) Any parameters to pass to the api call. Default: - no parameters

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9433aa3f3211ddd27b77c08aa787a27cdc9da47edb0dc2046e5d586c4c14451a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsApiCallProps(api=api, service=service, parameters=parameters)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="assertAtPath")
    def assert_at_path(self, path: builtins.str, expected: ExpectedResult) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall at the given path.

        For example the SQS.receiveMessage api response would look
        like:

        If you wanted to assert the value of ``Body`` you could do

        :param path: -
        :param expected: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588f8f0f272020db53bf8d05bda550af33274ea71216aadfafc008619572e352)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(None, jsii.invoke(self, "assertAtPath", [path, expected]))

    @jsii.member(jsii_name="expect")
    def expect(self, expected: ExpectedResult) -> None:
        '''(experimental) Assert that the ExpectedResult is equal to the result of the AwsApiCall.

        :param expected: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab151a7952e4ad640c15aaeebc0df5b7da7dbb39bceb809ccace3316a653d09e)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(None, jsii.invoke(self, "expect", [expected]))

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: builtins.str) -> _Reference_a96c80b4:
        '''(experimental) Returns the value of an attribute of the custom resource of an arbitrary type.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25cd24c4428abba46fd5502507ce53dc6626378133209c3c21cb35bdb0111d2)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(_Reference_a96c80b4, jsii.invoke(self, "getAtt", [attribute_name]))

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attribute_name: builtins.str) -> builtins.str:
        '''(experimental) Returns the value of an attribute of the custom resource of type string.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb68108ac7fe4ebd1394e5abce2a9e0a455ab2eaa93402517cd31c603f8c3a3)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "getAttString", [attribute_name]))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def _provider(self) -> AssertionsProvider:
        '''
        :stability: experimental
        '''
        return typing.cast(AssertionsProvider, jsii.get(self, "provider"))

    @_provider.setter
    def _provider(self, value: AssertionsProvider) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4483065ebdcc19d54e17b4ea9adf21a5d28756d97308c59b099ecb80a2bc1b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provider", value)


class LambdaInvokeFunction(
    AwsApiCall,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.LambdaInvokeFunction",
):
    '''(experimental) An AWS Lambda Invoke function API call.

    Use this istead of the generic AwsApiCall in order to
    invoke a lambda function. This will automatically create
    the correct permissions to invoke the function

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import integ_tests
        
        lambda_invoke_function = integ_tests.LambdaInvokeFunction(self, "MyLambdaInvokeFunction",
            function_name="functionName",
        
            # the properties below are optional
            invocation_type=integ_tests.InvocationType.EVENT,
            log_type=integ_tests.LogType.NONE,
            payload="payload"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        function_name: builtins.str,
        invocation_type: typing.Optional[InvocationType] = None,
        log_type: typing.Optional[LogType] = None,
        payload: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param function_name: (experimental) The name of the function to invoke.
        :param invocation_type: (experimental) The type of invocation to use. Default: InvocationType.REQUEST_RESPONE
        :param log_type: (experimental) Whether to return the logs as part of the response. Default: LogType.NONE
        :param payload: (experimental) Payload to send as part of the invoke. Default: - no payload

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b87b947b888e7c0ce26f21eb017bbf287e64dff17dabae64a5525f36ae3435)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaInvokeFunctionProps(
            function_name=function_name,
            invocation_type=invocation_type,
            log_type=log_type,
            payload=payload,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "ActualResult",
    "AssertionRequest",
    "AssertionResult",
    "AssertionResultData",
    "AssertionType",
    "AssertionsProvider",
    "AwsApiCall",
    "AwsApiCallOptions",
    "AwsApiCallProps",
    "AwsApiCallRequest",
    "AwsApiCallResult",
    "EqualsAssertion",
    "EqualsAssertionProps",
    "ExpectedResult",
    "IAwsApiCall",
    "IDeployAssert",
    "IntegTest",
    "IntegTestCase",
    "IntegTestCaseProps",
    "IntegTestCaseStack",
    "IntegTestCaseStackProps",
    "IntegTestProps",
    "InvocationType",
    "LambdaInvokeFunction",
    "LambdaInvokeFunctionProps",
    "LogType",
    "Match",
    "Status",
]

publication.publish()

def _typecheckingstub__daf0a35dc8b584618fd101445f6a16a7474d4538a5211ee2180b04c43f0f3a0c(
    query: IAwsApiCall,
    attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fecb853311b88e6c54c8b6fc004c806cfa6883449057df1309c3fc1947c2e47(
    custom_resource: _CustomResource_9c5112da,
    attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5aae03de3c56c51ea3d29c34abbb0ce8708ca59206bf81cc4edfcdbc889596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4030e9d317d57ff13f4c6fcb1baeae719f184f98e633744958682a75855b1d9(
    *,
    actual: typing.Any,
    expected: typing.Any,
    fail_deployment: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bc0f7c539b19de148ea78fa0171d311bfd2eb2527bfeaacc675f7f22ebaa56(
    *,
    data: builtins.str,
    failed: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e481d2fa04efe9b510e1a833547070cca1d6e3798a736f5b324373fd46fbed7(
    *,
    status: Status,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9dde7b2d27b7d5a2254f873e27b33f47d3649a5d101bac96d5dad9074a8eb6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1e8cda486b554525db3a6b7c902d3ea86b5c776dbc4e6b8bb8d7608f5863b0(
    service: builtins.str,
    api: builtins.str,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b975ea2041b07f5835d6704c3e01ed13682dc7728fc231a3dc537ce4e88b5e(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca91f6bbceeef568696be4828a2c693f09e7e58145083b9e286e17d7e8fb4fbe(
    *,
    api: builtins.str,
    service: builtins.str,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf58de5f81726112fc71071644768b314ec33c41449e05321883ee28e3fa69f(
    *,
    api: builtins.str,
    service: builtins.str,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d303790b049091ffee968459a0e4f6e9553ac92c3ee4cb9478b7910978492de(
    *,
    api: builtins.str,
    service: builtins.str,
    flatten_response: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade32195848192ce06935a91a3e1612fc1f70d944975ea098ef990d2c1e7ab2d(
    *,
    api_call_response: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d48c7e24b52e0f50040fba910fc7422057e6f3c1939daffece409faf74e1649(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    actual: ActualResult,
    expected: ExpectedResult,
    fail_deployment: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a075d4dbe35ce6ab0999aac810f840f5c086acb98ceec83ed07e91a080cf763(
    *,
    actual: ActualResult,
    expected: ExpectedResult,
    fail_deployment: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e186bf8a3f6df778944f09d8ba1ed5307c8fc16c75d2fabbf80574fb5665899(
    expected: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e8f980394f80968ccd7c34ba31335c4dacd0dee22bd9002df14901fa1f4df2(
    expected: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a635ed49719edf557718ceec9185b3632ad7cacf350195c8005460ea0bf205(
    expected: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6cc452cf2f0633e1fe92f19789f0df4093f0cc8e114c92ea02024ff107c0ce(
    expected: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afc6ed0cb784ac0b9dca691bb58b664deacee4d0b57ab6ce6d8140719bf9760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c70c7539ab2dcec1d3ee533e8b251ff7b5c9fe7b37df11e7aa9e5f00bd33d01(
    path: builtins.str,
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607ba2652f958b9a1caff27ef81475647ce95319b7dd98410086122ff8d5241f(
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb5984af4e2f4d55dbf8453d59370029f37147e38d3c8d2b89c147f5212320a(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f02ac6d85512dbc03ddfbac4cd7eedafda9bd7fc0259275fef0535d9f652f26(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723b226a328538d949b8e3fec802059e60948bfb52f3a682201c3255a06b2372(
    service: builtins.str,
    api: builtins.str,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1f8f020ba86c5a9596bc0ad7767aa1720d49b99dd755bd1521487942e58a75(
    id: builtins.str,
    expected: ExpectedResult,
    actual: ActualResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef48575e9a5fbcea489cfd7a16367b4e236b712020e1881809f842dab5aba39(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    test_cases: typing.Sequence[_Stack_9f43e4a3],
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e24ac92f5a33fa4bbc3132f824907485994e5f58e912d454c8650f83727523(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    stacks: typing.Sequence[_Stack_9f43e4a3],
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4cba82fb7f23f1c541750324cdfbedc3be7b1528482c716f40cc1ba24abc2c(
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    stacks: typing.Sequence[_Stack_9f43e4a3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4e80692903d66ffe93fc80560d03d27fbfa8a0f9f1dbe102bdae86963c49f1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_Environment_0cfdf5e4, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_IStackSynthesizer_a39ceded] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659dc864459a4d09f967ae43942dd4f6e3b37b161e292e93302a810cba19bbee(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f747cb770ef4deba2a35a52d44c50e29acbfe8bcad2e890a64cc4d5af14b7a9c(
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_Environment_0cfdf5e4, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_IStackSynthesizer_a39ceded] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53dc1f725a10fe89a339913fbcf33afc97f634e0d58d8cf180a2cd21adcc0dd(
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[_CdkCommands_3043a8a5, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[_Hooks_ffcd74d8, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    test_cases: typing.Sequence[_Stack_9f43e4a3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff2d3d5282c2f5bfee238fa2d4727d4ea3028d2b47caeac19d24f05c5fb89b3(
    *,
    function_name: builtins.str,
    invocation_type: typing.Optional[InvocationType] = None,
    log_type: typing.Optional[LogType] = None,
    payload: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64909b1dd15243aae75315ba4f1c7a823168d5cd238cb3827bfc5e716571f644(
    pattern: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f15d0f9d9bbe8f64ee41e6fe34b6b267e6dcbafa487e54ed1385e53bf76d7f(
    pattern: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637b7839a1018cba09f01b605443e0aaa5cfbcaf67e32c6b46d87655e61c0728(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9433aa3f3211ddd27b77c08aa787a27cdc9da47edb0dc2046e5d586c4c14451a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api: builtins.str,
    service: builtins.str,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588f8f0f272020db53bf8d05bda550af33274ea71216aadfafc008619572e352(
    path: builtins.str,
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab151a7952e4ad640c15aaeebc0df5b7da7dbb39bceb809ccace3316a653d09e(
    expected: ExpectedResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25cd24c4428abba46fd5502507ce53dc6626378133209c3c21cb35bdb0111d2(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb68108ac7fe4ebd1394e5abce2a9e0a455ab2eaa93402517cd31c603f8c3a3(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4483065ebdcc19d54e17b4ea9adf21a5d28756d97308c59b099ecb80a2bc1b43(
    value: AssertionsProvider,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b87b947b888e7c0ce26f21eb017bbf287e64dff17dabae64a5525f36ae3435(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    function_name: builtins.str,
    invocation_type: typing.Optional[InvocationType] = None,
    log_type: typing.Optional[LogType] = None,
    payload: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
