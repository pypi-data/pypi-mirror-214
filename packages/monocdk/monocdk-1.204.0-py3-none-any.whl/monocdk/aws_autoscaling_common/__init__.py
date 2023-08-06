'''
# AWS AutoScaling Common Library

This is a sister package to `@aws-cdk/aws-autoscaling` and
`@aws-cdk/aws-applicationautoscaling`. It contains shared implementation
details between them.

It does not need to be used directly.
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


@jsii.data_type(
    jsii_type="monocdk.aws_autoscaling_common.Alarms",
    jsii_struct_bases=[],
    name_mapping={
        "lower_alarm_interval_index": "lowerAlarmIntervalIndex",
        "upper_alarm_interval_index": "upperAlarmIntervalIndex",
    },
)
class Alarms:
    def __init__(
        self,
        *,
        lower_alarm_interval_index: typing.Optional[jsii.Number] = None,
        upper_alarm_interval_index: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lower_alarm_interval_index: 
        :param upper_alarm_interval_index: 

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_autoscaling_common as autoscaling_common
            
            alarms = autoscaling_common.Alarms(
                lower_alarm_interval_index=123,
                upper_alarm_interval_index=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effd62bed4f1d403fe62740ebfaa5e71aca023a8db05d622d40488d2b6ec5636)
            check_type(argname="argument lower_alarm_interval_index", value=lower_alarm_interval_index, expected_type=type_hints["lower_alarm_interval_index"])
            check_type(argname="argument upper_alarm_interval_index", value=upper_alarm_interval_index, expected_type=type_hints["upper_alarm_interval_index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lower_alarm_interval_index is not None:
            self._values["lower_alarm_interval_index"] = lower_alarm_interval_index
        if upper_alarm_interval_index is not None:
            self._values["upper_alarm_interval_index"] = upper_alarm_interval_index

    @builtins.property
    def lower_alarm_interval_index(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lower_alarm_interval_index")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def upper_alarm_interval_index(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("upper_alarm_interval_index")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Alarms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_autoscaling_common.ArbitraryIntervals",
    jsii_struct_bases=[],
    name_mapping={"absolute": "absolute", "intervals": "intervals"},
)
class ArbitraryIntervals:
    def __init__(
        self,
        *,
        absolute: builtins.bool,
        intervals: typing.Sequence[typing.Union["ScalingInterval", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param absolute: 
        :param intervals: 

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_autoscaling_common as autoscaling_common
            
            arbitrary_intervals = autoscaling_common.ArbitraryIntervals(
                absolute=False,
                intervals=[autoscaling_common.ScalingInterval(
                    change=123,
            
                    # the properties below are optional
                    lower=123,
                    upper=123
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9496ac1870eaa02210290e23658484940f8aed51ba6d9cbaadc3b2ebaab35fe4)
            check_type(argname="argument absolute", value=absolute, expected_type=type_hints["absolute"])
            check_type(argname="argument intervals", value=intervals, expected_type=type_hints["intervals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "absolute": absolute,
            "intervals": intervals,
        }

    @builtins.property
    def absolute(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        result = self._values.get("absolute")
        assert result is not None, "Required property 'absolute' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def intervals(self) -> typing.List["ScalingInterval"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("intervals")
        assert result is not None, "Required property 'intervals' is missing"
        return typing.cast(typing.List["ScalingInterval"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArbitraryIntervals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_autoscaling_common.CompleteScalingInterval",
    jsii_struct_bases=[],
    name_mapping={"lower": "lower", "upper": "upper", "change": "change"},
)
class CompleteScalingInterval:
    def __init__(
        self,
        *,
        lower: jsii.Number,
        upper: jsii.Number,
        change: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lower: 
        :param upper: 
        :param change: 

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_autoscaling_common as autoscaling_common
            
            complete_scaling_interval = autoscaling_common.CompleteScalingInterval(
                lower=123,
                upper=123,
            
                # the properties below are optional
                change=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb51740ae832ae7afb08e341768a116d792dd8782eb7ca3c6731852cd1437bed)
            check_type(argname="argument lower", value=lower, expected_type=type_hints["lower"])
            check_type(argname="argument upper", value=upper, expected_type=type_hints["upper"])
            check_type(argname="argument change", value=change, expected_type=type_hints["change"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lower": lower,
            "upper": upper,
        }
        if change is not None:
            self._values["change"] = change

    @builtins.property
    def lower(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("lower")
        assert result is not None, "Required property 'lower' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def upper(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("upper")
        assert result is not None, "Required property 'upper' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def change(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("change")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompleteScalingInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_autoscaling_common.IRandomGenerator")
class IRandomGenerator(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        '''
        :param min: -
        :param max: -

        :stability: experimental
        '''
        ...


class _IRandomGeneratorProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_autoscaling_common.IRandomGenerator"

    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "nextBoolean", []))

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        '''
        :param min: -
        :param max: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb4ea42dd4a6070fb443031246674bdeee6fdebe0e381eff9065b93a46801e2)
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
        return typing.cast(jsii.Number, jsii.invoke(self, "nextInt", [min, max]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRandomGenerator).__jsii_proxy_class__ = lambda : _IRandomGeneratorProxy


@jsii.data_type(
    jsii_type="monocdk.aws_autoscaling_common.ScalingInterval",
    jsii_struct_bases=[],
    name_mapping={"change": "change", "lower": "lower", "upper": "upper"},
)
class ScalingInterval:
    def __init__(
        self,
        *,
        change: jsii.Number,
        lower: typing.Optional[jsii.Number] = None,
        upper: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) A range of metric values in which to apply a certain scaling operation.

        :param change: (experimental) The capacity adjustment to apply in this interval. The number is interpreted differently based on AdjustmentType: - ChangeInCapacity: add the adjustment to the current capacity. The number can be positive or negative. - PercentChangeInCapacity: add or remove the given percentage of the current capacity to itself. The number can be in the range [-100..100]. - ExactCapacity: set the capacity to this number. The number must be positive.
        :param lower: (experimental) The lower bound of the interval. The scaling adjustment will be applied if the metric is higher than this value. Default: Threshold automatically derived from neighbouring intervals
        :param upper: (experimental) The upper bound of the interval. The scaling adjustment will be applied if the metric is lower than this value. Default: Threshold automatically derived from neighbouring intervals

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_autoscaling_common as autoscaling_common
            
            scaling_interval = autoscaling_common.ScalingInterval(
                change=123,
            
                # the properties below are optional
                lower=123,
                upper=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19d74c45e1f3e2cfbe3ff6d9863f5d02724a24dfbb036cb67e709dc9a80165a)
            check_type(argname="argument change", value=change, expected_type=type_hints["change"])
            check_type(argname="argument lower", value=lower, expected_type=type_hints["lower"])
            check_type(argname="argument upper", value=upper, expected_type=type_hints["upper"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "change": change,
        }
        if lower is not None:
            self._values["lower"] = lower
        if upper is not None:
            self._values["upper"] = upper

    @builtins.property
    def change(self) -> jsii.Number:
        '''(experimental) The capacity adjustment to apply in this interval.

        The number is interpreted differently based on AdjustmentType:

        - ChangeInCapacity: add the adjustment to the current capacity.
          The number can be positive or negative.
        - PercentChangeInCapacity: add or remove the given percentage of the current
          capacity to itself. The number can be in the range [-100..100].
        - ExactCapacity: set the capacity to this number. The number must
          be positive.

        :stability: experimental
        '''
        result = self._values.get("change")
        assert result is not None, "Required property 'change' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def lower(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The lower bound of the interval.

        The scaling adjustment will be applied if the metric is higher than this value.

        :default: Threshold automatically derived from neighbouring intervals

        :stability: experimental
        '''
        result = self._values.get("lower")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def upper(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The upper bound of the interval.

        The scaling adjustment will be applied if the metric is lower than this value.

        :default: Threshold automatically derived from neighbouring intervals

        :stability: experimental
        '''
        result = self._values.get("upper")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScalingInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Alarms",
    "ArbitraryIntervals",
    "CompleteScalingInterval",
    "IRandomGenerator",
    "ScalingInterval",
]

publication.publish()

def _typecheckingstub__effd62bed4f1d403fe62740ebfaa5e71aca023a8db05d622d40488d2b6ec5636(
    *,
    lower_alarm_interval_index: typing.Optional[jsii.Number] = None,
    upper_alarm_interval_index: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9496ac1870eaa02210290e23658484940f8aed51ba6d9cbaadc3b2ebaab35fe4(
    *,
    absolute: builtins.bool,
    intervals: typing.Sequence[typing.Union[ScalingInterval, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb51740ae832ae7afb08e341768a116d792dd8782eb7ca3c6731852cd1437bed(
    *,
    lower: jsii.Number,
    upper: jsii.Number,
    change: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb4ea42dd4a6070fb443031246674bdeee6fdebe0e381eff9065b93a46801e2(
    min: jsii.Number,
    max: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19d74c45e1f3e2cfbe3ff6d9863f5d02724a24dfbb036cb67e709dc9a80165a(
    *,
    change: jsii.Number,
    lower: typing.Optional[jsii.Number] = None,
    upper: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
