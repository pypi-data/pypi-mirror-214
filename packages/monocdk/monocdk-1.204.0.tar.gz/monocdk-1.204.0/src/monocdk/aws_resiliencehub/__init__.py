'''
# AWS::ResilienceHub Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as resiliencehub
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ResilienceHub construct libraries](https://constructs.dev/search?q=resiliencehub)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ResilienceHub resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResilienceHub.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ResilienceHub](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResilienceHub.html).

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
class CfnApp(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_resiliencehub.CfnApp",
):
    '''A CloudFormation ``AWS::ResilienceHub::App``.

    Creates an AWS Resilience Hub application. An AWS Resilience Hub application is a collection of AWS resources structured to prevent and recover AWS application disruptions. To describe a AWS Resilience Hub application, you provide an application name, resources from one or more AWS CloudFormation stacks, AWS Resource Groups , Terraform state files, AppRegistry applications, and an appropriate resiliency policy. In addition, you can also add resources that are located on Amazon Elastic Kubernetes Service ( Amazon EKS ) clusters as optional resources. For more information about the number of resources supported per application, see `Service quotas <https://docs.aws.amazon.com/general/latest/gr/resiliencehub.html#limits_resiliencehub>`_ .

    After you create an AWS Resilience Hub application, you publish it so that you can run a resiliency assessment on it. You can then use recommendations from the assessment to improve resiliency by running another assessment, comparing results, and then iterating the process until you achieve your goals for recovery time objective (RTO) and recovery point objective (RPO).

    :cloudformationResource: AWS::ResilienceHub::App
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_resiliencehub as resiliencehub
        
        cfn_app = resiliencehub.CfnApp(self, "MyCfnApp",
            app_template_body="appTemplateBody",
            name="name",
            resource_mappings=[resiliencehub.CfnApp.ResourceMappingProperty(
                mapping_type="mappingType",
                physical_resource_id=resiliencehub.CfnApp.PhysicalResourceIdProperty(
                    identifier="identifier",
                    type="type",
        
                    # the properties below are optional
                    aws_account_id="awsAccountId",
                    aws_region="awsRegion"
                ),
        
                # the properties below are optional
                eks_source_name="eksSourceName",
                logical_stack_name="logicalStackName",
                resource_name="resourceName",
                terraform_source_name="terraformSourceName"
            )],
        
            # the properties below are optional
            app_assessment_schedule="appAssessmentSchedule",
            description="description",
            resiliency_policy_arn="resiliencyPolicyArn",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        app_template_body: builtins.str,
        name: builtins.str,
        resource_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnApp.ResourceMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        app_assessment_schedule: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resiliency_policy_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ResilienceHub::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_template_body: A JSON string that provides information about your application structure. To learn more about the ``appTemplateBody`` template, see the sample template provided in the *Examples* section. The ``appTemplateBody`` JSON string has the following structure: - *``resources``* The list of logical resources that needs to be included in the AWS Resilience Hub application. Type: Array .. epigraph:: Don't add the resources that you want to exclude. Each ``resources`` array item includes the following fields: - *``logicalResourceId``* The logical identifier of the resource. Type: Object Each ``logicalResourceId`` object includes the following fields: - ``identifier`` The identifier of the resource. Type: String - ``logicalStackName`` The name of the AWS CloudFormation stack this resource belongs to. Type: String - ``resourceGroupName`` The name of the resource group this resource belongs to. Type: String - ``terraformSourceName`` The name of the Terraform S3 state file this resource belongs to. Type: String - ``eksSourceName`` The name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to. .. epigraph:: This parameter accepts values in "eks-cluster/namespace" format. Type: String - *``type``* The type of resource. Type: string - *``name``* The name of the resource. Type: String - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"`` - *``appComponents``* The list of Application Components (AppComponent) that this resource belongs to. If an AppComponent is not part of the AWS Resilience Hub application, it will be added. Type: Array Each ``appComponents`` array item includes the following fields: - ``name`` The name of the AppComponent. Type: String - ``type`` The type of AppComponent. For more information about the types of AppComponent, see `Grouping resources in an AppComponent <https://docs.aws.amazon.com/resilience-hub/latest/userguide/AppComponent.grouping.html>`_ . Type: String - ``resourceNames`` The list of included resources that are assigned to the AppComponent. Type: Array of strings - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"`` - *``excludedResources``* The list of logical resource identifiers to be excluded from the application. Type: Array .. epigraph:: Don't add the resources that you want to include. Each ``excludedResources`` array item includes the following fields: - *``logicalResourceIds``* The logical identifier of the resource. Type: Object .. epigraph:: You can configure only one of the following fields: - ``logicalStackName`` - ``resourceGroupName`` - ``terraformSourceName`` - ``eksSourceName`` Each ``logicalResourceIds`` object includes the following fields: - ``identifier`` The identifier of the resource. Type: String - ``logicalStackName`` The name of the AWS CloudFormation stack this resource belongs to. Type: String - ``resourceGroupName`` The name of the resource group this resource belongs to. Type: String - ``terraformSourceName`` The name of the Terraform S3 state file this resource belongs to. Type: String - ``eksSourceName`` The name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to. .. epigraph:: This parameter accepts values in "eks-cluster/namespace" format. Type: String - *``version``* The AWS Resilience Hub application version. - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``
        :param name: The name for the application.
        :param resource_mappings: An array of ResourceMapping objects.
        :param app_assessment_schedule: Assessment execution schedule with 'Daily' or 'Disabled' values.
        :param description: The optional description for an app.
        :param resiliency_policy_arn: The Amazon Resource Name (ARN) of the resiliency policy.
        :param tags: The tags assigned to the resource. A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191be28b7ba788a8b8a05ad8a3fa7d319f34a7a72975064a70f7865785979a8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppProps(
            app_template_body=app_template_body,
            name=name,
            resource_mappings=resource_mappings,
            app_assessment_schedule=app_assessment_schedule,
            description=description,
            resiliency_policy_arn=resiliency_policy_arn,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93fe4d3dd24522742d22aefedc4eb00864c557c5dbc87b8bdc00e5c28d3069ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__345373beef3fcbd0a7ba790559ac131d1d46093972e9cb3ab7b8bc64c07d38ef)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAppArn")
    def attr_app_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the app.

        :cloudformationAttribute: AppArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags assigned to the resource.

        A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="appTemplateBody")
    def app_template_body(self) -> builtins.str:
        '''A JSON string that provides information about your application structure.

        To learn more about the ``appTemplateBody`` template, see the sample template provided in the *Examples* section.

        The ``appTemplateBody`` JSON string has the following structure:

        - *``resources``*

        The list of logical resources that needs to be included in the AWS Resilience Hub application.

        Type: Array
        .. epigraph::

           Don't add the resources that you want to exclude.

        Each ``resources`` array item includes the following fields:

        - *``logicalResourceId``*

        The logical identifier of the resource.

        Type: Object

        Each ``logicalResourceId`` object includes the following fields:

        - ``identifier``

        The identifier of the resource.

        Type: String

        - ``logicalStackName``

        The name of the AWS CloudFormation stack this resource belongs to.

        Type: String

        - ``resourceGroupName``

        The name of the resource group this resource belongs to.

        Type: String

        - ``terraformSourceName``

        The name of the Terraform S3 state file this resource belongs to.

        Type: String

        - ``eksSourceName``

        The name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to.
        .. epigraph::

           This parameter accepts values in "eks-cluster/namespace" format.

        Type: String

        - *``type``*

        The type of resource.

        Type: string

        - *``name``*

        The name of the resource.

        Type: String

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        - *``appComponents``*

        The list of Application Components (AppComponent) that this resource belongs to. If an AppComponent is not part of the AWS Resilience Hub application, it will be added.

        Type: Array

        Each ``appComponents`` array item includes the following fields:

        - ``name``

        The name of the AppComponent.

        Type: String

        - ``type``

        The type of AppComponent. For more information about the types of AppComponent, see `Grouping resources in an AppComponent <https://docs.aws.amazon.com/resilience-hub/latest/userguide/AppComponent.grouping.html>`_ .

        Type: String

        - ``resourceNames``

        The list of included resources that are assigned to the AppComponent.

        Type: Array of strings

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        - *``excludedResources``*

        The list of logical resource identifiers to be excluded from the application.

        Type: Array
        .. epigraph::

           Don't add the resources that you want to include.

        Each ``excludedResources`` array item includes the following fields:

        - *``logicalResourceIds``*

        The logical identifier of the resource.

        Type: Object
        .. epigraph::

           You can configure only one of the following fields:

           - ``logicalStackName``
           - ``resourceGroupName``
           - ``terraformSourceName``
           - ``eksSourceName``

        Each ``logicalResourceIds`` object includes the following fields:

        - ``identifier``

        The identifier of the resource.

        Type: String

        - ``logicalStackName``

        The name of the AWS CloudFormation stack this resource belongs to.

        Type: String

        - ``resourceGroupName``

        The name of the resource group this resource belongs to.

        Type: String

        - ``terraformSourceName``

        The name of the Terraform S3 state file this resource belongs to.

        Type: String

        - ``eksSourceName``

        The name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to.
        .. epigraph::

           This parameter accepts values in "eks-cluster/namespace" format.

        Type: String

        - *``version``*

        The AWS Resilience Hub application version.

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-apptemplatebody
        '''
        return typing.cast(builtins.str, jsii.get(self, "appTemplateBody"))

    @app_template_body.setter
    def app_template_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5609e011edf46a7cec46ee8545dc0788bfb12d2b9fecdd112496e49d66defeaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appTemplateBody", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938e073419e540d389bc95bd46ac0f55afd44b49e923613b398cb3bd0a753545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceMappings")
    def resource_mappings(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.ResourceMappingProperty", _IResolvable_a771d0ef]]]:
        '''An array of ResourceMapping objects.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resourcemappings
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.ResourceMappingProperty", _IResolvable_a771d0ef]]], jsii.get(self, "resourceMappings"))

    @resource_mappings.setter
    def resource_mappings(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.ResourceMappingProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32747b74820eb4857637b8618bac336f91f9bd7143465a108fb5e1b8e84de9ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceMappings", value)

    @builtins.property
    @jsii.member(jsii_name="appAssessmentSchedule")
    def app_assessment_schedule(self) -> typing.Optional[builtins.str]:
        '''Assessment execution schedule with 'Daily' or 'Disabled' values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-appassessmentschedule
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appAssessmentSchedule"))

    @app_assessment_schedule.setter
    def app_assessment_schedule(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc899c63120586f60fc2edad67fa65243109453bfa5ab6e56b0a198818d0ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appAssessmentSchedule", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The optional description for an app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89809ab476f9e8859db11adab63a57b1b115c71d064fff56c77c641a9ecac5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="resiliencyPolicyArn")
    def resiliency_policy_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resiliency policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resiliencypolicyarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resiliencyPolicyArn"))

    @resiliency_policy_arn.setter
    def resiliency_policy_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f968981feddf143345de2a9b6cf44fd0703b55721939ab4cb08b5771e9e86c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resiliencyPolicyArn", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_resiliencehub.CfnApp.PhysicalResourceIdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "identifier": "identifier",
            "type": "type",
            "aws_account_id": "awsAccountId",
            "aws_region": "awsRegion",
        },
    )
    class PhysicalResourceIdProperty:
        def __init__(
            self,
            *,
            identifier: builtins.str,
            type: builtins.str,
            aws_account_id: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a physical resource identifier.

            :param identifier: The identifier of the physical resource.
            :param type: Specifies the type of physical resource identifier. - **Arn** - The resource identifier is an Amazon Resource Name (ARN) . - **Native** - The resource identifier is an AWS Resilience Hub -native identifier.
            :param aws_account_id: The AWS account that owns the physical resource.
            :param aws_region: The AWS Region that the physical resource is located in.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_resiliencehub as resiliencehub
                
                physical_resource_id_property = resiliencehub.CfnApp.PhysicalResourceIdProperty(
                    identifier="identifier",
                    type="type",
                
                    # the properties below are optional
                    aws_account_id="awsAccountId",
                    aws_region="awsRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d70a0c515e9b3bcc85d5e8803f7aafd8662e99e0454bd9389ee4801d43cd6c7)
                check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "identifier": identifier,
                "type": type,
            }
            if aws_account_id is not None:
                self._values["aws_account_id"] = aws_account_id
            if aws_region is not None:
                self._values["aws_region"] = aws_region

        @builtins.property
        def identifier(self) -> builtins.str:
            '''The identifier of the physical resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-identifier
            '''
            result = self._values.get("identifier")
            assert result is not None, "Required property 'identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''Specifies the type of physical resource identifier.

            - **Arn** - The resource identifier is an Amazon Resource Name (ARN) .
            - **Native** - The resource identifier is an AWS Resilience Hub -native identifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def aws_account_id(self) -> typing.Optional[builtins.str]:
            '''The AWS account that owns the physical resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-awsaccountid
            '''
            result = self._values.get("aws_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the physical resource is located in.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PhysicalResourceIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_resiliencehub.CfnApp.ResourceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mapping_type": "mappingType",
            "physical_resource_id": "physicalResourceId",
            "eks_source_name": "eksSourceName",
            "logical_stack_name": "logicalStackName",
            "resource_name": "resourceName",
            "terraform_source_name": "terraformSourceName",
        },
    )
    class ResourceMappingProperty:
        def __init__(
            self,
            *,
            mapping_type: builtins.str,
            physical_resource_id: typing.Union[typing.Union["CfnApp.PhysicalResourceIdProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            eks_source_name: typing.Optional[builtins.str] = None,
            logical_stack_name: typing.Optional[builtins.str] = None,
            resource_name: typing.Optional[builtins.str] = None,
            terraform_source_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a resource mapping.

            :param mapping_type: Specifies the type of resource mapping. Valid Values: CfnStack | Resource | AppRegistryApp | ResourceGroup | Terraform - **AppRegistryApp** - The resource is mapped to another application. The name of the application is contained in the ``appRegistryAppName`` property. - **CfnStack** - The resource is mapped to a CloudFormation stack. The name of the CloudFormation stack is contained in the ``logicalStackName`` property. - **Resource** - The resource is mapped to another resource. The name of the resource is contained in the ``resourceName`` property. - **ResourceGroup** - The resource is mapped to a resource group. The name of the resource group is contained in the ``resourceGroupName`` property.
            :param physical_resource_id: The identifier of this resource.
            :param eks_source_name: ``CfnApp.ResourceMappingProperty.EksSourceName``.
            :param logical_stack_name: The name of the CloudFormation stack this resource is mapped to.
            :param resource_name: The name of the resource this resource is mapped to.
            :param terraform_source_name: The short name of the Terraform source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_resiliencehub as resiliencehub
                
                resource_mapping_property = resiliencehub.CfnApp.ResourceMappingProperty(
                    mapping_type="mappingType",
                    physical_resource_id=resiliencehub.CfnApp.PhysicalResourceIdProperty(
                        identifier="identifier",
                        type="type",
                
                        # the properties below are optional
                        aws_account_id="awsAccountId",
                        aws_region="awsRegion"
                    ),
                
                    # the properties below are optional
                    eks_source_name="eksSourceName",
                    logical_stack_name="logicalStackName",
                    resource_name="resourceName",
                    terraform_source_name="terraformSourceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce10f7d2d1daa79742328e25ba0d426b0a44cd106da12996a3e5eb4845752b1b)
                check_type(argname="argument mapping_type", value=mapping_type, expected_type=type_hints["mapping_type"])
                check_type(argname="argument physical_resource_id", value=physical_resource_id, expected_type=type_hints["physical_resource_id"])
                check_type(argname="argument eks_source_name", value=eks_source_name, expected_type=type_hints["eks_source_name"])
                check_type(argname="argument logical_stack_name", value=logical_stack_name, expected_type=type_hints["logical_stack_name"])
                check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
                check_type(argname="argument terraform_source_name", value=terraform_source_name, expected_type=type_hints["terraform_source_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mapping_type": mapping_type,
                "physical_resource_id": physical_resource_id,
            }
            if eks_source_name is not None:
                self._values["eks_source_name"] = eks_source_name
            if logical_stack_name is not None:
                self._values["logical_stack_name"] = logical_stack_name
            if resource_name is not None:
                self._values["resource_name"] = resource_name
            if terraform_source_name is not None:
                self._values["terraform_source_name"] = terraform_source_name

        @builtins.property
        def mapping_type(self) -> builtins.str:
            '''Specifies the type of resource mapping.

            Valid Values: CfnStack | Resource | AppRegistryApp | ResourceGroup | Terraform

            - **AppRegistryApp** - The resource is mapped to another application. The name of the application is contained in the ``appRegistryAppName`` property.
            - **CfnStack** - The resource is mapped to a CloudFormation stack. The name of the CloudFormation stack is contained in the ``logicalStackName`` property.
            - **Resource** - The resource is mapped to another resource. The name of the resource is contained in the ``resourceName`` property.
            - **ResourceGroup** - The resource is mapped to a resource group. The name of the resource group is contained in the ``resourceGroupName`` property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-mappingtype
            '''
            result = self._values.get("mapping_type")
            assert result is not None, "Required property 'mapping_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def physical_resource_id(
            self,
        ) -> typing.Union["CfnApp.PhysicalResourceIdProperty", _IResolvable_a771d0ef]:
            '''The identifier of this resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-physicalresourceid
            '''
            result = self._values.get("physical_resource_id")
            assert result is not None, "Required property 'physical_resource_id' is missing"
            return typing.cast(typing.Union["CfnApp.PhysicalResourceIdProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def eks_source_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApp.ResourceMappingProperty.EksSourceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-ekssourcename
            '''
            result = self._values.get("eks_source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logical_stack_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudFormation stack this resource is mapped to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-logicalstackname
            '''
            result = self._values.get("logical_stack_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_name(self) -> typing.Optional[builtins.str]:
            '''The name of the resource this resource is mapped to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-resourcename
            '''
            result = self._values.get("resource_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def terraform_source_name(self) -> typing.Optional[builtins.str]:
            '''The short name of the Terraform source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-terraformsourcename
            '''
            result = self._values.get("terraform_source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_resiliencehub.CfnAppProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_template_body": "appTemplateBody",
        "name": "name",
        "resource_mappings": "resourceMappings",
        "app_assessment_schedule": "appAssessmentSchedule",
        "description": "description",
        "resiliency_policy_arn": "resiliencyPolicyArn",
        "tags": "tags",
    },
)
class CfnAppProps:
    def __init__(
        self,
        *,
        app_template_body: builtins.str,
        name: builtins.str,
        resource_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.ResourceMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        app_assessment_schedule: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resiliency_policy_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApp``.

        :param app_template_body: A JSON string that provides information about your application structure. To learn more about the ``appTemplateBody`` template, see the sample template provided in the *Examples* section. The ``appTemplateBody`` JSON string has the following structure: - *``resources``* The list of logical resources that needs to be included in the AWS Resilience Hub application. Type: Array .. epigraph:: Don't add the resources that you want to exclude. Each ``resources`` array item includes the following fields: - *``logicalResourceId``* The logical identifier of the resource. Type: Object Each ``logicalResourceId`` object includes the following fields: - ``identifier`` The identifier of the resource. Type: String - ``logicalStackName`` The name of the AWS CloudFormation stack this resource belongs to. Type: String - ``resourceGroupName`` The name of the resource group this resource belongs to. Type: String - ``terraformSourceName`` The name of the Terraform S3 state file this resource belongs to. Type: String - ``eksSourceName`` The name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to. .. epigraph:: This parameter accepts values in "eks-cluster/namespace" format. Type: String - *``type``* The type of resource. Type: string - *``name``* The name of the resource. Type: String - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"`` - *``appComponents``* The list of Application Components (AppComponent) that this resource belongs to. If an AppComponent is not part of the AWS Resilience Hub application, it will be added. Type: Array Each ``appComponents`` array item includes the following fields: - ``name`` The name of the AppComponent. Type: String - ``type`` The type of AppComponent. For more information about the types of AppComponent, see `Grouping resources in an AppComponent <https://docs.aws.amazon.com/resilience-hub/latest/userguide/AppComponent.grouping.html>`_ . Type: String - ``resourceNames`` The list of included resources that are assigned to the AppComponent. Type: Array of strings - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"`` - *``excludedResources``* The list of logical resource identifiers to be excluded from the application. Type: Array .. epigraph:: Don't add the resources that you want to include. Each ``excludedResources`` array item includes the following fields: - *``logicalResourceIds``* The logical identifier of the resource. Type: Object .. epigraph:: You can configure only one of the following fields: - ``logicalStackName`` - ``resourceGroupName`` - ``terraformSourceName`` - ``eksSourceName`` Each ``logicalResourceIds`` object includes the following fields: - ``identifier`` The identifier of the resource. Type: String - ``logicalStackName`` The name of the AWS CloudFormation stack this resource belongs to. Type: String - ``resourceGroupName`` The name of the resource group this resource belongs to. Type: String - ``terraformSourceName`` The name of the Terraform S3 state file this resource belongs to. Type: String - ``eksSourceName`` The name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to. .. epigraph:: This parameter accepts values in "eks-cluster/namespace" format. Type: String - *``version``* The AWS Resilience Hub application version. - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``
        :param name: The name for the application.
        :param resource_mappings: An array of ResourceMapping objects.
        :param app_assessment_schedule: Assessment execution schedule with 'Daily' or 'Disabled' values.
        :param description: The optional description for an app.
        :param resiliency_policy_arn: The Amazon Resource Name (ARN) of the resiliency policy.
        :param tags: The tags assigned to the resource. A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_resiliencehub as resiliencehub
            
            cfn_app_props = resiliencehub.CfnAppProps(
                app_template_body="appTemplateBody",
                name="name",
                resource_mappings=[resiliencehub.CfnApp.ResourceMappingProperty(
                    mapping_type="mappingType",
                    physical_resource_id=resiliencehub.CfnApp.PhysicalResourceIdProperty(
                        identifier="identifier",
                        type="type",
            
                        # the properties below are optional
                        aws_account_id="awsAccountId",
                        aws_region="awsRegion"
                    ),
            
                    # the properties below are optional
                    eks_source_name="eksSourceName",
                    logical_stack_name="logicalStackName",
                    resource_name="resourceName",
                    terraform_source_name="terraformSourceName"
                )],
            
                # the properties below are optional
                app_assessment_schedule="appAssessmentSchedule",
                description="description",
                resiliency_policy_arn="resiliencyPolicyArn",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0185f53c4600687ba6d7b89c953ed814b1a82992972bd3005f11bf8bc5f3b54a)
            check_type(argname="argument app_template_body", value=app_template_body, expected_type=type_hints["app_template_body"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_mappings", value=resource_mappings, expected_type=type_hints["resource_mappings"])
            check_type(argname="argument app_assessment_schedule", value=app_assessment_schedule, expected_type=type_hints["app_assessment_schedule"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument resiliency_policy_arn", value=resiliency_policy_arn, expected_type=type_hints["resiliency_policy_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_template_body": app_template_body,
            "name": name,
            "resource_mappings": resource_mappings,
        }
        if app_assessment_schedule is not None:
            self._values["app_assessment_schedule"] = app_assessment_schedule
        if description is not None:
            self._values["description"] = description
        if resiliency_policy_arn is not None:
            self._values["resiliency_policy_arn"] = resiliency_policy_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_template_body(self) -> builtins.str:
        '''A JSON string that provides information about your application structure.

        To learn more about the ``appTemplateBody`` template, see the sample template provided in the *Examples* section.

        The ``appTemplateBody`` JSON string has the following structure:

        - *``resources``*

        The list of logical resources that needs to be included in the AWS Resilience Hub application.

        Type: Array
        .. epigraph::

           Don't add the resources that you want to exclude.

        Each ``resources`` array item includes the following fields:

        - *``logicalResourceId``*

        The logical identifier of the resource.

        Type: Object

        Each ``logicalResourceId`` object includes the following fields:

        - ``identifier``

        The identifier of the resource.

        Type: String

        - ``logicalStackName``

        The name of the AWS CloudFormation stack this resource belongs to.

        Type: String

        - ``resourceGroupName``

        The name of the resource group this resource belongs to.

        Type: String

        - ``terraformSourceName``

        The name of the Terraform S3 state file this resource belongs to.

        Type: String

        - ``eksSourceName``

        The name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to.
        .. epigraph::

           This parameter accepts values in "eks-cluster/namespace" format.

        Type: String

        - *``type``*

        The type of resource.

        Type: string

        - *``name``*

        The name of the resource.

        Type: String

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        - *``appComponents``*

        The list of Application Components (AppComponent) that this resource belongs to. If an AppComponent is not part of the AWS Resilience Hub application, it will be added.

        Type: Array

        Each ``appComponents`` array item includes the following fields:

        - ``name``

        The name of the AppComponent.

        Type: String

        - ``type``

        The type of AppComponent. For more information about the types of AppComponent, see `Grouping resources in an AppComponent <https://docs.aws.amazon.com/resilience-hub/latest/userguide/AppComponent.grouping.html>`_ .

        Type: String

        - ``resourceNames``

        The list of included resources that are assigned to the AppComponent.

        Type: Array of strings

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        - *``excludedResources``*

        The list of logical resource identifiers to be excluded from the application.

        Type: Array
        .. epigraph::

           Don't add the resources that you want to include.

        Each ``excludedResources`` array item includes the following fields:

        - *``logicalResourceIds``*

        The logical identifier of the resource.

        Type: Object
        .. epigraph::

           You can configure only one of the following fields:

           - ``logicalStackName``
           - ``resourceGroupName``
           - ``terraformSourceName``
           - ``eksSourceName``

        Each ``logicalResourceIds`` object includes the following fields:

        - ``identifier``

        The identifier of the resource.

        Type: String

        - ``logicalStackName``

        The name of the AWS CloudFormation stack this resource belongs to.

        Type: String

        - ``resourceGroupName``

        The name of the resource group this resource belongs to.

        Type: String

        - ``terraformSourceName``

        The name of the Terraform S3 state file this resource belongs to.

        Type: String

        - ``eksSourceName``

        The name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to.
        .. epigraph::

           This parameter accepts values in "eks-cluster/namespace" format.

        Type: String

        - *``version``*

        The AWS Resilience Hub application version.

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-apptemplatebody
        '''
        result = self._values.get("app_template_body")
        assert result is not None, "Required property 'app_template_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_mappings(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.ResourceMappingProperty, _IResolvable_a771d0ef]]]:
        '''An array of ResourceMapping objects.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resourcemappings
        '''
        result = self._values.get("resource_mappings")
        assert result is not None, "Required property 'resource_mappings' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.ResourceMappingProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def app_assessment_schedule(self) -> typing.Optional[builtins.str]:
        '''Assessment execution schedule with 'Daily' or 'Disabled' values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-appassessmentschedule
        '''
        result = self._values.get("app_assessment_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The optional description for an app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resiliency_policy_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resiliency policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resiliencypolicyarn
        '''
        result = self._values.get("resiliency_policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags assigned to the resource.

        A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResiliencyPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_resiliencehub.CfnResiliencyPolicy",
):
    '''A CloudFormation ``AWS::ResilienceHub::ResiliencyPolicy``.

    Defines a resiliency policy.

    :cloudformationResource: AWS::ResilienceHub::ResiliencyPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_resiliencehub as resiliencehub
        
        cfn_resiliency_policy = resiliencehub.CfnResiliencyPolicy(self, "MyCfnResiliencyPolicy",
            policy={
                "policy_key": resiliencehub.CfnResiliencyPolicy.FailurePolicyProperty(
                    rpo_in_secs=123,
                    rto_in_secs=123
                )
            },
            policy_name="policyName",
            tier="tier",
        
            # the properties below are optional
            data_location_constraint="dataLocationConstraint",
            policy_description="policyDescription",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnResiliencyPolicy.FailurePolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        policy_name: builtins.str,
        tier: builtins.str,
        data_location_constraint: typing.Optional[builtins.str] = None,
        policy_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ResilienceHub::ResiliencyPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: The resiliency policy.
        :param policy_name: The name of the policy.
        :param tier: The tier for this resiliency policy, ranging from the highest severity ( ``MissionCritical`` ) to lowest ( ``NonCritical`` ).
        :param data_location_constraint: Specifies a high-level geographical location constraint for where your resilience policy data can be stored.
        :param policy_description: The description for the policy.
        :param tags: The tags assigned to the resource. A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb112793857ae984fc953958aa5a52f9edc4089f231122fd7bf7a980211cb97)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResiliencyPolicyProps(
            policy=policy,
            policy_name=policy_name,
            tier=tier,
            data_location_constraint=data_location_constraint,
            policy_description=policy_description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c313be30c4e0cb6c317ca29a70d179915bebd5835d2d429cbdc8a5ccdc5a4ed2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa9a15111dbafd9d223e08cdccd5e87c256dcfb7bcb7807e2b63ce245b1ddbc2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPolicyArn")
    def attr_policy_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the resiliency policy.

        :cloudformationAttribute: PolicyArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags assigned to the resource.

        A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnResiliencyPolicy.FailurePolicyProperty", _IResolvable_a771d0ef]]]:
        '''The resiliency policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policy
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnResiliencyPolicy.FailurePolicyProperty", _IResolvable_a771d0ef]]], jsii.get(self, "policy"))

    @policy.setter
    def policy(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnResiliencyPolicy.FailurePolicyProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5566d23ff9ffa1105985a21804b0d05e14c2926a4d67e33d35f4abd6a9291928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34d38766f0fca4f60866acb02c6e0e61094cb67d9c3bd99c6f348e263f1c56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        '''The tier for this resiliency policy, ranging from the highest severity ( ``MissionCritical`` ) to lowest ( ``NonCritical`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tier
        '''
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e4a57e259dbff131c069e2d3367c2db2f123475d6c06c25607bf5101c9482e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value)

    @builtins.property
    @jsii.member(jsii_name="dataLocationConstraint")
    def data_location_constraint(self) -> typing.Optional[builtins.str]:
        '''Specifies a high-level geographical location constraint for where your resilience policy data can be stored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-datalocationconstraint
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataLocationConstraint"))

    @data_location_constraint.setter
    def data_location_constraint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b4dde7c747164bca76bc263e40dac10768f2a174234aad5e345ccd111204b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataLocationConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="policyDescription")
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''The description for the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policydescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDescription"))

    @policy_description.setter
    def policy_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47b426ca25246eaf83bc09491cca8b476b9afa9e95240e8e3e6e16a0c76d9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDescription", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_resiliencehub.CfnResiliencyPolicy.FailurePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"rpo_in_secs": "rpoInSecs", "rto_in_secs": "rtoInSecs"},
    )
    class FailurePolicyProperty:
        def __init__(
            self,
            *,
            rpo_in_secs: jsii.Number,
            rto_in_secs: jsii.Number,
        ) -> None:
            '''Defines a failure policy.

            :param rpo_in_secs: The Recovery Point Objective (RPO), in seconds.
            :param rto_in_secs: The Recovery Time Objective (RTO), in seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_resiliencehub as resiliencehub
                
                failure_policy_property = resiliencehub.CfnResiliencyPolicy.FailurePolicyProperty(
                    rpo_in_secs=123,
                    rto_in_secs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22d9ef31de8853746f75fd6133427aa0b01c274270e6f409cb95aa37bb3851e6)
                check_type(argname="argument rpo_in_secs", value=rpo_in_secs, expected_type=type_hints["rpo_in_secs"])
                check_type(argname="argument rto_in_secs", value=rto_in_secs, expected_type=type_hints["rto_in_secs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rpo_in_secs": rpo_in_secs,
                "rto_in_secs": rto_in_secs,
            }

        @builtins.property
        def rpo_in_secs(self) -> jsii.Number:
            '''The Recovery Point Objective (RPO), in seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html#cfn-resiliencehub-resiliencypolicy-failurepolicy-rpoinsecs
            '''
            result = self._values.get("rpo_in_secs")
            assert result is not None, "Required property 'rpo_in_secs' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def rto_in_secs(self) -> jsii.Number:
            '''The Recovery Time Objective (RTO), in seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html#cfn-resiliencehub-resiliencypolicy-failurepolicy-rtoinsecs
            '''
            result = self._values.get("rto_in_secs")
            assert result is not None, "Required property 'rto_in_secs' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailurePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_resiliencehub.CfnResiliencyPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "policy_name": "policyName",
        "tier": "tier",
        "data_location_constraint": "dataLocationConstraint",
        "policy_description": "policyDescription",
        "tags": "tags",
    },
)
class CfnResiliencyPolicyProps:
    def __init__(
        self,
        *,
        policy: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnResiliencyPolicy.FailurePolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        policy_name: builtins.str,
        tier: builtins.str,
        data_location_constraint: typing.Optional[builtins.str] = None,
        policy_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResiliencyPolicy``.

        :param policy: The resiliency policy.
        :param policy_name: The name of the policy.
        :param tier: The tier for this resiliency policy, ranging from the highest severity ( ``MissionCritical`` ) to lowest ( ``NonCritical`` ).
        :param data_location_constraint: Specifies a high-level geographical location constraint for where your resilience policy data can be stored.
        :param policy_description: The description for the policy.
        :param tags: The tags assigned to the resource. A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_resiliencehub as resiliencehub
            
            cfn_resiliency_policy_props = resiliencehub.CfnResiliencyPolicyProps(
                policy={
                    "policy_key": resiliencehub.CfnResiliencyPolicy.FailurePolicyProperty(
                        rpo_in_secs=123,
                        rto_in_secs=123
                    )
                },
                policy_name="policyName",
                tier="tier",
            
                # the properties below are optional
                data_location_constraint="dataLocationConstraint",
                policy_description="policyDescription",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0df0d34fd711fafb86de3e1449da33fe4483d4e023c8408ddf51ba53db3ea9d)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument data_location_constraint", value=data_location_constraint, expected_type=type_hints["data_location_constraint"])
            check_type(argname="argument policy_description", value=policy_description, expected_type=type_hints["policy_description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "policy_name": policy_name,
            "tier": tier,
        }
        if data_location_constraint is not None:
            self._values["data_location_constraint"] = data_location_constraint
        if policy_description is not None:
            self._values["policy_description"] = policy_description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def policy(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnResiliencyPolicy.FailurePolicyProperty, _IResolvable_a771d0ef]]]:
        '''The resiliency policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnResiliencyPolicy.FailurePolicyProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''The name of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''The tier for this resiliency policy, ranging from the highest severity ( ``MissionCritical`` ) to lowest ( ``NonCritical`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tier
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_location_constraint(self) -> typing.Optional[builtins.str]:
        '''Specifies a high-level geographical location constraint for where your resilience policy data can be stored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-datalocationconstraint
        '''
        result = self._values.get("data_location_constraint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''The description for the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policydescription
        '''
        result = self._values.get("policy_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags assigned to the resource.

        A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResiliencyPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApp",
    "CfnAppProps",
    "CfnResiliencyPolicy",
    "CfnResiliencyPolicyProps",
]

publication.publish()

def _typecheckingstub__191be28b7ba788a8b8a05ad8a3fa7d319f34a7a72975064a70f7865785979a8d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    app_template_body: builtins.str,
    name: builtins.str,
    resource_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.ResourceMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    app_assessment_schedule: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resiliency_policy_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fe4d3dd24522742d22aefedc4eb00864c557c5dbc87b8bdc00e5c28d3069ec(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345373beef3fcbd0a7ba790559ac131d1d46093972e9cb3ab7b8bc64c07d38ef(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5609e011edf46a7cec46ee8545dc0788bfb12d2b9fecdd112496e49d66defeaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938e073419e540d389bc95bd46ac0f55afd44b49e923613b398cb3bd0a753545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32747b74820eb4857637b8618bac336f91f9bd7143465a108fb5e1b8e84de9ac(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.ResourceMappingProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc899c63120586f60fc2edad67fa65243109453bfa5ab6e56b0a198818d0ac5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89809ab476f9e8859db11adab63a57b1b115c71d064fff56c77c641a9ecac5f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f968981feddf143345de2a9b6cf44fd0703b55721939ab4cb08b5771e9e86c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d70a0c515e9b3bcc85d5e8803f7aafd8662e99e0454bd9389ee4801d43cd6c7(
    *,
    identifier: builtins.str,
    type: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce10f7d2d1daa79742328e25ba0d426b0a44cd106da12996a3e5eb4845752b1b(
    *,
    mapping_type: builtins.str,
    physical_resource_id: typing.Union[typing.Union[CfnApp.PhysicalResourceIdProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    eks_source_name: typing.Optional[builtins.str] = None,
    logical_stack_name: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    terraform_source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0185f53c4600687ba6d7b89c953ed814b1a82992972bd3005f11bf8bc5f3b54a(
    *,
    app_template_body: builtins.str,
    name: builtins.str,
    resource_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.ResourceMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    app_assessment_schedule: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resiliency_policy_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb112793857ae984fc953958aa5a52f9edc4089f231122fd7bf7a980211cb97(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnResiliencyPolicy.FailurePolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    policy_name: builtins.str,
    tier: builtins.str,
    data_location_constraint: typing.Optional[builtins.str] = None,
    policy_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c313be30c4e0cb6c317ca29a70d179915bebd5835d2d429cbdc8a5ccdc5a4ed2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9a15111dbafd9d223e08cdccd5e87c256dcfb7bcb7807e2b63ce245b1ddbc2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5566d23ff9ffa1105985a21804b0d05e14c2926a4d67e33d35f4abd6a9291928(
    value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnResiliencyPolicy.FailurePolicyProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34d38766f0fca4f60866acb02c6e0e61094cb67d9c3bd99c6f348e263f1c56f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e4a57e259dbff131c069e2d3367c2db2f123475d6c06c25607bf5101c9482e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b4dde7c747164bca76bc263e40dac10768f2a174234aad5e345ccd111204b3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47b426ca25246eaf83bc09491cca8b476b9afa9e95240e8e3e6e16a0c76d9cb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d9ef31de8853746f75fd6133427aa0b01c274270e6f409cb95aa37bb3851e6(
    *,
    rpo_in_secs: jsii.Number,
    rto_in_secs: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0df0d34fd711fafb86de3e1449da33fe4483d4e023c8408ddf51ba53db3ea9d(
    *,
    policy: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnResiliencyPolicy.FailurePolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    policy_name: builtins.str,
    tier: builtins.str,
    data_location_constraint: typing.Optional[builtins.str] = None,
    policy_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
