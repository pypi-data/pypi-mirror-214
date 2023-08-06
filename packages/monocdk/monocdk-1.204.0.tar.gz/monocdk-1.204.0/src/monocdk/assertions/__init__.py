'''
# Assertions

If you're migrating from the old `assert` library, the migration guide can be found in
[our GitHub repository](https://github.com/aws/aws-cdk/blob/master/packages/@aws-cdk/assertions/MIGRATING.md).

Functions for writing test asserting against CDK applications, with focus on CloudFormation templates.

The `Template` class includes a set of methods for writing assertions against CloudFormation templates. Use one of the `Template.fromXxx()` static methods to create an instance of this class.

To create `Template` from CDK stack, start off with:

```python
from monocdk import Stack
from monocdk.assertions import Template

stack = Stack()
# ...
template = Template.from_stack(stack)
```

Alternatively, assertions can be run on an existing CloudFormation template -

```python
template_json = "{ \"Resources\": ... }" # The CloudFormation template as JSON serialized string.
template = Template.from_string(template_json)
```

## Full Template Match

The simplest assertion would be to assert that the template matches a given
template.

```python
template.template_matches({
    "Resources": {
        "BarLogicalId": {
            "Type": "Foo::Bar",
            "Properties": {
                "Baz": "Qux"
            }
        }
    }
})
```

By default, the `templateMatches()` API will use the an 'object-like' comparison,
which means that it will allow for the actual template to be a superset of the
given expectation. See [Special Matchers](#special-matchers) for details on how
to change this.

Snapshot testing is a common technique to store a snapshot of the output and
compare it during future changes. Since CloudFormation templates are human readable,
they are a good target for snapshot testing.

The `toJSON()` method on the `Template` can be used to produce a well formatted JSON
of the CloudFormation template that can be used as a snapshot.

See [Snapshot Testing in Jest](https://jestjs.io/docs/snapshot-testing) and [Snapshot
Testing in Java](https://json-snapshot.github.io/).

## Counting Resources

This module allows asserting the number of resources of a specific type found
in a template.

```python
template.resource_count_is("Foo::Bar", 2)
```

## Resource Matching & Retrieval

Beyond resource counting, the module also allows asserting that a resource with
specific properties are present.

The following code asserts that the `Properties` section of a resource of type
`Foo::Bar` contains the specified properties -

```python
template.has_resource_properties("Foo::Bar", {
    "Foo": "Bar",
    "Baz": 5,
    "Qux": ["Waldo", "Fred"]
})
```

Alternatively, if you would like to assert the entire resource definition, you
can use the `hasResource()` API.

```python
template.has_resource("Foo::Bar", {
    "Properties": {"Foo": "Bar"},
    "DependsOn": ["Waldo", "Fred"]
})
```

Beyond assertions, the module provides APIs to retrieve matching resources.
The `findResources()` API is complementary to the `hasResource()` API, except,
instead of asserting its presence, it returns the set of matching resources.

By default, the `hasResource()` and `hasResourceProperties()` APIs perform deep
partial object matching. This behavior can be configured using matchers.
See subsequent section on [special matchers](#special-matchers).

## Output and Mapping sections

The module allows you to assert that the CloudFormation template contains an Output
that matches specific properties. The following code asserts that a template contains
an Output with a `logicalId` of `Foo` and the specified properties -

```python
expected = {
    "Value": "Bar",
    "Export": {"Name": "ExportBaz"}
}
template.has_output("Foo", expected)
```

If you want to match against all Outputs in the template, use `*` as the `logicalId`.

```python
template.has_output("*", {
    "Value": "Bar",
    "Export": {"Name": "ExportBaz"}
})
```

`findOutputs()` will return a set of outputs that match the `logicalId` and `props`,
and you can use the `'*'` special case as well.

```python
result = template.find_outputs("*", {"Value": "Fred"})
expect(result.Foo).to_equal({"Value": "Fred", "Description": "FooFred"})
expect(result.Bar).to_equal({"Value": "Fred", "Description": "BarFred"})
```

The APIs `hasMapping()`, `findMappings()`, `hasCondition()`, and `hasCondtions()` provide similar functionalities.

## Special Matchers

The expectation provided to the `hasXxx()`, `findXxx()` and `templateMatches()`
APIs, besides carrying literal values, as seen in the above examples, also accept
special matchers.

They are available as part of the `Match` class.

### Object Matchers

The `Match.objectLike()` API can be used to assert that the target is a superset
object of the provided pattern.
This API will perform a deep partial match on the target.
Deep partial matching is where objects are matched partially recursively. At each
level, the list of keys in the target is a subset of the provided pattern.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": "Flob",
#           "Bob": "Cat"
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Wobble": "Flob"
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Brew": "Coffee"
    })
})
```

The `Match.objectEquals()` API can be used to assert a target as a deep exact
match.

### Presence and Absence

The `Match.absent()` matcher can be used to specify that a specific
value should not exist on the target. This can be used within `Match.objectLike()`
or outside of any matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": "Flob",
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Bob": Match.absent()
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Wobble": Match.absent()
    })
})
```

The `Match.anyValue()` matcher can be used to specify that a specific value should be found
at the location. This matcher will fail if when the target location has null-ish values
(i.e., `null` or `undefined`).

This matcher can be combined with any of the other matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": ["Flob", "Flib"],
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": {
        "Wobble": [Match.any_value(), Match.any_value()]
    }
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": {
        "Wimble": Match.any_value()
    }
})
```

### Array Matchers

The `Match.arrayWith()` API can be used to assert that the target is equal to or a subset
of the provided pattern array.
This API will perform subset match on the target.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"]
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.array_with(["Flob"])
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", Match.object_like({
    "Fred": Match.array_with(["Wobble"])
}))
```

*Note:* The list of items in the pattern array should be in order as they appear in the
target array. Out of order will be recorded as a match failure.

Alternatively, the `Match.arrayEquals()` API can be used to assert that the target is
exactly equal to the pattern array.

### String Matchers

The `Match.stringLikeRegexp()` API can be used to assert that the target matches the
provided regular expression.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Template": "const includeHeaders = true;"
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Template": Match.string_like_regexp("includeHeaders = (true|false)")
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Template": Match.string_like_regexp("includeHeaders = null")
})
```

### Not Matcher

The not matcher inverts the search pattern and matches all patterns in the path that does
not match the pattern specified.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"]
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.not(["Flob"])
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", Match.object_like({
    "Fred": Match.not(["Flob", "Cat"])
}))
```

### Serialized JSON

Often, we find that some CloudFormation Resource types declare properties as a string,
but actually expect JSON serialized as a string.
For example, the [`BuildSpec` property of `AWS::CodeBuild::Project`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildspec),
the [`Definition` property of `AWS::StepFunctions::StateMachine`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definition),
to name a couple.

The `Match.serializedJson()` matcher allows deep matching within a stringified JSON.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Baz": "{ \"Fred\": [\"Waldo\", \"Willow\"] }"
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Baz": Match.serialized_json({
        "Fred": Match.array_with(["Waldo"])
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Baz": Match.serialized_json({
        "Fred": ["Waldo", "Johnny"]
    })
})
```

## Capturing Values

The matcher APIs documented above allow capturing values in the matching entry
(Resource, Output, Mapping, etc.). The following code captures a string from a
matching resource.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"],
#         "Waldo": ["Qix", "Qux"],
#       }
#     }
#   }
# }

fred_capture = Capture()
waldo_capture = Capture()
template.has_resource_properties("Foo::Bar", {
    "Fred": fred_capture,
    "Waldo": ["Qix", waldo_capture]
})

fred_capture.as_array() # returns ["Flob", "Cat"]
waldo_capture.as_string()
```

With captures, a nested pattern can also be specified, so that only targets
that match the nested pattern will be captured. This pattern can be literals or
further Matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar1": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"],
#       }
#     }
#     "MyBar2": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Qix", "Qux"],
#       }
#     }
#   }
# }

capture = Capture(Match.array_with(["Cat"]))
template.has_resource_properties("Foo::Bar", {
    "Fred": capture
})

capture.as_array()
```

When multiple resources match the given condition, each `Capture` defined in
the condition will capture all matching values. They can be paged through using
the `next()` API. The following example illustrates this -

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": "Flob",
#       }
#     },
#     "MyBaz": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": "Quib",
#       }
#     }
#   }
# }

fred_capture = Capture()
template.has_resource_properties("Foo::Bar", {
    "Fred": fred_capture
})

fred_capture.as_string() # returns "Flob"
fred_capture.next() # returns true
fred_capture.as_string()
```

## Asserting Annotations

In addition to template matching, we provide an API for annotation matching.
[Annotations](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Annotations.html)
can be added via the [Aspects](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Aspects.html)
API. You can learn more about Aspects [here](https://docs.aws.amazon.com/cdk/v2/guide/aspects.html).

Say you have a `MyAspect` and a `MyStack` that uses `MyAspect`:

```python
import monocdk as cdk
from constructs import Construct, IConstruct

class MyAspect(cdk.IAspect):
    def visit(self, node):
        if node instanceof cdk.CfnResource && node.cfn_resource_type == "Foo::Bar":
            self.error(node, "we do not want a Foo::Bar resource")

    def error(self, node, message):
        cdk.Annotations.of(node).add_error(message)

class MyStack(cdk.Stack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        stack = cdk.Stack()
        cdk.CfnResource(stack, "Foo",
            type="Foo::Bar",
            properties={
                "Fred": "Thud"
            }
        )
        cdk.Aspects.of(stack).add(MyAspect())
```

We can then assert that the stack contains the expected Error:

```python
# import { Annotations } from '@aws-cdk/assertions';

Annotations.from_stack(stack).has_error("/Default/Foo", "we do not want a Foo::Bar resource")
```

Here are the available APIs for `Annotations`:

* `hasError()`, `hasNoError()`, and `findError()`
* `hasWarning()`, `hasNoWarning()`, and `findWarning()`
* `hasInfo()`, `hasNoInfo()`, and `findInfo()`

The corresponding `findXxx()` API is complementary to the `hasXxx()` API, except instead
of asserting its presence, it returns the set of matching messages.

In addition, this suite of APIs is compatable with `Matchers` for more fine-grained control.
For example, the following assertion works as well:

```python
Annotations.from_stack(stack).has_error("/Default/Foo",
    Match.string_like_regexp(".*Foo::Bar.*"))
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

from .. import Stack as _Stack_9f43e4a3
from ..cx_api import SynthesisMessage as _SynthesisMessage_1968e4cf


class Annotations(metaclass=jsii.JSIIMeta, jsii_type="monocdk.assertions.Annotations"):
    '''(experimental) Suite of assertions that can be run on a CDK Stack.

    Focused on asserting annotations.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import assertions
        
        # stack: monocdk.Stack
        
        annotations = assertions.Annotations.from_stack(stack)
    '''

    @jsii.member(jsii_name="fromStack")
    @builtins.classmethod
    def from_stack(cls, stack: _Stack_9f43e4a3) -> "Annotations":
        '''(experimental) Base your assertions on the messages returned by a synthesized CDK ``Stack``.

        :param stack: the CDK Stack to run assertions on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631733d3e9cbf6dd144f56e8e1e76592f94e432c1268a7584cb60e8d2995c1a1)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast("Annotations", jsii.sinvoke(cls, "fromStack", [stack]))

    @jsii.member(jsii_name="findError")
    def find_error(
        self,
        construct_path: builtins.str,
        message: typing.Any,
    ) -> typing.List[_SynthesisMessage_1968e4cf]:
        '''(experimental) Get the set of matching errors of a given construct path and message.

        :param construct_path: the construct path to the error. Provide ``'*'`` to match all errors in the template.
        :param message: the error message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5843e0441097ff9b51d3e784dcdd9a0c991f825e665bb44aed4f3204b702ff)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(typing.List[_SynthesisMessage_1968e4cf], jsii.invoke(self, "findError", [construct_path, message]))

    @jsii.member(jsii_name="findInfo")
    def find_info(
        self,
        construct_path: builtins.str,
        message: typing.Any,
    ) -> typing.List[_SynthesisMessage_1968e4cf]:
        '''(experimental) Get the set of matching infos of a given construct path and message.

        :param construct_path: the construct path to the info. Provide ``'*'`` to match all infos in the template.
        :param message: the info message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd603c25ba3674a7980ae2c03451b04038c56c1499be5b92df7eb9867a9e7c6e)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(typing.List[_SynthesisMessage_1968e4cf], jsii.invoke(self, "findInfo", [construct_path, message]))

    @jsii.member(jsii_name="findWarning")
    def find_warning(
        self,
        construct_path: builtins.str,
        message: typing.Any,
    ) -> typing.List[_SynthesisMessage_1968e4cf]:
        '''(experimental) Get the set of matching warning of a given construct path and message.

        :param construct_path: the construct path to the warning. Provide ``'*'`` to match all warnings in the template.
        :param message: the warning message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc59171fe0ad048de3f4becf789d6e72fa72787437094cee144abe5885bbd29)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(typing.List[_SynthesisMessage_1968e4cf], jsii.invoke(self, "findWarning", [construct_path, message]))

    @jsii.member(jsii_name="hasError")
    def has_error(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''(experimental) Assert that an error with the given message exists in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the error. Provide ``'*'`` to match all errors in the template.
        :param message: the error message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042cf76bedabb0e9aa892227e67a30735fcb6f734d373db633954dddead3f177)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasError", [construct_path, message]))

    @jsii.member(jsii_name="hasInfo")
    def has_info(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''(experimental) Assert that an info with the given message exists in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the info. Provide ``'*'`` to match all info in the template.
        :param message: the info message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbb8be64b62bbe1c6d0cf3f6d4a569d3518fa21be7823afca1ffda6b433320e)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasInfo", [construct_path, message]))

    @jsii.member(jsii_name="hasNoError")
    def has_no_error(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''(experimental) Assert that an error with the given message does not exist in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the error. Provide ``'*'`` to match all errors in the template.
        :param message: the error message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84442f20411134a3edd3302f7f4735b7b871b8915a9de59f3c64b7085cd3c769)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasNoError", [construct_path, message]))

    @jsii.member(jsii_name="hasNoInfo")
    def has_no_info(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''(experimental) Assert that an info with the given message does not exist in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the info. Provide ``'*'`` to match all info in the template.
        :param message: the info message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2093789f85597a71eb9d6b4f4406f1f9b3a7d0c9286a0b86174014bfb1e55be6)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasNoInfo", [construct_path, message]))

    @jsii.member(jsii_name="hasNoWarning")
    def has_no_warning(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''(experimental) Assert that an warning with the given message does not exist in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the warning. Provide ``'*'`` to match all warnings in the template.
        :param message: the warning message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebb02c60beed07a6cf513d4d88836be25e3852d7b7a449a303774f1a3e76a4f)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasNoWarning", [construct_path, message]))

    @jsii.member(jsii_name="hasWarning")
    def has_warning(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''(experimental) Assert that an warning with the given message exists in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the warning. Provide ``'*'`` to match all warnings in the template.
        :param message: the warning message as should be expected. This should be a string or Matcher object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32402c67be184452bd2e32e2fd7debd7b883d4f0556e6851d4eeb379b1f9f7bb)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasWarning", [construct_path, message]))


class Match(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk.assertions.Match"):
    '''(experimental) Partial and special matching during template assertions.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="absent")
    @builtins.classmethod
    def absent(cls) -> "Matcher":
        '''(experimental) Use this matcher in the place of a field's value, if the field must not be present.

        :stability: experimental
        '''
        return typing.cast("Matcher", jsii.sinvoke(cls, "absent", []))

    @jsii.member(jsii_name="anyValue")
    @builtins.classmethod
    def any_value(cls) -> "Matcher":
        '''(experimental) Matches any non-null value at the target.

        :stability: experimental
        '''
        return typing.cast("Matcher", jsii.sinvoke(cls, "anyValue", []))

    @jsii.member(jsii_name="arrayEquals")
    @builtins.classmethod
    def array_equals(cls, pattern: typing.Sequence[typing.Any]) -> "Matcher":
        '''(experimental) Matches the specified pattern with the array found in the same relative path of the target.

        The set of elements (or matchers) must match exactly and in order.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b167ddd9ea74818fa49327447dc2d6c1f35b2d1286d7776089691814b3720e9)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "arrayEquals", [pattern]))

    @jsii.member(jsii_name="arrayWith")
    @builtins.classmethod
    def array_with(cls, pattern: typing.Sequence[typing.Any]) -> "Matcher":
        '''(experimental) Matches the specified pattern with the array found in the same relative path of the target.

        The set of elements (or matchers) must be in the same order as would be found.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4f6917a5d78453c2474afcc05406c55843d4b56801a1a05b96579d7dff4eb1)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "arrayWith", [pattern]))

    @jsii.member(jsii_name="exact")
    @builtins.classmethod
    def exact(cls, pattern: typing.Any) -> "Matcher":
        '''(experimental) Deep exact matching of the specified pattern to the target.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc0b0f43f7b316ee6ada660d9af56ca6091a8998c97b5c47229f105b2e7369c)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "exact", [pattern]))

    @jsii.member(jsii_name="not")
    @builtins.classmethod
    def not_(cls, pattern: typing.Any) -> "Matcher":
        '''(experimental) Matches any target which does NOT follow the specified pattern.

        :param pattern: the pattern to NOT match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4148bac354697727088adee5e40b0a6a2c3e3f1afee804035e242b37340b30c5)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "not", [pattern]))

    @jsii.member(jsii_name="objectEquals")
    @builtins.classmethod
    def object_equals(
        cls,
        pattern: typing.Mapping[builtins.str, typing.Any],
    ) -> "Matcher":
        '''(experimental) Matches the specified pattern to an object found in the same relative path of the target.

        The keys and their values (or matchers) must match exactly with the target.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f2f9ff6ec50cde745ec0cbb6c3830aca18882b8df13a0edfd92f54e6971f8d)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "objectEquals", [pattern]))

    @jsii.member(jsii_name="objectLike")
    @builtins.classmethod
    def object_like(
        cls,
        pattern: typing.Mapping[builtins.str, typing.Any],
    ) -> "Matcher":
        '''(experimental) Matches the specified pattern to an object found in the same relative path of the target.

        The keys and their values (or matchers) must be present in the target but the target can be a superset.

        :param pattern: the pattern to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e884b502cf631cec101c3e1bb4dcd2d716dc2fccb98ddc7056ee074c48a843)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "objectLike", [pattern]))

    @jsii.member(jsii_name="serializedJson")
    @builtins.classmethod
    def serialized_json(cls, pattern: typing.Any) -> "Matcher":
        '''(experimental) Matches any string-encoded JSON and applies the specified pattern after parsing it.

        :param pattern: the pattern to match after parsing the encoded JSON.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91232162096617249dddc77f38aba300aabb2874b76c28f03bf177d7a5a7df5)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "serializedJson", [pattern]))

    @jsii.member(jsii_name="stringLikeRegexp")
    @builtins.classmethod
    def string_like_regexp(cls, pattern: builtins.str) -> "Matcher":
        '''(experimental) Matches targets according to a regular expression.

        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40cfe13e96e671bdd46ed7f365d8e61b04174f317b665c516b2519808dad0f4)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "stringLikeRegexp", [pattern]))


class _MatchProxy(Match):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Match).__jsii_proxy_class__ = lambda : _MatchProxy


@jsii.data_type(
    jsii_type="monocdk.assertions.MatchCapture",
    jsii_struct_bases=[],
    name_mapping={"capture": "capture", "value": "value"},
)
class MatchCapture:
    def __init__(self, *, capture: "Capture", value: typing.Any) -> None:
        '''(experimental) Information about a value captured during match.

        :param capture: (experimental) The instance of Capture class to which this capture is associated with.
        :param value: (experimental) The value that was captured.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import assertions
            
            # capture: assertions.Capture
            # value: Any
            
            match_capture = assertions.MatchCapture(
                capture=capture,
                value=value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5665ea797c63a2956995c48fd8c8c356e0ddd6fe9f5af3ada355c4756c8f305)
            check_type(argname="argument capture", value=capture, expected_type=type_hints["capture"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capture": capture,
            "value": value,
        }

    @builtins.property
    def capture(self) -> "Capture":
        '''(experimental) The instance of Capture class to which this capture is associated with.

        :stability: experimental
        '''
        result = self._values.get("capture")
        assert result is not None, "Required property 'capture' is missing"
        return typing.cast("Capture", result)

    @builtins.property
    def value(self) -> typing.Any:
        '''(experimental) The value that was captured.

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
        return "MatchCapture(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.assertions.MatchFailure",
    jsii_struct_bases=[],
    name_mapping={"matcher": "matcher", "message": "message", "path": "path"},
)
class MatchFailure:
    def __init__(
        self,
        *,
        matcher: "Matcher",
        message: builtins.str,
        path: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) Match failure details.

        :param matcher: (experimental) The matcher that had the failure.
        :param message: (experimental) Failure message.
        :param path: (experimental) The relative path in the target where the failure occurred. If the failure occurred at root of the match tree, set the path to an empty list. If it occurs in the 5th index of an array nested within the 'foo' key of an object, set the path as ``['/foo', '[5]']``.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import assertions
            
            # matcher: assertions.Matcher
            
            match_failure = assertions.MatchFailure(
                matcher=matcher,
                message="message",
                path=["path"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c8c62af0ae9b6a9dba10d5b9b04155d6641d1520e3231925ca732dfc1474ec)
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matcher": matcher,
            "message": message,
            "path": path,
        }

    @builtins.property
    def matcher(self) -> "Matcher":
        '''(experimental) The matcher that had the failure.

        :stability: experimental
        '''
        result = self._values.get("matcher")
        assert result is not None, "Required property 'matcher' is missing"
        return typing.cast("Matcher", result)

    @builtins.property
    def message(self) -> builtins.str:
        '''(experimental) Failure message.

        :stability: experimental
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.List[builtins.str]:
        '''(experimental) The relative path in the target where the failure occurred.

        If the failure occurred at root of the match tree, set the path to an empty list.
        If it occurs in the 5th index of an array nested within the 'foo' key of an object,
        set the path as ``['/foo', '[5]']``.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MatchFailure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MatchResult(metaclass=jsii.JSIIMeta, jsii_type="monocdk.assertions.MatchResult"):
    '''(experimental) The result of ``Match.test()``.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import assertions
        
        # target: Any
        
        match_result = assertions.MatchResult(target)
    '''

    def __init__(self, target: typing.Any) -> None:
        '''
        :param target: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5afff3196050cfacf5be5ba484a1017f20723720bf45b3c4bff868dc1b07e0c6)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        jsii.create(self.__class__, self, [target])

    @jsii.member(jsii_name="compose")
    def compose(self, id: builtins.str, inner: "MatchResult") -> "MatchResult":
        '''(experimental) Compose the results of a previous match as a subtree.

        :param id: the id of the parent tree.
        :param inner: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab12c2c0853c3bb3f921bc86fa791ea8e2fd2856e5f80661797d8f97b345ba7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inner", value=inner, expected_type=type_hints["inner"])
        return typing.cast("MatchResult", jsii.invoke(self, "compose", [id, inner]))

    @jsii.member(jsii_name="finished")
    def finished(self) -> "MatchResult":
        '''(experimental) Prepare the result to be analyzed.

        This API *must* be called prior to analyzing these results.

        :stability: experimental
        '''
        return typing.cast("MatchResult", jsii.invoke(self, "finished", []))

    @jsii.member(jsii_name="hasFailed")
    def has_failed(self) -> builtins.bool:
        '''(experimental) Does the result contain any failures.

        If not, the result is a success

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "hasFailed", []))

    @jsii.member(jsii_name="push")
    def push(
        self,
        matcher: "Matcher",
        path: typing.Sequence[builtins.str],
        message: builtins.str,
    ) -> "MatchResult":
        '''(deprecated) DEPRECATED.

        :param matcher: -
        :param path: -
        :param message: -

        :deprecated: use recordFailure()

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f6373e1fdd28fe6a9397977356aa962617d31135d57d9e5c1229fc0c9f3f59)
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast("MatchResult", jsii.invoke(self, "push", [matcher, path, message]))

    @jsii.member(jsii_name="recordCapture")
    def record_capture(self, *, capture: "Capture", value: typing.Any) -> None:
        '''(experimental) Record a capture against in this match result.

        :param capture: (experimental) The instance of Capture class to which this capture is associated with.
        :param value: (experimental) The value that was captured.

        :stability: experimental
        '''
        options = MatchCapture(capture=capture, value=value)

        return typing.cast(None, jsii.invoke(self, "recordCapture", [options]))

    @jsii.member(jsii_name="recordFailure")
    def record_failure(
        self,
        *,
        matcher: "Matcher",
        message: builtins.str,
        path: typing.Sequence[builtins.str],
    ) -> "MatchResult":
        '''(experimental) Record a new failure into this result at a specific path.

        :param matcher: (experimental) The matcher that had the failure.
        :param message: (experimental) Failure message.
        :param path: (experimental) The relative path in the target where the failure occurred. If the failure occurred at root of the match tree, set the path to an empty list. If it occurs in the 5th index of an array nested within the 'foo' key of an object, set the path as ``['/foo', '[5]']``.

        :stability: experimental
        '''
        failure = MatchFailure(matcher=matcher, message=message, path=path)

        return typing.cast("MatchResult", jsii.invoke(self, "recordFailure", [failure]))

    @jsii.member(jsii_name="toHumanStrings")
    def to_human_strings(self) -> typing.List[builtins.str]:
        '''(experimental) Get the list of failures as human readable strings.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "toHumanStrings", []))

    @builtins.property
    @jsii.member(jsii_name="failCount")
    def fail_count(self) -> jsii.Number:
        '''(experimental) The number of failures.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "failCount"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Any:
        '''(experimental) The target for which this result was generated.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "target"))


class Matcher(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk.assertions.Matcher"):
    '''(experimental) Represents a matcher that can perform special data matching capabilities between a given pattern and a target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Given a template -
        # {
        #   "Resources": {
        #     "MyBar": {
        #       "Type": "Foo::Bar",
        #       "Properties": {
        #         "Fred": ["Flob", "Cat"]
        #       }
        #     }
        #   }
        # }
        
        # The following will NOT throw an assertion error
        template.has_resource_properties("Foo::Bar", {
            "Fred": Match.array_with(["Flob"])
        })
        
        # The following will throw an assertion error
        template.has_resource_properties("Foo::Bar", Match.object_like({
            "Fred": Match.array_with(["Wobble"])
        }))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="isMatcher")
    @builtins.classmethod
    def is_matcher(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Check whether the provided object is a subtype of the ``IMatcher``.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9c371f30d92c6b0bdc6534b682186c35e16fdfc03346914c68995e35e493d9)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isMatcher", [x]))

    @jsii.member(jsii_name="test")
    @abc.abstractmethod
    def test(self, actual: typing.Any) -> MatchResult:
        '''(experimental) Test whether a target matches the provided pattern.

        Every Matcher must implement this method.
        This method will be invoked by the assertions framework. Do not call this method directly.

        :param actual: the target to match.

        :return: the list of match failures. An empty array denotes a successful match.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''(experimental) A name for the matcher.

        This is collected as part of the result and may be presented to the user.

        :stability: experimental
        '''
        ...


class _MatcherProxy(Matcher):
    @jsii.member(jsii_name="test")
    def test(self, actual: typing.Any) -> MatchResult:
        '''(experimental) Test whether a target matches the provided pattern.

        Every Matcher must implement this method.
        This method will be invoked by the assertions framework. Do not call this method directly.

        :param actual: the target to match.

        :return: the list of match failures. An empty array denotes a successful match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2304e6ad57ff9742a5b5fb8a6ac6db5e5ccc67a5de3ee45b355d3407732b7971)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
        return typing.cast(MatchResult, jsii.invoke(self, "test", [actual]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) A name for the matcher.

        This is collected as part of the result and may be presented to the user.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Matcher).__jsii_proxy_class__ = lambda : _MatcherProxy


class Template(metaclass=jsii.JSIIMeta, jsii_type="monocdk.assertions.Template"):
    '''(experimental) Suite of assertions that can be run on a CDK stack.

    Typically used, as part of unit tests, to validate that the rendered
    CloudFormation template has expected resources and properties.

    :stability: experimental
    :exampleMetadata: nofixture infused

    Example::

        from monocdk import Stack
        from monocdk.assertions import Template
        
        stack = Stack()
        # ...
        template = Template.from_stack(stack)
    '''

    @jsii.member(jsii_name="fromJSON")
    @builtins.classmethod
    def from_json(
        cls,
        template: typing.Mapping[builtins.str, typing.Any],
    ) -> "Template":
        '''(experimental) Base your assertions from an existing CloudFormation template formatted as an in-memory JSON object.

        :param template: the CloudFormation template formatted as a nested set of records.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c7cea01fb04135bee9305415b9a2a36e289d63ee239f8896de0a2d4c50628e)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        return typing.cast("Template", jsii.sinvoke(cls, "fromJSON", [template]))

    @jsii.member(jsii_name="fromStack")
    @builtins.classmethod
    def from_stack(cls, stack: _Stack_9f43e4a3) -> "Template":
        '''(experimental) Base your assertions on the CloudFormation template synthesized by a CDK ``Stack``.

        :param stack: the CDK Stack to run assertions on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d490fcf374cc0cce632253030bc6590adb470f7cff97d5b91dd679111549edaf)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast("Template", jsii.sinvoke(cls, "fromStack", [stack]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, template: builtins.str) -> "Template":
        '''(experimental) Base your assertions from an existing CloudFormation template formatted as a JSON string.

        :param template: the CloudFormation template in.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5724918628e8208d75ae84f6b2eb9a2fdf6ad494a6ff7c1eb11d1afde4394b58)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        return typing.cast("Template", jsii.sinvoke(cls, "fromString", [template]))

    @jsii.member(jsii_name="findConditions")
    def find_conditions(
        self,
        logical_id: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Get the set of matching Conditions that match the given properties in the CloudFormation template.

        :param logical_id: the name of the condition. Provide ``'*'`` to match all conditions in the template.
        :param props: by default, matches all Conditions in the template. When a literal object is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd64d74015130952b98248a812280017f418e35fdf31a3c924c0f17935eecfd)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findConditions", [logical_id, props]))

    @jsii.member(jsii_name="findMappings")
    def find_mappings(
        self,
        logical_id: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Get the set of matching Mappings that match the given properties in the CloudFormation template.

        :param logical_id: the name of the mapping. Provide ``'*'`` to match all mappings in the template.
        :param props: by default, matches all Mappings in the template. When a literal object is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b78ca55ced37240b8d1f3dc9031399c72127367b988c6f7f6971ffaf22caa6)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findMappings", [logical_id, props]))

    @jsii.member(jsii_name="findOutputs")
    def find_outputs(
        self,
        logical_id: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Get the set of matching Outputs that match the given properties in the CloudFormation template.

        :param logical_id: the name of the output. Provide ``'*'`` to match all outputs in the template.
        :param props: by default, matches all Outputs in the template. When a literal object is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51c688a8a27e11c97f1207db55cb136d304131654814cff7ae24e021ba5fe2c)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findOutputs", [logical_id, props]))

    @jsii.member(jsii_name="findParameters")
    def find_parameters(
        self,
        logical_id: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Get the set of matching Parameters that match the given properties in the CloudFormation template.

        :param logical_id: the name of the parameter. Provide ``'*'`` to match all parameters in the template.
        :param props: by default, matches all Parameters in the template. When a literal object is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a47b2f071bcd44f0b0ea6bb7cdb99ee01e243382cbb08c1f5213a7b846b5fed)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findParameters", [logical_id, props]))

    @jsii.member(jsii_name="findResources")
    def find_resources(
        self,
        type: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Get the set of matching resources of a given type and properties in the CloudFormation template.

        :param type: the type to match in the CloudFormation template.
        :param props: by default, matches all resources with the given type. When a literal is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f85ea819d247656659b2fd5dc9f0c052153cb8dde82d85c579d57d67bc66372)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findResources", [type, props]))

    @jsii.member(jsii_name="hasCondition")
    def has_condition(self, logical_id: builtins.str, props: typing.Any) -> None:
        '''(experimental) Assert that a Condition with the given properties exists in the CloudFormation template.

        By default, performs partial matching on the resource, via the ``Match.objectLike()``.
        To configure different behavour, use other matchers in the ``Match`` class.

        :param logical_id: the name of the mapping. Provide ``'*'`` to match all conditions in the template.
        :param props: the output as should be expected in the template.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994787fd32b729a5a0c79b9f654ea00e2bb0d04ec6f5b412aee27b2b60e85be0)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasCondition", [logical_id, props]))

    @jsii.member(jsii_name="hasMapping")
    def has_mapping(self, logical_id: builtins.str, props: typing.Any) -> None:
        '''(experimental) Assert that a Mapping with the given properties exists in the CloudFormation template.

        By default, performs partial matching on the resource, via the ``Match.objectLike()``.
        To configure different behavour, use other matchers in the ``Match`` class.

        :param logical_id: the name of the mapping. Provide ``'*'`` to match all mappings in the template.
        :param props: the output as should be expected in the template.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a4bddb34550b90785422f2af5252548399970bfc8de64222b208adda060b39)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasMapping", [logical_id, props]))

    @jsii.member(jsii_name="hasOutput")
    def has_output(self, logical_id: builtins.str, props: typing.Any) -> None:
        '''(experimental) Assert that an Output with the given properties exists in the CloudFormation template.

        By default, performs partial matching on the resource, via the ``Match.objectLike()``.
        To configure different behavour, use other matchers in the ``Match`` class.

        :param logical_id: the name of the output. Provide ``'*'`` to match all outputs in the template.
        :param props: the output as should be expected in the template.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881ab1526be28edb945aadbff8033fea2b91de79c604cb8f071b545ee4a202e5)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasOutput", [logical_id, props]))

    @jsii.member(jsii_name="hasParameter")
    def has_parameter(self, logical_id: builtins.str, props: typing.Any) -> None:
        '''(experimental) Assert that a Parameter with the given properties exists in the CloudFormation template.

        By default, performs partial matching on the parameter, via the ``Match.objectLike()``.
        To configure different behavior, use other matchers in the ``Match`` class.

        :param logical_id: the name of the parameter. Provide ``'*'`` to match all parameters in the template.
        :param props: the parameter as should be expected in the template.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10136c681450ad497cd39b7459bfd85deed7c8b707ba681ef4d9fe96223bcded)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasParameter", [logical_id, props]))

    @jsii.member(jsii_name="hasResource")
    def has_resource(self, type: builtins.str, props: typing.Any) -> None:
        '''(experimental) Assert that a resource of the given type and given definition exists in the CloudFormation template.

        By default, performs partial matching on the resource, via the ``Match.objectLike()``.
        To configure different behavour, use other matchers in the ``Match`` class.

        :param type: the resource type; ex: ``AWS::S3::Bucket``
        :param props: the entire defintion of the resource as should be expected in the template.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746548bb6a90546de4c1b1e5d284286f881a9a8ade79e85a252c8f6a1340a945)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasResource", [type, props]))

    @jsii.member(jsii_name="hasResourceProperties")
    def has_resource_properties(self, type: builtins.str, props: typing.Any) -> None:
        '''(experimental) Assert that a resource of the given type and properties exists in the CloudFormation template.

        By default, performs partial matching on the ``Properties`` key of the resource, via the
        ``Match.objectLike()``. To configure different behavour, use other matchers in the ``Match`` class.

        :param type: the resource type; ex: ``AWS::S3::Bucket``
        :param props: the 'Properties' section of the resource as should be expected in the template.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836a25da815014f8d9d85d32300a2f3919e7e8695baf98491348e6802354e9cf)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasResourceProperties", [type, props]))

    @jsii.member(jsii_name="resourceCountIs")
    def resource_count_is(self, type: builtins.str, count: jsii.Number) -> None:
        '''(experimental) Assert that the given number of resources of the given type exist in the template.

        :param type: the resource type; ex: ``AWS::S3::Bucket``
        :param count: number of expected instances.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560838bce55105f8a25259588f7bd48cd6544187f85d797ee53999e7b21722d2)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        return typing.cast(None, jsii.invoke(self, "resourceCountIs", [type, count]))

    @jsii.member(jsii_name="templateMatches")
    def template_matches(self, expected: typing.Any) -> None:
        '''(experimental) Assert that the CloudFormation template matches the given value.

        :param expected: the expected CloudFormation template as key-value pairs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e1bd0753ce93b848cb0726822a124a30d3fc15ad7cf8db150c7c5cdd5098f5)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(None, jsii.invoke(self, "templateMatches", [expected]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) The CloudFormation template deserialized into an object.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "toJSON", []))


class Capture(Matcher, metaclass=jsii.JSIIMeta, jsii_type="monocdk.assertions.Capture"):
    '''(experimental) Capture values while matching templates.

    Using an instance of this class within a Matcher will capture the matching value.
    The ``as*()`` APIs on the instance can be used to get the captured value.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Given a template -
        # {
        #   "Resources": {
        #     "MyBar": {
        #       "Type": "Foo::Bar",
        #       "Properties": {
        #         "Fred": "Flob",
        #       }
        #     },
        #     "MyBaz": {
        #       "Type": "Foo::Bar",
        #       "Properties": {
        #         "Fred": "Quib",
        #       }
        #     }
        #   }
        # }
        
        fred_capture = Capture()
        template.has_resource_properties("Foo::Bar", {
            "Fred": fred_capture
        })
        
        fred_capture.as_string() # returns "Flob"
        fred_capture.next() # returns true
        fred_capture.as_string()
    '''

    def __init__(self, pattern: typing.Any = None) -> None:
        '''(experimental) Initialize a new capture.

        :param pattern: a nested pattern or Matcher. If a nested pattern is provided ``objectLike()`` matching is applied.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f83a963a4f389a16f17763a3427190f9fc3ca72f9fd78e59bae235659d2e83)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        jsii.create(self.__class__, self, [pattern])

    @jsii.member(jsii_name="asArray")
    def as_array(self) -> typing.List[typing.Any]:
        '''(experimental) Retrieve the captured value as an array.

        An error is generated if no value is captured or if the value is not an array.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "asArray", []))

    @jsii.member(jsii_name="asBoolean")
    def as_boolean(self) -> builtins.bool:
        '''(experimental) Retrieve the captured value as a boolean.

        An error is generated if no value is captured or if the value is not a boolean.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "asBoolean", []))

    @jsii.member(jsii_name="asNumber")
    def as_number(self) -> jsii.Number:
        '''(experimental) Retrieve the captured value as a number.

        An error is generated if no value is captured or if the value is not a number.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "asNumber", []))

    @jsii.member(jsii_name="asObject")
    def as_object(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Retrieve the captured value as a JSON object.

        An error is generated if no value is captured or if the value is not an object.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "asObject", []))

    @jsii.member(jsii_name="asString")
    def as_string(self) -> builtins.str:
        '''(experimental) Retrieve the captured value as a string.

        An error is generated if no value is captured or if the value is not a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "asString", []))

    @jsii.member(jsii_name="next")
    def next(self) -> builtins.bool:
        '''(experimental) When multiple results are captured, move the iterator to the next result.

        :return: true if another capture is present, false otherwise

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "next", []))

    @jsii.member(jsii_name="test")
    def test(self, actual: typing.Any) -> MatchResult:
        '''(experimental) Test whether a target matches the provided pattern.

        Every Matcher must implement this method.
        This method will be invoked by the assertions framework. Do not call this method directly.

        :param actual: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1e24130fc87f4a80d122da6f4a6748b852079c231f823b6820525a2a19db3e)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
        return typing.cast(MatchResult, jsii.invoke(self, "test", [actual]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) A name for the matcher.

        This is collected as part of the result and may be presented to the user.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


__all__ = [
    "Annotations",
    "Capture",
    "Match",
    "MatchCapture",
    "MatchFailure",
    "MatchResult",
    "Matcher",
    "Template",
]

publication.publish()

def _typecheckingstub__631733d3e9cbf6dd144f56e8e1e76592f94e432c1268a7584cb60e8d2995c1a1(
    stack: _Stack_9f43e4a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5843e0441097ff9b51d3e784dcdd9a0c991f825e665bb44aed4f3204b702ff(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd603c25ba3674a7980ae2c03451b04038c56c1499be5b92df7eb9867a9e7c6e(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc59171fe0ad048de3f4becf789d6e72fa72787437094cee144abe5885bbd29(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042cf76bedabb0e9aa892227e67a30735fcb6f734d373db633954dddead3f177(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbb8be64b62bbe1c6d0cf3f6d4a569d3518fa21be7823afca1ffda6b433320e(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84442f20411134a3edd3302f7f4735b7b871b8915a9de59f3c64b7085cd3c769(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2093789f85597a71eb9d6b4f4406f1f9b3a7d0c9286a0b86174014bfb1e55be6(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebb02c60beed07a6cf513d4d88836be25e3852d7b7a449a303774f1a3e76a4f(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32402c67be184452bd2e32e2fd7debd7b883d4f0556e6851d4eeb379b1f9f7bb(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b167ddd9ea74818fa49327447dc2d6c1f35b2d1286d7776089691814b3720e9(
    pattern: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4f6917a5d78453c2474afcc05406c55843d4b56801a1a05b96579d7dff4eb1(
    pattern: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc0b0f43f7b316ee6ada660d9af56ca6091a8998c97b5c47229f105b2e7369c(
    pattern: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4148bac354697727088adee5e40b0a6a2c3e3f1afee804035e242b37340b30c5(
    pattern: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f2f9ff6ec50cde745ec0cbb6c3830aca18882b8df13a0edfd92f54e6971f8d(
    pattern: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e884b502cf631cec101c3e1bb4dcd2d716dc2fccb98ddc7056ee074c48a843(
    pattern: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91232162096617249dddc77f38aba300aabb2874b76c28f03bf177d7a5a7df5(
    pattern: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40cfe13e96e671bdd46ed7f365d8e61b04174f317b665c516b2519808dad0f4(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5665ea797c63a2956995c48fd8c8c356e0ddd6fe9f5af3ada355c4756c8f305(
    *,
    capture: Capture,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c8c62af0ae9b6a9dba10d5b9b04155d6641d1520e3231925ca732dfc1474ec(
    *,
    matcher: Matcher,
    message: builtins.str,
    path: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afff3196050cfacf5be5ba484a1017f20723720bf45b3c4bff868dc1b07e0c6(
    target: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab12c2c0853c3bb3f921bc86fa791ea8e2fd2856e5f80661797d8f97b345ba7(
    id: builtins.str,
    inner: MatchResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f6373e1fdd28fe6a9397977356aa962617d31135d57d9e5c1229fc0c9f3f59(
    matcher: Matcher,
    path: typing.Sequence[builtins.str],
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9c371f30d92c6b0bdc6534b682186c35e16fdfc03346914c68995e35e493d9(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2304e6ad57ff9742a5b5fb8a6ac6db5e5ccc67a5de3ee45b355d3407732b7971(
    actual: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c7cea01fb04135bee9305415b9a2a36e289d63ee239f8896de0a2d4c50628e(
    template: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d490fcf374cc0cce632253030bc6590adb470f7cff97d5b91dd679111549edaf(
    stack: _Stack_9f43e4a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5724918628e8208d75ae84f6b2eb9a2fdf6ad494a6ff7c1eb11d1afde4394b58(
    template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd64d74015130952b98248a812280017f418e35fdf31a3c924c0f17935eecfd(
    logical_id: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b78ca55ced37240b8d1f3dc9031399c72127367b988c6f7f6971ffaf22caa6(
    logical_id: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51c688a8a27e11c97f1207db55cb136d304131654814cff7ae24e021ba5fe2c(
    logical_id: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a47b2f071bcd44f0b0ea6bb7cdb99ee01e243382cbb08c1f5213a7b846b5fed(
    logical_id: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f85ea819d247656659b2fd5dc9f0c052153cb8dde82d85c579d57d67bc66372(
    type: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994787fd32b729a5a0c79b9f654ea00e2bb0d04ec6f5b412aee27b2b60e85be0(
    logical_id: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a4bddb34550b90785422f2af5252548399970bfc8de64222b208adda060b39(
    logical_id: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881ab1526be28edb945aadbff8033fea2b91de79c604cb8f071b545ee4a202e5(
    logical_id: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10136c681450ad497cd39b7459bfd85deed7c8b707ba681ef4d9fe96223bcded(
    logical_id: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746548bb6a90546de4c1b1e5d284286f881a9a8ade79e85a252c8f6a1340a945(
    type: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836a25da815014f8d9d85d32300a2f3919e7e8695baf98491348e6802354e9cf(
    type: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560838bce55105f8a25259588f7bd48cd6544187f85d797ee53999e7b21722d2(
    type: builtins.str,
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e1bd0753ce93b848cb0726822a124a30d3fc15ad7cf8db150c7c5cdd5098f5(
    expected: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f83a963a4f389a16f17763a3427190f9fc3ca72f9fd78e59bae235659d2e83(
    pattern: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1e24130fc87f4a80d122da6f4a6748b852079c231f823b6820525a2a19db3e(
    actual: typing.Any,
) -> None:
    """Type checking stubs"""
    pass
