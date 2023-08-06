'''
# Amazon OpenSearch Service Construct Library

See [Migrating to OpenSearch](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-elasticsearch-readme.html#migrating-to-opensearch) for migration instructions from `@aws-cdk/aws-elasticsearch` to this module, `@aws-cdk/aws-opensearchservice`.

## Quick start

Create a development cluster by simply specifying the version:

```python
dev_domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0
)
```

To perform version upgrades without replacing the entire domain, specify the `enableVersionUpgrade` property.

```python
dev_domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    enable_version_upgrade=True
)
```

Create a production grade cluster by also specifying things like capacity and az distribution

```python
prod_domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    capacity=opensearch.aws_opensearchservice.CapacityConfig(
        master_nodes=5,
        data_nodes=20
    ),
    ebs=opensearch.aws_opensearchservice.EbsOptions(
        volume_size=20
    ),
    zone_awareness=opensearch.aws_opensearchservice.ZoneAwarenessConfig(
        availability_zone_count=3
    ),
    logging=opensearch.aws_opensearchservice.LoggingOptions(
        slow_search_log_enabled=True,
        app_log_enabled=True,
        slow_index_log_enabled=True
    )
)
```

This creates an Amazon OpenSearch Service cluster and automatically sets up log groups for
logging the domain logs and slow search logs.

## A note about SLR

Some cluster configurations (e.g VPC access) require the existence of the [`AWSServiceRoleForAmazonElasticsearchService`](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/slr.html) Service-Linked Role.

When performing such operations via the AWS Console, this SLR is created automatically when needed. However, this is not the behavior when using CloudFormation. If an SLR is needed, but doesn't exist, you will encounter a failure message simlar to:

```console
Before you can proceed, you must enable a service-linked role to give Amazon OpenSearch Service...
```

To resolve this, you need to [create](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html#create-service-linked-role) the SLR. We recommend using the AWS CLI:

```console
aws iam create-service-linked-role --aws-service-name es.amazonaws.com
```

You can also create it using the CDK, **but note that only the first application deploying this will succeed**:

```python
slr = iam.CfnServiceLinkedRole(self, "Service Linked Role",
    aws_service_name="es.amazonaws.com"
)
```

## Importing existing domains

To import an existing domain into your CDK application, use the `Domain.fromDomainEndpoint` factory method.
This method accepts a domain endpoint of an already existing domain:

```python
domain_endpoint = "https://my-domain-jcjotrt6f7otem4sqcwbch3c4u.us-east-1.es.amazonaws.com"
domain = opensearch.Domain.from_domain_endpoint(self, "ImportedDomain", domain_endpoint)
```

## Permissions

### IAM

Helper methods also exist for managing access to the domain.

```python
# fn: lambda.Function
# domain: opensearch.Domain


# Grant write access to the app-search index
domain.grant_index_write("app-search", fn)

# Grant read access to the 'app-search/_search' path
domain.grant_path_read("app-search/_search", fn)
```

## Encryption

The domain can also be created with encryption enabled:

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    ebs=opensearch.aws_opensearchservice.EbsOptions(
        volume_size=100,
        volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
    ),
    node_to_node_encryption=True,
    encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(
        enabled=True
    )
)
```

This sets up the domain with node to node encryption and encryption at
rest. You can also choose to supply your own KMS key to use for encryption at
rest.

## VPC Support

Domains can be placed inside a VPC, providing a secure communication between Amazon OpenSearch Service and other services within the VPC without the need for an internet gateway, NAT device, or VPN connection.

> Visit [VPC Support for Amazon OpenSearch Service Domains](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html) for more details.

```python
vpc = ec2.Vpc(self, "Vpc")
domain_props = opensearch.aws_opensearchservice.DomainProps(
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    removal_policy=RemovalPolicy.DESTROY,
    vpc=vpc,
    # must be enabled since our VPC contains multiple private subnets.
    zone_awareness=opensearch.aws_opensearchservice.ZoneAwarenessConfig(
        enabled=True
    ),
    capacity=opensearch.aws_opensearchservice.CapacityConfig(
        # must be an even number since the default az count is 2.
        data_nodes=2
    )
)
opensearch.Domain(self, "Domain", domain_props)
```

In addition, you can use the `vpcSubnets` property to control which specific subnets will be used, and the `securityGroups` property to control
which security groups will be attached to the domain. By default, CDK will select all *private* subnets in the VPC, and create one dedicated security group.

## Metrics

Helper methods exist to access common domain metrics for example:

```python
# domain: opensearch.Domain

free_storage_space = domain.metric_free_storage_space()
master_sys_memory_utilization = domain.metric("MasterSysMemoryUtilization")
```

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Fine grained access control

The domain can also be created with a master user configured. The password can
be supplied or dynamically created if not supplied.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    enforce_https=True,
    node_to_node_encryption=True,
    encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(
        enabled=True
    ),
    fine_grained_access_control=opensearch.aws_opensearchservice.AdvancedSecurityOptions(
        master_user_name="master-user"
    )
)

master_user_password = domain.master_user_password
```

## Using unsigned basic auth

For convenience, the domain can be configured to allow unsigned HTTP requests
that use basic auth. Unless the domain is configured to be part of a VPC this
means anyone can access the domain using the configured master username and
password.

To enable unsigned basic auth access the domain is configured with an access
policy that allows anyonmous requests, HTTPS required, node to node encryption,
encryption at rest and fine grained access control.

If the above settings are not set they will be configured as part of enabling
unsigned basic auth. If they are set with conflicting values, an error will be
thrown.

If no master user is configured a default master user is created with the
username `admin`.

If no password is configured a default master user password is created and
stored in the AWS Secrets Manager as secret. The secret has the prefix
`<domain id>MasterUser`.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    use_unsigned_basic_auth=True
)

master_user_password = domain.master_user_password
```

## Custom access policies

If the domain requires custom access control it can be configured either as a
constructor property, or later by means of a helper method.

For simple permissions the `accessPolicies` constructor may be sufficient:

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    access_policies=[
        iam.PolicyStatement(
            actions=["es:*ESHttpPost", "es:ESHttpPut*"],
            effect=iam.Effect.ALLOW,
            principals=[iam.AccountPrincipal("123456789012")],
            resources=["*"]
        )
    ]
)
```

For more complex use-cases, for example, to set the domain up to receive data from a
[cross-account Kinesis Firehose](https://aws.amazon.com/premiumsupport/knowledge-center/kinesis-firehose-cross-account-streaming/) the `addAccessPolicies` helper method
allows for policies that include the explicit domain ARN.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0
)
domain.add_access_policies(
    iam.PolicyStatement(
        actions=["es:ESHttpPost", "es:ESHttpPut"],
        effect=iam.Effect.ALLOW,
        principals=[iam.AccountPrincipal("123456789012")],
        resources=[domain.domain_arn, f"{domain.domainArn}/*"]
    ),
    iam.PolicyStatement(
        actions=["es:ESHttpGet"],
        effect=iam.Effect.ALLOW,
        principals=[iam.AccountPrincipal("123456789012")],
        resources=[f"{domain.domainArn}/_all/_settings", f"{domain.domainArn}/_cluster/stats", f"{domain.domainArn}/index-name*/_mapping/type-name", f"{domain.domainArn}/roletest*/_mapping/roletest", f"{domain.domainArn}/_nodes", f"{domain.domainArn}/_nodes/stats", f"{domain.domainArn}/_nodes/*/stats", f"{domain.domainArn}/_stats", f"{domain.domainArn}/index-name*/_stats", f"{domain.domainArn}/roletest*/_stat"
        ]
    ))
```

## Audit logs

Audit logs can be enabled for a domain, but only when fine grained access control is enabled.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    enforce_https=True,
    node_to_node_encryption=True,
    encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(
        enabled=True
    ),
    fine_grained_access_control=opensearch.aws_opensearchservice.AdvancedSecurityOptions(
        master_user_name="master-user"
    ),
    logging=opensearch.aws_opensearchservice.LoggingOptions(
        audit_log_enabled=True,
        slow_search_log_enabled=True,
        app_log_enabled=True,
        slow_index_log_enabled=True
    )
)
```

## UltraWarm

UltraWarm nodes can be enabled to provide a cost-effective way to store large amounts of read-only data.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    capacity=opensearch.aws_opensearchservice.CapacityConfig(
        master_nodes=2,
        warm_nodes=2,
        warm_instance_type="ultrawarm1.medium.search"
    )
)
```

## Custom endpoint

Custom endpoints can be configured to reach the domain under a custom domain name.

```python
opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    custom_endpoint=opensearch.aws_opensearchservice.CustomEndpointOptions(
        domain_name="search.example.com"
    )
)
```

It is also possible to specify a custom certificate instead of the auto-generated one.

Additionally, an automatic CNAME-Record is created if a hosted zone is provided for the custom endpoint

## Advanced options

[Advanced options](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html#createdomain-configure-advanced-options) can used to configure additional options.

```python
opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    advanced_options={
        "rest.action.multi.allow_explicit_index": "false",
        "indices.fielddata.cache.size": "25",
        "indices.query.bool.max_clause_count": "2048"
    }
)
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
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_certificatemanager import ICertificate as _ICertificate_c7bbdc16
from ..aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_ec2 import (
    Connections as _Connections_57ccbda9,
    EbsDeviceVolumeType as _EbsDeviceVolumeType_3b8e2d6d,
    IConnectable as _IConnectable_c1c0e72c,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IRole as _IRole_59af6f50,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_logs import ILogGroup as _ILogGroup_846e17a0
from ..aws_route53 import IHostedZone as _IHostedZone_78d5a9c9


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.AdvancedSecurityOptions",
    jsii_struct_bases=[],
    name_mapping={
        "master_user_arn": "masterUserArn",
        "master_user_name": "masterUserName",
        "master_user_password": "masterUserPassword",
    },
)
class AdvancedSecurityOptions:
    def __init__(
        self,
        *,
        master_user_arn: typing.Optional[builtins.str] = None,
        master_user_name: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[_SecretValue_c18506ef] = None,
    ) -> None:
        '''(experimental) Specifies options for fine-grained access control.

        :param master_user_arn: (experimental) ARN for the master user. Only specify this or masterUserName, but not both. Default: - fine-grained access control is disabled
        :param master_user_name: (experimental) Username for the master user. Only specify this or masterUserArn, but not both. Default: - fine-grained access control is disabled
        :param master_user_password: (experimental) Password for the master user. You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - A Secrets Manager generated password

        :stability: experimental
        :exampleMetadata: infused

        Example::

            domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                enforce_https=True,
                node_to_node_encryption=True,
                encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(
                    enabled=True
                ),
                fine_grained_access_control=opensearch.aws_opensearchservice.AdvancedSecurityOptions(
                    master_user_name="master-user"
                ),
                logging=opensearch.aws_opensearchservice.LoggingOptions(
                    audit_log_enabled=True,
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15084f043c619e8789d2c006b8f5e5c8f6f4706f24540d9e2add0c4e96061770)
            check_type(argname="argument master_user_arn", value=master_user_arn, expected_type=type_hints["master_user_arn"])
            check_type(argname="argument master_user_name", value=master_user_name, expected_type=type_hints["master_user_name"])
            check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if master_user_arn is not None:
            self._values["master_user_arn"] = master_user_arn
        if master_user_name is not None:
            self._values["master_user_name"] = master_user_name
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password

    @builtins.property
    def master_user_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN for the master user.

        Only specify this or masterUserName, but not both.

        :default: - fine-grained access control is disabled

        :stability: experimental
        '''
        result = self._values.get("master_user_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Username for the master user.

        Only specify this or masterUserArn, but not both.

        :default: - fine-grained access control is disabled

        :stability: experimental
        '''
        result = self._values.get("master_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) Password for the master user.

        You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or
        use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in
        Secrets Manager.

        :default: - A Secrets Manager generated password

        :stability: experimental
        '''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedSecurityOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.CapacityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "data_node_instance_type": "dataNodeInstanceType",
        "data_nodes": "dataNodes",
        "master_node_instance_type": "masterNodeInstanceType",
        "master_nodes": "masterNodes",
        "warm_instance_type": "warmInstanceType",
        "warm_nodes": "warmNodes",
    },
)
class CapacityConfig:
    def __init__(
        self,
        *,
        data_node_instance_type: typing.Optional[builtins.str] = None,
        data_nodes: typing.Optional[jsii.Number] = None,
        master_node_instance_type: typing.Optional[builtins.str] = None,
        master_nodes: typing.Optional[jsii.Number] = None,
        warm_instance_type: typing.Optional[builtins.str] = None,
        warm_nodes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Configures the capacity of the cluster such as the instance type and the number of instances.

        :param data_node_instance_type: (experimental) The instance type for your data nodes, such as ``m3.medium.search``. For valid values, see `Supported Instance Types <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ in the Amazon OpenSearch Service Developer Guide. Default: - r5.large.search
        :param data_nodes: (experimental) The number of data nodes (instances) to use in the Amazon OpenSearch Service domain. Default: - 1
        :param master_node_instance_type: (experimental) The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search``. For valid values, see [Supported Instance Types] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html) in the Amazon OpenSearch Service Developer Guide. Default: - r5.large.search
        :param master_nodes: (experimental) The number of instances to use for the master node. Default: - no dedicated master nodes
        :param warm_instance_type: (experimental) The instance type for your UltraWarm node, such as ``ultrawarm1.medium.search``. For valid values, see [UltraWarm Storage Limits] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#limits-ultrawarm) in the Amazon OpenSearch Service Developer Guide. Default: - ultrawarm1.medium.search
        :param warm_nodes: (experimental) The number of UltraWarm nodes (instances) to use in the Amazon OpenSearch Service domain. Default: - no UltraWarm nodes

        :stability: experimental
        :exampleMetadata: infused

        Example::

            domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                capacity=opensearch.aws_opensearchservice.CapacityConfig(
                    master_nodes=2,
                    warm_nodes=2,
                    warm_instance_type="ultrawarm1.medium.search"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca448e25b7379aa009919b66eb2b96b59ed3186a2a2d641ec988f4dced6e4dbe)
            check_type(argname="argument data_node_instance_type", value=data_node_instance_type, expected_type=type_hints["data_node_instance_type"])
            check_type(argname="argument data_nodes", value=data_nodes, expected_type=type_hints["data_nodes"])
            check_type(argname="argument master_node_instance_type", value=master_node_instance_type, expected_type=type_hints["master_node_instance_type"])
            check_type(argname="argument master_nodes", value=master_nodes, expected_type=type_hints["master_nodes"])
            check_type(argname="argument warm_instance_type", value=warm_instance_type, expected_type=type_hints["warm_instance_type"])
            check_type(argname="argument warm_nodes", value=warm_nodes, expected_type=type_hints["warm_nodes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_node_instance_type is not None:
            self._values["data_node_instance_type"] = data_node_instance_type
        if data_nodes is not None:
            self._values["data_nodes"] = data_nodes
        if master_node_instance_type is not None:
            self._values["master_node_instance_type"] = master_node_instance_type
        if master_nodes is not None:
            self._values["master_nodes"] = master_nodes
        if warm_instance_type is not None:
            self._values["warm_instance_type"] = warm_instance_type
        if warm_nodes is not None:
            self._values["warm_nodes"] = warm_nodes

    @builtins.property
    def data_node_instance_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The instance type for your data nodes, such as ``m3.medium.search``. For valid values, see `Supported Instance Types <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ in the Amazon OpenSearch Service Developer Guide.

        :default: - r5.large.search

        :stability: experimental
        '''
        result = self._values.get("data_node_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_nodes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of data nodes (instances) to use in the Amazon OpenSearch Service domain.

        :default: - 1

        :stability: experimental
        '''
        result = self._values.get("data_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def master_node_instance_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search``. For valid values, see [Supported Instance Types] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html) in the Amazon OpenSearch Service Developer Guide.

        :default: - r5.large.search

        :stability: experimental
        '''
        result = self._values.get("master_node_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_nodes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of instances to use for the master node.

        :default: - no dedicated master nodes

        :stability: experimental
        '''
        result = self._values.get("master_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warm_instance_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The instance type for your UltraWarm node, such as ``ultrawarm1.medium.search``. For valid values, see [UltraWarm Storage Limits] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#limits-ultrawarm) in the Amazon OpenSearch Service Developer Guide.

        :default: - ultrawarm1.medium.search

        :stability: experimental
        '''
        result = self._values.get("warm_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warm_nodes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of UltraWarm nodes (instances) to use in the Amazon OpenSearch Service domain.

        :default: - no UltraWarm nodes

        :stability: experimental
        '''
        result = self._values.get("warm_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CapacityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDomain(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_opensearchservice.CfnDomain",
):
    '''A CloudFormation ``AWS::OpenSearchService::Domain``.

    The AWS::OpenSearchService::Domain resource creates an Amazon OpenSearch Service domain.

    :cloudformationResource: AWS::OpenSearchService::Domain
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_opensearchservice as opensearchservice
        
        # access_policies: Any
        
        cfn_domain = opensearchservice.CfnDomain(self, "MyCfnDomain",
            access_policies=access_policies,
            advanced_options={
                "advanced_options_key": "advancedOptions"
            },
            advanced_security_options=opensearchservice.CfnDomain.AdvancedSecurityOptionsInputProperty(
                anonymous_auth_disable_date="anonymousAuthDisableDate",
                anonymous_auth_enabled=False,
                enabled=False,
                internal_user_database_enabled=False,
                master_user_options=opensearchservice.CfnDomain.MasterUserOptionsProperty(
                    master_user_arn="masterUserArn",
                    master_user_name="masterUserName",
                    master_user_password="masterUserPassword"
                ),
                saml_options=opensearchservice.CfnDomain.SAMLOptionsProperty(
                    enabled=False,
                    idp=opensearchservice.CfnDomain.IdpProperty(
                        entity_id="entityId",
                        metadata_content="metadataContent"
                    ),
                    master_backend_role="masterBackendRole",
                    master_user_name="masterUserName",
                    roles_key="rolesKey",
                    session_timeout_minutes=123,
                    subject_key="subjectKey"
                )
            ),
            cluster_config=opensearchservice.CfnDomain.ClusterConfigProperty(
                dedicated_master_count=123,
                dedicated_master_enabled=False,
                dedicated_master_type="dedicatedMasterType",
                instance_count=123,
                instance_type="instanceType",
                multi_az_with_standby_enabled=False,
                warm_count=123,
                warm_enabled=False,
                warm_type="warmType",
                zone_awareness_config=opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                    availability_zone_count=123
                ),
                zone_awareness_enabled=False
            ),
            cognito_options=opensearchservice.CfnDomain.CognitoOptionsProperty(
                enabled=False,
                identity_pool_id="identityPoolId",
                role_arn="roleArn",
                user_pool_id="userPoolId"
            ),
            domain_endpoint_options=opensearchservice.CfnDomain.DomainEndpointOptionsProperty(
                custom_endpoint="customEndpoint",
                custom_endpoint_certificate_arn="customEndpointCertificateArn",
                custom_endpoint_enabled=False,
                enforce_https=False,
                tls_security_policy="tlsSecurityPolicy"
            ),
            domain_name="domainName",
            ebs_options=opensearchservice.CfnDomain.EBSOptionsProperty(
                ebs_enabled=False,
                iops=123,
                throughput=123,
                volume_size=123,
                volume_type="volumeType"
            ),
            encryption_at_rest_options=opensearchservice.CfnDomain.EncryptionAtRestOptionsProperty(
                enabled=False,
                kms_key_id="kmsKeyId"
            ),
            engine_version="engineVersion",
            log_publishing_options={
                "log_publishing_options_key": opensearchservice.CfnDomain.LogPublishingOptionProperty(
                    cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                    enabled=False
                )
            },
            node_to_node_encryption_options=opensearchservice.CfnDomain.NodeToNodeEncryptionOptionsProperty(
                enabled=False
            ),
            off_peak_window_options=opensearchservice.CfnDomain.OffPeakWindowOptionsProperty(
                enabled=False,
                off_peak_window=opensearchservice.CfnDomain.OffPeakWindowProperty(
                    window_start_time=opensearchservice.CfnDomain.WindowStartTimeProperty(
                        hours=123,
                        minutes=123
                    )
                )
            ),
            snapshot_options=opensearchservice.CfnDomain.SnapshotOptionsProperty(
                automated_snapshot_start_hour=123
            ),
            software_update_options=opensearchservice.CfnDomain.SoftwareUpdateOptionsProperty(
                auto_software_update_enabled=False
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_options=opensearchservice.CfnDomain.VPCOptionsProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        advanced_security_options: typing.Optional[typing.Union[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cluster_config: typing.Optional[typing.Union[typing.Union["CfnDomain.ClusterConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cognito_options: typing.Optional[typing.Union[typing.Union["CfnDomain.CognitoOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        domain_endpoint_options: typing.Optional[typing.Union[typing.Union["CfnDomain.DomainEndpointOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union[typing.Union["CfnDomain.EBSOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        encryption_at_rest_options: typing.Optional[typing.Union[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        log_publishing_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnDomain.LogPublishingOptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        off_peak_window_options: typing.Optional[typing.Union[typing.Union["CfnDomain.OffPeakWindowOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        snapshot_options: typing.Optional[typing.Union[typing.Union["CfnDomain.SnapshotOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        software_update_options: typing.Optional[typing.Union[typing.Union["CfnDomain.SoftwareUpdateOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_options: typing.Optional[typing.Union[typing.Union["CfnDomain.VPCOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::OpenSearchService::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_policies: An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions. For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param advanced_options: Additional options to specify for the OpenSearch Service domain. For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.
        :param advanced_security_options: Specifies options for fine-grained access control and SAML authentication. If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.
        :param cluster_config: Container for the cluster configuration of a domain.
        :param cognito_options: Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.
        :param domain_endpoint_options: Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.
        :param domain_name: A name for the OpenSearch Service domain. The name must have a minimum length of 3 and a maximum length of 28. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . Required when creating a new domain. .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param ebs_options: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param encryption_at_rest_options: Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use. See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .
        :param engine_version: The version of OpenSearch to use. The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* . If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param log_publishing_options: An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish. Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .
        :param node_to_node_encryption_options: Specifies whether node-to-node encryption is enabled. See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .
        :param off_peak_window_options: Options for a domain's off-peak window, during which OpenSearch Service can perform mandatory configuration changes on the domain.
        :param snapshot_options: *DEPRECATED* . The automated snapshot configuration for the OpenSearch Service domain indexes.
        :param software_update_options: Options for configuring service software updates for a domain.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.
        :param vpc_options: The virtual private cloud (VPC) configuration for the OpenSearch Service domain. For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* . If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018822cada9fc20fbc2039d546a4c366118f3bef26f6fc2fe94aa0cb220d1470)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainProps(
            access_policies=access_policies,
            advanced_options=advanced_options,
            advanced_security_options=advanced_security_options,
            cluster_config=cluster_config,
            cognito_options=cognito_options,
            domain_endpoint_options=domain_endpoint_options,
            domain_name=domain_name,
            ebs_options=ebs_options,
            encryption_at_rest_options=encryption_at_rest_options,
            engine_version=engine_version,
            log_publishing_options=log_publishing_options,
            node_to_node_encryption_options=node_to_node_encryption_options,
            off_peak_window_options=off_peak_window_options,
            snapshot_options=snapshot_options,
            software_update_options=software_update_options,
            tags=tags,
            vpc_options=vpc_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb1400bb98361a78de6ef9cf05d155acdfc5938c0aa8797ea3ce685b903fda5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f840d8ec5fd917c982c76d2cd42534262ce6e8dbdfb6d133847f579200a26f7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAdvancedSecurityOptionsAnonymousAuthDisableDate")
    def attr_advanced_security_options_anonymous_auth_disable_date(
        self,
    ) -> builtins.str:
        '''Date and time when the migration period will be disabled.

        Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .

        :cloudformationAttribute: AdvancedSecurityOptions.AnonymousAuthDisableDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAdvancedSecurityOptionsAnonymousAuthDisableDate"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the domain, such as ``arn:aws:es:us-west-2:123456789012:domain/mystack-1ab2cdefghij`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainEndpoint")
    def attr_domain_endpoint(self) -> builtins.str:
        '''The domain-specific endpoint used for requests to the OpenSearch APIs, such as ``search-mystack-1ab2cdefghij-ab1c2deckoyb3hofw7wpqa3cm.us-west-1.es.amazonaws.com`` .

        :cloudformationAttribute: DomainEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainEndpoints")
    def attr_domain_endpoints(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: DomainEndpoints
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrDomainEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The resource ID.

        For example, ``123456789012/my-domain`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsAutomatedUpdateDate")
    def attr_service_software_options_automated_update_date(self) -> builtins.str:
        '''The timestamp, in Epoch time, until which you can manually request a service software update.

        After this date, we automatically update your service software.

        :cloudformationAttribute: ServiceSoftwareOptions.AutomatedUpdateDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsAutomatedUpdateDate"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsCancellable")
    def attr_service_software_options_cancellable(self) -> _IResolvable_a771d0ef:
        '''True if you're able to cancel your service software version update.

        False if you can't cancel your service software update.

        :cloudformationAttribute: ServiceSoftwareOptions.Cancellable
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrServiceSoftwareOptionsCancellable"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsCurrentVersion")
    def attr_service_software_options_current_version(self) -> builtins.str:
        '''The current service software version present on the domain.

        :cloudformationAttribute: ServiceSoftwareOptions.CurrentVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsCurrentVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsDescription")
    def attr_service_software_options_description(self) -> builtins.str:
        '''A description of the service software update status.

        :cloudformationAttribute: ServiceSoftwareOptions.Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsDescription"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsNewVersion")
    def attr_service_software_options_new_version(self) -> builtins.str:
        '''The new service software version, if one is available.

        :cloudformationAttribute: ServiceSoftwareOptions.NewVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsNewVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsOptionalDeployment")
    def attr_service_software_options_optional_deployment(
        self,
    ) -> _IResolvable_a771d0ef:
        '''True if a service software is never automatically updated.

        False if a service software is automatically updated after the automated update date.

        :cloudformationAttribute: ServiceSoftwareOptions.OptionalDeployment
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrServiceSoftwareOptionsOptionalDeployment"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsUpdateAvailable")
    def attr_service_software_options_update_available(self) -> _IResolvable_a771d0ef:
        '''True if you're able to update your service software version.

        False if you can't update your service software version.

        :cloudformationAttribute: ServiceSoftwareOptions.UpdateAvailable
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrServiceSoftwareOptionsUpdateAvailable"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsUpdateStatus")
    def attr_service_software_options_update_status(self) -> builtins.str:
        '''The status of your service software update.

        :cloudformationAttribute: ServiceSoftwareOptions.UpdateStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsUpdateStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="accessPolicies")
    def access_policies(self) -> typing.Any:
        '''An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions.

        For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-accesspolicies
        '''
        return typing.cast(typing.Any, jsii.get(self, "accessPolicies"))

    @access_policies.setter
    def access_policies(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6f6e6287a8f76ddecc7a9d29ab054c7b74e4d4155a8011bd17b8b8fb8c55e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPolicies", value)

    @builtins.property
    @jsii.member(jsii_name="advancedOptions")
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''Additional options to specify for the OpenSearch Service domain.

        For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "advancedOptions"))

    @advanced_options.setter
    def advanced_options(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9abf96dfc5d9aa21174bc8d8109978393eae992eebbd188f5cf8e2b402a74f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedOptions", value)

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityOptions")
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_a771d0ef]]:
        '''Specifies options for fine-grained access control and SAML authentication.

        If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedsecurityoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_a771d0ef]], jsii.get(self, "advancedSecurityOptions"))

    @advanced_security_options.setter
    def advanced_security_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5b06258e30adb72b3a47046a3870f9c0cd3ab173113bad068e65e38abc278f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedSecurityOptions", value)

    @builtins.property
    @jsii.member(jsii_name="clusterConfig")
    def cluster_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.ClusterConfigProperty", _IResolvable_a771d0ef]]:
        '''Container for the cluster configuration of a domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-clusterconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.ClusterConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "clusterConfig"))

    @cluster_config.setter
    def cluster_config(
        self,
        value: typing.Optional[typing.Union["CfnDomain.ClusterConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a4159cc2d44a14ad165e347e7a89d0df7152df0bc8d4280f6c2fa3a8d88db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterConfig", value)

    @builtins.property
    @jsii.member(jsii_name="cognitoOptions")
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_a771d0ef]]:
        '''Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-cognitooptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "cognitoOptions"))

    @cognito_options.setter
    def cognito_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534f1101ea263c69b158859d57da289df750668bec0b04ee04c0989dd93a7058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cognitoOptions", value)

    @builtins.property
    @jsii.member(jsii_name="domainEndpointOptions")
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_a771d0ef]]:
        '''Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainendpointoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "domainEndpointOptions"))

    @domain_endpoint_options.setter
    def domain_endpoint_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f447d8db4b62496f9fb0d90c4b6f8336ad6e5e479643874d3f6898402f4d5f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainEndpointOptions", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''A name for the OpenSearch Service domain.

        The name must have a minimum length of 3 and a maximum length of 28. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        Required when creating a new domain.
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0460497ae9efbf7fe21e22f0cf1d32f7628f113c89633beb99b40b2b997e9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="ebsOptions")
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_a771d0ef]]:
        '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.

        For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-ebsoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "ebsOptions"))

    @ebs_options.setter
    def ebs_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a865ef21ce88ff3767b8e44f8c883018fee98a43ca245435fdedd55dbf28c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsOptions", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionAtRestOptions")
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_a771d0ef]]:
        '''Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use.

        See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-encryptionatrestoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "encryptionAtRestOptions"))

    @encryption_at_rest_options.setter
    def encryption_at_rest_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a74c2a6db0b3e60bbc408b54e01c60cea001adba6011568efed86379c6c217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtRestOptions", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of OpenSearch to use.

        The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1280a20e9f907fd13f73a434a6e03496d28879f60aab4584c971e8e115858d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="logPublishingOptions")
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_a771d0ef]]]]:
        '''An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish.

        Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-logpublishingoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "logPublishingOptions"))

    @log_publishing_options.setter
    def log_publishing_options(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5692e0bae978b2c4c8b39ca4ce62d10d27651e91a1bd75fe7b51a0d3d825aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logPublishingOptions", value)

    @builtins.property
    @jsii.member(jsii_name="nodeToNodeEncryptionOptions")
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_a771d0ef]]:
        '''Specifies whether node-to-node encryption is enabled.

        See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-nodetonodeencryptionoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "nodeToNodeEncryptionOptions"))

    @node_to_node_encryption_options.setter
    def node_to_node_encryption_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fa08c60ea9a381906d6e170f52e1cb5a03e3f0ed199e9c475e7714b628be7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeToNodeEncryptionOptions", value)

    @builtins.property
    @jsii.member(jsii_name="offPeakWindowOptions")
    def off_peak_window_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.OffPeakWindowOptionsProperty", _IResolvable_a771d0ef]]:
        '''Options for a domain's off-peak window, during which OpenSearch Service can perform mandatory configuration changes on the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-offpeakwindowoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.OffPeakWindowOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "offPeakWindowOptions"))

    @off_peak_window_options.setter
    def off_peak_window_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.OffPeakWindowOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e212e148821f061762c02d4e532a8aacb2788158bf57698c5a4d070d6e244359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offPeakWindowOptions", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotOptions")
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_a771d0ef]]:
        '''*DEPRECATED* .

        The automated snapshot configuration for the OpenSearch Service domain indexes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-snapshotoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "snapshotOptions"))

    @snapshot_options.setter
    def snapshot_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546733aebb1dc8ca80aa8a36976d37ba971e08987010a37b593f31db5a429136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotOptions", value)

    @builtins.property
    @jsii.member(jsii_name="softwareUpdateOptions")
    def software_update_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.SoftwareUpdateOptionsProperty", _IResolvable_a771d0ef]]:
        '''Options for configuring service software updates for a domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-softwareupdateoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.SoftwareUpdateOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "softwareUpdateOptions"))

    @software_update_options.setter
    def software_update_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.SoftwareUpdateOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97be705d8a750b441a8c15d6ba1850f1a0dd73f190c9ab4a5289e77af77860f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "softwareUpdateOptions", value)

    @builtins.property
    @jsii.member(jsii_name="vpcOptions")
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_a771d0ef]]:
        '''The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

        For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-vpcoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcOptions"))

    @vpc_options.setter
    def vpc_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f1de6d7691e56980c1571598ce9803fac5744fbb94eed7590ee696b897b4d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcOptions", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.AdvancedSecurityOptionsInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "anonymous_auth_disable_date": "anonymousAuthDisableDate",
            "anonymous_auth_enabled": "anonymousAuthEnabled",
            "enabled": "enabled",
            "internal_user_database_enabled": "internalUserDatabaseEnabled",
            "master_user_options": "masterUserOptions",
            "saml_options": "samlOptions",
        },
    )
    class AdvancedSecurityOptionsInputProperty:
        def __init__(
            self,
            *,
            anonymous_auth_disable_date: typing.Optional[builtins.str] = None,
            anonymous_auth_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            master_user_options: typing.Optional[typing.Union[typing.Union["CfnDomain.MasterUserOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            saml_options: typing.Optional[typing.Union[typing.Union["CfnDomain.SAMLOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies options for fine-grained access control.

            If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.

            :param anonymous_auth_disable_date: Date and time when the migration period will be disabled. Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .
            :param anonymous_auth_enabled: True to enable a 30-day migration period during which administrators can create role mappings. Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .
            :param enabled: True to enable fine-grained access control. You must also enable encryption of data at rest and node-to-node encryption. See `Fine-grained access control in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html>`_ .
            :param internal_user_database_enabled: True to enable the internal user database.
            :param master_user_options: Specifies information about the master user.
            :param saml_options: Container for information about the SAML configuration for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                advanced_security_options_input_property = opensearchservice.CfnDomain.AdvancedSecurityOptionsInputProperty(
                    anonymous_auth_disable_date="anonymousAuthDisableDate",
                    anonymous_auth_enabled=False,
                    enabled=False,
                    internal_user_database_enabled=False,
                    master_user_options=opensearchservice.CfnDomain.MasterUserOptionsProperty(
                        master_user_arn="masterUserArn",
                        master_user_name="masterUserName",
                        master_user_password="masterUserPassword"
                    ),
                    saml_options=opensearchservice.CfnDomain.SAMLOptionsProperty(
                        enabled=False,
                        idp=opensearchservice.CfnDomain.IdpProperty(
                            entity_id="entityId",
                            metadata_content="metadataContent"
                        ),
                        master_backend_role="masterBackendRole",
                        master_user_name="masterUserName",
                        roles_key="rolesKey",
                        session_timeout_minutes=123,
                        subject_key="subjectKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f25e94733d813ccf0f9bc0aa6aa7edcfa0b559a04cb6255e5351f7a32a7c314)
                check_type(argname="argument anonymous_auth_disable_date", value=anonymous_auth_disable_date, expected_type=type_hints["anonymous_auth_disable_date"])
                check_type(argname="argument anonymous_auth_enabled", value=anonymous_auth_enabled, expected_type=type_hints["anonymous_auth_enabled"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument internal_user_database_enabled", value=internal_user_database_enabled, expected_type=type_hints["internal_user_database_enabled"])
                check_type(argname="argument master_user_options", value=master_user_options, expected_type=type_hints["master_user_options"])
                check_type(argname="argument saml_options", value=saml_options, expected_type=type_hints["saml_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if anonymous_auth_disable_date is not None:
                self._values["anonymous_auth_disable_date"] = anonymous_auth_disable_date
            if anonymous_auth_enabled is not None:
                self._values["anonymous_auth_enabled"] = anonymous_auth_enabled
            if enabled is not None:
                self._values["enabled"] = enabled
            if internal_user_database_enabled is not None:
                self._values["internal_user_database_enabled"] = internal_user_database_enabled
            if master_user_options is not None:
                self._values["master_user_options"] = master_user_options
            if saml_options is not None:
                self._values["saml_options"] = saml_options

        @builtins.property
        def anonymous_auth_disable_date(self) -> typing.Optional[builtins.str]:
            '''Date and time when the migration period will be disabled.

            Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-anonymousauthdisabledate
            '''
            result = self._values.get("anonymous_auth_disable_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def anonymous_auth_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True to enable a 30-day migration period during which administrators can create role mappings.

            Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-anonymousauthenabled
            '''
            result = self._values.get("anonymous_auth_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True to enable fine-grained access control.

            You must also enable encryption of data at rest and node-to-node encryption. See `Fine-grained access control in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def internal_user_database_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True to enable the internal user database.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-internaluserdatabaseenabled
            '''
            result = self._values.get("internal_user_database_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def master_user_options(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.MasterUserOptionsProperty", _IResolvable_a771d0ef]]:
            '''Specifies information about the master user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-masteruseroptions
            '''
            result = self._values.get("master_user_options")
            return typing.cast(typing.Optional[typing.Union["CfnDomain.MasterUserOptionsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def saml_options(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.SAMLOptionsProperty", _IResolvable_a771d0ef]]:
            '''Container for information about the SAML configuration for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-samloptions
            '''
            result = self._values.get("saml_options")
            return typing.cast(typing.Optional[typing.Union["CfnDomain.SAMLOptionsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedSecurityOptionsInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.ClusterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dedicated_master_count": "dedicatedMasterCount",
            "dedicated_master_enabled": "dedicatedMasterEnabled",
            "dedicated_master_type": "dedicatedMasterType",
            "instance_count": "instanceCount",
            "instance_type": "instanceType",
            "multi_az_with_standby_enabled": "multiAzWithStandbyEnabled",
            "warm_count": "warmCount",
            "warm_enabled": "warmEnabled",
            "warm_type": "warmType",
            "zone_awareness_config": "zoneAwarenessConfig",
            "zone_awareness_enabled": "zoneAwarenessEnabled",
        },
    )
    class ClusterConfigProperty:
        def __init__(
            self,
            *,
            dedicated_master_count: typing.Optional[jsii.Number] = None,
            dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            dedicated_master_type: typing.Optional[builtins.str] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            instance_type: typing.Optional[builtins.str] = None,
            multi_az_with_standby_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            warm_count: typing.Optional[jsii.Number] = None,
            warm_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            warm_type: typing.Optional[builtins.str] = None,
            zone_awareness_config: typing.Optional[typing.Union[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The cluster configuration for the OpenSearch Service domain.

            You can specify options such as the instance type and the number of instances. For more information, see `Creating and managing Amazon OpenSearch Service domains <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param dedicated_master_count: The number of instances to use for the master node. If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property.
            :param dedicated_master_enabled: Indicates whether to use a dedicated master node for the OpenSearch Service domain. A dedicated master node is a cluster node that performs cluster management tasks, but doesn't hold data or respond to data upload requests. Dedicated master nodes offload cluster management tasks to increase the stability of your search clusters. See `Dedicated master nodes in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html>`_ .
            :param dedicated_master_type: The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search`` . If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property. For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .
            :param instance_count: The number of data nodes (instances) to use in the OpenSearch Service domain.
            :param instance_type: The instance type for your data nodes, such as ``m3.medium.search`` . For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .
            :param multi_az_with_standby_enabled: Indicates whether Multi-AZ with Standby deployment option is enabled. For more information, see `Multi-AZ with Standby <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html#managedomains-za-standby>`_ .
            :param warm_count: The number of warm nodes in the cluster.
            :param warm_enabled: Whether to enable UltraWarm storage for the cluster. See `UltraWarm storage for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ultrawarm.html>`_ .
            :param warm_type: The instance type for the cluster's warm nodes.
            :param zone_awareness_config: Specifies zone awareness configuration options. Only use if ``ZoneAwarenessEnabled`` is ``true`` .
            :param zone_awareness_enabled: Indicates whether to enable zone awareness for the OpenSearch Service domain. When you enable zone awareness, OpenSearch Service allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see `Configuring a multi-AZ domain in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                cluster_config_property = opensearchservice.CfnDomain.ClusterConfigProperty(
                    dedicated_master_count=123,
                    dedicated_master_enabled=False,
                    dedicated_master_type="dedicatedMasterType",
                    instance_count=123,
                    instance_type="instanceType",
                    multi_az_with_standby_enabled=False,
                    warm_count=123,
                    warm_enabled=False,
                    warm_type="warmType",
                    zone_awareness_config=opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                        availability_zone_count=123
                    ),
                    zone_awareness_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19798e56dc23966a5ab47af146c9237b1946659af1c4f9e448eaef1a96adb383)
                check_type(argname="argument dedicated_master_count", value=dedicated_master_count, expected_type=type_hints["dedicated_master_count"])
                check_type(argname="argument dedicated_master_enabled", value=dedicated_master_enabled, expected_type=type_hints["dedicated_master_enabled"])
                check_type(argname="argument dedicated_master_type", value=dedicated_master_type, expected_type=type_hints["dedicated_master_type"])
                check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument multi_az_with_standby_enabled", value=multi_az_with_standby_enabled, expected_type=type_hints["multi_az_with_standby_enabled"])
                check_type(argname="argument warm_count", value=warm_count, expected_type=type_hints["warm_count"])
                check_type(argname="argument warm_enabled", value=warm_enabled, expected_type=type_hints["warm_enabled"])
                check_type(argname="argument warm_type", value=warm_type, expected_type=type_hints["warm_type"])
                check_type(argname="argument zone_awareness_config", value=zone_awareness_config, expected_type=type_hints["zone_awareness_config"])
                check_type(argname="argument zone_awareness_enabled", value=zone_awareness_enabled, expected_type=type_hints["zone_awareness_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dedicated_master_count is not None:
                self._values["dedicated_master_count"] = dedicated_master_count
            if dedicated_master_enabled is not None:
                self._values["dedicated_master_enabled"] = dedicated_master_enabled
            if dedicated_master_type is not None:
                self._values["dedicated_master_type"] = dedicated_master_type
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if multi_az_with_standby_enabled is not None:
                self._values["multi_az_with_standby_enabled"] = multi_az_with_standby_enabled
            if warm_count is not None:
                self._values["warm_count"] = warm_count
            if warm_enabled is not None:
                self._values["warm_enabled"] = warm_enabled
            if warm_type is not None:
                self._values["warm_type"] = warm_type
            if zone_awareness_config is not None:
                self._values["zone_awareness_config"] = zone_awareness_config
            if zone_awareness_enabled is not None:
                self._values["zone_awareness_enabled"] = zone_awareness_enabled

        @builtins.property
        def dedicated_master_count(self) -> typing.Optional[jsii.Number]:
            '''The number of instances to use for the master node.

            If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmastercount
            '''
            result = self._values.get("dedicated_master_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dedicated_master_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether to use a dedicated master node for the OpenSearch Service domain.

            A dedicated master node is a cluster node that performs cluster management tasks, but doesn't hold data or respond to data upload requests. Dedicated master nodes offload cluster management tasks to increase the stability of your search clusters. See `Dedicated master nodes in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmasterenabled
            '''
            result = self._values.get("dedicated_master_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def dedicated_master_type(self) -> typing.Optional[builtins.str]:
            '''The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search`` . If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property. For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmastertype
            '''
            result = self._values.get("dedicated_master_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            '''The number of data nodes (instances) to use in the OpenSearch Service domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-instancecount
            '''
            result = self._values.get("instance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The instance type for your data nodes, such as ``m3.medium.search`` . For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multi_az_with_standby_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether Multi-AZ with Standby deployment option is enabled.

            For more information, see `Multi-AZ with Standby <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html#managedomains-za-standby>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-multiazwithstandbyenabled
            '''
            result = self._values.get("multi_az_with_standby_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def warm_count(self) -> typing.Optional[jsii.Number]:
            '''The number of warm nodes in the cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmcount
            '''
            result = self._values.get("warm_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def warm_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether to enable UltraWarm storage for the cluster.

            See `UltraWarm storage for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ultrawarm.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmenabled
            '''
            result = self._values.get("warm_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def warm_type(self) -> typing.Optional[builtins.str]:
            '''The instance type for the cluster's warm nodes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmtype
            '''
            result = self._values.get("warm_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zone_awareness_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_a771d0ef]]:
            '''Specifies zone awareness configuration options.

            Only use if ``ZoneAwarenessEnabled`` is ``true`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-zoneawarenessconfig
            '''
            result = self._values.get("zone_awareness_config")
            return typing.cast(typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zone_awareness_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether to enable zone awareness for the OpenSearch Service domain.

            When you enable zone awareness, OpenSearch Service allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see `Configuring a multi-AZ domain in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-zoneawarenessenabled
            '''
            result = self._values.get("zone_awareness_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClusterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.CognitoOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "identity_pool_id": "identityPoolId",
            "role_arn": "roleArn",
            "user_pool_id": "userPoolId",
        },
    )
    class CognitoOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            identity_pool_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

            :param enabled: Whether to enable or disable Amazon Cognito authentication for OpenSearch Dashboards. See `Amazon Cognito authentication for OpenSearch Dashboards <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html>`_ .
            :param identity_pool_id: The Amazon Cognito identity pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication. Required if you enabled Cognito Authentication for OpenSearch Dashboards.
            :param role_arn: The ``AmazonOpenSearchServiceCognitoAccess`` role that allows OpenSearch Service to configure your user pool and identity pool. Required if you enabled Cognito Authentication for OpenSearch Dashboards.
            :param user_pool_id: The Amazon Cognito user pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication. Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                cognito_options_property = opensearchservice.CfnDomain.CognitoOptionsProperty(
                    enabled=False,
                    identity_pool_id="identityPoolId",
                    role_arn="roleArn",
                    user_pool_id="userPoolId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6112a9197eaf165567c1e897c33495f3a0f0e609b7916069e961a617313783cf)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if identity_pool_id is not None:
                self._values["identity_pool_id"] = identity_pool_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether to enable or disable Amazon Cognito authentication for OpenSearch Dashboards.

            See `Amazon Cognito authentication for OpenSearch Dashboards <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def identity_pool_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Cognito identity pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-identitypoolid
            '''
            result = self._values.get("identity_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ``AmazonOpenSearchServiceCognitoAccess`` role that allows OpenSearch Service to configure your user pool and identity pool.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Cognito user pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.DomainEndpointOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_endpoint": "customEndpoint",
            "custom_endpoint_certificate_arn": "customEndpointCertificateArn",
            "custom_endpoint_enabled": "customEndpointEnabled",
            "enforce_https": "enforceHttps",
            "tls_security_policy": "tlsSecurityPolicy",
        },
    )
    class DomainEndpointOptionsProperty:
        def __init__(
            self,
            *,
            custom_endpoint: typing.Optional[builtins.str] = None,
            custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
            custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            enforce_https: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            tls_security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.

            :param custom_endpoint: The fully qualified URL for your custom endpoint. Required if you enabled a custom endpoint for the domain.
            :param custom_endpoint_certificate_arn: The AWS Certificate Manager ARN for your domain's SSL/TLS certificate. Required if you enabled a custom endpoint for the domain.
            :param custom_endpoint_enabled: True to enable a custom endpoint for the domain. If enabled, you must also provide values for ``CustomEndpoint`` and ``CustomEndpointCertificateArn`` .
            :param enforce_https: True to require that all traffic to the domain arrive over HTTPS. Required if you enable fine-grained access control in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .
            :param tls_security_policy: The minimum TLS version required for traffic to the domain. Valid values are TLS 1.0 (default) or 1.2:. - ``Policy-Min-TLS-1-0-2019-07`` - ``Policy-Min-TLS-1-2-2019-07``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                domain_endpoint_options_property = opensearchservice.CfnDomain.DomainEndpointOptionsProperty(
                    custom_endpoint="customEndpoint",
                    custom_endpoint_certificate_arn="customEndpointCertificateArn",
                    custom_endpoint_enabled=False,
                    enforce_https=False,
                    tls_security_policy="tlsSecurityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5bc7f3bccfca867e6b746ea2aa1711359102884bb2fed42ee9ded52d28191fb)
                check_type(argname="argument custom_endpoint", value=custom_endpoint, expected_type=type_hints["custom_endpoint"])
                check_type(argname="argument custom_endpoint_certificate_arn", value=custom_endpoint_certificate_arn, expected_type=type_hints["custom_endpoint_certificate_arn"])
                check_type(argname="argument custom_endpoint_enabled", value=custom_endpoint_enabled, expected_type=type_hints["custom_endpoint_enabled"])
                check_type(argname="argument enforce_https", value=enforce_https, expected_type=type_hints["enforce_https"])
                check_type(argname="argument tls_security_policy", value=tls_security_policy, expected_type=type_hints["tls_security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_endpoint is not None:
                self._values["custom_endpoint"] = custom_endpoint
            if custom_endpoint_certificate_arn is not None:
                self._values["custom_endpoint_certificate_arn"] = custom_endpoint_certificate_arn
            if custom_endpoint_enabled is not None:
                self._values["custom_endpoint_enabled"] = custom_endpoint_enabled
            if enforce_https is not None:
                self._values["enforce_https"] = enforce_https
            if tls_security_policy is not None:
                self._values["tls_security_policy"] = tls_security_policy

        @builtins.property
        def custom_endpoint(self) -> typing.Optional[builtins.str]:
            '''The fully qualified URL for your custom endpoint.

            Required if you enabled a custom endpoint for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpoint
            '''
            result = self._values.get("custom_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_endpoint_certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The AWS Certificate Manager ARN for your domain's SSL/TLS certificate.

            Required if you enabled a custom endpoint for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpointcertificatearn
            '''
            result = self._values.get("custom_endpoint_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_endpoint_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True to enable a custom endpoint for the domain.

            If enabled, you must also provide values for ``CustomEndpoint`` and ``CustomEndpointCertificateArn`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpointenabled
            '''
            result = self._values.get("custom_endpoint_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def enforce_https(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True to require that all traffic to the domain arrive over HTTPS.

            Required if you enable fine-grained access control in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-enforcehttps
            '''
            result = self._values.get("enforce_https")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def tls_security_policy(self) -> typing.Optional[builtins.str]:
            '''The minimum TLS version required for traffic to the domain. Valid values are TLS 1.0 (default) or 1.2:.

            - ``Policy-Min-TLS-1-0-2019-07``
            - ``Policy-Min-TLS-1-2-2019-07``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-tlssecuritypolicy
            '''
            result = self._values.get("tls_security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainEndpointOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.EBSOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_enabled": "ebsEnabled",
            "iops": "iops",
            "throughput": "throughput",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EBSOptionsProperty:
        def __init__(
            self,
            *,
            ebs_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            iops: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.

            For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param ebs_enabled: Specifies whether Amazon EBS volumes are attached to data nodes in the OpenSearch Service domain.
            :param iops: The number of I/O operations per second (IOPS) that the volume supports. This property applies only to the ``gp3`` and provisioned IOPS EBS volume types.
            :param throughput: The throughput (in MiB/s) of the EBS volumes attached to data nodes. Applies only to the ``gp3`` volume type.
            :param volume_size: The size (in GiB) of the EBS volume for each data node. The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .
            :param volume_type: The EBS volume type to use with the OpenSearch Service domain. If you choose ``gp3`` , you must also specify values for ``Iops`` and ``Throughput`` . For more information about each type, see `Amazon EBS volume types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                e_bSOptions_property = opensearchservice.CfnDomain.EBSOptionsProperty(
                    ebs_enabled=False,
                    iops=123,
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9e5ba896288813a931fc55037d7cabde27b891be5c68322a634838446c07ac9)
                check_type(argname="argument ebs_enabled", value=ebs_enabled, expected_type=type_hints["ebs_enabled"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_enabled is not None:
                self._values["ebs_enabled"] = ebs_enabled
            if iops is not None:
                self._values["iops"] = iops
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def ebs_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether Amazon EBS volumes are attached to data nodes in the OpenSearch Service domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-ebsenabled
            '''
            result = self._values.get("ebs_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second (IOPS) that the volume supports.

            This property applies only to the ``gp3`` and provisioned IOPS EBS volume types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''The throughput (in MiB/s) of the EBS volumes attached to data nodes.

            Applies only to the ``gp3`` volume type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''The size (in GiB) of the EBS volume for each data node.

            The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The EBS volume type to use with the OpenSearch Service domain.

            If you choose ``gp3`` , you must also specify values for ``Iops`` and ``Throughput`` . For more information about each type, see `Amazon EBS volume types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EBSOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.EncryptionAtRestOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "kms_key_id": "kmsKeyId"},
    )
    class EncryptionAtRestOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Whether the domain should encrypt data at rest, and if so, the AWS Key Management Service key to use.

            :param enabled: Specify ``true`` to enable encryption at rest. Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .
            :param kms_key_id: The KMS key ID. Takes the form ``1a2a3a4-1a2a-3a4a-5a6a-1a2a3a4a5a6a`` . Required if you enable encryption at rest. You can also use ``keyAlias`` as a value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                encryption_at_rest_options_property = opensearchservice.CfnDomain.EncryptionAtRestOptionsProperty(
                    enabled=False,
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5f9d7edf63db161e1ddf10fc57a52b04e40cdb1af3b43f111b0dac0a7241ec7)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specify ``true`` to enable encryption at rest.

            Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html#cfn-opensearchservice-domain-encryptionatrestoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The KMS key ID. Takes the form ``1a2a3a4-1a2a-3a4a-5a6a-1a2a3a4a5a6a`` . Required if you enable encryption at rest.

            You can also use ``keyAlias`` as a value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html#cfn-opensearchservice-domain-encryptionatrestoptions-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionAtRestOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.IdpProperty",
        jsii_struct_bases=[],
        name_mapping={"entity_id": "entityId", "metadata_content": "metadataContent"},
    )
    class IdpProperty:
        def __init__(
            self,
            *,
            entity_id: builtins.str,
            metadata_content: builtins.str,
        ) -> None:
            '''The SAML Identity Provider's information.

            :param entity_id: The unique entity ID of the application in the SAML identity provider.
            :param metadata_content: The metadata of the SAML application, in XML format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-idp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                idp_property = opensearchservice.CfnDomain.IdpProperty(
                    entity_id="entityId",
                    metadata_content="metadataContent"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3789c2cead192a4265a38342abd75927c0b69587b8fc341c9d76bfd4ac852eee)
                check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
                check_type(argname="argument metadata_content", value=metadata_content, expected_type=type_hints["metadata_content"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "entity_id": entity_id,
                "metadata_content": metadata_content,
            }

        @builtins.property
        def entity_id(self) -> builtins.str:
            '''The unique entity ID of the application in the SAML identity provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-idp.html#cfn-opensearchservice-domain-idp-entityid
            '''
            result = self._values.get("entity_id")
            assert result is not None, "Required property 'entity_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metadata_content(self) -> builtins.str:
            '''The metadata of the SAML application, in XML format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-idp.html#cfn-opensearchservice-domain-idp-metadatacontent
            '''
            result = self._values.get("metadata_content")
            assert result is not None, "Required property 'metadata_content' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdpProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.LogPublishingOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_log_group_arn": "cloudWatchLogsLogGroupArn",
            "enabled": "enabled",
        },
    )
    class LogPublishingOptionProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies whether the OpenSearch Service domain publishes application, search slow logs, or index slow logs to Amazon CloudWatch.

            Each option must be an object of name ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , or ``AUDIT_LOGS`` depending on the type of logs you want to publish. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .

            Before you enable log publishing, you need to create a CloudWatch log group and provide OpenSearch Service the correct permissions to write to it. To learn more, see `Enabling log publishing ( AWS CloudFormation) <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createdomain-configure-slow-logs.html#createdomain-configure-slow-logs-cfn>`_ .

            :param cloud_watch_logs_log_group_arn: Specifies the CloudWatch log group to publish to. Required if you enable log publishing.
            :param enabled: If ``true`` , enables the publishing of logs to CloudWatch. Default: ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                log_publishing_option_property = opensearchservice.CfnDomain.LogPublishingOptionProperty(
                    cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42693055cd068c607ea45e66f4f1d9be14b396e9c5428d47c7242cc35cb9dee6)
                check_type(argname="argument cloud_watch_logs_log_group_arn", value=cloud_watch_logs_log_group_arn, expected_type=type_hints["cloud_watch_logs_log_group_arn"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_log_group_arn is not None:
                self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the CloudWatch log group to publish to.

            Required if you enable log publishing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html#cfn-opensearchservice-domain-logpublishingoption-cloudwatchlogsloggrouparn
            '''
            result = self._values.get("cloud_watch_logs_log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''If ``true`` , enables the publishing of logs to CloudWatch.

            Default: ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html#cfn-opensearchservice-domain-logpublishingoption-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPublishingOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.MasterUserOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "master_user_arn": "masterUserArn",
            "master_user_name": "masterUserName",
            "master_user_password": "masterUserPassword",
        },
    )
    class MasterUserOptionsProperty:
        def __init__(
            self,
            *,
            master_user_arn: typing.Optional[builtins.str] = None,
            master_user_name: typing.Optional[builtins.str] = None,
            master_user_password: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information about the master user.

            Required if if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :param master_user_arn: Amazon Resource Name (ARN) for the master user. The ARN can point to an IAM user or role. This property is required for Amazon Cognito to work, and it must match the role configured for Cognito. Only specify if ``InternalUserDatabaseEnabled`` is false in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .
            :param master_user_name: Username for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ . If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.
            :param master_user_password: Password for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ . If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                master_user_options_property = opensearchservice.CfnDomain.MasterUserOptionsProperty(
                    master_user_arn="masterUserArn",
                    master_user_name="masterUserName",
                    master_user_password="masterUserPassword"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd1175b93b058b14bd199f1d17669c78584c8acaa5dbf2de40332b6dc939a66d)
                check_type(argname="argument master_user_arn", value=master_user_arn, expected_type=type_hints["master_user_arn"])
                check_type(argname="argument master_user_name", value=master_user_name, expected_type=type_hints["master_user_name"])
                check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if master_user_arn is not None:
                self._values["master_user_arn"] = master_user_arn
            if master_user_name is not None:
                self._values["master_user_name"] = master_user_name
            if master_user_password is not None:
                self._values["master_user_password"] = master_user_password

        @builtins.property
        def master_user_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) for the master user.

            The ARN can point to an IAM user or role. This property is required for Amazon Cognito to work, and it must match the role configured for Cognito. Only specify if ``InternalUserDatabaseEnabled`` is false in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masteruserarn
            '''
            result = self._values.get("master_user_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_name(self) -> typing.Optional[builtins.str]:
            '''Username for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masterusername
            '''
            result = self._values.get("master_user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_password(self) -> typing.Optional[builtins.str]:
            '''Password for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masteruserpassword
            '''
            result = self._values.get("master_user_password")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MasterUserOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.NodeToNodeEncryptionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class NodeToNodeEncryptionOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies options for node-to-node encryption.

            :param enabled: Specifies to enable or disable node-to-node encryption on the domain. Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                node_to_node_encryption_options_property = opensearchservice.CfnDomain.NodeToNodeEncryptionOptionsProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f74f7c0f6498bb8b76b541391e2dc24c8dd9ca6a3e8cc87ea34b001425f460c5)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies to enable or disable node-to-node encryption on the domain.

            Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html#cfn-opensearchservice-domain-nodetonodeencryptionoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeToNodeEncryptionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.OffPeakWindowOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "off_peak_window": "offPeakWindow"},
    )
    class OffPeakWindowOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            off_peak_window: typing.Optional[typing.Union[typing.Union["CfnDomain.OffPeakWindowProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Off-peak window settings for the domain.

            :param enabled: Specifies whether off-peak window settings are enabled for the domain.
            :param off_peak_window: Off-peak window settings for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindowoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                off_peak_window_options_property = opensearchservice.CfnDomain.OffPeakWindowOptionsProperty(
                    enabled=False,
                    off_peak_window=opensearchservice.CfnDomain.OffPeakWindowProperty(
                        window_start_time=opensearchservice.CfnDomain.WindowStartTimeProperty(
                            hours=123,
                            minutes=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5caf8191da4b1f99f382e10c5a894613cc7eb5e57ca0c4b24a9e7118a1c4ae95)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument off_peak_window", value=off_peak_window, expected_type=type_hints["off_peak_window"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if off_peak_window is not None:
                self._values["off_peak_window"] = off_peak_window

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether off-peak window settings are enabled for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindowoptions.html#cfn-opensearchservice-domain-offpeakwindowoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def off_peak_window(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.OffPeakWindowProperty", _IResolvable_a771d0ef]]:
            '''Off-peak window settings for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindowoptions.html#cfn-opensearchservice-domain-offpeakwindowoptions-offpeakwindow
            '''
            result = self._values.get("off_peak_window")
            return typing.cast(typing.Optional[typing.Union["CfnDomain.OffPeakWindowProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OffPeakWindowOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.OffPeakWindowProperty",
        jsii_struct_bases=[],
        name_mapping={"window_start_time": "windowStartTime"},
    )
    class OffPeakWindowProperty:
        def __init__(
            self,
            *,
            window_start_time: typing.Optional[typing.Union[typing.Union["CfnDomain.WindowStartTimeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''A custom 10-hour, low-traffic window during which OpenSearch Service can perform mandatory configuration changes on the domain.

            These actions can include scheduled service software updates and blue/green Auto-Tune enhancements. OpenSearch Service will schedule these actions during the window that you specify. If you don't specify a window start time, it defaults to 10:00 P.M. local time.

            :param window_start_time: The desired start time for an off-peak maintenance window.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                off_peak_window_property = opensearchservice.CfnDomain.OffPeakWindowProperty(
                    window_start_time=opensearchservice.CfnDomain.WindowStartTimeProperty(
                        hours=123,
                        minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b432435aeb6103933df960b9cd463d11e0b08d4e79978e5f9717121c618e55a)
                check_type(argname="argument window_start_time", value=window_start_time, expected_type=type_hints["window_start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if window_start_time is not None:
                self._values["window_start_time"] = window_start_time

        @builtins.property
        def window_start_time(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.WindowStartTimeProperty", _IResolvable_a771d0ef]]:
            '''The desired start time for an off-peak maintenance window.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindow.html#cfn-opensearchservice-domain-offpeakwindow-windowstarttime
            '''
            result = self._values.get("window_start_time")
            return typing.cast(typing.Optional[typing.Union["CfnDomain.WindowStartTimeProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OffPeakWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.SAMLOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "idp": "idp",
            "master_backend_role": "masterBackendRole",
            "master_user_name": "masterUserName",
            "roles_key": "rolesKey",
            "session_timeout_minutes": "sessionTimeoutMinutes",
            "subject_key": "subjectKey",
        },
    )
    class SAMLOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            idp: typing.Optional[typing.Union[typing.Union["CfnDomain.IdpProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            master_backend_role: typing.Optional[builtins.str] = None,
            master_user_name: typing.Optional[builtins.str] = None,
            roles_key: typing.Optional[builtins.str] = None,
            session_timeout_minutes: typing.Optional[jsii.Number] = None,
            subject_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Container for information about the SAML configuration for OpenSearch Dashboards.

            :param enabled: True to enable SAML authentication for a domain.
            :param idp: The SAML Identity Provider's information.
            :param master_backend_role: The backend role that the SAML master user is mapped to.
            :param master_user_name: The SAML master user name, which is stored in the domain's internal user database.
            :param roles_key: Element of the SAML assertion to use for backend roles. Default is ``roles`` .
            :param session_timeout_minutes: The duration, in minutes, after which a user session becomes inactive. Acceptable values are between 1 and 1440, and the default value is 60.
            :param subject_key: Element of the SAML assertion to use for the user name. Default is ``NameID`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                s_aMLOptions_property = opensearchservice.CfnDomain.SAMLOptionsProperty(
                    enabled=False,
                    idp=opensearchservice.CfnDomain.IdpProperty(
                        entity_id="entityId",
                        metadata_content="metadataContent"
                    ),
                    master_backend_role="masterBackendRole",
                    master_user_name="masterUserName",
                    roles_key="rolesKey",
                    session_timeout_minutes=123,
                    subject_key="subjectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1044cfb3a0176eb79a302e5224d21aca834866dd3131f7b026bf2d38858d3635)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument idp", value=idp, expected_type=type_hints["idp"])
                check_type(argname="argument master_backend_role", value=master_backend_role, expected_type=type_hints["master_backend_role"])
                check_type(argname="argument master_user_name", value=master_user_name, expected_type=type_hints["master_user_name"])
                check_type(argname="argument roles_key", value=roles_key, expected_type=type_hints["roles_key"])
                check_type(argname="argument session_timeout_minutes", value=session_timeout_minutes, expected_type=type_hints["session_timeout_minutes"])
                check_type(argname="argument subject_key", value=subject_key, expected_type=type_hints["subject_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if idp is not None:
                self._values["idp"] = idp
            if master_backend_role is not None:
                self._values["master_backend_role"] = master_backend_role
            if master_user_name is not None:
                self._values["master_user_name"] = master_user_name
            if roles_key is not None:
                self._values["roles_key"] = roles_key
            if session_timeout_minutes is not None:
                self._values["session_timeout_minutes"] = session_timeout_minutes
            if subject_key is not None:
                self._values["subject_key"] = subject_key

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True to enable SAML authentication for a domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def idp(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.IdpProperty", _IResolvable_a771d0ef]]:
            '''The SAML Identity Provider's information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-idp
            '''
            result = self._values.get("idp")
            return typing.cast(typing.Optional[typing.Union["CfnDomain.IdpProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def master_backend_role(self) -> typing.Optional[builtins.str]:
            '''The backend role that the SAML master user is mapped to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-masterbackendrole
            '''
            result = self._values.get("master_backend_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_name(self) -> typing.Optional[builtins.str]:
            '''The SAML master user name, which is stored in the domain's internal user database.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-masterusername
            '''
            result = self._values.get("master_user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def roles_key(self) -> typing.Optional[builtins.str]:
            '''Element of the SAML assertion to use for backend roles.

            Default is ``roles`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-roleskey
            '''
            result = self._values.get("roles_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The duration, in minutes, after which a user session becomes inactive.

            Acceptable values are between 1 and 1440, and the default value is 60.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-sessiontimeoutminutes
            '''
            result = self._values.get("session_timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def subject_key(self) -> typing.Optional[builtins.str]:
            '''Element of the SAML assertion to use for the user name.

            Default is ``NameID`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-subjectkey
            '''
            result = self._values.get("subject_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMLOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.ServiceSoftwareOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automated_update_date": "automatedUpdateDate",
            "cancellable": "cancellable",
            "current_version": "currentVersion",
            "description": "description",
            "new_version": "newVersion",
            "optional_deployment": "optionalDeployment",
            "update_available": "updateAvailable",
            "update_status": "updateStatus",
        },
    )
    class ServiceSoftwareOptionsProperty:
        def __init__(
            self,
            *,
            automated_update_date: typing.Optional[builtins.str] = None,
            cancellable: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            current_version: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            new_version: typing.Optional[builtins.str] = None,
            optional_deployment: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            update_available: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            update_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The current status of the service software for an Amazon OpenSearch Service domain.

            For more information, see `Service software updates in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/service-software.html>`_ .

            :param automated_update_date: The timestamp, in Epoch time, until which you can manually request a service software update. After this date, we automatically update your service software.
            :param cancellable: True if you're able to cancel your service software version update. False if you can't cancel your service software update.
            :param current_version: The current service software version present on the domain.
            :param description: A description of the service software update status.
            :param new_version: The new service software version, if one is available.
            :param optional_deployment: True if a service software is never automatically updated. False if a service software is automatically updated after the automated update date.
            :param update_available: True if you're able to update your service software version. False if you can't update your service software version.
            :param update_status: The status of your service software update.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                service_software_options_property = opensearchservice.CfnDomain.ServiceSoftwareOptionsProperty(
                    automated_update_date="automatedUpdateDate",
                    cancellable=False,
                    current_version="currentVersion",
                    description="description",
                    new_version="newVersion",
                    optional_deployment=False,
                    update_available=False,
                    update_status="updateStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc00496502f222c3c2ef4f5ee4237cf51fc5eaf9f1d6ccfb22071a8d7fe6ae0c)
                check_type(argname="argument automated_update_date", value=automated_update_date, expected_type=type_hints["automated_update_date"])
                check_type(argname="argument cancellable", value=cancellable, expected_type=type_hints["cancellable"])
                check_type(argname="argument current_version", value=current_version, expected_type=type_hints["current_version"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument new_version", value=new_version, expected_type=type_hints["new_version"])
                check_type(argname="argument optional_deployment", value=optional_deployment, expected_type=type_hints["optional_deployment"])
                check_type(argname="argument update_available", value=update_available, expected_type=type_hints["update_available"])
                check_type(argname="argument update_status", value=update_status, expected_type=type_hints["update_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automated_update_date is not None:
                self._values["automated_update_date"] = automated_update_date
            if cancellable is not None:
                self._values["cancellable"] = cancellable
            if current_version is not None:
                self._values["current_version"] = current_version
            if description is not None:
                self._values["description"] = description
            if new_version is not None:
                self._values["new_version"] = new_version
            if optional_deployment is not None:
                self._values["optional_deployment"] = optional_deployment
            if update_available is not None:
                self._values["update_available"] = update_available
            if update_status is not None:
                self._values["update_status"] = update_status

        @builtins.property
        def automated_update_date(self) -> typing.Optional[builtins.str]:
            '''The timestamp, in Epoch time, until which you can manually request a service software update.

            After this date, we automatically update your service software.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-automatedupdatedate
            '''
            result = self._values.get("automated_update_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cancellable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True if you're able to cancel your service software version update.

            False if you can't cancel your service software update.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-cancellable
            '''
            result = self._values.get("cancellable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def current_version(self) -> typing.Optional[builtins.str]:
            '''The current service software version present on the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-currentversion
            '''
            result = self._values.get("current_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the service software update status.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def new_version(self) -> typing.Optional[builtins.str]:
            '''The new service software version, if one is available.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-newversion
            '''
            result = self._values.get("new_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def optional_deployment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True if a service software is never automatically updated.

            False if a service software is automatically updated after the automated update date.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-optionaldeployment
            '''
            result = self._values.get("optional_deployment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def update_available(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''True if you're able to update your service software version.

            False if you can't update your service software version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-updateavailable
            '''
            result = self._values.get("update_available")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def update_status(self) -> typing.Optional[builtins.str]:
            '''The status of your service software update.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-updatestatus
            '''
            result = self._values.get("update_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceSoftwareOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.SnapshotOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"automated_snapshot_start_hour": "automatedSnapshotStartHour"},
    )
    class SnapshotOptionsProperty:
        def __init__(
            self,
            *,
            automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''*DEPRECATED* .

            This setting is only relevant to domains running legacy Elasticsearch OSS versions earlier than 5.3. It does not apply to OpenSearch domains.

            The automated snapshot configuration for the OpenSearch Service domain indexes.

            :param automated_snapshot_start_hour: The hour in UTC during which the service takes an automated daily snapshot of the indexes in the OpenSearch Service domain. For example, if you specify 0, OpenSearch Service takes an automated snapshot everyday between midnight and 1 am. You can specify a value between 0 and 23.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-snapshotoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                snapshot_options_property = opensearchservice.CfnDomain.SnapshotOptionsProperty(
                    automated_snapshot_start_hour=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0e13b38afbded71e9992440effb17c3e5088d8154a74ea083ce5557a417d826)
                check_type(argname="argument automated_snapshot_start_hour", value=automated_snapshot_start_hour, expected_type=type_hints["automated_snapshot_start_hour"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automated_snapshot_start_hour is not None:
                self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour

        @builtins.property
        def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
            '''The hour in UTC during which the service takes an automated daily snapshot of the indexes in the OpenSearch Service domain.

            For example, if you specify 0, OpenSearch Service takes an automated snapshot everyday between midnight and 1 am. You can specify a value between 0 and 23.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-snapshotoptions.html#cfn-opensearchservice-domain-snapshotoptions-automatedsnapshotstarthour
            '''
            result = self._values.get("automated_snapshot_start_hour")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapshotOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.SoftwareUpdateOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"auto_software_update_enabled": "autoSoftwareUpdateEnabled"},
    )
    class SoftwareUpdateOptionsProperty:
        def __init__(
            self,
            *,
            auto_software_update_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Options for configuring service software updates for a domain.

            :param auto_software_update_enabled: Specifies whether automatic service software updates are enabled for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-softwareupdateoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                software_update_options_property = opensearchservice.CfnDomain.SoftwareUpdateOptionsProperty(
                    auto_software_update_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__418cf8f4a45cf995c69a66a82c4c6c8187337bc6b21c90e0c4d1e7240268e31f)
                check_type(argname="argument auto_software_update_enabled", value=auto_software_update_enabled, expected_type=type_hints["auto_software_update_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_software_update_enabled is not None:
                self._values["auto_software_update_enabled"] = auto_software_update_enabled

        @builtins.property
        def auto_software_update_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether automatic service software updates are enabled for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-softwareupdateoptions.html#cfn-opensearchservice-domain-softwareupdateoptions-autosoftwareupdateenabled
            '''
            result = self._values.get("auto_software_update_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SoftwareUpdateOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.VPCOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VPCOptionsProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

            For more information, see `Launching your Amazon OpenSearch Service domains using a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param security_group_ids: The list of security group IDs that are associated with the VPC endpoints for the domain. If you don't provide a security group ID, OpenSearch Service uses the default security group for the VPC. To learn more, see `Security groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .
            :param subnet_ids: Provide one subnet ID for each Availability Zone that your domain uses. For example, you must specify three subnet IDs for a three-AZ domain. To learn more, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* . If you specify more than one subnet, you must also configure ``ZoneAwarenessEnabled`` and ``ZoneAwarenessConfig`` within `ClusterConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html>`_ , otherwise you'll see the error "You must specify exactly one subnet" during template creation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                v_pCOptions_property = opensearchservice.CfnDomain.VPCOptionsProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24640fa2d7f598273178d92c1aa2b0796e30785f6245af6073ef634ed918a365)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of security group IDs that are associated with the VPC endpoints for the domain.

            If you don't provide a security group ID, OpenSearch Service uses the default security group for the VPC. To learn more, see `Security groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html#cfn-opensearchservice-domain-vpcoptions-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Provide one subnet ID for each Availability Zone that your domain uses.

            For example, you must specify three subnet IDs for a three-AZ domain. To learn more, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* .

            If you specify more than one subnet, you must also configure ``ZoneAwarenessEnabled`` and ``ZoneAwarenessConfig`` within `ClusterConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html>`_ , otherwise you'll see the error "You must specify exactly one subnet" during template creation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html#cfn-opensearchservice-domain-vpcoptions-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.WindowStartTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"hours": "hours", "minutes": "minutes"},
    )
    class WindowStartTimeProperty:
        def __init__(self, *, hours: jsii.Number, minutes: jsii.Number) -> None:
            '''A custom start time for the off-peak window, in Coordinated Universal Time (UTC).

            The window length will always be 10 hours, so you can't specify an end time. For example, if you specify 11:00 P.M. UTC as a start time, the end time will automatically be set to 9:00 A.M.

            :param hours: The start hour of the window in Coordinated Universal Time (UTC), using 24-hour time. For example, 17 refers to 5:00 P.M. UTC. The minimum value is 0 and the maximum value is 23.
            :param minutes: The start minute of the window, in UTC. The minimum value is 0 and the maximum value is 59.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-windowstarttime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                window_start_time_property = opensearchservice.CfnDomain.WindowStartTimeProperty(
                    hours=123,
                    minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2fa8406ba2a50b91cf259e2b56bf23273c4b98d511a136a5d4286fc6a1877858)
                check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
                check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hours": hours,
                "minutes": minutes,
            }

        @builtins.property
        def hours(self) -> jsii.Number:
            '''The start hour of the window in Coordinated Universal Time (UTC), using 24-hour time.

            For example, 17 refers to 5:00 P.M. UTC. The minimum value is 0 and the maximum value is 23.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-windowstarttime.html#cfn-opensearchservice-domain-windowstarttime-hours
            '''
            result = self._values.get("hours")
            assert result is not None, "Required property 'hours' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def minutes(self) -> jsii.Number:
            '''The start minute of the window, in UTC.

            The minimum value is 0 and the maximum value is 59.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-windowstarttime.html#cfn-opensearchservice-domain-windowstarttime-minutes
            '''
            result = self._values.get("minutes")
            assert result is not None, "Required property 'minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WindowStartTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchservice.CfnDomain.ZoneAwarenessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"availability_zone_count": "availabilityZoneCount"},
    )
    class ZoneAwarenessConfigProperty:
        def __init__(
            self,
            *,
            availability_zone_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies zone awareness configuration options.

            Only use if ``ZoneAwarenessEnabled`` is ``true`` .

            :param availability_zone_count: If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use. Valid values are ``2`` and ``3`` . Default is 2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-zoneawarenessconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchservice as opensearchservice
                
                zone_awareness_config_property = opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                    availability_zone_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__762161cbe51ffd2f00f50f8bcc4e95fb7d9340462d887c4a06d204b10e9f869a)
                check_type(argname="argument availability_zone_count", value=availability_zone_count, expected_type=type_hints["availability_zone_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone_count is not None:
                self._values["availability_zone_count"] = availability_zone_count

        @builtins.property
        def availability_zone_count(self) -> typing.Optional[jsii.Number]:
            '''If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use.

            Valid values are ``2`` and ``3`` . Default is 2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-zoneawarenessconfig.html#cfn-opensearchservice-domain-zoneawarenessconfig-availabilityzonecount
            '''
            result = self._values.get("availability_zone_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZoneAwarenessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "advanced_security_options": "advancedSecurityOptions",
        "cluster_config": "clusterConfig",
        "cognito_options": "cognitoOptions",
        "domain_endpoint_options": "domainEndpointOptions",
        "domain_name": "domainName",
        "ebs_options": "ebsOptions",
        "encryption_at_rest_options": "encryptionAtRestOptions",
        "engine_version": "engineVersion",
        "log_publishing_options": "logPublishingOptions",
        "node_to_node_encryption_options": "nodeToNodeEncryptionOptions",
        "off_peak_window_options": "offPeakWindowOptions",
        "snapshot_options": "snapshotOptions",
        "software_update_options": "softwareUpdateOptions",
        "tags": "tags",
        "vpc_options": "vpcOptions",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        advanced_security_options: typing.Optional[typing.Union[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cluster_config: typing.Optional[typing.Union[typing.Union[CfnDomain.ClusterConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cognito_options: typing.Optional[typing.Union[typing.Union[CfnDomain.CognitoOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        domain_endpoint_options: typing.Optional[typing.Union[typing.Union[CfnDomain.DomainEndpointOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union[typing.Union[CfnDomain.EBSOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        encryption_at_rest_options: typing.Optional[typing.Union[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        log_publishing_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnDomain.LogPublishingOptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        off_peak_window_options: typing.Optional[typing.Union[typing.Union[CfnDomain.OffPeakWindowOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        snapshot_options: typing.Optional[typing.Union[typing.Union[CfnDomain.SnapshotOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        software_update_options: typing.Optional[typing.Union[typing.Union[CfnDomain.SoftwareUpdateOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_options: typing.Optional[typing.Union[typing.Union[CfnDomain.VPCOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDomain``.

        :param access_policies: An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions. For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param advanced_options: Additional options to specify for the OpenSearch Service domain. For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.
        :param advanced_security_options: Specifies options for fine-grained access control and SAML authentication. If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.
        :param cluster_config: Container for the cluster configuration of a domain.
        :param cognito_options: Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.
        :param domain_endpoint_options: Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.
        :param domain_name: A name for the OpenSearch Service domain. The name must have a minimum length of 3 and a maximum length of 28. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . Required when creating a new domain. .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param ebs_options: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param encryption_at_rest_options: Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use. See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .
        :param engine_version: The version of OpenSearch to use. The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* . If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param log_publishing_options: An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish. Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .
        :param node_to_node_encryption_options: Specifies whether node-to-node encryption is enabled. See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .
        :param off_peak_window_options: Options for a domain's off-peak window, during which OpenSearch Service can perform mandatory configuration changes on the domain.
        :param snapshot_options: *DEPRECATED* . The automated snapshot configuration for the OpenSearch Service domain indexes.
        :param software_update_options: Options for configuring service software updates for a domain.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.
        :param vpc_options: The virtual private cloud (VPC) configuration for the OpenSearch Service domain. For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* . If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_opensearchservice as opensearchservice
            
            # access_policies: Any
            
            cfn_domain_props = opensearchservice.CfnDomainProps(
                access_policies=access_policies,
                advanced_options={
                    "advanced_options_key": "advancedOptions"
                },
                advanced_security_options=opensearchservice.CfnDomain.AdvancedSecurityOptionsInputProperty(
                    anonymous_auth_disable_date="anonymousAuthDisableDate",
                    anonymous_auth_enabled=False,
                    enabled=False,
                    internal_user_database_enabled=False,
                    master_user_options=opensearchservice.CfnDomain.MasterUserOptionsProperty(
                        master_user_arn="masterUserArn",
                        master_user_name="masterUserName",
                        master_user_password="masterUserPassword"
                    ),
                    saml_options=opensearchservice.CfnDomain.SAMLOptionsProperty(
                        enabled=False,
                        idp=opensearchservice.CfnDomain.IdpProperty(
                            entity_id="entityId",
                            metadata_content="metadataContent"
                        ),
                        master_backend_role="masterBackendRole",
                        master_user_name="masterUserName",
                        roles_key="rolesKey",
                        session_timeout_minutes=123,
                        subject_key="subjectKey"
                    )
                ),
                cluster_config=opensearchservice.CfnDomain.ClusterConfigProperty(
                    dedicated_master_count=123,
                    dedicated_master_enabled=False,
                    dedicated_master_type="dedicatedMasterType",
                    instance_count=123,
                    instance_type="instanceType",
                    multi_az_with_standby_enabled=False,
                    warm_count=123,
                    warm_enabled=False,
                    warm_type="warmType",
                    zone_awareness_config=opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                        availability_zone_count=123
                    ),
                    zone_awareness_enabled=False
                ),
                cognito_options=opensearchservice.CfnDomain.CognitoOptionsProperty(
                    enabled=False,
                    identity_pool_id="identityPoolId",
                    role_arn="roleArn",
                    user_pool_id="userPoolId"
                ),
                domain_endpoint_options=opensearchservice.CfnDomain.DomainEndpointOptionsProperty(
                    custom_endpoint="customEndpoint",
                    custom_endpoint_certificate_arn="customEndpointCertificateArn",
                    custom_endpoint_enabled=False,
                    enforce_https=False,
                    tls_security_policy="tlsSecurityPolicy"
                ),
                domain_name="domainName",
                ebs_options=opensearchservice.CfnDomain.EBSOptionsProperty(
                    ebs_enabled=False,
                    iops=123,
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                ),
                encryption_at_rest_options=opensearchservice.CfnDomain.EncryptionAtRestOptionsProperty(
                    enabled=False,
                    kms_key_id="kmsKeyId"
                ),
                engine_version="engineVersion",
                log_publishing_options={
                    "log_publishing_options_key": opensearchservice.CfnDomain.LogPublishingOptionProperty(
                        cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                        enabled=False
                    )
                },
                node_to_node_encryption_options=opensearchservice.CfnDomain.NodeToNodeEncryptionOptionsProperty(
                    enabled=False
                ),
                off_peak_window_options=opensearchservice.CfnDomain.OffPeakWindowOptionsProperty(
                    enabled=False,
                    off_peak_window=opensearchservice.CfnDomain.OffPeakWindowProperty(
                        window_start_time=opensearchservice.CfnDomain.WindowStartTimeProperty(
                            hours=123,
                            minutes=123
                        )
                    )
                ),
                snapshot_options=opensearchservice.CfnDomain.SnapshotOptionsProperty(
                    automated_snapshot_start_hour=123
                ),
                software_update_options=opensearchservice.CfnDomain.SoftwareUpdateOptionsProperty(
                    auto_software_update_enabled=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_options=opensearchservice.CfnDomain.VPCOptionsProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07dbf51fa688cc880a99add8bbb7e6ee2599448e85757252353abc406979e52)
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument advanced_options", value=advanced_options, expected_type=type_hints["advanced_options"])
            check_type(argname="argument advanced_security_options", value=advanced_security_options, expected_type=type_hints["advanced_security_options"])
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
            check_type(argname="argument cognito_options", value=cognito_options, expected_type=type_hints["cognito_options"])
            check_type(argname="argument domain_endpoint_options", value=domain_endpoint_options, expected_type=type_hints["domain_endpoint_options"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument ebs_options", value=ebs_options, expected_type=type_hints["ebs_options"])
            check_type(argname="argument encryption_at_rest_options", value=encryption_at_rest_options, expected_type=type_hints["encryption_at_rest_options"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument log_publishing_options", value=log_publishing_options, expected_type=type_hints["log_publishing_options"])
            check_type(argname="argument node_to_node_encryption_options", value=node_to_node_encryption_options, expected_type=type_hints["node_to_node_encryption_options"])
            check_type(argname="argument off_peak_window_options", value=off_peak_window_options, expected_type=type_hints["off_peak_window_options"])
            check_type(argname="argument snapshot_options", value=snapshot_options, expected_type=type_hints["snapshot_options"])
            check_type(argname="argument software_update_options", value=software_update_options, expected_type=type_hints["software_update_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_options", value=vpc_options, expected_type=type_hints["vpc_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if advanced_security_options is not None:
            self._values["advanced_security_options"] = advanced_security_options
        if cluster_config is not None:
            self._values["cluster_config"] = cluster_config
        if cognito_options is not None:
            self._values["cognito_options"] = cognito_options
        if domain_endpoint_options is not None:
            self._values["domain_endpoint_options"] = domain_endpoint_options
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if ebs_options is not None:
            self._values["ebs_options"] = ebs_options
        if encryption_at_rest_options is not None:
            self._values["encryption_at_rest_options"] = encryption_at_rest_options
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if log_publishing_options is not None:
            self._values["log_publishing_options"] = log_publishing_options
        if node_to_node_encryption_options is not None:
            self._values["node_to_node_encryption_options"] = node_to_node_encryption_options
        if off_peak_window_options is not None:
            self._values["off_peak_window_options"] = off_peak_window_options
        if snapshot_options is not None:
            self._values["snapshot_options"] = snapshot_options
        if software_update_options is not None:
            self._values["software_update_options"] = software_update_options
        if tags is not None:
            self._values["tags"] = tags
        if vpc_options is not None:
            self._values["vpc_options"] = vpc_options

    @builtins.property
    def access_policies(self) -> typing.Any:
        '''An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions.

        For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-accesspolicies
        '''
        result = self._values.get("access_policies")
        return typing.cast(typing.Any, result)

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''Additional options to specify for the OpenSearch Service domain.

        For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedoptions
        '''
        result = self._values.get("advanced_options")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, _IResolvable_a771d0ef]]:
        '''Specifies options for fine-grained access control and SAML authentication.

        If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedsecurityoptions
        '''
        result = self._values.get("advanced_security_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cluster_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.ClusterConfigProperty, _IResolvable_a771d0ef]]:
        '''Container for the cluster configuration of a domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-clusterconfig
        '''
        result = self._values.get("cluster_config")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.ClusterConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.CognitoOptionsProperty, _IResolvable_a771d0ef]]:
        '''Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-cognitooptions
        '''
        result = self._values.get("cognito_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.CognitoOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.DomainEndpointOptionsProperty, _IResolvable_a771d0ef]]:
        '''Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainendpointoptions
        '''
        result = self._values.get("domain_endpoint_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.DomainEndpointOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''A name for the OpenSearch Service domain.

        The name must have a minimum length of 3 and a maximum length of 28. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        Required when creating a new domain.
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.EBSOptionsProperty, _IResolvable_a771d0ef]]:
        '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.

        For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-ebsoptions
        '''
        result = self._values.get("ebs_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.EBSOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, _IResolvable_a771d0ef]]:
        '''Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use.

        See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-encryptionatrestoptions
        '''
        result = self._values.get("encryption_at_rest_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of OpenSearch to use.

        The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDomain.LogPublishingOptionProperty, _IResolvable_a771d0ef]]]]:
        '''An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish.

        Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-logpublishingoptions
        '''
        result = self._values.get("log_publishing_options")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDomain.LogPublishingOptionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, _IResolvable_a771d0ef]]:
        '''Specifies whether node-to-node encryption is enabled.

        See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-nodetonodeencryptionoptions
        '''
        result = self._values.get("node_to_node_encryption_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def off_peak_window_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.OffPeakWindowOptionsProperty, _IResolvable_a771d0ef]]:
        '''Options for a domain's off-peak window, during which OpenSearch Service can perform mandatory configuration changes on the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-offpeakwindowoptions
        '''
        result = self._values.get("off_peak_window_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.OffPeakWindowOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.SnapshotOptionsProperty, _IResolvable_a771d0ef]]:
        '''*DEPRECATED* .

        The automated snapshot configuration for the OpenSearch Service domain indexes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-snapshotoptions
        '''
        result = self._values.get("snapshot_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.SnapshotOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def software_update_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.SoftwareUpdateOptionsProperty, _IResolvable_a771d0ef]]:
        '''Options for configuring service software updates for a domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-softwareupdateoptions
        '''
        result = self._values.get("software_update_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.SoftwareUpdateOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.VPCOptionsProperty, _IResolvable_a771d0ef]]:
        '''The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

        For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-vpcoptions
        '''
        result = self._values.get("vpc_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.VPCOptionsProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.CognitoOptions",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_id": "identityPoolId",
        "role": "role",
        "user_pool_id": "userPoolId",
    },
)
class CognitoOptions:
    def __init__(
        self,
        *,
        identity_pool_id: builtins.str,
        role: _IRole_59af6f50,
        user_pool_id: builtins.str,
    ) -> None:
        '''(experimental) Configures Amazon OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :param identity_pool_id: (experimental) The Amazon Cognito identity pool ID that you want Amazon OpenSearch Service to use for OpenSearch Dashboards authentication.
        :param role: (experimental) A role that allows Amazon OpenSearch Service to configure your user pool and identity pool. It must have the ``AmazonESCognitoAccess`` policy attached to it.
        :param user_pool_id: (experimental) The Amazon Cognito user pool ID that you want Amazon OpenSearch Service to use for OpenSearch Dashboards authentication.

        :see: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html
        :stability: experimental
        :exampleMetadata: fixture=migrate-opensearch infused

        Example::

            opensearch.Domain(self, "Domain",
                cognito_dashboards_auth=cdk.aws_opensearchservice.CognitoOptions(
                    identity_pool_id="test-identity-pool-id",
                    user_pool_id="test-user-pool-id",
                    role=role
                ),
                version=open_search_version
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f829660d1eedfd90a45cc128da297e91a3aa6c686079478480083fe86ab063b2)
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_pool_id": identity_pool_id,
            "role": role,
            "user_pool_id": user_pool_id,
        }

    @builtins.property
    def identity_pool_id(self) -> builtins.str:
        '''(experimental) The Amazon Cognito identity pool ID that you want Amazon OpenSearch Service to use for OpenSearch Dashboards authentication.

        :stability: experimental
        '''
        result = self._values.get("identity_pool_id")
        assert result is not None, "Required property 'identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> _IRole_59af6f50:
        '''(experimental) A role that allows Amazon OpenSearch Service to configure your user pool and identity pool.

        It must have the ``AmazonESCognitoAccess`` policy attached to it.

        :see: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html#cognito-auth-prereq
        :stability: experimental
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_IRole_59af6f50, result)

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        '''(experimental) The Amazon Cognito user pool ID that you want Amazon OpenSearch Service to use for OpenSearch Dashboards authentication.

        :stability: experimental
        '''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.CustomEndpointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "certificate": "certificate",
        "hosted_zone": "hostedZone",
    },
)
class CustomEndpointOptions:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        certificate: typing.Optional[_ICertificate_c7bbdc16] = None,
        hosted_zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> None:
        '''(experimental) Configures a custom domain endpoint for the Amazon OpenSearch Service domain.

        :param domain_name: (experimental) The custom domain name to assign.
        :param certificate: (experimental) The certificate to use. Default: - create a new one
        :param hosted_zone: (experimental) The hosted zone in Route53 to create the CNAME record in. Default: - do not create a CNAME

        :stability: experimental
        :exampleMetadata: infused

        Example::

            opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                custom_endpoint=opensearch.aws_opensearchservice.CustomEndpointOptions(
                    domain_name="search.example.com"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2e4c1ed7f16e16882ac275095fc4da795e6c5436e6f7183ef25347e518eb19)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''(experimental) The custom domain name to assign.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[_ICertificate_c7bbdc16]:
        '''(experimental) The certificate to use.

        :default: - create a new one

        :stability: experimental
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_ICertificate_c7bbdc16], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_IHostedZone_78d5a9c9]:
        '''(experimental) The hosted zone in Route53 to create the CNAME record in.

        :default: - do not create a CNAME

        :stability: experimental
        '''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_IHostedZone_78d5a9c9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomEndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.DomainAttributes",
    jsii_struct_bases=[],
    name_mapping={"domain_arn": "domainArn", "domain_endpoint": "domainEndpoint"},
)
class DomainAttributes:
    def __init__(
        self,
        *,
        domain_arn: builtins.str,
        domain_endpoint: builtins.str,
    ) -> None:
        '''(experimental) Reference to an Amazon OpenSearch Service domain.

        :param domain_arn: (experimental) The ARN of the Amazon OpenSearch Service domain.
        :param domain_endpoint: (experimental) The domain endpoint of the Amazon OpenSearch Service domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_opensearchservice as opensearchservice
            
            domain_attributes = opensearchservice.DomainAttributes(
                domain_arn="domainArn",
                domain_endpoint="domainEndpoint"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afb7aa7127d416fcd578f0aad24ea72f95536d6d840f5d7164aa7c6d0b91928)
            check_type(argname="argument domain_arn", value=domain_arn, expected_type=type_hints["domain_arn"])
            check_type(argname="argument domain_endpoint", value=domain_endpoint, expected_type=type_hints["domain_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_arn": domain_arn,
            "domain_endpoint": domain_endpoint,
        }

    @builtins.property
    def domain_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Amazon OpenSearch Service domain.

        :stability: experimental
        '''
        result = self._values.get("domain_arn")
        assert result is not None, "Required property 'domain_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_endpoint(self) -> builtins.str:
        '''(experimental) The domain endpoint of the Amazon OpenSearch Service domain.

        :stability: experimental
        '''
        result = self._values.get("domain_endpoint")
        assert result is not None, "Required property 'domain_endpoint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.DomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "automated_snapshot_start_hour": "automatedSnapshotStartHour",
        "capacity": "capacity",
        "cognito_dashboards_auth": "cognitoDashboardsAuth",
        "custom_endpoint": "customEndpoint",
        "domain_name": "domainName",
        "ebs": "ebs",
        "enable_version_upgrade": "enableVersionUpgrade",
        "encryption_at_rest": "encryptionAtRest",
        "enforce_https": "enforceHttps",
        "fine_grained_access_control": "fineGrainedAccessControl",
        "logging": "logging",
        "node_to_node_encryption": "nodeToNodeEncryption",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "tls_security_policy": "tlsSecurityPolicy",
        "use_unsigned_basic_auth": "useUnsignedBasicAuth",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "zone_awareness": "zoneAwareness",
    },
)
class DomainProps:
    def __init__(
        self,
        *,
        version: "EngineVersion",
        access_policies: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        capacity: typing.Optional[typing.Union[CapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cognito_dashboards_auth: typing.Optional[typing.Union[CognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_endpoint: typing.Optional[typing.Union[CustomEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs: typing.Optional[typing.Union["EbsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_version_upgrade: typing.Optional[builtins.bool] = None,
        encryption_at_rest: typing.Optional[typing.Union["EncryptionAtRestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce_https: typing.Optional[builtins.bool] = None,
        fine_grained_access_control: typing.Optional[typing.Union[AdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union["LoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        node_to_node_encryption: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        tls_security_policy: typing.Optional["TLSSecurityPolicy"] = None,
        use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Sequence[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]]] = None,
        zone_awareness: typing.Optional[typing.Union["ZoneAwarenessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for an Amazon OpenSearch Service domain.

        :param version: (experimental) The Elasticsearch/OpenSearch version that your domain will leverage.
        :param access_policies: (experimental) Domain access policies. Default: - No access policies.
        :param advanced_options: (experimental) Additional options to specify for the Amazon OpenSearch Service domain. Default: - no advanced options are specified
        :param automated_snapshot_start_hour: (experimental) The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon OpenSearch Service domain. Only applies for Elasticsearch versions below 5.3. Default: - Hourly automated snapshots not used
        :param capacity: (experimental) The cluster capacity configuration for the Amazon OpenSearch Service domain. Default: - 1 r5.large.search data node; no dedicated master nodes.
        :param cognito_dashboards_auth: (experimental) Configures Amazon OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards. Default: - Cognito not used for authentication to OpenSearch Dashboards.
        :param custom_endpoint: (experimental) To configure a custom domain configure these options. If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate Default: - no custom domain endpoint will be configured
        :param domain_name: (experimental) Enforces a particular physical domain name. Default: - A name will be auto-generated.
        :param ebs: (experimental) The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon OpenSearch Service domain. Default: - 10 GiB General Purpose (SSD) volumes per node.
        :param enable_version_upgrade: (experimental) To upgrade an Amazon OpenSearch Service domain to a new version, rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy. Default: - false
        :param encryption_at_rest: (experimental) Encryption at rest options for the cluster. Default: - No encryption at rest
        :param enforce_https: (experimental) True to require that all traffic to the domain arrive over HTTPS. Default: - false
        :param fine_grained_access_control: (experimental) Specifies options for fine-grained access control. Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later. Enabling fine-grained access control also requires encryption of data at rest and node-to-node encryption, along with enforced HTTPS. Default: - fine-grained access control is disabled
        :param logging: (experimental) Configuration log publishing configuration options. Default: - No logs are published
        :param node_to_node_encryption: (experimental) Specify true to enable node to node encryption. Requires Elasticsearch version 6.0 or later or OpenSearch version 1.0 or later. Default: - Node to node encryption is not enabled.
        :param removal_policy: (experimental) Policy to apply when the domain is removed from the stack. Default: RemovalPolicy.RETAIN
        :param security_groups: (experimental) The list of security groups that are associated with the VPC endpoints for the domain. Only used if ``vpc`` is specified. Default: - One new security group is created.
        :param tls_security_policy: (experimental) The minimum TLS version required for traffic to the domain. Default: - TLSSecurityPolicy.TLS_1_0
        :param use_unsigned_basic_auth: (experimental) Configures the domain so that unsigned basic auth is enabled. If no master user is provided a default master user with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved by getting ``masterUserPassword`` from the domain instance. Setting this to true will also add an access policy that allows unsigned access, enable node to node encryption, encryption at rest. If conflicting settings are encountered (like disabling encryption at rest) enabling this setting will cause a failure. Default: - false
        :param vpc: (experimental) Place the domain inside this VPC. Default: - Domain is not placed in a VPC.
        :param vpc_subnets: (experimental) The specific vpc subnets the domain will be placed in. You must provide one subnet for each Availability Zone that your domain uses. For example, you must specify three subnet IDs for a three Availability Zone domain. Only used if ``vpc`` is specified. Default: - All private subnets.
        :param zone_awareness: (experimental) The cluster zone awareness configuration for the Amazon OpenSearch Service domain. Default: - no zone awareness (1 AZ)

        :stability: experimental
        :exampleMetadata: infused

        Example::

            domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                ebs=opensearch.aws_opensearchservice.EbsOptions(
                    volume_size=100,
                    volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
                ),
                node_to_node_encryption=True,
                encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(
                    enabled=True
                )
            )
        '''
        if isinstance(capacity, dict):
            capacity = CapacityConfig(**capacity)
        if isinstance(cognito_dashboards_auth, dict):
            cognito_dashboards_auth = CognitoOptions(**cognito_dashboards_auth)
        if isinstance(custom_endpoint, dict):
            custom_endpoint = CustomEndpointOptions(**custom_endpoint)
        if isinstance(ebs, dict):
            ebs = EbsOptions(**ebs)
        if isinstance(encryption_at_rest, dict):
            encryption_at_rest = EncryptionAtRestOptions(**encryption_at_rest)
        if isinstance(fine_grained_access_control, dict):
            fine_grained_access_control = AdvancedSecurityOptions(**fine_grained_access_control)
        if isinstance(logging, dict):
            logging = LoggingOptions(**logging)
        if isinstance(zone_awareness, dict):
            zone_awareness = ZoneAwarenessConfig(**zone_awareness)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daeaf001a77450352e8b108e87166dd340e72ae24394e56c4cd351f35b8e1962)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument advanced_options", value=advanced_options, expected_type=type_hints["advanced_options"])
            check_type(argname="argument automated_snapshot_start_hour", value=automated_snapshot_start_hour, expected_type=type_hints["automated_snapshot_start_hour"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument cognito_dashboards_auth", value=cognito_dashboards_auth, expected_type=type_hints["cognito_dashboards_auth"])
            check_type(argname="argument custom_endpoint", value=custom_endpoint, expected_type=type_hints["custom_endpoint"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
            check_type(argname="argument enable_version_upgrade", value=enable_version_upgrade, expected_type=type_hints["enable_version_upgrade"])
            check_type(argname="argument encryption_at_rest", value=encryption_at_rest, expected_type=type_hints["encryption_at_rest"])
            check_type(argname="argument enforce_https", value=enforce_https, expected_type=type_hints["enforce_https"])
            check_type(argname="argument fine_grained_access_control", value=fine_grained_access_control, expected_type=type_hints["fine_grained_access_control"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument node_to_node_encryption", value=node_to_node_encryption, expected_type=type_hints["node_to_node_encryption"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tls_security_policy", value=tls_security_policy, expected_type=type_hints["tls_security_policy"])
            check_type(argname="argument use_unsigned_basic_auth", value=use_unsigned_basic_auth, expected_type=type_hints["use_unsigned_basic_auth"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument zone_awareness", value=zone_awareness, expected_type=type_hints["zone_awareness"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if automated_snapshot_start_hour is not None:
            self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour
        if capacity is not None:
            self._values["capacity"] = capacity
        if cognito_dashboards_auth is not None:
            self._values["cognito_dashboards_auth"] = cognito_dashboards_auth
        if custom_endpoint is not None:
            self._values["custom_endpoint"] = custom_endpoint
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if ebs is not None:
            self._values["ebs"] = ebs
        if enable_version_upgrade is not None:
            self._values["enable_version_upgrade"] = enable_version_upgrade
        if encryption_at_rest is not None:
            self._values["encryption_at_rest"] = encryption_at_rest
        if enforce_https is not None:
            self._values["enforce_https"] = enforce_https
        if fine_grained_access_control is not None:
            self._values["fine_grained_access_control"] = fine_grained_access_control
        if logging is not None:
            self._values["logging"] = logging
        if node_to_node_encryption is not None:
            self._values["node_to_node_encryption"] = node_to_node_encryption
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tls_security_policy is not None:
            self._values["tls_security_policy"] = tls_security_policy
        if use_unsigned_basic_auth is not None:
            self._values["use_unsigned_basic_auth"] = use_unsigned_basic_auth
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if zone_awareness is not None:
            self._values["zone_awareness"] = zone_awareness

    @builtins.property
    def version(self) -> "EngineVersion":
        '''(experimental) The Elasticsearch/OpenSearch version that your domain will leverage.

        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast("EngineVersion", result)

    @builtins.property
    def access_policies(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Domain access policies.

        :default: - No access policies.

        :stability: experimental
        '''
        result = self._values.get("access_policies")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional options to specify for the Amazon OpenSearch Service domain.

        :default: - no advanced options are specified

        :see: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html#createdomain-configure-advanced-options
        :stability: experimental
        '''
        result = self._values.get("advanced_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon OpenSearch Service domain.

        Only applies for Elasticsearch versions
        below 5.3.

        :default: - Hourly automated snapshots not used

        :stability: experimental
        '''
        result = self._values.get("automated_snapshot_start_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def capacity(self) -> typing.Optional[CapacityConfig]:
        '''(experimental) The cluster capacity configuration for the Amazon OpenSearch Service domain.

        :default: - 1 r5.large.search data node; no dedicated master nodes.

        :stability: experimental
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[CapacityConfig], result)

    @builtins.property
    def cognito_dashboards_auth(self) -> typing.Optional[CognitoOptions]:
        '''(experimental) Configures Amazon OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :default: - Cognito not used for authentication to OpenSearch Dashboards.

        :stability: experimental
        '''
        result = self._values.get("cognito_dashboards_auth")
        return typing.cast(typing.Optional[CognitoOptions], result)

    @builtins.property
    def custom_endpoint(self) -> typing.Optional[CustomEndpointOptions]:
        '''(experimental) To configure a custom domain configure these options.

        If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate

        :default: - no custom domain endpoint will be configured

        :stability: experimental
        '''
        result = self._values.get("custom_endpoint")
        return typing.cast(typing.Optional[CustomEndpointOptions], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Enforces a particular physical domain name.

        :default: - A name will be auto-generated.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs(self) -> typing.Optional["EbsOptions"]:
        '''(experimental) The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon OpenSearch Service domain.

        :default: - 10 GiB General Purpose (SSD) volumes per node.

        :stability: experimental
        '''
        result = self._values.get("ebs")
        return typing.cast(typing.Optional["EbsOptions"], result)

    @builtins.property
    def enable_version_upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) To upgrade an Amazon OpenSearch Service domain to a new version, rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy.

        :default: - false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain
        :stability: experimental
        '''
        result = self._values.get("enable_version_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_at_rest(self) -> typing.Optional["EncryptionAtRestOptions"]:
        '''(experimental) Encryption at rest options for the cluster.

        :default: - No encryption at rest

        :stability: experimental
        '''
        result = self._values.get("encryption_at_rest")
        return typing.cast(typing.Optional["EncryptionAtRestOptions"], result)

    @builtins.property
    def enforce_https(self) -> typing.Optional[builtins.bool]:
        '''(experimental) True to require that all traffic to the domain arrive over HTTPS.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("enforce_https")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fine_grained_access_control(self) -> typing.Optional[AdvancedSecurityOptions]:
        '''(experimental) Specifies options for fine-grained access control.

        Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later. Enabling fine-grained access control
        also requires encryption of data at rest and node-to-node encryption, along with
        enforced HTTPS.

        :default: - fine-grained access control is disabled

        :stability: experimental
        '''
        result = self._values.get("fine_grained_access_control")
        return typing.cast(typing.Optional[AdvancedSecurityOptions], result)

    @builtins.property
    def logging(self) -> typing.Optional["LoggingOptions"]:
        '''(experimental) Configuration log publishing configuration options.

        :default: - No logs are published

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["LoggingOptions"], result)

    @builtins.property
    def node_to_node_encryption(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify true to enable node to node encryption.

        Requires Elasticsearch version 6.0 or later or OpenSearch version 1.0 or later.

        :default: - Node to node encryption is not enabled.

        :stability: experimental
        '''
        result = self._values.get("node_to_node_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Policy to apply when the domain is removed from the stack.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) The list of security groups that are associated with the VPC endpoints for the domain.

        Only used if ``vpc`` is specified.

        :default: - One new security group is created.

        :see: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def tls_security_policy(self) -> typing.Optional["TLSSecurityPolicy"]:
        '''(experimental) The minimum TLS version required for traffic to the domain.

        :default: - TLSSecurityPolicy.TLS_1_0

        :stability: experimental
        '''
        result = self._values.get("tls_security_policy")
        return typing.cast(typing.Optional["TLSSecurityPolicy"], result)

    @builtins.property
    def use_unsigned_basic_auth(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Configures the domain so that unsigned basic auth is enabled.

        If no master user is provided a default master user
        with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved
        by getting ``masterUserPassword`` from the domain instance.

        Setting this to true will also add an access policy that allows unsigned
        access, enable node to node encryption, encryption at rest. If conflicting
        settings are encountered (like disabling encryption at rest) enabling this
        setting will cause a failure.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("use_unsigned_basic_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) Place the domain inside this VPC.

        :default: - Domain is not placed in a VPC.

        :see: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html
        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[_SubnetSelection_1284e62c]]:
        '''(experimental) The specific vpc subnets the domain will be placed in.

        You must provide one subnet for each Availability Zone
        that your domain uses. For example, you must specify three subnet IDs for a three Availability Zone
        domain.

        Only used if ``vpc`` is specified.

        :default: - All private subnets.

        :see: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html
        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[typing.List[_SubnetSelection_1284e62c]], result)

    @builtins.property
    def zone_awareness(self) -> typing.Optional["ZoneAwarenessConfig"]:
        '''(experimental) The cluster zone awareness configuration for the Amazon OpenSearch Service domain.

        :default: - no zone awareness (1 AZ)

        :stability: experimental
        '''
        result = self._values.get("zone_awareness")
        return typing.cast(typing.Optional["ZoneAwarenessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.EbsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "iops": "iops",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class EbsOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[_EbsDeviceVolumeType_3b8e2d6d] = None,
    ) -> None:
        '''(experimental) The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon OpenSearch Service domain.

        For more information, see
        [Amazon EBS]
        (https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html)
        in the Amazon Elastic Compute Cloud Developer Guide.

        :param enabled: (experimental) Specifies whether Amazon EBS volumes are attached to data nodes in the Amazon OpenSearch Service domain. Default: - true
        :param iops: (experimental) The number of I/O operations per second (IOPS) that the volume supports. This property applies only to the Provisioned IOPS (SSD) EBS volume type. Default: - iops are not set.
        :param volume_size: (experimental) The size (in GiB) of the EBS volume for each data node. The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For valid values, see [EBS volume size limits] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource) in the Amazon OpenSearch Service Developer Guide. Default: 10
        :param volume_type: (experimental) The EBS volume type to use with the Amazon OpenSearch Service domain, such as standard, gp2, io1. Default: gp2

        :stability: experimental
        :exampleMetadata: infused

        Example::

            prod_domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                capacity=opensearch.aws_opensearchservice.CapacityConfig(
                    master_nodes=5,
                    data_nodes=20
                ),
                ebs=opensearch.aws_opensearchservice.EbsOptions(
                    volume_size=20
                ),
                zone_awareness=opensearch.aws_opensearchservice.ZoneAwarenessConfig(
                    availability_zone_count=3
                ),
                logging=opensearch.aws_opensearchservice.LoggingOptions(
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2867398f24c82c172a65efbed19b43310142877212a9e05d5eb51427aefb7d0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if iops is not None:
            self._values["iops"] = iops
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether Amazon EBS volumes are attached to data nodes in the Amazon OpenSearch Service domain.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of I/O operations per second (IOPS) that the volume supports.

        This property applies only to the Provisioned IOPS (SSD) EBS
        volume type.

        :default: - iops are not set.

        :stability: experimental
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size (in GiB) of the EBS volume for each data node.

        The minimum and
        maximum size of an EBS volume depends on the EBS volume type and the
        instance type to which it is attached.  For  valid values, see
        [EBS volume size limits]
        (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource)
        in the Amazon OpenSearch Service Developer Guide.

        :default: 10

        :stability: experimental
        '''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[_EbsDeviceVolumeType_3b8e2d6d]:
        '''(experimental) The EBS volume type to use with the Amazon OpenSearch Service domain, such as standard, gp2, io1.

        :default: gp2

        :stability: experimental
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[_EbsDeviceVolumeType_3b8e2d6d], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EbsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.EncryptionAtRestOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "kms_key": "kmsKey"},
)
class EncryptionAtRestOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
    ) -> None:
        '''(experimental) Whether the domain should encrypt data at rest, and if so, the AWS Key Management Service (KMS) key to use.

        Can only be used to create a new domain,
        not update an existing one. Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later.

        :param enabled: (experimental) Specify true to enable encryption at rest. Default: - encryption at rest is disabled.
        :param kms_key: (experimental) Supply if using KMS key for encryption at rest. Default: - uses default aws/es KMS key.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                enforce_https=True,
                node_to_node_encryption=True,
                encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(
                    enabled=True
                ),
                fine_grained_access_control=opensearch.aws_opensearchservice.AdvancedSecurityOptions(
                    master_user_name="master-user"
                ),
                logging=opensearch.aws_opensearchservice.LoggingOptions(
                    audit_log_enabled=True,
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5529bae98926c37013e7a351dce2b46c3a55cf1d7979d3f2465253b4a770f0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify true to enable encryption at rest.

        :default: - encryption at rest is disabled.

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Supply if using KMS key for encryption at rest.

        :default: - uses default aws/es KMS key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptionAtRestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_opensearchservice.EngineVersion",
):
    '''(experimental) OpenSearch version.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        domain = opensearch.Domain(self, "Domain",
            version=opensearch.EngineVersion.OPENSEARCH_1_0,
            ebs=opensearch.aws_opensearchservice.EbsOptions(
                volume_size=100,
                volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
            ),
            node_to_node_encryption=True,
            encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(
                enabled=True
            )
        )
    '''

    @jsii.member(jsii_name="elasticsearch")
    @builtins.classmethod
    def elasticsearch(cls, version: builtins.str) -> "EngineVersion":
        '''(experimental) Custom ElasticSearch version.

        :param version: custom version number.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2435ed2013b571bc41441375c2f09c9d2d3adb281ef6f54642f04470e68e46f8)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("EngineVersion", jsii.sinvoke(cls, "elasticsearch", [version]))

    @jsii.member(jsii_name="openSearch")
    @builtins.classmethod
    def open_search(cls, version: builtins.str) -> "EngineVersion":
        '''(experimental) Custom OpenSearch version.

        :param version: custom version number.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1025f8cc72d6a22885bd8484f72977e0c773e119480df469eb6d4bf624927da)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("EngineVersion", jsii.sinvoke(cls, "openSearch", [version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_1_5")
    def ELASTICSEARCH_1_5(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 1.5.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_1_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_2_3")
    def ELASTICSEARCH_2_3(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 2.3.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_2_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_5_1")
    def ELASTICSEARCH_5_1(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 5.1.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_5_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_5_3")
    def ELASTICSEARCH_5_3(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 5.3.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_5_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_5_5")
    def ELASTICSEARCH_5_5(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 5.5.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_5_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_5_6")
    def ELASTICSEARCH_5_6(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 5.6.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_5_6"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_0")
    def ELASTICSEARCH_6_0(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 6.0.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_2")
    def ELASTICSEARCH_6_2(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 6.2.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_3")
    def ELASTICSEARCH_6_3(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 6.3.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_4")
    def ELASTICSEARCH_6_4(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 6.4.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_5")
    def ELASTICSEARCH_6_5(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 6.5.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_7")
    def ELASTICSEARCH_6_7(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 6.7.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_7"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_8")
    def ELASTICSEARCH_6_8(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 6.8.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_8"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_1")
    def ELASTICSEARCH_7_1(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 7.1.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_10")
    def ELASTICSEARCH_7_10(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 7.10.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_10"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_4")
    def ELASTICSEARCH_7_4(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 7.4.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_7")
    def ELASTICSEARCH_7_7(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 7.7.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_7"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_8")
    def ELASTICSEARCH_7_8(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 7.8.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_8"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_9")
    def ELASTICSEARCH_7_9(cls) -> "EngineVersion":
        '''(experimental) AWS Elasticsearch 7.9.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_9"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENSEARCH_1_0")
    def OPENSEARCH_1_0(cls) -> "EngineVersion":
        '''(experimental) AWS OpenSearch 1.0.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "OPENSEARCH_1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENSEARCH_1_1")
    def OPENSEARCH_1_1(cls) -> "EngineVersion":
        '''(experimental) AWS OpenSearch 1.1.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "OPENSEARCH_1_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENSEARCH_1_2")
    def OPENSEARCH_1_2(cls) -> "EngineVersion":
        '''(experimental) AWS OpenSearch 1.2.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "OPENSEARCH_1_2"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) engine version identifier.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.interface(jsii_type="monocdk.aws_opensearchservice.IDomain")
class IDomain(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) An interface that represents an Amazon OpenSearch Service domain - either created with the CDK, or an existing one.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''(experimental) Arn of the Amazon OpenSearch Service domain.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''(experimental) Endpoint of the Amazon OpenSearch Service domain.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''(experimental) Identifier of the Amazon OpenSearch Service domain.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) Domain name of the Amazon OpenSearch Service domain.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

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
        '''(experimental) Return the given named metric for this domain.

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

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
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
        '''(experimental) Metric for automated snapshot failures.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricClusterIndexWritesBlocked")
    def metric_cluster_index_writes_blocked(
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
        '''(experimental) Metric for the cluster blocking index writes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
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
        '''(experimental) Metric for the time the cluster status is red.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
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
        '''(experimental) Metric for the time the cluster status is yellow.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        '''(experimental) Metric for CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        '''(experimental) Metric for the storage space of nodes in the cluster.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
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
        '''(experimental) Metric for indexing latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
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
        '''(experimental) Metric for JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
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
        '''(experimental) Metric for KMS key errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
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
        '''(experimental) Metric for KMS key being inaccessible.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
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
        '''(experimental) Metric for master CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
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
        '''(experimental) Metric for master JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
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
        '''(experimental) Metric for the number of nodes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
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
        '''(experimental) Metric for number of searchable documents.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
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
        '''(experimental) Metric for search latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

        :stability: experimental
        '''
        ...


class _IDomainProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) An interface that represents an Amazon OpenSearch Service domain - either created with the CDK, or an existing one.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_opensearchservice.IDomain"

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''(experimental) Arn of the Amazon OpenSearch Service domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''(experimental) Endpoint of the Amazon OpenSearch Service domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''(experimental) Identifier of the Amazon OpenSearch Service domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) Domain name of the Amazon OpenSearch Service domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ac8b364180aed741fa552bc1ad508380069ff006826f61dc143f7a6ba6ee23)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexRead", [index, identity]))

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a718660225a53424dfc32fa6ee2e93fc6d62bf499db8c8727c46ef8a0dac0c41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexReadWrite", [index, identity]))

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52125dd7a4f63f4db9a1aeca99dea1e1e624935e32bd8d4f091c94ce0b1eb1d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexWrite", [index, identity]))

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14368fbd624409aa8ec7fcb7c7124413793ae9dbbe1adba49c3b96e31efa97b4)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathRead", [path, identity]))

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095ae95840f33445e3f21a890841dda95f03dbfe517af54a54cc70397f65d115)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathReadWrite", [path, identity]))

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d06a58aeb59ff6522c081e0c564b1b904546c0241edd13bbaaa6a5db4fcbe8d)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathWrite", [path, identity]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c699384919e8404887ce2d952b3ba08c62a05a446b6c02ed022793bba47a815)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b4d09d33c78547a77b6dcf962ce7c588f728d509027e762d79c9b512731238)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWrite", [identity]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91db7dbc79871f47fc4e518d203372aa2bf37e469067749e81348f8f0f9a9279)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [identity]))

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
        '''(experimental) Return the given named metric for this domain.

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
            type_hints = typing.get_type_hints(_typecheckingstub__1ef034ee3ea6c3d782e7e1ccbeba0a4b8a220070b58e66c0d47fcfdb2f6a5846)
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

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
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
        '''(experimental) Metric for automated snapshot failures.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricAutomatedSnapshotFailure", [props]))

    @jsii.member(jsii_name="metricClusterIndexWritesBlocked")
    def metric_cluster_index_writes_blocked(
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
        '''(experimental) Metric for the cluster blocking index writes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterIndexWritesBlocked", [props]))

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
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
        '''(experimental) Metric for the time the cluster status is red.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterStatusRed", [props]))

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
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
        '''(experimental) Metric for the time the cluster status is yellow.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterStatusYellow", [props]))

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        '''(experimental) Metric for CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricCPUUtilization", [props]))

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        '''(experimental) Metric for the storage space of nodes in the cluster.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFreeStorageSpace", [props]))

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
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
        '''(experimental) Metric for indexing latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricIndexingLatency", [props]))

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
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
        '''(experimental) Metric for JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
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
        '''(experimental) Metric for KMS key errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricKMSKeyError", [props]))

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
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
        '''(experimental) Metric for KMS key being inaccessible.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricKMSKeyInaccessible", [props]))

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
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
        '''(experimental) Metric for master CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricMasterCPUUtilization", [props]))

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
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
        '''(experimental) Metric for master JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricMasterJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
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
        '''(experimental) Metric for the number of nodes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNodes", [props]))

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
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
        '''(experimental) Metric for number of searchable documents.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSearchableDocuments", [props]))

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
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
        '''(experimental) Metric for search latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSearchLatency", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDomain).__jsii_proxy_class__ = lambda : _IDomainProxy


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.LoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "app_log_enabled": "appLogEnabled",
        "app_log_group": "appLogGroup",
        "audit_log_enabled": "auditLogEnabled",
        "audit_log_group": "auditLogGroup",
        "slow_index_log_enabled": "slowIndexLogEnabled",
        "slow_index_log_group": "slowIndexLogGroup",
        "slow_search_log_enabled": "slowSearchLogEnabled",
        "slow_search_log_group": "slowSearchLogGroup",
    },
)
class LoggingOptions:
    def __init__(
        self,
        *,
        app_log_enabled: typing.Optional[builtins.bool] = None,
        app_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
        audit_log_enabled: typing.Optional[builtins.bool] = None,
        audit_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
        slow_index_log_enabled: typing.Optional[builtins.bool] = None,
        slow_index_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
        slow_search_log_enabled: typing.Optional[builtins.bool] = None,
        slow_search_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
    ) -> None:
        '''(experimental) Configures log settings for the domain.

        :param app_log_enabled: (experimental) Specify if Amazon OpenSearch Service application logging should be set up. Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later. Default: - false
        :param app_log_group: (experimental) Log Amazon OpenSearch Service application logs to this log group. Default: - a new log group is created if app logging is enabled
        :param audit_log_enabled: (experimental) Specify if Amazon OpenSearch Service audit logging should be set up. Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later and fine grained access control to be enabled. Default: - false
        :param audit_log_group: (experimental) Log Amazon OpenSearch Service audit logs to this log group. Default: - a new log group is created if audit logging is enabled
        :param slow_index_log_enabled: (experimental) Specify if slow index logging should be set up. Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later. Default: - false
        :param slow_index_log_group: (experimental) Log slow indices to this log group. Default: - a new log group is created if slow index logging is enabled
        :param slow_search_log_enabled: (experimental) Specify if slow search logging should be set up. Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later. Default: - false
        :param slow_search_log_group: (experimental) Log slow searches to this log group. Default: - a new log group is created if slow search logging is enabled

        :stability: experimental
        :exampleMetadata: infused

        Example::

            prod_domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                capacity=opensearch.aws_opensearchservice.CapacityConfig(
                    master_nodes=5,
                    data_nodes=20
                ),
                ebs=opensearch.aws_opensearchservice.EbsOptions(
                    volume_size=20
                ),
                zone_awareness=opensearch.aws_opensearchservice.ZoneAwarenessConfig(
                    availability_zone_count=3
                ),
                logging=opensearch.aws_opensearchservice.LoggingOptions(
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec91e0267db0b7900bddb74654a0434a14cf9302e27aaeaeb88ef794a11e97c5)
            check_type(argname="argument app_log_enabled", value=app_log_enabled, expected_type=type_hints["app_log_enabled"])
            check_type(argname="argument app_log_group", value=app_log_group, expected_type=type_hints["app_log_group"])
            check_type(argname="argument audit_log_enabled", value=audit_log_enabled, expected_type=type_hints["audit_log_enabled"])
            check_type(argname="argument audit_log_group", value=audit_log_group, expected_type=type_hints["audit_log_group"])
            check_type(argname="argument slow_index_log_enabled", value=slow_index_log_enabled, expected_type=type_hints["slow_index_log_enabled"])
            check_type(argname="argument slow_index_log_group", value=slow_index_log_group, expected_type=type_hints["slow_index_log_group"])
            check_type(argname="argument slow_search_log_enabled", value=slow_search_log_enabled, expected_type=type_hints["slow_search_log_enabled"])
            check_type(argname="argument slow_search_log_group", value=slow_search_log_group, expected_type=type_hints["slow_search_log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_log_enabled is not None:
            self._values["app_log_enabled"] = app_log_enabled
        if app_log_group is not None:
            self._values["app_log_group"] = app_log_group
        if audit_log_enabled is not None:
            self._values["audit_log_enabled"] = audit_log_enabled
        if audit_log_group is not None:
            self._values["audit_log_group"] = audit_log_group
        if slow_index_log_enabled is not None:
            self._values["slow_index_log_enabled"] = slow_index_log_enabled
        if slow_index_log_group is not None:
            self._values["slow_index_log_group"] = slow_index_log_group
        if slow_search_log_enabled is not None:
            self._values["slow_search_log_enabled"] = slow_search_log_enabled
        if slow_search_log_group is not None:
            self._values["slow_search_log_group"] = slow_search_log_group

    @builtins.property
    def app_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify if Amazon OpenSearch Service application logging should be set up.

        Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("app_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def app_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log Amazon OpenSearch Service application logs to this log group.

        :default: - a new log group is created if app logging is enabled

        :stability: experimental
        '''
        result = self._values.get("app_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    @builtins.property
    def audit_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify if Amazon OpenSearch Service audit logging should be set up.

        Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later and fine grained access control to be enabled.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("audit_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def audit_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log Amazon OpenSearch Service audit logs to this log group.

        :default: - a new log group is created if audit logging is enabled

        :stability: experimental
        '''
        result = self._values.get("audit_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    @builtins.property
    def slow_index_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify if slow index logging should be set up.

        Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("slow_index_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def slow_index_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log slow indices to this log group.

        :default: - a new log group is created if slow index logging is enabled

        :stability: experimental
        '''
        result = self._values.get("slow_index_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    @builtins.property
    def slow_search_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify if slow search logging should be set up.

        Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("slow_search_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def slow_search_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log slow searches to this log group.

        :default: - a new log group is created if slow search logging is enabled

        :stability: experimental
        '''
        result = self._values.get("slow_search_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_opensearchservice.TLSSecurityPolicy")
class TLSSecurityPolicy(enum.Enum):
    '''(experimental) The minimum TLS version required for traffic to the domain.

    :stability: experimental
    '''

    TLS_1_0 = "TLS_1_0"
    '''(experimental) Cipher suite TLS 1.0.

    :stability: experimental
    '''
    TLS_1_2 = "TLS_1_2"
    '''(experimental) Cipher suite TLS 1.2.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchservice.ZoneAwarenessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone_count": "availabilityZoneCount",
        "enabled": "enabled",
    },
)
class ZoneAwarenessConfig:
    def __init__(
        self,
        *,
        availability_zone_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Specifies zone awareness configuration options.

        :param availability_zone_count: (experimental) If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use. Valid values are 2 and 3. Default: - 2 if zone awareness is enabled.
        :param enabled: (experimental) Indicates whether to enable zone awareness for the Amazon OpenSearch Service domain. When you enable zone awareness, Amazon OpenSearch Service allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see [Configuring a Multi-AZ Domain] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html) in the Amazon OpenSearch Service Developer Guide. Default: - false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            prod_domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                capacity=opensearch.aws_opensearchservice.CapacityConfig(
                    master_nodes=5,
                    data_nodes=20
                ),
                ebs=opensearch.aws_opensearchservice.EbsOptions(
                    volume_size=20
                ),
                zone_awareness=opensearch.aws_opensearchservice.ZoneAwarenessConfig(
                    availability_zone_count=3
                ),
                logging=opensearch.aws_opensearchservice.LoggingOptions(
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0df4125eb09c26b8aef9a66bce9124980882b7b18ee277b1344ef0c0a101bb0)
            check_type(argname="argument availability_zone_count", value=availability_zone_count, expected_type=type_hints["availability_zone_count"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone_count is not None:
            self._values["availability_zone_count"] = availability_zone_count
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def availability_zone_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use.

        Valid values are 2 and 3.

        :default: - 2 if zone awareness is enabled.

        :stability: experimental
        '''
        result = self._values.get("availability_zone_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether to enable zone awareness for the Amazon OpenSearch Service domain.

        When you enable zone awareness, Amazon OpenSearch Service allocates the nodes and replica
        index shards that belong to a cluster across two Availability Zones (AZs)
        in the same region to prevent data loss and minimize downtime in the event
        of node or data center failure. Don't enable zone awareness if your cluster
        has no replica index shards or is a single-node cluster. For more information,
        see [Configuring a Multi-AZ Domain]
        (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html)
        in the Amazon OpenSearch Service Developer Guide.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneAwarenessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDomain, _IConnectable_c1c0e72c)
class Domain(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_opensearchservice.Domain",
):
    '''(experimental) Provides an Amazon OpenSearch Service domain.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        domain = opensearch.Domain(self, "Domain",
            version=opensearch.EngineVersion.OPENSEARCH_1_0,
            ebs=opensearch.aws_opensearchservice.EbsOptions(
                volume_size=100,
                volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
            ),
            node_to_node_encryption=True,
            encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(
                enabled=True
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        version: EngineVersion,
        access_policies: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        capacity: typing.Optional[typing.Union[CapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cognito_dashboards_auth: typing.Optional[typing.Union[CognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_endpoint: typing.Optional[typing.Union[CustomEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs: typing.Optional[typing.Union[EbsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        enable_version_upgrade: typing.Optional[builtins.bool] = None,
        encryption_at_rest: typing.Optional[typing.Union[EncryptionAtRestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        enforce_https: typing.Optional[builtins.bool] = None,
        fine_grained_access_control: typing.Optional[typing.Union[AdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[LoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        node_to_node_encryption: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        tls_security_policy: typing.Optional[TLSSecurityPolicy] = None,
        use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Sequence[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]]] = None,
        zone_awareness: typing.Optional[typing.Union[ZoneAwarenessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: (experimental) The Elasticsearch/OpenSearch version that your domain will leverage.
        :param access_policies: (experimental) Domain access policies. Default: - No access policies.
        :param advanced_options: (experimental) Additional options to specify for the Amazon OpenSearch Service domain. Default: - no advanced options are specified
        :param automated_snapshot_start_hour: (experimental) The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon OpenSearch Service domain. Only applies for Elasticsearch versions below 5.3. Default: - Hourly automated snapshots not used
        :param capacity: (experimental) The cluster capacity configuration for the Amazon OpenSearch Service domain. Default: - 1 r5.large.search data node; no dedicated master nodes.
        :param cognito_dashboards_auth: (experimental) Configures Amazon OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards. Default: - Cognito not used for authentication to OpenSearch Dashboards.
        :param custom_endpoint: (experimental) To configure a custom domain configure these options. If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate Default: - no custom domain endpoint will be configured
        :param domain_name: (experimental) Enforces a particular physical domain name. Default: - A name will be auto-generated.
        :param ebs: (experimental) The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon OpenSearch Service domain. Default: - 10 GiB General Purpose (SSD) volumes per node.
        :param enable_version_upgrade: (experimental) To upgrade an Amazon OpenSearch Service domain to a new version, rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy. Default: - false
        :param encryption_at_rest: (experimental) Encryption at rest options for the cluster. Default: - No encryption at rest
        :param enforce_https: (experimental) True to require that all traffic to the domain arrive over HTTPS. Default: - false
        :param fine_grained_access_control: (experimental) Specifies options for fine-grained access control. Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later. Enabling fine-grained access control also requires encryption of data at rest and node-to-node encryption, along with enforced HTTPS. Default: - fine-grained access control is disabled
        :param logging: (experimental) Configuration log publishing configuration options. Default: - No logs are published
        :param node_to_node_encryption: (experimental) Specify true to enable node to node encryption. Requires Elasticsearch version 6.0 or later or OpenSearch version 1.0 or later. Default: - Node to node encryption is not enabled.
        :param removal_policy: (experimental) Policy to apply when the domain is removed from the stack. Default: RemovalPolicy.RETAIN
        :param security_groups: (experimental) The list of security groups that are associated with the VPC endpoints for the domain. Only used if ``vpc`` is specified. Default: - One new security group is created.
        :param tls_security_policy: (experimental) The minimum TLS version required for traffic to the domain. Default: - TLSSecurityPolicy.TLS_1_0
        :param use_unsigned_basic_auth: (experimental) Configures the domain so that unsigned basic auth is enabled. If no master user is provided a default master user with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved by getting ``masterUserPassword`` from the domain instance. Setting this to true will also add an access policy that allows unsigned access, enable node to node encryption, encryption at rest. If conflicting settings are encountered (like disabling encryption at rest) enabling this setting will cause a failure. Default: - false
        :param vpc: (experimental) Place the domain inside this VPC. Default: - Domain is not placed in a VPC.
        :param vpc_subnets: (experimental) The specific vpc subnets the domain will be placed in. You must provide one subnet for each Availability Zone that your domain uses. For example, you must specify three subnet IDs for a three Availability Zone domain. Only used if ``vpc`` is specified. Default: - All private subnets.
        :param zone_awareness: (experimental) The cluster zone awareness configuration for the Amazon OpenSearch Service domain. Default: - no zone awareness (1 AZ)

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ce6156206ad90ca05817dbc08bf54fd8366f0a0a4b4e623ba3c00466bf9093)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DomainProps(
            version=version,
            access_policies=access_policies,
            advanced_options=advanced_options,
            automated_snapshot_start_hour=automated_snapshot_start_hour,
            capacity=capacity,
            cognito_dashboards_auth=cognito_dashboards_auth,
            custom_endpoint=custom_endpoint,
            domain_name=domain_name,
            ebs=ebs,
            enable_version_upgrade=enable_version_upgrade,
            encryption_at_rest=encryption_at_rest,
            enforce_https=enforce_https,
            fine_grained_access_control=fine_grained_access_control,
            logging=logging,
            node_to_node_encryption=node_to_node_encryption,
            removal_policy=removal_policy,
            security_groups=security_groups,
            tls_security_policy=tls_security_policy,
            use_unsigned_basic_auth=use_unsigned_basic_auth,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            zone_awareness=zone_awareness,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDomainAttributes")
    @builtins.classmethod
    def from_domain_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain_arn: builtins.str,
        domain_endpoint: builtins.str,
    ) -> IDomain:
        '''(experimental) Creates a domain construct that represents an external domain.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param domain_arn: (experimental) The ARN of the Amazon OpenSearch Service domain.
        :param domain_endpoint: (experimental) The domain endpoint of the Amazon OpenSearch Service domain.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ecfc5600024bd94b833304080dfe4bea0138baf9cfc883d2735b4b449bc0ce6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = DomainAttributes(
            domain_arn=domain_arn, domain_endpoint=domain_endpoint
        )

        return typing.cast(IDomain, jsii.sinvoke(cls, "fromDomainAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromDomainEndpoint")
    @builtins.classmethod
    def from_domain_endpoint(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        domain_endpoint: builtins.str,
    ) -> IDomain:
        '''(experimental) Creates a domain construct that represents an external domain via domain endpoint.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param domain_endpoint: The domain's endpoint.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac11b34aef555377b3624ebd9ba6def055e28b0be0b4c4c3c50dc6f361d4a49b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument domain_endpoint", value=domain_endpoint, expected_type=type_hints["domain_endpoint"])
        return typing.cast(IDomain, jsii.sinvoke(cls, "fromDomainEndpoint", [scope, id, domain_endpoint]))

    @jsii.member(jsii_name="addAccessPolicies")
    def add_access_policies(
        self,
        *access_policy_statements: _PolicyStatement_296fe8a3,
    ) -> None:
        '''(experimental) Add policy statements to the domain access policy.

        :param access_policy_statements: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ff9c1cb5e879c300c6eafe479d804b3bff71e03194d5cc2383cb1d137154ed)
            check_type(argname="argument access_policy_statements", value=access_policy_statements, expected_type=typing.Tuple[type_hints["access_policy_statements"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addAccessPolicies", [*access_policy_statements]))

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72c5934d29bfb4e29fba53805a0f2e2b3e4b928e60361d46dc6a55703476ce7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexRead", [index, identity]))

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d9190438ff8d1b2dc84347520bc90ec7a377432bb845f3aefc21b6dc4684d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexReadWrite", [index, identity]))

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31cd91b6cff60d70fb1ee7a18756da3431743abada029efabf3458d04734df8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexWrite", [index, identity]))

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0655635cb1352863004833aaf8215010eb6f013918f88eda92572485151b6115)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathRead", [path, identity]))

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c2851f34cc7648036f808895399de1854de7d7aada42e09633bce799e359bc)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathReadWrite", [path, identity]))

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced2d566a63467f958390929c74476644b516b8f649202777a813089ce7721ab)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathWrite", [path, identity]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098258ed1466c8b6188524853d28b50669b05bd883f2e97a79e02684566ed4b8)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc2d202a4ff3d182a3fd432163b8f9b87cd53700b424ec3fae72ffd1123a04d)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWrite", [identity]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140db81ca7b297c3d1e7cc9e40f2710d43f1a1195ca5815ef7ac013a5f3f9d90)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [identity]))

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
        '''(experimental) Return the given named metric for this domain.

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
            type_hints = typing.get_type_hints(_typecheckingstub__26aabd29c1c6d4ef0f0f5ee0e1d53cf79a6b1d91a84a1bb7575878de76ad554d)
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

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
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
        '''(experimental) Metric for automated snapshot failures.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricAutomatedSnapshotFailure", [props]))

    @jsii.member(jsii_name="metricClusterIndexWritesBlocked")
    def metric_cluster_index_writes_blocked(
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
        '''(experimental) Metric for the cluster blocking index writes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterIndexWritesBlocked", [props]))

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
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
        '''(experimental) Metric for the time the cluster status is red.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterStatusRed", [props]))

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
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
        '''(experimental) Metric for the time the cluster status is yellow.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterStatusYellow", [props]))

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        '''(experimental) Metric for CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricCPUUtilization", [props]))

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        '''(experimental) Metric for the storage space of nodes in the cluster.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFreeStorageSpace", [props]))

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
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
        '''(experimental) Metric for indexing latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricIndexingLatency", [props]))

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
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
        '''(experimental) Metric for JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
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
        '''(experimental) Metric for KMS key errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricKMSKeyError", [props]))

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
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
        '''(experimental) Metric for KMS key being inaccessible.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricKMSKeyInaccessible", [props]))

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
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
        '''(experimental) Metric for master CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricMasterCPUUtilization", [props]))

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
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
        '''(experimental) Metric for master JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricMasterJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
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
        '''(experimental) Metric for the number of nodes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNodes", [props]))

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
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
        '''(experimental) Metric for number of searchable documents.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSearchableDocuments", [props]))

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
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
        '''(experimental) Metric for search latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

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

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSearchLatency", [props]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) Manages network connections to the domain.

        This will throw an error in case the domain
        is not placed inside a VPC.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''(experimental) Arn of the Amazon OpenSearch Service domain.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''(experimental) Endpoint of the Amazon OpenSearch Service domain.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''(experimental) Identifier of the Amazon OpenSearch Service domain.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) Domain name of the Amazon OpenSearch Service domain.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="appLogGroup")
    def app_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log group that application logs are logged to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "appLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="auditLogGroup")
    def audit_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log group that audit logs are logged to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "auditLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) Master user password if fine grained access control is configured.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_SecretValue_c18506ef], jsii.get(self, "masterUserPassword"))

    @builtins.property
    @jsii.member(jsii_name="slowIndexLogGroup")
    def slow_index_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log group that slow indices are logged to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "slowIndexLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="slowSearchLogGroup")
    def slow_search_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log group that slow searches are logged to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "slowSearchLogGroup"))


__all__ = [
    "AdvancedSecurityOptions",
    "CapacityConfig",
    "CfnDomain",
    "CfnDomainProps",
    "CognitoOptions",
    "CustomEndpointOptions",
    "Domain",
    "DomainAttributes",
    "DomainProps",
    "EbsOptions",
    "EncryptionAtRestOptions",
    "EngineVersion",
    "IDomain",
    "LoggingOptions",
    "TLSSecurityPolicy",
    "ZoneAwarenessConfig",
]

publication.publish()

def _typecheckingstub__15084f043c619e8789d2c006b8f5e5c8f6f4706f24540d9e2add0c4e96061770(
    *,
    master_user_arn: typing.Optional[builtins.str] = None,
    master_user_name: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[_SecretValue_c18506ef] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca448e25b7379aa009919b66eb2b96b59ed3186a2a2d641ec988f4dced6e4dbe(
    *,
    data_node_instance_type: typing.Optional[builtins.str] = None,
    data_nodes: typing.Optional[jsii.Number] = None,
    master_node_instance_type: typing.Optional[builtins.str] = None,
    master_nodes: typing.Optional[jsii.Number] = None,
    warm_instance_type: typing.Optional[builtins.str] = None,
    warm_nodes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018822cada9fc20fbc2039d546a4c366118f3bef26f6fc2fe94aa0cb220d1470(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    access_policies: typing.Any = None,
    advanced_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    advanced_security_options: typing.Optional[typing.Union[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cluster_config: typing.Optional[typing.Union[typing.Union[CfnDomain.ClusterConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cognito_options: typing.Optional[typing.Union[typing.Union[CfnDomain.CognitoOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    domain_endpoint_options: typing.Optional[typing.Union[typing.Union[CfnDomain.DomainEndpointOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs_options: typing.Optional[typing.Union[typing.Union[CfnDomain.EBSOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    encryption_at_rest_options: typing.Optional[typing.Union[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    log_publishing_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnDomain.LogPublishingOptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    node_to_node_encryption_options: typing.Optional[typing.Union[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    off_peak_window_options: typing.Optional[typing.Union[typing.Union[CfnDomain.OffPeakWindowOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    snapshot_options: typing.Optional[typing.Union[typing.Union[CfnDomain.SnapshotOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    software_update_options: typing.Optional[typing.Union[typing.Union[CfnDomain.SoftwareUpdateOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_options: typing.Optional[typing.Union[typing.Union[CfnDomain.VPCOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb1400bb98361a78de6ef9cf05d155acdfc5938c0aa8797ea3ce685b903fda5(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f840d8ec5fd917c982c76d2cd42534262ce6e8dbdfb6d133847f579200a26f7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6f6e6287a8f76ddecc7a9d29ab054c7b74e4d4155a8011bd17b8b8fb8c55e3(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9abf96dfc5d9aa21174bc8d8109978393eae992eebbd188f5cf8e2b402a74f2(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5b06258e30adb72b3a47046a3870f9c0cd3ab173113bad068e65e38abc278f(
    value: typing.Optional[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a4159cc2d44a14ad165e347e7a89d0df7152df0bc8d4280f6c2fa3a8d88db7(
    value: typing.Optional[typing.Union[CfnDomain.ClusterConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534f1101ea263c69b158859d57da289df750668bec0b04ee04c0989dd93a7058(
    value: typing.Optional[typing.Union[CfnDomain.CognitoOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f447d8db4b62496f9fb0d90c4b6f8336ad6e5e479643874d3f6898402f4d5f54(
    value: typing.Optional[typing.Union[CfnDomain.DomainEndpointOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0460497ae9efbf7fe21e22f0cf1d32f7628f113c89633beb99b40b2b997e9b2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a865ef21ce88ff3767b8e44f8c883018fee98a43ca245435fdedd55dbf28c56(
    value: typing.Optional[typing.Union[CfnDomain.EBSOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a74c2a6db0b3e60bbc408b54e01c60cea001adba6011568efed86379c6c217(
    value: typing.Optional[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1280a20e9f907fd13f73a434a6e03496d28879f60aab4584c971e8e115858d4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5692e0bae978b2c4c8b39ca4ce62d10d27651e91a1bd75fe7b51a0d3d825aa(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDomain.LogPublishingOptionProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fa08c60ea9a381906d6e170f52e1cb5a03e3f0ed199e9c475e7714b628be7a(
    value: typing.Optional[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e212e148821f061762c02d4e532a8aacb2788158bf57698c5a4d070d6e244359(
    value: typing.Optional[typing.Union[CfnDomain.OffPeakWindowOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546733aebb1dc8ca80aa8a36976d37ba971e08987010a37b593f31db5a429136(
    value: typing.Optional[typing.Union[CfnDomain.SnapshotOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97be705d8a750b441a8c15d6ba1850f1a0dd73f190c9ab4a5289e77af77860f5(
    value: typing.Optional[typing.Union[CfnDomain.SoftwareUpdateOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f1de6d7691e56980c1571598ce9803fac5744fbb94eed7590ee696b897b4d6(
    value: typing.Optional[typing.Union[CfnDomain.VPCOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f25e94733d813ccf0f9bc0aa6aa7edcfa0b559a04cb6255e5351f7a32a7c314(
    *,
    anonymous_auth_disable_date: typing.Optional[builtins.str] = None,
    anonymous_auth_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    master_user_options: typing.Optional[typing.Union[typing.Union[CfnDomain.MasterUserOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    saml_options: typing.Optional[typing.Union[typing.Union[CfnDomain.SAMLOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19798e56dc23966a5ab47af146c9237b1946659af1c4f9e448eaef1a96adb383(
    *,
    dedicated_master_count: typing.Optional[jsii.Number] = None,
    dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    dedicated_master_type: typing.Optional[builtins.str] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    multi_az_with_standby_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    warm_count: typing.Optional[jsii.Number] = None,
    warm_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    warm_type: typing.Optional[builtins.str] = None,
    zone_awareness_config: typing.Optional[typing.Union[typing.Union[CfnDomain.ZoneAwarenessConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6112a9197eaf165567c1e897c33495f3a0f0e609b7916069e961a617313783cf(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bc7f3bccfca867e6b746ea2aa1711359102884bb2fed42ee9ded52d28191fb(
    *,
    custom_endpoint: typing.Optional[builtins.str] = None,
    custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
    custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enforce_https: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tls_security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e5ba896288813a931fc55037d7cabde27b891be5c68322a634838446c07ac9(
    *,
    ebs_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    iops: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f9d7edf63db161e1ddf10fc57a52b04e40cdb1af3b43f111b0dac0a7241ec7(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3789c2cead192a4265a38342abd75927c0b69587b8fc341c9d76bfd4ac852eee(
    *,
    entity_id: builtins.str,
    metadata_content: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42693055cd068c607ea45e66f4f1d9be14b396e9c5428d47c7242cc35cb9dee6(
    *,
    cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1175b93b058b14bd199f1d17669c78584c8acaa5dbf2de40332b6dc939a66d(
    *,
    master_user_arn: typing.Optional[builtins.str] = None,
    master_user_name: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74f7c0f6498bb8b76b541391e2dc24c8dd9ca6a3e8cc87ea34b001425f460c5(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5caf8191da4b1f99f382e10c5a894613cc7eb5e57ca0c4b24a9e7118a1c4ae95(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    off_peak_window: typing.Optional[typing.Union[typing.Union[CfnDomain.OffPeakWindowProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b432435aeb6103933df960b9cd463d11e0b08d4e79978e5f9717121c618e55a(
    *,
    window_start_time: typing.Optional[typing.Union[typing.Union[CfnDomain.WindowStartTimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1044cfb3a0176eb79a302e5224d21aca834866dd3131f7b026bf2d38858d3635(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    idp: typing.Optional[typing.Union[typing.Union[CfnDomain.IdpProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    master_backend_role: typing.Optional[builtins.str] = None,
    master_user_name: typing.Optional[builtins.str] = None,
    roles_key: typing.Optional[builtins.str] = None,
    session_timeout_minutes: typing.Optional[jsii.Number] = None,
    subject_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc00496502f222c3c2ef4f5ee4237cf51fc5eaf9f1d6ccfb22071a8d7fe6ae0c(
    *,
    automated_update_date: typing.Optional[builtins.str] = None,
    cancellable: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    current_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    new_version: typing.Optional[builtins.str] = None,
    optional_deployment: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    update_available: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    update_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e13b38afbded71e9992440effb17c3e5088d8154a74ea083ce5557a417d826(
    *,
    automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418cf8f4a45cf995c69a66a82c4c6c8187337bc6b21c90e0c4d1e7240268e31f(
    *,
    auto_software_update_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24640fa2d7f598273178d92c1aa2b0796e30785f6245af6073ef634ed918a365(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa8406ba2a50b91cf259e2b56bf23273c4b98d511a136a5d4286fc6a1877858(
    *,
    hours: jsii.Number,
    minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762161cbe51ffd2f00f50f8bcc4e95fb7d9340462d887c4a06d204b10e9f869a(
    *,
    availability_zone_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07dbf51fa688cc880a99add8bbb7e6ee2599448e85757252353abc406979e52(
    *,
    access_policies: typing.Any = None,
    advanced_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    advanced_security_options: typing.Optional[typing.Union[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cluster_config: typing.Optional[typing.Union[typing.Union[CfnDomain.ClusterConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cognito_options: typing.Optional[typing.Union[typing.Union[CfnDomain.CognitoOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    domain_endpoint_options: typing.Optional[typing.Union[typing.Union[CfnDomain.DomainEndpointOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs_options: typing.Optional[typing.Union[typing.Union[CfnDomain.EBSOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    encryption_at_rest_options: typing.Optional[typing.Union[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    log_publishing_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnDomain.LogPublishingOptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    node_to_node_encryption_options: typing.Optional[typing.Union[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    off_peak_window_options: typing.Optional[typing.Union[typing.Union[CfnDomain.OffPeakWindowOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    snapshot_options: typing.Optional[typing.Union[typing.Union[CfnDomain.SnapshotOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    software_update_options: typing.Optional[typing.Union[typing.Union[CfnDomain.SoftwareUpdateOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_options: typing.Optional[typing.Union[typing.Union[CfnDomain.VPCOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f829660d1eedfd90a45cc128da297e91a3aa6c686079478480083fe86ab063b2(
    *,
    identity_pool_id: builtins.str,
    role: _IRole_59af6f50,
    user_pool_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2e4c1ed7f16e16882ac275095fc4da795e6c5436e6f7183ef25347e518eb19(
    *,
    domain_name: builtins.str,
    certificate: typing.Optional[_ICertificate_c7bbdc16] = None,
    hosted_zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afb7aa7127d416fcd578f0aad24ea72f95536d6d840f5d7164aa7c6d0b91928(
    *,
    domain_arn: builtins.str,
    domain_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daeaf001a77450352e8b108e87166dd340e72ae24394e56c4cd351f35b8e1962(
    *,
    version: EngineVersion,
    access_policies: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
    capacity: typing.Optional[typing.Union[CapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cognito_dashboards_auth: typing.Optional[typing.Union[CognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_endpoint: typing.Optional[typing.Union[CustomEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[EbsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_version_upgrade: typing.Optional[builtins.bool] = None,
    encryption_at_rest: typing.Optional[typing.Union[EncryptionAtRestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce_https: typing.Optional[builtins.bool] = None,
    fine_grained_access_control: typing.Optional[typing.Union[AdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[LoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    node_to_node_encryption: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    tls_security_policy: typing.Optional[TLSSecurityPolicy] = None,
    use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    vpc_subnets: typing.Optional[typing.Sequence[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]]] = None,
    zone_awareness: typing.Optional[typing.Union[ZoneAwarenessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2867398f24c82c172a65efbed19b43310142877212a9e05d5eb51427aefb7d0(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    iops: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[_EbsDeviceVolumeType_3b8e2d6d] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5529bae98926c37013e7a351dce2b46c3a55cf1d7979d3f2465253b4a770f0(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    kms_key: typing.Optional[_IKey_36930160] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2435ed2013b571bc41441375c2f09c9d2d3adb281ef6f54642f04470e68e46f8(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1025f8cc72d6a22885bd8484f72977e0c773e119480df469eb6d4bf624927da(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ac8b364180aed741fa552bc1ad508380069ff006826f61dc143f7a6ba6ee23(
    index: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a718660225a53424dfc32fa6ee2e93fc6d62bf499db8c8727c46ef8a0dac0c41(
    index: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52125dd7a4f63f4db9a1aeca99dea1e1e624935e32bd8d4f091c94ce0b1eb1d1(
    index: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14368fbd624409aa8ec7fcb7c7124413793ae9dbbe1adba49c3b96e31efa97b4(
    path: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095ae95840f33445e3f21a890841dda95f03dbfe517af54a54cc70397f65d115(
    path: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d06a58aeb59ff6522c081e0c564b1b904546c0241edd13bbaaa6a5db4fcbe8d(
    path: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c699384919e8404887ce2d952b3ba08c62a05a446b6c02ed022793bba47a815(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b4d09d33c78547a77b6dcf962ce7c588f728d509027e762d79c9b512731238(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91db7dbc79871f47fc4e518d203372aa2bf37e469067749e81348f8f0f9a9279(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef034ee3ea6c3d782e7e1ccbeba0a4b8a220070b58e66c0d47fcfdb2f6a5846(
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

def _typecheckingstub__ec91e0267db0b7900bddb74654a0434a14cf9302e27aaeaeb88ef794a11e97c5(
    *,
    app_log_enabled: typing.Optional[builtins.bool] = None,
    app_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
    audit_log_enabled: typing.Optional[builtins.bool] = None,
    audit_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
    slow_index_log_enabled: typing.Optional[builtins.bool] = None,
    slow_index_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
    slow_search_log_enabled: typing.Optional[builtins.bool] = None,
    slow_search_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0df4125eb09c26b8aef9a66bce9124980882b7b18ee277b1344ef0c0a101bb0(
    *,
    availability_zone_count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ce6156206ad90ca05817dbc08bf54fd8366f0a0a4b4e623ba3c00466bf9093(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    version: EngineVersion,
    access_policies: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
    capacity: typing.Optional[typing.Union[CapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cognito_dashboards_auth: typing.Optional[typing.Union[CognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_endpoint: typing.Optional[typing.Union[CustomEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[EbsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_version_upgrade: typing.Optional[builtins.bool] = None,
    encryption_at_rest: typing.Optional[typing.Union[EncryptionAtRestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce_https: typing.Optional[builtins.bool] = None,
    fine_grained_access_control: typing.Optional[typing.Union[AdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[LoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    node_to_node_encryption: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    tls_security_policy: typing.Optional[TLSSecurityPolicy] = None,
    use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    vpc_subnets: typing.Optional[typing.Sequence[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]]] = None,
    zone_awareness: typing.Optional[typing.Union[ZoneAwarenessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ecfc5600024bd94b833304080dfe4bea0138baf9cfc883d2735b4b449bc0ce6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain_arn: builtins.str,
    domain_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac11b34aef555377b3624ebd9ba6def055e28b0be0b4c4c3c50dc6f361d4a49b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    domain_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ff9c1cb5e879c300c6eafe479d804b3bff71e03194d5cc2383cb1d137154ed(
    *access_policy_statements: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72c5934d29bfb4e29fba53805a0f2e2b3e4b928e60361d46dc6a55703476ce7(
    index: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d9190438ff8d1b2dc84347520bc90ec7a377432bb845f3aefc21b6dc4684d0(
    index: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31cd91b6cff60d70fb1ee7a18756da3431743abada029efabf3458d04734df8(
    index: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0655635cb1352863004833aaf8215010eb6f013918f88eda92572485151b6115(
    path: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c2851f34cc7648036f808895399de1854de7d7aada42e09633bce799e359bc(
    path: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced2d566a63467f958390929c74476644b516b8f649202777a813089ce7721ab(
    path: builtins.str,
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098258ed1466c8b6188524853d28b50669b05bd883f2e97a79e02684566ed4b8(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc2d202a4ff3d182a3fd432163b8f9b87cd53700b424ec3fae72ffd1123a04d(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140db81ca7b297c3d1e7cc9e40f2710d43f1a1195ca5815ef7ac013a5f3f9d90(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26aabd29c1c6d4ef0f0f5ee0e1d53cf79a6b1d91a84a1bb7575878de76ad554d(
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
