'''
# Amazon DynamoDB Accelerator Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as dax
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DAX construct libraries](https://constructs.dev/search?q=dax)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DAX resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DAX.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DAX](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DAX.html).

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
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnCluster(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dax.CfnCluster",
):
    '''A CloudFormation ``AWS::DAX::Cluster``.

    Creates a DAX cluster. All nodes in the cluster run the same DAX caching software.

    :cloudformationResource: AWS::DAX::Cluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_dax as dax
        
        # tags: Any
        
        cfn_cluster = dax.CfnCluster(self, "MyCfnCluster",
            iam_role_arn="iamRoleArn",
            node_type="nodeType",
            replication_factor=123,
        
            # the properties below are optional
            availability_zones=["availabilityZones"],
            cluster_endpoint_encryption_type="clusterEndpointEncryptionType",
            cluster_name="clusterName",
            description="description",
            notification_topic_arn="notificationTopicArn",
            parameter_group_name="parameterGroupName",
            preferred_maintenance_window="preferredMaintenanceWindow",
            security_group_ids=["securityGroupIds"],
            sse_specification=dax.CfnCluster.SSESpecificationProperty(
                sse_enabled=False
            ),
            subnet_group_name="subnetGroupName",
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        iam_role_arn: builtins.str,
        node_type: builtins.str,
        replication_factor: jsii.Number,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cluster_endpoint_encryption_type: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        sse_specification: typing.Optional[typing.Union[typing.Union["CfnCluster.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::DAX::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param iam_role_arn: A valid Amazon Resource Name (ARN) that identifies an IAM role. At runtime, DAX will assume this role and use the role's permissions to access DynamoDB on your behalf.
        :param node_type: The node type for the nodes in the cluster. (All nodes in a DAX cluster are of the same type.)
        :param replication_factor: The number of nodes in the DAX cluster. A replication factor of 1 will create a single-node cluster, without any read replicas. For additional fault tolerance, you can create a multiple node cluster with one or more read replicas. To do this, set ``ReplicationFactor`` to a number between 3 (one primary and two read replicas) and 10 (one primary and nine read replicas). ``If the AvailabilityZones`` parameter is provided, its length must equal the ``ReplicationFactor`` . .. epigraph:: AWS recommends that you have at least two read replicas per cluster.
        :param availability_zones: The Availability Zones (AZs) in which the cluster nodes will reside after the cluster has been created or updated. If provided, the length of this list must equal the ``ReplicationFactor`` parameter. If you omit this parameter, DAX will spread the nodes across Availability Zones for the highest availability.
        :param cluster_endpoint_encryption_type: The encryption type of the cluster's endpoint. Available values are:. - ``NONE`` - The cluster's endpoint will be unencrypted. - ``TLS`` - The cluster's endpoint will be encrypted with Transport Layer Security, and will provide an x509 certificate for authentication. The default value is ``NONE`` .
        :param cluster_name: The name of the DAX cluster.
        :param description: The description of the cluster.
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to which notifications will be sent. .. epigraph:: The Amazon SNS topic owner must be same as the DAX cluster owner.
        :param parameter_group_name: The parameter group to be associated with the DAX cluster.
        :param preferred_maintenance_window: A range of time when maintenance of DAX cluster software will be performed. For example: ``sun:01:00-sun:09:00`` . Cluster maintenance normally takes less than 30 minutes, and is performed automatically within the maintenance window.
        :param security_group_ids: A list of security group IDs to be assigned to each node in the DAX cluster. (Each of the security group ID is system-generated.) If this parameter is not specified, DAX assigns the default VPC security group to each node.
        :param sse_specification: Represents the settings used to enable server-side encryption on the cluster.
        :param subnet_group_name: The name of the subnet group to be used for the replication group. .. epigraph:: DAX clusters can only run in an Amazon VPC environment. All of the subnets that you specify in a subnet group must exist in the same VPC.
        :param tags: A set of tags to associate with the DAX cluster.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b96296132431ba81ef1e1f6f13a43c10ff7b0604997018b327dc0309eae954)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnClusterProps(
            iam_role_arn=iam_role_arn,
            node_type=node_type,
            replication_factor=replication_factor,
            availability_zones=availability_zones,
            cluster_endpoint_encryption_type=cluster_endpoint_encryption_type,
            cluster_name=cluster_name,
            description=description,
            notification_topic_arn=notification_topic_arn,
            parameter_group_name=parameter_group_name,
            preferred_maintenance_window=preferred_maintenance_window,
            security_group_ids=security_group_ids,
            sse_specification=sse_specification,
            subnet_group_name=subnet_group_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bee81e3b5cc3000939ce14e087470b8a258c9424866bdd226fd16cebf6a5880)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0224fb7c6125a6b5111e4fc64569cd98b56d99a73a029e56d5c64783517a5f4)
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
        '''Returns the ARN of the DAX cluster. For example:.

        ``{ "Fn::GetAtt": [" MyDAXCluster ", "Arn"] }``

        Returns a value similar to the following:

        ``arn:aws:dax:us-east-1:111122223333:cache/MyDAXCluster``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrClusterDiscoveryEndpoint")
    def attr_cluster_discovery_endpoint(self) -> builtins.str:
        '''Returns the endpoint of the DAX cluster. For example:.

        ``{ "Fn::GetAtt": [" MyDAXCluster ", "ClusterDiscoveryEndpoint"] }``

        Returns a value similar to the following:

        ``mydaxcluster.0h3d6x.clustercfg.dax.use1.cache.amazonaws.com:8111``

        :cloudformationAttribute: ClusterDiscoveryEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterDiscoveryEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrClusterDiscoveryEndpointUrl")
    def attr_cluster_discovery_endpoint_url(self) -> builtins.str:
        '''Returns the endpoint URL of the DAX cluster.

        :cloudformationAttribute: ClusterDiscoveryEndpointURL
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterDiscoveryEndpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A set of tags to associate with the DAX cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        '''A valid Amazon Resource Name (ARN) that identifies an IAM role.

        At runtime, DAX will assume this role and use the role's permissions to access DynamoDB on your behalf.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-iamrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30272e1d02eb05561bc655b322187126b31d1f40cf0f6e9a050ba9f09cef3de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        '''The node type for the nodes in the cluster.

        (All nodes in a DAX cluster are of the same type.)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-nodetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df106c5aaed9242a6bbd7159244ccdb4a241c4f72b88039c0aa942b2101f5fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

    @builtins.property
    @jsii.member(jsii_name="replicationFactor")
    def replication_factor(self) -> jsii.Number:
        '''The number of nodes in the DAX cluster.

        A replication factor of 1 will create a single-node cluster, without any read replicas. For additional fault tolerance, you can create a multiple node cluster with one or more read replicas. To do this, set ``ReplicationFactor`` to a number between 3 (one primary and two read replicas) and 10 (one primary and nine read replicas). ``If the AvailabilityZones`` parameter is provided, its length must equal the ``ReplicationFactor`` .
        .. epigraph::

           AWS recommends that you have at least two read replicas per cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-replicationfactor
        '''
        return typing.cast(jsii.Number, jsii.get(self, "replicationFactor"))

    @replication_factor.setter
    def replication_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5188f20fbde7cf2707c4ab3e40244725347aa39e2f6ad36f408d21961932d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationFactor", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Availability Zones (AZs) in which the cluster nodes will reside after the cluster has been created or updated.

        If provided, the length of this list must equal the ``ReplicationFactor`` parameter. If you omit this parameter, DAX will spread the nodes across Availability Zones for the highest availability.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-availabilityzones
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e86f7a9cdee4f65b7e44c2440d5b188f3364223582a20aef6928c1cb5f55cd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="clusterEndpointEncryptionType")
    def cluster_endpoint_encryption_type(self) -> typing.Optional[builtins.str]:
        '''The encryption type of the cluster's endpoint. Available values are:.

        - ``NONE`` - The cluster's endpoint will be unencrypted.
        - ``TLS`` - The cluster's endpoint will be encrypted with Transport Layer Security, and will provide an x509 certificate for authentication.

        The default value is ``NONE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clusterendpointencryptiontype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterEndpointEncryptionType"))

    @cluster_endpoint_encryption_type.setter
    def cluster_endpoint_encryption_type(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8572115c42d211c812fbc078bb96646948e948f06c934db3acb8aed340398c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterEndpointEncryptionType", value)

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DAX cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clustername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8e4fd9d36e14423a683ffd8d7788f800d84d3f27efc69dde8e6e1362dfb705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4d094028d26578cf8b0b7edbc0eb361eb6038c4b209bc1197bd03dd24291c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to which notifications will be sent.

        .. epigraph::

           The Amazon SNS topic owner must be same as the DAX cluster owner.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-notificationtopicarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTopicArn"))

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e4a5ced97333afb58109ce9ddfa4f588d9cb1ebd0e825610e398a8acb0e222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The parameter group to be associated with the DAX cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-parametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterGroupName"))

    @parameter_group_name.setter
    def parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74559d4afd4044fed10e08707c1f71801380bc5b559296a73eb8594bd3db0214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''A range of time when maintenance of DAX cluster software will be performed.

        For example: ``sun:01:00-sun:09:00`` . Cluster maintenance normally takes less than 30 minutes, and is performed automatically within the maintenance window.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56262ba393d776aa5df58c73fc012e8874cccc4b09b6d53473dba24dcf0e1e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs to be assigned to each node in the DAX cluster.

        (Each of the security group ID is system-generated.)

        If this parameter is not specified, DAX assigns the default VPC security group to each node.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ce04a80900d0e4ff121b26ea3f21e9a4fdaac4529549235d6c7ddd017aeaa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_a771d0ef]]:
        '''Represents the settings used to enable server-side encryption on the cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-ssespecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseSpecification"))

    @sse_specification.setter
    def sse_specification(
        self,
        value: typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36789324d3489f2f0fb7e057bdb0dccbe79344a7e84e6b122aed82cb41078de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group to be used for the replication group.

        .. epigraph::

           DAX clusters can only run in an Amazon VPC environment. All of the subnets that you specify in a subnet group must exist in the same VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-subnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetGroupName"))

    @subnet_group_name.setter
    def subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54685f31237e5c10a1e10dc06d6307c3e3658ea7c7ea6f21d22b073ecd192e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetGroupName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_dax.CfnCluster.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Represents the settings used to enable server-side encryption.

            :param sse_enabled: Indicates whether server-side encryption is enabled (true) or disabled (false) on the cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_dax as dax
                
                s_sESpecification_property = dax.CfnCluster.SSESpecificationProperty(
                    sse_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2293d285a74a4260de1735c6eac8803878c5357b916954dff0bc3bad62635f9f)
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether server-side encryption is enabled (true) or disabled (false) on the cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html#cfn-dax-cluster-ssespecification-sseenabled
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_dax.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_role_arn": "iamRoleArn",
        "node_type": "nodeType",
        "replication_factor": "replicationFactor",
        "availability_zones": "availabilityZones",
        "cluster_endpoint_encryption_type": "clusterEndpointEncryptionType",
        "cluster_name": "clusterName",
        "description": "description",
        "notification_topic_arn": "notificationTopicArn",
        "parameter_group_name": "parameterGroupName",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "security_group_ids": "securityGroupIds",
        "sse_specification": "sseSpecification",
        "subnet_group_name": "subnetGroupName",
        "tags": "tags",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        iam_role_arn: builtins.str,
        node_type: builtins.str,
        replication_factor: jsii.Number,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cluster_endpoint_encryption_type: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        sse_specification: typing.Optional[typing.Union[typing.Union[CfnCluster.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnCluster``.

        :param iam_role_arn: A valid Amazon Resource Name (ARN) that identifies an IAM role. At runtime, DAX will assume this role and use the role's permissions to access DynamoDB on your behalf.
        :param node_type: The node type for the nodes in the cluster. (All nodes in a DAX cluster are of the same type.)
        :param replication_factor: The number of nodes in the DAX cluster. A replication factor of 1 will create a single-node cluster, without any read replicas. For additional fault tolerance, you can create a multiple node cluster with one or more read replicas. To do this, set ``ReplicationFactor`` to a number between 3 (one primary and two read replicas) and 10 (one primary and nine read replicas). ``If the AvailabilityZones`` parameter is provided, its length must equal the ``ReplicationFactor`` . .. epigraph:: AWS recommends that you have at least two read replicas per cluster.
        :param availability_zones: The Availability Zones (AZs) in which the cluster nodes will reside after the cluster has been created or updated. If provided, the length of this list must equal the ``ReplicationFactor`` parameter. If you omit this parameter, DAX will spread the nodes across Availability Zones for the highest availability.
        :param cluster_endpoint_encryption_type: The encryption type of the cluster's endpoint. Available values are:. - ``NONE`` - The cluster's endpoint will be unencrypted. - ``TLS`` - The cluster's endpoint will be encrypted with Transport Layer Security, and will provide an x509 certificate for authentication. The default value is ``NONE`` .
        :param cluster_name: The name of the DAX cluster.
        :param description: The description of the cluster.
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to which notifications will be sent. .. epigraph:: The Amazon SNS topic owner must be same as the DAX cluster owner.
        :param parameter_group_name: The parameter group to be associated with the DAX cluster.
        :param preferred_maintenance_window: A range of time when maintenance of DAX cluster software will be performed. For example: ``sun:01:00-sun:09:00`` . Cluster maintenance normally takes less than 30 minutes, and is performed automatically within the maintenance window.
        :param security_group_ids: A list of security group IDs to be assigned to each node in the DAX cluster. (Each of the security group ID is system-generated.) If this parameter is not specified, DAX assigns the default VPC security group to each node.
        :param sse_specification: Represents the settings used to enable server-side encryption on the cluster.
        :param subnet_group_name: The name of the subnet group to be used for the replication group. .. epigraph:: DAX clusters can only run in an Amazon VPC environment. All of the subnets that you specify in a subnet group must exist in the same VPC.
        :param tags: A set of tags to associate with the DAX cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dax as dax
            
            # tags: Any
            
            cfn_cluster_props = dax.CfnClusterProps(
                iam_role_arn="iamRoleArn",
                node_type="nodeType",
                replication_factor=123,
            
                # the properties below are optional
                availability_zones=["availabilityZones"],
                cluster_endpoint_encryption_type="clusterEndpointEncryptionType",
                cluster_name="clusterName",
                description="description",
                notification_topic_arn="notificationTopicArn",
                parameter_group_name="parameterGroupName",
                preferred_maintenance_window="preferredMaintenanceWindow",
                security_group_ids=["securityGroupIds"],
                sse_specification=dax.CfnCluster.SSESpecificationProperty(
                    sse_enabled=False
                ),
                subnet_group_name="subnetGroupName",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561662f0de4a3748072b3ef794a5fafd469e73487e0ae8024f7b488dea9a20a6)
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument replication_factor", value=replication_factor, expected_type=type_hints["replication_factor"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cluster_endpoint_encryption_type", value=cluster_endpoint_encryption_type, expected_type=type_hints["cluster_endpoint_encryption_type"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument notification_topic_arn", value=notification_topic_arn, expected_type=type_hints["notification_topic_arn"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iam_role_arn": iam_role_arn,
            "node_type": node_type,
            "replication_factor": replication_factor,
        }
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cluster_endpoint_encryption_type is not None:
            self._values["cluster_endpoint_encryption_type"] = cluster_endpoint_encryption_type
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if description is not None:
            self._values["description"] = description
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def iam_role_arn(self) -> builtins.str:
        '''A valid Amazon Resource Name (ARN) that identifies an IAM role.

        At runtime, DAX will assume this role and use the role's permissions to access DynamoDB on your behalf.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(self) -> builtins.str:
        '''The node type for the nodes in the cluster.

        (All nodes in a DAX cluster are of the same type.)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-nodetype
        '''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_factor(self) -> jsii.Number:
        '''The number of nodes in the DAX cluster.

        A replication factor of 1 will create a single-node cluster, without any read replicas. For additional fault tolerance, you can create a multiple node cluster with one or more read replicas. To do this, set ``ReplicationFactor`` to a number between 3 (one primary and two read replicas) and 10 (one primary and nine read replicas). ``If the AvailabilityZones`` parameter is provided, its length must equal the ``ReplicationFactor`` .
        .. epigraph::

           AWS recommends that you have at least two read replicas per cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-replicationfactor
        '''
        result = self._values.get("replication_factor")
        assert result is not None, "Required property 'replication_factor' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Availability Zones (AZs) in which the cluster nodes will reside after the cluster has been created or updated.

        If provided, the length of this list must equal the ``ReplicationFactor`` parameter. If you omit this parameter, DAX will spread the nodes across Availability Zones for the highest availability.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cluster_endpoint_encryption_type(self) -> typing.Optional[builtins.str]:
        '''The encryption type of the cluster's endpoint. Available values are:.

        - ``NONE`` - The cluster's endpoint will be unencrypted.
        - ``TLS`` - The cluster's endpoint will be encrypted with Transport Layer Security, and will provide an x509 certificate for authentication.

        The default value is ``NONE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clusterendpointencryptiontype
        '''
        result = self._values.get("cluster_endpoint_encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the DAX cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to which notifications will be sent.

        .. epigraph::

           The Amazon SNS topic owner must be same as the DAX cluster owner.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-notificationtopicarn
        '''
        result = self._values.get("notification_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The parameter group to be associated with the DAX cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''A range of time when maintenance of DAX cluster software will be performed.

        For example: ``sun:01:00-sun:09:00`` . Cluster maintenance normally takes less than 30 minutes, and is performed automatically within the maintenance window.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group IDs to be assigned to each node in the DAX cluster.

        (Each of the security group ID is system-generated.)

        If this parameter is not specified, DAX assigns the default VPC security group to each node.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnCluster.SSESpecificationProperty, _IResolvable_a771d0ef]]:
        '''Represents the settings used to enable server-side encryption on the cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-ssespecification
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[CfnCluster.SSESpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group to be used for the replication group.

        .. epigraph::

           DAX clusters can only run in an Amazon VPC environment. All of the subnets that you specify in a subnet group must exist in the same VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''A set of tags to associate with the DAX cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnParameterGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dax.CfnParameterGroup",
):
    '''A CloudFormation ``AWS::DAX::ParameterGroup``.

    A named set of parameters that are applied to all of the nodes in a DAX cluster.

    :cloudformationResource: AWS::DAX::ParameterGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_dax as dax
        
        # parameter_name_values: Any
        
        cfn_parameter_group = dax.CfnParameterGroup(self, "MyCfnParameterGroup",
            description="description",
            parameter_group_name="parameterGroupName",
            parameter_name_values=parameter_name_values
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        parameter_name_values: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::DAX::ParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the parameter group.
        :param parameter_group_name: The name of the parameter group.
        :param parameter_name_values: An array of name-value pairs for the parameters in the group. Each element in the array represents a single parameter. .. epigraph:: ``record-ttl-millis`` and ``query-ttl-millis`` are the only supported parameter names. For more details, see `Configuring TTL Settings <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.cluster-management.html#DAX.cluster-management.custom-settings.ttl>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1ec7a40e5193f8460d805585a39516f2ce00d83407e629404c0313fe7efa1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnParameterGroupProps(
            description=description,
            parameter_group_name=parameter_group_name,
            parameter_name_values=parameter_name_values,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3849f5d98fdfbda39baf5619b9f4cc229a4ed30eb143f853b2e0f77dadf49b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39cd4f870ea03c1b48d860a8d9bca49d53ede4768e1de7cc0e841cd63dd0e24f)
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
    @jsii.member(jsii_name="parameterNameValues")
    def parameter_name_values(self) -> typing.Any:
        '''An array of name-value pairs for the parameters in the group.

        Each element in the array represents a single parameter.
        .. epigraph::

           ``record-ttl-millis`` and ``query-ttl-millis`` are the only supported parameter names. For more details, see `Configuring TTL Settings <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.cluster-management.html#DAX.cluster-management.custom-settings.ttl>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parameternamevalues
        '''
        return typing.cast(typing.Any, jsii.get(self, "parameterNameValues"))

    @parameter_name_values.setter
    def parameter_name_values(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac042e311087594163bdbeab1af3cf1d581291b0e5f78fd5adc0cf998eb9ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterNameValues", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9febb2ad5e5f5e90a93be875ea453c2da932b1e302e3de8ff6f09a828b680c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterGroupName"))

    @parameter_group_name.setter
    def parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6456574a96ab9313309a7184e7f93b520b01118755529a433058e8ed33b96597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_dax.CfnParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "parameter_group_name": "parameterGroupName",
        "parameter_name_values": "parameterNameValues",
    },
)
class CfnParameterGroupProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        parameter_name_values: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnParameterGroup``.

        :param description: A description of the parameter group.
        :param parameter_group_name: The name of the parameter group.
        :param parameter_name_values: An array of name-value pairs for the parameters in the group. Each element in the array represents a single parameter. .. epigraph:: ``record-ttl-millis`` and ``query-ttl-millis`` are the only supported parameter names. For more details, see `Configuring TTL Settings <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.cluster-management.html#DAX.cluster-management.custom-settings.ttl>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dax as dax
            
            # parameter_name_values: Any
            
            cfn_parameter_group_props = dax.CfnParameterGroupProps(
                description="description",
                parameter_group_name="parameterGroupName",
                parameter_name_values=parameter_name_values
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62934c71994340afa1c242b9aaa5150b0892a502d7395c3868edaa6ab0235ff3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument parameter_name_values", value=parameter_name_values, expected_type=type_hints["parameter_name_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if parameter_name_values is not None:
            self._values["parameter_name_values"] = parameter_name_values

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_name_values(self) -> typing.Any:
        '''An array of name-value pairs for the parameters in the group.

        Each element in the array represents a single parameter.
        .. epigraph::

           ``record-ttl-millis`` and ``query-ttl-millis`` are the only supported parameter names. For more details, see `Configuring TTL Settings <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.cluster-management.html#DAX.cluster-management.custom-settings.ttl>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parameternamevalues
        '''
        result = self._values.get("parameter_name_values")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSubnetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dax.CfnSubnetGroup",
):
    '''A CloudFormation ``AWS::DAX::SubnetGroup``.

    Creates a new subnet group.

    :cloudformationResource: AWS::DAX::SubnetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_dax as dax
        
        cfn_subnet_group = dax.CfnSubnetGroup(self, "MyCfnSubnetGroup",
            subnet_ids=["subnetIds"],
        
            # the properties below are optional
            description="description",
            subnet_group_name="subnetGroupName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::DAX::SubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subnet_ids: A list of VPC subnet IDs for the subnet group.
        :param description: The description of the subnet group.
        :param subnet_group_name: The name of the subnet group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0667f73913691bbbe7162303e8c7d8429d2813a3712faddc2ba848e97fd0bc4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubnetGroupProps(
            subnet_ids=subnet_ids,
            description=description,
            subnet_group_name=subnet_group_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485b53c18c43ea713897278330988277593c3cf328b5a3f9cfe79ffbc6ab7df5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20a707f2fc0e30acbe984250e6e2cf01d69a4407966270a1a3582f21e6d5a402)
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
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''A list of VPC subnet IDs for the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0052626a64ffc0dc0b7ded1814665518f1fdd447dcb86f1c3343f2b20b925a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64ba56cce8a36ad28e986ab2a8585052cf5104c4886e766c67ee530ff24d354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetGroupName"))

    @subnet_group_name.setter
    def subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7a97100e4a635c78141e14bbaa40392270e0ce8f852616da5b492e5b7a4673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_dax.CfnSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_ids": "subnetIds",
        "description": "description",
        "subnet_group_name": "subnetGroupName",
    },
)
class CfnSubnetGroupProps:
    def __init__(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSubnetGroup``.

        :param subnet_ids: A list of VPC subnet IDs for the subnet group.
        :param description: The description of the subnet group.
        :param subnet_group_name: The name of the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_dax as dax
            
            cfn_subnet_group_props = dax.CfnSubnetGroupProps(
                subnet_ids=["subnetIds"],
            
                # the properties below are optional
                description="description",
                subnet_group_name="subnetGroupName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd091a2d463531d25da9311b503115186bee266b678f4fb32229ae4f4d39f7a)
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_ids": subnet_ids,
        }
        if description is not None:
            self._values["description"] = description
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''A list of VPC subnet IDs for the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCluster",
    "CfnClusterProps",
    "CfnParameterGroup",
    "CfnParameterGroupProps",
    "CfnSubnetGroup",
    "CfnSubnetGroupProps",
]

publication.publish()

def _typecheckingstub__29b96296132431ba81ef1e1f6f13a43c10ff7b0604997018b327dc0309eae954(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    iam_role_arn: builtins.str,
    node_type: builtins.str,
    replication_factor: jsii.Number,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cluster_endpoint_encryption_type: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnCluster.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bee81e3b5cc3000939ce14e087470b8a258c9424866bdd226fd16cebf6a5880(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0224fb7c6125a6b5111e4fc64569cd98b56d99a73a029e56d5c64783517a5f4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30272e1d02eb05561bc655b322187126b31d1f40cf0f6e9a050ba9f09cef3de8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df106c5aaed9242a6bbd7159244ccdb4a241c4f72b88039c0aa942b2101f5fc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5188f20fbde7cf2707c4ab3e40244725347aa39e2f6ad36f408d21961932d0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e86f7a9cdee4f65b7e44c2440d5b188f3364223582a20aef6928c1cb5f55cd6(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8572115c42d211c812fbc078bb96646948e948f06c934db3acb8aed340398c7e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8e4fd9d36e14423a683ffd8d7788f800d84d3f27efc69dde8e6e1362dfb705(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4d094028d26578cf8b0b7edbc0eb361eb6038c4b209bc1197bd03dd24291c2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e4a5ced97333afb58109ce9ddfa4f588d9cb1ebd0e825610e398a8acb0e222(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74559d4afd4044fed10e08707c1f71801380bc5b559296a73eb8594bd3db0214(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56262ba393d776aa5df58c73fc012e8874cccc4b09b6d53473dba24dcf0e1e66(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ce04a80900d0e4ff121b26ea3f21e9a4fdaac4529549235d6c7ddd017aeaa1(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36789324d3489f2f0fb7e057bdb0dccbe79344a7e84e6b122aed82cb41078de(
    value: typing.Optional[typing.Union[CfnCluster.SSESpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54685f31237e5c10a1e10dc06d6307c3e3658ea7c7ea6f21d22b073ecd192e69(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2293d285a74a4260de1735c6eac8803878c5357b916954dff0bc3bad62635f9f(
    *,
    sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561662f0de4a3748072b3ef794a5fafd469e73487e0ae8024f7b488dea9a20a6(
    *,
    iam_role_arn: builtins.str,
    node_type: builtins.str,
    replication_factor: jsii.Number,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cluster_endpoint_encryption_type: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnCluster.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1ec7a40e5193f8460d805585a39516f2ce00d83407e629404c0313fe7efa1f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    parameter_name_values: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3849f5d98fdfbda39baf5619b9f4cc229a4ed30eb143f853b2e0f77dadf49b1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39cd4f870ea03c1b48d860a8d9bca49d53ede4768e1de7cc0e841cd63dd0e24f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac042e311087594163bdbeab1af3cf1d581291b0e5f78fd5adc0cf998eb9ce0(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9febb2ad5e5f5e90a93be875ea453c2da932b1e302e3de8ff6f09a828b680c83(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6456574a96ab9313309a7184e7f93b520b01118755529a433058e8ed33b96597(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62934c71994340afa1c242b9aaa5150b0892a502d7395c3868edaa6ab0235ff3(
    *,
    description: typing.Optional[builtins.str] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    parameter_name_values: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0667f73913691bbbe7162303e8c7d8429d2813a3712faddc2ba848e97fd0bc4e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    subnet_ids: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485b53c18c43ea713897278330988277593c3cf328b5a3f9cfe79ffbc6ab7df5(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a707f2fc0e30acbe984250e6e2cf01d69a4407966270a1a3582f21e6d5a402(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0052626a64ffc0dc0b7ded1814665518f1fdd447dcb86f1c3343f2b20b925a90(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64ba56cce8a36ad28e986ab2a8585052cf5104c4886e766c67ee530ff24d354(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7a97100e4a635c78141e14bbaa40392270e0ce8f852616da5b492e5b7a4673(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd091a2d463531d25da9311b503115186bee266b678f4fb32229ae4f4d39f7a(
    *,
    subnet_ids: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
