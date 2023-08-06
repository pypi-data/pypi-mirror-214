'''
# AWS Region-Specific Information Directory

## Usage

Some information used in CDK Applications differs from one AWS region to
another, such as service principals used in IAM policies, S3 static website
endpoints, ...

### The `RegionInfo` class

The library offers a simple interface to obtain region specific information in
the form of the `RegionInfo` class. This is the preferred way to interact with
the regional information database:

```python
# Get the information for "eu-west-1":
region = region_info.RegionInfo.get("eu-west-1")

# Access attributes:
region.s3_static_website_endpoint # s3-website-eu-west-1.amazonaws.com
region.service_principal("logs.amazonaws.com")
```

The `RegionInfo` layer is built on top of the Low-Level API, which is described
below and can be used to register additional data, including user-defined facts
that are not available through the `RegionInfo` interface.

### Low-Level API

This library offers a primitive database of such information so that CDK
constructs can easily access regional information. The `FactName` class provides
a list of known fact names, which can then be used with the `RegionInfo` to
retrieve a particular value:

```python
code_deploy_principal = region_info.Fact.find("us-east-1", region_info.FactName.service_principal("codedeploy.amazonaws.com"))
# => codedeploy.us-east-1.amazonaws.com

static_website = region_info.Fact.find("ap-northeast-1", region_info.FactName.S3_STATIC_WEBSITE_ENDPOINT)
```

## Supplying new or missing information

As new regions are released, it might happen that a particular fact you need is
missing from the library. In such cases, the `Fact.register` method can be used
to inject FactName into the database:

```python
class MyFact(region_info.IFact):

region_info.Fact.register(MyFact())
```

## Overriding incorrect information

In the event information provided by the library is incorrect, it can be
overridden using the same `Fact.register` method demonstrated above, simply
adding an extra boolean argument:

```python
class MyFact(region_info.IFact):

region_info.Fact.register(MyFact(), True)
```

If you happen to have stumbled upon incorrect data built into this library, it
is always a good idea to report your findings in a [GitHub issue](https://github.com/aws/aws-cdk/issues), so we can fix
it for everyone else!

---


This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
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


class Default(metaclass=jsii.JSIIMeta, jsii_type="monocdk.region_info.Default"):
    '''(experimental) Provides default values for certain regional information points.

    :stability: experimental
    '''

    @jsii.member(jsii_name="servicePrincipal")
    @builtins.classmethod
    def service_principal(
        cls,
        service_fqn: builtins.str,
        region: builtins.str,
        url_suffix: builtins.str,
    ) -> builtins.str:
        '''(experimental) Computes a "standard" AWS Service principal for a given service, region and suffix.

        This is useful for example when
        you need to compute a service principal name, but you do not have a synthesize-time region literal available (so
        all you have is ``{ "Ref": "AWS::Region" }``). This way you get the same defaulting behavior that is normally used
        for built-in data.

        :param service_fqn: the name of the service (s3, s3.amazonaws.com, ...).
        :param region: the region in which the service principal is needed.
        :param url_suffix: deprecated and ignored.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05004e17b1f785d1c8d508f9a12ba628b4093b33e9aa7386b6705e000a5c960a)
            check_type(argname="argument service_fqn", value=service_fqn, expected_type=type_hints["service_fqn"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument url_suffix", value=url_suffix, expected_type=type_hints["url_suffix"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "servicePrincipal", [service_fqn, region, url_suffix]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ENDPOINT_SERVICE_NAME_PREFIX")
    def VPC_ENDPOINT_SERVICE_NAME_PREFIX(cls) -> builtins.str:
        '''(experimental) The default value for a VPC Endpoint Service name prefix, useful if you do not have a synthesize-time region literal available (all you have is ``{ "Ref": "AWS::Region" }``).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "VPC_ENDPOINT_SERVICE_NAME_PREFIX"))


class Fact(metaclass=jsii.JSIIMeta, jsii_type="monocdk.region_info.Fact"):
    '''(experimental) A database of regional information.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        class MyFact(region_info.IFact):
        
        region_info.Fact.register(MyFact())
    '''

    @jsii.member(jsii_name="find")
    @builtins.classmethod
    def find(
        cls,
        region: builtins.str,
        name: builtins.str,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Retrieves a fact from this Fact database.

        :param region: the name of the region (e.g: ``us-east-1``).
        :param name: the name of the fact being looked up (see the ``FactName`` class for details).

        :return: the fact value if it is known, and ``undefined`` otherwise.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e34cbd95c7512205f09fca79e9476f2fd79534aa34ea0cfc5710efeae1eaae)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "find", [region, name]))

    @jsii.member(jsii_name="register")
    @builtins.classmethod
    def register(
        cls,
        fact: "IFact",
        allow_replacing: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Registers a new fact in this Fact database.

        :param fact: the new fact to be registered.
        :param allow_replacing: whether new facts can replace existing facts or not.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0da052ed5ca34eb55fe7bd2185ce19880cfc4a4cbaa5a6014efb4cc1a478bc0)
            check_type(argname="argument fact", value=fact, expected_type=type_hints["fact"])
            check_type(argname="argument allow_replacing", value=allow_replacing, expected_type=type_hints["allow_replacing"])
        return typing.cast(None, jsii.sinvoke(cls, "register", [fact, allow_replacing]))

    @jsii.member(jsii_name="requireFact")
    @builtins.classmethod
    def require_fact(cls, region: builtins.str, name: builtins.str) -> builtins.str:
        '''(experimental) Retrieve a fact from the Fact database.

        (retrieval will fail if the specified region or
        fact name does not exist.)

        :param region: the name of the region (e.g: ``us-east-1``).
        :param name: the name of the fact being looked up (see the ``FactName`` class for details).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640e2c57af5b108929ac940bb29a85c04680b38a433967f2a97c1370f1909f94)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "requireFact", [region, name]))

    @jsii.member(jsii_name="unregister")
    @builtins.classmethod
    def unregister(
        cls,
        region: builtins.str,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Removes a fact from the database.

        :param region: the region for which the fact is to be removed.
        :param name: the name of the fact to remove.
        :param value: the value that should be removed (removal will fail if the value is specified, but does not match the current stored value).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9890e917375bd8eb21cb383eafca9d8762b33f0882f23be0b25ae46a279d8a7b)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.sinvoke(cls, "unregister", [region, name, value]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="regions")
    def regions(cls) -> typing.List[builtins.str]:
        '''
        :return:

        the list of names of AWS regions for which there is at least one registered fact. This
        may not be an exhaustive list of all available AWS regions.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "regions"))


class FactName(metaclass=jsii.JSIIMeta, jsii_type="monocdk.region_info.FactName"):
    '''(experimental) All standardized fact names.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        class MyFact(region_info.IFact):
        
        region_info.Fact.register(MyFact())
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="cloudwatchLambdaInsightsVersion")
    @builtins.classmethod
    def cloudwatch_lambda_insights_version(
        cls,
        version: builtins.str,
        arch: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) The ARN of CloudWatch Lambda Insights for a version (e.g. 1.0.98.0).

        :param version: -
        :param arch: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643cad4ea1dcc132ad3a401d97a37817e71a0fe4e5d45b5ead2b613750ac0a49)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument arch", value=arch, expected_type=type_hints["arch"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "cloudwatchLambdaInsightsVersion", [version, arch]))

    @jsii.member(jsii_name="servicePrincipal")
    @builtins.classmethod
    def service_principal(cls, service: builtins.str) -> builtins.str:
        '''(experimental) The name of the regional service principal for a given service.

        :param service: the service name, either simple (e.g: ``s3``, ``codedeploy``) or qualified (e.g: ``s3.amazonaws.com``). The ``.amazonaws.com`` and ``.amazonaws.com.cn`` domains are stripped from service names, so they are canonicalized in that respect.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96533f5313ef8448cd6754e61b361a4ab6d70821b72089c8a24dd5bc62b0b57f)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "servicePrincipal", [service]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPMESH_ECR_ACCOUNT")
    def APPMESH_ECR_ACCOUNT(cls) -> builtins.str:
        '''(experimental) The ID of the AWS account that owns the public ECR repository that contains the AWS App Mesh Envoy Proxy images in a given region.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "APPMESH_ECR_ACCOUNT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CDK_METADATA_RESOURCE_AVAILABLE")
    def CDK_METADATA_RESOURCE_AVAILABLE(cls) -> builtins.str:
        '''(experimental) Whether the AWS::CDK::Metadata CloudFormation Resource is available in-region or not.

        The value is a boolean
        modelled as ``YES`` or ``NO``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CDK_METADATA_RESOURCE_AVAILABLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DLC_REPOSITORY_ACCOUNT")
    def DLC_REPOSITORY_ACCOUNT(cls) -> builtins.str:
        '''(experimental) The ID of the AWS account that owns the public ECR repository that contains the AWS Deep Learning Containers images in a given region.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DLC_REPOSITORY_ACCOUNT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOMAIN_SUFFIX")
    def DOMAIN_SUFFIX(cls) -> builtins.str:
        '''(experimental) The domain suffix for a region (e.g: 'amazonaws.com`).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DOMAIN_SUFFIX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EBS_ENV_ENDPOINT_HOSTED_ZONE_ID")
    def EBS_ENV_ENDPOINT_HOSTED_ZONE_ID(cls) -> builtins.str:
        '''(experimental) The hosted zone ID used by Route 53 to alias a EBS environment endpoint in this region (e.g: Z2O1EMRO9K5GLX).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "EBS_ENV_ENDPOINT_HOSTED_ZONE_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELBV2_ACCOUNT")
    def ELBV2_ACCOUNT(cls) -> builtins.str:
        '''(experimental) The account for ELBv2 in this region.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ELBV2_ACCOUNT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FIREHOSE_CIDR_BLOCK")
    def FIREHOSE_CIDR_BLOCK(cls) -> builtins.str:
        '''(experimental) The CIDR block used by Kinesis Data Firehose servers.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "FIREHOSE_CIDR_BLOCK"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARTITION")
    def PARTITION(cls) -> builtins.str:
        '''(experimental) The name of the partition for a region (e.g: 'aws', 'aws-cn', ...).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PARTITION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="S3_STATIC_WEBSITE_ENDPOINT")
    def S3_STATIC_WEBSITE_ENDPOINT(cls) -> builtins.str:
        '''(experimental) The endpoint used for hosting S3 static websites.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "S3_STATIC_WEBSITE_ENDPOINT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="S3_STATIC_WEBSITE_ZONE_53_HOSTED_ZONE_ID")
    def S3_STATIC_WEBSITE_ZONE_53_HOSTED_ZONE_ID(cls) -> builtins.str:
        '''(experimental) The endpoint used for aliasing S3 static websites in Route 53.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "S3_STATIC_WEBSITE_ZONE_53_HOSTED_ZONE_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ENDPOINT_SERVICE_NAME_PREFIX")
    def VPC_ENDPOINT_SERVICE_NAME_PREFIX(cls) -> builtins.str:
        '''(experimental) The prefix for VPC Endpoint Service names, cn.com.amazonaws.vpce for China regions, com.amazonaws.vpce otherwise.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "VPC_ENDPOINT_SERVICE_NAME_PREFIX"))


@jsii.interface(jsii_type="monocdk.region_info.IFact")
class IFact(typing_extensions.Protocol):
    '''(experimental) A fact that can be registered about a particular region.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this fact.

        Standardized values are provided by the ``Facts`` class.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        '''(experimental) The region for which this fact applies.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Optional[builtins.str]:
        '''(experimental) The value of this fact.

        :stability: experimental
        '''
        ...


class _IFactProxy:
    '''(experimental) A fact that can be registered about a particular region.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.region_info.IFact"

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this fact.

        Standardized values are provided by the ``Facts`` class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        '''(experimental) The region for which this fact applies.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Optional[builtins.str]:
        '''(experimental) The value of this fact.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "value"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFact).__jsii_proxy_class__ = lambda : _IFactProxy


class RegionInfo(metaclass=jsii.JSIIMeta, jsii_type="monocdk.region_info.RegionInfo"):
    '''(experimental) Information pertaining to an AWS region.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Get the information for "eu-west-1":
        region = region_info.RegionInfo.get("eu-west-1")
        
        # Access attributes:
        region.s3_static_website_endpoint # s3-website-eu-west-1.amazonaws.com
        region.service_principal("logs.amazonaws.com")
    '''

    @jsii.member(jsii_name="get")
    @builtins.classmethod
    def get(cls, name: builtins.str) -> "RegionInfo":
        '''(experimental) Obtain region info for a given region name.

        :param name: the name of the region (e.g: us-east-1).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc91282de8b4f6701b5eef059d4bb1fb319b25ae9e7a4936fca1c50bb93bf66)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("RegionInfo", jsii.sinvoke(cls, "get", [name]))

    @jsii.member(jsii_name="limitedRegionMap")
    @builtins.classmethod
    def limited_region_map(
        cls,
        fact_name: builtins.str,
        partitions: typing.Sequence[builtins.str],
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Retrieves a collection of all fact values for all regions, limited to some partitions.

        :param fact_name: the name of the fact to retrieve values for. For a list of common fact names, see the FactName class
        :param partitions: list of partitions to retrieve facts for. Defaults to ``['aws', 'aws-cn']``.

        :return:

        a mapping with AWS region codes as the keys,
        and the fact in the given region as the value for that key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f88879d9fdd720a531669194191d4fb28d0f0823833f5423e3efbf7560d32dd)
            check_type(argname="argument fact_name", value=fact_name, expected_type=type_hints["fact_name"])
            check_type(argname="argument partitions", value=partitions, expected_type=type_hints["partitions"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.sinvoke(cls, "limitedRegionMap", [fact_name, partitions]))

    @jsii.member(jsii_name="regionMap")
    @builtins.classmethod
    def region_map(
        cls,
        fact_name: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Retrieves a collection of all fact values for all regions that fact is defined in.

        :param fact_name: the name of the fact to retrieve values for. For a list of common fact names, see the FactName class

        :return:

        a mapping with AWS region codes as the keys,
        and the fact in the given region as the value for that key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6b4da698a4751bbc1138405d9be2690def3c71b704e9cbaafee874bb42c6fb)
            check_type(argname="argument fact_name", value=fact_name, expected_type=type_hints["fact_name"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.sinvoke(cls, "regionMap", [fact_name]))

    @jsii.member(jsii_name="cloudwatchLambdaInsightsArn")
    def cloudwatch_lambda_insights_arn(
        self,
        insights_version: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the CloudWatch Lambda Insights extension, for the given version.

        :param insights_version: the version (e.g. 1.0.98.0).
        :param architecture: the Lambda Function architecture (e.g. 'x86_64' or 'arm64').

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6193c6b65f1eb6a8c1db08bb7605b8fdd73c99c41f36c859c14706ea7e75e1a)
            check_type(argname="argument insights_version", value=insights_version, expected_type=type_hints["insights_version"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "cloudwatchLambdaInsightsArn", [insights_version, architecture]))

    @jsii.member(jsii_name="servicePrincipal")
    def service_principal(self, service: builtins.str) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the service principal for a given service in this region.

        :param service: the service name (e.g: s3.amazonaws.com).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a6577091227f63eefd4dbcd7c49bfa9cc09b45f339d3d0e69ebaf4c52d57ca)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "servicePrincipal", [service]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="regions")
    def regions(cls) -> typing.List["RegionInfo"]:
        '''
        :return:

        the list of names of AWS regions for which there is at least one registered fact. This
        may not be an exaustive list of all available AWS regions.

        :stability: experimental
        '''
        return typing.cast(typing.List["RegionInfo"], jsii.sget(cls, "regions"))

    @builtins.property
    @jsii.member(jsii_name="cdkMetadataResourceAvailable")
    def cdk_metadata_resource_available(self) -> builtins.bool:
        '''(experimental) Whether the ``AWS::CDK::Metadata`` CloudFormation Resource is available in this region or not.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "cdkMetadataResourceAvailable"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="appMeshRepositoryAccount")
    def app_mesh_repository_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the AWS account that owns the public ECR repository that contains the AWS App Mesh Envoy Proxy images in a given region.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appMeshRepositoryAccount"))

    @builtins.property
    @jsii.member(jsii_name="dlcRepositoryAccount")
    def dlc_repository_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the AWS account that owns the public ECR repository containing the AWS Deep Learning Containers images in this region.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dlcRepositoryAccount"))

    @builtins.property
    @jsii.member(jsii_name="domainSuffix")
    def domain_suffix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The domain name suffix (e.g: amazonaws.com) for this region.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainSuffix"))

    @builtins.property
    @jsii.member(jsii_name="ebsEnvEndpointHostedZoneId")
    def ebs_env_endpoint_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hosted zone ID used by Route 53 to alias a EBS environment endpoint in this region (e.g: Z2O1EMRO9K5GLX).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ebsEnvEndpointHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="elbv2Account")
    def elbv2_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The account ID for ELBv2 in this region.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elbv2Account"))

    @builtins.property
    @jsii.member(jsii_name="firehoseCidrBlock")
    def firehose_cidr_block(self) -> typing.Optional[builtins.str]:
        '''(experimental) The CIDR block used by Kinesis Data Firehose servers.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firehoseCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the ARN partition for this region (e.g: aws).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partition"))

    @builtins.property
    @jsii.member(jsii_name="s3StaticWebsiteEndpoint")
    def s3_static_website_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) The endpoint used by S3 static website hosting in this region (e.g: s3-static-website-us-east-1.amazonaws.com).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3StaticWebsiteEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="s3StaticWebsiteHostedZoneId")
    def s3_static_website_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hosted zone ID used by Route 53 to alias a S3 static website in this region (e.g: Z2O1EMRO9K5GLX).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3StaticWebsiteHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointServiceNamePrefix")
    def vpc_endpoint_service_name_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The prefix for VPC Endpoint Service names, cn.com.amazonaws.vpce for China regions, com.amazonaws.vpce otherwise.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcEndpointServiceNamePrefix"))


__all__ = [
    "Default",
    "Fact",
    "FactName",
    "IFact",
    "RegionInfo",
]

publication.publish()

def _typecheckingstub__05004e17b1f785d1c8d508f9a12ba628b4093b33e9aa7386b6705e000a5c960a(
    service_fqn: builtins.str,
    region: builtins.str,
    url_suffix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e34cbd95c7512205f09fca79e9476f2fd79534aa34ea0cfc5710efeae1eaae(
    region: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0da052ed5ca34eb55fe7bd2185ce19880cfc4a4cbaa5a6014efb4cc1a478bc0(
    fact: IFact,
    allow_replacing: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640e2c57af5b108929ac940bb29a85c04680b38a433967f2a97c1370f1909f94(
    region: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9890e917375bd8eb21cb383eafca9d8762b33f0882f23be0b25ae46a279d8a7b(
    region: builtins.str,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643cad4ea1dcc132ad3a401d97a37817e71a0fe4e5d45b5ead2b613750ac0a49(
    version: builtins.str,
    arch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96533f5313ef8448cd6754e61b361a4ab6d70821b72089c8a24dd5bc62b0b57f(
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc91282de8b4f6701b5eef059d4bb1fb319b25ae9e7a4936fca1c50bb93bf66(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f88879d9fdd720a531669194191d4fb28d0f0823833f5423e3efbf7560d32dd(
    fact_name: builtins.str,
    partitions: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6b4da698a4751bbc1138405d9be2690def3c71b704e9cbaafee874bb42c6fb(
    fact_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6193c6b65f1eb6a8c1db08bb7605b8fdd73c99c41f36c859c14706ea7e75e1a(
    insights_version: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a6577091227f63eefd4dbcd7c49bfa9cc09b45f339d3d0e69ebaf4c52d57ca(
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
