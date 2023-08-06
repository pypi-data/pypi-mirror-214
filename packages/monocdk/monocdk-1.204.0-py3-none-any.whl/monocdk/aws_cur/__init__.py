'''
# AWS::CUR Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as cur
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for CUR construct libraries](https://constructs.dev/search?q=cur)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::CUR resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CUR.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::CUR](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CUR.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnReportDefinition(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cur.CfnReportDefinition",
):
    '''A CloudFormation ``AWS::CUR::ReportDefinition``.

    The definition of AWS Cost and Usage Report. You can specify the report name, time unit, report format, compression format, S3 bucket, additional artifacts, and schema elements in the definition.

    :cloudformationResource: AWS::CUR::ReportDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cur as cur
        
        cfn_report_definition = cur.CfnReportDefinition(self, "MyCfnReportDefinition",
            compression="compression",
            format="format",
            refresh_closed_reports=False,
            report_name="reportName",
            report_versioning="reportVersioning",
            s3_bucket="s3Bucket",
            s3_prefix="s3Prefix",
            s3_region="s3Region",
            time_unit="timeUnit",
        
            # the properties below are optional
            additional_artifacts=["additionalArtifacts"],
            additional_schema_elements=["additionalSchemaElements"],
            billing_view_arn="billingViewArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        compression: builtins.str,
        format: builtins.str,
        refresh_closed_reports: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        report_name: builtins.str,
        report_versioning: builtins.str,
        s3_bucket: builtins.str,
        s3_prefix: builtins.str,
        s3_region: builtins.str,
        time_unit: builtins.str,
        additional_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_schema_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        billing_view_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CUR::ReportDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compression: The compression format that Amazon Web Services uses for the report.
        :param format: The format that Amazon Web Services saves the report in.
        :param refresh_closed_reports: Whether you want AWS to update your reports after they have been finalized if AWS detects charges related to previous months. These charges can include refunds, credits, or support fees.
        :param report_name: The name of the report that you want to create. The name must be unique, is case sensitive, and can't include spaces.
        :param report_versioning: Whether you want AWS to overwrite the previous version of each report or to deliver the report in addition to the previous versions.
        :param s3_bucket: The S3 bucket where Amazon Web Services delivers the report.
        :param s3_prefix: The prefix that Amazon Web Services adds to the report name when Amazon Web Services delivers the report. Your prefix can't include spaces.
        :param s3_region: The Region of the S3 bucket that Amazon Web Services delivers the report into.
        :param time_unit: The granularity of the line items in the report.
        :param additional_artifacts: A list of manifests that you want AWS to create for this report.
        :param additional_schema_elements: A list of strings that indicate additional content that AWS includes in the report, such as individual resource IDs.
        :param billing_view_arn: The Amazon Resource Name (ARN) of the billing view. You can get this value by using the billing view service public APIs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53cd46aaa23af10772e4fb95fcbf394bc52072a0184ce854374924a3ff7eeab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReportDefinitionProps(
            compression=compression,
            format=format,
            refresh_closed_reports=refresh_closed_reports,
            report_name=report_name,
            report_versioning=report_versioning,
            s3_bucket=s3_bucket,
            s3_prefix=s3_prefix,
            s3_region=s3_region,
            time_unit=time_unit,
            additional_artifacts=additional_artifacts,
            additional_schema_elements=additional_schema_elements,
            billing_view_arn=billing_view_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051c94b6eb3f1df4cdaae3be346d335f0b39324573cf4bc8c85a1cc367d7d5e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a4cd2b0ffd1f8691217084cc2dcd4a20bb8c5370242e35d727c0953d92781f0)
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
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        '''The compression format that Amazon Web Services uses for the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-compression
        '''
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5858d0bdc762543e002b3e993763324823e0a13b56d4d1f42b6563076d80bccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value)

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        '''The format that Amazon Web Services saves the report in.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-format
        '''
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5bb5d868ab3d3c124f179423a5d4de809fac27208f0916cc56f0435da0857be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value)

    @builtins.property
    @jsii.member(jsii_name="refreshClosedReports")
    def refresh_closed_reports(
        self,
    ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        '''Whether you want AWS to update your reports after they have been finalized if AWS detects charges related to previous months.

        These charges can include refunds, credits, or support fees.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-refreshclosedreports
        '''
        return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], jsii.get(self, "refreshClosedReports"))

    @refresh_closed_reports.setter
    def refresh_closed_reports(
        self,
        value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9ec9545522f213668a1703e7fbdd090ca6737c2730d788ff04384c7ecb3b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshClosedReports", value)

    @builtins.property
    @jsii.member(jsii_name="reportName")
    def report_name(self) -> builtins.str:
        '''The name of the report that you want to create.

        The name must be unique, is case sensitive, and can't include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-reportname
        '''
        return typing.cast(builtins.str, jsii.get(self, "reportName"))

    @report_name.setter
    def report_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f699c248784a508fcf284c65f6efd0f4c49bec707fe3d09345e6c6e867535360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportName", value)

    @builtins.property
    @jsii.member(jsii_name="reportVersioning")
    def report_versioning(self) -> builtins.str:
        '''Whether you want AWS to overwrite the previous version of each report or to deliver the report in addition to the previous versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-reportversioning
        '''
        return typing.cast(builtins.str, jsii.get(self, "reportVersioning"))

    @report_versioning.setter
    def report_versioning(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a29b0a36c0b80cf0871fb5338d7a82f2aa9111d8ef731bf185840eb5a516c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportVersioning", value)

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        '''The S3 bucket where Amazon Web Services delivers the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3bucket
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf15b340747b13416d0215127453960061ec0cba8f6e5c66e725f3e9d6bace38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value)

    @builtins.property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> builtins.str:
        '''The prefix that Amazon Web Services adds to the report name when Amazon Web Services delivers the report.

        Your prefix can't include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3prefix
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Prefix"))

    @s3_prefix.setter
    def s3_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31b66b3ac1dd489b20082d385ebcba554a3660114385f16b870c90f3f71949a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Prefix", value)

    @builtins.property
    @jsii.member(jsii_name="s3Region")
    def s3_region(self) -> builtins.str:
        '''The Region of the S3 bucket that Amazon Web Services delivers the report into.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3region
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Region"))

    @s3_region.setter
    def s3_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09e6b2450a20cb657091a3527be4e665ce5db158c3c39a896c6958bc25faee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Region", value)

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        '''The granularity of the line items in the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-timeunit
        '''
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80216e43264b99afc688981b9d824e1869da8c3526228e854cb28bba55e98309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value)

    @builtins.property
    @jsii.member(jsii_name="additionalArtifacts")
    def additional_artifacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of manifests that you want AWS to create for this report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-additionalartifacts
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalArtifacts"))

    @additional_artifacts.setter
    def additional_artifacts(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cf793b44c5fa7c7e44333f587aa80338c7a1ef20001052f13632621f53b456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalArtifacts", value)

    @builtins.property
    @jsii.member(jsii_name="additionalSchemaElements")
    def additional_schema_elements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of strings that indicate additional content that AWS includes in the report, such as individual resource IDs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-additionalschemaelements
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalSchemaElements"))

    @additional_schema_elements.setter
    def additional_schema_elements(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9bab98e6d0a17bb1e4a89b51a7d09a7f313c1256bae891b2d9255b27a28d38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalSchemaElements", value)

    @builtins.property
    @jsii.member(jsii_name="billingViewArn")
    def billing_view_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the billing view.

        You can get this value by using the billing view service public APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-billingviewarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingViewArn"))

    @billing_view_arn.setter
    def billing_view_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7caf70d77c34c1de916b7168637078422973d0460e48216f288934fecb0f903b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingViewArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_cur.CfnReportDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "compression": "compression",
        "format": "format",
        "refresh_closed_reports": "refreshClosedReports",
        "report_name": "reportName",
        "report_versioning": "reportVersioning",
        "s3_bucket": "s3Bucket",
        "s3_prefix": "s3Prefix",
        "s3_region": "s3Region",
        "time_unit": "timeUnit",
        "additional_artifacts": "additionalArtifacts",
        "additional_schema_elements": "additionalSchemaElements",
        "billing_view_arn": "billingViewArn",
    },
)
class CfnReportDefinitionProps:
    def __init__(
        self,
        *,
        compression: builtins.str,
        format: builtins.str,
        refresh_closed_reports: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        report_name: builtins.str,
        report_versioning: builtins.str,
        s3_bucket: builtins.str,
        s3_prefix: builtins.str,
        s3_region: builtins.str,
        time_unit: builtins.str,
        additional_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_schema_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        billing_view_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnReportDefinition``.

        :param compression: The compression format that Amazon Web Services uses for the report.
        :param format: The format that Amazon Web Services saves the report in.
        :param refresh_closed_reports: Whether you want AWS to update your reports after they have been finalized if AWS detects charges related to previous months. These charges can include refunds, credits, or support fees.
        :param report_name: The name of the report that you want to create. The name must be unique, is case sensitive, and can't include spaces.
        :param report_versioning: Whether you want AWS to overwrite the previous version of each report or to deliver the report in addition to the previous versions.
        :param s3_bucket: The S3 bucket where Amazon Web Services delivers the report.
        :param s3_prefix: The prefix that Amazon Web Services adds to the report name when Amazon Web Services delivers the report. Your prefix can't include spaces.
        :param s3_region: The Region of the S3 bucket that Amazon Web Services delivers the report into.
        :param time_unit: The granularity of the line items in the report.
        :param additional_artifacts: A list of manifests that you want AWS to create for this report.
        :param additional_schema_elements: A list of strings that indicate additional content that AWS includes in the report, such as individual resource IDs.
        :param billing_view_arn: The Amazon Resource Name (ARN) of the billing view. You can get this value by using the billing view service public APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cur as cur
            
            cfn_report_definition_props = cur.CfnReportDefinitionProps(
                compression="compression",
                format="format",
                refresh_closed_reports=False,
                report_name="reportName",
                report_versioning="reportVersioning",
                s3_bucket="s3Bucket",
                s3_prefix="s3Prefix",
                s3_region="s3Region",
                time_unit="timeUnit",
            
                # the properties below are optional
                additional_artifacts=["additionalArtifacts"],
                additional_schema_elements=["additionalSchemaElements"],
                billing_view_arn="billingViewArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e043b2d8a4c9e304e1648c0a877742c10be8c20cac91ae1e5fb831bd5940742)
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument refresh_closed_reports", value=refresh_closed_reports, expected_type=type_hints["refresh_closed_reports"])
            check_type(argname="argument report_name", value=report_name, expected_type=type_hints["report_name"])
            check_type(argname="argument report_versioning", value=report_versioning, expected_type=type_hints["report_versioning"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
            check_type(argname="argument s3_region", value=s3_region, expected_type=type_hints["s3_region"])
            check_type(argname="argument time_unit", value=time_unit, expected_type=type_hints["time_unit"])
            check_type(argname="argument additional_artifacts", value=additional_artifacts, expected_type=type_hints["additional_artifacts"])
            check_type(argname="argument additional_schema_elements", value=additional_schema_elements, expected_type=type_hints["additional_schema_elements"])
            check_type(argname="argument billing_view_arn", value=billing_view_arn, expected_type=type_hints["billing_view_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compression": compression,
            "format": format,
            "refresh_closed_reports": refresh_closed_reports,
            "report_name": report_name,
            "report_versioning": report_versioning,
            "s3_bucket": s3_bucket,
            "s3_prefix": s3_prefix,
            "s3_region": s3_region,
            "time_unit": time_unit,
        }
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if additional_schema_elements is not None:
            self._values["additional_schema_elements"] = additional_schema_elements
        if billing_view_arn is not None:
            self._values["billing_view_arn"] = billing_view_arn

    @builtins.property
    def compression(self) -> builtins.str:
        '''The compression format that Amazon Web Services uses for the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-compression
        '''
        result = self._values.get("compression")
        assert result is not None, "Required property 'compression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> builtins.str:
        '''The format that Amazon Web Services saves the report in.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-format
        '''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def refresh_closed_reports(
        self,
    ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        '''Whether you want AWS to update your reports after they have been finalized if AWS detects charges related to previous months.

        These charges can include refunds, credits, or support fees.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-refreshclosedreports
        '''
        result = self._values.get("refresh_closed_reports")
        assert result is not None, "Required property 'refresh_closed_reports' is missing"
        return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

    @builtins.property
    def report_name(self) -> builtins.str:
        '''The name of the report that you want to create.

        The name must be unique, is case sensitive, and can't include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-reportname
        '''
        result = self._values.get("report_name")
        assert result is not None, "Required property 'report_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def report_versioning(self) -> builtins.str:
        '''Whether you want AWS to overwrite the previous version of each report or to deliver the report in addition to the previous versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-reportversioning
        '''
        result = self._values.get("report_versioning")
        assert result is not None, "Required property 'report_versioning' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> builtins.str:
        '''The S3 bucket where Amazon Web Services delivers the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3bucket
        '''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_prefix(self) -> builtins.str:
        '''The prefix that Amazon Web Services adds to the report name when Amazon Web Services delivers the report.

        Your prefix can't include spaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3prefix
        '''
        result = self._values.get("s3_prefix")
        assert result is not None, "Required property 's3_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_region(self) -> builtins.str:
        '''The Region of the S3 bucket that Amazon Web Services delivers the report into.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-s3region
        '''
        result = self._values.get("s3_region")
        assert result is not None, "Required property 's3_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_unit(self) -> builtins.str:
        '''The granularity of the line items in the report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-timeunit
        '''
        result = self._values.get("time_unit")
        assert result is not None, "Required property 'time_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of manifests that you want AWS to create for this report.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-additionalartifacts
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def additional_schema_elements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of strings that indicate additional content that AWS includes in the report, such as individual resource IDs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-additionalschemaelements
        '''
        result = self._values.get("additional_schema_elements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def billing_view_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the billing view.

        You can get this value by using the billing view service public APIs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cur-reportdefinition.html#cfn-cur-reportdefinition-billingviewarn
        '''
        result = self._values.get("billing_view_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReportDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnReportDefinition",
    "CfnReportDefinitionProps",
]

publication.publish()

def _typecheckingstub__c53cd46aaa23af10772e4fb95fcbf394bc52072a0184ce854374924a3ff7eeab(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    compression: builtins.str,
    format: builtins.str,
    refresh_closed_reports: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    report_name: builtins.str,
    report_versioning: builtins.str,
    s3_bucket: builtins.str,
    s3_prefix: builtins.str,
    s3_region: builtins.str,
    time_unit: builtins.str,
    additional_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_schema_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    billing_view_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051c94b6eb3f1df4cdaae3be346d335f0b39324573cf4bc8c85a1cc367d7d5e9(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4cd2b0ffd1f8691217084cc2dcd4a20bb8c5370242e35d727c0953d92781f0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5858d0bdc762543e002b3e993763324823e0a13b56d4d1f42b6563076d80bccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bb5d868ab3d3c124f179423a5d4de809fac27208f0916cc56f0435da0857be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9ec9545522f213668a1703e7fbdd090ca6737c2730d788ff04384c7ecb3b94(
    value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f699c248784a508fcf284c65f6efd0f4c49bec707fe3d09345e6c6e867535360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a29b0a36c0b80cf0871fb5338d7a82f2aa9111d8ef731bf185840eb5a516c18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf15b340747b13416d0215127453960061ec0cba8f6e5c66e725f3e9d6bace38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31b66b3ac1dd489b20082d385ebcba554a3660114385f16b870c90f3f71949a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09e6b2450a20cb657091a3527be4e665ce5db158c3c39a896c6958bc25faee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80216e43264b99afc688981b9d824e1869da8c3526228e854cb28bba55e98309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cf793b44c5fa7c7e44333f587aa80338c7a1ef20001052f13632621f53b456(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9bab98e6d0a17bb1e4a89b51a7d09a7f313c1256bae891b2d9255b27a28d38(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7caf70d77c34c1de916b7168637078422973d0460e48216f288934fecb0f903b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e043b2d8a4c9e304e1648c0a877742c10be8c20cac91ae1e5fb831bd5940742(
    *,
    compression: builtins.str,
    format: builtins.str,
    refresh_closed_reports: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    report_name: builtins.str,
    report_versioning: builtins.str,
    s3_bucket: builtins.str,
    s3_prefix: builtins.str,
    s3_region: builtins.str,
    time_unit: builtins.str,
    additional_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_schema_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    billing_view_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
