'''
# AWS::Grafana Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as grafana
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Grafana construct libraries](https://constructs.dev/search?q=grafana)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Grafana resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Grafana.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Grafana](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Grafana.html).

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
class CfnWorkspace(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_grafana.CfnWorkspace",
):
    '''A CloudFormation ``AWS::Grafana::Workspace``.

    Specifies a *workspace* . In a workspace, you can create Grafana dashboards and visualizations to analyze your metrics, logs, and traces. You don't have to build, package, or deploy any hardware to run the Grafana server.

    :cloudformationResource: AWS::Grafana::Workspace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_grafana as grafana
        
        cfn_workspace = grafana.CfnWorkspace(self, "MyCfnWorkspace",
            account_access_type="accountAccessType",
            authentication_providers=["authenticationProviders"],
            permission_type="permissionType",
        
            # the properties below are optional
            client_token="clientToken",
            data_sources=["dataSources"],
            description="description",
            grafana_version="grafanaVersion",
            name="name",
            network_access_control=grafana.CfnWorkspace.NetworkAccessControlProperty(
                prefix_list_ids=["prefixListIds"],
                vpce_ids=["vpceIds"]
            ),
            notification_destinations=["notificationDestinations"],
            organizational_units=["organizationalUnits"],
            organization_role_name="organizationRoleName",
            role_arn="roleArn",
            saml_configuration=grafana.CfnWorkspace.SamlConfigurationProperty(
                idp_metadata=grafana.CfnWorkspace.IdpMetadataProperty(
                    url="url",
                    xml="xml"
                ),
        
                # the properties below are optional
                allowed_organizations=["allowedOrganizations"],
                assertion_attributes=grafana.CfnWorkspace.AssertionAttributesProperty(
                    email="email",
                    groups="groups",
                    login="login",
                    name="name",
                    org="org",
                    role="role"
                ),
                login_validity_duration=123,
                role_values=grafana.CfnWorkspace.RoleValuesProperty(
                    admin=["admin"],
                    editor=["editor"]
                )
            ),
            stack_set_name="stackSetName",
            vpc_configuration=grafana.CfnWorkspace.VpcConfigurationProperty(
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
        account_access_type: builtins.str,
        authentication_providers: typing.Sequence[builtins.str],
        permission_type: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        grafana_version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_access_control: typing.Optional[typing.Union[typing.Union["CfnWorkspace.NetworkAccessControlProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        notification_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        organizational_units: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_role_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        saml_configuration: typing.Optional[typing.Union[typing.Union["CfnWorkspace.SamlConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stack_set_name: typing.Optional[builtins.str] = None,
        vpc_configuration: typing.Optional[typing.Union[typing.Union["CfnWorkspace.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Grafana::Workspace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_access_type: Specifies whether the workspace can access AWS resources in this AWS account only, or whether it can also access AWS resources in other accounts in the same organization. If this is ``ORGANIZATION`` , the ``OrganizationalUnits`` parameter specifies which organizational units the workspace can access.
        :param authentication_providers: Specifies whether this workspace uses SAML 2.0, AWS IAM Identity Center (successor to AWS Single Sign-On) , or both to authenticate users for using the Grafana console within a workspace. For more information, see `User authentication in Amazon Managed Grafana <https://docs.aws.amazon.com/grafana/latest/userguide/authentication-in-AMG.html>`_ .
        :param permission_type: If this is ``SERVICE_MANAGED`` , and the workplace was created through the Amazon Managed Grafana console, then Amazon Managed Grafana automatically creates the IAM roles and provisions the permissions that the workspace needs to use AWS data sources and notification channels. If this is ``CUSTOMER_MANAGED`` , you must manage those roles and permissions yourself. If you are working with a workspace in a member account of an organization and that account is not a delegated administrator account, and you want the workspace to access data sources in other AWS accounts in the organization, this parameter must be set to ``CUSTOMER_MANAGED`` . For more information about converting between customer and service managed, see `Managing permissions for data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-datasource-and-notification.html>`_ . For more information about the roles and permissions that must be managed for customer managed workspaces, see `Amazon Managed Grafana permissions and policies for AWS data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-manage-permissions.html>`_
        :param client_token: A unique, case-sensitive, user-provided identifier to ensure the idempotency of the request.
        :param data_sources: Specifies the AWS data sources that have been configured to have IAM roles and permissions created to allow Amazon Managed Grafana to read data from these sources. This list is only used when the workspace was created through the AWS console, and the ``permissionType`` is ``SERVICE_MANAGED`` .
        :param description: The user-defined description of the workspace.
        :param grafana_version: Specifies the version of Grafana to support in the new workspace. Supported values are ``8.4`` and ``9.4`` .
        :param name: The name of the workspace.
        :param network_access_control: The configuration settings for network access to your workspace.
        :param notification_destinations: The AWS notification channels that Amazon Managed Grafana can automatically create IAM roles and permissions for, to allow Amazon Managed Grafana to use these channels.
        :param organizational_units: Specifies the organizational units that this workspace is allowed to use data sources from, if this workspace is in an account that is part of an organization.
        :param organization_role_name: The name of the IAM role that is used to access resources through Organizations .
        :param role_arn: The IAM role that grants permissions to the AWS resources that the workspace will view data from. This role must already exist.
        :param saml_configuration: If the workspace uses SAML, use this structure to map SAML assertion attributes to workspace user information and define which groups in the assertion attribute are to have the ``Admin`` and ``Editor`` roles in the workspace.
        :param stack_set_name: The name of the AWS CloudFormation stack set that is used to generate IAM roles to be used for this workspace.
        :param vpc_configuration: The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to. .. epigraph:: Connecting to a private VPC is not yet available in the Asia Pacific (Seoul) Region (ap-northeast-2).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6713a860a65fba5b301856d33d40253246fd4347f380275e14aadf8af43377fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkspaceProps(
            account_access_type=account_access_type,
            authentication_providers=authentication_providers,
            permission_type=permission_type,
            client_token=client_token,
            data_sources=data_sources,
            description=description,
            grafana_version=grafana_version,
            name=name,
            network_access_control=network_access_control,
            notification_destinations=notification_destinations,
            organizational_units=organizational_units,
            organization_role_name=organization_role_name,
            role_arn=role_arn,
            saml_configuration=saml_configuration,
            stack_set_name=stack_set_name,
            vpc_configuration=vpc_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f3b31b994f027eb35968aaeeaa06ffe9e6686ddca81209d5436314b4ddfe40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c66a4a24b4b34122522647798ff6da87f317846efe9bb9424d121bc24060096e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTimestamp")
    def attr_creation_timestamp(self) -> builtins.str:
        '''The date that the workspace was created.

        Type: Timestamp

        :cloudformationAttribute: CreationTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> builtins.str:
        '''The URL that users can use to access the Grafana console in the workspace.

        Type: String

        :cloudformationAttribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrGrafanaVersion")
    def attr_grafana_version(self) -> builtins.str:
        '''Specifies the version of Grafana supported by this workspace.

        Type: String

        :cloudformationAttribute: GrafanaVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGrafanaVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique ID of this workspace.

        Type: String

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrModificationTimestamp")
    def attr_modification_timestamp(self) -> builtins.str:
        '''The most recent date that the workspace was modified.

        Type: Timestamp

        :cloudformationAttribute: ModificationTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModificationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="attrSamlConfigurationStatus")
    def attr_saml_configuration_status(self) -> builtins.str:
        '''Specifies whether the workspace's SAML configuration is complete.

        Valid values: ``CONFIGURED | NOT_CONFIGURED``

        Type: String

        :cloudformationAttribute: SamlConfigurationStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSamlConfigurationStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrSsoClientId")
    def attr_sso_client_id(self) -> builtins.str:
        '''The ID of the IAM Identity Center-managed application that is created by Amazon Managed Grafana .

        Type: String

        :cloudformationAttribute: SsoClientId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSsoClientId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the workspace.

        Valid values: ``ACTIVE | CREATING | DELETING | FAILED | UPDATING | UPGRADING | DELETION_FAILED | CREATION_FAILED | UPDATE_FAILED | UPGRADE_FAILED | LICENSE_REMOVAL_FAILED``

        Type: String

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="accountAccessType")
    def account_access_type(self) -> builtins.str:
        '''Specifies whether the workspace can access AWS resources in this AWS account only, or whether it can also access AWS resources in other accounts in the same organization.

        If this is ``ORGANIZATION`` , the ``OrganizationalUnits`` parameter specifies which organizational units the workspace can access.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-accountaccesstype
        '''
        return typing.cast(builtins.str, jsii.get(self, "accountAccessType"))

    @account_access_type.setter
    def account_access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c68de275d25eb8faf6f7971c01fc2620e87d0b5931b025162966f7d9981d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountAccessType", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationProviders")
    def authentication_providers(self) -> typing.List[builtins.str]:
        '''Specifies whether this workspace uses SAML 2.0, AWS IAM Identity Center (successor to AWS Single Sign-On) , or both to authenticate users for using the Grafana console within a workspace. For more information, see `User authentication in Amazon Managed Grafana <https://docs.aws.amazon.com/grafana/latest/userguide/authentication-in-AMG.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-authenticationproviders
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "authenticationProviders"))

    @authentication_providers.setter
    def authentication_providers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd2f7239a8e347951c9d5b5d6df669b01c9b28d7b6d05d785d709c7f7e6618a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationProviders", value)

    @builtins.property
    @jsii.member(jsii_name="permissionType")
    def permission_type(self) -> builtins.str:
        '''If this is ``SERVICE_MANAGED`` , and the workplace was created through the Amazon Managed Grafana console, then Amazon Managed Grafana automatically creates the IAM roles and provisions the permissions that the workspace needs to use AWS data sources and notification channels.

        If this is ``CUSTOMER_MANAGED`` , you must manage those roles and permissions yourself.

        If you are working with a workspace in a member account of an organization and that account is not a delegated administrator account, and you want the workspace to access data sources in other AWS accounts in the organization, this parameter must be set to ``CUSTOMER_MANAGED`` .

        For more information about converting between customer and service managed, see `Managing permissions for data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-datasource-and-notification.html>`_ . For more information about the roles and permissions that must be managed for customer managed workspaces, see `Amazon Managed Grafana permissions and policies for AWS data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-manage-permissions.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-permissiontype
        '''
        return typing.cast(builtins.str, jsii.get(self, "permissionType"))

    @permission_type.setter
    def permission_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029fe3cac156670ed5fad3878580a59a54c247bacb993be0777c8a5de227cace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionType", value)

    @builtins.property
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        '''A unique, case-sensitive, user-provided identifier to ensure the idempotency of the request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-clienttoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientToken"))

    @client_token.setter
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3099f1f8ab1eda4d09b2968b374aae2d351223b265786221dd18b860250f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientToken", value)

    @builtins.property
    @jsii.member(jsii_name="dataSources")
    def data_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the AWS data sources that have been configured to have IAM roles and permissions created to allow Amazon Managed Grafana to read data from these sources.

        This list is only used when the workspace was created through the AWS console, and the ``permissionType`` is ``SERVICE_MANAGED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-datasources
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dataSources"))

    @data_sources.setter
    def data_sources(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d4b90ca0507d297d5e8b2f0e4aa92672d55a80e7bdf2e6323e305da994d3bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSources", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-defined description of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22189fc3dc23326eb415a1c005563cc19cc08ff7cf643d1f0912e772268f0dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="grafanaVersion")
    def grafana_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the version of Grafana to support in the new workspace.

        Supported values are ``8.4`` and ``9.4`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-grafanaversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaVersion"))

    @grafana_version.setter
    def grafana_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40cc8d3e49aef6f16db5367fbdaa5f7c23fbc86731c21ae8de05131832e87978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaVersion", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f1028f838a43ae15fe822ca3d08f7ddd0a1e962af43f23d82d74d3d93765d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkAccessControl")
    def network_access_control(
        self,
    ) -> typing.Optional[typing.Union["CfnWorkspace.NetworkAccessControlProperty", _IResolvable_a771d0ef]]:
        '''The configuration settings for network access to your workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-networkaccesscontrol
        '''
        return typing.cast(typing.Optional[typing.Union["CfnWorkspace.NetworkAccessControlProperty", _IResolvable_a771d0ef]], jsii.get(self, "networkAccessControl"))

    @network_access_control.setter
    def network_access_control(
        self,
        value: typing.Optional[typing.Union["CfnWorkspace.NetworkAccessControlProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b183d43621972c9790f4442b52be9c7c36219cb429a20e8850f92b4c78df6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAccessControl", value)

    @builtins.property
    @jsii.member(jsii_name="notificationDestinations")
    def notification_destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The AWS notification channels that Amazon Managed Grafana can automatically create IAM roles and permissions for, to allow Amazon Managed Grafana to use these channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-notificationdestinations
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationDestinations"))

    @notification_destinations.setter
    def notification_destinations(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85473b71d8335b413f0fd3d2f72098519854cec58129a60291ff73a3fbb96889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationDestinations", value)

    @builtins.property
    @jsii.member(jsii_name="organizationalUnits")
    def organizational_units(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the organizational units that this workspace is allowed to use data sources from, if this workspace is in an account that is part of an organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-organizationalunits
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "organizationalUnits"))

    @organizational_units.setter
    def organizational_units(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15850135d2afda880809758fce39dbcd2e304d2255997eb82684d65b64c782e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnits", value)

    @builtins.property
    @jsii.member(jsii_name="organizationRoleName")
    def organization_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role that is used to access resources through Organizations .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-organizationrolename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationRoleName"))

    @organization_role_name.setter
    def organization_role_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4321893828d23d1459f7af82bbb41106aa8060ce00c4dd0100604350778928e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationRoleName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM role that grants permissions to the AWS resources that the workspace will view data from.

        This role must already exist.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f75f8fed3e2455955925e5303457da6092cbf59bfa124f1902498df455ce78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="samlConfiguration")
    def saml_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnWorkspace.SamlConfigurationProperty", _IResolvable_a771d0ef]]:
        '''If the workspace uses SAML, use this structure to map SAML assertion attributes to workspace user information and define which groups in the assertion attribute are to have the ``Admin`` and ``Editor`` roles in the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-samlconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnWorkspace.SamlConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "samlConfiguration"))

    @saml_configuration.setter
    def saml_configuration(
        self,
        value: typing.Optional[typing.Union["CfnWorkspace.SamlConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6161aafe79f9227dd913cba72aa00b63f72a50936bd4b8db01cc3bbeca7a6a9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="stackSetName")
    def stack_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AWS CloudFormation stack set that is used to generate IAM roles to be used for this workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-stacksetname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackSetName"))

    @stack_set_name.setter
    def stack_set_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e19e83f9d03b79ab108c9d09aa57d05861a1b0ca1e3586712c2bbed978c72bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackSetName", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfiguration")
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnWorkspace.VpcConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to.

        .. epigraph::

           Connecting to a private VPC is not yet available in the Asia Pacific (Seoul) Region (ap-northeast-2).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-vpcconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnWorkspace.VpcConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcConfiguration"))

    @vpc_configuration.setter
    def vpc_configuration(
        self,
        value: typing.Optional[typing.Union["CfnWorkspace.VpcConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826fbeabf3caadecfa533a42add280ce7510442edb21af4e5045b1e18cf8f136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_grafana.CfnWorkspace.AssertionAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email": "email",
            "groups": "groups",
            "login": "login",
            "name": "name",
            "org": "org",
            "role": "role",
        },
    )
    class AssertionAttributesProperty:
        def __init__(
            self,
            *,
            email: typing.Optional[builtins.str] = None,
            groups: typing.Optional[builtins.str] = None,
            login: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            org: typing.Optional[builtins.str] = None,
            role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that defines which attributes in the IdP assertion are to be used to define information about the users authenticated by the IdP to use the workspace.

            :param email: The name of the attribute within the SAML assertion to use as the email names for SAML users.
            :param groups: The name of the attribute within the SAML assertion to use as the user full "friendly" names for user groups.
            :param login: The name of the attribute within the SAML assertion to use as the login names for SAML users.
            :param name: The name of the attribute within the SAML assertion to use as the user full "friendly" names for SAML users.
            :param org: The name of the attribute within the SAML assertion to use as the user full "friendly" names for the users' organizations.
            :param role: The name of the attribute within the SAML assertion to use as the user roles.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_grafana as grafana
                
                assertion_attributes_property = grafana.CfnWorkspace.AssertionAttributesProperty(
                    email="email",
                    groups="groups",
                    login="login",
                    name="name",
                    org="org",
                    role="role"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4387bd8e2cd43a58dcded35e6a623f414176440fd8493d7360785860462565b9)
                check_type(argname="argument email", value=email, expected_type=type_hints["email"])
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument login", value=login, expected_type=type_hints["login"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument org", value=org, expected_type=type_hints["org"])
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email is not None:
                self._values["email"] = email
            if groups is not None:
                self._values["groups"] = groups
            if login is not None:
                self._values["login"] = login
            if name is not None:
                self._values["name"] = name
            if org is not None:
                self._values["org"] = org
            if role is not None:
                self._values["role"] = role

        @builtins.property
        def email(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the email names for SAML users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-email
            '''
            result = self._values.get("email")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def groups(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the user full "friendly" names for user groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def login(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the login names for SAML users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-login
            '''
            result = self._values.get("login")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the user full "friendly" names for SAML users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def org(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the user full "friendly" names for the users' organizations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-org
            '''
            result = self._values.get("org")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute within the SAML assertion to use as the user roles.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-assertionattributes.html#cfn-grafana-workspace-assertionattributes-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssertionAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_grafana.CfnWorkspace.IdpMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"url": "url", "xml": "xml"},
    )
    class IdpMetadataProperty:
        def __init__(
            self,
            *,
            url: typing.Optional[builtins.str] = None,
            xml: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure containing the identity provider (IdP) metadata used to integrate the identity provider with this workspace.

            You can specify the metadata either by providing a URL to its location in the ``url`` parameter, or by specifying the full metadata in XML format in the ``xml`` parameter. Specifying both will cause an error.

            :param url: The URL of the location containing the IdP metadata.
            :param xml: The full IdP metadata, in XML format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-idpmetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_grafana as grafana
                
                idp_metadata_property = grafana.CfnWorkspace.IdpMetadataProperty(
                    url="url",
                    xml="xml"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78298ba18538acddf3aaa2baafaa4bd1ddd7fb19f31868b396dec6227c866ea9)
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument xml", value=xml, expected_type=type_hints["xml"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if url is not None:
                self._values["url"] = url
            if xml is not None:
                self._values["xml"] = xml

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL of the location containing the IdP metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-idpmetadata.html#cfn-grafana-workspace-idpmetadata-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def xml(self) -> typing.Optional[builtins.str]:
            '''The full IdP metadata, in XML format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-idpmetadata.html#cfn-grafana-workspace-idpmetadata-xml
            '''
            result = self._values.get("xml")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdpMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_grafana.CfnWorkspace.NetworkAccessControlProperty",
        jsii_struct_bases=[],
        name_mapping={"prefix_list_ids": "prefixListIds", "vpce_ids": "vpceIds"},
    )
    class NetworkAccessControlProperty:
        def __init__(
            self,
            *,
            prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpce_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration settings for in-bound network access to your workspace.

            When this is configured, only listed IP addresses and VPC endpoints will be able to access your workspace. Standard Grafana authentication and authorization are still required.

            Access is granted to a caller that is in either the IP address list or the VPC endpoint list - they do not need to be in both.

            If this is not configured, or is removed, then all IP addresses and VPC endpoints are allowed. Standard Grafana authentication and authorization are still required.
            .. epigraph::

               While both ``prefixListIds`` and ``vpceIds`` are required, you can pass in an empty array of strings for either parameter if you do not want to allow any of that type.

               If both are passed as empty arrays, no traffic is allowed to the workspace, because only *explicitly* allowed connections are accepted.

            :param prefix_list_ids: An array of prefix list IDs. A prefix list is a list of CIDR ranges of IP addresses. The IP addresses specified are allowed to access your workspace. If the list is not included in the configuration (passed an empty array) then no IP addresses are allowed to access the workspace. You create a prefix list using the Amazon VPC console. Prefix list IDs have the format ``pl- *1a2b3c4d*`` . For more information about prefix lists, see `Group CIDR blocks using managed prefix lists <https://docs.aws.amazon.com/vpc/latest/userguide/managed-prefix-lists.html>`_ in the *Amazon Virtual Private Cloud User Guide* .
            :param vpce_ids: An array of Amazon VPC endpoint IDs for the workspace. You can create VPC endpoints to your Amazon Managed Grafana workspace for access from within a VPC. If a ``NetworkAccessConfiguration`` is specified then only VPC endpoints specified here are allowed to access the workspace. If you pass in an empty array of strings, then no VPCs are allowed to access the workspace. VPC endpoint IDs have the format ``vpce- *1a2b3c4d*`` . For more information about creating an interface VPC endpoint, see `Interface VPC endpoints <https://docs.aws.amazon.com/grafana/latest/userguide/VPC-endpoints>`_ in the *Amazon Managed Grafana User Guide* . .. epigraph:: The only VPC endpoints that can be specified here are interface VPC endpoints for Grafana workspaces (using the ``com.amazonaws.[region].grafana-workspace`` service endpoint). Other VPC endpoints are ignored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-networkaccesscontrol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_grafana as grafana
                
                network_access_control_property = grafana.CfnWorkspace.NetworkAccessControlProperty(
                    prefix_list_ids=["prefixListIds"],
                    vpce_ids=["vpceIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efd1691a9705a914952b93352808dac6392b9a705d46a0bbd446b01431c3aa5f)
                check_type(argname="argument prefix_list_ids", value=prefix_list_ids, expected_type=type_hints["prefix_list_ids"])
                check_type(argname="argument vpce_ids", value=vpce_ids, expected_type=type_hints["vpce_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if prefix_list_ids is not None:
                self._values["prefix_list_ids"] = prefix_list_ids
            if vpce_ids is not None:
                self._values["vpce_ids"] = vpce_ids

        @builtins.property
        def prefix_list_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of prefix list IDs.

            A prefix list is a list of CIDR ranges of IP addresses. The IP addresses specified are allowed to access your workspace. If the list is not included in the configuration (passed an empty array) then no IP addresses are allowed to access the workspace. You create a prefix list using the Amazon VPC console.

            Prefix list IDs have the format ``pl- *1a2b3c4d*`` .

            For more information about prefix lists, see `Group CIDR blocks using managed prefix lists <https://docs.aws.amazon.com/vpc/latest/userguide/managed-prefix-lists.html>`_ in the *Amazon Virtual Private Cloud User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-networkaccesscontrol.html#cfn-grafana-workspace-networkaccesscontrol-prefixlistids
            '''
            result = self._values.get("prefix_list_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpce_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of Amazon VPC endpoint IDs for the workspace.

            You can create VPC endpoints to your Amazon Managed Grafana workspace for access from within a VPC. If a ``NetworkAccessConfiguration`` is specified then only VPC endpoints specified here are allowed to access the workspace. If you pass in an empty array of strings, then no VPCs are allowed to access the workspace.

            VPC endpoint IDs have the format ``vpce- *1a2b3c4d*`` .

            For more information about creating an interface VPC endpoint, see `Interface VPC endpoints <https://docs.aws.amazon.com/grafana/latest/userguide/VPC-endpoints>`_ in the *Amazon Managed Grafana User Guide* .
            .. epigraph::

               The only VPC endpoints that can be specified here are interface VPC endpoints for Grafana workspaces (using the ``com.amazonaws.[region].grafana-workspace`` service endpoint). Other VPC endpoints are ignored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-networkaccesscontrol.html#cfn-grafana-workspace-networkaccesscontrol-vpceids
            '''
            result = self._values.get("vpce_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkAccessControlProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_grafana.CfnWorkspace.RoleValuesProperty",
        jsii_struct_bases=[],
        name_mapping={"admin": "admin", "editor": "editor"},
    )
    class RoleValuesProperty:
        def __init__(
            self,
            *,
            admin: typing.Optional[typing.Sequence[builtins.str]] = None,
            editor: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure defines which groups defined in the SAML assertion attribute are to be mapped to the Grafana ``Admin`` and ``Editor`` roles in the workspace.

            SAML authenticated users not part of ``Admin`` or ``Editor`` role groups have ``Viewer`` permission over the workspace.

            :param admin: A list of groups from the SAML assertion attribute to grant the Grafana ``Admin`` role to.
            :param editor: A list of groups from the SAML assertion attribute to grant the Grafana ``Editor`` role to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-rolevalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_grafana as grafana
                
                role_values_property = grafana.CfnWorkspace.RoleValuesProperty(
                    admin=["admin"],
                    editor=["editor"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b4d72e8c31cb301c66d1ab5597d3d88b29b849d4b68f983f6902541a580c405)
                check_type(argname="argument admin", value=admin, expected_type=type_hints["admin"])
                check_type(argname="argument editor", value=editor, expected_type=type_hints["editor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if admin is not None:
                self._values["admin"] = admin
            if editor is not None:
                self._values["editor"] = editor

        @builtins.property
        def admin(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of groups from the SAML assertion attribute to grant the Grafana ``Admin`` role to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-rolevalues.html#cfn-grafana-workspace-rolevalues-admin
            '''
            result = self._values.get("admin")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def editor(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of groups from the SAML assertion attribute to grant the Grafana ``Editor`` role to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-rolevalues.html#cfn-grafana-workspace-rolevalues-editor
            '''
            result = self._values.get("editor")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoleValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_grafana.CfnWorkspace.SamlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "idp_metadata": "idpMetadata",
            "allowed_organizations": "allowedOrganizations",
            "assertion_attributes": "assertionAttributes",
            "login_validity_duration": "loginValidityDuration",
            "role_values": "roleValues",
        },
    )
    class SamlConfigurationProperty:
        def __init__(
            self,
            *,
            idp_metadata: typing.Union[typing.Union["CfnWorkspace.IdpMetadataProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            allowed_organizations: typing.Optional[typing.Sequence[builtins.str]] = None,
            assertion_attributes: typing.Optional[typing.Union[typing.Union["CfnWorkspace.AssertionAttributesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            login_validity_duration: typing.Optional[jsii.Number] = None,
            role_values: typing.Optional[typing.Union[typing.Union["CfnWorkspace.RoleValuesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''A structure containing information about how this workspace works with SAML.

            :param idp_metadata: A structure containing the identity provider (IdP) metadata used to integrate the identity provider with this workspace.
            :param allowed_organizations: Lists which organizations defined in the SAML assertion are allowed to use the Amazon Managed Grafana workspace. If this is empty, all organizations in the assertion attribute have access.
            :param assertion_attributes: A structure that defines which attributes in the SAML assertion are to be used to define information about the users authenticated by that IdP to use the workspace.
            :param login_validity_duration: How long a sign-on session by a SAML user is valid, before the user has to sign on again.
            :param role_values: A structure containing arrays that map group names in the SAML assertion to the Grafana ``Admin`` and ``Editor`` roles in the workspace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_grafana as grafana
                
                saml_configuration_property = grafana.CfnWorkspace.SamlConfigurationProperty(
                    idp_metadata=grafana.CfnWorkspace.IdpMetadataProperty(
                        url="url",
                        xml="xml"
                    ),
                
                    # the properties below are optional
                    allowed_organizations=["allowedOrganizations"],
                    assertion_attributes=grafana.CfnWorkspace.AssertionAttributesProperty(
                        email="email",
                        groups="groups",
                        login="login",
                        name="name",
                        org="org",
                        role="role"
                    ),
                    login_validity_duration=123,
                    role_values=grafana.CfnWorkspace.RoleValuesProperty(
                        admin=["admin"],
                        editor=["editor"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c03af6387019ef728cfebe307e6e9d79fa2879f803f1b28db04e08ce94c6b4a)
                check_type(argname="argument idp_metadata", value=idp_metadata, expected_type=type_hints["idp_metadata"])
                check_type(argname="argument allowed_organizations", value=allowed_organizations, expected_type=type_hints["allowed_organizations"])
                check_type(argname="argument assertion_attributes", value=assertion_attributes, expected_type=type_hints["assertion_attributes"])
                check_type(argname="argument login_validity_duration", value=login_validity_duration, expected_type=type_hints["login_validity_duration"])
                check_type(argname="argument role_values", value=role_values, expected_type=type_hints["role_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "idp_metadata": idp_metadata,
            }
            if allowed_organizations is not None:
                self._values["allowed_organizations"] = allowed_organizations
            if assertion_attributes is not None:
                self._values["assertion_attributes"] = assertion_attributes
            if login_validity_duration is not None:
                self._values["login_validity_duration"] = login_validity_duration
            if role_values is not None:
                self._values["role_values"] = role_values

        @builtins.property
        def idp_metadata(
            self,
        ) -> typing.Union["CfnWorkspace.IdpMetadataProperty", _IResolvable_a771d0ef]:
            '''A structure containing the identity provider (IdP) metadata used to integrate the identity provider with this workspace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-idpmetadata
            '''
            result = self._values.get("idp_metadata")
            assert result is not None, "Required property 'idp_metadata' is missing"
            return typing.cast(typing.Union["CfnWorkspace.IdpMetadataProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def allowed_organizations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Lists which organizations defined in the SAML assertion are allowed to use the Amazon Managed Grafana workspace.

            If this is empty, all organizations in the assertion attribute have access.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-allowedorganizations
            '''
            result = self._values.get("allowed_organizations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def assertion_attributes(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkspace.AssertionAttributesProperty", _IResolvable_a771d0ef]]:
            '''A structure that defines which attributes in the SAML assertion are to be used to define information about the users authenticated by that IdP to use the workspace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-assertionattributes
            '''
            result = self._values.get("assertion_attributes")
            return typing.cast(typing.Optional[typing.Union["CfnWorkspace.AssertionAttributesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def login_validity_duration(self) -> typing.Optional[jsii.Number]:
            '''How long a sign-on session by a SAML user is valid, before the user has to sign on again.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-loginvalidityduration
            '''
            result = self._values.get("login_validity_duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def role_values(
            self,
        ) -> typing.Optional[typing.Union["CfnWorkspace.RoleValuesProperty", _IResolvable_a771d0ef]]:
            '''A structure containing arrays that map group names in the SAML assertion to the Grafana ``Admin`` and ``Editor`` roles in the workspace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-samlconfiguration.html#cfn-grafana-workspace-samlconfiguration-rolevalues
            '''
            result = self._values.get("role_values")
            return typing.cast(typing.Optional[typing.Union["CfnWorkspace.RoleValuesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_grafana.CfnWorkspace.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Sequence[builtins.str],
            subnet_ids: typing.Sequence[builtins.str],
        ) -> None:
            '''The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to.

            .. epigraph::

               Provided ``securityGroupIds`` and ``subnetIds`` must be part of the same VPC.

               Connecting to a private VPC is not yet available in the Asia Pacific (Seoul) Region (ap-northeast-2).

            :param security_group_ids: The list of Amazon EC2 security group IDs attached to the Amazon VPC for your Grafana workspace to connect. Duplicates not allowed. *Array Members* : Minimum number of 1 items. Maximum number of 5 items. *Length* : Minimum length of 0. Maximum length of 255.
            :param subnet_ids: The list of Amazon EC2 subnet IDs created in the Amazon VPC for your Grafana workspace to connect. Duplicates not allowed. *Array Members* : Minimum number of 2 items. Maximum number of 6 items. *Length* : Minimum length of 0. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_grafana as grafana
                
                vpc_configuration_property = grafana.CfnWorkspace.VpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d63cf4c8e5e6dcfc5f0863271641bb5b98c35b5bf68eb3f25e5ba1e6f58de41d)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }

        @builtins.property
        def security_group_ids(self) -> typing.List[builtins.str]:
            '''The list of Amazon EC2 security group IDs attached to the Amazon VPC for your Grafana workspace to connect.

            Duplicates not allowed.

            *Array Members* : Minimum number of 1 items. Maximum number of 5 items.

            *Length* : Minimum length of 0. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-vpcconfiguration.html#cfn-grafana-workspace-vpcconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            assert result is not None, "Required property 'security_group_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_ids(self) -> typing.List[builtins.str]:
            '''The list of Amazon EC2 subnet IDs created in the Amazon VPC for your Grafana workspace to connect.

            Duplicates not allowed.

            *Array Members* : Minimum number of 2 items. Maximum number of 6 items.

            *Length* : Minimum length of 0. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-grafana-workspace-vpcconfiguration.html#cfn-grafana-workspace-vpcconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            assert result is not None, "Required property 'subnet_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_grafana.CfnWorkspaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_access_type": "accountAccessType",
        "authentication_providers": "authenticationProviders",
        "permission_type": "permissionType",
        "client_token": "clientToken",
        "data_sources": "dataSources",
        "description": "description",
        "grafana_version": "grafanaVersion",
        "name": "name",
        "network_access_control": "networkAccessControl",
        "notification_destinations": "notificationDestinations",
        "organizational_units": "organizationalUnits",
        "organization_role_name": "organizationRoleName",
        "role_arn": "roleArn",
        "saml_configuration": "samlConfiguration",
        "stack_set_name": "stackSetName",
        "vpc_configuration": "vpcConfiguration",
    },
)
class CfnWorkspaceProps:
    def __init__(
        self,
        *,
        account_access_type: builtins.str,
        authentication_providers: typing.Sequence[builtins.str],
        permission_type: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        grafana_version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_access_control: typing.Optional[typing.Union[typing.Union[CfnWorkspace.NetworkAccessControlProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        notification_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        organizational_units: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_role_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        saml_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.SamlConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stack_set_name: typing.Optional[builtins.str] = None,
        vpc_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkspace``.

        :param account_access_type: Specifies whether the workspace can access AWS resources in this AWS account only, or whether it can also access AWS resources in other accounts in the same organization. If this is ``ORGANIZATION`` , the ``OrganizationalUnits`` parameter specifies which organizational units the workspace can access.
        :param authentication_providers: Specifies whether this workspace uses SAML 2.0, AWS IAM Identity Center (successor to AWS Single Sign-On) , or both to authenticate users for using the Grafana console within a workspace. For more information, see `User authentication in Amazon Managed Grafana <https://docs.aws.amazon.com/grafana/latest/userguide/authentication-in-AMG.html>`_ .
        :param permission_type: If this is ``SERVICE_MANAGED`` , and the workplace was created through the Amazon Managed Grafana console, then Amazon Managed Grafana automatically creates the IAM roles and provisions the permissions that the workspace needs to use AWS data sources and notification channels. If this is ``CUSTOMER_MANAGED`` , you must manage those roles and permissions yourself. If you are working with a workspace in a member account of an organization and that account is not a delegated administrator account, and you want the workspace to access data sources in other AWS accounts in the organization, this parameter must be set to ``CUSTOMER_MANAGED`` . For more information about converting between customer and service managed, see `Managing permissions for data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-datasource-and-notification.html>`_ . For more information about the roles and permissions that must be managed for customer managed workspaces, see `Amazon Managed Grafana permissions and policies for AWS data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-manage-permissions.html>`_
        :param client_token: A unique, case-sensitive, user-provided identifier to ensure the idempotency of the request.
        :param data_sources: Specifies the AWS data sources that have been configured to have IAM roles and permissions created to allow Amazon Managed Grafana to read data from these sources. This list is only used when the workspace was created through the AWS console, and the ``permissionType`` is ``SERVICE_MANAGED`` .
        :param description: The user-defined description of the workspace.
        :param grafana_version: Specifies the version of Grafana to support in the new workspace. Supported values are ``8.4`` and ``9.4`` .
        :param name: The name of the workspace.
        :param network_access_control: The configuration settings for network access to your workspace.
        :param notification_destinations: The AWS notification channels that Amazon Managed Grafana can automatically create IAM roles and permissions for, to allow Amazon Managed Grafana to use these channels.
        :param organizational_units: Specifies the organizational units that this workspace is allowed to use data sources from, if this workspace is in an account that is part of an organization.
        :param organization_role_name: The name of the IAM role that is used to access resources through Organizations .
        :param role_arn: The IAM role that grants permissions to the AWS resources that the workspace will view data from. This role must already exist.
        :param saml_configuration: If the workspace uses SAML, use this structure to map SAML assertion attributes to workspace user information and define which groups in the assertion attribute are to have the ``Admin`` and ``Editor`` roles in the workspace.
        :param stack_set_name: The name of the AWS CloudFormation stack set that is used to generate IAM roles to be used for this workspace.
        :param vpc_configuration: The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to. .. epigraph:: Connecting to a private VPC is not yet available in the Asia Pacific (Seoul) Region (ap-northeast-2).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_grafana as grafana
            
            cfn_workspace_props = grafana.CfnWorkspaceProps(
                account_access_type="accountAccessType",
                authentication_providers=["authenticationProviders"],
                permission_type="permissionType",
            
                # the properties below are optional
                client_token="clientToken",
                data_sources=["dataSources"],
                description="description",
                grafana_version="grafanaVersion",
                name="name",
                network_access_control=grafana.CfnWorkspace.NetworkAccessControlProperty(
                    prefix_list_ids=["prefixListIds"],
                    vpce_ids=["vpceIds"]
                ),
                notification_destinations=["notificationDestinations"],
                organizational_units=["organizationalUnits"],
                organization_role_name="organizationRoleName",
                role_arn="roleArn",
                saml_configuration=grafana.CfnWorkspace.SamlConfigurationProperty(
                    idp_metadata=grafana.CfnWorkspace.IdpMetadataProperty(
                        url="url",
                        xml="xml"
                    ),
            
                    # the properties below are optional
                    allowed_organizations=["allowedOrganizations"],
                    assertion_attributes=grafana.CfnWorkspace.AssertionAttributesProperty(
                        email="email",
                        groups="groups",
                        login="login",
                        name="name",
                        org="org",
                        role="role"
                    ),
                    login_validity_duration=123,
                    role_values=grafana.CfnWorkspace.RoleValuesProperty(
                        admin=["admin"],
                        editor=["editor"]
                    )
                ),
                stack_set_name="stackSetName",
                vpc_configuration=grafana.CfnWorkspace.VpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148853e9b1f7f60342bae9830d7db601f4496adb7b7a4888a65379d2fc8b03b7)
            check_type(argname="argument account_access_type", value=account_access_type, expected_type=type_hints["account_access_type"])
            check_type(argname="argument authentication_providers", value=authentication_providers, expected_type=type_hints["authentication_providers"])
            check_type(argname="argument permission_type", value=permission_type, expected_type=type_hints["permission_type"])
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument grafana_version", value=grafana_version, expected_type=type_hints["grafana_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_access_control", value=network_access_control, expected_type=type_hints["network_access_control"])
            check_type(argname="argument notification_destinations", value=notification_destinations, expected_type=type_hints["notification_destinations"])
            check_type(argname="argument organizational_units", value=organizational_units, expected_type=type_hints["organizational_units"])
            check_type(argname="argument organization_role_name", value=organization_role_name, expected_type=type_hints["organization_role_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument saml_configuration", value=saml_configuration, expected_type=type_hints["saml_configuration"])
            check_type(argname="argument stack_set_name", value=stack_set_name, expected_type=type_hints["stack_set_name"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_access_type": account_access_type,
            "authentication_providers": authentication_providers,
            "permission_type": permission_type,
        }
        if client_token is not None:
            self._values["client_token"] = client_token
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if description is not None:
            self._values["description"] = description
        if grafana_version is not None:
            self._values["grafana_version"] = grafana_version
        if name is not None:
            self._values["name"] = name
        if network_access_control is not None:
            self._values["network_access_control"] = network_access_control
        if notification_destinations is not None:
            self._values["notification_destinations"] = notification_destinations
        if organizational_units is not None:
            self._values["organizational_units"] = organizational_units
        if organization_role_name is not None:
            self._values["organization_role_name"] = organization_role_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if saml_configuration is not None:
            self._values["saml_configuration"] = saml_configuration
        if stack_set_name is not None:
            self._values["stack_set_name"] = stack_set_name
        if vpc_configuration is not None:
            self._values["vpc_configuration"] = vpc_configuration

    @builtins.property
    def account_access_type(self) -> builtins.str:
        '''Specifies whether the workspace can access AWS resources in this AWS account only, or whether it can also access AWS resources in other accounts in the same organization.

        If this is ``ORGANIZATION`` , the ``OrganizationalUnits`` parameter specifies which organizational units the workspace can access.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-accountaccesstype
        '''
        result = self._values.get("account_access_type")
        assert result is not None, "Required property 'account_access_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_providers(self) -> typing.List[builtins.str]:
        '''Specifies whether this workspace uses SAML 2.0, AWS IAM Identity Center (successor to AWS Single Sign-On) , or both to authenticate users for using the Grafana console within a workspace. For more information, see `User authentication in Amazon Managed Grafana <https://docs.aws.amazon.com/grafana/latest/userguide/authentication-in-AMG.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-authenticationproviders
        '''
        result = self._values.get("authentication_providers")
        assert result is not None, "Required property 'authentication_providers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def permission_type(self) -> builtins.str:
        '''If this is ``SERVICE_MANAGED`` , and the workplace was created through the Amazon Managed Grafana console, then Amazon Managed Grafana automatically creates the IAM roles and provisions the permissions that the workspace needs to use AWS data sources and notification channels.

        If this is ``CUSTOMER_MANAGED`` , you must manage those roles and permissions yourself.

        If you are working with a workspace in a member account of an organization and that account is not a delegated administrator account, and you want the workspace to access data sources in other AWS accounts in the organization, this parameter must be set to ``CUSTOMER_MANAGED`` .

        For more information about converting between customer and service managed, see `Managing permissions for data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-datasource-and-notification.html>`_ . For more information about the roles and permissions that must be managed for customer managed workspaces, see `Amazon Managed Grafana permissions and policies for AWS data sources and notification channels <https://docs.aws.amazon.com/grafana/latest/userguide/AMG-manage-permissions.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-permissiontype
        '''
        result = self._values.get("permission_type")
        assert result is not None, "Required property 'permission_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''A unique, case-sensitive, user-provided identifier to ensure the idempotency of the request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the AWS data sources that have been configured to have IAM roles and permissions created to allow Amazon Managed Grafana to read data from these sources.

        This list is only used when the workspace was created through the AWS console, and the ``permissionType`` is ``SERVICE_MANAGED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-datasources
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-defined description of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the version of Grafana to support in the new workspace.

        Supported values are ``8.4`` and ``9.4`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-grafanaversion
        '''
        result = self._values.get("grafana_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_access_control(
        self,
    ) -> typing.Optional[typing.Union[CfnWorkspace.NetworkAccessControlProperty, _IResolvable_a771d0ef]]:
        '''The configuration settings for network access to your workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-networkaccesscontrol
        '''
        result = self._values.get("network_access_control")
        return typing.cast(typing.Optional[typing.Union[CfnWorkspace.NetworkAccessControlProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def notification_destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The AWS notification channels that Amazon Managed Grafana can automatically create IAM roles and permissions for, to allow Amazon Managed Grafana to use these channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-notificationdestinations
        '''
        result = self._values.get("notification_destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organizational_units(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the organizational units that this workspace is allowed to use data sources from, if this workspace is in an account that is part of an organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-organizationalunits
        '''
        result = self._values.get("organizational_units")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organization_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role that is used to access resources through Organizations .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-organizationrolename
        '''
        result = self._values.get("organization_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM role that grants permissions to the AWS resources that the workspace will view data from.

        This role must already exist.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnWorkspace.SamlConfigurationProperty, _IResolvable_a771d0ef]]:
        '''If the workspace uses SAML, use this structure to map SAML assertion attributes to workspace user information and define which groups in the assertion attribute are to have the ``Admin`` and ``Editor`` roles in the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-samlconfiguration
        '''
        result = self._values.get("saml_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnWorkspace.SamlConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def stack_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AWS CloudFormation stack set that is used to generate IAM roles to be used for this workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-stacksetname
        '''
        result = self._values.get("stack_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnWorkspace.VpcConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to.

        .. epigraph::

           Connecting to a private VPC is not yet available in the Asia Pacific (Seoul) Region (ap-northeast-2).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-grafana-workspace.html#cfn-grafana-workspace-vpcconfiguration
        '''
        result = self._values.get("vpc_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnWorkspace.VpcConfigurationProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnWorkspace",
    "CfnWorkspaceProps",
]

publication.publish()

def _typecheckingstub__6713a860a65fba5b301856d33d40253246fd4347f380275e14aadf8af43377fa(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    account_access_type: builtins.str,
    authentication_providers: typing.Sequence[builtins.str],
    permission_type: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    grafana_version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_access_control: typing.Optional[typing.Union[typing.Union[CfnWorkspace.NetworkAccessControlProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    notification_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    organizational_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_role_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    saml_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.SamlConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stack_set_name: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f3b31b994f027eb35968aaeeaa06ffe9e6686ddca81209d5436314b4ddfe40(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66a4a24b4b34122522647798ff6da87f317846efe9bb9424d121bc24060096e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c68de275d25eb8faf6f7971c01fc2620e87d0b5931b025162966f7d9981d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2f7239a8e347951c9d5b5d6df669b01c9b28d7b6d05d785d709c7f7e6618a8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029fe3cac156670ed5fad3878580a59a54c247bacb993be0777c8a5de227cace(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3099f1f8ab1eda4d09b2968b374aae2d351223b265786221dd18b860250f80(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d4b90ca0507d297d5e8b2f0e4aa92672d55a80e7bdf2e6323e305da994d3bc(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22189fc3dc23326eb415a1c005563cc19cc08ff7cf643d1f0912e772268f0dd6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cc8d3e49aef6f16db5367fbdaa5f7c23fbc86731c21ae8de05131832e87978(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f1028f838a43ae15fe822ca3d08f7ddd0a1e962af43f23d82d74d3d93765d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b183d43621972c9790f4442b52be9c7c36219cb429a20e8850f92b4c78df6d5(
    value: typing.Optional[typing.Union[CfnWorkspace.NetworkAccessControlProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85473b71d8335b413f0fd3d2f72098519854cec58129a60291ff73a3fbb96889(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15850135d2afda880809758fce39dbcd2e304d2255997eb82684d65b64c782e3(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4321893828d23d1459f7af82bbb41106aa8060ce00c4dd0100604350778928e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f75f8fed3e2455955925e5303457da6092cbf59bfa124f1902498df455ce78(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6161aafe79f9227dd913cba72aa00b63f72a50936bd4b8db01cc3bbeca7a6a9b(
    value: typing.Optional[typing.Union[CfnWorkspace.SamlConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e19e83f9d03b79ab108c9d09aa57d05861a1b0ca1e3586712c2bbed978c72bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826fbeabf3caadecfa533a42add280ce7510442edb21af4e5045b1e18cf8f136(
    value: typing.Optional[typing.Union[CfnWorkspace.VpcConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4387bd8e2cd43a58dcded35e6a623f414176440fd8493d7360785860462565b9(
    *,
    email: typing.Optional[builtins.str] = None,
    groups: typing.Optional[builtins.str] = None,
    login: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78298ba18538acddf3aaa2baafaa4bd1ddd7fb19f31868b396dec6227c866ea9(
    *,
    url: typing.Optional[builtins.str] = None,
    xml: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd1691a9705a914952b93352808dac6392b9a705d46a0bbd446b01431c3aa5f(
    *,
    prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpce_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4d72e8c31cb301c66d1ab5597d3d88b29b849d4b68f983f6902541a580c405(
    *,
    admin: typing.Optional[typing.Sequence[builtins.str]] = None,
    editor: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c03af6387019ef728cfebe307e6e9d79fa2879f803f1b28db04e08ce94c6b4a(
    *,
    idp_metadata: typing.Union[typing.Union[CfnWorkspace.IdpMetadataProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    allowed_organizations: typing.Optional[typing.Sequence[builtins.str]] = None,
    assertion_attributes: typing.Optional[typing.Union[typing.Union[CfnWorkspace.AssertionAttributesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    login_validity_duration: typing.Optional[jsii.Number] = None,
    role_values: typing.Optional[typing.Union[typing.Union[CfnWorkspace.RoleValuesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63cf4c8e5e6dcfc5f0863271641bb5b98c35b5bf68eb3f25e5ba1e6f58de41d(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148853e9b1f7f60342bae9830d7db601f4496adb7b7a4888a65379d2fc8b03b7(
    *,
    account_access_type: builtins.str,
    authentication_providers: typing.Sequence[builtins.str],
    permission_type: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    grafana_version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_access_control: typing.Optional[typing.Union[typing.Union[CfnWorkspace.NetworkAccessControlProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    notification_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    organizational_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_role_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    saml_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.SamlConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stack_set_name: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass
