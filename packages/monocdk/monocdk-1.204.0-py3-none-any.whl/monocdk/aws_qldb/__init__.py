'''
# AWS::QLDB Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as qldb
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for QLDB construct libraries](https://constructs.dev/search?q=qldb)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::QLDB resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_QLDB.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::QLDB](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_QLDB.html).

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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnLedger(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_qldb.CfnLedger",
):
    '''A CloudFormation ``AWS::QLDB::Ledger``.

    The ``AWS::QLDB::Ledger`` resource specifies a new Amazon Quantum Ledger Database (Amazon QLDB) ledger in your AWS account . Amazon QLDB is a fully managed ledger database that provides a transparent, immutable, and cryptographically verifiable transaction log owned by a central trusted authority. You can use QLDB to track all application data changes, and maintain a complete and verifiable history of changes over time.

    For more information, see `CreateLedger <https://docs.aws.amazon.com/qldb/latest/developerguide/API_CreateLedger.html>`_ in the *Amazon QLDB API Reference* .

    :cloudformationResource: AWS::QLDB::Ledger
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_qldb as qldb
        
        cfn_ledger = qldb.CfnLedger(self, "MyCfnLedger",
            permissions_mode="permissionsMode",
        
            # the properties below are optional
            deletion_protection=False,
            kms_key="kmsKey",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        permissions_mode: builtins.str,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::QLDB::Ledger``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param permissions_mode: The permissions mode to assign to the ledger that you want to create. This parameter can have one of the following values: - ``ALLOW_ALL`` : A legacy permissions mode that enables access control with API-level granularity for ledgers. This mode allows users who have the ``SendCommand`` API permission for this ledger to run all PartiQL commands (hence, ``ALLOW_ALL`` ) on any tables in the specified ledger. This mode disregards any table-level or command-level IAM permissions policies that you create for the ledger. - ``STANDARD`` : ( *Recommended* ) A permissions mode that enables access control with finer granularity for ledgers, tables, and PartiQL commands. By default, this mode denies all user requests to run any PartiQL commands on any tables in this ledger. To allow PartiQL commands to run, you must create IAM permissions policies for specific table resources and PartiQL actions, in addition to the ``SendCommand`` API permission for the ledger. For information, see `Getting started with the standard permissions mode <https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started-standard-mode.html>`_ in the *Amazon QLDB Developer Guide* . .. epigraph:: We strongly recommend using the ``STANDARD`` permissions mode to maximize the security of your ledger data.
        :param deletion_protection: Specifies whether the ledger is protected from being deleted by any user. If not defined during ledger creation, this feature is enabled ( ``true`` ) by default. If deletion protection is enabled, you must first disable it before you can delete the ledger. You can disable it by calling the ``UpdateLedger`` operation to set this parameter to ``false`` .
        :param kms_key: The key in AWS Key Management Service ( AWS KMS ) to use for encryption of data at rest in the ledger. For more information, see `Encryption at rest <https://docs.aws.amazon.com/qldb/latest/developerguide/encryption-at-rest.html>`_ in the *Amazon QLDB Developer Guide* . Use one of the following options to specify this parameter: - ``AWS_OWNED_KMS_KEY`` : Use an AWS KMS key that is owned and managed by AWS on your behalf. - *Undefined* : By default, use an AWS owned KMS key. - *A valid symmetric customer managed KMS key* : Use the specified symmetric encryption KMS key in your account that you create, own, and manage. Amazon QLDB does not support asymmetric keys. For more information, see `Using symmetric and asymmetric keys <https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* . To specify a customer managed KMS key, you can use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. When using an alias name, prefix it with ``"alias/"`` . To specify a key in a different AWS account , you must use the key ARN or alias ARN. For example: - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` - Alias name: ``alias/ExampleAlias`` - Alias ARN: ``arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias`` For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .
        :param name: The name of the ledger that you want to create. The name must be unique among all of the ledgers in your AWS account in the current Region. Naming constraints for ledger names are defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970cff924d6fb5dcd5e22d16660e973e31d588be7c40b2edc2862613767aee75)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLedgerProps(
            permissions_mode=permissions_mode,
            deletion_protection=deletion_protection,
            kms_key=kms_key,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a0aa067d365e16d9b4399209f3eb7d8c399a4f065b0c225db447ddf9a65a8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9240029664025ad9734bca068c8191e9bb06a20e94cc623cdb188d943b739fe9)
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="permissionsMode")
    def permissions_mode(self) -> builtins.str:
        '''The permissions mode to assign to the ledger that you want to create.

        This parameter can have one of the following values:

        - ``ALLOW_ALL`` : A legacy permissions mode that enables access control with API-level granularity for ledgers.

        This mode allows users who have the ``SendCommand`` API permission for this ledger to run all PartiQL commands (hence, ``ALLOW_ALL`` ) on any tables in the specified ledger. This mode disregards any table-level or command-level IAM permissions policies that you create for the ledger.

        - ``STANDARD`` : ( *Recommended* ) A permissions mode that enables access control with finer granularity for ledgers, tables, and PartiQL commands.

        By default, this mode denies all user requests to run any PartiQL commands on any tables in this ledger. To allow PartiQL commands to run, you must create IAM permissions policies for specific table resources and PartiQL actions, in addition to the ``SendCommand`` API permission for the ledger. For information, see `Getting started with the standard permissions mode <https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started-standard-mode.html>`_ in the *Amazon QLDB Developer Guide* .
        .. epigraph::

           We strongly recommend using the ``STANDARD`` permissions mode to maximize the security of your ledger data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-permissionsmode
        '''
        return typing.cast(builtins.str, jsii.get(self, "permissionsMode"))

    @permissions_mode.setter
    def permissions_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5155d59953c1330619e26c320be67d95d4717dcaa93a5a8897c4e63ba238a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsMode", value)

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the ledger is protected from being deleted by any user.

        If not defined during ledger creation, this feature is enabled ( ``true`` ) by default.

        If deletion protection is enabled, you must first disable it before you can delete the ledger. You can disable it by calling the ``UpdateLedger`` operation to set this parameter to ``false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-deletionprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a0defd0b06fa9a060becf3c260ad8e1de0739a1ed071bdb45994796d84b007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The key in AWS Key Management Service ( AWS KMS ) to use for encryption of data at rest in the ledger.

        For more information, see `Encryption at rest <https://docs.aws.amazon.com/qldb/latest/developerguide/encryption-at-rest.html>`_ in the *Amazon QLDB Developer Guide* .

        Use one of the following options to specify this parameter:

        - ``AWS_OWNED_KMS_KEY`` : Use an AWS KMS key that is owned and managed by AWS on your behalf.
        - *Undefined* : By default, use an AWS owned KMS key.
        - *A valid symmetric customer managed KMS key* : Use the specified symmetric encryption KMS key in your account that you create, own, and manage.

        Amazon QLDB does not support asymmetric keys. For more information, see `Using symmetric and asymmetric keys <https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

        To specify a customer managed KMS key, you can use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. When using an alias name, prefix it with ``"alias/"`` . To specify a key in a different AWS account , you must use the key ARN or alias ARN.

        For example:

        - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab``
        - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``
        - Alias name: ``alias/ExampleAlias``
        - Alias ARN: ``arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias``

        For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-kmskey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9637776850095a3b8e82739e01c453d618bdb174a075ada3777fe1b53c4fbbed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ledger that you want to create.

        The name must be unique among all of the ledgers in your AWS account in the current Region.

        Naming constraints for ledger names are defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2878f1010ee198cf4445275a213e206ce984c4afe0ddea0c00d1409addd5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_qldb.CfnLedgerProps",
    jsii_struct_bases=[],
    name_mapping={
        "permissions_mode": "permissionsMode",
        "deletion_protection": "deletionProtection",
        "kms_key": "kmsKey",
        "name": "name",
        "tags": "tags",
    },
)
class CfnLedgerProps:
    def __init__(
        self,
        *,
        permissions_mode: builtins.str,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLedger``.

        :param permissions_mode: The permissions mode to assign to the ledger that you want to create. This parameter can have one of the following values: - ``ALLOW_ALL`` : A legacy permissions mode that enables access control with API-level granularity for ledgers. This mode allows users who have the ``SendCommand`` API permission for this ledger to run all PartiQL commands (hence, ``ALLOW_ALL`` ) on any tables in the specified ledger. This mode disregards any table-level or command-level IAM permissions policies that you create for the ledger. - ``STANDARD`` : ( *Recommended* ) A permissions mode that enables access control with finer granularity for ledgers, tables, and PartiQL commands. By default, this mode denies all user requests to run any PartiQL commands on any tables in this ledger. To allow PartiQL commands to run, you must create IAM permissions policies for specific table resources and PartiQL actions, in addition to the ``SendCommand`` API permission for the ledger. For information, see `Getting started with the standard permissions mode <https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started-standard-mode.html>`_ in the *Amazon QLDB Developer Guide* . .. epigraph:: We strongly recommend using the ``STANDARD`` permissions mode to maximize the security of your ledger data.
        :param deletion_protection: Specifies whether the ledger is protected from being deleted by any user. If not defined during ledger creation, this feature is enabled ( ``true`` ) by default. If deletion protection is enabled, you must first disable it before you can delete the ledger. You can disable it by calling the ``UpdateLedger`` operation to set this parameter to ``false`` .
        :param kms_key: The key in AWS Key Management Service ( AWS KMS ) to use for encryption of data at rest in the ledger. For more information, see `Encryption at rest <https://docs.aws.amazon.com/qldb/latest/developerguide/encryption-at-rest.html>`_ in the *Amazon QLDB Developer Guide* . Use one of the following options to specify this parameter: - ``AWS_OWNED_KMS_KEY`` : Use an AWS KMS key that is owned and managed by AWS on your behalf. - *Undefined* : By default, use an AWS owned KMS key. - *A valid symmetric customer managed KMS key* : Use the specified symmetric encryption KMS key in your account that you create, own, and manage. Amazon QLDB does not support asymmetric keys. For more information, see `Using symmetric and asymmetric keys <https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* . To specify a customer managed KMS key, you can use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. When using an alias name, prefix it with ``"alias/"`` . To specify a key in a different AWS account , you must use the key ARN or alias ARN. For example: - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` - Alias name: ``alias/ExampleAlias`` - Alias ARN: ``arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias`` For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .
        :param name: The name of the ledger that you want to create. The name must be unique among all of the ledgers in your AWS account in the current Region. Naming constraints for ledger names are defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_qldb as qldb
            
            cfn_ledger_props = qldb.CfnLedgerProps(
                permissions_mode="permissionsMode",
            
                # the properties below are optional
                deletion_protection=False,
                kms_key="kmsKey",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cab1894b3432ea7571f97e9ae6a6ccdf31ec25c5bf9fcca3354c88dc3d7c37c)
            check_type(argname="argument permissions_mode", value=permissions_mode, expected_type=type_hints["permissions_mode"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permissions_mode": permissions_mode,
        }
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def permissions_mode(self) -> builtins.str:
        '''The permissions mode to assign to the ledger that you want to create.

        This parameter can have one of the following values:

        - ``ALLOW_ALL`` : A legacy permissions mode that enables access control with API-level granularity for ledgers.

        This mode allows users who have the ``SendCommand`` API permission for this ledger to run all PartiQL commands (hence, ``ALLOW_ALL`` ) on any tables in the specified ledger. This mode disregards any table-level or command-level IAM permissions policies that you create for the ledger.

        - ``STANDARD`` : ( *Recommended* ) A permissions mode that enables access control with finer granularity for ledgers, tables, and PartiQL commands.

        By default, this mode denies all user requests to run any PartiQL commands on any tables in this ledger. To allow PartiQL commands to run, you must create IAM permissions policies for specific table resources and PartiQL actions, in addition to the ``SendCommand`` API permission for the ledger. For information, see `Getting started with the standard permissions mode <https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started-standard-mode.html>`_ in the *Amazon QLDB Developer Guide* .
        .. epigraph::

           We strongly recommend using the ``STANDARD`` permissions mode to maximize the security of your ledger data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-permissionsmode
        '''
        result = self._values.get("permissions_mode")
        assert result is not None, "Required property 'permissions_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the ledger is protected from being deleted by any user.

        If not defined during ledger creation, this feature is enabled ( ``true`` ) by default.

        If deletion protection is enabled, you must first disable it before you can delete the ledger. You can disable it by calling the ``UpdateLedger`` operation to set this parameter to ``false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The key in AWS Key Management Service ( AWS KMS ) to use for encryption of data at rest in the ledger.

        For more information, see `Encryption at rest <https://docs.aws.amazon.com/qldb/latest/developerguide/encryption-at-rest.html>`_ in the *Amazon QLDB Developer Guide* .

        Use one of the following options to specify this parameter:

        - ``AWS_OWNED_KMS_KEY`` : Use an AWS KMS key that is owned and managed by AWS on your behalf.
        - *Undefined* : By default, use an AWS owned KMS key.
        - *A valid symmetric customer managed KMS key* : Use the specified symmetric encryption KMS key in your account that you create, own, and manage.

        Amazon QLDB does not support asymmetric keys. For more information, see `Using symmetric and asymmetric keys <https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

        To specify a customer managed KMS key, you can use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. When using an alias name, prefix it with ``"alias/"`` . To specify a key in a different AWS account , you must use the key ARN or alias ARN.

        For example:

        - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab``
        - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``
        - Alias name: ``alias/ExampleAlias``
        - Alias ARN: ``arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias``

        For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-kmskey
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ledger that you want to create.

        The name must be unique among all of the ledgers in your AWS account in the current Region.

        Naming constraints for ledger names are defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLedgerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStream(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_qldb.CfnStream",
):
    '''A CloudFormation ``AWS::QLDB::Stream``.

    The ``AWS::QLDB::Stream`` resource specifies a journal stream for a given Amazon Quantum Ledger Database (Amazon QLDB) ledger. The stream captures every document revision that is committed to the ledger's journal and delivers the data to a specified Amazon Kinesis Data Streams resource.

    For more information, see `StreamJournalToKinesis <https://docs.aws.amazon.com/qldb/latest/developerguide/API_StreamJournalToKinesis.html>`_ in the *Amazon QLDB API Reference* .

    :cloudformationResource: AWS::QLDB::Stream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_qldb as qldb
        
        cfn_stream = qldb.CfnStream(self, "MyCfnStream",
            inclusive_start_time="inclusiveStartTime",
            kinesis_configuration=qldb.CfnStream.KinesisConfigurationProperty(
                aggregation_enabled=False,
                stream_arn="streamArn"
            ),
            ledger_name="ledgerName",
            role_arn="roleArn",
            stream_name="streamName",
        
            # the properties below are optional
            exclusive_end_time="exclusiveEndTime",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        inclusive_start_time: builtins.str,
        kinesis_configuration: typing.Union[typing.Union["CfnStream.KinesisConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ledger_name: builtins.str,
        role_arn: builtins.str,
        stream_name: builtins.str,
        exclusive_end_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::QLDB::Stream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param inclusive_start_time: The inclusive start date and time from which to start streaming journal data. This parameter must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` . The ``InclusiveStartTime`` cannot be in the future and must be before ``ExclusiveEndTime`` . If you provide an ``InclusiveStartTime`` that is before the ledger's ``CreationDateTime`` , QLDB effectively defaults it to the ledger's ``CreationDateTime`` .
        :param kinesis_configuration: The configuration settings of the Kinesis Data Streams destination for your stream request.
        :param ledger_name: The name of the ledger.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role that grants QLDB permissions for a journal stream to write data records to a Kinesis Data Streams resource. To pass a role to QLDB when requesting a journal stream, you must have permissions to perform the ``iam:PassRole`` action on the IAM role resource. This is required for all journal stream requests.
        :param stream_name: The name that you want to assign to the QLDB journal stream. User-defined names can help identify and indicate the purpose of a stream. Your stream name must be unique among other *active* streams for a given ledger. Stream names have the same naming constraints as ledger names, as defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .
        :param exclusive_end_time: The exclusive date and time that specifies when the stream ends. If you don't define this parameter, the stream runs indefinitely until you cancel it. The ``ExclusiveEndTime`` must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d938a088971e76c4921b1058100604a7d1ac1bbec784b1582a44848e7000122)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStreamProps(
            inclusive_start_time=inclusive_start_time,
            kinesis_configuration=kinesis_configuration,
            ledger_name=ledger_name,
            role_arn=role_arn,
            stream_name=stream_name,
            exclusive_end_time=exclusive_end_time,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b592d193cd33983ae30b2d4d4229468330e346acb0f697a82af2c39834a46a2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e4b14d1110488613e40e53a7d00c9513d94162542ba33c523e7c4b58effed46)
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
        '''The Amazon Resource Name (ARN) of the QLDB journal stream.

        For example: ``arn:aws:qldb:us-east-1:123456789012:stream/exampleLedger/IiPT4brpZCqCq3f4MTHbYy`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique ID that QLDB assigns to each QLDB journal stream.

        For example: ``IiPT4brpZCqCq3f4MTHbYy`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="inclusiveStartTime")
    def inclusive_start_time(self) -> builtins.str:
        '''The inclusive start date and time from which to start streaming journal data.

        This parameter must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .

        The ``InclusiveStartTime`` cannot be in the future and must be before ``ExclusiveEndTime`` .

        If you provide an ``InclusiveStartTime`` that is before the ledger's ``CreationDateTime`` , QLDB effectively defaults it to the ledger's ``CreationDateTime`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-inclusivestarttime
        '''
        return typing.cast(builtins.str, jsii.get(self, "inclusiveStartTime"))

    @inclusive_start_time.setter
    def inclusive_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f326f580e14358615c7c19ac0985bbc06e081f2f96d35e6b234b1fa0fac40fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inclusiveStartTime", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisConfiguration")
    def kinesis_configuration(
        self,
    ) -> typing.Union["CfnStream.KinesisConfigurationProperty", _IResolvable_a771d0ef]:
        '''The configuration settings of the Kinesis Data Streams destination for your stream request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-kinesisconfiguration
        '''
        return typing.cast(typing.Union["CfnStream.KinesisConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "kinesisConfiguration"))

    @kinesis_configuration.setter
    def kinesis_configuration(
        self,
        value: typing.Union["CfnStream.KinesisConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50dd32d8f68dd72cfb73950508e2a2d6f2b8f97ef7560631226d4ca3f3729895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="ledgerName")
    def ledger_name(self) -> builtins.str:
        '''The name of the ledger.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-ledgername
        '''
        return typing.cast(builtins.str, jsii.get(self, "ledgerName"))

    @ledger_name.setter
    def ledger_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6428bcc424116d47d3d6bea5c54c60ec77004e8bf6f24bd3814844849d11c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ledgerName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role that grants QLDB permissions for a journal stream to write data records to a Kinesis Data Streams resource.

        To pass a role to QLDB when requesting a journal stream, you must have permissions to perform the ``iam:PassRole`` action on the IAM role resource. This is required for all journal stream requests.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2be5edca9ece5f45b943172fb2eedba190dcaa28a45249734c291429daf6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        '''The name that you want to assign to the QLDB journal stream.

        User-defined names can help identify and indicate the purpose of a stream.

        Your stream name must be unique among other *active* streams for a given ledger. Stream names have the same naming constraints as ledger names, as defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-streamname
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0804998e4ba726bc6e3d921a192b61f7d609a3257771ef9bac198ad25eea50ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value)

    @builtins.property
    @jsii.member(jsii_name="exclusiveEndTime")
    def exclusive_end_time(self) -> typing.Optional[builtins.str]:
        '''The exclusive date and time that specifies when the stream ends.

        If you don't define this parameter, the stream runs indefinitely until you cancel it.

        The ``ExclusiveEndTime`` must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-exclusiveendtime
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exclusiveEndTime"))

    @exclusive_end_time.setter
    def exclusive_end_time(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97bf85f2816ec727928ce6a9ab06dc20470ee62552c7c4d11cede6bb1f271563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusiveEndTime", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_qldb.CfnStream.KinesisConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_enabled": "aggregationEnabled",
            "stream_arn": "streamArn",
        },
    )
    class KinesisConfigurationProperty:
        def __init__(
            self,
            *,
            aggregation_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            stream_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings of the Amazon Kinesis Data Streams destination for an Amazon QLDB journal stream.

            :param aggregation_enabled: Enables QLDB to publish multiple data records in a single Kinesis Data Streams record, increasing the number of records sent per API call. Default: ``True`` .. epigraph:: Record aggregation has important implications for processing records and requires de-aggregation in your stream consumer. To learn more, see `KPL Key Concepts <https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-concepts.html>`_ and `Consumer De-aggregation <https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-consumer-deaggregation.html>`_ in the *Amazon Kinesis Data Streams Developer Guide* .
            :param stream_arn: The Amazon Resource Name (ARN) of the Kinesis Data Streams resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qldb-stream-kinesisconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_qldb as qldb
                
                kinesis_configuration_property = qldb.CfnStream.KinesisConfigurationProperty(
                    aggregation_enabled=False,
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2a801cbdb86f81dfc7c1b380aa01d0d1e9bc166356b235cf58ba3c511fa60c9)
                check_type(argname="argument aggregation_enabled", value=aggregation_enabled, expected_type=type_hints["aggregation_enabled"])
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation_enabled is not None:
                self._values["aggregation_enabled"] = aggregation_enabled
            if stream_arn is not None:
                self._values["stream_arn"] = stream_arn

        @builtins.property
        def aggregation_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Enables QLDB to publish multiple data records in a single Kinesis Data Streams record, increasing the number of records sent per API call.

            Default: ``True``
            .. epigraph::

               Record aggregation has important implications for processing records and requires de-aggregation in your stream consumer. To learn more, see `KPL Key Concepts <https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-concepts.html>`_ and `Consumer De-aggregation <https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-consumer-deaggregation.html>`_ in the *Amazon Kinesis Data Streams Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qldb-stream-kinesisconfiguration.html#cfn-qldb-stream-kinesisconfiguration-aggregationenabled
            '''
            result = self._values.get("aggregation_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def stream_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Kinesis Data Streams resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qldb-stream-kinesisconfiguration.html#cfn-qldb-stream-kinesisconfiguration-streamarn
            '''
            result = self._values.get("stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_qldb.CfnStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "inclusive_start_time": "inclusiveStartTime",
        "kinesis_configuration": "kinesisConfiguration",
        "ledger_name": "ledgerName",
        "role_arn": "roleArn",
        "stream_name": "streamName",
        "exclusive_end_time": "exclusiveEndTime",
        "tags": "tags",
    },
)
class CfnStreamProps:
    def __init__(
        self,
        *,
        inclusive_start_time: builtins.str,
        kinesis_configuration: typing.Union[typing.Union[CfnStream.KinesisConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ledger_name: builtins.str,
        role_arn: builtins.str,
        stream_name: builtins.str,
        exclusive_end_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStream``.

        :param inclusive_start_time: The inclusive start date and time from which to start streaming journal data. This parameter must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` . The ``InclusiveStartTime`` cannot be in the future and must be before ``ExclusiveEndTime`` . If you provide an ``InclusiveStartTime`` that is before the ledger's ``CreationDateTime`` , QLDB effectively defaults it to the ledger's ``CreationDateTime`` .
        :param kinesis_configuration: The configuration settings of the Kinesis Data Streams destination for your stream request.
        :param ledger_name: The name of the ledger.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role that grants QLDB permissions for a journal stream to write data records to a Kinesis Data Streams resource. To pass a role to QLDB when requesting a journal stream, you must have permissions to perform the ``iam:PassRole`` action on the IAM role resource. This is required for all journal stream requests.
        :param stream_name: The name that you want to assign to the QLDB journal stream. User-defined names can help identify and indicate the purpose of a stream. Your stream name must be unique among other *active* streams for a given ledger. Stream names have the same naming constraints as ledger names, as defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .
        :param exclusive_end_time: The exclusive date and time that specifies when the stream ends. If you don't define this parameter, the stream runs indefinitely until you cancel it. The ``ExclusiveEndTime`` must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_qldb as qldb
            
            cfn_stream_props = qldb.CfnStreamProps(
                inclusive_start_time="inclusiveStartTime",
                kinesis_configuration=qldb.CfnStream.KinesisConfigurationProperty(
                    aggregation_enabled=False,
                    stream_arn="streamArn"
                ),
                ledger_name="ledgerName",
                role_arn="roleArn",
                stream_name="streamName",
            
                # the properties below are optional
                exclusive_end_time="exclusiveEndTime",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1302652314c2198327e5f577c4fd9b9183fc2edf666120424573af8e88d384)
            check_type(argname="argument inclusive_start_time", value=inclusive_start_time, expected_type=type_hints["inclusive_start_time"])
            check_type(argname="argument kinesis_configuration", value=kinesis_configuration, expected_type=type_hints["kinesis_configuration"])
            check_type(argname="argument ledger_name", value=ledger_name, expected_type=type_hints["ledger_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument exclusive_end_time", value=exclusive_end_time, expected_type=type_hints["exclusive_end_time"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "inclusive_start_time": inclusive_start_time,
            "kinesis_configuration": kinesis_configuration,
            "ledger_name": ledger_name,
            "role_arn": role_arn,
            "stream_name": stream_name,
        }
        if exclusive_end_time is not None:
            self._values["exclusive_end_time"] = exclusive_end_time
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def inclusive_start_time(self) -> builtins.str:
        '''The inclusive start date and time from which to start streaming journal data.

        This parameter must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .

        The ``InclusiveStartTime`` cannot be in the future and must be before ``ExclusiveEndTime`` .

        If you provide an ``InclusiveStartTime`` that is before the ledger's ``CreationDateTime`` , QLDB effectively defaults it to the ledger's ``CreationDateTime`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-inclusivestarttime
        '''
        result = self._values.get("inclusive_start_time")
        assert result is not None, "Required property 'inclusive_start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kinesis_configuration(
        self,
    ) -> typing.Union[CfnStream.KinesisConfigurationProperty, _IResolvable_a771d0ef]:
        '''The configuration settings of the Kinesis Data Streams destination for your stream request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-kinesisconfiguration
        '''
        result = self._values.get("kinesis_configuration")
        assert result is not None, "Required property 'kinesis_configuration' is missing"
        return typing.cast(typing.Union[CfnStream.KinesisConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def ledger_name(self) -> builtins.str:
        '''The name of the ledger.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-ledgername
        '''
        result = self._values.get("ledger_name")
        assert result is not None, "Required property 'ledger_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role that grants QLDB permissions for a journal stream to write data records to a Kinesis Data Streams resource.

        To pass a role to QLDB when requesting a journal stream, you must have permissions to perform the ``iam:PassRole`` action on the IAM role resource. This is required for all journal stream requests.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_name(self) -> builtins.str:
        '''The name that you want to assign to the QLDB journal stream.

        User-defined names can help identify and indicate the purpose of a stream.

        Your stream name must be unique among other *active* streams for a given ledger. Stream names have the same naming constraints as ledger names, as defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-streamname
        '''
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclusive_end_time(self) -> typing.Optional[builtins.str]:
        '''The exclusive date and time that specifies when the stream ends.

        If you don't define this parameter, the stream runs indefinitely until you cancel it.

        The ``ExclusiveEndTime`` must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-exclusiveendtime
        '''
        result = self._values.get("exclusive_end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLedger",
    "CfnLedgerProps",
    "CfnStream",
    "CfnStreamProps",
]

publication.publish()

def _typecheckingstub__970cff924d6fb5dcd5e22d16660e973e31d588be7c40b2edc2862613767aee75(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    permissions_mode: builtins.str,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a0aa067d365e16d9b4399209f3eb7d8c399a4f065b0c225db447ddf9a65a8e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9240029664025ad9734bca068c8191e9bb06a20e94cc623cdb188d943b739fe9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5155d59953c1330619e26c320be67d95d4717dcaa93a5a8897c4e63ba238a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a0defd0b06fa9a060becf3c260ad8e1de0739a1ed071bdb45994796d84b007(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9637776850095a3b8e82739e01c453d618bdb174a075ada3777fe1b53c4fbbed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2878f1010ee198cf4445275a213e206ce984c4afe0ddea0c00d1409addd5e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cab1894b3432ea7571f97e9ae6a6ccdf31ec25c5bf9fcca3354c88dc3d7c37c(
    *,
    permissions_mode: builtins.str,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d938a088971e76c4921b1058100604a7d1ac1bbec784b1582a44848e7000122(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    inclusive_start_time: builtins.str,
    kinesis_configuration: typing.Union[typing.Union[CfnStream.KinesisConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    ledger_name: builtins.str,
    role_arn: builtins.str,
    stream_name: builtins.str,
    exclusive_end_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b592d193cd33983ae30b2d4d4229468330e346acb0f697a82af2c39834a46a2b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4b14d1110488613e40e53a7d00c9513d94162542ba33c523e7c4b58effed46(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f326f580e14358615c7c19ac0985bbc06e081f2f96d35e6b234b1fa0fac40fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50dd32d8f68dd72cfb73950508e2a2d6f2b8f97ef7560631226d4ca3f3729895(
    value: typing.Union[CfnStream.KinesisConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6428bcc424116d47d3d6bea5c54c60ec77004e8bf6f24bd3814844849d11c02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2be5edca9ece5f45b943172fb2eedba190dcaa28a45249734c291429daf6d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0804998e4ba726bc6e3d921a192b61f7d609a3257771ef9bac198ad25eea50ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bf85f2816ec727928ce6a9ab06dc20470ee62552c7c4d11cede6bb1f271563(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a801cbdb86f81dfc7c1b380aa01d0d1e9bc166356b235cf58ba3c511fa60c9(
    *,
    aggregation_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1302652314c2198327e5f577c4fd9b9183fc2edf666120424573af8e88d384(
    *,
    inclusive_start_time: builtins.str,
    kinesis_configuration: typing.Union[typing.Union[CfnStream.KinesisConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    ledger_name: builtins.str,
    role_arn: builtins.str,
    stream_name: builtins.str,
    exclusive_end_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
